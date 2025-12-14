# Feature Specification: Java Codebase Indexer Pipeline

**Feature Branch**: `001-java-codebase-indexer`
**Created**: 2025-12-12
**Status**: Draft
**Input**: User description: "Build a Python CLI pipeline that scans Java-family source trees, uses local Ollama model to understand each file, and indexes structured artifacts plus embeddings into a local Weaviate instance for later PRD and requirements generation"

## Clarifications

### Session 2025-12-12

- Q: What is the intended lifecycle for indexed project data in Weaviate? → A: Persist indefinitely - Data remains until user explicitly resets or re-indexes a project (aligns with idempotent design)
- Q: Can multiple pipeline operations run concurrently? → A: Per-project locking - Operations on different projects can run concurrently, but same project is locked (balanced approach)
- Q: How should the system handle the same project with multiple versions? → A: Separate projects - Each version gets unique project ID (groupId:artifactId:version), all versions can coexist in Weaviate
- Q: Should the system implement rate limiting for AI calls to Ollama? → A: Configurable rate limit - Max concurrent requests configurable via environment (e.g., MAX_CONCURRENT_AI_CALLS=10), with sensible defaults
- Q: How should the system present empty state scenarios to users? → A: Informative messages - Display clear message explaining the empty state with suggested next steps (e.g., "No Maven projects found. Check JAVA_SOURCE_DIR path.")

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Discover and Catalog Java Projects (Priority: P1)

As a developer analyzing a legacy Java codebase, I need to scan the directory tree and automatically identify all Maven projects, their modules, and file inventory, so that I understand the structure and scope of the codebase before deeper analysis.

**Why this priority**: This is the foundation - without project discovery and file inventory, no further analysis is possible. It provides immediate value by revealing the structure of complex multi-module codebases.

**Independent Test**: Can be fully tested by pointing the tool at a Java source directory and verifying it produces a complete inventory of projects, modules, and files with correct classifications. Delivers a navigable catalog of the codebase structure.

**Acceptance Scenarios**:

1. **Given** a directory containing multiple Maven projects with nested modules, **When** user runs the discover command with that directory path, **Then** the system identifies all pom.xml locations, extracts Maven coordinates, captures module hierarchy, and creates an inventory listing all source files with their types and paths.

2. **Given** a directory with mixed file types (Java, JSP, XML, SQL, JavaScript), **When** the discovery process analyzes the files, **Then** each file is classified by type (java_source, jsp_view, xml_config, sql_schema, etc.) based on extension and path patterns.

3. **Given** a project with standard Maven directory structure (src/main/java, src/main/resources, src/main/webapp), **When** discovery scans the project, **Then** the system records all source roots, test directories, and resource locations for each module.

4. **Given** a codebase with 10,000+ files, **When** user runs discovery, **Then** the process completes without loading all files into memory simultaneously and provides progress updates during scanning.

---

### User Story 2 - Extract Semantic Understanding with AI (Priority: P2)

As a developer analyzing legacy code, I need the system to use AI to understand what each file does, classify its purpose, identify key entities, and tag it with relevant metadata, so that I can search and navigate the codebase semantically rather than just by file names.

**Why this priority**: This transforms raw file inventory into meaningful, searchable knowledge. It's the core value proposition - using AI to understand code semantics.

**Independent Test**: Can be tested by running extraction on a discovered project and verifying that each file has an AI-generated summary, classification, entity list, and relevant tags. The output should be readable and accurate enough to understand file purposes without opening them.

**Acceptance Scenarios**:

1. **Given** a discovered inventory of Java source files, **When** user runs the extract command, **Then** the system processes each file to generate a natural language summary of its purpose, identifies key entities (classes, methods, interfaces), and tags it with relevant categories (layer, domain, frameworks, concerns).

2. **Given** a Java class implementing a data access layer, **When** extraction analyzes it, **Then** the AI summary describes its persistence role, identifies the database entities it manages, tags it as "persistence" layer and "data_access" concern, and recognizes frameworks like JDBC or iBATIS if present.

3. **Given** a JSP file with forms and controller references, **When** extraction processes it, **Then** the system identifies form fields, action targets, taglibs used, and tags it as "frontend" layer and "UI_flow" concern.

4. **Given** an XML file that could be Spring config, Hibernate mapping, or GWT descriptor, **When** extraction analyzes it, **Then** the AI examines the content structure and correctly classifies it (xml_config vs orm_mapping vs gwt_module) beyond just the file extension.

5. **Given** files with malformed syntax or incomplete code, **When** extraction processes them, **Then** the system continues processing other files and logs the error with the problematic file path, rather than failing the entire extraction.

