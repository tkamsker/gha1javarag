# Data Model for GEMINI Code Analysis and PRD Generator

This document defines the data structures used in the pipeline.

## 1. Project

Represents the codebase being analyzed.

- **project_name** (string, required): The unique name of the project.

## 2. DiscoveredFile

Represents a single file discovered in the source code directory.

- **project_name** (string, required): The name of the project this file belongs to.
- **file_path** (string, required): The absolute path to the file.
- **file_type** (string, required): The type of the file (e.g., 'java', 'jsp', 'xml').

## 3. CodeArtifact

Represents a structured piece of information extracted from a file. This is the primary object stored in Weaviate.

- **id** (string, required): A unique identifier for the artifact, following the format `{project_name}:{file_path_from_root}:{symbol_name}`.
- **project_name** (string, required): The name of the project this artifact belongs to.
- **file_path** (string, required): The absolute path to the file this artifact was extracted from.
- **artifact_type** (string, required): The type of the artifact (e.g., 'java_class', 'rest_endpoint', 'jsp_form').
- **language** (string, required): The programming language of the artifact (e.g., 'Java', 'JSP').
- **framework** (string): The framework used, if any (e.g., 'Spring', 'GWT').
- **details** (JSON, required): A flexible JSON object containing type-specific attributes. For example:
  - For a `rest_endpoint`: `{ "http_method": "POST", "url": "/api/users" }`
  - For a `jsp_form`: `{ "fields": ["username", "password"], "action": "/login" }`
  - For a `sql_statement`: `{ "tables": ["users", "orders"], "columns": ["user_id", "order_date"] }`
- **content_for_embedding** (string, required): A text representation of the artifact, used for generating vector embeddings.

## 4. State Transitions

The pipeline follows a linear sequence of stages:

1.  **Discovery**: `DiscoveredFile` objects are created.
2.  **Extraction**: `CodeArtifact` objects are created from `DiscoveredFile` objects.
3.  **Indexing**: `CodeArtifact` objects are transformed and stored in Weaviate.
4.  **Search**: `CodeArtifact` objects are retrieved from Weaviate.
5.  **PRD Generation**: `CodeArtifact` objects are used to generate Markdown documents.
