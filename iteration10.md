# Reverse Engineering Java JSP Application: Requirements & Process

This document outlines a comprehensive, implementable approach for reverse engineering a Java JSP application to extract detailed requirements, data structures, and business rules using a Python-based workflow with Cursor.ai and Weaviate. The process is divided into two main steps: (1) automated metadata extraction and structuring, and (2) requirements documentation generation from the extracted metadata.

Environment variables (use existing ones; only add if necessary):

- `JAVA_SOURCE_DIR` (required): path to root of Java/JSP source
- `AI_PROVIDER` (default: `ollama`)
- `OLLAMA_BASE_URL` (default: `http://localhost:11434`)
- `OLLAMA_MODEL_NAME` (required in practice; e.g. `danielsheep/Qwen3-Coder-30B-A3B-Instruct-1M-Unsloth`)
- `OLLAMA_TIMEOUT` (optional; defaults per mode)
- `OUTPUT_DIR` (optional; default: `./output`)
- `WEAVIATE_HOST` (optional; default: `http://localhost:8080`)

---

## Step-by-Step Solution Guide

### Step 1: Automated Codebase Analysis and Metadata Extraction

1. **Directory Loading & File Iteration**
   - Develop a Python script to recursively traverse the source code directory.
   - Target files: `.java`, `.jsp`, `.tsp`, `.xml`, `.html`, `.js`, `.sql`.
   - Use .env variables: `JAVA_SOURCE_DIR` (required), `OUTPUT_DIR` (default `./output`), `WEAVIATE_HOST` (default `http://localhost:8080`).
   - LLM config from .env: `AI_PROVIDER`, `OLLAMA_BASE_URL`, `OLLAMA_MODEL_NAME`, `OLLAMA_TIMEOUT`.

2. **Per-File Intelligent Prompting**
   - For each file, create a tailored prompt to extract:
     - File type and purpose
     - Classes, methods, and functions (for code files)
     - Database schema, tables, fields (for SQL/XML)
     - Form fields, endpoints, and UI elements (for JSP/HTML)
     - Configuration and mapping (for XML)
     - Comments and business logic hints[2].
   - Use .env OPENAI_MODEL_NAME AI to process and enrich the metadata for each file. 

3. **Metadata Structuring**
   - Organize the extracted information into a structured JSON format, including:
     - File path
     - File type
     - Extracted entities (classes, tables, endpoints, etc.)
     - Relationships and dependencies
     - Inline comments and business rules.

4. **Storage in Weaviate**
   - Store file embeddings and metadata in Weaviate classes for semantic retrieval and grouping.
   - Ensure metadata includes unique IDs and relevant tags for efficient querying (e.g., properties like `file_path`, `language`, `layer`, `domain`).
   - Configure embeddings/generation via existing `.env` keys. Prefer `WEAVIATE_HOST` for the endpoint; reuse `OLLAMA_*` for generation provider via the Weaviate Ollama modules.

5. **JSON Export**
   - Generate a consolidated JSON file representing the full structure and metadata of the application for use in Step 2.

---

### Step 2: Requirements Documentation Generation

1. **Input Processing**
   - Load the JSON metadata as the source of truth for requirements generation.
2. **Layered Grouping**
   - Group components by logical layers:
     - Database (SQL/XML)
     - Backend (Java classes/servlets)
     - Presentation (JSP/TSP/HTML/JS)
   - Use AI to analyze and map relationships, dependencies, and flows between layers.
   
3. **Requirements Document Structure**
   - For each logical section, generate documentation using the following template:

#### Requirements Document: ``

##### 1. Overview
Brief description of the logical section and its purpose within the application.

##### 2. Components
List of all relevant classes, files, or directories in this section.

##### 3. Functionality
- **Main Features:** High-level description of the section's features.
- **Inputs/Outputs:** Data received and produced (e.g., form fields, API endpoints, database tables).
- **Key Methods/Functions:** Important methods, functions, or queries and their roles.

##### 4. Dependencies
Other sections or external systems that this section interacts with.

##### 5. Notes
Special considerations, limitations, or comments (e.g., legacy code, known issues, business rule nuances)[4][5].

