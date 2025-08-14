#!/bin/bash

# Function to check if a Python module is installed
check_module() {
    python3 -c "import $1" 2>/dev/null
    return $?
}

# Function to install missing dependencies
install_dependencies() {
    echo "Installing missing web dependencies..."
    pip install flask fastapi uvicorn[standard]
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies. Please run: pip install -r requirements.txt"
        exit 1
    fi
}

# Load environment variables
if [ -f .env ]; then
    set -a
    source .env
    set +a
else
    echo "⚠️  Warning: .env file not found. Using default environment."
fi

echo "🤖 Project AI Assistant Web Interface"
echo "====================================="
echo ""

# Check for required web dependencies
flask_available=false
fastapi_available=false

if check_module "flask"; then
    flask_available=true
fi

if check_module "fastapi" && check_module "uvicorn"; then
    fastapi_available=true
fi

# If neither is available, offer to install
if [ "$flask_available" = false ] && [ "$fastapi_available" = false ]; then
    echo "❌ Neither Flask nor FastAPI is installed."
    read -p "Would you like to install the web dependencies now? (y/N): " install_choice
    if [[ $install_choice =~ ^[Yy]$ ]]; then
        install_dependencies
        flask_available=true
        fastapi_available=true
    else
        echo "Please install dependencies with: pip install -r requirements.txt"
        exit 1
    fi
fi

# Show available options
echo "Choose your web framework:"
if [ "$flask_available" = true ]; then
    echo "1) Flask (Recommended for simplicity)"
fi
if [ "$fastapi_available" = true ]; then
    echo "2) FastAPI (Recommended for performance)"
fi
echo ""
read -p "Enter your choice (1 or 2): " choice

case $choice in
    1)
        if [ "$flask_available" = true ]; then
            echo "Starting Flask server..."
            export FLASK_APP=flask_app.py
            export FLASK_ENV=development
            if ! python3 -m flask run --host=0.0.0.0 --port=8000; then
                echo "❌ Failed to start Flask server. Check if flask_app.py exists and all dependencies are installed."
                exit 1
            fi
        else
            echo "❌ Flask is not installed. Please install it with: pip install flask"
            exit 1
        fi
        ;;
    2)
        if [ "$fastapi_available" = true ]; then
            echo "Starting FastAPI server..."
            if ! uvicorn fastapi_app:app --host 0.0.0.0 --port=8000; then
                echo "❌ Failed to start FastAPI server. Check if fastapi_app.py exists and all dependencies are installed."
                exit 1
            fi
        else
            echo "❌ FastAPI/uvicorn is not installed. Please install with: pip install fastapi uvicorn[standard]"
            exit 1
        fi
        ;;
    *)
        echo "Invalid choice."
        if [ "$flask_available" = true ]; then
            echo "Starting Flask by default..."
            export FLASK_APP=flask_app.py
            export FLASK_ENV=development
            python3 -m flask run --host=0.0.0.0 --port=8000
        elif [ "$fastapi_available" = true ]; then
            echo "Starting FastAPI by default..."
            uvicorn fastapi_app:app --host 0.0.0.0 --port=8000
        else
            echo "❌ No web framework available. Please install dependencies."
            exit 1
        fi
        ;;
esac 