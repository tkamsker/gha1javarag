<!--
SYNC IMPACT REPORT
==================
Version Change: None → 1.0.0 (Initial Constitution)
Type: MINOR (New constitution establishment)

Modified Principles: N/A (initial version)

Added Sections:
- Core Principles (5 principles)
  - I. Code Quality Standards
  - II. Testing Discipline
  - III. User Experience Consistency
  - IV. Performance Requirements
  - V. Observability & Monitoring
- Quality Assurance Gates
- Development Workflow
- Governance

Removed Sections: N/A (initial version)

Templates Requiring Updates:
- ✅ .specify/templates/plan-template.md (Constitution Check section validated)
- ✅ .specify/templates/spec-template.md (Requirements section aligned)
- ✅ .specify/templates/tasks-template.md (Task phases aligned with testing discipline)

Follow-up TODOs:
- Ratification date set to project initialization date (2025-12-12)
- Monitor compliance in first feature implementation cycle
-->

# GEMINI Code Analysis Pipeline Constitution

## Core Principles

### I. Code Quality Standards

All code contributed to this project MUST meet the following quality requirements:

- **Type Safety**: Python code MUST use type hints for all function signatures and class attributes. External data boundaries (CLI args, environment variables, API responses, Weaviate queries) MUST be validated explicitly.
- **Error Handling**: All external dependencies (Weaviate, Ollama, file I/O) MUST have explicit error handling with meaningful error messages. Network operations MUST implement retry logic with exponential backoff.
- **Code Organization**: CLI commands MUST be organized by pipeline stage (discover, extract, index, search, prd). Each stage MUST be independently executable. Shared utilities MUST reside in dedicated modules (not mixed with business logic).
- **Configuration Management**: Configuration MUST follow priority: CLI args > environment variables > .env file > defaults. All configuration options MUST be documented with examples in .env.example.
- **Documentation**: All public functions MUST have docstrings describing purpose, parameters, return values, and exceptions. Complex algorithms (parsing, extraction) MUST include inline comments explaining business logic.

**Rationale**: This is a code analysis pipeline that processes diverse Java/JSP/GWT codebases. Type safety and error handling prevent runtime failures during long-running analysis jobs. Clear code organization enables users to run individual pipeline stages for debugging.

### II. Testing Discipline

Testing is mandatory for all features. The following testing standards MUST be followed:

- **Test Pyramid**: Unit tests for extraction logic and data transformations. Integration tests for Weaviate indexing and search. End-to-end tests for complete pipeline execution.
- **Test Isolation**: Unit tests MUST NOT depend on external services (Weaviate, Ollama). Use mocks or fixtures for external dependencies. Integration tests MUST use test-specific Weaviate collections that are cleaned up after execution.
- **Test Data**: Tests MUST include realistic Java/JSP/GWT code samples covering edge cases (malformed XML, missing dependencies, edge syntax). Test fixtures MUST be stored in tests/fixtures/ with clear naming.
- **Coverage Requirements**: New features MUST have test coverage for core logic paths. Critical components (extraction parsers, indexing logic, search query builders) MUST achieve >80% test coverage.
- **Test Performance**: Unit tests MUST complete in <100ms each. Integration tests MUST complete in <5 seconds each. Pipeline tests using real codebases MUST be marked with @pytest.mark.slow and excluded from default test runs.
- **Test-Driven Development**: For new extraction patterns or artifact types, tests MUST be written first to validate expected behavior before implementation.

**Rationale**: The pipeline analyzes diverse and potentially malformed codebases. Comprehensive testing prevents regressions when adding support for new frameworks (GWT versions, JSP variants). Fast tests enable rapid iteration during parser development.

### III. User Experience Consistency

The pipeline provides both CLI and programmatic interfaces. All user-facing components MUST provide consistent experiences:

- **CLI Design**: Commands MUST follow pattern: `python src/main.py <stage> --project <name> [options]`. All commands MUST support `--help` with clear descriptions and examples. Long-running operations (indexing, PRD generation) MUST show progress indicators.
- **Output Formats**: CLI output MUST be human-readable by default. All commands MUST support `--format json` for programmatic consumption. Error messages MUST include actionable guidance (e.g., "Weaviate not accessible at http://localhost:8080. Run ./docker-weaviate.sh start").
- **Logging**: Use structured logging with levels: ERROR (failures requiring user action), WARNING (degraded functionality), INFO (pipeline progress), DEBUG (detailed diagnostics). Log output MUST respect LOG_LEVEL environment variable.
- **Documentation**: All features MUST be documented in CLAUDE.md with working examples. Breaking changes MUST update both CLAUDE.md and .env.example. Common troubleshooting scenarios MUST be documented.
- **Generated Artifacts**: PRD outputs MUST follow consistent Markdown structure compatible with Spec Kit. All generated files MUST include metadata (project name, generation timestamp, pipeline version).

**Rationale**: Users analyze large codebases spanning months. Consistent CLI interfaces and clear error messages reduce cognitive load. Progress indicators and structured logging enable debugging long-running analysis jobs.

### IV. Performance Requirements

The pipeline MUST handle large-scale Java codebases efficiently:

