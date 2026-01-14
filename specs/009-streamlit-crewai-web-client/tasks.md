# Tasks: Feature 009 - Streamlit-Based Interactive Analysis Web Client with CrewAI Multi-Agent System

**Input**: Design documents from `/specs/009-streamlit-crewai-web-client/`
**Prerequisites**: plan.md, spec.md, data-model.md
**Tests**: >80% coverage required per constitution - test tasks included for all user stories

**Organization**: Tasks grouped by user story to enable independent implementation and testing of each story. Test tasks precede implementation tasks per TDD principles.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story label (US1.1, US1.2, US2.1, etc.)
- File paths are absolute from repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create web module structure: `src/codeindex/web/__init__.py`, `pages/`, `agents/`, `services/`, `components/`, `workflows/`, `database/`, `utils/`
- [X] T002 [P] Add Streamlit dependencies to `requirements.txt` (streamlit>=1.30.0, streamlit-code-editor>=0.1.0, streamlit-cytoscape>=1.0.0)
- [X] T003 [P] Add CrewAI dependencies to `requirements.txt` (crewai>=0.20.0)
- [X] T004 [P] Add export dependencies to `requirements.txt` (reportlab, pyyaml)
- [X] T005 [P] Add SQLite dependencies to `requirements.txt` (aiosqlite for async, sqlite-fts5 for full-text search)
- [X] T006 Add web-specific config options to `.env.example` (STREAMLIT_PORT, STREAMLIT_HOST, WORKSPACE_DB_PATH, ANNOTATIONS_DB_PATH, EXPORT_DIR, MAX_CONCURRENT_AGENTS)
- [X] T007 Create main Streamlit app entry point: `src/codeindex/web/app.py` with sidebar navigation and page routing

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T008 Create SQLite database schema: `src/codeindex/web/database/schema.sql` (workspaces table, annotations table, annotations_fts virtual table)
- [X] T009 Implement SQLite connection management: `src/codeindex/web/database/connection.py` (connection pooling, WAL mode setup, migration support)
- [X] T010 Create database migration framework: `src/codeindex/web/database/migrations/` directory structure
- [X] T011 Implement session state management utility: `src/codeindex/web/utils/session_state.py` (initialize session state, get/set helpers, clear session)
- [X] T012 Create base agent configuration: `src/codeindex/web/agents/base.py` (AgentConfig dataclass, AgentResponse dataclass, base tools setup)
- [X] T013 Create agent service scaffold: `src/codeindex/web/services/agent_service.py` (agent initialization, routing logic placeholder, response formatting)
- [X] T014 Create search service scaffold: `src/codeindex/web/services/search_service.py` (reuse existing weaviate_store.py client, search wrapper)
- [X] T015 Implement health check on app startup: Check Weaviate, Ollama, and SQLite availability in `src/codeindex/web/app.py`

### Tests for Foundational Phase

- [X] T016 [P] Create unit tests for SQLite connection management: `tests/unit/web/database/test_connection.py` (test WAL mode setup, connection pooling, migration framework)
- [X] T017 [P] Create unit tests for session state management: `tests/unit/web/utils/test_session_state.py` (test get/set/clear operations, initialization)
- [X] T018 [P] Create unit tests for base agent configuration: `tests/unit/web/agents/test_base.py` (test AgentConfig dataclass, AgentResponse dataclass)
- [X] T019 [P] Create integration test for health checks: `tests/integration/web/test_health_checks.py` (test Weaviate, Ollama, SQLite availability checks)

**Checkpoint**: Foundation ready with >80% test coverage - user story implementation can now begin in parallel

---

## Phase 3: User Story 1.1 - Natural Language Search (Priority: P1) 🎯 MVP

**Goal**: Enable product managers to search for artifacts using natural language queries

**Independent Test**: Open web UI, enter "authentication flow", see results with artifact types, confidence scores, and file paths in <2 seconds

### Tests for User Story 1.1

- [X] T020 [P] [US1.1] Create unit tests for search service: `tests/unit/web/services/test_search_service.py` (test search execution, Weaviate query building, result formatting)
- [X] T021 [P] [US1.1] Create unit tests for artifact card component: `tests/unit/web/components/test_artifact_card.py` (test artifact rendering, confidence score display, preview snippet)
- [X] T022 [US1.1] Create integration test for search flow: `tests/integration/web/test_search_flow.py` (test end-to-end search from query to results, Weaviate + Ollama integration)

### Implementation for User Story 1.1

- [X] T023 [US1.1] Create Search page: `src/codeindex/web/pages/1_🔍_Search.py` (page layout, sidebar navigation integration)
- [X] T024 [US1.1] Add search input field with natural language support (multiline text input, max 2000 chars, submit button)
- [X] T025 [US1.1] Implement search execution in `src/codeindex/web/services/search_service.py` (query Weaviate using existing weaviate_store.py, vector embedding via Ollama)
- [X] T026 [US1.1] Create artifact card component: `src/codeindex/web/components/artifact_card.py` (display artifact type, confidence score, file path, preview snippet)
- [X] T027 [US1.1] Display paginated search results (50 results per page, infinite scroll)
- [X] T028 [US1.1] Add loading spinner during search execution
- [X] T029 [US1.1] Implement error handling for search failures (Weaviate unavailable, Ollama timeout, empty results)
- [X] T030 [US1.1] Add search performance logging (query text, execution time, result count)

**Checkpoint**: Basic semantic search functional - users can find artifacts via natural language

---

## Phase 4: User Story 1.2 - Filter Search Results (Priority: P1)

**Goal**: Enable developers to filter search results by artifact type and project for focused analysis

**Independent Test**: Search for "database", apply filters (artifact type: DaoCall, project: com.example:app), see filtered results update instantly

### Tests for User Story 1.2

