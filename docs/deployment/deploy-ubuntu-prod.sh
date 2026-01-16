#!/bin/bash
################################################################################
# Feature 007: GWT Navigation Analysis and Error Fixes
# Production Deployment Script for Ubuntu
#
# This script guides you through deploying and running the codebase analysis
# pipeline on Ubuntu in production.
#
# Prerequisites:
# - Ubuntu 20.04+ (tested on 22.04)
# - Sudo access
# - Internet connection
# - At least 8GB RAM, 20GB disk space
#
# Usage:
#   chmod +x deploy-ubuntu-prod.sh
#   ./deploy-ubuntu-prod.sh
################################################################################

set -e  # Exit on error
set -u  # Exit on undefined variable

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on Ubuntu
check_ubuntu() {
    log_info "Checking OS compatibility..."
    if [ ! -f /etc/lsb-release ]; then
        log_error "This script is designed for Ubuntu. Please adapt for your OS."
        exit 1
    fi

    source /etc/lsb-release
    log_success "Running on Ubuntu ${DISTRIB_RELEASE}"
}

# Install system dependencies
install_system_deps() {
    log_info "Installing system dependencies..."

    sudo apt-get update
    sudo apt-get install -y \
        python3 \
        python3-pip \
        python3-venv \
        git \
        curl \
        docker.io \
        docker-compose \
        openjdk-11-jdk \
        maven

    # Add user to docker group
    sudo usermod -aG docker $USER

    log_success "System dependencies installed"
    log_warn "You may need to log out and back in for docker group changes to take effect"
}

# Install Ollama
install_ollama() {
    log_info "Installing Ollama (Local LLM service)..."

    if command -v ollama &> /dev/null; then
        log_success "Ollama already installed"
        return 0
    fi

    # Install Ollama
    curl -fsSL https://ollama.com/install.sh | sh

    # Start Ollama service
    sudo systemctl enable ollama
    sudo systemctl start ollama

    # Wait for Ollama to start
    sleep 5

    # Pull required model
    log_info "Pulling gemma3:12b model (this may take 10-15 minutes)..."
    ollama pull gemma3:12b

    log_success "Ollama installed and gemma3:12b model downloaded"
}

# Setup Weaviate
setup_weaviate() {
    log_info "Setting up Weaviate vector database..."

    # Check if Weaviate is already running
    if docker ps | grep -q weaviate-i19; then
        log_warn "Weaviate container already running"
        read -p "Stop and recreate? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker stop weaviate-i19 && docker rm weaviate-i19
        else
            log_success "Using existing Weaviate container"
            return 0
        fi
    fi

    # Start Weaviate using the project script
    log_info "Starting Weaviate with Ubuntu configuration..."
    ./docker-weaviate.sh start ubuntu

    # Wait for Weaviate to be ready
    log_info "Waiting for Weaviate to be ready..."
    for i in {1..30}; do
        if curl -sf http://localhost:8080/v1/meta > /dev/null 2>&1; then
            log_success "Weaviate is ready"
            return 0
        fi
        sleep 2
    done

    log_error "Weaviate failed to start within 60 seconds"
    exit 1
}

# Setup Python virtual environment
setup_python_env() {
    log_info "Setting up Python virtual environment..."

    # Create virtual environment
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
        log_success "Virtual environment created"
    else
        log_warn "Virtual environment already exists"
    fi

    # Activate virtual environment
    source .venv/bin/activate

    # Upgrade pip
    pip install --upgrade pip

    # Install dependencies
    log_info "Installing Python dependencies..."
    pip install -r requirements.txt

    # Install package in development mode
    pip install -e .

    log_success "Python environment configured"
}

# Create .env file
create_env_file() {
    log_info "Creating .env configuration file..."

    if [ -f ".env" ]; then
        log_warn ".env file already exists"
        read -p "Overwrite? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_info "Keeping existing .env file"
            return 0
        fi
    fi

    # Prompt for Java source directory
    read -p "Enter path to Java source directory (absolute path): " JAVA_SOURCE_DIR

    # Validate path exists
    if [ ! -d "$JAVA_SOURCE_DIR" ]; then
        log_error "Directory does not exist: $JAVA_SOURCE_DIR"
        exit 1
    fi

    # Create .env file
    cat > .env << EOF
# Java Source Directory (REQUIRED)
JAVA_SOURCE_DIR=$JAVA_SOURCE_DIR

# Weaviate Configuration
WEAVIATE_URL=http://localhost:8080

# Ollama Configuration
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL_NAME=gemma3:12b
OLLAMA_CONNECT_TIMEOUT=10
OLLAMA_READ_TIMEOUT=600

# Performance Tuning
MAX_CONCURRENT_AI_CALLS=10
BATCH_SIZE=50

# Logging
LOG_LEVEL=INFO

# Output Directory
OUTPUT_DIR=./output
EOF

    log_success ".env file created"
}

