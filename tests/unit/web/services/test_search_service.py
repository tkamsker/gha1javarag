"""
Unit tests for search service (T020 - US1.1).

Tests the SearchService class including:
- Search execution with Weaviate integration
- Query building and filtering
- Result formatting and pagination
- Project and artifact type enumeration
- Error handling for unavailable services
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from codeindex.web.services.search_service import (
    SearchService,
    get_search_service
)


class TestSearchServiceInitialization:
    """Test SearchService initialization."""

    def test_service_initialization(self):
        """Test service initializes without Weaviate client."""
        service = SearchService()

        assert service.weaviate_client is None

    def test_lazy_client_initialization(self):
        """Test Weaviate client is initialized on first use."""
        service = SearchService()

        with patch("codeindex.web.services.search_service.WeaviateStore") as mock_store:
            mock_instance = Mock()
            mock_store.return_value = mock_instance

            client = service._get_weaviate_client()

            assert client is mock_instance
            assert service.weaviate_client is mock_instance
            mock_store.assert_called_once()

    def test_client_initialization_cached(self):
        """Test Weaviate client is cached after first initialization."""
        service = SearchService()

        with patch("codeindex.web.services.search_service.WeaviateStore") as mock_store:
            mock_instance = Mock()
            mock_store.return_value = mock_instance

            client1 = service._get_weaviate_client()
            client2 = service._get_weaviate_client()

            assert client1 is client2
            mock_store.assert_called_once()  # Only initialized once

    def test_client_initialization_error(self):
        """Test error handling when Weaviate client fails to initialize."""
        service = SearchService()

        with patch("codeindex.web.services.search_service.WeaviateStore") as mock_store:
            mock_store.side_effect = Exception("Connection failed")

            with pytest.raises(Exception, match="Connection failed"):
                service._get_weaviate_client()


class TestSearchExecution:
    """Test search execution functionality."""

    @pytest.fixture
    def service(self):
        """Create SearchService instance."""
        return SearchService()

    @pytest.fixture
    def mock_weaviate_client(self):
        """Create mock Weaviate client."""
        return Mock()

    def test_search_basic_query(self, service, mock_weaviate_client):
        """Test basic search execution."""
        service.weaviate_client = mock_weaviate_client

        result = service.search("test query")

        assert result["query"] == "test query"
        assert result["total_results"] == 0  # Placeholder
        assert result["results"] == []
        assert result["filters_applied"] == {}
        assert result["error"] is None

    def test_search_with_filters(self, service, mock_weaviate_client):
        """Test search with filters."""
        service.weaviate_client = mock_weaviate_client

        filters = {
            "artifact_types": ["DaoCall", "GwtPresenter"],
            "project": "com.example:app:1.0.0"
        }

        result = service.search("test query", filters=filters)

        assert result["query"] == "test query"
        assert result["filters_applied"] == filters

    def test_search_with_limit(self, service, mock_weaviate_client):
        """Test search with custom limit."""
        service.weaviate_client = mock_weaviate_client

        result = service.search("test query", limit=100)

        assert result["query"] == "test query"
        # Limit is used in actual query (placeholder doesn't use it yet)

    def test_search_with_offset(self, service, mock_weaviate_client):
        """Test search with pagination offset."""
        service.weaviate_client = mock_weaviate_client

        result = service.search("test query", limit=50, offset=50)

        assert result["query"] == "test query"
        # Offset is used for pagination (placeholder doesn't use it yet)

    def test_search_empty_query(self, service, mock_weaviate_client):
        """Test search with empty query."""
        service.weaviate_client = mock_weaviate_client

        result = service.search("")

        assert result["query"] == ""
        assert result["total_results"] == 0

    def test_search_long_query(self, service, mock_weaviate_client):
        """Test search with long query."""
        service.weaviate_client = mock_weaviate_client

        long_query = "test " * 1000  # 5000 characters

        result = service.search(long_query)

        assert result["query"] == long_query

    def test_search_special_characters(self, service, mock_weaviate_client):
        """Test search with special characters."""
        service.weaviate_client = mock_weaviate_client

        special_query = "test @#$%^&*() query"

        result = service.search(special_query)

        assert result["query"] == special_query

    def test_search_execution_error(self, service):
        """Test error handling when search execution fails."""
        with patch.object(service, "_get_weaviate_client") as mock_get_client:
            mock_get_client.side_effect = Exception("Weaviate unavailable")

            result = service.search("test query")

            assert result["error"] == "Weaviate unavailable"
            assert result["total_results"] == 0
            assert result["results"] == []

    def test_search_logs_execution(self, service, mock_weaviate_client):
        """Test that search execution is logged."""
        service.weaviate_client = mock_weaviate_client

        filters = {"artifact_types": ["DaoCall"]}

        with patch("codeindex.web.services.search_service.logger") as mock_logger:
            service.search("test query", filters=filters, limit=100)

            # Verify logging occurred
            mock_logger.info.assert_called()
            call_args = str(mock_logger.info.call_args)
            assert "test query" in call_args or "Executing search" in call_args


class TestGetAllProjects:
    """Test project enumeration."""

    @pytest.fixture
    def service(self):
        """Create SearchService instance."""
        return SearchService()

    @pytest.fixture
    def mock_weaviate_client(self):
        """Create mock Weaviate client."""
        return Mock()

    def test_get_all_projects_placeholder(self, service, mock_weaviate_client):
        """Test get_all_projects returns empty list (placeholder)."""
        service.weaviate_client = mock_weaviate_client

        projects = service.get_all_projects()

        assert projects == []

    def test_get_all_projects_error_handling(self, service):
        """Test error handling when getting projects fails."""
        with patch.object(service, "_get_weaviate_client") as mock_get_client:
            mock_get_client.side_effect = Exception("Weaviate unavailable")

            projects = service.get_all_projects()

            assert projects == []


class TestGetArtifactTypes:
    """Test artifact type enumeration."""

    @pytest.fixture
    def service(self):
        """Create SearchService instance."""
        return SearchService()

    def test_get_artifact_types_returns_all(self, service):
        """Test get_artifact_types returns all 11 types."""
        types = service.get_artifact_types()

        assert len(types) == 11
        assert "DaoCall" in types
        assert "GwtPresenter" in types
        assert "GwtView" in types
        assert "GwtUiBinder" in types
        assert "DtoArtifact" in types
        assert "IbatisStatement" in types
        assert "DbTable" in types
        assert "GwtEndpoint" in types
        assert "JspForm" in types
        assert "BackendDoc" in types
        assert "JsArtifact" in types

    def test_get_artifact_types_order(self, service):
        """Test artifact types are in expected order."""
        types = service.get_artifact_types()

        # First type should be DaoCall
        assert types[0] == "DaoCall"

        # Last type should be JsArtifact
        assert types[-1] == "JsArtifact"


class TestFormatSearchResult:
    """Test search result formatting."""

    @pytest.fixture
    def service(self):
        """Create SearchService instance."""
        return SearchService()

    def test_format_result_basic(self, service):
        """Test formatting a basic search result."""
        raw_result = {
            "id": "art-123",
            "class": "DaoCall",
            "file_path": "/path/to/file.java",
            "description": "Test description",
            "_additional": {"certainty": 0.85}
        }

        formatted = service.format_search_result(raw_result)

        assert formatted["id"] == "art-123"
        assert formatted["artifact_type"] == "DaoCall"
        assert formatted["file_path"] == "/path/to/file.java"
        assert formatted["confidence"] == 0.85
        assert "Test description" in formatted["preview"]

    def test_format_result_missing_fields(self, service):
        """Test formatting with missing fields uses defaults."""
        raw_result = {}

        formatted = service.format_search_result(raw_result)

        assert formatted["id"] == ""
        assert formatted["artifact_type"] == ""
        assert formatted["file_path"] == ""
        assert formatted["confidence"] == 0.0
        assert formatted["preview"] == ""

    def test_format_result_long_description(self, service):
        """Test long descriptions are truncated."""
        raw_result = {
            "id": "art-123",
            "description": "A" * 300  # 300 characters
        }

        formatted = service.format_search_result(raw_result)

        # Should be truncated to 200 chars + "..."
        assert len(formatted["preview"]) == 203
        assert formatted["preview"].endswith("...")

    def test_format_result_short_description(self, service):
        """Test short descriptions are not truncated."""
        raw_result = {
            "id": "art-123",
            "description": "Short description"
        }

        formatted = service.format_search_result(raw_result)

        assert formatted["preview"] == "Short description"
        assert not formatted["preview"].endswith("...")

    def test_format_result_metadata(self, service):
        """Test metadata field is included."""
        raw_result = {"id": "art-123"}

        formatted = service.format_search_result(raw_result)

        assert "metadata" in formatted
        assert isinstance(formatted["metadata"], dict)


class TestGetSearchService:
    """Test global service instance management."""

    def test_get_search_service_singleton(self):
        """Test get_search_service returns singleton instance."""
        service1 = get_search_service()
        service2 = get_search_service()

        assert service1 is service2

    def test_get_search_service_creates_instance(self):
        """Test get_search_service creates SearchService instance."""
        service = get_search_service()

        assert isinstance(service, SearchService)


class TestSearchServiceIntegration:
    """Integration tests for SearchService."""

    def test_search_workflow(self):
        """Test complete search workflow."""
        service = SearchService()

        with patch.object(service, "_get_weaviate_client") as mock_get_client:
            mock_client = Mock()
            mock_get_client.return_value = mock_client

            # Execute search
            result = service.search(
                query="authentication flow",
                filters={"artifact_types": ["GwtPresenter"]},
                limit=10
            )

            # Verify result structure
            assert "query" in result
            assert "total_results" in result
            assert "results" in result
            assert "filters_applied" in result
            assert "execution_time_ms" in result
            assert "error" in result

    def test_artifact_type_filter_workflow(self):
        """Test workflow for filtering by artifact type."""
        service = SearchService()

        # Get available types
        types = service.get_artifact_types()

        # Execute search with type filter
        filters = {"artifact_types": [types[0], types[1]]}

        with patch.object(service, "_get_weaviate_client"):
            result = service.search("test", filters=filters)

            assert result["filters_applied"]["artifact_types"] == [types[0], types[1]]

    def test_project_filter_workflow(self):
        """Test workflow for filtering by project."""
        service = SearchService()

        with patch.object(service, "_get_weaviate_client") as mock_get_client:
            mock_client = Mock()
            mock_get_client.return_value = mock_client

            # Get available projects
            projects = service.get_all_projects()

            # Execute search with project filter (even though projects is empty in placeholder)
            filters = {"project": "com.example:app:1.0.0"}
            result = service.search("test", filters=filters)

            assert result["filters_applied"]["project"] == "com.example:app:1.0.0"

    def test_pagination_workflow(self):
        """Test pagination workflow."""
        service = SearchService()

        with patch.object(service, "_get_weaviate_client"):
            # Get first page
            page1 = service.search("test", limit=50, offset=0)

            # Get second page
            page2 = service.search("test", limit=50, offset=50)

            # Both should have same query
            assert page1["query"] == page2["query"] == "test"

    def test_error_recovery_workflow(self):
        """Test error recovery workflow."""
        service = SearchService()

        # First search fails
        with patch.object(service, "_get_weaviate_client") as mock_get_client:
            mock_get_client.side_effect = Exception("Connection failed")

            result1 = service.search("test")
            assert result1["error"] is not None

        # Second search succeeds (connection restored)
        with patch.object(service, "_get_weaviate_client") as mock_get_client:
            mock_client = Mock()
            mock_get_client.return_value = mock_client

            result2 = service.search("test")
            # Placeholder doesn't have error
            assert result2["error"] is None
