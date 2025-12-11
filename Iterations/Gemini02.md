Below is a Spec Kit–ready `prd.md` you can place under something like `specs/001-gemini-pipeline/prd.md` and then run `/speckit.specify` on to generate the detailed spec and Python files.[1][2][3]

***

# PRD: GEMINI Code Analysis and PRD Generator

## 1. Product overview

This product is a Python-based pipeline that analyzes large Java/JSP/GWT/JavaScript codebases, extracts structured information, and generates high-quality Product Requirements Documents (PRDs) and requirements from the code itself. The pipeline makes legacy and complex applications understandable by indexing code artifacts in a vector database and enabling semantic search and documentation generation.[1]

The system is used as an offline analysis and documentation tool that runs against existing repositories and produces Markdown PRDs that can be consumed by GitHub Spec Kit to drive spec-driven development and code generation.[3][4][1]

## 2. Goals and non-goals

### 2.1 Goals

- Enable product and engineering teams to understand complex Java-family codebases without reading every file.  
- Automatically discover relevant backend and frontend artifacts (services, endpoints, JSP pages, GWT modules, SQL mappings, etc.) and convert them into structured data.[1]
- Provide semantic search across code artifacts using a vector database, so users can ask natural-language questions about the system.[1]
- Generate Markdown PRDs and requirements derived from the behavior and structure of the existing codebase.[1]
- Produce PRD outputs that are directly consumable by GitHub Spec Kit as inputs to `/speckit.specify`, `/speckit.plan`, and `/speckit.tasks` for further specification and implementation.[2][4][3]

### 2.2 Non-goals

- Directly modifying or refactoring the original Java/JSP/GWT/JS codebase.  
- Providing full UI design or visual prototypes.  
- Replacing traditional monitoring, logging, or runtime observability tools.  
- Handling non–Java-family stacks in the first version.

## 3. Users and use cases

### 3.1 User types

- Product managers: want to derive accurate PRDs and feature descriptions from real system behavior to support roadmap and stakeholder communication.[5][1]
- Backend engineers: want to see an overview of services, APIs, data models, and persistence behavior across modules.[1]
- Frontend engineers: want to understand JSP pages, GWT modules, form flows, and how the UI talks to backend endpoints.[1]
- Architects / tech leads: want a holistic view of modules, dependencies, and cross-cutting concerns for modernization and migration.[1]

### 3.2 Primary use cases

- Analyze an existing Java monolith or multi-module project and generate a first-pass PRD to seed Spec Kit specs.  
- Explore where a particular feature or business concept is implemented across multiple layers (controller, service, DAO, JSP/GWT UI).  
- Keep documentation in sync by re-running the pipeline after code changes and updating PRDs/specs accordingly.  
- Provide a structured input to Spec Kit so AI agents can generate Python orchestration code and supporting utilities for the analysis pipeline.

## 4. Scope

### 4.1 In scope

- CLI-driven pipeline with the following stages (each as a subcommand): discover, extract, index, search, prd.[1]
- Support for analyzing Java/JSP/GWT/JavaScript and related XML/config files under a source root defined by an environment variable `JAVA_SOURCE_DIR`.[1]
- Integration with a Weaviate vector database for artifact embeddings and semantic search.[1]
- Integration with a local LLM (Ollama) for generating natural-language PRDs and requirements from indexed artifacts.[1]
- Generation of Markdown PRD files in a structure that can be placed directly into a Spec Kit repo under `specs/<id>/prd.md`.[2][1]

### 4.2 Out of scope (v1)

- Multi-repo correlation beyond a single configured project.  
- Real-time, incremental indexing triggered by CI; v1 assumes on-demand runs by a developer.  
- Non–Weaviate vector stores or SaaS LLM providers.

## 5. Functional requirements

### 5.1 Source discovery

- The system must read `JAVA_SOURCE_DIR` (from `.env` or environment) to determine the root directory of the codebase to analyze.[1]
- The `discover` stage must recursively scan the directory tree for relevant file types, including at minimum `.java`, `.jsp`, `.js`, `.xml`.[1]
- Discovered files must be stored as a structured list that includes project identifier, absolute or canonical path, and file type, to be consumed by later pipeline stages.[1]
- The discovery command must be invokable from the CLI as `python main.py discover --project <project_name>`.[1]

### 5.2 Artifact extraction

- The `extract` stage must parse discovered files and build structured artifacts for:  
  - Backend: controllers/endpoints, service classes, data access layers (DAOs/repositories), ORM or iBATIS mappings, SQL statements, and domain models.[1]
  - Frontend: JSP pages, forms, view templates, GWT modules, client-side controllers, key JavaScript front-end logic.[1]
- Each artifact must include:  
  - A stable identifier (e.g. project + path + symbol name).  
  - File path, artifact type, language/framework.  
  - Key metadata: e.g. for endpoints, HTTP method and URL; for forms, fields and validation; for SQL, tables and columns.[1]
- The `extract` command must support an `--include-frontend` flag to enable or disable frontend extraction: `python main.py extract --project <project_name> --include-frontend`.[1]
- Extraction must log progress and failures in a structured way with configurable log level via `LOG_LEVEL` and CLI flags.[1]

### 5.3 Indexing into Weaviate

