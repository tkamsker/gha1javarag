"""
Weaviate schema definitions for Java Codebase Indexer Pipeline.

Based on contracts/weaviate-schema.yaml
"""
import logging
import platform
from typing import Optional, Dict, Any
import weaviate

logger = logging.getLogger("codeindex.schemas")


def get_ollama_endpoint_for_weaviate() -> str:
    """
    Get the correct Ollama endpoint for Weaviate container to access host Ollama.

    Platform-specific configuration:
    - macOS: host.docker.internal:11434 (Docker Desktop provides this DNS)
    - Linux: 127.0.0.1:11434 (works with network_mode: host in docker-compose.ubuntu.yml)

    Returns:
        Ollama API endpoint URL for use inside Weaviate container
    """
    system = platform.system().lower()
    if system == "darwin":  # macOS
        return "http://host.docker.internal:11434"
    else:  # Linux and other Unix-like systems
        return "http://127.0.0.1:11434"


# ==============================================================================
# Schema Definitions
# ==============================================================================

def get_project_schema() -> Dict[str, Any]:
    """
    Get Project class schema definition.

    Returns:
        Project class configuration
    """
    return {
        "class": "Project",
        "description": "Maven project with metadata and module structure",
        "vectorizer": "text2vec-ollama",
        "moduleConfig": {
            "text2vec-ollama": {
                "model": "nomic-embed-text",
                "apiEndpoint": get_ollama_endpoint_for_weaviate(),
                "vectorizeClassName": False
            }
        },
        "properties": [
            {
                "name": "projectId",
                "dataType": ["text"],
                "description": "Unique project identifier (groupId:artifactId:version or hash)",
                "indexFilterable": True,
                "indexSearchable": True,
            },
            {
                "name": "name",
                "dataType": ["text"],
                "description": "Project name from Maven artifactId",
                "indexFilterable": True,
                "indexSearchable": True,
            },
            {
                "name": "groupId",
                "dataType": ["text"],
                "description": "Maven groupId",
                "indexFilterable": True,
                "indexSearchable": True,
            },
            {
                "name": "artifactId",
                "dataType": ["text"],
                "description": "Maven artifactId",
                "indexFilterable": True,
                "indexSearchable": True,
            },
            {
                "name": "version",
                "dataType": ["text"],
                "description": "Maven version string",
                "indexFilterable": True,
            },
            {
                "name": "packaging",
                "dataType": ["text"],
                "description": "Maven packaging type (jar, war, pom, ear)",
                "indexFilterable": True,
            },
            {
                "name": "path",
                "dataType": ["text"],
                "description": "Absolute path to project root",
                "indexFilterable": False,
                "indexSearchable": False,
            },
            {
                "name": "modules",
                "dataType": ["text[]"],
                "description": "List of child module names",
                "indexFilterable": True,
            },
            {
                "name": "dependencies",
                "dataType": ["text[]"],
                "description": "Maven dependencies as coordinates",
                "indexFilterable": False,
            },
            {
                "name": "frameworks",
                "dataType": ["text[]"],
                "description": "Detected frameworks (Spring, GWT, etc.)",
                "indexFilterable": True,
            },
            {
                "name": "sourceRoots",
                "dataType": ["text[]"],
                "description": "Source directory paths",
                "indexFilterable": False,
            },
            {
                "name": "testRoots",
                "dataType": ["text[]"],
                "description": "Test directory paths",
                "indexFilterable": False,
            },
            {
                "name": "resourceRoots",
                "dataType": ["text[]"],
                "description": "Resource directory paths",
                "indexFilterable": False,
            },
            {
                "name": "summary",
                "dataType": ["text"],
                "description": "AI-generated project summary (future)",
                "moduleConfig": {
                    "text2vec-ollama": {
                        "skip": False,
                        "vectorizePropertyName": False
                    }
                }
            },
            {
                "name": "indexedAt",
                "dataType": ["date"],
                "description": "Timestamp of last indexing",
                "indexFilterable": True,
            },
            {
                "name": "fileCount",
                "dataType": ["int"],
                "description": "Total files in project",
                "indexFilterable": True,
            },
        ]
    }


