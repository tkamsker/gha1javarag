#!/bin/bash

# =============================
# Weaviate Data Loading Test Script
# Tests the complete pipeline from data loading to search
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

# Function to format duration
format_duration() {
    local seconds=$1
    local hours=$((seconds / 3600))
    local minutes=$(((seconds % 3600) / 60))
    local secs=$((seconds % 60))
    printf "%02d:%02d:%02d" $hours $minutes $secs
}

# Record start time
START_TIME_EPOCH=$(date +%s)

echo "🧪 Weaviate Data Loading Test"
echo "=============================="
echo "Start Time: $(date +"%Y-%m-%d %H:%M:%S")"
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

# Test project name
TEST_PROJECT="test_$(date +%Y%m%d_%H%M%S)"
info "Test project name: $TEST_PROJECT"

echo ""
echo "🔍 Step 1: Pre-test Weaviate Status"
echo "===================================="

# Check Weaviate connection and current state
$PYTHON_CMD -c "
import sys
sys.path.insert(0, 'src')
from store.weaviate_client import WeaviateClient

print('Testing Weaviate connection...')
client = WeaviateClient(ensure_schema=False)

# Get current schema
schema = client.client.schema.get()
classes = schema.get('classes', [])
print(f'Current classes in Weaviate: {len(classes)}')

for cls in classes:
    class_name = cls.get('class', 'Unknown')
    print(f'  - {class_name}')

# Check if we have any data
total_objects = 0
for cls in classes:
    class_name = cls.get('class', 'Unknown')
    try:
        result = client.client.query.aggregate(class_name).with_meta_count().do()
        count = result.get('data', {}).get('Aggregate', {}).get(class_name, [{}])[0].get('meta', {}).get('count', 0)
        total_objects += count
        print(f'  {class_name}: {count} objects')
    except Exception as e:
        print(f'  {class_name}: Error getting count - {e}')

print(f'Total objects in Weaviate: {total_objects}')
"

echo ""
echo "🔍 Step 2: Test Data Discovery"
echo "=============================="

# Test the discover step
test_step "Running discover step..."
$PYTHON_CMD main.py discover --project "$TEST_PROJECT" --include-frontend || warn "Discover step failed"

# Check what files were discovered
if [ -d "data/build" ]; then
    info "Checking discovered files..."
    find data/build -name "*.json" -type f | head -10 | while read file; do
        file_size=$(wc -c < "$file")
        echo "  📄 $(basename "$file"): $file_size bytes"
    done
else
    warn "No data/build directory found after discover step"
fi

echo ""
echo "🔍 Step 3: Test Data Extraction"
echo "==============================="

# Test the extract step
test_step "Running extract step..."
$PYTHON_CMD main.py extract --project "$TEST_PROJECT" --include-frontend || warn "Extract step failed"

