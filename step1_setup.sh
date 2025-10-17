#!/bin/bash

# =============================
# Step 1: Setup Script
# =============================
# This script prepares Weaviate, checks LLM availability, and enables vectorization

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
    exit 1
}

# Check if we're in a virtual environment
check_venv() {
    if [ -n "$VIRTUAL_ENV" ]; then
        print_info "Virtual environment detected: $VIRTUAL_ENV"
        PYTHON_CMD="$VIRTUAL_ENV/bin/python"
        PIP_CMD="$VIRTUAL_ENV/bin/pip"
    else
        print_warning "No virtual environment detected. Please activate your virtual environment first:"
        echo "  python -m venv venv"
        echo "  source venv/bin/activate  # On macOS/Linux"
        echo "  # or"
        echo "  venv\\Scripts\\activate  # On Windows"
        exit 1
    fi
}

# Check Python dependencies
check_python_deps() {
    print_info "Checking Python dependencies..."
    
    if ! $PYTHON_CMD -c "import weaviate, javalang, lxml, esprima, beautifulsoup4, click, rich, pydantic, pydantic_settings" 2>/dev/null; then
        print_warning "Some Python dependencies are missing. Installing..."
        $PIP_CMD install -r requirements.txt
    fi
    
    print_success "Python dependencies checked"
}

# Check if Ollama is running and has required models
check_ollama() {
    print_info "Checking Ollama availability..."
    
    if ! command -v ollama &> /dev/null; then
        print_error "Ollama is not installed. Please install Ollama first:"
        echo "  Visit: https://ollama.ai/download"
        exit 1
    fi
    
    # Check if Ollama is running
    if ! curl -s http://localhost:11434/api/tags &> /dev/null; then
        print_warning "Ollama is not running. Starting Ollama..."
        ollama serve &
        sleep 5
    fi
    
    # Get required models from .env
    print_info "Getting required models from .env configuration..."
    
    # Use Python to read the models from .env
    MODELS=$($PYTHON_CMD -c "
import sys
from pathlib import Path

# Add src to Python path (same as main.py)
src_path = Path('.').absolute() / 'src'
sys.path.insert(0, str(src_path))

from config.settings import settings
print(f'{settings.ollama_model_name} {settings.ollama_embed_model_name}')
")
    
    # Parse the models
    read -r MAIN_MODEL EMBED_MODEL <<< "$MODELS"
    
    print_info "Required models: $MAIN_MODEL, $EMBED_MODEL"
    
    # Check for main model
    if ! ollama list | grep -q "$MAIN_MODEL"; then
        print_warning "Model $MAIN_MODEL not found. Pulling..."
        ollama pull "$MAIN_MODEL"
    else
        print_success "Model $MAIN_MODEL is available"
    fi
    
    # Check for embedding model
    if ! ollama list | grep -q "$EMBED_MODEL"; then
        print_warning "Model $EMBED_MODEL not found. Pulling..."
        ollama pull "$EMBED_MODEL"
    else
        print_success "Model $EMBED_MODEL is available"
    fi
}

# Setup Weaviate with vectorization enabled
setup_weaviate() {
    print_info "Setting up Weaviate with vectorization..."
    
    # Start Weaviate if not running
    if ! curl -s http://localhost:8080/v1/meta &> /dev/null; then
        print_info "Starting Weaviate..."
        ./docker-weaviate.sh start
        sleep 10
    fi
    
    # Check Weaviate status
    if curl -s http://localhost:8080/v1/meta &> /dev/null; then
        print_success "Weaviate is running"
    else
        print_error "Failed to start Weaviate"
        exit 1
    fi
    
    # Update Weaviate client to enable vectorization
    print_info "Updating Weaviate configuration for vectorization..."
    
    # Create a temporary script to update the Weaviate client
    cat > temp_update_weaviate.py << 'EOF'
import sys
from pathlib import Path

# Add src to Python path (same as main.py)
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from store.weaviate_client import WeaviateClient

# Delete existing classes to recreate with vectorization
client = WeaviateClient(ensure_schema=False)
class_names = [
    "IbatisStatement", "DaoCall", "JspForm", "DbTable", "Flow", "Requirement",
    "GwtModule", "GwtUiBinder", "GwtActivityPlace", "GwtEndpoint", 
    "JsArtifact", "FrontendRoute"
]

for class_name in class_names:
    if client.client.schema.exists(class_name):
        print(f"Deleting class: {class_name}")
        client.client.schema.delete_class(class_name)

print("Classes deleted. Ready for recreation with vectorization.")
EOF
    
    $PYTHON_CMD temp_update_weaviate.py
    rm temp_update_weaviate.py
    
    print_success "Weaviate setup completed"
}

# Update Weaviate client configuration for vectorization
update_weaviate_config() {
    print_info "Updating Weaviate client configuration for vectorization..."
    
    # Update the Weaviate client to use Ollama vectorization
    cat > temp_update_config.py << 'EOF'
import sys
from pathlib import Path

# Add src to Python path (same as main.py)
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Read the current weaviate_client.py
with open('src/store/weaviate_client.py', 'r') as f:
    content = f.read()

# Replace vectorizer: "none" with Ollama vectorization
content = content.replace('"vectorizer": "none",', '"vectorizer": "text2vec-ollama",')

# Write back the updated content
with open('src/store/weaviate_client.py', 'w') as f:
    f.write(content)

print("Weaviate client configuration updated for vectorization")
EOF
    
    $PYTHON_CMD temp_update_config.py
    rm temp_update_config.py
    
    print_success "Weaviate client configuration updated"
}

# Test the setup
test_setup() {
    print_info "Testing the setup..."
    
    # Test Weaviate connection
    if $PYTHON_CMD -c "
import sys
from pathlib import Path

# Add src to Python path (same as main.py)
src_path = Path('.').absolute() / 'src'
sys.path.insert(0, str(src_path))

from store.weaviate_client import WeaviateClient
client = WeaviateClient(ensure_schema=False)
print('Weaviate connection: OK')
" 2>/dev/null; then
        print_success "Weaviate connection test passed"
    else
        print_error "Weaviate connection test failed"
        exit 1
    fi
    
    # Test Ollama connection
    if curl -s http://localhost:11434/api/tags &> /dev/null; then
        print_success "Ollama connection test passed"
    else
        print_error "Ollama connection test failed"
        exit 1
    fi
}

# Main execution
main() {
    echo "=========================================="
    echo "Step 1: Setup Script"
    echo "=========================================="
    
    check_venv
    check_python_deps
    check_ollama
    setup_weaviate
    update_weaviate_config
    test_setup
    
    print_success "Setup completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Run: ./step2_fetch.sh <project_name> <include_frontend>"
    echo "2. Example: ./step2_fetch.sh 20251008_1034 true"
    echo ""
    echo "Available commands:"
    echo "  ./step2_fetch.sh <project> <frontend>  - Run complete pipeline"
    echo "  python main.py discover --project <project> --include-frontend"
    echo "  python main.py extract --project <project> --include-frontend"
    echo "  python main.py index --project <project>"
    echo "  python main.py search --query <query> --project <project> --frontend"
    echo "  python main.py prd --project <project> --frontend"
}

main "$@"