- **Discovery Performance**: File discovery MUST process at >1000 files/second. Large codebases (>100k files) MUST stream results rather than loading all paths into memory.
- **Extraction Performance**: Extraction MUST process at >50 Java files/second for typical enterprise code. Extraction errors in individual files MUST NOT block processing of other files.
- **Indexing Performance**: Weaviate indexing MUST batch operations (minimum 50 objects per batch). Indexing MUST be idempotent (re-running updates existing objects rather than duplicating).
- **Search Performance**: Vector search queries MUST complete in <2 seconds for typical queries. Search MUST support project filtering without full collection scans.
- **Memory Management**: Pipeline stages MUST process large codebases in streaming fashion. Peak memory usage MUST NOT exceed 2GB for processing 100k+ file codebases.
- **Resource Cleanup**: All external connections (Weaviate, Ollama) MUST be properly closed after use. Failed operations MUST not leak resources.

**Rationale**: Enterprise Java codebases can contain 100k+ files across multiple subprojects. Memory-efficient streaming and batching prevent OOM errors. Idempotent indexing enables incremental updates without reprocessing entire codebases.

### V. Observability & Monitoring

All pipeline operations MUST be observable for debugging and optimization:

- **Metrics Collection**: Each pipeline stage MUST log summary metrics (files discovered, artifacts extracted, objects indexed, search results). Metrics MUST be logged in structured format for parsing.
- **Diagnostic Tools**: The weaviate_stats.py tool MUST be maintained to diagnose indexing issues. All diagnostic tools MUST output human-readable summaries with actionable insights.
- **Progress Tracking**: Long-running operations MUST emit progress updates every 5 seconds or 1000 items processed (whichever is sooner). Progress MUST include estimated completion time when possible.
- **Error Aggregation**: Pipeline MUST collect and summarize errors by type (e.g., "150 JSP parse errors, 23 missing dependencies"). Detailed errors MUST be logged at DEBUG level.
- **Integration Health**: Pipeline MUST validate external service health (Ollama accessible, Weaviate schema exists) before starting operations. Health checks MUST provide clear status and remediation steps.

**Rationale**: Analyzing large codebases can take hours. Detailed metrics and progress tracking enable users to identify bottlenecks, estimate completion times, and debug issues without rerunning entire pipelines.

## Quality Assurance Gates

All feature implementations MUST pass these gates before merging:

### Gate 1: Pre-Implementation (Blocking)

- [ ] Constitution compliance reviewed and documented
- [ ] Test strategy defined (unit, integration, fixtures needed)
- [ ] External dependencies documented (Weaviate schema changes, new Ollama models)
- [ ] Performance impact assessed (expected throughput, memory usage)
- [ ] User-facing changes documented in CLAUDE.md

### Gate 2: Implementation Complete

- [ ] All tests passing (unit, integration)
- [ ] Test coverage meets requirements (>80% for critical components)
- [ ] CLI help text and error messages reviewed for clarity
- [ ] Logging statements use appropriate levels and include context
- [ ] Type hints added for all new functions and classes

### Gate 3: Integration Ready

- [ ] Integration tests validate end-to-end workflows
- [ ] Performance requirements validated (throughput, memory usage)
- [ ] Error handling tested with realistic failure scenarios (Weaviate down, malformed code)
- [ ] Documentation updated (CLAUDE.md, .env.example)
- [ ] Breaking changes noted in commit message and migration guide provided

## Development Workflow

### Feature Development Process

1. **Specification**: Create feature spec using /speckit.specify following constitution principles
2. **Planning**: Generate implementation plan with /speckit.plan including constitution compliance checks
3. **Test Design**: Write test cases covering core logic and edge cases
4. **Implementation**: Implement feature following code quality standards
5. **Validation**: Run full test suite and validate performance requirements
6. **Documentation**: Update CLAUDE.md with usage examples and troubleshooting
7. **Review**: Verify all quality gates passed before committing

### Testing Workflow

- Run unit tests before each commit: `pytest tests/unit/`
- Run integration tests before PR: `pytest tests/integration/`
- Run full pipeline test on sample codebase before release
- Use pytest markers to separate fast tests from slow end-to-end tests

### Code Review Requirements

- All PRs MUST include test coverage for new code
- Breaking changes MUST include migration documentation
- Performance-critical changes MUST include benchmark results
- Documentation updates MUST be included with feature PRs

## Governance

### Constitutional Authority

This constitution supersedes all other development practices. All feature implementations, code reviews, and architectural decisions MUST comply with these principles. Violations MUST be explicitly justified and documented in plan.md Complexity Tracking section.

### Amendment Process

Constitutional amendments require:
1. Documented proposal with rationale and impact analysis
2. Review by project maintainers
3. Version increment following semantic versioning (MAJOR for breaking principle changes, MINOR for new principles, PATCH for clarifications)
4. Update of all dependent templates (.specify/templates/)
5. Migration guidance for existing code if applicable

### Compliance Verification

- All planning documents MUST include Constitution Check section validating compliance
- Code reviews MUST verify adherence to code quality and testing standards
- Performance requirements MUST be validated with benchmarks for critical features
- Documentation updates MUST be verified for accuracy and completeness

### Living Document

This constitution is a living document. As the pipeline evolves to support new frameworks (additional GWT versions, Spring configurations) or use cases (GraphQL APIs, microservices), principles may be refined. All amendments MUST maintain backward compatibility with existing features unless breaking changes are explicitly justified.

**Version**: 1.0.0 | **Ratified**: 2025-12-12 | **Last Amended**: 2025-12-12