def get_code_artifact_schema() -> Dict[str, Any]:
    """
    Get CodeArtifact class schema definition.

    Returns:
        CodeArtifact class configuration
    """
    return {
        "class": "CodeArtifact",
        "description": "File or chunk with AI understanding and metadata",
        "vectorizer": "text2vec-ollama",
        "moduleConfig": {
            "text2vec-ollama": {
                "model": "nomic-embed-text",
                "apiEndpoint": get_ollama_endpoint_for_weaviate(),
                "vectorizeClassName": False
            }
        },
        "properties": [
            {
                "name": "projectId",
                "dataType": ["text"],
                "description": "Foreign key to Project.projectId",
                "indexFilterable": True,
                "indexSearchable": True,
            },
            {
                "name": "relativePath",
                "dataType": ["text"],
                "description": "Path relative to project root",
                "indexFilterable": True,
                "indexSearchable": True,
            },
            {
                "name": "fileName",
                "dataType": ["text"],
                "description": "File name with extension",
                "indexFilterable": True,
                "indexSearchable": True,
            },
            {
                "name": "language",
                "dataType": ["text"],
                "description": "Programming language (Java, JSP, SQL, etc.)",
                "indexFilterable": True,
            },
            {
                "name": "artifactType",
                "dataType": ["text"],
                "description": "Semantic type (java_source, jsp_view, etc.)",
                "indexFilterable": True,
            },
            {
                "name": "frameworks",
                "dataType": ["text[]"],
                "description": "Detected frameworks for this file",
                "indexFilterable": True,
            },
            {
                "name": "summary",
                "dataType": ["text"],
                "description": "AI-generated natural language summary (PRIMARY VECTOR)",
                "moduleConfig": {
                    "text2vec-ollama": {
                        "skip": False,
                        "vectorizePropertyName": False
                    }
                }
            },
            {
                "name": "entities",
                "dataType": ["text[]"],
                "description": "Extracted entities (classes, methods, tables, etc.)",
                "indexFilterable": True,
                "indexSearchable": True,
            },
            {
                "name": "tagsLayer",
                "dataType": ["text[]"],
                "description": "Layer tags (backend, frontend, persistence, etc.)",
                "indexFilterable": True,
            },
            {
                "name": "tagsDomain",
                "dataType": ["text[]"],
                "description": "Domain tags (auth, billing, reporting, etc.)",
                "indexFilterable": True,
            },
            {
                "name": "tagsConcerns",
                "dataType": ["text[]"],
                "description": "Concern tags (security, validation, etc.)",
                "indexFilterable": True,
            },
            {
                "name": "dependencies",
                "dataType": ["text[]"],
                "description": "Referenced dependencies or imports",
                "indexFilterable": False,
            },
            {
                "name": "pomContext",
                "dataType": ["text"],
                "description": "Maven coordinates of containing project",
                "indexFilterable": True,
            },
            {
                "name": "chunkIndex",
                "dataType": ["int"],
                "description": "Chunk number if file was chunked (0-based)",
                "indexFilterable": True,
            },
            {
                "name": "chunkCount",
                "dataType": ["int"],
                "description": "Total chunks for this file",
                "indexFilterable": True,
            },
            {
                "name": "rawTextHash",
                "dataType": ["text"],
                "description": "SHA-256 hash of file content",
                "indexFilterable": True,
            },
            {
                "name": "indexedAt",
                "dataType": ["date"],
                "description": "Timestamp of indexing",
                "indexFilterable": True,
            },
            {
                "name": "confidenceScore",
                "dataType": ["number"],
                "description": "AI confidence in classification (0-1)",
                "indexFilterable": True,
            },
            # GWT-specific metadata fields (FR-001 through FR-015)
            {
                "name": "gwtRole",
                "dataType": ["text"],
                "description": "GWT-specific artifact role: rpc_servlet, presenter, view, ui_binder, shared_dto",
                "indexFilterable": True,
                "indexSearchable": False,
                "moduleConfig": {
                    "text2vec-ollama": {
                        "skip": True
                    }
                }
            },
            {
                "name": "rpcMethods",
                "dataType": ["object[]"],
                "description": "Array of RPC method signatures with parameters, return types, exceptions",
                "indexFilterable": False,
                "indexSearchable": False,
                "nestedProperties": [
                    {
                        "name": "methodName",
                        "dataType": ["text"],
                        "description": "RPC method name"
                    },
                    {
                        "name": "returnType",
                        "dataType": ["text"],
                        "description": "Method return type"
                    },
                    {
                        "name": "parameters",
                        "dataType": ["text[]"],
                        "description": "Method parameters"
                    },
                    {
                        "name": "exceptions",
                        "dataType": ["text[]"],
                        "description": "Declared exceptions"
                    }
                ],
                "moduleConfig": {
                    "text2vec-ollama": {
                        "skip": True
                    }
                }
            },
            {
                "name": "presenterViewBinding",
                "dataType": ["object"],
                "description": "Presenter-view binding metadata with confidence score",
                "indexFilterable": False,
                "indexSearchable": False,
                "nestedProperties": [
                    {
                        "name": "viewName",
                        "dataType": ["text"],
                        "description": "Associated view class name"
                    },
                    {
                        "name": "confidence",
                        "dataType": ["number"],
                        "description": "Binding confidence score (0-1)"
                    },
                    {
                        "name": "bindingType",
                        "dataType": ["text"],
                        "description": "Type of binding (field, constructor, etc.)"
                    }
                ],
                "moduleConfig": {
                    "text2vec-ollama": {
                        "skip": True
                    }
                }
            },
            {
                "name": "uiComponents",
                "dataType": ["object[]"],
                "description": "Array of UI widgets, form fields, and panels from UiBinder",
                "indexFilterable": False,
                "indexSearchable": False,
                "nestedProperties": [
                    {
                        "name": "componentName",
                        "dataType": ["text"],
                        "description": "UI component field name"
                    },
                    {
                        "name": "componentType",
                        "dataType": ["text"],
                        "description": "GWT widget type (Button, TextBox, etc.)"
                    },
                    {
                        "name": "uiBinderField",
                        "dataType": ["boolean"],
                        "description": "Whether this is a UiBinder field"
                    }
                ],
                "moduleConfig": {
                    "text2vec-ollama": {
                        "skip": True
                    }
                }
            },
            {
                "name": "dtoFields",
                "dataType": ["object[]"],
                "description": "Array of DTO field definitions with types and validation rules",
                "indexFilterable": False,
                "indexSearchable": False,
                "nestedProperties": [
                    {
                        "name": "fieldName",
                        "dataType": ["text"],
                        "description": "DTO field name"
                    },
                    {
                        "name": "fieldType",
                        "dataType": ["text"],
                        "description": "Java type of the field"
                    },
                    {
                        "name": "validationAnnotations",
                        "dataType": ["text[]"],
                        "description": "JSR-303 validation annotations"
                    },
                    {
                        "name": "isNested",
                        "dataType": ["boolean"],
                        "description": "Whether this is a nested DTO"
                    }
                ],
                "moduleConfig": {
                    "text2vec-ollama": {
                        "skip": True
                    }
                }
            },
            {
                "name": "gwtFrameworkVersion",
                "dataType": ["text"],
                "description": "Detected GWT version (e.g., '2.8.2')",
                "indexFilterable": True,
                "indexSearchable": False,
                "moduleConfig": {
                    "text2vec-ollama": {
                        "skip": True
                    }
                }
            },
            {
                "name": "referencedDtos",
                "dataType": ["text[]"],
                "description": "List of DTO class names referenced by RPC methods",
                "indexFilterable": True,
                "indexSearchable": False,
                "moduleConfig": {
                    "text2vec-ollama": {
                        "skip": True
                    }
                }
            },
            {
                "name": "eventHandlers",
                "dataType": ["object[]"],
                "description": "Event handler methods in presenters",
                "indexFilterable": False,
                "indexSearchable": False,
                "nestedProperties": [
                    {
                        "name": "handlerName",
                        "dataType": ["text"],
                        "description": "Event handler method name"
                    },
                    {
                        "name": "eventType",
                        "dataType": ["text"],
                        "description": "Type of event being handled"
                    },
                    {
                        "name": "widgetSource",
                        "dataType": ["text"],
                        "description": "UI widget triggering the event"
                    }
                ],
                "moduleConfig": {
                    "text2vec-ollama": {
                        "skip": True
                    }
                }
            },
            {
                "name": "navigationLogic",
                "dataType": ["object[]"],
                "description": "Navigation between presenters",
                "indexFilterable": False,
                "indexSearchable": False,
                "nestedProperties": [
                    {
                        "name": "targetPresenter",
                        "dataType": ["text"],
                        "description": "Target presenter class"
                    },
                    {
                        "name": "navigationMethod",
                        "dataType": ["text"],
                        "description": "Method used for navigation"
                    },
                    {
                        "name": "placeToken",
                        "dataType": ["text"],
                        "description": "GWT Place token for navigation"
                    }
                ],
                "moduleConfig": {
                    "text2vec-ollama": {
                        "skip": True
                    }
                }
            },
            {
                "name": "hasHtmlEntities",
                "dataType": ["boolean"],
                "description": "Whether UiBinder template contains HTML entities",
                "indexFilterable": True,
                "indexSearchable": False,
                "moduleConfig": {
                    "text2vec-ollama": {
                        "skip": True
                    }
                }
            },
        ]
    }


