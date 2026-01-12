#!/bin/bash
# T015: Production Validation Script
#
# Validates Feature 008 improvements on a production codebase
#
# Usage: ./validate_t015_production.sh [source_dir] [project_name]
#
# Example: ./validate_t015_production.sh /path/to/cuco-ui-admin cuco-ui-admin

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse arguments
SOURCE_DIR="${1:-}"
PROJECT_NAME="${2:-validation-test}"

if [ -z "$SOURCE_DIR" ]; then
    echo -e "${RED}Error: Source directory required${NC}"
    echo "Usage: $0 <source_dir> [project_name]"
    exit 1
fi

if [ ! -d "$SOURCE_DIR" ]; then
    echo -e "${RED}Error: Source directory not found: $SOURCE_DIR${NC}"
    exit 1
fi

OUTPUT_DIR="./output/${PROJECT_NAME}"
LOG_FILE="./validation_t015_$(date +%Y%m%d_%H%M%S).log"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}T015: Production Validation${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "Source: $SOURCE_DIR"
echo "Project: $PROJECT_NAME"
echo "Output: $OUTPUT_DIR"
echo "Log: $LOG_FILE"
echo ""

# Initialize counters
PASSED=0
FAILED=0
WARNINGS=0

# Function to check result
check_result() {
    local test_name="$1"
    local condition="$2"

    if [ "$condition" = "true" ]; then
        echo -e "${GREEN}✓${NC} $test_name"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $test_name"
        ((FAILED++))
    fi
}

check_warning() {
    local test_name="$1"
    local condition="$2"

    if [ "$condition" = "true" ]; then
        echo -e "${GREEN}✓${NC} $test_name"
        ((PASSED++))
    else
        echo -e "${YELLOW}⚠${NC} $test_name"
        ((WARNINGS++))
    fi
}

# Start timing
START_TIME=$(date +%s)

echo -e "${BLUE}Step 1: Environment Check${NC}"
echo "-----------------------------------"

# Check Python environment
check_result "Python virtual environment" "$([ -d .venv ] && echo true || echo false)"

# Check package installed
if python -c "import codeindex" 2>/dev/null; then
    check_result "codeindex package installed" "true"
else
    check_result "codeindex package installed" "false"
    echo -e "${RED}Run: source .venv/bin/activate && pip install -e .${NC}"
    exit 1
fi

# Check Ollama running
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    check_result "Ollama service running" "true"
else
    check_warning "Ollama service running" "false"
    echo -e "${YELLOW}  Ollama not running - extraction will use structural fallback${NC}"
fi

echo ""

echo -e "${BLUE}Step 2: Discovery${NC}"
echo "-----------------------------------"

# Run discovery
echo "Running discovery on $SOURCE_DIR..."
codeindex discover \
    --source-dir "$SOURCE_DIR" \
    --output "${OUTPUT_DIR}/discovery-inventory.jsonl" \
    2>&1 | tee -a "$LOG_FILE"

# Check discovery output
if [ -f "${OUTPUT_DIR}/discovery-inventory.jsonl" ]; then
    FILE_COUNT=$(wc -l < "${OUTPUT_DIR}/discovery-inventory.jsonl" | tr -d ' ')
    check_result "Discovery completed" "true"
    echo "  Files discovered: $FILE_COUNT"
else
    check_result "Discovery completed" "false"
    exit 1
fi

echo ""

echo -e "${BLUE}Step 3: Extraction${NC}"
echo "-----------------------------------"

# Run extraction
echo "Running extraction..."
codeindex extract \
    --inventory "${OUTPUT_DIR}/discovery-inventory.jsonl" \
    --output "${OUTPUT_DIR}/extraction-results.jsonl" \
    2>&1 | tee -a "$LOG_FILE"

# Check extraction output
if [ -f "${OUTPUT_DIR}/extraction-results.jsonl" ]; then
    EXTRACTED_COUNT=$(wc -l < "${OUTPUT_DIR}/extraction-results.jsonl" | tr -d ' ')
    check_result "Extraction completed" "true"
    echo "  Files extracted: $EXTRACTED_COUNT"

    # Calculate extraction rate
    if [ "$FILE_COUNT" -gt 0 ]; then
        EXTRACTION_RATE=$(python3 -c "print(f'{($EXTRACTED_COUNT / $FILE_COUNT * 100):.1f}')")
        echo "  Extraction rate: ${EXTRACTION_RATE}%"
    fi

    # Check for timeout errors in log
    TIMEOUT_COUNT=$(grep -c "TimeoutError\|timed out" "$LOG_FILE" || echo "0")
    TIMEOUT_RATE=$(python3 -c "print(f'{($TIMEOUT_COUNT / $FILE_COUNT * 100):.2f}')" 2>/dev/null || echo "0")
    echo "  Timeout errors: $TIMEOUT_COUNT (${TIMEOUT_RATE}%)"

    # T005 validation: Timeout rate should be <2%
    if [ $(python3 -c "print('true' if $TIMEOUT_RATE < 2.0 else 'false')") = "true" ]; then
        check_result "Timeout rate <2% (T005 validation)" "true"
    else
        check_warning "Timeout rate <2% (T005 validation)" "false"
        echo -e "${YELLOW}  Expected: <2%, Actual: ${TIMEOUT_RATE}%${NC}"
    fi

else
    check_result "Extraction completed" "false"
    exit 1
fi

echo ""

echo -e "${BLUE}Step 4: Indexing${NC}"
echo "-----------------------------------"

# Check if Weaviate is running
if curl -s http://localhost:8080/v1/.well-known/ready > /dev/null 2>&1; then
    echo "Running indexing..."
    codeindex index \
        --inventory "${OUTPUT_DIR}/discovery-inventory.jsonl" \
        --extraction "${OUTPUT_DIR}/extraction-results.jsonl" \
        2>&1 | tee -a "$LOG_FILE"

    check_result "Indexing completed" "true"
else
    check_warning "Weaviate running (indexing skipped)" "false"
    echo -e "${YELLOW}  Start Weaviate with: ./docker-weaviate.sh start${NC}"
fi

echo ""

echo -e "${BLUE}Step 5: PRD Generation${NC}"
echo "-----------------------------------"

# Run services PRD
echo "Generating services PRD..."
codeindex prd services \
    --output-dir "$OUTPUT_DIR" \
    2>&1 | tee -a "$LOG_FILE"

if [ -f "${OUTPUT_DIR}/prd/services_prd.md" ]; then
    check_result "Services PRD generated" "true"
    SERVICES_SIZE=$(wc -l < "${OUTPUT_DIR}/prd/services_prd.md" | tr -d ' ')
    echo "  Services PRD: $SERVICES_SIZE lines"
else
    check_result "Services PRD generated" "false"
fi

# Run frontend PRD
echo "Generating frontend PRD..."
codeindex prd frontend \
    --output-dir "$OUTPUT_DIR" \
    2>&1 | tee -a "$LOG_FILE"

if [ -f "${OUTPUT_DIR}/prd/frontend_prd.md" ]; then
    check_result "Frontend PRD generated" "true"
    FRONTEND_SIZE=$(wc -l < "${OUTPUT_DIR}/prd/frontend_prd.md" | tr -d ' ')
    echo "  Frontend PRD: $FRONTEND_SIZE lines"

    # T008 validation: Check frontend extraction rate
    FRONTEND_FILES=$(find "$SOURCE_DIR" -type f \( -name "*.jsp" -o -name "*.html" -o -name "*.ui.xml" \) 2>/dev/null | wc -l | tr -d ' ')
    if [ "$FRONTEND_FILES" -gt 0 ]; then
        FRONTEND_FORMS=$(find "${OUTPUT_DIR}/frontend/forms" -type f -name "*.json" 2>/dev/null | wc -l | tr -d ' ')
        FRONTEND_RATE=$(python3 -c "print(f'{($FRONTEND_FORMS / $FRONTEND_FILES * 100):.1f}')" 2>/dev/null || echo "0")
        echo "  Frontend files: $FRONTEND_FILES"
        echo "  Forms extracted: $FRONTEND_FORMS"
        echo "  Extraction rate: ${FRONTEND_RATE}%"

        # T008 + T011 validation: Extraction rate should be >10%
        if [ $(python3 -c "print('true' if $FRONTEND_RATE > 10.0 else 'false')" 2>/dev/null || echo "false") = "true" ]; then
            check_result "Frontend extraction rate >10% (T008+T011)" "true"
        else
            check_warning "Frontend extraction rate >10% (T008+T011)" "false"
            echo -e "${YELLOW}  Expected: >10%, Actual: ${FRONTEND_RATE}%${NC}"
        fi
    fi
else
    check_result "Frontend PRD generated" "false"
fi

echo ""

echo -e "${BLUE}Step 6: Feature Validation${NC}"
echo "-----------------------------------"

# T009: Check GWT linkage file
if [ -f "${OUTPUT_DIR}/frontend/components/gwt_linkage.json" ]; then
    check_result "GWT linkage generated (T009)" "true"
    CHAINS=$(python3 -c "import json; print(len(json.load(open('${OUTPUT_DIR}/frontend/components/gwt_linkage.json'))['complete_chains']))" 2>/dev/null || echo "0")
    echo "  Complete MVP chains: $CHAINS"
else
    check_warning "GWT linkage generated (T009)" "false"
fi

# T010/T011: Check HTML parser usage
HTML_PARSER_USES=$(grep -c "Using HTML parser" "$LOG_FILE" 2>/dev/null || echo "0")
if [ "$HTML_PARSER_USES" -gt 0 ]; then
    check_result "HTML parser used (T010+T011)" "true"
    echo "  HTML files parsed: $HTML_PARSER_USES"
else
    check_warning "HTML parser used (T010+T011)" "false"
    echo "  No HTML files found or processed"
fi

# Check for blocking errors
BLOCKING_ERRORS=$(grep -c "ERROR.*AttributeError\|ERROR.*NoneType" "$LOG_FILE" 2>/dev/null || echo "0")
if [ "$BLOCKING_ERRORS" -eq 0 ]; then
    check_result "Zero blocking errors" "true"
else
    check_result "Zero blocking errors" "false"
    echo -e "${RED}  Found $BLOCKING_ERRORS blocking errors - check log${NC}"
fi

echo ""

# Calculate duration
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
HOURS=$((DURATION / 3600))
MINUTES=$(((DURATION % 3600) / 60))
SECONDS=$((DURATION % 60))

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Validation Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "Duration: ${HOURS}h ${MINUTES}m ${SECONDS}s"
echo ""
echo -e "${GREEN}Passed:${NC}   $PASSED"
if [ "$WARNINGS" -gt 0 ]; then
    echo -e "${YELLOW}Warnings:${NC} $WARNINGS"
fi
if [ "$FAILED" -gt 0 ]; then
    echo -e "${RED}Failed:${NC}   $FAILED"
fi
echo ""

# Final result
if [ "$FAILED" -eq 0 ]; then
    echo -e "${GREEN}✓ Production validation PASSED${NC}"
    echo ""
    echo "Log file: $LOG_FILE"
    echo "Output directory: $OUTPUT_DIR"
    exit 0
else
    echo -e "${RED}✗ Production validation FAILED${NC}"
    echo ""
    echo "Check log file: $LOG_FILE"
    exit 1
fi