6. **Given** large files that exceed token limits, **When** extraction encounters them, **Then** the system chunks the file into logical units (classes or methods), processes each chunk with maintained ordering, and preserves the relationship between chunks.

---

### User Story 3 - Index for Semantic Search (Priority: P3)

As a developer, I need all extracted artifacts and their AI-generated understanding indexed in a vector database, so that I can perform semantic searches to find code by what it does rather than just text matching, enabling downstream PRD generation.

**Why this priority**: Indexing enables semantic search and is the prerequisite for future PRD generation features. While critical for the complete workflow, it depends on successful discovery and extraction.

**Independent Test**: Can be tested by running indexing on extracted artifacts and then performing sample searches (e.g., "authentication logic", "database queries") to verify that semantically relevant files are returned, not just text matches.

**Acceptance Scenarios**:

1. **Given** extracted artifacts with summaries and tags, **When** user runs the index command, **Then** the system stores each artifact in Weaviate with all metadata (project, path, type, summary, entities, tags) and generates vector embeddings for semantic search.

2. **Given** a project that has been indexed previously, **When** user runs indexing again on the same project, **Then** the system updates existing records rather than creating duplicates, using a deterministic key based on project ID, file path, and content hash.

3. **Given** multiple Maven projects in the codebase, **When** indexing completes, **Then** each artifact is tagged with its project ID, enabling searches filtered to specific projects (e.g., "find authentication in project-auth module").

4. **Given** indexed artifacts with layer tags (backend, frontend, persistence), **When** user searches for specific functionality, **Then** results can be filtered by layer, domain, framework, or concern to narrow semantic search to relevant areas.

5. **Given** temporary network failures to Weaviate during indexing, **When** the failure occurs, **Then** the system retries with exponential backoff and logs the retry attempts, resuming from the last successful artifact rather than restarting from scratch.

---

### User Story 4 - Monitor and Validate Indexing Status (Priority: P4)

As a developer, I need to check what has been indexed and validate that the process completed successfully, so that I can verify completeness before relying on the indexed data for searches or PRD generation.

**Why this priority**: This provides essential observability but is lower priority than the core indexing workflow. It's most valuable after the pipeline is functional.

**Independent Test**: Can be tested by running a status command after indexing and verifying it displays accurate counts of projects and artifacts by type, matching what was actually indexed.

**Acceptance Scenarios**:

1. **Given** projects and artifacts have been indexed, **When** user runs the status command, **Then** the system queries Weaviate and displays counts of indexed projects, total artifacts, and breakdown by artifact type (java_source: X, jsp_view: Y, etc.).

2. **Given** indexing completed with some failures, **When** user views the status, **Then** the system reports both successful and failed items with error summaries, allowing the user to identify which files need attention.

3. **Given** multiple projects indexed at different times, **When** user checks status, **Then** the system shows per-project statistics including when each was last indexed and total artifact counts per project.

---

### Edge Cases

- What happens when pom.xml files are malformed or missing required fields (groupId, artifactId)?
  - System generates fallback project ID from directory path hash and logs a warning

- How does the system handle extremely large files (>100k lines)?
  - Files are chunked into logical units with preserved ordering, each chunk indexed separately

- What happens when Ollama service is unavailable during extraction?
  - System retries with exponential backoff, logs the error, and if persistent failure occurs, skips AI enhancement but continues with basic file classification

- How does indexing handle duplicate files (same content in multiple locations)?
  - Each file instance is indexed separately with its own path, but the content hash allows identifying duplicates if needed

- What happens when user interrupts a long-running operation?
  - System saves progress so far and can resume from the last checkpoint in subsequent runs

- How does the system handle non-UTF-8 encoded files?
  - System attempts to detect encoding, falls back to Latin-1 or ASCII, and logs encoding issues while continuing processing

- What happens when Weaviate schema already exists but with incompatible structure?
  - System detects schema mismatch, reports the conflict, and requires user to either migrate data or reset the schema

- What happens when user attempts to run multiple operations on the same project simultaneously?
  - Second operation detects the project lock, reports that project is currently being processed, and exits with clear error message suggesting to wait or use a different project

- What happens when discovery finds no Maven projects in the configured directory?
  - System displays informative message "No Maven projects found in [path]. Check that JAVA_SOURCE_DIR points to a directory containing pom.xml files." and exits successfully with empty inventory

- What happens when status command is run but no data has been indexed yet?
  - System displays "No projects have been indexed yet. Run discover, extract, and index commands to populate the database." with instructions for getting started

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST recursively scan a configured source directory to discover all subdirectories containing pom.xml files and treat each as a Maven project root.

