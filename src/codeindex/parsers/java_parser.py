"""
Java source file parser.

Extracts structural information from Java files including:
- Package declarations
- Import statements
- Classes and interfaces
- Methods and their signatures
- Annotations
"""

import re
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict

logger = logging.getLogger(__name__)


# ==============================================================================
# Data Structures
# ==============================================================================

@dataclass
class JavaElement:
    """Base class for Java code elements."""
    name: str
    type: str
    modifiers: List[str] = field(default_factory=list)
    annotations: List[str] = field(default_factory=list)
    line_number: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class JavaMethod(JavaElement):
    """Represents a Java method."""
    return_type: Optional[str] = None
    parameters: List[str] = field(default_factory=list)
    is_static: bool = False
    is_abstract: bool = False

    def __post_init__(self):
        """Set flags from modifiers."""
        if 'static' in self.modifiers:
            self.is_static = True
        if 'abstract' in self.modifiers:
            self.is_abstract = True


@dataclass
class JavaClass(JavaElement):
    """Represents a Java class or interface."""
    methods: List[JavaMethod] = field(default_factory=list)
    fields: List[str] = field(default_factory=list)
    is_abstract: bool = False
    is_interface: bool = False

    def __post_init__(self):
        """Set flags from modifiers."""
        if 'abstract' in self.modifiers:
            self.is_abstract = True
        if self.type == 'interface':
            self.is_interface = True


# ==============================================================================
# Regular Expressions
# ==============================================================================

# Package declaration
PACKAGE_PATTERN = re.compile(
    r'^\s*package\s+([\w.]+)\s*;',
    re.MULTILINE
)

# Import statements (including static)
IMPORT_PATTERN = re.compile(
    r'^\s*import\s+(?:static\s+)?([\w.*]+)\s*;',
    re.MULTILINE
)

# Class/Interface/Enum declaration
CLASS_PATTERN = re.compile(
    r'^\s*'
    r'(?:((?:@\w+(?:\([^)]*\))?\s+)*)'  # Annotations (group 1)
    r'((?:public|private|protected|static|final|abstract|strictfp)\s+)*)'  # Modifiers (group 2)
    r'(class|interface|enum)\s+'  # Type (group 3)
    r'(\w+)'  # Name (group 4)
    r'(?:<[^>]+>)?'  # Optional generics
    r'(?:\s+extends\s+[\w.<>,\s]+)?'  # Optional extends
    r'(?:\s+implements\s+[\w.<>,\s]+)?'  # Optional implements
    r'\s*\{',
    re.MULTILINE
)

# Method declaration
METHOD_PATTERN = re.compile(
    r'^\s*'
    r'(?:((?:@\w+(?:\([^)]*\))?\s+)*)'  # Annotations (group 1)
    r'((?:public|private|protected|static|final|abstract|synchronized|native|strictfp|default)\s+)*)'  # Modifiers (group 2)
    r'(?:<[^>]+>\s+)?'  # Optional generic type parameters
    r'([\w.<>,\[\]\s]+)\s+'  # Return type (group 3)
    r'(\w+)\s*'  # Method name (group 4)
    r'\(([^)]*)\)'  # Parameters (group 5)
    r'(?:\s*throws\s+[\w.,\s]+)?'  # Optional throws
    r'\s*[{;]',
    re.MULTILINE
)

# Annotation
ANNOTATION_PATTERN = re.compile(
    r'@(\w+)(?:\([^)]*\))?',
    re.MULTILINE
)

# Constructor pattern (for filtering out from methods)
CONSTRUCTOR_PATTERN = re.compile(
    r'^\s*'
    r'(?:public|private|protected)?\s*'
    r'(\w+)\s*\([^)]*\)\s*\{',
    re.MULTILINE
)

# Comments (for removal)
SINGLE_LINE_COMMENT = re.compile(r'//.*?$', re.MULTILINE)
MULTI_LINE_COMMENT = re.compile(r'/\*.*?\*/', re.DOTALL)
JAVADOC_COMMENT = re.compile(r'/\*\*.*?\*/', re.DOTALL)


