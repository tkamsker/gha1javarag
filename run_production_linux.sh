#!/bin/bash
# Quick-start script for running full iteration on Linux production

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info(){ echo -e "${BLUE}[INFO]${NC} $1"; }
ok(){ echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warn(){ echo -e "${YELLOW}[WARNING]${NC} $1"; }
err(){ echo -e "${RED}[ERROR]${NC} $1"; }

# Default values
PROJECT_NAME="${1:-production-project}"
INCLUDE_FRONTEND="${2:-true}"

info "Starting production iteration for project: $PROJECT_NAME"
info "Include frontend: $INCLUDE_FRONTEND"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    err "Virtual environment not found. Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Get script directory and ensure we're in the right place
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment
info "Activating virtual environment..."
source venv/bin/activate

# Ensure we're using the venv's Python
PYTHON_CMD="$(which python)"
info "Using Python: $PYTHON_CMD"

# Set PYTHONPATH to include src directory
export PYTHONPATH="${SCRIPT_DIR}/src:${PYTHONPATH:-}"

# Check if .env exists
if [ ! -f ".env" ]; then
    warn ".env file not found. Please create it from .env.example"
    exit 1
fi

# Verify src directory structure
info "Verifying project structure..."
info "Current directory: $(pwd)"
info "Script directory: $SCRIPT_DIR"

if [ ! -d "src" ]; then
    err "src/ directory not found in $(pwd)"
    err "Please ensure you're running this script from the project root directory"
    exit 1
fi

if [ ! -d "src/store" ]; then
    err "src/store/ directory not found"
    info "Contents of src/:"
    ls -la src/ 2>/dev/null || err "Cannot list src/ directory"
    exit 1
fi

if [ ! -f "src/store/weaviate_client.py" ]; then
    err "src/store/weaviate_client.py not found"
    info "Contents of src/store/:"
    ls -la src/store/ 2>/dev/null || err "Cannot list src/store/ directory"
    err ""
    err "Missing required files. Please ensure all project files are synced:"
    err "  - If using git: git pull"
    err "  - If using scp: sync the entire project directory"
    err "  - Required file: src/store/weaviate_client.py"
    exit 1
fi

if [ ! -f "main.py" ]; then
    err "main.py not found in project root"
    exit 1
fi

ok "Project structure verified"

# Verify critical packages are installed
info "Verifying Python packages..."
if ! "$PYTHON_CMD" -c "import weaviate" 2>/dev/null; then
    err "weaviate-client not installed. Run: pip install -r requirements.txt"
    exit 1
fi
if ! "$PYTHON_CMD" -c "import click" 2>/dev/null; then
    err "click not installed. Run: pip install -r requirements.txt"
    exit 1
fi
ok "Required packages are installed"

# Check services
info "Checking services..."

# Check Ollama
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    err "Ollama is not running on localhost:11434"
    err "Please start Ollama: ollama serve"
    exit 1
fi
ok "Ollama is running"

# Check Weaviate
if ! curl -s http://localhost:8080/v1/meta > /dev/null 2>&1; then
    warn "Weaviate is not running. Starting Weaviate..."
    ./docker-weaviate.sh start ubuntu
    sleep 10
    if ! curl -s http://localhost:8080/v1/meta > /dev/null 2>&1; then
        err "Failed to start Weaviate"
        exit 1
    fi
fi
ok "Weaviate is running"

# Run the pipeline
info "Running complete pipeline..."

if [ "$INCLUDE_FRONTEND" = "true" ]; then
    "$PYTHON_CMD" main.py all --project "$PROJECT_NAME" --include-frontend
else
    "$PYTHON_CMD" main.py all --project "$PROJECT_NAME"
fi

if [ $? -eq 0 ]; then
    ok "Pipeline completed successfully!"
    info "Output files:"
    ls -lh data/output/"${PROJECT_NAME}"_prd.md 2>/dev/null || warn "PRD file not found"
else
    err "Pipeline failed. Check logs above."
    exit 1
fi

