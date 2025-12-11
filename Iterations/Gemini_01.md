The initial Spec Kit document should describe a pipeline that reads Java-family source trees (rooted at `JAVA_SOURCE_DIR`), loads extracted artifacts into a Weaviate database, and then generates backend and frontend requirements plus PRDs on top of those indexed artifacts.[1][2]

Below is a concise, step-by-step spec-style draft you can paste into `specs/001-gemini-pipeline/spec.md` (or similar) in a Spec Kit repo and refine with `/speckit.specify` and `/speckit.plan`.[2][3]

***

## Problem and context

Legacy Java/JSP/GWT/JavaScript applications are organized as multiple subprojects under a common root, making it hard to understand behavior, dependencies, and feature scope without extensive manual analysis. The goal is to automate discovery and documentation so that product and engineering teams can derive high‑quality PRDs and implementation plans directly from code.[4][1]

## Users and goals

- Product managers  
  - Want PRDs and feature requirements derived from real system behavior, not out‑of‑date docs.[1][4]
- Backend engineers  
  - Want searchable insight into services, persistence, and integration points across subprojects to support refactoring and extensions.[1]
- Frontend engineers  
  - Want a map of UI flows, forms, and API usage patterns across JSP/GWT/JS frontends.[1]
- Architects / tech leads  
  - Want a consolidated view of modules and dependencies to guide modernization and migration work.[1]

## High-level solution

Create a Python-based pipeline that: discovers source files under `JAVA_SOURCE_DIR`, extracts structured artifacts, indexes them in Weaviate, and then drives requirements and PRD generation using a local LLM (Ollama), with outputs formatted for Spec Kit PRD/spec files.[2][1]

Core stages (CLI subcommands in `main.py` / `src/cli.py`):[1]
1. `discover`: Find relevant files under `JAVA_SOURCE_DIR` (e.g., `.java`, `.jsp`, `.js`, `.xml`,'.html','.css','.json','.htm', config).[1]
2. `extract`: Parse files into structured artifacts (e.g., GWT modules, iBATIS statements, JSP forms, DB schemas, endpoints).[1]
3. `index`: Create and store vector embeddings of artifacts in Weaviate.[1]
4. `search`: Provide natural‑language search over artifacts via CLI.[1]
5. `prd`: Generate PRDs and requirements from indexed artifacts using Ollama.[1]

This pipeline should integrate with Spec Kit by treating generated PRDs as inputs to `/speckit.specify` and related commands for downstream planning and task generation.[3][2]

## Scope

In scope (initial iteration):

- Single “project” at a time, configured via CLI `--project` and `.env` (including `JAVA_SOURCE_DIR`).[1]
- Reading and analyzing Java/JSP/GWT/JS/XML and related resources under a multi-module directory tree.[1]
- Populating a Weaviate instance with artifact embeddings, keyed by project and artifact type.[1]
- Generating Markdown PRDs and requirements that can be dropped into a Spec Kit repo (e.g., under `specs/<feature-id>/prd.md`).[3][1]
- Supporting both backend (services, persistence) and frontend (UI, navigation) requirement extraction.[1]

Out of scope (for v1):

- Automatic refactoring or code modification.  
- Full UI mockups; only structural and behavioral requirements.  
- Multi-repo correlation beyond a single configured project root.

## Functional requirements

### 1. Source discovery (using `JAVA_SOURCE_DIR`)

- The system MUST read the `JAVA_SOURCE_DIR` environment variable (from `.env` or environment) to determine the root of the source tree.[1]
- The `discover` stage MUST recursively scan `JAVA_SOURCE_DIR` for file types: `.java`, `.jsp`, `.js`, `.xml`,'.html','.css','.json','.htm', and any additional configured extensions.[1]
- The pipeline MUST organize discovered files into logical subprojects (e.g., by Maven/Gradle module, webapp folder, or configurable patterns).[1] it needs to understand that each directory havng an src subdirectory is to be considered a Java project. and because projects reuse objetcs from other projects (see pom.xml for details) we need to take care of this.[1]
- Discovery output MUST be persisted (e.g., JSON or database collection) keyed by project and path to feed into `extract`.[1]
- discovrey output needs to be organized in .env OUTPUT_DIR and subdirectory per project for futher use. 

### 2. Artifact extraction

- The `extract` stage MUST parse discovered files into typed artifacts, including at minimum:  
  - Backend: service classes, controllers/endpoints, DAO/repository definitions, ORM/iBATIS mappings, SQL statements, and data models.[1]
  - Frontend: JSP pages, forms, GWT modules, client‑side controllers, and significant JS views and html fragments.[1]
  - if necessary it must step into more detail files like .jsp, .js, .xml, .html, .css, .json, .htm 
- Each artifact MUST include:  
  - Canonical ID (e.g., project + path + symbol name).  
  - Source path and language/framework type.  
  - Key metadata (e.g., endpoints and HTTP verbs, DTO fields, DB table and column names, form fields, navigation targets).[1]
- The `extract` stage MUST support an `--include-frontend` flag to control whether frontend artifacts are processed.[1]
- Extraction MUST log progress and errors using the centralized logging configuration (configurable by `LOG_LEVEL`).[1]

### 3. Indexing into Weaviate (“aviate database”)