- The `index` stage must transform each artifact into a text representation suitable for embedding and store it in Weaviate along with its metadata.[1]
- Index entries must be grouped or filterable by `project`, artifact type, and possibly module or package namespace.[1]
- The indexing process must be idempotent: re-running indexing for the same project should update or upsert artifacts instead of duplicating them.  
- The system must allow configuration of Weaviate endpoint and credentials via `config/settings.py` and environment variables (e.g. `WEAVIATE_HOST`).[1]

### 5.4 Semantic search

- The `search` stage must allow natural-language queries such as “Where is user registration handled?” and return a ranked list of relevant artifacts from Weaviate.[1]
- Search results must include artifact type, name, relevance score, and source file path, rendered in a human-readable CLI format.[1]
- The search command must support filtering by project and optional filters such as artifact type (backend/frontend) or module.[1]
- The CLI command pattern must be `python main.py search --project <project_name> --query "<question>"`.[1]

### 5.5 PRD and requirements generation

- The `prd` stage must use Ollama to synthesize one or more Markdown PRD documents from the indexed artifacts of a single project.[1]
- PRD generation must support backend-only, frontend-only, and combined perspectives via CLI flags such as `--frontend` and `--include-frontend`.[1]
- Generated PRDs must include, at minimum: problem statement, user types, high-level architecture or module overview, feature-level summaries, functional requirements, and explicit out-of-scope items.[6][5][1]
- Output files must be written to a predictable directory (for example `out/prd/<project_name>.md`) so they can be moved into `specs/<id>/prd.md` in a Spec Kit repo.[1]
- The system must support generating additional requirement documents per artifact type or module (e.g. separate backend and frontend requirement files) if requested by the user.

### 5.6 CLI orchestration

- There must be a single entrypoint `main.py` that exposes a Click-based CLI with subcommands `all`, `discover`, `extract`, `index`, `search`, and `prd`.[1]
- The `all` command must execute the entire pipeline in sequence for a given project, with an option to include frontend analysis:  

  - `python main.py all --project <project_name> --include-frontend`.[1]

- CLI help text must document each command, required flags, and typical usage examples.[1]

### 5.7 Integration with Spec Kit

- Generated PRD files must be formatted as standard Markdown, with clear headings and sections compatible with Spec Kit’s `/speckit.specify` workflow.[3][2]
- Documentation must explain how to place the generated PRDs into `specs/<feature-id>/prd.md` in a Spec Kit–initialized repository and use `/speckit.specify` to create detailed feature specs.[7][3]
- The system should support including tags or metadata in PRDs (e.g., domain tags, project ID) that help Spec Kit organize and break down features into multiple specs and tasks.[4][2]

## 6. Non-functional requirements

- The pipeline must run on Python 3.8+ and be compatible with macOS for development and Linux for running Dockerized services.[1]
- It must use standard Python tooling: Click for CLI, pytest for tests, `logging` for logs, and `requirements.txt` for dependency management.[1]
- Weaviate must be runnable via Docker Compose or an existing shell script, and Ollama must be used as the LLM runtime, with clear startup instructions.[1]
- The system should be resilient to partial failures in extraction or indexing and log errors without aborting the entire run when possible.  
- The pipeline should scale to large monorepos by processing files in batches and avoiding loading the entire codebase into memory at once.[1]

## 7. Assumptions and dependencies

- A Weaviate instance is available and reachable from the machine running the pipeline, either locally or on a remote Linux host.[1]
- Ollama is installed and running on the developer machine and has at least one suitable model pulled for text generation.  
- The Java-family codebase resides under a path that can be referenced via `JAVA_SOURCE_DIR` and read by the pipeline process.[1]
- A Spec Kit–initialized repository exists or will be created, and the team has access to a compatible AI assistant (e.g., Copilot, Claude, Cursor) to run `/speckit.specify`, `/speckit.plan`, and `/speckit.tasks`.[4][3]

## 8. Success metrics

- Time to produce a first useful PRD for a medium-sized Java/JSP/GWT application is reduced from days of manual analysis to hours or less.  
- Product and engineering teams can answer core questions about system behavior (e.g., “where is login handled?”, “what data models support orders?”) via the search interface without deep code spelunking.[1]
- Spec Kit successfully consumes the generated PRDs to create detailed specs and plans, and the AI assistant can generate Python code that matches the envisioned pipeline behavior.[2][3][4]

***

You can now ask your AI assistant inside the Spec Kit–initialized repo to run `/speckit.specify` on this `prd.md` and then guide it to generate the Python CLI, pipeline modules, and integration glue code.

[1](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/10476480/83f01005-9c50-41f5-9074-1657c3125c40/GEMINI.md)
[2](https://github.com/github/spec-kit/blob/main/spec-driven.md)
[3](https://github.com/github/spec-kit)
[4](https://intuitionlabs.ai/articles/spec-driven-development-spec-kit)
[5](https://www.atlassian.com/agile/product-management/requirements)
[6](https://www.cycle.app/library/write-product-requirement-document)
[7](https://developer.microsoft.com/blog/spec-driven-development-spec-kit)
[8](https://intuitionlabs.ai/pdfs/github-spec-kit-a-guide-to-spec-driven-ai-development.pdf)
[9](https://www.reddit.com/r/ClaudeCode/comments/1ncbshm/used_spec_kit_to_create_a_full_spec_from_an/)
[10](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
[11](https://blog.logrocket.com/github-spec-kit/)