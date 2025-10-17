#!/bin/bash

# =============================
# Virtual Environment Setup Script
# =============================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Check if Python 3 is available
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed"
        exit 1
    fi
    print_success "Python 3 found"
}

# Create virtual environment
create_venv() {
    print_info "Creating virtual environment..."
    
    if [ -d "venv" ]; then
        print_warning "Virtual environment already exists"
        read -p "Do you want to recreate it? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_info "Removing existing virtual environment..."
            rm -rf venv
        else
            print_info "Using existing virtual environment"
            return 0
        fi
    fi
    
    python3 -m venv venv
    print_success "Virtual environment created"
}

# Activate virtual environment and install dependencies
setup_venv() {
    print_info "Activating virtual environment and installing dependencies..."
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    print_info "Upgrading pip..."
    pip install --upgrade pip
    
    # Install essential build tools
    print_info "Installing essential build tools..."
    pip install setuptools wheel
    
    # Install dependencies
    print_info "Installing Python dependencies..."
    pip install -r requirements.txt
    
    print_success "Dependencies installed successfully"
}

# Show activation instructions
show_activation_instructions() {
    print_success "Virtual environment setup complete!"
    echo ""
    print_info "To activate the virtual environment, run:"
    echo "  source venv/bin/activate"
    echo ""
    print_info "To deactivate the virtual environment, run:"
    echo "  deactivate"
    echo ""
    print_info "After activation, you can run the pipeline:"
    echo "  ./run_iteration17b.sh your-project true"
}

# Main execution
main() {
    echo "=========================================="
    echo "Virtual Environment Setup"
    echo "=========================================="
    
    check_python
    create_venv
    setup_venv
    show_activation_instructions
}

# Handle script arguments
case "${1:-}" in
    "help"|"--help"|"-h")
        echo "Usage: $0 [help]"
        echo ""
        echo "This script sets up a Python virtual environment for the Java/JSP/GWT/JS → PRD pipeline."
        echo ""
        echo "Arguments:"
        echo "  help, --help, -h    Show this help message"
        echo ""
        echo "After running this script:"
        echo "  1. Activate the virtual environment: source venv/bin/activate"
        echo "  2. Run the pipeline: ./run_iteration17b.sh your-project true"
        ;;
    *)
        main
        ;;
esac
