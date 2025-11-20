#!/bin/bash

# =============================
# Manual Fix for Docker Weaviate → Host Ollama
# =============================

echo "🔧 Manual Fix: Docker Weaviate → Host Ollama"
echo "==========================================="

# Get host IP
HOST_IP=$(hostname -I | awk '{print $1}')
echo "Host IP: $HOST_IP"

# Create .env file
cat > .env << EOF
# Ollama Configuration - Fixed for Docker → Host connection
OLLAMA_BASE_URL=http://$HOST_IP:11434
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

echo "✅ Created .env with Ollama URL: http://$HOST_IP:11434"
echo ""
echo "🔍 Testing connection..."

# Test connection
python -c "
import requests
try:
    response = requests.get('http://$HOST_IP:11434/api/tags', timeout=5)
    if response.status_code == 200:
        print('✅ Ollama connection successful')
    else:
        print(f'❌ Ollama connection failed: {response.status_code}')
except Exception as e:
    print(f'❌ Ollama connection failed: {e}')
"

echo ""
echo "🎯 Ready to test!"
echo "Run: python main.py index --project test"
