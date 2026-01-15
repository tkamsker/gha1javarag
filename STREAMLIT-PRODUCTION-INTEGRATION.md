# Streamlit Web UI + Production Pipeline Integration Guide

**Last Updated**: 2026-01-15
**Feature**: 009-streamlit-crewai-web-client
**Purpose**: Connect Streamlit web UI to production pipeline data

---

## Overview

This guide explains how the Streamlit web UI integrates with the production pipeline data created by `production-requirements-generation.sh` (Steps 1-4).

## Production Pipeline Flow

```
production-requirements-generation.sh
│
├─ Step 1: discover  → Creates discovery-inventory.jsonl
├─ Step 2: extract   → Creates extraction-results.jsonl
├─ Step 3: index     → Indexes to Weaviate vector database
└─ Step 4: prd       → Generates PRD documents
```

## How Streamlit Connects to Production Data

### 1. **Weaviate Vector Database** (Primary Data Source)

**What Gets Indexed:**
- All artifacts from Step 3 (index) are stored in Weaviate
- Artifacts include: GwtPresenter, GwtView, BackendDoc, DaoCall, DtoArtifact, etc.
- Each artifact has vector embeddings for semantic search

**How Streamlit Accesses It:**
```python
# src/codeindex/web/services/search_service.py
from codeindex.services.weaviate_store import WeaviateStore

client = WeaviateStore()  # Uses same Weaviate instance as pipeline
results = client.semantic_search(query="user authentication")
```

