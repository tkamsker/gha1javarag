#!/bin/bash
# Reload All Data Script
# Clears Weaviate, fixes project names, re-indexes all data, and verifies
# Works on both macOS and Linux

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
echo "Reload All Data - Complete Reset"
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

# Step 1: Check Weaviate
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
fi

# Step 2: Clear Weaviate
echo ""
echo -e "${BLUE}Step 2: Clearing Weaviate data...${NC}"
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
    
    print("Deleting all objects from classes...")
    for class_name in classes:
        try:
            # Check if class exists
            if wc._client.schema.exists(class_name):
                # Delete all objects using batch delete
                result = wc._client.batch.delete_objects(
                    class_name=class_name,
                    where={"operator": "Like", "path": ["project"], "valueText": "*"}
                )
                print(f"  ✓ Cleared class: {class_name}")
            else:
                print(f"  - Class {class_name} does not exist (skipping)")
        except Exception as e:
            # Try alternative method - delete class and recreate schema
            try:
                wc._client.schema.delete_class(class_name)
                print(f"  ✓ Deleted class schema: {class_name}")
            except Exception as e2:
                if "not found" not in str(e2).lower():
                    print(f"  ⚠ Could not clear {class_name}: {e2}")
    
    print("  ✓ Weaviate cleared")
except Exception as e:
    print(f"  ⚠ Error clearing Weaviate: {e}")
    print("  Continuing anyway...")
EOF

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

# Step 4: Re-index all artifacts
echo ""
echo -e "${BLUE}Step 4: Re-indexing all artifacts in Weaviate...${NC}"
echo "  This may take 5-15 minutes depending on data size..."
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
    python3 weaviate_stats.py | head -80
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

echo ""
echo "=========================================="
echo -e "${GREEN}Data Reload Complete!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Check statistics: ./weaviate_stats.sh"
echo "  2. Test search: python main.py search --query 'dao' --project 'cuco-core'"
echo "  3. Generate requirements: python main.py requirements --all-projects --use-crewai"
echo ""

