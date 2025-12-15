# Feature Specification: Maven Dependency Resolution and DTO Analysis

**Feature Branch**: `004-maven-dependency-resolution`
**Created**: 2025-12-15
**Status**: Draft
**Input**: User description: "we need to fix an general issue how we approach file reading we need to use the .env JAVA_SOURCE_DIR as an base directory to find the other files stated in pom.xml like <dependency><groupId>at.a1ta.cuco</groupId><artifactId>cuco-cct-core</artifactId></dependency> which translates to find the missing files for groupId info at JAVA_SOURCE_DIR plus artifactId as base directory to find the files holding the information. so our solution should be JAVA_SOURCE_DIR + researchproject coming from command line value to show main directory which we fetch requirements for. and we need to add the understanding of DTO"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Maven Dependency Discovery and Resolution (Priority: P1)

As a developer analyzing a Java codebase, I need the system to automatically discover and resolve Maven dependencies declared in pom.xml files so that I can analyze not just the main project but also its dependent modules and libraries within the same source tree.

**Why this priority**: Without dependency resolution, the system only analyzes files in the immediate project directory, missing critical code and business logic in dependent modules. This is foundational - all other analysis depends on discovering the complete codebase structure.

**Independent Test**: Can be fully tested by pointing the tool at a multi-module Maven project with dependencies declared in pom.xml, and verifying that files from dependent artifacts (located at JAVA_SOURCE_DIR/artifact-name/) are discovered and included in the analysis inventory.

**Acceptance Scenarios**:

1. **Given** a pom.xml with dependency `<groupId>at.a1ta.cuco</groupId><artifactId>cuco-cct-core</artifactId>`, **When** discovery runs with JAVA_SOURCE_DIR=/path/to/source, **Then** the system finds and scans files in /path/to/source/cuco-cct-core/
2. **Given** multiple dependencies in pom.xml, **When** discovery runs, **Then** all artifacts are resolved relative to JAVA_SOURCE_DIR and their files are included in the analysis
3. **Given** a dependency that doesn't exist in JAVA_SOURCE_DIR, **When** discovery runs, **Then** the system logs a warning but continues processing other dependencies
4. **Given** nested dependencies (dependency A depends on B), **When** discovery runs with depth limit, **Then** the system resolves dependencies up to the configured depth level
5. **Given** a --project parameter specifying a subdirectory, **When** discovery runs, **Then** JAVA_SOURCE_DIR is combined with the project path to form the base directory for dependency resolution

---

### User Story 2 - DTO Pattern Recognition and Analysis (Priority: P2)

As a developer analyzing a Java codebase, I need the system to identify and analyze Data Transfer Objects (DTOs) so that I can understand data structures exchanged between layers, forms, and services.

**Why this priority**: DTOs are critical for understanding system interfaces and data flow, but they're distinct from entities and require special handling. This builds on dependency resolution (P1) by adding semantic understanding of discovered files.

**Independent Test**: Can be tested by running extraction on a project with DTO classes, and verifying that the system correctly identifies them as DTOs (not entities or POJOs), extracts field definitions, detects validation annotations, and documents serialization patterns.

**Acceptance Scenarios**:

1. **Given** a Java class with DTO naming pattern (*DTO.java, *Request.java, *Response.java), **When** extraction runs, **Then** the system classifies it as a DTO artifact type
2. **Given** a DTO with JSR-303 validation annotations (@NotNull, @Size, @Pattern), **When** extraction analyzes the class, **Then** validation rules are documented in the DTO metadata
3. **Given** a DTO implementing Serializable or GWT IsSerializable, **When** extraction runs, **Then** serialization markers are recorded
4. **Given** nested DTOs (DTO contains other DTO fields), **When** extraction runs, **Then** the system captures the nested DTO relationships
5. **Given** DTOs in a .shared package (common in GWT), **When** classification runs, **Then** the system identifies them as shared DTOs accessible by frontend and backend

---

### User Story 3 - Project-Scoped Analysis with Base Directory Configuration (Priority: P3)

As a developer working with multiple projects in a monorepo, I need to specify which project to analyze and have the system correctly resolve paths relative to that project so that I can generate focused documentation for individual modules.

**Why this priority**: Enables targeted analysis of specific projects within a larger codebase. This is an optimization - the system can work without it (analyzing everything), but it improves usability for large codebases.

**Independent Test**: Can be tested by running the tool with --project mysubproject on a monorepo, and verifying that only files within JAVA_SOURCE_DIR/mysubproject and its dependencies are analyzed, with all paths correctly resolved.

**Acceptance Scenarios**:

1. **Given** JAVA_SOURCE_DIR=/workspace and --project cuco-ui-admin, **When** discovery runs, **Then** the base directory is /workspace/cuco-ui-admin and dependencies are resolved from there
2. **Given** a project-specific pom.xml at JAVA_SOURCE_DIR/myproject/pom.xml, **When** discovery runs with --project myproject, **Then** only dependencies declared in that pom.xml are resolved
3. **Given** multiple projects with the same dependency, **When** analyzing project A, **Then** the system uses the dependency version specified in project A's pom.xml
4. **Given** no --project parameter, **When** discovery runs, **Then** JAVA_SOURCE_DIR is used directly as the base directory (existing behavior preserved)
5. **Given** a project parameter pointing to a non-existent directory, **When** discovery runs, **Then** the system reports a clear error indicating the project directory was not found

