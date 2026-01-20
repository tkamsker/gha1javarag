#!/bin/bash
# ==============================================================================
# Test Script for Indexing Fix Validation
# ==============================================================================
# This script validates that the indexing fix works correctly
# Usage: ./test_indexing_fix.sh <project-name> <source-directory>

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info() { echo -e "${BLUE}[INFO]${NC} $1"; }
ok() { echo -e "${GREEN}[✓ PASS]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
fail() { echo -e "${RED}[✗ FAIL]${NC} $1"; }

PASS_COUNT=0
FAIL_COUNT=0

pass_test() {
    ok "$1"
    PASS_COUNT=$((PASS_COUNT + 1))
}

fail_test() {
    fail "$1"
    FAIL_COUNT=$((FAIL_COUNT + 1))
}

# ==============================================================================
# Parse Arguments
# ==============================================================================

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: ./test_indexing_fix.sh <project-name> <source-directory>"
    echo ""
    echo "Example:"
    echo "  ./test_indexing_fix.sh cuco-ui-admin /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-admin"
    exit 1
fi

PROJECT_NAME="$1"
SOURCE_DIR="$2"

echo ""
echo "=============================================="
echo "Indexing Fix Validation Tests"
echo "=============================================="
echo "Project:    $PROJECT_NAME"
echo "Source:     $SOURCE_DIR"
echo "=============================================="
echo ""

# Activate virtual environment
source .venv/bin/activate 2>/dev/null || true

# Define file paths
DISCOVERY_FILE="data/discovery-${PROJECT_NAME}.jsonl"
EXTRACTION_FILE="data/extraction-${PROJECT_NAME}.jsonl"

# ==============================================================================
# Test 1: Source Directory Exists
# ==============================================================================

info "Test 1: Source directory validation"

if [ -d "$SOURCE_DIR" ]; then
    pass_test "Source directory exists: $SOURCE_DIR"
else
    fail_test "Source directory does not exist: $SOURCE_DIR"
fi

# ==============================================================================
# Test 2: Discovery File Validation
# ==============================================================================

info "Test 2: Discovery file validation"

if [ -f "$DISCOVERY_FILE" ]; then
    pass_test "Discovery file exists: $DISCOVERY_FILE"

    # Check file is not empty
    DISCOVERY_LINES=$(wc -l < "$DISCOVERY_FILE" | tr -d ' ')
    if [ "$DISCOVERY_LINES" -gt 0 ]; then
        pass_test "Discovery file has content: $DISCOVERY_LINES lines"
    else
        fail_test "Discovery file is empty"
    fi

    # Check file contains valid JSON
    if head -1 "$DISCOVERY_FILE" | jq . > /dev/null 2>&1; then
        pass_test "Discovery file contains valid JSON"
    else
        fail_test "Discovery file does not contain valid JSON"
    fi
else
    fail_test "Discovery file does not exist: $DISCOVERY_FILE"
fi

# ==============================================================================
# Test 3: Extraction File Validation
# ==============================================================================

info "Test 3: Extraction file validation"

if [ -f "$EXTRACTION_FILE" ]; then
    pass_test "Extraction file exists: $EXTRACTION_FILE"

    # Check file is not empty
    EXTRACTION_LINES=$(wc -l < "$EXTRACTION_FILE" | tr -d ' ')
    if [ "$EXTRACTION_LINES" -gt 0 ]; then
        pass_test "Extraction file has content: $EXTRACTION_LINES lines"
    else
        fail_test "Extraction file is empty"
    fi

    # Check file contains valid JSON
    if head -1 "$EXTRACTION_FILE" | jq . > /dev/null 2>&1; then
        pass_test "Extraction file contains valid JSON"
    else
        fail_test "Extraction file does not contain valid JSON"
    fi

    # Check for artifact types
    if grep -q '"artifact_type"' "$EXTRACTION_FILE" 2>/dev/null; then
        pass_test "Extraction file contains artifact_type fields"
    else
        fail_test "Extraction file missing artifact_type fields"
    fi
else
    fail_test "Extraction file does not exist: $EXTRACTION_FILE"
fi

# ==============================================================================
# Test 4: Weaviate Connection
# ==============================================================================

info "Test 4: Weaviate service validation"

if curl -s -f http://localhost:8080/v1/meta > /dev/null 2>&1; then
    pass_test "Weaviate is accessible at http://localhost:8080"
else
    fail_test "Cannot connect to Weaviate at http://localhost:8080"
fi

# ==============================================================================
# Test 5: Ollama Connection
# ==============================================================================

info "Test 5: Ollama service validation"

if curl -s -f http://localhost:11434/api/tags > /dev/null 2>&1; then
    pass_test "Ollama is accessible at http://localhost:11434"
else
    fail_test "Ollama is not accessible at http://localhost:11434"
fi

# ==============================================================================
# Test 6: Weaviate Data Validation
# ==============================================================================

info "Test 6: Weaviate data validation"

# Get project status
PROJECT_STATUS=$(codeindex status 2>/dev/null | grep -A5 "Name: $PROJECT_NAME" || echo "")

if [ -n "$PROJECT_STATUS" ]; then
    pass_test "Project found in Weaviate: $PROJECT_NAME"

    # Extract artifact count
    ARTIFACT_COUNT=$(echo "$PROJECT_STATUS" | grep "Artifacts:" | head -1 | awk '{print $2}')

    if [ "$ARTIFACT_COUNT" -gt 0 ]; then
        pass_test "Project has artifacts indexed: $ARTIFACT_COUNT artifacts"
    else
        fail_test "Project has 0 artifacts indexed"
    fi
else
    fail_test "Project not found in Weaviate: $PROJECT_NAME"
fi

# ==============================================================================
# Test 7: Search Functionality
# ==============================================================================

info "Test 7: Search functionality validation"

# Try a basic search
SEARCH_RESULT=$(codeindex search "class" --project "$PROJECT_NAME" --limit 1 2>/dev/null || echo "")

if [ -n "$SEARCH_RESULT" ]; then
    pass_test "Search returns results for project"
else
    warn "Search did not return results (may be expected if no matching artifacts)"
fi

# ==============================================================================
# Test 8: File Content Validation
# ==============================================================================

info "Test 8: Pipeline artifact content validation"

# Check if discovery contains expected fields
if grep -q '"file_path"' "$DISCOVERY_FILE" 2>/dev/null; then
    pass_test "Discovery file contains file_path fields"
else
    fail_test "Discovery file missing file_path fields"
fi

# Check if extraction contains source paths
if grep -q '"source_path"' "$EXTRACTION_FILE" 2>/dev/null; then
    pass_test "Extraction file contains source_path fields"
else
    fail_test "Extraction file missing source_path fields"
fi

# ==============================================================================
# Test 9: Project ID Format Validation
# ==============================================================================

info "Test 9: Project ID format validation"

# Extract project IDs from status
PROJECT_IDS=$(codeindex status 2>/dev/null | grep -B2 "Name: $PROJECT_NAME" | grep -E "^  [a-zA-Z0-9:.-]+$" | tr -d ' ' || echo "")

if [ -n "$PROJECT_IDS" ]; then
    pass_test "Project has valid ID format in Weaviate"
    echo "  Project IDs found: $(echo "$PROJECT_IDS" | wc -l | tr -d ' ')"
else
    fail_test "No valid project IDs found for: $PROJECT_NAME"
fi

# ==============================================================================
# Test 10: Java File Discovery
# ==============================================================================

info "Test 10: Source file discovery validation"

JAVA_COUNT=$(find "$SOURCE_DIR" -name "*.java" -type f 2>/dev/null | wc -l | tr -d ' ')
JSP_COUNT=$(find "$SOURCE_DIR" -name "*.jsp" -type f 2>/dev/null | wc -l | tr -d ' ')

if [ "$JAVA_COUNT" -gt 0 ] || [ "$JSP_COUNT" -gt 0 ]; then
    pass_test "Source directory contains Java/JSP files: $JAVA_COUNT Java, $JSP_COUNT JSP"
else
    fail_test "No Java or JSP files found in source directory"
fi

# ==============================================================================
# Summary
# ==============================================================================

echo ""
echo "=============================================="
echo "Test Results Summary"
echo "=============================================="
echo ""
echo "  Passed: $PASS_COUNT"
echo "  Failed: $FAIL_COUNT"
echo ""

if [ "$FAIL_COUNT" -eq 0 ]; then
    ok "All tests passed! Indexing is working correctly."
    echo ""
    echo "Next steps:"
    echo "  1. Search your codebase:"
    echo "     codeindex search \"your query\" --project $PROJECT_NAME"
    echo ""
    echo "  2. Generate PRD:"
    echo "     codeindex prd --output-dir output/$PROJECT_NAME"
    exit 0
else
    fail "Some tests failed. Review the output above."
    echo ""
    echo "Troubleshooting:"
    echo "  1. Re-run the fix script:"
    echo "     ./fix_indexing.sh $PROJECT_NAME $SOURCE_DIR"
    echo ""
    echo "  2. Run diagnostics:"
    echo "     ./diagnose_indexing.sh $PROJECT_NAME $SOURCE_DIR"
    exit 1
fi
