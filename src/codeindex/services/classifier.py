"""
File classifier service.

Classifies source code files based on extensions, paths, and naming patterns
to determine their artifact type (Java source, test, JSP, SQL, etc.).
"""

import logging
import re
from pathlib import Path
from typing import Union

from codeindex.models import ArtifactType

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