---

### Edge Cases

- **What happens when a pom.xml dependency references an artifact not present in JAVA_SOURCE_DIR?**
  - System logs a warning with the missing artifact name and groupId/artifactId
  - Continues processing other dependencies
  - Flags the project as having unresolved dependencies in the analysis report

- **How does the system handle circular dependencies in pom.xml files?**
  - Tracks visited artifacts to detect cycles
  - Logs a warning about the circular dependency
  - Stops recursion at the detection point to prevent infinite loops

- **What if JAVA_SOURCE_DIR contains multiple versions of the same artifact?**
  - Uses artifact directory name matching (artifactId from pom.xml)
  - If multiple matches found, uses the first one discovered and logs a warning
  - Considers adding version resolution logic in future enhancement

- **How are transitive dependencies handled?**
  - System resolves direct dependencies from pom.xml by default
  - Supports --dependency-depth parameter to control how many levels deep to resolve
  - Default depth is 1 (direct dependencies only)

- **What if a DTO class doesn't follow standard naming conventions?**
  - Falls back to structural analysis: looks for classes with primarily field declarations, getters/setters, and no business logic
  - Checks for serialization markers (Serializable, IsSerializable)
  - Located in common DTO packages (.dto., .model., .shared., .transfer.)

- **How does the system differentiate between DTOs and Entities?**
  - DTOs: No @Entity annotation, serialization markers, simple field structures, located in .dto or .shared packages
  - Entities: @Entity annotation, JPA/Hibernate annotations, located in .entity or .domain packages
  - When ambiguous, classification favors entity if persistence annotations present, otherwise DTO

## Requirements *(mandatory)*

### Functional Requirements

#### Maven Dependency Resolution (User Story 1)

- **FR-001**: System MUST parse pom.xml files to extract dependency declarations including groupId and artifactId
- **FR-002**: System MUST resolve dependency artifact paths by combining JAVA_SOURCE_DIR with the artifactId value (e.g., JAVA_SOURCE_DIR/cuco-cct-core/ for artifactId=cuco-cct-core)
- **FR-003**: System MUST support a --project CLI parameter that specifies a subdirectory within JAVA_SOURCE_DIR to use as the analysis root
- **FR-004**: System MUST combine JAVA_SOURCE_DIR and --project parameter to form the effective base directory (JAVA_SOURCE_DIR/project-name/)
- **FR-005**: System MUST discover source files within resolved dependency directories and include them in the analysis inventory
- **FR-006**: System MUST support configurable dependency depth via --dependency-depth parameter (default: 1 for direct dependencies only)
- **FR-007**: System MUST detect and prevent circular dependency resolution by tracking visited artifacts
- **FR-008**: System MUST log warnings for dependencies that cannot be resolved (artifact directory not found in JAVA_SOURCE_DIR)
- **FR-009**: System MUST continue processing when individual dependencies fail to resolve, rather than stopping the entire analysis
- **FR-010**: System MUST preserve existing behavior when --project parameter is not specified (use JAVA_SOURCE_DIR directly as base)

#### DTO Pattern Recognition (User Story 2)

- **FR-011**: System MUST identify Java classes as DTOs based on naming patterns: *DTO.java, *Request.java, *Response.java, *Command.java, *Query.java, *Event.java
- **FR-012**: System MUST identify Java classes as DTOs based on structural patterns: primarily field declarations with getters/setters, minimal business logic
- **FR-013**: System MUST extract field definitions from DTO classes including field names, data types, and access modifiers
- **FR-014**: System MUST extract JSR-303 validation annotations from DTO fields including @NotNull, @Size, @Min, @Max, @Pattern, @Email, @Valid
- **FR-015**: System MUST detect serialization markers (implements Serializable, implements IsSerializable, @Serializable annotation)
- **FR-016**: System MUST identify nested DTO relationships when a DTO field is itself a DTO type
- **FR-017**: System MUST differentiate DTOs from JPA entities by checking for entity annotations (@Entity, @Table, @Document)
- **FR-018**: System MUST classify DTOs located in .shared packages as shared DTOs accessible by frontend and backend
- **FR-019**: System MUST extract inner class definitions within DTOs for nested data structures
- **FR-020**: System MUST support DTO identification in packages matching patterns: .dto., .model., .shared., .transfer., .command., .query., .event.

#### Path Resolution and Configuration (User Story 3)

- **FR-021**: System MUST read JAVA_SOURCE_DIR from environment variables (.env file)
- **FR-022**: System MUST accept --project parameter via CLI to specify a project subdirectory
- **FR-023**: System MUST validate that the computed base directory (JAVA_SOURCE_DIR or JAVA_SOURCE_DIR/project) exists
- **FR-024**: System MUST provide clear error messages when the project directory or JAVA_SOURCE_DIR cannot be found
- **FR-025**: System MUST resolve all file paths relative to the effective base directory for consistent artifact tracking
- **FR-026**: System MUST support both absolute and relative path specifications in --project parameter
- **FR-027**: System MUST document the resolved base directory in analysis logs and output metadata

