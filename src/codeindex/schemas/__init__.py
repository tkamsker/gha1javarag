"""
Weaviate schema definitions for Java Codebase Indexer.
"""

from .weaviate import (
    get_project_schema,
    get_code_artifact_schema,
    create_schema,
    validate_schema,
    check_weaviate_health,
    delete_schema,
)

__all__ = [
    'get_project_schema',
    'get_code_artifact_schema',
    'create_schema',
    'validate_schema',
    'check_weaviate_health',
    'delete_schema',
]
