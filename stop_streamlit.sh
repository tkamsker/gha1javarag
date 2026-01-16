#!/bin/bash
################################################################################
# Streamlit Stop Script
#
# Safely stops the Streamlit application.
################################################################################

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Stopping Streamlit Application${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Check if Streamlit is running
if pgrep -f "streamlit.*app.py" > /dev/null; then
    echo -e "${BLUE}Found running Streamlit process(es):${NC}"
    ps aux | grep "streamlit.*app.py" | grep -v grep
    echo ""

    # Stop the process
    echo -e "${BLUE}Stopping Streamlit...${NC}"
    pkill -f "streamlit.*app.py"

    # Wait for process to stop
    sleep 2

    # Verify it stopped
    if pgrep -f "streamlit.*app.py" > /dev/null; then
        echo -e "${YELLOW}⚠ Process still running, forcing shutdown...${NC}"
        pkill -9 -f "streamlit.*app.py"
        sleep 1
    fi

    # Final check
    if pgrep -f "streamlit.*app.py" > /dev/null; then
        echo -e "${RED}✗ Failed to stop Streamlit${NC}"
        exit 1
    else
        echo -e "${GREEN}✓ Streamlit stopped successfully${NC}"
    fi
else
    echo -e "${YELLOW}⚠ No running Streamlit process found${NC}"
fi

echo ""
