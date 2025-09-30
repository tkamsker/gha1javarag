#!/bin/bash

# Orchestrator for Weaviate pipeline
# Usage: ./orchestrate_weaviate_pipeline.sh [test|production]

set -euo pipefail

MODE=${1:-}

print_usage() {
  echo "Usage: $0 [test|production]"
}

if [ -z "$MODE" ]; then
  echo "❌ Missing parameter."
  print_usage
  exit 1
fi

case "$MODE" in
  test|production)
    ;;
  *)
    echo "❌ Invalid mode: $MODE"
    print_usage
    exit 1
    ;;
esac

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

echo "🚀 Orchestrating Weaviate pipeline in mode: $MODE"
echo "Root: $ROOT_DIR"

# Ensure Docker is available
if ! command -v docker >/dev/null 2>&1; then
  echo "❌ Docker is required. Please install and start Docker."
  exit 1
fi

# Reset Weaviate running in Docker
echo "🧹 Resetting Weaviate Docker state..."
if docker ps -a --format '{{.Names}}' | grep -q '^weaviate$'; then
  echo "⏹️  Stopping existing 'weaviate' container..."
  docker rm -f weaviate >/dev/null 2>&1 || true
fi

# Remove optional data volume to fully reset database
if docker volume ls --format '{{.Name}}' | grep -q '^weaviate_data$'; then
  echo "🗑️  Removing Docker volume 'weaviate_data'..."
  docker volume rm weaviate_data >/dev/null 2>&1 || true
fi

echo "▶️  Starting fresh Weaviate container..."
docker run -d --name weaviate \
  -p 8080:8080 -p 50051:50051 \
  -e QUERY_DEFAULTS_LIMIT=25 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \
  -v weaviate_data:/var/lib/weaviate \
  semitechnologies/weaviate:latest >/dev/null

echo "⏳ Waiting for Weaviate to become ready..."
for i in {1..60}; do
  if curl -s http://localhost:8080/v1/meta >/dev/null 2>&1; then
    echo "✅ Weaviate is ready"
    break
  fi
  sleep 1
  if [ "$i" -eq 60 ]; then
    echo "❌ Weaviate did not become ready in time"
    exit 1
  fi
done

# Activate venv if present
if [ -f "venv/bin/activate" ]; then
  # shellcheck disable=SC1091
  source "venv/bin/activate"
fi

export RATE_LIMIT_ENV="$MODE"
export OUTPUT_DIR="./output"

echo "\n▶️  Step 1: Enhanced Weaviate analysis"
bash Step1_Enhanced_Weaviate.sh "$MODE"

echo "\n▶️  Step 2: Enhanced Weaviate follow-up"
if [ -x "Step2_Enhanced_Weaviate.sh" ]; then
  bash Step2_Enhanced_Weaviate.sh "$MODE"
else
  echo "ℹ️  Skipping Step2_Enhanced_Weaviate.sh (not found or not executable)"
fi

echo "\n▶️  Step 3: Weaviate finalization"
if [ -x "Step3_Enhanced_Weaviate.sh" ]; then
  bash Step3_Enhanced_Weaviate.sh "$MODE"
elif [ -x "Step3_Weaviate.sh" ]; then
  bash Step3_Weaviate.sh "$MODE"
else
  echo "ℹ️  Skipping Step 3 (script not found or not executable)"
fi

# If test mode requested, rerun the pipeline in production to validate
if [ "$MODE" = "test" ]; then
  echo "\n🔁 Test mode complete. Re-running full pipeline in production mode for verification..."
  "$0" production
fi

echo "\n🎉 Orchestration completed for mode: $MODE"

