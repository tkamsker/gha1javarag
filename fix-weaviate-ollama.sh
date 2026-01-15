#!/bin/bash
# ==============================================================================
# Fix Weaviate + Ollama Integration
# ==============================================================================
# Resolves: "vectorizer: no module with name text2vec-ollama present"
#
# This script:
# 1. Checks if Ollama is running
# 2. Verifies Ollama model is available
# 3. Stops ALL Weaviate containers (including non-compose managed)
# 4. Ensures port 8080 is free
# 5. Restarts Weaviate with text2vec-ollama module enabled
# 6. Verifies Weaviate can connect to Ollama
#
# Compatibility: macOS and Ubuntu/Linux
# Usage: ./fix-weaviate-ollama.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info() { echo -e "${BLUE}[INFO]${NC} $1"; }
ok() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
err() { echo -e "${RED}[ERROR]${NC} $1"; }

echo "========================================"
echo "Weaviate + Ollama Integration Fix"
echo "========================================"
echo ""

# ==============================================================================
# Step 1: Check Ollama is running
# ==============================================================================
info "Checking if Ollama is running..."

if curl -s http://localhost:11434/ >/dev/null 2>&1; then
    ok "Ollama is running at http://localhost:11434"
else
    err "Ollama is NOT running!"
    echo ""
    echo "Please start Ollama first:"
    echo "  Option 1: Run 'ollama serve' in a separate terminal"
    echo "  Option 2: Start Ollama app (if using desktop version)"
    echo ""
    echo "After starting Ollama, run this script again."
    exit 1
fi

echo ""

# ==============================================================================
# Step 2: Check required models are available
# ==============================================================================
info "Checking if required models are available..."

# Check embedding model
if ollama list | grep -q "nomic-embed-text"; then
    ok "Embedding model 'nomic-embed-text' is available"
else
    warn "Embedding model 'nomic-embed-text' not found"
    info "Pulling nomic-embed-text model..."
    ollama pull nomic-embed-text
    ok "nomic-embed-text model downloaded"
fi

# Check LLM model
if ollama list | grep -q "gemma3:12b"; then
    ok "LLM model 'gemma3:12b' is available"
else
    warn "LLM model 'gemma3:12b' not found"
    info "Pulling gemma3:12b model (this may take a while)..."
    ollama pull gemma2:12b || ollama pull gemma3:12b
    ok "gemma model downloaded"
fi

echo ""

# ==============================================================================
# Step 3: Stop and clean ALL Weaviate containers
# ==============================================================================
info "Stopping all Weaviate containers to apply new configuration..."

# Stop any running Weaviate containers (not just docker-compose managed ones)
# Use name filter to catch all Weaviate containers regardless of image version
WEAVIATE_CONTAINERS=$(docker ps -q --filter "name=weaviate")
if [ -n "$WEAVIATE_CONTAINERS" ]; then
    info "Found running Weaviate containers, stopping them..."
    echo "$WEAVIATE_CONTAINERS" | xargs docker stop
    ok "All Weaviate containers stopped"
else
    info "No running Weaviate containers found (by name)"
fi

# Also check by image name pattern (catches containers without 'weaviate' in name)
IMAGE_CONTAINERS=$(docker ps -q | xargs -I {} docker inspect --format='{{.Id}} {{.Config.Image}}' {} 2>/dev/null | grep -i weaviate | awk '{print $1}')
if [ -n "$IMAGE_CONTAINERS" ]; then
    info "Found additional Weaviate containers by image, stopping them..."
    echo "$IMAGE_CONTAINERS" | xargs docker stop 2>/dev/null || true
fi

# Now stop docker-compose managed container
./docker-weaviate.sh stop || true

# Remove any stopped Weaviate containers to free port 8080
info "Removing stopped Weaviate containers..."
ALL_WEAVIATE=$(docker ps -aq --filter "name=weaviate")
if [ -n "$ALL_WEAVIATE" ]; then
    echo "$ALL_WEAVIATE" | xargs docker rm -f 2>/dev/null || true
    ok "Removed stopped Weaviate containers"
fi

# Also remove by image pattern
ALL_IMAGE_CONTAINERS=$(docker ps -aq | xargs -I {} docker inspect --format='{{.Id}} {{.Config.Image}}' {} 2>/dev/null | grep -i weaviate | awk '{print $1}')
if [ -n "$ALL_IMAGE_CONTAINERS" ]; then
    echo "$ALL_IMAGE_CONTAINERS" | xargs docker rm -f 2>/dev/null || true
fi

# Give it a moment to fully stop and release port
sleep 3

