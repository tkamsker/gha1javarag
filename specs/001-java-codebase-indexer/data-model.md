# Data Model: Java Codebase Indexer Pipeline

**Feature**: 001-java-codebase-indexer
**Date**: 2025-12-12
**Phase**: Phase 1 - Data Model Design

## Overview

This document defines the data entities, relationships, and validation rules for the Java Codebase Indexer Pipeline. The model supports the three-phase pipeline (discover → extract → index) with clear boundaries between intermediate and persisted data.

## Entity Hierarchy

```
DiscoveryInventory (intermediate, file-based)
  └─> Project[] (intermediate, then persisted to Weaviate)
        └─> CodeArtifact[] (intermediate, then persisted to Weaviate)
              └─> ExtractionResult (transient, AI output)
```

## Core Entities

### 1. Project

**Purpose**: Represents a Maven project root with its metadata and module structure.

**Lifecycle**: Created during discovery, enriched during extraction, persisted to Weaviate during indexing.

**Storage**: Weaviate class `Project`

**Fields**:

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| id | UUID | Yes | Deterministic ID from groupId:artifactId:version | UUID v5 from coordinates |
| project_id | string | Yes | Human-readable ID (groupId:artifactId:version or path hash) | Max 500 chars |
| name | string | Yes | Project name from POM artifactId | Max 200 chars |
| group_id | string | No | Maven groupId | Max 200 chars |
| artifact_id | string | Yes | Maven artifactId | Max 200 chars |
| version | string | No | Maven version | Semver or SNAPSHOT |
| packaging | string | Yes | Maven packaging type (jar, war, pom) | Enum: jar, war, pom, ear |
| path | string | Yes | Absolute path to project root | Valid directory path |
| modules | string[] | No | List of child module names | Max 1000 modules |
| dependencies | string[] | No | Maven dependencies as groupId:artifactId:version | Max 10000 deps |
| frameworks | string[] | Yes | Detected frameworks (Spring, GWT, iBATIS, etc.) | Controlled vocabulary |
| source_roots | string[] | Yes | Source directories (src/main/java, etc.) | Relative paths |
| test_roots | string[] | No | Test directories | Relative paths |
| resource_roots | string[] | No | Resource directories | Relative paths |
| summary | string | No | AI-generated project summary (future phase) | Max 2000 chars |
| indexed_at | datetime | Yes | Timestamp of last indexing | ISO 8601 |
| file_count | integer | Yes | Total files in project | >= 0 |

**Relationships**:
- Has many `CodeArtifact` (via project_id foreign key)
- Parent-child relationship via modules list (self-referential)

**Indexes**:
- Primary: id (UUID)
- Unique: project_id
- Filter: group_id, artifact_id, version (for version queries)
- Vector: summary (when implemented)

**Validation Rules**:
- If group_id is null, project_id must be path-based hash
- packaging must be one of: jar, war, pom, ear
- indexed_at must be valid ISO 8601 timestamp
- file_count must match actual artifact count

---

### 2. CodeArtifact

**Purpose**: Represents a single file or file chunk with AI-generated understanding and metadata.

**Lifecycle**: Created during extraction, persisted to Weaviate during indexing.

**Storage**: Weaviate class `CodeArtifact`

