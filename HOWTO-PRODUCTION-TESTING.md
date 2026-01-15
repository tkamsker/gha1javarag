# How-To: Production Testing - Streamlit Web Client

**Last Updated**: 2026-01-14
**Feature**: 009-streamlit-crewai-web-client
**Status**: Ready for internal testing

## Overview

This guide walks you through testing the Streamlit Web Client in a production-like environment using your existing `.env` configuration.

## Prerequisites

### Required Services
- ✅ Python 3.8+ with virtual environment
- ✅ Ollama (port 11434) - for LLM inference
- ✅ Weaviate (port 8080) - for vector search
- ✅ SQLite 3.35+ - for workspace storage
- ✅ Indexed codebase - artifacts already in Weaviate

### Required Packages
See Step 0 below for installation instructions.

## Step 0: Virtual Environment Setup

**Critical**: Always use a virtual environment to isolate project dependencies and avoid conflicts with system Python packages.

### 0.1 Create Virtual Environment

```bash
# Navigate to project root
cd /path/to/gha1javarag

# Create virtual environment (one-time setup)
python3 -m venv .venv

# This creates a .venv/ directory containing:
# - Python interpreter
# - pip package manager
# - Isolated package installation directory
```

### 0.2 Activate Virtual Environment

**Linux/macOS**:
```bash
source .venv/bin/activate

# Your prompt should change to show (.venv)
# Example: (.venv) user@host:~/gha1javarag$
```

**Windows (Command Prompt)**:
```cmd
.venv\Scripts\activate.bat
```

**Windows (PowerShell)**:
```powershell
.venv\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 0.3 Verify Virtual Environment is Active

```bash
# Check Python location (should point to .venv/)
which python3  # Linux/macOS
where python   # Windows

# Expected output (Linux/macOS):
# /path/to/gha1javarag/.venv/bin/python3

# Expected output (Windows):
# C:\path\to\gha1javarag\.venv\Scripts\python.exe

# Check pip location
which pip3     # Linux/macOS
where pip      # Windows

# Verify Python version
python3 --version  # Should be 3.8 or higher
```

### 0.4 Install Required Packages

**Important**: Only install packages after activating the virtual environment.

```bash
# Ensure .venv is activated (prompt shows (.venv))
# If not activated, run: source .venv/bin/activate

# Install all dependencies
pip install -r requirements.txt

# Key packages for web UI:
# - streamlit>=1.30.0
# - crewai>=0.20.0
# - streamlit-cytoscape>=1.0.0
# - reportlab>=4.0.0
# - aiosqlite>=0.19.0

# Verify installation
pip list | grep streamlit
# Expected: streamlit 1.30.0 (or higher)
```

### 0.5 Deactivating Virtual Environment (When Done)

```bash
# To deactivate when finished testing
deactivate

# Prompt should return to normal (no (.venv) prefix)
```

**Important Notes**:
- ✅ Always activate `.venv` before running any Python commands
- ✅ Each terminal session requires activation
- ✅ The `.venv/` directory is gitignored and project-specific
- ✅ To reactivate later: `source .venv/bin/activate`

## Step 1: Environment Configuration

### 1.1 Copy and Configure .env

```bash
# Copy example to active configuration
cp .env.example .env

# Edit .env with your settings
vim .env  # or nano, code, etc.
```

### 1.2 Verify Core Settings

Open `.env` and verify these critical settings:

```bash
# ==============================================================================
# JAVA SOURCE DIRECTORY (Required)
# ==============================================================================
JAVA_SOURCE_DIR=/path/to/your/java/source/root

# ==============================================================================
# Weaviate Configuration (Required)
# ==============================================================================
WEAVIATE_URL=http://localhost:8080
WEAVIATE_GRPC_PORT=50051

# ==============================================================================
# Ollama Configuration (Required)
# ==============================================================================
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL_NAME=gemma3:12b
OLLAMA_CONNECT_TIMEOUT=10
OLLAMA_READ_TIMEOUT=300

# ==============================================================================
# Feature 009: Web UI Configuration
# ==============================================================================
STREAMLIT_PORT=8501
STREAMLIT_HOST=localhost

# SQLite database paths for workspaces and annotations
WORKSPACE_DB_PATH=data/workspaces.db
ANNOTATIONS_DB_PATH=data/annotations.db

