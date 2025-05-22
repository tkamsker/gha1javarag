#!/bin/bash

# Exit on error
set -e

echo "Setting up Java Code Search environment..."

# Create and activate virtual environment
echo "Creating virtual environment..."
python -m venv venv
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p vendor build

# Clone tree-sitter-java if not exists
if [ ! -d "vendor/tree-sitter-java" ]; then
    echo "Cloning tree-sitter-java..."
    git clone https://github.com/tree-sitter/tree-sitter-java.git vendor/tree-sitter-java
fi

# Build tree-sitter library
echo "Building tree-sitter library..."
python -c "from tree_sitter import Language; Language.build_library('build/my-languages.so', ['vendor/tree-sitter-java'])"

echo "Setup completed successfully!"
echo "To activate the environment, run: source venv/bin/activate"
echo "To start the API server, run: python src/api/main.py" 