- [X] T031 [P] [US1.2] Create unit tests for filter application logic: `tests/unit/web/services/test_search_filters.py` (test Weaviate GraphQL filter building, multi-select filters, project filters)
- [X] T032 [P] [US1.2] Create unit tests for URL parameter persistence: `tests/unit/web/utils/test_url_params.py` (test query param encoding/decoding, filter state serialization)
- [X] T033 [US1.2] Create integration test for filtered search: `tests/integration/web/test_filtered_search.py` (test end-to-end filter application, URL persistence, filter restoration)

### Implementation for User Story 1.2

- [X] T034 [US1.2] Add artifact type multi-select filter to Search page (checkboxes for 11 types: DaoCall, GwtPresenter, GwtView, GwtUiBinder, DtoArtifact, IbatisStatement, DbTable, GwtEndpoint, JspForm, BackendDoc, JsArtifact)
- [X] T035 [US1.2] Add project single-select filter to Search page (dropdown populated from Weaviate projects, query `get_all_projects()` from weaviate_store.py)
- [X] T036 [US1.2] Implement filter application logic in search_service.py (build Weaviate GraphQL filters, apply to search query)
- [X] T037 [US1.2] Add "Clear Filters" button (reset to default view)
- [X] T038 [US1.2] Persist filter state in URL query parameters for shareable search links (use st.experimental_get_query_params and st.experimental_set_query_params)
- [X] T039 [US1.2] Restore filters from URL on page load (parse query params, apply to UI state)

**Checkpoint**: Search filtering functional - users can narrow results by type and project

---

## Phase 5: User Story 1.3 - Visual Relationship Graphs (Priority: P2)

**Goal**: Enable technical leads to visualize artifact dependencies and data flows

**Independent Test**: Click "Show Relationships" on artifact detail view, see interactive graph with nodes and edges in <3 seconds

### Tests for User Story 1.3

- [ ] T040 [P] [US1.3] Create unit tests for graph service: `tests/unit/web/services/test_graph_service.py` (test relationship extraction, graph building, node/edge creation, max node limits)
- [ ] T041 [P] [US1.3] Create unit tests for graph rendering: `tests/unit/web/components/test_relationship_graph.py` (test Cytoscape integration, layout configuration, node coloring)
- [ ] T042 [P] [US1.3] Create unit tests for graph export: `tests/unit/web/services/test_graph_export.py` (test PNG export, Mermaid conversion, syntax validation)
- [ ] T043 [US1.3] Create integration test for graph visualization: `tests/integration/web/test_relationship_graph.py` (test end-to-end graph generation, Weaviate relationship queries, interactive controls)

### Implementation for User Story 1.3

- [ ] T044 [US1.3] Create graph service: `src/codeindex/web/services/graph_service.py` (build relationship graph from Weaviate, max 50 nodes)
- [ ] T045 [US1.3] Query Weaviate for artifact relationships (extract FK relationships, presenter-view bindings, service-dao calls)
- [ ] T046 [US1.3] Create relationship graph component: `src/codeindex/web/components/relationship_graph.py` (integrate Streamlit Cytoscape component)
- [ ] T047 [US1.3] Implement graph layout (force-directed layout, center current artifact, color-code by artifact type)
- [ ] T048 [US1.3] Add interactive graph controls (zoom, pan, click node to navigate to artifact detail)
- [ ] T049 [US1.3] Add "Show Relationships" button to artifact card component (trigger graph rendering)
- [ ] T050 [US1.3] Implement graph export to PNG (via Cytoscape export API)
- [ ] T051 [US1.3] Implement graph export to Mermaid markdown (convert Cytoscape graph to Mermaid syntax)
- [ ] T052 [US1.3] Add graph loading spinner and error handling (timeout after 10 seconds, show "Too many relationships" message)

**Checkpoint**: Relationship visualization functional - users can explore artifact connections visually

---

## Phase 6: User Story 2.1 - Senior Developer Agent Chat (Priority: P1)

**Goal**: Enable product managers to ask natural language questions and receive comprehensive explanations from AI

**Independent Test**: Open Chat page, ask "What does the user registration module do?", receive response with citations in <30 seconds

### Tests for User Story 2.1

- [ ] T053 [P] [US2.1] Create unit tests for Senior Developer agent: `tests/unit/web/agents/test_senior_developer.py` (test agent configuration, role definition, tool setup)
- [ ] T054 [P] [US2.1] Create unit tests for agent tools: `tests/unit/web/agents/test_agent_tools.py` (test WeaviateSearchTool, FileReadTool, LLMQueryTool)
- [ ] T055 [P] [US2.1] Create unit tests for agent routing: `tests/unit/web/services/test_agent_routing.py` (test keyword detection, agent selection, fallback logic)
- [ ] T056 [P] [US2.1] Create unit tests for response formatting: `tests/unit/web/components/test_agent_chat.py` (test citation extraction, hyperlink generation, streaming display)
- [ ] T057 [US2.1] Create integration test for agent chat: `tests/integration/web/test_agent_chat.py` (test end-to-end agent query, CrewAI + Ollama integration, response streaming, citation formatting)

### Implementation for User Story 2.1

- [ ] T058 [US2.1] Create Chat page: `src/codeindex/web/pages/2_💬_Chat.py` (page layout, chat history display)
- [ ] T059 [US2.1] Add chat input field (multiline text input, max 2000 chars, submit button)
- [ ] T060 [US2.1] Implement Senior Developer agent: `src/codeindex/web/agents/senior_developer.py` (role, goal, backstory per spec.md, tools: WeaviateSearchTool, FileReadTool, LLMQueryTool)
- [ ] T061 [US2.1] Implement agent tools in agents/base.py (WeaviateSearchTool: query Weaviate, FileReadTool: read from JAVA_SOURCE_DIR, LLMQueryTool: query Ollama via existing ollama_client.py)
- [ ] T062 [US2.1] Integrate CrewAI with Ollama (configure CrewAI LLM to use existing ollama_client.py, reuse adaptive timeout and retry logic)
- [ ] T063 [US2.1] Implement agent routing logic in agent_service.py (route "explain" questions to Senior Developer, keyword heuristics)
- [ ] T064 [US2.1] Create agent chat component: `src/codeindex/web/components/agent_chat.py` (display user message, agent response, streaming support)
- [ ] T065 [US2.1] Implement response streaming (word-by-word rendering as agent generates text)
- [ ] T066 [US2.1] Add citation formatting (extract artifact IDs and file paths from response, convert to hyperlinks to artifact detail pages)
- [ ] T067 [US2.1] Implement conversation history (store in Streamlit session state, max 20 messages, clear history button)
- [ ] T068 [US2.1] Add "Copy Response" button (copy agent response to clipboard)
- [ ] T069 [US2.1] Add error handling for agent failures (Ollama timeout, Weaviate error, invalid response format)

