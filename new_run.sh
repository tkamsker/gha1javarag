#!/bin/bash

# =============================
# Full run with timestamped project and fresh Weaviate
# =============================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info(){ echo -e "${BLUE}[INFO]${NC} $1"; }
ok(){ echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warn(){ echo -e "${YELLOW}[WARNING]${NC} $1"; }
err(){ echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# Ensure venv
if [ -z "$VIRTUAL_ENV" ]; then
  err "No virtual environment detected. Activate with: source venv/bin/activate"
fi

# Use venv python explicitly
PYTHON_CMD="$VIRTUAL_ENV/bin/python"
if [ ! -f "$PYTHON_CMD" ]; then
  err "Virtual environment Python not found at $PYTHON_CMD"
fi

# Timestamped project name
TS=$(date +%Y%m%d_%H%M%S)
PROJECT="$TS"
info "Project name: $PROJECT"

# Start fresh Weaviate (clean)
info "Resetting Weaviate container and data..."
./docker-weaviate.sh clean || true
./docker-weaviate.sh || err "Failed to start Weaviate"

# Quick wait to ensure modules are up
sleep 2

# Pull required Ollama models if missing (generation + embed)
GEN_MODEL=${OLLAMA_MODEL_NAME:-gemma3:12b}
EMB_MODEL=${OLLAMA_EMBED_MODEL_NAME:-nomic-embed-text}
if command -v ollama >/dev/null 2>&1; then
  if ! ollama list | grep -q "$GEN_MODEL"; then
    info "Pulling generation model: $GEN_MODEL"; ollama pull "$GEN_MODEL" || warn "Model pull failed; continuing"; fi
  if ! ollama list | grep -q "$EMB_MODEL"; then
    info "Pulling embedding model: $EMB_MODEL"; ollama pull "$EMB_MODEL" || warn "Embed model pull failed; continuing"; fi
else
  warn "Ollama not found; ensure it's installed and running."
fi

# Ensure we're in the correct directory
cd "$(dirname "$0")"

# Test Python imports
info "Testing Python imports..."
$PYTHON_CMD -c "import sys; sys.path.insert(0, 'src'); from store.weaviate_client import WeaviateClient; print('Imports OK')" || err "Python imports failed"

# Run pipeline: discover, extract, index, prd
info "Running discover..."
$PYTHON_CMD main.py discover --project "$PROJECT" --include-frontend || err "discover failed"

info "Running extract..."
$PYTHON_CMD main.py extract --project "$PROJECT" --include-frontend || err "extract failed"

info "Running index..."
$PYTHON_CMD main.py index --project "$PROJECT" || err "index failed"

info "Generating PRD..."
$PYTHON_CMD main.py prd --project "$PROJECT" --frontend || warn "PRD generation completed with warnings"

ok "Full run complete"
echo "Project: $PROJECT"
echo "PRD: data/output/${PROJECT}_prd.md"