**Fields**:

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| id | UUID | Yes | Deterministic ID from project_id + path + hash | UUID v5 |
| project_id | string | Yes | Foreign key to Project | Must exist in Project |
| relative_path | string | Yes | Path relative to project root | Max 1000 chars, valid path |
| file_name | string | Yes | File name with extension | Max 255 chars |
| language | string | Yes | Programming language (Java, JSP, SQL, etc.) | Controlled vocabulary |
| artifact_type | string | Yes | Semantic type (java_source, jsp_view, etc.) | See type enum below |
| frameworks | string[] | No | Detected frameworks for this file | Controlled vocabulary |
| summary | string | Yes | AI-generated natural language summary | Max 2000 chars |
| entities | string[] | No | Extracted entities (classes, methods, tables, etc.) | Max 1000 entities |
| tags_layer | string[] | Yes | Layer tags (backend, frontend, persistence, etc.) | See tags enum |
| tags_domain | string[] | No | Domain tags (auth, billing, reporting, etc.) | Max 100 tags |
| tags_concerns | string[] | No | Concern tags (security, validation, etc.) | See tags enum |
| dependencies | string[] | No | Referenced dependencies or imports | Max 500 refs |
| pom_context | string | No | Maven coordinates of containing project | groupId:artifactId:version |
| chunk_index | integer | No | Chunk number if file was chunked | >= 0 |
| chunk_count | integer | No | Total chunks for this file | >= 1 |
| raw_text_hash | string | Yes | SHA-256 hash of file content | 64 hex chars |
| indexed_at | datetime | Yes | Timestamp of indexing | ISO 8601 |
| confidence_score | float | No | AI confidence in classification (0-1) | 0.0 to 1.0 |

**Relationships**:
- Belongs to one `Project` (via project_id)
- Chunks belong to same file (via relative_path + chunk_index)

**Indexes**:
- Primary: id (UUID)
- Foreign key: project_id
- Filter: artifact_type, language, tags_*
- Vector: summary (primary search field)

**Validation Rules**:
- project_id must reference existing Project
- If chunk_index is set, chunk_count must be set and >= chunk_index + 1
- raw_text_hash must be valid SHA-256 (64 hex characters)
- confidence_score if present must be 0.0 to 1.0
- artifact_type must be from allowed enum

---

### 3. DiscoveryInventory (Intermediate)

**Purpose**: Intermediate data structure capturing file system scan results before extraction.

**Lifecycle**: Created during discovery phase, consumed by extraction phase, not persisted to Weaviate.

**Storage**: JSON/JSONL file in output directory

**Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| scan_timestamp | datetime | Yes | When discovery was run |
| root_directory | string | Yes | Scanned directory path |
| projects | Project[] | Yes | Discovered projects (partial data) |
| total_files | integer | Yes | Total files discovered |
| files_by_type | dict[string, integer] | Yes | Count per artifact type |
| scan_duration_seconds | float | Yes | Time taken for discovery |

**Format**: JSONL (one project per line for streaming)

---

### 4. ExtractionResult (Transient)

**Purpose**: Captures AI output for a single file before converting to CodeArtifact.

**Lifecycle**: Created by Ollama client, immediately converted to CodeArtifact, not persisted.

**Storage**: In-memory only

**Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| summary | string | Yes | AI-generated summary |
| classification | string | Yes | AI-refined artifact type |
| entities | string[] | Yes | Extracted entities |
| tags | dict | Yes | Generated tags by category |
| frameworks | string[] | No | Detected frameworks |
| concerns | string[] | No | Detected concerns |
| confidence | float | No | AI confidence score |
| raw_response | string | No | Full Ollama JSON response |

**Conversion**: Maps directly to CodeArtifact fields after validation.

---

## Enumerations and Controlled Vocabularies

### Artifact Types

```python
ARTIFACT_TYPES = [
    "java_source",      # .java files with classes/interfaces
    "java_test",        # Test files (JUnit, TestNG)
    "jsp_view",         # JSP templates
    "html_template",    # Static HTML files
    "gwt_module",       # GWT module XML
    "gwt_ui_binder",    # GWT UiBinder XML
    "js_script",        # JavaScript files
    "sql_schema",       # SQL DDL files
    "sql_query",        # SQL query files
    "orm_mapping",      # Hibernate/JPA mapping XML
    "ibatis_mapping",   # iBATIS/MyBatis mapper XML
    "xml_config",       # Spring/config XML files
    "properties_file",  # .properties files
    "static_asset",     # CSS, images, fonts
    "other_text",       # Other text files
]
```

### Layer Tags

```python
LAYER_TAGS = [
    "backend",          # Server-side business logic
    "frontend",         # UI/presentation layer
    "integration",      # External system integration
    "persistence",      # Data access layer
    "config",           # Configuration files
    "test",             # Test code
]
```

### Concern Tags