# ==============================================================================
# Schema Management Functions
# ==============================================================================

def create_schema(client: weaviate.Client, skip_if_exists: bool = True) -> bool:
    """
    Create Weaviate schema (Project, CodeArtifact, and DtoArtifact classes).

    Args:
        client: Weaviate client
        skip_if_exists: If True, skip creation if schema already exists

    Returns:
        True if schema was created or already existed

    Raises:
        Exception: If schema creation fails
    """
    # Import here to avoid circular dependency
    from codeindex.schemas.dto_artifact_schema import get_dto_artifact_schema

    try:
        # Get existing schema
        existing_schema = client.schema.get()
        existing_classes = {c["class"] for c in existing_schema.get("classes", [])}

        # Check if classes already exist
        if skip_if_exists:
            required_classes = {"Project", "CodeArtifact", "DtoArtifact"}
            if required_classes.issubset(existing_classes):
                logger.info("Weaviate schema already exists, skipping creation")
                return True

        # Create Project class if not exists
        if "Project" not in existing_classes:
            logger.info("Creating Weaviate class: Project")
            client.schema.create_class(get_project_schema())
        else:
            logger.info("Weaviate class Project already exists")

        # Create CodeArtifact class if not exists
        if "CodeArtifact" not in existing_classes:
            logger.info("Creating Weaviate class: CodeArtifact")
            client.schema.create_class(get_code_artifact_schema())
        else:
            logger.info("Weaviate class CodeArtifact already exists")

        # Create DtoArtifact class if not exists (Feature 004)
        if "DtoArtifact" not in existing_classes:
            logger.info("Creating Weaviate class: DtoArtifact")
            client.schema.create_class(get_dto_artifact_schema())
        else:
            logger.info("Weaviate class DtoArtifact already exists")

        logger.info("Weaviate schema ready")
        return True

    except Exception as e:
        logger.error(f"Failed to create Weaviate schema: {e}")
        raise


