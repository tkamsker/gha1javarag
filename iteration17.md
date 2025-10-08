# iteration17.md — PRD: Refactor “Java/JSP → PRD” Pipeline (Ollama + Weaviate, .env-driven)

**Owner:** Thomas Neusser
**Date:** 2025-10-08
**Status:** Draft for implementation in Cursor
**Goal:** Refactor the local, offline reverse-engineering pipeline to reliably turn a **Java/JSP + iBATIS** codebase into a **PRD auto-draft** using **Ollama** (LLM + embeddings) and **Weaviate** (vector DB), fully configured via **.env**. Support multi-project runs by scanning `JAVA_SOURCE_DIR` and deriving the project name deterministically.

---

## 0) Executive Summary

We will:

* Keep everything **local**: Ollama for LLM + embeddings; Weaviate in Docker with **vectorizer:none**.
* Drive configuration from `.env` (no hard-coded constants).
* Normalize **project discovery** and **iteration over subfolders** under `JAVA_SOURCE_DIR`.
* Extract artifacts (iBATIS mappers, DAO calls, JSP forms, DB schema), create **traceable chunks**, embed with Ollama, index in Weaviate, and synthesize **PRD drafts** with FR/AC/NFR + trace back to files and statementIds.

Deliverables include a CLI (`reveng`) to run: `extract → index → prd`, and a Markdown PRD per project in `out/prd_<project>.md`.

---

## 1) Scope

### In scope

* Python-first implementation (avoid Java toolchains).
* iBATIS/MyBatis mapper parsing, DAO usage discovery, JSP form parsing, DB schema introspection.
* Weaviate schema & indexing (vectorizer:none) with **explicit vectors** from Ollama embeddings.
* Crew-style prompts to synthesize **Flows**, **Functional Requirements**, **Acceptance Criteria**, **NFRs**.
* Project discovery from `JAVA_SOURCE_DIR` with a configurable naming strategy.
* Deterministic outputs (low-temperature) and per-feature traceability.

### Out of scope (iteration17)

* UI/web dashboard.
* Runtime tracing/agents on the Java app.
* Full migration/upgrade advice for the Java code (separate document).

---

## 2) Environment & Configuration

Create `.env` (commit `.env.example` only):

```ini
# Paths & project discovery
JAVA_SOURCE_DIR=/abs/path/to/workspace
PROJECT_NAME_STRATEGY=FIRST_SUBDIR   # FIRST_SUBDIR | BASENAME | ENV_VALUE
PROJECT_NAME=                        # used only if strategy=ENV_VALUE
PROJECT_INCLUDE_GLOBS=**/*.java,**/*.jsp,**/*.jspf,**/*.xml
PROJECT_EXCLUDE_GLOBS=**/target/**,**/.git/**,**/node_modules/**

# Ollama (local)
OLLAMA_BASE=http://127.0.0.1:11434
OLLAMA_MODEL_NAME=qwen2.5:14b-instruct
OLLAMA_EMBED_MODEL_NAME=nomic-embed-text

# Weaviate (local in Docker)
WEAVIATE_URL=http://127.0.0.1:8080
WEAVIATE_API_KEY=
WEAVIATE_TENANT=default

# Database (optional)
DB_URL=postgresql+psycopg2://user:pass@localhost:5432/appdb
DB_SCHEMA=public

# Chunking / retrieval
CHUNK_MAX_TOKENS=800
RETRIEVAL_TOP_K=12

# Output
OUTPUT_DIR=./out
```

**Project naming rule**

* `FIRST_SUBDIR`: lexicographically first directory under `JAVA_SOURCE_DIR`.
* `BASENAME`: basename of `JAVA_SOURCE_DIR`.
* `ENV_VALUE`: use `PROJECT_NAME` verbatim.
  The pipeline must support iterating over **all** direct subdirectories as separate projects (`--all-projects`).

---

## 3) Architecture (refactored)

```
src/
  config/         # .env loader & validation
  discover/       # derive project(s) from JAVA_SOURCE_DIR
  extract/        # ibatis_xml.py, java_calls.py, jsp_forms.py, db_schema.py
  chunk/          # build_chunks.py (artifact -> chunk text + metadata)
  embed/          # ollama_embed.py
  store/          # weaviate_client.py (vectorizer:none, explicit vectors)
  retrieve/       # search.py (semantic + filters)
  synth/          # prompts.py, prd_markdown.py (compose PRD)
  cli.py          # Typer/Click CLI
data/
  build/          # intermediate JSONs
out/
  features/       # per-feature md
  prd_<project>.md
  erd.puml / erd.png
```

