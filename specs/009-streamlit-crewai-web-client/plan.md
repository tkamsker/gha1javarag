# Implementation Plan: Feature 009 - Streamlit-Based Interactive Analysis Web Client with CrewAI Multi-Agent System

**Branch**: `009-streamlit-crewai-web-client` | **Date**: 2026-01-14 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/009-streamlit-crewai-web-client/spec.md`

## Summary

This feature extends the GEMINI Code Analysis Pipeline from a CLI-only tool into an interactive web application with intelligent multi-agent capabilities. The implementation adds a Streamlit-based web interface enabling real-time code exploration, semantic search, and AI-powered analysis through 8 specialized CrewAI agents (Senior Developer, Data Analyst, Frontend/Backend Specialists, PRD Writer, Spec-Kit Writer, Gherkin Test Writer, Playwright Test Writer). The web UI democratizes access to the powerful analysis pipeline for non-CLI users while maintaining all existing CLI functionality.

**Technical Approach**: Build on existing infrastructure (Weaviate vector DB, Ollama LLM client, artifact schemas) by adding a new `src/codeindex/web/` module with Streamlit UI layer, CrewAI agent orchestration layer, and SQLite-based workspace/annotation persistence. Reuse proven patterns from existing services (connection pooling, retry logic, batch operations, concurrent processing with semaphores).

**Key Innovation**: Multi-agent collaboration workflows where specialized agents work together to generate comprehensive documentation (PRDs, specs, test cases) autonomously, significantly reducing manual effort for reverse-engineering existing codebases.

---

## Technical Context

**Language/Version**: Python 3.8+ (existing project requirement, type hints mandatory)

**Primary Dependencies**:
- Streamlit 1.30+ (web framework for rapid UI development)
- CrewAI 0.20+ (multi-agent orchestration framework)
- Ollama (existing LLM client - reuse existing integration)
- Weaviate 1.23+ (existing vector database - reuse existing client)
- SQLite 3.35+ (new - lightweight storage for workspaces and annotations)
- Streamlit Code Editor 0.1+ (syntax highlighting)
- Streamlit Cytoscape 1.0+ (interactive graph visualization)
- ReportLab (PDF generation)
- PyYAML (Markdown with YAML frontmatter)
- httpx (existing - HTTP client for Ollama/Weaviate)

**Storage**:
- Weaviate: Artifact storage (existing schemas, read-only from web UI)
- SQLite: Workspaces table, Annotations table (new, WAL mode for concurrency)
- File System: Source code files (read-only), export files (temporary, 24h TTL)

**Testing**:
- pytest (existing test framework)
- pytest-mock (existing - for mocking LLM calls)
- Streamlit AppTest (new - for UI component testing)
- pytest-asyncio (existing - for async timeout tests)

**Target Platform**: Linux/macOS server (Docker-ready for production deployment)

**Project Type**: Single project with new web module added to existing codebase

**Performance Goals**:
- Search query latency: <2 seconds (p95)
- Agent response latency: <30 seconds (p95) for single-agent queries
- Multi-agent workflow: <5 minutes for PRD generation (20-30 artifacts)
- Concurrent users: Support 50+ simultaneous users
- Memory footprint: <4GB per Streamlit worker process
- Page load time: <3 seconds initial app load

**Constraints**:
- Read-only access to Weaviate (no artifact create/update/delete from UI)
- Single Weaviate instance shared across users (no per-user isolation)
- Ollama model hardcoded to gemma3:12b (no runtime model switching)
- Desktop-first UI (mobile support best-effort)
- English language only (no i18n for MVP)

**Scale/Scope**:
- 100k+ artifact corpus supported
- 50+ concurrent users
- 8 specialized agents with distinct roles
- 6 pre-built multi-agent workflows
- 6 main UI pages (Search, Chat, Workspace, Files, Tests, Settings)

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Code Quality Standards

**Compliance**:
- ✅ Type Safety: All web modules, agents, and services will use type hints (Python 3.8+)
- ✅ Error Handling: Weaviate, Ollama, SQLite, and file I/O operations will have explicit error handling with user-friendly messages
- ✅ Code Organization: Web UI organized by layer (pages/, agents/, services/), separate from CLI
- ✅ Configuration Management: Follows existing priority (CLI args > env vars > .env > defaults)
- ✅ Documentation: All public functions will have docstrings; agent workflows will include inline comments

**Validation**: Code review checklist includes type hint verification, error handling for all external dependencies, and docstring completeness.

### Principle II: Testing Discipline

**Compliance**:
- ✅ Test Pyramid: Unit tests (agent logic, services), integration tests (Weaviate, SQLite, Ollama), E2E tests (user workflows)
- ✅ Test Isolation: Unit tests use mocks for Ollama/Weaviate; integration tests use test databases/collections
- ✅ Test Data: Fixtures for agent responses, sample artifacts, test workspaces
- ✅ Coverage Requirements: >80% for agent and service modules
- ✅ Test Performance: Unit tests <100ms, integration tests <5s, E2E tests marked with @pytest.mark.slow
- ⚠️ TDD: Agent routing logic and workflow orchestration will follow TDD approach

**Validation**: pytest coverage report must show >80% for `src/codeindex/web/agents/` and `src/codeindex/web/services/` modules.

### Principle III: User Experience Consistency

**Compliance**:
- ✅ CLI Design: Web UI does NOT replace CLI; CLI remains primary tool for pipeline execution
- ✅ Output Formats: Export supports Markdown (default), PDF, JSON, CSV for interoperability
- ✅ Logging: Structured logging with ERROR, WARNING, INFO, DEBUG levels; respects LOG_LEVEL
- ✅ Documentation: CLAUDE.md will include web UI usage guide, troubleshooting section, and quickstart
- ✅ Generated Artifacts: All exports include metadata (workspace ID, timestamp, generator version)

**Validation**: User guide includes working examples for all 6 main workflows. Error messages tested with non-technical users for clarity.

### Principle IV: Performance Requirements

**Compliance**:
- ✅ Search Performance: <2s p95 latency (reuses existing Weaviate client with connection pooling)
- ✅ Agent Performance: <30s single-agent response (Ollama timeout configuration reused from CLI)
- ✅ Memory Management: Streaming file reads, lazy rendering for large files, session state caching
- ✅ Resource Cleanup: Connection pooling for Weaviate/Ollama/SQLite; explicit connection closure
- ⚠️ Concurrency: Use existing semaphore pattern (MAX_CONCURRENT_AI_CALLS=5) for agent requests

**Validation**: Load testing with Locust framework (50 concurrent users); p95 latency monitoring; memory profiling with tracemalloc.

### Principle V: Observability & Monitoring

**Compliance**:
- ✅ Metrics Collection: Track search count, agent invocations, error rates, response times (per workflow)
- ✅ Diagnostic Tools: Health check endpoint (`/healthz`), metrics endpoint (`/metrics`) in Prometheus format
- ✅ Progress Tracking: Multi-agent workflows emit progress updates every 5 seconds
- ✅ Error Aggregation: Errors logged with context (user action, request ID, agent role, stack trace)
- ✅ Integration Health: Startup validation of Weaviate, Ollama, SQLite availability

**Validation**: Metrics endpoint returns valid Prometheus format. Health check validates all dependencies. Error logs include full context for debugging.

---

## Project Structure

### Documentation (this feature)

```text
specs/009-streamlit-crewai-web-client/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0 output (research unknowns)
├── data-model.md        # Phase 1 output (complete)
├── quickstart.md        # Phase 1 output (complete)
├── contracts/           # Phase 1 output (API schemas)
│   ├── agent-interfaces.md         # Agent tool interfaces
│   ├── workspace-schemas.sql       # SQLite table definitions
│   ├── agent-response-schema.json  # Agent response format
│   └── export-formats.md           # PDF/Markdown/JSON export specs
└── tasks.md             # Phase 2 output (NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
# Existing structure (unchanged)
src/codeindex/
├── cli/                 # Existing CLI commands (discover, extract, index, search, prd, diagram, status)
├── models/              # Existing data models (Project, CodeArtifact, ExtractionResult, DtoArtifact)
├── parsers/             # Existing parsers (Java, JSP, XML, SQL, GWT)
├── schemas/             # Existing Weaviate schemas (weaviate.py, dto_artifact_schema.py)
├── services/            # Existing services (discovery, extraction, indexing, ollama_client, weaviate_store)
└── utils/               # Existing utilities (config, retry, timeout_calculator, locking, metrics)

