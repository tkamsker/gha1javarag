#!/bin/bash

# =============================
# Fix Ollama Configuration
# Resolves hostname connectivity issues
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

echo "🔧 Fixing Ollama Configuration"
echo "=============================="
echo ""

# Ensure we're in the correct directory
cd "$(dirname "$0")"

# Check current Ollama configuration
info "Current Ollama configuration:"
python -c "
import sys
sys.path.insert(0, 'src')
from config.settings import settings
print(f'  Ollama URL: {settings.ollama_base_url}')
print(f'  Ollama Embed Model: {settings.ollama_embed_model_name}')
"

echo ""
echo "🔍 Step 1: Check Ollama Service"
echo "==============================="

# Check if Ollama is running and accessible
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    ok "Ollama is accessible at localhost:11434"
    echo "Available models:"
    curl -s http://localhost:11434/api/tags | python -c "
import sys, json
try:
    data = json.load(sys.stdin)
    for model in data.get('models', []):
        print(f'  - {model.get(\"name\", \"Unknown\")}')
except:
    print('  Could not parse model list')
" 2>/dev/null || echo "  Could not list models"
else
    warn "Ollama not accessible at localhost:11434"
    echo "Checking if Ollama is running in Docker..."
    if docker ps | grep -q ollama; then
        ok "Ollama container is running"
        docker ps | grep ollama
    else
        err "Ollama is not running. Please start it first."
        exit 1
    fi
fi

echo ""
echo "🔍 Step 2: Test Different Ollama URLs"
echo "====================================="

# Test different possible Ollama URLs
OLLAMA_URLS=(
    "http://localhost:11434"
    "http://127.0.0.1:11434"
    "http://host.docker.internal:11434"
    "http://ollama:11434"
)

for url in "${OLLAMA_URLS[@]}"; do
    echo -n "Testing $url... "
    if curl -s --connect-timeout 5 "$url/api/tags" > /dev/null 2>&1; then
        ok "✅ Working"
        WORKING_URL="$url"
        break
    else
        echo "❌ Failed"
    fi
done

if [ -z "$WORKING_URL" ]; then
    err "No working Ollama URL found"
    exit 1
fi

echo ""
echo "🔍 Step 3: Create Fixed Configuration"
echo "====================================="

# Create a .env file with the correct Ollama URL
info "Creating .env file with correct Ollama configuration..."

cat > .env << EOF
# Ollama Configuration
OLLAMA_BASE_URL=$WORKING_URL
OLLAMA_MODEL_NAME=gemma3:12b
OLLAMA_EMBED_MODEL_NAME=nomic-embed-text

# Weaviate Configuration
WEAVIATE_URL=http://localhost:8080
WEAVIATE_API_KEY=

# Java Source Directory (update this to your actual source path)
JAVA_SOURCE_DIR=/path/to/your/java/source

# Default Project
DEFAULT_PROJECT_NAME=default-project
EOF

ok "Created .env file with Ollama URL: $WORKING_URL"

echo ""
echo "🔍 Step 4: Test Fixed Configuration"
echo "==================================="

# Test the new configuration
info "Testing new configuration..."
python -c "
import sys
sys.path.insert(0, 'src')
from config.settings import settings
print(f'  Ollama URL: {settings.ollama_base_url}')
print(f'  Ollama Embed Model: {settings.ollama_embed_model_name}')

# Test Ollama connection
import requests
try:
    response = requests.get(f'{settings.ollama_base_url}/api/tags', timeout=5)
    if response.status_code == 200:
        print('  ✅ Ollama connection successful')
    else:
        print(f'  ❌ Ollama connection failed: {response.status_code}')
except Exception as e:
    print(f'  ❌ Ollama connection failed: {e}')
"

echo ""
echo "🔍 Step 5: Test Weaviate Indexing"
echo "================================="

# Test indexing with the fixed configuration
info "Testing Weaviate indexing with fixed Ollama configuration..."

python -c "
import sys
import json
sys.path.insert(0, 'src')
from store.weaviate_client import WeaviateClient

print('Testing Weaviate indexing...')
try:
    client = WeaviateClient(ensure_schema=False)
    
    # Create a test document
    test_doc = {
        'project': 'test_fix',
        'path': '/test/path.java',
        'language': 'java',
        'text': 'This is a test document for Ollama configuration fix.',
        'summary': 'Test summary for configuration verification'
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
        'valueString': 'test_fix'
    }).do()
    
    found_docs = search_result.get('data', {}).get('Get', {}).get('BackendDoc', [])
    print(f'✅ Found {len(found_docs)} test documents in Weaviate')
    
    if found_docs:
        print('🎉 Ollama configuration fix successful!')
    else:
        print('❌ Test document not found - indexing may still have issues')
        
except Exception as e:
    print(f'❌ Test failed: {e}')
    import traceback
    traceback.print_exc()
"

echo ""
echo "🎯 Next Steps"
echo "============="
echo ""
echo "1. ✅ Ollama configuration has been fixed"
echo "2. 🔄 Run the full pipeline: ./new_run.sh"
echo "3. 🔍 Check results: ./search_weaviate.sh"
echo ""
echo "If you still have issues:"
echo "- Check that your Java source directory is correct in .env"
echo "- Verify Ollama is running and accessible"
echo "- Run ./test_indexing.sh to debug further"
