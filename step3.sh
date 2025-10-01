#!/bin/bash

set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

echo "[INFO] Running Step 3: LLM+Weaviate requirements synthesis"

if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip >/dev/null
pip install -r requirements.txt >/dev/null

if [ ! -f ".env" ]; then
  echo "[ERROR] .env not found"; exit 1
fi

python -m src.cli --verbose step3

echo "[INFO] Step 3 completed. See _step3_overview.md in OUTPUT_DIR/requirements."


