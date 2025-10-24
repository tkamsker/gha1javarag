#!/bin/bash

# =============================
# Quick Weaviate Status Check
# =============================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info(){ echo -e "${BLUE}[INFO]${NC} $1"; }
ok(){ echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warn(){ echo -e "${YELLOW}[WARNING]${NC} $1"; }
err(){ echo -e "${RED}[ERROR]${NC} $1"; }

echo "🔍 Quick Weaviate Status Check"
echo "==============================="

# Ensure we're in the correct directory
cd "$(dirname "$0")"

# Check if Weaviate container is running
info "Checking Weaviate container status..."
if docker ps | grep -q weaviate; then
    ok "Weaviate container is running"
    docker ps | grep weaviate
else
    warn "Weaviate container is not running"
    echo "Run: ./docker-weaviate.sh"
fi

echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    ok "Virtual environment exists"
else
    err "Virtual environment not found. Run: python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
fi

# Activate virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    info "Activating virtual environment..."
    source venv/bin/activate || err "Failed to activate virtual environment"
fi

# Test Python connection to Weaviate
info "Testing Python connection to Weaviate..."
python -c "
import sys
sys.path.insert(0, 'src')
from store.weaviate_client import WeaviateClient
try:
    client = WeaviateClient(ensure_schema=False)
    print('✅ Python can connect to Weaviate')
    
    # Get schema info
    schema = client.client.schema.get()
    classes = schema.get('classes', [])
    print(f'📊 Found {len(classes)} classes in Weaviate:')
    for cls in classes:
        class_name = cls.get('class', 'Unknown')
        print(f'  - {class_name}')
    
    if len(classes) == 0:
        print('📭 No classes found - Weaviate is empty')
        print('💡 Run ./new_run.sh to populate with data')
        
except Exception as e:
    print(f'❌ Python connection failed: {e}')
    print('💡 Make sure Weaviate is running: ./docker-weaviate.sh')
" || warn "Python connection test failed"

echo ""
echo "🎯 Next Steps:"
echo "  - If Weaviate is empty: Run ./new_run.sh to create a project"
echo "  - If Weaviate has data: Run ./search_weaviate.sh to see projects"
echo "  - If container not running: Run ./docker-weaviate.sh"
