#!/bin/bash

# =============================
# Weaviate Search Script
# Shows available projects and entity counts
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
err(){ echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# Function to format numbers with commas
format_number() {
    printf "%'d" "$1"
}

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

echo "🔍 Weaviate Search & Analysis"
echo "============================="
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

# Test Weaviate connection
info "Testing Weaviate connection..."
$PYTHON_CMD -c "
import sys
sys.path.insert(0, 'src')
from store.weaviate_client import WeaviateClient
try:
    client = WeaviateClient(ensure_schema=False)
    print('✅ Weaviate connection successful')
    # Don't call close() as it may not exist in this version
except Exception as e:
    print(f'❌ Weaviate connection failed: {e}')
    sys.exit(1)
" || err "Weaviate connection failed"

echo ""
echo "📊 Analyzing Weaviate Data..."
echo "============================="

# Run the Python analysis script
$PYTHON_CMD -c "
import sys
import json
from collections import defaultdict
from datetime import datetime
sys.path.insert(0, 'src')
from store.weaviate_client import WeaviateClient

# All available entity types
ENTITY_TYPES = [
    'IbatisStatement', 'DaoCall', 'JspForm', 'DbTable', 'Flow', 'Requirement',
    'GwtModule', 'GwtUiBinder', 'GwtActivityPlace', 'GwtEndpoint', 
    'JsArtifact', 'FrontendRoute', 'BackendDoc'
]

def get_entity_counts():
    client = WeaviateClient(ensure_schema=False)
    project_data = defaultdict(lambda: defaultdict(int))
    total_entities = 0
    
    print('🔍 Scanning entity types...')
    
    for entity_type in ENTITY_TYPES:
        try:
            # Check if class exists
            if not client.client.schema.exists(entity_type):
                print(f'  ⚠️  {entity_type}: Class does not exist')
                continue
                
            # Get total count for this entity type
            result = client.client.query.aggregate(entity_type).with_meta_count().do()
            count = result.get('data', {}).get('Aggregate', {}).get(entity_type, [{}])[0].get('meta', {}).get('count', 0)
            
            if count > 0:
                print(f'  ✅ {entity_type}: {count:,} entities')
                
                # Get projects for this entity type
                projects_result = client.client.query.get(
                    class_name=entity_type,
                    properties=['project']
                ).with_group_by(['project']).do()
                
                projects = projects_result.get('data', {}).get('Get', {}).get(entity_type, [])
                
                for project_data_item in projects:
                    project_name = project_data_item.get('project', 'Unknown')
                    project_data[project_name][entity_type] = count
                    total_entities += count
            else:
                print(f'  📭 {entity_type}: No entities')
                
        except Exception as e:
            print(f'  ❌ {entity_type}: Error - {e}')
    
    print(f'\\n📈 Summary:')
    print(f'Total entities across all types: {total_entities:,}')
    print(f'Projects found: {len(project_data)}')
    
    if project_data:
        print(f'\\n📋 Projects and Entity Counts:')
        print('=' * 60)
        
        for project_name in sorted(project_data.keys()):
            print(f'\\n🏗️  Project: {project_name}')
            print('-' * 40)
            
            project_entities = project_data[project_name]
            project_total = sum(project_entities.values())
            
            for entity_type in ENTITY_TYPES:
                count = project_entities.get(entity_type, 0)
                if count > 0:
                    percentage = (count / project_total) * 100
                    print(f'  {entity_type:20} {count:>8,} ({percentage:5.1f}%)')
            
            print(f'  {\"TOTAL\":20} {project_total:>8,}')
    
    else:
        print('\\n📭 No projects found in Weaviate')
    
    # Don't call close() as it may not exist in this version

if __name__ == '__main__':
    get_entity_counts()
"

# Record end time
END_TIME_EPOCH=$(date +%s)
TOTAL_DURATION_SECONDS=$((END_TIME_EPOCH - START_TIME_EPOCH))
DURATION_FORMATTED=$(format_duration $TOTAL_DURATION_SECONDS)

echo ""
echo "🎉 Search Complete"
echo "=================="
echo "End Time: $(date +"%Y-%m-%d %H:%M:%S")"
echo "Duration: $DURATION_FORMATTED"
echo ""
