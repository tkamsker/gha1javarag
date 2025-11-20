#!/bin/bash

# =============================
# Fix Docker Weaviate → Host Ollama Connection
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

echo "🔧 Fixing Docker Weaviate → Host Ollama Connection"
echo "=================================================="
echo ""

# Ensure we're in the correct directory
cd "$(dirname "$0")"

echo "🔍 Step 1: Check Current Setup"
echo "=============================="

# Check if Weaviate is running in Docker
if docker ps | grep -q weaviate; then
    ok "Weaviate is running in Docker"
    docker ps | grep weaviate
else
    err "Weaviate container not found"
    exit 1
fi

# Check if Ollama is running on host
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    ok "Ollama is running on host at localhost:11434"
else
    warn "Ollama not accessible at localhost:11434"
    echo "Checking if Ollama is running..."
    if pgrep ollama > /dev/null; then
        ok "Ollama process is running"
    else
        err "Ollama is not running. Please start it first."
        exit 1
    fi
fi

echo ""
echo "🔍 Step 2: Find Host IP for Docker Container"
echo "============================================"

# Get the host IP that Docker containers can reach
HOST_IP=$(ip route show default | awk '/default/ {print $3}')
echo "Host IP (from Docker perspective): $HOST_IP"

# Alternative method
HOST_IP_ALT=$(hostname -I | awk '{print $1}')
echo "Alternative host IP: $HOST_IP_ALT"

# Test which IP works from inside Docker
echo "Testing connectivity from Docker container..."
docker run --rm --network host curlimages/curl:latest curl -s --connect-timeout 5 "http://$HOST_IP:11434/api/tags" > /dev/null 2>&1 && echo "✅ $HOST_IP works" || echo "❌ $HOST_IP failed"
docker run --rm --network host curlimages/curl:latest curl -s --connect-timeout 5 "http://$HOST_IP_ALT:11434/api/tags" > /dev/null 2>&1 && echo "✅ $HOST_IP_ALT works" || echo "❌ $HOST_IP_ALT failed"

# Use the working IP
if docker run --rm --network host curlimages/curl:latest curl -s --connect-timeout 5 "http://$HOST_IP:11434/api/tags" > /dev/null 2>&1; then
    WORKING_IP="$HOST_IP"
elif docker run --rm --network host curlimages/curl:latest curl -s --connect-timeout 5 "http://$HOST_IP_ALT:11434/api/tags" > /dev/null 2>&1; then
    WORKING_IP="$HOST_IP_ALT"
else
    # Try localhost
    if docker run --rm --network host curlimages/curl:latest curl -s --connect-timeout 5 "http://localhost:11434/api/tags" > /dev/null 2>&1; then
        WORKING_IP="localhost"
    else
        err "Cannot reach Ollama from Docker container"
        exit 1
    fi
fi

echo "Using IP: $WORKING_IP"

echo ""
echo "🔍 Step 3: Create Fixed Configuration"
echo "====================================="

# Create .env file with the correct Ollama URL for Docker
info "Creating .env file with Docker-compatible Ollama URL..."

cat > .env << EOF
# Ollama Configuration - Fixed for Docker → Host connection
OLLAMA_BASE_URL=http://$WORKING_IP:11434
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

ok "Created .env file with Ollama URL: http://$WORKING_IP:11434"

echo ""
echo "🔍 Step 4: Test Configuration"
echo "============================="

# Test the new configuration
info "Testing new configuration..."
python -c "
import sys
sys.path.insert(0, 'src')
from config.settings import settings
print(f'Ollama URL: {settings.ollama_base_url}')

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

# Test indexing with the fixed configuration
info "Testing Weaviate indexing with fixed configuration..."

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
        'project': 'test_docker_fix',
        'path': '/test/path.java',
        'language': 'java',
        'text': 'This is a test document for Docker Ollama configuration fix.',
        'summary': 'Test summary for Docker configuration verification'
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
        'valueString': 'test_docker_fix'
    }).do()
    
    found_docs = search_result.get('data', {}).get('Get', {}).get('BackendDoc', [])
    print(f'✅ Found {len(found_docs)} test documents in Weaviate')
    
    if found_docs:
        print('🎉 Docker Ollama configuration fix successful!')
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
echo "1. ✅ Docker Ollama configuration has been fixed"
echo "2. 🔄 Run the full pipeline: ./new_run.sh"
echo "3. 🔍 Check results: ./search_weaviate.sh"
echo ""
echo "If you still have issues:"
echo "- Check that your Java source directory is correct in .env"
echo "- Verify Ollama is running on the host"
echo "- Run ./test_indexing.sh to debug further"
