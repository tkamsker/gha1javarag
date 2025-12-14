"""
PRD (Product Requirements Document) models for codebase analysis.

Models for database entities, business rules, services, and frontend components
extracted from codebase analysis for PRD generation.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


# ==============================================================================
# Enumerations
# ==============================================================================

class SourceType(str, Enum):
    """Database entity source type."""
    JPA_ANNOTATION = "jpa_annotation"
    IBATIS_XML = "ibatis_xml"
    SQL_FILE = "sql_file"
    HIBERNATE_MAPPING = "hibernate_mapping"
    DAO_CODE = "dao_code"


class RuleLayer(str, Enum):
    """Business rule enforcement layer."""
    DATABASE = "database"
    SERVICE = "service"
    FRONTEND = "frontend"
    CROSS_LAYER = "cross_layer"


class RuleScope(str, Enum):
    """Business rule scope."""
    FIELD = "field"
    ENTITY = "entity"
    TRANSACTION = "transaction"
    APPLICATION = "application"


class RuleType(str, Enum):
    """Business rule type."""
    VALIDATION = "validation"
    CONSTRAINT = "constraint"
    CALCULATION = "calculation"
    WORKFLOW = "workflow"
    AUTHORIZATION = "authorization"
    BUSINESS_LOGIC = "business_logic"


class RuleSeverity(str, Enum):
    """Business rule severity."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class AnalysisLayer(str, Enum):
    """Analysis layer."""
    DATABASE = "database"
    SERVICE = "service"
    FRONTEND = "frontend"
    CROSS_LAYER = "cross_layer"


class VisitStatus(str, Enum):
    """File visit status."""
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    IN_PROGRESS = "in_progress"


class ServiceType(str, Enum):
    """Service type classification."""
    BUSINESS_SERVICE = "business_service"
    DAO_SERVICE = "dao_service"
    INTEGRATION_SERVICE = "integration_service"
    CONTROLLER = "controller"
    REST_CONTROLLER = "rest_controller"
    UTILITY_SERVICE = "utility_service"


