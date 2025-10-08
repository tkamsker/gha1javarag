#!/bin/bash

# =============================
# Java/JSP/GWT/JS → PRD Pipeline
# =============================
# Main script for running the complete iteration17b pipeline

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="${1:-default-project}"
INCLUDE_FRONTEND="${2:-true}"

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

# Check if Python is available
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed"
        exit 1
    fi
    print_success "Python 3 found"
}

# Check if required Python packages are installed
check_dependencies() {
    print_info "Checking Python dependencies..."
    
    # Check if we're in a virtual environment
    if [ -n "$VIRTUAL_ENV" ]; then
        print_info "Virtual environment detected: $VIRTUAL_ENV"
        PYTHON_CMD="python"
        PIP_CMD="pip"
    else
        print_warning "No virtual environment detected. Please activate your virtual environment first:"
        echo "  python -m venv venv"
        echo "  source venv/bin/activate  # On macOS/Linux"
        echo "  # or"
        echo "  venv\\Scripts\\activate  # On Windows"
        exit 1
    fi
    
    if ! $PYTHON_CMD -c "import weaviate, javalang, lxml, esprima, beautifulsoup4, click, rich" 2>/dev/null; then
        print_warning "Some Python dependencies are missing. Installing..."
        $PIP_CMD install -r requirements.txt
    fi
    
    print_success "Python dependencies checked"
}

# Check if Weaviate is running
check_weaviate() {
    print_info "Checking Weaviate connection..."
    
    if ! curl -s http://localhost:8080/v1/meta > /dev/null 2>&1; then
        print_error "Weaviate is not running. Please start it first:"
        echo "  ./docker-weaviate.sh"
        exit 1
    fi
    
    print_success "Weaviate is running"
}

# Check if Ollama is running
check_ollama() {
    print_info "Checking Ollama connection..."
    
    if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        print_warning "Ollama is not running. Some features may not work properly."
        print_info "To start Ollama:"
        echo "  ollama serve"
        echo "  ollama pull <model_from_env>"
        echo "  ollama pull nomic-embed-text"
    else
        print_success "Ollama is running"
    fi
}

# Validate Java source directory
validate_java_source() {
    JAVA_SOURCE_DIR=$(grep "^JAVA_SOURCE_DIR=" .env | cut -d'=' -f2)
    
    if [ "$JAVA_SOURCE_DIR" = "/path/to/java/source" ] || [ ! -d "$JAVA_SOURCE_DIR" ]; then
        print_error "JAVA_SOURCE_DIR is not set or directory does not exist"
        print_info "Please update .env file with the correct Java source directory:"
        echo "  JAVA_SOURCE_DIR=/path/to/your/java/source"
        exit 1
    fi
    
    print_success "Java source directory validated: $JAVA_SOURCE_DIR"
}

# Run the complete pipeline
run_pipeline() {
    print_info "Starting iteration17b pipeline for project: $PROJECT_NAME"
    
    cd "$SCRIPT_DIR"
    
    # Step 1: Discover files
    print_info "Step 1: Discovering files..."
    $PYTHON_CMD main.py discover --project "$PROJECT_NAME" --include-frontend
    
    # Step 2: Extract artifacts
    print_info "Step 2: Extracting artifacts..."
    if [ "$INCLUDE_FRONTEND" = "true" ]; then
        $PYTHON_CMD main.py extract --project "$PROJECT_NAME" --include-frontend
    else
        $PYTHON_CMD main.py extract --project "$PROJECT_NAME"
    fi
    
    # Step 3: Index in Weaviate
    print_info "Step 3: Indexing artifacts in Weaviate..."
    $PYTHON_CMD main.py index --project "$PROJECT_NAME"
    
    # Step 4: Generate PRD
    print_info "Step 4: Generating PRD..."
    if [ "$INCLUDE_FRONTEND" = "true" ]; then
        $PYTHON_CMD main.py prd --project "$PROJECT_NAME" --frontend
    else
        $PYTHON_CMD main.py prd --project "$PROJECT_NAME"
    fi
    
    print_success "Pipeline completed successfully!"
}

# Show usage
show_usage() {
    echo "Usage: $0 [PROJECT_NAME] [INCLUDE_FRONTEND]"
    echo ""
    echo "Arguments:"
    echo "  PROJECT_NAME      Name of the project (default: default-project)"
    echo "  INCLUDE_FRONTEND  Include frontend extraction (default: true)"
    echo ""
    echo "Examples:"
    echo "  $0 my-project true    # Run with frontend extraction"
    echo "  $0 my-project false   # Run without frontend extraction"
    echo "  $0                    # Use defaults"
    echo ""
    echo "Prerequisites:"
    echo "  1. Weaviate running (./docker-weaviate.sh)"
    echo "  2. Ollama running (optional, for LLM features)"
    echo "  3. JAVA_SOURCE_DIR set in .env file"
    echo "  4. Python virtual environment activated (recommended)"
}

# Main execution
main() {
    echo "=========================================="
    echo "Java/JSP/GWT/JS → PRD Pipeline (iteration17b)"
    echo "=========================================="
    
    # Parse arguments
    if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
        show_usage
        exit 0
    fi
    
    # Run checks
    check_python
    check_dependencies
    check_weaviate
    check_ollama
    validate_java_source
    
    # Run pipeline
    run_pipeline
    
    echo ""
    print_success "Pipeline completed! Check the following outputs:"
    echo "  - Build artifacts: ./data/build/"
    echo "  - PRD document: ./data/output/${PROJECT_NAME}_prd.md"
    echo "  - Weaviate data: ./weaviate-data/"
}

# Handle script arguments
case "${1:-}" in
    "help"|"--help"|"-h")
        show_usage
        ;;
    "check")
        print_info "Running system checks..."
        check_python
        check_dependencies
        check_weaviate
        check_ollama
        validate_java_source
        print_success "All checks passed!"
        ;;
    "clean")
        print_info "Cleaning build artifacts..."
        rm -rf data/build/*
        rm -rf data/output/*
        print_success "Build artifacts cleaned"
        ;;
    *)
        main "$@"
        ;;
esac
