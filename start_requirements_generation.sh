#!/bin/bash
# Start Requirements Generation Script
# Generates detailed requirements for all projects using enhanced CrewAI

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
else
    OS="Unknown"
fi

echo "=========================================="
echo "Requirements Generation Starter"
echo "OS: $OS"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo -e "${BLUE}Activating virtual environment...${NC}"
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo -e "${BLUE}Activating virtual environment...${NC}"
    source .venv/bin/activate
else
    echo -e "${RED}Error: No virtual environment found${NC}"
    echo "Please create one: python -m venv venv"
    exit 1
fi

# Step 1: Verify Weaviate
echo ""
echo -e "${BLUE}Step 1: Verifying Weaviate connection...${NC}"
WEAVIATE_URL="${WEAVIATE_URL:-http://localhost:8080}"

if command -v curl &> /dev/null; then
    if curl -s -f "$WEAVIATE_URL/v1/meta" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Weaviate is accessible${NC}"
    else
        echo -e "${RED}✗ Cannot connect to Weaviate${NC}"
        echo "Please start Weaviate first"
        exit 1
    fi
fi

# Step 2: Verify data is indexed
echo ""
echo -e "${BLUE}Step 2: Checking indexed data...${NC}"
python3 << 'EOF'
import sys
from pathlib import Path
sys.path.insert(0, str(Path('src')))
from store.weaviate_client import WeaviateClient

wc = WeaviateClient(ensure_schema=False)
client = wc._client

# Check DaoCall count
try:
    agg_res = client.query.aggregate("DaoCall").with_meta_count().do()
    count = agg_res.get('data', {}).get('Aggregate', {}).get('DaoCall', [{}])[0].get('meta', {}).get('count', 0)
    if count > 0:
        print(f"  ✓ Found {count:,} DaoCall objects")
    else:
        print("  ⚠ No DaoCall objects found")
        sys.exit(1)
except Exception as e:
    print(f"  ✗ Error checking data: {e}")
    sys.exit(1)
EOF

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: No data found in Weaviate${NC}"
    echo "Please run: ./reload_all_data.sh"
    exit 1
fi

# Step 3: Ask for generation mode
echo ""
echo -e "${BLUE}Step 3: Select generation mode${NC}"
echo "1. Generate for ALL projects (1-3 hours)"
echo "2. Generate for specific project(s)"
echo "3. Generate for top 10 projects"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        MODE="all"
        CMD="python main.py requirements --all-projects --use-crewai"
        echo -e "${GREEN}Selected: Generate for all projects${NC}"
        ;;
    2)
        MODE="specific"
        read -p "Enter project name(s), comma-separated: " projects
        echo -e "${GREEN}Selected: Generate for: $projects${NC}"
        CMD=""
        for proj in $(echo $projects | tr ',' ' '); do
            CMD="$CMD python main.py requirements --project '$proj' --use-crewai;"
        done
        ;;
    3)
        MODE="top10"
        TOP_PROJECTS=(
            "cuco-core"
            "cuco-ui-app"
            "cuco-ui-common"
            "cuco-ui-admin"
            "pkb-core"
            "cuco-ui-visitreports"
            "cuco-ui-cct-bi"
            "administration.ui"
            "cuco-cct-core"
            "pkb-ui-common"
        )
        echo -e "${GREEN}Selected: Generate for top 10 projects${NC}"
        CMD=""
        for proj in "${TOP_PROJECTS[@]}"; do
            CMD="$CMD python main.py requirements --project '$proj' --use-crewai;"
        done
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

# Step 4: Start generation
echo ""
echo -e "${BLUE}Step 4: Starting requirements generation...${NC}"
LOG_FILE="logprod_crewai_$(date +'%Y-%m-%d_%H-%M-%S').log"

if [ "$MODE" == "all" ]; then
    echo "  Running in background..."
    echo "  Log file: $LOG_FILE"
    nohup $CMD > "$LOG_FILE" 2>&1 &
    PID=$!
    echo -e "${GREEN}✓ Generation started (PID: $PID)${NC}"
else
    echo "  Running sequentially..."
    echo "  Log file: $LOG_FILE"
    eval $CMD > "$LOG_FILE" 2>&1
    echo -e "${GREEN}✓ Generation completed${NC}"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}Requirements Generation Started!${NC}"
echo "=========================================="
echo ""
echo "Monitor progress:"
echo "  tail -f $LOG_FILE"
echo ""
echo "Check for errors:"
echo "  grep -i error $LOG_FILE"
echo ""
echo "Check output files:"
echo "  ls -lh output/*_crewai_requirements.md"
echo ""
echo "Preview results:"
echo "  head -100 output/*_crewai_requirements.md"
echo ""

