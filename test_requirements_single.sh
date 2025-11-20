#!/bin/bash
# Test script for requirements generation with a single project
# Usage: ./test_requirements_single.sh [PROJECT_NAME]

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

PROJECT="${1:-PastExport}"
LOG_FILE="test_${PROJECT}_$(date +'%Y-%m-%d_%H-%M-%S').log"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Testing Requirements Generation${NC}"
echo -e "${BLUE}Project: ${PROJECT}${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Activate venv
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo -e "${RED}Error: No virtual environment found${NC}"
    exit 1
fi

# Check Weaviate
echo -e "${BLUE}Step 1: Checking Weaviate connection...${NC}"
WEAVIATE_URL="${WEAVIATE_URL:-http://localhost:8080}"
if curl -s -f "$WEAVIATE_URL/v1/meta" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Weaviate is accessible${NC}"
else
    echo -e "${RED}✗ Cannot connect to Weaviate${NC}"
    exit 1
fi

# Check if project has data
echo ""
echo -e "${BLUE}Step 2: Checking project data in Weaviate...${NC}"
python3 << EOF
import sys
from pathlib import Path
sys.path.insert(0, str(Path('src')))
from store.weaviate_client import WeaviateClient

client = WeaviateClient(ensure_schema=False)
wc = client._client

# Check DaoCall count for project
try:
    results = client.search_artifacts('DaoCall', 'dao', project='${PROJECT}', limit=1)
    if results:
        print(f"  ✓ Found data for ${PROJECT}")
    else:
        print(f"  ⚠ No DaoCall data found for ${PROJECT}")
except Exception as e:
    print(f"  ✗ Error: {e}")
    sys.exit(1)
EOF

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Warning: Project may not have data, but continuing...${NC}"
fi

# Run requirements generation
echo ""
echo -e "${BLUE}Step 3: Running requirements generation...${NC}"
echo -e "${YELLOW}Log file: ${LOG_FILE}${NC}"
echo ""

python main.py requirements --project "$PROJECT" --use-crewai 2>&1 | tee "$LOG_FILE"

EXIT_CODE=${PIPESTATUS[0]}

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Analysis${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check for tool calls
echo -e "${BLUE}Checking tool usage...${NC}"
SEARCH_CALLS=$(grep -c "search_weaviate\|searching weaviate\|Trying data_object.get" "$LOG_FILE" 2>/dev/null || echo "0")
READ_CALLS=$(grep -c "read_source_file\|reading source\|Found.*file.*matching" "$LOG_FILE" 2>/dev/null || echo "0")

echo "  Search tool calls: $SEARCH_CALLS"
echo "  File reader calls: $READ_CALLS"

if [ "$SEARCH_CALLS" -gt 0 ] || [ "$READ_CALLS" -gt 0 ]; then
    echo -e "${GREEN}✓ Tools are being called${NC}"
else
    echo -e "${RED}✗ No tool calls detected${NC}"
fi

# Check output file
echo ""
echo -e "${BLUE}Checking output file...${NC}"
OUTPUT_FILE="output/${PROJECT}_crewai_requirements.md"

if [ -f "$OUTPUT_FILE" ]; then
    FILE_SIZE=$(wc -c < "$OUTPUT_FILE")
    LINE_COUNT=$(wc -l < "$OUTPUT_FILE")
    echo -e "${GREEN}✓ Output file created: ${OUTPUT_FILE}${NC}"
    echo "  Size: $FILE_SIZE bytes"
    echo "  Lines: $LINE_COUNT"
    
    # Check for placeholders
    PLACEHOLDERS=$(grep -ci "placeholder\|unable to retrieve\|no results found\|incomplete" "$OUTPUT_FILE" || echo "0")
    if [ "$PLACEHOLDERS" -gt 0 ]; then
        echo -e "${YELLOW}⚠ Found $PLACEHOLDERS placeholder/incomplete messages${NC}"
    else
        echo -e "${GREEN}✓ No placeholders found${NC}"
    fi
    
    # Check for specific details
    FILE_PATHS=$(grep -cE "\.java|\.jsp|\.xml|/mnt/" "$OUTPUT_FILE" || echo "0")
    echo "  File paths referenced: $FILE_PATHS"
    
    if [ "$FILE_PATHS" -gt 0 ]; then
        echo -e "${GREEN}✓ Contains specific file references${NC}"
    else
        echo -e "${YELLOW}⚠ No specific file paths found${NC}"
    fi
    
    # Show first 20 lines
    echo ""
    echo -e "${BLUE}First 20 lines of output:${NC}"
    head -20 "$OUTPUT_FILE"
else
    echo -e "${RED}✗ Output file not found${NC}"
fi

# Summary
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "Log file: $LOG_FILE"
echo "Output file: $OUTPUT_FILE"
echo ""
echo "To view full log:"
echo "  cat $LOG_FILE"
echo ""
echo "To view output:"
echo "  cat $OUTPUT_FILE"
echo ""
echo "To check for errors:"
echo "  grep -i error $LOG_FILE"
echo ""

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ Test completed successfully${NC}"
else
    echo -e "${RED}✗ Test failed with exit code $EXIT_CODE${NC}"
fi

exit $EXIT_CODE

