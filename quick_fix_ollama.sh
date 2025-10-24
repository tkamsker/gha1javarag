#!/bin/bash

# =============================
# Quick Fix for Ollama Configuration
# =============================

set -e

echo "🔧 Quick Fix: Ollama Configuration"
echo "=================================="

# Create .env file with correct Ollama URL
cat > .env << 'EOF'
# Ollama Configuration - Fixed for localhost
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL_NAME=gemma3:12b
OLLAMA_EMBED_MODEL_NAME=nomic-embed-text

# Weaviate Configuration
WEAVIATE_URL=http://localhost:8080
WEAVIATE_API_KEY=

# Java Source Directory (update this to your actual source path)
JAVA_SOURCE_DIR=/path/to/your/java/source

# Default Project
DEFAULT_PROJECT_NAME=default-project
EOF

echo "✅ Created .env file with localhost Ollama URL"
echo ""
echo "🔍 Testing the fix..."

# Test the configuration
python -c "
import sys
sys.path.insert(0, 'src')
from config.settings import settings
print(f'Ollama URL: {settings.ollama_base_url}')

# Test connection
import requests
try:
    response = requests.get(f'{settings.ollama_base_url}/api/tags', timeout=5)
    if response.status_code == 200:
        print('✅ Ollama connection successful')
    else:
        print(f'❌ Ollama connection failed: {response.status_code}')
except Exception as e:
    print(f'❌ Ollama connection failed: {e}')
"

echo ""
echo "🎯 Ready to test indexing!"
echo "Run: python main.py index --project test"
