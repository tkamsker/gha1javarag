"""
ExtractionResult model for Java Codebase Indexer Pipeline.

Captures AI output for a single file before converting to CodeArtifact.
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from codeindex.models import ArtifactType


@dataclass
class ExtractionResult:
    """
    Extraction result entity.

    Transient structure capturing both structural and semantic extraction for a single file.
    """

    # File metadata
    file_path: str  # Path to extracted file
    artifact_type: "ArtifactType"  # Type of artifact
    extracted_at: datetime = field(default_factory=datetime.utcnow)  # Extraction timestamp

    # Extraction data
    structural_data: Dict[str, Any] = field(default_factory=dict)  # Parsed structural info
    semantic_data: Dict[str, Any] = field(default_factory=dict)  # AI-generated semantic info

    # Legacy fields (for backwards compatibility)
    summary: Optional[str] = None  # Natural language summary
    classification: Optional[str] = None  # AI-refined artifact type
    entities: list[str] = field(default_factory=list)  # Extracted entities
    tags: Dict[str, list[str]] = field(default_factory=dict)  # Tags by category
    frameworks: list[str] = field(default_factory=list)  # Detected frameworks
    concerns: list[str] = field(default_factory=list)  # Detected concerns

    # Metadata
    confidence: Optional[float] = None  # AI confidence score
    raw_response: Optional[str] = None  # Full Ollama response
    error: Optional[str] = None  # Error message if extraction failed

    def __post_init__(self):
        """Populate legacy fields from semantic_data if needed."""
        # Import at runtime to avoid circular import
        from codeindex.models import ArtifactType as AT

        # If semantic_data exists but legacy fields are empty, populate them
        if self.semantic_data and not self.summary:
            self.summary = self.semantic_data.get('summary', '')
            self.classification = self.semantic_data.get('classification', self.artifact_type.value if (self.artifact_type and isinstance(self.artifact_type, AT)) else '')
            self.entities = self.semantic_data.get('entities', [])
            self.frameworks = self.semantic_data.get('frameworks', [])
            self.concerns = self.semantic_data.get('concerns', [])

        # Validate confidence score
        if self.confidence is not None:
            if not (0.0 <= self.confidence <= 1.0):
                raise ValueError(f"confidence must be between 0.0 and 1.0, got {self.confidence}")

    def get_layer_tags(self) -> list[str]:
        """
        Get layer tags from tags dictionary.

        Returns:
            List of layer tags (backend, frontend, persistence, etc.)
        """
        return self.tags.get("layer", [])

    def get_domain_tags(self) -> list[str]:
        """
        Get domain tags from tags dictionary.

        Returns:
            List of domain tags (auth, billing, reporting, etc.)
        """
        return self.tags.get("domain", [])

    def get_concern_tags(self) -> list[str]:
        """
        Get concern tags from tags dictionary.

        Returns:
            List of concern tags (security, validation, business_rule, etc.)
        """
        return self.tags.get("concerns", self.concerns)  # Fallback to concerns field

    def merge_tags(self, deterministic_tags: Dict[str, list[str]]):
        """
        Merge deterministic tags with AI-generated tags.

        Args:
            deterministic_tags: Tags generated from path patterns (test, config, etc.)
        """
        for category, tag_list in deterministic_tags.items():
            if category not in self.tags:
                self.tags[category] = []
            # Add tags that don't already exist
            for tag in tag_list:
                if tag not in self.tags[category]:
                    self.tags[category].append(tag)

    def to_dict(self) -> dict:
        """
        Convert to dictionary for serialization.

        Returns:
            Dictionary representation
        """
        # Import at runtime to avoid circular import
        from codeindex.models import ArtifactType as AT

        return {
            "file_path": self.file_path,
            "artifact_type": self.artifact_type.value if isinstance(self.artifact_type, AT) else self.artifact_type,
            "extracted_at": self.extracted_at.isoformat() if isinstance(self.extracted_at, datetime) else self.extracted_at,
            "structural_data": self.structural_data,
            "semantic_data": self.semantic_data,
            "summary": self.summary,
            "classification": self.classification,
            "entities": self.entities,
            "tags": self.tags,
            "frameworks": self.frameworks,
            "concerns": self.concerns,
            "confidence": self.confidence,
            "raw_response": self.raw_response,
            "error": self.error,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ExtractionResult":
        """
        Create ExtractionResult from dictionary.

        Args:
            data: Dictionary with extraction data

        Returns:
            ExtractionResult instance
        """
        return cls(**data)

    @classmethod
    def from_ollama_response(cls, response: Dict[str, Any]) -> "ExtractionResult":
        """
        Create ExtractionResult from Ollama API response.

        Args:
            response: Ollama API JSON response

        Returns:
            ExtractionResult instance

        Example Ollama response format:
        {
            "summary": "Handles user authentication...",
            "classification": "java_source",
            "entities": ["AuthService", "validateCredentials", "generateToken"],
            "tags": {
                "layer": ["backend"],
                "domain": ["auth"],
                "concerns": ["security"]
            },
            "frameworks": ["Spring"],
            "confidence": 0.95
        }
        """
        return cls(
            summary=response.get("summary", ""),
            classification=response.get("classification", "other_text"),
            entities=response.get("entities", []),
            tags=response.get("tags", {}),
            frameworks=response.get("frameworks", []),
            concerns=response.get("concerns", []),
            confidence=response.get("confidence"),
            raw_response=str(response),  # Store full response for debugging
        )

    def validate_classification(self, valid_types: list[str]) -> bool:
        """
        Check if classification is in valid artifact types.

        Args:
            valid_types: List of valid artifact type strings

        Returns:
            True if classification is valid
        """
        return self.classification in valid_types

    def normalize_classification(self, valid_types: list[str], default: str = "other_text") -> str:
        """
        Get normalized classification, falling back to default if invalid.

        Args:
            valid_types: List of valid artifact type strings
            default: Default type if classification is invalid

        Returns:
            Normalized classification
        """
        if self.classification in valid_types:
            return self.classification
        return default
