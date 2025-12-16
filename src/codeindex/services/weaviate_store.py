"""
Weaviate store service for indexing and searching code artifacts.

Provides high-level operations for storing and retrieving projects and code artifacts.
"""

import logging
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

import weaviate

from codeindex.models import ArtifactType, Project
from codeindex.models.extraction import ExtractionResult
from codeindex.models.dto_artifact import DtoArtifact
from codeindex.schemas import create_schema, validate_schema, check_weaviate_health
from codeindex.utils.config import Config, get_config

logger = logging.getLogger(__name__)


# ==============================================================================
# Weaviate Store Service
# ==============================================================================

class WeaviateStore:
    """
    Service for storing and retrieving code artifacts in Weaviate.

    Handles:
    - Schema creation and validation
    - Project indexing
    - Code artifact indexing
    - Batch operations
    - Search operations
    """

    def __init__(
        self,
        config: Optional[Config] = None,
        auto_create_schema: bool = True
    ):
        """
        Initialize Weaviate store.

        Args:
            config: Configuration instance
            auto_create_schema: Automatically create schema if missing
        """
        self.config = config or get_config()
        self.logger = logging.getLogger(__name__)

        # Initialize Weaviate client
        self.client = self._create_client()

        # Ensure schema exists
        if auto_create_schema:
            create_schema(self.client, skip_if_exists=True)
        else:
            validate_schema(self.client)

    def _create_client(self) -> weaviate.Client:
        """
        Create Weaviate client instance.

        Returns:
            Weaviate client

        Raises:
            ConnectionError: If cannot connect to Weaviate
        """
        # Check health first
        check_weaviate_health(self.config.weaviate_url)

        # Create client using v3 API
        client = weaviate.Client(
            url=self.config.weaviate_url,
            timeout_config=(5, 120)  # (connect, read) timeouts
        )

        self.logger.info(f"Connected to Weaviate at {self.config.weaviate_url}")
        return client

    def health_check(self) -> bool:
        """
        Check if Weaviate is accessible.

        Returns:
            True if Weaviate is healthy
        """
        try:
            check_weaviate_health(self.config.weaviate_url)
            return True
        except Exception as e:
            self.logger.error(f"Weaviate health check failed: {e}")
            return False

    # ==========================================================================
    # Project Operations
    # ==========================================================================

    def index_project(self, project: Project) -> str:
        """
        Index a project to Weaviate.

        Args:
            project: Project information

        Returns:
            UUID of indexed project
        """
        self.logger.info(f"Indexing project: {project.project_id}")

        # Convert to Weaviate format
        project_data = self._project_to_weaviate(project)

        # Check if project already exists
        existing_uuid = self._find_project_by_id(project.project_id)

        if existing_uuid:
            # Update existing project
            self.logger.debug(f"Updating existing project: {existing_uuid}")
            self.client.data_object.update(
                data_object=project_data,
                class_name="Project",
                uuid=existing_uuid
            )
            return existing_uuid
        else:
            # Create new project
            self.logger.debug(f"Creating new project: {project.project_id}")
            uuid = self.client.data_object.create(
                data_object=project_data,
                class_name="Project"
            )
            return uuid

    def _project_to_weaviate(self, project: Project) -> Dict[str, Any]:
        """
        Convert Project to Weaviate data object.

        Args:
            project: Project information

        Returns:
            Weaviate data object
        """
        return {
            "projectId": project.project_id,
            "name": project.name or project.artifact_id,
            "groupId": project.group_id or "",
            "artifactId": project.artifact_id or "",
            "version": project.version or "",
            "packaging": project.packaging or "jar",
            "path": str(project.path),
            "modules": project.modules or [],
            "dependencies": project.dependencies or [],
            "frameworks": project.frameworks or [],
            "sourceRoots": project.source_roots or [],
            "testRoots": project.test_roots or [],
            "resourceRoots": project.resource_roots or [],
            "summary": project.summary or f"Maven project {project.artifact_id}",
            "indexedAt": datetime.utcnow().isoformat() + "Z",
            "fileCount": project.file_count or 0,
        }

    def _find_project_by_id(self, project_id: str) -> Optional[str]:
        """
        Find project UUID by project ID.

        Args:
            project_id: Project identifier

        Returns:
            UUID if found, None otherwise
        """
        try:
            result = (
                self.client.query
                .get("Project", ["projectId"])
                .with_where({
                    "path": ["projectId"],
                    "operator": "Equal",
                    "valueText": project_id
                })
                .with_limit(1)
                .do()
            )

            projects = result.get("data", {}).get("Get", {}).get("Project", [])
            if projects:
                return projects[0].get("_additional", {}).get("id")

            return None

        except Exception as e:
            self.logger.error(f"Error finding project: {e}")
            return None

    def get_project_stats(self) -> Dict[str, Any]:
        """
        Get statistics about indexed projects.

        Returns:
            Dictionary with project statistics
        """
        try:
            result = (
                self.client.query
                .aggregate("Project")
                .with_meta_count()
                .do()
            )

            count = result.get("data", {}).get("Aggregate", {}).get("Project", [{}])[0].get("meta", {}).get("count", 0)

            return {
                "total_projects": count
            }

        except Exception as e:
            self.logger.error(f"Error getting project stats: {e}")
            return {"total_projects": 0}

    # ==========================================================================
    # Code Artifact Operations
    # ==========================================================================

    def index_artifact(
        self,
        extraction_result: ExtractionResult,
        project_id: str
    ) -> str:
        """
        Index a code artifact to Weaviate.

        Args:
            extraction_result: Extraction result
            project_id: Project identifier

        Returns:
            UUID of indexed artifact
        """
        self.logger.debug(f"Indexing artifact: {extraction_result.file_path}")

        # Convert to Weaviate format
        artifact_data = self._artifact_to_weaviate(extraction_result, project_id)

        # Check if artifact already exists (by file path and project)
        existing_uuid = self._find_artifact_by_path(
            project_id,
            artifact_data["relativePath"]
        )

        if existing_uuid:
            # Update existing artifact
            self.logger.debug(f"Updating existing artifact: {existing_uuid}")
            self.client.data_object.update(
                data_object=artifact_data,
                class_name="CodeArtifact",
                uuid=existing_uuid
            )
            return existing_uuid
        else:
            # Create new artifact
            uuid = self.client.data_object.create(
                data_object=artifact_data,
                class_name="CodeArtifact"
            )
            return uuid

    def index_artifacts_batch(
        self,
        extraction_results: List[ExtractionResult],
        project_id: str,
        batch_size: int = 50
    ) -> Dict[str, Any]:
        """
        Index multiple artifacts in batch.

        Args:
            extraction_results: List of extraction results
            project_id: Project identifier
            batch_size: Batch size for Weaviate operations

        Returns:
            Dictionary with indexing statistics
        """
        self.logger.info(f"Indexing {len(extraction_results)} artifacts in batches of {batch_size}")

        total_indexed = 0
        total_errors = 0

        # Configure batch
        self.client.batch.configure(
            batch_size=batch_size,
            dynamic=True,
            timeout_retries=3,
        )

        # Process in batches
        with self.client.batch as batch:
            for result in extraction_results:
                try:
                    artifact_data = self._artifact_to_weaviate(result, project_id)

                    batch.add_data_object(
                        data_object=artifact_data,
                        class_name="CodeArtifact"
                    )

                    total_indexed += 1

                except Exception as e:
                    self.logger.error(f"Error indexing {result.file_path}: {e}")
                    total_errors += 1

        self.logger.info(f"Batch indexing complete: {total_indexed} indexed, {total_errors} errors")

        return {
            "total_indexed": total_indexed,
            "total_errors": total_errors
        }

    def _artifact_to_weaviate(
        self,
        extraction_result: ExtractionResult,
        project_id: str
    ) -> Dict[str, Any]:
        """
        Convert ExtractionResult to Weaviate data object.

        Args:
            extraction_result: Extraction result
            project_id: Project identifier

        Returns:
            Weaviate data object
        """
        file_path = Path(extraction_result.file_path)

        # Extract semantic data
        semantic = extraction_result.semantic_data or {}

        # Get artifact type string
        artifact_type_str = (
            extraction_result.artifact_type.value
            if hasattr(extraction_result.artifact_type, 'value')
            else str(extraction_result.artifact_type)
        )

        # Compute file hash
        file_hash = self._compute_file_hash(file_path)

        return {
            "projectId": project_id,
            "relativePath": str(file_path),  # Using full path for now
            "fileName": file_path.name,
            "language": semantic.get("language", artifact_type_str),
            "artifactType": artifact_type_str,
            "frameworks": semantic.get("frameworks", []),
            "summary": semantic.get("summary", f"{artifact_type_str}: {file_path.name}"),
            "entities": semantic.get("entities", []),
            "tagsLayer": semantic.get("tags", []),  # Map generic tags to layer
            "tagsDomain": [],
            "tagsConcerns": semantic.get("concerns", []),
            "dependencies": semantic.get("dependencies", []),
            "pomContext": project_id,
            "chunkIndex": 0,  # No chunking for now
            "chunkCount": 1,
            "rawTextHash": file_hash,
            "indexedAt": datetime.utcnow().isoformat() + "Z",
            "confidenceScore": extraction_result.confidence or 1.0,
        }

    def _compute_file_hash(self, file_path: Path) -> str:
        """
        Compute SHA-256 hash of file content.

        Args:
            file_path: Path to file

        Returns:
            Hex digest of file hash
        """
        try:
            if file_path.exists():
                content = file_path.read_bytes()
                return hashlib.sha256(content).hexdigest()
            return ""
        except Exception as e:
            self.logger.warning(f"Error hashing file {file_path}: {e}")
            return ""

    def _find_artifact_by_path(
        self,
        project_id: str,
        relative_path: str
    ) -> Optional[str]:
        """
        Find artifact UUID by project and path.

        Args:
            project_id: Project identifier
            relative_path: Relative file path

        Returns:
            UUID if found, None otherwise
        """
        try:
            result = (
                self.client.query
                .get("CodeArtifact", ["projectId", "relativePath"])
                .with_where({
                    "operator": "And",
                    "operands": [
                        {
                            "path": ["projectId"],
                            "operator": "Equal",
                            "valueText": project_id
                        },
                        {
                            "path": ["relativePath"],
                            "operator": "Equal",
                            "valueText": relative_path
                        }
                    ]
                })
                .with_limit(1)
                .do()
            )

            artifacts = result.get("data", {}).get("Get", {}).get("CodeArtifact", [])
            if artifacts:
                return artifacts[0].get("_additional", {}).get("id")

            return None

        except Exception as e:
            self.logger.error(f"Error finding artifact: {e}")
            return None

    def get_artifact_stats(self) -> Dict[str, Any]:
        """
        Get statistics about indexed artifacts.

        Returns:
            Dictionary with artifact statistics
        """
        try:
            result = (
                self.client.query
                .aggregate("CodeArtifact")
                .with_meta_count()
                .with_group_by_filter(["artifactType"])
                .do()
            )

            total = result.get("data", {}).get("Aggregate", {}).get("CodeArtifact", [{}])[0].get("meta", {}).get("count", 0)

            return {
                "total_artifacts": total
            }

        except Exception as e:
            self.logger.error(f"Error getting artifact stats: {e}")
            return {"total_artifacts": 0}

    # ==========================================================================
    # Search Operations
    # ==========================================================================

    def search_artifacts(
        self,
        query: str,
        project_id: Optional[str] = None,
        artifact_types: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for code artifacts using semantic search.

        Args:
            query: Search query
            project_id: Optional project filter
            artifact_types: Optional artifact type filters
            limit: Maximum results

        Returns:
            List of matching artifacts with metadata
        """
        self.logger.info(f"Searching artifacts: '{query}' (limit={limit})")

        try:
            # Build query
            query_builder = (
                self.client.query
                .get("CodeArtifact", [
                    "projectId",
                    "relativePath",
                    "fileName",
                    "artifactType",
                    "summary",
                    "entities",
                    "frameworks"
                ])
                .with_near_text({"concepts": [query]})
                .with_limit(limit)
                .with_additional(["distance", "id"])
            )

            # Add filters
            filters = []
            if project_id:
                filters.append({
                    "path": ["projectId"],
                    "operator": "Equal",
                    "valueText": project_id
                })

            if artifact_types:
                for artifact_type in artifact_types:
                    filters.append({
                        "path": ["artifactType"],
                        "operator": "Equal",
                        "valueText": artifact_type
                    })

            if filters:
                if len(filters) == 1:
                    query_builder = query_builder.with_where(filters[0])
                else:
                    query_builder = query_builder.with_where({
                        "operator": "And",
                        "operands": filters
                    })

            # Execute query
            result = query_builder.do()

            artifacts = result.get("data", {}).get("Get", {}).get("CodeArtifact", []) if result else []
            self.logger.info(f"Found {len(artifacts) if artifacts else 0} matching artifacts")

            return artifacts or []

        except Exception as e:
            self.logger.error(f"Search error: {e}", exc_info=True)
            return []

    def get_gwt_artifacts(
        self,
        project_id: Optional[str] = None,
        gwt_roles: Optional[List[str]] = None,
        limit: int = 1000
    ) -> List[Dict[str, Any]]:
        """
        Query GWT artifacts by role.

        Args:
            project_id: Optional project filter
            gwt_roles: List of GWT roles to filter (presenter, view, ui_binder, rpc_servlet, shared_dto)
            limit: Maximum results (default: 1000)

        Returns:
            List of GWT artifacts with full metadata
        """
        self.logger.info(f"Querying GWT artifacts (roles={gwt_roles}, project={project_id})")

        try:
            # Build query with all relevant fields
            query_builder = (
                self.client.query
                .get("CodeArtifact", [
                    "projectId",
                    "relativePath",
                    "fileName",
                    "artifactType",
                    "language",
                    "summary",
                    "entities",
                    "frameworks",
                    "tags",
                    "gwtRole",
                    "gwtPresenterName",
                    "gwtViewBinding",
                    "gwtEventHandlers",
                    "gwtNavigationLogic",
                    "gwtRpcCalls",
                    "gwtViewName",
                    "gwtComponentType",
                    "gwtUiFields",
                    "gwtTemplateName",
                    "gwtFormFields",
                    "gwtServiceClass",
                    "gwtRpcMethods",
                    "gwtDtoFields",
                ])
                .with_limit(limit)
            )

            # Build filters
            filters = []

            # Filter by project
            if project_id:
                filters.append({
                    "path": ["projectId"],
                    "operator": "Equal",
                    "valueText": project_id
                })

            # Filter by GWT roles
            if gwt_roles:
                role_filters = []
                for role in gwt_roles:
                    role_filters.append({
                        "path": ["gwtRole"],
                        "operator": "Equal",
                        "valueText": role
                    })

                if len(role_filters) == 1:
                    filters.append(role_filters[0])
                else:
                    filters.append({
                        "operator": "Or",
                        "operands": role_filters
                    })

            # Apply filters
            if filters:
                if len(filters) == 1:
                    query_builder = query_builder.with_where(filters[0])
                else:
                    query_builder = query_builder.with_where({
                        "operator": "And",
                        "operands": filters
                    })

            # Execute query
            result = query_builder.do()

            artifacts = result.get("data", {}).get("Get", {}).get("CodeArtifact", []) if result else []
            self.logger.info(f"Found {len(artifacts) if artifacts else 0} GWT artifacts")

            return artifacts or []

        except Exception as e:
            self.logger.error(f"GWT artifacts query error: {e}", exc_info=True)
            return []

    # ==========================================================================
    # Utility Operations
    # ==========================================================================

    def delete_project(self, project_id: str) -> bool:
        """
        Delete a project and all its artifacts.

        Args:
            project_id: Project identifier

        Returns:
            True if deleted successfully
        """
        self.logger.warning(f"Deleting project: {project_id}")

        try:
            # Delete all artifacts for this project
            self.client.batch.delete_objects(
                class_name="CodeArtifact",
                where={
                    "path": ["projectId"],
                    "operator": "Equal",
                    "valueText": project_id
                }
            )

            # Delete project
            project_uuid = self._find_project_by_id(project_id)
            if project_uuid:
                self.client.data_object.delete(
                    uuid=project_uuid,
                    class_name="Project"
                )

            self.logger.info(f"Deleted project: {project_id}")
            return True

        except Exception as e:
            self.logger.error(f"Error deleting project: {e}")
            return False

    # ==========================================================================
    # DTO Artifact Operations (T064)
    # ==========================================================================

    def index_dto(
        self,
        dto_artifact: DtoArtifact,
        project: Optional[str] = None
    ) -> str:
        """
        Index a DtoArtifact to Weaviate.

        Args:
            dto_artifact: DtoArtifact to index
            project: Optional project name (overrides dto_artifact.project)

        Returns:
            Artifact ID of indexed DTO

        Raises:
            Exception: If indexing fails
        """
        try:
            # Use project from parameter or dto_artifact
            project_name = project or dto_artifact.project or "unknown"

            # Check if DTO already exists (idempotent indexing)
            existing = self._find_dto_by_artifact_id(dto_artifact.artifact_id)
            if existing:
                self.logger.debug(f"Deleting existing DTO: {dto_artifact.artifact_id}")
                self.client.data_object.delete(existing, class_name="DtoArtifact")

            # Convert DtoArtifact to Weaviate data object
            import json

            data_object = {
                "artifact_id": dto_artifact.artifact_id,
                "class_name": dto_artifact.class_name,
                "package_name": dto_artifact.package_name or "",
                "source_path": str(dto_artifact.source_file) if dto_artifact.source_file else "",
                "project": project_name,
                "is_dto": dto_artifact.is_dto,
                "fields": [
                    {k: v for k, v in f.to_dict().items()
                     if k in ['name', 'field_type', 'modifiers', 'is_nested_dto']}
                    for f in dto_artifact.fields
                ],
                "classification_confidence": int(dto_artifact.confidence),
                "classification_signals": self._extract_classification_signals(dto_artifact),
                "validation_rules": json.dumps(dto_artifact.validation_rules),
                "serialization_markers": dto_artifact.serialization_markers,
                "nested_dtos": dto_artifact.nested_dto_types,
                "inner_classes": [],  # TODO: Extract from metadata if available
                "is_shared": ".shared." in (dto_artifact.package_name or ""),
                "language": dto_artifact.language,
                "framework": dto_artifact.framework_hints[0] if dto_artifact.framework_hints else "",
                "content_summary": f"DTO class {dto_artifact.class_name} with {len(dto_artifact.fields)} fields"
            }

            # Create the object in Weaviate
            result = self.client.data_object.create(
                data_object=data_object,
                class_name="DtoArtifact"
            )

            self.logger.info(f"Indexed DTO: {dto_artifact.class_name} (Weaviate UUID: {result}, artifact_id: {dto_artifact.artifact_id})")
            return dto_artifact.artifact_id

        except Exception as e:
            self.logger.error(f"Error indexing DTO {dto_artifact.class_name}: {e}", exc_info=True)
            raise

    def get_dto_by_id(self, artifact_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a DTO artifact by its ID.

        Args:
            artifact_id: Artifact ID to retrieve

        Returns:
            Dictionary with DTO data, or None if not found
        """
        try:
            self.logger.debug(f"Querying DTO by artifact_id: {artifact_id}")

            result = (
                self.client.query
                .get("DtoArtifact", [
                    "artifact_id",
                    "class_name",
                    "package_name",
                    "source_path",
                    "project",
                    "is_dto",
                    "fields { name field_type modifiers is_nested_dto }",
                    "classification_confidence",
                    "validation_rules",
                    "serialization_markers",
                    "nested_dtos",
                    "language",
                    "framework"
                ])
                .with_where({
                    "path": ["artifact_id"],
                    "operator": "Equal",
                    "valueText": artifact_id
                })
                .with_limit(1)
                .do()
            )

            self.logger.debug(f"Query result: {result}")
            dtos = result.get("data", {}).get("Get", {}).get("DtoArtifact", [])
            self.logger.debug(f"Found {len(dtos)} DTOs")

            # Add alias for backward compatibility
            if dtos:
                dto = dtos[0]
                dto['nested_dto_types'] = dto.get('nested_dtos', [])
                return dto

            return None

        except Exception as e:
            self.logger.error(f"Error retrieving DTO {artifact_id}: {e}", exc_info=True)
            return None

    def search_dtos(
        self,
        query: str,
        project: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for DTOs using semantic search.

        Args:
            query: Search query
            project: Optional project filter
            limit: Maximum number of results

        Returns:
            List of matching DTO artifacts
        """
        try:
            query_builder = (
                self.client.query
                .get("DtoArtifact", [
                    "artifact_id",
                    "class_name",
                    "package_name",
                    "source_path",
                    "project",
                    "fields { name field_type modifiers is_nested_dto }",
                    "classification_confidence",
                    "validation_rules",
                    "serialization_markers",
                    "nested_dtos"
                ])
                .with_near_text({"concepts": [query]})
                .with_limit(limit)
            )

            # Add project filter if specified
            if project:
                query_builder = query_builder.with_where({
                    "path": ["project"],
                    "operator": "Equal",
                    "valueText": project
                })

            result = query_builder.do()
            dtos = result.get("data", {}).get("Get", {}).get("DtoArtifact", [])

            # Add alias for backward compatibility
            for dto in dtos:
                dto['nested_dto_types'] = dto.get('nested_dtos', [])

            self.logger.debug(f"DTO search returned {len(dtos)} results")
            return dtos

        except Exception as e:
            self.logger.error(f"Error searching DTOs: {e}", exc_info=True)
            return []

    def _find_dto_by_artifact_id(self, artifact_id: str) -> Optional[str]:
        """
        Find Weaviate UUID by artifact_id.

        Args:
            artifact_id: Artifact ID to search for

        Returns:
            Weaviate UUID if found, None otherwise
        """
        try:
            result = (
                self.client.query
                .get("DtoArtifact", ["artifact_id"])
                .with_additional(["id"])
                .with_where({
                    "path": ["artifact_id"],
                    "operator": "Equal",
                    "valueText": artifact_id
                })
                .with_limit(1)
                .do()
            )

            dtos = result.get("data", {}).get("Get", {}).get("DtoArtifact", [])
            if dtos:
                return dtos[0].get("_additional", {}).get("id")
            return None

        except Exception as e:
            self.logger.warning(f"Error finding DTO by artifact_id {artifact_id}: {e}")
            return None

    def _extract_classification_signals(self, dto_artifact: DtoArtifact) -> List[str]:
        """
        Extract classification signals from DtoArtifact for indexing.

        Args:
            dto_artifact: DtoArtifact with classification result

        Returns:
            List of classification signals
        """
        signals = []

        if dto_artifact.classification_result:
            result = dto_artifact.classification_result

            if result.naming_pattern_score > 0:
                signals.append("naming_pattern")
            if result.structural_score > 0:
                signals.append("structural_analysis")
            if result.serialization_markers_found:
                signals.append("serialization_markers")
            if result.package_score > 0:
                signals.append("package_location")
            if result.nested_dtos_found:
                signals.append("nested_dtos")

        return signals

    # ==========================================================================
    # Statistics Operations
    # ==========================================================================

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics for status command.

        Returns:
            Dictionary containing:
                - project_count: Total number of projects
                - artifact_count: Total number of artifacts
                - projects: List of project stats with details
        """
        try:
            # Get all projects
            projects_result = (
                self.client.query
                .get("Project", ["projectId", "name", "indexedAt", "fileCount"])
                .do()
            )

            projects_list = projects_result.get("data", {}).get("Get", {}).get("Project", [])

            # Get statistics for each project
            project_stats = []
            total_artifacts = 0

            for project in projects_list:
                project_id = project.get("projectId")

                # Get artifact count for this project
                artifact_count = self.count_artifacts(project_id)
                total_artifacts += artifact_count

                # Get type breakdown
                type_breakdown = self.get_artifact_type_breakdown(project_id)

                project_stats.append({
                    "project_id": project_id,
                    "name": project.get("name", "Unknown"),
                    "artifact_count": artifact_count,
                    "type_breakdown": type_breakdown,
                    "last_indexed": project.get("indexedAt"),
                    "file_count": project.get("fileCount", 0)
                })

            return {
                "project_count": len(projects_list),
                "artifact_count": total_artifacts,
                "projects": project_stats
            }

        except Exception as e:
            self.logger.error(f"Error getting statistics: {e}")
            return {
                "project_count": 0,
                "artifact_count": 0,
                "projects": []
            }

    def get_project_statistics(self, project_id: str) -> Dict[str, Any]:
        """
        Get statistics for a specific project.

        Args:
            project_id: Project identifier

        Returns:
            Dictionary with project-specific statistics
        """
        try:
            # Get project details
            project_result = (
                self.client.query
                .get("Project", ["projectId", "name", "indexedAt", "fileCount"])
                .with_where({
                    "path": ["projectId"],
                    "operator": "Equal",
                    "valueText": project_id
                })
                .do()
            )

            projects = project_result.get("data", {}).get("Get", {}).get("Project", [])

            if not projects:
                return {
                    "project_id": project_id,
                    "found": False
                }

            project = projects[0]

            # Get artifact count
            artifact_count = self.count_artifacts(project_id)

            # Get type breakdown
            type_breakdown = self.get_artifact_type_breakdown(project_id)

            return {
                "project_id": project_id,
                "name": project.get("name", "Unknown"),
                "found": True,
                "artifact_count": artifact_count,
                "type_breakdown": type_breakdown,
                "last_indexed": project.get("indexedAt"),
                "file_count": project.get("fileCount", 0)
            }

        except Exception as e:
            self.logger.error(f"Error getting project statistics for {project_id}: {e}")
            return {
                "project_id": project_id,
                "found": False,
                "error": str(e)
            }

    def count_artifacts(self, project_id: Optional[str] = None) -> int:
        """
        Count artifacts, optionally filtered by project.

        Args:
            project_id: Optional project filter

        Returns:
            Number of artifacts
        """
        try:
            query = self.client.query.aggregate("CodeArtifact").with_meta_count()

            if project_id:
                query = query.with_where({
                    "path": ["projectId"],
                    "operator": "Equal",
                    "valueText": project_id
                })

            result = query.do()

            count = result.get("data", {}).get("Aggregate", {}).get("CodeArtifact", [{}])[0].get("meta", {}).get("count", 0)
            return count

        except Exception as e:
            self.logger.error(f"Error counting artifacts: {e}")
            return 0

    def get_artifact_type_breakdown(self, project_id: Optional[str] = None) -> Dict[str, int]:
        """
        Get breakdown of artifacts by type.

        Args:
            project_id: Optional project filter

        Returns:
            Dictionary mapping artifact types to counts
        """
        try:
            # Get all artifacts with types
            query = (
                self.client.query
                .get("CodeArtifact", ["artifactType", "projectId"])
            )

            if project_id:
                query = query.with_where({
                    "path": ["projectId"],
                    "operator": "Equal",
                    "valueText": project_id
                })

            result = query.with_limit(10000).do()  # High limit to get all

            artifacts = result.get("data", {}).get("Get", {}).get("CodeArtifact", [])

            # Count by type
            type_counts = {}
            for artifact in artifacts:
                artifact_type = artifact.get("artifactType", "unknown")
                type_counts[artifact_type] = type_counts.get(artifact_type, 0) + 1

            return type_counts

        except Exception as e:
            self.logger.error(f"Error getting artifact type breakdown: {e}")
            return {}

    def close(self):
        """Close Weaviate client connection."""
        # Weaviate client doesn't need explicit closing in v3
        pass


# ==============================================================================
# Convenience Functions
# ==============================================================================

def create_weaviate_store(
    config: Optional[Config] = None,
    auto_create_schema: bool = True
) -> WeaviateStore:
    """
    Create Weaviate store instance (convenience function).

    Args:
        config: Configuration instance
        auto_create_schema: Automatically create schema if missing

    Returns:
        Weaviate store instance
    """
    return WeaviateStore(config=config, auto_create_schema=auto_create_schema)
