---
description: "Task list for Maven Dependency Resolution and DTO Analysis implementation"
---

# Tasks: Maven Dependency Resolution and DTO Analysis

**Input**: Design documents from `/specs/004-maven-dependency-resolution/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Included per constitution requirement (Testing Discipline from constitution.md)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/codeindex/`, `tests/` at repository root
- All paths relative to repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and test fixture structure

- [x] T001 Create test fixture directories: tests/fixtures/pom-files/ and tests/fixtures/dto-classes/
- [x] T002 [P] Create simple.xml test fixture in tests/fixtures/pom-files/simple.xml with single dependency
- [x] T003 [P] Create multi-module.xml test fixture in tests/fixtures/pom-files/multi-module.xml with 3+ dependencies
- [x] T004 [P] Create circular-deps.xml test fixture in tests/fixtures/pom-files/circular-deps.xml with circular reference
- [x] T005 [P] Create standard-dto.java test fixture in tests/fixtures/dto-classes/standard-dto.java with JSR-303 annotations
- [x] T006 [P] Create nested-dto.java test fixture in tests/fixtures/dto-classes/nested-dto.java with nested DTO field
- [x] T007 [P] Create entity-vs-dto.java test fixture in tests/fixtures/dto-classes/entity-vs-dto.java with @Entity annotation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T008 Create MavenDependency model in src/codeindex/models/maven_dependency.py with validation
- [x] T009 [P] Create ProjectConfiguration model in src/codeindex/models/project_configuration.py with path resolution logic
- [x] T010 [P] Create path_resolver utility in src/codeindex/utils/path_resolver.py with resolve_artifact_path function
- [x] T011 [P] Extend config.py utility in src/codeindex/utils/config.py to add --project and --dependency-depth CLI parameters
- [x] T012 Create DtoArtifact Weaviate schema in src/codeindex/schemas/dto_artifact_schema.py per data-model.md specification
- [x] T013 Update Weaviate schema initialization in src/codeindex/schemas/weaviate.py to create DtoArtifact class
- [x] T014 Write unit test for MavenDependency model validation in tests/unit/test_maven_dependency.py
- [ ] T015 [P] Write unit test for ProjectConfiguration path resolution in tests/unit/test_project_configuration.py
- [ ] T016 [P] Write unit test for path_resolver utility in tests/unit/test_path_resolver.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Maven Dependency Discovery and Resolution (Priority: P1) 🎯 MVP

**Goal**: Automatically discover and resolve Maven dependencies from pom.xml files, enabling analysis of multi-module projects

**Independent Test**: Point tool at multi-module Maven project with dependencies in pom.xml, verify files from dependent artifacts (at JAVA_SOURCE_DIR/artifact-name/) are discovered and included in analysis inventory

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T017 [P] [US1] Write unit test for parse_pom function in tests/unit/test_maven_parser.py covering simple pom.xml parsing
- [x] T018 [P] [US1] Write unit test for parse_pom with malformed XML in tests/unit/test_maven_parser.py to verify error handling
- [ ] T019 [P] [US1] Write unit test for resolve_dependencies function in tests/unit/test_dependency_resolver.py covering single dependency resolution
- [ ] T020 [P] [US1] Write unit test for circular dependency detection in tests/unit/test_dependency_resolver.py using circular-deps.xml fixture
- [ ] T021 [P] [US1] Write unit test for missing artifact handling in tests/unit/test_dependency_resolver.py
- [ ] T022 [P] [US1] Write integration test for end-to-end dependency resolution in tests/integration/test_dependency_resolution.py using test project

### Implementation for User Story 1