# Export directory for generated reports (auto-cleanup after 24h)
EXPORT_DIR=data/exports

# Maximum concurrent agents for multi-agent workflows (default: 3)
MAX_CONCURRENT_AGENTS=3

# Optional: Authentication (disabled by default for internal use)
AUTH_ENABLED=false
```

### 1.3 Create Required Directories

```bash
# Create data directories
mkdir -p data/exports
mkdir -p data/workspaces

# Verify permissions
ls -la data/
```

## Step 2: Start Required Services

### 2.1 Start Ollama

```bash
# Start Ollama service
ollama serve

# Verify Ollama is running (in another terminal)
curl -s http://localhost:11434/api/tags

# Expected output: JSON list of models
```

### 2.2 Start Weaviate

```bash
# Start Weaviate using existing script
./docker-weaviate.sh start

# Verify Weaviate is running
./docker-weaviate.sh status

# Check Weaviate health
curl -s http://localhost:8080/v1/meta | jq .
```

### 2.3 Verify Service Health

**Option 1: Use Standalone Script (Recommended)**

```bash
# Run service health check script (works on macOS and Linux)
./check-services.sh

# For detailed output:
./check-services.sh --verbose

# Expected output (before Step 3 - Database Init):
# ✅ Ollama: Connected (http://localhost:11434)
# ✅ Weaviate: Connected (http://localhost:8080)
# ⚠️  SQLite: Database not found (data/workspaces.db)
#    This is normal if you haven't initialized the database yet (Step 3)
#    Run: ./init-database.sh
# ✅ All services healthy - ready to proceed!

# Note: SQLite warning is expected before Step 3. Services are still
# considered healthy - you can proceed with the guide.
```

**Option 2: Manual Check with Python**

```bash
# Ensure virtual environment is activated
source .venv/bin/activate  # Skip if already activated

# Test connectivity to all services
python3 << 'EOF'
import httpx
import sys

services = {
    "Ollama": "http://localhost:11434/api/tags",
    "Weaviate": "http://localhost:8080/v1/meta"
}

print("🔍 Checking service health...")
all_healthy = True

for name, url in services.items():
    try:
        response = httpx.get(url, timeout=5.0)
        if response.status_code == 200:
            print(f"✅ {name}: OK")
        else:
            print(f"❌ {name}: HTTP {response.status_code}")
            all_healthy = False
    except Exception as e:
        print(f"❌ {name}: {e}")
        all_healthy = False

if all_healthy:
    print("\n✅ All services healthy - ready to launch web UI!")
    sys.exit(0)
else:
    print("\n❌ Some services are unhealthy - fix before proceeding")
    sys.exit(1)
EOF
```

## Step 3: Initialize Database

### 3.1 Run Database Initialization

**Option 1: Use Standalone Script (Recommended)**

```bash
# Initialize SQLite databases (works on macOS and Linux)
./init-database.sh

# Expected output:
# ✅ Virtual environment activated
# ✅ Data directories created
# ✅ Database initialized successfully
#    Location: data/workspaces.db
# ✅ Tables created: 3
#    - workspaces
#    - workspace_artifacts
#    - annotations
# ✅ WAL mode enabled: wal
# ✅ Database initialization complete!
```

**Option 2: Manual Initialization with Python**

```bash
# Ensure virtual environment is activated
source .venv/bin/activate  # Skip if already activated

# Initialize SQLite databases
python3 << 'EOF'
import sys
from pathlib import Path

# Add src to path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

from codeindex.web.database.connection import get_workspace_manager

print("🔧 Initializing workspace database...")

try:
    # Get manager - initialization happens automatically in constructor
    # if database doesn't exist or is empty
    manager = get_workspace_manager()

    print("✅ Database initialized successfully")
    print(f"   Location: {manager.db_path}")

    # Verify schema
    with manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        print(f"\n📊 Tables created: {len(tables)}")
        for table in tables:
            print(f"   - {table[0]}")

except Exception as e:
    print(f"❌ Database initialization failed: {e}")
    sys.exit(1)
EOF
```

### 3.2 Verify Database

**Option 1: Quick Check with Service Health Script**

```bash
# Run service health check - should now show SQLite OK
./check-services.sh