# NEW: Web UI module
src/codeindex/web/
├── __init__.py
├── app.py               # Main Streamlit app entry point
├── pages/               # Streamlit multi-page app structure
│   ├── 1_🔍_Search.py
│   ├── 2_💬_Chat.py
│   ├── 3_📊_Workspace.py
│   ├── 4_🗂️_Files.py
│   ├── 5_🧪_Tests.py
│   └── 6_⚙️_Settings.py
├── agents/              # CrewAI agent definitions
│   ├── __init__.py
│   ├── base.py          # Base agent configuration and tooling
│   ├── senior_developer.py
│   ├── data_analyst.py
│   ├── frontend_specialist.py
│   ├── backend_specialist.py
│   ├── prd_writer.py
│   ├── speckit_writer.py
│   ├── gherkin_test_writer.py
│   └── playwright_test_writer.py
├── services/            # Web-specific services
│   ├── __init__.py
│   ├── search_service.py       # Weaviate search with annotation enrichment
│   ├── agent_service.py        # Agent orchestration and routing
│   ├── workspace_service.py    # Workspace CRUD (SQLite)
│   ├── annotation_service.py   # Annotation CRUD (SQLite)
│   ├── export_service.py       # PDF, Markdown, JSON, CSV generation
│   ├── code_service.py         # File reading, syntax highlighting
│   ├── test_generation_service.py  # Gherkin and Playwright test generation
│   └── graph_service.py        # Relationship graph building
├── components/          # Reusable Streamlit components
│   ├── __init__.py
│   ├── artifact_card.py         # Artifact result display
│   ├── code_viewer.py           # Syntax-highlighted code viewer
│   ├── relationship_graph.py    # Cytoscape graph component
│   ├── agent_chat.py            # Chat interface component
│   └── progress_indicator.py    # Multi-agent workflow progress
├── workflows/           # CrewAI multi-agent workflows
│   ├── __init__.py
│   ├── prd_generation.py
│   ├── code_review.py
│   ├── spec_creation.py
│   ├── gherkin_generation.py
│   ├── playwright_generation.py
│   └── complete_test_suite.py
├── database/            # SQLite database management
│   ├── __init__.py
│   ├── schema.sql       # Table definitions
│   ├── migrations/      # Schema migration scripts
│   └── connection.py    # Connection pooling, WAL mode setup
└── utils/               # Web-specific utilities
    ├── __init__.py
    ├── session_state.py # Streamlit session state management
    ├── auth.py          # Optional authentication (basic auth, OAuth2)
    └── rate_limiter.py  # Rate limiting per user