4. **Iterative Refinement**
   - Use AI to refine and cross-link requirements, ensuring consistency across sections and layers.
   - Validate business rules and data flows by referencing extracted metadata and comments.

---

## Example: Requirements Document Template

```
Requirements Document: 

## 1. Overview


## 2. Components
- 
- 
...

## 3. Functionality
- **Main Features:** 
- **Inputs/Outputs:** 
- **Key Methods/Functions:** 

## 4. Dependencies
- 
- 
...

## 5. Notes

```

---

## Best Practices for Cursor.ai and Weaviate Integration

- **Cursor Project Rules:** Define `.cursor/index.mdc` and task-specific `.cursor/rules/*.mdc` files to guide AI behavior, coding standards, and architectural decisions. Keep rules concise and context-aware for optimal token usage[5].
- **PRD and RFC Approach:** Use Product Requirements Documents (PRD) and Request for Comments (RFC) documents for each feature or logical section to break down the project into manageable, well-documented parts[4].
- **Feature Grouping:** Start with database and configuration layers, then backend logic, and finally presentation/UI, ensuring requirements are grouped logically and dependencies are clear[4][5].
- **Iterative Documentation:** Update requirements iteratively as more metadata is extracted or clarified, using AI to automate cross-referencing and consistency checks.

---

## step-by-step.md: Solution Walkthrough

```markdown
# Step-by-Step Reverse Engineering Workflow

## 1. Preparation
- Install Python, Cursor.ai, and Weaviate (Docker) or connect to an existing Weaviate instance.
- Clone the Java JSP application codebase locally.

## 2. Metadata Extraction
- Run the Python script to scan the codebase and process each relevant file type.
- For each file, generate an AI prompt to extract metadata.
- Store enriched metadata and embeddings in Weaviate.

---

## Practical execution with repository scripts

Use the provided orchestration to run end-to-end with Weaviate and Ollama, honoring existing `.env` variables:

1. Create/verify `.env` contains at least:
   - `JAVA_SOURCE_DIR=/absolute/path/to/your/java/repo`
   - `AI_PROVIDER=ollama`
   - `OLLAMA_BASE_URL=http://localhost:11434`
   - `OLLAMA_MODEL_NAME=danielsheep/Qwen3-Coder-30B-A3B-Instruct-1M-Unsloth`
   - Optionally: `OUTPUT_DIR=./output`, `WEAVIATE_HOST=http://localhost:8080`

2. Activate venv and run test pipeline (non-interactive recommended for CI):

   ```bash
   source venv/bin/activate
   printf "y\ny\nn\n" | bash ./reset_and_run_production_macos.sh test
   ```

   This will:
   - Start/refresh Weaviate (Docker)
   - Backup and recreate `./output`
   - Run Step 1/2/3 with timeouts from env or defaults
   - Produce logs under `./logs/<timestamp>` and artifacts in `./output`

3. Inspect outputs quickly:

   ```bash
   ls -R ./output | sed 's/^/  /'
   LOGDIR=$(ls -td logs/* | head -1); echo "Using logs: $LOGDIR"; tail -n 80 "$LOGDIR/step1_test.log" || true
   ```

4. Rerun targeted steps (optional):

   ```bash
   bash ./Step1_Enhanced_Weaviate.sh test
   bash ./Step2_Enhanced_Weaviate.sh test
   bash ./Step3_Enhanced_Weaviate.sh test
   ```

All LLM-related settings are sourced from `.env`; do not hardcode models in scripts or docs.
- Export a consolidated JSON file of the metadata.

## 3. Requirements Generation
- Load the JSON metadata.
- Group files and components by logical layers (database, backend, presentation).
- For each group, generate a requirements document using the provided template.
- Use AI to refine, cross-link, and validate requirements.

## 4. Documentation and Review
- Assemble all requirements documents into a master requirements specification.
- Review for completeness, accuracy, and clarity.
- Iterate as needed based on feedback or further analysis.

## 5. Project Rules and Best Practices
- Define and maintain Cursor project rules for style, architecture, and workflow.
- Use PRD and RFC documents to manage features and changes.
```
