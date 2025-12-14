"""
Discovery service.

Discovers Maven projects, scans files, and generates discovery inventories.
"""

import logging
import hashlib
import time
from pathlib import Path
from typing import Generator, List, Optional, Dict, Any, Callable
from datetime import datetime
from collections import defaultdict

from codeindex.models.project import Project
from codeindex.models.inventory import DiscoveryInventory
from codeindex.models import ArtifactType
from codeindex.services.maven import MavenParser, POMParseError
from codeindex.services.classifier import FileClassifier

logger = logging.getLogger(__name__)


# Directories to exclude from discovery
EXCLUDED_DIRS = {
    'target',
    'build',
    'out',
    '.git',
    '.svn',
    '.hg',
    'node_modules',
    '__pycache__',
    '.venv',
    'venv',
    '.idea',
    '.vscode',
}


def generate_project_id(
    group_id: Optional[str] = None,
    artifact_id: Optional[str] = None,
    version: Optional[str] = None,
    path: Optional[Path] = None
) -> str:
    """
    Generate a project ID from Maven coordinates or path.

    Args:
        group_id: Maven groupId
        artifact_id: Maven artifactId
        version: Maven version
        path: Fallback path for ID generation

    Returns:
        Project ID string (groupId:artifactId:version or path-based hash)
    """
    # If we have full Maven coordinates, use them
    if group_id and artifact_id and version:
        return f"{group_id}:{artifact_id}:{version}"

    # If we have partial coordinates, use what we have
    if artifact_id and version:
        return f"{artifact_id}:{version}"

    if artifact_id:
        # Use artifact ID with path hash for uniqueness
        if path:
            path_hash = hashlib.md5(str(path).encode()).hexdigest()[:8]
            return f"{artifact_id}:{path_hash}"
        return artifact_id

    # Fallback: use path-based ID
    if path:
        # Use last directory name + hash of full path
        dir_name = path.parent.name if path.is_file() else path.name
        path_hash = hashlib.md5(str(path.resolve()).encode()).hexdigest()[:8]
        return f"{dir_name}:{path_hash}"

    raise ValueError("Cannot generate project ID: no coordinates or path provided")


def create_project_from_pom(pom_path: Path) -> Project:
    """
    Create a Project object from a pom.xml file.

    Args:
        pom_path: Path to pom.xml file

    Returns:
        Project object with metadata from POM

    Raises:
        POMParseError: If POM parsing fails
    """
    parser = MavenParser()
    pom_data = parser.parse_pom(pom_path)

    # Generate project ID
    project_id = generate_project_id(
        group_id=pom_data.get('groupId'),
        artifact_id=pom_data.get('artifactId'),
        version=pom_data.get('version'),
        path=pom_path
    )

    # Create UUID v5 from project_id (deterministic)
    import uuid
    namespace = uuid.NAMESPACE_DNS
    project_uuid = uuid.uuid5(namespace, project_id)

    # Get project directory
    project_path = pom_path.parent

    # Create Project object
    project = Project(
        id=project_uuid,
        project_id=project_id,
        name=pom_data.get('name') or pom_data.get('artifactId', 'unknown'),
        artifact_id=pom_data.get('artifactId', ''),
        group_id=pom_data.get('groupId'),
        version=pom_data.get('version'),
        packaging=pom_data.get('packaging', 'jar'),
        path=str(project_path),
        modules=pom_data.get('modules', []),
        dependencies=pom_data.get('dependencies', []),
        source_roots=[pom_data.get('sourceDirectory', 'src/main/java')],
        test_roots=[pom_data.get('testSourceDirectory', 'src/test/java')],
        resource_roots=[r['directory'] for r in pom_data.get('resources', [])],
        summary=pom_data.get('description'),
    )

    return project


def scan_directory(
    directory: Path,
    pattern: Optional[str] = None,
    max_depth: Optional[int] = None,
    exclude_hidden: bool = True
) -> Generator[Path, None, None]:
    """
    Scan directory recursively and yield file paths.

    Args:
        directory: Directory to scan
        pattern: Optional glob pattern (e.g., "*.java")
        max_depth: Maximum directory depth (None for unlimited)
        exclude_hidden: Whether to exclude hidden files

    Yields:
        File paths
    """
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    if not directory.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    def _scan_recursive(path: Path, current_depth: int) -> Generator[Path, None, None]:
        """Recursive directory scanner."""
        # Check depth limit
        if max_depth is not None and current_depth > max_depth:
            return

        try:
            for item in path.iterdir():
                # Skip hidden files if requested
                if exclude_hidden and item.name.startswith('.'):
                    continue

                # Skip excluded directories
                if item.is_dir() and item.name in EXCLUDED_DIRS:
                    logger.debug(f"Skipping excluded directory: {item}")
                    continue

                if item.is_file():
                    # Apply pattern filter if specified
                    if pattern:
                        if item.match(pattern):
                            yield item
                    else:
                        yield item
                elif item.is_dir():
                    # Recurse into subdirectory
                    yield from _scan_recursive(item, current_depth + 1)

        except PermissionError as e:
            logger.warning(f"Permission denied accessing {path}: {e}")
        except Exception as e:
            logger.error(f"Error scanning {path}: {e}")

    yield from _scan_recursive(directory, 0)


