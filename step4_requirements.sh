#!/bin/bash

# =============================
# Step 4: Multi-Agent Requirements Generation
# Uses CrewAI-style approach to generate structured requirements documents
# for both backend services and frontend components
# =============================

set -e

# Function to format seconds into human readable time
format_duration() {
    local seconds=$1
    local hours=$((seconds / 3600))
    local minutes=$(((seconds % 3600) / 60))
    local secs=$((seconds % 60))
    printf "%02d:%02d:%02d" $hours $minutes $secs
}

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
err(){ echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# Record start time
START_TIME_EPOCH=$(date +%s)
START_TIME_FORMATTED=$(date +"%Y-%m-%d %H:%M:%S")

echo "🎯 Multi-Agent Requirements Generation"
echo "======================================"
echo "Start Date: $(date +"%Y-%m-%d")"
echo "Start Time: $(date +"%H:%M:%S")"
echo "Start Timestamp: $START_TIME_FORMATTED"
echo ""

# Ensure we're in the correct directory
cd "$(dirname "$0")"

# Activate virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -f venv/bin/activate ]; then
        info "Activating virtual environment..."
        source venv/bin/activate
    else
        err "Virtual environment not found. Please run: python3 -m venv venv"
    fi
fi

ok "Virtual environment activated"

# Get or detect project name
PROJECT=${1:-$(ls -t data/build/java_calls 2>/dev/null | head -1 | grep -o '^[^_]*' || echo "default-project")}
info "Project name: $PROJECT"

# Check if new_run.sh was run first
if [ ! -d "data/build/java_calls" ] || [ -z "$(ls -A data/build/java_calls 2>/dev/null)" ]; then
    warn "No build artifacts found. Running initial extraction non-interactively..."
    info "Running discover..."
    python main.py discover --project "$PROJECT" --include-frontend || err "discover failed"
    info "Running extract..."
    python main.py extract --project "$PROJECT" --include-frontend || err "extract failed"
    info "Running index..."
    python main.py index --project "$PROJECT" || err "index failed"
else
    info "Build artifacts found, proceeding with requirements generation"
fi

# Check if Weaviate has data
info "Verifying Weaviate has indexed data..."
python -c "
import sys
sys.path.insert(0, 'src')
from store.weaviate_client import WeaviateClient
client = WeaviateClient()
try:
    result = client.client.query.aggregate('BackendDoc').with_meta_count().do()
    count = result.get('data', {}).get('Aggregate', {}).get('BackendDoc', [{}])[0].get('meta', {}).get('count', 0)
    if count == 0:
        print('⚠️  No data in Weaviate. Please run indexing first.')
        sys.exit(1)
    print(f'✓ Found {count} BackendDoc entries in Weaviate')
except Exception as e:
    print(f'⚠️  Could not verify Weaviate data: {e}')
    print('Continuing anyway...')
" || warn "Continuing without Weaviate verification"

# Step 1: Generate Per-Artifact Requirements using CrewAI
echo ""
echo "📝 Step 1: CrewAI Multi-Agent Requirements Generation"
echo "====================================================="
info "Generating detailed requirements using CrewAI with multiple specialized agents..."
info "Agents: Code Analyst, Dependency Analyst, UI Flow Mapper, Technical Writer"
python main.py requirements --project "$PROJECT" --use-crewai || warn "CrewAI requirements generation had issues"

# Step 2: Generate Backend Services Requirements
echo ""
echo "🔧 Step 2: Backend Services Requirements"
echo "======================================="
info "Generating structured backend services requirements document..."

# Create backend requirements using the synthesis agent
python -c "
import sys
sys.path.insert(0, 'src')
from synth.prd_markdown import PRDMarkdownGenerator
from config.settings import settings
import json
from pathlib import Path

# Load backend artifacts
build_dir = settings.build_dir
backend_artifacts = {
    'dao_calls': [],
    'jsp_forms': [],
    'ibatis_statements': [],
    'db_tables': []
}

mapping = {
    'dao_calls': ('java_calls', 'all_dao_calls.json'),
    'jsp_forms': ('jsp_forms', 'all_forms.json'),
    'ibatis_statements': ('ibatis_statements', 'all_statements.json'),
    'db_tables': ('db_schema', 'all_tables.json')
}

for key, (subdir, fname) in mapping.items():
    p = build_dir / subdir / fname
    if p.exists():
        with p.open('r', encoding='utf-8') as f:
            backend_artifacts[key] = json.load(f)

print(f'Loaded {sum(len(v) for v in backend_artifacts.values())} backend artifacts')

# Generate backend requirements document
generator = PRDMarkdownGenerator()
backend_prd = generator.generate_backend_requirements('$PROJECT', backend_artifacts)

output_path = Path('data/output/${PROJECT}_backend_requirements.md')
output_path.write_text(backend_prd, encoding='utf-8')
print(f'✓ Generated backend requirements: {output_path}')
"

# Step 3: Generate Frontend Requirements
echo ""
echo "🎨 Step 3: Frontend Requirements"
echo "================================="
info "Generating structured frontend requirements document..."

python -c "
import sys
sys.path.insert(0, 'src')
from synth.prd_markdown import PRDMarkdownGenerator
from config.settings import settings
import json
from pathlib import Path

# Load frontend artifacts
build_dir = settings.build_dir
frontend_artifacts = {
    'gwt_modules': [],
    'gwt_uibinder': [],
    'gwt_client': [],
    'js_artifacts': []
}

mapping = {
    'gwt_modules': ('gwt_modules', 'all_modules.json'),
    'gwt_uibinder': ('gwt_uibinder', 'all_uibinder.json'),
    'gwt_client': ('gwt_client', 'all_artifacts.json'),
    'js_artifacts': ('js_artifacts', 'all_js_artifacts.json')
}

for key, (subdir, fname) in mapping.items():
    p = build_dir / subdir / fname
    if p.exists():
        with p.open('r', encoding='utf-8') as f:
            data = json.load(f)
            # Handle special case for gwt_client which is a dict
            if key == 'gwt_client' and isinstance(data, dict):
                frontend_artifacts[key] = data
            elif isinstance(data, list):
                frontend_artifacts[key] = data
            elif isinstance(data, dict) and 'activities_places' in data:
                # Extract the list from the dict
                frontend_artifacts[key] = data.get('activities_places', [])
            else:
                frontend_artifacts[key] = data

print(f'Loaded {sum(len(v) if isinstance(v, (list, dict)) else 1 for v in frontend_artifacts.values())} frontend artifacts')

# Generate frontend requirements document
generator = PRDMarkdownGenerator()
frontend_prd = generator.generate_frontend_requirements('$PROJECT', frontend_artifacts)

output_path = Path('data/output/${PROJECT}_frontend_requirements.md')
output_path.write_text(frontend_prd, encoding='utf-8')
print(f'✓ Generated frontend requirements: {output_path}')
"

# Step 4: Generate Consolidated Requirements Document
echo ""
echo "📋 Step 4: Consolidated Requirements Document"
echo "============================================="
info "Generating master requirements document combining backend and frontend..."

python -c "
import sys
sys.path.insert(0, 'src')
from synth.prd_markdown import PRDMarkdownGenerator
from pathlib import Path

# Load both backend and frontend requirements
backend_path = Path('data/output/${PROJECT}_backend_requirements.md')
frontend_path = Path('data/output/${PROJECT}_frontend_requirements.md')

if backend_path.exists() and frontend_path.exists():
    generator = PRDMarkdownGenerator()
    
    with open(backend_path, 'r', encoding='utf-8') as f:
        backend_content = f.read()
    
    with open(frontend_path, 'r', encoding='utf-8') as f:
        frontend_content = f.read()
    
    consolidated = generator.generate_consolidated_requirements('$PROJECT', backend_content, frontend_content)
    
    output_path = Path('data/output/${PROJECT}_full_requirements.md')
    output_path.write_text(consolidated, encoding='utf-8')
    print(f'✓ Generated consolidated requirements: {output_path}')
else:
    print('⚠️  Missing backend or frontend requirements files')
"

# Step 5: Generate Target Solution (Node.js + Postgres + Next.js)
echo ""
echo "🏗️  Step 5: Target Solution Blueprint"
echo "====================================="
info "Generating solution architecture, DB design, and UI plan for Node.js microservices + PostgreSQL + Next.js..."

python -c "
import sys
sys.path.insert(0, 'src')
from synth.solution_agent import SolutionAgent
from pathlib import Path

backend_path = Path('data/output/${PROJECT}_backend_requirements.md')
frontend_path = Path('data/output/${PROJECT}_frontend_requirements.md')
backend_md = backend_path.read_text(encoding='utf-8') if backend_path.exists() else ''
frontend_md = frontend_path.read_text(encoding='utf-8') if frontend_path.exists() else ''

agent = SolutionAgent()
files = agent.run('${PROJECT}', backend_md, frontend_md)
print('✓ Generated solution files:')
for k, v in files.items():
    print(f'  - {k}: {v}')
" || warn "Solution blueprint generation had issues"

# Summary
echo ""
echo "📊 Step 6: Requirements Summary"
echo "==============================="

if [ -d "data/output/requirements/$PROJECT" ]; then
    ARTIFACT_COUNT=$(find "data/output/requirements/$PROJECT" -name "*.md" -type f | wc -l | tr -d ' ')
    info "Generated $ARTIFACT_COUNT per-artifact requirement documents"
fi

if [ -f "data/output/${PROJECT}_backend_requirements.md" ]; then
    BACKEND_SIZE=$(wc -l < "data/output/${PROJECT}_backend_requirements.md" | tr -d ' ')
    info "Backend requirements: $BACKEND_SIZE lines"
fi

if [ -f "data/output/${PROJECT}_frontend_requirements.md" ]; then
    FRONTEND_SIZE=$(wc -l < "data/output/${PROJECT}_frontend_requirements.md" | tr -d ' ')
    info "Frontend requirements: $FRONTEND_SIZE lines"
fi

if [ -f "data/output/${PROJECT}_full_requirements.md" ]; then
    FULL_SIZE=$(wc -l < "data/output/${PROJECT}_full_requirements.md" | tr -d ' ')
    info "Consolidated requirements: $FULL_SIZE lines"
fi

if [ -f "data/output/${PROJECT}_solution.md" ]; then
    SOL_SIZE=$(wc -l < "data/output/${PROJECT}_solution.md" | tr -d ' ')
    info "Solution blueprint: $SOL_SIZE lines"
fi

# Record end time
END_TIME_EPOCH=$(date +%s)
END_TIME_FORMATTED=$(date +"%Y-%m-%d %H:%M:%S")

# Calculate duration
TOTAL_DURATION_SECONDS=$((END_TIME_EPOCH - START_TIME_EPOCH))
DURATION_FORMATTED=$(format_duration $TOTAL_DURATION_SECONDS)

echo ""
echo "🎉 Requirements Generation Complete"
echo "===================================="
echo "End Date: $(date +"%Y-%m-%d")"
echo "End Time: $(date +"%H:%M:%S")"
echo "Duration: $DURATION_FORMATTED (HH:MM:SS)"
echo ""
echo "📁 Output Files:"
echo "   • Per-artifact requirements: data/output/requirements/$PROJECT/"
echo "   • Backend requirements: data/output/${PROJECT}_backend_requirements.md"
echo "   • Frontend requirements: data/output/${PROJECT}_frontend_requirements.md"
echo "   • Full requirements: data/output/${PROJECT}_full_requirements.md"
echo "   • Solution architecture: data/output/${PROJECT}_solution_architecture.md"
echo "   • Database design: data/output/${PROJECT}_db_design.md"
echo "   • UI plan: data/output/${PROJECT}_ui_plan.md"
echo "   • Combined solution: data/output/${PROJECT}_solution.md"
echo ""
ok "Requirements generation complete for project: $PROJECT"

