# CLI Interface Contract: PRD Document Generation

**Feature**: 002-prd-document-generation
**Date**: 2025-12-14
**Phase**: Phase 1 - Contracts

## Overview

This document defines the command-line interface contract for the `codeindex prd` command, which generates Product Requirements Documents from indexed codebase artifacts. The interface supports layer-specific analysis (database, services, frontend) or full PRD generation with comprehensive options for customization and incremental processing.

## Command Structure

```bash
codeindex prd [OPTIONS] [LAYER]
```

## Arguments

### Positional Arguments

| Argument | Required | Description | Valid Values |
|----------|----------|-------------|--------------|
| LAYER | No | Specific layer to analyze; if omitted, runs full analysis | `database`, `services`, `frontend`, `full` |

**Default**: `full` (analyze all layers and generate master PRD)

## Options

### General Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--project` | `-p` | string | None | Project name/ID to analyze (filters CodeArtifacts in Weaviate) |
| `--source-dir` | `-s` | path | `$JAVA_SOURCE_DIR` | Root directory of source code (overrides .env) |
| `--output-dir` | `-o` | path | `./output` | Output directory for generated PRD documents |
| `--force-refresh` | `-f` | flag | false | Re-analyze all files even if unchanged (ignore visit log) |
| `--parallel` | `-j` | integer | 10 | Number of parallel LLM analysis tasks |
| `--verbose` | `-v` | flag | false | Enable verbose logging (DEBUG level) |
| `--quiet` | `-q` | flag | false | Suppress progress output (only errors/warnings) |
| `--help` | `-h` | flag | - | Display help message and exit |

### Layer-Specific Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--skip-database` | flag | false | Skip database layer analysis (only with `full` layer) |
| `--skip-services` | flag | false | Skip service layer analysis (only with `full` layer) |
| `--skip-frontend` | flag | false | Skip frontend layer analysis (only with `full` layer) |

### LLM Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--llm-timeout` | integer | 120 | Timeout for each LLM call in seconds |
| `--llm-retries` | integer | 3 | Maximum retry attempts for failed LLM calls |
| `--llm-model` | string | `$OLLAMA_MODEL_NAME` | Ollama model to use (e.g., gemma3:12b) |

### Output Format Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--format` | string | `markdown` | Output format for PRD documents |
| `--include-html` | flag | false | Also generate HTML versions of markdown files |
| `--include-diagrams` | flag | false | Generate Mermaid diagrams for ERD and architecture |

**Valid `--format` values**: `markdown`, `json`, `both`

### Filtering Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--domain-filter` | string | None | Only analyze entities in specified domain (e.g., `auth`, `billing`) |
| `--include-tests` | flag | false | Include test files in analysis |
| `--exclude-generated` | flag | true | Exclude auto-generated code from analysis |

### Progress Reporting Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--progress-interval` | integer | 10 | Progress report frequency in seconds |
| `--show-current-file` | flag | true | Display currently analyzed file in progress output |

## Exit Codes

| Code | Name | Description |
|------|------|-------------|
| 0 | SUCCESS | PRD generation completed successfully |
| 1 | GENERAL_ERROR | Unspecified error occurred |
| 2 | INVALID_ARGUMENTS | Invalid command-line arguments provided |
| 3 | SOURCE_DIR_NOT_FOUND | Specified source directory does not exist or is not accessible |
| 4 | PROJECT_NOT_FOUND | Specified project not found in Weaviate (no indexed artifacts) |
| 5 | OUTPUT_DIR_ERROR | Cannot create or write to output directory |
| 6 | WEAVIATE_CONNECTION_ERROR | Cannot connect to Weaviate service |
| 7 | OLLAMA_CONNECTION_ERROR | Cannot connect to Ollama service |
| 8 | LLM_ANALYSIS_FAILED | LLM analysis failed for critical files after all retries |
| 9 | PARTIAL_SUCCESS | Some layers completed but others failed (warning exit) |
| 10 | NO_ARTIFACTS_FOUND | No artifacts found in specified project or source directory |

## Usage Examples

### Example 1: Generate Full PRD for a Project

```bash
codeindex prd --project myapp --output-dir ./docs/myapp-prd
```

