# Implementation Plan: GWT Application Support for PRD Generation

**Branch**: `001-gwt-prd-support` | **Date**: 2025-12-14 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-gwt-prd-support/spec.md`

## Summary

Add GWT (Google Web Toolkit) application support to the Java codebase indexer PRD generation system. Currently, the system generates empty PRDs (0 endpoints, 0 components) for GWT applications because it only recognizes traditional Java EE patterns (DAOs, REST services, JSP). This feature will implement specialized analyzers for GWT RPC servlets, MVP presenters/views, UiBinder XML templates, and shared DTOs to enable complete PRD generation for GWT codebases.

**Technical Approach**: Create four new analyzer modules (GWT RPC, Presenter, View, Model) that detect GWT-specific patterns through file naming conventions and semantic analysis. Enhance existing XML parser to handle HTML entities. Extend service and frontend analyzers to recognize GWT patterns alongside Java EE patterns. Leverage existing indexed data in Weaviate where possible.

## Technical Context

**Language/Version**: Python 3.8+ (existing codebase requirement)
**Primary Dependencies**:
- lxml (XML parsing with HTML entity support)
- javalang or tree-sitter-java (Java AST parsing for RPC method extraction)
- Ollama client (semantic extraction via LLM)
- Weaviate Python client (vector database queries)

**Storage**: Weaviate vector database (existing - adds GWT-specific metadata fields)
**Testing**: pytest (existing test infrastructure)
**Target Platform**: CLI tool running on Linux/macOS developer machines
**Project Type**: Single project (Python CLI extending existing codebase)
**Performance Goals**:
- Process 200 GWT files in <10 minutes
- Extract >80% of RPC methods, presenters, views
- File discovery at >1000 files/second (existing requirement)

**Constraints**:
- Must maintain backward compatibility with Java EE analysis
- XML parsing must handle malformed templates with HTML entities
- Must function with or without LLM availability (fallback to structural parsing)
- Memory usage must stay <2GB for 100k+ file codebases (existing requirement)

**Scale/Scope**:
- Target: ~200 GWT files (cuco-ui-admin test case: 184 files)
- Real-world: Enterprise GWT apps with 1000+ client-side classes
- File types: .java (servlets, presenters, views), .ui.xml (UiBinder), *.gwt.xml (module descriptors)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate 1: Pre-Implementation (Blocking)

- [x] **Constitution compliance reviewed**: Feature adds new analyzers following existing patterns (db_analyzer, service_analyzer, frontend_analyzer). Extends classification system with GWT patterns.
- [x] **Test strategy defined**:
  - Unit tests: GWT pattern detection, RPC method extraction, UiBinder parsing with HTML entities
  - Integration tests: Weaviate queries for GWT artifacts, end-to-end PRD generation on cuco-ui-admin
  - Fixtures: Sample GWT servlet, presenter, view, UiBinder XML with entities, DTOs
- [x] **External dependencies documented**:
  - lxml XML parser (already dependency - enhanced usage for HTML entity handling)
  - Optional: javalang for Java AST parsing (if semantic extraction insufficient)
  - Weaviate schema: Add gwt_role, rpc_methods, presenter_view_binding fields to artifact metadata
  - Ollama: Enhanced prompts for GWT pattern detection (backward compatible)
- [x] **Performance impact assessed**:
  - Discovery: No impact (file classification remains O(n))
  - Extraction: +20% time for GWT files due to RPC method parsing (acceptable for 200-file codebases)
  - Indexing: No impact (same batch size, adds metadata fields)
  - Expected: 184-file test case completes in 8-10 minutes (within 10-minute goal)
- [x] **User-facing changes documented**: Will update CLAUDE.md with GWT support section, examples of GWT PRD generation, troubleshooting for UiBinder parsing errors

### Gate 2: Implementation Complete

- [ ] All tests passing (unit, integration)
- [ ] Test coverage >80% for new analyzers (gwt_rpc_analyzer, gwt_presenter_analyzer, gwt_view_analyzer, gwt_model_analyzer)
- [ ] CLI help text updated (prd command mentions GWT support)
- [ ] Logging includes GWT-specific context (e.g., "Found 15 RPC servlets", "Parsed 23 UiBinder templates")
- [ ] Type hints added for all new analyzer functions and classes

### Gate 3: Integration Ready

- [ ] Integration test validates cuco-ui-admin generates non-empty PRDs (>0 RPC endpoints, >0 UI components)
- [ ] Performance validated: 184-file codebase completes in <10 minutes
- [ ] Error handling tested: Malformed UiBinder XML, missing presenter bindings, empty RPC methods
- [ ] CLAUDE.md updated with GWT section and cuco-ui-admin example
- [ ] Breaking changes: None (additive feature)

## Project Structure

### Documentation (this feature)

```text
specs/001-gwt-prd-support/
├── plan.md              # This file
├── research.md          # Phase 0: GWT pattern research, library evaluation
├── data-model.md        # Phase 1: GWT artifact metadata model
├── quickstart.md        # Phase 1: Quick start guide for GWT PRD generation
├── contracts/           # Phase 1: Analyzer interfaces, Weaviate schema additions
└── tasks.md             # Phase 2: Implementation tasks (created by /speckit.tasks)
```

### Source Code (repository root)

```text
src/codeindex/
├── models/
│   └── __init__.py              # [EXTEND] Add GWT-specific metadata to artifact models
├── services/
│   ├── classifier.py            # [EXTEND] Add GWT file pattern detection
│   ├── extraction.py            # [EXTEND] Route GWT files to appropriate analyzer
│   ├── db_analyzer.py           # [EXTEND] Recognize shared DTOs as data model
│   ├── service_analyzer.py      # [EXTEND] Recognize RPC servlets as services
│   ├── frontend_analyzer.py     # [EXTEND] Parse UiBinder XML for UI components
│   ├── gwt_rpc_analyzer.py      # [NEW] Extract RPC servlet methods
│   ├── gwt_presenter_analyzer.py # [NEW] Extract MVP presenter logic
│   ├── gwt_view_analyzer.py     # [NEW] Extract MVP view components
│   └── gwt_model_analyzer.py    # [NEW] Extract shared DTOs
├── parsers/
│   └── xml_parser.py            # [EXTEND] Add HTML entity handling (already done)
├── schemas/
│   └── weaviate_schema.py       # [EXTEND] Add GWT metadata fields
├── cli/
│   └── prd.py                   # [EXTEND] Update PRD templates for GWT sections
└── utils/
    └── gwt_patterns.py          # [NEW] GWT pattern matching utilities

