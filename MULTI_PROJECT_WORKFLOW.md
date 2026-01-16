# Multi-Project Workflow Guide

**Purpose**: How to index multiple directories/projects and generate PRDs for each

---

## Overview

The codebase indexer supports **multiple projects in a single Weaviate instance** with proper isolation and filtering. Each project gets:

1. **Unique project ID**: `groupId:artifactId:version` or path-based hash
2. **Isolated artifacts**: All indexed artifacts tagged with project ID
3. **Filtered queries**: Search and PRD generation can target specific projects

---

## Architecture

### Project Identification

Each discovered project gets a unique identifier:

```python
# Maven projects (from pom.xml)
project_id = "com.example:myapp:1.0.0"  # groupId:artifactId:version

# Non-Maven projects (from directory path)
project_id = "hash_of_path_12345678"
```

### Weaviate Storage

All artifacts are stored with project metadata:

```json
{
  "class": "BackendDoc",
  "properties": {
    "artifact_id": "abc-123",
    "project": "com.example:myapp:1.0.0",  // ← Project filter
    "file_path": "/path/to/file.java",
    "content": "..."
  }
}
```

### Project Isolation

- **Discovery**: Each `run.sh` execution discovers one project tree
- **Indexing**: All artifacts tagged with project ID
- **Querying**: Filter by project ID to isolate results

---

## Workflow 1: Index Multiple Independent Projects

**Use Case**: You have several separate Java projects (e.g., microservices)

### Project Structure

```
/workspace/
├── project-a/          # Service A
│   ├── pom.xml
│   └── src/
├── project-b/          # Service B
│   ├── pom.xml
│   └── src/
└── project-c/          # Service C
    ├── pom.xml
    └── src/
```

### Step 1: Index Each Project Separately

```bash
# Index Project A
./run.sh project-a /workspace/project-a

# Index Project B
./run.sh project-b /workspace/project-b

# Index Project C
./run.sh project-c /workspace/project-c
```

**What Happens:**
- Each run creates separate discovery/extraction files:
  - `data/discovery-project-a.jsonl`
  - `data/discovery-project-b.jsonl`
  - `data/discovery-project-c.jsonl`
- All projects coexist in same Weaviate instance
- Each artifact tagged with its project ID

### Step 2: Verify Indexing

```bash
# Check all projects
codeindex status

# Output shows:
# Projects indexed: 3
#   - com.example:project-a:1.0.0 (543 artifacts)
#   - com.example:project-b:2.0.0 (312 artifacts)
#   - com.example:project-c:1.5.0 (789 artifacts)

# Check specific project
codeindex status --project "com.example:project-a:1.0.0"
```

### Step 3: Generate PRDs for Each Project

```bash
# Generate PRD for Project A
codeindex prd full \
  --project "com.example:project-a:1.0.0" \
  --source-dir /workspace/project-a \
  --output-dir ./output/project-a-prd

# Generate PRD for Project B
codeindex prd full \
  --project "com.example:project-b:2.0.0" \
  --source-dir /workspace/project-b \
  --output-dir ./output/project-b-prd

# Generate PRD for Project C
codeindex prd full \
  --project "com.example:project-c:1.5.0" \
  --source-dir /workspace/project-c \
  --output-dir ./output/project-c-prd
```

**Result:**
```
./output/
├── project-a-prd/
│   ├── master_prd.md
│   └── prd/
│       ├── database_prd.md
│       ├── service_prd.md
│       └── frontend_prd.md
├── project-b-prd/
│   └── ...
└── project-c-prd/
    └── ...
```

---

## Workflow 2: Monorepo with Multiple Projects

**Use Case**: Single repository with multiple Maven modules

### Project Structure

```
/monorepo/
├── pom.xml              # Parent POM
├── backend-api/         # Module 1
│   ├── pom.xml
│   └── src/
├── frontend-web/        # Module 2
│   ├── pom.xml
│   └── src/
└── shared-models/       # Module 3
    ├── pom.xml
    └── src/
```

### Option A: Index Entire Monorepo (Recommended)

```bash
# Index all modules at once with dependency resolution
./run.sh monorepo /monorepo

# This discovers:
# - Parent project: com.example:monorepo:1.0.0
# - Module: com.example:backend-api:1.0.0
# - Module: com.example:frontend-web:1.0.0
# - Module: com.example:shared-models:1.0.0
```

**Benefits:**
- Single indexing run
- Automatic dependency resolution between modules
- Cross-module references preserved

**Generate PRDs:**
```bash
# Generate PRD for specific module
codeindex prd full \
  --project "com.example:backend-api:1.0.0" \
  --source-dir /monorepo/backend-api \
  --output-dir ./output/backend-api-prd

# Generate PRD for another module
codeindex prd full \
  --project "com.example:frontend-web:1.0.0" \
  --source-dir /monorepo/frontend-web \
  --output-dir ./output/frontend-web-prd
```

### Option B: Index Specific Module Only

```bash
# Index only backend-api with its dependencies
./run.sh backend-api /monorepo

# Uses --project flag internally to scope discovery
# Still resolves dependencies (shared-models)
```

