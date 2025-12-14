# Implementation Plan: PRD Document Generation from Codebase Analysis

**Branch**: `002-prd-document-generation` | **Date**: 2025-12-14 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-prd-document-generation/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a PRD document generation system that analyzes Java codebases bottom-up (database → services → frontend → synthesis) to produce hierarchical documentation. The system leverages existing indexed artifacts from Feature 001, queries Weaviate for semantic context, uses Ollama LLM for intelligent code analysis, and generates structured markdown documentation in layered directories (output/database/, output/services/, output/frontend/, output/prd/). Includes visit log tracking for incremental analysis, 120-second LLM timeouts with 3-retry exponential backoff, and progress reporting every 10 seconds.

## Technical Context

**Language/Version**: Python 3.8+ (minimum version for type hints and async support, consistent with Feature 001)
**Primary Dependencies**:
- Click 8.x (CLI framework, existing from Feature 001)
- weaviate-client 3.x (vector database queries for artifact context)
- httpx (Ollama HTTP API communication, existing from Feature 001)
- python-dotenv (environment configuration)
- lxml (XML/POM parsing, existing from Feature 001)
- pytest + pytest-mock (testing framework)

**Storage**:
- JSON Lines (.jsonl) for visit log tracking (output/.visit_log.jsonl)
- Markdown files in layered directory structure (output/database/, output/services/, output/frontend/, output/prd/)
- Weaviate vector database for querying indexed artifacts (read-only, populated by Feature 001)

**Testing**: pytest with fixtures for unit tests, mocked Ollama/Weaviate for integration tests, end-to-end tests with sample Java projects

**Target Platform**: Developer workstations (macOS, Linux, Windows with WSL), single-node execution, 8GB+ RAM recommended

**Project Type**: Single CLI application extending existing codeindex pipeline from Feature 001

**Performance Goals**:
- Database documentation: <10 minutes for 100+ entities
- LLM analysis: 120s timeout per file, 3 retries with exponential backoff
- Overall throughput: Generate complete PRD for 10,000+ file codebase within 2-4 hours
- Memory usage: <2GB for streaming processing

**Constraints**:
- Local-only processing (Ollama at localhost:11434)
- Must integrate with existing Feature 001 pipeline (reuse discovery/extraction)
- Progress updates every 10 seconds minimum (constitution requirement)
- Visit log must support incremental analysis (skip unchanged files)
- Output must be markdown-compatible with optional HTML rendering

**Scale/Scope**:
- 100+ database entities per project
- 1000+ service methods across hundreds of classes
- 100+ JSP/GWT/HTML forms and components
- 10,000+ files total per analyzed codebase
- Multiple project versions coexisting in Weaviate

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Code Quality Standards ✅ PASS

- **Type Safety**: Will use Python type hints for all PRD generation functions. LLM responses and Weaviate queries will be validated explicitly (PASS)
- **Error Handling**: LLM timeouts (120s) with 3-retry exponential backoff specified. Weaviate query failures will be handled gracefully with fallback to direct file analysis (PASS)
- **Code Organization**: New CLI command `codeindex prd` will be added following existing stage pattern (discover, extract, index, search, prd). PRD generation logic isolated in src/codeindex/services/prd_generator.py (PASS)
- **Configuration**: Will reuse existing config hierarchy (CLI args > env > .env > defaults). New options: --output-dir, --layer (database/services/frontend/all), --force-refresh (PASS)
- **Documentation**: All PRD generation functions will have docstrings. Complex LLM prompting logic will include inline comments explaining prompt engineering strategies (PASS)

**Rationale**: Extends existing Feature 001 architecture with consistent patterns. PRD generation is naturally a new pipeline stage after indexing.

### II. Testing Discipline ✅ PASS

- **Test Pyramid**: Unit tests for markdown generation, visit log tracking, LLM prompt construction. Integration tests for Weaviate queries and file writing. E2E tests for complete PRD generation (PASS)
- **Test Isolation**: Unit tests will mock Ollama and Weaviate. Integration tests will use test-specific Weaviate collections and fixture responses (PASS)
- **Test Data**: Will include realistic DAO/Service/JSP fixtures covering edge cases (complex SQL, nested GWT components, malformed JSP). Stored in tests/fixtures/prd/ (PASS)
- **Coverage Requirements**: >80% coverage for prd_generator.py, markdown_builder.py, visit_log.py (PASS)
- **Test Performance**: Unit tests <100ms, integration tests <5s, E2E PRD generation tests marked @pytest.mark.slow (PASS)
- **TDD**: Tests written first for visit log format, markdown structure, LLM prompt validation (PASS)