**Configuration:**
- Both use same `WEAVIATE_URL` from `.env` (default: http://localhost:8080)
- No additional setup needed - if pipeline indexed data, Streamlit can search it

### 2. **Project Filtering**

**Pipeline Creates Project Metadata:**
```bash
# When you run:
./production-requirements-generation.sh cuco-ui-admin /path/to/source

# Pipeline creates artifacts with project field:
{
  "project": "cuco-ui-admin",
  "artifact_type": "GwtPresenter",
  "name": "UserPresenter",
  ...
}
```

**Streamlit Filters by Project:**
```python
# Search page automatically filters by project
results = search_service.search(
    query="login flow",
    filters={"project": "cuco-ui-admin"}
)
```

### 3. **Artifact Types** (from Pipeline)

The pipeline indexes these artifact types (accessible in Streamlit):

| Artifact Type | Created By | Searchable in Streamlit |
|---------------|------------|-------------------------|
| `GwtPresenter` | GWT Presenter extraction | ✅ Yes |
| `GwtView` | GWT View extraction | ✅ Yes |
| `BackendDoc` | Backend service extraction | ✅ Yes |
| `DaoCall` | DAO extraction | ✅ Yes |
| `DtoArtifact` | DTO extraction | ✅ Yes |
| `IbatisStatement` | iBATIS XML parsing | ✅ Yes |
| `DbTable` | Database schema extraction | ✅ Yes |
| `JspForm` | JSP form extraction | ✅ Yes |
| `GwtModule` | GWT module parsing | ✅ Yes |
| `GwtUiBinder` | UiBinder template parsing | ✅ Yes |
| `JsArtifact` | JavaScript extraction | ✅ Yes |

### 4. **File Browser Integration**

**Pipeline Discovers Files:**
```bash
# Step 1 (discover) finds all source files
# Stored in: output/<project>/discovery-inventory.jsonl
```

**Streamlit File Browser:**
```python
# src/codeindex/web/pages/4_🗂️_Files.py
# Reads from JAVA_SOURCE_DIR (same source as pipeline)
source_dir = config.java_source_dir  # From .env
files = discover_files(source_dir)
```

**Configuration:**
- Both use same `JAVA_SOURCE_DIR` from `.env`
- File browser shows same files that were indexed

---

## Step-by-Step Integration Workflow

### Step 1: Run Production Pipeline

```bash
# This creates all the data Streamlit needs
./production-requirements-generation.sh cuco-ui-admin /path/to/source

# Output:
# - output/cuco-ui-admin/discovery-inventory.jsonl
# - output/cuco-ui-admin/extraction-results.jsonl
# - Weaviate indexed artifacts (in vector database)
# - output/cuco-ui-admin/prd/services_prd.md
# - output/cuco-ui-admin/prd/frontend_prd.md
```

### Step 2: Verify Data is Indexed

```bash
# Check Weaviate has data
curl -s http://localhost:8080/v1/schema | jq '.classes[].class'

# Expected output:
# "Artifact"
# "Project"
# ... etc

# Check artifact count
python3 << 'EOF'
from codeindex.services.weaviate_store import WeaviateStore
store = WeaviateStore()
count = store.get_total_artifact_count()
print(f"Total artifacts in Weaviate: {count}")
EOF
```

### Step 3: Launch Streamlit

```bash
# Streamlit automatically connects to same Weaviate instance
streamlit run src/codeindex/web/app.py

# Browse to: http://localhost:8501
```

### Step 4: Use Streamlit to Explore Data

**Search Page** (🔍 Search):
- Enter natural language query: "user login authentication"
- Filter by project: "cuco-ui-admin"
- Filter by artifact type: GwtPresenter, BackendDoc
- Results come from Weaviate (same data as pipeline)

**Chat Page** (💬 Chat):
- Ask questions: "Explain the user authentication flow"
- AI agents use Weaviate search to find relevant artifacts
- Agents cite specific files and line numbers

**Files Page** (🗂️ Files):
- Browse source files from `JAVA_SOURCE_DIR`
- Same files that were discovered and indexed by pipeline

**Tests Page** (🧪 Tests):
- Generate tests based on artifacts in Weaviate
- Uses same semantic understanding as PRD generation

---

## Configuration Mapping

All settings are in `.env` file (shared by pipeline and Streamlit):

| Setting | Pipeline Uses | Streamlit Uses | Purpose |
|---------|---------------|----------------|---------|
| `JAVA_SOURCE_DIR` | ✅ Yes | ✅ Yes | Source code location |
| `WEAVIATE_URL` | ✅ Yes | ✅ Yes | Vector database connection |
| `OLLAMA_BASE_URL` | ✅ Yes | ✅ Yes | LLM for semantic analysis |
| `OLLAMA_MODEL_NAME` | ✅ Yes | ✅ Yes | Model to use (gemma3:12b) |
| `WORKSPACE_DB_PATH` | ❌ No | ✅ Yes | Workspace persistence (SQLite) |
| `STREAMLIT_PORT` | ❌ No | ✅ Yes | Web UI port (8501) |

**Key Point**: Pipeline and Streamlit share the same Weaviate instance and source directory.

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  Production Pipeline (production-requirements-generation.sh) │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ├─> Step 1: discover → discovery-inventory.jsonl
                 ├─> Step 2: extract  → extraction-results.jsonl
                 ├─> Step 3: index    → Weaviate Vector DB
                 └─> Step 4: prd      → services_prd.md, frontend_prd.md
                                             │
                                             │ (all data now in Weaviate)
                                             ↓
┌─────────────────────────────────────────────────────────────┐
│  Streamlit Web UI (src/codeindex/web/app.py)                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  🔍 Search Page                                              │
│  ├─ Connects to same Weaviate instance                      │
│  ├─ Filters by project name (from pipeline)                 │
│  └─ Returns artifacts indexed by pipeline                   │
│                                                              │
│  💬 Chat Page                                                │
│  ├─ AI agents query Weaviate for context                    │
│  ├─ Uses same artifacts as pipeline                         │
│  └─ Generates answers from indexed data                     │
│                                                              │
│  🗂️ Files Page                                               │
│  ├─ Reads from JAVA_SOURCE_DIR (same as pipeline)           │
│  └─ Shows files discovered by pipeline Step 1               │
│                                                              │
│  🧪 Tests Page                                               │
│  ├─ Uses artifacts from Weaviate                            │
│  └─ Generates tests based on extracted patterns             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Verification Checklist

Use this checklist to verify integration is working:

### ✅ Pipeline Data Created

- [ ] `output/<project>/discovery-inventory.jsonl` exists
- [ ] `output/<project>/extraction-results.jsonl` exists
- [ ] `output/<project>/prd/services_prd.md` exists
- [ ] `output/<project>/prd/frontend_prd.md` exists

### ✅ Weaviate Has Data

```bash
# Check schema exists
curl -s http://localhost:8080/v1/schema | jq '.classes[].class'

# Check artifact count > 0
python3 -c "from codeindex.services.weaviate_store import WeaviateStore; print(WeaviateStore().get_total_artifact_count())"
```

### ✅ Streamlit Can Access Data

- [ ] Launch Streamlit: `streamlit run src/codeindex/web/app.py`
- [ ] Search page loads without errors
- [ ] Search for "test query" returns results (if data indexed)
- [ ] Project filter shows your project name
- [ ] File browser shows files from `JAVA_SOURCE_DIR`

### ✅ Services Healthy

```bash
# Run health check
./check-services.sh

# Expected:
# ✅ Ollama: Connected
# ✅ Weaviate: Connected
# ✅ SQLite: Database exists
# ✅ All services healthy
```

---

## Current Implementation Status

### ✅ **Working** (Production Ready)

1. **Service Connectivity**
   - Weaviate connection (uses same instance as pipeline)
   - Ollama connection (uses same LLM as pipeline)
   - SQLite workspace storage

2. **Configuration**
   - All settings from `.env` work for both pipeline and Streamlit
   - Project filtering infrastructure
   - Artifact type filtering infrastructure

3. **Pages**
   - 🏠 Home page (welcome, navigation)
   - 🗂️ Files page (file browser from JAVA_SOURCE_DIR)
   - ⚙️ Settings page (agent configuration, diagnostics)
   - 📊 Workspace page (session persistence)

### 🚧 **Implemented but Using Placeholders**

4. **Search Service** (infrastructure complete, needs real queries)
   - File: `src/codeindex/web/services/search_service.py`
   - Status: Uses placeholder responses (TODO: connect to real Weaviate)
   - Fix: Replace placeholder with actual `WeaviateStore.semantic_search()` calls

5. **Agent Service** (routing complete, needs real LLM integration)
   - File: `src/codeindex/web/services/agent_service.py`
   - Status: All 8 agents implemented with placeholder responses
   - Fix: Connect agents to Ollama for real answers

### 📝 **To Complete Full Integration**

**Priority 1: Connect Search to Real Data**

```python
# src/codeindex/web/services/search_service.py
# Replace placeholder with:
client = self._get_weaviate_client()
results = client.semantic_search(
    query=query,
    limit=limit,
    offset=offset,
    filters=filters
)
```

**Priority 2: Connect Agents to Real LLM**

```python
# src/codeindex/web/agents/senior_developer.py
# Replace placeholder with:
from codeindex.services.ollama_client import OllamaClient
ollama = OllamaClient()
response = ollama.generate_response(query, context=artifacts)
```

**Priority 3: Test End-to-End Flow**

1. Run pipeline: `./production-requirements-generation.sh`
2. Verify Weaviate has data
3. Launch Streamlit
4. Search for artifacts (should return real results)
5. Ask AI agents questions (should use real LLM)

---

## Troubleshooting

### Issue: "No search results found"

**Cause**: Weaviate is empty or project name mismatch

**Fix**:
```bash
# Check Weaviate has data
python3 -c "from codeindex.services.weaviate_store import WeaviateStore; print(WeaviateStore().get_total_artifact_count())"

# If count is 0, run pipeline first:
./production-requirements-generation.sh <project-name> <source-path>

# Check project name in Weaviate matches filter
curl -s http://localhost:8080/v1/objects | jq '.objects[].properties.project' | sort -u
```

### Issue: "Agent responses are generic/placeholder"

**Cause**: Agents are using placeholder responses (not yet connected to Ollama)

**Fix**: This is expected in current implementation. Agents need to be connected to real Ollama LLM (see Priority 2 above).

### Issue: "File browser shows no files"

**Cause**: `JAVA_SOURCE_DIR` not set or incorrect in `.env`

**Fix**:
```bash
# Check environment variable
echo $JAVA_SOURCE_DIR

# Verify directory exists
ls -la $JAVA_SOURCE_DIR

# Update .env if needed
vim .env
# Set: JAVA_SOURCE_DIR=/correct/path/to/source
```

### Issue: "Cannot connect to Weaviate"

**Cause**: Weaviate not running or wrong URL

**Fix**:
```bash
# Check Weaviate is running
./docker-weaviate.sh status

# Start if needed
./docker-weaviate.sh start

# Verify URL in .env
grep WEAVIATE_URL .env
# Should be: WEAVIATE_URL=http://localhost:8080
```

---

## Summary

**Key Points:**

1. ✅ **Same Data Source**: Streamlit and pipeline use the same Weaviate instance
2. ✅ **Same Configuration**: Both read from `.env` file
3. ✅ **Same Artifacts**: Search returns what pipeline indexed
4. 🚧 **Needs Connection**: Search service has placeholder (connect to real Weaviate)
5. 🚧 **Needs Integration**: Agents have placeholders (connect to real Ollama)

**What Works Now:**
- Service health checks
- Database initialization
- UI navigation and pages
- Configuration management
- Agent routing infrastructure

**What Needs Real Data:**
- Search results (currently placeholder)
- Agent responses (currently placeholder)
- Relationship graphs (needs Weaviate queries)

**Next Steps:**
1. ✅ Fix TypeError (DONE - parameter mapping)
2. 📝 Connect search to real Weaviate queries
3. 📝 Connect agents to real Ollama LLM
4. 📝 Test with production pipeline data

---

**For More Information:**
- Pipeline: See `HOWTO-PRODUCTION-TESTING.md`
- Web UI: See `FEATURE-009-PROGRESS.md`
- Config: See `.env.example`
