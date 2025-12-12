# Implementation Plan: Java Codebase Indexer Pipeline

**Branch**: `001-java-codebase-indexer` | **Date**: 2025-12-12 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-java-codebase-indexer/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a Python CLI pipeline that discovers Maven Java projects, extracts semantic understanding using local Ollama AI (gemma3:12b), and indexes structured artifacts with embeddings into local Weaviate for semantic search and future PRD generation. The system processes discovery → extraction → indexing phases independently, handles large codebases efficiently, and provides observability through status commands.

## Technical Context

**Language/Version**: Python 3.8+ (minimum version for type hints and modern async support)
**Primary Dependencies**:
- Click 8.x (CLI framework)
- weaviate-client 4.x (vector database client)
- requests/httpx (Ollama HTTP API communication)
- python-dotenv (environment configuration)
- lxml (XML/POM parsing)
- pytest (testing framework)

**Storage**:
- Weaviate vector database (Docker container, local deployment)
- JSON/JSONL for intermediate inventory files
- File system for logs and temporary data

**Testing**: pytest with fixtures for unit tests, integration tests with test Weaviate collections, @pytest.mark.slow for end-to-end pipeline tests

**Target Platform**: Developer workstations (macOS, Linux, Windows with WSL), single-node execution, 8GB+ RAM recommended

**Project Type**: Single CLI application with modular pipeline stages

**Performance Goals**:
- Discovery: 1000+ files/second file system scanning
- Extraction: 50+ Java files/minute including AI processing
- Indexing: Batch operations to Weaviate for efficiency
- Memory: <2GB for 100k file codebases (streaming architecture)

**Constraints**:
- Local-only processing (no cloud LLM calls)
- Ollama gemma3:12b model at localhost:11434
- Weaviate at localhost:8080 (or configured URL)
- Progress updates every 10 seconds minimum
- Resume capability for interrupted operations
- Per-project locking for concurrent safety

**Scale/Scope**:
- 100+ Maven modules per codebase
- 100k+ files per analysis run
- 10+ concurrent AI requests (configurable)
- Multiple project versions coexisting in Weaviate
- Indefinite data persistence

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Code Quality Standards ✅ PASS

- **Type Safety**: All functions will use Python type hints (PASS)
- **Error Handling**: Retry logic with exponential backoff for Weaviate/Ollama (PASS)
- **Code Organization**: CLI stages organized by pipeline phase (discover, extract, index, search, status) (PASS)
- **Configuration**: CLI args > env vars > .env file > defaults hierarchy (PASS)
- **Documentation**: Docstrings for all public functions, comments for complex parsing logic (PASS)

### II. Testing Discipline ✅ PASS

- **Test Pyramid**: Unit (parsers, classifiers), Integration (Weaviate, search), E2E (full pipeline) (PASS)
- **Test Isolation**: Mocks for Ollama/Weaviate in unit tests, test collections for integration (PASS)
- **Test Data**: Fixtures with realistic Java/JSP/GWT samples including edge cases (PASS)
- **Coverage**: >80% for extraction parsers, indexing logic, search builders (PASS)
- **Performance**: Unit <100ms, Integration <5s, E2E marked @pytest.mark.slow (PASS)
- **TDD**: Tests first for new artifact types and extraction patterns (PASS)

### III. User Experience Consistency ✅ PASS

- **CLI Design**: `python -m codeindex <stage> --project <name>` pattern with --help (PASS)
- **Output Formats**: Human-readable default, --format json for programmatic use (PASS)
- **Logging**: ERROR/WARNING/INFO/DEBUG levels, LOG_LEVEL environment variable (PASS)
- **Documentation**: CLAUDE.md with examples, .env.example for configuration (PASS)
- **Generated Artifacts**: Weaviate objects with consistent metadata structure (PASS)

### IV. Performance Requirements ✅ PASS

- **Discovery**: Streaming file discovery, no full path tree in memory (PASS)
- **Extraction**: Batched AI calls with rate limiting (10 concurrent default) (PASS)
- **Indexing**: Weaviate batch operations (50+ objects per batch), idempotent updates (PASS)
- **Search**: <2 second response time, project-filtered queries (PASS)
- **Memory**: Streaming architecture, incremental processing (PASS)
- **Cleanup**: Proper connection/resource cleanup in all stages (PASS)

### V. Observability & Monitoring ✅ PASS

- **Metrics**: Summary logs per stage (files discovered, artifacts extracted, objects indexed) (PASS)
- **Diagnostic Tools**: Status command showing indexed project counts and types (PASS)
- **Progress**: Updates every 10 seconds with estimated completion times (PASS)
- **Error Aggregation**: Error summaries by type at end of execution (PASS)
- **Health Checks**: Validate Ollama/Weaviate availability before operations (PASS)

### Quality Gates

**Gate 1: Pre-Implementation** ✅ READY
- Constitution compliance: ALL principles satisfied
- Test strategy: Defined (unit, integration, E2E with fixtures)
- External dependencies: Documented (Ollama gemma3:12b, Weaviate, Maven POMs)
- Performance impact: Streaming architecture designed for large scale
- Documentation: CLAUDE.md and .env.example planned

**Gate 2: Implementation Complete** - Pending implementation
**Gate 3: Integration Ready** - Pending implementation

## Project Structure

### Documentation (this feature)

