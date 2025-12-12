# CLI Interface Contract

**Feature**: 001-java-codebase-indexer
**Date**: 2025-12-12
**Version**: 1.0.0

## Overview

This document defines the command-line interface for the Java Codebase Indexer Pipeline. All commands follow Click framework conventions with consistent parameter naming and output formats.

## Global Options

Available for all commands:

```bash
--config PATH          # Path to .env file (default: .env)
--log-level LEVEL      # Logging level: DEBUG, INFO, WARNING, ERROR (default: INFO)
--format FORMAT        # Output format: text, json (default: text)
--help                 # Show help message
```

## Entry Point

```bash
python -m codeindex [GLOBAL_OPTIONS] COMMAND [COMMAND_OPTIONS]
```

or after installation:

```bash
codeindex [GLOBAL_OPTIONS] COMMAND [COMMAND_OPTIONS]
```

## Commands

### 1. discover

**Purpose**: Recursively scan directory tree to discover Maven projects and create file inventory.

**Usage**:
```bash
codeindex discover [OPTIONS]
```

**Options**:

| Option | Short | Type | Required | Default | Description |
|--------|-------|------|----------|---------|-------------|
| --source-dir | -s | PATH | Yes* | $JAVA_SOURCE_DIR | Root directory to scan |
| --output | -o | PATH | No | ./data/inventory.jsonl | Output inventory file path |
| --project | -p | TEXT | No | None | Specific project name filter |
| --force | -f | FLAG | No | False | Re-scan even if inventory exists |
| --verbose | -v | FLAG | No | False | Show detailed progress |

\* Required if JAVA_SOURCE_DIR not set in environment

**Output** (text format):
```
Scanning directory: /path/to/source
Found 3 Maven projects:
  - com.example:my-app:1.0.0 (2,450 files)
  - com.example:my-lib:1.0.0 (1,200 files)
  - com.example:my-web:2.0.0 (3,100 files)

Total: 6,750 files discovered in 12.5 seconds
Inventory saved to: ./data/inventory.jsonl
```

**Output** (json format):
```json
{
  "scan_timestamp": "2025-12-12T10:30:00Z",
  "root_directory": "/path/to/source",
  "projects": [
    {
      "project_id": "com.example:my-app:1.0.0",
      "name": "my-app",
      "path": "/path/to/source/my-app",
      "file_count": 2450
    }
  ],
  "total_files": 6750,
  "scan_duration_seconds": 12.5
}
```

**Exit Codes**:
- 0: Success
- 1: Error (invalid path, permission denied, etc.)
- 2: No projects found (with informative message)

---

### 2. extract

**Purpose**: Process discovered files to generate AI summaries, classifications, and tags.

**Usage**:
```bash
codeindex extract [OPTIONS]
```

**Options**:

| Option | Short | Type | Required | Default | Description |
|--------|-------|------|----------|---------|-------------|
| --inventory | -i | PATH | No | ./data/inventory.jsonl | Input inventory file |
| --output | -o | PATH | No | ./data/extracted/ | Output directory for results |
| --project | -p | TEXT | No | None | Specific project to extract |
| --max-concurrent | -c | INT | No | $MAX_CONCURRENT_AI_CALLS or 10 | Max concurrent AI requests |
| --skip-ai | | FLAG | No | False | Skip AI processing (classification only) |
| --force | -f | FLAG | No | False | Re-extract even if results exist |
| --verbose | -v | FLAG | No | False | Show detailed progress |

**Output** (text format):
```
Extracting files from inventory: ./data/inventory.jsonl
Processing project: com.example:my-app:1.0.0 (2,450 files)

Progress: [████████████████████] 2,450/2,450 files (100%)
Elapsed: 00:08:15 | ETA: 00:00:00 | Rate: 50.2 files/min

Summary:
  - Files processed: 2,450
  - Files skipped: 12 (binary, empty)
  - AI calls: 2,438
  - Errors: 5 (see logs)
  - Duration: 8 minutes 15 seconds

Extraction complete. Results saved to: ./data/extracted/
```

**Output** (json format):
```json
{
  "project_id": "com.example:my-app:1.0.0",
  "files_processed": 2450,
  "files_skipped": 12,
  "ai_calls": 2438,
  "errors": 5,
  "duration_seconds": 495,
  "output_directory": "./data/extracted/"
}
```

**Exit Codes**:
- 0: Success (even with some errors, if majority succeeded)
- 1: Fatal error (Ollama unavailable, invalid inventory, etc.)
- 3: Project locked (another extraction in progress)