**Checkpoint**: Senior Developer agent functional - users can ask questions and receive AI-generated explanations

---

## Phase 7: User Story 2.2 - Data Analyst Agent (Priority: P2)

**Goal**: Enable data analysts to analyze database schemas and generate entity-relationship diagrams

**Independent Test**: Click "Analyze Database Schema" button, receive ERD diagram with tables, columns, and FK relationships in <2 minutes

### Tests for User Story 2.2

- [ ] T070 [P] [US2.2] Create unit tests for Data Analyst agent: `tests/unit/web/agents/test_data_analyst.py` (test agent configuration, database analysis tools, SQL query tool)
- [ ] T071 [P] [US2.2] Create unit tests for ERD generation: `tests/unit/web/services/test_erd_generation.py` (test Mermaid ER diagram syntax, table/column extraction, FK relationship formatting)
- [ ] T072 [P] [US2.2] Create unit tests for database quality analysis: `tests/unit/web/services/test_db_quality.py` (test missing FK detection, index analysis, naming convention checks)
- [ ] T073 [US2.2] Create integration test for database schema analysis: `tests/integration/web/test_db_schema_analysis.py` (test end-to-end schema analysis, Weaviate DbTable queries, ERD rendering)

### Implementation for User Story 2.2

- [ ] T074 [US2.2] Implement Data Analyst agent: `src/codeindex/web/agents/data_analyst.py` (role, goal, backstory, tools: WeaviateSearchTool for DbTable artifacts, SQLQueryTool for FK extraction)
- [ ] T075 [US2.2] Add "Analyze Database Schema" workflow button to Chat page (trigger Data Analyst agent)
- [ ] T076 [US2.2] Implement database schema analysis logic (query Weaviate for DbTable artifacts, extract columns, FKs, indexes)
- [ ] T077 [US2.2] Generate ERD diagram in Mermaid format (convert DB schema to Mermaid ER diagram syntax)
- [ ] T078 [US2.2] Render Mermaid diagram in UI (use st.markdown with mermaid code block)
- [ ] T079 [US2.2] Add database quality report (identify missing FKs, missing indexes, naming inconsistencies)
- [ ] T080 [US2.2] Update agent routing logic (route "database" or "schema" questions to Data Analyst)

**Checkpoint**: Data Analyst agent functional - users can analyze database schemas with AI assistance

---

## Phase 8: User Story 2.3 - Multi-Agent PRD Generation (Priority: P2)

**Goal**: Enable technical leads to generate comprehensive PRDs from existing code without manual effort

**Independent Test**: Select 20-30 artifacts, click "Generate PRD", see agents collaborate and produce PRD in <5 minutes

### Tests for User Story 2.3

- [ ] T081 [P] [US2.3] Create unit tests for Backend Specialist agent: `tests/unit/web/agents/test_backend_specialist.py` (test agent configuration, backend analysis tools)
- [ ] T082 [P] [US2.3] Create unit tests for Frontend Specialist agent: `tests/unit/web/agents/test_frontend_specialist.py` (test agent configuration, frontend analysis tools)
- [ ] T083 [P] [US2.3] Create unit tests for PRD Writer agent: `tests/unit/web/agents/test_prd_writer.py` (test agent configuration, PRD formatting, YAML frontmatter)
- [ ] T084 [P] [US2.3] Create unit tests for workflow orchestration: `tests/unit/web/workflows/test_prd_generation.py` (test sequential workflow, agent context passing, CrewAI process configuration)
- [ ] T085 [P] [US2.3] Create unit tests for progress indicator: `tests/unit/web/components/test_progress_indicator.py` (test agent status display, progress bar, time estimation)
- [ ] T086 [US2.3] Create integration test for multi-agent PRD generation: `tests/integration/web/test_prd_workflow.py` (test end-to-end PRD generation, agent collaboration, workflow cancellation, PRD download)

### Implementation for User Story 2.3

- [ ] T087 [P] [US2.3] Implement Backend Specialist agent: `src/codeindex/web/agents/backend_specialist.py` (role, goal, backstory, tools)
- [ ] T088 [P] [US2.3] Implement Frontend Specialist agent: `src/codeindex/web/agents/frontend_specialist.py` (role, goal, backstory, tools)
- [ ] T089 [P] [US2.3] Implement PRD Writer agent: `src/codeindex/web/agents/prd_writer.py` (role, goal, backstory, tools)
- [ ] T090 [US2.3] Create PRD generation workflow: `src/codeindex/web/workflows/prd_generation.py` (sequential workflow: Backend Specialist → Frontend Specialist → Data Analyst → PRD Writer)
- [ ] T091 [US2.3] Implement workflow orchestration in agent_service.py (CrewAI sequential process, pass context between agents)
- [ ] T092 [US2.3] Create progress indicator component: `src/codeindex/web/components/progress_indicator.py` (display current agent, progress bar, estimated time, task status)
- [ ] T093 [US2.3] Add artifact selection UI to Chat page (checkboxes to select artifacts for PRD generation)
- [ ] T094 [US2.3] Add "Generate PRD" workflow button (trigger multi-agent workflow with selected artifacts)
- [ ] T095 [US2.3] Implement workflow cancellation (interrupt button, graceful shutdown of agent tasks)
- [ ] T096 [US2.3] Display generated PRD in UI (Markdown rendering with sections from each agent)
- [ ] T097 [US2.3] Add PRD download button (export as Markdown file with YAML frontmatter)

