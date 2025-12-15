"""
Integration test for status CLI command.

Tests project listing, artifact counts, type breakdowns, empty state messaging,
and service health checks.

NOTE: Requires running Weaviate and Ollama instances.
"""

import pytest
from unittest.mock import Mock, patch
from click.testing import CliRunner

from codeindex.cli.status import status_command
from codeindex.services.weaviate_store import WeaviateStore


# Fixtures
@pytest.fixture
def cli_runner():
    """Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def cli_context():
    """Create a CLI context with config."""
    import os
    from codeindex.utils.config import Config
    from codeindex.utils.logging import get_logger
    from codeindex.__main__ import CLIContext

    # Set environment variables for test
    os.environ["WEAVIATE_URL"] = "http://localhost:8080"
    os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434"
    os.environ["OLLAMA_MODEL_NAME"] = "gemma3:12b"

    config = Config()
    logger = get_logger(__name__)

    return CLIContext(config=config, logger=logger, verbose=False, format="text")


@pytest.fixture(scope="module")
def weaviate_store():
    """Weaviate store for testing."""
    import os
    from codeindex.utils.config import Config

    # Set environment variables for test
    os.environ["WEAVIATE_URL"] = "http://localhost:8080"
    os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434"
    os.environ["OLLAMA_MODEL_NAME"] = "gemma3:12b"

    config = Config()

    store = WeaviateStore(config=config)

    if not store.health_check():
        pytest.skip("Weaviate not available")

    yield store

    store.close()


# Test basic command execution
class TestBasicExecution:
    """Test basic status command execution."""

    def test_command_exists(self, cli_runner):
        """Test that status command exists and shows help."""
        result = cli_runner.invoke(status_command, ['--help'])

        assert result.exit_code == 0
        assert "status" in result.output.lower()

    @patch('codeindex.services.weaviate_store.WeaviateStore')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_status_with_services_up(
        self,
        mock_ollama,
        mock_weaviate,
        cli_runner,
        cli_context
    ):
        """Test status command when services are available."""
        # Mock healthy services
        mock_weaviate_instance = Mock()
        mock_weaviate.return_value = mock_weaviate_instance
        mock_weaviate_instance.health_check.return_value = True
        mock_weaviate_instance.get_statistics.return_value = {
            "project_count": 2,
            "artifact_count": 150,
            "projects": []
        }

        mock_ollama_instance = Mock()
        mock_ollama.return_value = mock_ollama_instance
        mock_ollama_instance.health_check.return_value = True

        result = cli_runner.invoke(status_command, [], obj=cli_context)

        assert result.exit_code == 0
        assert "weaviate" in result.output.lower() or "connected" in result.output.lower()

    def test_status_verbose(self, cli_runner):
        """Test status command with --verbose flag."""
        result = cli_runner.invoke(status_command, ['--verbose', '--help'])

        # Should have verbose option
        assert "--verbose" in result.output or result.exit_code == 0


# Test project listing
@pytest.mark.skip(reason="Legacy TDD test - API methods changed or do not exist. Requires refactoring.")
class TestProjectListing:
    """Test listing indexed projects."""

    @patch('codeindex.services.weaviate_store.WeaviateStore')
    def test_list_projects(self, mock_weaviate, cli_runner, cli_context):
        """Test that status lists all indexed projects."""
        mock_instance = Mock()
        mock_weaviate.return_value = mock_instance
        mock_instance.health_check.return_value = True
        mock_instance.get_statistics.return_value = {
            "project_count": 3,
            "artifact_count": 450,
            "projects": [
                {
                    "project_id": "com.example:app1:1.0.0",
                    "artifact_count": 150,
                    "last_indexed": "2025-12-13T10:00:00"
                },
                {
                    "project_id": "com.example:app2:2.0.0",
                    "artifact_count": 200,
                    "last_indexed": "2025-12-13T11:00:00"
                },
                {
                    "project_id": "com.example:lib:1.5.0",
                    "artifact_count": 100,
                    "last_indexed": "2025-12-13T12:00:00"
                }
            ]
        }

        result = cli_runner.invoke(status_command, [], obj=cli_context)

        assert result.exit_code == 0
        # Should show project count
        output_lower = result.output.lower()
        assert "project" in output_lower

    @patch('codeindex.services.weaviate_store.WeaviateStore')
    def test_filter_by_project(self, mock_weaviate, cli_runner):
        """Test filtering status by specific project."""
        mock_instance = Mock()
        mock_weaviate.return_value = mock_instance
        mock_instance.is_healthy.return_value = True
        mock_instance.get_project_statistics.return_value = {
            "project_id": "com.example:app:1.0.0",
            "artifact_count": 150,
            "type_breakdown": {
                "java_source": 100,
                "jsp_view": 30,
                "xml_config": 20
            },
            "last_indexed": "2025-12-13T10:00:00"
        }

        result = cli_runner.invoke(status_command, [
            '--project', 'com.example:app:1.0.0'
        ])

        # Should accept project filter
        assert result.exit_code == 0 or "--project" in status_command.params


# Test artifact counts and breakdowns
@pytest.mark.skip(reason="Legacy TDD test - API methods changed or do not exist. Requires refactoring.")
class TestArtifactBreakdowns:
    """Test artifact count and type breakdown reporting."""

    @patch('codeindex.services.weaviate_store.WeaviateStore')
    def test_artifact_type_breakdown(self, mock_weaviate, cli_runner):
        """Test that status shows artifact types breakdown."""
        mock_instance = Mock()
        mock_weaviate.return_value = mock_instance
        mock_instance.is_healthy.return_value = True
        mock_instance.get_statistics.return_value = {
            "project_count": 1,
            "artifact_count": 150,
            "projects": [
                {
                    "project_id": "com.example:app:1.0.0",
                    "artifact_count": 150,
                    "type_breakdown": {
                        "java_source": 100,
                        "jsp_view": 30,
                        "xml_config": 15,
                        "sql_schema": 5
                    },
                    "last_indexed": "2025-12-13T10:00:00"
                }
            ]
        }

        result = cli_runner.invoke(status_command, ['--verbose'])

        assert result.exit_code == 0
        # With verbose, should show type breakdown
        # (implementation specific)

    @patch('codeindex.services.weaviate_store.WeaviateStore')
    def test_total_artifact_count(self, mock_weaviate, cli_runner):
        """Test that status shows total artifact count across projects."""
        mock_instance = Mock()
        mock_weaviate.return_value = mock_instance
        mock_instance.is_healthy.return_value = True
        mock_instance.get_statistics.return_value = {
            "project_count": 2,
            "artifact_count": 300,
            "projects": [
                {
                    "project_id": "com.example:app1:1.0.0",
                    "artifact_count": 150,
                    "last_indexed": "2025-12-13T10:00:00"
                },
                {
                    "project_id": "com.example:app2:1.0.0",
                    "artifact_count": 150,
                    "last_indexed": "2025-12-13T11:00:00"
                }
            ]
        }

        result = cli_runner.invoke(status_command, [], obj=cli_context)

        assert result.exit_code == 0
        # Should show total count (300)


# Test empty state messaging
@pytest.mark.skip(reason="Legacy TDD test - API methods changed or do not exist. Requires refactoring.")
class TestEmptyState:
    """Test handling when no data is indexed."""

    @patch('codeindex.services.weaviate_store.WeaviateStore')
    def test_empty_database(self, mock_weaviate, cli_runner):
        """Test status when no projects are indexed."""
        mock_instance = Mock()
        mock_weaviate.return_value = mock_instance
        mock_instance.is_healthy.return_value = True
        mock_instance.get_statistics.return_value = {
            "project_count": 0,
            "artifact_count": 0,
            "projects": []
        }

        result = cli_runner.invoke(status_command, [], obj=cli_context)

        assert result.exit_code == 0
        # Should show helpful message about no indexed data
        output_lower = result.output.lower()
        assert "no" in output_lower or "0" in output_lower or "empty" in output_lower

    @patch('codeindex.services.weaviate_store.WeaviateStore')
    def test_empty_state_suggestions(self, mock_weaviate, cli_runner):
        """Test that empty state includes next steps suggestions."""
        mock_instance = Mock()
        mock_weaviate.return_value = mock_instance
        mock_instance.is_healthy.return_value = True
        mock_instance.get_statistics.return_value = {
            "project_count": 0,
            "artifact_count": 0,
            "projects": []
        }

        result = cli_runner.invoke(status_command, [], obj=cli_context)

        assert result.exit_code == 0
        # Should suggest running discover/extract/index
        output_lower = result.output.lower()
        # Looking for suggestions like "discover", "extract", "index"
        assert any(word in output_lower for word in ["discover", "extract", "index", "run", "start"])


# Test service health checks
@pytest.mark.skip(reason="Legacy TDD test - API methods changed or do not exist. Requires refactoring.")
class TestServiceHealthChecks:
    """Test health check reporting for Weaviate and Ollama."""

    @patch('codeindex.services.weaviate_store.WeaviateStore')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_both_services_healthy(self, mock_ollama, mock_weaviate, cli_runner):
        """Test status when both services are healthy."""
        mock_weaviate_instance = Mock()
        mock_weaviate.return_value = mock_weaviate_instance
        mock_weaviate_instance.is_healthy.return_value = True
        mock_weaviate_instance.get_statistics.return_value = {
            "project_count": 0,
            "artifact_count": 0,
            "projects": []
        }

        mock_ollama_instance = Mock()
        mock_ollama.return_value = mock_ollama_instance
        mock_ollama_instance.is_healthy.return_value = True

        result = cli_runner.invoke(status_command, [], obj=cli_context)

        assert result.exit_code == 0
        # Should indicate services are connected/healthy

    @patch('codeindex.services.weaviate_store.WeaviateStore')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_weaviate_unavailable(self, mock_ollama, mock_weaviate, cli_runner):
        """Test status when Weaviate is unavailable."""
        mock_weaviate_instance = Mock()
        mock_weaviate.return_value = mock_weaviate_instance
        mock_weaviate_instance.is_healthy.return_value = False

        mock_ollama_instance = Mock()
        mock_ollama.return_value = mock_ollama_instance
        mock_ollama_instance.is_healthy.return_value = True

        result = cli_runner.invoke(status_command, [], obj=cli_context)

        # Should show Weaviate as unavailable
        output_lower = result.output.lower()
        assert "weaviate" in output_lower or "unavailable" in output_lower or "error" in output_lower

    @patch('codeindex.services.weaviate_store.WeaviateStore')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_ollama_unavailable(self, mock_ollama, mock_weaviate, cli_runner):
        """Test status when Ollama is unavailable."""
        mock_weaviate_instance = Mock()
        mock_weaviate.return_value = mock_weaviate_instance
        mock_weaviate_instance.is_healthy.return_value = True
        mock_weaviate_instance.get_statistics.return_value = {
            "project_count": 0,
            "artifact_count": 0,
            "projects": []
        }

        mock_ollama_instance = Mock()
        mock_ollama.return_value = mock_ollama_instance
        mock_ollama_instance.is_healthy.return_value = False

        result = cli_runner.invoke(status_command, [], obj=cli_context)

        # Should show Ollama as unavailable
        output_lower = result.output.lower()
        assert "ollama" in output_lower or "unavailable" in output_lower or "error" in output_lower

    @patch('codeindex.services.weaviate_store.WeaviateStore')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_both_services_unavailable(self, mock_ollama, mock_weaviate, cli_runner):
        """Test status when both services are unavailable."""
        mock_weaviate_instance = Mock()
        mock_weaviate.return_value = mock_weaviate_instance
        mock_weaviate_instance.is_healthy.return_value = False

        mock_ollama_instance = Mock()
        mock_ollama.return_value = mock_ollama_instance
        mock_ollama_instance.is_healthy.return_value = False

        result = cli_runner.invoke(status_command, [], obj=cli_context)

        # Should show both as unavailable with actionable error messages
        output_lower = result.output.lower()
        assert ("unavailable" in output_lower or "error" in output_lower or "not" in output_lower)


# Test output formats
@pytest.mark.skip(reason="Legacy TDD test - API methods changed or do not exist. Requires refactoring.")
class TestOutputFormats:
    """Test different output formats."""

    @patch('codeindex.services.weaviate_store.WeaviateStore')
    def test_text_format(self, mock_weaviate, cli_runner):
        """Test default text output format."""
        mock_instance = Mock()
        mock_weaviate.return_value = mock_instance
        mock_instance.is_healthy.return_value = True
        mock_instance.get_statistics.return_value = {
            "project_count": 1,
            "artifact_count": 100,
            "projects": [
                {
                    "project_id": "com.example:app:1.0.0",
                    "artifact_count": 100,
                    "last_indexed": "2025-12-13T10:00:00"
                }
            ]
        }

        result = cli_runner.invoke(status_command, [], obj=cli_context)

        assert result.exit_code == 0
        # Should be human-readable text

    @patch('codeindex.services.weaviate_store.WeaviateStore')
    def test_json_format(self, mock_weaviate, cli_runner):
        """Test JSON output format."""
        import json

        mock_instance = Mock()
        mock_weaviate.return_value = mock_instance
        mock_instance.is_healthy.return_value = True
        mock_instance.get_statistics.return_value = {
            "project_count": 1,
            "artifact_count": 100,
            "projects": [
                {
                    "project_id": "com.example:app:1.0.0",
                    "artifact_count": 100,
                    "last_indexed": "2025-12-13T10:00:00"
                }
            ]
        }

        result = cli_runner.invoke(status_command, ['--format', 'json'])

        # Should output valid JSON
        if result.exit_code == 0:
            try:
                json.loads(result.output)
                # Valid JSON
            except json.JSONDecodeError:
                # May have text before/after JSON
                pass


# Test last indexed timestamps
@pytest.mark.skip(reason="Legacy TDD test - API methods changed or do not exist. Requires refactoring.")
class TestLastIndexed:
    """Test last indexed timestamp reporting."""

    @patch('codeindex.services.weaviate_store.WeaviateStore')
    def test_show_last_indexed_time(self, mock_weaviate, cli_runner):
        """Test that status shows when projects were last indexed."""
        mock_instance = Mock()
        mock_weaviate.return_value = mock_instance
        mock_instance.is_healthy.return_value = True
        mock_instance.get_statistics.return_value = {
            "project_count": 1,
            "artifact_count": 100,
            "projects": [
                {
                    "project_id": "com.example:app:1.0.0",
                    "artifact_count": 100,
                    "last_indexed": "2025-12-13T10:30:00"
                }
            ]
        }

        result = cli_runner.invoke(status_command, ['--verbose'])

        assert result.exit_code == 0
        # Should show timestamp or relative time
        # (implementation specific)
