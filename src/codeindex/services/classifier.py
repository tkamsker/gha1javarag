"""
File classifier service.

Classifies source code files based on extensions, paths, and naming patterns
to determine their artifact type (Java source, test, JSP, SQL, etc.).
"""

import logging
import re
from pathlib import Path
from typing import Union, Optional, List, Dict, Any

from codeindex.models import ArtifactType
from codeindex.models.dto_artifact import ClassificationResult

logger = logging.getLogger(__name__)


# Path patterns for different artifact types
TEST_PATH_PATTERNS = [
    r'(^|/)src/test/',          # Unix-style (absolute or relative)
    r'(^|/)src/tests/',
    r'(^|\\)src\\test\\',       # Windows-style
    r'(^|\\)src\\tests\\',
]

SOURCE_PATH_PATTERNS = [
    r'/src/main/java/',
    r'\\src\\main\\java\\',
]

RESOURCE_PATH_PATTERNS = [
    r'/src/main/resources/',
    r'\\src\\main\\resources\\',
]

TEMPLATES_PATH_PATTERNS = [
    r'/templates/',
    r'\\templates\\',
]

WEBAPP_PATH_PATTERNS = [
    r'/webapp/',
    r'/WEB-INF/',
    r'\\webapp\\',
    r'\\WEB-INF\\',
]


def _matches_pattern(path: Path, patterns: list) -> bool:
    """Check if path matches any of the given patterns."""
    path_str = str(path)
    for pattern in patterns:
        if re.search(pattern, path_str):
            return True
    return False


def is_java_source(path: Path) -> bool:
    """
    Check if file is a Java source file (not test).

    Args:
        path: File path to check

    Returns:
        True if Java source file
    """
    if path.suffix.lower() != '.java':
        return False

    # Exclude test files
    if is_java_test(path):
        return False

    return True


def is_java_test(path: Path) -> bool:
    """
    Check if file is a Java test file.

    Args:
        path: File path to check

    Returns:
        True if Java test file
    """
    if path.suffix.lower() != '.java':
        return False

    # Check for test path patterns
    if _matches_pattern(path, TEST_PATH_PATTERNS):
        return True

    # Check for test file naming conventions
    stem = path.stem
    test_suffixes = ['Test', 'Tests', 'TestCase']

    # Files ending with Test/Tests/TestCase are test files
    for suffix in test_suffixes:
        if stem.endswith(suffix):
            return True

    # Files starting with Test are tests ONLY if they end with Test/Tests
    # (e.g., TestRunner is a test, but TestUtils is not)
    if stem.startswith('Test'):
        # Check if it ends with a test suffix (already checked above)
        # Or if it's a simple pattern like "TestSomething" (no Utils, Helper, Base, etc.)
        utility_keywords = ['Utils', 'Util', 'Helper', 'Support', 'Base', 'Abstract']
        is_utility = any(keyword in stem for keyword in utility_keywords)
        if not is_utility:
            return True

    return False


def is_jsp_file(path: Path) -> bool:
    """
    Check if file is a JSP file.

    Args:
        path: File path to check

    Returns:
        True if JSP file
    """
    jsp_extensions = ['.jsp', '.jspx', '.jspf']
    return path.suffix.lower() in jsp_extensions


def is_xml_config(path: Path) -> bool:
    """
    Check if file is an XML configuration file (not POM).

    Args:
        path: File path to check

    Returns:
        True if XML configuration file
    """
    if path.suffix.lower() != '.xml':
        return False

    # Exclude pom.xml
    if path.name.lower() == 'pom.xml':
        return False

    # Check for config file locations
    config_locations = [
        r'(^|/)resources/',
        r'(^|/)config/',
        r'(^|/)WEB-INF/',
        r'(^|/)META-INF/',
        r'(^|\\)resources\\',
        r'(^|\\)config\\',
        r'(^|\\)WEB-INF\\',
        r'(^|\\)META-INF\\',
    ]

    if _matches_pattern(path, config_locations):
        return True

    # Check for common config file names
    config_names = [
        'applicationcontext',
        'spring',
        'beans',
        'persistence',
        'mybatis',
        'ibatis',
        'web',
        'struts',
        'hibernate',
    ]

    filename_lower = path.stem.lower()
    for config_name in config_names:
        if config_name in filename_lower:
            return True

    return False


