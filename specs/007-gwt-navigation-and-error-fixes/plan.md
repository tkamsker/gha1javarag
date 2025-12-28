# Implementation Plan: GWT Navigation Analysis and Error Fixes

**Branch**: `007-gwt-navigation-and-error-fixes` | **Date**: 2025-12-22 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/007-gwt-navigation-and-error-fixes/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This feature fixes critical production issues in the GEMINI Code Analysis Pipeline: 29 Ollama timeout failures blocking complete documentation, 4 database foreign key validation errors causing incomplete data models, and limited GWT frontend detection (only 1 Presenter found). The implementation adds adaptive timeout handling with exponential backoff and fallback to structural analysis, multi-source foreign key extraction (Java + iBATIS + SQL), and comprehensive GWT navigation path analysis starting from index.html/jsp entry points through modules to all Presenters/Views/Activities.

## Technical Context

**Language/Version**: Python 3.8+ (existing project requirement, type hints mandatory)
**Primary Dependencies**:
- Ollama (local LLM for semantic extraction)
- Weaviate 1.32+ (vector database for artifact indexing)
- lxml (XML parsing for GWT modules, iBATIS, UiBinder)
- javalang (Java AST parsing for structural fallback)
- Click (CLI framework)
- Pydantic (data validation and models)

**Storage**: Weaviate vector database (persistent storage in weaviate-data/ directory), JSONL files for intermediate pipeline stages
**Testing**: pytest with fixtures in tests/fixtures/, unit tests in tests/unit/, integration tests in tests/integration/
**Target Platform**: Linux/macOS servers with Docker (Weaviate container), Python 3.8+ virtual environment
**Project Type**: Single Python package (codeindex) with CLI entry point
**Performance Goals**:
- Zero timeout failures on production codebases (539+ files)
- >50 files/second extraction throughput
- <20% performance overhead from new features
- >90% GWT component discovery rate

**Constraints**:
- Must maintain backward compatibility with existing pipeline stages
- Ollama read timeout configurable (600s for large files)
- Memory usage <2GB for 100k+ file codebases
- Idempotent indexing (re-running updates, not duplicates)
- All external services (Weaviate, Ollama) must have health checks

**Scale/Scope**:
- Production codebase: 539 files (cuco-ui-admin)
- Target: Support codebases up to 100k+ files
- Expected: ~100-200 GWT Presenters/Views per large application
- Typical: 20-50 DAO files with 5-10 foreign keys each

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate 1: Pre-Implementation (Blocking)

- [x] **Constitution compliance reviewed and documented**
  - ✅ Follows Code Quality Standards: Type hints for all new functions, error handling for Ollama/file I/O, retry logic with exponential backoff
  - ✅ Follows Testing Discipline: Unit tests for parsers (index.html, GWT module, SQL JOIN), integration tests for timeout scenarios, fixtures for GWT code samples
  - ✅ Follows UX Consistency: Progress indicators for navigation analysis, structured logging for timeout metrics, clear error messages
  - ✅ Follows Performance Requirements: Streaming navigation graph building, batched Weaviate updates, memory-efficient parsing
  - ✅ Follows Observability: Timeout metrics logged, FK extraction metrics tracked, navigation analysis progress reported

- [x] **Test strategy defined**
  - Unit tests: Timeout retry logic, exponential backoff calculation, FK extraction from multiple sources, GWT module parsing, navigation graph building
  - Integration tests: End-to-end timeout scenarios with mock Ollama, DAO analysis with test fixtures, GWT navigation from index.html to components
  - Fixtures needed: Large Java service files (>1000 lines), DAO files with various FK patterns, index.html/jsp with GWT modules, GWT module descriptors, Presenter/View/UiBinder samples

- [x] **External dependencies documented**
  - Weaviate schema: No changes required (existing artifact types support new metadata)
  - Ollama: Configurable timeout (READ_TIMEOUT env var), existing qwen2.5-coder:32b model sufficient
  - New Python dependencies: None (lxml, javalang already in requirements.txt)

