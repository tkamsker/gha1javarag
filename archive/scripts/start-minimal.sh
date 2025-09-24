#!/bin/bash

echo "🚀 Starting minimal Java Analysis Tool environment..."

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "⚠️  Ollama not detected. Starting Ollama..."
    brew services start ollama
    sleep 3
fi

# Load minimal environment (filter out comments)
if [ -f .env.minimal ]; then
    set -a  # automatically export all variables
    source <(grep -v '^#' .env.minimal | grep -v '^$')
    set +a  # disable automatic export
fi

# Start minimal Docker services
docker-compose -f docker-compose.m3-dev-minimal.yml up -d

echo ""
echo "✅ Minimal environment started!"
echo ""
echo "🌐 Services:"
echo "   • Web Interface: http://localhost:8000"
echo "   • Weaviate: http://localhost:8080" 
echo "   • Local Ollama: http://localhost:11434"
echo "   • Redis: localhost:6379"
echo ""
echo "📊 Resource Usage:"
docker stats --no-stream --format "   • {{.Name}}: {{.MemUsage}} ({{.MemPerc}})"
echo ""
echo "🛠️  Commands:"
echo "   • View logs: docker-compose -f docker-compose.m3-dev-minimal.yml logs -f"
echo "   • Stop: ./stop-minimal.sh"
echo "   • Ollama models: ollama list"
