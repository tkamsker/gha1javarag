#!/bin/bash

# =============================
# Test Indexing Process
# Debug why data isn't being indexed into Weaviate
# =============================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

info(){ echo -e "${BLUE}[INFO]${NC} $1"; }
ok(){ echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warn(){ echo -e "${YELLOW}[WARNING]${NC} $1"; }
err(){ echo -e "${RED}[ERROR]${NC} $1"; }
test_step(){ echo -e "${CYAN}[TEST]${NC} $1"; }
debug(){ echo -e "${PURPLE}[DEBUG]${NC} $1"; }

echo "🔍 Testing Indexing Process"
echo "==========================="
echo ""

# Ensure we're in the correct directory
cd "$(dirname "$0")"

# Activate virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    info "Activating virtual environment..."
    source venv/bin/activate || err "Failed to activate virtual environment"
fi

# Use venv python explicitly
PYTHON_CMD="$VIRTUAL_ENV/bin/python"
if [ ! -f "$PYTHON_CMD" ]; then
    err "Virtual environment Python not found at $PYTHON_CMD"
fi

TEST_PROJECT="test_indexing_$(date +%Y%m%d_%H%M%S)"
info "Test project: $TEST_PROJECT"

echo ""
echo "🔍 Step 1: Check Data Files"
echo "==========================="

# Check what data files exist
debug "Checking data/build directory structure..."
find data/build -name "*.json" -type f | head -20 | while read file; do
    file_size=$(wc -c < "$file")
    echo "  📄 $(basename "$file"): $file_size bytes"
done

echo ""
echo "🔍 Step 2: Test Manual Indexing"
echo "==============================="

# Test indexing a specific file manually
test_step "Testing manual indexing of BackendDoc data..."

$PYTHON_CMD -c "
import sys
import json
sys.path.insert(0, 'src')
from store.weaviate_client import WeaviateClient

print('Loading BackendDoc data...')
try:
    # Load backend docs
    with open('data/build/backend_docs/all_backend_docs.json', 'r', encoding='utf-8') as f:
        backend_docs = json.load(f)
    
    print(f'Found {len(backend_docs)} BackendDoc entries')
    
    if backend_docs:
        # Show first entry structure
        first_doc = backend_docs[0]
        print('First document structure:')
        for key, value in first_doc.items():
            if isinstance(value, str) and len(value) > 100:
                print(f'  {key}: {value[:100]}...')
            else:
                print(f'  {key}: {value}')
        
        print('\\nTesting Weaviate indexing...')
        client = WeaviateClient(ensure_schema=False)
        
        # Test indexing first document
        test_doc = backend_docs[0].copy()
        test_doc['project'] = '$TEST_PROJECT'
        
        print('Indexing test document...')
        result = client.index_artifact('BackendDoc', test_doc)
        print(f'✅ Successfully indexed document with ID: {result}')
        
        # Verify it was indexed
        print('\\nVerifying indexing...')
        search_result = client.client.query.get(
            class_name='BackendDoc',
            properties=['project', 'path', 'text']
        ).with_where({
            'path': ['project'],
            'operator': 'Equal',
            'valueString': '$TEST_PROJECT'
        }).do()
        
        found_docs = search_result.get('data', {}).get('Get', {}).get('BackendDoc', [])
        print(f'Found {len(found_docs)} documents for test project')
        
        if found_docs:
            print('✅ Manual indexing test successful!')
        else:
            print('❌ Manual indexing test failed - document not found')
    else:
        print('❌ No BackendDoc data found')
        
except Exception as e:
    print(f'❌ Manual indexing test failed: {e}')
    import traceback
    traceback.print_exc()
"

echo ""
echo "🔍 Step 3: Test Full Index Command"
echo "=================================="

# Test the actual index command
test_step "Running: python main.py index --project $TEST_PROJECT"

# First, let's see what the index command actually does
$PYTHON_CMD -c "
import sys
sys.path.insert(0, 'src')
from config.settings import settings

print('Configuration check:')
print(f'  Build directory: {settings.build_dir}')
print(f'  Default project: {settings.default_project_name}')

# Check if build directory exists and what's in it
import os
if os.path.exists(settings.build_dir):
    print(f'  Build directory exists: {settings.build_dir}')
    for item in os.listdir(settings.build_dir):
        item_path = os.path.join(settings.build_dir, item)
        if os.path.isdir(item_path):
            json_files = [f for f in os.listdir(item_path) if f.endswith('.json')]
            print(f'    {item}: {len(json_files)} JSON files')
else:
    print(f'  Build directory does not exist: {settings.build_dir}')
"

echo ""
echo "🔍 Step 4: Run Index Command with Debug"
echo "======================================"

# Run the index command with verbose output
info "Running index command..."
$PYTHON_CMD main.py index --project "$TEST_PROJECT" --verbose || warn "Index command failed"

echo ""
echo "🔍 Step 5: Verify Results"
echo "========================"

# Check if data was actually indexed
$PYTHON_CMD -c "
import sys
sys.path.insert(0, 'src')
from store.weaviate_client import WeaviateClient

print('Checking Weaviate after indexing...')
client = WeaviateClient(ensure_schema=False)

# Get all classes and their counts
schema = client.client.schema.get()
classes = schema.get('classes', [])

total_objects = 0
for cls in classes:
    class_name = cls.get('class', 'Unknown')
    try:
        result = client.client.query.aggregate(class_name).with_meta_count().do()
        count = result.get('data', {}).get('Aggregate', {}).get(class_name, [{}])[0].get('meta', {}).get('count', 0)
        total_objects += count
        if count > 0:
            print(f'  ✅ {class_name}: {count} objects')
        else:
            print(f'  📭 {class_name}: No objects')
    except Exception as e:
        print(f'  ❌ {class_name}: Error - {e}')

print(f'\\nTotal objects in Weaviate: {total_objects}')

# Check specifically for our test project
print(f'\\nChecking for test project: $TEST_PROJECT')
for cls in classes:
    class_name = cls.get('class', 'Unknown')
    try:
        result = client.client.query.get(
            class_name=class_name,
            properties=['project']
        ).with_where({
            'path': ['project'],
            'operator': 'Equal',
            'valueString': '$TEST_PROJECT'
        }).do()
        
        count = len(result.get('data', {}).get('Get', {}).get(class_name, []))
        if count > 0:
            print(f'  ✅ {class_name}: {count} objects for test project')
    except Exception as e:
        print(f'  ❌ {class_name}: Error checking test project - {e}')
"

echo ""
echo "🎯 Analysis Complete"
echo "==================="
echo ""
echo "If indexing failed, check:"
echo "1. Are the JSON files in the expected format?"
echo "2. Are there any errors in the index command output?"
echo "3. Is the Weaviate client working correctly?"
echo "4. Are there any permission issues?"
