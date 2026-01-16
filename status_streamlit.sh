#!/bin/bash
################################################################################
# Streamlit Status Script
#
# Checks the status of Streamlit and related services.
################################################################################

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Streamlit Application Status${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# ============================================
# Check Streamlit Process
# ============================================
echo -e "${BLUE}[1] Streamlit Process:${NC}"
if pgrep -f "streamlit.*app.py" > /dev/null; then
    echo -e "${GREEN}✓ Running${NC}"
    ps aux | grep "streamlit.*app.py" | grep -v grep | awk '{print "    PID: " $2 ", CPU: " $3 "%, MEM: " $4 "%"}'
else
    echo -e "${RED}✗ Not running${NC}"
fi
echo ""

# ============================================
# Check Streamlit Port
# ============================================
echo -e "${BLUE}[2] Streamlit Port (8501):${NC}"
if netstat -tuln 2>/dev/null | grep -q ":8501 " || ss -tuln 2>/dev/null | grep -q ":8501 "; then
    echo -e "${GREEN}✓ Port 8501 is listening${NC}"
    netstat -tuln 2>/dev/null | grep ":8501 " || ss -tuln 2>/dev/null | grep ":8501 "
else
    echo -e "${RED}✗ Port 8501 is not listening${NC}"
fi
echo ""

# ============================================
# Check Ollama Service
# ============================================
echo -e "${BLUE}[3] Ollama Service:${NC}"
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Ollama is running${NC}"

    # Check current model from environment
    if [ -n "$OLLAMA_MODEL_NAME" ]; then
        echo -e "    Configured model: ${OLLAMA_MODEL_NAME}"
        if curl -s http://localhost:11434/api/tags | grep -q "$OLLAMA_MODEL_NAME"; then
            echo -e "    ${GREEN}✓ Model is available${NC}"
        else
            echo -e "    ${RED}✗ Model not found${NC}"
        fi
    fi
else
    echo -e "${RED}✗ Ollama is not running${NC}"
fi
echo ""

# ============================================
# Check Weaviate Service
# ============================================
echo -e "${BLUE}[4] Weaviate Service:${NC}"
if curl -s http://localhost:8080/v1/.well-known/ready > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Weaviate is running${NC}"
else
    echo -e "${RED}✗ Weaviate is not running${NC}"
fi
echo ""

# ============================================
# Check Log File
# ============================================
PROJECT_DIR="/home/tkamsker/development/Iteration20/gha1javarag"
LOG_FILE="$PROJECT_DIR/streamlit.log"

echo -e "${BLUE}[5] Log File:${NC}"
if [ -f "$LOG_FILE" ]; then
    FILE_SIZE=$(du -h "$LOG_FILE" | cut -f1)
    LAST_MODIFIED=$(stat -c %y "$LOG_FILE" 2>/dev/null || stat -f "%Sm" "$LOG_FILE" 2>/dev/null)
    echo -e "${GREEN}✓ Log file exists${NC}"
    echo -e "    Location: $LOG_FILE"
    echo -e "    Size: $FILE_SIZE"
    echo -e "    Modified: $LAST_MODIFIED"
    echo ""
    echo -e "${BLUE}Last 10 lines:${NC}"
    tail -10 "$LOG_FILE" | sed 's/^/    /'
else
    echo -e "${YELLOW}⚠ Log file not found${NC}"
    echo -e "    Expected: $LOG_FILE"
fi
echo ""

# ============================================
# Check URLs
# ============================================
echo -e "${BLUE}[6] Application URLs:${NC}"
echo -e "    Local:    http://localhost:8501"
echo -e "    Network:  http://$(hostname -I 2>/dev/null | awk '{print $1}'):8501"
echo ""

# ============================================
# Quick Actions
# ============================================
echo -e "${BLUE}Quick Actions:${NC}"
echo -e "    Start:    ./start_streamlit.sh"
echo -e "    Stop:     ./stop_streamlit.sh"
echo -e "    Logs:     tail -f $LOG_FILE"
echo ""