class HTTPMethod(str, Enum):
    """HTTP method enum."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


# ==============================================================================
# Nested Data Types
# ==============================================================================

@dataclass
class Column:
    """Database column definition."""
    name: str
    data_type: str
    nullable: bool = True
    default_value: Optional[str] = None
    description: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "data_type": self.data_type,
            "nullable": self.nullable,
            "default_value": self.default_value,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Column":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class ForeignKey:
    """Foreign key relationship."""
    column_name: str
    referenced_table: str
    referenced_column: str
    on_delete: Optional[str] = None
    on_update: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "column_name": self.column_name,
            "referenced_table": self.referenced_table,
            "referenced_column": self.referenced_column,
            "on_delete": self.on_delete,
            "on_update": self.on_update,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ForeignKey":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class Index:
    """Database index definition."""
    name: str
    columns: List[str]
    unique: bool = False
    index_type: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "columns": self.columns,
            "unique": self.unique,
            "index_type": self.index_type,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Index":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class Constraint:
    """Database constraint definition."""
    name: str
    type: str  # CHECK, UNIQUE, NOT NULL
    definition: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "type": self.type,
            "definition": self.definition,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Constraint":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class CodeSnippet:
    """Source code snippet."""
    file_path: str
    line_start: int
    line_end: int
    code_text: str
    language: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "file_path": self.file_path,
            "line_start": self.line_start,
            "line_end": self.line_end,
            "code_text": self.code_text,
            "language": self.language,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CodeSnippet":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class Parameter:
    """Method parameter definition."""
    name: str
    type: str
    description: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "type": self.type,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Parameter":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class ServiceOperation:
    """Service operation/method definition."""
    name: str
    signature: str
    return_type: str
    parameters: List[Parameter] = field(default_factory=list)
    description: Optional[str] = None
    throws: List[str] = field(default_factory=list)
    annotations: List[str] = field(default_factory=list)
    line_number: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "signature": self.signature,
            "return_type": self.return_type,
            "parameters": [p.to_dict() for p in self.parameters],
            "description": self.description,
            "throws": self.throws,
            "annotations": self.annotations,
            "line_number": self.line_number,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ServiceOperation":
        """Create from dictionary."""
        if "parameters" in data:
            data["parameters"] = [Parameter.from_dict(p) for p in data["parameters"]]
        return cls(**data)


@dataclass
class ServiceDependency:
    """Service dependency/injection definition."""
    target_service: str
    dependency_type: str  # injection, reference, static
    injection_method: Optional[str] = None  # constructor, field, setter

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "target_service": self.target_service,
            "dependency_type": self.dependency_type,
            "injection_method": self.injection_method,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ServiceDependency":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class TransactionInfo:
    """Transaction boundary information."""
    method_name: str
    transaction_type: str  # REQUIRED, REQUIRES_NEW, SUPPORTS, etc.
    propagation: Optional[str] = None
    isolation_level: Optional[str] = None
    read_only: Optional[bool] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "method_name": self.method_name,
            "transaction_type": self.transaction_type,
            "propagation": self.propagation,
            "isolation_level": self.isolation_level,
            "read_only": self.read_only,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TransactionInfo":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class EndpointParameter:
    """API endpoint parameter definition."""
    name: str
    location: str  # path, query, header, body
    type: str
    required: bool
    description: Optional[str] = None
    default_value: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "location": self.location,
            "type": self.type,
            "required": self.required,
            "description": self.description,
            "default_value": self.default_value,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EndpointParameter":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class StatusCode:
    """HTTP status code definition."""
    code: int
    description: str
    response_type: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "code": self.code,
            "description": self.description,
            "response_type": self.response_type,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StatusCode":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class RequestFormat:
    """API request format definition."""
    content_type: str
    schema_description: Optional[str] = None
    parameters: List[EndpointParameter] = field(default_factory=list)
    example: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "content_type": self.content_type,
            "schema_description": self.schema_description,
            "parameters": [p.to_dict() for p in self.parameters],
            "example": self.example,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RequestFormat":
        """Create from dictionary."""
        if "parameters" in data:
            data["parameters"] = [EndpointParameter.from_dict(p) for p in data["parameters"]]
        return cls(**data)


@dataclass
class ResponseFormat:
    """API response format definition."""
    content_type: str
    status_codes: List[StatusCode]
    schema_description: Optional[str] = None
    example: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "content_type": self.content_type,
            "status_codes": [sc.to_dict() for sc in self.status_codes],
            "schema_description": self.schema_description,
            "example": self.example,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ResponseFormat":
        """Create from dictionary."""
        if "status_codes" in data:
            data["status_codes"] = [StatusCode.from_dict(sc) for sc in data["status_codes"]]
        return cls(**data)


# ==============================================================================
# Core Entities
# ==============================================================================

@dataclass
class DatabaseEntity:
    """
    Database table or entity.

    Represents a database table/entity discovered from DAO classes, ORM mappings,
    or SQL files with its structure, relationships, and business rules.
    """
    # Identifiers
    id: str  # Unique identifier (table name or qualified name)
    name: str  # Table or entity name
    source_type: SourceType  # Where discovered
    source_files: List[str]  # Paths to files where entity was found
    columns: List[Column]  # List of columns/fields
    created_at: datetime  # When entity was analyzed

    # Optional fields
    qualified_name: Optional[str] = None  # Schema-qualified name (schema.table)
    primary_key: List[str] = field(default_factory=list)  # Column names forming PK
    foreign_keys: List[ForeignKey] = field(default_factory=list)  # FK relationships
    indexes: List[Index] = field(default_factory=list)  # Database indexes
    constraints: List[Constraint] = field(default_factory=list)  # Constraints
    business_rules: List[str] = field(default_factory=list)  # BusinessRule IDs
    description: Optional[str] = None  # LLM-generated description
    estimated_row_count: Optional[str] = None  # small, medium, large, massive
    domain: Optional[str] = None  # Business domain (billing, auth, etc.)

    def __post_init__(self):
        """Validate after initialization."""
        if not self.id:
            raise ValueError("id is required")
        if not self.name:
            raise ValueError("name is required")
        if not self.source_files:
            raise ValueError("source_files is required (at least one)")
        if not self.columns:
            raise ValueError("columns is required (at least one)")

        # Validate primary_key columns exist
        column_names = {col.name for col in self.columns}
        for pk_col in self.primary_key:
            if pk_col not in column_names:
                raise ValueError(f"Primary key column '{pk_col}' not in columns")

        # Validate foreign_key columns exist
        for fk in self.foreign_keys:
            if fk.column_name not in column_names:
                raise ValueError(f"Foreign key column '{fk.column_name}' not in columns")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "qualified_name": self.qualified_name,
            "source_type": self.source_type.value,
            "source_files": self.source_files,
            "columns": [col.to_dict() for col in self.columns],
            "primary_key": self.primary_key,
            "foreign_keys": [fk.to_dict() for fk in self.foreign_keys],
            "indexes": [idx.to_dict() for idx in self.indexes],
            "constraints": [cons.to_dict() for cons in self.constraints],
            "business_rules": self.business_rules,
            "description": self.description,
            "estimated_row_count": self.estimated_row_count,
            "domain": self.domain,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DatabaseEntity":
        """Create from dictionary."""
        # Convert nested objects
        if "columns" in data:
            data["columns"] = [Column.from_dict(col) for col in data["columns"]]
        if "foreign_keys" in data:
            data["foreign_keys"] = [ForeignKey.from_dict(fk) for fk in data["foreign_keys"]]
        if "indexes" in data:
            data["indexes"] = [Index.from_dict(idx) for idx in data["indexes"]]
        if "constraints" in data:
            data["constraints"] = [Constraint.from_dict(cons) for cons in data["constraints"]]

        # Convert enums
        if "source_type" in data and isinstance(data["source_type"], str):
            data["source_type"] = SourceType(data["source_type"])

        # Convert datetime
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])

        return cls(**data)


@dataclass
class BusinessRule:
    """
    Business rule or validation constraint.

    Represents a validation, constraint, or business logic pattern discovered
    in code at any layer (database, service, frontend, or cross-layer).
    """
    # Identifiers
    id: str  # Unique identifier (UUID or BR_XXX)
    name: str  # Short name/label for the rule
    layer: RuleLayer  # Where rule is enforced
    scope: RuleScope  # Scope of enforcement
    rule_type: RuleType  # Type of rule
    description: str  # Natural language description
    source_files: List[str]  # Files where rule is implemented
    created_at: datetime  # When rule was extracted

    # Optional fields
    source_code_snippets: List[CodeSnippet] = field(default_factory=list)  # Code excerpts
    related_entities: List[str] = field(default_factory=list)  # Entity IDs
    conditions: Optional[str] = None  # Rule conditions/triggers
    enforcement_mechanism: Optional[str] = None  # How it's enforced
    severity: Optional[RuleSeverity] = None  # Impact if violated
    security_relevant: bool = False  # Is this security-related?
    domain: Optional[str] = None  # Business domain

    def __post_init__(self):
        """Validate after initialization."""
        if not self.id:
            raise ValueError("id is required")
        if not self.name:
            raise ValueError("name is required")
        if not self.description:
            raise ValueError("description is required")
        if not self.source_files:
            raise ValueError("source_files is required (at least one)")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "layer": self.layer.value,
            "scope": self.scope.value,
            "rule_type": self.rule_type.value,
            "description": self.description,
            "source_files": self.source_files,
            "source_code_snippets": [snippet.to_dict() for snippet in self.source_code_snippets],
            "related_entities": self.related_entities,
            "conditions": self.conditions,
            "enforcement_mechanism": self.enforcement_mechanism,
            "severity": self.severity.value if self.severity else None,
            "security_relevant": self.security_relevant,
            "domain": self.domain,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BusinessRule":
        """Create from dictionary."""
        # Convert nested objects
        if "source_code_snippets" in data:
            data["source_code_snippets"] = [
                CodeSnippet.from_dict(snippet) for snippet in data["source_code_snippets"]
            ]

        # Convert enums
        if "layer" in data and isinstance(data["layer"], str):
            data["layer"] = RuleLayer(data["layer"])
        if "scope" in data and isinstance(data["scope"], str):
            data["scope"] = RuleScope(data["scope"])
        if "rule_type" in data and isinstance(data["rule_type"], str):
            data["rule_type"] = RuleType(data["rule_type"])
        if "severity" in data and isinstance(data["severity"], str):
            data["severity"] = RuleSeverity(data["severity"])

        # Convert datetime
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])

        return cls(**data)


@dataclass
class ServiceDefinition:
    """
    Backend service class definition.

    Represents a service class with its operations, dependencies, and exposed endpoints.
    """
    # Identifiers
    id: str  # Unique identifier (qualified class name)
    class_name: str  # Simple class name
    qualified_name: str  # Fully qualified class name
    package: str  # Java package
    source_file: str  # Path to service class file
    service_type: ServiceType  # Type of service
    operations: List[ServiceOperation]  # Public methods/operations
    created_at: datetime  # When service was analyzed

    # Optional fields
    description: Optional[str] = None  # LLM-generated description
    dependencies: List[ServiceDependency] = field(default_factory=list)
    data_dependencies: List[str] = field(default_factory=list)  # DatabaseEntity IDs
    endpoints: List[str] = field(default_factory=list)  # APIEndpoint IDs
    business_rules: List[str] = field(default_factory=list)  # BusinessRule IDs
    transaction_boundaries: List[TransactionInfo] = field(default_factory=list)
    frameworks: List[str] = field(default_factory=list)  # Spring, EJB, etc.
    domain: Optional[str] = None  # Business domain

    def __post_init__(self):
        """Validate after initialization."""
        if not self.id:
            raise ValueError("id is required")
        if not self.class_name:
            raise ValueError("class_name is required")
        if not self.qualified_name:
            raise ValueError("qualified_name is required")
        if not self.source_file:
            raise ValueError("source_file is required")
        if not self.operations:
            raise ValueError("operations is required (at least one)")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "class_name": self.class_name,
            "qualified_name": self.qualified_name,
            "package": self.package,
            "source_file": self.source_file,
            "service_type": self.service_type.value,
            "description": self.description,
            "operations": [op.to_dict() for op in self.operations],
            "dependencies": [dep.to_dict() for dep in self.dependencies],
            "data_dependencies": self.data_dependencies,
            "endpoints": self.endpoints,
            "business_rules": self.business_rules,
            "transaction_boundaries": [tb.to_dict() for tb in self.transaction_boundaries],
            "frameworks": self.frameworks,
            "domain": self.domain,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ServiceDefinition":
        """Create from dictionary."""
        # Convert nested objects
        if "operations" in data:
            data["operations"] = [ServiceOperation.from_dict(op) for op in data["operations"]]
        if "dependencies" in data:
            data["dependencies"] = [ServiceDependency.from_dict(dep) for dep in data["dependencies"]]
        if "transaction_boundaries" in data:
            data["transaction_boundaries"] = [TransactionInfo.from_dict(tb) for tb in data["transaction_boundaries"]]

        # Convert enums
        if "service_type" in data and isinstance(data["service_type"], str):
            data["service_type"] = ServiceType(data["service_type"])

        # Convert datetime
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])

        return cls(**data)


@dataclass
class APIEndpoint:
    """
    REST or SOAP endpoint definition.

    Represents an API endpoint exposed by a backend service.
    """
    # Identifiers
    id: str  # Unique identifier (method:path)
    http_method: HTTPMethod  # HTTP method
    path: str  # URL path or pattern
    service_id: str  # ServiceDefinition ID implementing this endpoint
    operation_name: str  # Service method handling this endpoint
    source_file: str  # File where endpoint is defined
    created_at: datetime  # When endpoint was analyzed

    # Optional fields
    description: Optional[str] = None  # LLM-generated description
    request_format: Optional[RequestFormat] = None
    response_format: Optional[ResponseFormat] = None
    authentication_required: bool = True
    authorization_roles: List[str] = field(default_factory=list)
    rate_limited: bool = False
    deprecated: bool = False
    produces: List[str] = field(default_factory=list)  # Media types produced
    consumes: List[str] = field(default_factory=list)  # Media types consumed

    def __post_init__(self):
        """Validate after initialization."""
        if not self.id:
            raise ValueError("id is required")
        if not self.path:
            raise ValueError("path is required")
        if not self.service_id:
            raise ValueError("service_id is required")
        if not self.operation_name:
            raise ValueError("operation_name is required")
        if not self.source_file:
            raise ValueError("source_file is required")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "http_method": self.http_method.value,
            "path": self.path,
            "service_id": self.service_id,
            "operation_name": self.operation_name,
            "source_file": self.source_file,
            "description": self.description,
            "request_format": self.request_format.to_dict() if self.request_format else None,
            "response_format": self.response_format.to_dict() if self.response_format else None,
            "authentication_required": self.authentication_required,
            "authorization_roles": self.authorization_roles,
            "rate_limited": self.rate_limited,
            "deprecated": self.deprecated,
            "produces": self.produces,
            "consumes": self.consumes,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "APIEndpoint":
        """Create from dictionary."""
        # Convert nested objects
        if "request_format" in data and data["request_format"]:
            data["request_format"] = RequestFormat.from_dict(data["request_format"])
        if "response_format" in data and data["response_format"]:
            data["response_format"] = ResponseFormat.from_dict(data["response_format"])

        # Convert enums
        if "http_method" in data and isinstance(data["http_method"], str):
            data["http_method"] = HTTPMethod(data["http_method"])

        # Convert datetime
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])

        return cls(**data)


@dataclass
class FileVisitEntry:
    """
    File visit log entry for incremental processing.

    Tracks which files have been analyzed with content hash to enable
    skipping unchanged files on subsequent runs.
    """
    file_path: str  # Absolute path to analyzed file
    timestamp: datetime  # When file was last analyzed
    status: VisitStatus  # Analysis result
    content_hash: str  # SHA-256 hash of file contents (64 hex chars)
    layer: AnalysisLayer  # Which layer analysis was performed

    # Optional fields
    analysis_type: Optional[str] = None  # Specific analysis (dao_extraction, etc.)
    error_message: Optional[str] = None  # If status=failed, what went wrong
    duration_seconds: Optional[float] = None  # How long analysis took
    extracted_entities: List[str] = field(default_factory=list)  # IDs of entities extracted

    def __post_init__(self):
        """Validate after initialization."""
        if not self.file_path:
            raise ValueError("file_path is required")
        if not self.content_hash:
            raise ValueError("content_hash is required")
        if len(self.content_hash) != 64:
            raise ValueError(f"content_hash must be 64 hex chars (SHA-256), got {len(self.content_hash)}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON Lines serialization."""
        return {
            "file_path": self.file_path,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status.value,
            "content_hash": self.content_hash,
            "layer": self.layer.value,
            "analysis_type": self.analysis_type,
            "error_message": self.error_message,
            "duration_seconds": self.duration_seconds,
            "extracted_entities": self.extracted_entities,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FileVisitEntry":
        """Create from dictionary."""
        # Convert enums
        if "status" in data and isinstance(data["status"], str):
            data["status"] = VisitStatus(data["status"])
        if "layer" in data and isinstance(data["layer"], str):
            data["layer"] = AnalysisLayer(data["layer"])

        # Convert datetime
        if "timestamp" in data and isinstance(data["timestamp"], str):
            data["timestamp"] = datetime.fromisoformat(data["timestamp"])

        return cls(**data)