# Expected output:
# ✅ Ollama: Connected (http://localhost:11434)
# ✅ Weaviate: Connected (http://localhost:8080)
# ✅ SQLite: Database exists (data/workspaces.db)
# ✅ SQLite: Valid database format
# ✅ All services healthy - ready to proceed!
```

**Option 2: Manual Verification**

```bash
# Check database file exists and is accessible
ls -lh data/workspaces.db

# Verify WAL mode (Write-Ahead Logging)
sqlite3 data/workspaces.db "PRAGMA journal_mode;"
# Expected output: wal

# Check tables
sqlite3 data/workspaces.db ".tables"
# Expected: workspaces, workspace_artifacts, annotations
```

## Step 4: Launch Web Application

### 4.1 Start Streamlit Server

```bash
# Ensure virtual environment is activated
source .venv/bin/activate  # Skip if already activated

# Launch Streamlit app
streamlit run src/codeindex/web/app.py \
  --server.port ${STREAMLIT_PORT:-8501} \
  --server.address ${STREAMLIT_HOST:-localhost} \
  --server.headless true

# Expected output:
# You can now view your Streamlit app in your browser.
# Local URL: http://localhost:8501
```

### 4.2 Access Web Interface

Open your browser and navigate to:
```
http://localhost:8501
```

You should see the welcome page with navigation to 6 pages:
- 🔍 Search
- 💬 Chat
- 📊 Workspace
- 🗂️ Files
- 🧪 Tests
- ⚙️ Settings

## Step 5: Test Each Feature

### 5.1 Test Search Page

**Goal**: Verify semantic search and filtering work

1. **Navigate to Search** (🔍 Search in sidebar)

2. **Basic Search**:
   ```
   Query: "user authentication login"
   Expected: Results ranked by semantic similarity
   ```

3. **Apply Filters**:
   - Select artifact types: GwtPresenter, BackendDoc
   - Select project: (choose from dropdown)
   - Click "Search"
   - Expected: Filtered results

4. **Test Pagination**:
   - Scroll to bottom
   - Click "Next Page"
   - Expected: Page 2 results

5. **Test URL Persistence**:
   - Copy URL from browser
   - Open in new tab
   - Expected: Same search/filters restored

**Success Criteria**:
- ✅ Search returns results in <5 seconds
- ✅ Filters reduce result count appropriately
- ✅ Pagination works correctly
- ✅ URL sharing restores state

### 5.2 Test Relationship Graph

**Goal**: Verify interactive graph visualization

1. **From Search Results**:
   - Find an artifact (e.g., GwtPresenter)
   - Click "🔗 Relationships" button

2. **Verify Graph Display**:
   - Graph should render with colored nodes
   - Should show relationships as edges
   - Should include max 50 nodes

3. **Test Graph Controls**:
   - Try zooming (mouse wheel)
   - Try panning (click and drag)
   - Click a node (should highlight)

4. **Test Export**:
   - Click "📝 Export Mermaid"
   - Download should contain valid Mermaid syntax
   - Open in Mermaid Live Editor to verify

**Success Criteria**:
- ✅ Graph renders in <3 seconds
- ✅ Interactive controls work
- ✅ Mermaid export is valid
- ✅ No errors in browser console

### 5.3 Test Chat with AI Agents

**Goal**: Verify all 8 agents respond correctly

1. **Navigate to Chat** (💬 Chat in sidebar)

2. **Test Agent Routing**:
   ```
   Queries to test each agent:

   1. Senior Developer:
      "Explain the architecture of the application"

   2. Data Analyst:
      "Show me the database schema for users table"

   3. Frontend Specialist:
      "Describe the UI components for login screen"

   4. Backend Specialist:
      "What services handle user authentication?"

   5. PRD Writer:
      "Generate requirements for user management"

   6. Spec-Kit Writer:
      "Create technical spec for login feature"

   7. Gherkin Test Writer:
      "Generate BDD tests for user login"

   8. Playwright Test Writer:
      "Generate E2E tests for login flow"
   ```

3. **Verify Response Quality**:
   - Responses should be relevant to query
   - Should include citations (if artifacts found)
   - Should show confidence score
   - Should suggest follow-up questions

4. **Test Agent Selector**:
   - Manually select "Data Analyst" from dropdown
   - Ask: "Analyze database relationships"
   - Expected: Data Analyst should respond

**Success Criteria**:
- ✅ All 8 agents respond to appropriate queries
- ✅ Responses include citations
- ✅ Chat history persists during session
- ✅ Manual agent selection works

### 5.4 Test Workspace Management

**Goal**: Verify save/load of analysis sessions

1. **Create Workspace**:
   - Navigate to Workspace (📊 Workspace)
   - Fill form:
     - Name: "Test Analysis Session"
     - Description: "Testing workspace features"
     - Tags: "test, production, validation"
   - Click "Create Workspace"
   - Expected: Success message

2. **Load Workspace**:
   - Click "📂 Load" on created workspace
   - Expected: Workspace loads with saved state

3. **Test State Preservation**:
   - Go to Search page
   - Perform a search
   - Return to Workspace
   - Click "💾 Save Changes"
   - Close browser
   - Reopen and load workspace
   - Expected: Search state restored

4. **Delete Workspace**:
   - Click "🗑️ Delete" on test workspace
   - Expected: Workspace removed

**Success Criteria**:
- ✅ Workspaces create successfully
- ✅ State saves and restores correctly
- ✅ Workspace metadata displays
- ✅ Delete removes workspace

### 5.5 Test File Browser

**Goal**: Verify code viewing works

1. **Navigate to Files** (🗂️ Files)

2. **Browse File Tree**:
   - Sidebar shows files from JAVA_SOURCE_DIR
   - Search for filename: "User"
   - Click a Java file
   - Expected: Code displays with syntax highlighting

3. **Test Search Within File**:
   - Click "🔍 Search in File"
   - Enter: "class"
   - Expected: Matching lines highlighted

4. **Test Jump to Line**:
   - Enter line number: 50
   - Expected: View centers on line 50

**Success Criteria**:
- ✅ File tree loads in <5 seconds
- ✅ Code displays with syntax highlighting
- ✅ Search within file works
- ✅ Jump to line works

### 5.6 Test Test Generation

**Goal**: Verify Gherkin and Playwright test generation

1. **Navigate to Tests** (🧪 Tests)

2. **Generate Gherkin Tests**:
   - Select "📝 Gherkin (BDD)"
   - Enter description:
     ```
     Feature: User Login
     Test login with valid and invalid credentials
     ```
   - Click "🎯 Generate Tests"
   - Expected: Gherkin scenario with Given-When-Then

3. **Generate Playwright Tests**:
   - Select "🎭 Playwright (E2E)"
   - Enter description:
     ```
     Test the login flow:
     1. Navigate to login page
     2. Enter credentials
     3. Click login
     4. Verify dashboard
     ```
   - Click "🎯 Generate Tests"
   - Expected: Playwright test script

4. **Test Download**:
   - Click "💾 Download" on generated test
   - Verify file downloads correctly

**Success Criteria**:
- ✅ Gherkin tests generate in <30 seconds
- ✅ Playwright tests generate in <30 seconds
- ✅ Test syntax is valid
- ✅ Download works

### 5.7 Test Settings

**Goal**: Verify configuration changes work

1. **Navigate to Settings** (⚙️ Settings)

2. **Test Agent Settings**:
   - Change "Response Detail Level" to "detailed"
   - Change "Technical Level" to "junior"
   - Change "LLM Temperature" to 0.5
   - Click "💾 Save Settings"
   - Expected: Settings saved message

3. **Test Service Diagnostics**:
   - Click "Test Connection" for Weaviate
   - Expected: "✅ Connected" message
   - Click "Test Connection" for Ollama
   - Expected: "✅ Connected" message

4. **Verify Settings Apply**:
   - Go to Chat page
   - Ask a question
   - Expected: Response reflects settings (more detailed, simpler language)

**Success Criteria**:
- ✅ Settings save successfully
- ✅ Service diagnostics work
- ✅ Settings affect agent behavior
- ✅ Reset to defaults works

## Step 6: Test Multi-Agent Workflows

### 6.1 Test PRD Generation Workflow

**Goal**: Verify multi-agent collaboration

1. **From Chat Page**:
   - Enter query:
     ```
     Generate a PRD for the user authentication module
     ```
   - Select agent: "PRD Writer"
   - Click send

2. **Monitor Progress**:
   - Should show workflow progress indicator
   - Should display current agent
   - Should show estimated time remaining

3. **Verify Output**:
   - Generated PRD should include:
     - Overview section
     - User stories
     - Functional requirements
     - Non-functional requirements
   - Should include citations from multiple agents

**Success Criteria**:
- ✅ Workflow executes without errors
- ✅ Progress indicator updates
- ✅ PRD contains all sections
- ✅ Multiple agents contributed

## Step 7: Performance Testing

### 7.1 Search Performance

```bash
# Test search response time
time curl -s "http://localhost:8501" > /dev/null

