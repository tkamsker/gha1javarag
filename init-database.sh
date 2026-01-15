#!/bin/bash
# ==============================================================================
# Database Initialization Script
# ==============================================================================
# Initializes SQLite databases for the Streamlit Web UI
# Works on both macOS and Linux
#
# Usage: ./init-database.sh
#
# Creates:
#   - data/workspaces.db (workspace storage)
#   - data/annotations.db (optional annotations)
#
# Based on: HOWTO-PRODUCTION-TESTING.md Step 3.1

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

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

echo "======================================"
echo "Database Initialization"
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
    exit 1
fi

# Activate virtual environment
if [ -f "$VENV_DIR/bin/activate" ]; then
    # shellcheck source=/dev/null
    source "$VENV_DIR/bin/activate"
    ok "Virtual environment activated"
else
    err "Cannot activate virtual environment (missing bin/activate)"
    exit 1
fi

echo ""

# ==============================================================================
# Check 2: Create Data Directory
# ==============================================================================
info "Creating data directories..."

mkdir -p data/exports
mkdir -p data/workspaces

ok "Data directories created"
echo ""

# ==============================================================================
# Check 3: Initialize Database
# ==============================================================================
info "Initializing SQLite databases..."

python3 << 'PYTHON_EOF'
import sys
from pathlib import Path

# ANSI color codes
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'

def ok(msg):
    print(f"{GREEN}[SUCCESS]{NC} {msg}")

def err(msg):
    print(f"{RED}[ERROR]{NC} {msg}")

def info(msg):
    print(f"{BLUE}[INFO]{NC} {msg}")

# Add src to path
src_dir = Path(__file__).parent / "src"
if not src_dir.exists():
    src_dir = Path.cwd() / "src"

sys.path.insert(0, str(src_dir))

try:
    from codeindex.web.database.connection import get_workspace_manager

    info("Initializing workspace database...")

    manager = get_workspace_manager()
    manager.initialize_database()

    ok(f"Database initialized successfully")
    info(f"Location: {manager.db_path}")

    # Verify schema
    with manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        print("")
        ok(f"Tables created: {len(tables)}")
        for table in tables:
            print(f"   - {table[0]}")

    # Verify WAL mode
    with manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode")
        journal_mode = cursor.fetchone()[0]

        print("")
        if journal_mode.lower() == "wal":
            ok(f"WAL mode enabled: {journal_mode}")
        else:
            print(f"{YELLOW}[WARNING]{NC} Journal mode: {journal_mode} (expected: wal)")

    print("")
    print("=" * 50)
    ok("Database initialization complete!")
    print("=" * 50)
    print("")
    print("Next steps:")
    print("  1. Verify with: ./check-services.sh")
    print("  2. Launch web UI: streamlit run src/codeindex/web/app.py")

except ImportError as e:
    err(f"Cannot import database module: {e}")
    print("")
    print("Possible causes:")
    print("  1. Package not installed in development mode")
    print("     Fix: pip install -e .")
    print("  2. Missing dependencies")
    print("     Fix: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    err(f"Database initialization failed: {e}")
    import traceback
    print("")
    print("Traceback:")
    traceback.print_exc()
    sys.exit(1)
PYTHON_EOF

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    ok "All done! Run ./check-services.sh to verify."
else
    echo ""
    err "Database initialization failed (exit code: $EXIT_CODE)"
    exit 1
fi
