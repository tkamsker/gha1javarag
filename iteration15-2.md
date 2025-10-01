# Iteration 15 — Consolidated Requirements (Weaviate-First)

**Purpose:** This document consolidates and de-duplicates requirements from earlier iterations to guide Cursor in generating a **Python application** that analyzes Java/JSP/GWT codebases, extracts metadata and requirements, and stores/searches them in **Weaviate**.  
**Key change:** All vector database references are standardized to **Weaviate**.  
**Primary constraint:** **Step 1 must read a directory set via `.env` variable `JAVA_SOURCE_DIR`** and iterate all files. **The first directory level represents the project name.**

---

## 0) High-Level Objectives

1. Traverse one or more Java/JSP/GWT repositories under `JAVA_SOURCE_DIR`, treating **each first-level subdirectory** as a distinct **project**.
2. Extract rich, structured metadata from source files (code, SQL, XML, JSP/HTML, JS, CSS, GWT UiBinder).
3. Chunk, vectorize, and **store in Weaviate** for semantic retrieval.
4. Generate consolidated JSON exports and human-readable requirements docs (Cursor-driven).
5. Provide optional modernization insights (architecture, business rules, and GWT → modern UI mapping).

---

## 1) Environment & Configuration

Use a `.env` file at repository root. Required/optional variables:

```

```bash
# =============================
# Core Paths
# =============================
# Mandatory: root directory containing first-level project folders
JAVA_SOURCE_DIR=/absolute/or/relative/path/to/source-root

# Where JSON catalogs, logs, and generated requirements are written
OUTPUT_DIR=./output

# =============================
# Weaviate (Vector DB)
# =============================
WEAVIATE_URL=http://localhost:8080
WEAVIATE_API_KEY=                             # leave empty if anonymous enabled
WEAVIATE_TIMEOUT=60                           # seconds
WEAVIATE_BATCH_SIZE=256                       # initial batch size; tune for throughput

# Choose embedding pipeline for Weaviate:
# - If using Weaviate text2vec-ollama:  EMBEDDING_PROVIDER=weaviate_ollama
# - If embedding in the client (OpenAI/Anthropic/Ollama HTTP): EMBEDDING_PROVIDER=client
EMBEDDING_PROVIDER=weaviate_ollama
EMBEDDING_MODEL=nomic-embed-text              # for text2vec-ollama; adjust to your local model

# =============================
# AI Provider Configuration
# =============================
# Switch between 'openai', 'ollama', or 'anthropic' for generation/summarization.
# (This affects summaries, requirements generation, and any LLM-assisted parsing.)
AI_PROVIDER=ollama

# ---- OpenAI ----
OPENAI_API_KEY=                               # e.g., sk-...  (do NOT commit to git)
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_API_TYPE=openai
OPENAI_API_VERSION=2024-02-15-preview
OPENAI_MODEL_NAME=gpt-4.1                     # used for summarization/requirements if AI_PROVIDER=openai
OPENAI_EMBED_MODEL=text-embedding-3-large     # only used when EMBEDDING_PROVIDER=client

# ---- Ollama (local) ----
# OLLAMA_BASE_URL=http://localhost:11434      # or your LAN host, e.g., http://192.168.0.50:11434
OLLAMA_MODEL_NAME=danielsheep/Qwen3-Coder-30B-A3B-Instruct-1M-Unsloth
OLLAMA_TIMEOUT=240                            # seconds
# If EMBEDDING_PROVIDER=client and you run a local HTTP embedding endpoint, set:
# LOCAL_EMBED_URL=http://localhost:11435/embed
# LOCAL_EMBED_MODEL=nomic-embed-text

# ---- Anthropic ----
ANTHROPIC_API_KEY=                            # do NOT commit
ANTHROPIC_API_BASE=https://api.anthropic.com
ANTHROPIC_MODEL_NAME=claude-3-5-sonnet-20240620
# Embeddings with Anthropic require a separate service; if using client-side embeddings,
# point to LOCAL_EMBED_URL/OPENAI_EMBED_MODEL accordingly.

# =============================
# Processing Controls
# =============================
MAX_FILE_BYTES=2000000                        # 2MB/file guardrail
INCLUDE_FILE_TYPES=.java,.jsp,.tsp,.xml,.html,.js,.sql,.properties,.json,.md,.css,.ui.xml,.gwt.xml
EXCLUDE_DIRS=.git,node_modules,build,out,target,dist,.idea,.vscode,.gradle

