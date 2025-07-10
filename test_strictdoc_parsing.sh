#!/bin/bash

# Test StrictDoc Parsing
# This script tests if StrictDoc can parse the fixed files

set -e

echo "=== Testing StrictDoc Parsing ==="

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
REQUIREMENTS_DIR="$PROJECT_ROOT/output/requirements"
VENV_DIR="$SCRIPT_DIR/strictdoc/venv2"

# Activate virtual environment
if [[ -d "$VENV_DIR" ]]; then
    echo "Activating virtual environment..."
    source "$VENV_DIR/bin/activate"
else
    echo "Error: Virtual environment not found at $VENV_DIR"
    exit 1
fi

# Test parsing a few files
echo "Testing file parsing..."

# Test the problematic file first
echo "Testing CucoSett.gwt.sdoc..."
if strictdoc parse "output/requirements/administration.ui/CucoSett.gwt.sdoc" > /dev/null 2>&1; then
    echo "✅ CucoSett.gwt.sdoc parses successfully"
else
    echo "❌ CucoSett.gwt.sdoc still has parsing errors"
    exit 1
fi

# Test a few more files
echo "Testing additional files..."
for file in "output/requirements/cuco/web.sdoc" "output/requirements/cuco/pom.sdoc"; do
    if [[ -f "$file" ]]; then
        if strictdoc parse "$file" > /dev/null 2>&1; then
            echo "✅ $(basename "$file") parses successfully"
        else
            echo "❌ $(basename "$file") has parsing errors"
        fi
    fi
done

echo "=== Parsing Test Complete ==="
echo "If all files parse successfully, you can now run the StrictDoc server." 