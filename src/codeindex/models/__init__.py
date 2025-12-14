"""
Models package for Java Codebase Indexer Pipeline.

Contains data models and controlled vocabularies (enums).
"""
from enum import Enum
from typing import List

# Import models for convenient access
from .project import Project
from .artifact import CodeArtifact
from .inventory import DiscoveryInventory
from .extraction import ExtractionResult


# ==============================================================================
# Artifact Types - Controlled Vocabulary
# ==============================================================================

class ArtifactType(str, Enum):
    """
    Artifact type enumeration.

    Defines the semantic types for code artifacts based on file purpose.
    """
    JAVA_SOURCE = "java_source"          # .java files with classes/interfaces
    JAVA_TEST = "java_test"              # Test files (JUnit, TestNG)
    JSP_VIEW = "jsp_view"                # JSP templates
    HTML_TEMPLATE = "html_template"      # Static HTML files
    GWT_MODULE = "gwt_module"            # GWT module XML
    GWT_UI_BINDER = "gwt_ui_binder"      # GWT UiBinder XML
    JS_SCRIPT = "js_script"              # JavaScript files
    SQL_SCHEMA = "sql_schema"            # SQL DDL files
    SQL_QUERY = "sql_query"              # SQL query files
    ORM_MAPPING = "orm_mapping"          # Hibernate/JPA mapping XML
    IBATIS_MAPPING = "ibatis_mapping"    # iBATIS/MyBatis mapper XML
    XML_CONFIG = "xml_config"            # Spring/config XML files
    PROPERTIES_FILE = "properties_file"  # .properties files
    STATIC_ASSET = "static_asset"        # CSS, images, fonts
    OTHER_TEXT = "other_text"            # Other text files


ARTIFACT_TYPES: List[str] = [t.value for t in ArtifactType]


# ==============================================================================
# Layer Tags - Controlled Vocabulary
# ==============================================================================

class LayerTag(str, Enum):
    """
    Layer tag enumeration.

    Defines architectural layers for code classification.
    """
    BACKEND = "backend"                  # Server-side business logic
    FRONTEND = "frontend"                # UI/presentation layer
    INTEGRATION = "integration"          # External system integration
    PERSISTENCE = "persistence"          # Data access layer
    CONFIG = "config"                    # Configuration files
    TEST = "test"                        # Test code


LAYER_TAGS: List[str] = [t.value for t in LayerTag]


# ==============================================================================
# Concern Tags - Controlled Vocabulary
# ==============================================================================

class ConcernTag(str, Enum):
    """
    Concern tag enumeration.

    Defines cross-cutting concerns and responsibilities.
    """
    SECURITY = "security"                # Authentication, authorization, encryption
    VALIDATION = "validation"            # Input validation, business rules
    BUSINESS_RULE = "business_rule"      # Core business logic
    DATA_ACCESS = "data_access"          # Database operations
    UI_FLOW = "ui_flow"                  # User interface workflows
    API_ENDPOINT = "api_endpoint"        # REST/SOAP endpoints
    ERROR_HANDLING = "error_handling"    # Exception handling
    LOGGING = "logging"                  # Logging and monitoring


CONCERN_TAGS: List[str] = [t.value for t in ConcernTag]


# ==============================================================================
# Framework Tags - Controlled Vocabulary
# ==============================================================================

class FrameworkTag(str, Enum):
    """
    Framework tag enumeration.

    Defines detected frameworks and libraries.
    """
    GWT = "GWT"                          # Google Web Toolkit
    STRUTS = "Struts"                    # Apache Struts
    SPRING = "Spring"                    # Spring Framework
    SPRING_MVC = "Spring MVC"            # Spring MVC
    IBATIS = "iBATIS"                    # iBATIS SQL mapper
    MYBATIS = "MyBatis"                  # MyBatis (iBATIS successor)
    JDBC = "JDBC"                        # JDBC direct access
    JSP = "JSP"                          # JavaServer Pages
    SERVLET = "Servlet"                  # Java Servlets
    JUNIT = "JUnit"                      # JUnit testing
    TESTNG = "TestNG"                    # TestNG testing
    HIBERNATE = "Hibernate"              # Hibernate ORM
    JPA = "JPA"                          # Java Persistence API


FRAMEWORK_TAGS: List[str] = [t.value for t in FrameworkTag]


# ==============================================================================
# Packaging Types - Maven
# ==============================================================================

class PackagingType(str, Enum):
    """
    Maven packaging type enumeration.
    """
    JAR = "jar"      # Java Archive
    WAR = "war"      # Web Application Archive
    POM = "pom"      # Parent POM (no code)
    EAR = "ear"      # Enterprise Application Archive


PACKAGING_TYPES: List[str] = [t.value for t in PackagingType]


# ==============================================================================
# Helper Functions
# ==============================================================================

def is_valid_artifact_type(artifact_type: str) -> bool:
    """
    Check if artifact type is valid.

    Args:
        artifact_type: Type string to validate

    Returns:
        True if valid
    """
    return artifact_type in ARTIFACT_TYPES


def is_valid_layer_tag(layer_tag: str) -> bool:
    """
    Check if layer tag is valid.

    Args:
        layer_tag: Tag string to validate

    Returns:
        True if valid
    """
    return layer_tag in LAYER_TAGS


def is_valid_concern_tag(concern_tag: str) -> bool:
    """
    Check if concern tag is valid.

    Args:
        concern_tag: Tag string to validate

    Returns:
        True if valid
    """
    return concern_tag in CONCERN_TAGS


def is_valid_framework_tag(framework_tag: str) -> bool:
    """
    Check if framework tag is valid.

    Args:
        framework_tag: Tag string to validate

    Returns:
        True if valid
    """
    return framework_tag in FRAMEWORK_TAGS


def normalize_artifact_type(artifact_type: str, default: str = "other_text") -> str:
    """
    Normalize artifact type to valid value.

    Args:
        artifact_type: Type string to normalize
        default: Default value if invalid (default: "other_text")

    Returns:
        Normalized artifact type
    """
    return artifact_type if is_valid_artifact_type(artifact_type) else default


# ==============================================================================
# Exports
# ==============================================================================

__all__ = [
    # Models
    "Project",
    "CodeArtifact",
    "DiscoveryInventory",
    "ExtractionResult",
    # Enums
    "ArtifactType",
    "LayerTag",
    "ConcernTag",
    "FrameworkTag",
    "PackagingType",
    # Lists
    "ARTIFACT_TYPES",
    "LAYER_TAGS",
    "CONCERN_TAGS",
    "FRAMEWORK_TAGS",
    "PACKAGING_TYPES",
    # Helper functions
    "is_valid_artifact_type",
    "is_valid_layer_tag",
    "is_valid_concern_tag",
    "is_valid_framework_tag",
    "normalize_artifact_type",
]
