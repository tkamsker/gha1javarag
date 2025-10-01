"""
Project discovery module for finding and indexing Java projects.
Discovers projects in JAVA_SOURCE_DIR and builds file inventories.
"""

import os
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging

from .env_loader import Config


@dataclass
class FileInfo:
    """Information about a discovered file."""
    file_path: str
    project_name: str
    language: str
    size_bytes: int
    sha256: str
    last_modified: datetime
    relative_path: str


@dataclass
class ProjectInfo:
    """Information about a discovered project."""
    name: str
    path: str
    files: List[FileInfo]
    total_files: int
    total_size: int


class ProjectDiscovery:
    """Discovers and catalogs Java projects and their files."""
    
    def __init__(self, config: Config):
        """Initialize project discovery with configuration."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Normalize file extensions
        self.include_extensions = {ext.lower() for ext in config.include_file_types}
        self.exclude_dirs = {dir_name.lower() for dir_name in config.exclude_dirs}
    
    def discover_projects(self) -> List[ProjectInfo]:
        """Discover all projects in the configured source directory."""
        source_path = Path(self.config.java_source_dir)
        
        if not source_path.exists():
            raise FileNotFoundError(f"Source directory does not exist: {source_path}")
        
        projects = []
        
        # Check if there are files directly in the root directory
        root_files = self._get_files_in_directory(source_path, is_root=True)
        if root_files:
            root_project = ProjectInfo(
                name="__root__",
                path=str(source_path),
                files=root_files,
                total_files=len(root_files),
                total_size=sum(f.size_bytes for f in root_files)
            )
            projects.append(root_project)
            self.logger.info(f"Found root project with {len(root_files)} files")
        
        # Find first-level subdirectories as projects
        for item in source_path.iterdir():
            if item.is_dir() and item.name.lower() not in self.exclude_dirs:
                project_files = self._get_files_in_directory(item)
                if project_files:
                    project = ProjectInfo(
                        name=item.name,
                        path=str(item),
                        files=project_files,
                        total_files=len(project_files),
                        total_size=sum(f.size_bytes for f in project_files)
                    )
                    projects.append(project)
                    self.logger.info(f"Found project '{item.name}' with {len(project_files)} files")
        
        return projects
    
    def _get_files_in_directory(self, directory: Path, is_root: bool = False) -> List[FileInfo]:
        """Recursively get all files in a directory that match inclusion criteria."""
        files = []
        
        try:
            for item in directory.rglob('*'):
                if item.is_file():
                    # Check if file should be excluded
                    if self._should_exclude_file(item):
                        continue
                    
                    # Check file extension
                    if not self._has_valid_extension(item):
                        continue
                    
                    # Check file size
                    if item.stat().st_size > self.config.max_file_bytes:
                        self.logger.warning(f"File too large, skipping: {item} ({item.stat().st_size} bytes)")
                        continue
                    
                    # Determine project name
                    if is_root:
                        project_name = "__root__"
                    else:
                        project_name = directory.name
                    
                    # Create file info
                    file_info = self._create_file_info(item, project_name)
                    files.append(file_info)
        
        except PermissionError as e:
            self.logger.error(f"Permission denied accessing directory {directory}: {e}")
        except Exception as e:
            self.logger.error(f"Error processing directory {directory}: {e}")
        
        return files
    
    def _should_exclude_file(self, file_path: Path) -> bool:
        """Check if a file should be excluded based on directory exclusions."""
        # Check if any parent directory is in exclude list
        for parent in file_path.parents:
            if parent.name.lower() in self.exclude_dirs:
                return True
        return False
    
    def _has_valid_extension(self, file_path: Path) -> bool:
        """Check if file has a valid extension."""
        return file_path.suffix.lower() in self.include_extensions
    
    def _create_file_info(self, file_path: Path, project_name: str) -> FileInfo:
        """Create FileInfo object for a file."""
        try:
            # Get file stats
            stat = file_path.stat()
            size_bytes = stat.st_size
            last_modified = datetime.fromtimestamp(stat.st_mtime)
            
            # Calculate SHA256
            sha256 = self._calculate_sha256(file_path)
            
            # Determine language from extension
            language = self._get_language_from_extension(file_path.suffix)
            
            # Create relative path
            source_path = Path(self.config.java_source_dir)
            try:
                relative_path = str(file_path.relative_to(source_path))
            except ValueError:
                # If file is not under source path, use absolute path
                relative_path = str(file_path)
            
            return FileInfo(
                file_path=str(file_path),
                project_name=project_name,
                language=language,
                size_bytes=size_bytes,
                sha256=sha256,
                last_modified=last_modified,
                relative_path=relative_path
            )
        
        except Exception as e:
            self.logger.error(f"Error creating file info for {file_path}: {e}")
            raise
    
    def _calculate_sha256(self, file_path: Path) -> str:
        """Calculate SHA256 hash of a file."""
        hash_sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            self.logger.error(f"Error calculating SHA256 for {file_path}: {e}")
            return ""
    
    def _get_language_from_extension(self, extension: str) -> str:
        """Map file extension to programming language."""
        ext_map = {
            '.java': 'java',
            '.jsp': 'jsp',
            '.tsp': 'jsp',  # Treat .tsp as JSP
            '.xml': 'xml',
            '.html': 'html',
            '.js': 'javascript',
            '.sql': 'sql',
            '.properties': 'properties',
            '.json': 'json',
            '.md': 'markdown',
            '.css': 'css',
            '.ui.xml': 'gwt_ui',
            '.gwt.xml': 'gwt_config'
        }
        return ext_map.get(extension.lower(), 'unknown')
    
    def create_project_catalog(self, projects: List[ProjectInfo]) -> Dict[str, Any]:
        """Create a catalog of all discovered projects."""
        catalog = {
            'discovery_timestamp': datetime.now().isoformat(),
            'source_directory': self.config.java_source_dir,
            'total_projects': len(projects),
            'total_files': sum(p.total_files for p in projects),
            'total_size_bytes': sum(p.total_size for p in projects),
            'projects': []
        }
        
        for project in projects:
            project_data = {
                'name': project.name,
                'path': project.path,
                'total_files': project.total_files,
                'total_size_bytes': project.total_size,
                'files_by_language': self._count_files_by_language(project.files),
                'file_list': [
                    {
                        'path': f.relative_path,
                        'language': f.language,
                        'size_bytes': f.size_bytes,
                        'sha256': f.sha256,
                        'last_modified': f.last_modified.isoformat()
                    }
                    for f in project.files
                ]
            }
            catalog['projects'].append(project_data)
        
        return catalog
    
    def _count_files_by_language(self, files: List[FileInfo]) -> Dict[str, int]:
        """Count files by programming language."""
        counts = {}
        for file_info in files:
            counts[file_info.language] = counts.get(file_info.language, 0) + 1
        return counts