```text
specs/001-java-codebase-indexer/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (technology decisions)
├── data-model.md        # Phase 1 output (entities and schemas)
├── quickstart.md        # Phase 1 output (getting started guide)
├── contracts/           # Phase 1 output (Weaviate schemas, CLI interface)
├── checklists/          # Quality validation checklists
│   └── requirements.md  # Requirements checklist (complete)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT yet created)
```

### Source Code (repository root)

```text
# Single CLI application structure
src/
├── codeindex/
│   ├── __init__.py
│   ├── __main__.py          # CLI entry point
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── discover.py      # Discovery command
│   │   ├── extract.py       # Extraction command
│   │   ├── index.py         # Indexing command
│   │   ├── search.py        # Search command
│   │   └── status.py        # Status command
│   ├── models/
│   │   ├── __init__.py
│   │   ├── project.py       # Project entity
│   │   ├── artifact.py      # CodeArtifact entity
│   │   ├── inventory.py     # DiscoveryInventory
│   │   └── extraction.py    # ExtractionResult
│   ├── services/
│   │   ├── __init__.py
│   │   ├── discovery.py     # File discovery service
│   │   ├── maven.py         # POM parser
│   │   ├── classifier.py    # File type classification
│   │   ├── extractor.py     # Extraction orchestration
│   │   ├── ollama_client.py # Ollama API client
│   │   ├── indexer.py       # Indexing orchestration
│   │   └── weaviate_store.py # Weaviate operations
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── java_parser.py   # Java source parsing
│   │   ├── jsp_parser.py    # JSP parsing
│   │   ├── xml_parser.py    # XML config parsing
│   │   └── sql_parser.py    # SQL parsing
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py        # Configuration management
│   │   ├── logging.py       # Structured logging setup
│   │   ├── retry.py         # Retry logic with backoff
│   │   ├── progress.py      # Progress indicators
│   │   └── locking.py       # Per-project locking
│   └── schemas/
│       ├── __init__.py
│       └── weaviate.py      # Weaviate schema definitions

tests/
├── fixtures/
│   ├── sample_java/         # Sample Java files
│   ├── sample_jsp/          # Sample JSP files
│   ├── sample_pom.xml       # Sample Maven POMs
│   └── malformed/           # Edge case samples
├── unit/
│   ├── test_discovery.py
│   ├── test_classifier.py
│   ├── test_maven_parser.py
│   ├── test_parsers.py
│   ├── test_ollama_client.py
│   └── test_models.py
├── integration/
│   ├── test_weaviate_store.py
│   ├── test_indexing.py
│   ├── test_search.py
│   └── conftest.py          # Integration test fixtures
└── e2e/
    ├── test_full_pipeline.py
    └── conftest.py          # E2E test fixtures

# Configuration files
.env.example                 # Example configuration
requirements.txt             # Python dependencies
setup.py or pyproject.toml   # Package configuration
pytest.ini                   # Pytest configuration
```

**Structure Decision**: Single CLI application structure selected because this is a command-line tool with a clear pipeline architecture (discover → extract → index → search). All pipeline stages share common models and utilities, making a unified structure more maintainable than splitting into separate services. The modular organization by CLI commands, services, parsers, and utilities enables independent testing and clear separation of concerns while maintaining simplicity for AI-assisted development.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No constitutional violations detected. All principles are satisfied by the planned architecture.

---

## Phase 1 Complete: Constitution Re-Check

*Post-design validation after Phase 1 artifacts generated*

### Design Artifacts Generated

✅ **research.md**: Technology decisions documented (10 decisions, 3 patterns)
✅ **data-model.md**: 4 entities with full schemas, enums, validations
✅ **contracts/weaviate-schema.yaml**: Weaviate class definitions
✅ **contracts/cli-interface.md**: 5 CLI commands with full specifications
✅ **quickstart.md**: Developer onboarding guide with examples

### Constitution Compliance Re-Validation

**I. Code Quality Standards** ✅ PASS
- Type hints enforced in data model design
- Error handling patterns documented (retry, exponential backoff)
- CLI organization by pipeline stage confirmed in contracts
- Configuration hierarchy validated in research decisions

**II. Testing Discipline** ✅ PASS
- Test structure defined in project layout (unit/integration/e2e)
- Fixture organization specified
- pytest configuration documented
- TDD approach for parsers confirmed

**III. User Experience Consistency** ✅ PASS
- CLI interface fully specified with examples
- Progress indicators designed (10s updates, ETA)
- Error messages with actionable guidance documented
- Empty state handling specified in contracts

**IV. Performance Requirements** ✅ PASS
- Streaming architecture confirmed in data model
- Rate limiting pattern designed (Semaphore, 10 concurrent)
- Batch operations specified (50+ objects, configurable)
- Memory constraints addressed in quickstart

**V. Observability & Monitoring** ✅ PASS
- Status command fully specified
- Metrics collection documented
- Progress tracking designed
- Error aggregation pattern defined

### No New Issues Identified

All design decisions align with constitutional principles. No violations introduced during planning phase.

---

## Implementation Readiness

**Status**: ✅ READY FOR TASKS GENERATION

**Next Command**: `/speckit.tasks`

**Deliverables Complete**:
- ✅ Technical context defined
- ✅ Constitution compliance validated (twice)
- ✅ Technology research complete
- ✅ Data model designed
- ✅ API contracts specified (Weaviate + CLI)
- ✅ Quickstart guide written
- ✅ Agent context updated (CLAUDE.md)

**What's Next**:
The planning phase is complete. Use `/speckit.tasks` to break down this plan into actionable, dependency-ordered implementation tasks following the tasks template structure.
