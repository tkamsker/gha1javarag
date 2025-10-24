#!/bin/bash

# =============================
# Docker Weaviate Management Script
# Automatically detects OS and uses appropriate Docker Compose file
# =============================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info(){ echo -e "${BLUE}[INFO]${NC} $1"; }
ok(){ echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warn(){ echo -e "${YELLOW}[WARNING]${NC} $1"; }
err(){ echo -e "${RED}[ERROR]${NC} $1"; }

# Function to detect OS
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    else
        echo "unknown"
    fi
}

# Function to get appropriate Docker Compose file
get_compose_file() {
    local os=$(detect_os)
    case $os in
        "macos")
            echo "docker-compose.macos.yml"
            ;;
        "linux")
            echo "docker-compose.ubuntu.yml"
            ;;
        *)
            echo "docker-compose.yml"
            ;;
    esac
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start     Start Weaviate container"
    echo "  stop      Stop Weaviate container"
    echo "  restart   Restart Weaviate container"
    echo "  clean     Stop container and remove data"
    echo "  status    Show container status"
    echo "  logs      Show container logs"
    echo ""
    echo "Environment:"
    echo "  OS: $(detect_os)"
    echo "  Compose file: $(get_compose_file)"
}

# Main script logic
case "${1:-start}" in
    "start")
        info "Starting Weaviate container..."
        COMPOSE_FILE=$(get_compose_file)
        info "Using Docker Compose file: $COMPOSE_FILE"
        
        # Check if Ollama is running
        if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
            warn "Ollama is not running on localhost:11434"
            echo "Please start Ollama first: ollama serve"
            exit 1
        fi
        
        docker-compose -f "$COMPOSE_FILE" up -d weaviate
        ok "Weaviate container started"
        
        # Wait for Weaviate to be ready
        info "Waiting for Weaviate to be ready..."
        sleep 10
        
        # Test connection
        if curl -s http://localhost:8080/v1/meta > /dev/null 2>&1; then
            ok "Weaviate is ready and accessible"
        else
            warn "Weaviate may not be ready yet, check logs with: $0 logs"
        fi
        ;;
        
    "stop")
        info "Stopping Weaviate container..."
        COMPOSE_FILE=$(get_compose_file)
        docker-compose -f "$COMPOSE_FILE" down
        ok "Weaviate container stopped"
        ;;
        
    "restart")
        info "Restarting Weaviate container..."
        $0 stop
        sleep 2
        $0 start
        ;;
        
    "clean")
        warn "This will stop Weaviate and remove all data!"
        read -p "Are you sure? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            info "Stopping Weaviate container..."
            COMPOSE_FILE=$(get_compose_file)
            docker-compose -f "$COMPOSE_FILE" down
            
            info "Removing Weaviate data..."
            rm -rf weaviate-data/*
            
            ok "Weaviate data cleaned"
        else
            info "Clean operation cancelled"
        fi
        ;;
        
    "status")
        info "Weaviate container status:"
        if docker ps | grep -q weaviate-java-analysis; then
            ok "Weaviate container is running"
            docker ps | grep weaviate-java-analysis
        else
            warn "Weaviate container is not running"
        fi
        
        echo ""
        info "Weaviate API status:"
        if curl -s http://localhost:8080/v1/meta > /dev/null 2>&1; then
            ok "Weaviate API is accessible"
        else
            warn "Weaviate API is not accessible"
        fi
        
        echo ""
        info "Ollama status:"
        if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
            ok "Ollama is accessible"
        else
            warn "Ollama is not accessible"
        fi
        ;;
        
    "logs")
        info "Showing Weaviate container logs..."
        docker logs weaviate-java-analysis
        ;;
        
    "help"|"-h"|"--help")
        show_usage
        ;;
        
    *)
        err "Unknown command: $1"
        show_usage
        exit 1
        ;;
esac