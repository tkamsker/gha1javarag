# Fix: Weaviate Schema Missing

**Error**: `Weaviate schema is missing required classes: {'Project', 'CodeArtifact'}`

**Root Cause**: Weaviate database has no schema defined (empty database)

**Solution**: Run indexing pipeline to create schema automatically

---

## Quick Fix (Production)

### Option 1: Index Your Codebase (Recommended)

This creates the schema AND indexes your code:

```bash
cd /home/tkamsker/development/Iteration20/gha1javarag
source .venv/bin/activate

# For cuco-ui-admin project
./run-cuco.sh --yes /mnt/cucocalcai/cuco-master/cuco-ui-admin

# This will:
# 1. Discover all source files
# 2. Extract semantic information
# 3. Create Weaviate schema automatically (--create-schema flag)
# 4. Index all artifacts
# 5. Show status
```

### Option 2: Create Schema Only (No Indexing)

If you just want to create the schema without indexing:

```bash
cd /home/tkamsker/development/Iteration20/gha1javarag
source .venv/bin/activate

# Create minimal discovery file
echo '{"projects": []}' > data/empty-discovery.jsonl
echo '{}' > data/empty-extraction.jsonl

# Run index with --create-schema (creates schema, indexes nothing)
codeindex index \
  --inventory data/empty-discovery.jsonl \
  --extraction data/empty-extraction.jsonl \
  --create-schema

# Verify schema created
codeindex status
```

---

## Understanding the Error

### What Happened

1. **Weaviate is running**: ✓ API accessible at http://localhost:8080
2. **Schema is empty**: ✗ No classes defined (Project, CodeArtifact, etc.)
3. **Status command fails**: Can't check status without schema

### Why This Happens

Fresh Weaviate instances have **no schema** until you:
- Run `codeindex index --create-schema`, OR
- Manually create schema via API

### What Schema Gets Created

Running the pipeline creates these classes:

**Core Classes:**
- `Project` - Maven project metadata
- `CodeArtifact` - Generic code artifact (deprecated but still used)

**Typed Artifact Classes:**
- `BackendDoc` - Backend services/classes
- `DaoCall` - Data access objects
- `DbTable` - Database tables (needed for Chat "Analyze Database")
- `GwtModule` - GWT modules
- `GwtEndpoint` - GWT RPC endpoints
- `GwtUiBinder` - GWT UI templates
- `JspForm` - JSP forms
- `IbatisStatement` - iBATIS SQL statements
- `DtoArtifact` - Data Transfer Objects

---

## Verification After Fix

```bash
# 1. Check schema classes exist
curl -s http://localhost:8080/v1/schema | jq -r '.classes[].class'

# Should show:
# Project
# CodeArtifact
# BackendDoc
# DaoCall
# DbTable
# ... etc

# 2. Check status works now
codeindex status

# Should show:
# Service Health:
#   Weaviate: ✓ Connected
#   Ollama:   ✓ Connected
# Projects indexed: 0 (or more if you indexed)

# 3. Verify DbTable class exists (for Chat feature)
curl -s http://localhost:8080/v1/schema | jq '.classes[] | select(.class=="DbTable")'

# Should return DbTable class definition
```

---

## Detailed Indexing Steps

If you want to see what happens during indexing:

```bash
cd /home/tkamsker/development/Iteration20/gha1javarag
source .venv/bin/activate

# Set your source directory
SOURCE_DIR="/mnt/cucocalcai/cuco-master/cuco-ui-admin"

# Step 1: Discover (auto-detects workspace root for dependencies)
codeindex discover \
  --source-dir "$SOURCE_DIR" \
  --output data/discovery-cuco.jsonl \
  --dependency-depth 1 \
  --workspace-root "$(dirname "$SOURCE_DIR")"

# Step 2: Extract semantic information
codeindex extract \
  --inventory data/discovery-cuco.jsonl \
  --output data/extraction-cuco.jsonl

# Step 3: Index with schema creation
codeindex index \
  --inventory data/discovery-cuco.jsonl \
  --extraction data/extraction-cuco.jsonl \
  --create-schema

# Step 4: Verify
codeindex status
```

---

## What --create-schema Does

The `--create-schema` flag:

1. **Checks existing schema**: Queries Weaviate for current classes
2. **Identifies missing classes**: Compares with required schema
3. **Creates missing classes**: Adds all required classes to Weaviate
4. **Configures properties**: Sets up all fields, indexes, vectorizers
5. **Continues indexing**: Proceeds to index your artifacts

**Safe to run multiple times**: If schema exists, it's not recreated.

---

## Why Both run.sh and run-cuco.sh Work

Both scripts include `--create-schema` automatically:

```bash
# run.sh line 163
codeindex index --inventory "$DISCOVERY_FILE" --extraction "$EXTRACTION_FILE" --create-schema

# run-cuco.sh line 212
codeindex index --inventory "$DISCOVERY_FILE" --extraction "$EXTRACTION_FILE" --create-schema
```

So just running either script will fix the schema issue.

---

## Container Status Confusion

You saw:
```
[WARNING] Weaviate container is not running
[SUCCESS] Weaviate API is accessible
```

This is expected! Possible reasons:

1. **Container running under different name**: Docker may use a different container name than expected
2. **Multiple Weaviate instances**: You might have Weaviate running outside Docker
3. **Port forwarding**: Weaviate accessible via port forward even if container check fails

**What matters**: API is accessible (✓), so Weaviate works!

To check actual container:
```bash
docker ps | grep weaviate
# OR
docker ps | grep 8080
```

---

## Troubleshooting

### Issue: "Permission denied" during indexing

```bash
# Make sure you own the data directory
sudo chown -R $USER:$USER data/
```

### Issue: "Disk space" error

```bash
# Check disk space
df -h

# Clean old files if needed
rm data/discovery-*.jsonl
rm data/extraction-*.jsonl
```

### Issue: Schema creation fails

```bash
# Check Weaviate logs
docker logs $(docker ps | grep weaviate | awk '{print $1}')

# Or if using docker-compose
cd /home/tkamsker/development/Iteration20/gha1javarag
docker-compose logs weaviate
```

### Issue: Ollama model not found

```bash
# Check available models
ollama list

# Pull the model if needed
ollama pull qwen2.5-coder:32b
```

---

## Expected Timeline

For a typical Java project (500-1000 files):

- **Discovery**: 1-2 minutes
- **Extraction**: 10-30 minutes (depends on file size, LLM speed)
- **Indexing**: 2-5 minutes (includes schema creation)
- **Total**: ~15-40 minutes

For cuco-ui-admin (539 files reported in logs):
- **Expected**: ~20-30 minutes total

---

## After Schema is Created

Once schema exists, you can:

1. **Use Streamlit Chat**: "Analyze Database" will work
2. **Search code**: `codeindex search "query"`
3. **Generate PRDs**: `codeindex prd full --project ...`
4. **Check status**: `codeindex status`

---

## Summary

**Immediate Action**:
```bash
cd /home/tkamsker/development/Iteration20/gha1javarag
./run-cuco.sh --yes /mnt/cucocalcai/cuco-master/cuco-ui-admin
```

This single command will:
- ✅ Create the complete Weaviate schema
- ✅ Index your entire codebase
- ✅ Fix the "No database tables found" issue in Streamlit
- ✅ Enable all features (search, PRD generation, Chat analysis)

**Verification**:
```bash
codeindex status
# Should now show: Weaviate: ✓ Connected
```
