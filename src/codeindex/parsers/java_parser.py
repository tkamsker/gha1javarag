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


# ==============================================================================
# Validation Annotation Extraction (T055-T057)
# ==============================================================================

def extract_validation_annotations(file_path: Path) -> List[Dict[str, Any]]:
    """
    Extract JSR-303 validation annotations from Java file (T055-T057).

    Supports:
    - @NotNull
    - @NotEmpty
    - @NotBlank
    - @Size(min=, max=)
    - @Min(value=)
    - @Max(value=)
    - @Pattern(regexp=)
    - @Email
    - @Valid (for nested DTOs)

    Args:
        file_path: Path to Java source file

    Returns:
        List of validation annotations with field names and parameters

    Example:
        >>> annotations = extract_validation_annotations(Path("UserDTO.java"))
        >>> print(annotations)
        [
            {'type': 'NotNull', 'field_name': 'username', 'parameters': {}},
            {'type': 'Size', 'field_name': 'password', 'parameters': {'min': 8, 'max': 50}}
        ]
    """
    if not file_path.exists():
        return []

    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception:
        return []

    annotations = []

    # Split content into lines for line-by-line processing
    lines = content.split('\n')

    # Pattern to match field declarations
    field_pattern = r'^\s*(?:private|protected|public)\s+(?:static\s+)?(?:final\s+)?([\w<>\[\],\s]+?)\s+(\w+)\s*[;=]'

    # Pattern to match annotations
    annotation_pattern = r'^\s*(@[\w]+(?:\([^)]*\))?)\s*$'

    # Iterate through lines to find fields and their annotations
    i = 0
    while i < len(lines):
        line = lines[i]

        # Check if this line is a field declaration
        field_match = re.match(field_pattern, line)
        if field_match:
            field_type = field_match.group(1).strip()
            field_name = field_match.group(2)

            # Look backward to collect all annotations for this field
            field_annotations = []
            j = i - 1
            while j >= 0:
                prev_line = lines[j].strip()

                # Check if previous line is an annotation
                ann_match = re.match(annotation_pattern, lines[j])
                if ann_match:
                    annotation_str = ann_match.group(1)
                    annotation_info = _parse_annotation(annotation_str, field_name)
                    if annotation_info:
                        field_annotations.insert(0, annotation_info)  # Insert at beginning to maintain order
                    j -= 1
                # Stop if we hit an empty line, comment, or non-annotation
                elif not prev_line or prev_line.startswith('//') or prev_line.startswith('/*'):
                    break
                else:
                    # Check if it's a multi-line annotation or other code
                    if not prev_line.startswith('@'):
                        break
                    j -= 1

            # Add all annotations for this field
            annotations.extend(field_annotations)

        i += 1

    return annotations


def _parse_annotation(annotation_str: str, field_name: str) -> Optional[Dict[str, Any]]:
    """
    Parse a single annotation string into structured data (T056-T057).

    Args:
        annotation_str: Annotation string (e.g., "@Size(min=8, max=50)")
        field_name: Name of the field being annotated

    Returns:
        Dictionary with annotation type, field name, and parameters
    """
    # Extract annotation type
    type_match = re.match(r'@(\w+)', annotation_str)
    if not type_match:
        return None

    annotation_type = type_match.group(1)

    # List of validation annotations we care about
    validation_annotations = {
        'NotNull', 'NotEmpty', 'NotBlank',
        'Size', 'Min', 'Max',
        'Pattern', 'Email', 'Valid',
        'Positive', 'Negative', 'DecimalMin', 'DecimalMax',
        'Future', 'Past', 'AssertTrue', 'AssertFalse'
    }

    if annotation_type not in validation_annotations:
        return None

    # Parse parameters if present
    parameters = {}

    # Check for parameters: @Size(min=8, max=50)
    params_match = re.search(r'\(([^)]+)\)', annotation_str)
    if params_match:
        params_str = params_match.group(1)
        parameters = _parse_annotation_parameters(params_str)

    return {
        'type': annotation_type,
        'field_name': field_name,
        'parameters': parameters
    }


def _parse_annotation_parameters(params_str: str) -> Dict[str, Any]:
    """
    Parse annotation parameters into dictionary (T057).

    Handles:
    - Simple values: min=8, max=50
    - String values: regexp="[A-Z]+"
    - Array values: groups={Group1.class, Group2.class}

    Args:
        params_str: Parameter string (e.g., "min=8, max=50")

    Returns:
        Dictionary of parameter names and values
    """
    parameters = {}

    # Pattern for key=value pairs
    # Handles: min=8, max=50, regexp="...", message="..."
    param_pattern = r'(\w+)\s*=\s*([^,]+?)(?:,|$)'

    matches = re.finditer(param_pattern, params_str)

    for match in matches:
        key = match.group(1).strip()
        value_str = match.group(2).strip()

        # Parse value based on type
        value = _parse_parameter_value(value_str)
        parameters[key] = value

    return parameters


