#!/bin/bash

echo "🧪 Testing minimal environment..."

# Test Ollama
echo -n "Ollama: "
if curl -s http://localhost:11434/api/tags >/dev/null; then
    echo "✅ Running"
else
    echo "❌ Not responding"
fi

# Test Weaviate
echo -n "Weaviate: "
if curl -s http://localhost:8080/v1/.well-known/ready >/dev/null; then
    echo "✅ Running"  
else
    echo "❌ Not responding"
fi

# Test Redis
echo -n "Redis: "
if docker exec $(docker-compose -f docker-compose.m3-dev-minimal.yml ps -q redis 2>/dev/null) redis-cli ping 2>/dev/null | grep -q PONG; then
    echo "✅ Running"
else
    echo "❌ Not responding" 
fi

# Test Web Interface
echo -n "Web Interface: "
if curl -s http://localhost:8000/api/health >/dev/null; then
    echo "✅ Running"
else
    echo "❌ Not responding"
fi

echo ""
echo "📊 Current Docker usage:"
docker stats --no-stream --format "{{.Name}}: {{.MemUsage}} CPU: {{.CPUPerc}}"
