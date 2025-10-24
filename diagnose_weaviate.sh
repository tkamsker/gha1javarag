#!/bin/bash

# =============================
# Weaviate Diagnostic Script
# Quick diagnosis of common issues
# =============================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

info(){ echo -e "${BLUE}[INFO]${NC} $1"; }
ok(){ echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warn(){ echo -e "${YELLOW}[WARNING]${NC} $1"; }
err(){ echo -e "${RED}[ERROR]${NC} $1"; }
check(){ echo -e "${PURPLE}[CHECK]${NC} $1"; }

echo "🔧 Weaviate Diagnostic Tool"
echo "==========================="
echo ""

# Ensure we're in the correct directory
cd "$(dirname "$0")"

# Check 1: Weaviate Container
check "1. Weaviate Container Status"
if docker ps | grep -q weaviate; then
    ok "Weaviate container is running"
    docker ps | grep weaviate | awk '{print "  Container ID: " $1 ", Status: " $7 ", Ports: " $8}'
else
    err "Weaviate container is not running"
    echo "  Fix: Run ./docker-weaviate.sh"
    exit 1
fi

echo ""

# Check 2: Weaviate API Access
check "2. Weaviate API Access"
if curl -s http://localhost:8080/v1/meta > /dev/null 2>&1; then
    ok "Weaviate API is accessible"
    curl -s http://localhost:8080/v1/meta | python -m json.tool 2>/dev/null | head -10 || echo "  (Could not parse JSON response)"
else
    err "Cannot access Weaviate API at localhost:8080"
    echo "  Fix: Check if Weaviate is running and accessible"
    exit 1
fi

echo ""

# Check 3: Python Environment
check "3. Python Environment"
if [ -d "venv" ]; then
    ok "Virtual environment exists"
    if [ -z "$VIRTUAL_ENV" ]; then
        info "Activating virtual environment..."
        source venv/bin/activate
    fi
    
    # Check Python version
    python_version=$(python --version 2>&1)
    echo "  Python version: $python_version"
    
    # Check required packages
    if python -c "import weaviate" 2>/dev/null; then
        ok "weaviate package is installed"
        weaviate_version=$(python -c "import weaviate; print(weaviate.__version__)" 2>/dev/null)
        echo "  weaviate version: $weaviate_version"
    else
        err "weaviate package not found"
        echo "  Fix: pip install weaviate-client"
        exit 1
    fi
    
    if python -c "import ollama" 2>/dev/null; then
        ok "ollama package is installed"
    else
        warn "ollama package not found (may be needed for embeddings)"
    fi
else
    err "Virtual environment not found"
    echo "  Fix: python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

echo ""

# Check 4: Configuration
check "4. Configuration Check"
if [ -f "src/config/settings.py" ]; then
    ok "Settings file exists"
    
    # Check Weaviate URL
    weaviate_url=$(python -c "
import sys
sys.path.insert(0, 'src')
from config.settings import settings
print(settings.weaviate_url)
" 2>/dev/null)
    echo "  Weaviate URL: $weaviate_url"
    
    # Check Ollama settings
    ollama_url=$(python -c "
import sys
sys.path.insert(0, 'src')
from config.settings import settings
print(settings.ollama_base_url)
" 2>/dev/null)
    echo "  Ollama URL: $ollama_url"
    
    ollama_model=$(python -c "
import sys
sys.path.insert(0, 'src')
from config.settings import settings
print(settings.ollama_embed_model_name)
" 2>/dev/null)
    echo "  Ollama Embed Model: $ollama_model"
else
    err "Settings file not found"
    echo "  Fix: Check src/config/settings.py exists"
    exit 1
fi

echo ""

# Check 5: Data Directory
check "5. Data Directory Structure"
if [ -d "data" ]; then
    ok "Data directory exists"
    echo "  Data directory contents:"
    find data -maxdepth 2 -type d | head -10 | while read dir; do
        echo "    $dir"
    done
    
    json_files=$(find data -name "*.json" -type f | wc -l)
    echo "  JSON files found: $json_files"
    
    if [ $json_files -eq 0 ]; then
        warn "No JSON files found in data directory"
        echo "  Fix: Run discover step first: python main.py discover --project test"
    fi
else
    warn "Data directory not found"
    echo "  Fix: Run discover step first: python main.py discover --project test"
fi

echo ""

# Check 6: Ollama Service (if needed)
check "6. Ollama Service Check"
if command -v ollama >/dev/null 2>&1; then
    ok "Ollama command available"
    
    if ollama list >/dev/null 2>&1; then
        ok "Ollama service is running"
        echo "  Available models:"
        ollama list | head -5 | while read line; do
            echo "    $line"
        done
    else
        warn "Ollama service not running"
        echo "  Fix: Start Ollama service"
    fi
else
    warn "Ollama not installed"
    echo "  Note: Ollama is needed for embeddings, but Weaviate can work without it"
fi

echo ""

# Check 7: Test Weaviate Connection
check "7. Test Weaviate Connection"
python -c "
import sys
sys.path.insert(0, 'src')
from store.weaviate_client import WeaviateClient

try:
    client = WeaviateClient(ensure_schema=False)
    print('✅ Successfully connected to Weaviate')
    
    # Test schema operations
    schema = client.client.schema.get()
    classes = schema.get('classes', [])
    print(f'  Schema classes: {len(classes)}')
    
    # Test data operations
    if classes:
        first_class = classes[0]['class']
        try:
            result = client.client.query.aggregate(first_class).with_meta_count().do()
            count = result.get('data', {}).get('Aggregate', {}).get(first_class, [{}])[0].get('meta', {}).get('count', 0)
            print(f'  Objects in {first_class}: {count}')
        except Exception as e:
            print(f'  Could not count objects in {first_class}: {e}')
    else:
        print('  No classes found in schema')
        
except Exception as e:
    print(f'❌ Failed to connect to Weaviate: {e}')
    exit(1)
" || err "Weaviate connection test failed"

echo ""
echo "🎯 Summary & Recommendations"
echo "============================"
echo ""

# Provide recommendations based on findings
if [ -d "data" ] && [ $(find data -name "*.json" -type f | wc -l) -gt 0 ]; then
    echo "✅ Data files found - ready to index"
    echo "  Next step: python main.py index --project test"
elif [ -d "data" ]; then
    echo "⚠️  Data directory exists but no JSON files found"
    echo "  Next step: python main.py discover --project test"
else
    echo "⚠️  No data directory found"
    echo "  Next step: python main.py discover --project test"
fi

echo ""
echo "🔧 Common Issues & Fixes:"
echo "1. If Weaviate is empty: Run the full pipeline: ./new_run.sh"
echo "2. If discover fails: Check if source code exists in expected locations"
echo "3. If extract fails: Check if required tools are installed"
echo "4. If index fails: Check Weaviate connection and Ollama service"
echo "5. If search fails: Verify data was actually indexed"
