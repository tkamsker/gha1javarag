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

# Step 2: Extract (placeholder - will be implemented in Phase 4)
info "Step 2: Extracting semantic understanding..."
echo "  (To be implemented in Phase 4)"
# codeindex extract $PROJECT_FILTER
echo ""

# Step 3: Index (placeholder - will be implemented in Phase 5)
info "Step 3: Indexing to Weaviate..."
echo "  (To be implemented in Phase 5)"
# codeindex index $PROJECT_FILTER
echo ""

# Step 4: Status
info "Step 4: Checking status..."
codeindex status $PROJECT_FILTER
ok "Pipeline complete"
echo ""

echo "=============================================="
ok "Full pipeline finished!"
echo "=============================================="
