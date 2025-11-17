#!/bin/bash
# Fix Weaviate schema endpoint issue on Linux
# This script deletes all schema classes and restarts Weaviate with the correct Ubuntu configuration

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info(){ echo -e "${BLUE}[INFO]${NC} $1"; }
ok(){ echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warn(){ echo -e "${YELLOW}[WARNING]${NC} $1"; }
err(){ echo -e "${RED}[ERROR]${NC} $1"; }

WEAVIATE_URL="${WEAVIATE_URL:-http://localhost:8080}"

# List of all schema classes that need to be deleted
CLASSES=(
    "IbatisStatement"
    "DaoCall"
    "JspForm"
    "DbTable"
    "GwtModule"
    "GwtUiBinder"
    "GwtActivityPlace"
    "GwtEndpoint"
    "JsArtifact"
    "BackendDoc"
)

info "Fixing Weaviate schema endpoint for Linux production..."
info "This will delete all existing schema classes and restart Weaviate with the correct configuration."

# Check if Weaviate is accessible
if ! curl -s "${WEAVIATE_URL}/v1/meta" > /dev/null 2>&1; then
    warn "Weaviate is not accessible at ${WEAVIATE_URL}"
    warn "Attempting to start Weaviate..."
    if [ -f "./docker-weaviate.sh" ]; then
        ./docker-weaviate.sh start ubuntu
        sleep 5
        if ! curl -s "${WEAVIATE_URL}/v1/meta" > /dev/null 2>&1; then
            err "Failed to start Weaviate. Please check docker-weaviate.sh"
            exit 1
        fi
    else
        err "docker-weaviate.sh not found. Please start Weaviate manually."
        exit 1
    fi
fi

ok "Weaviate is accessible"

# Delete all schema classes
info "Deleting existing schema classes..."
for class in "${CLASSES[@]}"; do
    info "Deleting class: ${class}"
    response=$(curl -s -w "\n%{http_code}" -X DELETE "${WEAVIATE_URL}/v1/schema/${class}")
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "200" ] || [ "$http_code" = "204" ]; then
        ok "Deleted class: ${class}"
    elif echo "$body" | grep -q "not found\|does not exist"; then
        warn "Class ${class} does not exist (already deleted or never created)"
    else
        warn "Failed to delete class ${class} (HTTP ${http_code}): ${body}"
    fi
done

ok "Schema classes deleted"

# Restart Weaviate with Ubuntu configuration
info "Restarting Weaviate with Ubuntu configuration..."
if [ -f "./docker-weaviate.sh" ]; then
    ./docker-weaviate.sh restart ubuntu
    sleep 10
    
    # Verify Weaviate is running
    if curl -s "${WEAVIATE_URL}/v1/meta" > /dev/null 2>&1; then
        ok "Weaviate restarted successfully"
    else
        err "Weaviate failed to start after restart"
        exit 1
    fi
else
    warn "docker-weaviate.sh not found. Please restart Weaviate manually with:"
    warn "  docker-compose -f docker-compose.ubuntu.yml restart"
fi

# Verify environment variables in container
info "Verifying Weaviate container environment variables..."
if docker exec weaviate-i17 env | grep -q "OLLAMA_API_ENDPOINT=http://127.0.0.1:11434"; then
    ok "Weaviate container has correct OLLAMA_API_ENDPOINT"
else
    warn "Weaviate container may not have correct OLLAMA_API_ENDPOINT"
    warn "Expected: OLLAMA_API_ENDPOINT=http://127.0.0.1:11434"
    docker exec weaviate-i17 env | grep OLLAMA || warn "No OLLAMA environment variables found"
fi

# Test Ollama connectivity from container
info "Testing Ollama connectivity from Weaviate container..."
if docker exec weaviate-i17 curl -s http://127.0.0.1:11434/api/tags > /dev/null 2>&1; then
    ok "Ollama is accessible from Weaviate container"
else
    warn "Ollama is not accessible from Weaviate container"
    warn "Make sure Ollama is running on the host: ollama serve"
fi

ok "Schema fix complete!"
info ""
info "Next steps:"
info "1. Run indexing to recreate schema with correct endpoint:"
info "   python main.py index --project <project-name>"
info ""
info "2. Or run the full pipeline:"
info "   python main.py all --project <project-name>"