**Expected Behavior**:
- Analyzes all layers (database, services, frontend)
- Uses project filter `myapp` to query Weaviate for CodeArtifacts
- Generates complete PRD in `./docs/myapp-prd/`
- Creates index files at each layer
- Generates master PRD with cross-references

**Exit Code**: 0 on success, appropriate error code on failure

---

### Example 2: Analyze Only Database Layer

```bash
codeindex prd database --project myapp
```

**Expected Behavior**:
- Analyzes only database layer (DAOs, entities, SQL files)
- Generates `./output/database/` with entities and index
- Generates `./output/prd/database_prd.md`
- Does NOT analyze services or frontend
- Visit log tracks only database layer files

**Exit Code**: 0 on success

---

### Example 3: Analyze Services Layer with Custom LLM Settings

```bash
codeindex prd services --llm-timeout 180 --llm-retries 5 --parallel 5
```

**Expected Behavior**:
- Analyzes only service layer (service classes, controllers, REST endpoints)
- Uses 180-second timeout for LLM calls
- Retries up to 5 times on failure
- Runs 5 parallel analysis tasks
- Generates `./output/services/` with definitions, endpoints, and index

**Exit Code**: 0 on success

---

### Example 4: Full PRD with HTML Output and Diagrams

```bash
codeindex prd full --include-html --include-diagrams --project myapp
```

**Expected Behavior**:
- Analyzes all layers
- Generates markdown PRD documents
- Also generates HTML versions of all markdown files
- Includes Mermaid diagrams for database ER diagram and architecture overview
- Output includes both `.md` and `.html` files

**Exit Code**: 0 on success

---

### Example 5: Force Refresh All Files (Ignore Visit Log)

```bash
codeindex prd --force-refresh --project myapp
```

**Expected Behavior**:
- Ignores `.visit_log.jsonl` (re-analyzes all files regardless of content hash)
- Useful after LLM prompt changes or model upgrades
- Updates visit log with new timestamps and analysis results
- Regenerates all entity JSON files and PRD markdown

**Exit Code**: 0 on success

---

### Example 6: Analyze Specific Domain Only

```bash
codeindex prd --domain-filter auth --project myapp
```

**Expected Behavior**:
- Analyzes all layers but filters entities by domain `auth`
- Only processes files/entities related to authentication/authorization
- Generates filtered PRD focused on auth subsystem
- Useful for subsystem-specific documentation

**Exit Code**: 0 on success

---

### Example 7: Analyze with Custom Source Directory

```bash
codeindex prd --source-dir /path/to/legacy/app --output-dir ./legacy-prd
```

**Expected Behavior**:
- Overrides `JAVA_SOURCE_DIR` from .env
- Scans `/path/to/legacy/app` for source files
- Queries Weaviate for artifacts matching source paths
- Generates PRD in `./legacy-prd/`

**Exit Code**: 3 if source directory not found, 0 on success

---

### Example 8: Quiet Mode for Automation

```bash
codeindex prd --quiet --project myapp > /dev/null 2>&1
echo $?
```

**Expected Behavior**:
- Suppresses all progress output
- Only prints errors or warnings to stderr
- Useful for CI/CD pipelines or scheduled jobs
- Exit code indicates success/failure

**Exit Code**: 0 on success, error code otherwise

---

### Example 9: Skip Frontend Layer

```bash
codeindex prd full --skip-frontend --project myapp
```

**Expected Behavior**:
- Analyzes database and services layers only
- Skips frontend analysis entirely
- Generates database_prd.md and service_prd.md
- Master PRD notes that frontend analysis was skipped
- Useful for backend-only systems or APIs

**Exit Code**: 0 on success

---

### Example 10: Generate JSON Output for Tooling

```bash
codeindex prd --format json --project myapp
```

**Expected Behavior**:
- Generates JSON output files instead of (or in addition to) markdown
- Entity files remain JSON (no change)
- PRD sections generated as structured JSON (PRDSection objects)
- Useful for post-processing or integration with other tools

**Exit Code**: 0 on success

## Output Structure

### Standard Output (stdout)

Progress messages when `--quiet` is not set:

