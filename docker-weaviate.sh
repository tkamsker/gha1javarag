#!/bin/bash

# =============================
# Weaviate Docker Setup Script
# =============================
# This script sets up Weaviate with the required modules for Java codebase analysis

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
WEAVIATE_IMAGE="semitechnologies/weaviate:latest"
CONTAINER_NAME="weaviate-java-analysis"
HOST_PORT="8080"
GRPC_PORT="50051"
DATA_DIR="./weaviate-data"

# Functions
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    print_success "Docker is running"
}

# Stop and remove existing container
cleanup_existing() {
    if docker ps -a --format "table {{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
        print_info "Stopping existing Weaviate container..."
        docker stop ${CONTAINER_NAME} > /dev/null 2>&1 || true
        docker rm ${CONTAINER_NAME} > /dev/null 2>&1 || true
        print_success "Existing container removed"
    fi
}

# Create data directory
create_data_dir() {
    if [ ! -d "$DATA_DIR" ]; then
        print_info "Creating data directory: $DATA_DIR"
        mkdir -p "$DATA_DIR"
        print_success "Data directory created"
    else
        print_info "Using existing data directory: $DATA_DIR"
    fi
}

# Pull Weaviate image
pull_image() {
    print_info "Pulling Weaviate image..."
    docker pull ${WEAVIATE_IMAGE}
    print_success "Weaviate image pulled"
}

# Run Weaviate container
run_weaviate() {
    print_info "Starting Weaviate container with required modules..."
    
    docker run -d \
        --name ${CONTAINER_NAME} \
        -p ${HOST_PORT}:8080 \
        -p ${GRPC_PORT}:50051 \
        -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
        -e PERSISTENCE_DATA_PATH='/var/lib/weaviate' \
        -e ENABLE_MODULES='text2vec-ollama,generative-ollama' \
        -e CLUSTER_HOSTNAME='node1' \
        -e OLLAMA_API_ENDPOINT='http://host.docker.internal:11434' \
        -e DEFAULT_VECTORIZER_MODULE='text2vec-ollama' \
        -e ENABLE_CORS=true \
        -e CORS_ALLOWED_ORIGINS='*' \
        -v "$(pwd)/${DATA_DIR}":/var/lib/weaviate \
        --restart unless-stopped \
        ${WEAVIATE_IMAGE}
    
    print_success "Weaviate container started"
}

# Wait for Weaviate to be ready
wait_for_weaviate() {
    print_info "Waiting for Weaviate to be ready..."
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:${HOST_PORT}/v1/meta > /dev/null 2>&1; then
            print_success "Weaviate is ready!"
            return 0
        fi
        
        print_info "Attempt $attempt/$max_attempts - waiting for Weaviate..."
        sleep 2
        ((attempt++))
    done
    
    print_error "Weaviate failed to start within expected time"
    return 1
}

# Verify modules
verify_modules() {
    print_info "Verifying Weaviate modules..."
    
    local response=$(curl -s http://localhost:${HOST_PORT}/v1/meta)
    
    if echo "$response" | grep -q "text2vec-ollama"; then
        print_success "text2vec-ollama module is available"
    else
        print_warning "text2vec-ollama module not found"
    fi
    
    if echo "$response" | grep -q "generative-ollama"; then
        print_success "generative-ollama module is available"
    else
        print_warning "generative-ollama module not found"
    fi
}

# Show container status
show_status() {
    print_info "Container status:"
    docker ps --filter "name=${CONTAINER_NAME}" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    
    print_info "Weaviate is available at:"
    echo "  - HTTP: http://localhost:${HOST_PORT}"
    echo "  - gRPC: localhost:${GRPC_PORT}"
    echo "  - Data: $(pwd)/${DATA_DIR}"
}

# Main execution
main() {
    echo "=========================================="
    echo "Weaviate Docker Setup for Java Analysis"
    echo "=========================================="
    
    check_docker
    cleanup_existing
    create_data_dir
    pull_image
    run_weaviate
    
    if wait_for_weaviate; then
        verify_modules
        show_status
        print_success "Weaviate is ready for Java codebase analysis!"
        echo ""
        print_info "You can now run: ./run_iteration.sh"
    else
        print_error "Failed to start Weaviate properly"
        exit 1
    fi
}

# Handle script arguments
case "${1:-}" in
    "stop")
        print_info "Stopping Weaviate container..."
        docker stop ${CONTAINER_NAME} > /dev/null 2>&1 || true
        print_success "Weaviate stopped"
        ;;
    "restart")
        print_info "Restarting Weaviate container..."
        docker restart ${CONTAINER_NAME} > /dev/null 2>&1 || true
        if wait_for_weaviate; then
            print_success "Weaviate restarted successfully"
        else
            print_error "Failed to restart Weaviate"
            exit 1
        fi
        ;;
    "status")
        show_status
        ;;
    "logs")
        docker logs ${CONTAINER_NAME}
        ;;
    "clean")
        print_info "Cleaning up Weaviate container and data..."
        docker stop ${CONTAINER_NAME} > /dev/null 2>&1 || true
        docker rm ${CONTAINER_NAME} > /dev/null 2>&1 || true
        rm -rf ${DATA_DIR}
        print_success "Cleanup completed"
        ;;
    *)
        main
        ;;
esac