- [x] **Performance impact assessed**
  - Timeout handling: Adds 5-45s retry delays only on failures (acceptable for reliability)
  - FK extraction: Adds ~100ms per DAO file for SQL parsing (negligible compared to LLM extraction)
  - Navigation analysis: Adds ~5-10 seconds for typical GWT app (50-100 modules), one-time cost during discovery
  - Expected throughput: No degradation for successful extractions, improved overall success rate eliminates need for reruns

- [x] **User-facing changes documented in CLAUDE.md**
  - New timeout configuration: READ_TIMEOUT environment variable
  - New metrics logged: Timeout summary, FK extraction metrics, navigation graph statistics
  - New CLI output: Progress indicators for navigation analysis, detailed fallback logging
  - Documentation: Updated troubleshooting section with timeout scenarios

### Gate 2: Implementation Complete

- [ ] All tests passing (unit, integration) - *Will be validated during implementation*
- [ ] Test coverage meets requirements (>80% for critical components) - *Target: >85% for new parsers and analyzers*
- [ ] CLI help text and error messages reviewed for clarity - *Will include actionable remediation steps*
- [ ] Logging statements use appropriate levels and include context - *ERROR for failures, WARNING for fallbacks, INFO for progress, DEBUG for details*
- [ ] Type hints added for all new functions and classes - *Mandatory per constitution*

### Gate 3: Integration Ready

- [ ] Integration tests validate end-to-end workflows - *Full pipeline test on cuco-ui-admin codebase*
- [ ] Performance requirements validated - *Zero timeouts, >90% discovery, <20% overhead*
- [ ] Error handling tested with realistic failure scenarios - *Ollama down, malformed XML, circular dependencies*
- [ ] Documentation updated - *CLAUDE.md examples, troubleshooting, configuration*
- [ ] Breaking changes noted - *None expected, all changes are additive*

## Project Structure

### Documentation (this feature)

