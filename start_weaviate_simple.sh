#!/bin/bash

# =============================
# Simple Weaviate Start Script
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

echo "🚀 Simple Weaviate Start"
echo "======================="
echo ""

# Ensure we're in the correct directory
cd "$(dirname "$0")"

echo "🔍 Step 1: Check Docker Status"
echo "=============================="

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    err "Docker is not running. Please start Docker Desktop."
    exit 1
fi
ok "Docker is running"

# Check available resources
info "Checking Docker resources..."
docker system df

echo ""
echo "🔍 Step 2: Stop Existing Containers"
echo "==================================="

# Stop any existing Weaviate containers
info "Stopping existing Weaviate containers..."
docker stop weaviate-java-analysis 2>/dev/null || warn "No existing container to stop"
docker rm weaviate-java-analysis 2>/dev/null || warn "No existing container to remove"

echo ""
echo "🔍 Step 3: Check Ollama Status"
echo "=============================="

# Check if Ollama is running
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    ok "Ollama is running on localhost:11434"
else
    warn "Ollama is not running on localhost:11434"
    echo "Please start Ollama first: ollama serve"
    echo "Or run: brew services start ollama"
fi

echo ""
echo "🔍 Step 4: Start Weaviate (macOS)"
echo "================================="

# Start Weaviate with macOS configuration
info "Starting Weaviate with macOS configuration..."

# Use direct docker run command instead of docker-compose
docker run -d \
  --name weaviate-java-analysis \
  -p 8080:8080 \
  -p 50051:50051 \
  --add-host host.docker.internal:host-gateway \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \
  -e ENABLE_MODULES=text2vec-ollama,generative-ollama \
  -e DEFAULT_VECTORIZER_MODULE=text2vec-ollama \
  -e OLLAMA_API_ENDPOINT=http://host.docker.internal:11434 \
  -e ENABLE_CORS=true \
  -e CORS_ALLOWED_ORIGINS="*" \
  -e CLUSTER_HOSTNAME=node1 \
  -e QUERY_DEFAULTS_LIMIT=25 \
  -v "$(pwd)/weaviate-data:/var/lib/weaviate" \
  semitechnologies/weaviate:latest

ok "Weaviate container started"

echo ""
echo "🔍 Step 5: Wait for Weaviate to be Ready"
echo "========================================"

# Wait for Weaviate to be ready
info "Waiting for Weaviate to be ready..."
sleep 10

# Test connection with retries
for i in {1..5}; do
    if curl -s http://localhost:8080/v1/meta > /dev/null 2>&1; then
        ok "Weaviate is ready and accessible"
        break
    else
        warn "Weaviate not ready yet, attempt $i/5..."
        sleep 5
    fi
done

echo ""
echo "🔍 Step 6: Test Connection"
echo "========================="

# Test Weaviate connection
if curl -s http://localhost:8080/v1/meta > /dev/null 2>&1; then
    ok "Weaviate API is accessible"
    
    # Test Ollama connection from Weaviate perspective
    info "Testing Ollama connection from Weaviate..."
    if docker exec weaviate-java-analysis curl -s http://host.docker.internal:11434/api/tags > /dev/null 2>&1; then
        ok "Ollama is accessible from Weaviate container"
    else
        warn "Ollama is not accessible from Weaviate container"
        echo "This may cause indexing issues"
    fi
else
    err "Weaviate API is not accessible"
    echo "Check container logs: docker logs weaviate-java-analysis"
    exit 1
fi

echo ""
echo "🎉 Weaviate is Ready!"
echo "===================="
echo ""
echo "✅ Weaviate is running on http://localhost:8080"
echo "✅ Ready for indexing and searching"
echo ""
echo "Next steps:"
echo "1. Test indexing: python main.py index --project test"
echo "2. Search data: ./search_weaviate.sh"
echo "3. Run full pipeline: ./new_run.sh"
