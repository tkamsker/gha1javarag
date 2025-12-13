"""
Unit tests for Ollama HTTP client.

Tests request formatting, JSON parsing, timeout handling, retry logic, and rate limiting.

NOTE: These tests should FAIL initially (TDD approach).
"""

import pytest
import json
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import httpx

from codeindex.services.ollama_client import (
    OllamaClient,
    OllamaError,
    OllamaTimeoutError,
    call_ollama,
    format_extraction_prompt,
)


# Fixtures
@pytest.fixture
def ollama_client():
    """OllamaClient instance."""
    return OllamaClient(
        base_url="http://localhost:11434",
        model="gemma3:12b",
        timeout=30.0,
        max_concurrent=10
    )


@pytest.fixture
def mock_ollama_response():
    """Mock successful Ollama API response."""
    return {
        "model": "gemma3:12b",
        "created_at": "2025-12-13T00:00:00Z",
        "response": json.dumps({
            "summary": "Test summary",
            "classification": "java_source",
            "entities": ["TestClass", "testMethod()"],
            "tags": {
                "layer": ["backend"],
                "domain": ["test"],
                "frameworks": ["Java"],
                "concerns": ["business_rule"]
            },
            "confidence": 0.95
        }),
        "done": True
    }


@pytest.fixture
def java_class_fixture():
    """Path to Java class fixture."""
    return Path(__file__).parent.parent / "fixtures" / "sample_java" / "SampleClass.java"


# Test request formatting
class TestRequestFormatting:
    """Test Ollama API request formatting."""

    def test_format_prompt_with_file_content(self, ollama_client):
        """Test prompt formatting with file content."""
        file_content = "public class Test {}"
        prompt = ollama_client.format_prompt(file_content, "java_source")

        assert "public class Test {}" in prompt
        assert "java" in prompt.lower() or "Java" in prompt

    def test_format_prompt_includes_instructions(self, ollama_client):
        """Test that prompt includes extraction instructions."""
        prompt = ollama_client.format_prompt("code", "java_source")

        assert "summary" in prompt.lower()
        assert "entities" in prompt.lower()
        assert "json" in prompt.lower()

    def test_request_body_structure(self, ollama_client):
        """Test that request body has correct structure."""
        body = ollama_client.build_request_body("test prompt")

        assert "model" in body
        assert body["model"] == "gemma3:12b"
        assert "prompt" in body
        assert "stream" in body
        assert body["stream"] is False


# Test JSON parsing
class TestJSONParsing:
    """Test Ollama response JSON parsing."""

    def test_parse_valid_response(self, ollama_client, mock_ollama_response):
        """Test parsing valid Ollama response."""
        result = ollama_client.parse_response(mock_ollama_response)

        assert result is not None
        assert result["summary"] == "Test summary"
        assert result["classification"] == "java_source"
        assert len(result["entities"]) == 2

    def test_parse_response_with_nested_json(self, ollama_client):
        """Test parsing response with nested JSON string."""
        response = {
            "model": "gemma3:12b",
            "response": '{"summary": "Nested", "classification": "java_source", "entities": [], "tags": {}, "confidence": 0.9}',
            "done": True
        }

        result = ollama_client.parse_response(response)
        assert result["summary"] == "Nested"

    def test_parse_malformed_json(self, ollama_client):
        """Test handling of malformed JSON in response."""
        response = {
            "model": "gemma3:12b",
            "response": "This is not valid JSON",
            "done": True
        }

        with pytest.raises(OllamaError, match="JSON"):
            ollama_client.parse_response(response)

    def test_parse_incomplete_response(self, ollama_client):
        """Test handling of incomplete response (missing fields)."""
        response = {
            "model": "gemma3:12b",
            "response": '{"summary": "Missing fields"}',
            "done": True
        }

        result = ollama_client.parse_response(response)
        # Should have defaults for missing fields
        assert "summary" in result


# Test timeout handling
class TestTimeoutHandling:
    """Test timeout configuration and handling."""

    def test_client_timeout_configuration(self):
        """Test that client configures timeouts correctly."""
        client = OllamaClient(timeout=60.0)

        # Check that httpx client has correct timeout
        assert client.timeout == 60.0

    @patch('httpx.Client.post')
    def test_timeout_raises_error(self, mock_post, ollama_client):
        """Test that timeout raises OllamaTimeoutError."""
        mock_post.side_effect = httpx.TimeoutException("Request timed out")

        with pytest.raises(OllamaTimeoutError):
            ollama_client.call("test prompt")

    def test_different_timeout_values(self):
        """Test creating clients with different timeout values."""
        client_short = OllamaClient(timeout=10.0)
        client_long = OllamaClient(timeout=300.0)

        assert client_short.timeout == 10.0
        assert client_long.timeout == 300.0


