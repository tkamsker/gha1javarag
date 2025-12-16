#!/bin/bash
# ==============================================================================
# Environment Configuration Checker
# ==============================================================================
# Checks .env file for common configuration issues and provides fixes
#
# Usage: ./check-env.sh [--fix]
#
# Options:
#   --fix    Automatically fix detected issues

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

info() { echo -e "${BLUE}[INFO]${NC} $1"; }
ok() { echo -e "${GREEN}[OK]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
err() { echo -e "${RED}[ERROR]${NC} $1"; }

AUTO_FIX=false
if [[ "$1" == "--fix" ]]; then
    AUTO_FIX=true
fi

echo "======================================"
echo "Environment Configuration Checker"
echo "======================================"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    warn ".env file not found"
    echo ""
    echo "Creating .env from .env.example..."

    if [ -f ".env.example" ]; then
        cp .env.example .env
        ok ".env created from .env.example"
        echo ""
        echo "Please edit .env and set JAVA_SOURCE_DIR to your source code path"
        exit 0
    else
        err ".env.example not found!"
        echo "Please create .env manually"
        exit 1
    fi
fi

ok ".env file exists"
echo ""

# Load .env
export $(grep -v '^#' .env | xargs 2>/dev/null || true)

ISSUES_FOUND=0

# ==============================================================================
# Check 1: OLLAMA_BASE_URL
# ==============================================================================
info "Checking OLLAMA_BASE_URL..."

if [ -z "$OLLAMA_BASE_URL" ]; then
    ok "OLLAMA_BASE_URL not set (will use default: http://localhost:11434)"
elif [[ "$OLLAMA_BASE_URL" == *"host.docker.internal"* ]]; then
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
    err "OLLAMA_BASE_URL is set to: $OLLAMA_BASE_URL"
    echo ""
    echo "  ❌ host.docker.internal only works INSIDE Docker containers"
    echo "  ✅ For host-side Python code, use: http://localhost:11434"
    echo ""

    if [ "$AUTO_FIX" = true ]; then
        info "Auto-fixing OLLAMA_BASE_URL..."
        sed -i.bak 's|OLLAMA_BASE_URL=http://host.docker.internal:11434|OLLAMA_BASE_URL=http://localhost:11434|g' .env
        ok "Fixed OLLAMA_BASE_URL in .env (backup saved to .env.bak)"
    else
        echo "  To fix, run: sed -i.bak 's|host.docker.internal|localhost|g' .env"
        echo "  Or run: ./check-env.sh --fix"
    fi
    echo ""
elif [[ "$OLLAMA_BASE_URL" == "http://localhost:11434" ]] || [[ "$OLLAMA_BASE_URL" == "http://127.0.0.1:11434" ]]; then
    ok "OLLAMA_BASE_URL is correct: $OLLAMA_BASE_URL"
else
    warn "OLLAMA_BASE_URL is set to: $OLLAMA_BASE_URL"
    echo "  Expected: http://localhost:11434 or http://127.0.0.1:11434"
    echo ""
fi

# ==============================================================================
# Check 2: JAVA_SOURCE_DIR
# ==============================================================================
info "Checking JAVA_SOURCE_DIR..."

if [ -z "$JAVA_SOURCE_DIR" ]; then
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
    err "JAVA_SOURCE_DIR not set!"
    echo "  Please set JAVA_SOURCE_DIR to your Java source code directory"
    echo ""
elif [ ! -d "$JAVA_SOURCE_DIR" ]; then
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
    err "JAVA_SOURCE_DIR does not exist: $JAVA_SOURCE_DIR"
    echo "  Please update JAVA_SOURCE_DIR in .env"
    echo ""
else
    ok "JAVA_SOURCE_DIR exists: $JAVA_SOURCE_DIR"
fi

# ==============================================================================
# Check 3: Platform Detection
# ==============================================================================
info "Checking platform configuration..."

OS=$(uname -s | tr '[:upper:]' '[:lower:]')
if [[ "$OS" == "darwin" ]]; then
    ok "Platform: macOS"
    echo "  Docker compose will use: docker-compose.macos.yml"
    echo "  Weaviate → Ollama: host.docker.internal:11434 (automatic)"
elif [[ "$OS" == "linux" ]]; then
    ok "Platform: Linux"
    echo "  Docker compose will use: docker-compose.ubuntu.yml"
    echo "  Weaviate → Ollama: 127.0.0.1:11434 with network_mode: host (automatic)"
else
    warn "Platform: $OS (unknown)"
    echo "  May need manual Docker configuration"
fi
echo ""

# ==============================================================================
# Summary
# ==============================================================================
echo "======================================"
if [ $ISSUES_FOUND -eq 0 ]; then
    ok "All checks passed! ✓"
    echo "======================================"
    echo ""
    echo "Your environment is configured correctly."
    echo "You can now run: ./run-cuco.sh --yes /path/to/source"
else
    err "Found $ISSUES_FOUND issue(s)"
    echo "======================================"
    echo ""
    if [ "$AUTO_FIX" = false ]; then
        echo "To automatically fix issues, run:"
        echo "  ./check-env.sh --fix"
        echo ""
    fi
    exit 1
fi
