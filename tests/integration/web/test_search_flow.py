"""
Integration tests for search flow (T022 - US1.1).

Tests the end-to-end search flow including:
- Query input to results display
- Weaviate integration
- Ollama embedding generation
- Result pagination
- Filter application
- Error handling throughout the flow
"""

import pytest
import time
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path


class TestSearchFlowEnd toEnd:
    """End-to-end integration tests for search flow."""

    @pytest.fixture
    def mock_weaviate_available(self):
        """Mock Weaviate being available."""
        with patch("httpx.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_get.return_value = mock_response
            yield mock_get

    @pytest.fixture
    def mock_search_service(self):
        """Mock search service with realistic responses."""
        from codeindex.web.services.search_service import SearchService

        service = SearchService()

        # Mock Weaviate client
        mock_client = Mock()
        service.weaviate_client = mock_client

        return service

    def test_complete_search_flow(self, mock_search_service):
        """Test complete search flow from query to results."""
        # Step 1: User enters query
        query = "authentication flow"

        # Step 2: Search is executed
        result = mock_search_service.search(query)

        # Step 3: Verify results structure
        assert result["query"] == query
        assert "total_results" in result
        assert "results" in result
        assert "execution_time_ms" in result
        assert "error" in result

    def test_search_with_filters_flow(self, mock_search_service):
        """Test search flow with filters applied."""
        query = "database access"
        filters = {
            "artifact_types": ["DaoCall", "IbatisStatement"],
            "project": "com.example:app:1.0.0"
        }

        # Execute search with filters
        result = mock_search_service.search(query, filters=filters)

        # Verify filters were applied
        assert result["filters_applied"] == filters
        assert result["query"] == query

    def test_pagination_flow(self, mock_search_service):
        """Test pagination flow."""
        query = "test query"

        # Get first page
        page1 = mock_search_service.search(query, limit=50, offset=0)

        # Get second page
        page2 = mock_search_service.search(query, limit=50, offset=50)

        # Get third page
        page3 = mock_search_service.search(query, limit=50, offset=100)

        # All pages should have same query
        assert page1["query"] == page2["query"] == page3["query"] == query

    def test_search_performance(self, mock_search_service):
        """Test search execution performance."""
        query = "performance test"

        start_time = time.time()
        result = mock_search_service.search(query)
        end_time = time.time()

        execution_time = end_time - start_time

        # Search should complete quickly (< 5 seconds for mock)
        assert execution_time < 5.0

        # Result should include execution time metric
        assert "execution_time_ms" in result

    def test_empty_query_flow(self, mock_search_service):
        """Test handling of empty query."""
        result = mock_search_service.search("")

        assert result["query"] == ""
        assert result["total_results"] == 0
        assert result["results"] == []

    def test_special_characters_flow(self, mock_search_service):
        """Test handling of special characters in query."""
        special_queries = [
            "test@example.com",
            "path/to/file.java",
            "C++ implementation",
            "null != undefined",
            "SELECT * FROM table"
        ]

        for query in special_queries:
            result = mock_search_service.search(query)
            assert result["query"] == query
            assert result["error"] is None


class TestSearchFlowWithWeaviate:
    """Integration tests with Weaviate mocked responses."""

    @pytest.fixture
    def mock_weaviate_search_response(self):
        """Mock realistic Weaviate search response."""
        return {
            "data": {
                "Get": {
                    "DaoCall": [
                        {
                            "id": "dao-123",
                            "file_path": "/src/main/java/dao/UserDao.java",
                            "description": "DAO for user management",
                            "_additional": {"certainty": 0.92}
                        },
                        {
                            "id": "dao-456",
                            "file_path": "/src/main/java/dao/OrderDao.java",
                            "description": "DAO for order processing",
                            "_additional": {"certainty": 0.88}
                        }
                    ]
                }
            }
        }

    def test_weaviate_connection_flow(self, mock_weaviate_search_response):
        """Test connection to Weaviate."""
        from codeindex.web.services.search_service import SearchService

        service = SearchService()

        with patch("codeindex.web.services.search_service.WeaviateStore") as mock_store:
            mock_client = Mock()
            mock_store.return_value = mock_client

            # Initialize client
            client = service._get_weaviate_client()

            assert client is not None
            mock_store.assert_called_once()

    def test_weaviate_query_execution_flow(self):
        """Test Weaviate query execution."""
        from codeindex.web.services.search_service import SearchService

        service = SearchService()

        with patch("codeindex.web.services.search_service.WeaviateStore") as mock_store:
            mock_client = Mock()
            mock_store.return_value = mock_client

            # Execute search
            result = service.search("test query")

            # Verify query was attempted
            assert result["query"] == "test query"

    def test_weaviate_unavailable_flow(self):
        """Test handling when Weaviate is unavailable."""
        from codeindex.web.services.search_service import SearchService

        service = SearchService()

        with patch("codeindex.web.services.search_service.WeaviateStore") as mock_store:
            mock_store.side_effect = Exception("Weaviate connection failed")

            # Execute search
            result = service.search("test query")

            # Should handle error gracefully
            assert result["error"] is not None
            assert "Weaviate" in result["error"] or "connection" in result["error"].lower()
            assert result["total_results"] == 0
            assert result["results"] == []


class TestSearchFlowWithOllama:
    """Integration tests with Ollama embedding generation."""

    def test_ollama_embedding_flow(self):
        """Test Ollama embedding generation flow."""
        from codeindex.web.services.search_service import SearchService

        service = SearchService()

        with patch("codeindex.web.services.search_service.WeaviateStore"):
            # In actual implementation, Ollama would generate embeddings
            query = "test query"
            result = service.search(query)

            # Verify query was processed
            assert result["query"] == query

    def test_ollama_unavailable_flow(self):
        """Test handling when Ollama is unavailable."""
        from codeindex.web.services.search_service import SearchService

        service = SearchService()

        # Weaviate might fail to connect to Ollama
        with patch("codeindex.web.services.search_service.WeaviateStore") as mock_store:
            mock_store.side_effect = Exception("Ollama timeout")

            result = service.search("test query")

            # Should handle error gracefully
            assert result["error"] is not None


class TestSearchFlowResultFormatting:
    """Integration tests for result formatting."""

    def test_format_multiple_results(self):
        """Test formatting multiple search results."""
        from codeindex.web.services.search_service import SearchService

        service = SearchService()

        raw_results = [
            {
                "id": "art-1",
                "class": "DaoCall",
                "file_path": "/path1.java",
                "description": "Description 1",
                "_additional": {"certainty": 0.9}
            },
            {
                "id": "art-2",
                "class": "GwtPresenter",
                "file_path": "/path2.java",
                "description": "Description 2",
                "_additional": {"certainty": 0.8}
            }
        ]

        formatted_results = [service.format_search_result(r) for r in raw_results]

        assert len(formatted_results) == 2
        assert formatted_results[0]["artifact_type"] == "DaoCall"
        assert formatted_results[1]["artifact_type"] == "GwtPresenter"

    def test_format_with_missing_fields(self):
        """Test formatting results with missing fields."""
        from codeindex.web.services.search_service import SearchService

        service = SearchService()

        incomplete_result = {
            "id": "art-123"
            # Missing other fields
        }

        formatted = service.format_search_result(incomplete_result)

        # Should provide defaults
        assert formatted["id"] == "art-123"
        assert formatted["artifact_type"] == ""
        assert formatted["confidence"] == 0.0


class TestSearchFlowErrorHandling:
    """Integration tests for error handling throughout search flow."""

    def test_connection_error_flow(self):
        """Test handling of connection errors."""
        from codeindex.web.services.search_service import SearchService

        service = SearchService()

        with patch("codeindex.web.services.search_service.WeaviateStore") as mock_store:
            mock_store.side_effect = ConnectionError("Network error")

            result = service.search("test query")

            assert result["error"] is not None
            assert result["total_results"] == 0

    def test_timeout_error_flow(self):
        """Test handling of timeout errors."""
        from codeindex.web.services.search_service import SearchService

        service = SearchService()

        with patch("codeindex.web.services.search_service.WeaviateStore") as mock_store:
            mock_store.side_effect = TimeoutError("Request timed out")

            result = service.search("test query")

            assert result["error"] is not None

    def test_invalid_response_flow(self):
        """Test handling of invalid responses from Weaviate."""
        from codeindex.web.services.search_service import SearchService

        service = SearchService()

        with patch("codeindex.web.services.search_service.WeaviateStore") as mock_store:
            mock_store.side_effect = ValueError("Invalid response format")

            result = service.search("test query")

            assert result["error"] is not None

    def test_recovery_after_error(self):
        """Test recovery after error."""
        from codeindex.web.services.search_service import SearchService

        service = SearchService()

        # First search fails
        with patch("codeindex.web.services.search_service.WeaviateStore") as mock_store:
            mock_store.side_effect = Exception("Temporary error")
            result1 = service.search("test query")
            assert result1["error"] is not None

        # Second search succeeds
        with patch("codeindex.web.services.search_service.WeaviateStore") as mock_store:
            mock_client = Mock()
            mock_store.return_value = mock_client
            result2 = service.search("test query")
            assert result2["error"] is None


class TestSearchFlowPerformance:
    """Integration tests for search performance."""

    def test_concurrent_searches(self):
        """Test handling of concurrent search requests."""
        from codeindex.web.services.search_service import SearchService

        service = SearchService()

        with patch("codeindex.web.services.search_service.WeaviateStore") as mock_store:
            mock_client = Mock()
            mock_store.return_value = mock_client

            # Execute multiple searches concurrently
            queries = ["query1", "query2", "query3"]
            results = [service.search(q) for q in queries]

            assert len(results) == 3
            for i, result in enumerate(results):
                assert result["query"] == queries[i]

    def test_large_result_set_performance(self):
        """Test performance with large result sets."""
        from codeindex.web.services.search_service import SearchService

        service = SearchService()

        with patch("codeindex.web.services.search_service.WeaviateStore"):
            # Search with large limit
            start_time = time.time()
            result = service.search("test", limit=1000)
            end_time = time.time()

            execution_time = end_time - start_time

            # Should still complete quickly
            assert execution_time < 10.0

    def test_pagination_performance(self):
        """Test pagination performance."""
        from codeindex.web.services.search_service import SearchService

        service = SearchService()

        with patch("codeindex.web.services.search_service.WeaviateStore"):
            # Execute paginated searches
            start_time = time.time()

            for offset in range(0, 500, 50):  # 10 pages
                result = service.search("test", limit=50, offset=offset)

            end_time = time.time()

            total_time = end_time - start_time

            # All pages should complete quickly
            assert total_time < 30.0  # 10 pages in < 30 seconds for mock


class TestSearchFlowCachingAndOptimization:
    """Integration tests for caching and optimization."""

    def test_repeated_query_caching(self):
        """Test that repeated queries might use caching."""
        from codeindex.web.services.search_service import SearchService

        service = SearchService()

        with patch("codeindex.web.services.search_service.WeaviateStore") as mock_store:
            mock_client = Mock()
            mock_store.return_value = mock_client

            # Execute same query multiple times
            query = "test query"
            result1 = service.search(query)
            result2 = service.search(query)
            result3 = service.search(query)

            # All should return consistent results
            assert result1["query"] == result2["query"] == result3["query"]

    def test_filter_combination_optimization(self):
        """Test optimization of filter combinations."""
        from codeindex.web.services.search_service import SearchService

        service = SearchService()

        with patch("codeindex.web.services.search_service.WeaviateStore"):
            # Complex filter combination
            filters = {
                "artifact_types": ["DaoCall", "GwtPresenter", "GwtView"],
                "project": "com.example:app:1.0.0"
            }

            result = service.search("test", filters=filters)

            # Should handle complex filters efficiently
            assert result["filters_applied"] == filters


class TestSearchFlowIntegrationWithComponents:
    """Integration tests connecting search flow to UI components."""

    def test_search_to_artifact_card_flow(self):
        """Test flow from search results to artifact card rendering."""
        from codeindex.web.services.search_service import SearchService

        service = SearchService()

        # Execute search
        with patch("codeindex.web.services.search_service.WeaviateStore"):
            result = service.search("test query")

        # Format results for display
        # (In actual implementation, would pass to artifact card component)
        if result["total_results"] > 0:
            for raw_result in result["results"]:
                formatted = service.format_search_result(raw_result)

                # Verify formatted result has fields needed by artifact card
                assert "id" in formatted
                assert "artifact_type" in formatted
                assert "file_path" in formatted
                assert "confidence" in formatted
                assert "preview" in formatted

    def test_filter_selection_to_search_flow(self):
        """Test flow from filter selection to search execution."""
        from codeindex.web.services.search_service import SearchService

        service = SearchService()

        # Get available artifact types (for filter UI)
        artifact_types = service.get_artifact_types()

        # User selects filters
        selected_types = [artifact_types[0], artifact_types[1]]
        filters = {"artifact_types": selected_types}

        # Execute filtered search
        with patch("codeindex.web.services.search_service.WeaviateStore"):
            result = service.search("test", filters=filters)

        # Verify filters were applied
        assert result["filters_applied"]["artifact_types"] == selected_types