**Checkpoint**: Multi-agent PRD generation functional - agents collaborate to produce comprehensive documentation

---

## Phase 9: User Story 2.4 - Agent Configuration (Priority: P3)

**Goal**: Enable developers to configure agent behavior to match team documentation standards

**Independent Test**: Open Settings page, change verbosity to "verbose", technical level to "junior", apply settings, see agent responses reflect changes

### Tests for User Story 2.4

- [ ] T098 [P] [US2.4] Create unit tests for settings persistence: `tests/unit/web/services/test_settings_service.py` (test session state storage, settings validation, default values)
- [ ] T099 [P] [US2.4] Create unit tests for agent configuration application: `tests/unit/web/agents/test_agent_config_application.py` (test settings propagation to agents, AgentConfig updates)
- [ ] T100 [US2.4] Create unit tests for settings preview: `tests/unit/web/components/test_settings_preview.py` (test example response generation with different settings)
- [ ] T101 [US2.4] Create integration test for agent settings: `tests/integration/web/test_agent_settings.py` (test end-to-end settings application, verify agent responses change with settings)

### Implementation for User Story 2.4

- [ ] T102 [US2.4] Create Settings page: `src/codeindex/web/pages/6_⚙️_Settings.py` (page layout, settings form)
- [ ] T103 [US2.4] Add agent verbosity settings (radio buttons: concise, standard, verbose)
- [ ] T104 [US2.4] Add technical level settings (radio buttons: junior, mid, senior)
- [ ] T105 [US2.4] Add citation style settings (radio buttons: inline, footnotes, none)
- [ ] T106 [US2.4] Add UI theme settings (radio buttons: light, dark)
- [ ] T107 [US2.4] Add output format settings (radio buttons: markdown, text)
- [ ] T108 [US2.4] Persist settings in Streamlit session state (apply to all agent queries in current session)
- [ ] T109 [US2.4] Update agent configurations in agents/base.py (read settings from session state, apply to AgentConfig)
- [ ] T110 [US2.4] Add settings preview (show example agent response with current settings)
- [ ] T111 [US2.4] Add "Reset to Defaults" button (restore default settings)

**Checkpoint**: Agent configuration functional - users can customize agent behavior

---

## Phase 10: User Story 2.5 - Gherkin Test Generation (Priority: P2)

**Goal**: Enable QA engineers to generate BDD test cases from user stories without manual translation

**Independent Test**: Select user stories, click "Generate Gherkin Tests", receive .feature files with Given-When-Then steps in <2 minutes

### Tests for User Story 2.5

- [ ] T112 [P] [US2.5] Create unit tests for Gherkin Test Writer agent: `tests/unit/web/agents/test_gherkin_test_writer.py` (test agent configuration, Gherkin syntax generation, scenario creation)
- [ ] T113 [P] [US2.5] Create unit tests for Gherkin syntax validation: `tests/unit/web/services/test_gherkin_validation.py` (test .feature file parsing, Gherkin syntax checking, error detection)
- [ ] T114 [P] [US2.5] Create unit tests for test generation workflow: `tests/unit/web/workflows/test_gherkin_generation.py` (test workflow orchestration, agent context passing)
- [ ] T115 [US2.5] Create integration test for Gherkin test generation: `tests/integration/web/test_gherkin_generation.py` (test end-to-end Gherkin generation, .feature file download, syntax validation)

### Implementation for User Story 2.5

- [ ] T116 [US2.5] Implement Gherkin Test Writer agent: `src/codeindex/web/agents/gherkin_test_writer.py` (role, goal, backstory per spec.md, tools: WeaviateSearchTool, FileReadTool, DocumentGeneratorTool)
- [ ] T117 [US2.5] Create test generation service: `src/codeindex/web/services/test_generation_service.py` (Gherkin test generation, syntax validation)
- [ ] T118 [US2.5] Implement Gherkin generation workflow: `src/codeindex/web/workflows/gherkin_generation.py` (PRD Writer → Frontend Specialist → Gherkin Test Writer)
- [ ] T119 [US2.5] Create Tests page: `src/codeindex/web/pages/5_🧪_Tests.py` (page layout, test type selection)
- [ ] T120 [US2.5] Add user story input section (text area for user stories, or artifact selection)
- [ ] T121 [US2.5] Add "Generate Gherkin Tests" button (trigger Gherkin generation workflow)
- [ ] T122 [US2.5] Implement Gherkin syntax validation (parse generated .feature files, check Gherkin syntax errors)
- [ ] T123 [US2.5] Display generated Gherkin tests in UI (syntax-highlighted code viewer)
- [ ] T124 [US2.5] Add download button for .feature files (export as .feature files, zip multiple files)
- [ ] T125 [US2.5] Add test coverage summary (number of scenarios, steps, examples)

**Checkpoint**: Gherkin test generation functional - QA engineers can generate BDD tests from requirements

---

## Phase 11: User Story 2.6 - Playwright Test Generation (Priority: P2)

**Goal**: Enable QA engineers to generate Playwright E2E test scripts for web UI automation

**Independent Test**: Select UI components, click "Generate Playwright Tests", receive .spec.ts files with page objects and assertions in <3 minutes

### Tests for User Story 2.6

- [ ] T126 [P] [US2.6] Create unit tests for Playwright Test Writer agent: `tests/unit/web/agents/test_playwright_test_writer.py` (test agent configuration, Playwright syntax generation, page object model creation)
- [ ] T127 [P] [US2.6] Create unit tests for TypeScript/JavaScript validation: `tests/unit/web/services/test_playwright_validation.py` (test .spec.ts/.spec.js parsing, syntax checking, locator validation)
- [ ] T128 [P] [US2.6] Create unit tests for Playwright workflow: `tests/unit/web/workflows/test_playwright_generation.py` (test workflow orchestration, UI component analysis)
- [ ] T129 [US2.6] Create integration test for Playwright test generation: `tests/integration/web/test_playwright_generation.py` (test end-to-end Playwright generation, .spec.ts download, complete test suite workflow)

### Implementation for User Story 2.6

