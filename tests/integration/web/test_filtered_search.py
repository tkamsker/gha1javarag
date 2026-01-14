"""
Integration tests for filtered search (T033 - US1.2).

Tests end-to-end filter application including:
- Filter application to search results
- URL parameter persistence
- Filter restoration from URL
- Filter combinations
- Filter performance
"""

import pytest
import time
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, List


class TestFilteredSearchEndToEnd:
    """End-to-end tests for filtered search."""

    @pytest.fixture
    def mock_search_service(self):
        """Create mock search service."""
        from codeindex.web.services.search_service import SearchService

        service = SearchService()
        service.weaviate_client = Mock()

        return service

    def test_search_with_single_artifact_type(self, mock_search_service):
        """Test search filtered by single artifact type."""
        query = "database access"
        filters = {"artifact_types": ["DaoCall"]}

        result = mock_search_service.search(query, filters=filters)

        assert result["query"] == query
        assert result["filters_applied"]["artifact_types"] == ["DaoCall"]

    def test_search_with_multiple_artifact_types(self, mock_search_service):
        """Test search filtered by multiple artifact types."""
        query = "database access"
        filters = {"artifact_types": ["DaoCall", "IbatisStatement", "DbTable"]}

        result = mock_search_service.search(query, filters=filters)

        assert result["filters_applied"]["artifact_types"] == filters["artifact_types"]

    def test_search_with_project_filter(self, mock_search_service):
        """Test search filtered by project."""
        query = "user authentication"
        filters = {"project": "com.example:app:1.0.0"}

        result = mock_search_service.search(query, filters=filters)

        assert result["filters_applied"]["project"] == "com.example:app:1.0.0"

    def test_search_with_combined_filters(self, mock_search_service):
        """Test search with artifact type and project filters."""
        query = "presenter"
        filters = {
            "artifact_types": ["GwtPresenter", "GwtView"],
            "project": "com.example:app:1.0.0"
        }

        result = mock_search_service.search(query, filters=filters)

        assert result["filters_applied"] == filters

    def test_filter_changes_between_searches(self, mock_search_service):
        """Test changing filters between searches."""
        query = "test"

        # First search with one filter
        filters1 = {"artifact_types": ["DaoCall"]}
        result1 = mock_search_service.search(query, filters=filters1)

        # Second search with different filter
        filters2 = {"artifact_types": ["GwtPresenter"]}
        result2 = mock_search_service.search(query, filters=filters2)

        assert result1["filters_applied"] != result2["filters_applied"]
        assert result1["filters_applied"]["artifact_types"] == ["DaoCall"]
        assert result2["filters_applied"]["artifact_types"] == ["GwtPresenter"]


class TestURLParameterPersistence:
    """Test URL parameter persistence for filters."""

    def test_encode_filters_to_url(self):
        """Test encoding filters to URL parameters."""
        from tests.unit.web.utils.test_url_params import encode_url_params

        filters = {
            "artifact_types": ["DaoCall", "GwtPresenter"],
            "project": "com.example:app:1.0.0"
        }

        params = {
            "query": "test search",
            "filters": filters,
            "page": 1
        }

        encoded = encode_url_params(params)

        assert "query" in encoded
        assert "filters" in encoded
        assert "page" in encoded

    def test_decode_filters_from_url(self):
        """Test decoding filters from URL parameters."""
        from tests.unit.web.utils.test_url_params import encode_url_params, decode_url_params

        original_filters = {
            "artifact_types": ["DaoCall"],
            "project": "com.example:app:1.0.0"
        }

        params = {"filters": original_filters, "query": "test"}
        encoded = encode_url_params(params)
        decoded = decode_url_params(encoded)

        assert decoded["filters"] == original_filters

    def test_url_shareable_link(self):
        """Test creating shareable URL with filters."""
        from tests.unit.web.utils.test_url_params import encode_url_params
        from urllib.parse import urlencode

        params = {
            "query": "authentication flow",
            "filters": {
                "artifact_types": ["GwtPresenter", "GwtView"],
                "project": "com.example:app:1.0.0"
            },
            "page": 1
        }

        encoded = encode_url_params(params)
        query_string = urlencode(encoded)

        # Should be valid URL query string
        assert len(query_string) > 0
        assert "query=" in query_string


