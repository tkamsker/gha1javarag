# Generate Requirements Documentation (PRD) - Production Guide

**After Pipeline Completion: Creating Product Requirements Documents**

This guide explains how to generate PRD (Product Requirements Document) files after the discovery/extraction/indexing pipeline completes.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Production Workflow](#production-workflow)
5. [PRD Generation Options](#prd-generation-options)
6. [Monitoring & Validation](#monitoring--validation)
7. [Output Structure](#output-structure)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

### What is PRD Generation?

After the analysis pipeline completes (discover → extract → index), the system has:
- ✅ All source files discovered and classified
- ✅ Semantic metadata extracted (services, DAOs, DTOs, GWT components)
- ✅ Foreign key relationships mapped
- ✅ GWT navigation graph built
- ✅ Everything indexed in Weaviate vector database

**PRD Generation** transforms this indexed data into human-readable Product Requirements Documents that describe:
- Backend architecture and components
- Frontend architecture (GWT Presenters, Views, UiBinder)
- Database schema and relationships
- API endpoints and services
- User workflows and navigation

---

## ✅ Prerequisites

### 1. Pipeline Must Be Complete

Verify the pipeline finished successfully:

```bash
# Check status
codeindex status

# You should see:
# - Total artifacts indexed: X
# - No errors in extraction
# - Foreign key extraction complete
# - GWT navigation graph built
```

### 2. Services Must Be Running

```bash
# Check Weaviate is running
curl http://localhost:8080/v1/meta

# Check Ollama is running (for PRD generation)
curl http://localhost:11434/api/tags
```

### 3. Environment Variables Set

```bash
source .venv/bin/activate
source .env
```

---

## 🚀 Quick Start

### Simple PRD Generation

```bash
# Activate environment
source .venv/bin/activate

# Generate backend PRD
codeindex prd backend --output-dir ./output/prd

# Generate frontend PRD (includes GWT components!)
codeindex prd frontend --output-dir ./output/prd

# View generated files
ls -lh ./output/prd/
```

**Output files**:
- `backend_prd.md` - Backend architecture, services, DAOs, database
- `frontend_prd.md` - Frontend architecture, GWT presenters/views, forms
- `backend/` - Individual component JSON files
- `frontend/` - Individual component JSON files

---

## 🏭 Production Workflow

### Matching Your Current Process

Based on your production command pattern, here's the complete workflow:

```bash
#!/bin/bash
# production-requirements-generation.sh
#
# Usage: ./production-requirements-generation.sh <project-name> <source-path>
# Example: ./production-requirements-generation.sh cuco-ui-admin /mnt/cucocalcai/cuco-master/cuco-ui-admin

PROJECT_NAME=$1
SOURCE_PATH=$2
TIMESTAMP=$(date +'%Y-%m-%d_%H-%M-%S')
LOG_DIR="./logs"
OUTPUT_DIR="./output/${PROJECT_NAME}"

# Create directories
mkdir -p "$LOG_DIR"
mkdir -p "$OUTPUT_DIR"

echo "==================================="
echo "PRD Generation for: $PROJECT_NAME"
echo "Source: $SOURCE_PATH"
echo "==================================="

# Step 1: Run analysis pipeline (equivalent to run-cuco.sh)
echo "Step 1: Running analysis pipeline..."
nohup ./run.sh \
    --source-dir "$SOURCE_PATH" \
    --project "$PROJECT_NAME" \
    --output "$OUTPUT_DIR" \
    > "${LOG_DIR}/log_${PROJECT_NAME}_pipeline_${TIMESTAMP}.log" 2>&1 &

PIPELINE_PID=$!
echo "Pipeline started (PID: $PIPELINE_PID)"
echo "Log: ${LOG_DIR}/log_${PROJECT_NAME}_pipeline_${TIMESTAMP}.log"

# Wait for pipeline to complete
wait $PIPELINE_PID

if [ $? -eq 0 ]; then
    echo "✓ Pipeline completed successfully"
else
    echo "✗ Pipeline failed. Check log file."
    exit 1
fi

# Step 2: Generate PRD documents (equivalent to step2.sh)
echo ""
echo "Step 2: Generating PRD documents..."
nohup codeindex prd backend \
    --project "$PROJECT_NAME" \
    --output-dir "$OUTPUT_DIR/prd" \
    > "${LOG_DIR}/log_${PROJECT_NAME}_backend_prd_${TIMESTAMP}.log" 2>&1 &

BACKEND_PID=$!

nohup codeindex prd frontend \
    --project "$PROJECT_NAME" \
    --output-dir "$OUTPUT_DIR/prd" \
    > "${LOG_DIR}/log_${PROJECT_NAME}_frontend_prd_${TIMESTAMP}.log" 2>&1 &

FRONTEND_PID=$!

echo "Backend PRD generation started (PID: $BACKEND_PID)"
echo "Frontend PRD generation started (PID: $FRONTEND_PID)"

# Wait for PRD generation to complete
wait $BACKEND_PID
BACKEND_STATUS=$?

wait $FRONTEND_PID
FRONTEND_STATUS=$?

# Check results
if [ $BACKEND_STATUS -eq 0 ] && [ $FRONTEND_STATUS -eq 0 ]; then
    echo ""
    echo "==================================="
    echo "✓ SUCCESS!"
    echo "==================================="
    echo "PRD documents generated:"
    echo "  - Backend PRD: $OUTPUT_DIR/prd/backend_prd.md"
    echo "  - Frontend PRD: $OUTPUT_DIR/prd/frontend_prd.md"
    echo ""
    echo "View results:"
    echo "  ls -lh $OUTPUT_DIR/prd/"
else
    echo ""
    echo "==================================="
    echo "✗ PRD Generation Failed"
    echo "==================================="
    echo "Check log files:"
    echo "  - Backend: ${LOG_DIR}/log_${PROJECT_NAME}_backend_prd_${TIMESTAMP}.log"
    echo "  - Frontend: ${LOG_DIR}/log_${PROJECT_NAME}_frontend_prd_${TIMESTAMP}.log"
    exit 1
fi
```

### Make Script Executable

```bash
chmod +x production-requirements-generation.sh
```

### Run in Production

```bash
# Example: cuco-ui-admin project
./production-requirements-generation.sh \
    cuco-ui-admin \
    /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-admin

# Monitor progress
tail -f logs/log_cuco-ui-admin_pipeline_*.log
tail -f logs/log_cuco-ui-admin_backend_prd_*.log
```

---

## 📦 PRD Generation Options

### Backend PRD

Generates documentation for:
- ✅ Services and business logic
- ✅ DAOs (Data Access Objects)
- ✅ Database schema and tables
- ✅ Foreign key relationships
- ✅ iBATIS SQL mappings
- ✅ API endpoints

```bash
# Basic backend PRD
codeindex prd backend --output-dir ./output/prd

# With project filter (monorepo)
codeindex prd backend \
    --project cuco-ui-admin \
    --output-dir ./output/prd

# Specify extraction file
codeindex prd backend \
    --extraction-file ./output/extraction-results.jsonl \
    --output-dir ./output/prd
```

**Generated files**:
```
output/prd/
├── backend_prd.md                 # Main PRD document
└── backend/
    ├── services/
    │   ├── UserService.json
    │   └── OrderService.json
    ├── daos/
    │   ├── UserDao.json
    │   └── OrderDao.json
    ├── tables/
    │   ├── users.json
    │   └── orders.json
    └── endpoints/
        ├── UserEndpoint.json
        └── OrderEndpoint.json
```

### Frontend PRD

Generates documentation for:
- ✅ GWT Presenters with event handlers
- ✅ GWT Views with UI fields
- ✅ UiBinder forms and widgets
- ✅ Navigation graph and flows
- ✅ RPC service calls
- ✅ Activity/Place patterns

```bash
# Basic frontend PRD
codeindex prd frontend --output-dir ./output/prd

# With project filter
codeindex prd frontend \
    --project cuco-ui-admin \
    --output-dir ./output/prd

# Specify extraction file
codeindex prd frontend \
    --extraction-file ./output/extraction-results.jsonl \
    --output-dir ./output/prd
```

**Generated files**:
```
output/prd/
├── frontend_prd.md                # Main PRD document
└── frontend/
    ├── components/
    │   ├── UserPresenter.json
    │   ├── UserView.json
    │   └── DashboardPresenter.json
    └── forms/
        ├── UserForm.json
        └── OrderForm.json
```

### Combined Generation

```bash
# Generate both backend and frontend PRDs
codeindex prd backend --output-dir ./output/prd
codeindex prd frontend --output-dir ./output/prd

# Or in parallel (faster)
codeindex prd backend --output-dir ./output/prd &
BACKEND_PID=$!

codeindex prd frontend --output-dir ./output/prd &
FRONTEND_PID=$!

# Wait for both to complete
wait $BACKEND_PID
wait $FRONTEND_PID

echo "PRD generation complete!"
```

---

## 📊 Monitoring & Validation

### Monitor Progress

```bash
# Watch log file in real-time
tail -f logs/log_cuco-ui-admin_backend_prd_*.log

# Check process status
ps aux | grep "codeindex prd"

# Check if still running
pgrep -f "codeindex prd"
```

### Validate Results

```bash
# 1. Check if files were generated
ls -lh ./output/prd/

# Expected files:
# - backend_prd.md (100-500KB typical)
# - frontend_prd.md (50-300KB typical)
# - backend/ directory with JSON files
# - frontend/ directory with JSON files

# 2. Check file sizes (should not be empty)
du -sh ./output/prd/*

# 3. Check PRD content
head -50 ./output/prd/backend_prd.md
head -50 ./output/prd/frontend_prd.md

# 4. Count components documented
echo "Backend services documented:"
ls ./output/prd/backend/services/ | wc -l

echo "Frontend components documented:"
ls ./output/prd/frontend/components/ | wc -l

echo "GWT Presenters documented:"
grep -c "## GWT Presenters" ./output/prd/frontend_prd.md
```

### Validation Checklist

After PRD generation, verify:

- [ ] `backend_prd.md` exists and is >10KB
- [ ] `frontend_prd.md` exists and is >10KB
- [ ] Backend JSON files in `backend/services/`, `backend/daos/`
- [ ] Frontend JSON files in `frontend/components/`, `frontend/forms/`
- [ ] PRD contains correct project name
- [ ] PRD contains table of contents
- [ ] PRD contains component descriptions
- [ ] No error messages in log files

---

## 📁 Output Structure

### Complete PRD Output

```
output/
└── cuco-ui-admin/
    ├── discovery-inventory.jsonl      # Step 1: Discovery results
    ├── extraction-results.jsonl       # Step 2: Extraction results
    ├── navigation-graph.json          # Step 2: GWT navigation
    └── prd/                           # Step 3: PRD generation
        ├── backend_prd.md             # Backend requirements
        ├── frontend_prd.md            # Frontend requirements
        ├── backend/
        │   ├── services/
        │   │   ├── UserService.json
        │   │   ├── OrderService.json
        │   │   └── ProductService.json
        │   ├── daos/
        │   │   ├── UserDao.json
        │   │   ├── OrderDao.json
        │   │   └── ProductDao.json
        │   ├── tables/
        │   │   ├── users.json
        │   │   ├── orders.json
        │   │   └── products.json
        │   └── endpoints/
        │       ├── UserEndpoint.json
        │       └── OrderEndpoint.json
        └── frontend/
            ├── components/
            │   ├── UserPresenter.json
            │   ├── UserView.json
            │   ├── OrderPresenter.json
            │   └── DashboardPresenter.json
            └── forms/
                ├── UserForm.json
                ├── OrderForm.json
                └── ProductForm.json
```

### PRD Document Structure

**backend_prd.md** contains:
1. **Project Overview** - Architecture summary
2. **Services** - Business logic components
3. **Data Access Layer** - DAOs and database
4. **Database Schema** - Tables and relationships
5. **Foreign Keys** - Multi-source FK relationships
6. **API Endpoints** - REST/RPC endpoints
7. **iBATIS Mappings** - SQL queries and mappings

**frontend_prd.md** contains:
1. **Project Overview** - Frontend architecture
2. **GWT Application Components** - Modules and entry points
3. **GWT Presenters** - Event handlers and navigation
4. **GWT Views** - UI fields and bindings
5. **UiBinder Forms** - Form fields and widgets
6. **Navigation Graph** - Application flows
7. **RPC Services** - Client-server communication

---

## 🔧 Advanced Usage

### Filter by Project (Monorepo)

```bash
# Generate PRD for specific project in monorepo
codeindex prd backend \
    --project backend-api \
    --output-dir ./output/backend-api/prd

codeindex prd frontend \
    --project frontend-app \
    --output-dir ./output/frontend-app/prd
```

### Custom Extraction File

```bash
# Use specific extraction results file
codeindex prd backend \
    --extraction-file ./archive/extraction-2024-12-15.jsonl \
    --output-dir ./output/historical-prd
```

### Batch PRD Generation

```bash
#!/bin/bash
# generate-all-prds.sh
# Generate PRDs for multiple projects

PROJECTS=("backend-api" "frontend-app" "shared-models")

for project in "${PROJECTS[@]}"; do
    echo "Generating PRD for $project..."

    # Backend PRD
    codeindex prd backend \
        --project "$project" \
        --output-dir "./output/${project}/prd" \
        > "logs/prd_${project}_backend.log" 2>&1 &

    # Frontend PRD (if applicable)
    if [ "$project" != "shared-models" ]; then
        codeindex prd frontend \
            --project "$project" \
            --output-dir "./output/${project}/prd" \
            > "logs/prd_${project}_frontend.log" 2>&1 &
    fi
done

# Wait for all PRD generations to complete
wait

echo "All PRDs generated!"
ls -lh ./output/*/prd/*.md
```

---

## 🐛 Troubleshooting

### Issue: PRD Files Are Empty or Very Small

**Symptoms**:
```bash
ls -lh output/prd/backend_prd.md
# Shows <5KB file
```

**Causes & Solutions**:

1. **No data indexed**
   ```bash
   # Check if indexing completed
   codeindex status

   # Re-run indexing if needed
   codeindex index \
       --inventory ./output/discovery-inventory.jsonl \
       --extraction ./output/extraction-results.jsonl
   ```

2. **Wrong project name**
   ```bash
   # List available projects
   codeindex status --verbose

   # Use correct project name
   codeindex prd backend --project correct-project-name
   ```

3. **Ollama not running**
   ```bash
   # Check Ollama
   curl http://localhost:11434/api/tags

   # Start if needed
   sudo systemctl start ollama
   ```

### Issue: PRD Generation Takes Too Long

**Expected time**:
- Small project (<100 components): 2-5 minutes
- Medium project (100-500 components): 5-15 minutes
- Large project (>500 components): 15-30 minutes

**Solutions**:
```bash
# Check if Ollama is responding
curl http://localhost:11434/api/tags

# Monitor progress
tail -f logs/log_*_prd_*.log

# Check system resources
htop  # CPU and memory usage
```

### Issue: Missing Components in PRD

**Symptoms**: PRD doesn't include all expected components

**Diagnosis**:
```bash
# 1. Check extraction results
jq '.gwt_role' output/extraction-results.jsonl | sort | uniq -c

# 2. Check indexing
codeindex status --verbose

# 3. Search for specific component
codeindex search "UserPresenter"
```

**Solutions**:
```bash
# Re-run extraction if needed
codeindex extract \
    --inventory ./output/discovery-inventory.jsonl \
    --output ./output/extraction-results.jsonl

# Re-index
codeindex index \
    --inventory ./output/discovery-inventory.jsonl \
    --extraction ./output/extraction-results.jsonl

# Re-generate PRD
codeindex prd frontend --output-dir ./output/prd
```

### Issue: Ollama Timeout During PRD Generation

**Symptoms**:
```
TimeoutError: Request to Ollama timed out
```

**Solutions**:
```bash
# 1. Increase timeout in .env
nano .env
# Add/modify:
OLLAMA_READ_TIMEOUT=900  # 15 minutes

# 2. Restart PRD generation
source .env
codeindex prd backend --output-dir ./output/prd
```

---

## 📈 Expected Results

### Successful PRD Generation

```bash
$ codeindex prd backend --output-dir ./output/prd

Generating backend PRD...
Loading artifacts from Weaviate...
Found 45 services
Found 32 DAOs
Found 28 database tables
Found 67 foreign key relationships
Found 23 API endpoints

Processing services...
Processing DAOs...
Processing database schema...
Processing foreign keys...
Processing endpoints...

Backend PRD generated successfully!
Output: ./output/prd/backend_prd.md

$ codeindex prd frontend --output-dir ./output/prd

Generating frontend PRD...
Loading GWT artifacts from Weaviate...
Found 38 GWT Presenters
Found 35 GWT Views
Found 42 UiBinder forms
Found 54 navigation edges

Processing GWT components...
Processing presenters...
Processing views...
Processing forms...
Processing navigation graph...

Frontend PRD generated successfully!
Output: ./output/prd/frontend_prd.md
```

### PRD Quality Indicators

**Backend PRD** should include:
- ✅ 20+ services documented
- ✅ 15+ DAOs documented
- ✅ Database schema with FK relationships
- ✅ Multi-source FK coverage (Java + iBATIS + SQL)
- ✅ API endpoint documentation

**Frontend PRD** should include:
- ✅ 30+ GWT Presenters documented
- ✅ 25+ GWT Views documented
- ✅ UiBinder form fields
- ✅ Navigation graph visualization
- ✅ Event handler documentation

---

## 🎯 Best Practices

### 1. Always Run After Pipeline Completion

```bash
# Wrong: Generate PRD before indexing completes
codeindex prd backend --output-dir ./output/prd  # No data!

# Right: Wait for pipeline to complete
./run.sh
# Wait for completion...
codeindex status  # Verify
codeindex prd backend --output-dir ./output/prd  # Generate
```

### 2. Use Timestamped Logs

```bash
# Production pattern
TIMESTAMP=$(date +'%Y-%m-%d_%H-%M-%S')
codeindex prd backend \
    --output-dir ./output/prd \
    > "logs/prd_backend_${TIMESTAMP}.log" 2>&1
```

### 3. Generate Both Backend and Frontend

```bash
# Always generate both for complete documentation
codeindex prd backend --output-dir ./output/prd
codeindex prd frontend --output-dir ./output/prd
```

### 4. Archive PRD Versions

```bash
# Archive PRDs with timestamps
TIMESTAMP=$(date +'%Y-%m-%d')
cp output/prd/backend_prd.md "archive/backend_prd_${TIMESTAMP}.md"
cp output/prd/frontend_prd.md "archive/frontend_prd_${TIMESTAMP}.md"
```

### 5. Validate Results

```bash
# Always check PRD quality after generation
ls -lh output/prd/*.md
grep -c "## " output/prd/backend_prd.md  # Count sections
grep -c "Presenter" output/prd/frontend_prd.md  # Count components
```

---

## 🔑 Quick Command Reference

```bash
# Generate backend PRD
codeindex prd backend --output-dir ./output/prd

# Generate frontend PRD
codeindex prd frontend --output-dir ./output/prd

# With project filter
codeindex prd backend --project my-project --output-dir ./output/prd

# View generated PRD
less output/prd/backend_prd.md

# Count documented components
ls output/prd/backend/services/ | wc -l
ls output/prd/frontend/components/ | wc -l

# Validate file sizes
du -sh output/prd/*
```

---

**Last Updated**: 2025-12-28
**Feature**: 007 (MVP Complete)
**Status**: ✅ Production Ready
