"""Path resolution utility for Maven artifact directories."""

from pathlib import Path
from typing import Optional, List
import logging
import xml.etree.ElementTree as ET

log = logging.getLogger(__name__)


def resolve_artifact_path(
    artifact_id: str,
    base_dir: Path,
    group_id: Optional[str] = None
) -> Optional[Path]:
    """
    Resolve Maven artifact to directory path.

    Resolution strategy: base_dir / artifact_id
    This follows Assumption 1 from research.md: artifact directories are named
    after artifactId only, not groupId-artifactId.

    Args:
        artifact_id: Maven artifactId (e.g., "cuco-cct-core")
        base_dir: Base directory (JAVA_SOURCE_DIR or JAVA_SOURCE_DIR/project)
        group_id: Maven groupId (not used in path resolution per Assumption 1,
                  included for logging purposes only)

    Returns:
        Resolved path if directory exists, None otherwise

    Example:
        >>> from pathlib import Path
        >>> resolve_artifact_path(
        ...     artifact_id="cuco-cct-core",
        ...     base_dir=Path("/workspace")
        ... )
        Path("/workspace/cuco-cct-core")
    """
    # Ensure base_dir is a Path object
    base_dir = Path(base_dir)

    # Resolve artifact path: base_dir / artifact_id
    artifact_path = base_dir / artifact_id

    if artifact_path.exists() and artifact_path.is_dir():
        log.debug(f"Resolved artifact '{artifact_id}' to {artifact_path}")
        return artifact_path
    else:
        # Log warning with detailed information
        log.warning(f"Artifact directory not found: {artifact_path}")
        if group_id:
            log.warning(f"  groupId: {group_id}, artifactId: {artifact_id}")
        else:
            log.warning(f"  artifactId: {artifact_id}")
        log.warning(f"  Expected at: {artifact_path}")
        log.warning(f"  Searched from base: {base_dir}")
        return None


def validate_pom_xml(artifact_path: Path, expected_artifact_id: str, expected_group_id: Optional[str] = None) -> bool:
    """
    Validate that a directory contains a pom.xml with matching artifact metadata.

    Args:
        artifact_path: Directory path to validate
        expected_artifact_id: Expected Maven artifactId
        expected_group_id: Expected Maven groupId (optional)

    Returns:
        True if pom.xml exists and metadata matches, False otherwise
    """
    pom_path = artifact_path / "pom.xml"

    if not pom_path.exists():
        log.debug(f"No pom.xml found in {artifact_path}")
        return False

    try:
        tree = ET.parse(pom_path)
        root = tree.getroot()

        # Handle Maven namespace
        ns = {'maven': 'http://maven.apache.org/POM/4.0.0'}

        # Try with namespace first, fallback to no namespace
        artifact_id_elem = root.find('maven:artifactId', ns)
        if artifact_id_elem is None:
            artifact_id_elem = root.find('artifactId')

        if artifact_id_elem is not None:
            actual_artifact_id = artifact_id_elem.text
            if actual_artifact_id != expected_artifact_id:
                log.debug(f"ArtifactId mismatch in {pom_path}: expected '{expected_artifact_id}', got '{actual_artifact_id}'")
                return False

        # Optionally validate groupId
        if expected_group_id:
            group_id_elem = root.find('maven:groupId', ns)
            if group_id_elem is None:
                group_id_elem = root.find('groupId')

            if group_id_elem is not None:
                actual_group_id = group_id_elem.text
                if actual_group_id != expected_group_id:
                    log.debug(f"GroupId mismatch in {pom_path}: expected '{expected_group_id}', got '{actual_group_id}'")
                    return False

        return True

    except ET.ParseError as e:
        log.warning(f"Failed to parse pom.xml at {pom_path}: {e}")
        return False
    except Exception as e:
        log.warning(f"Error validating pom.xml at {pom_path}: {e}")
        return False


