"""
Dependency resolver service for Maven projects.

Recursively resolves Maven dependencies with circular detection.
Implements FR-007: Circular dependency detection with visited artifact tracking.
"""

from pathlib import Path
from typing import Set, List, Optional
from datetime import datetime
import logging

from ..models.maven_dependency import MavenDependency
from ..models.dependency_graph import DependencyGraph, DependencyNode
from .maven_parser import parse_pom
from ..utils.path_resolver import resolve_artifact_path, resolve_artifact_path_with_siblings

log = logging.getLogger(__name__)


def resolve_dependencies(
    root_pom: Path,
    base_dir: Path,
    max_depth: int = 1,
    project_name: Optional[str] = None,
    workspace_root: Optional[Path] = None,
    search_siblings: bool = True
) -> DependencyGraph:
    """
    Resolve dependency graph with circular detection.

    Implements FR-002, FR-006, FR-007: Resolve dependencies recursively up to
    max_depth with circular dependency detection.

    Algorithm:
    1. Parse root pom.xml to get direct dependencies
    2. For each dependency:
       a. Check if already visited (circular detection)
       b. Resolve artifact path using multi-level search:
          - First: base_dir / artifact_id (monorepo pattern)
          - Then: workspace_root / artifact_id (sibling pattern)
          - Finally: parent levels (multi-level pattern)
       c. Update resolution_status (resolved, not_found, circular)
       d. If resolved and depth < max_depth, recurse into dependency's pom.xml
    3. Return DependencyGraph with complete tree

    Args:
        root_pom: Path to root pom.xml
        base_dir: Base directory for artifact resolution (project directory)
        max_depth: Maximum dependency depth to resolve (default: 1)
        project_name: Project name for graph metadata
        workspace_root: Workspace root directory for sibling search (default: None, auto-detect)
        search_siblings: Enable sibling directory search (default: True)

    Returns:
        Complete dependency graph with statistics

    Raises:
        FileNotFoundError: If root pom.xml doesn't exist

    Example:
        >>> from pathlib import Path
        >>> graph = resolve_dependencies(
        ...     root_pom=Path("/workspace/cuco-ui-admin/pom.xml"),
        ...     base_dir=Path("/workspace/cuco-ui-admin"),
        ...     max_depth=1,
        ...     project_name="cuco-ui-admin",
        ...     workspace_root=Path("/workspace"),
        ...     search_siblings=True
        ... )
        >>> print(f"Resolved {graph.resolved_count} dependencies")
        Resolved 14 dependencies
    """
    if not root_pom.exists():
        raise FileNotFoundError(f"Root pom.xml not found: {root_pom}")

    # Auto-detect workspace root if not provided (use parent of base_dir)
    if workspace_root is None and search_siblings:
        workspace_root = base_dir.parent
        log.debug(f"Auto-detected workspace root: {workspace_root}")

    # Initialize timing
    start_time = datetime.now()

    # Track visited artifacts for circular detection
    visited: Set[str] = set()
    circular_paths: List[List[str]] = []
    resolution_errors: List[str] = []

    # Parse root pom to get direct dependencies
    try:
        root_dependencies = parse_pom(root_pom, depth=0)
    except Exception as e:
        log.error(f"Failed to parse root pom.xml: {e}")
        resolution_errors.append(f"Root POM parse error: {e}")
        # Return empty graph on root parse failure
        return _create_empty_graph(
            project_name or "unknown",
            root_pom,
            start_time,
            resolution_errors
        )

    # Create synthetic root node
    root_node = DependencyNode(
        dependency=MavenDependency(
            group_id="",
            artifact_id=project_name or "root",
            depth=-1  # Synthetic root
        ),
        children=[]
    )

    # Resolve each direct dependency
    for dep in root_dependencies:
        child_node = _resolve_dependency_recursive(
            dependency=dep,
            base_dir=base_dir,
            max_depth=max_depth,
            visited=visited.copy(),  # Copy for each branch
            path=[],
            circular_paths=circular_paths,
            resolution_errors=resolution_errors,
            workspace_root=workspace_root,
            search_siblings=search_siblings
        )
        if child_node:
            root_node.add_child(child_node)

    # Build dependency graph
    graph = DependencyGraph(
        project_name=project_name or "unknown",
        root_pom=root_pom,
        root_node=root_node,
        circular_paths=circular_paths,
        resolution_errors=resolution_errors,
        resolution_start=start_time,
        resolution_end=datetime.now()
    )

    # Calculate statistics
    _calculate_statistics(graph)

    # Log summary
    log.info(f"Dependency resolution complete for '{graph.project_name}':")
    log.info(f"  Total: {graph.total_dependencies}")
    log.info(f"  Resolved: {graph.resolved_count}")
    log.info(f"  Not found: {graph.not_found_count}")
    log.info(f"  Circular: {graph.circular_count}")
    log.info(f"  Max depth: {graph.max_depth}")

    return graph