def is_sql_file(path: Path) -> bool:
    """
    Check if file is a SQL file.

    Args:
        path: File path to check

    Returns:
        True if SQL file
    """
    return path.suffix.lower() == '.sql'


def is_sql_schema(path: Path) -> bool:
    """
    Check if SQL file is a schema/DDL file.

    Args:
        path: File path to check

    Returns:
        True if SQL schema file
    """
    if not is_sql_file(path):
        return False

    schema_keywords = [
        'schema',
        'create',
        'ddl',
        'table',
        'migration',
    ]

    filename_lower = path.stem.lower()
    for keyword in schema_keywords:
        if keyword in filename_lower:
            return True

    return False


def is_sql_query(path: Path) -> bool:
    """
    Check if SQL file is a query file.

    Args:
        path: File path to check

    Returns:
        True if SQL query file
    """
    if not is_sql_file(path):
        return False

    # If not schema, likely queries
    if not is_sql_schema(path):
        return True

    return False


def is_html_template(path: Path) -> bool:
    """
    Check if file is an HTML template.

    Args:
        path: File path to check

    Returns:
        True if HTML template file
    """
    if path.suffix.lower() not in ['.html', '.htm']:
        return False

    # Check if in templates directory
    if _matches_pattern(path, TEMPLATES_PATH_PATTERNS):
        return True

    # Check for template keywords in path
    template_keywords = ['template', 'view']
    path_lower = str(path).lower()
    for keyword in template_keywords:
        if keyword in path_lower:
            return True

    return False


def is_properties_file(path: Path) -> bool:
    """
    Check if file is a properties file.

    Args:
        path: File path to check

    Returns:
        True if properties file
    """
    return path.suffix.lower() == '.properties'


def is_javascript(path: Path) -> bool:
    """
    Check if file is a JavaScript file.

    Args:
        path: File path to check

    Returns:
        True if JavaScript file
    """
    js_extensions = ['.js', '.mjs', '.jsx']
    return path.suffix.lower() in js_extensions


def is_gwt_module(path: Path) -> bool:
    """
    Check if file is a GWT module XML.

    Args:
        path: File path to check

    Returns:
        True if GWT module file
    """
    if path.suffix.lower() != '.xml':
        return False

    # GWT modules end with .gwt.xml
    return '.gwt.xml' in path.name.lower()


def is_gwt_ui_binder(path: Path) -> bool:
    """
    Check if file is a GWT UiBinder XML template.

    Args:
        path: File path to check

    Returns:
        True if GWT UiBinder template file
    """
    if path.suffix.lower() != '.xml':
        return False

    # UiBinder templates end with .ui.xml
    return '.ui.xml' in path.name.lower()


def get_artifact_type(path: Path) -> ArtifactType:
    """
    Determine artifact type for a file.

    Args:
        path: File path to classify

    Returns:
        ArtifactType enum value
    """
    # Check in order of specificity
    if is_java_test(path):
        return ArtifactType.JAVA_TEST

    if is_java_source(path):
        return ArtifactType.JAVA_SOURCE

    if is_gwt_module(path):
        return ArtifactType.GWT_MODULE

    if is_gwt_ui_binder(path):
        return ArtifactType.GWT_UI_BINDER

    if is_jsp_file(path):
        return ArtifactType.JSP_VIEW

    if is_xml_config(path):
        return ArtifactType.XML_CONFIG

    if is_sql_schema(path):
        return ArtifactType.SQL_SCHEMA

    if is_sql_query(path):
        return ArtifactType.SQL_QUERY

    if is_html_template(path):
        return ArtifactType.HTML_TEMPLATE

    if is_properties_file(path):
        return ArtifactType.PROPERTIES_FILE

    if is_javascript(path):
        return ArtifactType.JS_SCRIPT

    # Additional types - map to existing enum values
    suffix = path.suffix.lower()

    # Static assets (CSS, images, fonts, videos, etc.)
    if suffix == '.css':
        return ArtifactType.STATIC_ASSET

    # Image files
    if suffix in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.bmp', '.webp', '.tiff', '.tif', '.pspimage', '.psd', '.ai', '.sketch']:
        return ArtifactType.STATIC_ASSET

    # Video and audio files
    if suffix in ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv', '.mp3', '.wav', '.ogg', '.m4a']:
        return ArtifactType.STATIC_ASSET

    # Font files
    if suffix in ['.ttf', '.otf', '.woff', '.woff2', '.eot']:
        return ArtifactType.STATIC_ASSET

    # Binary and compiled files
    if suffix in ['.class', '.jar', '.war', '.ear', '.zip', '.tar', '.gz', '.7z', '.rar']:
        return ArtifactType.STATIC_ASSET

    # Office documents
    if suffix in ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']:
        return ArtifactType.STATIC_ASSET

    # Configuration and data files
    if suffix == '.json':
        return ArtifactType.XML_CONFIG  # JSON config files

    if suffix in ['.yml', '.yaml']:
        return ArtifactType.XML_CONFIG  # YAML config files

    if suffix == '.md':
        return ArtifactType.OTHER_TEXT  # Documentation

    # Default fallback for unknown types
    return ArtifactType.OTHER_TEXT


