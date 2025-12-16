#!/bin/bash
# ==============================================================================
# cuco-ui-admin Pipeline Runner
# ==============================================================================
# Dedicated script for analyzing the cuco-ui-admin codebase
# This script can be run in a separate terminal while you work on other tasks
#
# Usage: ./run-cuco.sh [source-dir]
#
# Examples:
#   ./run-cuco.sh                                    # Use JAVA_SOURCE_DIR from .env
#   ./run-cuco.sh /path/to/cuco-ui-admin             # Specify source directory

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

# Project configuration
PROJECT_NAME="cuco-ui-admin"

# ==============================================================================
# Environment Setup
# ==============================================================================

# Check if virtual environment exists
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    err "Virtual environment not found. Please run:"
    echo "  python -m venv .venv"
    echo "  source .venv/bin/activate"
    echo "  pip install -e ."
    exit 1
fi

# Activate virtual environment
source $VENV_DIR/bin/activate

# Load .env for JAVA_SOURCE_DIR
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
fi

# ==============================================================================
# Source Directory Setup
# ==============================================================================

# Get source directory (argument or from .env)
if [ -n "$1" ]; then
    SOURCE_DIR="$1"
elif [ -n "$JAVA_SOURCE_DIR" ]; then
    SOURCE_DIR="$JAVA_SOURCE_DIR"
else
    err "Source directory not specified!"
    echo "Either provide it as argument or set JAVA_SOURCE_DIR in .env"
    echo "Usage: ./run-cuco.sh [source-dir]"
    exit 1
fi

# Verify source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    err "Source directory does not exist: $SOURCE_DIR"
    exit 1
fi

# Verify it looks like cuco-ui-admin (check for pom.xml)
if [ ! -f "$SOURCE_DIR/pom.xml" ]; then
    warn "No pom.xml found in $SOURCE_DIR"
    warn "Are you sure this is the cuco-ui-admin project?"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        info "Aborted"
        exit 0
    fi
fi

# ==============================================================================
# Pre-flight Checks
# ==============================================================================

info "Checking services..."

# Check if Weaviate is running
if ! curl -s http://localhost:8080/v1/meta > /dev/null 2>&1; then
    err "Weaviate is not running!"
    echo "Please start Weaviate first:"
    echo "  ./docker-weaviate.sh start"
    exit 1
fi
ok "Weaviate is running"

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    err "Ollama is not running!"
    echo "Please start Ollama first:"
    echo "  ollama serve"
    exit 1
fi
ok "Ollama is running"

# ==============================================================================
# Pipeline Execution
# ==============================================================================

# Define file paths for pipeline artifacts
DISCOVERY_FILE="data/discovery-${PROJECT_NAME}.jsonl"
EXTRACTION_FILE="data/extraction-${PROJECT_NAME}.jsonl"

# Create data directory if it doesn't exist
mkdir -p data

echo ""
echo "=============================================="
echo "cuco-ui-admin Pipeline Runner"
echo "=============================================="
echo "Project:    $PROJECT_NAME"
echo "Source:     $SOURCE_DIR"
echo "Artifacts:  data/"
echo "=============================================="
echo ""

# Confirm before starting
read -p "Start pipeline? This may take a while for large codebases. (Y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Nn]$ ]]; then
    info "Aborted"
    exit 0
fi

# Record start time
START_TIME=$(date +%s)

# Step 1: Discover
info "Step 1: Discovering source files and resolving dependencies..."
# Feature 005: Enable sibling dependency search with auto-detected workspace root
WORKSPACE_ROOT=$(dirname "$SOURCE_DIR")
echo "Command: codeindex discover --source-dir \"$SOURCE_DIR\" --output \"$DISCOVERY_FILE\" --dependency-depth 1 --workspace-root \"$WORKSPACE_ROOT\""
codeindex discover --source-dir "$SOURCE_DIR" --output "$DISCOVERY_FILE" --dependency-depth 1 --workspace-root "$WORKSPACE_ROOT"
ok "Discovery complete"
echo ""

# Step 2: Extract
info "Step 2: Extracting semantic information with AI..."
warn "This step may take 10-30 minutes depending on codebase size..."
echo "Command: codeindex extract --inventory \"$DISCOVERY_FILE\" --output \"$EXTRACTION_FILE\""
codeindex extract --inventory "$DISCOVERY_FILE" --output "$EXTRACTION_FILE"
ok "Extraction complete"
echo ""

# Step 3: Index
info "Step 3: Indexing artifacts in Weaviate..."
echo "Command: codeindex index --inventory \"$DISCOVERY_FILE\" --extraction \"$EXTRACTION_FILE\" --create-schema"
codeindex index --inventory "$DISCOVERY_FILE" --extraction "$EXTRACTION_FILE" --create-schema
ok "Indexing complete"
echo ""

# Step 4: Status
info "Step 4: Checking indexing status..."
echo "Command: codeindex status"
codeindex status
ok "Status check complete"
echo ""

# ==============================================================================
# Summary
# ==============================================================================

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
MINUTES=$((DURATION / 60))
SECONDS=$((DURATION % 60))

echo "=============================================="
ok "cuco-ui-admin Pipeline Complete!"
echo "=============================================="
echo ""
echo "Pipeline Results:"
echo "  Project:    $PROJECT_NAME"
echo "  Source:     $SOURCE_DIR"
echo "  Discovery:  $DISCOVERY_FILE"
echo "  Extraction: $EXTRACTION_FILE"
echo "  Duration:   ${MINUTES}m ${SECONDS}s"
echo ""
echo "Next steps:"
echo "  1. Search your codebase:"
echo "     codeindex search \"your query\""
echo ""
echo "  2. Search with project filter:"
echo "     codeindex search \"user authentication\" --project cuco-ui-admin"
echo ""
echo "  3. View indexing status:"
echo "     codeindex status"
echo ""
echo "  4. Generate PRD documentation:"
echo "     codeindex prd frontend --output-dir ./output/cuco-prd"
echo "     codeindex prd backend --output-dir ./output/cuco-prd"
echo ""
echo "=============================================="