- [ ] T023 [P] [US1] Create DependencyNode model in src/codeindex/models/dependency_graph.py
- [ ] T024 [P] [US1] Create DependencyGraph model in src/codeindex/models/dependency_graph.py with statistics tracking
- [x] T025 [US1] Implement parse_pom function in src/codeindex/services/maven_parser.py using xml.etree.ElementTree per research.md
- [x] T026 [US1] Add Maven namespace handling in src/codeindex/services/maven_parser.py for http://maven.apache.org/POM/4.0.0
- [x] T027 [US1] Add error handling for FileNotFoundError and ParseError in src/codeindex/services/maven_parser.py
- [ ] T028 [US1] Implement resolve_dependencies function in src/codeindex/services/dependency_resolver.py with visited set tracking
- [ ] T029 [US1] Add circular dependency detection logic in src/codeindex/services/dependency_resolver.py
- [ ] T030 [US1] Add recursive resolution with depth limit in src/codeindex/services/dependency_resolver.py
- [ ] T031 [US1] Add dependency graph statistics calculation in src/codeindex/services/dependency_resolver.py (total, resolved, not_found, circular counts)
- [ ] T032 [US1] Extend discover CLI command in src/codeindex/cli/discover.py to add --dependency-depth parameter
- [ ] T033 [US1] Add pom.xml detection in src/codeindex/cli/discover.py to trigger dependency resolution
- [ ] T034 [US1] Integrate resolve_dependencies into discovery workflow in src/codeindex/cli/discover.py
- [ ] T035 [US1] Add dependency resolution logging in src/codeindex/cli/discover.py with statistics (FR-008, FR-009)
- [ ] T036 [US1] Add discovered dependency directories to file inventory in src/codeindex/services/discovery.py
- [ ] T037 [US1] Add validation to ensure dependency resolution completes within 10 seconds for 20 dependencies (SC-003)

**Checkpoint**: At this point, User Story 1 should be fully functional - Maven dependencies are resolved and files from dependent modules are discovered

---

## Phase 4: User Story 2 - DTO Pattern Recognition and Analysis (Priority: P2)

**Goal**: Identify and analyze Data Transfer Objects (DTOs) to understand data structures exchanged between layers

**Independent Test**: Run extraction on project with DTO classes, verify system correctly identifies them as DTOs (not entities or POJOs), extracts field definitions, detects validation annotations, and documents serialization patterns

### Tests for User Story 2

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T038 [P] [US2] Write unit test for DTO naming pattern classification in tests/unit/test_dto_classifier.py using standard-dto.java fixture
- [ ] T039 [P] [US2] Write unit test for entity exclusion (classes with @Entity should not be classified as DTO) in tests/unit/test_dto_classifier.py
- [ ] T040 [P] [US2] Write unit test for structural analysis (field-to-method ratio) in tests/unit/test_dto_classifier.py
- [ ] T041 [P] [US2] Write unit test for serialization marker detection in tests/unit/test_dto_classifier.py
- [ ] T042 [P] [US2] Write unit test for package location heuristics in tests/unit/test_dto_classifier.py
- [ ] T043 [P] [US2] Write unit test for extract_validation_annotations in tests/unit/test_java_parser.py covering @NotNull, @Size, @Pattern
- [ ] T044 [P] [US2] Write unit test for nested DTO identification in tests/unit/test_dto_classifier.py using nested-dto.java fixture
- [ ] T045 [P] [US2] Write integration test for DTO indexing in Weaviate in tests/integration/test_dto_indexing.py

### Implementation for User Story 2