# =============================
# Rate Limiting / Runtime Mode
# =============================
# Options: production | development | test | emergency
RATE_LIMIT_ENV=production
```



**Weaviate deployment assumptions:**  
- Local single-node is acceptable for development. Production may use Docker Compose (Weaviate + **text2vec-ollama**/**generative-ollama**) or managed cloud.  
- Anonymous access may be enabled locally; secure with `WEAVIATE_API_KEY` for shared environments.

---

## 2) Input Model & Project Detection

**Project model:**  
- Let `JAVA_SOURCE_DIR` contain subdirectories: `projectA/`, `projectB/`, …  
- **Each first-level directory** under `JAVA_SOURCE_DIR` is a **project**.  
- Files directly under `JAVA_SOURCE_DIR` (without a parent dir) belong to a synthetic project named: `__root__`.

**Traversal rules:**  
- Recurse all subdirectories except those in `EXCLUDE_DIRS`.
- Process only files whose extensions are in `INCLUDE_FILE_TYPES`.
- Capture file size & skip if larger than `MAX_FILE_BYTES` (log a warning).

**Path normalization:**  
- Store canonical path with forward slashes.  
- Store `project_name` as the first-level folder (or `__root__`).

---

## 3) File Processing & Extraction

**Targets:** `.java`, `.jsp`, `.tsp`, `.xml` (incl. `web.xml`, config), `.html`, `.js`, `.sql`, `.properties`, `.json`, `.md`, `.css`, GWT: `.ui.xml`, `.gwt.xml`.

**Per file, extract/derive:**  
- **General:** `file_path`, `project_name`, `language`, `size_bytes`, `sha256`, `last_modified`  
- **Code metadata:** classes/interfaces, methods, imports, package, annotations, comments  
- **JSP/HTML/JS:** forms, endpoints, DOM structures, scripts, handlers, UI elements  
- **SQL/XML:** table/view definitions, fields, keys, constraints, queries, mappings  
- **GWT UiBinder / GWT Java:** widget hierarchy, `@UiField`, `@UiHandler`, `@UiTemplate`, navigation flows  
- **Business hints:** validation rules, feature flags, roles/permissions, domain entities  
- **Complexity metrics (approx.):** LoC, cyclomatic estimate, nesting heuristics  
- **Cross-links (when discoverable):** called methods, referenced tables, REST endpoints, servlets, navigation targets

> Implement light-weight static parsing; do not require full language servers. Favor regex/AST-lite approaches, then enrich with LLM where configured.

---

## 4) Chunking Strategy (Repository → Module → File → Class → Method)

Design for retrieval quality and large-context assembly:

1. **Repository/Project summaries:** ~50–100KB text per project (high-level readme-like synthesis).
2. **Module/Package chunks:** 20–50KB.
3. **File-level chunks:** 8–25KB.
4. **Class/Interface chunks:** 2–8KB.
5. **Method/Function chunks:** 0.5–2KB.
6. **UI/GWT chunks:** mirror templates and widget trees (2–8KB), plus **Navigation** chunks (5–15KB).

**Overlap:** 10–20% where helpful to preserve continuity.  
**Metadata on chunks (all required):** `file_path`, `project_name`, `chunk_kind`, `language`, `start_line`, `end_line`, `class_name?`, `function_name?`, `architectural_layer? (db/backend/ui)`, `business_domain?`, `complexity_score?`, `parent_refs[]`, `child_refs[]`.

---

## 5) Weaviate Collections (Schema)

Create the following **classes** (collections). Names can be adjusted, but keep the separation:

### 5.1 `JavaCodeChunks`
Core code + config chunks.
```json
{
  "class": "JavaCodeChunks",
  "description": "Code/config chunks with rich metadata",
  "vectorizer": "text2vec-ollama",
  "moduleConfig": {
    "text2vec-ollama": { "model": "${EMBEDDING_MODEL}" }
  },
  "properties": [
    {"name": "projectName", "dataType": ["text"]},
    {"name": "filePath", "dataType": ["text"]},
    {"name": "chunkKind", "dataType": ["text"]},
    {"name": "language", "dataType": ["text"]},
    {"name": "content", "dataType": ["text"]},
    {"name": "className", "dataType": ["text"]},
    {"name": "functionName", "dataType": ["text"]},
    {"name": "architecturalLayer", "dataType": ["text"]},
    {"name": "businessDomain", "dataType": ["text"]},
    {"name": "complexityScore", "dataType": ["number"]},
    {"name": "startLine", "dataType": ["int"]},
    {"name": "endLine", "dataType": ["int"]},
    {"name": "parentRefs", "dataType": ["text[]"]},
    {"name": "childRefs", "dataType": ["text[]"]},
    {"name": "repositoryContext", "dataType": ["text"]}
  ]
}
```

### 5.2 `DocumentationChunks`
Comments, README, markdown, docstrings.
```json
{
  "class": "DocumentationChunks",
  "vectorizer": "text2vec-ollama",
  "properties": [
    {"name": "projectName", "dataType": ["text"]},
    {"name": "filePath", "dataType": ["text"]},
    {"name": "content", "dataType": ["text"]},
    {"name": "language", "dataType": ["text"]},
    {"name": "section", "dataType": ["text"]}
  ]
}
```

### 5.3 `BusinessRules`
Validation, workflows, domain entities.
```json
{
  "class": "BusinessRules",
  "vectorizer": "text2vec-ollama",
  "properties": [
    {"name": "projectName", "dataType": ["text"]},
    {"name": "filePath", "dataType": ["text"]},
    {"name": "content", "dataType": ["text"]},
    {"name": "domainEntities", "dataType": ["text[]"]},
    {"name": "dataFlows", "dataType": ["text[]"]}
  ]
}
```

### 5.4 `IntegrationPoints`
APIs, DB interactions, external systems.
```json
{
  "class": "IntegrationPoints",
  "vectorizer": "text2vec-ollama",
  "properties": [
    {"name": "projectName", "dataType": ["text"]},
    {"name": "filePath", "dataType": ["text"]},
    {"name": "content", "dataType": ["text"]},
    {"name": "endpoint", "dataType": ["text"]},
    {"name": "protocol", "dataType": ["text"]},
    {"name": "databaseObjects", "dataType": ["text[]"]}
  ]
}
```

### 5.5 `UIComponents` (GWT & general UI)
```json
{
  "class": "UIComponents",
  "vectorizer": "text2vec-ollama",
  "properties": [
    {"name": "projectName", "dataType": ["text"]},
    {"name": "componentName", "dataType": ["text"]},
    {"name": "componentType", "dataType": ["text"]},
    {"name": "filePath", "dataType": ["text"]},
    {"name": "packageName", "dataType": ["text"]},
    {"name": "sourceCode", "dataType": ["text"]},
    {"name": "uiTemplate", "dataType": ["text"]},
    {"name": "gwtWidgets", "dataType": ["text[]"]},
    {"name": "businessDomains", "dataType": ["text[]"]},
    {"name": "userRoles", "dataType": ["text[]"]},
    {"name": "navigationTargets", "dataType": ["text[]"]},
    {"name": "eventHandlers", "dataType": ["text[]"]},
    {"name": "complexityScore", "dataType": ["int"]},
    {"name": "accessibilityScore", "dataType": ["int"]},
    {"name": "responsiveCapability", "dataType": ["boolean"]}
  ]
}
```

### 5.6 `NavigationFlows`
```json
{
  "class": "NavigationFlows",
  "vectorizer": "text2vec-ollama",
  "properties": [
    {"name": "projectName", "dataType": ["text"]},
    {"name": "flowName", "dataType": ["text"]},
    {"name": "flowDescription", "dataType": ["text"]},
    {"name": "sourceComponent", "dataType": ["text"]},
    {"name": "targetComponent", "dataType": ["text"]},
    {"name": "transitionTrigger", "dataType": ["text"]},
    {"name": "userRole", "dataType": ["text"]},
    {"name": "businessProcess", "dataType": ["text"]}
  ]
}
```

> **Note:** If Weaviate Ollama modules aren’t available, set `EMBEDDING_PROVIDER=openai` and vectorize client-side before upsert (store embeddings as `vector` using the Python client).

---

## 6) Processing Pipeline (Step-by-Step)

### Step 1 — Discovery & Index

> **AI provider switch:** Runtime chooses summarization/generation backend via `AI_PROVIDER` (`openai|ollama|anthropic`). Embedding pipeline is chosen independently via `EMBEDDING_PROVIDER` (`weaviate_ollama|client`).
1. Load `.env`. Validate `JAVA_SOURCE_DIR`, else exit with actionable error.
2. Build project list from first-level directories; include `__root__` if files exist directly in root.
3. Walk each project; filter with `EXCLUDE_DIRS` & `INCLUDE_FILE_TYPES`.
4. For each file:
   - Collect file stats and fingerprint.
   - Extract raw text with safe decoding (utf-8 → fallback).
   - Produce **structured metadata** (Section 3).
   - **Chunk** per Section 4; attach metadata to each chunk.
   - Vectorize chunks (provider per `.env`), **upsert** into Weaviate class by kind:
     - code/config → `JavaCodeChunks`
     - docs/comments → `DocumentationChunks`
     - business rules → `BusinessRules`
     - integrations → `IntegrationPoints`
     - UI components → `UIComponents`
     - navigation flows → `NavigationFlows`

5. Write per-project JSON summary: `OUTPUT_DIR/projects/{project}.summary.json`.
6. Write global catalog: `OUTPUT_DIR/catalog.index.json` (projects, files, stats).

### Step 2 — Requirements Generation
1. Load consolidated project JSON (from Step 1).
2. Group by **architectural layers**: Database, Backend, Presentation/UI.
3. For each group, generate a requirements doc using the template below (Cursor prompt rules).
4. Cross-link dependencies (DB↔Backend↔UI) and produce modernization hints (optional).  
5. Output: `OUTPUT_DIR/requirements/{project}/…md` and a master `OUTPUT_DIR/requirements/_master.md`.

**Requirements Template (for each logical section):**
```markdown
# Requirements — <Section Name>