# Check what was extracted
if [ -d "data/build" ]; then
    info "Checking extracted data..."
    for subdir in data/build/*/; do
        if [ -d "$subdir" ]; then
            subdir_name=$(basename "$subdir")
            file_count=$(find "$subdir" -name "*.json" -type f | wc -l)
            echo "  📁 $subdir_name: $file_count JSON files"
        fi
    done
fi

echo ""
echo "🔍 Step 4: Test Data Indexing"
echo "============================="

# Test the index step
test_step "Running index step..."
$PYTHON_CMD main.py index --project "$TEST_PROJECT" || warn "Index step failed"

echo ""
echo "🔍 Step 5: Post-index Weaviate Status"
echo "====================================="

# Check Weaviate after indexing
$PYTHON_CMD -c "
import sys
sys.path.insert(0, 'src')
from store.weaviate_client import WeaviateClient

print('Checking Weaviate after indexing...')
client = WeaviateClient(ensure_schema=False)

# Get current schema
schema = client.client.schema.get()
classes = schema.get('classes', [])
print(f'Classes in Weaviate: {len(classes)}')

total_objects = 0
project_objects = 0

for cls in classes:
    class_name = cls.get('class', 'Unknown')
    try:
        # Total count
        result = client.client.query.aggregate(class_name).with_meta_count().do()
        count = result.get('data', {}).get('Aggregate', {}).get(class_name, [{}])[0].get('meta', {}).get('count', 0)
        total_objects += count
        
        # Count for our test project
        project_result = client.client.query.get(
            class_name=class_name,
            properties=['project']
        ).with_where({
            'path': ['project'],
            'operator': 'Equal',
            'valueString': '$TEST_PROJECT'
        }).do()
        
        project_count = len(project_result.get('data', {}).get('Get', {}).get(class_name, []))
        project_objects += project_count
        
        if count > 0:
            print(f'  ✅ {class_name}: {count} total, {project_count} for test project')
        else:
            print(f'  📭 {class_name}: No objects')
            
    except Exception as e:
        print(f'  ❌ {class_name}: Error - {e}')

print(f'\\nTotal objects in Weaviate: {total_objects}')
print(f'Objects for test project \"$TEST_PROJECT\": {project_objects}')
"

echo ""
echo "🔍 Step 6: Test Search Functionality"
echo "===================================="

# Test search functionality
$PYTHON_CMD -c "
import sys
sys.path.insert(0, 'src')
from store.weaviate_client import WeaviateClient

print('Testing search functionality...')
client = WeaviateClient(ensure_schema=False)

# Test search for our project
try:
    # Search for any artifacts in our test project
    result = client.client.query.get(
        class_name='BackendDoc',
        properties=['project', 'path', 'text']
    ).with_where({
        'path': ['project'],
        'operator': 'Equal',
        'valueString': '$TEST_PROJECT'
    }).with_limit(5).do()
    
    artifacts = result.get('data', {}).get('Get', {}).get('BackendDoc', [])
    print(f'Found {len(artifacts)} BackendDoc artifacts for test project')
    
    for i, artifact in enumerate(artifacts[:3]):
        path = artifact.get('path', 'Unknown')
        text_preview = artifact.get('text', '')[:100] + '...' if len(artifact.get('text', '')) > 100 else artifact.get('text', '')
        print(f'  {i+1}. {path}: {text_preview}')
        
except Exception as e:
    print(f'Search test failed: {e}')

# Test vector search
try:
    print('\\nTesting vector search...')
    result = client.client.query.get(
        class_name='BackendDoc',
        properties=['project', 'path', 'text']
    ).with_near_text({'concepts': ['java']}).with_limit(3).do()
    
    artifacts = result.get('data', {}).get('Get', {}).get('BackendDoc', [])
    print(f'Vector search found {len(artifacts)} artifacts')
    
except Exception as e:
    print(f'Vector search failed: {e}')
"

echo ""
echo "🔍 Step 7: Debug Information"
echo "============================"

# Show debug information
debug "Environment variables:"
env | grep -E "(OLLAMA|WEAVIATE)" | sort || echo "No relevant environment variables found"

debug "Python path:"
$PYTHON_CMD -c "import sys; print('\\n'.join(sys.path))"

debug "Installed packages:"
$PYTHON_CMD -c "import pkg_resources; [print(f'{pkg.project_name}=={pkg.version}') for pkg in pkg_resources.working_set if 'weaviate' in pkg.project_name.lower() or 'ollama' in pkg.project_name.lower()]"

# Check if data files exist
debug "Data directory structure:"
if [ -d "data" ]; then
    find data -type f -name "*.json" | head -20 | while read file; do
        echo "  $file"
    done
else
    echo "  No data directory found"
fi

# Record end time
END_TIME_EPOCH=$(date +%s)
TOTAL_DURATION_SECONDS=$((END_TIME_EPOCH - START_TIME_EPOCH))
DURATION_FORMATTED=$(format_duration $TOTAL_DURATION_SECONDS)

echo ""
echo "🎉 Test Complete"
echo "================"
echo "End Time: $(date +"%Y-%m-%d %H:%M:%S")"
echo "Duration: $DURATION_FORMATTED"
echo "Test Project: $TEST_PROJECT"
echo ""
echo "📋 Next Steps:"
echo "1. Review the output above for any errors"
echo "2. Check if data was successfully indexed"
echo "3. Verify search functionality works"
echo "4. If issues found, check the debug information"
