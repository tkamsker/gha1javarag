# Feature Specification: PRD Document Generation from Codebase Analysis

**Feature Branch**: `002-prd-document-generation`
**Created**: 2025-12-14
**Status**: Draft
**Input**: User description: "lets implement next phase is target to genertae prd documents. make it reuseable revisit the .env JAVA_SOURCE_DIR if necessary. make an step by step bottum up concept where you revisit dao and sql objects to generate an database structure and document all bussiness rules from backend then find all services and if necessary revisit the source files to find details and make heavvy use of LLM and write proper prompts to find all details. Fetch info from Weaviate where is necessary. structure the documents hierachical and make an idex file for reuse. Then start at the frontend layer fetch from index.html or htm or jsp and step dwon each form and document it finding all objects you alerady discovered. dig into all GWT and javascript files to also understand the logic in frontends to be able to replicate it in new solution. make also an index files for forntend. and in general keep track of all files you have visited to avoid losing track"

## Clarifications

### Session 2025-12-14

- Q: How should the generated PRD documentation be organized in the output directory? → A: Layered structure with separate subdirectories for each layer (output/database/, output/services/, output/frontend/, output/prd/) with index.md in each
- Q: What timeout and retry limits should apply to LLM calls for analyzing code files? → A: 120 second timeout per LLM call, maximum 3 retry attempts with exponential backoff
- Q: What format should the visit log use to track analyzed files? → A: JSON Lines (.jsonl) format with one JSON object per line containing {file_path, timestamp, status, content_hash, layer} stored in output/.visit_log.jsonl
- Q: How should security-sensitive patterns be marked in the generated documentation? → A: Use markdown admonition blocks with emoji (> 🔒 **Security Pattern:** description) for visual distinction
- Q: How frequently and at what granularity should progress be reported during analysis? → A: Report progress every 10 seconds showing current layer, files processed count, estimated time remaining, and current file being analyzed

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Database Schema and Business Rules Documentation (Priority: P1)

As a business analyst or technical architect, I need to understand the complete database structure and business rules embedded in the backend code so that I can create accurate technical documentation and make informed decisions about system modernization.

**Why this priority**: Database schema and business rules form the foundation of the system. Without understanding the data model and core business logic, any migration or modernization effort will be incomplete or incorrect. This is the most critical starting point.

**Independent Test**: Can be fully tested by pointing the tool at a Java project with DAO/SQL files and verifying it produces a complete database schema document with all tables, relationships, constraints, and business rules extracted from the code.

**Acceptance Scenarios**:

1. **Given** a Java project with DAO classes containing database operations, **When** I run the database documentation generator, **Then** the system produces a structured document listing all database tables with their columns, data types, and relationships
2. **Given** SQL files and iBATIS/MyBatis mapping files in the codebase, **When** the analysis runs, **Then** all queries are analyzed and documented with their purpose and the business rules they enforce
3. **Given** service classes with transaction logic and validation rules, **When** the system analyzes business rules, **Then** all constraints, validations, and business logic patterns are documented with references to source files
4. **Given** a large codebase with multiple modules, **When** the generator creates the database documentation, **Then** an index file is created organizing all discovered entities hierarchically by domain or module
5. **Given** previously analyzed files tracked in a visit log, **When** rerunning the analysis, **Then** the system skips already-processed files unless explicitly requested to refresh

---

### User Story 2 - Backend Services and API Documentation (Priority: P2)

As a developer or integration specialist, I need comprehensive documentation of all backend services, their responsibilities, and API contracts so that I can understand system capabilities and plan service-level migrations.

**Why this priority**: After understanding the data layer, documenting services provides the business logic layer view. This enables understanding of how the system processes data and exposes functionality, which is essential for API-first modernization strategies.

**Independent Test**: Can be tested by analyzing a project with service classes and REST/SOAP endpoints, verifying the tool produces complete service documentation with method signatures, dependencies, and business operations.

**Acceptance Scenarios**:

1. **Given** service classes implementing business logic, **When** the service analyzer runs, **Then** each service is documented with its purpose, public methods, dependencies on DAOs, and business operations
2. **Given** REST controllers or web services in the codebase, **When** API documentation is generated, **Then** all endpoints are listed with HTTP methods, parameters, request/response formats, and linked to their implementing services
3. **Given** complex service orchestration with multiple service interactions, **When** the LLM analyzes the code, **Then** the documentation includes flow descriptions showing how services collaborate to fulfill business processes
4. **Given** services referencing database entities, **When** cross-referencing with database documentation, **Then** the service documentation links to relevant database tables and shows data dependencies
5. **Given** incomplete or ambiguous service logic, **When** LLM-powered analysis is applied, **Then** the system generates intelligent summaries and asks targeted clarifying questions for critical gaps