```text
specs/007-gwt-navigation-and-error-fixes/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output - Timeout strategies, FK extraction methods, GWT patterns
├── data-model.md        # Phase 1 output - NavigationGraph, TimeoutMetric, FKRelationship entities
├── quickstart.md        # Phase 1 output - Test scenarios for timeout, FK, navigation analysis
├── contracts/           # Phase 1 output - Internal API contracts (not REST endpoints)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/codeindex/
├── cli/                 # Existing CLI commands (discover, extract, index, search, prd, diagram, status)
│   ├── discover.py      # MODIFIED: Add navigation analysis phase after file discovery
│   ├── extract.py       # MODIFIED: Add timeout handling and fallback logic
│   └── status.py        # MODIFIED: Add timeout metrics and navigation statistics
├── models/              # Existing data models (Project, CodeArtifact, etc.)
│   ├── navigation.py    # NEW: NavigationGraph, NavigationNode, GWTModule models
│   └── metrics.py       # NEW: TimeoutMetric, FKExtractionMetric models
├── parsers/             # Existing parsers (Java, JSP, XML, SQL)
│   ├── index_parser.py  # NEW: Parse index.html/jsp for GWT module references
│   ├── gwt_module_parser.py  # NEW: Parse *.gwt.xml module descriptors
│   └── sql_parser.py    # MODIFIED: Add FK extraction from JOIN statements
├── services/            # Existing services (discovery, extraction, indexing, etc.)
│   ├── ollama_client.py         # MODIFIED: Add adaptive timeout, exponential backoff, fallback
│   ├── db_analyzer.py           # MODIFIED: Multi-source FK extraction (Java + iBATIS + SQL)
│   ├── gwt_navigation_analyzer.py  # NEW: Build navigation graph from entry points
│   ├── gwt_presenter_analyzer.py   # MODIFIED: Extract navigation targets
│   ├── gwt_view_analyzer.py        # MODIFIED: Extract navigation widgets
│   └── structural_analyzer.py   # NEW: Java AST parsing fallback (no LLM)
├── utils/               # Existing utilities (config, logging, retry, progress)
│   ├── retry.py         # MODIFIED: Add exponential backoff for timeouts
│   └── metrics.py       # NEW: Collect and log timeout/FK/navigation metrics
└── schemas/             # Existing Weaviate schemas
    └── artifacts.py     # NO CHANGES: Existing artifact types support new metadata

tests/
├── fixtures/
│   ├── gwt/             # NEW: Sample GWT modules, presenters, views, UiBinder templates
│   │   ├── index.html
│   │   ├── App.gwt.xml
│   │   ├── UserPresenter.java
│   │   ├── UserView.java
│   │   └── UserView.ui.xml
│   ├── dao/             # NEW: Sample DAOs with various FK patterns
│   │   ├── MyNotesDao.java
│   │   ├── InventoryProductGroupDao.java
│   │   └── notes.ibatis.xml
│   └── large_service.java  # NEW: 500+ line file for timeout testing
├── unit/
│   ├── test_timeout_handling.py  # NEW: Test exponential backoff, fallback
│   ├── test_fk_extraction.py     # NEW: Test multi-source FK parsing
│   ├── test_index_parser.py      # NEW: Test index.html/jsp parsing
│   ├── test_gwt_module_parser.py # NEW: Test GWT module descriptor parsing
│   ├── test_gwt_navigation.py    # NEW: Test navigation graph building
│   └── test_sql_parser.py        # NEW: Test FK extraction from SQL JOINs
└── integration/
    ├── test_timeout_scenarios.py      # NEW: End-to-end timeout with mock Ollama
    ├── test_dao_analysis.py           # NEW: Full DAO extraction with FK validation
    └── test_gwt_navigation_e2e.py     # NEW: Index.html → navigation graph
```

**Structure Decision**: Single Python package (codeindex) following existing project structure. This is a CLI tool that analyzes Java/GWT codebases, not a web application. All new components integrate into existing pipeline stages (discover, extract, status). The modular service architecture allows independent testing of timeout handling, FK extraction, and navigation analysis without coupling to the full pipeline.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations. This feature adheres to all constitutional principles:
- Code Quality: Type hints, error handling, retry logic, clear organization
- Testing: Comprehensive unit/integration tests, >80% coverage target, realistic fixtures
- UX: Progress indicators, structured logging, actionable error messages
- Performance: <20% overhead, streaming processing, memory efficient
- Observability: Detailed metrics, diagnostic tools, progress tracking

## Implementation Strategy

### Phase 0: Research & Analysis

**Goal**: Resolve technical unknowns and establish implementation patterns.

**Research Topics**:
1. **Timeout Strategies**: Investigate adaptive timeout calculation based on file size, exponential backoff parameters (5s, 15s, 45s), graceful degradation patterns
2. **FK Extraction**: Research SQL JOIN parsing libraries, iBATIS XML XPath patterns, column detection heuristics
3. **GWT Navigation Patterns**: Study GWT module inheritance, Activity/Place navigation, PlaceHistoryMapper patterns, circular dependency detection
4. **Structural Analysis Fallback**: Evaluate javalang AST parser capabilities, identify extractable metadata without LLM (class names, methods, imports)
5. **Performance Optimization**: Investigate streaming navigation graph construction, memory-efficient GWT module caching

**Deliverable**: `research.md` documenting decisions, rationale, and alternatives considered.

### Phase 1: Core Implementation

**Approach**: Implement features in priority order (US1 → US2 → US3 → US4), each independently testable.

#### US1: Fix Ollama Timeout Failures

**Components**:
- `ollama_client.py`: Add adaptive timeout calculation, exponential backoff retry, fallback trigger
- `structural_analyzer.py`: NEW service for Java AST parsing without LLM
- `retry.py`: Add exponential backoff utility function
- `metrics.py`: NEW utility for timeout metric collection

