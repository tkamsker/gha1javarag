#!/bin/bash

# =============================
# Web Client Start Script
# =============================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

info(){ echo -e "${BLUE}[INFO]${NC} $1"; }
ok(){ echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warn(){ echo -e "${YELLOW}[WARNING]${NC} $1"; }
err(){ echo -e "${RED}[ERROR]${NC} $1"; }

echo "🌐 Web Client for Weaviate Search"
echo "=================================="
echo ""

# Ensure we're in the correct directory
cd "$(dirname "$0")"

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    info "Activating virtual environment..."
    if [ -f venv/bin/activate ]; then
        source venv/bin/activate
    else
        err "Virtual environment not found. Please run: python3 -m venv venv"
        exit 1
    fi
fi

ok "Virtual environment activated"

# Check if Flask is installed
info "Checking dependencies..."
if ! python -c "import flask" 2>/dev/null; then
    warn "Flask not installed. Installing dependencies..."
    pip install flask flask-cors
fi

if ! python -c "import flask_cors" 2>/dev/null; then
    warn "Flask-CORS not installed. Installing..."
    pip install flask-cors
fi

ok "Dependencies checked"

# Check if Weaviate is running
echo ""
echo "🔍 Checking Weaviate Connection"
echo "================================"

if curl -s http://localhost:8080/v1/meta > /dev/null 2>&1; then
    ok "Weaviate is running on http://localhost:8080"
else
    err "Weaviate is not running!"
    echo ""
    echo "Please start Weaviate first:"
    echo "  macOS:   ./start_weaviate_simple.sh"
    echo "  Ubuntu:  ./start_weaviate_simple.sh"
    echo ""
    echo "Or if you prefer the full script:"
    echo "  ./docker-weaviate.sh start"
    exit 1
fi

# Detect OS for opening browser
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    else
        echo "unknown"
    fi
}

os=$(detect_os)

echo ""
echo "🚀 Starting Web Client"
echo "======================"
echo ""
info "Starting Flask web server on http://localhost"
info "Note: Port 80 requires sudo privileges"
info "Press Ctrl+C to stop the server"
echo ""

# Check if running on port 80
if [ "$(id -u)" -ne 0 ]; then
    warn "Running on port 80 requires root privileges"
    warn "You may need to run with: sudo ./start_web_client.sh"
fi

# Start the web client
python src/web/weaviate_client.py
