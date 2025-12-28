# Feature Specification: GWT Navigation Analysis and Error Fixes

**Feature Branch**: `007-gwt-navigation-and-error-fixes`
**Created**: 2025-12-22
**Status**: Draft
**Input**: User description: "Analyse log file and try to fix errors and fix the reading frontend layout and function especially GWT based informations go from index.htm or index.jsp or index.htm down to each href and web function"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Fix Ollama Timeout Failures (Priority: P1)

As a developer analyzing large codebases, I need the extraction process to complete successfully for all files without timeout failures, so that I can generate complete Product Requirements Documents with all service and DAO documentation.

**Why this priority**: This is blocking - 29 timeout failures were observed in production logs, meaning critical services and DAOs are missing from PRD documentation. Without fixing this, the entire analysis pipeline is unreliable for large codebases.

**Independent Test**: Can be fully tested by running extraction on the cuco-ui-admin codebase (539 files) and verifying zero timeout errors in logs. Delivers immediate value by enabling complete documentation generation.

**Acceptance Scenarios**:

1. **Given** a large service file (>1000 lines) being analyzed, **When** LLM extraction is triggered, **Then** the system completes analysis within timeout threshold OR falls back gracefully to structural analysis
2. **Given** Ollama service is temporarily slow, **When** extraction timeout occurs, **Then** system retries with exponential backoff up to 3 attempts before falling back
3. **Given** extraction completes with fallback mode, **When** results are logged, **Then** detailed metrics show timeout duration, retry count, and fallback reason
4. **Given** a batch of 100 files being analyzed, **When** some files timeout, **Then** remaining files continue processing without cascading failures

---

### User Story 2 - Fix Database Foreign Key Validation (Priority: P1)

As a database analyst, I need accurate foreign key relationships extracted from DAO files, so that generated data model diagrams show correct entity relationships and dependencies.

**Why this priority**: This is critical for data model accuracy - 4 FK validation failures were observed (salesInfoId, productId, customerId, user_id). Inaccurate FK relationships lead to incorrect ERD diagrams and mislead architects about data dependencies.

**Independent Test**: Can be fully tested by analyzing DAOs with known FK relationships (MyNotesDao, InventoryProductGroupDao, SingleTurnaroundDao, TeamDao) and verifying all foreign keys are correctly extracted and validated. Delivers complete and accurate database schema documentation.

**Acceptance Scenarios**:

1. **Given** a DAO file with foreign key annotations (@JoinColumn), **When** columns are extracted, **Then** system collects all column definitions before validating foreign keys
2. **Given** a DAO with foreign keys defined in iBATIS XML, **When** extraction occurs, **Then** system parses both Java annotations AND iBATIS statements to find FK relationships
3. **Given** a foreign key column not found in Java code, **When** SQL queries are analyzed, **Then** system extracts FK from SQL JOIN statements as fallback
4. **Given** a missing FK column after all sources checked, **When** validation fails, **Then** system logs warning but continues processing other relationships gracefully

---

### User Story 3 - Implement GWT Navigation Path Analysis (Priority: P1)

As a frontend architect, I need a complete navigation graph starting from entry points (index.html, index.jsp, *.gwt.xml), so that I understand the full GWT application structure, all user flows, and how Presenters/Views are connected.

**Why this priority**: This is essential for frontend architecture understanding - currently only 1 GWT Presenter was detected (RestrictedPartyDataPortletPresenter), missing the entire UI structure. Without this, frontend PRDs are incomplete and navigation flows are undocumented.

**Independent Test**: Can be fully tested by parsing cuco-ui-admin's index.jsp entry point, following all GWT module references, and verifying >90% of GWT Presenters/Views are discovered. Delivers complete frontend architecture map.

**Acceptance Scenarios**:

1. **Given** an index.html/jsp file with GWT module references, **When** navigation analysis starts, **Then** system parses all `<script>` and `<module>` tags to find GWT entry points
2. **Given** a GWT module descriptor (*.gwt.xml), **When** module is analyzed, **Then** system extracts entry-point classes, inherits clauses, and source paths
3. **Given** an entry-point Presenter class, **When** navigation paths are followed, **Then** system discovers bound Views, Activities, Places, and navigation targets
4. **Given** a View with UiBinder template, **When** template is parsed, **Then** system extracts widget references, event handlers, and navigation buttons/links
5. **Given** navigation analysis completes, **When** results are generated, **Then** system produces a navigation graph showing all paths from index.html to leaf UI components

---

### User Story 4 - Enhanced Frontend Layout Extraction (Priority: P2)

As a UI/UX analyst, I need detailed frontend component hierarchies with Presenter-View-UiBinder relationships mapped, so that I can understand the UI structure, widget composition, and generate architecture diagrams with navigation flows.

