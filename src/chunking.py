"""
Chunking module for breaking down code and documentation into manageable pieces.
Implements the hierarchical chunking strategy from iteration15-2.md.
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import logging


@dataclass
class Chunk:
    """Represents a chunk of code or documentation."""
    content: str
    chunk_kind: str
    file_path: str
    project_name: str
    language: str
    start_line: int
    end_line: int
    class_name: Optional[str] = None
    function_name: Optional[str] = None
    architectural_layer: Optional[str] = None
    business_domain: Optional[str] = None
    complexity_score: Optional[int] = None
    parent_refs: List[str] = None
    child_refs: List[str] = None
    repository_context: str = ""


class ChunkingStrategy:
    """Implements hierarchical chunking strategy for code repositories."""
    
    def __init__(self, config):
        """Initialize chunking strategy with configuration."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Chunk size limits (in characters)
        self.chunk_sizes = {
            'repository': 100000,  # 50-100KB
            'module': 50000,       # 20-50KB
            'file': 25000,         # 8-25KB
            'class': 8000,         # 2-8KB
            'method': 2000,        # 0.5-2KB
            'ui': 8000,            # 2-8KB
            'navigation': 15000    # 5-15KB
        }
        
        # Overlap percentage
        self.overlap_percent = config.chunk_overlap_percent / 100.0
    
    def chunk_file(self, file_path: str, content: str, metadata: Dict[str, Any]) -> List[Chunk]:
        """Chunk a file based on its type and content."""
        language = metadata.get('language', 'unknown')
        project_name = metadata.get('project_name', 'unknown')
        
        chunks = []
        
        try:
            if language == 'java':
                chunks = self._chunk_java_file(file_path, content, metadata, project_name)
            elif language == 'jsp':
                chunks = self._chunk_jsp_file(file_path, content, metadata, project_name)
            elif language == 'xml':
                chunks = self._chunk_xml_file(file_path, content, metadata, project_name)
            elif language == 'html':
                chunks = self._chunk_html_file(file_path, content, metadata, project_name)
            elif language == 'javascript':
                chunks = self._chunk_js_file(file_path, content, metadata, project_name)
            elif language == 'css':
                chunks = self._chunk_css_file(file_path, content, metadata, project_name)
            elif language in ['gwt_java', 'gwt_uibinder', 'gwt_config']:
                chunks = self._chunk_gwt_file(file_path, content, metadata, project_name)
            else:
                chunks = self._chunk_generic_file(file_path, content, metadata, project_name)
        
        except Exception as e:
            self.logger.error(f"Error chunking file {file_path}: {e}")
            # Create a single fallback chunk
            chunks = [self._create_fallback_chunk(file_path, content, metadata, project_name)]
        
        return chunks
    
    def _chunk_java_file(self, file_path: str, content: str, metadata: Dict[str, Any], project_name: str) -> List[Chunk]:
        """Chunk Java file by classes and methods."""
        chunks = []
        lines = content.splitlines()
        
        # Extract classes from metadata
        classes = metadata.get('classes', [])
        
        if not classes:
            # Fallback: chunk by file
            return self._chunk_by_file(file_path, content, metadata, project_name, 'java')
        
        for class_info in classes:
            class_name = class_info.get('name', 'UnknownClass')
            
            # Create class-level chunk
            class_chunk = self._create_class_chunk(
                file_path, content, metadata, project_name, 
                class_info, lines
            )
            if class_chunk:
                chunks.append(class_chunk)
            
            # Create method-level chunks
            methods = class_info.get('methods', [])
            for method in methods:
                method_chunk = self._create_method_chunk(
                    file_path, content, metadata, project_name,
                    class_name, method, lines
                )
                if method_chunk:
                    chunks.append(method_chunk)
        
        return chunks
    
    def _chunk_jsp_file(self, file_path: str, content: str, metadata: Dict[str, Any], project_name: str) -> List[Chunk]:
        """Chunk JSP file by forms, scripts, and UI components."""
        chunks = []
        
        # Extract forms
        forms = metadata.get('forms', [])
        for form in forms:
            form_chunk = self._create_form_chunk(file_path, form, metadata, project_name)
            if form_chunk:
                chunks.append(form_chunk)
        
        # Extract scripts
        scripts = metadata.get('scripts', [])
        for i, script in enumerate(scripts):
            script_chunk = self._create_script_chunk(file_path, script, metadata, project_name, i)
            if script_chunk:
                chunks.append(script_chunk)
        
        # Create file-level chunk for remaining content
        file_chunk = self._chunk_by_file(file_path, content, metadata, project_name, 'jsp')
        chunks.extend(file_chunk)
        
        return chunks
    
    def _chunk_xml_file(self, file_path: str, content: str, metadata: Dict[str, Any], project_name: str) -> List[Chunk]:
        """Chunk XML file by configuration sections."""
        chunks = []
        
        # Extract configuration data
        config = metadata.get('configuration', {})
        
        if 'servlets' in config:
            servlet_chunk = self._create_servlet_chunk(file_path, config['servlets'], metadata, project_name)
            if servlet_chunk:
                chunks.append(servlet_chunk)
        
        if 'filters' in config:
            filter_chunk = self._create_filter_chunk(file_path, config['filters'], metadata, project_name)
            if filter_chunk:
                chunks.append(filter_chunk)
        
        # Create file-level chunk
        file_chunk = self._chunk_by_file(file_path, content, metadata, project_name, 'xml')
        chunks.extend(file_chunk)
        
        return chunks
    
    def _chunk_html_file(self, file_path: str, content: str, metadata: Dict[str, Any], project_name: str) -> List[Chunk]:
        """Chunk HTML file by forms and UI components."""
        chunks = []
        
        # Extract forms
        forms = metadata.get('forms', [])
        for form in forms:
            form_chunk = self._create_form_chunk(file_path, form, metadata, project_name)
            if form_chunk:
                chunks.append(form_chunk)
        
        # Extract scripts
        scripts = metadata.get('scripts', [])
        for i, script in enumerate(scripts):
            script_chunk = self._create_script_chunk(file_path, script, metadata, project_name, i)
            if script_chunk:
                chunks.append(script_chunk)
        
        # Create file-level chunk
        file_chunk = self._chunk_by_file(file_path, content, metadata, project_name, 'html')
        chunks.extend(file_chunk)
        
        return chunks
    
    def _chunk_js_file(self, file_path: str, content: str, metadata: Dict[str, Any], project_name: str) -> List[Chunk]:
        """Chunk JavaScript file by functions and classes."""
        chunks = []
        lines = content.splitlines()
        
        # Extract functions
        functions = metadata.get('functions', [])
        for func_name in functions:
            func_chunk = self._create_function_chunk(file_path, content, metadata, project_name, func_name, lines)
            if func_chunk:
                chunks.append(func_chunk)
        
        # Extract classes
        classes = metadata.get('classes', [])
        for class_name in classes:
            class_chunk = self._create_js_class_chunk(file_path, content, metadata, project_name, class_name, lines)
            if class_chunk:
                chunks.append(class_chunk)
        
        # Create file-level chunk
        file_chunk = self._chunk_by_file(file_path, content, metadata, project_name, 'javascript')
        chunks.extend(file_chunk)
        
        return chunks
    
    def _chunk_css_file(self, file_path: str, content: str, metadata: Dict[str, Any], project_name: str) -> List[Chunk]:
        """Chunk CSS file by rules and sections."""
        chunks = []
        
        # Extract CSS rules
        rules = metadata.get('rules', [])
        for rule in rules:
            rule_chunk = self._create_css_rule_chunk(file_path, rule, metadata, project_name)
            if rule_chunk:
                chunks.append(rule_chunk)
        
        # Create file-level chunk
        file_chunk = self._chunk_by_file(file_path, content, metadata, project_name, 'css')
        chunks.extend(file_chunk)
        
        return chunks
    
    def _chunk_gwt_file(self, file_path: str, content: str, metadata: Dict[str, Any], project_name: str) -> List[Chunk]:
        """Chunk GWT file by UI components and navigation flows."""
        chunks = []
        
        # Extract UI components
        ui_fields = metadata.get('ui_fields', [])
        if ui_fields:
            ui_chunk = self._create_ui_component_chunk(file_path, ui_fields, metadata, project_name)
            if ui_chunk:
                chunks.append(ui_chunk)
        
        # Extract navigation flows
        navigation_flows = metadata.get('navigation_flows', [])
        if navigation_flows:
            nav_chunk = self._create_navigation_chunk(file_path, navigation_flows, metadata, project_name)
            if nav_chunk:
                chunks.append(nav_chunk)
        
        # Create file-level chunk
        file_chunk = self._chunk_by_file(file_path, content, metadata, project_name, 'gwt')
        chunks.extend(file_chunk)
        
        return chunks
    
    def _chunk_generic_file(self, file_path: str, content: str, metadata: Dict[str, Any], project_name: str) -> List[Chunk]:
        """Chunk generic file by file size."""
        return self._chunk_by_file(file_path, content, metadata, project_name, 'unknown')
    
    def _chunk_by_file(self, file_path: str, content: str, metadata: Dict[str, Any], project_name: str, language: str) -> List[Chunk]:
        """Create file-level chunks based on size limits."""
        chunks = []
        max_size = self.chunk_sizes['file']
        
        if len(content) <= max_size:
            # Single chunk
            chunk = Chunk(
                content=content,
                chunk_kind='file',
                file_path=file_path,
                project_name=project_name,
                language=language,
                start_line=1,
                end_line=len(content.splitlines()),
                repository_context=self._get_repository_context(metadata)
            )
            chunks.append(chunk)
        else:
            # Split into multiple chunks
            lines = content.splitlines()
            chunk_size = max_size // 2  # Rough estimate for line-based chunking
            
            for i in range(0, len(lines), chunk_size):
                end_idx = min(i + chunk_size, len(lines))
                chunk_content = '\n'.join(lines[i:end_idx])
                
                chunk = Chunk(
                    content=chunk_content,
                    chunk_kind='file',
                    file_path=file_path,
                    project_name=project_name,
                    language=language,
                    start_line=i + 1,
                    end_line=end_idx,
                    repository_context=self._get_repository_context(metadata)
                )
                chunks.append(chunk)
        
        return chunks
    
    def _create_class_chunk(self, file_path: str, content: str, metadata: Dict[str, Any], 
                          project_name: str, class_info: Dict[str, Any], lines: List[str]) -> Optional[Chunk]:
        """Create a chunk for a Java class."""
        class_name = class_info.get('name', 'UnknownClass')
        
        # Find class boundaries in the content
        class_start = self._find_class_start(content, class_name)
        if class_start == -1:
            return None
        
        class_end = self._find_class_end(content, class_start)
        if class_end == -1:
            return None
        
        class_content = content[class_start:class_end]
        
        # Determine architectural layer
        architectural_layer = self._determine_architectural_layer(class_info, metadata)
        
        # Determine business domain
        business_domain = self._determine_business_domain(class_info, metadata)
        
        return Chunk(
            content=class_content,
            chunk_kind='class',
            file_path=file_path,
            project_name=project_name,
            language='java',
            start_line=class_start,
            end_line=class_end,
            class_name=class_name,
            architectural_layer=architectural_layer,
            business_domain=business_domain,
            complexity_score=class_info.get('complexity_score'),
            repository_context=self._get_repository_context(metadata)
        )
    
    def _create_method_chunk(self, file_path: str, content: str, metadata: Dict[str, Any],
                           project_name: str, class_name: str, method: Dict[str, Any], lines: List[str]) -> Optional[Chunk]:
        """Create a chunk for a Java method."""
        method_name = method.get('name', 'unknownMethod')
        
        # Find method boundaries (simplified)
        method_start = self._find_method_start(content, method_name)
        if method_start == -1:
            return None
        
        method_end = self._find_method_end(content, method_start)
        if method_end == -1:
            return None
        
        method_content = content[method_start:method_end]
        
        return Chunk(
            content=method_content,
            chunk_kind='method',
            file_path=file_path,
            project_name=project_name,
            language='java',
            start_line=method_start,
            end_line=method_end,
            class_name=class_name,
            function_name=method_name,
            repository_context=self._get_repository_context(metadata)
        )
    
    def _create_form_chunk(self, file_path: str, form: Dict[str, Any], metadata: Dict[str, Any], project_name: str) -> Optional[Chunk]:
        """Create a chunk for an HTML form."""
        form_content = form.get('content', '')
        if not form_content:
            return None
        
        return Chunk(
            content=form_content,
            chunk_kind='ui',
            file_path=file_path,
            project_name=project_name,
            language=metadata.get('language', 'html'),
            start_line=1,
            end_line=len(form_content.splitlines()),
            architectural_layer='ui',
            repository_context=self._get_repository_context(metadata)
        )
    
    def _create_script_chunk(self, file_path: str, script: str, metadata: Dict[str, Any], project_name: str, index: int) -> Optional[Chunk]:
        """Create a chunk for a JavaScript script."""
        if not script:
            return None
        
        return Chunk(
            content=script,
            chunk_kind='ui',
            file_path=file_path,
            project_name=project_name,
            language='javascript',
            start_line=1,
            end_line=len(script.splitlines()),
            architectural_layer='ui',
            repository_context=self._get_repository_context(metadata)
        )
    
    def _create_servlet_chunk(self, file_path: str, servlets: List[Dict[str, Any]], metadata: Dict[str, Any], project_name: str) -> Optional[Chunk]:
        """Create a chunk for servlet configuration."""
        if not servlets:
            return None
        
        content = "Servlet Configuration:\n"
        for servlet in servlets:
            content += f"Servlet: {servlet.get('name', 'Unknown')}\n"
            content += f"Class: {servlet.get('class', 'Unknown')}\n"
            content += f"Init Params: {servlet.get('init_params', {})}\n\n"
        
        return Chunk(
            content=content,
            chunk_kind='integration',
            file_path=file_path,
            project_name=project_name,
            language='xml',
            start_line=1,
            end_line=len(content.splitlines()),
            architectural_layer='backend',
            repository_context=self._get_repository_context(metadata)
        )
    
    def _create_filter_chunk(self, file_path: str, filters: List[Dict[str, Any]], metadata: Dict[str, Any], project_name: str) -> Optional[Chunk]:
        """Create a chunk for filter configuration."""
        if not filters:
            return None
        
        content = "Filter Configuration:\n"
        for filter_elem in filters:
            content += f"Filter: {filter_elem.get('name', 'Unknown')}\n"
            content += f"Class: {filter_elem.get('class', 'Unknown')}\n\n"
        
        return Chunk(
            content=content,
            chunk_kind='integration',
            file_path=file_path,
            project_name=project_name,
            language='xml',
            start_line=1,
            end_line=len(content.splitlines()),
            architectural_layer='backend',
            repository_context=self._get_repository_context(metadata)
        )
    
    def _create_function_chunk(self, file_path: str, content: str, metadata: Dict[str, Any], 
                             project_name: str, func_name: str, lines: List[str]) -> Optional[Chunk]:
        """Create a chunk for a JavaScript function."""
        # Find function boundaries (simplified)
        func_start = self._find_function_start(content, func_name)
        if func_start == -1:
            return None
        
        func_end = self._find_function_end(content, func_start)
        if func_end == -1:
            return None
        
        func_content = content[func_start:func_end]
        
        return Chunk(
            content=func_content,
            chunk_kind='method',
            file_path=file_path,
            project_name=project_name,
            language='javascript',
            start_line=func_start,
            end_line=func_end,
            function_name=func_name,
            architectural_layer='ui',
            repository_context=self._get_repository_context(metadata)
        )
    
    def _create_js_class_chunk(self, file_path: str, content: str, metadata: Dict[str, Any],
                             project_name: str, class_name: str, lines: List[str]) -> Optional[Chunk]:
        """Create a chunk for a JavaScript class."""
        # Find class boundaries (simplified)
        class_start = self._find_js_class_start(content, class_name)
        if class_start == -1:
            return None
        
        class_end = self._find_js_class_end(content, class_start)
        if class_end == -1:
            return None
        
        class_content = content[class_start:class_end]
        
        return Chunk(
            content=class_content,
            chunk_kind='class',
            file_path=file_path,
            project_name=project_name,
            language='javascript',
            start_line=class_start,
            end_line=class_end,
            class_name=class_name,
            architectural_layer='ui',
            repository_context=self._get_repository_context(metadata)
        )
    
    def _create_css_rule_chunk(self, file_path: str, rule: str, metadata: Dict[str, Any], project_name: str) -> Optional[Chunk]:
        """Create a chunk for a CSS rule."""
        if not rule:
            return None
        
        return Chunk(
            content=rule,
            chunk_kind='ui',
            file_path=file_path,
            project_name=project_name,
            language='css',
            start_line=1,
            end_line=len(rule.splitlines()),
            architectural_layer='ui',
            repository_context=self._get_repository_context(metadata)
        )
    
    def _create_ui_component_chunk(self, file_path: str, ui_fields: List[Dict[str, Any]], metadata: Dict[str, Any], project_name: str) -> Optional[Chunk]:
        """Create a chunk for GWT UI components."""
        if not ui_fields:
            return None
        
        content = "UI Components:\n"
        for field in ui_fields:
            content += f"Field: {field.get('name', 'Unknown')} ({field.get('type', 'Unknown')})\n"
        
        return Chunk(
            content=content,
            chunk_kind='ui',
            file_path=file_path,
            project_name=project_name,
            language='gwt',
            start_line=1,
            end_line=len(content.splitlines()),
            architectural_layer='ui',
            repository_context=self._get_repository_context(metadata)
        )
    
    def _create_navigation_chunk(self, file_path: str, navigation_flows: List[Dict[str, Any]], metadata: Dict[str, Any], project_name: str) -> Optional[Chunk]:
        """Create a chunk for navigation flows."""
        if not navigation_flows:
            return None
        
        content = "Navigation Flows:\n"
        for flow in navigation_flows:
            content += f"Method: {flow.get('method', 'Unknown')}\n"
            content += f"Target: {flow.get('target', 'Unknown')}\n\n"
        
        return Chunk(
            content=content,
            chunk_kind='navigation',
            file_path=file_path,
            project_name=project_name,
            language='gwt',
            start_line=1,
            end_line=len(content.splitlines()),
            architectural_layer='ui',
            repository_context=self._get_repository_context(metadata)
        )
    
    def _create_fallback_chunk(self, file_path: str, content: str, metadata: Dict[str, Any], project_name: str) -> Chunk:
        """Create a fallback chunk when other chunking methods fail."""
        return Chunk(
            content=content[:self.chunk_sizes['file']],  # Truncate if too long
            chunk_kind='file',
            file_path=file_path,
            project_name=project_name,
            language=metadata.get('language', 'unknown'),
            start_line=1,
            end_line=len(content.splitlines()),
            repository_context=self._get_repository_context(metadata)
        )
    
    def _find_class_start(self, content: str, class_name: str) -> int:
        """Find the start position of a class in content."""
        pattern = rf'class\s+{re.escape(class_name)}'
        match = re.search(pattern, content)
        return match.start() if match else -1
    
    def _find_class_end(self, content: str, start_pos: int) -> int:
        """Find the end position of a class in content."""
        # Simple implementation - find matching closing brace
        brace_count = 0
        in_string = False
        escape_next = False
        
        for i in range(start_pos, len(content)):
            char = content[i]
            
            if escape_next:
                escape_next = False
                continue
            
            if char == '\\':
                escape_next = True
                continue
            
            if char == '"' or char == "'":
                in_string = not in_string
                continue
            
            if not in_string:
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        return i + 1
        
        return -1
    
    def _find_method_start(self, content: str, method_name: str) -> int:
        """Find the start position of a method in content."""
        pattern = rf'(\w+\s+)*{re.escape(method_name)}\s*\('
        match = re.search(pattern, content)
        return match.start() if match else -1
    
    def _find_method_end(self, content: str, start_pos: int) -> int:
        """Find the end position of a method in content."""
        # Similar to class end but for methods
        brace_count = 0
        paren_count = 0
        in_string = False
        escape_next = False
        
        for i in range(start_pos, len(content)):
            char = content[i]
            
            if escape_next:
                escape_next = False
                continue
            
            if char == '\\':
                escape_next = True
                continue
            
            if char == '"' or char == "'":
                in_string = not in_string
                continue
            
            if not in_string:
                if char == '(':
                    paren_count += 1
                elif char == ')':
                    paren_count -= 1
                elif char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0 and paren_count == 0:
                        return i + 1
        
        return -1
    
    def _find_function_start(self, content: str, func_name: str) -> int:
        """Find the start position of a JavaScript function."""
        pattern = rf'function\s+{re.escape(func_name)}\s*\('
        match = re.search(pattern, content)
        return match.start() if match else -1
    
    def _find_function_end(self, content: str, start_pos: int) -> int:
        """Find the end position of a JavaScript function."""
        return self._find_method_end(content, start_pos)
    
    def _find_js_class_start(self, content: str, class_name: str) -> int:
        """Find the start position of a JavaScript class."""
        pattern = rf'class\s+{re.escape(class_name)}'
        match = re.search(pattern, content)
        return match.start() if match else -1
    
    def _find_js_class_end(self, content: str, start_pos: int) -> int:
        """Find the end position of a JavaScript class."""
        return self._find_class_end(content, start_pos)
    
    def _determine_architectural_layer(self, class_info: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Determine the architectural layer of a class."""
        class_name = class_info.get('name', '').lower()
        package = class_info.get('package', '').lower()
        
        # Check package patterns
        if any(keyword in package for keyword in ['dao', 'repository', 'entity', 'model']):
            return 'database'
        elif any(keyword in package for keyword in ['service', 'controller', 'manager', 'handler']):
            return 'backend'
        elif any(keyword in package for keyword in ['ui', 'view', 'presenter', 'widget']):
            return 'ui'
        
        # Check class name patterns
        if any(keyword in class_name for keyword in ['dao', 'repository', 'entity', 'model']):
            return 'database'
        elif any(keyword in class_name for keyword in ['service', 'controller', 'manager', 'handler']):
            return 'backend'
        elif any(keyword in class_name for keyword in ['ui', 'view', 'presenter', 'widget']):
            return 'ui'
        
        return 'backend'  # Default
    
    def _determine_business_domain(self, class_info: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Determine the business domain of a class."""
        class_name = class_info.get('name', '').lower()
        package = class_info.get('package', '').lower()
        
        # Extract domain from package or class name
        domain_hints = ['user', 'customer', 'order', 'product', 'payment', 'inventory', 'report']
        
        for hint in domain_hints:
            if hint in package or hint in class_name:
                return hint.title()
        
        return 'General'
    
    def _get_repository_context(self, metadata: Dict[str, Any]) -> str:
        """Get repository context for a chunk."""
        context_parts = []
        
        if 'package' in metadata:
            context_parts.append(f"Package: {metadata['package']}")
        
        if 'project_name' in metadata:
            context_parts.append(f"Project: {metadata['project_name']}")
        
        return ' | '.join(context_parts)
