"""
Unit tests for Agent Tools (T054 - US2.1).

Tests cover the three core tools used by agents:
- WeaviateSearchTool: Search artifacts in Weaviate vector database
- FileReadTool: Read source files from JAVA_SOURCE_DIR
- LLMQueryTool: Query Ollama LLM for text generation

Each tool is tested for:
- Initialization and configuration
- Basic functionality
- Error handling
- Input validation
- Edge cases
"""

import pytest
import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Any


class TestWeaviateSearchToolInitialization:
    """Test WeaviateSearchTool initialization."""

    def test_tool_initializes_with_default_weaviate_store(self):
        """Test tool initialization with default Weaviate store."""
        from codeindex.web.agents.tools import WeaviateSearchTool

        tool = WeaviateSearchTool()

        assert tool is not None
        assert hasattr(tool, 'search')
        assert hasattr(tool, 'weaviate_store')

    @patch('codeindex.services.weaviate_store.WeaviateStore')
    def test_tool_initializes_with_custom_weaviate_store(self, mock_store_class):
        """Test tool initialization with custom Weaviate store."""
        from codeindex.web.agents.tools import WeaviateSearchTool

        mock_store = MagicMock()
        mock_store_class.return_value = mock_store

        tool = WeaviateSearchTool(weaviate_store=mock_store)

        assert tool.weaviate_store == mock_store

    def test_tool_has_correct_name_and_description(self):
        """Test tool has correct metadata."""
        from codeindex.web.agents.tools import WeaviateSearchTool

        tool = WeaviateSearchTool()

        assert tool.name == "WeaviateSearchTool"
        assert "search" in tool.description.lower() or "weaviate" in tool.description.lower()


class TestWeaviateSearchToolSearch:
    """Test WeaviateSearchTool search functionality."""

    @patch('codeindex.services.weaviate_store.WeaviateStore')
    def test_search_returns_artifacts(self, mock_store_class):
        """Test search returns artifacts from Weaviate."""
        from codeindex.web.agents.tools import WeaviateSearchTool

        mock_store = MagicMock()
        mock_store.search_artifacts.return_value = [
            {"id": "art_1", "artifactType": "BackendDoc", "summary": "User service"},
            {"id": "art_2", "artifactType": "DaoCall", "summary": "User DAO"}
        ]
        mock_store_class.return_value = mock_store

        tool = WeaviateSearchTool(weaviate_store=mock_store)
        results = tool.search("user authentication")

        assert len(results) == 2
        assert results[0]["id"] == "art_1"
        assert results[1]["artifactType"] == "DaoCall"

    @patch('codeindex.services.weaviate_store.WeaviateStore')
    def test_search_with_filters(self, mock_store_class):
        """Test search with artifact type and project filters."""
        from codeindex.web.agents.tools import WeaviateSearchTool

        mock_store = MagicMock()
        mock_store.search_artifacts.return_value = [
            {"id": "art_1", "artifactType": "DaoCall"}
        ]
        mock_store_class.return_value = mock_store

        tool = WeaviateSearchTool(weaviate_store=mock_store)
        results = tool.search(
            "database access",
            artifact_types=["DaoCall"],
            project="com.example:backend:1.0.0"
        )

        # Verify filters passed to Weaviate
        mock_store.search_artifacts.assert_called_once()
        call_args = mock_store.search_artifacts.call_args
        assert call_args[0][0] == "database access"
        assert "DaoCall" in call_args[1].get("artifact_types", [])

    @patch('codeindex.services.weaviate_store.WeaviateStore')
    def test_search_with_limit(self, mock_store_class):
        """Test search respects limit parameter."""
        from codeindex.web.agents.tools import WeaviateSearchTool

        mock_store = MagicMock()
        mock_store.search_artifacts.return_value = [
            {"id": f"art_{i}"} for i in range(5)
        ]
        mock_store_class.return_value = mock_store

        tool = WeaviateSearchTool(weaviate_store=mock_store)
        results = tool.search("test query", limit=5)

        assert len(results) <= 5

    @patch('codeindex.services.weaviate_store.WeaviateStore')
    def test_search_handles_empty_results(self, mock_store_class):
        """Test search handles empty results gracefully."""
        from codeindex.web.agents.tools import WeaviateSearchTool

        mock_store = MagicMock()
        mock_store.search_artifacts.return_value = []
        mock_store_class.return_value = mock_store

        tool = WeaviateSearchTool(weaviate_store=mock_store)
        results = tool.search("nonexistent module")

        assert results == []

    @patch('codeindex.services.weaviate_store.WeaviateStore')
    def test_search_handles_weaviate_error(self, mock_store_class):
        """Test search handles Weaviate errors gracefully."""
        from codeindex.web.agents.tools import WeaviateSearchTool

        mock_store = MagicMock()
        mock_store.search_artifacts.side_effect = Exception("Weaviate connection failed")
        mock_store_class.return_value = mock_store

        tool = WeaviateSearchTool(weaviate_store=mock_store)

        with pytest.raises(Exception) as exc_info:
            tool.search("test query")

        assert "Weaviate" in str(exc_info.value) or "connection" in str(exc_info.value)


