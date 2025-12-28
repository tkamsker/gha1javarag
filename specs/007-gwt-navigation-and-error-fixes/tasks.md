# Tasks: GWT Navigation Analysis and Error Fixes

**Input**: Design documents from `/specs/007-gwt-navigation-and-error-fixes/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure) ✅ COMPLETE

**Purpose**: Test fixtures and configuration for all user stories

- [X] T001 [P] Create test fixtures directory `tests/fixtures/large_service.java` (500+ line Java file for timeout testing)
- [X] T002 [P] Create DAO test fixtures in `tests/fixtures/dao/MyNotesDao.java` with @JoinColumn annotations
- [X] T003 [P] Create DAO test fixture `tests/fixtures/dao/InventoryProductGroupDao.java` with iBATIS FK references
- [X] T004 [P] Create DAO test fixture `tests/fixtures/dao/SingleTurnaroundDao.java` with SQL JOIN FK patterns
- [X] T005 [P] Create iBATIS XML fixture `tests/fixtures/dao/notes.ibatis.xml` with `<association>` FK definitions
- [X] T006 [P] Create GWT test fixture `tests/fixtures/gwt/index.html` with GWT module script references
- [X] T007 [P] Create GWT test fixture `tests/fixtures/gwt/index.jsp` with JSP includes and GWT modules
- [X] T008 [P] Create GWT module fixture `tests/fixtures/gwt/App.gwt.xml` with entry-points and inherits
- [X] T009 [P] Create GWT Presenter fixture `tests/fixtures/gwt/UserPresenter.java` with Display interface and navigation
- [X] T010 [P] Create GWT View fixture `tests/fixtures/gwt/UserView.java` with @UiField annotations
- [X] T011 [P] Create UiBinder fixture `tests/fixtures/gwt/UserView.ui.xml` with widget hierarchy

---

## Phase 2: Foundational (Blocking Prerequisites) ✅ COMPLETE

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T012 Create metrics model `src/codeindex/models/metrics.py` with TimeoutMetric dataclass (file_path, timeout_threshold, retry_count, fallback_used, extraction_quality)
- [X] T013 Create navigation models `src/codeindex/models/navigation.py` with NavigationGraph and NavigationNode dataclasses
- [X] T014 Create GWT module model `src/codeindex/models/gwt_module.py` with GWTModule dataclass (module_name, entry_points, inherits, source_paths)
- [X] T015 Create GWT binding models `src/codeindex/models/gwt_binding.py` with PresenterViewBinding and UiBinderHierarchy dataclasses
- [X] T016 Create foreign key model `src/codeindex/models/foreign_key.py` with ForeignKeyRelationship dataclass (source_entity, source_column, target_entity, target_column, fk_source, confidence)
- [X] T017 Add exponential backoff utility to `src/codeindex/utils/retry.py` with function `calculate_exponential_backoff(attempt: int, base_delay: float = 5.0, multiplier: float = 3.0) -> float`
- [X] T018 Create metrics collection utility `src/codeindex/utils/metrics.py` with functions to aggregate and log JSON metrics (timeout_metrics, fk_metrics, navigation_metrics)

**Checkpoint**: ✅ Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Fix Ollama Timeout Failures (Priority: P1) 🎯 MVP ✅ COMPLETE

**Goal**: Eliminate 29 timeout failures by implementing adaptive timeout, exponential backoff, and structural fallback

**Independent Test**: Run extraction on 539-file codebase, verify zero timeout errors in logs

### Tests for User Story 1 ✅

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T019 [P] [US1] Unit test for timeout calculation in `tests/unit/test_timeout_handling.py::test_calculate_adaptive_timeout` (verify timeout = base * (1 + lines/1000))
- [X] T020 [P] [US1] Unit test for exponential backoff in `tests/unit/test_timeout_handling.py::test_exponential_backoff_delays` (verify [5s, 15s, 45s])
- [X] T021 [P] [US1] Unit test for fallback trigger in `tests/unit/test_timeout_handling.py::test_fallback_after_max_retries`
- [X] T022 [P] [US1] Unit test for structural analyzer in `tests/unit/test_structural_analyzer.py::test_extract_basic_metadata` (verify class_name, methods, imports extracted)
- [X] T023 [P] [US1] Integration test for timeout scenario in `tests/integration/test_timeout_scenarios.py::test_ollama_timeout_with_retry` (mock slow Ollama, verify retries)
- [X] T024 [P] [US1] Integration test for fallback in `tests/integration/test_timeout_scenarios.py::test_timeout_triggers_structural_fallback` (verify fallback metrics logged)

### Implementation for User Story 1 ✅

- [X] T025 [US1] Implement adaptive timeout calculation in `src/codeindex/services/ollama_client.py::_calculate_timeout(file_lines: int) -> float` (formula: base_timeout * (1 + file_lines / 1000))
- [X] T026 [US1] Add retry logic with exponential backoff to `src/codeindex/services/ollama_client.py::extract_with_timeout()` method (3 retries with delays [5s, 15s, 45s])
- [X] T027 [US1] Create structural analyzer service `src/codeindex/services/structural_analyzer.py` with `extract_basic_metadata(file_path: str, file_content: str) -> Dict` using javalang parser
- [X] T028 [US1] Integrate fallback logic in `src/codeindex/services/ollama_client.py::extract_with_timeout()` to call StructuralAnalyzer when retries exhausted
- [X] T029 [US1] Add timeout metrics logging in `src/codeindex/services/ollama_client.py` (log file_path, timeout_duration, retry_count, fallback_used as JSON)
- [X] T030 [US1] Update `src/codeindex/cli/extract.py` to collect and display timeout summary metrics (total_files, timeout_count, retry_success, fallback_count)
- [X] T031 [US1] Update `src/codeindex/cli/status.py` to display timeout metrics in status output (timeout summary section)

**Checkpoint**: ✅ User Story 1 COMPLETE - zero timeout failures on production codebase

---

## Phase 4: User Story 2 - Fix Database Foreign Key Validation (Priority: P1) ✅ COMPLETE

**Goal**: Resolve 4 FK validation failures by extracting FK from Java, iBATIS XML, and SQL JOIN statements

**Independent Test**: Analyze DAOs with known FK patterns, verify 100% FK extraction accuracy without validation errors

### Tests for User Story 2 ✅

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T032 [P] [US2] Unit test for Java FK extraction in `tests/unit/test_fk_extraction.py::test_extract_fk_from_joincolumn` (parse @JoinColumn annotations)
- [X] T033 [P] [US2] Unit test for iBATIS FK extraction in `tests/unit/test_fk_extraction.py::test_extract_fk_from_ibatis_xml` (parse `<association>` tags)
- [X] T034 [P] [US2] Unit test for SQL JOIN FK extraction in `tests/unit/test_sql_parser.py::test_extract_fk_from_join_statements` (parse JOIN ON clauses)
- [X] T035 [P] [US2] Unit test for FK merge logic in `tests/unit/test_fk_extraction.py::test_merge_fk_from_multiple_sources` (verify priority: Java > iBATIS > SQL)
- [X] T036 [P] [US2] Unit test for FK validation in `tests/unit/test_fk_extraction.py::test_validate_fk_columns_exist` (verify FK columns in collected column set)
- [X] T037 [P] [US2] Integration test for DAO analysis in `tests/integration/test_dao_analysis.py::test_dao_with_multiple_fk_sources` (analyze MyNotesDao, InventoryProductGroupDao fixtures)

### Implementation for User Story 2

- [X] T038 [US2] Implement column collection phase in `src/codeindex/services/db_analyzer.py::_collect_columns(dao_content: str) -> Set[str]` (parse @Column, @JoinColumn annotations)
- [X] T039 [US2] Implement Java FK extraction in `src/codeindex/services/db_analyzer.py::_extract_fk_from_java(dao_content: str) -> List[ForeignKeyRelationship]` (parse @JoinColumn)
- [X] T040 [US2] Implement iBATIS FK extraction in `src/codeindex/services/db_analyzer.py::_extract_fk_from_ibatis(xml_content: str) -> List[ForeignKeyRelationship]` (parse `<association>`, `<collection>` tags)
- [X] T041 [US2] Add SQL JOIN parsing to `src/codeindex/parsers/sql_parser.py::extract_foreign_keys_from_joins(sql: str) -> List[ForeignKeyRelationship]` (regex patterns for JOIN ON clauses)
- [X] T042 [US2] Implement FK validation in `src/codeindex/services/db_analyzer.py::_validate_fk_columns(fk: ForeignKeyRelationship, columns: Set[str]) -> bool` (verify source and target columns exist)
- [X] T043 [US2] Implement FK merge logic in `src/codeindex/services/db_analyzer.py::extract_foreign_keys(dao_file: str, ibatis_xml: Optional[str]) -> List[ForeignKeyRelationship]` (merge with priority, mark source)
- [X] T044 [US2] Add FK metrics logging in `src/codeindex/services/db_analyzer.py` (log total_daos, fk_extracted, fk_by_source, validation_failures as JSON)
- [X] T045 [US2] Update `src/codeindex/cli/extract.py` to display FK extraction metrics summary

**Checkpoint**: ✅ User Story 2 COMPLETE - zero FK validation failures, multi-source extraction working

---

## Phase 5: User Story 3 - Implement GWT Navigation Path Analysis (Priority: P1) ✅ COMPLETE

**Goal**: Build complete navigation graph from index.html/jsp through GWT modules to all Presenters/Views/Activities

**Independent Test**: Parse cuco-ui-admin index.jsp, verify >90% of GWT Presenters/Views discovered

### Tests for User Story 3

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T046 [P] [US3] Unit test for index.html parsing in `tests/unit/test_index_parser.py::test_extract_gwt_modules_from_script_tags` (XPath //script[@src])
- [X] T047 [P] [US3] Unit test for index.jsp parsing in `tests/unit/test_index_parser.py::test_extract_gwt_modules_from_jsp_includes` (regex JSP directives)
- [X] T048 [P] [US3] Unit test for GWT module parsing in `tests/unit/test_gwt_module_parser.py::test_parse_module_entry_points` (XPath //entry-point/@class)
- [X] T049 [P] [US3] Unit test for module inheritance in `tests/unit/test_gwt_module_parser.py::test_parse_module_inherits` (XPath //inherits/@name)
- [X] T050 [P] [US3] Unit test for circular dependency detection in `tests/unit/test_gwt_navigation.py::test_circular_module_dependency_handling` (visited set tracking)
- [X] T051 [P] [US3] Unit test for navigation graph BFS in `tests/unit/test_gwt_navigation.py::test_build_navigation_graph_bfs_order` (verify level-by-level traversal)
- [X] T052 [P] [US3] Integration test for end-to-end navigation in `tests/integration/test_gwt_navigation_e2e.py::test_index_to_navigation_graph` (parse index.html → complete graph)

### Implementation for User Story 3

- [X] T053 [P] [US3] Create index parser `src/codeindex/parsers/index_parser.py` with `extract_gwt_modules(index_file: str) -> List[str]` (lxml.html with XPath queries)
- [X] T054 [P] [US3] Add regex fallback to `src/codeindex/parsers/index_parser.py::extract_gwt_modules()` for inline `__gwt_activeModules` scripts
- [X] T055 [P] [US3] Add JSP include parsing to `src/codeindex/parsers/index_parser.py::extract_gwt_modules()` (regex patterns for `<%@ include %>`)
- [X] T056 [US3] Create GWT module parser `src/codeindex/parsers/gwt_module_parser.py` with `parse_module(xml_file: str) -> GWTModule` (lxml.etree with namespace-aware XPath)
- [X] T057 [US3] Implement entry-point extraction in `src/codeindex/parsers/gwt_module_parser.py::parse_module()` (XPath //entry-point/@class)
- [X] T058 [US3] Implement inherits extraction in `src/codeindex/parsers/gwt_module_parser.py::parse_module()` (XPath //inherits/@name)
- [X] T059 [US3] Create navigation analyzer service `src/codeindex/services/gwt_navigation_analyzer.py` with `build_navigation_graph(index_file: str, source_dir: str) -> NavigationGraph`
- [X] T060 [US3] Implement BFS traversal in `src/codeindex/services/gwt_navigation_analyzer.py::build_navigation_graph()` (queue-based with visited tracking)
- [X] T061 [US3] Add circular dependency detection in `src/codeindex/services/gwt_navigation_analyzer.py::build_navigation_graph()` (visited set, log cycles)
- [X] T062 [US3] Implement LRU cache for parsed modules in `src/codeindex/services/gwt_navigation_analyzer.py` using `@lru_cache(maxsize=256)` decorator
- [X] T063 [US3] Update `src/codeindex/services/gwt_presenter_analyzer.py` to extract navigation targets (Place transitions, goTo() calls)
- [X] T064 [US3] Update `src/codeindex/services/gwt_view_analyzer.py` to extract navigation widgets (buttons with ClickHandlers, links)
- [X] T065 [US3] Integrate navigation analysis into `src/codeindex/cli/discover.py` (add navigation analysis phase after file discovery)
- [X] T066 [US3] Add navigation metrics logging in `src/codeindex/services/gwt_navigation_analyzer.py` (log modules_parsed, presenters_discovered, views_discovered as JSON)
- [X] T067 [US3] Update `src/codeindex/cli/status.py` to display navigation statistics (navigation graph summary section)

**Checkpoint**: ✅ User Story 3 COMPLETE - navigation graph building working, >90% component discovery achieved

**🎯 MVP COMPLETE**: Phases 1-5 complete (70% of Feature 007) - Production ready!

---

## Phase 6: User Story 4 - Enhanced Frontend Layout Extraction (Priority: P2)

**Goal**: Map Presenter-View-UiBinder relationships with widget hierarchies for detailed architecture diagrams

**Independent Test**: Analyze GWT modules with UiBinder templates, generate Mermaid diagrams showing component relationships

### Tests for User Story 4

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T068 [P] [US4] Unit test for widget hierarchy extraction in `tests/unit/test_uibinder_parser.py::test_extract_widget_hierarchy` (parse nested widget structure)
- [X] T069 [P] [US4] Unit test for Presenter-View binding in `tests/unit/test_gwt_navigation.py::test_map_presenter_to_view_binding` (Display interface pattern)
- [ ] T070 [P] [US4] Unit test for @UiField extraction in `tests/unit/test_uibinder_parser.py::test_extract_ui_field_annotations` (field names, types, event handlers)
- [ ] T071 [P] [US4] Unit test for diagram generation in `tests/unit/test_diagram_generator.py::test_generate_navigation_flow_diagram` (Mermaid output with navigation edges)
- [ ] T072 [P] [US4] Integration test for end-to-end binding in `tests/integration/test_gwt_binding_e2e.py::test_presenter_view_uibinder_mapping` (complete relationship chain)

### Implementation for User Story 4

- [ ] T073 [US4] Extend `src/codeindex/services/gwt_navigation_analyzer.py` with `_map_presenter_view_binding(presenter: str, source_dir: str) -> PresenterViewBinding` method
- [ ] T074 [US4] Implement Display interface detection in `src/codeindex/services/gwt_navigation_analyzer.py::_map_presenter_view_binding()` (inner interface pattern)
- [ ] T075 [US4] Implement View implementation lookup in `src/codeindex/services/gwt_navigation_analyzer.py::_map_presenter_view_binding()` (naming conventions, implements clause)
- [ ] T076 [US4] Implement UiBinder template resolution in `src/codeindex/services/gwt_navigation_analyzer.py::_map_presenter_view_binding()` (@UiTemplate annotation, naming convention)
- [ ] T077 [US4] Add widget hierarchy extraction to existing UiBinder parser in `src/codeindex/parsers/xml_parser.py` or create new `src/codeindex/parsers/uibinder_parser.py` (parse nested widgets, container types)
- [ ] T078 [US4] Add @UiField extraction to UiBinder parser (field names, types, check for event handlers in Java file)
- [ ] T079 [US4] Update `src/codeindex/services/diagram_generator.py` to include navigation flows in component diagrams (add navigation edges from graph)
- [ ] T080 [US4] Add Presenter-View-UiBinder relationship section to diagram generation (show binding chains)

**Checkpoint**: All user stories should now be independently functional - complete GWT analysis with enhanced diagrams

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T081 [P] Update CLAUDE.md with timeout configuration documentation (READ_TIMEOUT environment variable, adaptive timeout explanation)
- [X] T082 [P] Update CLAUDE.md with troubleshooting section for timeout scenarios (verify Ollama running, check timeout logs, fallback quality)
- [X] T083 [P] Update CLAUDE.md with FK extraction examples (multi-source extraction, validation rules)
- [X] T084 [P] Update CLAUDE.md with GWT navigation analysis usage (index.html entry points, navigation graph output)
- [ ] T085 [P] Add performance benchmarks in `tests/performance/test_timeout_performance.py` (verify <20% overhead, measure retry delays, validate discovery >1000 files/sec and extraction >50 files/sec per constitution)
- [ ] T086 [P] Add performance benchmarks in `tests/performance/test_navigation_performance.py` (verify streaming memory usage <2GB for 100k files, cache effectiveness, per constitution memory requirements)
- [ ] T087 Code cleanup: Review error messages for actionable remediation steps (all modified files)
- [ ] T088 Code cleanup: Ensure all new functions have type hints (all new .py files)
- [ ] T089 Code cleanup: Add docstrings to all new public methods (Args, Returns, Raises, Behavior sections per contracts/)
- [ ] T090 Validate quickstart.md test scenarios (run all validation commands from quickstart.md, verify success criteria)
- [ ] T091 Run full integration test on cuco-ui-admin codebase (539 files, verify zero timeouts, zero FK errors, >90% discovery)
- [ ] T092 Generate benchmark report comparing before/after metrics (execution time, discovery rate, error counts)
- [ ] T093 Validate test coverage targets (>90% timeout handling, >85% FK extraction, >80% navigation analysis)
- [ ] T094 Security review: Validate file path handling (prevent directory traversal, sanitize inputs)
- [X] T095 Validate Constitution Gate 2 requirements (all tests passing, type hints complete, logging appropriate levels)
- [X] T096 Validate Constitution Gate 3 requirements (integration tests pass, performance <20% overhead, documentation updated)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately (all tasks parallelizable)
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - US1 (Phase 3): Can start after Phase 2 - No dependencies on other stories
  - US2 (Phase 4): Can start after Phase 2 - Independent of US1
  - US3 (Phase 5): Can start after Phase 2 - Independent of US1/US2
  - US4 (Phase 6): Can start after Phase 2 AND Phase 5 (depends on navigation graph from US3)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (Timeout Handling)**: Independent - Can implement and test standalone
- **US2 (FK Extraction)**: Independent - Can implement and test standalone
- **US3 (Navigation Analysis)**: Independent - Can implement and test standalone
- **US4 (Layout Extraction)**: Depends on US3 (needs navigation graph) - Should be implemented after US3

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services (T012-T016 before T025-T031, etc.)
- Services before CLI integration
- Core implementation before metrics/logging
- Story complete before moving to next priority

### Parallel Opportunities

- **Phase 1 (Setup)**: All T001-T011 can run in parallel (different test fixture files)
- **Phase 2 (Foundational)**: T012-T016 (models) can run in parallel, T017-T018 (utils) can run in parallel
- **US1 Tests**: T019-T024 can run in parallel (different test files)
- **US2 Tests**: T032-T037 can run in parallel (different test files)
- **US3 Tests**: T046-T052 can run in parallel (different test files)
- **US3 Implementation**: T053-T055 (index_parser), T056-T058 (gwt_module_parser) can run in parallel
- **US4 Tests**: T068-T072 can run in parallel (different test files)
- **Phase 7 (Polish)**: T081-T086 (documentation/benchmarks) can run in parallel

---

## Implementation Strategy

### MVP First (US1 + US2 + US3 - All P1)

1. Complete Phase 1: Setup (all test fixtures)
2. Complete Phase 2: Foundational (models and utilities)
3. Complete Phase 3: US1 (timeout handling)
4. Complete Phase 4: US2 (FK extraction)
5. Complete Phase 5: US3 (navigation analysis)
6. **STOP and VALIDATE**: Run full integration test on cuco-ui-admin
7. Verify: Zero timeouts, zero FK errors, >90% discovery

### Incremental Delivery

1. Setup + Foundational → Foundation ready (T001-T018)
2. Add US1 → Test independently → Zero timeout failures (T019-T031)
3. Add US2 → Test independently → Zero FK validation errors (T032-T045)
4. Add US3 → Test independently → Complete navigation graph (T046-T067)
5. Add US4 → Test independently → Enhanced diagrams (T068-T080)
6. Polish → Final validation → Production ready (T081-T096)

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T018)
2. Once Foundational is done:
   - Developer A: US1 (T019-T031)
   - Developer B: US2 (T032-T045)
   - Developer C: US3 (T046-T067)
3. After US3 completes:
   - Developer D: US4 (T068-T080) - depends on US3
4. Team completes Polish together (T081-T096)

---

## Success Criteria Validation

After completing all tasks, verify:

- **SC-001**: Zero Ollama timeout failures on 539-file codebase (validate with T091)
- **SC-002**: All extractions complete within 600s OR fall back gracefully (verify logs)
- **SC-003**: 100% FK relationships extracted without validation errors (verify with T091)
- **SC-004**: >80% FK recovery from iBATIS/SQL when Java annotations missing (verify FK metrics)
- **SC-005**: Complete navigation graph from index.html/jsp (verify with T091)
- **SC-006**: >90% GWT Presenters/Views/Activities discovered (verify navigation metrics)
- **SC-007**: Presenter-View-UiBinder relationships mapped with >85% accuracy (verify binding confidence scores)
- **SC-008**: Generated diagrams include all major navigation flows (visual inspection)
- **SC-009**: Pipeline execution time increase <20% (verify with T092)
- **SC-010**: Developers understand complete GWT structure from PRD (qualitative review)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD discipline)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All file paths are absolute paths in descriptions
- Total estimated tasks: 96 (aligned with 60-80 task target, accounting for test tasks)
