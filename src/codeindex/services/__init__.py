"""
Service layer for codeindex.

Contains business logic for discovery, extraction, and indexing operations.
"""

from .maven import MavenParser, POMParseError, parse_pom_file
from .classifier import FileClassifier, classify_file, get_artifact_type
from .discovery import (
    DiscoveryService,
    discover_projects,
    scan_directory,
    generate_project_id,
    create_project_from_pom,
)
from .extraction import (
    ExtractionService,
    extract_file,
    extract_from_inventory,
)
from .weaviate_store import (
    WeaviateStore,
    create_weaviate_store,
)
from .indexing import (
    IndexingService,
    index_from_files,
)

__all__ = [
    'MavenParser',
    'POMParseError',
    'parse_pom_file',
    'FileClassifier',
    'classify_file',
    'get_artifact_type',
    'DiscoveryService',
    'discover_projects',
    'scan_directory',
    'generate_project_id',
    'create_project_from_pom',
    'ExtractionService',
    'extract_file',
    'extract_from_inventory',
    'WeaviateStore',
    'create_weaviate_store',
    'IndexingService',
    'index_from_files',
]
