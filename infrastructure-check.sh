#!/bin/bash

echo "🔍 Enhanced Weaviate Infrastructure Status Check"
echo "================================================"

# Check Weaviate
if curl -s http://localhost:8080/v1/.well-known/ready > /dev/null 2>&1; then
    echo "✅ Weaviate: Running on http://localhost:8080"
    WEAVIATE_VERSION=$(curl -s http://localhost:8080/v1/meta | jq -r .version 2>/dev/null || echo "unknown")
    echo "   Version: $WEAVIATE_VERSION"
else
    echo "❌ Weaviate: Not accessible on http://localhost:8080"
    echo "   Start with: docker run -d --name weaviate -p 8080:8080 -p 50051:50051 semitechnologies/weaviate:latest"
fi

# Check Ollama
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama: Running on http://localhost:11434"
    OLLAMA_MODELS=$(curl -s http://localhost:11434/api/tags | jq -r '.models | length' 2>/dev/null || echo "unknown")
    echo "   Models available: $OLLAMA_MODELS"
    echo "   Required models:"
    
    # Check for embedding model
    if curl -s http://localhost:11434/api/tags | grep -q "nomic-embed-text"; then
        echo "   ✅ nomic-embed-text (embedding)"
    else
        echo "   ❌ nomic-embed-text (embedding) - Run: ollama pull nomic-embed-text"
    fi
    
    # Check for main model (case-insensitive)
    if curl -s http://localhost:11434/api/tags | grep -qi "qwen.*coder"; then
        echo "   ✅ Qwen Coder model (main model)"
        # Show the actual model name found
        QWEN_MODEL=$(curl -s http://localhost:11434/api/tags | jq -r '.models[].name' | grep -i "qwen.*coder" | head -1)
        if [ -n "$QWEN_MODEL" ]; then
            echo "      Found: $QWEN_MODEL"
        fi
    else
        echo "   ❌ Qwen Coder model - Run: ollama pull danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth"
        echo "      Or alternative: ollama pull qwen2.5-coder:7b (smaller model)"
    fi
else
    echo "❌ Ollama: Not accessible on http://localhost:11434"
    echo "   Start with: ollama serve"
fi

# Check Python dependencies
echo ""
echo "🐍 Python Dependencies:"
python3 -c "
import sys

# Test Weaviate client
try:
    import weaviate
    try:
        # Try to import a basic component without triggering the error
        weaviate_version = getattr(weaviate, '__version__', 'unknown')
        print('   ✅ weaviate-client: installed (version: ' + str(weaviate_version) + ')')
        
        # Try to test actual compatibility
        try:
            from weaviate.auth import AuthApiKey
            print('   ✅ weaviate-client: API compatible')
        except Exception as api_err:
            print('   ⚠️  weaviate-client: may have compatibility issues')
            print('   Error: ' + str(api_err)[:80])
    except Exception as inner_e:
        print('   ⚠️  weaviate-client: installed but has import issues')
        print('   Try: pip uninstall weaviate-client && pip install \"weaviate-client>=4.5.0,<4.8.0\"')
except ImportError:
    print('   ❌ weaviate-client not installed')
    print('   Install: pip install \"weaviate-client>=4.5.0,<4.8.0\"')

# Test other dependencies
try:
    import aiohttp
    print('   ✅ aiohttp:', aiohttp.__version__)
except ImportError:
    print('   ❌ aiohttp not installed - Run: pip install aiohttp')

try:
    import asyncio
    print('   ✅ asyncio: available')
except ImportError:
    print('   ❌ asyncio not available')

try:
    import javalang
    print('   ✅ javalang: available')
except ImportError:
    print('   ❌ javalang not installed - Run: pip install javalang')
"

echo ""
echo "💾 System Resources:"
if [[ "$OSTYPE" == "darwin"* ]]; then
    MEMORY_GB=$(sysctl -n hw.memsize | awk '{print int($0/1024/1024/1024)}')
    echo "   Memory: ${MEMORY_GB}GB"
    if [ "$MEMORY_GB" -lt 32 ]; then
        echo "   ⚠️  Warning: Less than 32GB memory may cause performance issues with large models"
    fi
elif command -v free >/dev/null 2>&1; then
    MEMORY_INFO=$(free -h | grep "Mem:" | awk '{print $2}')
    echo "   Memory: $MEMORY_INFO"
fi

echo ""
echo "📁 Directory Structure:"
for dir in output data/weaviate logs; do
    if [ -d "$dir" ]; then
        echo "   ✅ $dir/"
    else
        echo "   ❓ $dir/ (will be created automatically)"
    fi
done

echo ""
echo "⚙️  Environment Configuration:"
if [ -f ".env" ]; then
    echo "   ✅ .env file exists"
    if grep -q "AI_PROVIDER" .env; then
        AI_PROVIDER=$(grep "AI_PROVIDER" .env | cut -d'=' -f2)
        echo "   AI Provider: $AI_PROVIDER"
    fi
    if grep -q "OLLAMA_MODEL_NAME" .env; then
        OLLAMA_MODEL=$(grep "OLLAMA_MODEL_NAME" .env | cut -d'=' -f2)
        echo "   Ollama Model: $OLLAMA_MODEL"
    fi
else
    echo "   ❌ .env file missing - Copy from env.example"
fi

echo ""
echo "🔧 Next Steps:"
echo "   1. Fix Weaviate client: pip uninstall weaviate-client && pip install \"weaviate-client>=4.5.0,<4.9.0\""
echo "   2. Re-run this check: ./infrastructure-check.sh"
echo "   3. Then run: ./Step1_Enhanced_Weaviate.sh test"
echo "   4. Check output in: ./output/"
echo "   5. Use web interface: ./start_web.sh"