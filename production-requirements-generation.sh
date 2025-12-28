#!/bin/bash
# production-requirements-generation.sh
#
# Usage: ./production-requirements-generation.sh <project-name> <source-path>
# Example: ./production-requirements-generation.sh cuco-ui-admin /mnt/cucocalcai/cuco-master/cuco-ui-admin

PROJECT_NAME=$1
SOURCE_PATH=$2
TIMESTAMP=$(date +'%Y-%m-%d_%H-%M-%S')
LOG_DIR="./logs"
OUTPUT_DIR="./output/${PROJECT_NAME}"

# Create directories
mkdir -p "$LOG_DIR"
mkdir -p "$OUTPUT_DIR"

echo "==================================="
echo "PRD Generation for: $PROJECT_NAME"
echo "Source: $SOURCE_PATH"
echo "==================================="

# Step 1: Run analysis pipeline (equivalent to run-cuco.sh)
echo "Step 1: Running analysis pipeline..."
nohup ./run.sh \
    --source-dir "$SOURCE_PATH" \
    --project "$PROJECT_NAME" \
    --output "$OUTPUT_DIR" \
    > "${LOG_DIR}/log_${PROJECT_NAME}_pipeline_${TIMESTAMP}.log" 2>&1 &

PIPELINE_PID=$!
echo "Pipeline started (PID: $PIPELINE_PID)"
echo "Log: ${LOG_DIR}/log_${PROJECT_NAME}_pipeline_${TIMESTAMP}.log"

# Wait for pipeline to complete
wait $PIPELINE_PID

if [ $? -eq 0 ]; then
    echo "✓ Pipeline completed successfully"
else
    echo "✗ Pipeline failed. Check log file."
    exit 1
fi

# Step 2: Generate PRD documents (equivalent to step2.sh)
echo ""
echo "Step 2: Generating PRD documents..."
nohup codeindex prd backend \
    --project "$PROJECT_NAME" \
    --output-dir "$OUTPUT_DIR/prd" \
    > "${LOG_DIR}/log_${PROJECT_NAME}_backend_prd_${TIMESTAMP}.log" 2>&1 &

BACKEND_PID=$!

nohup codeindex prd frontend \
    --project "$PROJECT_NAME" \
    --output-dir "$OUTPUT_DIR/prd" \
    > "${LOG_DIR}/log_${PROJECT_NAME}_frontend_prd_${TIMESTAMP}.log" 2>&1 &

FRONTEND_PID=$!

echo "Backend PRD generation started (PID: $BACKEND_PID)"
echo "Frontend PRD generation started (PID: $FRONTEND_PID)"

# Wait for PRD generation to complete
wait $BACKEND_PID
BACKEND_STATUS=$?

wait $FRONTEND_PID
FRONTEND_STATUS=$?

# Check results
if [ $BACKEND_STATUS -eq 0 ] && [ $FRONTEND_STATUS -eq 0 ]; then
    echo ""
    echo "==================================="
    echo "✓ SUCCESS!"
    echo "==================================="
    echo "PRD documents generated:"
    echo "  - Backend PRD: $OUTPUT_DIR/prd/backend_prd.md"
    echo "  - Frontend PRD: $OUTPUT_DIR/prd/frontend_prd.md"
    echo ""
    echo "View results:"
    echo "  ls -lh $OUTPUT_DIR/prd/"
else
    echo ""
    echo "==================================="
    echo "✗ PRD Generation Failed"
    echo "==================================="
    echo "Check log files:"
    echo "  - Backend: ${LOG_DIR}/log_${PROJECT_NAME}_backend_prd_${TIMESTAMP}.log"
    echo "  - Frontend: ${LOG_DIR}/log_${PROJECT_NAME}_frontend_prd_${TIMESTAMP}.log"
    exit 1
fi