```
[INFO] Starting PRD generation for project: myapp
[INFO] Output directory: ./output
[INFO] Analyzing database layer...
[PROGRESS] Database: 15/47 files processed (31.9%), current: UserDAO.java, ETA: 2m 15s
[PROGRESS] Database: 30/47 files processed (63.8%), current: BillingDAO.java, ETA: 1m 8s
[INFO] Database layer complete: 47 entities, 23 business rules
[INFO] Analyzing service layer...
[PROGRESS] Services: 8/25 services processed (32.0%), current: UserService.java, ETA: 1m 45s
[INFO] Service layer complete: 25 services, 43 endpoints
[INFO] Analyzing frontend layer...
[PROGRESS] Frontend: 12/38 forms processed (31.6%), current: UserRegistration.jsp, ETA: 3m 12s
[INFO] Frontend layer complete: 38 forms, 64 components, 12 navigation flows
[INFO] Generating PRD documents...
[INFO] PRD generation complete!
[INFO] Output location: ./output/prd/master_prd.md
[INFO] Total analysis time: 8m 42s
[INFO] Files processed: 110, skipped: 23 (unchanged), failed: 0
```

### Error Output (stderr)

Error messages when failures occur:

```
[ERROR] Cannot connect to Weaviate at http://localhost:8080
[ERROR] Failed to analyze file: src/main/java/com/example/UserDAO.java (timeout after 120s)
[WARNING] No artifacts found for project 'myapp' in Weaviate; did you run 'codeindex index'?
[WARNING] LLM analysis failed for 3 files; PRD may be incomplete
```

### Generated Files

#### Full Analysis (all layers)

```
output/
├── .visit_log.jsonl
├── database/
│   ├── index.md
│   └── entities/
│       ├── user.json
│       ├── invoice.json
│       └── ...
├── services/
│   ├── index.md
│   ├── definitions/
│   │   └── UserService.json
│   └── endpoints/
│       └── POST_api_user_create.json
├── frontend/
│   ├── index.md
│   ├── forms/
│   │   └── user_registration.json
│   ├── components/
│   │   └── UserListView.json
│   └── navigation/
│       └── user_registration_flow.json
├── business_rules/
│   ├── index.md
│   └── BR_001_email_validation.json
└── prd/
    ├── index.md
    ├── master_prd.md
    ├── database_prd.md
    ├── service_prd.md
    ├── frontend_prd.md
    └── cross_references.md
```

#### Layer-Specific Analysis (e.g., `database`)

```
output/
├── .visit_log.jsonl
├── database/
│   ├── index.md
│   └── entities/
│       └── ...
├── business_rules/
│   ├── index.md
│   └── BR_*.json (database-level rules only)
└── prd/
    └── database_prd.md
```

## Visit Log Format

The `.visit_log.jsonl` file tracks analyzed files to enable incremental processing.

### Format

JSON Lines (one JSON object per line):

```jsonl
{"file_path": "/path/to/UserDAO.java", "timestamp": "2025-12-14T10:30:15Z", "status": "success", "content_hash": "a1b2c3d4e5f6...", "layer": "database", "analysis_type": "dao_extraction", "duration_seconds": 2.34, "extracted_entities": ["User"]}
{"file_path": "/path/to/UserService.java", "timestamp": "2025-12-14T10:32:48Z", "status": "success", "content_hash": "f6e5d4c3b2a1...", "layer": "service", "analysis_type": "service_extraction", "duration_seconds": 3.12, "extracted_entities": ["UserService"]}
{"file_path": "/path/to/UserForm.jsp", "timestamp": "2025-12-14T10:35:22Z", "status": "failed", "content_hash": "1234567890ab...", "layer": "frontend", "analysis_type": "form_parsing", "error_message": "LLM timeout after 120s", "duration_seconds": 120.0}
```

### Schema

See `contracts/output-formats.md` for detailed `.visit_log.jsonl` schema.

## Environment Variables

The command respects these environment variables (can be overridden by CLI options):

| Variable | CLI Override | Default | Description |
|----------|--------------|---------|-------------|
| `JAVA_SOURCE_DIR` | `--source-dir` | - | Root source directory (required) |
| `OUTPUT_DIR` | `--output-dir` | `./output` | Output directory |
| `OLLAMA_MODEL_NAME` | `--llm-model` | `gemma3:12b` | Ollama model name |
| `MAX_CONCURRENT_AI_CALLS` | `--parallel` | 10 | Parallel LLM tasks |
| `WEAVIATE_URL` | - | `http://localhost:8080` | Weaviate endpoint |
| `OLLAMA_URL` | - | `http://localhost:11434` | Ollama endpoint |
| `LOG_LEVEL` | `--verbose` | `INFO` | Logging level |