**Test Strategy**:
- Unit: Test timeout calculation logic, retry delay calculation, fallback triggering
- Integration: Mock slow Ollama responses, verify retries and fallback execution

**Files Modified**:
- `src/codeindex/services/ollama_client.py`
- `src/codeindex/services/structural_analyzer.py` (NEW)
- `src/codeindex/utils/retry.py`
- `src/codeindex/utils/metrics.py` (NEW)
- `src/codeindex/cli/extract.py`
- `src/codeindex/cli/status.py`

#### US2: Fix Database Foreign Key Validation

**Components**:
- `db_analyzer.py`: Add multi-phase column collection, merge FK from multiple sources
- `sql_parser.py`: Add FK extraction from JOIN statements
- Existing `ibatis_parser.py`: Extract FK from XML `<resultMap>` and queries

**Test Strategy**:
- Unit: Test SQL JOIN parsing, iBATIS XML FK extraction, column merge logic
- Integration: Test with realistic DAO fixtures containing various FK patterns

**Files Modified**:
- `src/codeindex/services/db_analyzer.py`
- `src/codeindex/parsers/sql_parser.py`

#### US3: Implement GWT Navigation Path Analysis

**Components**:
- `index_parser.py`: NEW parser for index.html/jsp to extract GWT module references
- `gwt_module_parser.py`: NEW parser for *.gwt.xml module descriptors
- `gwt_navigation_analyzer.py`: NEW service to build navigation graph from entry points
- `navigation.py`: NEW models for NavigationGraph, NavigationNode, GWTModule
- `gwt_presenter_analyzer.py`: MODIFIED to extract navigation targets
- `gwt_view_analyzer.py`: MODIFIED to extract navigation widgets

**Test Strategy**:
- Unit: Test index.html parsing, GWT module parsing, navigation graph construction, circular dependency detection
- Integration: Test end-to-end from index.html to complete navigation graph

**Files Modified/Created**:
- `src/codeindex/parsers/index_parser.py` (NEW)
- `src/codeindex/parsers/gwt_module_parser.py` (NEW)
- `src/codeindex/services/gwt_navigation_analyzer.py` (NEW)
- `src/codeindex/models/navigation.py` (NEW)
- `src/codeindex/services/gwt_presenter_analyzer.py` (MODIFIED)
- `src/codeindex/services/gwt_view_analyzer.py` (MODIFIED)
- `src/codeindex/cli/discover.py` (MODIFIED)

#### US4: Enhanced Frontend Layout Extraction

**Components**:
- Extend `gwt_navigation_analyzer.py`: Add Presenter-View-UiBinder relationship mapping
- Extend `navigation.py`: Add PresenterViewBinding, UiBinderHierarchy models
- Extend `diagram_generator.py`: Add navigation flow diagrams with entry points

**Test Strategy**:
- Unit: Test Presenter-View binding logic, UiBinder hierarchy extraction, diagram generation
- Integration: Test complete workflow from GWT analysis to diagram output

**Files Modified**:
- `src/codeindex/services/gwt_navigation_analyzer.py`
- `src/codeindex/models/navigation.py`
- `src/codeindex/services/diagram_generator.py`

### Phase 2: Integration & Polish

**Tasks**:
1. Run full integration test suite on cuco-ui-admin (539 files)
2. Validate performance requirements (zero timeouts, >90% discovery, <20% overhead)
3. Update CLAUDE.md with usage examples, configuration, troubleshooting
4. Generate benchmark report comparing before/after metrics
5. Create migration guide (if any breaking changes)

**Validation**:
- Run pipeline on production codebase: `./run.sh cuco-ui-admin`
- Verify zero timeout errors in logs
- Verify all 4 DAO FK validation errors resolved
- Verify >90% GWT Presenters/Views discovered
- Measure execution time increase (<20% acceptable)

