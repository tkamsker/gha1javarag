#!/bin/bash
# ==============================================================================
# Fix Script for Re-indexing Projects with 0 Artifacts
# ==============================================================================
# This script properly re-runs the indexing pipeline for a project
# Usage: ./fix_indexing.sh <project-name> <source-directory>
#
# Example: ./fix_indexing.sh cuco-ui-admin /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-admin

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info() { echo -e "${BLUE}[INFO]${NC} $1"; }
ok() { echo -e "${GREEN}[✓]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
err() { echo -e "${RED}[ERROR]${NC} $1"; }

# ==============================================================================
# Parse Arguments
# ==============================================================================

if [ -z "$1" ] || [ -z "$2" ]; then
    err "Usage: ./fix_indexing.sh <project-name> <source-directory>"
    echo ""
    echo "Example:"
    echo "  ./fix_indexing.sh cuco-ui-admin /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-admin"
    echo ""
    echo "This will:"
    echo "  1. Verify source directory exists"
    echo "  2. Run discovery stage"
    echo "  3. Run extraction stage (with AI semantic analysis)"
    echo "  4. Run indexing stage (update Weaviate)"
    echo "  5. Display status"
    exit 1
fi

PROJECT_NAME="$1"
SOURCE_DIR="$2"

# ==============================================================================
# Pre-flight Checks
# ==============================================================================

echo ""
echo "=============================================="
echo "Code Indexing Fix Script"
echo "=============================================="
echo "Project:    $PROJECT_NAME"
echo "Source:     $SOURCE_DIR"
echo "=============================================="
echo ""

# Check virtual environment
if [ ! -d ".venv" ]; then
    err "Virtual environment not found. Run: python -m venv .venv && source .venv/bin/activate && pip install -e ."
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Check source directory
if [ ! -d "$SOURCE_DIR" ]; then
    err "Source directory does not exist: $SOURCE_DIR"
    exit 1
else
    ok "Source directory exists"
fi

# Check services
info "Checking services..."

if ! curl -s -f http://localhost:8080/v1/meta > /dev/null 2>&1; then
    err "Weaviate is not running. Start it with: ./docker-weaviate.sh start"
    exit 1
else
    ok "Weaviate is running"
fi

if ! curl -s -f http://localhost:11434/api/tags > /dev/null 2>&1; then
    err "Ollama is not running. Start it with: ollama serve"
    exit 1
else
    ok "Ollama is running"
fi

echo ""

# ==============================================================================
# Pipeline Execution
# ==============================================================================

# Define file paths
DISCOVERY_FILE="data/discovery-${PROJECT_NAME}.jsonl"
EXTRACTION_FILE="data/extraction-${PROJECT_NAME}.jsonl"

# Ensure data directory exists
mkdir -p data

# Backup old files if they exist
if [ -f "$DISCOVERY_FILE" ]; then
    BACKUP_FILE="${DISCOVERY_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
    mv "$DISCOVERY_FILE" "$BACKUP_FILE"
    info "Backed up old discovery file to: $BACKUP_FILE"
fi

if [ -f "$EXTRACTION_FILE" ]; then
    BACKUP_FILE="${EXTRACTION_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
    mv "$EXTRACTION_FILE" "$BACKUP_FILE"
    info "Backed up old extraction file to: $BACKUP_FILE"
fi

echo ""

# ==============================================================================
# Step 1: Discovery
# ==============================================================================

info "Step 1/4: Running discovery..."
echo "Command: codeindex discover --source-dir \"$SOURCE_DIR\" --output \"$DISCOVERY_FILE\" --dependency-depth 1"
echo ""

if codeindex discover --source-dir "$SOURCE_DIR" --output "$DISCOVERY_FILE" --dependency-depth 1; then
    ok "Discovery completed"

    # Verify discovery file
    if [ -f "$DISCOVERY_FILE" ]; then
        LINES=$(wc -l < "$DISCOVERY_FILE" | tr -d ' ')
        echo "  Discovered artifacts: $LINES lines"

        if [ "$LINES" -eq 0 ]; then
            err "Discovery file is empty! No files were discovered."
            echo ""
            echo "Possible reasons:"
            echo "  1. Source directory is empty"
            echo "  2. No Java/JSP/XML files in directory"
            echo "  3. File permissions issue"
            exit 1
        fi
    else
        err "Discovery file was not created!"
        exit 1
    fi
else
    err "Discovery failed!"
    exit 1
fi

echo ""

# ==============================================================================
# Step 2: Extraction
# ==============================================================================

info "Step 2/4: Running extraction with AI semantic analysis..."
warn "This may take a while depending on file count and Ollama performance"
echo "Command: codeindex extract --inventory \"$DISCOVERY_FILE\" --output \"$EXTRACTION_FILE\""
echo ""

if codeindex extract --inventory "$DISCOVERY_FILE" --output "$EXTRACTION_FILE"; then
    ok "Extraction completed"

    # Verify extraction file
    if [ -f "$EXTRACTION_FILE" ]; then
        LINES=$(wc -l < "$EXTRACTION_FILE" | tr -d ' ')
        echo "  Extracted artifacts: $LINES lines"

        if [ "$LINES" -eq 0 ]; then
            err "Extraction file is empty! No artifacts were extracted."
            exit 1
        fi
    else
        err "Extraction file was not created!"
        exit 1
    fi
else
    err "Extraction failed!"
    exit 1
fi

echo ""

# ==============================================================================
# Step 3: Indexing
# ==============================================================================

info "Step 3/4: Indexing artifacts in Weaviate..."
echo "Command: codeindex index --inventory \"$DISCOVERY_FILE\" --extraction \"$EXTRACTION_FILE\" --create-schema"
echo ""

if codeindex index --inventory "$DISCOVERY_FILE" --extraction "$EXTRACTION_FILE" --create-schema; then
    ok "Indexing completed"
else
    err "Indexing failed!"
    exit 1
fi

echo ""

# ==============================================================================
# Step 4: Verification
# ==============================================================================

info "Step 4/4: Verifying indexed data..."
echo ""

codeindex status | grep -A10 "Name: $PROJECT_NAME" || warn "Project not found in status output"

echo ""

# ==============================================================================
# Summary
# ==============================================================================

echo "=============================================="
ok "Indexing Fix Complete!"
echo "=============================================="
echo ""
echo "Pipeline Results:"
echo "  Project:    $PROJECT_NAME"
echo "  Source:     $SOURCE_DIR"
echo "  Discovery:  $DISCOVERY_FILE"
echo "  Extraction: $EXTRACTION_FILE"
echo ""
echo "Next steps:"
echo "  1. Search your codebase:"
echo "     codeindex search \"your query\" --project $PROJECT_NAME"
echo ""
echo "  2. View full status:"
echo "     codeindex status"
echo ""
echo "  3. Generate PRD (if needed):"
echo "     codeindex prd --output-dir output/$PROJECT_NAME"
echo ""
echo "=============================================="
