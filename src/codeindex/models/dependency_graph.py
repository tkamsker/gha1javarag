"""
Dependency graph models for Maven dependency resolution.

Represents the complete dependency tree with resolution statistics.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from .maven_dependency import MavenDependency


@dataclass
class DependencyNode:
    """
    Node in the dependency graph tree.

    Represents a single dependency with its children (transitive dependencies)
    and parent reference for tree navigation.
    """

    dependency: MavenDependency
    children: List['DependencyNode'] = field(default_factory=list)
    parent: Optional['DependencyNode'] = None

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"DependencyNode("
            f"artifact={self.dependency.artifact_id}, "
            f"children={len(self.children)})"
        )

    def add_child(self, child: 'DependencyNode') -> None:
        """Add a child node and set parent reference."""
        child.parent = self
        self.children.append(child)

    def get_depth(self) -> int:
        """Get depth of this node in the tree."""
        return self.dependency.depth

    def is_leaf(self) -> bool:
        """Check if this is a leaf node (no children)."""
        return len(self.children) == 0

    def get_path_from_root(self) -> List[str]:
        """
        Get path from root to this node as list of artifact IDs.

        Returns:
            List of artifact IDs from root to this node
        """
        path = []
        current = self
        while current is not None:
            if current.dependency.depth >= 0:  # Skip synthetic root
                path.insert(0, current.dependency.artifact_id)
            current = current.parent
        return path


@dataclass
class DependencyGraph:
    """
    Complete dependency resolution graph for a project.

    Tracks the entire dependency tree with resolution statistics,
    circular dependency detection, and timing information.
    """

    # Root project information
    project_name: str
    root_pom: Path
    root_node: DependencyNode

    # Resolution statistics
    total_dependencies: int = 0
    resolved_count: int = 0
    not_found_count: int = 0
    circular_count: int = 0
    max_depth: int = 0

    # Error tracking
    resolution_errors: List[str] = field(default_factory=list)
    circular_paths: List[List[str]] = field(default_factory=list)

    # Timing information
    resolution_start: Optional[datetime] = None
    resolution_end: Optional[datetime] = None

    def __post_init__(self):
        """Validate graph after initialization."""
        if self.root_node.dependency.depth != -1 and self.root_node.dependency.depth != 0:
            # Root node should have depth -1 (synthetic) or 0 (actual root project)
            pass  # Allow flexibility

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"DependencyGraph("
            f"project={self.project_name}, "
            f"total={self.total_dependencies}, "
            f"resolved={self.resolved_count}, "
            f"not_found={self.not_found_count}, "
            f"circular={self.circular_count})"
        )

    @property
    def resolution_duration(self) -> Optional[float]:
        """
        Get resolution duration in seconds.

        Returns:
            Duration in seconds, or None if resolution not complete
        """
        if self.resolution_start and self.resolution_end:
            delta = self.resolution_end - self.resolution_start
            return delta.total_seconds()
        return None

    @property
    def success_rate(self) -> float:
        """
        Calculate dependency resolution success rate.

        Returns:
            Percentage of successfully resolved dependencies (0-100)
        """
        if self.total_dependencies == 0:
            return 100.0
        return (self.resolved_count / self.total_dependencies) * 100.0

    def get_all_dependencies(self) -> List[MavenDependency]:
        """
        Flatten dependency tree to list of all dependencies.

        Returns:
            List of all MavenDependency objects in the graph
        """
        dependencies = []
        self._collect_dependencies(self.root_node, dependencies)
        return dependencies

    def _collect_dependencies(
        self,
        node: DependencyNode,
        dependencies: List[MavenDependency]
    ) -> None:
        """Recursively collect dependencies from tree."""
        # Skip synthetic root node
        if node.dependency.depth >= 0:
            dependencies.append(node.dependency)

        for child in node.children:
            self._collect_dependencies(child, dependencies)

    def get_dependencies_at_depth(self, depth: int) -> List[MavenDependency]:
        """
        Get all dependencies at a specific depth level.

        Args:
            depth: Depth level (0=direct, 1=first level transitive, etc.)

        Returns:
            List of dependencies at specified depth
        """
        all_deps = self.get_all_dependencies()
        return [d for d in all_deps if d.depth == depth]

    def get_resolved_dependencies(self) -> List[MavenDependency]:
        """Get list of successfully resolved dependencies."""
        all_deps = self.get_all_dependencies()
        return [d for d in all_deps if d.is_resolved]

    def get_unresolved_dependencies(self) -> List[MavenDependency]:
        """Get list of dependencies that were not found."""
        all_deps = self.get_all_dependencies()
        return [d for d in all_deps if d.is_not_found]

    def get_circular_dependencies(self) -> List[MavenDependency]:
        """Get list of dependencies involved in circular references."""
        all_deps = self.get_all_dependencies()
        return [d for d in all_deps if d.is_circular]

    def find_dependency(self, artifact_id: str) -> Optional[DependencyNode]:
        """
        Find a dependency node by artifact ID.

        Args:
            artifact_id: Maven artifactId to search for

        Returns:
            DependencyNode if found, None otherwise
        """
        return self._find_dependency_recursive(self.root_node, artifact_id)

    def _find_dependency_recursive(
        self,
        node: DependencyNode,
        artifact_id: str
    ) -> Optional[DependencyNode]:
        """Recursively search for dependency node."""
        if node.dependency.artifact_id == artifact_id:
            return node

        for child in node.children:
            result = self._find_dependency_recursive(child, artifact_id)
            if result:
                return result

        return None

    def get_summary(self) -> str:
        """
        Get human-readable summary of dependency resolution.

        Returns:
            Multi-line summary string
        """
        lines = [
            f"Dependency Resolution Summary for '{self.project_name}'",
            f"=" * 60,
            f"Total dependencies: {self.total_dependencies}",
            f"  ✓ Resolved: {self.resolved_count} ({self.success_rate:.1f}%)",
            f"  ✗ Not found: {self.not_found_count}",
            f"  ⟳ Circular: {self.circular_count}",
            f"Maximum depth: {self.max_depth}",
        ]

        if self.resolution_duration:
            lines.append(f"Resolution time: {self.resolution_duration:.2f} seconds")

        if self.circular_paths:
            lines.append(f"\nCircular dependency paths detected:")
            for path in self.circular_paths:
                lines.append(f"  {' → '.join(path)}")

        if self.resolution_errors:
            lines.append(f"\nErrors: {len(self.resolution_errors)}")
            for error in self.resolution_errors[:5]:  # Show first 5
                lines.append(f"  - {error}")

        return "\n".join(lines)
