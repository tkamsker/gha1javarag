"""
Metadata extraction and management module.
Handles extraction of metadata from parsed files and creation of structured data.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import hashlib
import logging
from datetime import datetime


@dataclass
class FileMetadata:
    """Structured metadata for a file."""
    file_path: str
    project_name: str
    language: str
    size_bytes: int
    sha256: str
    last_modified: datetime
    relative_path: str
    package: Optional[str] = None
    classes: List[Dict[str, Any]] = None
    imports: List[str] = None
    comments: str = ""
    complexity_score: int = 0
    line_count: int = 0
    business_hints: Dict[str, Any] = None
    error: Optional[str] = None


class MetadataExtractor:
    """Extracts and manages metadata from parsed files."""
    
    def __init__(self, config):
        """Initialize metadata extractor with configuration."""
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def extract_metadata(self, file_path: str, content: str, parsed_data: Dict[str, Any]) -> FileMetadata:
        """Extract comprehensive metadata from a parsed file."""
        try:
            # Basic file information
            file_info = self._get_file_info(file_path, content)
            
            # Extract language-specific metadata
            language_metadata = self._extract_language_metadata(parsed_data)
            
            # Extract business hints
            business_hints = self._extract_business_hints(parsed_data)
            
            # Calculate complexity
            complexity_score = self._calculate_complexity(parsed_data)
            
            # Count lines
            line_count = len(content.splitlines())
            
            return FileMetadata(
                file_path=file_info['file_path'],
                project_name=file_info['project_name'],
                language=file_info['language'],
                size_bytes=file_info['size_bytes'],
                sha256=file_info['sha256'],
                last_modified=file_info['last_modified'],
                relative_path=file_info['relative_path'],
                package=language_metadata.get('package'),
                classes=language_metadata.get('classes', []),
                imports=language_metadata.get('imports', []),
                comments=language_metadata.get('comments', ''),
                complexity_score=complexity_score,
                line_count=line_count,
                business_hints=business_hints
            )
        
        except Exception as e:
            self.logger.error(f"Error extracting metadata for {file_path}: {e}")
            return FileMetadata(
                file_path=file_path,
                project_name='unknown',
                language='unknown',
                size_bytes=0,
                sha256='',
                last_modified=datetime.now(),
                relative_path=file_path,
                error=str(e)
            )
    
    def _get_file_info(self, file_path: str, content: str) -> Dict[str, Any]:
        """Get basic file information."""
        from pathlib import Path
        
        file_path_obj = Path(file_path)
        
        # Determine project name from path
        project_name = self._determine_project_name(file_path)
        
        # Determine language from extension
        language = self._determine_language(file_path)
        
        # Calculate file hash
        sha256 = hashlib.sha256(content.encode('utf-8')).hexdigest()
        
        # Get file stats
        try:
            stat = file_path_obj.stat()
            size_bytes = stat.st_size
            last_modified = datetime.fromtimestamp(stat.st_mtime)
        except OSError:
            size_bytes = len(content.encode('utf-8'))
            last_modified = datetime.now()
        
        # Create relative path
        try:
            source_path = Path(self.config.java_source_dir)
            relative_path = str(file_path_obj.relative_to(source_path))
        except ValueError:
            relative_path = str(file_path_obj)
        
        return {
            'file_path': str(file_path),
            'project_name': project_name,
            'language': language,
            'size_bytes': size_bytes,
            'sha256': sha256,
            'last_modified': last_modified,
            'relative_path': relative_path
        }
    
    def _determine_project_name(self, file_path: str) -> str:
        """Determine project name from file path."""
        from pathlib import Path
        
        file_path_obj = Path(file_path)
        source_path = Path(self.config.java_source_dir)
        
        try:
            # Get relative path from source directory
            relative_path = file_path_obj.relative_to(source_path)
            parts = relative_path.parts
            
            if len(parts) > 0:
                return parts[0]  # First directory is project name
            else:
                return "__root__"
        except ValueError:
            # File is not under source directory
            return "__root__"
    
    def _determine_language(self, file_path: str) -> str:
        """Determine programming language from file extension."""
        from pathlib import Path
        
        extension = Path(file_path).suffix.lower()
        
        language_map = {
            '.java': 'java',
            '.jsp': 'jsp',
            '.tsp': 'jsp',
            '.xml': 'xml',
            '.html': 'html',
            '.js': 'javascript',
            '.sql': 'sql',
            '.properties': 'properties',
            '.json': 'json',
            '.md': 'markdown',
            '.css': 'css',
            '.ui.xml': 'gwt_uibinder',
            '.gwt.xml': 'gwt_config'
        }
        
        return language_map.get(extension, 'unknown')
    
    def _extract_language_metadata(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract language-specific metadata from parsed data."""
        metadata = {}
        
        # Extract common fields
        if 'package' in parsed_data:
            metadata['package'] = parsed_data['package']
        
        if 'classes' in parsed_data:
            metadata['classes'] = parsed_data['classes']
        
        if 'imports' in parsed_data:
            metadata['imports'] = parsed_data['imports']
        
        if 'comments' in parsed_data:
            metadata['comments'] = parsed_data['comments']
        
        return metadata
    
    def _extract_business_hints(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract business logic hints from parsed data."""
        hints = {
            'validation_rules': [],
            'feature_flags': [],
            'roles_permissions': [],
            'domain_entities': [],
            'endpoints': [],
            'navigation_targets': []
        }
        
        # Extract from various sources
        if 'business_hints' in parsed_data:
            hints.update(parsed_data['business_hints'])
        
        if 'endpoints' in parsed_data:
            hints['endpoints'] = parsed_data['endpoints']
        
        if 'navigation_targets' in parsed_data:
            hints['navigation_targets'] = parsed_data['navigation_targets']
        
        if 'forms' in parsed_data:
            hints['forms'] = parsed_data['forms']
        
        if 'ui_fields' in parsed_data:
            hints['ui_components'] = parsed_data['ui_fields']
        
        return hints
    
    def _calculate_complexity(self, parsed_data: Dict[str, Any]) -> int:
        """Calculate complexity score for parsed data."""
        complexity = 1  # Base complexity
        
        # Add complexity from parsed data
        if 'complexity_score' in parsed_data:
            complexity += parsed_data['complexity_score']
        
        # Add complexity based on structure
        if 'classes' in parsed_data:
            complexity += len(parsed_data['classes']) * 2
        
        if 'methods' in parsed_data:
            complexity += len(parsed_data['methods'])
        
        if 'functions' in parsed_data:
            complexity += len(parsed_data['functions'])
        
        if 'forms' in parsed_data:
            complexity += len(parsed_data['forms'])
        
        if 'scripts' in parsed_data:
            complexity += len(parsed_data['scripts'])
        
        return complexity
    
    def create_chunk_metadata(self, chunk, file_metadata: FileMetadata) -> Dict[str, Any]:
        """Create metadata for a chunk based on file metadata."""
        return {
            'file_path': chunk.file_path,
            'project_name': chunk.project_name,
            'chunk_kind': chunk.chunk_kind,
            'language': chunk.language,
            'start_line': chunk.start_line,
            'end_line': chunk.end_line,
            'class_name': chunk.class_name,
            'function_name': chunk.function_name,
            'architectural_layer': chunk.architectural_layer,
            'business_domain': chunk.business_domain,
            'complexity_score': chunk.complexity_score,
            'parent_refs': chunk.parent_refs or [],
            'child_refs': chunk.child_refs or [],
            'repository_context': chunk.repository_context,
            'package': file_metadata.package,
            'file_sha256': file_metadata.sha256,
            'file_size_bytes': file_metadata.size_bytes,
            'file_last_modified': file_metadata.last_modified.isoformat()
        }
    
    def create_weaviate_object(self, chunk, file_metadata: FileMetadata, collection_name: str) -> Dict[str, Any]:
        """Create a Weaviate object from a chunk and file metadata."""
        base_object = {
            'projectName': chunk.project_name,
            'filePath': chunk.file_path,
            'chunkKind': chunk.chunk_kind,
            'language': chunk.language,
            'content': chunk.content,
            'className': chunk.class_name or '',
            'functionName': chunk.function_name or '',
            'architecturalLayer': chunk.architectural_layer or '',
            'businessDomain': chunk.business_domain or '',
            'complexityScore': chunk.complexity_score or 0,
            'startLine': chunk.start_line,
            'endLine': chunk.end_line,
            'parentRefs': chunk.parent_refs or [],
            'childRefs': chunk.child_refs or [],
            'repositoryContext': chunk.repository_context
        }
        
        # Add collection-specific fields
        if collection_name == 'DocumentationChunks':
            base_object.update({
                'section': chunk.chunk_kind
            })
        elif collection_name == 'BusinessRules':
            base_object.update({
                'domainEntities': file_metadata.business_hints.get('domain_entities', []) if file_metadata.business_hints else [],
                'dataFlows': file_metadata.business_hints.get('data_flows', []) if file_metadata.business_hints else []
            })
        elif collection_name == 'IntegrationPoints':
            base_object.update({
                'endpoint': file_metadata.business_hints.get('endpoints', [])[0] if file_metadata.business_hints and file_metadata.business_hints.get('endpoints') else '',
                'protocol': 'HTTP',  # Default, could be extracted from content
                'databaseObjects': file_metadata.business_hints.get('database_objects', []) if file_metadata.business_hints else []
            })
        elif collection_name == 'UIComponents':
            base_object.update({
                'componentName': chunk.class_name or chunk.function_name or 'Unknown',
                'componentType': chunk.chunk_kind,
                'packageName': file_metadata.package or '',
                'sourceCode': chunk.content,
                'uiTemplate': '',  # Would be extracted from UiBinder files
                'gwtWidgets': file_metadata.business_hints.get('ui_components', []) if file_metadata.business_hints else [],
                'businessDomains': [chunk.business_domain] if chunk.business_domain else [],
                'userRoles': file_metadata.business_hints.get('roles_permissions', []) if file_metadata.business_hints else [],
                'navigationTargets': file_metadata.business_hints.get('navigation_targets', []) if file_metadata.business_hints else [],
                'eventHandlers': file_metadata.business_hints.get('event_handlers', []) if file_metadata.business_hints else [],
                'accessibilityScore': 0,  # Would be calculated
                'responsiveCapability': False  # Would be determined
            })
        elif collection_name == 'NavigationFlows':
            base_object.update({
                'flowName': chunk.function_name or chunk.class_name or 'Unknown',
                'flowDescription': chunk.content[:200],  # First 200 chars
                'sourceComponent': chunk.class_name or '',
                'targetComponent': '',  # Would be extracted from navigation logic
                'transitionTrigger': '',  # Would be extracted from event handlers
                'userRole': '',  # Would be extracted from business hints
                'businessProcess': chunk.business_domain or ''
            })
        
        return base_object