**Why this priority**: This is important for comprehensive documentation - while US3 provides navigation structure, this user story adds depth by mapping exact component relationships, widget hierarchies, and template bindings. It enables generation of detailed frontend architecture diagrams.

**Independent Test**: Can be fully tested by analyzing GWT modules with UiBinder templates, extracting widget hierarchies, mapping Presenter-View bindings, and generating Mermaid diagrams showing component relationships. Delivers enhanced frontend documentation and visual architecture diagrams.

**Acceptance Scenarios**:

1. **Given** a UiBinder XML template with nested widgets, **When** template is parsed, **Then** system extracts widget hierarchy showing parent-child relationships and container types
2. **Given** a Presenter with Display interface, **When** binding analysis occurs, **Then** system maps Presenter → View interface → concrete View implementation → UiBinder template
3. **Given** UiBinder widgets with @UiField annotations, **When** extraction completes, **Then** system documents field names, types, and whether they have event handlers
4. **Given** navigation analysis completes for all modules, **When** diagram generation is triggered, **Then** system produces Mermaid diagrams showing Presenter-View-UiBinder relationships with navigation flows

---

### Edge Cases

- **What happens when index.html/jsp has multiple GWT module references?** System analyzes all modules in parallel and merges navigation graphs, marking entry points clearly
- **What happens when GWT module descriptor has circular `<inherits>` clauses?** System detects circular dependencies, logs warning, and processes each module once using visited tracking
- **What happens when Presenter-View binding uses non-standard patterns (not Display interface)?** System falls back to naming conventions (FooPresenter → FooView) and logs confidence score
- **What happens when UiBinder template references widgets not in classpath?** System logs missing widget types but continues extracting available widgets
- **What happens when Ollama times out after all retry attempts?** System falls back to structural analysis (parsing Java AST) and logs detailed fallback metrics
- **What happens when DAO has foreign keys in both @JoinColumn and iBATIS XML?** System merges FK sources, prioritizes Java annotations, and marks duplicate FKs in validation
- **What happens when navigation path leads to external URL (non-GWT)?** System marks as external boundary, logs URL, and stops traversal at that point

## Requirements *(mandatory)*

### Functional Requirements

#### Ollama Timeout Handling (US1)

- **FR-001**: System MUST use adaptive Ollama read timeout with configurable base (default 600 seconds), calculated as `base_timeout * (1 + file_lines / 1000)` for files larger than 1000 lines
- **FR-002**: System MUST implement exponential backoff retry logic with 3 attempts (delays: 5s, 15s, 45s)
- **FR-003**: System MUST fall back to structural analysis (Java AST parsing without LLM) when all retry attempts fail, extracting class names, method signatures, imports, and annotations (estimated 60-70% semantic coverage compared to LLM analysis)
- **FR-004**: System MUST log timeout metrics including file path, timeout duration, retry count, and fallback reason
- **FR-005**: System MUST continue processing remaining files when individual file timeouts occur
- **FR-006**: System MUST display timeout summary in pipeline status showing: total timeouts, successful retries, fallback count

#### Database Foreign Key Validation (US2)

- **FR-007**: System MUST collect all column definitions from Java annotations (@Column, @JoinColumn) before validating foreign keys
- **FR-008**: System MUST extract foreign key relationships from iBATIS XML `<select>`, `<insert>`, `<update>` statements
- **FR-009**: System MUST parse SQL JOIN statements to extract foreign key column relationships as fallback
- **FR-010**: System MUST validate foreign key columns exist in collected column set before creating FK relationship
- **FR-011**: System MUST handle missing FK columns gracefully by logging WARNING with FK details (source/target columns) and continuing processing of other FK relationships without failing entire DAO analysis
- **FR-012**: System MUST merge foreign keys from multiple sources (Java, iBATIS, SQL) and mark source in metadata

#### GWT Navigation Path Analysis (US3)

- **FR-013**: System MUST parse index.html and index.jsp files to extract GWT module references from `<script>` tags
- **FR-014**: System MUST parse GWT module descriptors (*.gwt.xml) to extract entry-point classes, inherits, and source paths
- **FR-015**: System MUST follow GWT module `<inherits>` clauses recursively to discover all inherited modules
- **FR-016**: System MUST detect circular module dependencies, log WARNING with cycle path (e.g., "A → B → A"), and process each module exactly once using visited tracking
- **FR-017**: System MUST extract GWT Presenters by analyzing entry-point classes and following Activity/Place patterns
- **FR-018**: System MUST discover View interfaces and implementations through Presenter Display pattern analysis
- **FR-019**: System MUST extract GWT Activities and Places from PlaceHistoryMapper and ActivityMapper classes
- **FR-020**: System MUST parse UiBinder XML templates to extract navigation widgets (buttons, links) and their targets
- **FR-021**: System MUST build navigation graph showing paths from index.html through modules to Presenters to Views
- **FR-022**: System MUST mark navigation boundaries (entry points, external URLs, dead ends) in navigation graph

