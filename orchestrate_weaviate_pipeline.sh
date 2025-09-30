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

# Helper to run a step and stop on failure while printing an error message
run_step() {
  local step_name="$1"
  shift
  echo "\n▶️  ${step_name}"
  set +e
  bash -c "$*"
  local rc=$?
  set -e
  if [ $rc -ne 0 ]; then
    echo "❌ ${step_name} failed with exit code ${rc}. Aborting subsequent steps."
    exit $rc
  fi
}

# Helper to archive current output directory with a datetime suffix
archive_output() {
  local ts
  ts="$(date +%Y%m%d_%H%M%S)"
  local src="./output"
  local dst="output_${ts}"
  if [ -d "$src" ]; then
    echo "🗄️  Archiving output to ${dst}"
    mkdir -p "$dst"
    # Copy contents preserving attributes
    cp -a "$src/." "$dst/"
  else
    echo "ℹ️  No output directory to archive (${src} not found)"
  fi
}

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

run_step "Step 1: Enhanced Weaviate analysis" "./Step1_Enhanced_Weaviate.sh $MODE"

if [ -x "Step2_Enhanced_Weaviate.sh" ]; then
  run_step "Step 2: Enhanced Weaviate follow-up" "./Step2_Enhanced_Weaviate.sh $MODE"
else
  echo "ℹ️  Skipping Step2_Enhanced_Weaviate.sh (not found or not executable)"
fi

if [ -x "Step3_Enhanced_Weaviate.sh" ]; then
  run_step "Step 3: Weaviate finalization (Enhanced)" "./Step3_Enhanced_Weaviate.sh $MODE"
elif [ -x "Step3_Weaviate.sh" ]; then
  run_step "Step 3: Weaviate finalization" "./Step3_Weaviate.sh $MODE"
else
  echo "ℹ️  Skipping Step 3 (script not found or not executable)"
fi

# If test mode requested, rerun the pipeline in production to validate
if [ "$MODE" = "test" ]; then
  # Archive test run outputs before production rerun
  archive_output
  echo "\n🔁 Test mode complete. Re-running full pipeline in production mode for verification..."
  "$0" production
else
  # Archive production run outputs
  archive_output
fi

echo "\n🎉 Orchestration completed for mode: $MODE"