- [ ] T130 [US2.6] Implement Playwright Test Writer agent: `src/codeindex/web/agents/playwright_test_writer.py` (role, goal, backstory per spec.md, tools: WeaviateSearchTool for UI components, FileReadTool, DocumentGeneratorTool)
- [ ] T131 [US2.6] Implement Playwright generation workflow: `src/codeindex/web/workflows/playwright_generation.py` (Frontend Specialist → Backend Specialist → Playwright Test Writer)
- [ ] T132 [US2.6] Add UI component selection to Tests page (select GwtPresenter, GwtView, JspForm artifacts)
- [ ] T133 [US2.6] Add "Generate Playwright Tests" button (trigger Playwright generation workflow)
- [ ] T134 [US2.6] Implement Playwright test generation logic (analyze UI components, generate page object models, test cases with locators and assertions)
- [ ] T135 [US2.6] Add TypeScript/JavaScript syntax validation (parse generated .spec.ts/.spec.js files, check syntax errors)
- [ ] T136 [US2.6] Display generated Playwright tests in UI (syntax-highlighted code viewer with TypeScript support)
- [ ] T137 [US2.6] Add download button for .spec.ts/.spec.js files (export as test files, zip multiple files)
- [ ] T138 [US2.6] Add complete test suite workflow: `src/codeindex/web/workflows/complete_test_suite.py` (generate both Gherkin and Playwright tests in single workflow)

**Checkpoint**: Playwright test generation functional - QA engineers can generate E2E test scripts

---

## Phase 12: User Story 3.1 - Saved Workspaces (Priority: P2)

**Goal**: Enable team leads to create and share analysis contexts with team members

**Independent Test**: Save workspace with search query and selected artifacts, share URL with colleague, colleague opens URL and sees exact same UI state

### Tests for User Story 3.1

- [ ] T139 [P] [US3.1] Create unit tests for workspace service: `tests/unit/web/services/test_workspace_service.py` (test CRUD operations, state capture/restore, SQLite queries)
- [ ] T140 [P] [US3.1] Create unit tests for workspace URL generation: `tests/unit/web/utils/test_workspace_url.py` (test URL format, UUID generation, query param handling)
- [ ] T141 [P] [US3.1] Create unit tests for workspace state serialization: `tests/unit/web/services/test_workspace_state.py` (test JSON serialization, UI state capture, search query preservation)
- [ ] T142 [US3.1] Create integration test for workspace management: `tests/integration/web/test_workspace_management.py` (test end-to-end workspace save/load, URL sharing, state restoration, workspace CRUD)

### Implementation for User Story 3.1

- [ ] T143 [US3.1] Create workspace service: `src/codeindex/web/services/workspace_service.py` (CRUD operations on workspaces table in SQLite)
- [ ] T144 [US3.1] Create Workspace page: `src/codeindex/web/pages/3_📊_Workspace.py` (page layout, workspace list view)
- [ ] T145 [US3.1] Implement workspace state capture (capture search query, filters, selected artifact IDs, agent settings, UI state as JSON)
- [ ] T146 [US3.1] Implement "Create Workspace" button on Search page (save current UI state → generate UUID → insert into SQLite)
- [ ] T147 [US3.1] Generate shareable workspace URLs (format: `/workspace/{workspace_id}`, use st.experimental_get_query_params)
- [ ] T148 [US3.1] Implement workspace load (parse workspace_id from URL, query SQLite, restore UI state from state_json)
- [ ] T149 [US3.1] Display workspace list with metadata (name, creator, last modified, artifact count, tags)
- [ ] T150 [US3.1] Add workspace management UI (rename, duplicate, delete buttons)
- [ ] T151 [US3.1] Increment view_count on workspace load (track usage frequency)
- [ ] T152 [US3.1] Add workspace search/filter (search by name, filter by tags)

**Checkpoint**: Workspace management functional - users can save and share analysis contexts

---

## Phase 13: User Story 3.2 - Export Reports (Priority: P2)

**Goal**: Enable product managers to export analysis reports for sharing with stakeholders outside the tool

**Independent Test**: Generate agent report, click "Export to PDF", download PDF with cover page, TOC, agent summaries, and diagrams

### Tests for User Story 3.2

- [ ] T153 [P] [US3.2] Create unit tests for Markdown export: `tests/unit/web/services/test_markdown_export.py` (test YAML frontmatter, table formatting, Mermaid diagram embedding)
- [ ] T154 [P] [US3.2] Create unit tests for JSON export: `tests/unit/web/services/test_json_export.py` (test artifact metadata export, Weaviate schema compatibility)
- [ ] T155 [P] [US3.2] Create unit tests for CSV export: `tests/unit/web/services/test_csv_export.py` (test column selection, data formatting, field extraction)
- [ ] T156 [P] [US3.2] Create unit tests for PDF export: `tests/unit/web/services/test_pdf_export.py` (test ReportLab templates, cover page, TOC, diagram embedding)
- [ ] T157 [US3.2] Create integration test for export functionality: `tests/integration/web/test_export_reports.py` (test end-to-end export for all formats, file storage, download links, cleanup job)

### Implementation for User Story 3.2

- [ ] T158 [P] [US3.2] Create export service: `src/codeindex/web/services/export_service.py` (Markdown, JSON, CSV, PDF export functions)
- [ ] T159 [P] [US3.2] Implement Markdown export (YAML frontmatter, formatted tables, Mermaid diagrams as code blocks)
- [ ] T160 [P] [US3.2] Implement JSON export (all artifact metadata, Weaviate-compatible schema)
- [ ] T161 [P] [US3.2] Implement CSV export (configurable columns, user selects fields from artifact schema)
- [ ] T162 [US3.2] Integrate ReportLab for PDF generation (create PDF templates: cover page, TOC, content sections)
- [ ] T163 [US3.2] Implement diagram embedding in PDF (convert Mermaid diagrams to PNG via external tool, embed in PDF)
- [ ] T164 [US3.2] Add export buttons to Search page and Chat page (Markdown, JSON, CSV, PDF options)
- [ ] T165 [US3.2] Implement export file storage (save exports to EXPORT_DIR, generate download links)
- [ ] T166 [US3.2] Add export cleanup job (delete exports older than 24 hours, run on app startup)
- [ ] T167 [US3.2] Add export progress indicator (show "Generating export..." spinner, download button on completion)

