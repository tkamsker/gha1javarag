#!/bin/bash

# Load environment variables
set -a
source .env
set +a

echo "🤖 Project AI Assistant Web Interface"
echo "====================================="
echo ""
echo "Choose your web framework:"
echo "1) Flask (Recommended for simplicity)"
echo "2) FastAPI (Recommended for performance)"
echo ""
read -p "Enter your choice (1 or 2): " choice

case $choice in
    1)
        echo "Starting Flask server..."
        export FLASK_APP=flask_app.py
        export FLASK_ENV=development
        python -m flask run --host=0.0.0.0 --port=8000
        ;;
    2)
        echo "Starting FastAPI server..."
        uvicorn fastapi_app:app --host 0.0.0.0 --port=8000
        ;;
    *)
        echo "Invalid choice. Starting Flask by default..."
        export FLASK_APP=flask_app.py
        export FLASK_ENV=development
        python -m flask run --host=0.0.0.0 --port=8000
        ;;
esac 