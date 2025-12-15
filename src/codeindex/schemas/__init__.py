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
from .dto_artifact_schema import (
    get_dto_artifact_schema,
    get_dto_artifact_schema_name,
    validate_dto_artifact_schema,
)

__all__ = [
    'get_project_schema',
    'get_code_artifact_schema',
    'get_dto_artifact_schema',
    'get_dto_artifact_schema_name',
    'validate_dto_artifact_schema',
    'create_schema',
    'validate_schema',
    'check_weaviate_health',
    'delete_schema',
]
