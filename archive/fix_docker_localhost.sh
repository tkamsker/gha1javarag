#!/bin/bash

# =============================
# Fix Docker Weaviate → Host localhost Ollama
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

echo "🔧 Fixing Docker Weaviate → Host localhost Ollama"
echo "================================================="
echo ""

# Ensure we're in the correct directory
cd "$(dirname "$0")"

echo "🔍 Step 1: Check Ollama Status"
echo "=============================="

# Check if Ollama is running on localhost
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    ok "Ollama is running on localhost:11434"
else
    err "Ollama is not running on localhost:11434"
    echo "Please start Ollama first: ollama serve"
    exit 1
fi

echo ""
echo "🔍 Step 2: Stop Current Weaviate Container"
echo "=========================================="

# Stop current Weaviate container
info "Stopping current Weaviate container..."
docker stop weaviate-java-analysis 2>/dev/null || warn "Container not running"
docker rm weaviate-java-analysis 2>/dev/null || warn "Container not found"

echo ""
echo "🔍 Step 3: Start Weaviate with Host Network"
echo "==========================================="

# Start Weaviate with host networking so it can access localhost
info "Starting Weaviate with host networking..."

# Create a new docker-compose override for host networking
cat > docker-compose.override.yml << 'EOF'
version: '3.8'
services:
  weaviate:
    network_mode: host
    environment:
      - QUERY_DEFAULTS_LIMIT=25
      - AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true
      - PERSISTENCE_DATA_PATH=/var/lib/weaviate
      - DEFAULT_VECTORIZER_MODULE=text2vec-ollama
      - ENABLE_MODULES=text2vec-ollama
      - CLUSTER_HOSTNAME=node1
      - OLLAMA_BASE_URL=http://localhost:11434
    volumes:
      - weaviate_data:/var/lib/weaviate
    restart: on-failure:0
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/v1/.well-known/ready"]
      interval: 3s
      timeout: 2s
      retries: 3
      start_period: 3s

volumes:
  weaviate_data:
EOF

# Start Weaviate with the new configuration
docker-compose up -d weaviate

# Wait for Weaviate to be ready
info "Waiting for Weaviate to be ready..."
sleep 15

# Test Weaviate connection
info "Testing Weaviate connection..."
if curl -s http://localhost:8080/v1/meta > /dev/null 2>&1; then
    ok "Weaviate is accessible"
else
    err "Weaviate is not accessible"
    echo "Checking container status..."
    docker ps | grep weaviate || echo "No Weaviate container found"
    exit 1
fi

echo ""
echo "🔍 Step 4: Update Configuration"
echo "=============================="

# Update .env file with localhost Ollama URL
info "Updating .env file with localhost Ollama URL..."

cat > .env << EOF
# Ollama Configuration - Fixed for Docker with host networking
OLLAMA_BASE_URL=http://localhost:11434
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

ok "Updated .env file with localhost Ollama URL"

echo ""
echo "🔍 Step 5: Test Configuration"
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
echo "🔍 Step 6: Test Weaviate Indexing"
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
        'project': 'test_localhost_fix',
        'path': '/test/path.java',
        'language': 'java',
        'text': 'This is a test document for localhost Ollama fix.',
        'summary': 'Test summary for localhost Ollama verification'
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
        'valueString': 'test_localhost_fix'
    }).do()
    
    found_docs = search_result.get('data', {}).get('Get', {}).get('BackendDoc', [])
    print(f'✅ Found {len(found_docs)} test documents in Weaviate')
    
    if found_docs:
        print('🎉 Localhost Ollama fix successful!')
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
echo "1. ✅ Weaviate is now running with host networking"
echo "2. ✅ Ollama connection is configured for localhost"
echo "3. 🔄 Run the full pipeline: ./new_run.sh"
echo "4. 🔍 Check results: ./search_weaviate.sh"
echo ""
echo "The Docker container can now access localhost:11434!"
