"""
Utility functions for project name detection and extraction.
"""
from pathlib import Path
from typing import Optional
from config.settings import settings


def extract_project_name_from_path(file_path: str, java_source_dir: Optional[str] = None) -> str:
    """
    Extract project name from file path based on directory structure.
    
    Rules:
    1. If path contains 'src' directory, the directory immediately before 'src' is the project
    2. If JAVA_SOURCE_DIR has a 'src' subdirectory, it's a single project (use basename of JAVA_SOURCE_DIR)
    3. If JAVA_SOURCE_DIR has multiple subdirectories, each subdirectory is a project
    4. Otherwise, use the first meaningful directory name before common build directories
    
    Args:
        file_path: Full path to the file
        java_source_dir: Optional JAVA_SOURCE_DIR to help determine project structure
        
    Returns:
        Project name string
    """
    if not file_path:
        return settings.default_project_name
    
    path_parts = Path(file_path).parts
    
    # Ignore common build/system directories
    ignore_dirs = {
        'src', 'main', 'java', 'webapp', 'resources', 'dao', 'service',
        'test', 'target', 'build', 'node_modules', '.git', '.idea',
        'web', 'WEB-INF', 'classes', 'generated', 'mnt', 'cucocalcai'
    }
    
    # Strategy 1: Look for 'src' directory and get the directory before it
    # Example: /mnt/cucocalcai/cuco-master/cuco-master@hash/cuco-cct-core/src/... -> cuco-cct-core
    for i, part in enumerate(path_parts):
        if part == 'src' and i > 0:
            # Get the directory immediately before 'src'
            project_candidate = path_parts[i - 1]
            # Clean up project name (remove @hash suffixes, etc.) before checking ignore_dirs
            clean_candidate = project_candidate.split('@')[0].split('#')[0]
            if clean_candidate not in ignore_dirs and len(clean_candidate) > 1:
                return clean_candidate
    
    # Strategy 2: If JAVA_SOURCE_DIR is provided, check its structure
    if java_source_dir:
        source_path = Path(java_source_dir)
        if source_path.exists():
            # Check if JAVA_SOURCE_DIR has a 'src' subdirectory (single project)
            if (source_path / 'src').exists() and (source_path / 'src').is_dir():
                # Single project - use basename of JAVA_SOURCE_DIR
                project_name = source_path.name
                if project_name not in ignore_dirs:
                    return project_name.split('@')[0].split('#')[0]
            
            # Check if file_path is under JAVA_SOURCE_DIR
            try:
                file_path_obj = Path(file_path)
                if file_path_obj.is_relative_to(source_path):
                    # Get the relative path
                    relative_path = file_path_obj.relative_to(source_path)
                    relative_parts = relative_path.parts
                    
                    # If first part is not 'src', it's likely a project subdirectory
                    if relative_parts and relative_parts[0] not in ignore_dirs:
                        project_name = relative_parts[0]
                        return project_name.split('@')[0].split('#')[0]
            except (ValueError, AttributeError):
                pass  # Not relative to source dir, continue with other strategies
    
    # Strategy 3: Find first meaningful directory name
    for part in path_parts:
        if part in ignore_dirs:
            continue
        # Skip very short names, hidden directories, and common system paths
        if (len(part) > 2 and 
            not part.startswith('.') and 
            part not in ['home', 'usr', 'var', 'tmp', 'opt', 'root']):
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

