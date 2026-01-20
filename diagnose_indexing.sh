#!/bin/bash
# ==============================================================================
# Diagnostic Script for Code Indexing Issues
# ==============================================================================
# This script helps diagnose why projects show 0 artifacts in Weaviate
# Usage: ./diagnose_indexing.sh <project-name> <source-directory>
#
# Example: ./diagnose_indexing.sh cuco-ui-admin /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c

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
    err "Usage: ./diagnose_indexing.sh <project-name> <source-directory>"
    echo ""
    echo "Example:"
    echo "  ./diagnose_indexing.sh cuco-ui-admin /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-admin"
    exit 1
fi

PROJECT_NAME="$1"
SOURCE_DIR="$2"

echo ""
echo "=============================================="
echo "Indexing Diagnostic Tool"
echo "=============================================="
echo "Project:    $PROJECT_NAME"
echo "Source:     $SOURCE_DIR"
echo "=============================================="
echo ""

# ==============================================================================
# Step 1: Check Source Directory
# ==============================================================================

info "Step 1: Checking source directory..."

if [ ! -d "$SOURCE_DIR" ]; then
    err "Source directory does not exist: $SOURCE_DIR"
    echo ""
    echo "Possible fixes:"
    echo "  1. Verify the path is correct"
    echo "  2. Check if you're on the correct machine (Linux vs macOS)"
    echo "  3. Ensure the directory is mounted"
    exit 1
else
    ok "Source directory exists"
fi

# Check if it contains pom.xml
if [ -f "$SOURCE_DIR/pom.xml" ]; then
    ok "Found pom.xml (Maven project detected)"
else
    warn "No pom.xml found in root (may not be a Maven project)"
fi

# Count Java files
JAVA_COUNT=$(find "$SOURCE_DIR" -name "*.java" -type f 2>/dev/null | wc -l | tr -d ' ')
JSP_COUNT=$(find "$SOURCE_DIR" -name "*.jsp" -type f 2>/dev/null | wc -l | tr -d ' ')
XML_COUNT=$(find "$SOURCE_DIR" -name "*.xml" -type f 2>/dev/null | wc -l | tr -d ' ')

echo "  Java files: $JAVA_COUNT"
echo "  JSP files:  $JSP_COUNT"
echo "  XML files:  $XML_COUNT"

if [ "$JAVA_COUNT" -eq 0 ] && [ "$JSP_COUNT" -eq 0 ]; then
    err "No Java or JSP files found! Directory may be empty or wrong."
    exit 1
fi

echo ""

# ==============================================================================
# Step 2: Check Pipeline Artifacts
# ==============================================================================

info "Step 2: Checking pipeline artifacts..."

DISCOVERY_FILE="data/discovery-${PROJECT_NAME}.jsonl"
EXTRACTION_FILE="data/extraction-${PROJECT_NAME}.jsonl"

# Check discovery file
if [ -f "$DISCOVERY_FILE" ]; then
    ok "Discovery file exists: $DISCOVERY_FILE"
    DISCOVERY_SIZE=$(wc -l < "$DISCOVERY_FILE" | tr -d ' ')
    echo "  Lines in discovery file: $DISCOVERY_SIZE"

    if [ "$DISCOVERY_SIZE" -eq 0 ]; then
        err "Discovery file is empty!"
    fi
else
    warn "Discovery file does not exist: $DISCOVERY_FILE"
    echo "  This means discovery stage hasn't run or failed"
fi

echo ""

# Check extraction file
if [ -f "$EXTRACTION_FILE" ]; then
    ok "Extraction file exists: $EXTRACTION_FILE"
    EXTRACTION_SIZE=$(wc -l < "$EXTRACTION_FILE" | tr -d ' ')
    echo "  Lines in extraction file: $EXTRACTION_SIZE"

    if [ "$EXTRACTION_SIZE" -eq 0 ]; then
        err "Extraction file is empty!"
    fi
else
    warn "Extraction file does not exist: $EXTRACTION_FILE"
    echo "  This means extraction stage hasn't run or failed"