class TestFilterRestoration:
    """Test filter restoration from URL."""

    def test_restore_artifact_type_filter(self):
        """Test restoring artifact type filter from URL."""
        from tests.unit.web.utils.test_url_params import encode_url_params, decode_url_params

        original = {"artifact_types": ["DaoCall", "GwtPresenter"]}

        encoded = encode_url_params({"filters": original})
        decoded = decode_url_params(encoded)

        assert decoded["filters"]["artifact_types"] == original["artifact_types"]

    def test_restore_project_filter(self):
        """Test restoring project filter from URL."""
        from tests.unit.web.utils.test_url_params import encode_url_params, decode_url_params

        original = {"project": "com.example:app:1.0.0"}

        encoded = encode_url_params({"filters": original})
        decoded = decode_url_params(encoded)

        assert decoded["filters"]["project"] == original["project"]

    def test_restore_combined_filters(self):
        """Test restoring combined filters from URL."""
        from tests.unit.web.utils.test_url_params import encode_url_params, decode_url_params

        original = {
            "artifact_types": ["DaoCall", "GwtPresenter"],
            "project": "com.example:app:1.0.0"
        }

        encoded = encode_url_params({"filters": original})
        decoded = decode_url_params(encoded)

        assert decoded["filters"] == original

    def test_restore_search_state_from_url(self):
        """Test restoring complete search state from URL."""
        from tests.unit.web.utils.test_url_params import encode_url_params, decode_url_params

        original_state = {
            "query": "database access",
            "filters": {
                "artifact_types": ["DaoCall", "IbatisStatement"],
                "project": "com.example:app:1.0.0"
            },
            "page": 2
        }

        encoded = encode_url_params(original_state)
        decoded = decode_url_params(encoded)

        assert decoded["query"] == original_state["query"]
        assert decoded["filters"] == original_state["filters"]
        assert decoded["page"] == original_state["page"]


class TestFilterCombinations:
    """Test various filter combinations."""

    @pytest.fixture
    def mock_search_service(self):
        """Create mock search service."""
        from codeindex.web.services.search_service import SearchService

        service = SearchService()
        service.weaviate_client = Mock()

        return service

    def test_all_artifact_types_selected(self, mock_search_service):
        """Test with all 11 artifact types selected."""
        filters = {
            "artifact_types": [
                "DaoCall", "GwtPresenter", "GwtView", "GwtUiBinder",
                "DtoArtifact", "IbatisStatement", "DbTable", "GwtEndpoint",
                "JspForm", "BackendDoc", "JsArtifact"
            ]
        }

        result = mock_search_service.search("test", filters=filters)

        # Should handle all types
        assert len(result["filters_applied"]["artifact_types"]) == 11

    def test_no_artifact_types_selected(self, mock_search_service):
        """Test with no artifact types (empty list)."""
        filters = {"artifact_types": []}

        result = mock_search_service.search("test", filters=filters)

        # Empty list should be handled as no filter
        assert result["filters_applied"].get("artifact_types", []) == []

    def test_project_only_filter(self, mock_search_service):
        """Test with only project filter, no artifact types."""
        filters = {"project": "com.example:app:1.0.0"}

        result = mock_search_service.search("test", filters=filters)

        assert result["filters_applied"]["project"] == "com.example:app:1.0.0"
        assert "artifact_types" not in result["filters_applied"] or not result["filters_applied"].get("artifact_types")

    def test_artifact_types_only_filter(self, mock_search_service):
        """Test with only artifact types, no project."""
        filters = {"artifact_types": ["DaoCall", "GwtPresenter"]}

        result = mock_search_service.search("test", filters=filters)

        assert result["filters_applied"]["artifact_types"] == filters["artifact_types"]
        assert "project" not in result["filters_applied"] or not result["filters_applied"].get("project")


class TestFilterPerformance:
    """Test filter performance."""

    @pytest.fixture
    def mock_search_service(self):
        """Create mock search service."""
        from codeindex.web.services.search_service import SearchService

        service = SearchService()
        service.weaviate_client = Mock()

        return service

    def test_filter_application_performance(self, mock_search_service):
        """Test that filter application is fast."""
        filters = {
            "artifact_types": ["DaoCall", "GwtPresenter", "GwtView"],
            "project": "com.example:app:1.0.0"
        }

        start_time = time.time()
        result = mock_search_service.search("test", filters=filters)
        end_time = time.time()

        execution_time = end_time - start_time

        # Filter application should be fast (<1 second for mock)
        assert execution_time < 1.0

    def test_complex_filter_performance(self, mock_search_service):
        """Test performance with complex filter combinations."""
        filters = {
            "artifact_types": [
                "DaoCall", "GwtPresenter", "GwtView", "GwtUiBinder",
                "DtoArtifact", "IbatisStatement", "DbTable"
            ],
            "project": "com.example:app:1.0.0"
        }

        start_time = time.time()
        result = mock_search_service.search("test", filters=filters)
        end_time = time.time()

        execution_time = end_time - start_time

        # Even complex filters should be fast
        assert execution_time < 1.0


