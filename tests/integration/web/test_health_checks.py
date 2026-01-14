"""
Integration tests for health checks (T019).

Tests the service health checking functionality including:
- Weaviate health check via HTTP
- Ollama health check via HTTP
- SQLite health check via connection
- Error handling for unavailable services
- Health status response format
"""

import pytest
import sqlite3
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import httpx

from codeindex.web.app import check_service_health


class TestHealthChecksIntegration:
    """Integration tests for check_service_health function."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test databases."""
        temp_path = tempfile.mkdtemp()
        yield Path(temp_path)
        shutil.rmtree(temp_path, ignore_errors=True)

    @pytest.fixture
    def mock_config(self, temp_dir):
        """Mock configuration for tests."""
        db_path = str(temp_dir / "test.db")

        # Create a valid database file
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE test (id INTEGER)")
        conn.commit()
        conn.close()

        return {
            "WEAVIATE_URL": "http://localhost:8080",
            "OLLAMA_BASE_URL": "http://localhost:11434",
            "WORKSPACE_DB_PATH": db_path
        }

    def test_all_services_available(self, mock_config):
        """Test health check when all services are available."""
        with patch("codeindex.web.app.get_config", return_value=mock_config):
            with patch("httpx.get") as mock_get:
                # Mock successful HTTP responses
                mock_response = Mock()
                mock_response.status_code = 200
                mock_get.return_value = mock_response

                result = check_service_health()

        assert result["weaviate"]["status"] == "available"
        assert result["weaviate"]["url"] == "http://localhost:8080"
        assert result["weaviate"]["error"] is None

        assert result["ollama"]["status"] == "available"
        assert result["ollama"]["url"] == "http://localhost:11434"
        assert result["ollama"]["error"] is None

        assert result["sqlite"]["status"] == "available"
        assert result["sqlite"]["path"] == mock_config["WORKSPACE_DB_PATH"]
        assert result["sqlite"]["error"] is None

    def test_weaviate_unavailable_connection_error(self, mock_config):
        """Test Weaviate unavailable due to connection error."""
        with patch("codeindex.web.app.get_config", return_value=mock_config):
            with patch("httpx.get") as mock_get:
                # Mock Weaviate connection error
                def side_effect(url, timeout):
                    if "localhost:8080" in url:
                        raise httpx.ConnectError("Connection refused")
                    mock_response = Mock()
                    mock_response.status_code = 200
                    return mock_response

                mock_get.side_effect = side_effect

                result = check_service_health()

        assert result["weaviate"]["status"] == "unavailable"
        assert "Connection refused" in result["weaviate"]["error"]

    def test_weaviate_unavailable_http_error(self, mock_config):
        """Test Weaviate unavailable due to HTTP error."""
        with patch("codeindex.web.app.get_config", return_value=mock_config):
            with patch("httpx.get") as mock_get:
                # Mock Weaviate HTTP error
                def side_effect(url, timeout):
                    if "localhost:8080" in url:
                        mock_response = Mock()
                        mock_response.status_code = 503
                        return mock_response
                    mock_response = Mock()
                    mock_response.status_code = 200
                    return mock_response

                mock_get.side_effect = side_effect

                result = check_service_health()

        assert result["weaviate"]["status"] == "unavailable"
        assert result["weaviate"]["error"] == "HTTP 503"

    def test_weaviate_unavailable_timeout(self, mock_config):
        """Test Weaviate unavailable due to timeout."""
        with patch("codeindex.web.app.get_config", return_value=mock_config):
            with patch("httpx.get") as mock_get:
                # Mock Weaviate timeout
                def side_effect(url, timeout):
                    if "localhost:8080" in url:
                        raise httpx.TimeoutException("Request timed out")
                    mock_response = Mock()
                    mock_response.status_code = 200
                    return mock_response

                mock_get.side_effect = side_effect

                result = check_service_health()

        assert result["weaviate"]["status"] == "unavailable"
        assert "timed out" in result["weaviate"]["error"].lower()

    def test_ollama_unavailable_connection_error(self, mock_config):
        """Test Ollama unavailable due to connection error."""
        with patch("codeindex.web.app.get_config", return_value=mock_config):
            with patch("httpx.get") as mock_get:
                # Mock Ollama connection error
                def side_effect(url, timeout):
                    if "localhost:11434" in url:
                        raise httpx.ConnectError("Connection refused")
                    mock_response = Mock()
                    mock_response.status_code = 200
                    return mock_response

                mock_get.side_effect = side_effect

                result = check_service_health()

        assert result["ollama"]["status"] == "unavailable"
        assert "Connection refused" in result["ollama"]["error"]

    def test_ollama_unavailable_http_error(self, mock_config):
        """Test Ollama unavailable due to HTTP error."""
        with patch("codeindex.web.app.get_config", return_value=mock_config):
            with patch("httpx.get") as mock_get:
                # Mock Ollama HTTP error
                def side_effect(url, timeout):
                    if "localhost:11434" in url:
                        mock_response = Mock()
                        mock_response.status_code = 404
                        return mock_response
                    mock_response = Mock()
                    mock_response.status_code = 200
                    return mock_response

                mock_get.side_effect = side_effect

                result = check_service_health()

        assert result["ollama"]["status"] == "unavailable"
        assert result["ollama"]["error"] == "HTTP 404"

    def test_sqlite_unavailable_missing_database(self, temp_dir):
        """Test SQLite unavailable when database doesn't exist and directory not writable."""
        mock_config = {
            "WEAVIATE_URL": "http://localhost:8080",
            "OLLAMA_BASE_URL": "http://localhost:11434",
            "WORKSPACE_DB_PATH": "/nonexistent/path/test.db"
        }

        with patch("codeindex.web.app.get_config", return_value=mock_config):
            with patch("httpx.get") as mock_get:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_get.return_value = mock_response

                result = check_service_health()

        assert result["sqlite"]["status"] == "unavailable"
        assert result["sqlite"]["error"] is not None

    def test_sqlite_unavailable_connection_error(self, temp_dir):
        """Test SQLite unavailable when connection fails."""
        db_path = str(temp_dir / "test.db")

        # Create a corrupted or locked database
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE test (id INTEGER)")
        conn.commit()
        # Don't close connection to simulate lock

        mock_config = {
            "WEAVIATE_URL": "http://localhost:8080",
            "OLLAMA_BASE_URL": "http://localhost:11434",
            "WORKSPACE_DB_PATH": db_path
        }

        with patch("codeindex.web.app.get_config", return_value=mock_config):
            with patch("httpx.get") as mock_get:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_get.return_value = mock_response

                with patch("sqlite3.connect") as mock_connect:
                    mock_connect.side_effect = sqlite3.OperationalError("database is locked")

                    result = check_service_health()

        conn.close()  # Clean up

        assert result["sqlite"]["status"] == "unavailable"
        assert "locked" in result["sqlite"]["error"].lower()

    def test_sqlite_available_new_database(self, temp_dir):
        """Test SQLite available when database doesn't exist but directory is writable."""
        db_path = str(temp_dir / "new_test.db")

        mock_config = {
            "WEAVIATE_URL": "http://localhost:8080",
            "OLLAMA_BASE_URL": "http://localhost:11434",
            "WORKSPACE_DB_PATH": db_path
        }

        with patch("codeindex.web.app.get_config", return_value=mock_config):
            with patch("httpx.get") as mock_get:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_get.return_value = mock_response

                result = check_service_health()

        assert result["sqlite"]["status"] == "available"
        assert result["sqlite"]["path"] == db_path

    def test_multiple_services_unavailable(self, temp_dir):
        """Test health check when multiple services are unavailable."""
        mock_config = {
            "WEAVIATE_URL": "http://localhost:8080",
            "OLLAMA_BASE_URL": "http://localhost:11434",
            "WORKSPACE_DB_PATH": "/nonexistent/test.db"
        }

        with patch("codeindex.web.app.get_config", return_value=mock_config):
            with patch("httpx.get") as mock_get:
                # Mock all HTTP services unavailable
                mock_get.side_effect = httpx.ConnectError("Connection refused")

                result = check_service_health()

        assert result["weaviate"]["status"] == "unavailable"
        assert result["ollama"]["status"] == "unavailable"
        assert result["sqlite"]["status"] == "unavailable"

    def test_health_check_response_structure(self, mock_config):
        """Test that health check response has correct structure."""
        with patch("codeindex.web.app.get_config", return_value=mock_config):
            with patch("httpx.get") as mock_get:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_get.return_value = mock_response

                result = check_service_health()

        # Verify structure
        assert "weaviate" in result
        assert "ollama" in result
        assert "sqlite" in result

        # Verify each service has required fields
        for service in ["weaviate", "ollama"]:
            assert "status" in result[service]
            assert "url" in result[service]
            assert "error" in result[service]

        assert "status" in result["sqlite"]
        assert "path" in result["sqlite"]
        assert "error" in result["sqlite"]

    def test_health_check_timeout_value(self, mock_config):
        """Test that health check uses correct timeout."""
        with patch("codeindex.web.app.get_config", return_value=mock_config):
            with patch("httpx.get") as mock_get:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_get.return_value = mock_response

                check_service_health()

                # Verify timeout was passed correctly
                calls = mock_get.call_args_list
                for call in calls:
                    assert call.kwargs.get("timeout") == 5.0

    def test_health_check_error_truncation(self, mock_config):
        """Test that error messages are truncated to 50 chars."""
        long_error = "A" * 100

        with patch("codeindex.web.app.get_config", return_value=mock_config):
            with patch("httpx.get") as mock_get:
                # Mock error with very long message
                def side_effect(url, timeout):
                    raise Exception(long_error)

                mock_get.side_effect = side_effect

                result = check_service_health()

        # All errors should be truncated
        assert len(result["weaviate"]["error"]) <= 50
        assert len(result["ollama"]["error"]) <= 50

    def test_health_check_sqlite_select_query(self, mock_config):
        """Test that SQLite health check executes SELECT query."""
        with patch("codeindex.web.app.get_config", return_value=mock_config):
            with patch("httpx.get") as mock_get:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_get.return_value = mock_response

                with patch("sqlite3.connect") as mock_connect:
                    mock_conn = MagicMock()
                    mock_cursor = MagicMock()
                    mock_conn.cursor.return_value = mock_cursor
                    mock_connect.return_value = mock_conn

                    check_service_health()

                    # Verify SELECT 1 was executed
                    mock_cursor.execute.assert_called_once_with("SELECT 1")
                    mock_conn.close.assert_called_once()

    def test_health_check_uses_config_values(self):
        """Test that health check uses values from config."""
        custom_config = {
            "WEAVIATE_URL": "http://custom-weaviate:9000",
            "OLLAMA_BASE_URL": "http://custom-ollama:9999",
            "WORKSPACE_DB_PATH": "/custom/path/db.sqlite"
        }

        with patch("codeindex.web.app.get_config", return_value=custom_config):
            with patch("httpx.get") as mock_get:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_get.return_value = mock_response

                with patch("sqlite3.connect"):
                    result = check_service_health()

        assert result["weaviate"]["url"] == "http://custom-weaviate:9000"
        assert result["ollama"]["url"] == "http://custom-ollama:9999"
        assert result["sqlite"]["path"] == "/custom/path/db.sqlite"

    def test_health_check_concurrent_calls(self, mock_config):
        """Test that health check handles concurrent calls safely."""
        with patch("codeindex.web.app.get_config", return_value=mock_config):
            with patch("httpx.get") as mock_get:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_get.return_value = mock_response

                # Call health check multiple times
                result1 = check_service_health()
                result2 = check_service_health()
                result3 = check_service_health()

        # All results should be independent
        assert result1 == result2 == result3
        assert result1 is not result2  # Different objects