**Key decision:** Use Weaviate **vectorizer:none** and push vectors explicitly from Ollama embeddings. This keeps everything local and model-agnostic.

---

## 4) Weaviate Schema

All classes have `vectorizer: "none"` and will receive an explicit `vector`.

**Common properties for all classes**

* `project` (string), `path` (string), `lineStart` (int), `lineEnd` (int),
* `namespace` (string), `statementId` (string), `tables` (string[]),
* `text` (string), `meta` (text JSON), `createdAt` (date).

**Classes**

1. `IbatisStatement`

   * `verb` (string: SELECT/INSERT/UPDATE/DELETE)
   * `parameterType` (string)
   * `resultTypeOrMap` (string)
   * `dynamic` (boolean)
   * `rawSql` (text)
   * `file` (string)
2. `DaoCall`

   * `methodName` (string)
   * `callKind` (string: selectList/selectOne/insert/update/delete)
   * `file` (string)
3. `JspForm`

   * `jspPath` (string)
   * `action` (string)
   * `method` (string)
   * `fieldsJson` (text)
   * `validationsJson` (text)
4. `DbTable`

   * `tableName` (string)
   * `columnsJson` (text)
   * `pkJson` (text)
   * `fkJson` (text)
   * `indexesJson` (text)
5. `Flow` (synthesized)

   * `title` (string)
   * `summary` (text)
   * `stepsJson` (text)
   * `reads` (string[])
   * `writes` (string[])
   * `traceJson` (text)
6. `Requirement` (synthesized)

   * `reqId` (string)
   * `kind` (string: FR|NFR|AC)
   * `title` (string)
   * `body` (text)
   * `priority` (string: MUST|SHOULD|CAN)
   * `traceJson` (text)

**Schema acceptance**

* CLI `reveng schema --ensure` creates/updates the above without data loss.

---

## 5) Extraction (inputs → artifacts)

**Inputs scanned**

* iBATIS/MyBatis: `SqlMapConfig.xml`, `*.xml` mappers (`<mapper>` or `<sqlMap>`).
* Java DAOs/Controllers: `.java` for `queryForList/queryForObject/selectList/selectOne/insert/update/delete`.
* JSP/JSF: `.jsp`, `.jspf` for `<form>`, input fields, validations.
* DB schema (optional): via SQLAlchemy Inspector.

**Outputs (JSON in `data/build/`)**

* `ibatis_index.json`: namespace, statementId, verb, parameter/result types, dynamic, tables[], rawSql, file.
* `dao_calls.json`: file, methodName, callKind, line, statementId.
* `jsp_forms.json`: jspPath, action, method, fieldsJson, validationsJson.
* `schema.json`: tables, columns, PK/FK, indexes.

**Acceptance**

* For a sample project, extractor counts are non-zero; iBATIS/DAO pairs resolve for common flows.

---

## 6) Chunking & Embedding

**Chunking rules**

* One chunk per iBATIS statement (preferred).
* Additional chunks for DAO callsites and JSP forms.
* Each chunk `text` starts with a readable header, then the source content:

```
[IbatisStatement] Order.insert (INSERT)
tables: orders
SQL:
INSERT INTO orders (...) VALUES (...);
```

**Embedding**

* Use `OLLAMA_EMBED_MODEL_NAME` to produce vectors.
* Store vectors alongside objects in Weaviate (explicit vectors).

**Acceptance**

* Indexing a medium project yields ≥ 1,000 chunks without errors.
* Similarity search for `"Order insert"` finds the `IbatisStatement` and related `DaoCall` + `JspForm`.

---

## 7) Retrieval & Synthesis

**Retrieval**

* Semantic search across `IbatisStatement`, `DaoCall`, `JspForm` filtered by `project`.
* `RETRIEVAL_TOP_K` default 12 (configurable).

**Synthesis steps (Ollama: `OLLAMA_MODEL_NAME`, temp 0.1–0.2)**

1. **Flow synthesis**
   Input: retrieved chunks (statements+DAO+JSP) for a namespace/feature candidate
   Output: `Flow` object (title, summary, steps, reads/writes, traceJson).
2. **Requirements synthesis**
   Input: Flow
   Output: FR list (numbered), ACs (Gherkin), inferred NFRs (caching, transactional, performance).