- The `index` stage MUST connect to a Weaviate instance (configured via `config/settings.py`, `.env`, and/or CLI flags).[1]
- For each artifact, the system MUST generate a vector embedding suitable for semantic search and store it in Weaviate along with its metadata.[1]
- The index MUST be partitioned or tagged by `project` and artifact type to support multi-project usage within a shared Weaviate instance.[1]
- The system SHOULD provide idempotent indexing (re‑running `index` for the same project updates or upserts artifacts rather than duplicating).[1]

### 4. Search over indexed artifacts

- The `search` stage MUST accept a natural language `--query` and `--project`, perform a vector search over Weaviate, and return the most relevant artifacts.[1]
- Search results MUST be human-readable in CLI (summaries, key fields, and links to source paths) and may be optionally exported for further processing.[1]
- The system SHOULD support filters by artifact type (e.g., only backend services, only JSP) and by subproject/module.[1]

### 5. PRD and requirements generation

- The `prd` stage MUST use Ollama to generate a Markdown PRD and requirement set from the indexed artifacts of a given project.[1]
- The `prd` command MUST support generating both:  
  - Backend-focused requirements (services, data models, integrations).  
  - Frontend-focused requirements (pages, flows, forms, UI‑to‑backend interactions), controlled via flags like `--frontend` and `--include-frontend`.[1]
- Generated PRDs MUST follow a structure compatible with PRD best practices (e.g., objectives, stakeholders, user stories, functional/non‑functional requirements, out of scope).[5][4][1]
- The system MUST separate concerns so that:  
  - One PRD can describe system‑level context.  
  - Additional requirement documents can be generated per feature, module, or service and later mapped into Spec Kit feature specs.[6][3]

### 6. Integration with Spec Kit

- The pipeline MUST support writing PRD/requirements output into a directory layout compatible with Spec Kit (e.g., `specs/<feature-id>/prd.md` and `specs/<feature-id>/spec.md`).[2][3]
- There MUST be documentation or scripts explaining how to:  
  - Initialize a Spec Kit repo using `specify init`.  
  - Copy or generate PRD files from the pipeline into that repo.  
  - Use `/speckit.specify` to transform PRDs into Spec Kit feature specs.[6][3][2]
- The system SHOULD tag artifacts and generated documents with feature or domain labels to help Spec Kit planning and task breakdown later.[3]

## Non-functional requirements

- The pipeline MUST run on Python 3.8+ and use Click for CLI, pytest for tests, and standard logging.[1]
- Weaviate MUST run via Docker (e.g., `docker-compose` or helper script) and be documented as a runtime dependency.[1]
- Ollama MUST be treated as a local dependency, with clear instructions for starting the service (`ollama serve`) and configuring models.[1]
- Configurations MUST be centralized in `config/settings.py` but overrideable via `.env` and environment variables, including `JAVA_SOURCE_DIR`, Weaviate host, and model parameters.[1]
- The system SHOULD handle large monorepos by streaming discovery/extraction and by batching indexing operations.[1]

## Step-by-step workflow (for teams)

1. **Prepare environment**  
   - Set up Python environment, install dependencies, and start Weaviate and Ollama as documented.[1]
   - Create `.env` with `JAVA_SOURCE_DIR` pointing to the root of the multi-subproject codebase.[1]

2. **Run pipeline for a project**  
   - Execute `python main.py discover --project <project>` to scan code.[1]
   - Execute `python main.py extract --project <project> --include-frontend` to build artifacts.[1]
   - Execute `python main.py index --project <project>` to populate Weaviate.[1]
   - Optionally use `python main.py search --project <project> --query "<question>"` for exploration.[1]

3. **Generate PRDs and requirements**  
   - Run `python main.py prd --project <project> --frontend` (and variants) to produce Markdown PRDs and requirement documents for backend and frontend.[1]
   - Save or move these outputs into a Spec Kit repository under `specs/` as PRD inputs.[6][2][3]

4. **Use Spec Kit for deployment planning**  
   - Initialize a Spec Kit project (`specify init ...`).[7][2]
   - Use `/speckit.specify` with the generated PRDs to create structured specifications.[2][3][6]
   - Run `/speckit.plan` and `/speckit.tasks` to derive detailed implementation plans and tasks for backend and frontend modernization or feature work.[3][2]

***

If you like, the next step can be drafting a concrete `prd.md` template tailored to one example project, so that you can drop it directly into `specs/001-<project-name>/prd.md` and use it as the seed for Spec Kit.

[1](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/10476480/83f01005-9c50-41f5-9074-1657c3125c40/GEMINI.md)
[2](https://github.com/github/spec-kit)
[3](https://github.com/github/spec-kit/blob/main/spec-driven.md)
[4](https://cpoclub.com/product-development/product-requirements-document/)
[5](https://formlabs.com/blog/product-requirements-document-prd-with-template/)
[6](https://www.reddit.com/r/ClaudeCode/comments/1ncbshm/used_spec_kit_to_create_a_full_spec_from_an/)
[7](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
[8](https://www.youtube.com/watch?v=LA_HqmiGvsE)
[9](https://www.youtube.com/watch?v=a9eR1xsfvHg)
[10](https://www.youtube.com/watch?v=61K-2VRaC6s)
[11](https://www.youtube.com/watch?v=-9obEHJkQc8)