# ==============================================================================
# JavaParser Class
# ==============================================================================

class JavaParser:
    """
    Parser for Java source files.

    Extracts structural information using regex patterns.
    """

    def __init__(self):
        """Initialize Java parser."""
        self.logger = logging.getLogger(__name__)

    def parse_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Parse a Java file.

        Args:
            file_path: Path to Java file

        Returns:
            Dictionary with parsed elements

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Java file not found: {file_path}")

        content = file_path.read_text(encoding='utf-8')
        return self.parse(content)

    def parse(self, content: str) -> Dict[str, Any]:
        """
        Parse Java source code.

        Args:
            content: Java source code as string

        Returns:
            Dictionary with structural information
        """
        try:
            # Remove comments first to avoid false matches
            cleaned_content = self._remove_comments(content)

            # Extract all elements
            result = {
                'package': self.extract_package(cleaned_content),
                'imports': self.extract_imports(cleaned_content),
                'annotations': self.extract_annotations(content),  # Use original for annotations
                'classes': [],
                'interfaces': [],
                'methods': [],
            }

            # Extract classes and interfaces
            classes = self.extract_classes(cleaned_content)
            for cls in classes:
                if cls['type'] == 'interface':
                    result['interfaces'].append(cls)
                else:
                    result['classes'].append(cls)

            # Extract methods
            result['methods'] = self.extract_methods(cleaned_content)

            return result

        except Exception as e:
            self.logger.error(f"Error parsing Java code: {e}", exc_info=True)
            # Return minimal result on error
            return {
                'package': None,
                'imports': [],
                'annotations': [],
                'classes': [],
                'interfaces': [],
                'methods': [],
                'parse_error': str(e)
            }

    def _remove_comments(self, content: str) -> str:
        """
        Remove comments from Java code.

        Args:
            content: Java source code

        Returns:
            Code without comments
        """
        # Remove single-line comments
        content = SINGLE_LINE_COMMENT.sub('', content)
        # Remove multi-line comments
        content = MULTI_LINE_COMMENT.sub('', content)
        # Remove JavaDoc comments
        content = JAVADOC_COMMENT.sub('', content)

        return content

    def extract_package(self, content: str) -> Optional[str]:
        """
        Extract package declaration.

        Args:
            content: Java source code

        Returns:
            Package name or None
        """
        match = PACKAGE_PATTERN.search(content)
        if match:
            return match.group(1)
        return None

    def extract_imports(self, content: str) -> List[str]:
        """
        Extract import statements.

        Args:
            content: Java source code

        Returns:
            List of imported packages/classes
        """
        matches = IMPORT_PATTERN.findall(content)
        return list(matches)

    def extract_classes(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract class and interface declarations.

        Args:
            content: Java source code

        Returns:
            List of class/interface information
        """
        classes = []

        for match in CLASS_PATTERN.finditer(content):
            annotations_str = match.group(1) or ''
            modifiers_str = match.group(2) or ''
            class_type = match.group(3)  # class, interface, or enum
            class_name = match.group(4)

            # Parse modifiers
            modifiers = [m.strip() for m in modifiers_str.split() if m.strip()]

            # Parse annotations
            annotations = ANNOTATION_PATTERN.findall(annotations_str)

            class_info = {
                'name': class_name,
                'type': class_type,
                'modifiers': modifiers,
                'annotations': annotations,
                'is_abstract': 'abstract' in modifiers,
            }

            classes.append(class_info)

        return classes

    def extract_interfaces(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract interface declarations.

        Args:
            content: Java source code

        Returns:
            List of interface information
        """
        all_classes = self.extract_classes(content)
        return [c for c in all_classes if c['type'] == 'interface']

    def extract_methods(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract method declarations.

        Args:
            content: Java source code

        Returns:
            List of method information
        """
        methods = []

        # Get class names to filter out constructors
        class_names = set()
        for cls in self.extract_classes(content):
            class_names.add(cls['name'])

        for match in METHOD_PATTERN.finditer(content):
            annotations_str = match.group(1) or ''
            modifiers_str = match.group(2) or ''
            return_type = match.group(3).strip()
            method_name = match.group(4)
            parameters_str = match.group(5) or ''

            # Skip constructors (methods with same name as class)
            if method_name in class_names:
                continue

            # Parse modifiers
            modifiers = [m.strip() for m in modifiers_str.split() if m.strip()]

            # Parse annotations
            annotations = ANNOTATION_PATTERN.findall(annotations_str)

            # Parse parameters
            parameters = []
            if parameters_str.strip():
                # Split by comma, handling generics
                param_parts = self._split_parameters(parameters_str)
                for param in param_parts:
                    param = param.strip()
                    if param:
                        parameters.append(param)

            method_info = {
                'name': method_name,
                'return_type': return_type,
                'parameters': parameters,
                'modifiers': modifiers,
                'annotations': annotations,
                'is_static': 'static' in modifiers,
                'is_abstract': 'abstract' in modifiers,
            }

            methods.append(method_info)

        return methods

    def _split_parameters(self, params_str: str) -> List[str]:
        """
        Split parameter string by comma, handling generics.

        Args:
            params_str: Parameter string

        Returns:
            List of parameter declarations
        """
        parameters = []
        current_param = []
        depth = 0  # Track generic depth

        for char in params_str:
            if char == '<':
                depth += 1
                current_param.append(char)
            elif char == '>':
                depth -= 1
                current_param.append(char)
            elif char == ',' and depth == 0:
                # Split here
                param = ''.join(current_param).strip()
                if param:
                    parameters.append(param)
                current_param = []
            else:
                current_param.append(char)

        # Add last parameter
        param = ''.join(current_param).strip()
        if param:
            parameters.append(param)

        return parameters

    def extract_annotations(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract annotations from code.

        Args:
            content: Java source code

        Returns:
            List of annotation information
        """
        annotations = []
        seen = set()  # Avoid duplicates

        for match in ANNOTATION_PATTERN.finditer(content):
            annotation_name = match.group(1)

            if annotation_name not in seen:
                seen.add(annotation_name)
                annotations.append({
                    'name': annotation_name,
                    'full_text': match.group(0)
                })

        return annotations


# ==============================================================================
# Standalone Functions
# ==============================================================================

def parse_java_file(file_path: Path) -> Dict[str, Any]:
    """
    Parse a Java file (convenience function).

    Args:
        file_path: Path to Java file

    Returns:
        Dictionary with parsed elements
    """
    parser = JavaParser()
    return parser.parse_file(file_path)


def extract_package(content: str) -> Optional[str]:
    """
    Extract package declaration (convenience function).

    Args:
        content: Java source code

    Returns:
        Package name or None
    """
    parser = JavaParser()
    return parser.extract_package(content)


def extract_imports(content: str) -> List[str]:
    """
    Extract import statements (convenience function).

    Args:
        content: Java source code

    Returns:
        List of imported packages/classes
    """
    parser = JavaParser()
    return parser.extract_imports(content)


def extract_classes(content: str) -> List[Dict[str, Any]]:
    """
    Extract class declarations (convenience function).

    Args:
        content: Java source code

    Returns:
        List of class information
    """
    parser = JavaParser()
    return parser.extract_classes(content)


def extract_interfaces(content: str) -> List[Dict[str, Any]]:
    """
    Extract interface declarations (convenience function).

    Args:
        content: Java source code

    Returns:
        List of interface information
    """
    parser = JavaParser()
    return parser.extract_interfaces(content)


def extract_methods(content: str) -> List[Dict[str, Any]]:
    """
    Extract method declarations (convenience function).

    Args:
        content: Java source code

    Returns:
        List of method information
    """
    parser = JavaParser()
    return parser.extract_methods(content)


def extract_annotations(content: str) -> List[Dict[str, Any]]:
    """
    Extract annotations (convenience function).

    Args:
        content: Java source code

    Returns:
        List of annotation information
    """
    parser = JavaParser()
    return parser.extract_annotations(content)