**Rationale**: PRD generation involves complex LLM interactions and file I/O. Comprehensive testing prevents regressions when adding support for new artifact types.

### III. User Experience Consistency ✅ PASS

- **CLI Design**: New command `codeindex prd --project <name> --layer <database|services|frontend|all>` follows existing pattern. Supports --help with examples (PASS)
- **Output Formats**: Generated markdown is human-readable. Structured format enables programmatic parsing. Errors include actionable guidance (e.g., "No artifacts found. Run 'codeindex index' first") (PASS)
- **Logging**: Structured logging at INFO (progress), DEBUG (LLM prompts/responses), WARNING (missing artifacts), ERROR (failures). Respects LOG_LEVEL env var (PASS)
- **Documentation**: Will update CLAUDE.md with PRD generation examples, output structure, troubleshooting. Will document .env options (OUTPUT_DIR, PRD_TEMPLATE_PATH) (PASS)
- **Generated Artifacts**: PRD markdown follows hierarchical structure with metadata headers (project name, generation timestamp, layer, version). Compatible with Spec Kit consumption (PASS)

**Rationale**: Users generate PRDs for large codebases spanning weeks. Clear progress indicators and well-structured output enable navigation and incremental updates.

### IV. Performance Requirements ✅ PASS

- **Discovery Performance**: Reuses existing Feature 001 discovery (already meets >1000 files/second) (PASS)
- **Extraction Performance**: Reuses existing Feature 001 extraction (already indexed). PRD generation queries Weaviate for context rather than re-extracting (PASS)
- **Indexing Performance**: Read-only Weaviate queries for artifact lookup. No new indexing (PASS)
- **Search Performance**: Weaviate vector search for cross-referencing (form → service → database) uses existing indexed embeddings (PASS)
- **Memory Management**: Streams visit log entries one line at a time. Generates documentation files incrementally per entity/service/form (PASS)
- **Resource Cleanup**: LLM connections (httpx) and file handles properly closed in try/finally blocks (PASS)

**Rationale**: PRD generation is document-focused, not compute-intensive. Performance depends on Weaviate query efficiency (already optimized in Feature 001) and LLM throughput (limited by Ollama, hence 120s timeout).

### V. Observability & Monitoring ✅ PASS

- **Metrics Collection**: Logs summary metrics (entities documented, LLM calls made, files written, cross-references created). Structured JSON format for parsing (PASS)
- **Diagnostic Tools**: Can extend weaviate_stats.py to show PRD generation statistics (documented entities by layer). Logs include artifact counts and missing references (PASS)
- **Progress Tracking**: Updates every 10 seconds showing current layer, files processed, estimated completion time, current entity being analyzed (constitution requirement, FR-044) (PASS)
- **Error Aggregation**: Collects LLM timeouts, missing artifacts, failed cross-references. Summarizes by type at end (e.g., "23 services missing DAO references, 5 forms without backend endpoints") (PASS)
- **Integration Health**: Validates Weaviate has indexed artifacts before starting. Validates Ollama accessible. Provides clear error messages with remediation (PASS)

**Rationale**: PRD generation can take hours for large codebases. Detailed progress and error aggregation enable users to identify gaps in indexed artifacts or LLM configuration issues.

### Gate Status: ✅ ALL GATES PASS

No constitution violations. This feature naturally extends Feature 001 pipeline with consistent architecture, testing practices, and observability.

## Project Structure

### Documentation (this feature)