#### Enhanced Frontend Layout Extraction (US4)

- **FR-023**: System MUST extract UiBinder widget hierarchies showing parent-child relationships and container types, up to 10 levels deep, logging WARNING for deeper nesting
- **FR-024**: System MUST map Presenter → Display interface → View implementation → UiBinder template relationships
- **FR-025**: System MUST extract @UiField annotations with field names, types, and event handler presence
- **FR-026**: System MUST document widget event handlers (@UiHandler) with handler methods and event types
- **FR-027**: System MUST generate Mermaid component diagrams showing Presenter-View-UiBinder relationships
- **FR-028**: System MUST include navigation flows in generated diagrams using arrows and labels

### Key Entities

- **NavigationGraph**: Represents complete UI navigation structure starting from entry points
  - Attributes: entry_points (list of index.html/jsp), modules (GWT module descriptors), paths (navigation flows)
  - Relationships: Contains NavigationNodes, references GWT Modules

- **NavigationNode**: Single node in navigation graph (Presenter, View, Activity, Place, or external URL)
  - Attributes: node_id, node_type (presenter/view/activity/place/external), label, source_file
  - Relationships: Has outgoing edges to other NavigationNodes, belongs to NavigationGraph

- **GWTModule**: GWT module descriptor parsed from *.gwt.xml
  - Attributes: module_name, entry_points (classes), inherits (parent modules), source_paths
  - Relationships: Has entry-point Presenters, inherits other GWTModules

- **PresenterViewBinding**: Maps Presenter to View interface to concrete View implementation to UiBinder template
  - Attributes: presenter_class, display_interface, view_class, ui_binder_template, confidence_score
  - Relationships: Presenter has-one Display, Display implemented-by View, View uses UiBinder

- **UiBinderHierarchy**: Widget hierarchy extracted from UiBinder XML template
  - Attributes: template_path, root_widget, widgets (nested structure), event_handlers
  - Relationships: Belongs to View, contains Widget nodes

- **ForeignKeyRelationship**: Database foreign key relationship with source tracking
  - Attributes: source_entity, source_column, target_entity, target_column, fk_source (Java/iBATIS/SQL)
  - Relationships: Links two database entities, extracted from DAO

- **TimeoutMetric**: Tracks Ollama timeout events for monitoring
  - Attributes: file_path, file_size, timeout_duration, retry_count, fallback_used, timestamp
  - Relationships: Logged per extraction attempt

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Zero Ollama timeout failures result in missing documentation when analyzing production codebases (539+ files)
- **SC-002**: All extraction attempts complete within 600 seconds OR fall back gracefully to structural analysis
- **SC-003**: 100% of foreign key relationships are correctly extracted from DAO files without validation errors
- **SC-004**: Foreign keys missing in Java annotations are recovered from iBATIS XML or SQL statements (>80% recovery rate)
- **SC-005**: Complete GWT navigation graph is generated starting from index.html/jsp entry points
- **SC-006**: Greater than 90% of GWT Presenters, Views, Activities, and Places are discovered through navigation analysis
- **SC-007**: Presenter-View-UiBinder relationships are mapped with >85% accuracy based on Display pattern and naming conventions
- **SC-008**: Generated frontend architecture diagrams include navigation flows from all entry points to at least 80% of discovered Presenters and Views
- **SC-009**: Pipeline execution time increases by less than 20% compared to current implementation (acceptable overhead for improved accuracy)
- **SC-010**: Developers can understand complete GWT application structure by reading generated PRD and navigation graph

### Assumptions

- GWT applications follow standard MVP patterns (Presenter-Display-View)
- UiBinder templates use standard naming conventions (*.ui.xml)
- GWT module descriptors are valid XML and follow GWT schema
- iBATIS XML statements follow standard iBATIS/MyBatis syntax
- Ollama service is running and accessible on configured port
- Log file analysis provides representative sample of production errors
- Foreign key columns use standard naming conventions (entityId, entity_id)
- Navigation widgets (buttons, links) have click handlers or hrefs leading to navigation events
- Structural analysis (Java AST parsing) is sufficient fallback when LLM unavailable
- Production codebase (cuco-ui-admin) is representative test case for validation

### Out of Scope

- Analyzing non-GWT frontend frameworks (React, Angular, Vue)
- Parsing JavaScript navigation logic in non-GWT codebases
- Extracting foreign keys from JPA @Entity classes (already handled in existing code)
- Generating interactive navigation diagrams (Mermaid static diagrams only)
- Fixing other extraction errors not related to timeouts or FK validation
- Adding support for custom GWT widget libraries beyond standard GWT widgets
- Optimizing Ollama model performance (infrastructure concern)
- Migrating from Ollama to other LLM providers
- Supporting multiple concurrent extraction processes
