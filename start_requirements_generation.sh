#!/bin/bash
# Start Requirements Generation Script
# Generates detailed requirements for all projects using enhanced CrewAI
#
# Usage:
#   ./start_requirements_generation.sh [MODE] [PROJECTS...]
#
# Parameters:
#   MODE: 1 = All projects, 2 = Specific projects, 3 = Top 10 projects
#   PROJECTS: (for MODE 2) Project name(s), space-separated
#
# Examples:
#   ./start_requirements_generation.sh 1                    # All projects
#   ./start_requirements_generation.sh 2 cuco-core PastExport  # Specific projects
#   ./start_requirements_generation.sh 3                    # Top 10 projects
#   nohup ./start_requirements_generation.sh 1 > start.log 2>&1 &  # Background with nohup

# Don't exit on error for nohup compatibility, but track errors
set +e

# Colors for output (only if terminal supports it)
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    NC='\033[0m'
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    NC=''
fi

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

# Parse command-line arguments
MODE="${1:-}"
shift  # Remove first argument

# If no mode provided, use interactive mode
if [ -z "$MODE" ]; then
    echo -e "${BLUE}Step 3: Select generation mode${NC}"
    echo "1. Generate for ALL projects (1-3 hours)"
    echo "2. Generate for specific project(s)"
    echo "3. Generate for top 10 projects"
    echo ""
    read -p "Enter choice (1-3): " MODE
fi

# Validate mode
if [[ ! "$MODE" =~ ^[123]$ ]]; then
    echo -e "${RED}Error: Invalid mode. Must be 1, 2, or 3${NC}"
    echo "Usage: $0 [1|2|3] [PROJECTS...]"
    exit 1
fi

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
else
    echo -e "${YELLOW}⚠ curl not found, skipping Weaviate check${NC}"
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

# Step 3: Determine generation mode and build command
echo ""
echo -e "${BLUE}Step 3: Generation mode: $MODE${NC}"

case $MODE in
    1)
        MODE_NAME="all"
        CMD="python main.py requirements --all-projects --use-crewai"
        echo -e "${GREEN}Selected: Generate for all projects${NC}"
        ;;
    2)
        MODE_NAME="specific"
        if [ $# -eq 0 ]; then
            # Interactive mode: ask for projects
            read -p "Enter project name(s), comma or space-separated: " projects_input
            # Handle both comma and space separated
            PROJECTS=$(echo "$projects_input" | tr ',' ' ')
        else
            # Command-line mode: use remaining arguments
            PROJECTS="$@"
        fi
        
        if [ -z "$PROJECTS" ]; then
            echo -e "${RED}Error: No projects specified${NC}"
            exit 1
        fi
        
        echo -e "${GREEN}Selected: Generate for: $PROJECTS${NC}"
        CMD=""
        for proj in $PROJECTS; do
            CMD="$CMD python main.py requirements --project '$proj' --use-crewai;"
        done
        ;;
    3)
        MODE_NAME="top10"
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
esac

# Step 4: Start generation
echo ""
echo -e "${BLUE}Step 4: Starting requirements generation...${NC}"
LOG_FILE="log_start_requirements_generationj_$(date +'%Y-%m-%d_%H-%M-%S').log"

if [ "$MODE_NAME" == "all" ]; then
    echo "  Running in background with nohup..."
    echo "  Log file: $LOG_FILE"
    echo "  Command: $CMD"
    nohup bash -c "$CMD" > "$LOG_FILE" 2>&1 &
    PID=$!
    echo -e "${GREEN}✓ Generation started (PID: $PID)${NC}"
    echo "  Monitor with: tail -f $LOG_FILE"
    echo "  Check status with: ps -p $PID"
    echo "  To stop: kill $PID"
elif [ "$MODE_NAME" == "top10" ]; then
    echo "  Running sequentially for top 10 projects..."
    echo "  Log file: $LOG_FILE"
    nohup bash -c "$CMD" > "$LOG_FILE" 2>&1 &
    PID=$!
    echo -e "${GREEN}✓ Generation started (PID: $PID)${NC}"
    echo "  Monitor with: tail -f $LOG_FILE"
else
    echo "  Running sequentially for specific projects..."
    echo "  Log file: $LOG_FILE"
    eval "$CMD" >> "$LOG_FILE" 2>&1
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 0 ]; then
        echo -e "${GREEN}✓ Generation completed${NC}"
    else
        echo -e "${RED}✗ Generation failed with exit code $EXIT_CODE${NC}"
        echo "  Check log: $LOG_FILE"
        exit $EXIT_CODE
    fi
fi

echo ""
echo "=========================================="
echo -e "${GREEN}Requirements Generation Started!${NC}"
echo "=========================================="
echo ""
if [ "$MODE_NAME" == "all" ] || [ "$MODE_NAME" == "top10" ]; then
    echo "Process running in background (PID: $PID)"
    echo ""
    echo "Monitor progress:"
    echo "  tail -f $LOG_FILE"
    echo ""
    echo "Check process status:"
    echo "  ps -p $PID"
    echo ""
    echo "Stop the process:"
    echo "  kill $PID"
    echo ""
else
    echo "Process completed. Check log for details."
    echo ""
fi
echo "Check for errors:"
echo "  grep -i error $LOG_FILE"
echo ""
echo "Check output files:"
echo "  ls -lh output/*_crewai_requirements.md"
echo ""
echo "Count completed projects:"
echo "  ls -1 output/*_crewai_requirements.md | wc -l"
echo ""
echo "Check for placeholders:"
echo "  grep -l -i 'placeholder\\|unable to retrieve' output/*_crewai_requirements.md || echo 'No placeholders found'"
echo ""