class FileClassifier:
    """
    File classifier for determining artifact types.

    Classifies files based on extensions, paths, and naming patterns.
    """

    def __init__(self):
        """Initialize file classifier."""
        self.logger = logging.getLogger(__name__)

    def classify(self, path: Union[Path, str]) -> ArtifactType:
        """
        Classify a file and return its artifact type.

        Args:
            path: File path to classify (Path object or string)

        Returns:
            ArtifactType enum value
        """
        if isinstance(path, str):
            path = Path(path)

        artifact_type = get_artifact_type(path)

        self.logger.debug(f"Classified {path.name} as {artifact_type.value}")

        return artifact_type


# Convenience function for external use
def classify_file(path: Union[Path, str]) -> ArtifactType:
    """
    Classify a file (convenience function).

    Args:
        path: File path to classify

    Returns:
        ArtifactType enum value
    """
    classifier = FileClassifier()
    return classifier.classify(path)


# ===================================================================
# DTO Classification Functions (T049-T054)
# ===================================================================

def classify_dto(file_path: Path) -> 'ClassificationResult':
    """
    Classify a Java file as DTO using 5-phase scoring system (T049-T054).

    5-Phase Classification:
    - Phase 1: Naming pattern match (80 points max)
    - Phase 2: Entity exclusion check (disqualifying)
    - Phase 3: Structural analysis (field-to-method ratio)
    - Phase 4: Serialization marker detection (10 points max)
    - Phase 5: Package location heuristics (15 points max)

    Threshold: confidence >= 70 for DTO classification.

    Args:
        file_path: Path to Java source file

    Returns:
        ClassificationResult with confidence scoring

    Example:
        >>> result = classify_dto(Path("UserDTO.java"))
        >>> print(f"Is DTO: {result.is_dto}, Confidence: {result.confidence}")
        Is DTO: True, Confidence: 95.0
    """
    # Initialize scores
    naming_score = 0.0
    structural_score = 0.0
    serialization_score = 0.0
    package_score = 0.0

    # Initialize flags
    entity_markers_found = False
    serialization_markers_found = False
    nested_dtos_found = False

    # Initialize metadata
    field_count = 0
    method_count = 0
    nested_dto_types = []
    package_name = None
    class_name = None

    # Read file content
    if not file_path.exists():
        # Return negative result for non-existent files
        return ClassificationResult(
            is_dto=False,
            confidence=0.0,
            class_name=file_path.stem
        )

    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception:
        return ClassificationResult(
            is_dto=False,
            confidence=0.0,
            class_name=file_path.stem
        )

    # Extract class name from file
    class_name = _extract_class_name(content, file_path)

    # Extract package name
    package_name = _extract_package_name(content)

    # Phase 1: Naming pattern match (T049) - 80 points
    naming_score = _score_naming_pattern(class_name)

    # Phase 2: Entity exclusion check (T050) - Disqualifying
    entity_markers_found = _has_entity_markers(content)
    if entity_markers_found:
        # Entity markers disqualify - return immediately with all scores at 0
        return ClassificationResult(
            is_dto=False,
            confidence=0.0,
            naming_pattern_score=0.0,
            entity_markers_found=True,
            class_name=class_name,
            package_name=package_name
        )

    # Phase 3: Structural analysis (T051) - Variable score
    field_count, method_count = _count_fields_and_methods(content)
    structural_score = _score_structural_analysis(field_count, method_count)

    # Phase 4: Serialization marker detection (T052) - 10 points
    serialization_markers_found = _has_serialization_markers(content)
    if serialization_markers_found:
        serialization_score = 10.0

    # Phase 5: Package location heuristics (T053) - 15 points
    package_score = _score_package_location(package_name)

    # Identify nested DTOs (T059)
    nested_dto_types = _identify_nested_dtos(content)
    nested_dtos_found = len(nested_dto_types) > 0

    # Calculate total confidence (T054)
    total_confidence = min(
        naming_score + structural_score + serialization_score + package_score,
        100.0
    )

    # Threshold decision: confidence >= 70 (T054)
    is_dto = total_confidence >= 70.0

    return ClassificationResult(
        is_dto=is_dto,
        confidence=total_confidence,
        naming_pattern_score=naming_score,
        structural_score=structural_score,
        serialization_score=serialization_score,
        package_score=package_score,
        entity_markers_found=entity_markers_found,
        serialization_markers_found=serialization_markers_found,
        nested_dtos_found=nested_dtos_found,
        field_count=field_count,
        method_count=method_count,
        nested_dto_types=nested_dto_types,
        nested_dto_count=len(nested_dto_types),
        package_name=package_name,
        class_name=class_name
    )