# Expected: <2 seconds for page load
```

### 7.2 Database Performance

```bash
# Test workspace query performance
sqlite3 data/workspaces.db << 'EOF'
.timer on
SELECT COUNT(*) FROM workspaces;
SELECT * FROM workspaces ORDER BY updated_at DESC LIMIT 10;
EOF

# Expected: <100ms for both queries
```

### 7.3 Graph Generation Performance

1. **Navigate to Search**
2. **Find artifact with many relationships**
3. **Click "🔗 Relationships"**
4. **Measure time to graph display**

**Success Criteria**:
- ✅ Graph renders in <3 seconds
- ✅ Max 50 nodes enforced
- ✅ No browser lag

## Step 8: Error Handling Testing

### 8.1 Test Service Failures

1. **Stop Weaviate**:
   ```bash
   ./docker-weaviate.sh stop
   ```

2. **Try to Search**:
   - Expected: Graceful error message
   - Should not crash application

3. **Restart Weaviate**:
   ```bash
   ./docker-weaviate.sh start
   ```

4. **Retry Search**:
   - Expected: Works again

### 8.2 Test Invalid Inputs

1. **Search with empty query**:
   - Expected: Prompt to enter query

2. **Create workspace with no name**:
   - Expected: Validation error

3. **Upload invalid file** (if file upload exists):
   - Expected: File type validation error

**Success Criteria**:
- ✅ Errors display user-friendly messages
- ✅ Application doesn't crash
- ✅ Can recover from errors

## Step 9: Service Health Monitoring

### 9.1 Quick Service Check

```bash
# Run anytime to verify services are healthy
./check-services.sh