```text
specs/002-prd-document-generation/
├── plan.md              # This file (/speckit.plan command output)
├── spec.md              # Feature specification
├── research.md          # Phase 0 output (LLM prompting, documentation structure, state management)
├── data-model.md        # Phase 1 output (10 key entities: DatabaseEntity, BusinessRule, etc.)
├── quickstart.md        # Phase 1 output (getting started guide)
├── contracts/           # Phase 1 output (CLI contract, output formats, LLM schemas)
│   ├── cli-interface.md
│   ├── output-structure.md
│   └── llm-contracts.md
├── checklists/          # Quality validation checklists
│   └── requirements.md
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/codeindex/
├── cli/
│   ├── discover.py          # Existing from Feature 001
│   ├── extract.py           # Existing from Feature 001
│   ├── index.py             # Existing from Feature 001
│   ├── search.py            # Existing from Feature 001
│   ├── status.py            # Existing from Feature 001
│   └── prd.py               # NEW: PRD generation command
├── models/
│   ├── project.py           # Existing from Feature 001
│   ├── artifact.py          # Existing from Feature 001
│   ├── inventory.py         # Existing from Feature 001
│   ├── extraction.py        # Existing from Feature 001
│   └── prd.py               # NEW: PRD-specific models (DatabaseEntity, ServiceDefinition, etc.)
├── services/
│   ├── discovery.py         # Existing from Feature 001
│   ├── extraction.py        # Existing from Feature 001
│   ├── indexing.py          # Existing from Feature 001
│   ├── maven.py             # Existing from Feature 001
│   ├── classifier.py        # Existing from Feature 001
│   ├── ollama_client.py     # Existing from Feature 001, EXTEND for PRD prompts
│   ├── weaviate_store.py    # Existing from Feature 001, EXTEND for artifact queries
│   ├── prd_generator.py     # NEW: Orchestrates PRD generation
│   ├── db_analyzer.py       # NEW: Database layer analysis
│   ├── service_analyzer.py  # NEW: Service layer analysis
│   ├── frontend_analyzer.py # NEW: Frontend layer analysis
│   ├── markdown_builder.py  # NEW: Generates markdown documentation
│   └── visit_log.py         # NEW: Tracks analyzed files (.visit_log.jsonl)
├── parsers/
│   ├── java_parser.py       # Existing from Feature 001, REUSE for service analysis
│   ├── jsp_parser.py        # Existing from Feature 001, REUSE for frontend analysis
│   ├── xml_parser.py        # Existing from Feature 001, REUSE for config analysis
│   └── sql_parser.py        # Existing from Feature 001, REUSE for DB analysis
├── utils/
│   ├── config.py            # Existing from Feature 001
│   ├── logging.py           # Existing from Feature 001
│   ├── retry.py             # Existing from Feature 001
│   ├── progress.py          # Existing from Feature 001
│   └── locking.py           # Existing from Feature 001
└── __main__.py              # Existing from Feature 001, EXTEND with prd command

tests/
├── unit/
│   ├── test_prd_generator.py      # NEW: PRD orchestration tests
│   ├── test_db_analyzer.py        # NEW: Database analysis tests
│   ├── test_service_analyzer.py   # NEW: Service analysis tests
│   ├── test_frontend_analyzer.py  # NEW: Frontend analysis tests
│   ├── test_markdown_builder.py   # NEW: Markdown generation tests
│   └── test_visit_log.py          # NEW: Visit log tracking tests
├── integration/
│   ├── test_prd_weaviate.py       # NEW: Weaviate query integration
│   └── test_prd_generation.py     # NEW: Full PRD generation integration
├── e2e/
│   └── test_prd_pipeline.py       # NEW: Complete pipeline test
└── fixtures/
    └── prd/                        # NEW: Sample DAO/Service/JSP files
        ├── sample_dao.java
        ├── sample_service.java
        ├── sample_jsp.jsp
        ├── sample_gwt.java
        └── expected_prd_output/
```

**Structure Decision**: Single project structure extending Feature 001. All PRD generation code lives in src/codeindex following existing organizational patterns (cli/, services/, models/). This enables code reuse (parsers, Ollama client, Weaviate store) and maintains architectural consistency.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

N/A - All constitution checks pass. No violations to justify.

## Architecture Decisions

### Decision 1: Layered Output Directory Structure

**Context**: FR-040 and clarifications specify separate subdirectories for each layer (database/, services/, frontend/, prd/) with index.md in each.

**Decision**: Use layered directory structure:
```
output/<project-name>/
├── database/
│   ├── index.md          # List of all entities with links
│   ├── entity_User.md
│   ├── entity_Order.md
│   └── ...
├── services/
│   ├── index.md          # List of all services with links
│   ├── service_UserService.md
│   ├── service_OrderService.md
│   └── ...
├── frontend/
│   ├── index.md          # List of all forms/components with links
│   ├── form_UserRegistration.md
│   ├── component_OrderSummary.md
│   └── ...
├── prd/
│   ├── index.md          # Master PRD with cross-references
│   ├── executive_summary.md
│   ├── architecture.md
│   └── cross_references.md
└── .visit_log.jsonl      # Tracking file
```

**Rationale**:
- Clear separation of concerns (each layer independently navigable)
- Supports incremental generation (can regenerate single layer without affecting others)
- Index files enable quick navigation and external tool integration
- Aligns with bottom-up workflow (database → services → frontend → synthesis)

**Alternatives Considered**:
- Flat structure: Rejected due to poor scalability (hundreds of files in one directory)
- Single file: Rejected due to difficulty navigating large documents and lack of reusability
- Module-based: Rejected as too complex for initial implementation (may revisit if projects have clear module boundaries)

