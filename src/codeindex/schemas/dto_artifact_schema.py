"""
Weaviate schema definition for DtoArtifact class.

Schema for Data Transfer Object (DTO) artifacts extracted from Java source code.
Based on data-model.md specification from Feature 004.
"""

from typing import Dict, Any


def get_dto_artifact_schema() -> Dict[str, Any]:
    """
    Get DtoArtifact class schema definition.

    Schema includes:
    - Basic identification (artifact_id, class_name, package_name, source_path, project)
    - DTO structure (fields as object array with types and annotations)
    - Classification metadata (confidence, signals)
    - Validation rules (JSR-303 annotations per field)
    - Serialization markers (Serializable, IsSerializable)
    - Relationships (nested_dtos, inner_classes, is_shared)
    - Standard fields (language, framework, content_summary)

    Returns:
        DtoArtifact class configuration for Weaviate
    """
    return {
        "class": "DtoArtifact",
        "description": "Data Transfer Object extracted from Java codebase with validation and serialization metadata",
        "vectorizer": "text2vec-ollama",
        "moduleConfig": {
            "text2vec-ollama": {
                "model": "nomic-embed-text",
                "apiEndpoint": "http://host.docker.internal:11434",
                "vectorizeClassName": False,
                "vectorizePropertyName": False,
            }
        },
        "properties": [
            # Identification fields
            {
                "name": "artifact_id",
                "dataType": ["text"],
                "description": "Canonical ID in format project:path:classname",
                "indexFilterable": True,
                "indexSearchable": True,
            },
            {
                "name": "class_name",
                "dataType": ["text"],
                "description": "Simple class name (e.g., UserDTO)",
                "indexFilterable": True,
                "indexSearchable": True,
            },
            {
                "name": "package_name",
                "dataType": ["text"],
                "description": "Fully qualified package name (e.g., com.example.dto)",
                "indexFilterable": True,
                "indexSearchable": True,
            },
            {
                "name": "source_path",
                "dataType": ["text"],
                "description": "Relative path to source file from JAVA_SOURCE_DIR",
                "indexFilterable": False,
                "indexSearchable": False,
            },
            {
                "name": "project",
                "dataType": ["text"],
                "description": "Project name for filtering and multi-project support",
                "indexFilterable": True,
                "indexSearchable": True,
            },

            # DTO structure fields
            {
                "name": "fields",
                "dataType": ["object[]"],
                "description": "Array of field definitions with name, type, modifiers, and validation annotations",
                "nestedProperties": [
                    {
                        "name": "name",
                        "dataType": ["text"],
                        "description": "Field name"
                    },
                    {
                        "name": "field_type",
                        "dataType": ["text"],
                        "description": "Java type (e.g., String, Long, List<UserDTO>)"
                    },
                    {
                        "name": "modifiers",
                        "dataType": ["text[]"],
                        "description": "Field modifiers (private, public, static, final)"
                    },
                    {
                        "name": "is_nested_dto",
                        "dataType": ["boolean"],
                        "description": "True if field type is another DTO"
                    }
                ]
            },

            # Classification metadata
            {
                "name": "classification_confidence",
                "dataType": ["int"],
                "description": "Classification confidence score (0-100)",
                "indexFilterable": True,
            },
            {
                "name": "classification_signals",
                "dataType": ["text[]"],
                "description": "Reasons for DTO classification (naming_pattern, structural_analysis, etc.)",
                "indexFilterable": False,
            },

            # Validation and serialization
            {
                "name": "validation_rules",
                "dataType": ["object"],
                "description": "JSR-303 validation annotations mapped by field name",
            },
            {
                "name": "serialization_markers",
                "dataType": ["text[]"],
                "description": "Serialization interfaces/annotations (Serializable, IsSerializable)",
                "indexFilterable": True,
            },

            # Relationships
            {
                "name": "nested_dtos",
                "dataType": ["text[]"],
                "description": "Class names of nested DTO fields for relationship tracking",
                "indexFilterable": True,
            },
            {
                "name": "inner_classes",
                "dataType": ["text[]"],
                "description": "Inner class names defined within this DTO",
                "indexFilterable": False,
            },
            {
                "name": "is_shared",
                "dataType": ["boolean"],
                "description": "True if located in .shared package (GWT frontend-backend sharing)",
                "indexFilterable": True,
            },

            # Standard fields
            {
                "name": "language",
                "dataType": ["text"],
                "description": "Programming language (always 'java' for this schema)",
                "indexFilterable": True,
            },
            {
                "name": "framework",
                "dataType": ["text"],
                "description": "Detected framework (GWT, Spring, JAX-RS, Jersey)",
                "indexFilterable": True,
            },
            {
                "name": "content_summary",
                "dataType": ["text"],
                "description": "AI-generated summary of DTO purpose and usage",
                "indexSearchable": True,
            },
        ],
    }


def get_dto_artifact_schema_name() -> str:
    """Get the class name for DtoArtifact schema."""
    return "DtoArtifact"


def validate_dto_artifact_schema(schema: Dict[str, Any]) -> bool:
    """
    Validate DtoArtifact schema structure.

    Args:
        schema: Schema dictionary to validate

    Returns:
        True if schema is valid, False otherwise
    """
    required_keys = ["class", "description", "properties"]
    if not all(key in schema for key in required_keys):
        return False

    if schema["class"] != "DtoArtifact":
        return False

    required_properties = {
        "artifact_id", "class_name", "package_name", "source_path", "project",
        "fields", "classification_confidence", "serialization_markers",
        "language"
    }

    property_names = {prop["name"] for prop in schema["properties"]}
    if not required_properties.issubset(property_names):
        return False

    return True
