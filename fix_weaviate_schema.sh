#!/bin/bash

# =============================
# Fix Weaviate Schema with New Ollama Configuration
# =============================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

info(){ echo -e "${BLUE}[INFO]${NC} $1"; }
ok(){ echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warn(){ echo -e "${YELLOW}[WARNING]${NC} $1"; }
err(){ echo -e "${RED}[ERROR]${NC} $1"; }

echo "🔧 Fixing Weaviate Schema with New Ollama Configuration"
echo "======================================================="
echo ""

# Ensure we're in the correct directory
cd "$(dirname "$0")"

# Activate virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    info "Activating virtual environment..."
    source venv/bin/activate || err "Failed to activate virtual environment"
fi

echo "🔍 Step 1: Check Current Configuration"
echo "====================================="

# Check current Ollama configuration
python -c "
import sys
sys.path.insert(0, 'src')
from config.settings import settings
print(f'Current Ollama URL: {settings.ollama_base_url}')
print(f'Current Embed Model: {settings.ollama_embed_model_name}')
"

echo ""
echo "🔍 Step 2: Stop Weaviate Container"
echo "=================================="

# Stop Weaviate container to clear schema
info "Stopping Weaviate container..."
docker stop weaviate-java-analysis || warn "Container not running or different name"

echo ""
echo "🔍 Step 3: Clear Weaviate Data"
echo "=============================="

# Clear Weaviate data directory
info "Clearing Weaviate data directory..."
if [ -d "weaviate-data" ]; then
    rm -rf weaviate-data/*
    ok "Cleared Weaviate data directory"
else
    warn "Weaviate data directory not found"
fi

echo ""
echo "🔍 Step 4: Restart Weaviate Container"
echo "====================================="

# Restart Weaviate container
info "Starting Weaviate container with clean data..."
./docker-weaviate.sh || err "Failed to start Weaviate"

# Wait for Weaviate to be ready
info "Waiting for Weaviate to be ready..."
sleep 10

# Test Weaviate connection
info "Testing Weaviate connection..."
python -c "
import sys
sys.path.insert(0, 'src')
from store.weaviate_client import WeaviateClient
try:
    client = WeaviateClient(ensure_schema=False)
    print('✅ Weaviate connection successful')
except Exception as e:
    print(f'❌ Weaviate connection failed: {e}')
    exit(1)
"

echo ""
echo "🔍 Step 5: Recreate Schema with New Configuration"
echo "================================================="

# Recreate schema with new Ollama configuration
info "Recreating Weaviate schema with new Ollama configuration..."
python -c "
import sys
sys.path.insert(0, 'src')
from store.weaviate_client import WeaviateClient
try:
    client = WeaviateClient(ensure_schema=True)
    print('✅ Schema recreated successfully')
except Exception as e:
    print(f'❌ Schema recreation failed: {e}')
    exit(1)
"

echo ""
echo "🔍 Step 6: Test Indexing with New Schema"
echo "========================================"

# Test indexing with the new schema
info "Testing indexing with new schema..."
python -c "
import sys
import json
sys.path.insert(0, 'src')
from store.weaviate_client import WeaviateClient

print('Testing BackendDoc indexing...')
try:
    client = WeaviateClient(ensure_schema=False)
    
    # Create a test document
    test_doc = {
        'project': 'test_schema_fix',
        'path': '/test/path.java',
        'language': 'java',
        'text': 'This is a test document for schema fix verification.',
        'summary': 'Test summary for schema fix verification'
    }
    
    print('Indexing test document...')
    result = client.index_artifact('BackendDoc', test_doc)
    print(f'✅ Successfully indexed test document with ID: {result}')
    
    # Verify it was indexed
    search_result = client.client.query.get(
        class_name='BackendDoc',
        properties=['project', 'path', 'text']
    ).with_where({
        'path': ['project'],
        'operator': 'Equal',
        'valueString': 'test_schema_fix'
    }).do()
    
    found_docs = search_result.get('data', {}).get('Get', {}).get('BackendDoc', [])
    print(f'✅ Found {len(found_docs)} test documents in Weaviate')
    
    if found_docs:
        print('🎉 Schema fix successful! BackendDoc indexing works now.')
    else:
        print('❌ Test document not found - schema fix may not have worked')
        
except Exception as e:
    print(f'❌ Test failed: {e}')
    import traceback
    traceback.print_exc()
"

echo ""
echo "🎯 Next Steps"
echo "============="
echo ""
echo "1. ✅ Weaviate schema has been recreated with new Ollama configuration"
echo "2. 🔄 Run the full pipeline: ./new_run.sh"
echo "3. 🔍 Check results: ./search_weaviate.sh"
echo ""
echo "The BackendDoc indexing should now work properly!"