## 1. Overview
<Brief purpose within the application>

## 2. Components
- <list of classes/files/directories>

## 3. Functionality
- **Main Features:** <bullets>
- **Inputs/Outputs:** <forms, endpoints, tables>
- **Key Methods/Functions:** <list>

## 4. Dependencies
- <other sections or external systems>

## 5. Notes
- <legacy code, known issues, business rule nuances>
```

---

## 7) Error Handling & Logging

- Log JSON lines (`.jsonl`) to `OUTPUT_DIR/logs/app.log.jsonl` with fields: `ts`, `level`, `event`, `file`, `detail`, `exception?`.
- Continue on file-level errors; record `status=failed` with reason.
- On Weaviate failures:
  - Retry with exponential backoff (configurable).
  - If batch write fails, split to smaller batches; persist dead-letter file `OUTPUT_DIR/logs/bad_upserts.jsonl`.
- Emit a final run report: processed counts, failures, skipped, average upsert latency.

---

## 8) Performance Expectations

- Batch upserts with `WEAVIATE_BATCH_SIZE` (start at 256, tune).
- Parallel file parsing (CPU-bound) with bounded workers; preserve write ordering per project.
- Avoid embedding duplicate chunks (hash content); reuse vectors via a de-dup map.
- Target end-to-end pipeline: handle **10k+ files** within acceptable time on a modern workstation.

---

## 9) Testing & Acceptance Criteria

**Unit tests:** parsers (Java/JSP/XML/GWT), chunker, metadata validators.  
**Integration tests:** Weaviate upsert/query, batch behavior, retry paths.  
**Golden tests:** known repositories with expected counts & sample queries.

**Acceptance:**  
- Finds all first-level projects and indexes >95% eligible files.  
- Stores chunks in correct Weaviate classes with required metadata fields.  
- JSON catalogs exist and are valid (`catalog.index.json`, per-project summaries).  
- Requirements docs generated per template with cross-links between layers.  
- Clear logs and zero unhandled exceptions.

---

## 10) Python Package Layout (Suggested)

```
src/
  env_loader.py
  discovery.py
  parsers/
    __init__.py
    java_parser.py
    jsp_parser.py
    xml_sql_parser.py
    html_js_parser.py
    gwt_parser.py
  chunking.py
  metadata.py
  weaviate_client.py
  upsert.py
  reporting.py
  requirements_gen/
    __init__.py
    template.md
    generator.py
  cli.py
