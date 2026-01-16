#!/bin/bash
################################################################################
# Streamlit Startup Script (Background Mode)
#
# Starts Streamlit in the background with logging to a file.
################################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Streamlit Background Startup${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Configuration
PROJECT_DIR="/home/tkamsker/development/Iteration20/gha1javarag"
VENV_PATH="venv"
OLLAMA_MODEL="qwen2.5-coder:32b"
STREAMLIT_PORT="${STREAMLIT_PORT:-8501}"
LOG_FILE="$PROJECT_DIR/streamlit.log"

# Navigate to project
cd "$PROJECT_DIR" || exit 1

# Activate venv
source "$VENV_PATH/bin/activate" || exit 1

# Set environment
export OLLAMA_MODEL_NAME="$OLLAMA_MODEL"
export STREAMLIT_PORT="$STREAMLIT_PORT"

# Load .env if exists
if [ -f .env ]; then
    set -a
    source .env
    set +a
fi

# Stop existing
pkill -f "streamlit.*app.py" 2>/dev/null || true
sleep 2

# Clear cache
find src/codeindex -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

# Check Ollama
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${RED}ERROR: Ollama is not running${NC}"
    exit 1
fi

# Start in background
echo -e "${BLUE}Starting Streamlit in background...${NC}"
nohup streamlit run src/codeindex/web/app.py --server.port "$STREAMLIT_PORT" > "$LOG_FILE" 2>&1 &
STREAMLIT_PID=$!

# Wait a moment to check if it started
sleep 3

if ps -p $STREAMLIT_PID > /dev/null; then
    echo -e "${GREEN}✓ Streamlit started successfully${NC}"
    echo -e ""
    echo -e "  PID:     ${STREAMLIT_PID}"
    echo -e "  Port:    ${STREAMLIT_PORT}"
    echo -e "  Model:   ${OLLAMA_MODEL}"
    echo -e "  Log:     ${LOG_FILE}"
    echo -e ""
    echo -e "${BLUE}View logs with:${NC}"
    echo -e "  tail -f $LOG_FILE"
    echo -e ""
    echo -e "${BLUE}Stop with:${NC}"
    echo -e "  ./stop_streamlit.sh"
    echo -e "  OR"
    echo -e "  pkill -f streamlit"
else
    echo -e "${RED}ERROR: Streamlit failed to start${NC}"
    echo -e "Check logs: $LOG_FILE"
    exit 1
fi