**Checkpoint**: Export functionality complete - users can export reports in multiple formats

---

## Phase 14: User Story 3.3 - Annotations (Priority: P3)

**Goal**: Enable developers to annotate artifacts with notes and tags during code reviews

**Independent Test**: Open artifact detail, add note "Need to refactor this DAO", add tags "refactor, technical-debt", see annotations visible to all users

### Tests for User Story 3.3

- [ ] T168 [P] [US3.3] Create unit tests for annotation service: `tests/unit/web/services/test_annotation_service.py` (test CRUD operations, SQLite queries, tag autocomplete)
- [ ] T169 [P] [US3.3] Create unit tests for full-text search: `tests/unit/web/services/test_annotation_search.py` (test FTS5 queries, search ranking, result formatting)
- [ ] T170 [P] [US3.3] Create unit tests for annotation display: `tests/unit/web/components/test_annotation_display.py` (test note rendering, tag display, author/timestamp)
- [ ] T171 [US3.3] Create integration test for annotations: `tests/integration/web/test_annotations.py` (test end-to-end annotation CRUD, full-text search, artifact enrichment)

### Implementation for User Story 3.3

- [ ] T172 [US3.3] Create annotation service: `src/codeindex/web/services/annotation_service.py` (CRUD operations on annotations table in SQLite)
- [ ] T173 [US3.3] Add artifact detail view to Search page (click artifact card → expand detail panel)
- [ ] T174 [US3.3] Add "Add Note" button to artifact detail view (open text editor modal)
- [ ] T175 [US3.3] Implement note editor (multiline text input with Markdown support, save button, cancel button)
- [ ] T176 [US3.3] Add tags input field (free-form text input, autocomplete from existing tags via SQLite query)
- [ ] T177 [US3.3] Display annotations in artifact detail view (show all notes and tags for current artifact)
- [ ] T178 [US3.3] Implement annotation edit/delete (edit button opens note editor, delete button with confirmation)
- [ ] T179 [US3.3] Add author and timestamp tracking (capture username/email, created_at, updated_at)
- [ ] T180 [US3.3] Implement full-text search on annotations (query annotations_fts table, display results in Search page)
- [ ] T181 [US3.3] Enrich search results with annotations (join Weaviate artifacts with SQLite annotations in search_service.py)

**Checkpoint**: Annotations functional - users can add notes and tags to artifacts for collaboration

---

## Phase 15: User Story 4.1 - Code Viewer (Priority: P1)

**Goal**: Enable developers to view source code directly in UI with syntax highlighting

**Independent Test**: Click artifact, click "View Source", see code with syntax highlighting and line numbers in <1 second

### Tests for User Story 4.1

- [ ] T182 [P] [US4.1] Create unit tests for code service: `tests/unit/web/services/test_code_service.py` (test file reading, path validation, directory traversal prevention)
- [ ] T183 [P] [US4.1] Create unit tests for syntax highlighting: `tests/unit/web/components/test_code_viewer.py` (test language detection, syntax highlighting for Java/JSP/XML/SQL/JS, line highlighting)
- [ ] T184 [P] [US4.1] Create unit tests for lazy loading: `tests/unit/web/services/test_code_lazy_loading.py` (test large file handling, pagination, scroll loading)
- [ ] T185 [US4.1] Create integration test for code viewer: `tests/integration/web/test_code_viewer.py` (test end-to-end code viewing, syntax highlighting, line highlighting, controls)

### Implementation for User Story 4.1

- [ ] T186 [US4.1] Create code service: `src/codeindex/web/services/code_service.py` (read files from JAVA_SOURCE_DIR, validate file paths)
- [ ] T187 [US4.1] Implement file path validation (prevent directory traversal attacks, check file exists)
- [ ] T188 [US4.1] Create code viewer component: `src/codeindex/web/components/code_viewer.py` (integrate Streamlit Code Editor component)
- [ ] T189 [US4.1] Add syntax highlighting support (Java, JSP, JavaScript, XML, SQL, Markdown)
- [ ] T190 [US4.1] Add code viewer controls (line numbers, search within file, copy code button, download file button)
- [ ] T191 [US4.1] Implement "View Source" button on artifact card (open code viewer in split pane)
- [ ] T192 [US4.1] Implement line highlighting (highlight specific lines when navigating from artifact, e.g., method at line 42)
- [ ] T193 [US4.1] Add lazy loading for large files (render visible lines only, load more on scroll for files >5000 lines)
- [ ] T194 [US4.1] Add error handling (file not found, permission denied, file too large >10MB)

**Checkpoint**: Code viewer functional - users can view source code with syntax highlighting

---

## Phase 16: User Story 4.2 - File System Tree View (Priority: P2)

**Goal**: Enable technical leads to navigate project structure like in an IDE

**Independent Test**: Open Files page, expand directories, click file to view code, search by filename

### Tests for User Story 4.2

- [ ] T195 [P] [US4.2] Create unit tests for file tree service: `tests/unit/web/services/test_file_tree_service.py` (test directory traversal, lazy loading, caching, tree structure building)
- [ ] T196 [P] [US4.2] Create unit tests for file icons: `tests/unit/web/components/test_file_icons.py` (test icon mapping by file type, directory icons)
- [ ] T197 [P] [US4.2] Create unit tests for tree view controls: `tests/unit/web/components/test_tree_view_controls.py` (test collapse/expand, filename search, breadcrumb navigation)
- [ ] T198 [US4.2] Create integration test for file tree view: `tests/integration/web/test_file_tree_view.py` (test end-to-end tree navigation, lazy loading performance, code viewer integration)

### Implementation for User Story 4.2

