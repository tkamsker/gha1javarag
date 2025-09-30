# Refactoring Proposal (30 Sep 2025)

### Objectives
- Improve result quality for data/backend/frontend requirements.
- Remove hardcoded LLM config; use `.env` exclusively.
- Increase robustness: timeouts, process management, preflight checks.
- Add file coverage visibility and QA gates.
- Prepare the pipeline for CI/non-interactive execution.

### Scope Overview
1. Orchestration hardening (bash) and preflight.
2. Unified file discovery and manifest.
3. Step1 prompts, chunking, and entity extraction improvements.
4. Step2 requirements mapping (by layer, by domain) with cross-links.
5. Step3 modernization proposals and backlog generation.
6. Observability (JSON summaries, metrics) and QA thresholds.
7. Optional: Convert orchestration to Python CLI; Docker Compose infra.

### Phase 1: Reliability & Config (now)
- Add preflight: verify required commands, `.env` keys, Weaviate/Ollama health, and that `JAVA_SOURCE_DIR` contains supported files.
- Ensure all LLM settings (provider, base URL, model, timeouts) come from `.env`.
- Strengthen timeouts and process group handling to avoid orphaned processes.
- Generate `output/file_manifest.json` and print coverage per file type.

Deliverables:
- Updated `reset_and_run_production_macos.sh` with preflight and manifest generation.
- `output/file_manifest.json` and coverage summary in console/logs.

### Phase 2: Discovery & Entities (Step1)
- Tailored prompts per file type (Java/Kotlin, JSP/HTML/JS/TS, YAML/XML, SQL).
- Intelligent chunking per type (class/function; template sections; config blocks).
- Extract entities: Components, Endpoints, DataModels, ConfigSettings, DbQueries.
- Persist entities to Weaviate classes for later linking.

Deliverables:
- Enhanced Step1 Python logic and schemas; entity counts in summary.

### Phase 3: Requirements Mapping (Step2)
- Build layer mapping (presentation/application/data) from Step1 entities.
- Infer domains via packages, paths, and keywords.
- Generate markdown using consistent templates, with cross-links.

Deliverables:
- Richer `output/requirements_*` with layer/domain docs and links.

### Phase 4: Modernization & Backlog (Step3)
- Detect legacy patterns and coupling; propose target architectures.
- Output prioritized modernization backlog with dependencies and estimates.

Deliverables:
- `requirements_modern` with actionable plan and metrics.

### Phase 5: Observability & QA
- `output/run_summary.json` capturing statuses, durations, coverage, error rates.
- Threshold checks (e.g., min coverage per type) with warnings/fail option.

Deliverables:
- JSON summary, CI-friendly exit codes, dashboards later.

### Phase 6: Orchestration & Infra (optional)
- CLI flags: `--mode`, `--yes`, `--auto-model`, `--no-web`.
- Docker Compose for Weaviate with configurable resources/ports.
- Optionally migrate bash orchestration to Python for testability.

### Risks & Mitigations
- Large repos: control parallelism; cache by file fingerprint.
- Model variability: deterministic prompts, retries with smaller chunks.
- Incomplete configs: strong preflight with clear remediation tips.

### Milestones
1. M1 (today): Phase 1 complete, manifest + preflight in place.
2. M2 (+2-3 days): Phase 2 entity extraction and Step1 summaries.
3. M3 (+1 week): Phase 3/4 mapping and modernization backlog.
4. M4 (+2 weeks): Phase 5 observability and Phase 6 CLI/compose.


