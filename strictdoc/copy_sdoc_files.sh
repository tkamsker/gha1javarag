#!/bin/bash

# Copy SDoc Files to Requirements Directory
# This script copies existing SDoc files to the output/requirements directory

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
REQUIREMENTS_DIR="$PROJECT_ROOT/output/requirements"

echo "=== Copying SDoc Files to Requirements Directory ==="

# Create requirements directory if it doesn't exist
mkdir -p "$REQUIREMENTS_DIR"

# Copy SDoc files from strictdoc directory
echo "Copying SDoc files from strictdoc directory..."

# Copy files from reqdoc directory
if [[ -d "$SCRIPT_DIR/reqdoc" ]]; then
    echo "Copying from reqdoc directory..."
    cp -r "$SCRIPT_DIR/reqdoc"/* "$REQUIREMENTS_DIR/" 2>/dev/null || true
fi

# Copy individual SDoc files
echo "Copying individual SDoc files..."
find "$SCRIPT_DIR" -maxdepth 1 -name "*.sdoc" -exec cp {} "$REQUIREMENTS_DIR/" \;

# Copy from frznbrnf directory if it exists
if [[ -d "$SCRIPT_DIR/frznbrnf" ]]; then
    echo "Copying from frznbrnf directory..."
    find "$SCRIPT_DIR/frznbrnf" -name "*.sdoc" -exec cp {} "$REQUIREMENTS_DIR/" \;
fi

# List copied files
echo "Files in requirements directory:"
ls -la "$REQUIREMENTS_DIR"/*.sdoc 2>/dev/null || echo "No SDoc files found"

echo "Done! You can now run: ./strictdoc/run_server.sh" 