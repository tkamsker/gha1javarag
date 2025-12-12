"""
Indexing service for orchestrating Weaviate indexing operations.

Coordinates loading extraction results and indexing to Weaviate.
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from codeindex.models.extraction import ExtractionResult
from codeindex.models.inventory import DiscoveryInventory
from codeindex.models import ArtifactType, Project
from codeindex.services.weaviate_store import WeaviateStore, create_weaviate_store
from codeindex.utils.config import Config, get_config

logger = logging.getLogger(__name__)


# ==============================================================================
# Indexing Service
# ==============================================================================

class IndexingService:
    """
    Service for orchestrating indexing operations to Weaviate.

    Handles:
    - Loading extraction results from JSONL
    - Loading discovery inventory
    - Indexing projects
    - Indexing code artifacts in batches
    - Progress tracking
    """

    def __init__(
        self,
        config: Optional[Config] = None,
        weaviate_store: Optional[WeaviateStore] = None
    ):
        """
        Initialize indexing service.

        Args:
            config: Configuration instance
            weaviate_store: Optional Weaviate store (for testing)
        """
        self.config = config or get_config()
        self.logger = logging.getLogger(__name__)

        # Initialize Weaviate store
        if weaviate_store:
            self.store = weaviate_store
        else:
            self.store = create_weaviate_store(config=self.config)

    def index_from_files(
        self,
        inventory_path: Path,
        extraction_path: Path,
        batch_size: int = 50
    ) -> Dict[str, Any]:
        """
        Index from discovery inventory and extraction results files.

        Args:
            inventory_path: Path to discovery inventory JSONL
            extraction_path: Path to extraction results JSONL
            batch_size: Batch size for artifact indexing

        Returns:
            Dictionary with indexing statistics
        """
        self.logger.info(f"Indexing from inventory: {inventory_path}")
        self.logger.info(f"Using extraction results: {extraction_path}")

        # Load inventory
        inventory = DiscoveryInventory.load_jsonl(inventory_path)
        self.logger.info(f"Loaded inventory with {len(inventory.projects)} projects")

        # Load extraction results
        extraction_results = self._load_extraction_results(extraction_path)
        self.logger.info(f"Loaded {len(extraction_results)} extraction results")

        # Index projects
        projects_indexed = 0
        for project_dict in inventory.projects:
            try:
                project = self._dict_to_project(project_dict)
                self.store.index_project(project)
                projects_indexed += 1
            except Exception as e:
                self.logger.error(f"Error indexing project {project_dict.get('project_id')}: {e}")

        self.logger.info(f"Indexed {projects_indexed} projects")

        # Index artifacts
        artifacts_stats = self.store.index_artifacts_batch(
            extraction_results,
            project_id=inventory.projects[0].get('project_id') if inventory.projects else "unknown",
            batch_size=batch_size
        )

        return {
            "projects_indexed": projects_indexed,
            "artifacts_indexed": artifacts_stats.get("total_indexed", 0),
            "artifacts_errors": artifacts_stats.get("total_errors", 0),
            "total_files": len(extraction_results)
        }

    def index_extraction_results(
        self,
        extraction_results: List[ExtractionResult],
        project_id: str,
        batch_size: int = 50
    ) -> Dict[str, Any]:
        """
        Index extraction results for a specific project.

        Args:
            extraction_results: List of extraction results
            project_id: Project identifier
            batch_size: Batch size for Weaviate operations

        Returns:
            Dictionary with indexing statistics
        """
        self.logger.info(f"Indexing {len(extraction_results)} artifacts for project {project_id}")

        stats = self.store.index_artifacts_batch(
            extraction_results,
            project_id=project_id,
            batch_size=batch_size
        )

        return stats

    def index_project(self, project: Project) -> str:
        """
        Index a single project.

        Args:
            project: Project information

        Returns:
            UUID of indexed project
        """
        return self.store.index_project(project)

    def _load_extraction_results(self, extraction_path: Path) -> List[ExtractionResult]:
        """
        Load extraction results from JSONL file.

        Args:
            extraction_path: Path to extraction results JSONL

        Returns:
            List of extraction results

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        if not extraction_path.exists():
            raise FileNotFoundError(f"Extraction results not found: {extraction_path}")

        results = []

        with extraction_path.open('r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                try:
                    data = json.loads(line)

                    # Skip metadata line (first line)
                    if 'extraction_timestamp' in data or 'scan_timestamp' in data:
                        continue

                    # Convert to ExtractionResult
                    result = self._dict_to_extraction_result(data)
                    results.append(result)

                except json.JSONDecodeError as e:
                    self.logger.warning(f"Invalid JSON on line {line_num}: {e}")
                except Exception as e:
                    self.logger.error(f"Error loading extraction result on line {line_num}: {e}")

        return results

    def _dict_to_extraction_result(self, data: Dict[str, Any]) -> ExtractionResult:
        """
        Convert dictionary to ExtractionResult.

        Args:
            data: Dictionary with extraction data

        Returns:
            ExtractionResult instance
        """
        # Parse artifact type
        artifact_type_str = data.get('artifact_type')
        if isinstance(artifact_type_str, str):
            try:
                artifact_type = ArtifactType[artifact_type_str]
            except KeyError:
                # Try finding by value
                artifact_type = next(
                    (t for t in ArtifactType if t.value == artifact_type_str),
                    ArtifactType.OTHER_TEXT
                )
        else:
            artifact_type = ArtifactType.OTHER_TEXT

        # Parse datetime
        extracted_at = data.get('extracted_at')
        if isinstance(extracted_at, str):
            try:
                extracted_at = datetime.fromisoformat(extracted_at.replace('Z', '+00:00'))
            except:
                extracted_at = datetime.utcnow()
        else:
            extracted_at = datetime.utcnow()

        return ExtractionResult(
            file_path=data.get('file_path', ''),
            artifact_type=artifact_type,
            structural_data=data.get('structural_data', {}),
            semantic_data=data.get('semantic_data', {}),
            extracted_at=extracted_at,
            summary=data.get('summary'),
            classification=data.get('classification'),
            entities=data.get('entities', []),
            tags=data.get('tags', {}),
            frameworks=data.get('frameworks', []),
            concerns=data.get('concerns', []),
            confidence=data.get('confidence'),
            raw_response=data.get('raw_response'),
            error=data.get('error')
        )

    def _dict_to_project(self, data: Dict[str, Any]) -> Project:
        """
        Convert dictionary to Project.

        Args:
            data: Dictionary with project data

        Returns:
            Project instance
        """
        from uuid import uuid5, NAMESPACE_OID

        # Generate UUID if not present
        project_id = data.get('project_id', '')
        if 'id' not in data:
            data['id'] = uuid5(NAMESPACE_OID, project_id)

        # Use from_dict if available, otherwise construct directly
        return Project.from_dict(data)

    def get_status(self) -> Dict[str, Any]:
        """
        Get indexing status and statistics.

        Returns:
            Dictionary with status information
        """
        project_stats = self.store.get_project_stats()
        artifact_stats = self.store.get_artifact_stats()

        return {
            "weaviate_connected": self.store.health_check(),
            "total_projects": project_stats.get("total_projects", 0),
            "total_artifacts": artifact_stats.get("total_artifacts", 0)
        }


# ==============================================================================
# Convenience Functions
# ==============================================================================

def index_from_files(
    inventory_path: Path,
    extraction_path: Path,
    config: Optional[Config] = None,
    batch_size: int = 50
) -> Dict[str, Any]:
    """
    Index from files (convenience function).

    Args:
        inventory_path: Path to discovery inventory JSONL
        extraction_path: Path to extraction results JSONL
        config: Optional configuration
        batch_size: Batch size for artifact indexing

    Returns:
        Dictionary with indexing statistics
    """
    service = IndexingService(config=config)
    return service.index_from_files(inventory_path, extraction_path, batch_size)