def resolve_artifact_path_with_siblings(
    artifact_id: str,
    base_dir: Path,
    group_id: Optional[str] = None,
    search_levels: int = 3,
    validate_pom: bool = True
) -> Optional[Path]:
    """
    Resolve Maven artifact path with multi-level sibling search.

    This enhanced resolver supports multiple workspace patterns:
    1. Monorepo pattern: artifact as subdirectory (existing behavior)
    2. Sibling pattern: artifact in parent's sibling directory (NEW)
    3. Multi-level pattern: search up to N parent levels (NEW)

    Search Strategy (stops at first match):
        1. Check subdirectory: base_dir/artifact_id/
        2. Check sibling: base_dir/../artifact_id/
        3. Check parent siblings: base_dir/../../artifact_id/
        4. Continue up to search_levels

    Args:
        artifact_id: Maven artifactId (e.g., "cuco-cct-core")
        base_dir: Starting directory (project being analyzed)
        group_id: Maven groupId (optional, used for validation)
        search_levels: How many parent levels to search (default: 3)
        validate_pom: Whether to validate pom.xml metadata (default: True)

    Returns:
        Resolved path if found and validated, None otherwise

    Example:
        # Directory structure:
        # /workspace/
        #   ├── cuco-ui-admin/  (analyzing this)
        #   ├── cuco-cct-core/  (dependency - sibling)
        #   └── administration.ui/  (dependency - sibling)

        >>> from pathlib import Path
        >>> resolve_artifact_path_with_siblings(
        ...     artifact_id="cuco-cct-core",
        ...     base_dir=Path("/workspace/cuco-ui-admin")
        ... )
        Path("/workspace/cuco-cct-core")  # Found as sibling
    """
    base_dir = Path(base_dir).resolve()
    search_paths: List[Path] = []

    # Strategy 1: Subdirectory search (existing monorepo pattern)
    subdirectory_path = base_dir / artifact_id
    search_paths.append(("subdirectory", subdirectory_path))

    # Strategy 2-N: Sibling search at multiple levels
    current_dir = base_dir
    for level in range(1, search_levels + 1):
        # Go up one level
        parent_dir = current_dir.parent

        # Check if we've reached filesystem root
        if parent_dir == current_dir:
            log.debug(f"Reached filesystem root, stopping search at level {level}")
            break

        # Look for artifact as sibling at this level
        sibling_path = parent_dir / artifact_id
        search_level = "sibling" if level == 1 else f"level-{level}"
        search_paths.append((search_level, sibling_path))

        current_dir = parent_dir

    # Search all paths in order
    for search_type, artifact_path in search_paths:
        log.debug(f"Searching for '{artifact_id}' as {search_type}: {artifact_path}")

        # Check if directory exists
        if not artifact_path.exists() or not artifact_path.is_dir():
            log.debug(f"  Not found: {artifact_path}")
            continue

        # Optionally validate pom.xml
        if validate_pom:
            if not validate_pom_xml(artifact_path, artifact_id, group_id):
                log.debug(f"  Found directory but pom.xml validation failed: {artifact_path}")
                continue

        # Found and validated!
        log.info(f"Resolved artifact '{artifact_id}' ({search_type}): {artifact_path}")
        return artifact_path

    # Not found anywhere
    log.warning(f"Artifact directory not found after searching {len(search_paths)} locations: {artifact_id}")
    if group_id:
        log.warning(f"  groupId: {group_id}, artifactId: {artifact_id}")
    log.warning(f"  Searched from base: {base_dir}")
    log.warning(f"  Search levels: {search_levels}")
    log.warning(f"  Locations checked:")
    for search_type, path in search_paths:
        log.warning(f"    [{search_type}] {path}")

    return None


def validate_base_directory(base_dir: Path, context: str = "") -> bool:
    """
    Validate that a base directory exists and is accessible.

    Args:
        base_dir: Directory path to validate
        context: Optional context string for error messages

    Returns:
        True if directory is valid, False otherwise

    Logs errors if validation fails.
    """
    base_dir = Path(base_dir)
    context_msg = f" ({context})" if context else ""

    if not base_dir.exists():
        log.error(f"Base directory does not exist{context_msg}: {base_dir}")
        return False

    if not base_dir.is_dir():
        log.error(f"Base directory is not a directory{context_msg}: {base_dir}")
        return False

    return True


def get_relative_path(file_path: Path, base_dir: Path) -> Path:
    """
    Get relative path of file from base directory.

    Args:
        file_path: Absolute file path
        base_dir: Base directory

    Returns:
        Relative path from base_dir to file_path

    Raises:
        ValueError: If file_path is not under base_dir
    """
    file_path = Path(file_path).resolve()
    base_dir = Path(base_dir).resolve()

    try:
        return file_path.relative_to(base_dir)
    except ValueError:
        raise ValueError(
            f"File path is not under base directory:\n"
            f"  file_path: {file_path}\n"
            f"  base_dir: {base_dir}"
        )