# Existing tests structure (extended)
tests/
├── unit/
│   ├── test_agents/     # NEW: Agent logic tests (mocked LLM)
│   ├── test_web_services/  # NEW: Web service tests (mocked Weaviate/SQLite)
│   └── test_workflows/  # NEW: Workflow orchestration tests
├── integration/
│   ├── test_agent_ollama_integration.py  # NEW: Real Ollama calls
│   ├── test_weaviate_search_integration.py  # NEW: Real Weaviate queries
│   ├── test_sqlite_integration.py  # NEW: Real SQLite operations
│   └── test_export_integration.py  # NEW: PDF/Markdown generation
└── e2e/
    ├── test_search_workflow.py  # NEW: Selenium tests for search → view artifact
    ├── test_agent_workflow.py   # NEW: Selenium tests for chat → agent response
    └── test_prd_generation_workflow.py  # NEW: Multi-agent PRD generation
```

**Structure Decision**: Single project with new web module added to existing codebase. This aligns with the existing structure and avoids unnecessary separation. The web UI is logically a new interface layer on top of existing services, not a separate application. All existing CLI functionality remains unchanged and fully supported.

---

## Complexity Tracking

**No constitutional violations detected.** All requirements align with existing project principles and patterns.

---

## Phase 0: Research and Feasibility (1 week)

### Research Unknowns

The following areas require investigation before detailed design:

1. **CrewAI Framework Feasibility**
   - **Question**: Can CrewAI orchestrate 8 agents effectively with Ollama backend?
   - **Risk**: CrewAI may have limitations with local LLMs vs cloud APIs
   - **Validation**: Prototype 3-agent workflow (Senior Developer → Backend Specialist → PRD Writer) using existing Ollama client
   - **Success Criteria**: Agents can pass context between steps; workflow completes in <5 minutes for 20 artifacts

2. **Streamlit Performance with 50+ Users**
   - **Question**: Can Streamlit handle 50 concurrent users with <3s page load times?
   - **Risk**: Streamlit's reactive model may struggle with high concurrency
   - **Validation**: Load test prototype with Locust framework (simulate 50 users searching simultaneously)
   - **Success Criteria**: p95 search latency <2s; no memory leaks; CPU usage <80%

3. **SQLite Concurrency for Workspaces**
   - **Question**: Can SQLite handle concurrent writes (multiple users saving workspaces)?
   - **Risk**: SQLite may have write bottlenecks under high concurrency
   - **Validation**: Stress test SQLite in WAL mode (50 concurrent writers)
   - **Success Criteria**: Zero write failures; p95 write latency <100ms; no database locking errors

4. **Agent Routing Algorithm**
   - **Question**: How to route user questions to appropriate agent (keyword heuristics vs LLM classifier)?
   - **Risk**: Poor routing reduces agent response quality
   - **Validation**: Test 50 sample questions with keyword heuristics vs LLM-based routing
   - **Success Criteria**: >90% routing accuracy; routing decision <100ms

**Deliverable**: `research.md` document with findings, prototypes, and recommendations for each unknown.

---

## Phase 1: Foundation and Basic UI (2 weeks)

### Tasks

1. **Streamlit App Structure** (3 days)
   - Create `src/codeindex/web/app.py` main entry point
   - Set up multi-page app structure (`pages/` directory)
   - Implement navigation sidebar with page icons
   - Add session state management (`utils/session_state.py`)

2. **Basic Search Interface** (3 days)
   - Build Search page (`pages/1_🔍_Search.py`)
   - Add search input field with natural language support
   - Implement artifact type filters (multi-select checkboxes)
   - Implement project filter (dropdown populated from Weaviate)
   - Display paginated search results (50 per page)

3. **Weaviate Integration** (2 days)
   - Create `services/search_service.py`
   - Reuse existing `weaviate_store.py` client with connection pooling
   - Implement vector search with filters
   - Add result enrichment (join with annotations from SQLite)

4. **Code Viewer** (3 days)
   - Build Files page (`pages/4_🗂️_Files.py`)
   - Integrate Streamlit Code Editor component
   - Implement syntax highlighting (Java, JSP, JavaScript, XML, SQL)
   - Add file tree navigation (lazy loading for large directories)
   - Implement search within file

5. **Configuration Management** (2 days)
   - Add web-specific config options to `.env.example`
   - Create Settings page (`pages/6_⚙️_Settings.py`)
   - Implement runtime settings (agent verbosity, theme, page size)
   - Persist settings in Streamlit session state

### Success Criteria

- App launches at `http://localhost:8501` without errors
- Search returns results from Weaviate in <2 seconds
- Code viewer displays files with correct syntax highlighting
- File tree loads in <2 seconds for 10k files
- All pages navigate correctly via sidebar