def _resolve_dependency_recursive(
    dependency: MavenDependency,
    base_dir: Path,
    max_depth: int,
    visited: Set[str],
    path: List[str],
    circular_paths: List[List[str]],
    resolution_errors: List[str],
    workspace_root: Optional[Path] = None,
    search_siblings: bool = True
) -> Optional[DependencyNode]:
    """
    Recursively resolve a single dependency.

    Args:
        dependency: MavenDependency to resolve
        base_dir: Base directory for resolution
        max_depth: Maximum recursion depth
        visited: Set of visited artifact IDs (for circular detection)
        path: Current dependency path (for circular detection reporting)
        circular_paths: List to collect detected circular paths
        resolution_errors: List to collect error messages
        workspace_root: Workspace root for sibling search (optional)
        search_siblings: Enable sibling directory search (default: True)

    Returns:
        DependencyNode with resolved children, or None on failure
    """
    artifact_id = dependency.artifact_id

    # Circular dependency detection (FR-007)
    if artifact_id in visited:
        cycle_path = path + [artifact_id]
        log.warning(f"Circular dependency detected: {' → '.join(cycle_path)}")
        dependency.resolution_status = "circular"
        circular_paths.append(cycle_path)
        # Return node but don't recurse
        return DependencyNode(dependency=dependency, children=[])

    # Add to visited set
    visited.add(artifact_id)

    # Resolve artifact path with multi-level search (FR-002)
    if search_siblings and workspace_root:
        # Use enhanced sibling search
        resolved_path = resolve_artifact_path_with_siblings(
            artifact_id=artifact_id,
            base_dir=workspace_root,
            group_id=dependency.group_id,
            search_levels=3,
            validate_pom=True
        )
    else:
        # Fallback to classic subdirectory search (backwards compatibility)
        resolved_path = resolve_artifact_path(
            artifact_id=artifact_id,
            base_dir=base_dir,
            group_id=dependency.group_id
        )

    if resolved_path:
        # Successfully resolved
        dependency.resolved_path = resolved_path
        dependency.resolution_status = "resolved"
        log.debug(f"Resolved {artifact_id} to {resolved_path}")

        # Check if we should recurse (FR-006)
        if dependency.depth < max_depth:
            # Look for pom.xml in resolved directory
            child_pom = resolved_path / "pom.xml"

            if child_pom.exists():
                try:
                    # Parse child dependencies
                    child_dependencies = parse_pom(child_pom, depth=dependency.depth + 1)

                    # Create node with children
                    node = DependencyNode(dependency=dependency, children=[])

                    # Recursively resolve children
                    for child_dep in child_dependencies:
                        child_node = _resolve_dependency_recursive(
                            dependency=child_dep,
                            base_dir=base_dir,
                            max_depth=max_depth,
                            visited=visited.copy(),  # Copy for each child branch
                            path=path + [artifact_id],
                            circular_paths=circular_paths,
                            resolution_errors=resolution_errors,
                            workspace_root=workspace_root,
                            search_siblings=search_siblings
                        )
                        if child_node:
                            node.add_child(child_node)

                    return node

                except Exception as e:
                    log.warning(f"Failed to parse {child_pom}: {e}")
                    resolution_errors.append(f"Parse error for {artifact_id}: {e}")
                    # Return node without children
                    return DependencyNode(dependency=dependency, children=[])
            else:
                log.debug(f"No pom.xml found in {resolved_path}")
                # Return node without children (leaf)
                return DependencyNode(dependency=dependency, children=[])
        else:
            # Max depth reached, return leaf node
            log.debug(f"Max depth reached for {artifact_id}")
            return DependencyNode(dependency=dependency, children=[])

    else:
        # Artifact not found (FR-008, FR-009)
        dependency.resolution_status = "not_found"
        error_msg = f"Artifact not found: {artifact_id} (groupId: {dependency.group_id})"
        log.warning(error_msg)
        resolution_errors.append(error_msg)
        # Return node even if not found (for tracking)
        return DependencyNode(dependency=dependency, children=[])


def _calculate_statistics(graph: DependencyGraph) -> None:
    """
    Calculate statistics for dependency graph.

    Updates graph.total_dependencies, resolved_count, not_found_count,
    circular_count, and max_depth.
    """
    all_deps = graph.get_all_dependencies()

    graph.total_dependencies = len(all_deps)
    graph.resolved_count = sum(1 for d in all_deps if d.is_resolved)
    graph.not_found_count = sum(1 for d in all_deps if d.is_not_found)
    graph.circular_count = len(graph.circular_paths)
    graph.max_depth = max((d.depth for d in all_deps), default=0)


def _create_empty_graph(
    project_name: str,
    root_pom: Path,
    start_time: datetime,
    errors: List[str]
) -> DependencyGraph:
    """Create an empty dependency graph for error cases."""
    root_node = DependencyNode(
        dependency=MavenDependency(
            group_id="",
            artifact_id=project_name,
            depth=-1
        ),
        children=[]
    )

    return DependencyGraph(
        project_name=project_name,
        root_pom=root_pom,
        root_node=root_node,
        resolution_errors=errors,
        resolution_start=start_time,
        resolution_end=datetime.now()
    )
