#!/bin/bash

# Exit on error
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print status messages
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

# Function to print error messages
print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install requirements
print_status "Installing requirements..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_error ".env file not found. Please create it with the following content:"
    echo "XML_INPUT_DIR=./docs/xml"
    echo "LOG_LEVEL=INFO"
    echo "CHUNK_SIZE=100"
    exit 1
fi

# Check if XML input directory exists
if [ ! -d "$(grep XML_INPUT_DIR .env | cut -d '=' -f2)" ]; then
    print_error "XML input directory not found. Please ensure Doxygen XML files are present."
    exit 1
fi

# Create output directory if it doesn't exist
print_status "Creating output directory..."
mkdir -p generated_documentation

# Run the documentation generation script
print_status "Starting documentation generation..."
python src/run_documentation_crew.py

# Check if documentation was generated successfully
if [ $? -eq 0 ]; then
    print_status "Documentation generated successfully!"
    print_status "Output files are in the 'generated_documentation' directory."
else
    print_error "Documentation generation failed. Please check the logs for details."
    exit 1
fi

# Deactivate virtual environment
deactivate

print_status "Done!" 