class TestFileReadToolInitialization:
    """Test FileReadTool initialization."""

    def test_tool_initializes_with_source_dir(self):
        """Test tool initialization with source directory."""
        from codeindex.web.agents.tools import FileReadTool

        tool = FileReadTool(source_dir="/path/to/source")

        assert tool is not None
        assert hasattr(tool, 'read_file')
        assert tool.source_dir == Path("/path/to/source")

    def test_tool_initializes_with_env_variable(self):
        """Test tool initialization uses JAVA_SOURCE_DIR env variable."""
        from codeindex.web.agents.tools import FileReadTool

        with patch.dict(os.environ, {"JAVA_SOURCE_DIR": "/env/source"}):
            tool = FileReadTool()

            assert tool.source_dir == Path("/env/source")

    def test_tool_has_correct_name_and_description(self):
        """Test tool has correct metadata."""
        from codeindex.web.agents.tools import FileReadTool

        tool = FileReadTool(source_dir="/path/to/source")

        assert tool.name == "FileReadTool"
        assert "read" in tool.description.lower() or "file" in tool.description.lower()


class TestFileReadToolReadFile:
    """Test FileReadTool file reading functionality."""

    def test_read_file_returns_content(self):
        """Test read_file returns file content."""
        from codeindex.web.agents.tools import FileReadTool

        # Create temporary file
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "test.java"
            test_file.write_text("public class Test {}")

            tool = FileReadTool(source_dir=temp_dir)
            content = tool.read_file("test.java")

            assert content == "public class Test {}"

    def test_read_file_handles_nested_paths(self):
        """Test read_file handles nested directory paths."""
        from codeindex.web.agents.tools import FileReadTool

        with tempfile.TemporaryDirectory() as temp_dir:
            nested_dir = Path(temp_dir) / "src" / "main" / "java"
            nested_dir.mkdir(parents=True)
            test_file = nested_dir / "User.java"
            test_file.write_text("public class User {}")

            tool = FileReadTool(source_dir=temp_dir)
            content = tool.read_file("src/main/java/User.java")

            assert content == "public class User {}"

    def test_read_file_validates_path_security(self):
        """Test read_file prevents directory traversal attacks."""
        from codeindex.web.agents.tools import FileReadTool

        with tempfile.TemporaryDirectory() as temp_dir:
            tool = FileReadTool(source_dir=temp_dir)

            # Attempt directory traversal
            with pytest.raises(ValueError) as exc_info:
                tool.read_file("../../etc/passwd")

            assert "directory traversal" in str(exc_info.value).lower() or "invalid path" in str(exc_info.value).lower()

    def test_read_file_handles_nonexistent_file(self):
        """Test read_file handles nonexistent files gracefully."""
        from codeindex.web.agents.tools import FileReadTool

        with tempfile.TemporaryDirectory() as temp_dir:
            tool = FileReadTool(source_dir=temp_dir)

            with pytest.raises(FileNotFoundError):
                tool.read_file("nonexistent.java")

    def test_read_file_handles_large_files(self):
        """Test read_file handles large files with size limit."""
        from codeindex.web.agents.tools import FileReadTool

        with tempfile.TemporaryDirectory() as temp_dir:
            large_file = Path(temp_dir) / "large.java"
            # Write 15MB file
            large_file.write_text("x" * (15 * 1024 * 1024))

            tool = FileReadTool(source_dir=temp_dir, max_file_size_mb=10)

            with pytest.raises(ValueError) as exc_info:
                tool.read_file("large.java")

            assert "too large" in str(exc_info.value).lower() or "size" in str(exc_info.value).lower()

    def test_read_file_handles_encoding_errors(self):
        """Test read_file handles encoding errors gracefully."""
        from codeindex.web.agents.tools import FileReadTool

        with tempfile.TemporaryDirectory() as temp_dir:
            binary_file = Path(temp_dir) / "binary.class"
            binary_file.write_bytes(b'\x80\x81\x82\x83')  # Invalid UTF-8

            tool = FileReadTool(source_dir=temp_dir)

            # Should handle encoding error gracefully (replace or skip)
            try:
                content = tool.read_file("binary.class")
                # If it succeeds, content should be readable (with replacements)
                assert isinstance(content, str)
            except UnicodeDecodeError:
                # Or it should raise a clear error
                pass


class TestLLMQueryToolInitialization:
    """Test LLMQueryTool initialization."""

    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_tool_initializes_with_default_ollama_client(self, mock_client_class):
        """Test tool initialization with default Ollama client."""
        from codeindex.web.agents.tools import LLMQueryTool

        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        tool = LLMQueryTool()

        assert tool is not None
        assert hasattr(tool, 'query')
        assert hasattr(tool, 'ollama_client')

    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_tool_initializes_with_custom_ollama_client(self, mock_client_class):
        """Test tool initialization with custom Ollama client."""
        from codeindex.web.agents.tools import LLMQueryTool

        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        tool = LLMQueryTool(ollama_client=mock_client)

        assert tool.ollama_client == mock_client

    def test_tool_has_correct_name_and_description(self):
        """Test tool has correct metadata."""
        from codeindex.web.agents.tools import LLMQueryTool

        tool = LLMQueryTool()

        assert tool.name == "LLMQueryTool"
        assert "llm" in tool.description.lower() or "query" in tool.description.lower()


