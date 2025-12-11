# Tasks: GEMINI Code Analysis and PRD Generator

**Input**: Design documents from `specs/001-gemini-pipeline/`
**Prerequisites**: plan.md, prd.md, research.md, data-model.md, contracts/

**Tests**: Included as `pytest` is a specified dependency.

**Organization**: Tasks are grouped by CLI feature (user story) to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure.

- [x] T001 Create project directories: `src/`, `tests/`, `output/`
- [x] T002 Create empty `__init__.py` in `src/` and `tests/`
- [x] T003 Create `requirements.txt` with initial dependencies: `click`, `weaviate-client`, `ollama`, `pytest`, `python-dotenv`
- [x] T004 Create `.env.example` file with `JAVA_SOURCE_DIR=`
- [x] T005 Create `config/settings.py` for application configuration

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure for the CLI application.

- [x] T006 Create `src/common/models.py` for data models from `data-model.md`
- [x] T007 Create `src/main.py` with a basic Click group structure.
- [x] T008 Implement basic logging configuration in `src/common/logging.py`
- [x] T009 Create `tests/unit/test_main.py` to test basic CLI invocation.

**Checkpoint**: Foundation ready - CLI can be run and shows help.

---

## Phase 3: User Story 1 - `discover` command (Priority: P1) 🎯 MVP

**Goal**: Implement the `discover` command to find relevant files in a project.

**Independent Test**: Run `python main.py discover --project test-project` and verify it creates a structured list of files.

### Tests for User Story 1 ⚠️

- [x] T010 [P] [US1] Create `tests/unit/test_discovery.py` to test file discovery logic.

### Implementation for User Story 1

- [x] T011 [US1] Create `src/discovery/` directory with `__init__.py`.
- [x] T012 [US1] Implement file discovery logic in `src/discovery/discover_files.py`.
- [x] T013 [US1] Add the `discover` command to `src/main.py` and call the discovery logic.

**Checkpoint**: `discover` command is functional and independently testable.

---

## Phase 4: User Story 2 - `extract` command (Priority: P2)

**Goal**: Implement the `extract` command to parse files and create artifacts.

**Independent Test**: Run `python main.py extract --project test-project` and verify it creates structured artifacts.

### Tests for User Story 2 ⚠️

- [x] T014 [P] [US2] Create `tests/unit/test_extraction.py` for parsing different file types.

### Implementation for User Story 2

- [x] T015 [US2] Create `src/extraction/` directory with `__init__.py`.
- [x] T016 [US2] Implement artifact extraction logic in `src/extraction/extract_artifacts.py`.
- [x] T017 [US2] Add the `extract` command to `src/main.py` and call the extraction logic.

**Checkpoint**: `extract` command is functional and independently testable.

---

## Phase 5: User Story 3 - `index` command (Priority: P3)

**Goal**: Implement the `index` command to store artifacts in Weaviate.

**Independent Test**: Run `python main.py index --project test-project` and verify artifacts are in Weaviate.

### Tests for User Story 3 ⚠️

- [x] T018 [P] [US3] Create `tests/integration/test_indexing.py` to test Weaviate integration.

### Implementation for User Story 3

- [x] T019 [US3] Create `src/indexing/` directory with `__init__.py`.
- [x] T020 [US3] Implement Weaviate client and indexing logic in `src/indexing/index_artifacts.py`.
- [x] T021 [US3] Add the `index` command to `src/main.py` and call the indexing logic.

**Checkpoint**: `index` command is functional and independently testable.

---

## Phase 6: User Story 4 - `search` command (Priority: P4)

**Goal**: Implement the `search` command for natural language queries.

**Independent Test**: Run `python main.py search --project test-project --query "test"` and verify results.

### Tests for User Story 4 ⚠️

- [x] T022 [P] [US4] Create `tests/integration/test_search.py` to test search functionality.

### Implementation for User Story 4

- [x] T023 [US4] Create `src/search/` directory with `__init__.py`.
- [x] T024 [US4] Implement search logic in `src/search/search_artifacts.py`.
- [x] T025 [US4] Add the `search` command to `src/main.py` and call the search logic.

**Checkpoint**: `search` command is functional and independently testable.

---

## Phase 7: User Story 5 - `prd` command (Priority: P5)

**Goal**: Implement the `prd` command to generate PRD documents.

**Independent Test**: Run `python main.py prd --project test-project` and verify `prd.md` is created.

### Tests for User Story 5 ⚠️

- [x] T026 [P] [US5] Create `tests/unit/test_prd_generation.py` to test markdown generation.

### Implementation for User Story 5

- [x] T027 [US5] Create `src/prd/` directory with `__init__.py`.
- [x] T028 [US5] Implement PRD generation logic using Ollama in `src/prd/generate_prd.py`.
- [x] T029 [US5] Add the `prd` command to `src/main.py` and call the generation logic.

**Checkpoint**: `prd` command is functional and independently testable.

---

## Phase 8: User Story 6 - `all` command (Priority: P6)

**Goal**: Implement the `all` command to run the full pipeline.

**Independent Test**: Run `python main.py all --project test-project` and verify all stages complete successfully.

### Implementation for User Story 6

- [x] T030 [US6] Implement the `all` command in `src/main.py` to orchestrate the calls to discover, extract, index, and prd.

---

## Phase 9: Polish & Cross-Cutting Concerns

- [x] T031 [P] Add comprehensive CLI help text for all commands and options in `src/main.py`.
- [x] T032 [P] Enhance logging with more detailed progress indicators.
- [x] T033 Review and add comments to complex code sections.
- [x] T034 Create a `README.md` with full usage instructions, based on `quickstart.md`.
- [x] T035 Run `pytest` to ensure all tests pass.

---

## Dependencies & Execution Order

- **Setup (Phase 1)** and **Foundational (Phase 2)** must be completed first.
- User Stories can be implemented in the following order: `discover` -> `extract` -> `index` -> `search` / `prd`.
- `all` (US6) depends on all other user stories.

## Implementation Strategy

### MVP First (`discover` command)
1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (`discover`)
4. **STOP and VALIDATE**: Test the `discover` command independently.

### Incremental Delivery
1.  Complete MVP.
2.  Add `extract` (US2).
3.  Add `index` (US3).
4.  Add `search` (US4).
5.  Add `prd` (US5).
6.  Add `all` (US6).
7.  Complete Polish phase.
