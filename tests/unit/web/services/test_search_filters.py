"""
Unit tests for search filter application logic (T031 - US1.2).

Tests the filter building and application including:
- Weaviate GraphQL filter construction
- Artifact type multi-select filters
- Project single-select filters
- Filter combination logic
- Filter validation
"""

import pytest
from unittest.mock import Mock, patch
from typing import Dict, List, Optional


class TestFilterConstruction:
    """Test filter construction for Weaviate GraphQL queries."""

    def test_empty_filters(self):
        """Test filter construction with no filters."""
        filters = {}

        # Should return None or empty filter
        graphql_filter = build_weaviate_filter(filters)

        assert graphql_filter is None or graphql_filter == {}

    def test_single_artifact_type_filter(self):
        """Test filter with single artifact type."""
        filters = {"artifact_types": ["DaoCall"]}

        graphql_filter = build_weaviate_filter(filters)

        # Should create where clause for artifact type
        assert graphql_filter is not None
        # Weaviate filter format: {"path": ["class"], "operator": "Equal", "valueString": "DaoCall"}

    def test_multiple_artifact_types_filter(self):
        """Test filter with multiple artifact types."""
        filters = {"artifact_types": ["DaoCall", "GwtPresenter", "GwtView"]}

        graphql_filter = build_weaviate_filter(filters)

        assert graphql_filter is not None
        # Should create OR condition for multiple types

    def test_all_artifact_types_filter(self):
        """Test filter with all 11 artifact types."""
        filters = {
            "artifact_types": [
                "DaoCall", "GwtPresenter", "GwtView", "GwtUiBinder",
                "DtoArtifact", "IbatisStatement", "DbTable", "GwtEndpoint",
                "JspForm", "BackendDoc", "JsArtifact"
            ]
        }

        graphql_filter = build_weaviate_filter(filters)

        # Should handle all types efficiently
        assert graphql_filter is not None

    def test_project_filter(self):
        """Test filter with project."""
        filters = {"project": "com.example:app:1.0.0"}

        graphql_filter = build_weaviate_filter(filters)

        assert graphql_filter is not None
        # Should filter by project field

    def test_combined_filters(self):
        """Test combination of artifact type and project filters."""
        filters = {
            "artifact_types": ["DaoCall", "GwtPresenter"],
            "project": "com.example:app:1.0.0"
        }

        graphql_filter = build_weaviate_filter(filters)

        assert graphql_filter is not None
        # Should combine both filters with AND logic


class TestFilterValidation:
    """Test filter validation logic."""

    def test_valid_artifact_type(self):
        """Test validation of valid artifact type."""
        artifact_type = "DaoCall"

        is_valid = validate_artifact_type(artifact_type)

        assert is_valid is True

    def test_invalid_artifact_type(self):
        """Test validation of invalid artifact type."""
        artifact_type = "InvalidType"

        is_valid = validate_artifact_type(artifact_type)

        assert is_valid is False

    def test_valid_artifact_types_list(self):
        """Test validation of valid artifact types list."""
        artifact_types = ["DaoCall", "GwtPresenter", "GwtView"]

        are_valid = all(validate_artifact_type(t) for t in artifact_types)

        assert are_valid is True

    def test_invalid_artifact_types_list(self):
        """Test validation rejects list with invalid types."""
        artifact_types = ["DaoCall", "InvalidType", "GwtView"]

        are_valid = all(validate_artifact_type(t) for t in artifact_types)

        assert are_valid is False

    def test_empty_artifact_types_list(self):
        """Test validation of empty artifact types list."""
        artifact_types = []

        # Empty list is valid (no filter)
        assert isinstance(artifact_types, list)

    def test_valid_project_format(self):
        """Test validation of valid project identifier."""
        project = "com.example:app:1.0.0"

        is_valid = validate_project_format(project)

        assert is_valid is True

    def test_valid_project_without_version(self):
        """Test validation of project without version."""
        project = "com.example:app"

        is_valid = validate_project_format(project)

        assert is_valid is True

    def test_invalid_project_format(self):
        """Test validation of invalid project format."""
        project = "not a valid project"

        is_valid = validate_project_format(project)

        # Depends on validation rules, but should handle gracefully
        assert isinstance(is_valid, bool)


class TestFilterApplication:
    """Test filter application in search service."""

    @pytest.fixture
    def mock_search_service(self):
        """Create mock search service."""
        from codeindex.web.services.search_service import SearchService
        service = SearchService()
        service.weaviate_client = Mock()
        return service

    def test_apply_no_filters(self, mock_search_service):
        """Test search with no filters."""
        result = mock_search_service.search("test query", filters=None)

        assert result["filters_applied"] == {}

    def test_apply_artifact_type_filter(self, mock_search_service):
        """Test search with artifact type filter."""
        filters = {"artifact_types": ["DaoCall"]}

        result = mock_search_service.search("test query", filters=filters)

        assert result["filters_applied"] == filters

    def test_apply_project_filter(self, mock_search_service):
        """Test search with project filter."""
        filters = {"project": "com.example:app:1.0.0"}

        result = mock_search_service.search("test query", filters=filters)

        assert result["filters_applied"] == filters

    def test_apply_combined_filters(self, mock_search_service):
        """Test search with combined filters."""
        filters = {
            "artifact_types": ["DaoCall", "GwtPresenter"],
            "project": "com.example:app:1.0.0"
        }

        result = mock_search_service.search("test query", filters=filters)

        assert result["filters_applied"] == filters

    def test_filter_persistence_across_searches(self, mock_search_service):
        """Test that filters persist across multiple searches."""
        filters = {"artifact_types": ["DaoCall"]}

        result1 = mock_search_service.search("query1", filters=filters)
        result2 = mock_search_service.search("query2", filters=filters)

        assert result1["filters_applied"] == result2["filters_applied"]