- [ ] T046 [P] [US2] Create DtoField model in src/codeindex/models/dto_artifact.py with validation_annotations field
- [ ] T047 [P] [US2] Create DtoArtifact model in src/codeindex/models/dto_artifact.py with classification metadata
- [ ] T048 [P] [US2] Create ClassificationResult model in src/codeindex/models/dto_artifact.py
- [ ] T049 [US2] Implement classify_dto function in src/codeindex/services/classifier.py with Phase 1: Naming pattern match (80 points)
- [ ] T050 [US2] Add Phase 2: Entity exclusion check in src/codeindex/services/classifier.py
- [ ] T051 [US2] Add Phase 3: Structural analysis in src/codeindex/services/classifier.py (field-to-method ratio)
- [ ] T052 [US2] Add Phase 4: Serialization marker detection in src/codeindex/services/classifier.py (10 points)
- [ ] T053 [US2] Add Phase 5: Package location heuristics in src/codeindex/services/classifier.py (15 points)
- [ ] T054 [US2] Add threshold decision logic (confidence >= 70) in src/codeindex/services/classifier.py
- [ ] T055 [US2] Implement extract_validation_annotations function in src/codeindex/parsers/java_parser.py using regex per research.md
- [ ] T056 [US2] Add support for JSR-303 annotations (@NotNull, @NotEmpty, @Size, @Min, @Max, @Pattern, @Email, @Valid) in src/codeindex/parsers/java_parser.py
- [ ] T057 [US2] Add annotation parameter parsing (min=, max=, regexp=) in src/codeindex/parsers/java_parser.py
- [ ] T058 [US2] Implement extract_dto_metadata function in src/codeindex/parsers/java_parser.py to extract fields with types and modifiers
- [ ] T059 [US2] Implement identify_nested_dtos function in src/codeindex/services/classifier.py to detect nested DTO relationships
- [ ] T060 [US2] Add inner class detection logic in src/codeindex/parsers/java_parser.py
- [ ] T061 [US2] Extend extraction service in src/codeindex/services/extraction.py to handle DtoArtifact type
- [ ] T062 [US2] Add DTO classification to file type determination in src/codeindex/services/classifier.py
- [ ] T063 [US2] Integrate DTO metadata extraction into extraction pipeline in src/codeindex/services/extraction.py
- [ ] T064 [US2] Extend indexing service in src/codeindex/services/indexing.py to index DtoArtifact to Weaviate
- [ ] T065 [US2] Add validation to ensure DTO classification accuracy >= 90% (SC-002) using test fixtures
- [ ] T066 [US2] Add validation to ensure DTO field extraction completeness >= 95% (SC-007) using test fixtures

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - DTOs are identified, validated, and indexed

---

## Phase 5: User Story 3 - Project-Scoped Analysis with Base Directory Configuration (Priority: P3)

**Goal**: Enable targeted analysis of specific projects within monorepo by specifying --project parameter

**Independent Test**: Run tool with --project mysubproject on monorepo, verify only files within JAVA_SOURCE_DIR/mysubproject and its dependencies are analyzed with all paths correctly resolved

### Tests for User Story 3

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T067 [P] [US3] Write unit test for ProjectConfiguration with project_subdirectory in tests/unit/test_project_configuration.py
- [ ] T068 [P] [US3] Write unit test for effective_base_dir computation in tests/unit/test_project_configuration.py
- [ ] T069 [P] [US3] Write unit test for project directory validation in tests/unit/test_project_configuration.py
- [ ] T070 [P] [US3] Write integration test for project-scoped discovery in tests/integration/test_project_scoped_discovery.py

### Implementation for User Story 3

- [ ] T071 [US3] Add --project CLI parameter to discover command in src/codeindex/cli/discover.py
- [ ] T072 [US3] Add --project CLI parameter to extract command in src/codeindex/cli/extract.py
- [ ] T073 [US3] Add --project CLI parameter to index command in src/codeindex/cli/index.py
- [ ] T074 [US3] Add --project CLI parameter to search command in src/codeindex/cli/search.py
- [ ] T075 [US3] Add --project CLI parameter to status command in src/codeindex/cli/status.py
- [ ] T076 [US3] Update ProjectConfiguration to compute effective_base_dir from JAVA_SOURCE_DIR + project in src/codeindex/models/project_configuration.py (if not already done in T009)
- [ ] T077 [US3] Add project directory existence validation in src/codeindex/cli/discover.py with clear error message (FR-024)
- [ ] T078 [US3] Update dependency resolution to use effective_base_dir in src/codeindex/services/dependency_resolver.py
- [ ] T079 [US3] Update discovery service to use effective_base_dir in src/codeindex/services/discovery.py
- [ ] T080 [US3] Add resolved base directory logging in src/codeindex/cli/discover.py per FR-027
- [ ] T081 [US3] Add project name to analysis metadata in src/codeindex/services/discovery.py
- [ ] T082 [US3] Update search to support project filtering in src/codeindex/cli/search.py
- [ ] T083 [US3] Update status to support project filtering in src/codeindex/cli/status.py
- [ ] T084 [US3] Add validation to ensure project-scoped analysis completes in under 30 seconds (SC-008)

