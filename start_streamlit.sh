#!/bin/bash
################################################################################
# Streamlit Startup Script for Feature 009 - Web Client
#
# This script starts the Streamlit web application with proper environment
# configuration and error handling.
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Streamlit Application Startup${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# ============================================
# Configuration
# ============================================
PROJECT_DIR="/home/tkamsker/development/Iteration20/gha1javarag"
VENV_PATH="venv"
OLLAMA_MODEL="qwen2.5-coder:32b"
STREAMLIT_PORT="${STREAMLIT_PORT:-8501}"

# ============================================
# Step 1: Navigate to project directory
# ============================================
echo -e "${BLUE}[1/8]${NC} Navigating to project directory..."
cd "$PROJECT_DIR" || {
    echo -e "${RED}ERROR: Project directory not found: $PROJECT_DIR${NC}"
    exit 1
}
echo -e "${GREEN}✓${NC} Current directory: $(pwd)"
echo ""

# ============================================
# Step 2: Check if virtual environment exists
# ============================================
echo -e "${BLUE}[2/8]${NC} Checking virtual environment..."
if [ ! -d "$VENV_PATH" ]; then
    echo -e "${RED}ERROR: Virtual environment not found at: $VENV_PATH${NC}"
    echo -e "${YELLOW}Please create it with: python3 -m venv venv${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Virtual environment found"
echo ""

# ============================================
# Step 3: Activate virtual environment
# ============================================
echo -e "${BLUE}[3/8]${NC} Activating virtual environment..."
source "$VENV_PATH/bin/activate" || {
    echo -e "${RED}ERROR: Failed to activate virtual environment${NC}"
    exit 1
}
echo -e "${GREEN}✓${NC} Virtual environment activated"
echo -e "    Python: $(which python)"
echo ""

# ============================================
# Step 4: Set environment variables
# ============================================
echo -e "${BLUE}[4/8]${NC} Setting environment variables..."
export OLLAMA_MODEL_NAME="$OLLAMA_MODEL"
export STREAMLIT_PORT="$STREAMLIT_PORT"

# Load .env file if it exists
if [ -f .env ]; then
    echo -e "${GREEN}✓${NC} Loading .env file"
    set -a
    source .env
    set +a
else
    echo -e "${YELLOW}⚠${NC}  No .env file found (optional)"
fi

echo -e "${GREEN}✓${NC} Environment variables set:"
echo -e "    OLLAMA_MODEL_NAME: $OLLAMA_MODEL_NAME"
echo -e "    STREAMLIT_PORT: $STREAMLIT_PORT"
echo ""

# ============================================
# Step 5: Verify Ollama is running
# ============================================
echo -e "${BLUE}[5/8]${NC} Checking Ollama service..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Ollama is running at http://localhost:11434"

    # Verify the model exists
    if curl -s http://localhost:11434/api/tags | grep -q "$OLLAMA_MODEL"; then
        echo -e "${GREEN}✓${NC} Model '$OLLAMA_MODEL' is available"
    else
        echo -e "${YELLOW}⚠${NC}  Model '$OLLAMA_MODEL' not found in Ollama"
        echo -e "${YELLOW}    Available models:${NC}"
        curl -s http://localhost:11434/api/tags | jq -r '.models[]?.name' 2>/dev/null | sed 's/^/    - /' || echo "    (unable to list models)"
        echo ""
        echo -e "${YELLOW}    Continuing anyway... (may cause errors)${NC}"
    fi
else
    echo -e "${RED}ERROR: Ollama is not running at http://localhost:11434${NC}"
    echo -e "${YELLOW}Please start Ollama with: ollama serve${NC}"
    exit 1
fi
echo ""

# ============================================
# Step 6: Stop existing Streamlit process
# ============================================
echo -e "${BLUE}[6/8]${NC} Stopping any existing Streamlit processes..."
if pgrep -f "streamlit.*app.py" > /dev/null; then
    pkill -f "streamlit.*app.py" || true
    sleep 2
    echo -e "${GREEN}✓${NC} Existing Streamlit process stopped"
else
    echo -e "${GREEN}✓${NC} No existing Streamlit process found"
fi
echo ""

# ============================================
# Step 7: Clear Python cache
# ============================================
echo -e "${BLUE}[7/8]${NC} Clearing Python bytecode cache..."
find src/codeindex -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find src/codeindex -name "*.pyc" -delete 2>/dev/null || true
echo -e "${GREEN}✓${NC} Python cache cleared"
echo ""

# ============================================
# Step 8: Start Streamlit
# ============================================
echo -e "${BLUE}[8/8]${NC} Starting Streamlit application..."
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  Streamlit is starting...                                 ║${NC}"
echo -e "${GREEN}║                                                            ║${NC}"
echo -e "${GREEN}║  Model: ${OLLAMA_MODEL}                    ║${NC}"
echo -e "${GREEN}║  Port:  ${STREAMLIT_PORT}                                           ║${NC}"
echo -e "${GREEN}║                                                            ║${NC}"
echo -e "${GREEN}║  Press Ctrl+C to stop                                     ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Start Streamlit
exec streamlit run src/codeindex/web/app.py --server.port "$STREAMLIT_PORT"
