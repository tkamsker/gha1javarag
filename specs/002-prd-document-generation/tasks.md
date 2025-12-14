# Tasks: PRD Document Generation from Codebase Analysis

**Status**: 🚧 **IN PROGRESS** - Ready for implementation
**Created**: 2025-12-14

**Input**: Design documents from `/specs/002-prd-document-generation/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/

**Tests**: No test tasks included (not requested in spec.md)

**Organization**: Tasks are grouped by user story following priority order P1→P2→P3→P4 to enable independent implementation and testing of each story.

---

## 🎯 User Stories Overview

- **US1 (P1)**: Database Schema and Business Rules Documentation
- **US2 (P2)**: Backend Services and API Documentation
- **US3 (P3)**: Frontend Form and Component Documentation
- **US4 (P4)**: Comprehensive Cross-Layer PRD Generation

---

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/codeindex/`, `tests/` at repository root
- All paths relative to project root `/Users/thomaskamsker/Documents/Atom/vron.one/playground/Iteration17/gha1javarag/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, directory structure, dependencies

### Project Structure

- [ ] T001 [P] Create test fixtures directory at tests/fixtures/prd/ for sample DAO/Service/JSP files
- [ ] T002 [P] Create output directory structure: output/database/, output/services/, output/frontend/, output/business_rules/, output/prd/
- [ ] T003 [P] Update .gitignore to exclude output/ directory if not already present

### Dependencies and Configuration

- [ ] T004 Update requirements.txt if needed (all dependencies from Feature 001 should already be present: Click, weaviate-client, httpx, python-dotenv, lxml, pytest)
- [ ] T005 Update .env.example to document OUTPUT_DIR (default: ./output) per contracts/cli-interface.md
- [ ] T006 [P] Create test fixtures: tests/fixtures/prd/sample_dao.java (simple DAO with CRUD operations)
- [ ] T007 [P] Create test fixtures: tests/fixtures/prd/sample_service.java (service with business logic and transactions)
- [ ] T008 [P] Create test fixtures: tests/fixtures/prd/sample_jsp.jsp (form with fields and validation)
- [ ] T009 [P] Create test fixtures: tests/fixtures/prd/sample_gwt.java (GWT widget or activity)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core PRD infrastructure that ALL user stories depend on - BLOCKS all stories

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Data Models for PRD Entities

- [ ] T010 [P] Create PRD models file at src/codeindex/models/prd.py with all entity classes from data-model.md
- [ ] T011 [P] Implement DatabaseEntity dataclass in src/codeindex/models/prd.py with fields: id, name, qualified_name, source_type, source_files, columns[], primary_key[], foreign_keys[], indexes[], constraints[], business_rules[], description, estimated_row_count, domain, created_at
- [ ] T012 [P] Implement BusinessRule dataclass in src/codeindex/models/prd.py with fields: id, name, layer, scope, rule_type, description, source_files[], source_code_snippets[], related_entities[], conditions, enforcement_mechanism, severity, security_relevant, domain, created_at
- [ ] T013 [P] Implement ServiceDefinition dataclass in src/codeindex/models/prd.py with fields: id, class_name, qualified_name, package, source_file, service_type, description, operations[], dependencies[], data_dependencies[], endpoints[], business_rules[], transaction_boundaries[], frameworks[], domain, created_at
- [ ] T014 [P] Implement APIEndpoint dataclass in src/codeindex/models/prd.py with fields: id, http_method, path, service_id, operation_name, description, request_format, response_format, authentication_required, authorization_roles[], rate_limited, deprecated, produces[], consumes[], source_file, created_at
- [ ] T015 [P] Implement FormDefinition dataclass in src/codeindex/models/prd.py with fields: id, name, source_file, form_type, description, fields[], submission_endpoint, submission_method, submission_service, validation_rules[], bound_entities[], navigation_on_success, navigation_on_cancel, security_patterns[], domain, created_at
- [ ] T016 [P] Implement UIComponent dataclass in src/codeindex/models/prd.py with fields: id, name, component_type, source_file, description, responsibilities[], events_handled[], events_emitted[], data_bindings[], navigation_targets[], child_components[], parent_component, related_forms[], framework_annotations[], domain, created_at
- [ ] T017 [P] Implement NavigationFlow dataclass in src/codeindex/models/prd.py with fields: id, name, description, entry_points[], steps[], exit_points[], flow_type, related_forms[], related_components[], business_process, domain, created_at
- [ ] T018 [P] Implement PRDSection dataclass in src/codeindex/models/prd.py with fields: id, title, level, content, section_type, cross_references[], metadata, order, parent_section, created_at
- [ ] T019 Add enumerations to src/codeindex/models/prd.py: SOURCE_TYPES, SERVICE_TYPES, FORM_TYPES, COMPONENT_TYPES, FLOW_TYPES, ANALYSIS_LAYERS, VISIT_STATUS, RULE_TYPES, RULE_LAYERS per data-model.md

### Visit Log Tracking

- [ ] T020 Implement VisitLog service in src/codeindex/services/visit_log.py with functions: load_visit_log(output_dir), append_visit_entry(file_path, timestamp, status, content_hash, layer, analysis_type, duration, entities, error_message), check_file_visited(file_path, content_hash), get_visit_status(file_path)
- [ ] T021 Implement visit log entry dataclass FileVisitEntry in src/codeindex/services/visit_log.py with fields: file_path, timestamp, status, content_hash, layer, analysis_type, error_message, duration_seconds, extracted_entities[]
- [ ] T022 Implement content hashing function in src/codeindex/services/visit_log.py using hashlib.sha256 to generate SHA-256 hash of file contents
- [ ] T023 Implement JSONL read/write functions in src/codeindex/services/visit_log.py with streaming append-only writes and deduplication by file_path (latest entry wins)

### Markdown Documentation Builder

- [ ] T024 Implement MarkdownBuilder service in src/codeindex/services/markdown_builder.py with functions: build_entity_markdown(entity), build_service_markdown(service), build_form_markdown(form), build_index_markdown(entities, layer, project), build_prd_section(section)
- [ ] T025 Implement markdown formatting functions in src/codeindex/services/markdown_builder.py: format_table(headers, rows), format_list(items), format_code_block(code, language), format_security_admonition(pattern, description, source, recommendation)
- [ ] T026 Implement cross-reference link generation in src/codeindex/services/markdown_builder.py to create relative markdown links between entities, services, forms

### CLI Command Skeleton

- [ ] T027 Create CLI command skeleton at src/codeindex/cli/prd.py with Click command group and options per contracts/cli-interface.md: --project, --source-dir, --output-dir, --force-refresh, --parallel, --llm-timeout, --llm-retries, --llm-model, --format, --domain-filter, --progress-interval, --verbose, --quiet
- [ ] T028 Implement CLI argument validation in src/codeindex/cli/prd.py: source directory exists, output directory writable, project exists in Weaviate (if --project specified)
- [ ] T029 Implement service health checks in src/codeindex/cli/prd.py: verify Weaviate accessible (HTTP 200 from /v1/meta), verify Ollama accessible (HTTP 200 from /api/tags), exit with appropriate error codes (6 for Weaviate, 7 for Ollama)
- [ ] T030 Implement progress reporting framework in src/codeindex/cli/prd.py with periodic updates every --progress-interval seconds showing: current layer, files processed count, estimated time remaining, current file being analyzed
- [ ] T031 Add positional argument [LAYER] in src/codeindex/cli/prd.py with values: database, services, frontend, full (default: full)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Database Schema and Business Rules Documentation (Priority: P1) 🎯 MVP

**Goal**: Analyze DAO classes, entity classes, SQL files, ORM mappings to produce complete database schema documentation with business rules

**Independent Test**: Point tool at Java project with DAO/SQL files, verify it produces output/database/ with entities, business rules, and index.md

### Implementation for User Story 1

#### Database Analysis Service

- [ ] T032 [US1] Implement database analyzer service in src/codeindex/services/db_analyzer.py with main function: analyze_database_layer(project, source_dir, output_dir, ollama_client, weaviate_store, visit_log, config)
- [ ] T033 [US1] Implement DAO file identification in src/codeindex/services/db_analyzer.py to find files by naming patterns (*DAO.java, *Repository.java) or by querying Weaviate for artifact_type=java_source with tags_layer=DATA
- [ ] T034 [US1] Implement entity class identification in src/codeindex/services/db_analyzer.py to find @Entity, @Table, @Document annotations or iBATIS/MyBatis mapper references
- [ ] T035 [US1] Implement SQL file identification in src/codeindex/services/db_analyzer.py to find .sql files and iBATIS/MyBatis XML mapper files

#### DAO and Entity Extraction

- [ ] T036 [US1] Implement DAO entity extraction function in src/codeindex/services/db_analyzer.py: extract_database_entity(file_path, file_content, ollama_client, weaviate_context) returning DatabaseEntity
- [ ] T037 [US1] Extend OllamaClient in src/codeindex/services/ollama_client.py with new method: extract_dao_entity(file_path, file_content, related_entities) using DAO extraction prompt template from contracts/llm-contracts.md
- [ ] T038 [US1] Implement JPA annotation parsing in src/codeindex/services/db_analyzer.py to extract table name from @Table, columns from @Column, primary keys from @Id, foreign keys from @ManyToOne/@OneToMany/@JoinColumn
- [ ] T039 [US1] Implement iBATIS/MyBatis mapper parsing in src/codeindex/services/db_analyzer.py to extract table names from SQL statements, columns from result maps, relationships from foreign key references in queries

#### Business Rule Extraction (Database Layer)

- [ ] T040 [US1] Implement database business rule extraction in src/codeindex/services/db_analyzer.py: extract_database_business_rules(entity, file_content, ollama_client) returning BusinessRule[]
- [ ] T041 [US1] Extend OllamaClient with method: extract_sql_business_rules(sql_code, tables, context) using SQL query analysis prompt from contracts/llm-contracts.md
- [ ] T042 [US1] Implement constraint extraction in src/codeindex/services/db_analyzer.py to identify CHECK constraints, UNIQUE constraints, NOT NULL constraints, foreign key constraints from annotations and SQL DDL
- [ ] T043 [US1] Implement validation rule extraction in src/codeindex/services/db_analyzer.py to find validation annotations (@NotNull, @Size, @Pattern, @Email, @Min, @Max) on entity fields

#### Weaviate Integration for Context

- [ ] T044 [US1] Extend WeaviateStore in src/codeindex/services/weaviate_store.py with method: query_database_artifacts(project_id, entity_name) to fetch related DAOs, entities, SQL files for context enrichment
- [ ] T045 [US1] Implement context enrichment in src/codeindex/services/db_analyzer.py to query Weaviate for related artifacts and pass as context to LLM prompts

#### Output Generation

- [ ] T046 [US1] Implement database entity JSON serialization in src/codeindex/services/db_analyzer.py to save DatabaseEntity as output/database/entities/{entity_name}.json
- [ ] T047 [US1] Implement business rule JSON serialization in src/codeindex/services/db_analyzer.py to save BusinessRule as output/business_rules/BR_{id}_{name}.json
- [ ] T048 [US1] Implement database index.md generation in src/codeindex/services/db_analyzer.py using MarkdownBuilder to create output/database/index.md with entity catalog organized by domain
- [ ] T049 [US1] Implement database PRD markdown generation in src/codeindex/services/db_analyzer.py using MarkdownBuilder to create output/prd/database_prd.md with sections: Overview, Entity Catalog, Relationships, Business Rules, Data Dictionary

#### Visit Log Integration

- [ ] T050 [US1] Integrate visit log in src/codeindex/services/db_analyzer.py to check if files already analyzed (matching content_hash), skip unchanged files unless --force-refresh specified
- [ ] T051 [US1] Add visit log tracking in src/codeindex/services/db_analyzer.py to append entry for each analyzed file with status (success/failed/skipped), duration, extracted entities, error messages

#### Error Handling and Progress

- [ ] T052 [US1] Implement LLM timeout and retry logic in src/codeindex/services/db_analyzer.py using retry decorator with 120s timeout, 3 retry attempts, exponential backoff (1s, 2s, 4s)
- [ ] T053 [US1] Implement progress reporting in src/codeindex/services/db_analyzer.py to emit progress updates every 10 seconds with: files processed, current file, estimated time remaining
- [ ] T054 [US1] Implement error aggregation in src/codeindex/services/db_analyzer.py to collect all failures and report summary at end: "X files failed, Y entities extracted, Z business rules identified"

#### CLI Command Integration

- [ ] T055 [US1] Wire database analyzer into src/codeindex/cli/prd.py for layer='database' mode, calling db_analyzer.analyze_database_layer() with CLI options
- [ ] T056 [US1] Add database-only output structure validation in src/codeindex/cli/prd.py to verify output/database/, output/business_rules/, output/prd/database_prd.md were created

**Checkpoint**: User Story 1 complete - database layer analysis produces entities, business rules, and PRD documentation

---

## Phase 4: User Story 2 - Backend Services and API Documentation (Priority: P2)

**Goal**: Analyze service classes, REST controllers, SOAP services to document business logic, API endpoints, and service dependencies

**Independent Test**: Run service analysis on project with service classes, verify output/services/ with service definitions, endpoints, and index.md

### Implementation for User Story 2

#### Service Analysis Service

- [ ] T057 [US2] Implement service analyzer in src/codeindex/services/service_analyzer.py with main function: analyze_service_layer(project, source_dir, output_dir, ollama_client, weaviate_store, visit_log, config)
- [ ] T058 [US2] Implement service file identification in src/codeindex/services/service_analyzer.py to find files by naming patterns (*Service.java, *Controller.java) or by querying Weaviate for artifact_type=java_source with tags_layer=BUSINESS
- [ ] T059 [US2] Implement REST controller identification in src/codeindex/services/service_analyzer.py to find @RestController, @Controller, @RequestMapping annotations
- [ ] T060 [US2] Implement SOAP service identification in src/codeindex/services/service_analyzer.py to find @WebService, JAX-WS annotations

#### Service Definition Extraction

- [ ] T061 [US2] Implement service extraction function in src/codeindex/services/service_analyzer.py: extract_service_definition(file_path, file_content, ollama_client, weaviate_context) returning ServiceDefinition
- [ ] T062 [US2] Extend OllamaClient with method: extract_service_definition(file_path, file_content, related_services, entities) using service extraction prompt template from contracts/llm-contracts.md
- [ ] T063 [US2] Implement service type classification in src/codeindex/services/service_analyzer.py to categorize as: business_service, dao_service, integration_service, controller, rest_controller, utility_service based on annotations and naming
- [ ] T064 [US2] Implement operation extraction in src/codeindex/services/service_analyzer.py to extract public methods with signatures, parameters, return types, annotations, exceptions thrown, line numbers

#### Service Dependencies and Relationships

- [ ] T065 [US2] Implement dependency extraction in src/codeindex/services/service_analyzer.py to find injected dependencies (@Autowired, @Inject, constructor injection), DAO references, service-to-service calls
- [ ] T066 [US2] Implement data dependency linking in src/codeindex/services/service_analyzer.py to identify which database entities (from User Story 1) this service accesses via DAO calls
- [ ] T067 [US2] Implement transaction boundary detection in src/codeindex/services/service_analyzer.py to find @Transactional annotations with propagation, isolation, read-only settings

#### API Endpoint Extraction

- [ ] T068 [US2] Implement REST endpoint extraction function in src/codeindex/services/service_analyzer.py: extract_api_endpoints(controller_class, service_def) returning APIEndpoint[]
- [ ] T069 [US2] Extend OllamaClient with method: extract_rest_endpoints(file_content, class_name, services) using REST endpoint extraction prompt from contracts/llm-contracts.md
- [ ] T070 [US2] Implement endpoint path construction in src/codeindex/services/service_analyzer.py to combine class-level @RequestMapping with method-level paths
- [ ] T071 [US2] Implement request/response format extraction in src/codeindex/services/service_analyzer.py to extract request parameters (path/query/header/body), response status codes, content types (application/json, etc.), request/response examples from @RequestBody/@ResponseBody annotations

#### Business Rule Extraction (Service Layer)

- [ ] T072 [US2] Implement service business rule extraction in src/codeindex/services/service_analyzer.py: extract_service_business_rules(service_def, file_content, ollama_client) returning BusinessRule[]
- [ ] T073 [US2] Implement validation logic extraction in src/codeindex/services/service_analyzer.py to find validation calls, exception throwing patterns (ValidationException, IllegalArgumentException), business logic conditionals
- [ ] T074 [US2] Implement authorization rule extraction in src/codeindex/services/service_analyzer.py to find @PreAuthorize, @Secured, @RolesAllowed annotations with role requirements

#### Weaviate Integration for Context

- [ ] T075 [US2] Extend WeaviateStore with method: query_service_artifacts(project_id, service_name) to fetch related services, DAOs, entities for context enrichment
- [ ] T076 [US2] Implement cross-referencing with database entities in src/codeindex/services/service_analyzer.py to link ServiceDefinition.data_dependencies[] to DatabaseEntity IDs from User Story 1 output

#### Output Generation

- [ ] T077 [US2] Implement service definition JSON serialization in src/codeindex/services/service_analyzer.py to save ServiceDefinition as output/services/definitions/{ServiceClassName}.json
- [ ] T078 [US2] Implement API endpoint JSON serialization in src/codeindex/services/service_analyzer.py to save APIEndpoint as output/services/endpoints/{METHOD}_{path}.json
- [ ] T079 [US2] Implement service business rules JSON serialization in src/codeindex/services/service_analyzer.py to save BusinessRule (service layer) as output/business_rules/BR_{id}_{name}.json
- [ ] T080 [US2] Implement service index.md generation in src/codeindex/services/service_analyzer.py using MarkdownBuilder to create output/services/index.md with service catalog organized by domain
- [ ] T081 [US2] Implement service PRD markdown generation in src/codeindex/services/service_analyzer.py using MarkdownBuilder to create output/prd/service_prd.md with sections: Overview, Service Catalog, API Endpoints, Dependencies Graph, Business Operations

#### Visit Log Integration

- [ ] T082 [US2] Integrate visit log in src/codeindex/services/service_analyzer.py to check if files already analyzed, skip unchanged files unless --force-refresh
- [ ] T083 [US2] Add visit log tracking in src/codeindex/services/service_analyzer.py to append entry for each analyzed file with layer='service'

#### Error Handling and Progress

- [ ] T084 [US2] Implement LLM timeout and retry logic in src/codeindex/services/service_analyzer.py (120s timeout, 3 retries, exponential backoff)
- [ ] T085 [US2] Implement progress reporting in src/codeindex/services/service_analyzer.py with updates every 10 seconds
- [ ] T086 [US2] Implement error aggregation in src/codeindex/services/service_analyzer.py with summary: "X services analyzed, Y endpoints found, Z failed"

#### CLI Command Integration

- [ ] T087 [US2] Wire service analyzer into src/codeindex/cli/prd.py for layer='services' mode, calling service_analyzer.analyze_service_layer()
- [ ] T088 [US2] Add service-only output structure validation in src/codeindex/cli/prd.py to verify output/services/, output/prd/service_prd.md were created

**Checkpoint**: User Story 2 complete - service layer analysis produces service definitions, API endpoints, and PRD documentation

---

## Phase 5: User Story 3 - Frontend Form and Component Documentation (Priority: P3)

**Goal**: Analyze JSP files, GWT modules, JavaScript to document UI forms, components, navigation flows with backend linkage

**Independent Test**: Run frontend analysis on project with JSP/GWT files, verify output/frontend/ with forms, components, navigation flows, and index.md

### Implementation for User Story 3

#### Frontend Analysis Service

- [ ] T089 [US3] Implement frontend analyzer in src/codeindex/services/frontend_analyzer.py with main function: analyze_frontend_layer(project, source_dir, output_dir, ollama_client, weaviate_store, visit_log, config)
- [ ] T090 [US3] Implement JSP file identification in src/codeindex/services/frontend_analyzer.py to find .jsp, .jspf files or by querying Weaviate for artifact_type=jsp_view
- [ ] T091 [US3] Implement HTML file identification in src/codeindex/services/frontend_analyzer.py to find .html, .htm files or artifact_type=html_template
- [ ] T092 [US3] Implement GWT file identification in src/codeindex/services/frontend_analyzer.py to find GWT widgets, activities, views, presenters or artifact_type=gwt_module, gwt_ui_binder, gwt_activity_place
- [ ] T093 [US3] Implement JavaScript file identification in src/codeindex/services/frontend_analyzer.py to find .js files or artifact_type=js_script

#### Form Extraction

- [ ] T094 [US3] Implement form extraction function in src/codeindex/services/frontend_analyzer.py: extract_form_definition(file_path, file_content, ollama_client, weaviate_context) returning FormDefinition
- [ ] T095 [US3] Extend OllamaClient with method: extract_jsp_form(file_content, endpoints) using JSP form extraction prompt template from contracts/llm-contracts.md
- [ ] T096 [US3] Implement form field parsing in src/codeindex/services/frontend_analyzer.py to extract field name, label, type (text/email/password/select/checkbox/textarea/date/file), required flag, validation patterns, default values, options (for select/radio)
- [ ] T097 [US3] Implement form submission target extraction in src/codeindex/services/frontend_analyzer.py to find form action URL, HTTP method (GET/POST), and link to APIEndpoint from User Story 2

#### UI Component Extraction

- [ ] T098 [US3] Implement UI component extraction function in src/codeindex/services/frontend_analyzer.py: extract_ui_component(file_path, file_content, component_type, ollama_client, weaviate_context) returning UIComponent
- [ ] T099 [US3] Extend OllamaClient with method: extract_gwt_component(file_content, component_type, related_components) using GWT component extraction prompt from contracts/llm-contracts.md
- [ ] T100 [US3] Implement GWT widget parsing in src/codeindex/services/frontend_analyzer.py to extract widget hierarchy, child widgets, parent-child relationships
- [ ] T101 [US3] Implement event handling extraction in src/codeindex/services/frontend_analyzer.py to find click/change/submit/load handlers, event names, handler method names

#### Client-Side Business Rules

- [ ] T102 [US3] Implement frontend business rule extraction in src/codeindex/services/frontend_analyzer.py: extract_frontend_business_rules(form, component, file_content, ollama_client) returning BusinessRule[]
- [ ] T103 [US3] Implement JavaScript validation extraction in src/codeindex/services/frontend_analyzer.py to find validation functions, regex patterns, HTML5 validation attributes (required, pattern, min, max, minlength, maxlength)
- [ ] T104 [US3] Implement security pattern detection in src/codeindex/services/frontend_analyzer.py to find CSRF tokens, input sanitization, XSS prevention patterns

#### Navigation Flow Extraction

- [ ] T105 [US3] Implement navigation flow extraction in src/codeindex/services/frontend_analyzer.py: extract_navigation_flows(forms, components, file_paths) returning NavigationFlow[]
- [ ] T106 [US3] Implement entry point detection in src/codeindex/services/frontend_analyzer.py to find direct URLs, link clicks, button actions, menu items
- [ ] T107 [US3] Implement navigation step tracking in src/codeindex/services/frontend_analyzer.py to build ordered steps with page URLs, form submissions, component transitions, success/cancel/error paths

#### Cross-Referencing with Backend

- [ ] T108 [US3] Implement backend linkage in src/codeindex/services/frontend_analyzer.py to link FormDefinition.submission_endpoint to APIEndpoint IDs from User Story 2
- [ ] T109 [US3] Implement service linkage in src/codeindex/services/frontend_analyzer.py to link FormDefinition.submission_service to ServiceDefinition IDs from User Story 2
- [ ] T110 [US3] Implement entity linkage in src/codeindex/services/frontend_analyzer.py to link FormDefinition.bound_entities[] to DatabaseEntity IDs from User Story 1 by matching field names to column names

#### Weaviate Integration for Context

- [ ] T111 [US3] Extend WeaviateStore with method: query_frontend_artifacts(project_id, form_name) to fetch related JSP/GWT files, endpoints, services for context enrichment
- [ ] T112 [US3] Implement context enrichment in src/codeindex/services/frontend_analyzer.py to query backend endpoints and services when analyzing form submission targets

#### Output Generation

- [ ] T113 [US3] Implement form definition JSON serialization in src/codeindex/services/frontend_analyzer.py to save FormDefinition as output/frontend/forms/{form_name}.json
- [ ] T114 [US3] Implement UI component JSON serialization in src/codeindex/services/frontend_analyzer.py to save UIComponent as output/frontend/components/{ComponentName}.json
- [ ] T115 [US3] Implement navigation flow JSON serialization in src/codeindex/services/frontend_analyzer.py to save NavigationFlow as output/frontend/navigation/{flow_name}.json
- [ ] T116 [US3] Implement frontend business rules JSON serialization in src/codeindex/services/frontend_analyzer.py to save BusinessRule (frontend layer) as output/business_rules/BR_{id}_{name}.json
- [ ] T117 [US3] Implement frontend index.md generation in src/codeindex/services/frontend_analyzer.py using MarkdownBuilder to create output/frontend/index.md with forms, components, navigation flows organized by entry point
- [ ] T118 [US3] Implement frontend PRD markdown generation in src/codeindex/services/frontend_analyzer.py using MarkdownBuilder to create output/prd/frontend_prd.md with sections: Overview, Component Hierarchy, Forms Catalog, Navigation Flows, User Journeys

#### Visit Log Integration

- [ ] T119 [US3] Integrate visit log in src/codeindex/services/frontend_analyzer.py to check if files already analyzed, skip unchanged files unless --force-refresh
- [ ] T120 [US3] Add visit log tracking in src/codeindex/services/frontend_analyzer.py to append entry for each analyzed file with layer='frontend'

#### Error Handling and Progress

- [ ] T121 [US3] Implement LLM timeout and retry logic in src/codeindex/services/frontend_analyzer.py (120s timeout, 3 retries, exponential backoff)
- [ ] T122 [US3] Implement progress reporting in src/codeindex/services/frontend_analyzer.py with updates every 10 seconds
- [ ] T123 [US3] Implement error aggregation in src/codeindex/services/frontend_analyzer.py with summary: "X forms analyzed, Y components found, Z navigation flows identified"

#### CLI Command Integration

- [ ] T124 [US3] Wire frontend analyzer into src/codeindex/cli/prd.py for layer='frontend' mode, calling frontend_analyzer.analyze_frontend_layer()
- [ ] T125 [US3] Add frontend-only output structure validation in src/codeindex/cli/prd.py to verify output/frontend/, output/prd/frontend_prd.md were created

**Checkpoint**: User Story 3 complete - frontend layer analysis produces forms, components, navigation flows, and PRD documentation

---

## Phase 6: User Story 4 - Comprehensive Cross-Layer PRD Generation (Priority: P4)

**Goal**: Synthesize all layer analyses into master PRD with executive summary, architecture overview, cross-layer flows, gaps and recommendations

**Independent Test**: Run full analysis (all layers), verify output/prd/master_prd.md with complete cross-references, executive summary, and cohesive documentation

### Implementation for User Story 4

#### PRD Orchestration Service

- [ ] T126 [US4] Implement PRD generator orchestrator in src/codeindex/services/prd_generator.py with main function: generate_prd(project, output_dir, ollama_client, weaviate_store, config)
- [ ] T127 [US4] Implement layer coordination in src/codeindex/services/prd_generator.py to call analyze_database_layer(), analyze_service_layer(), analyze_frontend_layer() in sequence or skip layers based on --skip-* flags
- [ ] T128 [US4] Implement incremental regeneration support in src/codeindex/services/prd_generator.py to allow regenerating specific layers without redoing all analysis (check which layer PRD files exist)

#### Loading Analyzed Artifacts

- [ ] T129 [US4] Implement artifact loading in src/codeindex/services/prd_generator.py to load all DatabaseEntity JSON files from output/database/entities/
- [ ] T130 [US4] Implement artifact loading in src/codeindex/services/prd_generator.py to load all ServiceDefinition JSON files from output/services/definitions/
- [ ] T131 [US4] Implement artifact loading in src/codeindex/services/prd_generator.py to load all APIEndpoint JSON files from output/services/endpoints/
- [ ] T132 [US4] Implement artifact loading in src/codeindex/services/prd_generator.py to load all FormDefinition JSON files from output/frontend/forms/
- [ ] T133 [US4] Implement artifact loading in src/codeindex/services/prd_generator.py to load all UIComponent JSON files from output/frontend/components/
- [ ] T134 [US4] Implement artifact loading in src/codeindex/services/prd_generator.py to load all NavigationFlow JSON files from output/frontend/navigation/
- [ ] T135 [US4] Implement artifact loading in src/codeindex/services/prd_generator.py to load all BusinessRule JSON files from output/business_rules/

#### Executive Summary Generation

- [ ] T136 [US4] Implement executive summary generation in src/codeindex/services/prd_generator.py: generate_executive_summary(entities, services, endpoints, forms, components, rules, ollama_client) returning PRDSection
- [ ] T137 [US4] Extend OllamaClient with method: generate_executive_summary(entity_count, service_count, endpoint_count, form_count, rule_count, technologies, domains, key_entities, key_services) using executive summary prompt from contracts/llm-contracts.md
- [ ] T138 [US4] Implement technology stack detection in src/codeindex/services/prd_generator.py to aggregate frameworks[] from all artifacts and categorize as backend/frontend/database/frameworks
- [ ] T139 [US4] Implement domain detection in src/codeindex/services/prd_generator.py to aggregate domain[] from all artifacts and identify primary domains (auth, billing, reporting, etc.)

#### Architecture Overview Generation

- [ ] T140 [US4] Implement architecture section generation in src/codeindex/services/prd_generator.py to create System Architecture section with: technology stack, architectural patterns (layered, MVC, microservices), module structure (Maven modules)
- [ ] T141 [US4] Implement architectural pattern detection in src/codeindex/services/prd_generator.py to identify patterns from service structure, layering, naming conventions (Controller-Service-DAO pattern, REST API, etc.)

#### Cross-Layer Flow Generation

- [ ] T142 [US4] Implement cross-layer flow generation in src/codeindex/services/prd_generator.py: generate_cross_layer_flows(forms, endpoints, services, entities, ollama_client) returning cross_reference flows
- [ ] T143 [US4] Extend OllamaClient with method: generate_cross_layer_flow(form_json, endpoint_json, service_json, entities_json) using cross-layer flow prompt from contracts/llm-contracts.md
- [ ] T144 [US4] Implement flow tracing in src/codeindex/services/prd_generator.py to trace: form submission → APIEndpoint → ServiceDefinition → DatabaseEntity with all intermediate steps
- [ ] T145 [US4] Implement business rule aggregation in src/codeindex/services/prd_generator.py to identify which rules are applied at each step in cross-layer flows

#### Business Rule Consolidation

- [ ] T146 [US4] Implement business rule consolidation in src/codeindex/services/prd_generator.py to identify duplicate or related rules across layers (same rule enforced at DB, service, and frontend)
- [ ] T147 [US4] Implement rule deduplication in src/codeindex/services/prd_generator.py to merge related rules and show enforcement layers (e.g., "Email validation enforced at: frontend (HTML5 pattern), service (ValidationUtils), database (CHECK constraint)")

#### Gaps and Recommendations

- [ ] T148 [US4] Implement gap analysis in src/codeindex/services/prd_generator.py: identify_gaps(entities, services, forms, components, visit_log) returning gaps and recommendations
- [ ] T149 [US4] Implement missing documentation detection in src/codeindex/services/prd_generator.py to find entities with no description, services with unclear purposes, forms with no backend linkage
- [ ] T150 [US4] Implement missing reference detection in src/codeindex/services/prd_generator.py to find forms with no matching endpoint, endpoints with no implementing service, services accessing unknown entities
- [ ] T151 [US4] Implement failure aggregation in src/codeindex/services/prd_generator.py to collect all failed files from visit_log and report as "Areas Needing Further Investigation"

#### Master PRD Generation

- [ ] T152 [US4] Implement master PRD markdown generation in src/codeindex/services/prd_generator.py using MarkdownBuilder to create output/prd/master_prd.md with sections: Executive Summary, System Architecture, Database Layer (link to database_prd.md), Service Layer (link to service_prd.md), Frontend Layer (link to frontend_prd.md), Business Rules (link to business_rules/index.md), Cross-Layer Flows (detailed flows), Gaps and Recommendations, Appendix
- [ ] T153 [US4] Implement table of contents generation in src/codeindex/services/prd_generator.py with markdown anchor links to all sections
- [ ] T154 [US4] Implement PRD metadata header in src/codeindex/services/prd_generator.py with: generated timestamp, project name, codebase location, analysis date, analysis duration, files analyzed, files skipped, LLM model used

#### Cross-Reference Document Generation

- [ ] T155 [US4] Implement cross-references markdown generation in src/codeindex/services/prd_generator.py to create output/prd/cross_references.md with detailed end-to-end flows, Mermaid sequence diagrams, form→service→database mappings
- [ ] T156 [US4] Implement Mermaid diagram generation in src/codeindex/services/prd_generator.py for sequence diagrams showing flow steps (optional if --include-diagrams flag set)

#### Business Rules Index Generation

- [ ] T157 [US4] Implement business rules index.md generation in src/codeindex/services/prd_generator.py to create output/business_rules/index.md with all rules organized by layer, domain, severity, and type

#### PRD Index Generation

- [ ] T158 [US4] Implement PRD index/table of contents generation in src/codeindex/services/prd_generator.py to create output/prd/index.md with links to all PRD documents: master_prd.md, database_prd.md, service_prd.md, frontend_prd.md, cross_references.md

#### CLI Command Integration

- [ ] T159 [US4] Wire PRD generator orchestrator into src/codeindex/cli/prd.py for layer='full' mode (default), calling prd_generator.generate_prd() which coordinates all layer analyzers
- [ ] T160 [US4] Implement --skip-database, --skip-services, --skip-frontend flags in src/codeindex/cli/prd.py to selectively skip layers
- [ ] T161 [US4] Add full output structure validation in src/codeindex/cli/prd.py to verify all expected output directories and files were created
- [ ] T162 [US4] Implement final summary reporting in src/codeindex/cli/prd.py showing: total entities, services, endpoints, forms, components, rules, cross-layer flows, failed files, gaps identified, output location, analysis duration

**Checkpoint**: User Story 4 complete - master PRD synthesizes all layers with cross-references, executive summary, and comprehensive documentation

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, code quality, and final validations

### Documentation

- [ ] T163 [P] Update CLAUDE.md with PRD generation usage: codeindex prd command, --layer options, output structure, troubleshooting, example workflows
- [ ] T164 [P] Update CLAUDE.md with environment variable documentation: OUTPUT_DIR, PRD generation options
- [ ] T165 [P] Create usage examples in CLAUDE.md: database-only analysis, full PRD generation, incremental updates, domain filtering

### Code Quality

- [ ] T166 [P] Add type hints to all PRD generation functions (db_analyzer, service_analyzer, frontend_analyzer, prd_generator, visit_log, markdown_builder)
- [ ] T167 [P] Add docstrings to all public functions explaining parameters, return values, and purpose
- [ ] T168 [P] Add inline comments for complex LLM prompt engineering logic and cross-referencing algorithms

### Validation

- [ ] T169 [P] Verify all JSON output files conform to schemas from contracts/output-formats.md
- [ ] T170 [P] Verify all markdown output files have valid structure (proper heading levels, valid links)
- [ ] T171 [P] Verify visit log (.visit_log.jsonl) is valid JSONL format with all required fields
- [ ] T172 [P] Verify cross-references point to existing entity/service/form files

### Constitution Checks

- [ ] T173 Run constitution validation checks from plan.md (type safety, error handling, code organization, configuration, documentation, testing, UX, performance, observability)
- [ ] T174 Verify progress reporting meets requirement: updates every 10 seconds showing current layer, files processed, estimated time remaining, current file

### Quickstart Validation

- [ ] T175 Follow quickstart.md walkthrough from start to finish to verify all commands work
- [ ] T176 Verify generated PRD documents are human-readable and well-formatted

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase - can start after Phase 2
- **User Story 2 (Phase 4)**: Depends on Foundational phase - can start after Phase 2 (references US1 entities but independently testable)
- **User Story 3 (Phase 5)**: Depends on Foundational phase - can start after Phase 2 (references US2 endpoints but independently testable)
- **User Story 4 (Phase 6)**: Depends on User Stories 1, 2, 3 completion - must run last to synthesize all layers
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May reference US1 entities (data_dependencies) but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May reference US2 endpoints (submission_endpoint) but independently testable
- **User Story 4 (P4)**: MUST complete after US1, US2, US3 - Synthesizes all layers and cannot run without their outputs

### Within Each User Story

- Phase 2 (Foundational) must complete before any user story
- Within each user story: services before CLI integration
- Visit log integration happens within each analyzer service
- Output generation happens after analysis completes
- CLI command integration is last step for each user story

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (Phase 1)
- All Foundational model creation tasks marked [P] can run in parallel (T010-T019)
- After Foundational phase completes, User Stories 1, 2, 3 CAN run in parallel if team capacity allows (though US2 may reference US1 entities, US3 may reference US2 endpoints - but each is independently testable)
- All Polish tasks marked [P] can run in parallel (Phase 7)

---

## Implementation Strategy

### MVP First (Database Layer Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Database documentation)
4. **STOP and VALIDATE**: Test database analysis independently on a real Java project
5. Verify output/database/ has entities, business rules, index.md, database_prd.md

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Database) → Test independently → Validate (MVP!)
3. Add User Story 2 (Services) → Test independently → Validate
4. Add User Story 3 (Frontend) → Test independently → Validate
5. Add User Story 4 (Master PRD) → Test full pipeline → Validate
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Database)
   - Developer B: User Story 2 (Services)
   - Developer C: User Story 3 (Frontend)
3. Once US1, US2, US3 complete:
   - Developer A: User Story 4 (Master PRD synthesis)
4. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability (US1, US2, US3, US4)
- Each user story should be independently testable
- NO TEST TASKS included (not requested in spec.md)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All file paths are absolute paths from project root
- LLM timeouts: 120 seconds per call, 3 retry attempts, exponential backoff
- Progress reporting: every 10 seconds minimum (constitution requirement)
- Visit log enables incremental analysis (skip unchanged files)
- Cross-references link layers together (form→service→database)
- Master PRD (US4) synthesizes all layer PRDs with executive summary and gaps analysis