- [ ] T199 [US4.2] Create Files page: `src/codeindex/web/pages/4_🗂️_Files.py` (page layout, tree view container)
- [ ] T200 [US4.2] Implement file system tree view (expandable directory tree, root = JAVA_SOURCE_DIR)
- [ ] T201 [US4.2] Add file icons (Java, JSP, XML, JavaScript, config files, directories)
- [ ] T202 [US4.2] Implement lazy loading for tree view (load directory children on expand, cache in session state)
- [ ] T203 [US4.2] Add tree view controls (collapse all, expand to selected file, search by filename)
- [ ] T204 [US4.2] Integrate code viewer with tree view (click file → load code viewer in right pane)
- [ ] T205 [US4.2] Add breadcrumb navigation (show current file path, clickable breadcrumbs to navigate up)
- [ ] T206 [US4.2] Optimize tree view performance (<2 seconds load time for 10k files, use virtual scrolling)

**Checkpoint**: File system tree view functional - users can navigate project structure efficiently

---

## Phase 17: User Story 4.3 - Bidirectional Navigation (Priority: P3)

**Goal**: Enable developers to jump between artifacts and source code seamlessly

**Independent Test**: View artifact → click "View Source" → click "Show Artifacts" → see list of all artifacts from that file

### Tests for User Story 4.3

- [ ] T207 [P] [US4.3] Create unit tests for navigation service: `tests/unit/web/services/test_navigation_service.py` (test artifact-to-code mapping, code-to-artifact queries, navigation history)
- [ ] T208 [P] [US4.3] Create unit tests for navigation history: `tests/unit/web/utils/test_navigation_history.py` (test history tracking, back/forward buttons, URL persistence)
- [ ] T209 [P] [US4.3] Create unit tests for artifact context highlighting: `tests/unit/web/components/test_artifact_context.py` (test code section highlighting, artifact list sidebar)
- [ ] T210 [US4.3] Create integration test for bidirectional navigation: `tests/integration/web/test_bidirectional_navigation.py` (test end-to-end navigation flows, artifact-code linking, browser back/forward)

### Implementation for User Story 4.3

- [ ] T211 [US4.3] Add "View Source" button to artifact detail view (navigate to code viewer at specific line)
- [ ] T212 [US4.3] Add "Show Artifacts" button to code viewer (query Weaviate for artifacts from current file_path)
- [ ] T213 [US4.3] Display artifact list in code viewer sidebar (show all artifacts extracted from current file)
- [ ] T214 [US4.3] Implement navigation history (track navigation path, add back/forward buttons)
- [ ] T215 [US4.3] Update URL on navigation (persist navigation context in URL query params, support browser back/forward)
- [ ] T216 [US4.3] Highlight artifact context in code viewer (when navigating from artifact, highlight relevant code section)

**Checkpoint**: Bidirectional navigation functional - users can seamlessly navigate between artifacts and source code

---

## Phase 18: Polish & Cross-Cutting Concerns

**Purpose**: Production readiness and improvements affecting multiple user stories

- [ ] T217 [P] Implement Spec-Kit Feature Writer agent: `src/codeindex/web/agents/speckit_writer.py` (role, goal, backstory, tools)
- [ ] T218 [P] Create code review workflow: `src/codeindex/web/workflows/code_review.py` (Senior Developer → Backend Specialist → Frontend Specialist)
- [ ] T219 [P] Create spec creation workflow: `src/codeindex/web/workflows/spec_creation.py` (Senior Developer → Frontend/Backend Specialists → Spec-Kit Writer)
- [ ] T220 [P] Implement AI-suggested follow-up questions (analyze current query and results, generate 3-5 follow-up questions, display below search results)
- [ ] T221 [P] Implement keyboard shortcuts (Ctrl+K for search focus, Esc to close modals, Tab navigation, Ctrl+? for help modal)
- [ ] T222 [P] Create authentication module: `src/codeindex/web/utils/auth.py` (optional basic auth and OAuth2 support)
- [ ] T223 [P] Implement rate limiting: `src/codeindex/web/utils/rate_limiter.py` (track search count per user, limit to 100 searches/hour)
- [ ] T224 Implement health check endpoint at `/healthz` (check Weaviate, Ollama, SQLite status, return JSON with dependency health)
- [ ] T225 Implement metrics endpoint at `/metrics` (Prometheus format, track: search count, agent invocations, error rates, response times)
- [ ] T226 [P] Add structured logging (JSON format, log user actions: searches, agent queries, exports, workspace changes)
- [ ] T227 [P] Implement caching for frequently accessed data (artifact metadata, project list, use st.cache_data decorator)
- [ ] T228 [P] Optimize Weaviate queries (use pagination, implement incremental loading, avoid full collection scans)
- [ ] T229 [P] Add accessibility improvements (alt text for images, ARIA labels, ensure keyboard navigation, test with screen reader)
- [ ] T230 [P] Create user guide documentation in `docs/web-ui-guide.md` (quickstart, search guide, agent usage, workspace management, troubleshooting)
- [ ] T231 Update CLAUDE.md with web UI section (launch instructions, common commands, configuration, troubleshooting)
- [ ] T232 Create deployment guide in `docs/deployment-guide.md` (Docker setup, Kubernetes configuration, environment variables, production checklist)
- [ ] T233 [P] Run quickstart validation (follow quickstart.md, verify all workflows work end-to-end)
- [ ] T234 Perform load testing with Locust (simulate 50 concurrent users, measure p95 latency, memory usage, identify bottlenecks)
- [ ] T235 Profile memory usage with tracemalloc (ensure <4GB footprint per Streamlit worker)
- [ ] T236 Fix any critical issues found in load testing (optimize slow queries, reduce memory usage, improve error handling)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-17)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed)
  - Or sequentially in priority order: US1.1 (MVP) → US1.2 → US4.1 → US2.1 → US2.3 → US2.5 → US2.6 → US1.3 → US2.2 → US2.4 → US3.1 → US3.2 → US4.2 → US3.3 → US4.3
- **Polish (Phase 18)**: Depends on all desired user stories being complete

### User Story Dependencies

