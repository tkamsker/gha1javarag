#!/bin/bash
# ==============================================================================
# Java Codebase Indexer - Full Pipeline Runner
# ==============================================================================
# Usage: ./run.sh [project-name]
# Runs the complete pipeline: discover -> extract -> index -> status

set -e  # Exit on error

# Colors for output
BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m'

info() { echo -e "${BLUE}[INFO]${NC} $1"; }
ok() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }

# Check if virtual environment exists
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found. Run ./step1.sh first."
    exit 1
fi

# Activate virtual environment
source $VENV_DIR/bin/activate

# Determine project filter (optional)
PROJECT_FILTER=""
if [ -n "$1" ]; then
    PROJECT_FILTER="--project $1"
    info "Running pipeline for project: $1"
else
    info "Running pipeline for all projects"
fi

echo "=============================================="
echo "Java Codebase Indexer - Full Pipeline"
echo "=============================================="
echo ""

# Step 1: Discover
info "Step 1: Discovering Maven projects..."
codeindex discover $PROJECT_FILTER
ok "Discovery complete"
echo ""

# Step 2: Extract
info "Step 2: Extracting semantic understanding..."
INVENTORY_FILE="./output/discovery-inventory.jsonl"
EXTRACTION_FILE="./output/extraction-results.jsonl"

if [ ! -f "$INVENTORY_FILE" ]; then
    echo "ERROR: Discovery inventory not found at $INVENTORY_FILE"
    echo "Run discover command first or check --output path"
    exit 1
fi

codeindex extract --inventory "$INVENTORY_FILE" --output "$EXTRACTION_FILE" $PROJECT_FILTER
ok "Extraction complete"
echo ""

# Step 3: Index
info "Step 3: Indexing to Weaviate..."
if [ ! -f "$EXTRACTION_FILE" ]; then
    echo "ERROR: Extraction results not found at $EXTRACTION_FILE"
    exit 1
fi

codeindex index --inventory "$INVENTORY_FILE" --extraction "$EXTRACTION_FILE" $PROJECT_FILTER
ok "Indexing complete"
echo ""

# Step 4: Status
info "Step 4: Checking status..."
codeindex status $PROJECT_FILTER
ok "Pipeline complete"
echo ""

echo "=============================================="
ok "Full pipeline finished!"
echo "=============================================="