### Deliverables

- Runnable Streamlit app with 3/6 pages functional (Search, Files, Settings)
- Unit tests for `search_service.py` (mocked Weaviate)
- Integration test for Weaviate search (real queries)
- Updated CLAUDE.md with web UI launch instructions

---

## Phase 2: Agent Framework Integration (2 weeks)

### Tasks

1. **CrewAI Setup** (2 days)
   - Add CrewAI to `requirements.txt`
   - Create `agents/base.py` with common agent configuration
   - Implement agent tools (WeaviateSearchTool, FileReadTool, LLMQueryTool)

2. **Agent Definitions** (4 days)
   - Implement 8 agent modules:
     - `agents/senior_developer.py`
     - `agents/data_analyst.py`
     - `agents/frontend_specialist.py`
     - `agents/backend_specialist.py`
     - `agents/prd_writer.py`
     - `agents/speckit_writer.py`
     - `agents/gherkin_test_writer.py`
     - `agents/playwright_test_writer.py`
   - Define role, goal, backstory for each agent
   - Configure tools (Weaviate search, file read, Ollama query)

3. **Chat Interface** (3 days)
   - Build Chat page (`pages/2_💬_Chat.py`)
   - Add multiline text input (max 2000 chars)
   - Implement agent routing logic (`services/agent_service.py`)
   - Display agent responses with streaming (word-by-word)
   - Maintain conversation history (session-scoped, max 20 messages)