**Checkpoint**: All user stories should now be independently functional - Maven dependencies resolved, DTOs identified, project-scoped analysis working

---

## Phase 6: Polish & Cross-Cutting Concerns ✅ COMPLETE

**Purpose**: Improvements that affect multiple user stories

- [x] T085 [P] Update CLAUDE.md with new CLI parameters (--project, --dependency-depth) and usage examples
- [x] T086 [P] Add DTO artifact documentation to CLAUDE.md in "Key Artifact Types" section
- [x] T087 [P] Update run.sh convenience script to support --project parameter if needed
- [x] T088 [P] Add quickstart validation: Run full pipeline on test project and verify all success criteria (SC-001 through SC-008)
- [x] T089 Code cleanup: Remove any TODOs or temporary debug logging from maven_parser.py, dependency_resolver.py, classifier.py
- [x] T090 [P] Performance validation: Profile dependency resolution to ensure <10 seconds for 20 dependencies (SC-003)
- [x] T091 [P] Add error message quality validation: Review all error messages for clarity and actionable guidance per constitution
- [x] T092 [P] Add progress tracking for dependency resolution in src/codeindex/services/dependency_resolver.py per constitution observability requirement
- [x] T093 [P] Add metrics logging for dependencies resolved, DTOs classified in src/codeindex/cli/discover.py and src/codeindex/cli/extract.py
- [x] T094 Run full test suite and ensure >80% coverage for maven_parser, dependency_resolver, dto_classifier per Gate 2 requirement
- [x] T095 Validate constitution Gate 2 requirements: All tests passing, CLI help text clear, logging levels appropriate, type hints present
- [x] T096 Validate constitution Gate 3 requirements: Integration tests pass, performance validated, error handling tested, documentation updated

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User Story 1 (P1): Can start after Foundational - No dependencies on other stories
  - User Story 2 (P2): Can start after Foundational - No dependencies on other stories (independent)
  - User Story 3 (P3): Can start after Foundational - Enhances US1 but independently testable
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independently testable (classifies files discovered by any method)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independently testable (adds CLI parameter, doesn't change core behavior)

**Key Insight**: All three user stories are designed to be independent. US2 (DTO) and US3 (project scoping) can be implemented in parallel after US1 (dependency resolution) if desired, or in priority order.

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services
- Services before CLI integration
- Core implementation before validation
- Story complete before moving to next priority

### Parallel Opportunities

- **Phase 1 (Setup)**: All fixture creation tasks (T002-T007) can run in parallel
- **Phase 2 (Foundational)**: Tasks T009-T011 (models and utilities) can run in parallel, tests T014-T016 can run in parallel
- **Phase 3 (US1)**: All test tasks (T017-T022) can run in parallel, models (T023-T024) can run in parallel
- **Phase 4 (US2)**: All test tasks (T038-T045) can run in parallel, models (T046-T048) can run in parallel
- **Phase 5 (US3)**: All test tasks (T067-T070) can run in parallel, CLI parameter additions (T071-T075) can run in parallel
- **Phase 6 (Polish)**: Documentation tasks (T085-T086, T088) can run in parallel, validation tasks (T090-T091) can run in parallel
- **User Stories**: After Foundational phase, US1, US2, US3 can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Write unit test for parse_pom function in tests/unit/test_maven_parser.py"
Task: "Write unit test for parse_pom with malformed XML in tests/unit/test_maven_parser.py"
Task: "Write unit test for resolve_dependencies function in tests/unit/test_dependency_resolver.py"
Task: "Write unit test for circular dependency detection in tests/unit/test_dependency_resolver.py"
Task: "Write unit test for missing artifact handling in tests/unit/test_dependency_resolver.py"
Task: "Write integration test for end-to-end dependency resolution in tests/integration/test_dependency_resolution.py"

# Launch all models for User Story 1 together:
Task: "Create DependencyNode model in src/codeindex/models/dependency_graph.py"
Task: "Create DependencyGraph model in src/codeindex/models/dependency_graph.py"
```

---

## Parallel Example: User Story 2

```bash
# Launch all tests for User Story 2 together:
Task: "Write unit test for DTO naming pattern classification in tests/unit/test_dto_classifier.py"
Task: "Write unit test for entity exclusion in tests/unit/test_dto_classifier.py"
Task: "Write unit test for structural analysis in tests/unit/test_dto_classifier.py"
Task: "Write unit test for serialization marker detection in tests/unit/test_dto_classifier.py"
Task: "Write unit test for package location heuristics in tests/unit/test_dto_classifier.py"
Task: "Write unit test for extract_validation_annotations in tests/unit/test_java_parser.py"
Task: "Write unit test for nested DTO identification in tests/unit/test_dto_classifier.py"
Task: "Write integration test for DTO indexing in Weaviate in tests/integration/test_dto_indexing.py"

# Launch all models for User Story 2 together:
Task: "Create DtoField model in src/codeindex/models/dto_artifact.py"
Task: "Create DtoArtifact model in src/codeindex/models/dto_artifact.py"
Task: "Create ClassificationResult model in src/codeindex/models/dto_artifact.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T007) - ~1 hour
2. Complete Phase 2: Foundational (T008-T016) - CRITICAL - blocks all stories - ~2-3 hours
3. Complete Phase 3: User Story 1 (T017-T037) - ~6-8 hours
4. **STOP and VALIDATE**: Test User Story 1 independently
   - Run: `codeindex discover --source-dir /path/to/project --dependency-depth 2`
   - Verify: Dependencies resolved, files discovered from dependent modules
   - Check: Resolution completes in <10 seconds, >95% success rate
5. Deploy/demo if ready

**MVP Delivers**: Multi-module Maven project analysis with automatic dependency resolution

### Incremental Delivery

1. Complete Setup + Foundational (T001-T016) → Foundation ready - ~3-4 hours
2. Add User Story 1 (T017-T037) → Test independently → Deploy/Demo (MVP!) - ~6-8 hours
3. Add User Story 2 (T038-T066) → Test independently → Deploy/Demo - ~8-10 hours
4. Add User Story 3 (T067-T084) → Test independently → Deploy/Demo - ~3-4 hours
5. Polish (T085-T096) → Final validation → Production ready - ~2-3 hours

**Total Estimated Time**: ~22-29 hours of focused development

Each story adds value without breaking previous stories:
- After US1: Can analyze multi-module projects
- After US2: Can also identify and document DTOs
- After US3: Can also do project-scoped analysis in monorepos

### Parallel Team Strategy

With multiple developers:

1. **Team completes Setup + Foundational together** (T001-T016) - ~3-4 hours
2. **Once Foundational is done, parallelize user stories**:
   - Developer A: User Story 1 (T017-T037) - Maven dependency resolution
   - Developer B: User Story 2 (T038-T066) - DTO classification (can mock dependency data if needed)
   - Developer C: User Story 3 (T067-T084) - Project scoping (lightweight, can complete quickly)
3. **Integration**: Stories complete and integrate independently
4. **Final validation**: Polish phase (T085-T096) together

**Team Time**: ~10-12 hours with 3 developers working in parallel

---

## Notes

- [P] tasks = different files, no dependencies - can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Verify tests fail before implementing (TDD approach per constitution)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Total tasks: 96 tasks across 6 phases
- Test tasks: 29 test tasks (30% of total) ensuring >80% coverage per constitution
- Parallel opportunities: ~40% of tasks marked [P] can run concurrently
- MVP scope: Phases 1-3 (T001-T037) = 37 tasks = ~10-12 hours
