#!/bin/bash

# Simple StrictDoc Server Runner
# This script runs StrictDoc server with the requirements directory

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
REQUIREMENTS_DIR="$PROJECT_ROOT/output/requirements"
VENV_DIR="$SCRIPT_DIR/venv2"

echo "=== StrictDoc Server Runner ==="

# Check if virtual environment exists
if [[ ! -d "$VENV_DIR" ]]; then
    echo "Error: Virtual environment not found at $VENV_DIR"
    echo "Please ensure the virtual environment is set up with StrictDoc installed"
    exit 1
fi

# Create requirements directory if it doesn't exist
mkdir -p "$REQUIREMENTS_DIR"

# Check if there are any SDoc files
if [[ -z "$(find "$REQUIREMENTS_DIR" -name "*.sdoc" 2>/dev/null)" ]]; then
    echo "Warning: No SDoc files found in $REQUIREMENTS_DIR"
    echo "Creating a sample file..."
    
    cat > "$REQUIREMENTS_DIR/sample.sdoc" << 'EOF'
[DOCUMENT]
TITLE: Sample Requirement
UID: SAMPLE_001
VERSION: 1.0

[GRAMMAR]
ELEMENTS:
- TAG: REQUIREMENT
  FIELDS:
  - TITLE: UID
    TYPE: String
    REQUIRED: True
  - TITLE: STATEMENT
    TYPE: String
    REQUIRED: True

[REQUIREMENT]
UID: REQ_001
STATEMENT: >>>
This is a sample requirement for testing the StrictDoc server.
<<<
EOF
    echo "Created sample.sdoc"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Change to requirements directory
cd "$REQUIREMENTS_DIR"

echo "Starting StrictDoc server..."
echo "Server will be available at: http://localhost:5111"
echo "Requirements directory: $REQUIREMENTS_DIR"
echo "Press Ctrl+C to stop the server"

# Run StrictDoc server
strictdoc server . --port 5111 --host 0.0.0.0 