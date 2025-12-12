"""
CodeArtifact model for Java Codebase Indexer Pipeline.

Represents a single file or file chunk with AI-generated understanding and metadata.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class CodeArtifact:
    """
    Code artifact entity.

    Represents a single file or file chunk with AI-generated semantic understanding,
    classifications, entities, and tags for semantic search.
    """

    # Unique identifiers
    id: UUID  # Deterministic UUID v5 from project_id + path + hash
    project_id: str  # Foreign key to Project.project_id

    # File information
    relative_path: str  # Path relative to project root
    file_name: str  # File name with extension
    language: str  # Programming language (Java, JSP, SQL, etc.)
    artifact_type: str  # Semantic type (java_source, jsp_view, etc.)

    # AI-generated understanding
    summary: str  # Natural language summary (PRIMARY VECTOR for search)
    entities: list[str] = field(default_factory=list)  # Classes, methods, tables, etc.

    # Normalized tags
    tags_layer: list[str] = field(default_factory=list)  # backend, frontend, persistence, etc.
    tags_domain: list[str] = field(default_factory=list)  # auth, billing, reporting, etc.
    tags_concerns: list[str] = field(default_factory=list)  # security, validation, etc.

    # Framework and dependency information
    frameworks: list[str] = field(default_factory=list)  # Detected frameworks for this file
    dependencies: list[str] = field(default_factory=list)  # Referenced dependencies or imports

    # Maven context
    pom_context: Optional[str] = None  # Maven coordinates of containing project

    # Chunking information (for large files)
    chunk_index: Optional[int] = None  # Chunk number if file was chunked (0-based)
    chunk_count: Optional[int] = None  # Total chunks for this file

    # Content integrity
    raw_text_hash: str = ""  # SHA-256 hash of file content

    # Metadata
    indexed_at: Optional[datetime] = None  # Timestamp of indexing
    confidence_score: Optional[float] = None  # AI confidence in classification (0-1)

    def __post_init__(self):
        """Validate fields after initialization."""
        # Ensure required fields are set
        if not self.project_id:
            raise ValueError("project_id is required")
        if not self.relative_path:
            raise ValueError("relative_path is required")
        if not self.file_name:
            raise ValueError("file_name is required")
        if not self.summary:
            raise ValueError("summary is required")

        # Validate chunk information
        if self.chunk_index is not None:
            if self.chunk_count is None:
                raise ValueError("chunk_count must be set if chunk_index is set")
            if self.chunk_index >= self.chunk_count:
                raise ValueError(f"chunk_index ({self.chunk_index}) must be < chunk_count ({self.chunk_count})")
            if self.chunk_index < 0:
                raise ValueError("chunk_index must be >= 0")

        # Validate confidence score
        if self.confidence_score is not None:
            if not (0.0 <= self.confidence_score <= 1.0):
                raise ValueError(f"confidence_score must be between 0.0 and 1.0, got {self.confidence_score}")

    @property
    def is_chunked(self) -> bool:
        """Check if this artifact is part of a chunked file."""
        return self.chunk_index is not None and self.chunk_count is not None

    @property
    def full_path(self) -> str:
        """Get project-relative path (for display)."""
        return self.relative_path

    def to_dict(self) -> dict:
        """
        Convert to dictionary for serialization.

        Returns:
            Dictionary representation
        """
        return {
            "id": str(self.id),
            "project_id": self.project_id,
            "relative_path": self.relative_path,
            "file_name": self.file_name,
            "language": self.language,
            "artifact_type": self.artifact_type,
            "frameworks": self.frameworks,
            "summary": self.summary,
            "entities": self.entities,
            "tags_layer": self.tags_layer,
            "tags_domain": self.tags_domain,
            "tags_concerns": self.tags_concerns,
            "dependencies": self.dependencies,
            "pom_context": self.pom_context,
            "chunk_index": self.chunk_index,
            "chunk_count": self.chunk_count,
            "raw_text_hash": self.raw_text_hash,
            "indexed_at": self.indexed_at.isoformat() if self.indexed_at else None,
            "confidence_score": self.confidence_score,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CodeArtifact":
        """
        Create CodeArtifact from dictionary.

        Args:
            data: Dictionary with artifact data

        Returns:
            CodeArtifact instance
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
