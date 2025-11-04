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
    elif [[ "$OSTYPE" == "linux-gnu"* ]] || [[ -f /etc/os-release ]] && grep -q "Ubuntu" /etc/os-release; then
        echo "linux"
    elif [[ -f /etc/os-release ]] && grep -q "Ubuntu" /etc/os-release; then
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

# Function to get Docker Compose command
get_docker_compose_cmd() {
    # Prefer docker compose (plugin), fallback to docker-compose (standalone)
    if command -v docker >/dev/null 2>&1; then
        if docker compose version >/dev/null 2>&1; then
            echo "docker compose"
            return
        fi
    fi
    if command -v docker-compose >/dev/null 2>&1; then
        echo "docker-compose"
        return
    fi
    err "Neither 'docker compose' nor 'docker-compose' found"
    exit 1
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [COMMAND] [OS]"
    echo ""
    echo "Commands:"
    echo "  start     Start Weaviate container"
    echo "  stop      Stop Weaviate container"
    echo "  restart   Restart Weaviate container"
    echo "  clean     Stop container and remove data"
    echo "  status    Show container status"
    echo "  logs      Show container logs"
    echo ""
    echo "OS Options (optional):"
    echo "  macos     Force macOS configuration"
    echo "  ubuntu    Force Ubuntu/Linux configuration"
    echo "  auto      Auto-detect OS (default)"
    echo ""
    echo "Examples:"
    echo "  $0 start                    # Auto-detect OS"
    echo "  $0 start ubuntu             # Force Ubuntu config"
    echo "  $0 start macos              # Force macOS config"
    echo ""
    echo "Current Environment:"
    echo "  Detected OS: $(detect_os)"
    echo "  Compose file: $(get_compose_file)"
}

# Main script logic
COMMAND="${1:-start}"
FORCE_OS="${2:-auto}"

# Function to get compose file with manual override
get_compose_file_with_override() {
    local os
    if [[ "$FORCE_OS" == "auto" ]]; then
        os=$(detect_os)
    else
        os="$FORCE_OS"
    fi
    
    case $os in
        "macos")
            echo "docker-compose.macos.yml"
            ;;
        "ubuntu"|"linux")
            echo "docker-compose.ubuntu.yml"
            ;;
        *)
            echo "docker-compose.yml"
            ;;
    esac
}

case "$COMMAND" in
    "start")
        info "Starting Weaviate container..."
        os=""
        if [[ "$FORCE_OS" == "auto" ]]; then
            os=$(detect_os)
            info "Auto-detected OS: $os"
        else
            os="$FORCE_OS"
            info "Forced OS: $os"
        fi
        COMPOSE_FILE=$(get_compose_file_with_override)
        info "Using Docker Compose file: $COMPOSE_FILE"
        
        # Check if Ollama is running
        if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
            warn "Ollama is not running on localhost:11434"
            echo "Please start Ollama first: ollama serve"
            exit 1
        fi
        
        $(get_docker_compose_cmd) -f "$COMPOSE_FILE" up -d weaviate
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
        COMPOSE_FILE=$(get_compose_file_with_override)
        $(get_docker_compose_cmd) -f "$COMPOSE_FILE" down
        ok "Weaviate container stopped"
        ;;
        
    "restart")
        info "Restarting Weaviate container..."
        $0 stop "$FORCE_OS"
        sleep 2
        $0 start "$FORCE_OS"
        ;;
        
    "clean")
        warn "This will stop Weaviate and remove all data!"
        read -p "Are you sure? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            info "Stopping Weaviate container..."
            COMPOSE_FILE=$(get_compose_file_with_override)
            $(get_docker_compose_cmd) -f "$COMPOSE_FILE" down
            
            info "Removing Weaviate data..."
            rm -rf weaviate-data/*
            
            ok "Weaviate data cleaned"
        else
            info "Clean operation cancelled"
        fi
        ;;
        
    "status")
        info "Weaviate container status:"
        if docker ps | grep -q weaviate-i17; then
            ok "Weaviate container is running"
            docker ps | grep weaviate-i17
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
        docker logs weaviate-i17
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