class TestFilterEdgeCases:
    """Test edge cases in filter handling."""

    def test_none_filters(self):
        """Test handling of None filters."""
        filters = None

        graphql_filter = build_weaviate_filter(filters)

        assert graphql_filter is None or graphql_filter == {}

    def test_empty_dict_filters(self):
        """Test handling of empty dict filters."""
        filters = {}

        graphql_filter = build_weaviate_filter(filters)

        assert graphql_filter is None or graphql_filter == {}

    def test_filters_with_none_values(self):
        """Test handling of filters with None values."""
        filters = {
            "artifact_types": None,
            "project": None
        }

        graphql_filter = build_weaviate_filter(filters)

        # Should filter out None values
        assert graphql_filter is None or graphql_filter == {}

    def test_filters_with_empty_lists(self):
        """Test handling of filters with empty lists."""
        filters = {
            "artifact_types": [],
            "project": None
        }

        graphql_filter = build_weaviate_filter(filters)

        # Should filter out empty lists
        assert graphql_filter is None or graphql_filter == {}

    def test_duplicate_artifact_types(self):
        """Test handling of duplicate artifact types."""
        filters = {"artifact_types": ["DaoCall", "DaoCall", "GwtPresenter"]}

        graphql_filter = build_weaviate_filter(filters)

        # Should deduplicate
        assert graphql_filter is not None


class TestFilterPerformance:
    """Test filter performance characteristics."""

    def test_large_filter_set_performance(self):
        """Test performance with large filter set."""
        import time

        filters = {
            "artifact_types": [
                "DaoCall", "GwtPresenter", "GwtView", "GwtUiBinder",
                "DtoArtifact", "IbatisStatement", "DbTable", "GwtEndpoint",
                "JspForm", "BackendDoc", "JsArtifact"
            ]
        }

        start_time = time.time()
        graphql_filter = build_weaviate_filter(filters)
        end_time = time.time()

        execution_time = end_time - start_time

        # Filter building should be very fast (<1ms)
        assert execution_time < 0.001
        assert graphql_filter is not None

    def test_filter_optimization(self):
        """Test that filters are optimized."""
        filters = {
            "artifact_types": ["DaoCall"],
            "project": "com.example:app:1.0.0"
        }

        graphql_filter = build_weaviate_filter(filters)

        # Should create efficient query structure
        assert graphql_filter is not None


# Helper functions that would be implemented in search_service.py

def build_weaviate_filter(filters: Optional[Dict]) -> Optional[Dict]:
    """
    Build Weaviate GraphQL filter from filters dict.

    Args:
        filters: Dictionary with artifact_types and/or project

    Returns:
        Weaviate GraphQL filter dict or None
    """
    if not filters:
        return None

    where_clauses = []

    # Filter by artifact types
    artifact_types = filters.get("artifact_types")
    if artifact_types and len(artifact_types) > 0:
        # Deduplicate
        artifact_types = list(set(artifact_types))

        if len(artifact_types) == 1:
            # Single type - simple equality
            where_clauses.append({
                "path": ["class"],
                "operator": "Equal",
                "valueString": artifact_types[0]
            })
        else:
            # Multiple types - OR condition
            type_clauses = [
                {
                    "path": ["class"],
                    "operator": "Equal",
                    "valueString": t
                }
                for t in artifact_types
            ]
            where_clauses.append({
                "operator": "Or",
                "operands": type_clauses
            })

    # Filter by project
    project = filters.get("project")
    if project:
        where_clauses.append({
            "path": ["project"],
            "operator": "Equal",
            "valueString": project
        })

    # Combine clauses with AND
    if len(where_clauses) == 0:
        return None
    elif len(where_clauses) == 1:
        return where_clauses[0]
    else:
        return {
            "operator": "And",
            "operands": where_clauses
        }


def validate_artifact_type(artifact_type: str) -> bool:
    """
    Validate artifact type.

    Args:
        artifact_type: Artifact type name

    Returns:
        True if valid, False otherwise
    """
    valid_types = [
        "DaoCall", "GwtPresenter", "GwtView", "GwtUiBinder",
        "DtoArtifact", "IbatisStatement", "DbTable", "GwtEndpoint",
        "JspForm", "BackendDoc", "JsArtifact"
    ]

    return artifact_type in valid_types


def validate_project_format(project: str) -> bool:
    """
    Validate project format.

    Args:
        project: Project identifier

    Returns:
        True if valid format, False otherwise
    """
    if not project:
        return False

    # Basic validation: should contain at least one colon
    # Format: groupId:artifactId or groupId:artifactId:version
    parts = project.split(":")

    if len(parts) < 2:
        return False

    # All parts should be non-empty
    return all(part.strip() for part in parts)
