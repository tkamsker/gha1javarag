#!/bin/bash

set -e

# Step 2: Generate requirements from consolidated JSON

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

if [ -n "$OUTPUT_DIR" ]; then
  OUT_DIR="$OUTPUT_DIR"
else
  OUT_DIR=$(grep '^OUTPUT_DIR=' .env | cut -d'=' -f2)
fi
if [ -z "$OUT_DIR" ]; then
  print_error "OUTPUT_DIR not set (env or .env)"
  exit 1
fi

if [ ! -f "$OUT_DIR/consolidated_metadata.json" ]; then
  print_status "consolidated_metadata.json not found in $OUT_DIR. Requirements will still be generated, but with placeholders."
fi

print_status "Generating requirements (Step 2) ..."
python -m src.cli --verbose requirements

print_status "Step 2 completed. Requirements in \"$OUT_DIR/requirements\""


