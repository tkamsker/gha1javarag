# Tasks: GWT Application Support for PRD Generation

**Input**: Design documents from `/specs/001-gwt-prd-support/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Tests are included per user story requirements - each analyzer must have unit tests for validation

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/codeindex/`, `tests/` at repository root
- All paths shown assume Python package structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency installation

- [X] T001 Install javalang dependency by adding `javalang==0.13.0` to requirements.txt
- [X] T002 [P] Create test fixtures directory at tests/fixtures/gwt/
- [X] T003 [P] Copy GWT interface contracts from specs/001-gwt-prd-support/contracts/ to src/codeindex/contracts/ (for reference)
- [X] T004 [P] Create GWT utilities module at src/codeindex/utils/gwt_patterns.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Create hybrid Java parser at src/codeindex/parsers/hybrid_java_parser.py with javalang + regex fallback
- [X] T006 [P] Add GWT file patterns to classifier at src/codeindex/services/classifier.py (lines 365-400)
- [X] T007 [P] Update Weaviate schema with GWT metadata fields in src/codeindex/schemas/weaviate_schema.py
- [X] T008 Create GWT analyzer registry at src/codeindex/services/gwt_analyzer_registry.py
- [X] T009 Update extraction service routing at src/codeindex/services/extraction.py to use GWT analyzer registry
- [X] T010 [P] Create GWT pattern detector utility in src/codeindex/utils/gwt_patterns.py (implements GwtPatternDetector interface)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Generate PRDs from GWT RPC Servlets (Priority: P1) 🎯 MVP

**Goal**: Enable system to recognize and document GWT RPC servlets so PRDs show documented RPC endpoints instead of empty service sections

**Independent Test**: Run PRD generation on cuco-ui-admin and verify service layer PRD lists RPC methods with input/output types

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T011 [P] [US1] Create test fixture FlashInfoServletImpl.java in tests/fixtures/gwt/ with 3 RPC methods
- [X] T012 [P] [US1] Create test fixture FlashInfoService.java (service interface) in tests/fixtures/gwt/
- [X] T013 [P] [US1] Create test fixture FlashInfoServiceAsync.java (async interface) in tests/fixtures/gwt/
- [X] T014 [P] [US1] Unit test for GWT RPC pattern detection in tests/unit/test_gwt_rpc_analyzer.py
- [X] T015 [P] [US1] Unit test for RPC method extraction (javalang path) in tests/unit/test_gwt_rpc_analyzer.py
- [X] T016 [P] [US1] Unit test for RPC method extraction (regex fallback) in tests/unit/test_gwt_rpc_analyzer.py
- [X] T017 [P] [US1] Unit test for DTO reference extraction in tests/unit/test_gwt_rpc_analyzer.py

### Implementation for User Story 1

- [X] T018 [US1] Implement GwtRpcAnalyzer class in src/codeindex/services/gwt_rpc_analyzer.py following gwt_analyzer_interface.py contract
- [X] T019 [US1] Implement extract_rpc_methods() using hybrid parser in gwt_rpc_analyzer.py
- [X] T020 [US1] Implement identify_service_interface() in gwt_rpc_analyzer.py
- [X] T021 [US1] Implement extract_referenced_dtos() in gwt_rpc_analyzer.py
- [X] T022 [US1] Update service_analyzer.py to recognize RPC servlets as services (add GWT RPC detection at line ~150)
- [X] T023 [US1] Register GwtRpcAnalyzer in gwt_analyzer_registry.py
- [X] T024 [US1] Update PRD template at src/codeindex/cli/prd.py to add "RPC Endpoints" section for GWT servlets
- [X] T025 [US1] Add validation and error handling for malformed servlet files in gwt_rpc_analyzer.py
- [X] T026 [US1] Add logging for RPC servlet detection and method extraction in gwt_rpc_analyzer.py

**Checkpoint**: At this point, User Story 1 should be fully functional - PRDs should show RPC endpoints with methods

---

## Phase 4: User Story 2 - Extract UI Components from UiBinder Files (Priority: P2)

**Goal**: Enable system to parse UiBinder XML templates and extract form fields so frontend PRDs show UI components instead of empty forms

**Independent Test**: Run PRD generation on cuco-ui-admin and verify frontend PRD lists form fields from UiBinder templates

### Tests for User Story 2

- [ ] T027 [P] [US2] Create test fixture FlashInfoEditView.ui.xml in tests/fixtures/gwt/ with form fields including HTML entities (&nbsp;)
- [ ] T028 [P] [US2] Unit test for UiBinder XML parsing with HTML entities in tests/unit/test_gwt_view_analyzer.py
- [ ] T029 [P] [US2] Unit test for form field extraction (TextBox, TextArea, CheckBox) in tests/unit/test_gwt_view_analyzer.py
- [ ] T030 [P] [US2] Unit test for label matching heuristic in tests/unit/test_gwt_view_analyzer.py
- [ ] T031 [P] [US2] Unit test for ListBox options extraction in tests/unit/test_gwt_view_analyzer.py

