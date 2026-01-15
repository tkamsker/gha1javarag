"""
Search service for semantic search over Weaviate vector database.

This service wraps the existing weaviate_store.py client to provide
search functionality for the web UI with filtering and result formatting.
"""

import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class SearchService:
    """
    Service for executing semantic searches over Weaviate.

    Features:
    - Natural language semantic search
    - Artifact type and project filtering
    - Result formatting and pagination
    - Error handling for Weaviate unavailability
    """

    def __init__(self):
        """Initialize search service."""
        self.weaviate_client = None  # Will be initialized on first use

    def _get_weaviate_client(self):
        """
        Get or initialize Weaviate client.

        Returns:
            Weaviate client instance
        """
        if self.weaviate_client is None:
            try:
                # Import here to avoid circular dependencies
                from codeindex.services.weaviate_store import WeaviateStore

                self.weaviate_client = WeaviateStore()
                logger.info("Initialized Weaviate client for search service")
            except Exception as e:
                logger.error(f"Failed to initialize Weaviate client: {e}")
                raise

        return self.weaviate_client

    def search(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Execute semantic search over Weaviate.

        Args:
            query: Natural language search query
            filters: Optional filters (artifact_types, project, date_range)
            limit: Maximum number of results (default: 50)
            offset: Result offset for pagination (default: 0)

        Returns:
            Dictionary with search results and metadata
        """
        import time
        start_time = time.time()

        try:
            client = self._get_weaviate_client()

            # Extract filters
            filters = filters or {}
            project_id = filters.get("project")
            artifact_types = filters.get("artifact_types", [])

            logger.info(f"Executing search: query='{query[:50]}...', project={project_id}, types={artifact_types}, limit={limit}")

            # Execute search using WeaviateStore.search_artifacts()
            artifacts = client.search_artifacts(
                query=query,
                project_id=project_id,
                artifact_types=artifact_types,
                limit=limit + offset  # Get more to handle offset
            )

            # Apply pagination offset
            paginated_artifacts = artifacts[offset:offset + limit] if offset > 0 else artifacts[:limit]

            # Calculate execution time
            execution_time_ms = int((time.time() - start_time) * 1000)

            logger.info(f"Search completed: found {len(artifacts)} results in {execution_time_ms}ms")

            return {
                "query": query,
                "total_results": len(artifacts),
                "results": paginated_artifacts,
                "filters_applied": filters,
                "execution_time_ms": execution_time_ms,
                "error": None
            }

        except Exception as e:
            execution_time_ms = int((time.time() - start_time) * 1000)
            logger.error(f"Search failed: {e}", exc_info=True)
            return {
                "query": query,
                "total_results": 0,
                "results": [],
                "filters_applied": filters or {},
                "execution_time_ms": execution_time_ms,
                "error": str(e)
            }

    def get_all_projects(self) -> List[str]:
        """
        Get list of all projects in Weaviate for filter dropdown.

        Returns:
            List of project identifiers
        """
        try:
            client = self._get_weaviate_client()

            # Get statistics which includes all projects
            stats = client.get_statistics()
            projects = stats.get("projects", [])

            # Extract project IDs
            project_ids = [p.get("project_id") for p in projects if p.get("project_id")]

            logger.info(f"Retrieved {len(project_ids)} projects from Weaviate")
            return project_ids

        except Exception as e:
            logger.error(f"Failed to get projects: {e}")
            return []

    def get_artifact_types(self) -> List[str]:
        """
        Get list of all artifact types for filter options.

        Returns:
            List of artifact type names
        """
        # These are defined in the schema
        return [
            "DaoCall",
            "GwtPresenter",
            "GwtView",
            "GwtUiBinder",
            "DtoArtifact",
            "IbatisStatement",
            "DbTable",
            "GwtEndpoint",
            "JspForm",
            "BackendDoc",
            "JsArtifact"
        ]

    def format_search_result(self, raw_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format raw Weaviate result for UI display.

        Args:
            raw_result: Raw result from Weaviate

        Returns:
            Formatted result dictionary
        """
        # TODO: Implement in Phase 3 (US1.1)
        # Extract relevant fields, format confidence scores, create preview snippets

        return {
            "id": raw_result.get("id", ""),
            "artifact_type": raw_result.get("class", ""),
            "file_path": raw_result.get("file_path", ""),
            "confidence": raw_result.get("_additional", {}).get("certainty", 0.0),
            "preview": raw_result.get("description", "")[:200] + "..." if len(raw_result.get("description", "")) > 200 else raw_result.get("description", ""),
            "metadata": {}
        }


# Global service instance
_search_service: Optional[SearchService] = None


def get_search_service() -> SearchService:
    """
    Get global search service instance.

    Returns:
        SearchService singleton
    """
    global _search_service

    if _search_service is None:
        _search_service = SearchService()
        logger.info("Initialized search service")

    return _search_service