class TestHealthCheckEndpoints:
    """Test specific health check endpoints."""

    def test_weaviate_ready_endpoint(self):
        """Test that Weaviate health check uses /v1/.well-known/ready endpoint."""
        mock_config = {
            "WEAVIATE_URL": "http://localhost:8080",
            "OLLAMA_BASE_URL": "http://localhost:11434",
            "WORKSPACE_DB_PATH": ":memory:"
        }

        with patch("codeindex.web.app.get_config", return_value=mock_config):
            with patch("httpx.get") as mock_get:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_get.return_value = mock_response

                check_service_health()

                # Find the Weaviate call
                weaviate_call = None
                for call in mock_get.call_args_list:
                    if "localhost:8080" in call.args[0]:
                        weaviate_call = call
                        break

                assert weaviate_call is not None
                assert "/v1/.well-known/ready" in weaviate_call.args[0]

    def test_ollama_tags_endpoint(self):
        """Test that Ollama health check uses /api/tags endpoint."""
        mock_config = {
            "WEAVIATE_URL": "http://localhost:8080",
            "OLLAMA_BASE_URL": "http://localhost:11434",
            "WORKSPACE_DB_PATH": ":memory:"
        }

        with patch("codeindex.web.app.get_config", return_value=mock_config):
            with patch("httpx.get") as mock_get:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_get.return_value = mock_response

                check_service_health()

                # Find the Ollama call
                ollama_call = None
                for call in mock_get.call_args_list:
                    if "localhost:11434" in call.args[0]:
                        ollama_call = call
                        break

                assert ollama_call is not None
                assert "/api/tags" in ollama_call.args[0]
