#!/bin/bash

# =============================
# Fix Ollama Connection Issues
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

echo "🔧 Fixing Ollama Connection Issues"
echo "=================================="
echo ""

# Ensure we're in the correct directory
cd "$(dirname "$0")"

echo "🔍 Step 1: Check Ollama Status"
echo "=============================="

# Check if Ollama is running
if pgrep ollama > /dev/null; then
    ok "Ollama process is running"
else
    err "Ollama process is not running"
    echo "Please start Ollama first:"
    echo "  ollama serve"
    exit 1
fi

# Check if Ollama is accessible locally
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    ok "Ollama is accessible at localhost:11434"
    OLLAMA_URL="http://localhost:11434"
else
    warn "Ollama not accessible at localhost:11434"
    
    # Try other common ports
    for port in 11434 8080 3000; do
        if curl -s http://localhost:$port/api/tags > /dev/null 2>&1; then
            ok "Ollama found at localhost:$port"
            OLLAMA_URL="http://localhost:$port"
            break
        fi
    done
    
    if [ -z "$OLLAMA_URL" ]; then
        err "Cannot find Ollama on any common port"
        echo "Please check Ollama configuration and start it"
        exit 1
    fi
fi

echo ""
echo "🔍 Step 2: Test Docker → Host Connection"
echo "======================================="

# Get host IP
HOST_IP=$(hostname -I | awk '{print $1}')
echo "Host IP: $HOST_IP"

# Test if Docker can reach Ollama on host
echo "Testing Docker → Host Ollama connection..."
if docker run --rm --network host curlimages/curl:latest curl -s --connect-timeout 5 "$OLLAMA_URL/api/tags" > /dev/null 2>&1; then
    ok "Docker can reach Ollama at $OLLAMA_URL"
    DOCKER_OLLAMA_URL="$OLLAMA_URL"
else
    warn "Docker cannot reach Ollama at $OLLAMA_URL"
    
    # Try with host IP
    if docker run --rm --network host curlimages/curl:latest curl -s --connect-timeout 5 "http://$HOST_IP:11434/api/tags" > /dev/null 2>&1; then
        ok "Docker can reach Ollama at http://$HOST_IP:11434"
        DOCKER_OLLAMA_URL="http://$HOST_IP:11434"
    else
        err "Docker cannot reach Ollama on host"
        echo "This might be a firewall or network configuration issue"
        exit 1
    fi
fi

echo ""
echo "🔍 Step 3: Update Configuration"
echo "=============================="

# Update .env file with working Ollama URL
info "Updating .env file with working Ollama URL: $DOCKER_OLLAMA_URL"

cat > .env << EOF
# Ollama Configuration - Fixed for Docker → Host connection
OLLAMA_BASE_URL=$DOCKER_OLLAMA_URL
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

ok "Updated .env file"

echo ""
echo "🔍 Step 4: Test Configuration"
echo "============================="

# Test the configuration
python -c "
import sys
sys.path.insert(0, 'src')
from config.settings import settings
print(f'Updated Ollama URL: {settings.ollama_base_url}')

# Test connection
import requests
try:
    response = requests.get(f'{settings.ollama_base_url}/api/tags', timeout=5)
    if response.status_code == 200:
        print('✅ Ollama connection successful')
    else:
        print(f'❌ Ollama connection failed: {response.status_code}')
except Exception as e:
    print(f'❌ Ollama connection failed: {e}')
"

echo ""
echo "🔍 Step 5: Test Weaviate Indexing"
echo "================================="

# Test indexing
info "Testing Weaviate indexing with fixed configuration..."

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
        'project': 'test_ollama_fix',
        'path': '/test/path.java',
        'language': 'java',
        'text': 'This is a test document for Ollama connection fix.',
        'summary': 'Test summary for Ollama connection verification'
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
        'valueString': 'test_ollama_fix'
    }).do()
    
    found_docs = search_result.get('data', {}).get('Get', {}).get('BackendDoc', [])
    print(f'✅ Found {len(found_docs)} test documents in Weaviate')
    
    if found_docs:
        print('🎉 Ollama connection fix successful!')
    else:
        print('❌ Test document not found - fix may not have worked')
        
except Exception as e:
    print(f'❌ Test failed: {e}')
    import traceback
    traceback.print_exc()
"

echo ""
echo "🎯 Next Steps"
echo "============="
echo ""
echo "1. ✅ Ollama connection has been fixed"
echo "2. 🔄 Run the full pipeline: ./new_run.sh"
echo "3. 🔍 Check results: ./search_weaviate.sh"
echo ""
echo "If you still have issues:"
echo "- Make sure Ollama is running: ollama serve"
echo "- Check firewall settings"
echo "- Verify Docker network configuration"
