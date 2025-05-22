#!/bin/bash
set -e

# Check if Clever Cloud CLI is installed
if ! command -v clever &> /dev/null; then
    echo "Clever Cloud CLI not found. Installing..."
    curl -fsSL https://clever-tools.clever-cloud.com/install.sh | bash
fi

# Login to Clever Cloud (if not already logged in)
if ! clever whoami &> /dev/null; then
    echo "Please login to Clever Cloud..."
    clever login
fi

# Create a new application if it doesn't exist
if ! clever apps | grep -q "chromadb"; then
    echo "Creating new ChromaDB application..."
    clever create --type docker chromadb
fi

# Link the application to the current directory
clever link chromadb

# Deploy the application
echo "Deploying ChromaDB..."
clever deploy

# Get the application URL
APP_URL=$(clever url)
echo "ChromaDB is deployed at: $APP_URL"

# Show application status
clever status

# Show application logs
echo "Showing application logs (press Ctrl+C to exit)..."
clever logs --follow 