### Implementation for User Story 2

- [ ] T032 [P] [US2] Implement GwtUiBinderParser class in src/codeindex/parsers/uibinder_parser.py following gwt_analyzer_interface.py contract
- [ ] T033 [US2] Implement parse_form_fields() with widget type mapping in uibinder_parser.py
- [ ] T034 [US2] Implement extract_select_options() for ListBox widgets in uibinder_parser.py
- [ ] T035 [US2] Implement find_associated_labels() heuristic in uibinder_parser.py
- [ ] T036 [US2] Update frontend_analyzer.py to use GwtUiBinderParser for *.ui.xml files (add at line ~200)
- [ ] T037 [US2] Register GwtUiBinderParser in gwt_analyzer_registry.py
- [ ] T038 [US2] Update PRD template at src/codeindex/cli/prd.py to add "UI Components" section for UiBinder forms
- [ ] T039 [US2] Add validation for missing ui:field attributes in uibinder_parser.py
- [ ] T040 [US2] Add logging for UiBinder parsing and form field extraction in uibinder_parser.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - PRDs show both RPC endpoints and UI components

---

## Phase 5: User Story 3 - Document MVP Pattern Relationships (Priority: P3)

**Goal**: Enable system to identify and document Model-View-Presenter pattern relationships so PRDs show how presenters connect to views

**Independent Test**: Run PRD generation on cuco-ui-admin and verify frontend PRD shows presenter-to-view bindings with confidence scores

### Tests for User Story 3

- [ ] T041 [P] [US3] Create test fixture FlashAdministrationPresenter.java in tests/fixtures/gwt/ with Display interface
- [ ] T042 [P] [US3] Create test fixture FlashAdministrationView.java in tests/fixtures/gwt/ implementing Display
- [ ] T043 [P] [US3] Create test fixture UserListPresenter.java with separate view interface binding
- [ ] T044 [P] [US3] Unit test for Display interface detection (90% confidence) in tests/unit/test_gwt_presenter_analyzer.py
- [ ] T045 [P] [US3] Unit test for separate interface detection (85% confidence) in tests/unit/test_gwt_presenter_analyzer.py
- [ ] T046 [P] [US3] Unit test for naming convention detection (70% confidence) in tests/unit/test_gwt_presenter_analyzer.py
- [ ] T047 [P] [US3] Unit test for event handler extraction in tests/unit/test_gwt_presenter_analyzer.py
- [ ] T048 [P] [US3] Unit test for navigation logic extraction in tests/unit/test_gwt_presenter_analyzer.py
- [ ] T049 [P] [US3] Unit test for view component type detection in tests/unit/test_gwt_view_analyzer.py
- [ ] T050 [P] [US3] Unit test for UiBinder template linking in tests/unit/test_gwt_view_analyzer.py

### Implementation for User Story 3

- [ ] T051 [P] [US3] Implement GwtPresenterAnalyzer class in src/codeindex/services/gwt_presenter_analyzer.py
- [ ] T052 [US3] Implement detect_view_binding() with 3 strategies and confidence scoring in gwt_presenter_analyzer.py
- [ ] T053 [US3] Implement extract_event_handlers() in gwt_presenter_analyzer.py
- [ ] T054 [US3] Implement extract_navigation_logic() in gwt_presenter_analyzer.py
- [ ] T055 [P] [US3] Implement GwtViewAnalyzer class in src/codeindex/services/gwt_view_analyzer.py
- [ ] T056 [US3] Implement find_uibinder_template() with @UiTemplate detection in gwt_view_analyzer.py
- [ ] T057 [US3] Implement extract_ui_field_bindings() for @UiField annotations in gwt_view_analyzer.py
- [ ] T058 [US3] Implement detect_component_type() (popup/portlet/panel/composite) in gwt_view_analyzer.py
- [ ] T059 [US3] Register GwtPresenterAnalyzer and GwtViewAnalyzer in gwt_analyzer_registry.py
- [ ] T060 [US3] Update PRD template at src/codeindex/cli/prd.py to add "MVP Components" section with presenter-view bindings
- [ ] T061 [US3] Add validation for low confidence bindings (<0.7) with warnings in gwt_presenter_analyzer.py
- [ ] T062 [US3] Add logging for MVP detection and confidence scoring in gwt_presenter_analyzer.py

