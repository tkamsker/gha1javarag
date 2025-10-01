"""
Java source code parser for extracting metadata from .java files.
"""

import re
import ast
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass
import logging


@dataclass
class JavaClass:
    """Represents a Java class or interface."""
    name: str
    type: str  # 'class', 'interface', 'enum', 'annotation'
    package: str
    imports: List[str]
    annotations: List[str]
    methods: List['JavaMethod']
    fields: List['JavaField']
    extends: Optional[str] = None
    implements: List[str] = None
    modifiers: List[str] = None
    comments: str = ""


@dataclass
class JavaMethod:
    """Represents a Java method."""
    name: str
    return_type: str
    parameters: List[Dict[str, str]]  # [{"name": "param1", "type": "String"}]
    modifiers: List[str]
    annotations: List[str]
    comments: str = ""
    line_start: int = 0
    line_end: int = 0


@dataclass
class JavaField:
    """Represents a Java field."""
    name: str
    type: str
    modifiers: List[str]
    annotations: List[str]
    comments: str = ""


class JavaParser:
    """Parser for Java source code files."""
    
    def __init__(self):
        """Initialize the Java parser."""
        self.logger = logging.getLogger(__name__)
        
        # Regex patterns for parsing
        self.package_pattern = re.compile(r'^\s*package\s+([\w.]+);', re.MULTILINE)
        self.import_pattern = re.compile(r'^\s*import\s+(?:static\s+)?([\w.*]+);', re.MULTILINE)
        self.class_pattern = re.compile(
            r'(?:public|private|protected)?\s*(?:static\s+)?(?:final\s+)?(?:abstract\s+)?'
            r'(class|interface|enum|@interface)\s+(\w+)',
            re.MULTILINE
        )
        self.annotation_pattern = re.compile(r'@(\w+)(?:\([^)]*\))?')
        self.method_pattern = re.compile(
            r'(?:public|private|protected)?\s*(?:static\s+)?(?:final\s+)?(?:abstract\s+)?'
            r'(?:synchronized\s+)?(?:native\s+)?(\w+(?:<[^>]*>)?)\s+(\w+)\s*\([^)]*\)',
            re.MULTILINE
        )
        self.field_pattern = re.compile(
            r'(?:public|private|protected)?\s*(?:static\s+)?(?:final\s+)?(?:volatile\s+)?'
            r'(\w+(?:<[^>]*>)?)\s+(\w+)\s*[=;]',
            re.MULTILINE
        )
        self.comment_pattern = re.compile(r'/\*.*?\*/', re.DOTALL)
        self.line_comment_pattern = re.compile(r'//.*$', re.MULTILINE)
    
    def parse_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Parse a Java file and extract metadata."""
        try:
            # Extract basic information
            package = self._extract_package(content)
            imports = self._extract_imports(content)
            classes = self._extract_classes(content)
            comments = self._extract_comments(content)
            
            # Calculate complexity metrics
            complexity_score = self._calculate_complexity(content)
            line_count = len(content.splitlines())
            
            # Extract business hints
            business_hints = self._extract_business_hints(content)
            
            return {
                'file_path': file_path,
                'package': package,
                'imports': imports,
                'classes': [self._class_to_dict(cls) for cls in classes],
                'comments': comments,
                'complexity_score': complexity_score,
                'line_count': line_count,
                'business_hints': business_hints,
                'language': 'java'
            }
        
        except Exception as e:
            self.logger.error(f"Error parsing Java file {file_path}: {e}")
            return {
                'file_path': file_path,
                'error': str(e),
                'language': 'java'
            }
    
    def _extract_package(self, content: str) -> str:
        """Extract package declaration."""
        match = self.package_pattern.search(content)
        return match.group(1) if match else ""
    
    def _extract_imports(self, content: str) -> List[str]:
        """Extract import statements."""
        imports = []
        for match in self.import_pattern.finditer(content):
            imports.append(match.group(1))
        return imports
    
    def _extract_classes(self, content: str) -> List[JavaClass]:
        """Extract class, interface, enum, and annotation definitions."""
        classes = []
        
        for match in self.class_pattern.finditer(content):
            class_type = match.group(1)
            class_name = match.group(2)
            
            # Extract annotations
            annotations = self._extract_annotations_at_position(content, match.start())
            
            # Extract methods and fields
            methods = self._extract_methods(content, class_name)
            fields = self._extract_fields(content, class_name)
            
            # Extract extends/implements
            extends, implements = self._extract_inheritance(content, match.start())
            
            # Extract modifiers
            modifiers = self._extract_modifiers_at_position(content, match.start())
            
            # Extract comments
            comments = self._extract_comments_at_position(content, match.start())
            
            java_class = JavaClass(
                name=class_name,
                type=class_type,
                package=self._extract_package(content),
                imports=self._extract_imports(content),
                annotations=annotations,
                methods=methods,
                fields=fields,
                extends=extends,
                implements=implements,
                modifiers=modifiers,
                comments=comments
            )
            classes.append(java_class)
        
        return classes
    
    def _extract_annotations_at_position(self, content: str, position: int) -> List[str]:
        """Extract annotations at a specific position."""
        # Look backwards from position to find annotations
        before_position = content[:position]
        lines = before_position.split('\n')
        
        annotations = []
        for line in reversed(lines):
            line = line.strip()
            if not line or line.endswith('{') or line.endswith(';'):
                break
            if line.startswith('@'):
                for match in self.annotation_pattern.finditer(line):
                    annotations.insert(0, match.group(1))
        
        return annotations
    
    def _extract_modifiers_at_position(self, content: str, position: int) -> List[str]:
        """Extract modifiers at a specific position."""
        before_position = content[:position]
        lines = before_position.split('\n')
        
        modifiers = []
        for line in reversed(lines):
            line = line.strip()
            if not line or line.endswith('{') or line.endswith(';'):
                break
            if line.startswith('@'):
                continue
            # Extract common modifiers
            modifier_keywords = ['public', 'private', 'protected', 'static', 'final', 
                               'abstract', 'synchronized', 'volatile', 'transient', 'native']
            for keyword in modifier_keywords:
                if keyword in line:
                    modifiers.insert(0, keyword)
        
        return modifiers
    
    def _extract_comments_at_position(self, content: str, position: int) -> str:
        """Extract comments at a specific position."""
        before_position = content[:position]
        lines = before_position.split('\n')
        
        comments = []
        for line in reversed(lines):
            line = line.strip()
            if not line:
                continue
            if line.startswith('//'):
                comments.insert(0, line[2:].strip())
            elif line.startswith('/*') and line.endswith('*/'):
                comment = line[2:-2].strip()
                comments.insert(0, comment)
            else:
                break
        
        return '\n'.join(comments)
    
    def _extract_methods(self, content: str, class_name: str) -> List[JavaMethod]:
        """Extract methods from a class."""
        methods = []
        
        # Find class boundaries
        class_start = content.find(f'class {class_name}')
        if class_start == -1:
            return methods
        
        # Find opening brace
        brace_start = content.find('{', class_start)
        if brace_start == -1:
            return methods
        
        # Find matching closing brace
        brace_count = 1
        i = brace_start + 1
        while i < len(content) and brace_count > 0:
            if content[i] == '{':
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
            i += 1
        
        class_content = content[brace_start:i-1]
        
        for match in self.method_pattern.finditer(class_content):
            return_type = match.group(1)
            method_name = match.group(2)
            
            # Skip constructors
            if method_name == class_name:
                continue
            
            # Extract parameters (simplified)
            method_start = match.start()
            paren_start = class_content.find('(', method_start)
            paren_end = class_content.find(')', paren_start)
            param_str = class_content[paren_start+1:paren_end]
            
            parameters = self._parse_parameters(param_str)
            
            # Extract annotations and modifiers
            annotations = self._extract_annotations_at_position(class_content, method_start)
            modifiers = self._extract_modifiers_at_position(class_content, method_start)
            comments = self._extract_comments_at_position(class_content, method_start)
            
            method = JavaMethod(
                name=method_name,
                return_type=return_type,
                parameters=parameters,
                modifiers=modifiers,
                annotations=annotations,
                comments=comments
            )
            methods.append(method)
        
        return methods
    
    def _extract_fields(self, content: str, class_name: str) -> List[JavaField]:
        """Extract fields from a class."""
        fields = []
        
        # Find class boundaries (same as methods)
        class_start = content.find(f'class {class_name}')
        if class_start == -1:
            return fields
        
        brace_start = content.find('{', class_start)
        if brace_start == -1:
            return fields
        
        # Find matching closing brace
        brace_count = 1
        i = brace_start + 1
        while i < len(content) and brace_count > 0:
            if content[i] == '{':
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
            i += 1
        
        class_content = content[brace_start:i-1]
        
        for match in self.field_pattern.finditer(class_content):
            field_type = match.group(1)
            field_name = match.group(2)
            
            field_start = match.start()
            annotations = self._extract_annotations_at_position(class_content, field_start)
            modifiers = self._extract_modifiers_at_position(class_content, field_start)
            comments = self._extract_comments_at_position(class_content, field_start)
            
            field = JavaField(
                name=field_name,
                type=field_type,
                modifiers=modifiers,
                annotations=annotations,
                comments=comments
            )
            fields.append(field)
        
        return fields
    
    def _extract_inheritance(self, content: str, class_start: int) -> tuple[Optional[str], List[str]]:
        """Extract extends and implements clauses."""
        # Find the line containing the class declaration
        lines = content[:class_start].split('\n')
        class_line = lines[-1] if lines else ""
        
        extends = None
        implements = []
        
        if 'extends' in class_line:
            extends_match = re.search(r'extends\s+(\w+)', class_line)
            if extends_match:
                extends = extends_match.group(1)
        
        if 'implements' in class_line:
            implements_match = re.search(r'implements\s+([^{]+)', class_line)
            if implements_match:
                implements = [imp.strip() for imp in implements_match.group(1).split(',')]
        
        return extends, implements
    
    def _parse_parameters(self, param_str: str) -> List[Dict[str, str]]:
        """Parse method parameters."""
        if not param_str.strip():
            return []
        
        parameters = []
        for param in param_str.split(','):
            param = param.strip()
            if param:
                parts = param.split()
                if len(parts) >= 2:
                    param_type = parts[-2]
                    param_name = parts[-1]
                    parameters.append({
                        'name': param_name,
                        'type': param_type
                    })
        
        return parameters
    
    def _extract_comments(self, content: str) -> str:
        """Extract all comments from the file."""
        comments = []
        
        # Extract block comments
        for match in self.comment_pattern.finditer(content):
            comment = match.group(0)[2:-2].strip()
            comments.append(comment)
        
        # Extract line comments
        for match in self.line_comment_pattern.finditer(content):
            comment = match.group(0)[2:].strip()
            comments.append(comment)
        
        return '\n'.join(comments)
    
    def _calculate_complexity(self, content: str) -> int:
        """Calculate a simple complexity score."""
        # Count control flow statements
        complexity_keywords = ['if', 'else', 'for', 'while', 'do', 'switch', 'case', 'catch', 'try']
        complexity = 1  # Base complexity
        
        for keyword in complexity_keywords:
            complexity += len(re.findall(rf'\b{keyword}\b', content))
        
        return complexity
    
    def _extract_business_hints(self, content: str) -> Dict[str, Any]:
        """Extract business logic hints from the code."""
        hints = {
            'validation_rules': [],
            'feature_flags': [],
            'roles_permissions': [],
            'domain_entities': []
        }
        
        # Look for validation annotations
        validation_patterns = [
            r'@Valid\w*',
            r'@NotNull\w*',
            r'@NotEmpty\w*',
            r'@Size\w*',
            r'@Pattern\w*'
        ]
        for pattern in validation_patterns:
            for match in re.finditer(pattern, content):
                hints['validation_rules'].append(match.group(0))
        
        # Look for feature flags
        feature_flag_patterns = [
            r'feature\.\w+',
            r'flag\.\w+',
            r'isEnabled\w*',
            r'isFeatureEnabled\w*'
        ]
        for pattern in feature_flag_patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                hints['feature_flags'].append(match.group(0))
        
        # Look for role/permission patterns
        role_patterns = [
            r'@PreAuthorize\w*',
            r'@Secured\w*',
            r'hasRole\w*',
            r'hasPermission\w*',
            r'ROLE_\w+'
        ]
        for pattern in role_patterns:
            for match in re.finditer(pattern, content):
                hints['roles_permissions'].append(match.group(0))
        
        # Look for domain entities (simplified)
        entity_patterns = [
            r'@Entity\w*',
            r'@Table\w*',
            r'class\s+(\w*Entity\w*)',
            r'class\s+(\w*Model\w*)',
            r'class\s+(\w*DTO\w*)'
        ]
        for pattern in entity_patterns:
            for match in re.finditer(pattern, content):
                hints['domain_entities'].append(match.group(0))
        
        return hints
    
    def _class_to_dict(self, java_class: JavaClass) -> Dict[str, Any]:
        """Convert JavaClass to dictionary."""
        return {
            'name': java_class.name,
            'type': java_class.type,
            'package': java_class.package,
            'imports': java_class.imports,
            'annotations': java_class.annotations,
            'methods': [
                {
                    'name': method.name,
                    'return_type': method.return_type,
                    'parameters': method.parameters,
                    'modifiers': method.modifiers,
                    'annotations': method.annotations,
                    'comments': method.comments
                }
                for method in java_class.methods
            ],
            'fields': [
                {
                    'name': field.name,
                    'type': field.type,
                    'modifiers': field.modifiers,
                    'annotations': field.annotations,
                    'comments': field.comments
                }
                for field in java_class.fields
            ],
            'extends': java_class.extends,
            'implements': java_class.implements or [],
            'modifiers': java_class.modifiers or [],
            'comments': java_class.comments
        }