- **FR-002**: System MUST parse pom.xml files to extract Maven coordinates (groupId, artifactId, version), packaging type, module declarations, dependency lists, and plugin configurations.

- **FR-003**: System MUST classify discovered files by type based on extension and path patterns, supporting at minimum: java_source, java_test, jsp_view, html_template, gwt_module, js_script, sql_schema, sql_query, orm_mapping, ibatis_mapping, xml_config, properties_file, static_asset, and other_text.

- **FR-004**: System MUST generate a structured inventory output (JSON, SQLite, or JSONL) containing all discovered projects, their module hierarchy, and complete file listings with classifications.

- **FR-005**: System MUST send file content to a local AI model to generate natural language summaries describing each file's purpose and functionality.

- **FR-006**: System MUST use AI to identify key entities within files, including class names, method names, interfaces, form fields, endpoints, database tables, and queries.

- **FR-007**: System MUST generate normalized tags for each file capturing layer (backend, frontend, integration, persistence, config), domain (auth, billing, reporting, etc.), frameworks (GWT, Struts, Spring MVC, iBATIS, JDBC, JSP), technology (Java, SQL, HTML, XML), and concerns (security, validation, business_rule, data_access, UI_flow).

- **FR-008**: System MUST add deterministic tags based on directory path and file type patterns (test, config, resource, view, controller) independent of AI output.

- **FR-009**: System MUST chunk large files into logical units (classes, methods, or natural sections) when they exceed token limits, preserving ordering through chunk index and count fields.

- **FR-010**: System MUST store all extracted artifacts and metadata in a vector database with semantic embeddings for search.

- **FR-011**: System MUST create a stable project identifier for each Maven project using the full Maven coordinates (groupId:artifactId:version) when available, treating each version as a distinct project, or from a hash of path and POM content as fallback, enabling multiple versions of the same project to coexist in Weaviate.

- **FR-012**: System MUST make indexing idempotent - re-running on the same codebase updates existing records using deterministic keys (project ID + file path + content hash) rather than creating duplicates.

- **FR-013**: System MUST provide a reset option to clear all previously indexed data for a specific project before re-indexing.

- **FR-014**: System MUST implement retry logic with exponential backoff for transient failures when communicating with external services.

- **FR-015**: System MUST log all operations with configurable verbosity levels, recording project detection, file counts per type, AI processing, indexing success/failure, and performance metrics.

- **FR-016**: System MUST provide progress indicators for long-running operations, updating at reasonable intervals during scanning, extraction, and indexing.

- **FR-017**: System MUST validate availability and schema compatibility of external services (Ollama, Weaviate) before starting operations.

- **FR-018**: System MUST provide a status command that queries the vector database and reports indexed project counts, artifact counts by type, and per-project statistics.

- **FR-019**: System MUST collect and summarize errors by type at the end of execution, reporting total failures with categorized error messages.

- **FR-020**: System MUST support resuming partially completed operations by tracking processed files and skipping already-indexed items unless force flag is set.

- **FR-021**: System MUST read configuration from environment file including source directory path, vector database URL, AI model name, token limits, chunk sizes, maximum concurrent AI calls, and operational flags.

- **FR-022**: System MUST accept command-line arguments that override environment file configuration for flexibility in different execution contexts.

- **FR-023**: System MUST process codebases incrementally without loading all files into memory simultaneously to support large codebases on limited-memory workstations.

- **FR-024**: System MUST persist indexed data indefinitely in Weaviate until explicitly removed via the reset command, supporting long-term historical queries and avoiding data loss.

- **FR-025**: System MUST support concurrent operations on different projects but prevent concurrent operations on the same project through per-project locking, avoiding race conditions while enabling parallel analysis of multiple codebases.

- **FR-026**: System MUST implement configurable rate limiting for AI calls to Ollama with a default maximum of 10 concurrent requests, preventing service overload while maintaining good throughput during extraction operations.

- **FR-027**: System MUST provide informative messages for empty state scenarios (no projects found, no files to extract, no indexed data) with clear explanations and suggested next steps, helping users diagnose configuration issues or understand system state.

### Key Entities

- **Project**: Represents a Maven project root, containing Maven coordinates (groupId, artifactId, version), packaging type, module list, dependency information, framework usage, source root directories, and aggregated metadata about the project's purpose and scope. Each version of a project is treated as a distinct entity with its own unique project ID, allowing multiple versions to coexist for comparison and historical analysis.

- **CodeArtifact**: Represents a single file or chunk of a file, containing the project it belongs to, relative file path, file name, programming language, artifact type classification, detected frameworks, AI-generated summary, list of entities (classes, methods, forms, queries), normalized tags (layer, domain, concerns), dependency references, Maven context, chunk ordering information (if chunked), content hash, and vector embedding for semantic search.

