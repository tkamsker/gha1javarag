# Implementation Plan: Maven Dependency Resolution and DTO Analysis

**Branch**: `004-maven-dependency-resolution` | **Date**: 2025-12-15 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-maven-dependency-resolution/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This feature extends the Java Codebase Indexer to automatically discover and resolve Maven dependencies declared in pom.xml files, enabling analysis of multi-module projects with dependent artifacts. It adds DTO (Data Transfer Object) pattern recognition to identify and analyze data structures exchanged between layers. The system resolves dependencies by mapping artifactId to directory paths under JAVA_SOURCE_DIR, supports project-scoped analysis via --project parameter, and extracts DTO metadata including validation annotations and serialization markers.

**Technical Approach**: Extend existing discovery service to parse pom.xml using XML parser, resolve artifact paths by combining JAVA_SOURCE_DIR + artifactId, implement circular dependency detection with visited artifact tracking, enhance classifier with DTO naming and structural pattern recognition, extend extraction service to capture JSR-303 validation annotations and serialization markers.

## Technical Context

**Language/Version**: Python 3.8+ (minimum for type hints and async support, consistent with Feature 001)
**Primary Dependencies**:
- lxml or xml.etree.ElementTree (pom.xml parsing)
- Existing: weaviate-client, ollama, click (CLI), pytest (testing)

**Storage**: Weaviate vector database (existing) - extended with DtoArtifact schema
**Testing**: pytest with unit tests (parsers, classifiers), integration tests (Weaviate indexing), E2E tests (full pipeline)
**Target Platform**: Linux/macOS server environments (existing deployment model)
**Project Type**: Single project (CLI application) - extends existing src/codeindex/ structure

**Performance Goals**:
- Dependency resolution: <10 seconds for 20 dependencies (SC-003)
- DTO classification: >90% accuracy (SC-002)
- Maven dependency resolution: >95% success rate (SC-001)
- Discovery throughput: >1000 files/second (existing requirement)

**Constraints**:
- Local source tree only (no Maven Central downloads)
- First-match strategy for duplicate artifacts (log warnings)
- Default depth=1 for dependencies (configurable via --dependency-depth)
- Memory efficient: streaming for large dependency graphs

**Scale/Scope**:
- Multi-module Maven projects with up to 20 direct dependencies
- Typical enterprise Java codebases (50k-100k+ files)
- 50-200% inventory increase expected from dependency resolution (SC-004)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate 1: Pre-Implementation (Blocking)

- [x] **Constitution compliance reviewed and documented**
  - Code Quality Standards: Type hints for all new functions (maven parser, DTO classifier), error handling for pom.xml parsing with meaningful messages
  - Testing Discipline: Unit tests for maven parser (malformed XML), DTO classifier (edge cases), integration tests for dependency graph resolution
  - User Experience Consistency: CLI follows existing pattern `codeindex discover --project <name> --dependency-depth <n>`, error messages include actionable guidance ("pom.xml not found at {path}")
  - Performance Requirements: Streaming dependency resolution (not loading all into memory), idempotent indexing (DTO artifacts update existing records)
  - Observability: Progress tracking for dependency resolution, metrics logged (dependencies resolved, DTOs classified)

- [x] **Test strategy defined**
  - Unit tests: Maven POM parser with fixtures (valid pom.xml, missing dependencies, circular refs), DTO classifier (naming patterns, structural analysis, entity vs DTO)
  - Integration tests: End-to-end dependency resolution on test project, Weaviate indexing of DTO artifacts
  - Fixtures needed: Sample pom.xml files (simple, multi-module, circular), DTO classes (standard naming, non-standard, entities, nested DTOs)

- [x] **External dependencies documented**
  - Weaviate schema change: New DtoArtifact class with fields (fields array, validation_rules, serialization_markers, nested_dtos, package_location)
  - Ollama: No new models required (uses existing gemma3:12b for extraction)
  - New Python dependency: lxml or xml.etree.ElementTree (stdlib) for pom.xml parsing

- [x] **Performance impact assessed**
  - Discovery stage: +2-5 seconds for pom.xml parsing per project (linear with dependency count)
  - Extraction stage: +10-20ms per DTO file for validation annotation extraction
  - Indexing stage: +50-100 DTO artifacts per typical project (minimal impact, batched)
  - Memory usage: +5-10MB for dependency graph tracking (well within 2GB limit)

