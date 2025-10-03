#!/bin/bash

set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

echo "[INFO] Running Step 3: LLM+Weaviate requirements synthesis (Refactored)"

# Parse command line arguments
PARALLEL="--parallel"
MAX_WORKERS="3"
INCREMENTAL=""
FORCE=""
VERBOSE="--verbose"

while [[ $# -gt 0 ]]; do
  case $1 in
    --sequential)
      PARALLEL="--sequential"
      shift
      ;;
    --parallel)
      PARALLEL="--parallel"
      shift
      ;;
    --max-workers)
      MAX_WORKERS="$2"
      shift 2
      ;;
    --incremental)
      INCREMENTAL="--incremental"
      shift
      ;;
    --force)
      FORCE="--force"
      shift
      ;;
    --no-verbose)
      VERBOSE=""
      shift
      ;;
    -h|--help)
      echo "Usage: $0 [OPTIONS]"
      echo ""
      echo "Options:"
      echo "  --sequential      Disable parallel processing"
      echo "  --parallel        Enable parallel processing (default)"
      echo "  --max-workers N   Set maximum number of workers (default: 3)"
      echo "  --incremental     Run incremental processing (skip existing outputs)"
      echo "  --force           Force regenerate all outputs (use with --incremental)"
      echo "  --no-verbose      Disable verbose logging"
      echo "  -h, --help        Show this help message"
      exit 0
      ;;
    *)
      echo "[ERROR] Unknown option: $1"
      echo "Use --help for usage information"
      exit 1
      ;;
  esac
done

# Environment setup
if [ ! -d "venv" ]; then
  echo "[INFO] Creating Python virtual environment..."
  python3 -m venv venv
fi

echo "[INFO] Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install --upgrade pip >/dev/null 2>&1
pip install -r requirements.txt >/dev/null 2>&1

# Configuration validation
if [ ! -f ".env" ]; then
  echo "[ERROR] .env configuration file not found"
  echo "[ERROR] Please create .env with required variables:"
  echo "        WEAVIATE_URL, OUTPUT_DIR, AI_PROVIDER, etc."
  exit 1
fi

# Build command with options
CMD="python -m src.cli"
if [ -n "$VERBOSE" ]; then
  CMD="$CMD $VERBOSE"
fi

CMD="$CMD step3 $PARALLEL --max-workers $MAX_WORKERS"
if [ -n "$INCREMENTAL" ]; then
  CMD="$CMD $INCREMENTAL"
fi
if [ -n "$FORCE" ]; then
  CMD="$CMD $FORCE"
fi

echo "[INFO] Executing: $CMD"
echo "[INFO] Processing mode: $([ "$PARALLEL" = "--parallel" ] && echo "Parallel ($MAX_WORKERS workers)" || echo "Sequential")"
echo "[INFO] Processing type: $([ -n "$INCREMENTAL" ] && echo "Incremental" || echo "Full")"

# Execute step3 processing
eval $CMD

echo "[INFO] Step 3 completed successfully!"
echo "[INFO] Output location: \$OUTPUT_DIR/requirements/"
echo "[INFO] - Executive summary: requirements/_step3_overview.md"
echo "[INFO] - Project details: requirements/projects/{project_name}/"


