#!/bin/bash
# ==============================================================================
# Java Codebase Indexer - Full Pipeline Runner (Updated)
# ==============================================================================
# Usage: ./run.sh [project-name] [source-dir]
#
# Project name determination (in priority order):
#   1. If provided as first argument, use it
#   2. If source-dir contains pom.xml, use directory name
#   3. Otherwise use timestamp: YYYY_MMM_DD_HHMM
#
# Source directory determination:
#   1. If provided as second argument, use it
#   2. Otherwise use JAVA_SOURCE_DIR from .env
#
# Examples:
#   ./run.sh myapp                    # Uses JAVA_SOURCE_DIR from .env
#   ./run.sh myapp /path/to/source    # Explicit source dir
#   ./run.sh                          # Auto-detect everything

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

# Load .env for JAVA_SOURCE_DIR
if [ ! -f ".env" ]; then
    warn ".env file not found. JAVA_SOURCE_DIR must be provided as argument."
else
    # Load .env
    export $(grep -v '^#' .env | xargs)
fi

# ==============================================================================
# Parse Arguments and Determine Project Name
# ==============================================================================

# Get source directory (argument or from .env)
if [ -n "$2" ]; then
    SOURCE_DIR="$2"
elif [ -n "$JAVA_SOURCE_DIR" ]; then
    SOURCE_DIR="$JAVA_SOURCE_DIR"
else
    err "Source directory not specified!"
    echo "Either provide it as second argument or set JAVA_SOURCE_DIR in .env"
    echo "Usage: ./run.sh [project-name] [source-dir]"
    exit 1
fi

# Verify source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    err "Source directory does not exist: $SOURCE_DIR"
    exit 1
fi

# Determine project name
if [ -n "$1" ]; then
    # Project name provided as argument
    PROJECT_NAME="$1"
    info "Using provided project name: $PROJECT_NAME"
else
    # Auto-detect project name
    info "No project name provided, auto-detecting..."

    # Check if source directory contains pom.xml
    if [ -f "$SOURCE_DIR/pom.xml" ]; then
        # Use directory name as project name
        PROJECT_NAME=$(basename "$SOURCE_DIR")
        ok "Found pom.xml, using directory name: $PROJECT_NAME"
    else
        # Use timestamp as project name
        PROJECT_NAME=$(date +"%Y_%b_%d_%H%M" | tr '[:upper:]' '[:lower:]')
        warn "No pom.xml found, using timestamp: $PROJECT_NAME"
    fi
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
echo "     ./step2.sh $PROJECT_NAME"
echo "     # or with explicit source:"
echo "     ./step2.sh $PROJECT_NAME \"$SOURCE_DIR\""
echo ""
echo "=============================================="