# Verify port 8080 is free
info "Verifying port 8080 is available..."
if command -v lsof >/dev/null 2>&1; then
    # macOS/BSD systems
    PORT_USED=$(lsof -ti :8080 2>/dev/null || true)
elif command -v ss >/dev/null 2>&1; then
    # Linux systems
    PORT_USED=$(ss -tuln | grep ":8080 " || true)
else
    warn "Cannot check port availability (lsof/ss not found)"
    PORT_USED=""
fi

if [ -n "$PORT_USED" ]; then
    err "Port 8080 is still in use!"
    echo ""
    echo "Please free port 8080 before continuing:"
    if command -v lsof >/dev/null 2>&1; then
        echo "  lsof -ti :8080 | xargs kill -9"
    else
        echo "  Check what's using the port: ss -tuln | grep :8080"
    fi
    exit 1
fi

ok "Port 8080 is available"
echo ""

# ==============================================================================
# Step 4: Start Weaviate with text2vec-ollama enabled
# ==============================================================================
info "Starting Weaviate with text2vec-ollama module enabled..."

./docker-weaviate.sh start

# Wait for Weaviate to be ready
info "Waiting for Weaviate to be ready..."
RETRIES=0
MAX_RETRIES=30

until curl -sf http://localhost:8080/v1/meta > /dev/null; do
    RETRIES=$((RETRIES+1))
    if [ $RETRIES -ge $MAX_RETRIES ]; then
        err "Weaviate failed to start after ${MAX_RETRIES} attempts"
        echo ""
        echo "Check logs with: ./docker-weaviate.sh logs"
        exit 1
    fi
    echo "Waiting for Weaviate... (attempt $RETRIES/$MAX_RETRIES)"
    sleep 2
done

ok "Weaviate is running and ready"
echo ""

# ==============================================================================
# Step 5: Verify Weaviate configuration
# ==============================================================================
info "Verifying Weaviate configuration..."

# Check if text2vec-ollama module is enabled
MODULES=$(curl -s http://localhost:8080/v1/meta | jq -r '.modules | keys[]' 2>/dev/null || echo "")

if echo "$MODULES" | grep -q "text2vec-ollama"; then
    ok "text2vec-ollama module is enabled"
else
    err "text2vec-ollama module NOT enabled"
    echo ""
    echo "Modules found: $MODULES"
    echo ""
    echo "Troubleshooting:"
    echo "1. Check docker-compose.macos.yml has:"
    echo "   ENABLE_MODULES: \"text2vec-ollama,generative-ollama\""
    echo "2. Check logs: ./docker-weaviate.sh logs"
    exit 1
fi

# Check if Weaviate can reach Ollama
info "Testing Weaviate → Ollama connection..."

# Try to create a test schema (will be cleaned up)
TEST_RESULT=$(curl -s -X POST http://localhost:8080/v1/schema \
    -H "Content-Type: application/json" \
    -d '{
        "class": "TestConnection",
        "vectorizer": "text2vec-ollama",
        "moduleConfig": {
            "text2vec-ollama": {
                "apiEndpoint": "http://host.docker.internal:11434",
                "model": "nomic-embed-text"
            }
        }
    }' 2>&1)

if echo "$TEST_RESULT" | grep -q '"class":"TestConnection"'; then
    ok "Weaviate can connect to Ollama successfully"

    # Clean up test schema
    curl -s -X DELETE http://localhost:8080/v1/schema/TestConnection > /dev/null 2>&1 || true
elif echo "$TEST_RESULT" | grep -q "already exists"; then
    warn "Test schema already exists (cleaning up)"
    curl -s -X DELETE http://localhost:8080/v1/schema/TestConnection > /dev/null 2>&1 || true
    ok "Weaviate can connect to Ollama successfully"
else
    err "Weaviate cannot connect to Ollama"
    echo ""
    echo "Error: $TEST_RESULT"
    echo ""
    echo "Troubleshooting:"
    echo "1. Verify Ollama is accessible from Docker:"
    echo "   docker exec weaviate-i19 curl -v http://host.docker.internal:11434/"
    echo "2. Check docker-compose.macos.yml has correct Ollama endpoint"
    exit 1
fi

echo ""

# ==============================================================================
# Step 6: Verify complete setup
# ==============================================================================
info "Running final verification..."

./check-services.sh

echo ""
echo "========================================"
ok "Setup Complete!"
echo "========================================"
echo ""
echo "You can now run Streamlit:"
echo "  streamlit run src/codeindex/web/app.py"
echo ""
echo "Or check the status:"
echo "  ./check-services.sh"
echo ""