3. **PRD composition**
   Group related flows into features; write `out/features/*.md` and `out/prd_<project>.md`.

**Traceability rules**

* Every FR and AC includes **statementIds**, **files:lines**, **tables** when available.

---

## 8) CLI (developer workflow)

```
reveng init                   # check env, connectivity
reveng schema --ensure        # create/upgrade Weaviate classes
reveng extract [--project auto|name|--all-projects]
reveng index   [--project name]
reveng search  --q "Order insert" [--project name]
reveng prd     [--project name]
```

**Makefile shortcuts**

* `make all` → `extract → index → prd`
* `make clean` → remove `data/build` and `out` (keep Weaviate)

---

## 9) Milestones & Acceptance Criteria

### M1 — Config, Discovery, Schema (2–3 dev-days)

* `.env` loader with validation (missing keys → helpful error).
* Project discovery (FIRST_SUBDIR/BASENAME/ENV_VALUE) and `--all-projects`.
* Weaviate schema bootstrap (idempotent).
  **Acceptance:** `reveng schema --ensure` succeeds; `reveng init` prints health & classes.

### M2 — Extractors (2–4 dev-days)

* Robust iBATIS/MyBatis XML parsing (namespace, statements, resultMaps, dynamic tags).
* DAO callsite detection via `javalang`.
* JSP form parsing (action, method, fields, required/pattern).
* Optional DB schema via SQLAlchemy inspector.
  **Acceptance:** JSONs generated with non-zero counts; spot-check a statementId links to a DAO call and a JSP action.

### M3 — Indexing (1–2 dev-days)

* Chunk builder with token caps and readable headers.
* Ollama embedding; Weaviate batch upsert with explicit vectors; retries/backoff.
  **Acceptance:** Weaviate shows objects for project; `reveng search` returns sensible results.

### M4 — Synthesis & PRD (2–4 dev-days)

* Retrieval assembly per feature candidate (namespace + common verbs).
* Flow → FR/AC/NFR prompts; write per-feature and master PRD.
* Low temperature; deterministic formatting.
  **Acceptance:** `out/prd_<project>.md` contains ≥ 5 features with FRs + ACs, each with traceability blocks.

### M5 — QA & DX (1–2 dev-days)

* Tiny fixture repo tests; smoke tests in CI.
* `--debug` mode prints retrieved chunk IDs & sources per feature.
* README quickstart; `.cursor` task hints.
  **Acceptance:** New dev can run end-to-end in ≤ 10 minutes on a clean machine.

---

## 10) Data Contracts (object shapes)

### `IbatisStatement` (example)

```json
{
  "project": "shop-core",
  "namespace": "Order",
  "statementId": "insert",
  "verb": "INSERT",
  "parameterType": "com.app.Order",
  "resultTypeOrMap": null,
  "dynamic": false,
  "tables": ["orders"],
  "rawSql": "INSERT INTO orders (...) VALUES (...);",
  "file": "src/main/resources/sqlmap/order.xml",
  "path": "src/main/resources/sqlmap/order.xml",
  "lineStart": 120,
  "lineEnd": 164,
  "text": "[IbatisStatement] Order.insert (INSERT)\n..."
}
```

### `Requirement` (example)

```json
{
  "project": "shop-core",
  "reqId": "FR-001",
  "kind": "FR",
  "title": "Create Order",
  "priority": "MUST",
  "body": "Allow authenticated users to submit a valid order via POST /order/create, validate qty>0, persist row, decrement stock, redirect.",
  "traceJson": "{\"statements\":[\"Order.insert\",\"Stock.decrement\"],\"files\":[\"OrderService.java:45-102\",\"order.xml:120-164\"],\"tables\":[\"orders\",\"products\"]}"
}
```

---

## 11) Prompts (concise, for Cursor)

### Flow synthesis prompt

```
You are a senior product analyst. From the following artifacts (iBATIS statements, DAO calls, JSP forms),
produce a SINGLE coherent user-visible flow.

Return JSON:
{
  "title": "...",
  "summary": "...",
  "steps": ["..."],
  "inputs": [{"name":"...", "type":"...", "required":true, "validation":"..."}],
  "reads": ["table.column", ...],
  "writes": ["table.column", ...],
  "trace": {
    "statements": ["Namespace.id", ...],
    "files": ["path:lineStart-lineEnd", ...]
  }
}

Artifacts:
<<<CONTEXT>>>
```