### Decision 2: Visit Log Format (JSON Lines)

**Context**: FR-008 requires tracking visited files for incremental analysis. Clarifications specify JSON Lines format.

**Decision**: Use JSON Lines (.jsonl) with schema:
```json
{"file_path": "/path/to/file.java", "timestamp": "2025-12-14T10:30:00Z", "status": "success", "content_hash": "sha256:abc123...", "layer": "database"}
```

**Rationale**:
- Append-only: New entries added without rewriting entire file
- Streaming: Can process large logs line-by-line without loading into memory
- Structured: Easy to query for specific files or filter by layer/status
- Human-readable: Can inspect with standard Unix tools (grep, tail, etc.)

**Alternatives Considered**:
- SQLite: More complex, requires schema migrations, overkill for simple tracking
- CSV: Less structured, harder to handle escaped values, no native JSON types
- Plain text: Too limited, can't store structured metadata (hash, layer, status)

### Decision 3: LLM Prompt Engineering Strategy

**Context**: FR-033 requires targeted prompts based on artifact type. Need to extract business rules from DAOs, understand service orchestration, analyze form bindings.

**Decision**: Use artifact-type-specific prompt templates with contextual enrichment:

**DAO Prompt Template**:
```
You are analyzing a Data Access Object (DAO) class.

Context from Weaviate:
- Related entities: {entity_names}
- Database tables accessed: {table_names}

Code:
{dao_source_code}

Extract:
1. Database operations (CRUD, queries)
2. Business rules (validation, constraints)
3. Transaction boundaries
4. Relationships to entities

Output JSON format:
{
  "operations": [{"name": "...", "type": "...", "tables": [...], "purpose": "..."}],
  "business_rules": [{"rule": "...", "scope": "...", "source_line": ...}],
  "relationships": [{"entity": "...", "relationship_type": "..."}]
}
```

**Service Prompt Template**:
```
You are analyzing a business logic service class.

Context from Weaviate:
- DAOs used: {dao_names}
- Entities involved: {entity_names}
- API endpoints: {endpoint_paths}

Code:
{service_source_code}

Extract:
1. Public API methods (signatures, purposes)
2. Business operations (workflows, validations)
3. Dependencies on DAOs/other services
4. Transaction management

Output JSON format:
{
  "operations": [{"method": "...", "purpose": "...", "dao_calls": [...], "business_logic": "..."}],
  "dependencies": [{"type": "...", "name": "..."}],
  "transactions": [{"method": "...", "scope": "..."}]
}
```

**Frontend Prompt Template**:
```
You are analyzing a user interface component (JSP/GWT/JavaScript).

Context from Weaviate:
- Backend endpoints: {endpoint_urls}
- Services called: {service_names}
- Related entities: {entity_names}

Code:
{frontend_source_code}

Extract:
1. Forms (fields, validation, submission)
2. User interactions (buttons, events, navigation)
3. Client-side business rules
4. Backend integration points

Output JSON format:
{
  "forms": [{"name": "...", "fields": [...], "validation": [...], "submit_to": "..."}],
  "interactions": [{"element": "...", "event": "...", "action": "..."}],
  "client_rules": [{"rule": "...", "trigger": "..."}],
  "backend_calls": [{"endpoint": "...", "method": "..."}]
}
```

**Rationale**:
- Context enrichment: Provides related artifacts from Weaviate to improve LLM understanding
- Structured output: JSON format enables programmatic processing and validation
- Artifact-specific: Each prompt focuses on information relevant to that layer
- Actionable: Extracts business-oriented information, not just code structure

**Alternatives Considered**:
- Generic prompts: Rejected due to lower quality results (LLM needs context)
- Few-shot examples: Deferred to research phase (may add if initial results insufficient)
- Chain-of-thought: Deferred (adds complexity, assess need based on initial accuracy)

### Decision 4: Cross-Referencing Strategy

**Context**: FR-027 requires creating cross-references between layers (form → service → database). Need to link artifacts discovered at different stages.

**Decision**: Two-phase approach:
1. **Analysis Phase**: Each layer analyzer stores artifact references in intermediate data structures (e.g., FormDefinition stores `submit_endpoint`, ServiceDefinition stores `dao_dependencies`)
2. **Synthesis Phase**: PRD generator queries Weaviate to resolve references and create bidirectional links

