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

# Ensure timestamped OUTPUT_DIR for this run if not set
if ! grep -q '^OUTPUT_DIR=' .env; then
  TS=$(date +"%Y%m%d_%H%M%S")
  echo "OUTPUT_DIR=./output_${TS}" >> .env
fi

print_status "Running analysis (Step 1) ..."

# Allow --no-upsert via env STEP1_NO_UPSERT=1
if [ "$STEP1_NO_UPSERT" = "1" ]; then
  python -m src.cli --verbose analyze --no-upsert
else
  python -m src.cli --verbose analyze
fi

print_status "Step 1 completed. Consolidated JSON should be in \"$(grep '^OUTPUT_DIR=' .env | cut -d'=' -f2)/consolidated_metadata.json\""