4. **Ollama Integration** (2 days)
   - Reuse existing `ollama_client.py` (adaptive timeout, retry logic)
   - Configure agent LLM calls to use existing rate limiter (semaphore)
   - Implement response formatting (Markdown with citations)

5. **Testing** (3 days)
   - Unit tests for agent routing logic (keyword matching)
   - Unit tests for agent response formatting
   - Integration tests with real Ollama (short prompts only)
   - Mock tests for long-running agent queries

### Success Criteria

- User can ask questions in chat and receive relevant responses in <30 seconds
- Agent responses include citations (artifact IDs with hyperlinks)
- Chat maintains conversation context for follow-up questions
- All 8 agents accessible via chat interface
- No Ollama timeout errors (adaptive timeout works)

### Deliverables

- Chat page functional with 8 agents
- `services/agent_service.py` with routing logic
- Unit tests for agent logic (>80% coverage)
- Integration tests with Ollama (3 sample queries per agent)
- Updated CLAUDE.md with agent usage examples

---

## Phase 3: Multi-Agent Workflows (2 weeks)

### Tasks

1. **CrewAI Workflow Configuration** (3 days)
   - Implement sequential workflow pattern
   - Implement hierarchical workflow pattern (if needed)
   - Create workflow progress tracking (emit updates every 5 seconds)
   - Add cancellation support (interrupt button)

2. **Test Generation Service** (4 days)
   - Create `services/test_generation_service.py`
   - Implement Gherkin test generation (parse user stories, generate feature files)
   - Implement Playwright test generation (analyze UI components, generate test scripts)
   - Add syntax validation (Gherkin parser, TypeScript/JavaScript syntax checker)
   - Create Tests page (`pages/5_🧪_Tests.py`)

3. **Pre-Built Workflows** (5 days)
   - `workflows/prd_generation.py` (Backend → Frontend → Data Analyst → PRD Writer)
   - `workflows/code_review.py` (Senior Developer → Backend Specialist → Frontend Specialist)
   - `workflows/spec_creation.py` (Senior Developer → Frontend/Backend → Spec-Kit Writer)
   - `workflows/gherkin_generation.py` (PRD Writer → Frontend Specialist → Gherkin Test Writer)
   - `workflows/playwright_generation.py` (Frontend Specialist → Backend Specialist → Playwright Test Writer)
   - `workflows/complete_test_suite.py` (PRD Writer → Frontend → Backend → Gherkin + Playwright Writers)

4. **Workflow UI Components** (2 days)
   - Create `components/progress_indicator.py` (display current agent, progress bar, estimated time)
   - Add workflow selection dropdown (6 workflows)
   - Add artifact selection checkboxes (input for workflows)
   - Add workflow output preview (Markdown rendering)

### Success Criteria