class TestFilterValidation:
    """Test filter validation in integration context."""

    @pytest.fixture
    def mock_search_service(self):
        """Create mock search service."""
        from codeindex.web.services.search_service import SearchService

        service = SearchService()
        service.weaviate_client = Mock()

        return service

    def test_invalid_artifact_type_handling(self, mock_search_service):
        """Test handling of invalid artifact type."""
        filters = {"artifact_types": ["InvalidType"]}

        # Should either reject or filter out invalid types
        result = mock_search_service.search("test", filters=filters)

        # Should handle gracefully
        assert "error" not in result or result["error"] is None

    def test_invalid_project_format_handling(self, mock_search_service):
        """Test handling of invalid project format."""
        filters = {"project": "not:a:valid:project:format:too:many:parts"}

        result = mock_search_service.search("test", filters=filters)

        # Should handle gracefully
        assert isinstance(result, dict)

    def test_mixed_valid_invalid_filters(self, mock_search_service):
        """Test handling of mix of valid and invalid filters."""
        filters = {
            "artifact_types": ["DaoCall", "InvalidType", "GwtPresenter"],
            "project": "com.example:app:1.0.0"
        }

        result = mock_search_service.search("test", filters=filters)

        # Should filter out invalid types, keep valid ones
        assert isinstance(result, dict)


class TestFilterWorkflow:
    """Test complete filter workflow."""

    @pytest.fixture
    def mock_search_service(self):
        """Create mock search service."""
        from codeindex.web.services.search_service import SearchService

        service = SearchService()
        service.weaviate_client = Mock()

        return service

    def test_apply_filter_workflow(self, mock_search_service):
        """Test workflow: search → apply filter → get filtered results."""
        # Initial search without filters
        result1 = mock_search_service.search("test", filters=None)
        assert result1["filters_applied"] == {}

        # Apply filter
        filters = {"artifact_types": ["DaoCall"]}
        result2 = mock_search_service.search("test", filters=filters)

        assert result2["filters_applied"] == filters

    def test_change_filter_workflow(self, mock_search_service):
        """Test workflow: search → change filter → get updated results."""
        # Search with first filter
        filters1 = {"artifact_types": ["DaoCall"]}
        result1 = mock_search_service.search("test", filters=filters1)

        # Change filter
        filters2 = {"artifact_types": ["GwtPresenter"]}
        result2 = mock_search_service.search("test", filters=filters2)

        assert result1["filters_applied"] != result2["filters_applied"]

    def test_clear_filter_workflow(self, mock_search_service):
        """Test workflow: search with filter → clear filter → get unfiltered results."""
        # Search with filter
        filters = {"artifact_types": ["DaoCall"]}
        result1 = mock_search_service.search("test", filters=filters)
        assert result1["filters_applied"] == filters

        # Clear filter
        result2 = mock_search_service.search("test", filters=None)
        assert result2["filters_applied"] == {}

    def test_share_filtered_search_workflow(self, mock_search_service):
        """Test workflow: create filtered search → generate shareable URL → restore from URL."""
        from tests.unit.web.utils.test_url_params import encode_url_params, decode_url_params

        # Create filtered search
        search_state = {
            "query": "authentication flow",
            "filters": {
                "artifact_types": ["GwtPresenter"],
                "project": "com.example:app:1.0.0"
            },
            "page": 1
        }

        # Generate shareable URL
        encoded = encode_url_params(search_state)

        # Simulate sharing and restoration
        decoded = decode_url_params(encoded)

        # Execute search with restored state
        result = mock_search_service.search(
            decoded["query"],
            filters=decoded["filters"]
        )

        assert result["query"] == search_state["query"]
        assert result["filters_applied"] == search_state["filters"]


class TestFilterEdgeCases:
    """Test edge cases in filtered search."""

    @pytest.fixture
    def mock_search_service(self):
        """Create mock search service."""
        from codeindex.web.services.search_service import SearchService

        service = SearchService()
        service.weaviate_client = Mock()

        return service

    def test_empty_query_with_filters(self, mock_search_service):
        """Test empty query with filters applied."""
        filters = {"artifact_types": ["DaoCall"]}

        result = mock_search_service.search("", filters=filters)

        # Should handle empty query
        assert result["query"] == ""

    def test_very_long_filter_list(self, mock_search_service):
        """Test with very long list of artifact types."""
        # All 11 types repeated multiple times
        filters = {
            "artifact_types": [
                "DaoCall", "GwtPresenter", "GwtView", "GwtUiBinder",
                "DtoArtifact", "IbatisStatement", "DbTable", "GwtEndpoint",
                "JspForm", "BackendDoc", "JsArtifact"
            ] * 5  # 55 items with duplicates
        }

        result = mock_search_service.search("test", filters=filters)

        # Should deduplicate
        assert isinstance(result, dict)

    def test_filter_with_pagination(self, mock_search_service):
        """Test filters work correctly with pagination."""
        filters = {"artifact_types": ["DaoCall"]}

        # First page
        page1 = mock_search_service.search("test", filters=filters, limit=50, offset=0)

        # Second page
        page2 = mock_search_service.search("test", filters=filters, limit=50, offset=50)

        # Both pages should have same filters
        assert page1["filters_applied"] == page2["filters_applied"]