### Key Entities

- **MavenDependency**: Represents a dependency declaration from pom.xml with groupId, artifactId, version (optional), scope, and resolved directory path
- **DtoArtifact**: Represents a Data Transfer Object with fields (name, type, annotations), validation rules, serialization markers, nested DTOs, and package location
- **DependencyGraph**: Represents the dependency resolution tree with parent-child relationships, depth levels, and circular dependency detection
- **ProjectConfiguration**: Represents analysis configuration with JAVA_SOURCE_DIR base path, project subdirectory (optional), dependency depth limit, and resolved base directory

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: System correctly resolves 95% or more of declared Maven dependencies in typical multi-module projects (measured by comparing declared dependencies to successfully resolved artifact directories)
- **SC-002**: DTO classification accuracy of 90% or higher when compared to manual classification by developers (measured on sample codebases with known DTOs)
- **SC-003**: Dependency resolution completes within 10 seconds for projects with up to 20 dependencies
- **SC-004**: Analysis inventory size increases by 50-200% when dependency resolution is enabled, indicating successful discovery of additional code in dependent modules
- **SC-005**: Zero false positives for circular dependency detection (no valid dependency chains incorrectly flagged as circular)
- **SC-006**: Clear and actionable error messages for 100% of configuration errors (missing directories, invalid paths, unresolved dependencies)
- **SC-007**: DTO field extraction completeness of 95% or higher (all fields with their types and validation annotations captured)
- **SC-008**: Developers can analyze a specific project in a monorepo in under 30 seconds using the --project parameter, compared to minutes when analyzing the entire monorepo

## Assumptions

The following assumptions were made to complete this specification:

1. **Dependency Resolution Strategy**: The system assumes artifact directories are named exactly after their artifactId (not groupId-artifactId or other Maven conventions). This matches the user's example where `cuco-cct-core` artifactId maps to `JAVA_SOURCE_DIR/cuco-cct-core/`.

2. **Default Dependency Depth**: Resolving only direct dependencies (depth=1) is sufficient for most use cases. Transitive dependencies can be enabled via --dependency-depth parameter if needed.

3. **DTO Naming Conventions**: Common DTO naming patterns (*DTO, *Request, *Response, *Command, *Query, *Event) cover 90%+ of DTOs in enterprise Java applications. Structural analysis serves as fallback for non-standard names.

4. **Serialization Requirements**: DTOs typically implement Serializable (Java) or IsSerializable (GWT) for remote communication. This is used as a classification signal but not a strict requirement.

5. **Package Structure**: Standard Maven project layout with src/main/java structure is assumed. Custom source directories require explicit configuration.

6. **Error Handling Philosophy**: The system should be resilient - missing dependencies or classification ambiguities should generate warnings but not stop the entire analysis pipeline.

7. **Project Parameter Format**: The --project parameter specifies a relative directory name under JAVA_SOURCE_DIR (e.g., "cuco-ui-admin"), not an absolute path or complex expression.

8. **Version Handling**: When multiple versions of the same artifact exist, the system uses the first match found. Version-aware resolution is deferred to future enhancement if needed.

## Out of Scope

The following are explicitly excluded from this feature:

- **Maven Repository Integration**: The system does NOT download artifacts from Maven Central, private repositories, or resolve dependencies from external sources. It only works with source code present in JAVA_SOURCE_DIR.

- **Version Conflict Resolution**: The system does NOT implement Maven's dependency mediation algorithm or resolve version conflicts. It assumes developers maintain consistent dependency versions in their source tree.

- **Build System Integration**: The system does NOT execute Maven commands, validate pom.xml syntax against Maven schema, or integrate with Maven plugins. It only parses pom.xml as XML to extract dependency information.

- **IDE Integration**: The system does NOT provide IDE plugins, .classpath generation, or integration with IntelliJ IDEA / Eclipse / VS Code for dependency visualization.

- **Gradle Support**: This feature focuses on Maven pom.xml files. Gradle build.gradle files are not supported and require a separate feature specification.

- **Custom DTO Frameworks**: The system uses standard Java and GWT serialization patterns. Custom DTO frameworks (e.g., Avro, Protocol Buffers, custom code generators) require explicit configuration or future enhancement.

- **DTO Transformation Logic**: The system identifies and documents DTOs but does NOT analyze mapping logic between DTOs and entities (e.g., MapStruct, ModelMapper configurations). That belongs to service layer analysis.

## Dependencies

This feature extends:
- **Feature 001 (Java Codebase Indexer)**: Adds Maven dependency resolution to the existing discovery process
- **Feature 002 (PRD Document Generation)**: DTO analysis enhances frontend and service layer documentation

Integration points:
- Discovery service: Extended to parse pom.xml and resolve dependency paths
- Classifier: Enhanced with DTO classification rules
- Extraction service: Extended to extract DTO-specific metadata (validation, serialization)
- Configuration: New CLI parameters (--project, --dependency-depth)