```python
CONCERN_TAGS = [
    "security",         # Authentication, authorization, encryption
    "validation",       # Input validation, business rules
    "business_rule",    # Core business logic
    "data_access",      # Database operations
    "ui_flow",          # User interface workflows
    "api_endpoint",     # REST/SOAP endpoints
    "error_handling",   # Exception handling
    "logging",          # Logging and monitoring
]
```

### Framework Tags

```python
FRAMEWORK_TAGS = [
    "GWT",              # Google Web Toolkit
    "Struts",           # Apache Struts
    "Spring",           # Spring Framework
    "Spring MVC",       # Spring MVC
    "iBATIS",           # iBATIS SQL mapper
    "MyBatis",          # MyBatis (iBATIS successor)
    "JDBC",             # JDBC direct access
    "JSP",              # JavaServer Pages
    "Servlet",          # Java Servlets
    "JUnit",            # JUnit testing
    "TestNG",           # TestNG testing
    "Hibernate",        # Hibernate ORM
    "JPA",              # Java Persistence API
]
```

## State Transitions

### Project Lifecycle

```
DISCOVERED → EXTRACTING → INDEXING → INDEXED
                             ↓
                          FAILED (with error state)
```

**States**:
- DISCOVERED: Project found, POM parsed, file list created
- EXTRACTING: AI processing files
- INDEXING: Writing to Weaviate
- INDEXED: Successfully persisted, searchable
- FAILED: Error occurred, see error logs

### CodeArtifact Lifecycle

```
PENDING → EXTRACTING → EXTRACTED → INDEXING → INDEXED
              ↓            ↓
           FAILED      SKIPPED (empty file, binary, etc.)
```

## Data Integrity Rules

### Referential Integrity

1. Every CodeArtifact.project_id MUST reference an existing Project.id
2. Deleting a Project (via reset) MUST cascade delete all its CodeArtifacts
3. Chunk artifacts (same relative_path, different chunk_index) MUST have consistent metadata

### Idempotency Rules

1. Re-indexing same file (same project_id + path + hash) → UPDATE existing artifact
2. Re-indexing same project with changed files → UPDATE changed artifacts, keep unchanged
3. Project ID generation MUST be deterministic: same POM → same project_id

### Validation on Write

1. All required fields must be present
2. Enums must match controlled vocabularies
3. Foreign keys must exist (project_id)
4. Dates must be valid ISO 8601
5. Hashes must be valid hex strings of correct length

## Weaviate-Specific Considerations

### Vectorization Strategy

**Project**:
- Vectorize: summary (when implemented)
- Not vectorized: metadata fields (id, project_id, coordinates, etc.)

**CodeArtifact**:
- Vectorize: summary + tags + entities (concatenated text)
- Not vectorized: structural metadata (paths, hashes, timestamps)

### Batch Operations

- Batch size: 50-100 objects per batch (configurable)
- Use deterministic UUIDs for upsert behavior
- Commit strategy: Batch commit after each batch, not end of run

### Schema Evolution

- Version schema files in contracts/
- Migration strategy: Drop and recreate (data loss acceptable per clarification - indefinite persistence but manual reset OK)
- Schema changes require manual migration or reset

## Performance Optimizations

### Indexing Optimizations

1. **Batch Writes**: Group 50-100 artifacts per Weaviate batch
2. **Parallel Extraction**: Process files concurrently (10 threads default)
3. **Streaming**: Never load all artifacts into memory simultaneously
4. **Incremental Hashing**: Skip unchanged files using raw_text_hash comparison

### Query Optimizations

1. **Project Filtering**: Always filter by project_id when possible
2. **Type Filtering**: Pre-filter by artifact_type before vector search
3. **Hybrid Search**: Combine vector similarity with keyword filters
4. **Limit Results**: Default limit 20, max 100 per query

## Next Steps

1. Define Weaviate schema YAML (contracts/weaviate-schema.yaml)
2. Define CLI interface contract (contracts/cli-interface.md)
3. Create Python dataclasses matching this model
4. Implement validation functions
5. Create quickstart guide