tests/
├── unit/
│   ├── test_gwt_rpc_analyzer.py # [NEW] Test RPC method extraction
│   ├── test_gwt_presenter_analyzer.py # [NEW] Test presenter analysis
│   ├── test_gwt_view_analyzer.py # [NEW] Test UiBinder parsing
│   ├── test_gwt_model_analyzer.py # [NEW] Test DTO extraction
│   └── test_classifier.py       # [EXTEND] Add GWT pattern tests
├── integration/
│   └── test_gwt_prd_generation.py # [NEW] E2E test on cuco-ui-admin
└── fixtures/
    └── gwt/                     # [NEW] Sample GWT files for testing
        ├── FlashInfoServletImpl.java
        ├── FlashAdministrationPresenter.java
        ├── FlashInfoEditView.java
        ├── FlashInfoEditView.ui.xml
        └── FlashInfoDTO.java
```

**Structure Decision**: Single project structure (Option 1) as this extends the existing Java codebase indexer CLI tool. New GWT analyzers follow the same pattern as existing analyzers (db_analyzer, service_analyzer, frontend_analyzer). No separate projects needed.

## Complexity Tracking

> **No constitutional violations - all patterns follow existing analyzer architecture**

No entries required. This feature:
- Adds 4 new analyzers following existing patterns
- Extends 3 existing analyzers with GWT detection
- Maintains <2GB memory requirement through streaming
- Achieves >80% coverage requirement with targeted test fixtures
- Uses existing error handling and retry patterns

All constitution principles (I-V) are satisfied by following established codebase patterns.
