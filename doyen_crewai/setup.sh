#!/bin/bash

# Check if running on M1/M2 Mac
if [[ $(uname -m) == 'arm64' ]]; then
    echo "Detected Apple Silicon (M1/M2) architecture"
    # Ensure we're using the correct Python version
    if ! command -v python3 &> /dev/null; then
        echo "Python3 not found. Please install Python 3 using Homebrew:"
        echo "brew install python@3.11"
        exit 1
    fi
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

# Create virtual environment
echo "Creating virtual environment..."
$PYTHON_CMD -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
$PYTHON_CMD -m pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p docs logs

# Copy example environment file
echo "Setting up environment configuration..."
cp .env.example .env

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "Warning: Ollama not found. Please install it from https://ollama.ai"
    echo "After installation, run: ollama pull all-minilm"
else
    echo "Pulling required Ollama model..."
    ollama pull all-minilm
fi

echo "Setup complete! Please edit .env file with your configuration."
echo "To activate the virtual environment, run: source venv/bin/activate" 