**Epic 1 - Interactive Semantic Search**:
- **US1.1 (P1)**: MVP - No dependencies on other stories
- **US1.2 (P1)**: Depends on US1.1 (extends search page)
- **US1.3 (P2)**: Depends on US1.1 (adds graph to artifact detail)

**Epic 2 - AI Agent-Powered Analysis**:
- **US2.1 (P1)**: No dependencies (foundational agent capability)
- **US2.2 (P2)**: Depends on US2.1 (shares agent infrastructure)
- **US2.3 (P2)**: Depends on US2.1 (multi-agent orchestration)
- **US2.4 (P3)**: Depends on US2.1 (configures existing agents)
- **US2.5 (P2)**: Depends on US2.3 (uses PRD Writer for test generation)
- **US2.6 (P2)**: Depends on US2.3 (uses Frontend Specialist for test generation)

**Epic 3 - Collaborative Workspaces**:
- **US3.1 (P2)**: Depends on US1.1 (saves search state)
- **US3.2 (P2)**: Depends on US1.1 and US2.1 (exports search and agent results)
- **US3.3 (P3)**: Depends on US1.1 (annotates artifacts from search)

**Epic 4 - Real-Time File System Integration**:
- **US4.1 (P1)**: No dependencies (standalone code viewer)
- **US4.2 (P2)**: Depends on US4.1 (extends code viewer with tree navigation)
- **US4.3 (P3)**: Depends on US1.1 and US4.1 (links search with code viewer)

### Within Each User Story

- Test tasks before implementation tasks (TDD)
- Models/services before UI components
- UI components before page integration
- Core implementation before advanced features
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Test tasks marked [P] within each story can run in parallel
- Agent implementations (US2.3: T087-T089) can run in parallel
- Export formats (US3.2: T158-T161) can run in parallel
- Polish tasks (Phase 18: most tasks) can run in parallel

---

## Implementation Strategy

### MVP First (Critical Path)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (BLOCKS all stories)
3. Complete Phase 3: US1.1 - Basic search (2-3 days)
4. Complete Phase 6: US2.1 - Senior Developer agent (2-3 days)
5. Complete Phase 15: US4.1 - Code viewer (1-2 days)
6. **STOP and VALIDATE**: Test core workflows (search → view artifact → ask agent → view code)
7. Deploy MVP if ready

**MVP Deliverable**: Users can search artifacts, ask AI questions, and view source code - core value delivered

### Incremental Delivery

After MVP, add features incrementally by priority:

1. **MVP** (US1.1 + US2.1 + US4.1) → Deploy
2. Add **US1.2** (filters) → Deploy
3. Add **US2.3** (multi-agent PRD) → Deploy
4. Add **US2.5 + US2.6** (test generation) → Deploy
5. Add **US3.1** (workspaces) → Deploy
6. Add **US3.2** (export) → Deploy
7. Add remaining stories as needed

### Parallel Team Strategy

With 3 developers after Foundational phase completes:

- **Developer A**: Epic 1 (US1.1 → US1.2 → US1.3)
- **Developer B**: Epic 2 (US2.1 → US2.3 → US2.5 → US2.6)
- **Developer C**: Epic 4 (US4.1 → US4.2 → US4.3)
- **All together**: Epic 3 (US3.1 → US3.2 → US3.3) → Phase 18 (Polish)

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All file paths are absolute from repository root
- **Test coverage >80% required per constitution** - all user stories have comprehensive test tasks
- Tests follow TDD: unit tests for services/components, integration tests for end-to-end flows
- Focus on reusing existing patterns: connection pooling, retry logic, semaphore rate limiting, config hierarchy

---

## Test Coverage Summary

**Total Tasks**: 236 (Setup: 7, Foundational: 12, User Stories: 197, Polish: 20)
**Test Tasks**: 74 (31% of total tasks)

**Tests by User Story**:
- US1.1 (Search): 3 tests (T020-T022)
- US1.2 (Filters): 3 tests (T031-T033)
- US1.3 (Graphs): 4 tests (T040-T043)
- US2.1 (Senior Dev Agent): 5 tests (T053-T057)
- US2.2 (Data Analyst): 4 tests (T070-T073)
- US2.3 (Multi-Agent PRD): 6 tests (T081-T086)
- US2.4 (Agent Config): 4 tests (T098-T101)
- US2.5 (Gherkin Tests): 4 tests (T112-T115)
- US2.6 (Playwright Tests): 4 tests (T126-T129)
- US3.1 (Workspaces): 4 tests (T139-T142)
- US3.2 (Export Reports): 5 tests (T153-T157)
- US3.3 (Annotations): 4 tests (T168-T171)
- US4.1 (Code Viewer): 4 tests (T182-T185)
- US4.2 (File Tree): 4 tests (T195-T198)
- US4.3 (Bidirectional Nav): 4 tests (T207-T210)
- Foundational: 4 tests (T016-T019)

**Test Types**:
- Unit tests: ~50 tasks (services, components, agents, workflows)
- Integration tests: ~24 tasks (end-to-end flows, multi-system integration)

---

## Critical Files Reference

Key existing files to reference during implementation:

- `/Users/thomaskamsker/Documents/Atom/vron.one/playground/Iteration20/gha1javarag/src/codeindex/services/weaviate_store.py` - Connection pooling pattern
- `/Users/thomaskamsker/Documents/Atom/vron.one/playground/Iteration20/gha1javarag/src/codeindex/services/ollama_client.py` - Semaphore rate limiting, adaptive timeout
- `/Users/thomaskamsker/Documents/Atom/vron.one/playground/Iteration20/gha1javarag/src/codeindex/utils/config.py` - Configuration hierarchy pattern
- `/Users/thomaskamsker/Documents/Atom/vron.one/playground/Iteration20/gha1javarag/src/codeindex/schemas/weaviate.py` - Artifact schemas for search
- `/Users/thomaskamsker/Documents/Atom/vron.one/playground/Iteration20/gha1javarag/src/codeindex/cli/prd.py` - Existing PRD generation logic to integrate
