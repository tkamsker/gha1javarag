"""Path resolution utility for Maven artifact directories."""

from pathlib import Path
from typing import Optional
import logging

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