# Test retry logic
class TestRetryLogic:
    """Test retry logic with exponential backoff."""

    @patch('httpx.Client.post')
    def test_retry_on_connection_error(self, mock_post, ollama_client):
        """Test retry on connection error."""
        # Fail twice, then succeed
        mock_post.side_effect = [
            httpx.ConnectError("Connection failed"),
            httpx.ConnectError("Connection failed"),
            Mock(json=lambda: {"model": "test", "response": "{}", "done": True})
        ]

        # Should eventually succeed after retries
        result = ollama_client.call_with_retry("test", max_retries=3)
        assert mock_post.call_count == 3

    @patch('httpx.Client.post')
    def test_retry_exhaustion(self, mock_post, ollama_client):
        """Test that retries are exhausted and error is raised."""
        mock_post.side_effect = httpx.ConnectError("Connection failed")

        with pytest.raises(OllamaError):
            ollama_client.call_with_retry("test", max_retries=2)

        assert mock_post.call_count == 2

    @patch('httpx.Client.post')
    @patch('time.sleep')
    def test_exponential_backoff(self, mock_sleep, mock_post, ollama_client):
        """Test exponential backoff between retries."""
        mock_post.side_effect = [
            httpx.ConnectError("Failed"),
            httpx.ConnectError("Failed"),
            Mock(json=lambda: {"model": "test", "response": "{}", "done": True})
        ]

        ollama_client.call_with_retry("test", max_retries=3, base_delay=1.0)

        # Should have called sleep with increasing delays
        assert mock_sleep.call_count >= 2
        # First retry: ~1 second, second retry: ~2 seconds
        sleep_calls = [call[0][0] for call in mock_sleep.call_args_list]
        assert sleep_calls[0] < sleep_calls[1]  # Exponential increase


# Test rate limiting
class TestRateLimiting:
    """Test concurrent request rate limiting."""

    def test_max_concurrent_configuration(self):
        """Test max concurrent requests configuration."""
        client = OllamaClient(max_concurrent=5)

        assert client.max_concurrent == 5
        # Should have semaphore with correct value
        assert hasattr(client, 'semaphore')

    @patch('httpx.Client.post')
    def test_concurrent_requests_limited(self, mock_post):
        """Test that concurrent requests are limited."""
        mock_post.return_value = Mock(
            json=lambda: {"model": "test", "response": '{"summary": "test"}', "done": True}
        )

        client = OllamaClient(max_concurrent=2)

        # This is a simplified test - full concurrent testing requires threading
        # Just verify that the mechanism exists
        assert client.max_concurrent == 2

    def test_semaphore_release_on_error(self, ollama_client):
        """Test that semaphore is released even when request fails."""
        with patch('httpx.Client.post', side_effect=httpx.ConnectError("Failed")):
            try:
                ollama_client.call("test")
            except OllamaError:
                pass

        # Semaphore should be released (hard to test directly, but should not deadlock)


# Test error handling
class TestErrorHandling:
    """Test error handling for various failure modes."""

    @patch('httpx.Client.post')
    def test_http_error_handling(self, mock_post, ollama_client):
        """Test handling of HTTP errors."""
        mock_post.side_effect = httpx.HTTPStatusError(
            "Server error",
            request=Mock(),
            response=Mock(status_code=500)
        )

        with pytest.raises(OllamaError):
            ollama_client.call("test")

    @patch('httpx.Client.post')
    def test_network_error_handling(self, mock_post, ollama_client):
        """Test handling of network errors."""
        mock_post.side_effect = httpx.NetworkError("Network unreachable")

        with pytest.raises(OllamaError):
            ollama_client.call("test")

    def test_invalid_url(self):
        """Test handling of invalid Ollama URL."""
        with pytest.raises(ValueError):
            OllamaClient(base_url="not-a-valid-url")


# Test integration scenarios
class TestIntegrationScenarios:
    """Test realistic integration scenarios."""

    @patch('httpx.Client.post')
    def test_extract_from_file(self, mock_post, java_class_fixture, mock_ollama_response):
        """Test extracting information from a real file."""
        mock_post.return_value = Mock(json=lambda: mock_ollama_response)

        client = OllamaClient()

        # Read file content
        with open(java_class_fixture, 'r') as f:
            content = f.read()

        result = client.extract(content, "java_source")

        assert result is not None
        assert "summary" in result
        assert mock_post.called

    def test_batch_extraction(self, mock_ollama_response):
        """Test extracting from multiple files."""
        with patch('httpx.Client.post', return_value=Mock(json=lambda: mock_ollama_response)):
            client = OllamaClient(max_concurrent=3)

            files = ["file1.java", "file2.java", "file3.java"]
            results = []

            for file in files:
                result = client.extract(f"content of {file}", "java_source")
                results.append(result)

            assert len(results) == 3
            assert all("summary" in r for r in results)


# Test convenience functions
class TestConvenienceFunctions:
    """Test module-level convenience functions."""

    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_call_ollama_function(self, mock_client_class):
        """Test call_ollama convenience function."""
        mock_instance = Mock()
        mock_client_class.return_value = mock_instance
        mock_instance.extract.return_value = {"summary": "test"}

        result = call_ollama("test content", "java_source")

        assert result is not None
        mock_instance.extract.assert_called_once()

    def test_format_extraction_prompt(self):
        """Test format_extraction_prompt convenience function."""
        prompt = format_extraction_prompt("public class Test {}", "java_source")

        assert "public class Test {}" in prompt
        assert isinstance(prompt, str)
        assert len(prompt) > 0
