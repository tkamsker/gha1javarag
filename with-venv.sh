#!/bin/bash
# ==============================================================================
# Helper Script: Run Commands in Virtual Environment
# ==============================================================================
# Usage: ./with-venv.sh <command> [args...]
# Example: ./with-venv.sh codeindex --help
#          ./with-venv.sh pytest tests/unit/

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

err() { echo -e "${RED}[ERROR]${NC} $1" >&2; }

VENV_DIR=".venv"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    err "Virtual environment not found at $VENV_DIR"
    echo "Run ./step1.sh first to set up the environment"
    exit 1
fi

# Check if command provided
if [ $# -eq 0 ]; then
    err "No command provided"
    echo "Usage: $0 <command> [args...]"
    echo "Example: $0 codeindex --help"
    exit 1
fi

# Activate virtual environment and run command
source $VENV_DIR/bin/activate

# Run the command with all arguments
exec "$@"
