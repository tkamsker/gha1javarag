"""
Foreign key relationship model for multi-source extraction.

This module defines dataclasses for representing foreign key relationships
extracted from Java annotations, iBATIS XML, and SQL JOIN statements.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum


class ForeignKeySource(Enum):
    """Source of foreign key extraction"""
    JAVA = "Java"
    IBATIS = "iBATIS"
    SQL = "SQL"
    UNKNOWN = "Unknown"


@dataclass
class ForeignKeyRelationship:
    """
    Database foreign key relationship with multi-source extraction tracking.

    Represents a foreign key constraint extracted from Java @JoinColumn annotations,
    iBATIS XML <association> tags, or SQL JOIN ON clauses, with source tracking
    and confidence scoring.
    """

    source_entity: str
    """Source entity/table name"""

    source_column: str
    """Source column name (foreign key column)"""

    target_entity: str
    """Target entity/table name (referenced table)"""

    target_column: str
    """Target column name (referenced column)"""

    fk_source: ForeignKeySource
    """Source of FK extraction (Java, iBATIS, SQL)"""

    confidence: float = 1.0
    """Confidence score for this FK (0.0-1.0)"""

    nullable: Optional[bool] = None
    """Whether FK can be null (from @JoinColumn nullable attribute)"""

    cascade_type: Optional[str] = None
    """Cascade operations (from JPA annotations)"""

    fetch_type: Optional[str] = None
    """Fetch type (LAZY, EAGER) from JPA annotations"""

    relationship_type: Optional[str] = None
    """Relationship type: OneToOne, OneToMany, ManyToOne, ManyToMany"""

    source_file: Optional[str] = None
    """Path to source file where FK was found"""

    validated: bool = False
    """Whether FK columns were validated against collected columns"""

    validation_error: Optional[str] = None
    """Validation error message if validation failed"""

    def __post_init__(self):
        """Validate foreign key relationship values"""
        if not self.source_entity:
            raise ValueError("source_entity cannot be empty")

        if not self.source_column:
            raise ValueError("source_column cannot be empty")

        if not self.target_entity:
            raise ValueError("target_entity cannot be empty")

        if not self.target_column:
            raise ValueError("target_column cannot be empty")

        if self.confidence < 0.0 or self.confidence > 1.0:
            raise ValueError(f"confidence must be 0.0-1.0, got {self.confidence}")

        if not isinstance(self.fk_source, ForeignKeySource):
            raise ValueError(f"fk_source must be ForeignKeySource enum, got {type(self.fk_source)}")

    def is_validated(self) -> bool:
        """Check if FK has been validated"""
        return self.validated and self.validation_error is None

    def is_from_java(self) -> bool:
        """Check if FK was extracted from Java annotations"""
        return self.fk_source == ForeignKeySource.JAVA

    def is_from_ibatis(self) -> bool:
        """Check if FK was extracted from iBATIS XML"""
        return self.fk_source == ForeignKeySource.IBATIS

    def is_from_sql(self) -> bool:
        """Check if FK was extracted from SQL statements"""
        return self.fk_source == ForeignKeySource.SQL

    def get_source_priority(self) -> int:
        """
        Get priority score for this FK source (higher is better).

        Java annotations have highest priority (3), then iBATIS (2), then SQL (1).

        Returns:
            Priority score (1-3)
        """
        priority_map = {
            ForeignKeySource.JAVA: 3,
            ForeignKeySource.IBATIS: 2,
            ForeignKeySource.SQL: 1,
            ForeignKeySource.UNKNOWN: 0
        }
        return priority_map.get(self.fk_source, 0)

    def mark_validated(self, error: Optional[str] = None):
        """
        Mark FK as validated with optional error.

        Args:
            error: Validation error message, None if validation passed
        """
        self.validated = True
        self.validation_error = error

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'source_entity': self.source_entity,
            'source_column': self.source_column,
            'target_entity': self.target_entity,
            'target_column': self.target_column,
            'fk_source': self.fk_source.value,
            'confidence': self.confidence,
            'nullable': self.nullable,
            'cascade_type': self.cascade_type,
            'fetch_type': self.fetch_type,
            'relationship_type': self.relationship_type,
            'source_file': self.source_file,
            'validated': self.validated,
            'validation_error': self.validation_error
        }

    def __hash__(self):
        """Make FK hashable for set operations"""
        return hash((self.source_entity, self.source_column, self.target_entity, self.target_column))

    def __eq__(self, other):
        """Check FK equality based on entities and columns"""
        if not isinstance(other, ForeignKeyRelationship):
            return False
        return (
            self.source_entity == other.source_entity and
            self.source_column == other.source_column and
            self.target_entity == other.target_entity and
            self.target_column == other.target_column
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ForeignKeyRelationship':
        """Create ForeignKeyRelationship from dictionary"""
        fk_source = ForeignKeySource(data['fk_source']) if 'fk_source' in data else ForeignKeySource.UNKNOWN

        return cls(
            source_entity=data['source_entity'],
            source_column=data['source_column'],
            target_entity=data['target_entity'],
            target_column=data['target_column'],
            fk_source=fk_source,
            confidence=data.get('confidence', 1.0),
            nullable=data.get('nullable'),
            cascade_type=data.get('cascade_type'),
            fetch_type=data.get('fetch_type'),
            relationship_type=data.get('relationship_type'),
            source_file=data.get('source_file'),
            validated=data.get('validated', False),
            validation_error=data.get('validation_error')
        )
