#!/bin/bash
# ==============================================================================
# Step 1: Virtual Environment Setup for Java Codebase Indexer Pipeline
# ==============================================================================
# This script sets up a Python virtual environment and installs dependencies
# Reusable - can be run multiple times safely

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions for colored output
info() { echo -e "${BLUE}[INFO]${NC} $1"; }
ok() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
err() { echo -e "${RED}[ERROR]${NC} $1"; }

echo "=============================================="
echo "Java Codebase Indexer - Setup (Step 1)"
echo "=============================================="
echo ""

# ==============================================================================
# Step 1: Check Python Version
# ==============================================================================

info "Checking Python version..."

# Try python3 first, then python
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    err "Python not found! Please install Python 3.8 or higher."
    exit 1
fi

# Get Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

info "Found: $PYTHON_CMD $PYTHON_VERSION"

# Check if version is 3.8+
if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    err "Python 3.8 or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi

ok "Python version is compatible"

# ==============================================================================
# Step 2: Create/Activate Virtual Environment
# ==============================================================================

VENV_DIR=".venv"

if [ -d "$VENV_DIR" ]; then
    warn "Virtual environment already exists at $VENV_DIR"
    info "Reusing existing virtual environment"
else
    info "Creating virtual environment at $VENV_DIR..."
    $PYTHON_CMD -m venv $VENV_DIR
    ok "Virtual environment created"
fi

# Activate virtual environment
info "Activating virtual environment..."
source $VENV_DIR/bin/activate

# Verify activation
if [ -z "$VIRTUAL_ENV" ]; then
    err "Failed to activate virtual environment"
    exit 1
fi

ok "Virtual environment activated: $VIRTUAL_ENV"

# ==============================================================================
# Step 3: Upgrade pip
# ==============================================================================

info "Upgrading pip to latest version..."
pip install --upgrade pip setuptools wheel --quiet
ok "pip upgraded"

# ==============================================================================
# Step 4: Install Dependencies
# ==============================================================================

if [ ! -f "requirements.txt" ]; then
    err "requirements.txt not found!"
    exit 1
fi

info "Installing dependencies from requirements.txt..."
pip install -r requirements.txt --quiet

ok "Dependencies installed"

# ==============================================================================
# Step 5: Install Package in Development Mode
# ==============================================================================

if [ ! -f "setup.py" ]; then
    err "setup.py not found!"
    exit 1
fi

info "Installing codeindex package in development mode..."
pip install -e . --quiet

ok "Package installed in development mode"

# ==============================================================================
# Step 6: Verify Installation
# ==============================================================================

info "Verifying installation..."

# Check if codeindex command is available
if ! command -v codeindex &> /dev/null; then
    err "codeindex command not found after installation!"
    exit 1
fi

# Test the CLI
CODEINDEX_VERSION=$(codeindex --version 2>&1 || echo "unknown")
ok "codeindex CLI is available"

# ==============================================================================
# Step 7: Check Configuration
# ==============================================================================

info "Checking configuration files..."

if [ -f ".env" ]; then
    ok ".env file exists"
else
    warn ".env file not found"
    if [ -f ".env.example" ]; then
        info "Copy .env.example to .env and configure your settings:"
        echo "  cp .env.example .env"
    fi
fi

# ==============================================================================
# Step 8: Summary
# ==============================================================================

echo ""
echo "=============================================="
ok "Setup Complete!"
echo "=============================================="
echo ""
echo "Virtual environment: $VIRTUAL_ENV"
echo "Python version: $PYTHON_VERSION"
echo "Installed packages:"
pip list --format=columns | grep -E "(click|weaviate|httpx|lxml|filelock|pytest)" || echo "  (dependencies installed)"
echo ""
echo "Next steps:"
echo "  1. Configure your .env file if not already done:"
echo "     cp .env.example .env"
echo "     # Edit .env with your settings (JAVA_SOURCE_DIR, etc.)"
echo ""
echo "  2. Verify services are running:"
echo "     ./docker-weaviate.sh status"
echo "     curl http://localhost:11434/api/tags  # Ollama"
echo ""
echo "  3. Test the CLI:"
echo "     codeindex --help"
echo "     codeindex discover --help"
echo ""
echo "  4. To activate this environment in a new shell:"
echo "     source .venv/bin/activate"
echo ""
echo "  5. To deactivate when done:"
echo "     deactivate"
echo ""
echo "=============================================="