- Multi-agent PRD generation completes in <5 minutes for 20-30 artifacts
- Gherkin test generation completes in <2 minutes for 10 user stories
- Playwright test generation completes in <3 minutes for 20 UI components
- Generated Gherkin files pass syntax validation (Cucumber parser)
- Generated Playwright files pass TypeScript/JavaScript syntax check
- Workflow progress updates every 5 seconds
- User can cancel workflow without app crash

### Deliverables

- 6 functional multi-agent workflows
- Tests page with test generation UI
- `services/test_generation_service.py` with syntax validation
- Unit tests for workflows (mocked agents)
- Integration tests for full workflows (real Ollama, short artifacts)
- Updated CLAUDE.md with workflow usage guide

---

## Phase 4: Visualization and Collaboration (2 weeks)

### Tasks

1. **Relationship Graph Visualization** (4 days)
   - Create `services/graph_service.py` (build graph from Weaviate relationships)
   - Integrate Streamlit Cytoscape component
   - Implement graph layout (force-directed, hierarchical)
   - Add interactive controls (zoom, pan, click node to navigate)
   - Add graph export (PNG, SVG, Mermaid markdown)

2. **SQLite Database Setup** (2 days)
   - Create `database/schema.sql` (workspaces, annotations tables)
   - Implement `database/connection.py` (connection pooling, WAL mode)
   - Add migration support (`database/migrations/`)

3. **Workspace Management** (3 days)
   - Create `services/workspace_service.py` (CRUD operations)
   - Build Workspace page (`pages/3_📊_Workspace.py`)
   - Implement workspace save (capture UI state → JSON → SQLite)
   - Implement workspace load (restore UI state from JSON)
   - Add workspace list view (name, creator, last modified, artifact count)
   - Generate shareable URLs (`/workspace/abc123`)

4. **Annotations** (3 days)
   - Create `services/annotation_service.py` (CRUD operations)
   - Add "Add Note" button to artifact detail view
   - Add "Add Tags" input with autocomplete (query existing tags)
   - Implement full-text search on annotations (SQLite FTS5)
   - Display annotations in artifact detail view

5. **Export Functionality** (2 days)
   - Create `services/export_service.py`
   - Implement Markdown export (YAML frontmatter, formatted tables, Mermaid diagrams)
   - Implement JSON export (all artifact metadata)
   - Implement CSV export (configurable columns)
   - Add export download buttons (browser download prompt)
   - Implement export cleanup (cron job to delete files >24h old)

### Success Criteria

- Relationship graphs render in <3 seconds for 50 nodes
- Workspaces persist across browser sessions
- Workspace URLs shareable (same URL restores exact UI state)
- Annotations visible to all users
- Full-text search on annotations returns results in <500ms
- Exports download in <10 seconds for 50-page reports

### Deliverables

- Workspace page functional with save/load/share
- Annotations feature integrated into artifact detail views
- Relationship graph visualization functional
- Export service with Markdown, JSON, CSV formats
- Unit tests for workspace and annotation services (mocked SQLite)
- Integration tests with real SQLite database

---

## Phase 5: Advanced Features and Polish (2 weeks)

### Tasks

1. **PDF Export** (4 days)
   - Integrate ReportLab library
   - Create PDF templates (cover page, TOC, content sections)
   - Implement diagram embedding (convert Mermaid to PNG via external tool)
   - Add PDF formatting (fonts, colors, page breaks)
   - Optimize PDF generation performance (<10s for 50 pages)

2. **File System Tree View** (2 days)
   - Implement lazy-loading tree component (render visible nodes only)
   - Add file icons (Java, JSP, XML, config)
   - Add search by filename
   - Add expand/collapse controls

3. **AI-Suggested Follow-Ups** (3 days)
   - Implement follow-up question generator (analyze current query + results)
   - Display 3-5 suggested questions after search results
   - Make suggestions clickable (auto-fill search box)

4. **Keyboard Shortcuts** (2 days)
   - Implement Ctrl+K for search focus
   - Implement Esc to close modals
   - Implement Tab navigation for accessibility
   - Add keyboard shortcut help modal (Ctrl+?)