## Integration with Feature 001

### Dependencies

The `codeindex prd` command **depends on** Feature 001 having run successfully:

1. **Discovery** (`codeindex discover`) - Source files must be discovered
2. **Extraction** (`codeindex extract`) - CodeArtifacts must be extracted
3. **Indexing** (`codeindex index`) - Artifacts must be indexed in Weaviate

### Artifact Retrieval

The PRD command queries Weaviate for CodeArtifacts:

- **Project Filter**: `project_id == <project>`
- **Type Filter**: Filters by `artifact_type` for layer-specific analysis
  - Database: `java_source` (DAOs, entities), `orm_mapping`, `ibatis_mapping`, `sql_schema`
  - Services: `java_source` (services, controllers)
  - Frontend: `jsp_view`, `html_template`, `gwt_module`, `gwt_ui_binder`, `js_script`

### Reusing Indexed Data

- The command reads `CodeArtifact.summary` for LLM-generated summaries
- Uses `CodeArtifact.entities` for extracted entities
- Uses `CodeArtifact.tags_layer`, `tags_domain`, `tags_concerns` for filtering
- Re-visits source files (via `relative_path`) for deep analysis beyond initial extraction

## Error Handling

### Graceful Degradation

- If LLM analysis fails for some files, continue with others and report partial success
- If an entire layer fails, still attempt other layers
- Exit code 9 (PARTIAL_SUCCESS) if some but not all layers complete

### Retry Logic

- LLM calls retry up to `--llm-retries` times with exponential backoff
- Exponential backoff: 2^n seconds (1s, 2s, 4s, 8s, ...)
- After max retries, mark file as `failed` in visit log and continue

### User-Facing Error Messages

- Clear error messages with actionable guidance
- Example: "Cannot connect to Weaviate at http://localhost:8080. Run './docker-weaviate.sh status' to check service."
- Include exit codes in error messages for scripting

## Performance Considerations

### Parallelization

- Default 10 parallel LLM calls via `--parallel` option
- Adjust based on Ollama instance capacity and system resources
- Each parallel task processes one file at a time

### Progress Reporting

- Progress updates every 10 seconds by default (configurable via `--progress-interval`)
- Reports: current layer, files processed, percentage, current file, ETA
- ETA calculated from average processing time per file

### Incremental Processing

- Visit log enables skipping unchanged files (content_hash comparison)
- `--force-refresh` disables this optimization
- Useful for iterative documentation improvements without re-analyzing entire codebase

## Validation

### Pre-Execution Validation

Before starting analysis, validate:

1. Source directory exists and is readable
2. Output directory can be created/written
3. Weaviate is accessible (HTTP 200 from `/v1/meta`)
4. Ollama is accessible (HTTP 200 from `/api/tags`)
5. If `--project` specified, at least one CodeArtifact exists in Weaviate for that project

### Post-Execution Validation

After analysis, verify:

1. All expected output files were created
2. Visit log is valid JSON Lines
3. Generated markdown is well-formed
4. Cross-references in PRD sections point to existing entities

## Future Enhancements (Out of Scope for Phase 1)

- `--watch` mode for continuous documentation updates
- `--compare` option to diff two PRD versions
- `--export-html` with custom CSS themes
- Integration with Confluence/Notion/GitHub Wikis
- Real-time progress via WebSocket or SSE
- `--incremental-layer` to re-analyze only one layer without full pipeline

## Compatibility

- **Python Version**: 3.8+
- **Operating Systems**: macOS, Linux (Ubuntu), Windows (WSL)
- **Required Services**: Weaviate, Ollama
- **Optional Services**: None

## Testing the CLI

### Unit Tests

```bash
pytest tests/unit/test_prd_cli.py
```

### Integration Tests

```bash
pytest tests/integration/test_prd_command.py
```

### End-to-End Tests

```bash
pytest tests/e2e/test_full_prd_generation.py
```

## See Also

- `contracts/output-formats.md` - Output file format specifications
- `contracts/llm-contracts.md` - LLM prompt/response contracts
- `quickstart.md` - Getting started guide
- `data-model.md` - Entity definitions