**Use Case:**
- Large monorepo, only care about one module
- Faster indexing
- Still includes dependencies via dependency resolution

---

## Workflow 3: Multiple Unrelated Directories

**Use Case**: Different Java codebases in different locations

### Structure

```
/path1/legacy-system/       # Old Java EE app
/path2/new-microservice/    # Spring Boot app
/path3/gwt-frontend/        # GWT application
```

### Step 1: Index Each Directory

```bash
# Index legacy system
./run.sh legacy-system /path1/legacy-system

# Index microservice
./run.sh microservice /path2/new-microservice

# Index GWT frontend
./run.sh gwt-app /path3/gwt-frontend
```

### Step 2: Generate PRDs

```bash
# Method 1: Use project ID (if Maven)
codeindex prd full \
  --project "com.legacy:legacy-system:3.0.0" \
  --source-dir /path1/legacy-system \
  --output-dir ./output/legacy-prd

# Method 2: Use custom name (non-Maven)
codeindex prd full \
  --project "legacy-system" \
  --source-dir /path1/legacy-system \
  --output-dir ./output/legacy-prd
```

---

## Workflow 4: Batch Processing Multiple Projects

**Use Case**: Automate indexing and PRD generation for many projects

### Script: `batch-index-and-prd.sh`

```bash
#!/bin/bash
# Batch index and generate PRDs for multiple projects

set -e

# Define projects (name and path)
declare -A PROJECTS=(
    ["project-a"]="/workspace/project-a"
    ["project-b"]="/workspace/project-b"
    ["project-c"]="/workspace/project-c"
)

# Index all projects
for name in "${!PROJECTS[@]}"; do
    path="${PROJECTS[$name]}"
    echo "==================================="
    echo "Indexing: $name"
    echo "Path: $path"
    echo "==================================="

    ./run.sh "$name" "$path"
done

echo ""
echo "==================================="
echo "All projects indexed!"
echo "==================================="

# Get project IDs from Weaviate
source .venv/bin/activate
PROJECT_IDS=$(codeindex status --verbose | grep "project_id" | awk '{print $2}')

# Generate PRDs for each project
for name in "${!PROJECTS[@]}"; do
    path="${PROJECTS[$name]}"

    # Find matching project ID
    PROJECT_ID=$(codeindex status --verbose | grep -A5 "name: $name" | grep "project_id" | awk '{print $2}')

    echo "==================================="
    echo "Generating PRD: $name"
    echo "Project ID: $PROJECT_ID"
    echo "==================================="

    codeindex prd full \
        --project "$PROJECT_ID" \
        --source-dir "$path" \
        --output-dir "./output/${name}-prd" \
        --quiet
done

echo ""
echo "==================================="
echo "Batch processing complete!"
echo "==================================="
echo "PRD outputs in ./output/"
ls -lh ./output/
```

### Usage

```bash
chmod +x batch-index-and-prd.sh
./batch-index-and-prd.sh
```

---

## Workflow 5: Incremental Updates

**Use Case**: Re-index one project without affecting others

### Scenario

You have 3 projects indexed, but only Project A changed.

### Solution: Re-index Single Project

```bash
# Re-index only Project A
./run.sh project-a /workspace/project-a

# This UPDATES existing artifacts for Project A
# Project B and C remain unchanged
```

**How It Works:**
- Discovery generates new inventory for Project A
- Extraction analyzes Project A files
- Indexing UPSERTS (updates or inserts) Project A artifacts
- Other projects untouched

**Note**: Current implementation has **partial idempotency**:
- Re-indexing MAY create duplicates in some cases
- Best practice: Use `--dry-run` first to preview
- Future: Full idempotent indexing (update-only mode)

---

## Workflow 6: Cross-Project Search

**Use Case**: Search across all indexed projects or filter by project

### Search All Projects

```bash
# Search everything in Weaviate
codeindex search "user authentication"

# Returns results from ALL projects
```

### Search Specific Project

```bash
# Search only Project A
codeindex search "user authentication" \
  --project "com.example:project-a:1.0.0"

# Returns results ONLY from Project A
```

### Search Multiple Projects (Programmatic)

```python
from codeindex.services.weaviate_client import WeaviateClient

client = WeaviateClient()

# Search in specific projects
projects = [
    "com.example:project-a:1.0.0",
    "com.example:project-b:2.0.0"
]

for project in projects:
    results = client.search(
        query="database connection",
        filters={"project": project},
        limit=10
    )
    print(f"Results from {project}: {len(results)}")
```

---

## Workflow 7: Project Cleanup

**Use Case**: Remove a specific project from Weaviate

### Option A: Selective Deletion (Future Feature)

```bash
# Not yet implemented
codeindex delete --project "com.example:old-project:1.0.0"
```

### Option B: Full Weaviate Rebuild

```bash
# Nuclear option: Clear all data and re-index
./docker-weaviate.sh clean
./docker-weaviate.sh start

# Re-index only the projects you want
./run.sh project-a /workspace/project-a
./run.sh project-b /workspace/project-b
# Skip old-project
```

---

## Best Practices

### 1. **Consistent Naming**

