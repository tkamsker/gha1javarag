#!/bin/bash
# production-requirements-generation.sh
#
# Usage: ./production-requirements-generation.sh <project-name> <source-path>
# Example: ./production-requirements-generation.sh cuco-ui-admin /mnt/cucocalcai/cuco-master/cuco-ui-admin

# Don't exit on error immediately - we want to check status codes
set +e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

info() { echo -e "${BLUE}[INFO]${NC} $1"; }
ok() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
err() { echo -e "${RED}[ERROR]${NC} $1"; }

# Validate arguments
if [ -z "$1" ] || [ -z "$2" ]; then
    err "Missing required arguments"
    echo "Usage: ./production-requirements-generation.sh <project-name> <source-path>"
    echo "Example: ./production-requirements-generation.sh cuco-ui-admin /mnt/cucocalcai/cuco-master/cuco-ui-admin"
    exit 1
fi

PROJECT_NAME=$1
SOURCE_PATH=$2
TIMESTAMP=$(date +'%Y-%m-%d_%H-%M-%S')
LOG_DIR="./logs"
OUTPUT_DIR="./output/${PROJECT_NAME}"

# Validate virtual environment exists
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    err "Virtual environment not found at $VENV_DIR"
    echo "Please run: python -m venv .venv && source .venv/bin/activate && pip install -e ."
    exit 1
fi

# Validate codeindex command exists
if [ ! -f "$VENV_DIR/bin/codeindex" ]; then
    err "codeindex command not found in virtual environment"
    echo "Please run: source .venv/bin/activate && pip install -e ."
    exit 1
fi

# Create directories
mkdir -p "$LOG_DIR"
mkdir -p "$OUTPUT_DIR"

echo "==================================="
echo "PRD Generation for: $PROJECT_NAME"
echo "Source: $SOURCE_PATH"
echo "Timestamp: $TIMESTAMP"
echo "==================================="

# Step 1: Run analysis pipeline (equivalent to run-cuco.sh)
echo ""
info "Step 1: Running analysis pipeline (discover → extract → index → status)..."
info "Source: $SOURCE_PATH"
info "Project: $PROJECT_NAME"
nohup ./run.sh \
    "$PROJECT_NAME" \
    "$SOURCE_PATH" \
    > "${LOG_DIR}/log_${PROJECT_NAME}_pipeline_${TIMESTAMP}.log" 2>&1 &

PIPELINE_PID=$!
info "Pipeline started (PID: $PIPELINE_PID)"
info "Log: ${LOG_DIR}/log_${PROJECT_NAME}_pipeline_${TIMESTAMP}.log"
info "Monitoring progress (Ctrl+C to stop monitoring, pipeline continues)..."

# Monitor pipeline progress
tail -f "${LOG_DIR}/log_${PROJECT_NAME}_pipeline_${TIMESTAMP}.log" &
TAIL_PID=$!

# Wait for pipeline to complete
wait $PIPELINE_PID
PIPELINE_STATUS=$?

# Stop tail monitoring
kill $TAIL_PID 2>/dev/null || true

echo ""
if [ $PIPELINE_STATUS -eq 0 ]; then
    ok "Pipeline completed successfully"
else
    err "Pipeline failed (exit code: $PIPELINE_STATUS)"
    echo "Check log: ${LOG_DIR}/log_${PROJECT_NAME}_pipeline_${TIMESTAMP}.log"
    exit 1
fi

# Step 2: Generate PRD documents (equivalent to step2.sh)
echo ""
echo "Step 2: Generating PRD documents..."
info "Starting services (backend) PRD generation..."
# Increase LLM timeout to handle large files that may timeout
nohup "$VENV_DIR/bin/codeindex" prd services \
    --project "$PROJECT_NAME" \
    --output-dir "$OUTPUT_DIR/prd" \
    --llm-timeout 240 \
    --llm-retries 3 \
    > "${LOG_DIR}/log_${PROJECT_NAME}_services_prd_${TIMESTAMP}.log" 2>&1 &

SERVICES_PID=$!

info "Starting frontend PRD generation..."
# Increase LLM timeout to handle large files that may timeout
nohup "$VENV_DIR/bin/codeindex" prd frontend \
    --project "$PROJECT_NAME" \
    --output-dir "$OUTPUT_DIR/prd" \
    --llm-timeout 240 \
    --llm-retries 3 \
    > "${LOG_DIR}/log_${PROJECT_NAME}_frontend_prd_${TIMESTAMP}.log" 2>&1 &

FRONTEND_PID=$!

info "Services PRD generation started (PID: $SERVICES_PID)"
info "Frontend PRD generation started (PID: $FRONTEND_PID)"
info "Waiting for PRD generation to complete..."

# Wait for PRD generation to complete
wait $SERVICES_PID
SERVICES_STATUS=$?

wait $FRONTEND_PID
FRONTEND_STATUS=$?

# Check results
echo ""
echo "==================================="
if [ $SERVICES_STATUS -eq 0 ] && [ $FRONTEND_STATUS -eq 0 ]; then
    ok "PRD GENERATION COMPLETE!"
    echo "==================================="
    echo ""
    ok "Services PRD: $OUTPUT_DIR/prd/services_prd.md"
    ok "Frontend PRD: $OUTPUT_DIR/prd/frontend_prd.md"
    echo ""
    info "View results:"
    echo "  ls -lh $OUTPUT_DIR/prd/"
    echo ""
    info "Log files:"
    echo "  - Pipeline: ${LOG_DIR}/log_${PROJECT_NAME}_pipeline_${TIMESTAMP}.log"
    echo "  - Services PRD: ${LOG_DIR}/log_${PROJECT_NAME}_services_prd_${TIMESTAMP}.log"
    echo "  - Frontend PRD: ${LOG_DIR}/log_${PROJECT_NAME}_frontend_prd_${TIMESTAMP}.log"
    echo ""
    info "Next steps:"
    echo "  1. Review PRDs: cat $OUTPUT_DIR/prd/services_prd.md"
    echo "  2. Check status: codeindex status"
    echo "  3. Search codebase: codeindex search 'your query'"
else
    err "PRD GENERATION FAILED"
    echo "==================================="
    echo ""
    if [ $SERVICES_STATUS -ne 0 ]; then
        err "Services PRD generation failed (exit code: $SERVICES_STATUS)"
        echo "  Log: ${LOG_DIR}/log_${PROJECT_NAME}_services_prd_${TIMESTAMP}.log"
    fi
    if [ $FRONTEND_STATUS -ne 0 ]; then
        err "Frontend PRD generation failed (exit code: $FRONTEND_STATUS)"
        echo "  Log: ${LOG_DIR}/log_${PROJECT_NAME}_frontend_prd_${TIMESTAMP}.log"
    fi
    echo ""
    info "Troubleshooting:"
    echo "  1. Check log files above for detailed errors"
    echo "  2. Verify Weaviate is running: docker ps | grep weaviate"
    echo "  3. Verify indexing completed: codeindex status"
    echo "  4. Check for Ollama timeout errors in logs (may need to increase --llm-timeout)"
    exit 1
fi
