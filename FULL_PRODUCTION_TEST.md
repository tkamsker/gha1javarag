# Full Production Test - Step by Step Guide

This guide walks you through running a complete production test using existing shell scripts, including the new HTML/HTM extraction and frontend trace features.

## Prerequisites

1. **Virtual environment activated**
2. **Weaviate running** (Docker container)
3. **Ollama running** (for LLM features)
4. **Java source code** available at `JAVA_SOURCE_DIR`

## Step-by-Step Process

### Step 1: Verify Environment

```bash
# Navigate to project directory
cd /path/to/gha1javarag

# Activate virtual environment
source venv/bin/activate

# Verify Weaviate is running
curl http://localhost:8080/v1/meta

# Verify Ollama is running
curl http://localhost:11434/api/tags
```

### Step 2: Start Weaviate (if not running)

```bash
# Start Weaviate using Docker Compose
docker-compose up -d

# Or use the simple start script
./start_weaviate_simple.sh

# Verify it's running
curl http://localhost:8080/v1/meta
```

### Step 3: Extract All Artifacts (Including HTML)

This step extracts all artifacts from your Java source code, **including the new HTML/HTM files with GWT detection**.

```bash
# Extract all artifacts including frontend (HTML, JSP, GWT, JS)
python main.py extract --include-frontend

# This will:
# - Discover all files (Java, JSP, GWT, JS, XML, SQL, HTML/HTM)
# - Extract artifacts including:
#   * iBATIS statements
#   * DAO calls
#   * JSP forms
#   * Database schema
#   * Backend docs (LLM summaries)
#   * GWT modules
#   * GWT client code (Activities/Places)
#   * GWT UiBinder files
#   * JavaScript artifacts
#   * HTML/HTM artifacts (NEW - with GWT feature detection)
```

**Expected output:**
- Artifacts saved to `data/build/` directory
- HTML artifacts saved to `data/build/html_artifacts/all_html_artifacts.json`
- Console shows extraction progress and counts

**Time estimate:** 10-30 minutes (depending on codebase size)

### Step 4: Index All Artifacts in Weaviate

This step loads all extracted artifacts (including HTML) into Weaviate for semantic search.

```bash
# Index all artifacts (preserves project names from artifacts)
python main.py index --all-projects

# This will:
# - Load all artifact JSON files from data/build/
# - Index them in Weaviate with proper project names
# - Include the new HtmlArtifact class
```

**Expected output:**
- Console shows indexing progress for each artifact type
- Total count of indexed artifacts
- HTML artifacts indexed in `HtmlArtifact` class

**Time estimate:** 5-15 minutes (depending on data size)

### Step 5: Verify Indexing

```bash
# Check Weaviate statistics
./weaviate_stats.sh

# Or use Python script
python weaviate_stats.py

# Expected output shows:
# - Total objects per class
# - Should include HtmlArtifact objects
# - Project distribution
```

**Verify HTML artifacts were indexed:**
```bash
# Search for HTML artifacts
python main.py search --query "html" --frontend --limit 10

# Should show HTML artifacts with GWT features detected
```

### Step 6: Generate Requirements (Full Pipeline)

This step generates comprehensive requirements using CrewAI with the new frontend trace agent.

```bash
# Option A: Generate for ALL projects (recommended for full test)
./start_requirements_generation.sh 1

# Option B: Generate for specific project
./start_requirements_generation.sh 2 cuco-ui-admin

# Option C: Generate for top 10 projects
./start_requirements_generation.sh 3
```

**What happens:**
1. Verifies Weaviate connection
2. Checks indexed data
3. Runs CrewAI multi-agent workflow:
   - **Backend Architecture Analyst** - analyzes backend code
   - **Dependency Analyst** - maps dependencies
   - **Frontend Trace Specialist** (NEW) - traces ALL frontend files (HTML, JSP, GWT, JS)
   - **Frontend Architecture Analyst** - maps frontend to Next.js/React
   - **Placeholder Fulfillment Agent** - fills in missing information
   - **Technical Writer** - creates final requirements document

**Expected output:**
- Requirements files in `output/` directory
- Format: `{project}_crewai_requirements.md`
- Each file includes complete frontend trace results

**Time estimate:** 
- Per project: 10-60 minutes
- All projects: 8-15 hours

### Step 7: Monitor Progress

```bash
# Find the log file
ls -lt log_start_requirements_generationj_*.log | head -1

# Watch in real-time
tail -f log_start_requirements_generationj_*.log

# Check current project being processed
tail -f log_start_requirements_generationj_*.log | grep -E "Processing project|Starting CrewAI|Frontend Trace"

# Check for errors
tail -f log_start_requirements_generationj_*.log | grep -i error

# Count completed projects
ls -1 output/*_crewai_requirements.md | wc -l

# Check which projects are done
ls -1 output/*_crewai_requirements.md | sed 's|output/||' | sed 's|_crewai_requirements.md||' | sort
```