**Implementation**:
```python
# Analysis phase: Frontend analyzer stores endpoint reference
form_def = FormDefinition(
    name="UserRegistration",
    fields=[...],
    submit_endpoint="/api/users/register"  # Store reference
)

# Synthesis phase: Resolve endpoint → service → database
search_results = weaviate_store.search_artifacts(
    query="register user endpoint",
    artifact_type="GWT_ENDPOINT"
)
service_def = resolve_service_from_endpoint(search_results)
dao_deps = service_def.dao_dependencies
entities = resolve_entities_from_daos(dao_deps)

# Generate cross-reference markdown
cross_ref_md = f"""
## User Registration Flow

**Frontend**: UserRegistration form (`src/ui/UserRegistration.jsp`)
- Fields: {form_def.fields}
- Validates: {form_def.validation_rules}

**Backend**: UserService.registerUser (`src/services/UserService.java`)
- Calls DAO: UserDAO.create
- Validates: email format, password strength
- Transaction: REQUIRED

**Database**: User table
- Primary key: user_id
- Constraints: UNIQUE(email)
"""
```

**Rationale**:
- Leverages Weaviate semantic search for fuzzy matching (handles naming inconsistencies)
- Two-phase approach allows each analyzer to work independently
- Resolves references during synthesis enables handling of missing artifacts gracefully

**Alternatives Considered**:
- Direct code parsing: Rejected due to complexity of tracking references across multiple files
- String matching: Rejected due to fragility (naming conventions vary)
- Manual annotation: Rejected as defeats purpose of automated analysis

## Phase 0 Deliverables

**Status**: Research agents dispatched (running in background)

Expected research.md contents:
1. LLM prompt engineering best practices for code analysis
2. Hierarchical documentation generation patterns
3. Incremental analysis and state management approaches

## Phase 1 Deliverables

**Status**: Design agents dispatched (running in background)

Expected artifacts:
1. data-model.md: 10 key entities with fields, relationships, validation
2. contracts/: CLI interface, output structure, LLM schemas
3. quickstart.md: Getting started guide with examples

## Integration Points

### Feature 001 (Java Codebase Indexer)

**Dependencies**:
- Reuses discovery service for finding source files
- Reuses parsers (java_parser, jsp_parser, xml_parser, sql_parser)
- Reuses Ollama client for LLM calls (extend with new prompt templates)
- Reuses Weaviate store for querying indexed artifacts (extend with PRD-specific queries)
- Reuses CLI framework and utilities (config, logging, progress, retry)

**Extension Points**:
- New CLI command: `codeindex prd`
- New services: prd_generator, db_analyzer, service_analyzer, frontend_analyzer, markdown_builder, visit_log
- New models: prd.py with PRD-specific entities
- New tests: PRD generation unit/integration/e2e tests

### Ollama LLM Service

**Integration**:
- HTTP API calls to localhost:11434
- 120-second timeout per call (FR-035, clarifications)
- Maximum 3 retry attempts with exponential backoff
- Artifact-type-specific prompt templates

**Error Handling**:
- LLM unavailable: Log warning, fall back to basic structure extraction without AI summaries
- Timeout: Retry with reduced context window
- Malformed response: Log error with prompt/response for debugging, use fallback extraction
- Rate limiting: Respect MAX_CONCURRENT_AI_CALLS from config

### Weaviate Vector Database

**Integration**:
- Read-only queries for artifact lookup
- Semantic search for cross-referencing (form → service, service → DAO, DAO → entity)
- Project filtering to scope queries to analyzed codebase

**Query Patterns**:
```python
# Find services that use a specific DAO
services = weaviate_store.search_artifacts(
    query=f"services using {dao_name}",
    artifact_type="JAVA_SOURCE",
    project_id=project_id
)

# Find frontend forms that submit to an endpoint
forms = weaviate_store.search_artifacts(
    query=f"forms submitting to {endpoint_path}",
    artifact_type="JSP_VIEW",
    project_id=project_id
)

# Find database entities referenced by a service
entities = weaviate_store.search_artifacts(
    query=f"entities accessed by {service_name}",
    artifact_type="JAVA_SOURCE",
    tags_layer="DATA",
    project_id=project_id
)
```

## Next Steps

After `/speckit.plan` completes (Phase 0 research and Phase 1 design artifacts created):

1. Run `/speckit.tasks` to generate tasks.md with detailed implementation breakdown
2. Review tasks for completeness and priority ordering
3. Begin implementation following constitution gates
4. Update CLAUDE.md with PRD generation usage examples

**Note**: This plan document serves as the technical blueprint. The tasks.md generated by `/speckit.tasks` will decompose this plan into actionable development tasks with dependencies and test requirements.