## Technical Decisions

### 1. Adaptive Timeout Strategy

**Decision**: Use file-size-based timeout calculation with configurable base timeout.

**Rationale**:
- Large service files (>1000 lines) inherently take longer to analyze
- Fixed timeout penalizes large files unnecessarily
- Adaptive timeout: `base_timeout * (1 + file_lines / 1000)` scales linearly
- Base timeout configurable via READ_TIMEOUT environment variable (default 600s)

**Alternatives Considered**:
- **Per-file timeout calibration**: Too complex, requires historical data
- **Fixed high timeout**: Wastes time on small files that will never complete
- **Immediate fallback**: Loses semantic analysis benefits

**Implementation**: Modify `ollama_client.py` to calculate timeout dynamically before each request.

### 2. Exponential Backoff Parameters

**Decision**: Use 3 retry attempts with delays [5s, 15s, 45s] (multiplier 3x).

**Rationale**:
- Industry standard for transient failures (AWS SDK, Google APIs use 2-3x multiplier)
- 5s first retry handles temporary Ollama slowness
- 15s second retry handles heavier load
- 45s third retry handles worst-case scenarios
- Total max wait time: 65 seconds before fallback (acceptable for reliability)

**Alternatives Considered**:
- **Fibonacci delays [1s, 2s, 3s, 5s]**: Too short, doesn't handle sustained load
- **Fixed 10s delays**: Not adaptive to problem severity
- **More than 3 retries**: Diminishing returns, delays pipeline excessively

**Implementation**: Add exponential backoff to `retry.py` utility, use in `ollama_client.py`.

### 3. Structural Analysis Fallback

**Decision**: Use javalang library for Java AST parsing without LLM.

**Rationale**:
- javalang already in requirements.txt (used elsewhere in project)
- Can extract basic metadata: class name, methods, imports, annotations
- Zero external dependency (no Ollama required)
- Fast (<100ms per file)
- Provides 60-70% of semantic value (better than nothing)

**Alternatives Considered**:
- **Skip file entirely**: Loses all documentation for timed-out files
- **Use simpler regex extraction**: Error-prone, misses complex patterns
- **Queue for later retry**: Delays final results, complicates pipeline

**Implementation**: Create `structural_analyzer.py` service wrapping javalang parser.

### 4. Multi-Source Foreign Key Extraction

**Decision**: Extract FK from Java annotations → iBATIS XML → SQL JOINs (priority order).

**Rationale**:
- Java @JoinColumn most authoritative (code of record)
- iBATIS XML captures query-time FK not in Java (legacy patterns)
- SQL JOIN fallback handles pure SQL DAOs
- Merge all sources, prioritize Java, mark duplicates

**Alternatives Considered**:
- **Java annotations only**: Misses 20-30% of FK in legacy iBATIS codebases
- **iBATIS only**: Incomplete for modern JPA codebases
- **Parallel extraction without priority**: Ambiguous when sources conflict

**Implementation**: Modify `db_analyzer.py` to collect columns first, then validate FK from all sources.

### 5. GWT Navigation Graph Structure

**Decision**: Use directed graph with typed nodes (Presenter/View/Activity/Place/External).

**Rationale**:
- Graph captures navigation flow naturally (A navigates-to B)
- Typed nodes enable different rendering (Presenters blue, Views green, etc.)
- Supports cycles (back buttons) and multiple paths (tabs, menus)
- External boundaries marked clearly (exit points from GWT app)

**Alternatives Considered**:
- **Tree structure**: Doesn't support cycles or multiple entry points
- **Flat list of components**: Loses navigation flow information
- **Nested JSON**: Hard to query, inefficient for graph operations

**Implementation**: Create `navigation.py` models: NavigationGraph, NavigationNode, edge relationships.

### 6. Index.html/jsp Parsing Strategy

**Decision**: Use lxml HTML parser with XPath queries for GWT module references.