---

### 3. index

**Purpose**: Store extracted artifacts in Weaviate with vector embeddings.

**Usage**:
```bash
codeindex index [OPTIONS]
```

**Options**:

| Option | Short | Type | Required | Default | Description |
|--------|-------|------|----------|---------|-------------|
| --input | -i | PATH | No | ./data/extracted/ | Input extraction results directory |
| --project | -p | TEXT | No | None | Specific project to index |
| --batch-size | -b | INT | No | 50 | Objects per Weaviate batch |
| --reset | -r | FLAG | No | False | Clear existing project data before indexing |
| --verbose | -v | FLAG | No | False | Show detailed progress |

**Output** (text format):
```
Connecting to Weaviate at http://localhost:8080...
Schema validated. Classes: Project, CodeArtifact

Indexing project: com.example:my-app:1.0.0

Progress: [████████████████████] 2,438/2,438 artifacts (100%)
Elapsed: 00:02:30 | ETA: 00:00:00 | Rate: 975 artifacts/min

Summary:
  - Project records: 1 (created)
  - Artifact records: 2,438 (1,200 created, 1,238 updated)
  - Batches committed: 49
  - Duration: 2 minutes 30 seconds

Indexing complete. Project searchable in Weaviate.
```

**Output** (json format):
```json
{
  "project_id": "com.example:my-app:1.0.0",
  "projects_indexed": 1,
  "artifacts_created": 1200,
  "artifacts_updated": 1238,
  "batches_committed": 49,
  "duration_seconds": 150
}
```

**Exit Codes**:
- 0: Success
- 1: Fatal error (Weaviate unavailable, schema mismatch, etc.)
- 3: Project locked (another indexing in progress)

---

### 4. search

**Purpose**: Perform semantic search over indexed artifacts.

**Usage**:
```bash
codeindex search [OPTIONS] QUERY
```

**Options**:

| Option | Short | Type | Required | Default | Description |
|--------|-------|------|----------|---------|-------------|
| --project | -p | TEXT | No | None | Filter by specific project |
| --type | -t | TEXT | No | None | Filter by artifact type (java_source, etc.) |
| --layer | -l | TEXT | No | None | Filter by layer tag (backend, frontend, etc.) |
| --limit | -n | INT | No | 20 | Maximum results to return |
| --verbose | -v | FLAG | No | False | Show detailed metadata |

**Arguments**:
- QUERY: Natural language search query (required)

**Example**:
```bash
codeindex search "authentication logic" --project "com.example:my-app:1.0.0" --layer backend --limit 10
```

**Output** (text format):
```
Searching for: "authentication logic"
Filters: project=com.example:my-app:1.0.0, layer=backend

Results (10 of 47 matches):

1. [Score: 0.92] src/main/java/com/example/auth/AuthService.java
   Type: java_source | Layer: backend | Concern: security
   Summary: Handles user authentication using JWT tokens. Validates credentials
   against database and generates access tokens with expiration...

2. [Score: 0.88] src/main/java/com/example/auth/AuthFilter.java
   Type: java_source | Layer: backend | Concern: security
   Summary: Servlet filter that intercepts requests and validates JWT tokens
   from Authorization header. Rejects unauthenticated requests...

[... 8 more results ...]
```

**Output** (json format):
```json
{
  "query": "authentication logic",
  "filters": {
    "project": "com.example:my-app:1.0.0",
    "layer": "backend"
  },
  "total_matches": 47,
  "results": [
    {
      "id": "uuid-here",
      "project_id": "com.example:my-app:1.0.0",
      "relative_path": "src/main/java/com/example/auth/AuthService.java",
      "artifact_type": "java_source",
      "summary": "Handles user authentication...",
      "score": 0.92,
      "tags_layer": ["backend"],
      "tags_concerns": ["security"]
    }
  ]
}
```

**Exit Codes**:
- 0: Success (even if no results found)
- 1: Error (Weaviate unavailable, invalid query, etc.)

---

### 5. status

**Purpose**: Show indexed project statistics and system status.

**Usage**:
```bash
codeindex status [OPTIONS]
```

**Options**:

| Option | Short | Type | Required | Default | Description |
|--------|-------|------|----------|---------|-------------|
| --project | -p | TEXT | No | None | Show specific project details |
| --verbose | -v | FLAG | No | False | Show detailed breakdown |

