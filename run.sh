#!/bin/bash

# Ensure the script is run from the project root
if [ ! -f "src/main.py" ]; then
    echo "Error: 'src/main.py' not found. Please run this script from the project root."
    exit 1
fi

# Set PYTHONPATH to include the current directory so Python can find 'src'
export PYTHONPATH=$(pwd):$PYTHONPATH

# Determine project name
PROJECT_NAME="test" # Default project name
if [ -n "$1" ]; then # If a parameter is provided
    PROJECT_NAME="$1"
fi

# Activate virtual environment if it exists (optional, but good practice)
# if [ -d ".venv" ]; then
#     echo "Activating virtual environment..."
#     source .venv/bin/activate
# fi

# Run the main application
echo "Running GEMINI pipeline for project: $PROJECT_NAME..."
python src/main.py all --project "$PROJECT_NAME" --include-frontend

# Deactivate virtual environment (if activated)
# if [ -d ".venv" ]; then
#     deactivate
# fi