```bash
# Good: Use meaningful names
./run.sh backend-api /workspace/backend-api
./run.sh frontend /workspace/frontend

# Bad: Generic names
./run.sh myapp /workspace/backend-api
./run.sh app2 /workspace/frontend
```

### 2. **Organize Output Directories**

```bash
# Good structure
./output/
├── backend-api-prd/
├── frontend-prd/
└── shared-models-prd/

# Bad: All in one directory
./output/
├── backend_prd.md
├── frontend_prd.md
└── shared_prd.md
```

### 3. **Use Project IDs for PRD Generation**

```bash
# Always specify --project to ensure correct filtering
codeindex prd full \
  --project "com.example:myapp:1.0.0" \
  --source-dir /path/to/source \
  --output-dir ./output/myapp-prd
```

### 4. **Check Status Before PRD Generation**

```bash
# Verify project is indexed
codeindex status --project "com.example:myapp:1.0.0"

# If no artifacts, run indexing first
if [ $? -ne 0 ]; then
    echo "Project not indexed, running pipeline..."
    ./run.sh myapp /path/to/source
fi

# Now generate PRD
codeindex prd full --project "com.example:myapp:1.0.0" ...
```

### 5. **Parallel PRD Generation**

```bash
# Generate PRDs for multiple projects in parallel
codeindex prd full --project "com.example:project-a:1.0.0" ... &
codeindex prd full --project "com.example:project-b:2.0.0" ... &
codeindex prd full --project "com.example:project-c:1.5.0" ... &

# Wait for all to complete
wait

echo "All PRDs generated!"
```

---

## Limitations & Considerations

### Current Limitations

1. **Partial Idempotency**: Re-indexing may create duplicates
   - **Workaround**: Clean and rebuild Weaviate if unsure

2. **No Selective Deletion**: Can't delete individual projects
   - **Workaround**: Full Weaviate rebuild

3. **Manual Project ID Discovery**: Must check status for exact project IDs
   - **Workaround**: Use `codeindex status --verbose` to find IDs

### Performance Considerations

1. **Indexing Time**: ~10-30 minutes per project (depends on size)
   - **Tip**: Use `run-cuco.sh` in background: `nohup ./run-cuco.sh ... &`

2. **PRD Generation Time**: ~5-15 minutes per project
   - **Tip**: Generate PRDs in parallel (see Best Practices #5)

3. **Weaviate Memory**: Scales with number of artifacts
   - **Rule of thumb**: ~1GB RAM per 10,000 artifacts
   - **Monitor**: `docker stats weaviate-i19`

### Disk Space

```bash
# Typical space requirements per project
data/
├── discovery-project-a.jsonl     # ~1-5 MB
└── extraction-project-a.jsonl    # ~10-50 MB

output/
└── project-a-prd/                # ~500 KB - 2 MB

# Weaviate data (persistent)
weaviate-data/                    # ~500 MB - 5 GB (all projects)
```

---

## Troubleshooting

### Problem: Can't Find Project ID

```bash
# List all indexed projects
codeindex status --verbose

# Shows:
# Projects:
#   - com.example:project-a:1.0.0
#   - com.example:project-b:2.0.0

# Use exact ID in PRD command
codeindex prd full --project "com.example:project-a:1.0.0" ...
```

### Problem: Empty PRD Generated

```bash
# Check if project has artifacts
codeindex status --project "com.example:myapp:1.0.0"

# If "Artifacts: 0", re-run indexing
./run.sh myapp /path/to/source
```

### Problem: Wrong Project Artifacts in PRD

```bash
# Verify project ID matches exactly
codeindex search "test" --project "com.example:myapp:1.0.0"

# If wrong artifacts appear, check for:
# 1. Typos in project ID
# 2. Multiple versions indexed (1.0.0 vs 2.0.0)
# 3. Weaviate state corruption (rebuild)
```

### Problem: Indexing One Project Affects Others

```bash
# This shouldn't happen, but if it does:
# 1. Check logs for errors
# 2. Verify project IDs are unique
# 3. Rebuild Weaviate if corrupted

./docker-weaviate.sh clean
./docker-weaviate.sh start
# Re-index all projects
```

---

## Summary

**To index and generate PRDs for multiple directories:**

1. **Index each project separately**:
   ```bash
   ./run.sh project-a /path/to/project-a
   ./run.sh project-b /path/to/project-b
   ```

2. **Verify indexing**:
   ```bash
   codeindex status
   ```

3. **Generate PRDs with project filtering**:
   ```bash
   codeindex prd full \
     --project "PROJECT_ID" \
     --source-dir /path/to/source \
     --output-dir ./output/project-prd
   ```

4. **Use batch scripts for automation**:
   ```bash
   # Create custom batch script for your projects
   ```

**Key Points:**
- ✅ Multiple projects coexist in Weaviate with isolation
- ✅ Use `--project` flag to filter queries and PRD generation
- ✅ Each project gets unique output directory
- ✅ Projects can be indexed and updated independently
- ⚠️ Re-indexing may create duplicates (partial idempotency)
- ⚠️ No selective deletion (clean and rebuild to remove projects)