**Output** (text format, no project filter):
```
Weaviate Status: Connected (http://localhost:8080)
Ollama Status: Connected (http://localhost:11434, model: gemma3:12b)

Indexed Projects: 3

com.example:my-app:1.0.0
  Files: 2,438 artifacts
  Last Indexed: 2025-12-12 10:45:30
  Types: java_source (1,200), jsp_view (450), xml_config (300), ...

com.example:my-lib:1.0.0
  Files: 1,180 artifacts
  Last Indexed: 2025-12-11 15:20:10
  Types: java_source (980), java_test (200)

com.example:my-web:2.0.0
  Files: 3,050 artifacts
  Last Indexed: 2025-12-10 09:30:00
  Types: java_source (800), jsp_view (1,100), js_script (900), ...

Total Artifacts: 6,668
```

**Output** (text format, with project filter):
```
Project: com.example:my-app:1.0.0
Status: Indexed
Last Updated: 2025-12-12 10:45:30

Statistics:
  Total Artifacts: 2,438
  Artifact Types:
    - java_source: 1,200 (49.2%)
    - jsp_view: 450 (18.5%)
    - xml_config: 300 (12.3%)
    - sql_query: 200 (8.2%)
    - properties_file: 150 (6.2%)
    - other: 138 (5.6%)

  Layers:
    - backend: 1,800 (73.9%)
    - frontend: 450 (18.5%)
    - persistence: 188 (7.7%)

  Frameworks:
    - Spring: 800 artifacts
    - iBATIS: 200 artifacts
    - JSP: 450 artifacts
    - JUnit: 180 artifacts
```

**Output** (json format):
```json
{
  "weaviate_status": "connected",
  "ollama_status": "connected",
  "projects": [
    {
      "project_id": "com.example:my-app:1.0.0",
      "artifact_count": 2438,
      "indexed_at": "2025-12-12T10:45:30Z",
      "artifact_types": {
        "java_source": 1200,
        "jsp_view": 450
      }
    }
  ],
  "total_artifacts": 6668
}
```

**Exit Codes**:
- 0: Success
- 1: Error (Weaviate unavailable)
- 2: No data indexed yet (with informative message)

---

## Environment Variables

Configuration via `.env` file or environment:

```bash
# Required
JAVA_SOURCE_DIR=/path/to/java/source

# Optional (with defaults)
WEAVIATE_URL=http://localhost:8080
OLLAMA_MODEL_NAME=gemma3:12b
OLLAMA_URL=http://localhost:11434
MAX_CONCURRENT_AI_CALLS=10
BATCH_SIZE=50
LOG_LEVEL=INFO
DRY_RUN=false
```

## Error Handling

All commands follow these conventions:

1. **Validation Errors**: Show clear message with suggested fix, exit code 1
2. **Service Unavailable**: Check health, show connection details, exit code 1
3. **Project Locked**: Show lock owner/time, suggest wait, exit code 3
4. **Empty Results**: Informative message with next steps, exit code 0 or 2
5. **Partial Failures**: Complete operation, log errors, summarize, exit code 0

## Progress Indicators

All long-running operations show:
- Progress bar with percentage
- Items processed / total
- Elapsed time
- Estimated time remaining
- Processing rate (items/minute or items/second)

Updated every 1 second or 100 items (whichever is sooner).

## Logging

Structured logging to stderr:
```
2025-12-12 10:30:00 [INFO] Starting discovery scan: /path/to/source
2025-12-12 10:30:05 [INFO] Found project: com.example:my-app:1.0.0
2025-12-12 10:30:10 [WARNING] Malformed POM: /path/to/source/broken/pom.xml
2025-12-12 10:30:15 [ERROR] Failed to parse file: IOException (see logs)
```

## Example Workflows

### Full Pipeline
```bash
# 1. Discover projects
codeindex discover --source-dir /path/to/source --output inventory.jsonl

# 2. Extract with AI
codeindex extract --inventory inventory.jsonl --output extracted/

# 3. Index to Weaviate
codeindex index --input extracted/

# 4. Check status
codeindex status

# 5. Search
codeindex search "database access logic" --layer persistence
```

### Single Project
```bash
# Filter all operations to one project
export PROJECT=com.example:my-app:1.0.0

codeindex discover --project $PROJECT
codeindex extract --project $PROJECT
codeindex index --project $PROJECT
codeindex status --project $PROJECT
```

### Re-index with Reset
```bash
# Clear existing data and re-index
codeindex index --project com.example:my-app:1.0.0 --reset --force
```