**Checkpoint**: User Stories 1, 2, AND 3 should all work independently - PRDs show RPC endpoints, UI components, and MVP relationships

---

## Phase 6: User Story 4 - Extract Shared Data Models (Priority: P3)

**Goal**: Enable system to identify shared DTOs and models used between client and server so PRDs document data contracts

**Independent Test**: Run PRD generation on cuco-ui-admin and verify data model PRD shows DTOs with fields and validation rules

### Tests for User Story 4

- [ ] T063 [P] [US4] Create test fixture FlashInfoDTO.java in tests/fixtures/gwt/ with fields and validation annotations
- [ ] T064 [P] [US4] Create test fixture UserDTO.java with nested DTO references
- [ ] T065 [P] [US4] Unit test for DTO field extraction in tests/unit/test_gwt_model_analyzer.py
- [ ] T066 [P] [US4] Unit test for validation rule extraction (@NotNull, @Size) in tests/unit/test_gwt_model_analyzer.py
- [ ] T067 [P] [US4] Unit test for GWT serialization check in tests/unit/test_gwt_model_analyzer.py
- [ ] T068 [P] [US4] Unit test for nested DTO detection in tests/unit/test_gwt_model_analyzer.py

### Implementation for User Story 4

- [ ] T069 [P] [US4] Implement GwtModelAnalyzer class in src/codeindex/services/gwt_model_analyzer.py
- [ ] T070 [US4] Implement extract_dto_fields() using hybrid parser in gwt_model_analyzer.py
- [ ] T071 [US4] Implement extract_validation_rules() for validation annotations in gwt_model_analyzer.py
- [ ] T072 [US4] Implement check_gwt_serializable() in gwt_model_analyzer.py
- [ ] T073 [US4] Update db_analyzer.py to recognize shared DTOs as data models (add GWT DTO detection at line ~100)
- [ ] T074 [US4] Register GwtModelAnalyzer in gwt_analyzer_registry.py
- [ ] T075 [US4] Update PRD template at src/codeindex/cli/prd.py to add "Data Transfer Objects" section
- [ ] T076 [US4] Add validation for missing default constructor in gwt_model_analyzer.py
- [ ] T077 [US4] Add logging for DTO detection and field extraction in gwt_model_analyzer.py

**Checkpoint**: All user stories should now be independently functional - PRDs show complete GWT application documentation

---

## Phase 7: Integration & Testing

**Purpose**: End-to-end validation and integration testing

- [ ] T078 [P] Create integration test at tests/integration/test_gwt_prd_generation.py for full pipeline on cuco-ui-admin
- [ ] T079 [P] Add classifier tests for GWT patterns in tests/unit/test_classifier.py
- [ ] T080 [P] Create integration test for Weaviate queries with GWT metadata in tests/integration/test_gwt_weaviate_queries.py
- [ ] T081 Run full pipeline on cuco-ui-admin test case (184 files) and validate results
- [ ] T082 Verify PRD generation time is <10 minutes for 184-file codebase (performance requirement SC-006)
- [ ] T083 Verify PRD coverage is >80% of manually identifiable components (success criteria SC-005)
- [ ] T084 Test backward compatibility by running pipeline on non-GWT Java EE codebase (success criteria SC-007)

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T085 [P] Update CLAUDE.md with GWT support section and example usage
- [ ] T086 [P] Add troubleshooting guide for common GWT issues to CLAUDE.md
- [ ] T087 [P] Update CLI help text in src/codeindex/cli/prd.py to mention GWT support
- [ ] T088 [P] Add GWT-specific logging context (e.g., "Found 15 RPC servlets") in extraction.py
- [ ] T089 [P] Add type hints for all GWT analyzer functions (mypy validation)
- [ ] T090 Code review and refactoring for consistency across all analyzers
- [ ] T091 Run quickstart.md validation on test codebase
- [ ] T092 Update constitution checklist gates 2 and 3 in plan.md with actual test coverage numbers

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories CAN proceed in parallel after Phase 2 (if team capacity allows)
  - Or sequentially in priority order (US1 → US2 → US3 → US4)
- **Integration (Phase 7)**: Depends on at least US1 completion for MVP testing, all stories for full testing
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1 but integrates with US1 in PRD generation
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent of US1/US2, presenter detection may reference views from US2
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - Independent but DTOs referenced by US1 RPC methods

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD approach)
- Analyzer interface implementation before registration
- Registration before PRD template updates
- Core implementation before validation/logging
- Story complete and tested before moving to next priority

### Parallel Opportunities