def _parse_parameter_value(value_str: str) -> Any:
    """
    Parse a parameter value string into appropriate Python type.

    Args:
        value_str: Value string (e.g., "8", '"pattern"', 'true')

    Returns:
        Parsed value (int, str, bool, etc.)
    """
    value_str = value_str.strip()

    # String value (quoted)
    if value_str.startswith('"') and value_str.endswith('"'):
        return value_str[1:-1]  # Remove quotes

    # Boolean value
    if value_str.lower() == 'true':
        return True
    if value_str.lower() == 'false':
        return False

    # Integer value
    try:
        return int(value_str)
    except ValueError:
        pass

    # Float value
    try:
        return float(value_str)
    except ValueError:
        pass

    # Default: return as string
    return value_str


# ==============================================================================
# DTO Metadata Extraction (T058-T060)
# ==============================================================================

def extract_dto_metadata(file_path: Path) -> Dict[str, Any]:
    """
    Extract comprehensive DTO metadata from Java file (T058-T060).

    Extracts:
    - Class name and package
    - Field definitions with types and modifiers
    - Validation annotations per field
    - Nested DTO relationships
    - Inner class detection
    - Serialization markers

    Args:
        file_path: Path to Java source file

    Returns:
        Dictionary with complete DTO metadata

    Example:
        >>> metadata = extract_dto_metadata(Path("UserDTO.java"))
        >>> print(metadata['class_name'])
        'UserDTO'
        >>> print(len(metadata['fields']))
        7
    """
    from codeindex.models.dto_artifact import DtoField

    if not file_path.exists():
        return _empty_dto_metadata(file_path)

    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception:
        return _empty_dto_metadata(file_path)

    # Extract basic class info
    class_name = _extract_class_name_from_content(content, file_path)
    package_name = _extract_package_name_from_content(content)

    # Extract fields with their metadata (T058)
    fields = _extract_fields_with_metadata(content)

    # Extract validation annotations
    validation_annotations = extract_validation_annotations(file_path)

    # Map validation annotations to fields
    fields_with_validation = _attach_validation_to_fields(fields, validation_annotations)

    # Detect inner classes (T060)
    inner_classes = _detect_inner_classes(content)

    # Identify nested DTOs
    nested_dto_types = _identify_nested_dto_types(content)

    # Check for serialization markers
    serialization_markers = _extract_serialization_markers(content)

    return {
        'class_name': class_name,
        'package_name': package_name,
        'source_file': str(file_path),
        'fields': fields_with_validation,
        'field_count': len(fields_with_validation),
        'nested_dto_types': nested_dto_types,
        'inner_classes': inner_classes,
        'has_inner_classes': len(inner_classes) > 0,
        'serialization_markers': serialization_markers,
        'implements_serializable': 'Serializable' in serialization_markers
    }


def _empty_dto_metadata(file_path: Path) -> Dict[str, Any]:
    """Return empty metadata structure for error cases."""
    return {
        'class_name': file_path.stem,
        'package_name': None,
        'source_file': str(file_path),
        'fields': [],
        'field_count': 0,
        'nested_dto_types': [],
        'inner_classes': [],
        'has_inner_classes': False,
        'serialization_markers': [],
        'implements_serializable': False
    }


def _extract_class_name_from_content(content: str, file_path: Path) -> str:
    """Extract class name from content."""
    class_pattern = r'(?:public\s+)?class\s+(\w+)'
    match = re.search(class_pattern, content)
    return match.group(1) if match else file_path.stem


def _extract_package_name_from_content(content: str) -> Optional[str]:
    """Extract package name from content."""
    package_pattern = r'package\s+([\w.]+);'
    match = re.search(package_pattern, content)
    return match.group(1) if match else None


def _extract_fields_with_metadata(content: str) -> List[Dict[str, Any]]:
    """
    Extract field definitions with types and modifiers (T058).

    Returns list of field dictionaries with:
    - name: Field name
    - field_type: Java type
    - modifiers: List of modifiers (private, public, static, final, etc.)
    - is_collection: Boolean
    - collection_type: Type of collection (List, Set, Map)
    - generic_types: Generic type parameters
    """
    fields = []

    # Pattern to match field declarations
    # Matches: private String username;
    # Matches: private List<String> tags;
    # Matches: private final int id = 0;
    field_pattern = r'((?:private|protected|public)\s+(?:static\s+)?(?:final\s+)?)([\w<>\[\],\s]+?)\s+(\w+)\s*[;=]'

    matches = re.finditer(field_pattern, content, re.MULTILINE)

    for match in matches:
        modifiers_str = match.group(1).strip()
        field_type = match.group(2).strip()
        field_name = match.group(3)

        # Parse modifiers
        modifiers = [m for m in modifiers_str.split() if m in ['private', 'protected', 'public', 'static', 'final']]

        # Check if collection type
        is_collection, collection_type, generic_types = _parse_collection_type(field_type)

        # Check if nested DTO
        is_nested_dto = 'DTO' in field_type

        field_dict = {
            'name': field_name,
            'field_type': field_type,
            'modifiers': modifiers,
            'is_collection': is_collection,
            'collection_type': collection_type,
            'generic_types': generic_types,
            'is_nested_dto': is_nested_dto,
            'validation_annotations': []  # Will be populated later
        }

        fields.append(field_dict)

    return fields