- **DiscoveryInventory**: Intermediate structure capturing scan results, containing list of detected projects with their locations, complete file tree with type classifications, module hierarchies, and statistics about discovered content.

- **ExtractionResult**: Intermediate structure containing AI-generated understanding of a file, including classification refinement, natural language summary, identified entities, generated tags, detected frameworks and technologies, confidence scores, and any parsing errors or warnings.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can discover all projects in a codebase containing 100+ Maven modules in under 5 minutes with complete inventory of file types and counts.

- **SC-002**: System accurately classifies 95%+ of common Java ecosystem files (Java, JSP, XML configs, SQL) into correct artifact types.

- **SC-003**: AI-generated summaries provide enough context that users can understand a file's purpose without opening it, as validated by user testing or review samples.

- **SC-004**: Semantic search returns relevant code artifacts for natural language queries like "authentication logic" or "database persistence" with precision above 80% (relevant results in top 10).

- **SC-005**: Indexing operations are idempotent - running indexing twice on the same codebase produces identical results without duplication.

- **SC-006**: System processes at least 50 Java source files per minute during extraction including AI analysis, suitable for overnight processing of large enterprise codebases.

- **SC-007**: System recovers from temporary service failures (network blips, service restarts) and completes operations without manual intervention through automatic retries.

- **SC-008**: Users can determine indexing completeness and identify any failures within 30 seconds using the status command.

- **SC-009**: System operates successfully on a developer workstation with 8GB RAM when processing codebases with 100k+ files by using streaming and incremental processing.

- **SC-010**: Progress indicators update at least every 10 seconds during long-running operations, providing estimated completion times so users can plan their work.

- **SC-011**: 95% of extraction operations complete successfully even when encountering malformed files, with errors logged but not blocking processing of other files.

## Assumptions

- Local Ollama service is properly installed and the gemma3:12b model is available at localhost:11434
- Local Weaviate instance is running and accessible at the configured URL
- Source code directories are readable by the user running the tool
- Maven projects follow standard directory conventions (src/main/java, pom.xml at project root)
- Target codebases are Java-family technologies (Java, JSP, GWT, JavaScript) as specified
- Users have sufficient disk space for inventory files and logs
- Network connectivity between Python application, Ollama, and Weaviate is reliable within the local environment
- Users understand basic command-line operation and can configure environment files
- Source code files use UTF-8 or compatible encoding
- Weaviate is configured with appropriate vectorization settings for semantic search

## Out of Scope

- Cloud-based LLM services - only local Ollama is supported in this phase
- Actual PRD generation - this phase focuses on indexing only, PRD generation is future work
- Advanced search interfaces - basic search capability only, advanced UI or query languages are future work
- Multi-language codebases beyond Java family (C++, C#, Python) - focused on Java ecosystem only
- Real-time monitoring dashboards - basic status command only
- Distributed processing across multiple machines - single workstation only
- Code modification or refactoring - read-only analysis only
- Security scanning or vulnerability detection - focus is on understanding and indexing, not security analysis
- Performance profiling or code quality metrics - focus is on semantic understanding for documentation
- Integration with specific IDEs or editors - standalone CLI tool only
- Automatic updates or version management - manual execution only
- Multi-user access control or collaboration features - single-user local tool
- Historical analysis or change tracking - snapshot analysis only, not tracking changes over time

## Dependencies

- Local Ollama installation with gemma3:12b model
- Local Weaviate instance running in Docker
- Python environment with required libraries (Click, Weaviate client, HTTP client for Ollama)
- Access to Java source code directories
- Adequate disk space for temporary inventory files

## Non-Functional Considerations

### Performance
- Discovery should process 1000+ files per second
- Extraction should process 50+ files per minute including AI calls
- Indexing should batch operations to Weaviate for efficiency
- Memory usage should remain under 2GB for 100k file codebases

### Reliability
- Automatic retry on transient failures
- Graceful degradation when AI service is slow or unavailable
- Resume capability for interrupted operations
- Comprehensive error logging and reporting
- Indexed data persists indefinitely to prevent data loss and support historical analysis

### Usability
- Clear progress indicators for long operations
- Helpful error messages with remediation guidance
- Simple configuration through environment files
- Minimal required parameters (just source directory for basic use)

### Maintainability
- Clear separation between discovery, extraction, and indexing phases
- Well-defined data structures for intermediate results
- Comprehensive logging for debugging
- Simple and explicit design suitable for AI-assisted development

### Privacy & Security
- All processing happens locally - no cloud LLM calls
- No code transmitted outside local environment
- Respects source code intellectual property
- Configurable to avoid processing sensitive files