- **Setup Phase**: T002, T003, T004 can all run in parallel
- **Foundational Phase**: T006, T007, T010 can run in parallel after T005 completes
- **US1 Tests**: T011-T017 can all run in parallel
- **US2 Tests**: T027-T031 can all run in parallel
- **US2 Implementation**: T032-T035 can run in parallel (different methods)
- **US3 Tests**: T041-T050 can all run in parallel
- **US3 Implementation**: T051-T054 (presenter) and T055-T058 (view) can run in parallel
- **US4 Tests**: T063-T068 can all run in parallel
- **US4 Implementation**: T069-T072 can run in parallel (different methods)
- **Integration Phase**: T078, T079, T080 can run in parallel
- **Polish Phase**: T085-T089 can all run in parallel
- **Across User Stories**: After Phase 2, different team members can work on US1, US2, US3, US4 simultaneously

---

## Parallel Example: User Story 1

```bash
# Launch all test fixtures for User Story 1 together:
Task: "Create test fixture FlashInfoServletImpl.java in tests/fixtures/gwt/"
Task: "Create test fixture FlashInfoService.java in tests/fixtures/gwt/"
Task: "Create test fixture FlashInfoServiceAsync.java in tests/fixtures/gwt/"

# Launch all unit tests for User Story 1 together:
Task: "Unit test for GWT RPC pattern detection in tests/unit/test_gwt_rpc_analyzer.py"
Task: "Unit test for RPC method extraction (javalang) in tests/unit/test_gwt_rpc_analyzer.py"
Task: "Unit test for RPC method extraction (regex) in tests/unit/test_gwt_rpc_analyzer.py"
Task: "Unit test for DTO reference extraction in tests/unit/test_gwt_rpc_analyzer.py"
```

---

## Parallel Example: User Story 3

```bash
# Launch presenter and view analyzers in parallel (different files):
Task: "Implement GwtPresenterAnalyzer class in src/codeindex/services/gwt_presenter_analyzer.py"
Task: "Implement GwtViewAnalyzer class in src/codeindex/services/gwt_view_analyzer.py"

# Launch all test fixtures for User Story 3 together:
Task: "Create test fixture FlashAdministrationPresenter.java in tests/fixtures/gwt/"
Task: "Create test fixture FlashAdministrationView.java in tests/fixtures/gwt/"
Task: "Create test fixture UserListPresenter.java in tests/fixtures/gwt/"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (install javalang, create structure)
2. Complete Phase 2: Foundational (CRITICAL - hybrid parser, classifier, schema, registry, routing)
3. Complete Phase 3: User Story 1 (RPC servlet analysis)
4. **STOP and VALIDATE**: Test User Story 1 independently on cuco-ui-admin
5. Deploy/demo PRD generation with RPC endpoints

**Result**: PRDs now show documented RPC endpoints instead of empty service sections - immediate value delivered!

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → PRDs show RPC endpoints (MVP!)
3. Add User Story 2 → Test independently → PRDs show UI components
4. Add User Story 3 → Test independently → PRDs show MVP relationships
5. Add User Story 4 → Test independently → PRDs show data models
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. **Team completes Setup + Foundational together** (2 devs, 1-2 days)
2. **Once Foundational is done, split into parallel tracks**:
   - Developer A: User Story 1 (RPC servlets) - 2-3 days
   - Developer B: User Story 2 (UiBinder) - 2-3 days
   - Developer C: User Story 3 (MVP patterns) - 3-4 days
   - Developer D: User Story 4 (DTOs) - 2 days
3. Stories complete and integrate independently
4. Integration testing validates all stories work together

**Benefit**: 4 user stories completed in 3-4 days instead of 10-12 days sequential

---

## Task Count Summary

- **Phase 1 (Setup)**: 4 tasks
- **Phase 2 (Foundational)**: 6 tasks (CRITICAL PATH)
- **Phase 3 (US1 - RPC Servlets)**: 16 tasks (7 tests + 9 implementation)
- **Phase 4 (US2 - UiBinder)**: 14 tasks (5 tests + 9 implementation)
- **Phase 5 (US3 - MVP Patterns)**: 22 tasks (10 tests + 12 implementation)
- **Phase 6 (US4 - DTOs)**: 15 tasks (6 tests + 9 implementation)
- **Phase 7 (Integration)**: 7 tasks
- **Phase 8 (Polish)**: 8 tasks

**Total**: 92 tasks

**MVP Scope** (US1 only): 26 tasks (Setup + Foundational + US1)
**Full Feature**: 92 tasks (all user stories)

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests written FIRST, must FAIL before implementation
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- **CRITICAL**: Phase 2 (Foundational) must be 100% complete before any user story work begins
- **MVP**: Focus on US1 first to deliver immediate value (PRDs with RPC endpoints)
- **Parallel**: After Phase 2, all user stories can proceed in parallel with different team members