# If services are unhealthy, see troubleshooting output
# Script will provide specific commands to fix each service
```

## Step 10: Cleanup and Shutdown

### 10.1 Export Test Data

```bash
# Export workspaces for backup
sqlite3 data/workspaces.db .dump > backup/workspaces_backup.sql

# Export test results
cp data/exports/* backup/test-exports/
```

### 10.2 Shutdown Services

```bash
# Stop Streamlit (Ctrl+C in terminal)

# Stop Weaviate
./docker-weaviate.sh stop

# Stop Ollama (Ctrl+C in terminal or)
pkill ollama
```

### 10.3 Clean Test Data (Optional)

```bash
# Remove test workspaces
rm data/workspaces.db
rm data/annotations.db

# Clean export directory
rm -rf data/exports/*

# Keep: Weaviate data is preserved in weaviate-data/
```

## Troubleshooting

### Quick Diagnostics

```bash
# Run comprehensive service health check first
./check-services.sh --verbose

# This will identify which services are having issues
# and provide specific troubleshooting steps
```

### Issue: Virtual Environment Not Working

**Symptoms**: "ModuleNotFoundError" or packages not found

**Solution**:
```bash
# Check if venv is activated (prompt should show (.venv))
echo $VIRTUAL_ENV  # Linux/macOS - should show path to .venv
echo %VIRTUAL_ENV% # Windows - should show path to .venv

# If empty, activate venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Verify Python is from venv
which python3  # Should show: .../gha1javarag/.venv/bin/python3

# If packages still missing, reinstall
pip install -r requirements.txt

# If venv is corrupted, recreate it
deactivate
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Common Mistakes**:
- ❌ Running `pip install` without activating venv (installs to system Python)
- ❌ Using wrong Python interpreter (system Python instead of venv Python)
- ❌ Forgetting to activate venv in new terminal sessions
- ❌ Using `python` instead of `python3` on some systems

### Issue: Streamlit Won't Start

**Symptoms**: Port already in use

**Solution**:
```bash
# Check what's using port 8501
lsof -i :8501

# Kill existing Streamlit process
pkill -f streamlit

# Or use different port
export STREAMLIT_PORT=8502
streamlit run src/codeindex/web/app.py --server.port 8502
```

### Issue: "No Search Results"

**Symptoms**: Search returns empty results

**Solution**:
```bash
# Verify Weaviate has data
curl -s http://localhost:8080/v1/schema | jq '.classes[].class'

# Ensure virtual environment is activated
source .venv/bin/activate

# Check artifact count
python3 << 'EOF'
from codeindex.weaviate.weaviate_store import get_weaviate_store
store = get_weaviate_store()
count = store.get_total_artifact_count()
print(f"Total artifacts: {count}")
EOF

# If count is 0, need to run indexing first:
codeindex discover --source-dir $JAVA_SOURCE_DIR --output discovery.jsonl
codeindex extract --inventory discovery.jsonl --output extraction.jsonl
codeindex index --inventory discovery.jsonl --extraction extraction.jsonl
```

### Issue: Database Locked

**Symptoms**: "database is locked" error

**Solution**:
```bash
# Check for other processes using database
lsof | grep workspaces.db

# Verify WAL mode is enabled
sqlite3 data/workspaces.db "PRAGMA journal_mode;"

# Should return: wal

# If not WAL, enable it:
sqlite3 data/workspaces.db "PRAGMA journal_mode=WAL;"
```

### Issue: Ollama Not Responding

**Symptoms**: Agent responses timeout

**Solution**:
```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
pkill ollama
ollama serve

# Verify model is loaded
ollama list | grep gemma3

# Pull model if missing
ollama pull gemma3:12b
```

### Issue: Graph Not Rendering

**Symptoms**: Relationship graph shows blank

**Solution**:
```bash
# Install streamlit-cytoscape
pip install streamlit-cytoscape

# Clear Streamlit cache
rm -rf ~/.streamlit/cache

# Restart Streamlit
```

## Production Readiness Checklist

Use this checklist before deploying to production:

### ✅ Environment
- [ ] Python 3.8+ installed
- [ ] Virtual environment created (`.venv/`)
- [ ] Virtual environment activated (prompt shows `(.venv)`)
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Python points to venv (`which python3` shows `.venv/bin/python3`)

### ✅ Services
- [ ] Ollama running and responsive
- [ ] Weaviate running with data indexed
- [ ] SQLite databases initialized with WAL mode
- [ ] All services pass health checks

### ✅ Configuration
- [ ] .env file configured correctly
- [ ] JAVA_SOURCE_DIR points to correct location
- [ ] Database paths are writable
- [ ] Export directory has cleanup configured

### ✅ Features
- [ ] Search returns results in <5 seconds
- [ ] All 8 agents respond correctly
- [ ] Workspaces save and load
- [ ] File browser shows code
- [ ] Test generation works
- [ ] Settings persist

### ✅ Performance
- [ ] Page load <2 seconds
- [ ] Search response <5 seconds
- [ ] Graph rendering <3 seconds
- [ ] Database queries <100ms

### ✅ Error Handling
- [ ] Service failures show graceful errors
- [ ] Invalid inputs are validated
- [ ] Application doesn't crash on errors
- [ ] Can recover from failures

### ✅ Documentation
- [ ] README.md updated with web UI section
- [ ] CLAUDE.md includes launch instructions
- [ ] This HOWTO guide is available
- [ ] Known issues documented

## Next Steps After Testing

1. **Document Issues**: Record any bugs or issues found
2. **Performance Tuning**: Optimize slow queries or operations
3. **User Feedback**: Gather feedback from team testing
4. **Production Deploy**: Follow deployment guide when ready
5. **Monitoring**: Set up logging and metrics

## Support

For issues or questions:
- **Documentation**: See `FEATURE-009-PROGRESS.md`
- **Troubleshooting**: See CLAUDE.md troubleshooting section
- **Logs**: Check `~/.streamlit/logs/` for Streamlit logs

---

**Version**: 1.0
**Last Tested**: 2026-01-14
**Status**: ✅ Ready for production testing