### Requirements synthesis prompt

```
You are a product requirements writer.
From this Flow JSON, output:
- Functional Requirements (numbered, 3-8)
- Acceptance Criteria (Gherkin style, 3-8)
- Non-Functional Requirements (2-5)
Add MUST/SHOULD/CAN priorities.

Return Markdown with sections: ## Requirements, ## Acceptance Criteria, ## NFRs.
Include a final **Traceability** list with statementIds and files.
```

---

## 12) PRD Structure (generated)

```
# Product Requirements Document — <project>
Date: <iso date>

## 1. Overview
Local reverse-engineered from Java/JSP + iBATIS using Ollama + Weaviate.

## 2. Personas & Goals
TBD with stakeholders.

## 3. Features & Functional Requirements
### Feature: <title>
<summary>

#### Requirements
1. ...
2. ...

#### Acceptance Criteria
Given ...
When ...
Then ...

#### NFRs
- ...

#### Traceability
- Statements: Order.insert, Stock.decrement
- Files: OrderService.java:45-102; order.xml:120-164
- Tables: orders, products

(repeat per feature)

## 4. Data Model
Link: out/erd.png (from DB + resultMaps)

## 5. Validations & Errors
Summarized from JSP forms + dynamic SQL guards.

## 6. Open Questions & Risks
- ...

## 7. Appendix
Generator version, config snapshot.
```

---

## 13) Test Plan

* **Fixture project** (tiny demo with 2 entities, 4 statements, 2 JSP forms).
* Unit tests for:

  * iBATIS XML parsing (handles `<if>`, `<choose>`, `<foreach>`, `<sql refid>`).
  * DAO call extraction (literal first arg).
  * JSP field extraction (required/pattern).
* Smoke test: `make all` produces PRD with at least 3 FRs + ACs; search finds “insert” statement.

---

## 14) Risks & Mitigations

* **Dynamic SQL complexity** → missed logic.
  *Mitigation:* include raw SQL in chunks; heuristics to surface `<if>` conditions in ACs.
* **LLM variance** → inconsistent PRD wording.
  *Mitigation:* temperature 0.1–0.2; stricter JSON-first then Markdown rendering.
* **Batch upsert errors** in Weaviate.
  *Mitigation:* small batches, retries, logging with dead-letter dump.

---

## 15) Work Breakdown (for Cursor)

* `src/config/env.py` — load/validate .env (fail fast with clear messages).
* `src/discover/project.py` — implement strategies; `--all-projects` iterator.
* `src/store/weaviate_client.py` — schema ensure; batch upsert with vectors; health check.
* `src/embed/ollama_embed.py` — text → vectors via `OLLAMA_EMBED_MODEL_NAME`.
* `src/extract/{ibatis_xml,java_calls,jsp_forms,db_schema}.py` — write outputs to `data/build/`.
* `src/chunk/build_chunks.py` — assemble chunks with headers + metadata.
* `src/retrieve/search.py` — cross-class semantic search w/ filters.
* `src/synth/{prompts,prd_markdown}.py` — flow/req synthesis + PRD composer.
* `src/cli.py` — Typer CLI commands listed in §8.
* `README.md` — quickstart; `.env.example`; notes for Weaviate Docker & Ollama models.

---

## 16) Definition of Done (iteration17)

* Run `reveng schema --ensure` with no errors.
* Run `reveng extract --project auto` on a real repo → JSONs populated.
* Run `reveng index --project <name>` → Weaviate populated; `reveng search` returns expected hits.
* Run `reveng prd --project <name>` → `out/prd_<name>.md` created with ≥ 5 FRs including ACs and traceability.
* Fixture tests pass locally.

---

## 17) Migration Notes (if coming from Chroma)

* Replace embedding/indexing stage with Weaviate client.
* Keep extractor JSONs unchanged.
* Swap retrieval to Weaviate semantic search (class-filtered).
* Validate parity: the same feature queries return equivalent chunk sets.

---

## 18) Next Actions

1. Scaffold `src` folders and `cli.py` with Typer + basic `init/schema/status`.
2. Port extractors; verify JSONs on a sample repo.
3. Implement Weaviate client (schema + upsert) and embedding; index one project.
4. Add retrieval + one synthesis path; generate first feature.
5. Compose full PRD and iterate prompts on a real codebase.

---

**End of iteration17.md**
