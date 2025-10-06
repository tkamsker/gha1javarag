## Analysis and Refactor Plan for `run_iteration.sh`

### Scope
- Make step1 (index/analyze) a one-time operation per source snapshot.
- Allow step2 and step3 to be repeatable and fast to iterate.
- Support two step3 approaches in parallel for comparison: programmatic (PGM) and CrewAI.
- Ensure Docker Weaviate storage is persistent across runs.

### Current State (as implemented)
- `run_iteration.sh` performs:
  - Environment checks (venv, deps, `.env`, `JAVA_SOURCE_DIR`, LLM provider).
  - Weaviate availability check and LLM checks.
  - Creates a timestamped `OUTPUT_DIR` by rewriting `.env` each run.
  - If `step1.sh`, `step2.sh`, and `step3-crewai.sh` exist, runs a three-step flow:
    - Step1: `./step1.sh` → `python -m src.cli analyze` (optionally `--no-upsert` via env)
    - Step2: `./step2.sh` → `python -m src.cli requirements`
    - Step3: `./step3-crewai.sh --no-verbose` → `python -m src.cli step3-crewai`
    - Stats + summary
  - Else falls back to legacy `index` → `requirements` → `stats`.

- Step scripts:
  - `step1.sh`: creates/activates venv, installs deps, ensures `.env` exists, sets `OUTPUT_DIR` if missing, runs `analyze` (with or without upsert). Writes `consolidated_metadata.json` to `$OUTPUT_DIR`.
  - `step2.sh`: similar env bootstrap, requires `.env`, expects `$OUTPUT_DIR` present, warns if `consolidated_metadata.json` missing, runs `requirements` to `$OUTPUT_DIR/requirements`.
  - `step3.sh` (refactored): `python -m src.cli step3` with parallel/sequential, incremental/force flags.
  - `step3-pgm.sh`: `python -m src.cli step3-pgm` with `--enhanced` default; requires `$OUTPUT_DIR/intermediate_step2.json` or `consolidated_metadata.json`.
  - `step3-crewai.sh`: `python -m src.cli step3-crewai`; validates Weaviate and LLM provider; requires intermediate data; installs CrewAI if missing.

- Docker:
  - `docker-compose.yml` mounts `./weaviate-data:/var/lib/weaviate` ensuring persistence; healthcheck configured; Ollama endpoint set to `host.docker.internal:11434`.
  - `docker-weaviate.sh` also mounts `./weaviate-data` and supports lifecycle commands; persistence documented in `DOCKER_SETUP.md`.

### Detailed Behavior of Each Step

- Step1 (`python -m src.cli analyze`):
  - Reads `JAVA_SOURCE_DIR`, walks and parses source files using parsers in `src/parsers/` and chunkers in `src/chunking.py`.
  - Upserts to Weaviate unless `STEP1_NO_UPSERT=1` is set in environment, writing semantic objects via `src/weaviate_client.py`.
  - Writes consolidated metadata to `$OUTPUT_DIR/consolidated_metadata.json`. Indexes and logs land under `$OUTPUT_DIR/logs/` and `$OUTPUT_DIR/catalog.index.json` (via `src/reporting.py`).

- Step2 (`python -m src.cli requirements`):
  - Consumes consolidated metadata or intermediate artifacts to generate requirement docs under `$OUTPUT_DIR/requirements/` via `src/requirements_gen/generator.py`.

- Step3-PGM (`python -m src.cli step3-pgm`):
  - Performs deterministic programmatic classification using `src/enhanced_component_classifier.py` with optional LLM enhancement; produces backend/frontend docs under `$OUTPUT_DIR/requirements/pgm/` and traceability JSON.

- Step3-CrewAI (`python -m src.cli step3-crewai`):
  - Runs multi-agent orchestration in `src/step3_crewai_processor.py`, writes agent artifacts under `$OUTPUT_DIR/requirements/crewai/`.

### Identified Gaps
- `run_iteration.sh` unconditionally rewrites `.env` to a new timestamped `OUTPUT_DIR` every run, which makes repeatable step2/3 over the same dataset cumbersome.
- No built-in guard in `run_iteration.sh` to detect an already-completed Step1 and skip it automatically.
- Comparison workflow between PGM and CrewAI is manual; outputs land in separate directories but `run_iteration.sh` runs only CrewAI by default in the three-step branch.
- Optional idempotency flags exist at step3 level (`--incremental`, `--force`) but are not surfaced or orchestrated by `run_iteration.sh`.

### Goals
- Preserve a stable `OUTPUT_DIR` for iterative work; allow explicit opt-in to rotate outputs.
- Add detection for existing Step1 artifacts to skip re-index when unchanged.
- Make Step3 dual-mode comparison first-class: run PGM and CrewAI in one command and collate a simple comparison index.
- Keep Docker persistence as-is; add minimal checks and guidance in script output.

### Proposed Changes

1) Output directory handling
- Default: Do not rewrite `OUTPUT_DIR` in `.env` if already set. Only create a timestamped `OUTPUT_DIR` when a new flag is passed (e.g., `--new-output`).
- Add `--output-dir <path>` to override `OUTPUT_DIR` for a single run (without modifying `.env`).
- Provide `--rotate-output` shorthand to set `OUTPUT_DIR=./output_$(date +%Y%m%d_%H%M%S)` for this run only.

