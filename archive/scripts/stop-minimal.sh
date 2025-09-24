#!/bin/bash

echo "🛑 Stopping minimal Java Analysis Tool environment..."

docker-compose -f docker-compose.m3-dev-minimal.yml down

echo "✅ Docker services stopped!"
echo ""
echo "ℹ️  Local Ollama is still running (use 'brew services stop ollama' to stop)"