def _parse_collection_type(field_type: str) -> tuple[bool, Optional[str], List[str]]:
    """
    Parse collection type and extract generic parameters.

    Args:
        field_type: Java type string (e.g., "List<String>", "Map<String, Integer>")

    Returns:
        Tuple of (is_collection, collection_type, generic_types)
    """
    collection_types = ['List', 'Set', 'Map', 'Collection', 'ArrayList', 'HashSet', 'HashMap']

    # Check if it's a collection
    is_collection = any(ctype in field_type for ctype in collection_types)

    if not is_collection:
        return False, None, []

    # Extract collection type
    collection_type = None
    for ctype in collection_types:
        if field_type.startswith(ctype):
            collection_type = ctype
            break

    # Extract generic types from <>
    generic_match = re.search(r'<(.+)>', field_type)
    if generic_match:
        generic_str = generic_match.group(1)
        # Split by comma, handling nested generics
        generic_types = [t.strip() for t in generic_str.split(',')]
    else:
        generic_types = []

    return True, collection_type, generic_types


def _attach_validation_to_fields(
    fields: List[Dict[str, Any]],
    validation_annotations: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Attach validation annotations to their corresponding fields.

    Args:
        fields: List of field dictionaries
        validation_annotations: List of validation annotation dictionaries

    Returns:
        Fields with validation_annotations populated
    """
    # Create lookup map
    validation_by_field = {}
    for ann in validation_annotations:
        field_name = ann['field_name']
        if field_name not in validation_by_field:
            validation_by_field[field_name] = []
        validation_by_field[field_name].append(ann)

    # Attach to fields
    for field in fields:
        field_name = field['name']
        if field_name in validation_by_field:
            field['validation_annotations'] = validation_by_field[field_name]

    return fields


def _detect_inner_classes(content: str) -> List[str]:
    """
    Detect inner class definitions (T060).

    Args:
        content: Java source content

    Returns:
        List of inner class names
    """
    inner_classes = []

    # Pattern for inner classes
    # Matches: public static class Address { ... }
    # Matches: private class Helper { ... }
    inner_class_pattern = r'(?:^|\s)(?:public|private|protected)?\s*(?:static\s+)?class\s+(\w+)\s*(?:\{|extends|implements)'

    matches = re.finditer(inner_class_pattern, content, re.MULTILINE)

    for match in matches:
        class_name = match.group(1)
        inner_classes.append(class_name)

    # Remove the main class name (first match is usually the main class)
    if inner_classes:
        inner_classes = inner_classes[1:]  # Skip first (main class)

    return inner_classes


def _identify_nested_dto_types(content: str) -> List[str]:
    """
    Identify nested DTO type names in fields.

    Args:
        content: Java source content

    Returns:
        List of DTO type names used in fields
    """
    nested_types = []

    # Pattern for fields with DTO types
    dto_field_pattern = r'(?:private|protected|public)\s+([\w<>]+DTO[\w<>]*)\s+\w+\s*[;=]'

    matches = re.finditer(dto_field_pattern, content)

    for match in matches:
        dto_type = match.group(1)
        # Extract DTO type name (handle generics)
        dto_type_clean = re.sub(r'<.*?>', '', dto_type)
        nested_types.append(dto_type_clean)

    # Also check generic parameters
    generic_dto_pattern = r'<([\w]+DTO[\w]*)>'
    generic_matches = re.finditer(generic_dto_pattern, content)

    for match in generic_matches:
        dto_type = match.group(1)
        nested_types.append(dto_type)

    # Remove duplicates and sort
    nested_types = sorted(set(nested_types))

    return nested_types


def _extract_serialization_markers(content: str) -> List[str]:
    """
    Extract serialization marker names from content.

    Returns list of marker names found (e.g., ['Serializable', 'JsonProperty'])
    """
    markers = []

    serialization_indicators = {
        'Serializable': 'implements.*Serializable',
        'JsonProperty': '@JsonProperty',
        'JsonIgnore': '@JsonIgnore',
        'JsonSerialize': '@JsonSerialize',
        'JsonDeserialize': '@JsonDeserialize',
        'XmlRootElement': '@XmlRootElement',
        'XmlElement': '@XmlElement',
        'XmlAccessorType': '@XmlAccessorType'
    }

    for marker_name, pattern in serialization_indicators.items():
        if re.search(pattern, content):
            markers.append(marker_name)

    return markers
