"""
Metrics collection and aggregation utility.

This module provides functions to aggregate and log metrics in JSON format
for timeout events, foreign key extraction, and navigation analysis.
"""

import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from codeindex.models.metrics import TimeoutMetric, ForeignKeyMetric, NavigationMetric

logger = logging.getLogger("codeindex.metrics")


class MetricsCollector:
    """
    Collects and aggregates metrics from various pipeline stages.

    Stores metrics in memory and provides JSON logging and aggregation functions.
    """

    def __init__(self):
        """Initialize empty metrics collections"""
        self.timeout_metrics: List[TimeoutMetric] = []
        self.fk_metrics: List[ForeignKeyMetric] = []
        self.navigation_metrics: List[NavigationMetric] = []

    def add_timeout_metric(self, metric: TimeoutMetric):
        """Add a timeout metric to the collection"""
        self.timeout_metrics.append(metric)
        logger.debug(f"Recorded timeout metric: {metric.file_path}")

    def add_fk_metric(self, metric: ForeignKeyMetric):
        """Add a foreign key metric to the collection"""
        self.fk_metrics.append(metric)
        logger.debug(f"Recorded FK metric: {metric.dao_file}")

    def add_navigation_metric(self, metric: NavigationMetric):
        """Add a navigation metric to the collection"""
        self.navigation_metrics.append(metric)
        logger.debug(f"Recorded navigation metric: {metric.entry_point}")

    def get_timeout_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics for timeout metrics.

        Returns:
            Dictionary with timeout statistics
        """
        if not self.timeout_metrics:
            return {
                'total_files': 0,
                'timeout_count': 0,
                'retry_success': 0,
                'fallback_count': 0,
                'failed_count': 0,
                'avg_retry_count': 0.0,
                'avg_timeout_duration': 0.0
            }

        total_files = len(self.timeout_metrics)
        timeout_count = len([m for m in self.timeout_metrics if m.timeout_duration > 0])
        retry_success = len([m for m in self.timeout_metrics if m.retry_count > 0 and m.extraction_quality == 'full'])
        fallback_count = len([m for m in self.timeout_metrics if m.fallback_used])
        failed_count = len([m for m in self.timeout_metrics if m.extraction_quality == 'failed'])

        total_retries = sum(m.retry_count for m in self.timeout_metrics)
        avg_retry_count = total_retries / total_files if total_files > 0 else 0.0

        total_duration = sum(m.timeout_duration for m in self.timeout_metrics)
        avg_timeout_duration = total_duration / total_files if total_files > 0 else 0.0

        return {
            'total_files': total_files,
            'timeout_count': timeout_count,
            'retry_success': retry_success,
            'fallback_count': fallback_count,
            'failed_count': failed_count,
            'avg_retry_count': round(avg_retry_count, 2),
            'avg_timeout_duration': round(avg_timeout_duration, 2)
        }

    def get_fk_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics for foreign key metrics.

        Returns:
            Dictionary with FK extraction statistics
        """
        if not self.fk_metrics:
            return {
                'total_daos': 0,
                'total_fk_extracted': 0,
                'fk_from_java': 0,
                'fk_from_ibatis': 0,
                'fk_from_sql': 0,
                'total_validation_errors': 0,
                'avg_fk_per_dao': 0.0
            }

        total_daos = len(self.fk_metrics)
        total_fk_extracted = sum(m.fk_extracted for m in self.fk_metrics)
        fk_from_java = sum(m.fk_from_java for m in self.fk_metrics)
        fk_from_ibatis = sum(m.fk_from_ibatis for m in self.fk_metrics)
        fk_from_sql = sum(m.fk_from_sql for m in self.fk_metrics)
        total_validation_errors = sum(m.validation_errors for m in self.fk_metrics)

        avg_fk_per_dao = total_fk_extracted / total_daos if total_daos > 0 else 0.0

        return {
            'total_daos': total_daos,
            'total_fk_extracted': total_fk_extracted,
            'fk_from_java': fk_from_java,
            'fk_from_ibatis': fk_from_ibatis,
            'fk_from_sql': fk_from_sql,
            'total_validation_errors': total_validation_errors,
            'avg_fk_per_dao': round(avg_fk_per_dao, 2)
        }

    def get_navigation_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics for navigation metrics.

        Returns:
            Dictionary with navigation analysis statistics
        """
        if not self.navigation_metrics:
            return {
                'entry_points': 0,
                'total_modules': 0,
                'total_presenters': 0,
                'total_views': 0,
                'total_activities': 0,
                'total_places': 0,
                'total_navigation_edges': 0,
                'circular_dependencies': 0,
                'avg_discovery_rate': 0.0
            }

        entry_points = len(self.navigation_metrics)
        total_modules = sum(m.modules_parsed for m in self.navigation_metrics)
        total_presenters = sum(m.presenters_discovered for m in self.navigation_metrics)
        total_views = sum(m.views_discovered for m in self.navigation_metrics)
        total_activities = sum(m.activities_discovered for m in self.navigation_metrics)
        total_places = sum(m.places_discovered for m in self.navigation_metrics)
        total_navigation_edges = sum(m.navigation_edges for m in self.navigation_metrics)
        circular_dependencies = sum(m.circular_dependencies for m in self.navigation_metrics)

        total_discovery_rate = sum(m.discovery_rate for m in self.navigation_metrics)
        avg_discovery_rate = total_discovery_rate / entry_points if entry_points > 0 else 0.0

        return {
            'entry_points': entry_points,
            'total_modules': total_modules,
            'total_presenters': total_presenters,
            'total_views': total_views,
            'total_activities': total_activities,
            'total_places': total_places,
            'total_navigation_edges': total_navigation_edges,
            'circular_dependencies': circular_dependencies,
            'avg_discovery_rate': round(avg_discovery_rate, 2)
        }

    def log_timeout_metrics_json(self):
        """Log timeout metrics as JSON"""
        if not self.timeout_metrics:
            return

        summary = self.get_timeout_summary()
        logger.info(f"Timeout metrics summary: {json.dumps(summary)}")

        # Log individual metrics at debug level
        for metric in self.timeout_metrics:
            logger.debug(f"Timeout metric: {json.dumps(metric.to_dict())}")

    def log_fk_metrics_json(self):
        """Log foreign key metrics as JSON"""
        if not self.fk_metrics:
            return

        summary = self.get_fk_summary()
        logger.info(f"FK metrics summary: {json.dumps(summary)}")

        # Log individual metrics at debug level
        for metric in self.fk_metrics:
            logger.debug(f"FK metric: {json.dumps(metric.to_dict())}")

    def log_navigation_metrics_json(self):
        """Log navigation metrics as JSON"""
        if not self.navigation_metrics:
            return

        summary = self.get_navigation_summary()
        logger.info(f"Navigation metrics summary: {json.dumps(summary)}")

        # Log individual metrics at debug level
        for metric in self.navigation_metrics:
            logger.debug(f"Navigation metric: {json.dumps(metric.to_dict())}")

    def log_all_metrics_json(self):
        """Log all metrics as JSON"""
        self.log_timeout_metrics_json()
        self.log_fk_metrics_json()
        self.log_navigation_metrics_json()

    def export_to_json(self, file_path: str):
        """
        Export all metrics to a JSON file.

        Args:
            file_path: Path to output JSON file
        """
        data = {
            'timestamp': datetime.now().isoformat(),
            'timeout_metrics': [m.to_dict() for m in self.timeout_metrics],
            'fk_metrics': [m.to_dict() for m in self.fk_metrics],
            'navigation_metrics': [m.to_dict() for m in self.navigation_metrics],
            'summaries': {
                'timeout': self.get_timeout_summary(),
                'fk': self.get_fk_summary(),
                'navigation': self.get_navigation_summary()
            }
        }

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

        logger.info(f"Exported metrics to {file_path}")

    def reset(self):
        """Clear all collected metrics"""
        self.timeout_metrics.clear()
        self.fk_metrics.clear()
        self.navigation_metrics.clear()
        logger.debug("Metrics collector reset")


# Global metrics collector instance
_global_collector: Optional[MetricsCollector] = None


def get_metrics_collector() -> MetricsCollector:
    """
    Get the global metrics collector instance.

    Returns:
        Global MetricsCollector singleton
    """
    global _global_collector
    if _global_collector is None:
        _global_collector = MetricsCollector()
    return _global_collector


def reset_metrics_collector():
    """Reset the global metrics collector"""
    global _global_collector
    if _global_collector is not None:
        _global_collector.reset()