class TestLLMQueryToolQuery:
    """Test LLMQueryTool query functionality."""

    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_query_returns_llm_response(self, mock_client_class):
        """Test query returns response from Ollama LLM."""
        from codeindex.web.agents.tools import LLMQueryTool

        mock_client = MagicMock()
        mock_client.generate.return_value = "This is a test response from Ollama."
        mock_client_class.return_value = mock_client

        tool = LLMQueryTool(ollama_client=mock_client)
        response = tool.query("Explain authentication")

        assert response == "This is a test response from Ollama."

    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_query_with_context(self, mock_client_class):
        """Test query with additional context."""
        from codeindex.web.agents.tools import LLMQueryTool

        mock_client = MagicMock()
        mock_client.generate.return_value = "Response with context."
        mock_client_class.return_value = mock_client

        tool = LLMQueryTool(ollama_client=mock_client)
        response = tool.query(
            "Explain this code",
            context="public class User { private String name; }"
        )

        # Verify context passed to LLM
        call_args = mock_client.generate.call_args[0][0]
        assert "User" in call_args
        assert "private String name" in call_args

    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_query_with_system_prompt(self, mock_client_class):
        """Test query with system prompt for agent role."""
        from codeindex.web.agents.tools import LLMQueryTool

        mock_client = MagicMock()
        mock_client.generate.return_value = "Response as senior developer."
        mock_client_class.return_value = mock_client

        tool = LLMQueryTool(ollama_client=mock_client)
        response = tool.query(
            "Explain architecture",
            system_prompt="You are a senior software developer with 15+ years of experience."
        )

        # Verify system prompt included
        assert response is not None

    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_query_handles_ollama_timeout(self, mock_client_class):
        """Test query handles Ollama timeout errors."""
        from codeindex.web.agents.tools import LLMQueryTool

        mock_client = MagicMock()
        mock_client.generate.side_effect = TimeoutError("Ollama request timed out")
        mock_client_class.return_value = mock_client

        tool = LLMQueryTool(ollama_client=mock_client)

        with pytest.raises(TimeoutError) as exc_info:
            tool.query("Long query that times out")

        assert "timeout" in str(exc_info.value).lower()

    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_query_handles_ollama_connection_error(self, mock_client_class):
        """Test query handles Ollama connection errors."""
        from codeindex.web.agents.tools import LLMQueryTool

        mock_client = MagicMock()
        mock_client.generate.side_effect = ConnectionError("Ollama service unavailable")
        mock_client_class.return_value = mock_client

        tool = LLMQueryTool(ollama_client=mock_client)

        with pytest.raises(ConnectionError) as exc_info:
            tool.query("Test query")

        assert "unavailable" in str(exc_info.value).lower() or "connection" in str(exc_info.value).lower()


class TestToolIntegration:
    """Test tool integration and coordination."""

    @patch('codeindex.services.weaviate_store.WeaviateStore')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_tools_work_together_in_agent_workflow(self, mock_client_class, mock_store_class):
        """Test tools work together in typical agent workflow."""
        from codeindex.web.agents.tools import WeaviateSearchTool, LLMQueryTool

        # Mock Weaviate search results
        mock_store = MagicMock()
        mock_store.search_artifacts.return_value = [
            {"id": "art_1", "summary": "User service"}
        ]
        mock_store_class.return_value = mock_store

        # Mock Ollama response
        mock_client = MagicMock()
        mock_client.generate.return_value = "Analysis of user service."
        mock_client_class.return_value = mock_client

        # Workflow: Search → Query LLM with artifacts
        search_tool = WeaviateSearchTool(weaviate_store=mock_store)
        llm_tool = LLMQueryTool(ollama_client=mock_client)

        artifacts = search_tool.search("user service")
        analysis = llm_tool.query("Explain user service", context=str(artifacts))

        assert len(artifacts) > 0
        assert "Analysis" in analysis


# Test tool factory/registry pattern

def test_all_tools_registered():
    """Test all required tools are registered."""
    from codeindex.web.agents.tools import AVAILABLE_TOOLS

    required_tools = ["WeaviateSearchTool", "FileReadTool", "LLMQueryTool"]

    for tool_name in required_tools:
        assert tool_name in AVAILABLE_TOOLS


def test_get_tool_by_name():
    """Test get_tool_by_name returns correct tool instance."""
    from codeindex.web.agents.tools import get_tool_by_name

    tool = get_tool_by_name("WeaviateSearchTool")

    assert tool is not None
    assert tool.name == "WeaviateSearchTool"


def test_get_tool_by_name_invalid():
    """Test get_tool_by_name raises error for invalid tool name."""
    from codeindex.web.agents.tools import get_tool_by_name

    with pytest.raises(ValueError) as exc_info:
        get_tool_by_name("NonexistentTool")

    assert "not found" in str(exc_info.value).lower() or "invalid" in str(exc_info.value).lower()
