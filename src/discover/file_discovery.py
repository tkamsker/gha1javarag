"""
File discovery module for finding Java/JSP/GWT/JS files.
"""
import os
import glob
import logging
from pathlib import Path
from typing import List, Dict, Set
from fnmatch import fnmatch

from config.settings import settings

logger = logging.getLogger(__name__)

class FileDiscovery:
    """Discovers files matching the specified patterns."""
    
    def __init__(self):
        """Initialize file discovery."""
        self.java_source_path = settings.get_java_source_path()
        self.discovered_files = {
            'java': set(),
            'jsp': set(),
            'gwt': set(),
            'js': set(),
            'xml': set(),
            'sql': set()
        }
    
    def discover_all_files(self, project_name: str = None) -> Dict[str, Set[str]]:
        """Discover all relevant files for the project."""
        if not settings.is_java_source_valid():
            logger.error(f"Java source directory is not valid: {self.java_source_path}")
            return self.discovered_files
        
        logger.info(f"Discovering files in: {self.java_source_path}")
        
        # Discover Java files
        self._discover_java_files()
        
        # Discover JSP files
        self._discover_jsp_files()
        
        # Discover GWT files
        self._discover_gwt_files()
        
        # Discover JavaScript files
        self._discover_js_files()
        
        # Discover XML files (iBATIS, web.xml, etc.)
        self._discover_xml_files()
        
        # Discover SQL files
        self._discover_sql_files()
        
        # Log discovery results
        total_files = sum(len(files) for files in self.discovered_files.values())
        logger.info(f"Discovered {total_files} files total:")
        for file_type, files in self.discovered_files.items():
            logger.info(f"  {file_type}: {len(files)} files")
        
        return self.discovered_files
    
    def _discover_java_files(self):
        """Discover Java source files."""
        for pattern in settings.get_java_include_globs():
            pattern_path = self.java_source_path / pattern
            for file_path in glob.glob(str(pattern_path), recursive=True):
                if os.path.isfile(file_path) and file_path.endswith('.java'):
                    self.discovered_files['java'].add(file_path)
    
    def _discover_jsp_files(self):
        """Discover JSP files."""
        for pattern in settings.get_jsp_include_globs():
            pattern_path = self.java_source_path / pattern
            for file_path in glob.glob(str(pattern_path), recursive=True):
                if os.path.isfile(file_path) and (file_path.endswith('.jsp') or file_path.endswith('.jspf')):
                    self.discovered_files['jsp'].add(file_path)
    
    def _discover_gwt_files(self):
        """Discover GWT-related files."""
        for pattern in settings.get_gwt_include_globs():
            pattern_path = self.java_source_path / pattern
            for file_path in glob.glob(str(pattern_path), recursive=True):
                if os.path.isfile(file_path):
                    if (file_path.endswith('.gwt.xml') or 
                        file_path.endswith('.ui.xml') or
                        'EntryPoint' in file_path or
                        'Activity' in file_path or
                        'Place' in file_path or
                        'Service' in file_path or
                        'RequestFactory' in file_path):
                        self.discovered_files['gwt'].add(file_path)
    
    def _discover_js_files(self):
        """Discover JavaScript files."""
        for pattern in settings.get_js_include_globs():
            pattern_path = self.java_source_path / pattern
            for file_path in glob.glob(str(pattern_path), recursive=True):
                if os.path.isfile(file_path) and file_path.endswith('.js'):
                    self.discovered_files['js'].add(file_path)
    
    def _discover_xml_files(self):
        """Discover XML files (iBATIS, web.xml, etc.)."""
        xml_patterns = [
            "**/*.xml",
            "**/web.xml",
            "**/pom.xml",
            "**/build.xml"
        ]
        
        for pattern in xml_patterns:
            pattern_path = self.java_source_path / pattern
            for file_path in glob.glob(str(pattern_path), recursive=True):
                if os.path.isfile(file_path) and file_path.endswith('.xml'):
                    self.discovered_files['xml'].add(file_path)
    
    def _discover_sql_files(self):
        """Discover SQL files."""
        sql_patterns = [
            "**/*.sql",
            "**/*.ddl",
            "**/*.dml"
        ]
        
        for pattern in sql_patterns:
            pattern_path = self.java_source_path / pattern
            for file_path in glob.glob(str(pattern_path), recursive=True):
                if os.path.isfile(file_path) and (file_path.endswith('.sql') or 
                                                 file_path.endswith('.ddl') or 
                                                 file_path.endswith('.dml')):
                    self.discovered_files['sql'].add(file_path)
    
    def get_files_by_type(self, file_type: str) -> List[str]:
        """Get files of a specific type."""
        return list(self.discovered_files.get(file_type, set()))
    
    def get_all_files(self) -> List[str]:
        """Get all discovered files."""
        all_files = []
        for files in self.discovered_files.values():
            all_files.extend(files)
        return all_files
    
    def filter_files_by_project(self, project_name: str) -> Dict[str, Set[str]]:
        """Filter files that belong to a specific project."""
        filtered_files = {
            'java': set(),
            'jsp': set(),
            'gwt': set(),
            'js': set(),
            'xml': set(),
            'sql': set()
        }
        
        for file_type, files in self.discovered_files.items():
            for file_path in files:
                # Simple project filtering based on path structure
                if project_name.lower() in file_path.lower():
                    filtered_files[file_type].add(file_path)
        
        return filtered_files
    
    def get_project_name_from_path(self, file_path: str) -> str:
        """Extract project name from file path."""
        path_parts = Path(file_path).parts
        
        # Look for common project indicators
        for part in path_parts:
            if part in ['src', 'main', 'java', 'webapp', 'resources']:
                continue
            if '.' in part and len(part) > 3:  # Likely a package name
                return part.split('.')[0]
            if part and not part.startswith('.') and len(part) > 2:
                return part
        
        return settings.default_project_name
