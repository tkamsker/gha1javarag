"""
Project model for Java Codebase Indexer Pipeline.

Represents a Maven project with its metadata and module structure.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class Project:
    """
    Maven project entity.

    Represents a Maven project root with coordinates, modules, dependencies,
    and aggregated metadata.
    """

    # Unique identifiers
    id: UUID  # Deterministic UUID v5 from project_id
    project_id: str  # Human-readable ID (groupId:artifactId:version or path hash)

    # Maven coordinates
    name: str  # Project name from artifactId
    artifact_id: str  # Maven artifactId
    group_id: Optional[str] = None  # Maven groupId (None for non-Maven projects)
    version: Optional[str] = None  # Maven version
    packaging: str = "jar"  # Maven packaging type (jar, war, pom, ear)

    # File system
    path: str = ""  # Absolute path to project root

    # Project structure
    modules: list[str] = field(default_factory=list)  # Child module names
    dependencies: list[str] = field(default_factory=list)  # Maven dependencies as coordinates
    frameworks: list[str] = field(default_factory=list)  # Detected frameworks (Spring, GWT, etc.)

    # Source directories
    source_roots: list[str] = field(default_factory=list)  # Source directories (src/main/java, etc.)
    test_roots: list[str] = field(default_factory=list)  # Test directories
    resource_roots: list[str] = field(default_factory=list)  # Resource directories

    # Metadata
    summary: Optional[str] = None  # AI-generated project summary (future)
    indexed_at: Optional[datetime] = None  # Timestamp of last indexing
    file_count: int = 0  # Total files in project

    def __post_init__(self):
        """Validate fields after initialization."""
        # Ensure packaging is valid
        valid_packaging = ["jar", "war", "pom", "ear"]
        if self.packaging not in valid_packaging:
            raise ValueError(f"Invalid packaging: {self.packaging}. Must be one of {valid_packaging}")

        # Ensure project_id is set
        if not self.project_id:
            raise ValueError("project_id is required")

        # Ensure artifact_id is set
        if not self.artifact_id:
            raise ValueError("artifact_id is required")

    @property
    def maven_coordinates(self) -> str:
        """
        Get full Maven coordinates.

        Returns:
            groupId:artifactId:version format, or just artifactId if no groupId
        """
        if self.group_id and self.version:
            return f"{self.group_id}:{self.artifact_id}:{self.version}"
        elif self.group_id:
            return f"{self.group_id}:{self.artifact_id}"
        else:
            return self.artifact_id

    @property
    def is_maven_project(self) -> bool:
        """Check if this is a valid Maven project."""
        return self.group_id is not None

    def to_dict(self) -> dict:
        """
        Convert to dictionary for serialization.

        Returns:
            Dictionary representation
        """
        return {
            "id": str(self.id),
            "project_id": self.project_id,
            "name": self.name,
            "group_id": self.group_id,
            "artifact_id": self.artifact_id,
            "version": self.version,
            "packaging": self.packaging,
            "path": self.path,
            "modules": self.modules,
            "dependencies": self.dependencies,
            "frameworks": self.frameworks,
            "source_roots": self.source_roots,
            "test_roots": self.test_roots,
            "resource_roots": self.resource_roots,
            "summary": self.summary,
            "indexed_at": self.indexed_at.isoformat() if self.indexed_at else None,
            "file_count": self.file_count,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        """
        Create Project from dictionary.

        Args:
            data: Dictionary with project data

        Returns:
            Project instance
        """
        # Convert indexed_at string to datetime if present
        if data.get("indexed_at"):
            if isinstance(data["indexed_at"], str):
                data["indexed_at"] = datetime.fromisoformat(data["indexed_at"])

        # Convert id string to UUID if present
        if data.get("id"):
            if isinstance(data["id"], str):
                data["id"] = UUID(data["id"])

        return cls(**data)
