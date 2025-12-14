#!/bin/bash
# ==============================================================================
# Java Codebase Indexer - Full Pipeline Runner (Updated)
# ==============================================================================
# Usage: ./run.sh [project-name] [source-dir]
# Runs the complete pipeline: discover -> extract -> index -> status
#
# Examples:
#   ./run.sh myapp /path/to/source
#   ./run.sh myapp  # Uses JAVA_SOURCE_DIR from .env

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

info() { echo -e "${BLUE}[INFO]${NC} $1"; }
ok() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
err() { echo -e "${RED}[ERROR]${NC} $1"; }

# ==============================================================================
# Environment Setup
# ==============================================================================

# Check if virtual environment exists
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    err "Virtual environment not found. Run ./step1.sh first."
    exit 1
fi

# Activate virtual environment
source $VENV_DIR/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    warn ".env file not found. Using defaults."
else
    # Load .env for JAVA_SOURCE_DIR
    export $(grep -v '^#' .env | xargs)
fi

# ==============================================================================
# Parse Arguments
# ==============================================================================

PROJECT_NAME="${1:-}"
SOURCE_DIR="${2:-$JAVA_SOURCE_DIR}"

if [ -z "$PROJECT_NAME" ]; then
    err "Project name is required!"
    echo "Usage: ./run.sh [project-name] [source-dir]"
    echo "Example: ./run.sh myapp /path/to/source"
    exit 1
fi

if [ -z "$SOURCE_DIR" ]; then
    err "Source directory not specified!"
    echo "Either provide it as second argument or set JAVA_SOURCE_DIR in .env"
    exit 1
fi

if [ ! -d "$SOURCE_DIR" ]; then
    err "Source directory does not exist: $SOURCE_DIR"
    exit 1
fi

# ==============================================================================
# Pipeline Execution
# ==============================================================================

echo ""
echo "=============================================="
echo "Java Codebase Indexer - Full Pipeline"
echo "=============================================="
echo "Project:    $PROJECT_NAME"
echo "Source:     $SOURCE_DIR"
echo "=============================================="
echo ""

# Step 1: Discover
info "Step 1: Discovering source files..."
echo "Command: codeindex discover --source-dir \"$SOURCE_DIR\" --project \"$PROJECT_NAME\""
codeindex discover --source-dir "$SOURCE_DIR" --project "$PROJECT_NAME"
ok "Discovery complete"
echo ""

# Step 2: Extract
info "Step 2: Extracting semantic information with AI..."
echo "Command: codeindex extract --project \"$PROJECT_NAME\""
codeindex extract --project "$PROJECT_NAME"
ok "Extraction complete"
echo ""

# Step 3: Index
info "Step 3: Indexing artifacts in Weaviate..."
echo "Command: codeindex index --project \"$PROJECT_NAME\""
codeindex index --project "$PROJECT_NAME"
ok "Indexing complete"
echo ""

# Step 4: Status
info "Step 4: Checking indexing status..."
echo "Command: codeindex status --project \"$PROJECT_NAME\""
codeindex status --project "$PROJECT_NAME"
ok "Status check complete"
echo ""

# ==============================================================================
# Summary
# ==============================================================================

echo "=============================================="
ok "Full Pipeline Complete!"
echo "=============================================="
echo ""
echo "Pipeline Results:"
echo "  Project: $PROJECT_NAME"
echo "  Source:  $SOURCE_DIR"
echo ""
echo "Next steps:"
echo "  1. Search your codebase:"
echo "     codeindex search \"your query\" --project $PROJECT_NAME"
echo ""
echo "  2. Generate PRD documentation:"
echo "     ./step2.sh $PROJECT_NAME \"$SOURCE_DIR\""
echo "     or"
echo "     codeindex prd full --project $PROJECT_NAME --source-dir \"$SOURCE_DIR\""
echo ""
echo "=============================================="