**Rationale**:
- lxml already in requirements.txt (used for XML parsing)
- HTML mode handles malformed HTML gracefully
- XPath `//script[@src]` efficiently finds GWT module scripts
- Regex fallback for `nocache.js` patterns in inline scripts

**Alternatives Considered**:
- **BeautifulSoup**: Additional dependency, similar capabilities
- **Regex only**: Brittle, misses complex HTML structures
- **Manual string parsing**: Error-prone, doesn't handle encodings

**Implementation**: Create `index_parser.py` using lxml.html module.

### 7. GWT Module Descriptor Parsing

**Decision**: Use lxml XML parser with namespace-aware XPath queries.

**Rationale**:
- GWT module descriptors are valid XML with known namespace
- XPath efficiently extracts entry-points, inherits, source-paths
- Validates XML schema compliance
- Handles namespaces and entity references

**Alternatives Considered**:
- **Regex**: Can't handle XML namespaces, entity references
- **Custom XML parser**: Reinventing the wheel, lxml is battle-tested
- **Plain text parsing**: Misses nested structures, comments

**Implementation**: Create `gwt_module_parser.py` using lxml.etree with namespace map.

### 8. Circular Dependency Detection

**Decision**: Use visited set to track processed modules, detect and log cycles.

**Rationale**:
- GWT `<inherits>` clauses can form cycles (A inherits B inherits A)
- Visited set prevents infinite recursion
- Logging cycle detection helps identify configuration issues
- Process each module exactly once even in cycles

**Alternatives Considered**:
- **Depth limit**: Arbitrary, doesn't prevent cycles, may truncate valid inheritance
- **Ignore cycles**: Causes stack overflow or infinite loops
- **Fail on cycle**: Too strict, many valid GWT apps have cycles

**Implementation**: Add visited tracking to `gwt_navigation_analyzer.py` module traversal.

### 9. Performance Optimization

**Decision**: Stream navigation graph construction, cache parsed GWT modules in memory.

**Rationale**:
- Large GWT apps can have 100+ modules with complex inheritance
- Caching parsed modules avoids re-parsing inherited modules
- Stream node creation prevents memory spike from loading entire graph
- Batched Weaviate updates maintain indexing performance

**Alternatives Considered**:
- **Load entire graph then process**: Memory spike for large apps
- **No caching**: Re-parses inherited modules multiple times (slow)
- **Disk caching**: I/O overhead, complexity

**Implementation**: In-memory LRU cache for GWT modules, streaming node creation.

### 10. Metrics Collection

**Decision**: Log structured metrics in JSON format for parsing and monitoring.

**Rationale**:
- Structured JSON enables automated log parsing and dashboards
- Metrics include: timeout count, retry count, fallback count, FK sources, navigation node count
- Summary metrics logged at end of each pipeline stage
- Individual metrics at DEBUG level for detailed diagnostics

**Alternatives Considered**:
- **Plain text logs**: Hard to parse, no structured querying
- **Separate metrics file**: Complicates deployment, synchronization issues
- **External metrics system**: Overkill for CLI tool, adds dependencies

**Implementation**: Add metrics dict to services, log with `logger.info(json.dumps(metrics))`.

## Data Model

See [data-model.md](./data-model.md) for detailed entity definitions.

**Key Entities**:
- **NavigationGraph**: Complete UI navigation structure from entry points
- **NavigationNode**: Single node (Presenter/View/Activity/Place/External)
- **GWTModule**: Parsed *.gwt.xml module descriptor
- **PresenterViewBinding**: Presenter-View-UiBinder relationship
- **UiBinderHierarchy**: Widget hierarchy from UiBinder template
- **ForeignKeyRelationship**: Database FK with source tracking (Java/iBATIS/SQL)
- **TimeoutMetric**: Ollama timeout event details

## API Contracts

See [contracts/](./contracts/) directory for detailed internal API specifications.