---

### User Story 3 - Frontend Form and Component Documentation (Priority: P3)

As a UX designer or frontend developer, I need documentation of all user interfaces, forms, and their data bindings so that I can recreate the user experience in a modern framework while maintaining business functionality.

**Why this priority**: Frontend documentation enables understanding of how users interact with the system. This is critical for UI modernization but can be addressed after backend understanding is complete, as frontend often depends on backend contracts.

**Independent Test**: Can be tested by analyzing JSP, HTML, GWT, and JavaScript files, verifying the tool produces UI documentation showing all forms, fields, validation rules, and their connections to backend services.

**Acceptance Scenarios**:

1. **Given** JSP files with forms, **When** the frontend analyzer runs, **Then** all forms are documented with field names, types, validation rules, and submission endpoints
2. **Given** GWT modules and UI widgets, **When** the analysis processes GWT code, **Then** component hierarchies are documented showing activities, views, and their associated presenters or controllers
3. **Given** JavaScript files implementing client-side logic, **When** the LLM analyzes the code, **Then** business rules enforced on the client side are extracted and documented
4. **Given** forms referencing backend entities, **When** cross-referencing with backend documentation, **Then** the UI documentation shows which database entities and services each form interacts with
5. **Given** navigation flows across multiple pages, **When** the frontend documentation is generated, **Then** an index file organizes all entry points (index.html, main JSPs) and maps user journeys through the application

---

### User Story 4 - Comprehensive Cross-Layer PRD Generation (Priority: P4)

As a product manager or project stakeholder, I need a complete Product Requirements Document that synthesizes all technical findings into business-oriented documentation so that I can understand system capabilities, plan modernization roadmaps, and communicate with stakeholders.

**Why this priority**: The final PRD synthesizes all previous analysis layers into actionable business documentation. This is the ultimate deliverable but depends on completing the foundational analysis in stories 1-3.

**Independent Test**: Can be tested by running the full analysis pipeline on a complete Java application, verifying it produces a hierarchical PRD with executive summary, detailed sections for each layer, and cross-references throughout.

**Acceptance Scenarios**:

1. **Given** completed database, service, and frontend documentation, **When** the PRD generator runs, **Then** a master PRD document is created with sections for data model, business logic, and user interface organized hierarchically
2. **Given** multiple modules or subsystems in the codebase, **When** generating the PRD, **Then** the document includes a high-level architecture section showing how modules relate and depend on each other
3. **Given** business rules discovered across all layers, **When** the PRD consolidates findings, **Then** duplicate or related rules are merged and presented coherently with references to all source locations
4. **Given** gaps or ambiguities identified during analysis, **When** the PRD is finalized, **Then** a section highlights areas needing clarification or further investigation with specific questions
5. **Given** the need for ongoing documentation updates, **When** the codebase changes, **Then** the system can regenerate specific sections incrementally without redoing the entire analysis

---

### Edge Cases

- **What happens when analyzing a mixed-technology codebase** (Java + Python services, React frontend)?
  - System should detect and document all languages but may require extending parsers. Initial implementation focuses on Java/JSP/GWT as specified, with clear boundaries documented.

- **How does the system handle extremely large codebases** (>100k files, >10M lines)?
  - System should process in batches with progress tracking, resume capability after interruptions, and memory-efficient streaming. LLM calls should be rate-limited to avoid API overload.

- **What if database schemas are defined in DDL files rather than ORM code?**
  - System should support multiple schema sources: JPA annotations, Hibernate mappings, iBATIS XML, raw DDL files, and database introspection if connection available.

- **How does the system handle generated code** (auto-generated DTOs, proxies)?
  - Generated code should be detected (via annotations or file patterns) and either skipped or documented separately to avoid cluttering business logic documentation.

- **What if the codebase uses custom frameworks or proprietary libraries?**
  - System should gracefully handle unknown patterns by documenting them as "custom implementations" and using LLM to infer purpose from context, method names, and comments.

- **How are security-sensitive patterns handled** (authentication, authorization, encryption)?
  - Security patterns should be highlighted in documentation using markdown admonition blocks with emoji (> 🔒 **Security Pattern:** description). Actual credentials or secrets should never be included in output, only patterns and configuration locations.

- **What happens when LLM analysis produces incorrect or nonsensical results?**
  - System should include confidence scores, allow manual review/correction, and maintain original code references so humans can verify LLM interpretations.

## Requirements *(mandatory)*

### Functional Requirements

#### Database Layer Analysis (User Story 1)