### Step 8: Verify Results

```bash
# Check output files
ls -lh output/*_crewai_requirements.md

# Check for placeholders (should be zero)
grep -l -i "placeholder\|unable to retrieve" output/*_crewai_requirements.md || echo "✓ No placeholders!"

# Check file sizes (larger = more detailed)
ls -lhS output/*_crewai_requirements.md | head -10

# Verify HTML artifacts are included in requirements
grep -i "html\|htm" output/*_crewai_requirements.md | head -20

# Verify GWT features are documented
grep -i "gwt\|nocache" output/*_crewai_requirements.md | head -20
```

## Complete Workflow Script

For convenience, here's a complete workflow that does everything:

```bash
#!/bin/bash
# Full Production Test Workflow

set -e

echo "=========================================="
echo "Full Production Test"
echo "=========================================="
echo ""

# Step 1: Activate virtual environment
echo "Step 1: Activating virtual environment..."
source venv/bin/activate

# Step 2: Verify Weaviate
echo ""
echo "Step 2: Verifying Weaviate..."
if ! curl -s -f http://localhost:8080/v1/meta > /dev/null 2>&1; then
    echo "Starting Weaviate..."
    docker-compose up -d
    sleep 5
fi

# Step 3: Extract artifacts (including HTML)
echo ""
echo "Step 3: Extracting artifacts (including HTML/HTM)..."
python main.py extract --include-frontend

# Step 4: Index artifacts
echo ""
echo "Step 4: Indexing artifacts in Weaviate..."
python main.py index --all-projects

# Step 5: Verify indexing
echo ""
echo "Step 5: Verifying indexing..."
python weaviate_stats.py | head -20

# Step 6: Generate requirements
echo ""
echo "Step 6: Generating requirements..."
echo "This will take 8-15 hours for all projects..."
./start_requirements_generation.sh 1

echo ""
echo "=========================================="
echo "Full Production Test Started!"
echo "=========================================="
echo ""
echo "Monitor progress:"
echo "  tail -f log_start_requirements_generationj_*.log"
echo ""
echo "Check completed projects:"
echo "  ls -1 output/*_crewai_requirements.md | wc -l"
```

Save this as `run_full_production_test.sh` and make it executable:
```bash
chmod +x run_full_production_test.sh
./run_full_production_test.sh
```

## Quick Test (Single Project)

For a quick test on a single project:

```bash
# 1. Extract (if not already done)
python main.py extract --include-frontend

# 2. Index (if not already done)
python main.py index --all-projects

# 3. Generate requirements for one project
./start_requirements_generation.sh 2 cuco-ui-admin

# 4. Check results
ls -lh output/cuco-ui-admin_crewai_requirements.md
grep -i "html\|gwt" output/cuco-ui-admin_crewai_requirements.md | head -20
```

## Reload Everything (Fresh Start)

If you need to start completely fresh:

```bash
# This script does everything:
# 1. Clears Weaviate
# 2. Fixes project names
# 3. Re-indexes all data
# 4. Verifies indexing
./reload_all_data.sh

# Then generate requirements
./start_requirements_generation.sh 1
```

## Troubleshooting

### HTML artifacts not found
```bash
# Check if HTML files were discovered
python main.py discover --include-frontend | grep -i html

# Check if HTML artifacts were extracted
ls -lh data/build/html_artifacts/all_html_artifacts.json

# Check if HTML artifacts were indexed
python main.py search --query "html" --frontend --limit 5
```

### Frontend trace agent not finding files
```bash
# Verify Weaviate has HTML artifacts
python -c "
from src.store.weaviate_client import WeaviateClient
wc = WeaviateClient(ensure_schema=False)
results = wc.search_artifacts('HtmlArtifact', 'html', limit=10)
print(f'Found {len(results)} HTML artifacts')
"

# Check search is working
python main.py search --query "gwt nocache" --frontend --limit 10
```

### Requirements generation stuck
```bash
# Check process status
ps aux | grep "main.py requirements" | grep -v grep

# Check log for errors
tail -100 log_start_requirements_generationj_*.log | grep -i error

# Kill and restart if needed
pkill -f "main.py requirements"
./start_requirements_generation.sh 1
```

## Expected Results

After completing the full test, you should have:

1. **Extracted artifacts** in `data/build/`:
   - `html_artifacts/all_html_artifacts.json` (NEW)
   - All other artifact types

2. **Indexed data** in Weaviate:
   - `HtmlArtifact` class with HTML files
   - All other artifact classes

3. **Requirements documents** in `output/`:
   - `{project}_crewai_requirements.md` for each project
   - Each includes complete frontend trace
   - HTML/GWT features documented
   - Zero placeholders

## Next Steps

After the full test:
1. Review requirements files for quality
2. Check that HTML/GWT features are properly documented
3. Verify frontend trace agent found all files
4. Compare with previous runs to ensure improvements