def _extract_class_name(content: str, file_path: Path) -> str:
    """Extract class name from Java source content."""
    import re

    # Try to find class declaration
    class_pattern = r'(?:public\s+)?class\s+(\w+)'
    match = re.search(class_pattern, content)

    if match:
        return match.group(1)

    # Fallback to filename
    return file_path.stem


def _extract_package_name(content: str) -> Optional[str]:
    """Extract package name from Java source content."""
    import re

    package_pattern = r'package\s+([\w.]+);'
    match = re.search(package_pattern, content)

    if match:
        return match.group(1)

    return None


def _score_naming_pattern(class_name: str) -> float:
    """
    Phase 1: Score naming pattern (T049).

    Awards 80 points if class name ends with 'DTO' (case-insensitive).

    Args:
        class_name: Name of the class

    Returns:
        Score (0 or 80)
    """
    if not class_name:
        return 0.0

    # Check for DTO suffix (case-insensitive)
    if class_name.upper().endswith('DTO'):
        return 80.0

    return 0.0


def _has_entity_markers(content: str) -> bool:
    """
    Phase 2: Check for entity markers (T050).

    Entity markers disqualify a class from being a DTO.
    Markers: @Entity, @Table, @MappedSuperclass

    Args:
        content: Java source code content

    Returns:
        True if entity markers found, False otherwise
    """
    entity_annotations = ['@Entity', '@Table', '@MappedSuperclass']

    for annotation in entity_annotations:
        if annotation in content:
            return True

    return False


def _count_fields_and_methods(content: str) -> tuple[int, int]:
    """
    Count fields and methods in Java class.

    Args:
        content: Java source code content

    Returns:
        Tuple of (field_count, method_count)
    """
    import re

    # Count fields (private/protected/public instance variables)
    # Match: private Type fieldName; or private Type fieldName = ...;
    field_pattern = r'(?:private|protected|public)\s+(?:static\s+)?(?:final\s+)?[\w<>\[\]]+\s+\w+\s*[=;]'
    field_matches = re.findall(field_pattern, content)

    # Filter out static final constants (usually ALL_CAPS)
    fields = [f for f in field_matches if not re.search(r'\s+[A-Z_]+\s*[=;]', f)]
    field_count = len(fields)

    # Count methods (exclude constructors)
    # Match method signatures: public/private/protected Type methodName(...)
    method_pattern = r'(?:public|private|protected)\s+(?:static\s+)?(?!class\s)[\w<>\[\]]+\s+\w+\s*\([^)]*\)\s*(?:throws\s+[\w,\s]+)?\s*\{'
    method_matches = re.findall(method_pattern, content)
    method_count = len(method_matches)

    return field_count, method_count