tests/
  unit/
  integration/
  golden/
scripts/
  run_index.py
  run_requirements.py
```

**CLI examples:**
```bash
python -m src.cli index        # runs Step 1
python -m src.cli requirements # runs Step 2
```

---

## 11) Query Examples (Weaviate)

- **Find classes touching a specific table:**
```graphql
{
  Get {
    IntegrationPoints(
      where: {
        operator: ContainsAny
        path: ["databaseObjects"]
        valueTextArray: ["CUSTOMER","ORDER"]
      }
    ){
      projectName filePath content endpoint protocol databaseObjects
    }
  }
}
```

- **Top-relevant code chunks for 'address validation':**
```graphql
{
  Get {
    JavaCodeChunks(nearText: { concepts: ["address validation"] }, limit: 10){
      projectName filePath className functionName startLine endLine content
    }
  }
}
```

---

## 12) Cursor Project Rules (Recommendation)

- Place **short, targeted MDC rules** in `.cursor/rules/*.mdc` to guide LLM: naming, style, chunk sizes, metadata fields, Weaviate class routing.
- Keep prompts grounded with **examples** (from `OUTPUT_DIR/projects/*.summary.json`).  
- Maintain an **Appendix** with representative chunks to ground drafting.  

---

## 13) Modernization Insights (Optional)

- Detect legacy JSP/GWT patterns; emit modernization suggestions (e.g., React/Vite + REST/GraphQL; accessibility fixes; performance).  
- Produce **NavigationFlows** from GWT UiBinder + handlers; recommend routing in target frameworks.  

---

## 14) Security & Privacy

- Do not exfiltrate source code; keep processing local by default.  
- If using external APIs (OpenAI), allow **explicit opt-in** via `.env` and redact secrets from logs.  

---

## 15) Deliverables

1. Running CLI with **Step 1** (index) and **Step 2** (requirements).  
2. Weaviate schema creation scripts and idempotent migration.  
3. JSON catalogs and per-project summaries in `OUTPUT_DIR`.  
4. Requirements markdown files grouped by layer and project.  
5. Test suite & minimal developer docs (`README.md`).

---

**End of Iteration 15 Requirements**