2) Step1 one-time semantics
- Detect if Step1 artifacts exist and are fresh enough:
  - Presence of `$OUTPUT_DIR/consolidated_metadata.json` (or `catalog.index.json`) and a `.step1_complete` marker.
  - Optional freshness check: if `JAVA_SOURCE_DIR` tree has newer mtime than the marker, prompt or re-run.
- Add flags:
  - `--force-step1`: re-run Step1 regardless of cache.
  - `--no-step1`: skip Step1 explicitly.
- Behavior:
  - If no artifacts → run `./step1.sh`.
  - If artifacts exist and no force → skip Step1 and continue.

3) Step2 repeatability
- Allow `--repeat-step2` to re-run requirements generation into the current `$OUTPUT_DIR/requirements`.
- Default: run Step2 if either it has not been run yet (no requirements folder) or `--repeat-step2` is set.

4) Step3 dual-mode comparison
- New flags in `run_iteration.sh`:
  - `--step3=pgm|crewai|both` (default: `both`).
  - `--step3-parallel|--step3-sequential`, `--step3-max-workers N` forwarded to `step3-pgm.sh` and `step3.sh` as applicable.
  - `--crewai-verbose/--crewai-no-verbose` forwarder.
  - `--pgm-enhanced/--pgm-pattern-based` forwarder.
  - `--step3-incremental`, `--step3-force` (forward to refactored `step3.sh`).
- Execution:
  - When `both`, run `./step3-pgm.sh` then `./step3-crewai.sh` (or vice versa) and generate a comparison index file:
    - Write to `$OUTPUT_DIR/requirements/_comparison/index.md` containing links to `requirements/pgm/` and `requirements/crewai/` and a small summary matrix (projects covered, counts, warnings).

5) Stats and summary
- Keep existing `stats` step.
- Update `create_summary` to include:
  - Whether Step1 was reused or re-executed.
  - Which step3 modes ran and pointers to their output roots.
  - Link to the comparison index if `both`.

6) Docker persistence and readiness
- Add a quick readiness check with actionable guidance:
  - If `curl $WEAVIATE_URL/v1/meta` fails → print `docker compose up -d` hint and `./docker-weaviate.sh` hint.
  - Detect missing persistent volume dir `./weaviate-data` and inform that it will be created by compose/script.
  - Print the data path in use when connected.

### Minimal Implementation Outline (edits)

In `run_iteration.sh`:
- Replace `create_output_dir` with logic:
  - Respect existing `.env` `OUTPUT_DIR`.
  - Allow `--output-dir` and `--rotate-output` without persisting to `.env`.
- Parse new CLI flags (`--new-output`, `--rotate-output`, `--output-dir`, `--force-step1`, `--no-step1`, `--repeat-step2`, `--step3=`, `--step3-parallel`, `--step3-sequential`, `--step3-max-workers`, `--step3-incremental`, `--step3-force`, `--crewai-no-verbose`, `--pgm-pattern-based`).
- Implement Step1 artifact detection with a `.step1_complete` marker written by `step1.sh` at end of success.
- Gate Step2 execution based on `requirements` presence or `--repeat-step2`.
- Add a `run_step3_both` orchestrator that calls the two step3 scripts and creates `_comparison/index.md`.
- Update `create_summary` to reflect the above and link to comparison outputs.

In `step1.sh`:
- After successful analyze, write `$OUTPUT_DIR/.step1_complete` with timestamp and summary (e.g., file counts, model provider).
- Do not mutate `.env` if `OUTPUT_DIR` is already set; only append if missing.

In `step2.sh`:
- No change required; it is already repeatable and safe. Optionally add `--clean` to clear previous requirements before regenerating.

In `step3-pgm.sh` and `step3-crewai.sh`:
- Ensure they respect `$OUTPUT_DIR` and do not overwrite unrelated outputs.
- Accept pass-through flags from `run_iteration.sh`.

### Example Workflows

Initial run (fresh project):
```bash
./docker-weaviate.sh             # start Weaviate with persistence
./run_iteration.sh --rotate-output --step3=both
```

Iterate on requirements without re-indexing:
```bash
./run_iteration.sh --no-step1 --repeat-step2 --step3=both --step3-incremental
```

Force re-index after source changes, keep same output dir:
```bash
./run_iteration.sh --force-step1 --repeat-step2 --step3=pgm
```

Write outputs to a custom directory for an A/B run:
```bash
./run_iteration.sh --output-dir ./output_experiment_A --step3=crewai --crewai-no-verbose
```

### Output Structure (after refactor)
```
$OUTPUT_DIR/
├── projects/
├── requirements/
│   ├── pgm/
│   ├── crewai/
│   └── _comparison/
│       └── index.md
├── logs/
├── consolidated_metadata.json
├── catalog.index.json
└── .step1_complete
```

### Backward Compatibility
- If users call `run_iteration.sh` with no flags:
  - Keep existing three-step flow.
  - Do not rotate `OUTPUT_DIR` if already present in `.env`.
  - If `OUTPUT_DIR` is missing in `.env`, create a timestamped directory once.

### Risks and Mitigations
- Risk: Users rely on per-run timestamped output directories.
  - Mitigation: Provide `--rotate-output` to retain previous behavior.
- Risk: Artifact freshness detection may be costly on large trees.
  - Mitigation: Default to presence marker check; make deep freshness check opt-in via `--check-freshness`.

### Acceptance Criteria
- Step1 is skipped when `.step1_complete` exists and not forced.
- Step2 and both Step3 modes can be re-run repeatedly without touching Step1.
- A comparison page is produced when running both Step3 modes.
- Docker Weaviate data persists across container restarts.


