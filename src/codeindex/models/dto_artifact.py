"""
DTO artifact models for data transfer object analysis.

Implements T046-T048: DtoField, DtoArtifact, ClassificationResult models.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime


@dataclass
class DtoField:
    """
    Model representing a field in a Data Transfer Object (T046).

    Captures field metadata including type, modifiers, and validation annotations.
    """

    name: str
    field_type: str
    modifiers: List[str] = field(default_factory=list)  # public, private, static, final, etc.
    is_nested_dto: bool = False
    validation_annotations: List[Dict[str, Any]] = field(default_factory=list)

    # Additional metadata
    is_collection: bool = False
    collection_type: Optional[str] = None  # List, Set, Map, etc.
    generic_types: List[str] = field(default_factory=list)  # For List<String>, etc.

    def __post_init__(self):
        """Validate field after initialization."""
        if not self.name:
            raise ValueError("Field name is required")
        if not self.field_type:
            raise ValueError("Field type is required")

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"DtoField(name='{self.name}', type='{self.field_type}', nested={self.is_nested_dto})"

    @property
    def has_validation(self) -> bool:
        """Check if field has validation annotations."""
        return len(self.validation_annotations) > 0

    @property
    def is_required(self) -> bool:
        """Check if field is marked as required (@NotNull, @NotEmpty)."""
        required_annotations = {'NotNull', 'NotEmpty', 'NotBlank'}
        return any(
            ann.get('type') in required_annotations
            for ann in self.validation_annotations
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'name': self.name,
            'field_type': self.field_type,
            'modifiers': self.modifiers,
            'is_nested_dto': self.is_nested_dto,
            'validation_annotations': self.validation_annotations,
            'is_collection': self.is_collection,
            'collection_type': self.collection_type,
            'generic_types': self.generic_types,
            'has_validation': self.has_validation,
            'is_required': self.is_required
        }


@dataclass
class ClassificationResult:
    """
    Result of DTO classification with confidence scoring (T048).

    Contains detailed scoring breakdown from 5-phase classification process:
    - Phase 1: Naming pattern (80 points)
    - Phase 2: Entity exclusion (disqualifying)
    - Phase 3: Structural analysis (field-to-method ratio)
    - Phase 4: Serialization markers (10 points)
    - Phase 5: Package location heuristics (15 points)

    Threshold: confidence >= 70 for DTO classification.
    """

    # Final classification
    is_dto: bool
    confidence: float  # 0-100

    # Phase scores
    naming_pattern_score: float = 0  # 0-80 points
    structural_score: float = 0  # Variable based on ratio
    serialization_score: float = 0  # 0-10 points
    package_score: float = 0  # 0-15 points

    # Detection flags
    entity_markers_found: bool = False
    serialization_markers_found: bool = False
    nested_dtos_found: bool = False

    # Metadata
    field_count: int = 0
    method_count: int = 0
    nested_dto_types: List[str] = field(default_factory=list)
    nested_dto_count: int = 0
    package_name: Optional[str] = None
    class_name: Optional[str] = None

    def __post_init__(self):
        """Validate classification result."""
        if self.confidence < 0 or self.confidence > 100:
            raise ValueError(f"Confidence must be 0-100, got: {self.confidence}")

        # Confidence should match scoring logic
        calculated_confidence = min(
            self.naming_pattern_score +
            self.structural_score +
            self.serialization_score +
            self.package_score,
            100
        )

        # Allow small rounding differences
        if abs(self.confidence - calculated_confidence) > 1.0:
            raise ValueError(
                f"Confidence ({self.confidence}) doesn't match "
                f"calculated score ({calculated_confidence})"
            )

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"ClassificationResult(is_dto={self.is_dto}, "
            f"confidence={self.confidence:.1f}, "
            f"class={self.class_name})"
        )

    @property
    def field_to_method_ratio(self) -> float:
        """Calculate field-to-method ratio."""
        if self.method_count == 0:
            return float(self.field_count)
        return self.field_count / self.method_count

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'is_dto': self.is_dto,
            'confidence': self.confidence,
            'naming_pattern_score': self.naming_pattern_score,
            'structural_score': self.structural_score,
            'serialization_score': self.serialization_score,
            'package_score': self.package_score,
            'entity_markers_found': self.entity_markers_found,
            'serialization_markers_found': self.serialization_markers_found,
            'nested_dtos_found': self.nested_dtos_found,
            'field_count': self.field_count,
            'method_count': self.method_count,
            'nested_dto_types': self.nested_dto_types,
            'nested_dto_count': self.nested_dto_count,
            'package_name': self.package_name,
            'class_name': self.class_name,
            'field_to_method_ratio': self.field_to_method_ratio
        }


@dataclass
class DtoArtifact:
    """
    Complete DTO artifact with classification metadata (T047).

    Represents a Data Transfer Object with all extracted information:
    - Classification results
    - Field definitions
    - Validation rules
    - Nested DTO relationships
    - Source location
    """

    # Identification
    artifact_id: str  # Canonical ID (hash of path + class name)
    class_name: str
    package_name: Optional[str] = None
    source_file: Optional[Path] = None

    # Classification
    is_dto: bool = False
    confidence: float = 0.0
    classification_result: Optional[ClassificationResult] = None

    # Structure
    fields: List[DtoField] = field(default_factory=list)
    nested_dto_types: List[str] = field(default_factory=list)

    # Validation
    has_validation_annotations: bool = False
    validation_rules: Dict[str, Any] = field(default_factory=dict)

    # Serialization
    serialization_markers: List[str] = field(default_factory=list)
    implements_serializable: bool = False

    # Metadata
    project: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    language: str = "java"
    framework_hints: List[str] = field(default_factory=list)  # Jackson, JAXB, etc.

    def __post_init__(self):
        """Validate DTO artifact after initialization."""
        if not self.artifact_id:
            raise ValueError("artifact_id is required")
        if not self.class_name:
            raise ValueError("class_name is required")

        # Ensure confidence is valid
        if self.confidence < 0 or self.confidence > 100:
            raise ValueError(f"Confidence must be 0-100, got: {self.confidence}")

        # Sync nested DTO count
        if self.nested_dto_types and not self.classification_result:
            # If we have nested types but no classification result, create minimal one
            pass

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"DtoArtifact(class={self.class_name}, "
            f"is_dto={self.is_dto}, "
            f"confidence={self.confidence:.1f}, "
            f"fields={len(self.fields)})"
        )

    @property
    def field_count(self) -> int:
        """Get number of fields in DTO."""
        return len(self.fields)

    @property
    def required_fields(self) -> List[DtoField]:
        """Get list of required fields (@NotNull, @NotEmpty)."""
        return [f for f in self.fields if f.is_required]

    @property
    def nested_dto_fields(self) -> List[DtoField]:
        """Get list of fields that are nested DTOs."""
        return [f for f in self.fields if f.is_nested_dto]

    @property
    def has_nested_dtos(self) -> bool:
        """Check if DTO has nested DTO fields."""
        return len(self.nested_dto_types) > 0

    @classmethod
    def from_classification(
        cls,
        file_path: Path,
        classification: ClassificationResult,
        fields: Optional[List[DtoField]] = None,
        project_name: Optional[str] = None
    ) -> 'DtoArtifact':
        """
        Create DtoArtifact from classification result.

        Args:
            file_path: Path to source file
            classification: ClassificationResult from classify_dto
            fields: Optional list of extracted DtoField objects (auto-extracted if not provided)
            project_name: Optional project name

        Returns:
            DtoArtifact instance
        """
        import hashlib

        # Generate artifact ID from path and class name
        artifact_id = hashlib.md5(
            f"{file_path}:{classification.class_name}".encode()
        ).hexdigest()

        # Auto-extract fields if not provided
        if fields is None and file_path.exists():
            from codeindex.parsers.java_parser import extract_dto_metadata
            try:
                metadata = extract_dto_metadata(file_path)
                fields = []
                for field_data in metadata.get('fields', []):
                    field_obj = DtoField(
                        name=field_data['name'],
                        field_type=field_data['field_type'],
                        modifiers=field_data.get('modifiers', []),
                        is_nested_dto=field_data.get('is_nested_dto', False),
                        validation_annotations=field_data.get('validation_annotations', []),
                        is_collection=field_data.get('is_collection', False),
                        collection_type=field_data.get('collection_type'),
                        generic_types=field_data.get('generic_types', [])
                    )
                    fields.append(field_obj)
            except Exception:
                fields = []

        # Extract validation rules from fields
        validation_rules = {}
        has_validation = False
        if fields:
            for f in fields:
                if f.has_validation:
                    has_validation = True
                    validation_rules[f.name] = f.validation_annotations

        return cls(
            artifact_id=artifact_id,
            class_name=classification.class_name or file_path.stem,
            package_name=classification.package_name,
            source_file=file_path,
            is_dto=classification.is_dto,
            confidence=classification.confidence,
            classification_result=classification,
            fields=fields or [],
            nested_dto_types=classification.nested_dto_types,
            has_validation_annotations=has_validation,
            validation_rules=validation_rules,
            project=project_name
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'artifact_id': self.artifact_id,
            'class_name': self.class_name,
            'package_name': self.package_name,
            'source_file': str(self.source_file) if self.source_file else None,
            'is_dto': self.is_dto,
            'confidence': self.confidence,
            'classification_result': self.classification_result.to_dict() if self.classification_result else None,
            'fields': [f.to_dict() for f in self.fields],
            'field_count': self.field_count,
            'nested_dto_types': self.nested_dto_types,
            'has_nested_dtos': self.has_nested_dtos,
            'has_validation_annotations': self.has_validation_annotations,
            'validation_rules': self.validation_rules,
            'serialization_markers': self.serialization_markers,
            'implements_serializable': self.implements_serializable,
            'project': self.project,
            'created_at': self.created_at.isoformat(),
            'language': self.language,
            'framework_hints': self.framework_hints
        }