fi

echo ""

# ==============================================================================
# Step 3: Check Weaviate Connection
# ==============================================================================

info "Step 3: Checking Weaviate connection..."

if curl -s -f http://localhost:8080/v1/meta > /dev/null 2>&1; then
    ok "Weaviate is accessible at http://localhost:8080"
else
    err "Cannot connect to Weaviate at http://localhost:8080"
    echo ""
    echo "Possible fixes:"
    echo "  1. Start Weaviate: ./docker-weaviate.sh start"
    echo "  2. Check Docker is running: docker ps"
    exit 1
fi

echo ""

# ==============================================================================
# Step 4: Check Ollama Connection
# ==============================================================================

info "Step 4: Checking Ollama connection..."

if curl -s -f http://localhost:11434/api/tags > /dev/null 2>&1; then
    ok "Ollama is accessible at http://localhost:11434"
else
    err "Cannot connect to Ollama at http://localhost:11434"
    echo ""
    echo "Possible fixes:"
    echo "  1. Start Ollama: ollama serve"
    echo "  2. Check Ollama is installed: ollama list"
    exit 1
fi

echo ""

# ==============================================================================
# Step 5: Check for Recent Logs
# ==============================================================================

info "Step 5: Checking for recent log files..."

LOG_FILES=$(find . -maxdepth 1 -name "log_run_*.log" -type f -mtime -1 2>/dev/null)

if [ -n "$LOG_FILES" ]; then
    ok "Found recent log files:"
    echo "$LOG_FILES" | while read -r log; do
        echo "  - $log"

        # Check for errors in log
        if grep -qi "error\|exception\|failed" "$log" 2>/dev/null; then
            warn "Errors found in $log (showing last 10 lines):"
            tail -10 "$log" | sed 's/^/    /'
        fi
    done
else
    warn "No recent log files found in current directory"
fi

echo ""

# ==============================================================================
# Step 6: Check Weaviate Data
# ==============================================================================

info "Step 6: Checking Weaviate for project data..."

source .venv/bin/activate 2>/dev/null || true

# Try to get status for this specific project
PROJECT_STATUS=$(codeindex status 2>/dev/null | grep -A5 "Name: $PROJECT_NAME" || echo "")

if [ -n "$PROJECT_STATUS" ]; then
    ok "Project found in Weaviate:"
    echo "$PROJECT_STATUS" | sed 's/^/  /'

    # Extract artifact count
    ARTIFACT_COUNT=$(echo "$PROJECT_STATUS" | grep "Artifacts:" | head -1 | awk '{print $2}')

    if [ "$ARTIFACT_COUNT" = "0" ]; then
        err "Project has 0 artifacts indexed!"
        echo ""
        echo "This means indexing stage failed or indexed empty data"
    fi
else
    warn "Project '$PROJECT_NAME' not found in Weaviate"
fi

echo ""

# ==============================================================================
# Summary and Recommendations
# ==============================================================================

echo "=============================================="
echo "Diagnostic Summary"
echo "=============================================="
echo ""

if [ -f "$DISCOVERY_FILE" ] && [ -f "$EXTRACTION_FILE" ]; then
    ok "All pipeline files exist"
    echo ""
    echo "Next steps:"
    echo "  1. Re-run indexing to update Weaviate:"
    echo "     ./fix_indexing.sh $PROJECT_NAME $SOURCE_DIR"
    echo ""
    echo "  2. Or run full pipeline:"
    echo "     ./run.sh $PROJECT_NAME $SOURCE_DIR"
else
    warn "Pipeline files are missing or incomplete"
    echo ""
    echo "Recommended action:"
    echo "  Run the full pipeline with correct syntax:"
    echo "     ./run.sh $PROJECT_NAME $SOURCE_DIR"
    echo ""
    echo "  Or use the fix script:"
    echo "     ./fix_indexing.sh $PROJECT_NAME $SOURCE_DIR"
fi

echo ""
echo "=============================================="
