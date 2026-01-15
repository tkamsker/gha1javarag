#!/bin/bash
# ==============================================================================
# Service Health Check Script
# ==============================================================================
# Tests connectivity to all required services (Ollama, Weaviate, SQLite)
# Works on both macOS and Linux
#
# Usage: ./check-services.sh [--verbose]
#
# Exit codes:
#   0 - All services healthy
#   1 - One or more services unhealthy
#   2 - Dependencies missing (httpx)
#
# Based on HOWTO-PRODUCTION-TESTING.md Step 2.3

set -e

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

VERBOSE=false
if [[ "$1" == "--verbose" ]] || [[ "$1" == "-v" ]]; then
    VERBOSE=true
fi

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

echo "======================================"
echo "Service Health Check"
echo "======================================"
echo ""

# ==============================================================================
# Check 1: Virtual Environment
# ==============================================================================
info "Checking Python virtual environment..."

VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    err "Virtual environment not found at $VENV_DIR"
    echo ""
    echo "Please create virtual environment first:"
    echo "  python3 -m venv .venv"
    echo "  source .venv/bin/activate"
    echo "  pip install -r requirements.txt"
    echo ""
    exit 2
fi

ok "Virtual environment exists: $VENV_DIR"

# Activate virtual environment
if [ -f "$VENV_DIR/bin/activate" ]; then
    # shellcheck source=/dev/null
    source "$VENV_DIR/bin/activate"
    ok "Virtual environment activated"
else
    err "Cannot activate virtual environment (missing bin/activate)"
    exit 2
fi

# Check if httpx is installed
if ! python3 -c "import httpx" 2>/dev/null; then
    err "httpx package not installed"
    echo ""
    echo "Please install dependencies:"
    echo "  source .venv/bin/activate"
    echo "  pip install -r requirements.txt"
    echo ""
    exit 2
fi

ok "httpx package available"
echo ""

# ==============================================================================
# Check 2: Test Service Connectivity
# ==============================================================================
info "Testing service connectivity..."
echo ""

# Run Python script to test services
python3 << 'PYTHON_EOF'
import httpx
import sys
import os
from pathlib import Path

# ANSI color codes
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
NC = '\033[0m'

def ok(msg):
    print(f"{GREEN}✅ {msg}{NC}")

def err(msg):
    print(f"{RED}❌ {msg}{NC}")

def warn(msg):
    print(f"{YELLOW}⚠️  {msg}{NC}")

# Load .env file if exists
env_file = Path(".env")
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

# Get service URLs from environment or use defaults
ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
weaviate_url = os.getenv("WEAVIATE_URL", "http://localhost:8080")

# Services to check
services = {
    "Ollama": f"{ollama_url}/api/tags",
    "Weaviate": f"{weaviate_url}/v1/meta"
}

print("🔍 Testing service connectivity...")
print("")

all_healthy = True
service_details = []

for name, url in services.items():
    try:
        response = httpx.get(url, timeout=5.0)
        if response.status_code == 200:
            ok(f"{name}: Connected ({url})")
            service_details.append({
                "name": name,
                "status": "ok",
                "url": url,
                "response_time": response.elapsed.total_seconds()
            })
        else:
            err(f"{name}: HTTP {response.status_code} ({url})")
            all_healthy = False
            service_details.append({
                "name": name,
                "status": "error",
                "url": url,
                "error": f"HTTP {response.status_code}"
            })
    except httpx.ConnectError as e:
        err(f"{name}: Connection refused ({url})")
        print(f"   {str(e)}")
        all_healthy = False
        service_details.append({
            "name": name,
            "status": "error",
            "url": url,
            "error": "Connection refused"
        })
    except httpx.TimeoutException:
        err(f"{name}: Connection timeout ({url})")
        all_healthy = False
        service_details.append({
            "name": name,
            "status": "error",
            "url": url,
            "error": "Timeout"
        })
    except Exception as e:
        err(f"{name}: {type(e).__name__} - {str(e)}")
        all_healthy = False
        service_details.append({
            "name": name,
            "status": "error",
            "url": url,
            "error": str(e)
        })

print("")

# Check SQLite database (optional - just verify file exists)
db_path = Path(os.getenv("WORKSPACE_DB_PATH", "data/workspaces.db"))
if db_path.exists():
    ok(f"SQLite: Database exists ({db_path})")
    try:
        # Quick check if file is accessible
        with open(db_path, 'rb') as f:
            header = f.read(16)
            if header.startswith(b'SQLite format 3'):
                ok("SQLite: Valid database format")
            else:
                warn("SQLite: File exists but may not be valid SQLite database")
    except Exception as e:
        warn(f"SQLite: Cannot read database - {e}")
else:
    warn(f"SQLite: Database not found ({db_path})")
    print("   This is normal if you haven't initialized the database yet")
    print("   Run: python3 -c 'from codeindex.web.database.connection import get_workspace_manager; get_workspace_manager().initialize_database()'")

print("")
print("=" * 50)

if all_healthy:
    ok("All services healthy - ready to proceed!")
    print("=" * 50)
    print("")
    print("Next steps:")
    print("  1. Launch Streamlit: streamlit run src/codeindex/web/app.py")
    print("  2. Run pipeline: ./run.sh <project-name> <source-path>")
    print("  3. Generate PRD: ./production-requirements-generation.sh")
    sys.exit(0)
else:
    err("Some services are unhealthy")
    print("=" * 50)
    print("")
    print("Troubleshooting:")

    # Specific troubleshooting for each failed service
    for detail in service_details:
        if detail["status"] == "error":
            print(f"\n{detail['name']}:")
            if detail['name'] == 'Ollama':
                print("  1. Check if Ollama is running:")
                print("     ps aux | grep ollama")
                print("  2. Start Ollama:")
                print("     ollama serve")
                print("  3. Verify model is installed:")
                print("     ollama list | grep gemma3")
                print("  4. Pull model if missing:")
                print("     ollama pull gemma3:12b")
            elif detail['name'] == 'Weaviate':
                print("  1. Check if Weaviate is running:")
                print("     docker ps | grep weaviate")
                print("  2. Start Weaviate:")
                print("     ./docker-weaviate.sh start")
                print("  3. Check logs:")
                print("     ./docker-weaviate.sh logs")
                print("  4. Restart if needed:")
                print("     ./docker-weaviate.sh restart")

    sys.exit(1)
PYTHON_EOF

EXIT_CODE=$?

# ==============================================================================
# Verbose Output (if requested)
# ==============================================================================
if [ "$VERBOSE" = true ]; then
    echo ""
    echo "======================================"
    echo "Detailed Service Information"
    echo "======================================"
    echo ""

    info "Checking Ollama version..."
    if curl -s http://localhost:11434/api/tags 2>/dev/null | python3 -m json.tool 2>/dev/null; then
        ok "Ollama API response valid"
    else
        warn "Ollama API response invalid or service not running"
    fi

    echo ""
    info "Checking Weaviate schema..."
    if curl -s http://localhost:8080/v1/schema 2>/dev/null | python3 -m json.tool 2>/dev/null | head -20; then
        ok "Weaviate schema accessible"
    else
        warn "Weaviate schema not accessible or service not running"
    fi
fi

exit $EXIT_CODE