def validate_schema(client: weaviate.Client) -> bool:
    """
    Validate that required schema exists.

    Args:
        client: Weaviate client

    Returns:
        True if schema is valid

    Raises:
        ValueError: If schema is missing or invalid
    """
    try:
        schema = client.schema.get()
        existing_classes = {c["class"] for c in schema.get("classes", [])}

        # Check for required classes
        required_classes = {"Project", "CodeArtifact"}
        missing_classes = required_classes - existing_classes

        if missing_classes:
            raise ValueError(
                f"Weaviate schema is missing required classes: {missing_classes}. "
                f"Run indexing with schema creation enabled."
            )

        logger.debug("Weaviate schema validation passed")
        return True

    except Exception as e:
        logger.error(f"Weaviate schema validation failed: {e}")
        raise


def check_weaviate_health(weaviate_url: str, timeout: int = 10) -> bool:
    """
    Check if Weaviate is accessible and healthy.

    Args:
        weaviate_url: Weaviate URL
        timeout: Connection timeout in seconds

    Returns:
        True if Weaviate is healthy

    Raises:
        ConnectionError: If Weaviate is not accessible
    """
    import httpx

    try:
        response = httpx.get(f"{weaviate_url}/v1/meta", timeout=timeout)
        response.raise_for_status()

        meta = response.json()
        logger.info(f"Weaviate is healthy: {meta.get('version', 'unknown version')}")
        return True

    except httpx.ConnectError:
        raise ConnectionError(
            f"Cannot connect to Weaviate at {weaviate_url}. "
            f"Make sure Weaviate is running. "
            f"Try: ./docker-weaviate.sh start"
        )
    except httpx.HTTPStatusError as e:
        raise ConnectionError(
            f"Weaviate returned error: {e.response.status_code}. "
            f"Check Weaviate logs."
        )
    except Exception as e:
        raise ConnectionError(f"Failed to check Weaviate health: {e}")


def delete_schema(client: weaviate.Client, confirm: bool = False) -> bool:
    """
    Delete all Weaviate schema (DANGEROUS - deletes all data).

    Args:
        client: Weaviate client
        confirm: Must be True to actually delete

    Returns:
        True if schema was deleted

    Raises:
        ValueError: If confirm is False
    """
    if not confirm:
        raise ValueError(
            "Schema deletion requires explicit confirmation. "
            "Pass confirm=True to delete all data."
        )

    try:
        logger.warning("Deleting entire Weaviate schema (all data will be lost)")
        client.schema.delete_all()
        logger.info("Weaviate schema deleted")
        return True

    except Exception as e:
        logger.error(f"Failed to delete Weaviate schema: {e}")
        raise
