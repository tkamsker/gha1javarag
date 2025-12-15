"""Maven dependency model for pom.xml parsing and resolution."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class MavenDependency:
    """
    Maven dependency declaration from pom.xml.

    Represents a single dependency with resolution state tracking.
    Used by maven_parser to extract dependencies and dependency_resolver
    to track resolution progress.
    """

    # Required fields (from pom.xml)
    group_id: str
    artifact_id: str

    # Optional fields (may be absent in pom.xml)
    version: Optional[str] = None
    scope: str = "compile"

    # Resolution fields (computed during discovery)
    resolved_path: Optional[Path] = None
    resolution_status: str = "pending"

    # Metadata
    declared_in: Optional[Path] = None
    depth: int = 0

    def __post_init__(self):
        """Validate fields after initialization."""
        # Allow empty group_id for synthetic root nodes (depth == -1)
        if self.depth != -1:
            if not self.group_id or not self.artifact_id:
                raise ValueError("group_id and artifact_id are required")

        valid_scopes = {"compile", "test", "provided", "runtime", "system"}
        if self.scope not in valid_scopes:
            raise ValueError(
                f"Invalid scope: {self.scope}. Must be one of: {valid_scopes}"
            )

        valid_statuses = {"pending", "resolved", "not_found", "circular"}
        if self.resolution_status not in valid_statuses:
            raise ValueError(
                f"Invalid resolution_status: {self.resolution_status}. "
                f"Must be one of: {valid_statuses}"
            )

        # Allow depth -1 for synthetic root nodes
        if self.depth < -1:
            raise ValueError(f"Depth must be >= -1, got: {self.depth}")

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"MavenDependency(group_id='{self.group_id}', "
            f"artifact_id='{self.artifact_id}', "
            f"version='{self.version}', "
            f"status='{self.resolution_status}')"
        )

    @property
    def coordinates(self) -> str:
        """Maven coordinates string (groupId:artifactId:version)."""
        if self.version:
            return f"{self.group_id}:{self.artifact_id}:{self.version}"
        return f"{self.group_id}:{self.artifact_id}"

    @property
    def is_resolved(self) -> bool:
        """Check if dependency was successfully resolved."""
        return self.resolution_status == "resolved"

    @property
    def is_circular(self) -> bool:
        """Check if dependency is part of a circular reference."""
        return self.resolution_status == "circular"

    @property
    def is_not_found(self) -> bool:
        """Check if dependency artifact was not found."""
        return self.resolution_status == "not_found"
