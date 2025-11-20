#!/bin/bash
# Production Setup Script - Start from Scratch
# Works on both macOS and Linux
# 
# This script:
# 1. Verifies Weaviate is running
# 2. Optionally clears Weaviate data
# 3. Fixes project names in artifacts
# 4. Indexes all artifacts
# 5. Verifies indexing
# 6. Optionally generates requirements

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
echo "Production Setup - Start from Scratch"
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
    echo -e "${YELLOW}Warning: No virtual environment found. Using system Python.${NC}"
fi

# Step 1: Check Weaviate connection
echo ""
echo -e "${BLUE}Step 1: Checking Weaviate connection...${NC}"
WEAVIATE_URL="${WEAVIATE_URL:-http://localhost:8080}"

if command -v curl &> /dev/null; then
    if curl -s -f "$WEAVIATE_URL/v1/meta" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Weaviate is accessible at $WEAVIATE_URL${NC}"
    else
        echo -e "${RED}✗ Cannot connect to Weaviate at $WEAVIATE_URL${NC}"
        echo -e "${YELLOW}  Please start Weaviate first:${NC}"
        echo "    docker-compose up -d"
        echo "    or"
        echo "    ./start_weaviate_simple.sh"
        exit 1
    fi
else
    echo -e "${YELLOW}Warning: curl not found, skipping Weaviate connection check${NC}"
fi

# Step 2: Ask about clearing Weaviate
echo ""
echo -e "${BLUE}Step 2: Weaviate Data${NC}"
read -p "Clear existing Weaviate data? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Clearing Weaviate data...${NC}"
    
    # Try to delete all classes
    python3 << 'EOF'
import sys
from pathlib import Path
sys.path.insert(0, str(Path('src')))
from store.weaviate_client import WeaviateClient

try:
    wc = WeaviateClient(ensure_schema=False)
    classes = ['DaoCall', 'IbatisStatement', 'BackendDoc', 'JspForm', 
               'DbTable', 'GwtModule', 'GwtUiBinder', 'GwtActivityPlace',
               'GwtEndpoint', 'JsArtifact']
    
    for class_name in classes:
        try:
            wc._client.schema.delete_class(class_name)
            print(f"  ✓ Deleted class: {class_name}")
        except Exception as e:
            if "not found" not in str(e).lower():
                print(f"  ⚠ Could not delete {class_name}: {e}")
    
    print("  ✓ Weaviate cleared")
except Exception as e:
    print(f"  ⚠ Error clearing Weaviate: {e}")
    print("  Continuing anyway...")
EOF
else
    echo -e "${YELLOW}Skipping Weaviate clear (keeping existing data)${NC}"
fi

# Step 3: Fix project names
echo ""
echo -e "${BLUE}Step 3: Fixing project names in artifacts...${NC}"
if [ -f "fix_project_names.py" ]; then
    python3 fix_project_names.py
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Project names fixed${NC}"
    else
        echo -e "${RED}✗ Error fixing project names${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}Warning: fix_project_names.py not found, skipping${NC}"
fi

# Step 4: Index all artifacts
echo ""
echo -e "${BLUE}Step 4: Indexing all artifacts in Weaviate...${NC}"
echo "  This may take several minutes..."
python3 main.py index --all-projects

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Indexing completed${NC}"
else
    echo -e "${RED}✗ Error during indexing${NC}"
    exit 1
fi

# Step 5: Verify indexing
echo ""
echo -e "${BLUE}Step 5: Verifying indexing...${NC}"
if [ -f "weaviate_stats.py" ]; then
    python3 weaviate_stats.py | head -100
    echo ""
    echo -e "${GREEN}✓ Statistics generated${NC}"
else
    echo -e "${YELLOW}Warning: weaviate_stats.py not found, skipping verification${NC}"
fi

# Step 6: Test search
echo ""
echo -e "${BLUE}Step 6: Testing search...${NC}"
python3 << 'EOF'
import sys
from pathlib import Path
sys.path.insert(0, str(Path('src')))
from store.weaviate_client import WeaviateClient

wc = WeaviateClient(ensure_schema=False)

# Test search for a common project
test_projects = ['cuco-core', 'cuco-ui-app', 'PastExport']
for project in test_projects:
    results = wc.search_artifacts('DaoCall', 'dao', project=project, limit=3)
    if results:
        print(f"  ✓ {project}: Found {len(results)} results")
    else:
        print(f"  ✗ {project}: No results")
EOF

# Step 7: Ask about generating requirements
echo ""
echo -e "${BLUE}Step 7: Requirements Generation${NC}"
read -p "Generate requirements documents? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Generating requirements (this may take a long time)...${NC}"
    echo "  Using CrewAI multi-agent approach..."
    
    # Generate with timestamped log
    LOG_FILE="logprod_crewai_$(date +'%Y-%m-%d_%H-%M-%S').log"
    echo "  Log file: $LOG_FILE"
    
    nohup python3 main.py requirements --all-projects --use-crewai > "$LOG_FILE" 2>&1 &
    PID=$!
    
    echo -e "${GREEN}✓ Requirements generation started in background (PID: $PID)${NC}"
    echo "  Monitor progress: tail -f $LOG_FILE"
    echo "  Check status: ps aux | grep $PID"
else
    echo -e "${YELLOW}Skipping requirements generation${NC}"
fi

# Summary
echo ""
echo "=========================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Check Weaviate statistics: ./weaviate_stats.sh"
echo "  2. Test searches: python main.py search --query 'dao' --project 'cuco-core'"
echo "  3. Monitor requirements generation: tail -f $LOG_FILE"
echo ""