- **FR-001**: System MUST scan all source directories configured in JAVA_SOURCE_DIR for DAO classes, entity classes, SQL files, and ORM mapping files
- **FR-002**: System MUST extract database table definitions from JPA/Hibernate annotations, iBATIS/MyBatis XML mappings, and embedded SQL
- **FR-003**: System MUST identify relationships between entities (one-to-many, many-to-many, foreign keys) from ORM configurations and code analysis
- **FR-004**: System MUST extract business rules from DAO methods, including validation logic, constraints, and transaction boundaries
- **FR-005**: System MUST use LLM to analyze complex SQL queries and stored procedures to infer their business purpose
- **FR-006**: System MUST generate a hierarchical database schema document with sections for each entity, organized by domain or module
- **FR-007**: System MUST create an index file listing all discovered database entities with links to their detailed documentation
- **FR-008**: System MUST track all visited files in a persistent JSON Lines log (output/.visit_log.jsonl) with entries containing {file_path, timestamp, status, content_hash, layer} to enable incremental analysis and avoid reprocessing unchanged files

#### Service Layer Analysis (User Story 2)

- **FR-009**: System MUST identify all service classes by scanning for service annotations, naming patterns, or configuration files
- **FR-010**: System MUST document each service's public interface including method signatures, parameters, return types, and exceptions thrown
- **FR-011**: System MUST analyze service dependencies on DAOs and other services to create a dependency graph
- **FR-012**: System MUST extract REST/SOAP endpoint definitions from controller classes or service configurations
- **FR-013**: System MUST use LLM to generate natural language descriptions of complex business operations implemented in services
- **FR-014**: System MUST cross-reference service operations with database entities to show which tables each service accesses
- **FR-015**: System MUST identify transaction boundaries and transaction management patterns in service code
- **FR-016**: System MUST generate a hierarchical service documentation with sections organized by business capability or module

#### Frontend Analysis (User Story 3)

- **FR-017**: System MUST scan for all HTML, JSP, GWT, and JavaScript files in configured web application directories
- **FR-018**: System MUST extract all forms with their fields, including field names, types, labels, validation rules, and submission targets
- **FR-019**: System MUST analyze GWT modules to document activities, places, views, and UI components
- **FR-020**: System MUST extract client-side JavaScript logic and identify business rules enforced in the browser
- **FR-021**: System MUST identify navigation flows by analyzing links, button actions, and routing configurations
- **FR-022**: System MUST cross-reference form actions with backend endpoints to show which services handle each form submission
- **FR-023**: System MUST use LLM to analyze complex JavaScript event handlers and state management patterns
- **FR-024**: System MUST generate a frontend documentation organized by entry points (main pages) with hierarchical breakdown of components

#### PRD Generation and Integration (User Story 4)

- **FR-025**: System MUST synthesize database, service, and frontend documentation into a cohesive PRD document
- **FR-026**: System MUST generate an executive summary section highlighting key system capabilities and architectural patterns
- **FR-027**: System MUST create cross-references between layers (e.g., which forms use which services, which services access which tables)
- **FR-028**: System MUST identify and consolidate duplicate or related business rules discovered across different layers
- **FR-029**: System MUST highlight gaps, ambiguities, or areas needing further investigation with specific questions or recommendations
- **FR-030**: System MUST organize the PRD hierarchically with a table of contents and section navigation
- **FR-031**: System MUST support incremental regeneration of specific sections without reanalyzing the entire codebase

#### LLM Integration and Prompting (Cross-cutting)

- **FR-032**: System MUST query Weaviate for indexed artifact information before analyzing files to leverage existing semantic understanding
- **FR-033**: System MUST construct targeted LLM prompts based on artifact type (DAO, service, JSP, etc.) to extract relevant information
- **FR-034**: System MUST include relevant context in LLM prompts (related entities, imported classes, calling methods) to improve analysis quality
- **FR-035**: System MUST retry LLM calls with adjusted prompts if initial responses are incomplete or malformed, using 120 second timeout per call with maximum 3 retry attempts using exponential backoff
- **FR-036**: System MUST validate LLM responses for required fields and reasonable content before incorporating into documentation
- **FR-037**: System MUST batch LLM requests efficiently to balance throughput and rate limits

#### Reusability and Configuration (Cross-cutting)