# Verify services are running
verify_services() {
    log_info "Verifying services..."

    # Check Ollama
    if ! curl -sf http://localhost:11434/api/tags > /dev/null 2>&1; then
        log_error "Ollama is not responding on http://localhost:11434"
        exit 1
    fi
    log_success "✓ Ollama is running"

    # Check Weaviate
    if ! curl -sf http://localhost:8080/v1/meta > /dev/null 2>&1; then
        log_error "Weaviate is not responding on http://localhost:8080"
        exit 1
    fi
    log_success "✓ Weaviate is running"

    # Check Python environment
    if [ ! -f ".venv/bin/python" ]; then
        log_error "Python virtual environment not found"
        exit 1
    fi
    log_success "✓ Python environment ready"
}

# Run the pipeline
run_pipeline() {
    log_info "Running analysis pipeline..."

    # Activate virtual environment
    source .venv/bin/activate

    # Load environment variables
    source .env

    # Create output directory
    mkdir -p ./output

    echo ""
    log_info "=========================================="
    log_info "STEP 1: DISCOVER FILES"
    log_info "=========================================="
    codeindex discover \
        --source-dir "$JAVA_SOURCE_DIR" \
        --output ./output/discovery-inventory.jsonl

    echo ""
    log_info "=========================================="
    log_info "STEP 2: EXTRACT METADATA"
    log_info "=========================================="
    codeindex extract \
        --inventory ./output/discovery-inventory.jsonl \
        --output ./output/extraction-results.jsonl

    echo ""
    log_info "=========================================="
    log_info "STEP 3: INDEX TO WEAVIATE"
    log_info "=========================================="
    codeindex index \
        --inventory ./output/discovery-inventory.jsonl \
        --extraction ./output/extraction-results.jsonl

    echo ""
    log_info "=========================================="
    log_info "STEP 4: DISPLAY STATUS"
    log_info "=========================================="
    codeindex status

    log_success "Pipeline completed successfully!"

    echo ""
    log_info "=========================================="
    log_info "NEXT STEPS"
    log_info "=========================================="
    echo "1. Search indexed code:"
    echo "   codeindex search \"your search query\""
    echo ""
    echo "2. Generate PRD documents:"
    echo "   codeindex prd backend --output-dir ./output/prd"
    echo "   codeindex prd frontend --output-dir ./output/prd"
    echo ""
    echo "3. Generate architecture diagrams:"
    echo "   codeindex diagram component --output ./output"
    echo "   codeindex diagram gwt --output ./output"
    echo ""
    echo "4. View Weaviate statistics:"
    echo "   python3 weaviate_stats.py"
}

# Main installation flow
main() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║  Feature 007: Production Deployment for Ubuntu            ║"
    echo "║  GWT Navigation Analysis and Error Fixes                  ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""

    # Check if running from project root
    if [ ! -f "setup.py" ] || [ ! -f "docker-weaviate.sh" ]; then
        log_error "Please run this script from the project root directory"
        exit 1
    fi

    # Prompt for installation mode
    echo "Select installation mode:"
    echo "1) Full installation (install all dependencies + run pipeline)"
    echo "2) Setup only (install dependencies, don't run pipeline)"
    echo "3) Run pipeline only (assumes dependencies already installed)"
    echo "4) Verify installation only"
    read -p "Enter choice [1-4]: " -n 1 -r
    echo ""

    case $REPLY in
        1)
            log_info "Starting full installation..."
            check_ubuntu
            install_system_deps
            install_ollama
            setup_weaviate
            setup_python_env
            create_env_file
            verify_services
            run_pipeline
            ;;
        2)
            log_info "Starting setup only..."
            check_ubuntu
            install_system_deps
            install_ollama
            setup_weaviate
            setup_python_env
            create_env_file
            verify_services
            log_success "Setup complete! Run './deploy-ubuntu-prod.sh' and select option 3 to run the pipeline."
            ;;
        3)
            log_info "Running pipeline only..."
            verify_services
            run_pipeline
            ;;
        4)
            log_info "Verifying installation..."
            verify_services
            log_success "All services are running correctly!"
            ;;
        *)
            log_error "Invalid choice"
            exit 1
            ;;
    esac

    echo ""
    log_success "╔════════════════════════════════════════════════════════════╗"
    log_success "║  Deployment Complete!                                      ║"
    log_success "╚════════════════════════════════════════════════════════════╝"
}

# Run main function
main
