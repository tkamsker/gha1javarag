Here is a structured PRD (Product Requirements Document) you can drop into your `docs/prd/step3_prd.md` (or similar) for Cursor to guide the **refactoring and implementation of step3** into a maintainable, modular Python workflow.  

***

# PRD: Step 3 Requirements Synthesis (LLM + Weaviate)

## 1. Overview

The goal of **Step 3** is to replace the `step3.sh` shell wrapper with a structured, modular Python-based processing pipeline.  
This step synthesizes **deep requirements documentation per project domain** using metadata from earlier steps, stored in Weaviate, and enhanced with LLM analysis.  

The system should:
- Read intermediate metadata (`intermediate_step2.json` or `consolidated_metadata.json`).
- Query Weaviate for statistics and grouped embeddings.
- Generate structured Markdown requirements outlines per project (and sub-documents if enabled).
- Provide an executive summary across projects.

***

## 2. Objectives

- Consolidate orchestration into a dedicated processor (`Step3Processor`).
- Add **robust error handling** for configuration, Weaviate, and LLM provider validation.
- Generate **modular output files**, not a single append-only markdown.
- Allow for **parallel processing of projects** to speed up requirements generation.
- Enable **incremental re-runs**, processing only missing outputs when possible.  

***

## 3. Functional Requirements

### 3.1 Input Sources
- Requires `.env` configuration:
  - `WEAVIATE_URL`, `WEAVIATE_API_KEY`
  - `OPENAI_MODEL_NAME` or `ANTHROPIC_MODEL` (depending on provider)
  - `OUTPUT_DIR`
- Requires intermediate JSON:
  - `intermediate_step2.json` (preferred)
  - fallback: `consolidated_metadata.json`
- Uses data structures containing:
  - Project metadata (name, file list, classifications, AI analysis metadata).

### 3.2 Processing Flow
1. **Configuration and Validation**
   - Validate `.env` variables.
   - Verify Weaviate connectivity.
   - Validate JSON structure against schema.
   - Check LLM provider credentials.

2. **Statistics Collection**
   - Query Weaviate once per run for collection stats.
   - Cache stats in memory for reuse across project processing.

3. **Requirement Synthesis Loop**
   - Iterate over projects.
   - For each project:
     - Aggregate metadata.
     - Build LLM prompt including:
       - Project summary
       - File classifications
       - Weaviate statistics
     - Run LLM to generate structured Markdown requirement outline.
   - Optionally process sub-domains (e.g., database, backend, UI).

4. **Output Generation**
   - Executive summary: `_step3_overview.md`
   - Per-project requirements: `projects/{project_name}/requirements.md`
   - Optionally:
     - `projects/{project_name}/architecture.md`
     - `projects/{project_name}/dependencies.md`

5. **Logging and Reporting**
   - Write logs under `logs/`
   - Progress reporting for large project runs.

### 3.3 Parallelism
- Use `concurrent.futures.ThreadPoolExecutor` to process projects concurrently.
- Ensure shared resources (logs, stats, output dirs) are thread-safe.

***

## 4. Non-Functional Requirements
- Maintainability: Modular code with `Step3Processor` class.
- Scalability: Should support projects with 1,000+ files.
- Extensibility: Easy to add new output templates (Markdown/JSON).
- Reliability: Fail fast on bad config or missing data.
- Auditability: Preserve all LLM prompts and responses for traceability.

***

## 5. Output Structure

```
{OUTPUT_DIR}/requirements/
  ├── _step3_overview.md             # Executive summary across projects
  ├── projects/
  │     ├── project1/
  │     │     ├── requirements.md
  │     │     ├── architecture.md
  │     │     └── dependencies.md
  │     ├── project2/
  │     │     └── requirements.md
  │     ...
  └── logs/
        └── step3_run.log
```

***

## 6. Implementation Plan (for Cursor coding)

### Phase 1: Core Processor
- [ ] Create `src/step3_processor.py`
- [ ] Implement `Step3Processor` with methods:
  - `load_intermediate_data()`
  - `collect_weaviate_statistics()`
  - `synthesize_requirements(project_data: Dict, stats: Dict) -> str`
  - `generate_output_files(project_name: str, markdown: str)`

### Phase 2: Error Handling and Validation
- [ ] Add `Step3Config` class to validate `.env` and prerequisites.
- [ ] Raise custom exceptions for missing data or invalid connectivity.

### Phase 3: Output Enhancements
- [ ] Add template-based generation for `requirements.md`, `architecture.md`, `dependencies.md`.
- [ ] Structure project directories dynamically.
- [ ] Append executive summary from project outputs.

### Phase 4: Optimization
- [ ] Add parallel processing of projects.
- [ ] Implement incremental processing (skip if files already generated).
- [ ] Add progress tracking with status updates.

***

## 7. Success Criteria
- Running `python -m src.cli step3 --verbose` should:
  - Validate config and inputs.
  - Process all projects (with parallelism).
  - Generate structured requirements documents in the specified output directory.
  - Provide a global executive summary.
- Refactored solution should fully replace `step3.sh`.

***

Would you like me to also draft the **Cursor rules file (`.cursor/rules/step3.mdc`)** that enforces coding style, error handling, and modularization for this step? That way, Cursor auto-completes and generates Python code aligned with the PRD.