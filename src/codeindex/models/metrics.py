"""
Metrics models for tracking extraction performance and quality.

This module defines dataclasses for tracking timeout events, foreign key extraction,
and navigation analysis metrics.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class TimeoutMetric:
    """
    Tracks an Ollama timeout event with retry and fallback information.

    Used to monitor extraction reliability and identify files that consistently timeout.
    """

    file_path: str
    """Absolute path to the file that timed out"""

    timeout_threshold: float
    """Timeout threshold in seconds that was used"""

    retry_count: int
    """Number of retry attempts made (0-3)"""

    fallback_used: bool
    """Whether structural analysis fallback was triggered"""

    extraction_quality: str
    """Quality of extraction: 'full' (LLM), 'structural' (fallback), 'failed'"""

    file_lines: int = 0
    """Number of lines in the file"""

    timeout_duration: float = 0.0
    """Actual time spent before timeout (seconds)"""

    timestamp: datetime = field(default_factory=datetime.now)
    """When the timeout occurred"""

    error_message: Optional[str] = None
    """Error message from timeout exception"""

    def __post_init__(self):
        """Validate timeout metric values"""
        if self.timeout_threshold <= 0:
            raise ValueError(f"timeout_threshold must be positive, got {self.timeout_threshold}")

        if self.retry_count < 0 or self.retry_count > 3:
            raise ValueError(f"retry_count must be 0-3, got {self.retry_count}")

        if self.extraction_quality not in ['full', 'structural', 'failed']:
            raise ValueError(f"extraction_quality must be 'full', 'structural', or 'failed', got {self.extraction_quality}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON logging"""
        return {
            'file_path': self.file_path,
            'timeout_threshold': self.timeout_threshold,
            'retry_count': self.retry_count,
            'fallback_used': self.fallback_used,
            'extraction_quality': self.extraction_quality,
            'file_lines': self.file_lines,
            'timeout_duration': self.timeout_duration,
            'timestamp': self.timestamp.isoformat(),
            'error_message': self.error_message
        }


@dataclass
class ForeignKeyMetric:
    """
    Tracks foreign key extraction statistics for a DAO file.

    Monitors multi-source FK extraction (Java, iBATIS, SQL) and validation success.
    """

    dao_file: str
    """Path to DAO file"""

    fk_extracted: int
    """Total foreign keys extracted"""

    fk_from_java: int = 0
    """Foreign keys from @JoinColumn annotations"""

    fk_from_ibatis: int = 0
    """Foreign keys from iBATIS XML"""

    fk_from_sql: int = 0
    """Foreign keys from SQL JOIN statements"""

    validation_errors: int = 0
    """Number of FK validation failures"""

    columns_collected: int = 0
    """Total columns collected before validation"""

    timestamp: datetime = field(default_factory=datetime.now)
    """When extraction occurred"""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON logging"""
        return {
            'dao_file': self.dao_file,
            'fk_extracted': self.fk_extracted,
            'fk_from_java': self.fk_from_java,
            'fk_from_ibatis': self.fk_from_ibatis,
            'fk_from_sql': self.fk_from_sql,
            'validation_errors': self.validation_errors,
            'columns_collected': self.columns_collected,
            'timestamp': self.timestamp.isoformat()
        }


@dataclass
class NavigationMetric:
    """
    Tracks GWT navigation analysis statistics.

    Monitors component discovery rate and navigation graph construction performance.
    """

    entry_point: str
    """Path to index.html/jsp entry point"""

    modules_parsed: int
    """Number of GWT modules parsed"""

    presenters_discovered: int
    """Number of Presenters found"""

    views_discovered: int
    """Number of Views found"""

    activities_discovered: int = 0
    """Number of Activities found"""

    places_discovered: int = 0
    """Number of Places found"""

    navigation_edges: int = 0
    """Number of navigation paths found"""

    circular_dependencies: int = 0
    """Number of circular module dependencies detected"""

    discovery_rate: float = 0.0
    """Percentage of expected components discovered (0-100)"""

    timestamp: datetime = field(default_factory=datetime.now)
    """When navigation analysis completed"""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON logging"""
        return {
            'entry_point': self.entry_point,
            'modules_parsed': self.modules_parsed,
            'presenters_discovered': self.presenters_discovered,
            'views_discovered': self.views_discovered,
            'activities_discovered': self.activities_discovered,
            'places_discovered': self.places_discovered,
            'navigation_edges': self.navigation_edges,
            'circular_dependencies': self.circular_dependencies,
            'discovery_rate': self.discovery_rate,
            'timestamp': self.timestamp.isoformat()
        }
