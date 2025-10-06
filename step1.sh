#!/bin/bash

set -e

# Step 1: Analyze and export consolidated JSON (optionally upsert to Weaviate)

print_status() { echo "[INFO] $1"; }
print_error() { echo "[ERROR] $1"; }

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

if [ ! -d "venv" ]; then
  print_status "Creating Python virtual environment..."
  python3 -m venv venv
fi

print_status "Activating virtual environment..."
source venv/bin/activate

print_status "Installing dependencies..."
pip install --upgrade pip >/dev/null
pip install -r requirements.txt >/dev/null

if [ ! -f ".env" ]; then
  print_error ".env not found. Please create it (cp .env.example .env)"
  exit 1
fi

# Ensure OUTPUT_DIR exists; if not set in .env, append once
if ! grep -q '^OUTPUT_DIR=' .env; then
  TS=$(date +"%Y%m%d_%H%M%S")
  echo "OUTPUT_DIR=./output_${TS}" >> .env
fi
OUT_DIR=$(grep '^OUTPUT_DIR=' .env | cut -d'=' -f2)
mkdir -p "$OUT_DIR"

print_status "Running analysis (Step 1) ..."

# Allow --no-upsert via env STEP1_NO_UPSERT=1
if [ "$STEP1_NO_UPSERT" = "1" ]; then
  python -m src.cli --verbose analyze --no-upsert
else
  python -m src.cli --verbose analyze
fi

# Write completion marker for run_iteration.sh to detect reuse
MARKER_FILE="$OUT_DIR/.step1_complete"
echo "completed_at=$(date -Is)" > "$MARKER_FILE"
echo "source_dir=$(grep '^JAVA_SOURCE_DIR=' .env | cut -d'=' -f2)" >> "$MARKER_FILE"

print_status "Step 1 completed. Consolidated JSON should be in \"$OUT_DIR/consolidated_metadata.json\""