def _score_structural_analysis(field_count: int, method_count: int) -> float:
    """
    Phase 3: Score structural analysis based on field-to-method ratio (T051).

    DTOs are data-heavy with few methods (mostly getters/setters).
    High field count with low method count indicates DTO pattern.

    Scoring:
    - Ratio >= 2.0: 20 points (many fields, few methods)
    - Ratio >= 1.0: 15 points (more fields than methods)
    - Ratio >= 0.5: 10 points (decent field count)
    - Ratio < 0.5: 5 points (method-heavy, likely not DTO)

    Args:
        field_count: Number of fields in class
        method_count: Number of methods in class

    Returns:
        Structural score (0-20 points)
    """
    # Must have at least one field to be a DTO
    if field_count == 0:
        return 0.0

    # Calculate ratio
    if method_count == 0:
        # All fields, no methods (unusual but DTO-like)
        return 15.0

    ratio = field_count / method_count

    # Score based on ratio
    if ratio >= 2.0:
        return 20.0
    elif ratio >= 1.0:
        return 15.0
    elif ratio >= 0.5:
        return 10.0
    else:
        return 5.0


def _has_serialization_markers(content: str) -> bool:
    """
    Phase 4: Check for serialization markers (T052).

    Serialization markers indicate the class is designed for data transfer.
    Markers:
    - implements Serializable
    - Jackson annotations (@JsonProperty, @JsonIgnore, etc.)
    - JAXB annotations (@XmlRootElement, @XmlElement, etc.)

    Args:
        content: Java source code content

    Returns:
        True if serialization markers found, False otherwise
    """
    serialization_markers = [
        'implements Serializable',
        'implements java.io.Serializable',
        '@JsonProperty',
        '@JsonIgnore',
        '@JsonSerialize',
        '@JsonDeserialize',
        '@XmlRootElement',
        '@XmlElement',
        '@XmlAccessorType'
    ]

    for marker in serialization_markers:
        if marker in content:
            return True

    return False


def _score_package_location(package_name: Optional[str]) -> float:
    """
    Phase 5: Score package location heuristics (T053).

    DTOs are typically in specific packages.
    Awards 15 points for typical DTO package patterns.

    Package patterns (case-insensitive):
    - *.dto.* (15 points)
    - *.model.* (15 points)
    - *.domain.* (10 points)
    - *.api.* (10 points)
    - *.transfer.* (15 points)

    Args:
        package_name: Package name (e.g., "com.example.dto")

    Returns:
        Package score (0-15 points)
    """
    if not package_name:
        return 0.0

    package_lower = package_name.lower()

    # Check for DTO-specific packages (highest score)
    if '.dto.' in package_lower or package_lower.endswith('.dto'):
        return 15.0

    if '.transfer.' in package_lower or package_lower.endswith('.transfer'):
        return 15.0

    if '.model.' in package_lower or package_lower.endswith('.model'):
        return 15.0

    # Check for likely DTO packages (medium score)
    if '.domain.' in package_lower or package_lower.endswith('.domain'):
        return 10.0

    if '.api.' in package_lower or package_lower.endswith('.api'):
        return 10.0

    return 0.0


def _identify_nested_dtos(content: str) -> List[str]:
    """
    Identify nested DTO types in class (T059).

    Looks for:
    - Fields with type names ending in 'DTO'
    - Inner classes
    - Generic type parameters (List<CustomerDTO>)

    Args:
        content: Java source code content

    Returns:
        List of nested DTO type names
    """
    import re

    nested_types = []

    # Pattern 1: Field declarations with DTO type
    # private CustomerDTO customer;
    field_pattern = r'(?:private|protected|public)\s+(\w*DTO\w*)\s+\w+\s*[;=]'
    field_matches = re.findall(field_pattern, content)
    nested_types.extend(field_matches)

    # Pattern 2: Generic types with DTO
    # private List<OrderItemDTO> items;
    generic_pattern = r'<(\w*DTO\w*)>'
    generic_matches = re.findall(generic_pattern, content)
    nested_types.extend(generic_matches)

    # Pattern 3: Inner class DTOs
    # public static class AddressDTO { ... }
    inner_class_pattern = r'(?:public|private|protected)?\s+(?:static\s+)?class\s+(\w*DTO\w*)'
    inner_matches = re.findall(inner_class_pattern, content)
    nested_types.extend(inner_matches)

    # Remove duplicates and sort
    nested_types = sorted(set(nested_types))

    return nested_types