def discover_projects(
    root_directory: Path,
    artifact_filter: Optional[str] = None,
    progress_callback: Optional[Callable] = None
) -> Generator[Project, None, None]:
    """
    Discover Maven projects in a directory tree.

    Args:
        root_directory: Root directory to search
        artifact_filter: Optional artifact ID filter
        progress_callback: Optional callback(current, total, message)

    Yields:
        Project objects
    """
    if not root_directory.exists():
        raise FileNotFoundError(f"Directory not found: {root_directory}")

    if not root_directory.is_dir():
        raise ValueError(f"Not a directory: {root_directory}")

    logger.info(f"Discovering Maven projects in {root_directory}")

    # Find all pom.xml files
    pom_files = list(scan_directory(root_directory, pattern="pom.xml"))
    total_poms = len(pom_files)

    logger.info(f"Found {total_poms} pom.xml files")

    for idx, pom_path in enumerate(pom_files):
        if progress_callback:
            progress_callback(idx + 1, total_poms, f"Processing {pom_path.name}")

        try:
            # Parse POM and create Project
            project = create_project_from_pom(pom_path)

            # Apply artifact filter if specified
            if artifact_filter:
                if artifact_filter not in project.artifact_id:
                    logger.debug(f"Skipping {project.artifact_id} (filtered)")
                    continue

            logger.info(f"Discovered project: {project.project_id}")
            yield project

        except POMParseError as e:
            logger.warning(f"Failed to parse {pom_path}: {e}")
            continue
        except Exception as e:
            logger.error(f"Error processing {pom_path}: {e}")
            continue


class DiscoveryService:
    """
    Discovery service for finding Maven projects and scanning files.

    Orchestrates project discovery, file scanning, and inventory generation.
    """

    def __init__(self, config: Optional[Any] = None):
        """
        Initialize discovery service.

        Args:
            config: Optional configuration object
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.classifier = FileClassifier()
        self.maven_parser = MavenParser()

    def discover_projects(
        self,
        root_directory: Path,
        progress_callback: Optional[Callable] = None
    ) -> Generator[Project, None, None]:
        """
        Discover Maven projects in a directory tree.

        Args:
            root_directory: Root directory to search
            progress_callback: Optional callback(current, total, message)

        Yields:
            Project objects
        """
        yield from discover_projects(root_directory, progress_callback=progress_callback)

    def scan_files(
        self,
        directory: Path,
        max_depth: Optional[int] = None
    ) -> Generator[Path, None, None]:
        """
        Scan directory for files.

        Args:
            directory: Directory to scan
            max_depth: Maximum directory depth

        Yields:
            File paths
        """
        yield from scan_directory(directory, max_depth=max_depth)

    def scan_and_classify(
        self,
        directory: Path,
        max_depth: Optional[int] = None
    ) -> Generator[tuple[Path, ArtifactType], None, None]:
        """
        Scan directory and classify each file.

        Args:
            directory: Directory to scan
            max_depth: Maximum directory depth

        Yields:
            Tuples of (file_path, artifact_type)
        """
        for file_path in self.scan_files(directory, max_depth=max_depth):
            artifact_type = self.classifier.classify(file_path)
            yield (file_path, artifact_type)

    def generate_inventory(
        self,
        root_directory: Path,
        progress_callback: Optional[Callable] = None
    ) -> DiscoveryInventory:
        """
        Generate discovery inventory for a directory tree.

        Args:
            root_directory: Root directory to analyze
            progress_callback: Optional progress callback

        Returns:
            DiscoveryInventory object
        """
        start_time = time.time()
        scan_timestamp = datetime.now()

        self.logger.info(f"Generating discovery inventory for {root_directory}")

        # Discover projects
        projects = list(self.discover_projects(root_directory, progress_callback))

        # Scan and classify files for each project
        total_files = 0
        files_by_type: Dict[str, int] = defaultdict(int)

        # Collect project data with file lists
        projects_with_files = []

        for project in projects:
            project_path = Path(project.path)

            if not project_path.exists():
                self.logger.warning(f"Project path does not exist: {project_path}")
                continue

            # Scan files in project and collect file list
            file_count = 0
            file_list = []

            for file_path, artifact_type in self.scan_and_classify(project_path):
                # Skip binary static assets (images, videos, etc.) - not useful for code analysis
                if artifact_type == ArtifactType.STATIC_ASSET:
                    continue

                file_count += 1
                files_by_type[artifact_type.value] += 1

                # Add file entry to project file list
                file_list.append({
                    'path': str(file_path),
                    'type': artifact_type.name,  # Use enum name (e.g., JAVA_SOURCE)
                    'relative_path': str(file_path.relative_to(project_path)) if file_path.is_relative_to(project_path) else str(file_path)
                })

            project.file_count = file_count
            total_files += file_count

            self.logger.debug(f"Project {project.artifact_id}: {file_count} files")

            # Add project with file list
            project_dict = project.to_dict()
            project_dict['files'] = file_list
            projects_with_files.append(project_dict)

        # Calculate duration
        duration = time.time() - start_time

        # Create inventory
        inventory = DiscoveryInventory(
            scan_timestamp=scan_timestamp,
            root_directory=str(root_directory),
            projects=projects_with_files,
            total_files=total_files,
            files_by_type=dict(files_by_type),
            scan_duration_seconds=duration
        )

        self.logger.info(
            f"Discovery complete: {len(projects)} projects, "
            f"{total_files} files in {duration:.2f}s"
        )

        return inventory
