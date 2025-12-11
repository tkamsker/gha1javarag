import os
from typing import List
from src.common.models import DiscoveredFile

def discover_files(project_name: str, source_dir: str) -> List[DiscoveredFile]:
    """
    Recursively scans a directory for relevant files.
    """
    discovered_files = []
    supported_extensions = {".java", ".jsp", ".js", ".xml"}

    for root, _, files in os.walk(source_dir):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext in supported_extensions:
                file_path = os.path.join(root, file)
                file_type = ext[1:]
                discovered_files.append(
                    DiscoveredFile(
                        project_name=project_name,
                        file_path=file_path,
                        file_type=file_type,
                    )
                )
    return discovered_files