- **FR-038**: System MUST read JAVA_SOURCE_DIR from .env file with ability to override via command-line argument
- **FR-039**: System MUST support analyzing multiple projects sequentially or in parallel with separate output directories
- **FR-040**: System MUST generate reusable index files (index.md) in a layered directory structure: output/database/, output/services/, output/frontend/, and output/prd/, where each layer's index references its detailed documentation files
- **FR-041**: System MUST persist analysis state in JSON Lines format (output/.visit_log.jsonl tracking visited files, plus intermediate extracted entities) to enable resuming interrupted runs
- **FR-042**: System MUST provide a command-line interface with options to analyze specific layers (database-only, services-only, etc.)
- **FR-043**: System MUST output documentation in markdown format organized in layered subdirectories (database/, services/, frontend/, prd/) with optional HTML rendering capability
- **FR-044**: System MUST report analysis progress every 10 seconds minimum showing current layer being analyzed, files processed count, estimated time remaining, and current file being processed

### Key Entities

- **DatabaseEntity**: Represents a table or collection in the database with attributes (columns), relationships (foreign keys), and constraints
- **BusinessRule**: Represents a validation, constraint, or business logic pattern with its scope (database, service, frontend), description, and source code references
- **ServiceDefinition**: Represents a backend service with its operations (methods), dependencies, and exposed endpoints
- **APIEndpoint**: Represents a REST/SOAP endpoint with HTTP method, path, parameters, request/response formats, and implementing service
- **FormDefinition**: Represents a UI form with fields, validation rules, submission endpoint, and associated data entities
- **UIComponent**: Represents a frontend component (GWT widget, JavaScript module) with its responsibilities, events, and data bindings
- **NavigationFlow**: Represents a user journey through multiple pages/screens with entry points, transitions, and exit points
- **VisitLog**: Tracks which files have been analyzed with timestamps and analysis status to enable incremental processing
- **IndexEntry**: Entry in a hierarchical index file pointing to detailed documentation with metadata (layer, domain, category)
- **PRDSection**: A section of the final PRD document with title, content, and cross-references to other sections

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can generate a complete database schema document from a Java project with 100+ entity classes in under 10 minutes
- **SC-002**: Service documentation accurately captures 95%+ of public APIs and their business purposes as validated by manual spot-checking
- **SC-003**: Frontend documentation identifies all user entry points and critical forms in a web application within one analysis run
- **SC-004**: The generated PRD includes cross-references showing end-to-end flows (UI form → service → database) for 90%+ of major features
- **SC-005**: Incremental analysis (reanalyzing only changed files) completes 10x faster than full analysis for codebases with <10% file changes
- **SC-006**: LLM-generated descriptions of business logic achieve 80%+ accuracy as measured by developer validation surveys
- **SC-007**: The system successfully tracks and skips 95%+ of previously analyzed files in subsequent runs to avoid duplicate work
- **SC-008**: Generated documentation follows a consistent hierarchical structure across all analyzed projects enabling easy navigation
- **SC-009**: The system handles codebases with 10,000+ files without running out of memory by using streaming and batch processing
- **SC-010**: Generated PRDs reduce the time required for technical due diligence or modernization planning by 60%+ compared to manual analysis

## Assumptions

- The Java codebases to analyze follow common architectural patterns (DAO/Service/Controller layers)
- Ollama LLM service is available and has sufficient context window for analyzing medium-sized classes (1000-2000 lines)
- The Weaviate vector database contains indexed artifacts from prior discovery and extraction phases (feature 001)
- Source code has at least minimal comments or meaningful naming conventions to aid LLM analysis
- The .env configuration correctly points to all relevant source directories
- Generated documentation is intended for human readers (business analysts, architects, developers) not machine processing
- Output markdown files will be stored in a designated output directory with adequate disk space (assume <1GB per analyzed project)
- Users running the analysis have read access to all source files and configuration files in JAVA_SOURCE_DIR

## Out of Scope

- Runtime analysis or dynamic behavior monitoring (only static code analysis)
- Modifying or refactoring the analyzed codebase
- Generating executable code or migration scripts from the documentation
- Real-time documentation updates as code changes (batch analysis only)
- Analyzing non-Java/non-web frontend technologies (mobile apps, desktop applications)
- Version control integration (tracking documentation changes over time)
- Collaborative editing or multi-user access to generated documentation
- Compliance verification (GDPR, HIPAA) or security vulnerability scanning
- Performance profiling or optimization recommendations
- Automated testing of the analyzed application

## Dependencies

- **Feature 001 (Java Codebase Indexer)**: This feature builds on the discovery and extraction capabilities from the existing indexer
- **Ollama LLM Service**: Requires local or accessible Ollama instance for generating business logic summaries and inferring intent
- **Weaviate Vector Database**: Requires indexed artifacts to provide context and avoid redundant analysis
- **Python Environment**: Implementation will use the existing Python codebase and CLI framework
- **File System Access**: Requires read access to JAVA_SOURCE_DIR and write access to output directory
- **Markdown Renderer** (optional): For converting generated markdown to HTML if viewing in browser is needed