**Key Internal Contracts**:
- `OllamaClient.extract_with_timeout()`: Adaptive timeout with fallback
- `StructuralAnalyzer.extract_basic_metadata()`: Fallback extraction
- `DBAnalyzer.extract_foreign_keys()`: Multi-source FK extraction
- `IndexParser.extract_gwt_modules()`: Parse index.html/jsp for modules
- `GWTModuleParser.parse_module()`: Parse *.gwt.xml descriptor
- `GWTNavigationAnalyzer.build_navigation_graph()`: Build complete graph

## Testing Strategy

See [quickstart.md](./quickstart.md) for test scenarios and validation steps.

**Test Coverage Targets**:
- Timeout handling: >90% (critical for reliability)
- FK extraction: >85% (critical for data model accuracy)
- Navigation analysis: >80% (complex graph algorithms)
- Index/module parsing: >90% (deterministic parsing)

**Integration Test Scenarios**:
1. Full pipeline on cuco-ui-admin codebase (539 files)
2. Timeout simulation with mock slow Ollama responses
3. DAO analysis with known FK patterns (4 previously failing cases)
4. GWT navigation from index.jsp through 50+ modules

**Performance Benchmarks**:
- Baseline: Current pipeline execution time on cuco-ui-admin
- Target: New pipeline execution time <20% increase
- Measure: Timeout overhead, FK extraction overhead, navigation analysis overhead

## Dependencies

**No New External Dependencies**: All required libraries already in requirements.txt:
- lxml (XML/HTML parsing)
- javalang (Java AST parsing)
- Click (CLI framework)
- Pydantic (data validation)

**Service Dependencies**:
- Ollama: Local LLM service on port 11434 (existing)
- Weaviate: Vector database on port 8080 (existing)
- Docker: For Weaviate container (existing)

## Migration Plan

**Breaking Changes**: None. All changes are additive or internal improvements.

**Configuration Changes**:
- **Optional**: Set `READ_TIMEOUT` environment variable for custom timeout (default 600s remains)
- **Optional**: Increase Docker Weaviate memory if indexing very large GWT apps (>500 modules)

**Data Migration**: None required. Existing Weaviate artifacts compatible with new metadata fields.

**Rollback Plan**: Git revert to previous commit. No data migration needed, so zero rollback risk.

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Exponential backoff delays pipeline too much | HIGH | LOW | Configurable retry count, max 3 attempts, fallback after 65s |
| Structural fallback produces low-quality metadata | MEDIUM | MEDIUM | Log fallback usage, document limitations, prioritize Ollama fixes |
| GWT module parsing misses complex inheritance | MEDIUM | MEDIUM | Comprehensive test fixtures, log parsing failures with file paths |
| Navigation graph memory usage spikes | LOW | LOW | Streaming construction, LRU cache with size limit |
| SQL JOIN parsing has false positives | LOW | MEDIUM | Validate FK columns exist, mark source as "SQL" with lower confidence |
| Performance degrades beyond 20% overhead | MEDIUM | LOW | Profile hotspots, optimize navigation caching, parallelize where safe |

## Success Metrics

**Quantitative**:
- Zero Ollama timeout failures on cuco-ui-admin (539 files)
- All 4 DAO FK validation errors resolved
- >90% GWT Presenters/Views discovered (target ~100-200 components)
- Pipeline execution time increase <20%

**Qualitative**:
- Developers can understand complete GWT application structure from PRD
- Error messages provide clear remediation steps
- Timeout fallback doesn't significantly degrade documentation quality
- Navigation diagrams visually communicate application flow

**Validation Steps**:
1. Run `./run.sh cuco-ui-admin` and verify zero timeout errors in logs
2. Check status output for FK extraction metrics (0 validation failures)
3. Count discovered GWT components in PRD (target >90% of known components)
4. Compare pipeline execution times (before/after, target <20% increase)
5. Manual review of generated PRD for completeness and accuracy
