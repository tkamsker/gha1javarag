"""
Utility functions for project name detection and extraction.
"""
from pathlib import Path
from typing import Optional
from config.settings import settings


def extract_project_name_from_path(file_path: str, java_source_dir: Optional[str] = None) -> str:
    """
    Extract project name from file path based on directory structure.
    
    Rules (in priority order):
    1. If JAVA_SOURCE_DIR is set, use it as the base and extract the first subdirectory as project
    2. If path contains 'src' directory, the directory immediately before 'src' is the project
    3. Otherwise, use the first meaningful directory name before common build directories
    
    Args:
        file_path: Full path to the file
        java_source_dir: Optional JAVA_SOURCE_DIR to help determine project structure
                       (if not provided, uses settings.java_source_dir)
        
    Returns:
        Project name string
    """
    if not file_path:
        return settings.default_project_name
    
    # Use JAVA_SOURCE_DIR from settings if not provided
    if java_source_dir is None:
        java_source_dir = settings.java_source_dir
    
    file_path_obj = Path(file_path)
    
    # Ignore common build/system directories
    ignore_dirs = {
        'src', 'main', 'java', 'webapp', 'resources', 'dao', 'service',
        'test', 'target', 'build', 'node_modules', '.git', '.idea',
        'web', 'WEB-INF', 'classes', 'generated', '_deprecated', '_scripts'
    }
    
    # Strategy 1: Use JAVA_SOURCE_DIR as base (HIGHEST PRIORITY)
    # Example: JAVA_SOURCE_DIR=/mnt/cucocalcai/cuco-master/cuco-master@hash
    #          Path: /mnt/cucocalcai/cuco-master/cuco-master@hash/cuco-cct-core/src/...
    #          Project: cuco-cct-core
    if java_source_dir and java_source_dir != "/path/to/java/source":
        source_path = Path(java_source_dir)
        if source_path.exists():
            try:
                # Check if file_path is under JAVA_SOURCE_DIR
                if file_path_obj.is_relative_to(source_path):
                    # Get the relative path
                    relative_path = file_path_obj.relative_to(source_path)
                    relative_parts = relative_path.parts
                    
                    # The first part after JAVA_SOURCE_DIR is the project name
                    # (unless it's a common directory like 'src')
                    if relative_parts:
                        first_part = relative_parts[0]
                        # Clean up project name (remove @hash suffixes, etc.)
                        project_name = first_part.split('@')[0].split('#')[0]
                        
                        # If first part is not in ignore list, it's the project
                        if project_name not in ignore_dirs and len(project_name) > 1:
                            return project_name
                        
                        # If first part is 'src', check if JAVA_SOURCE_DIR itself is a project
                        # (single project structure)
                        if first_part == 'src':
                            # Single project - use basename of JAVA_SOURCE_DIR
                            project_name = source_path.name.split('@')[0].split('#')[0]
                            if project_name not in ignore_dirs:
                                return project_name
            except (ValueError, AttributeError):
                pass  # Not relative to source dir, continue with other strategies
    
    # Strategy 2: Look for 'src' directory and get the directory before it
    # Example: /mnt/cucocalcai/cuco-master/cuco-master@hash/cuco-cct-core/src/... -> cuco-cct-core
    path_parts = file_path_obj.parts
    for i, part in enumerate(path_parts):
        if part == 'src' and i > 0:
            # Get the directory immediately before 'src'
            project_candidate = path_parts[i - 1]
            # Clean up project name (remove @hash suffixes, etc.)
            clean_candidate = project_candidate.split('@')[0].split('#')[0]
            if clean_candidate not in ignore_dirs and len(clean_candidate) > 1:
                return clean_candidate
    
    # Strategy 3: Find first meaningful directory name (fallback)
    # Skip system paths and common directories
    system_paths = {'home', 'usr', 'var', 'tmp', 'opt', 'root', 'mnt', 'cucocalcai', 'cuco-master'}
    for part in path_parts:
        if part in ignore_dirs or part in system_paths:
            continue
        # Skip very short names, hidden directories
        if (len(part) > 2 and not part.startswith('.')):
            # Clean up project name
            project_name = part.split('@')[0].split('#')[0]
            return project_name
    
    # Fallback to default
    return settings.default_project_name


def get_all_projects_from_artifacts(artifacts: dict) -> set:
    """
    Extract all unique project names from artifacts.
    
    Args:
        artifacts: Dictionary with artifact types as keys and lists of artifacts as values
        
    Returns:
        Set of unique project names
    """
    projects = set()
    
    for artifact_type, artifact_list in artifacts.items():
        if not isinstance(artifact_list, list):
            continue
        for artifact in artifact_list:
            if isinstance(artifact, dict):
                project = artifact.get('project')
                if project:
                    projects.add(project)
    
    return projects