- [x] **User-facing changes documented in CLAUDE.md**
  - New CLI parameters: --project <subdirectory>, --dependency-depth <n>
  - New artifact type: DtoArtifact visible in search and PRD generation
  - Configuration: No new .env variables required (uses existing JAVA_SOURCE_DIR)
  - Usage examples: `codeindex discover --project cuco-ui-admin --dependency-depth 2`

### Gate 2: Implementation Complete

- [ ] All tests passing (unit, integration)
- [ ] Test coverage meets requirements (>80% for maven parser, DTO classifier)
- [ ] CLI help text and error messages reviewed for clarity
- [ ] Logging statements use appropriate levels and include context
- [ ] Type hints added for all new functions and classes

### Gate 3: Integration Ready

- [ ] Integration tests validate end-to-end workflows
- [ ] Performance requirements validated (throughput, memory usage)
- [ ] Error handling tested with realistic failure scenarios (missing pom.xml, malformed XML, circular dependencies)
- [ ] Documentation updated (CLAUDE.md, .env.example if needed)
- [ ] Breaking changes noted in commit message and migration guide provided

**Violations Requiring Justification**: None - feature fully complies with constitution principles.

## Project Structure

### Documentation (this feature)

```text
specs/004-maven-dependency-resolution/
├── plan.md              # This file (/speckit.plan command output)
├── spec.md              # Feature specification (complete)
├── research.md          # Phase 0 output (to be generated)
├── data-model.md        # Phase 1 output (to be generated)
├── quickstart.md        # Phase 1 output (to be generated)
├── contracts/           # Phase 1 output (to be generated)
│   ├── maven-parser-api.yaml
│   └── dto-classifier-api.yaml
├── checklists/
│   └── requirements.md  # Specification quality checklist (complete)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/codeindex/
├── models/
│   ├── maven_dependency.py        # NEW: MavenDependency model
│   ├── dto_artifact.py            # NEW: DtoArtifact model
│   └── dependency_graph.py        # NEW: DependencyGraph model
├── services/
│   ├── discovery.py               # EXTENDED: Add dependency resolution
│   ├── maven_parser.py            # NEW: POM XML parsing
│   ├── dependency_resolver.py     # NEW: Dependency graph resolution
│   ├── classifier.py              # EXTENDED: Add DTO classification
│   └── extraction.py              # EXTENDED: Extract DTO metadata
├── parsers/
│   ├── java_parser.py             # EXTENDED: Extract validation annotations
│   └── pom_parser.py              # NEW: Dedicated POM XML parser
├── schemas/
│   └── dto_artifact_schema.py     # NEW: Weaviate schema for DTOs
├── cli/
│   ├── discover.py                # EXTENDED: Add --project, --dependency-depth params
│   ├── extract.py                 # EXTENDED: Handle DTO artifacts
│   └── index.py                   # EXTENDED: Index DTO artifacts
└── utils/
    ├── config.py                  # EXTENDED: Add new CLI params
    └── path_resolver.py           # NEW: JAVA_SOURCE_DIR + project path logic

tests/
├── unit/
│   ├── test_maven_parser.py       # NEW: POM parsing tests
│   ├── test_dependency_resolver.py # NEW: Dependency graph tests
│   ├── test_dto_classifier.py     # NEW: DTO classification tests
│   └── test_path_resolver.py      # NEW: Path resolution tests
├── integration/
│   ├── test_dependency_resolution.py # NEW: E2E dependency resolution
│   └── test_dto_indexing.py       # NEW: Weaviate DTO indexing
└── fixtures/
    ├── pom-files/                 # NEW: Sample pom.xml files
    │   ├── simple.xml
    │   ├── multi-module.xml
    │   └── circular-deps.xml
    └── dto-classes/               # NEW: Sample DTO Java files
        ├── standard-dto.java
        ├── nested-dto.java
        └── entity-vs-dto.java
```

**Structure Decision**: Single project (CLI application) structure is maintained. This feature extends existing pipeline stages (discover, extract, index) with new services and models. No new pipeline stages are introduced. The extension points are:
1. Discovery service: Add pom.xml parsing and dependency resolution
2. Classifier: Add DTO pattern recognition
3. Extraction service: Add DTO metadata extraction
4. Weaviate schemas: Add DtoArtifact class

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations requiring justification. Feature aligns with constitution:
- Single project structure (no additional projects)
- Streaming dependency resolution (performance requirement)
- Explicit error handling (code quality standard)
- Test-first approach for maven parser and DTO classifier (testing discipline)
