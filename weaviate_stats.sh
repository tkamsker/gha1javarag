#!/bin/bash
# Weaviate Statistics Script
# Works on both macOS and Linux
# Shows what's actually indexed in Weaviate

set -e

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
else
    OS="Unknown"
fi

echo "=========================================="
echo "Weaviate Statistics Tool"
echo "OS: $OS"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
else
    echo "Warning: No virtual environment found. Using system Python."
fi

# Check if Weaviate is accessible
echo "Checking Weaviate connection..."
if command -v curl &> /dev/null; then
    WEAVIATE_URL="${WEAVIATE_URL:-http://localhost:8080}"
    if curl -s -f "$WEAVIATE_URL/v1/meta" > /dev/null 2>&1; then
        echo "✓ Weaviate is accessible at $WEAVIATE_URL"
    else
        echo "✗ Warning: Cannot connect to Weaviate at $WEAVIATE_URL"
        echo "  Make sure Weaviate is running: docker-compose up -d"
        echo ""
    fi
else
    echo "Warning: curl not found, skipping Weaviate connection check"
fi

echo ""
echo "Running statistics script..."
echo ""

# Run the Python script
python3 weaviate_stats.py

# Exit with Python script's exit code
exit $?