5. **Accessibility Improvements** (3 days)
   - Audit WCAG 2.1 Level A compliance
   - Add alt text for images/icons
   - Ensure color contrast meets standards
   - Test keyboard navigation across all pages
   - Add ARIA labels where needed

### Success Criteria

- PDF exports include cover page, TOC, and embedded diagrams
- File tree loads in <2 seconds for 10k files
- Follow-up suggestions relevant to current query (manual validation)
- Keyboard shortcuts functional across all pages
- WCAG 2.1 Level A compliance verified by accessibility audit

### Deliverables

- PDF export functional
- File tree with lazy loading
- AI-suggested follow-ups feature
- Keyboard shortcuts implemented
- Accessibility audit report (all issues resolved)

---

## Phase 6: Production Readiness (2 weeks)

### Tasks

1. **Authentication** (3 days)
   - Implement optional basic auth (username/password)
   - Add OAuth2 support (optional, for enterprise)
   - Create login page (conditional on auth enabled)
   - Implement session management

2. **Rate Limiting** (2 days)
   - Create `utils/rate_limiter.py`
   - Track search count per user (SQLite or Redis)
   - Implement rate limit (100 searches per user per hour)
   - Display rate limit error message

3. **Health Check and Metrics** (3 days)
   - Implement `/healthz` endpoint (check Weaviate, Ollama, SQLite)
   - Implement `/metrics` endpoint (Prometheus format)
   - Track metrics: search count, agent invocations, error rates, response times
   - Add structured logging (JSON format)

4. **Performance Tuning** (3 days)
   - Implement caching (frequently accessed artifacts, project list)
   - Optimize Weaviate queries (pagination, filtering)
   - Profile memory usage (tracemalloc)
   - Optimize SQLite queries (indexes, query plans)

5. **Deployment Guide and Testing** (3 days)
   - Write Docker deployment guide
   - Write Kubernetes deployment guide (optional)
   - Run comprehensive E2E tests (50 concurrent users with Locust)
   - Validate performance requirements (p95 latency, memory usage)
   - Fix all critical issues found in load testing

### Success Criteria

- Authentication prevents unauthorized access (if enabled)
- Rate limiting blocks excessive requests (test with 200 searches/hour)
- Health check validates all dependencies (Weaviate, Ollama, SQLite)
- Metrics endpoint returns valid Prometheus format
- App handles 50 concurrent users without degradation (<20% response time increase)
- All E2E tests passing (10 critical user paths)

### Deliverables

- Authentication and rate limiting functional
- Health check and metrics endpoints implemented
- Deployment guide (Docker + Kubernetes)
- Performance tuning complete (caching, connection pooling)
- Load test report (50 concurrent users, p95 latency, memory usage)
- Updated CLAUDE.md with production deployment section

---

## Critical Files for Implementation

The following files are most critical for implementing this feature:

- **/Users/thomaskamsker/Documents/Atom/vron.one/playground/Iteration20/gha1javarag/src/codeindex/services/weaviate_store.py**
  - Reason: Core Weaviate client to reuse for search service; connection pooling pattern to replicate

- **/Users/thomaskamsker/Documents/Atom/vron.one/playground/Iteration20/gha1javarag/src/codeindex/services/ollama_client.py**
  - Reason: Existing LLM client with adaptive timeout, retry logic, and semaphore rate limiting to integrate with CrewAI agents

- **/Users/thomaskamsker/Documents/Atom/vron.one/playground/Iteration20/gha1javarag/src/codeindex/utils/config.py**
  - Reason: Configuration management pattern to extend with web-specific options

- **/Users/thomaskamsker/Documents/Atom/vron.one/playground/Iteration20/gha1javarag/src/codeindex/schemas/weaviate.py**
  - Reason: Artifact schemas to understand Weaviate data model for search and visualization

- **/Users/thomaskamsker/Documents/Atom/vron.one/playground/Iteration20/gha1javarag/src/codeindex/cli/prd.py**
  - Reason: Existing PRD generation logic to integrate with PRD Writer agent

---

**Version**: 1.0.0 | **Created**: 2026-01-14 | **Status**: Ready for Phase 0 Research
