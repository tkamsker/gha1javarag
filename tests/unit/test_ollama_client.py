"""
Unit tests for OllamaClient.

Tests timeout configuration, error handling, and logging.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import httpx

from codeindex.services.ollama_client import OllamaClient


@pytest.fixture
def ollama_client():
    """OllamaClient instance with default configuration."""
    return OllamaClient(
        base_url="http://localhost:11434",
        model="gemma2:12b",
        read_timeout=240.0
    )


def test_ollama_timeout_logging(ollama_client, caplog):
    """
    Test that timeout exceptions log the correct timeout value.

    This test verifies the fix for NameError where READ_TIMEOUT was undefined.
    The error message should now correctly reference self.read_timeout.
    """
    # Arrange: Mock httpx client to raise TimeoutException
    with patch.object(ollama_client, 'client') as mock_client:
        mock_response = Mock()
        mock_response.post.side_effect = httpx.TimeoutException("Request timed out")
        mock_client.post.side_effect = httpx.TimeoutException("Request timed out")

        # Act & Assert: Call should raise TimeoutError and log correct timeout
        with pytest.raises(TimeoutError, match="Ollama request timed out"):
            ollama_client.call_ollama(
                prompt="test prompt",
                temperature=0.2,
                format_json=True
            )

        # Verify log message contains correct timeout value (self.read_timeout)
        assert "Ollama timeout after 240.0s" in caplog.text
        assert "READ_TIMEOUT" not in caplog.text  # Ensure old bug doesn't exist


def test_ollama_client_initialization_with_custom_timeout():
    """Test that OllamaClient correctly stores custom timeout values."""
    # Arrange & Act
    client = OllamaClient(
        base_url="http://localhost:11434",
        model="gemma2:12b",
        connect_timeout=15.0,
        read_timeout=300.0
    )

    # Assert
    assert client.read_timeout == 300.0
    assert client.connect_timeout == 15.0


def test_ollama_client_default_timeout():
    """Test that OllamaClient uses default timeout when not specified."""
    # Arrange & Act
    client = OllamaClient()

    # Assert - should use DEFAULT_READ_TIMEOUT (240.0)
    assert client.read_timeout == 240.0
    assert client.connect_timeout == 10.0
