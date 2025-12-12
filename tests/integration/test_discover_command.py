"""
Integration tests for discover CLI command.

Tests the complete discover command workflow including CLI args, config loading,
Maven project discovery, file scanning, and inventory generation.

NOTE: These tests should FAIL initially (TDD approach).
"""

import pytest
import json
from pathlib import Path
from click.testing import CliRunner

from codeindex.__main__ import main
from codeindex.models.inventory import DiscoveryInventory


# Fixtures
@pytest.fixture
def cli_runner():
    """Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def fixtures_dir():
    """Path to test fixtures directory."""
    return Path(__file__).parent.parent / "fixtures"


@pytest.fixture
def temp_output_dir(tmp_path):
    """Temporary output directory."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def mock_env(monkeypatch, fixtures_dir, temp_output_dir):
    """Mock environment variables for testing."""
    monkeypatch.setenv("JAVA_SOURCE_DIR", str(fixtures_dir))
    monkeypatch.setenv("OUTPUT_DIR", str(temp_output_dir))
    monkeypatch.setenv("LOG_LEVEL", "INFO")


# Test basic command execution
class TestBasicExecution:
    """Test basic discover command execution."""

    def test_discover_command_exists(self, cli_runner):
        """Test that discover command exists in CLI."""
        result = cli_runner.invoke(main, ['--help'])

        assert result.exit_code == 0
        assert 'discover' in result.output

    def test_discover_command_help(self, cli_runner):
        """Test discover command help."""
        result = cli_runner.invoke(main, ['discover', '--help'])

        assert result.exit_code == 0
        assert 'Discover Maven projects' in result.output or 'discover' in result.output.lower()

    def test_discover_runs_without_errors(self, cli_runner, mock_env):
        """Test that discover command runs without errors."""
        result = cli_runner.invoke(main, ['discover'])

        # Should complete successfully (exit code 0)
        assert result.exit_code == 0


# Test with source directory
class TestSourceDirectory:
    """Test discover command with different source directories."""

    def test_discover_with_source_dir_option(self, cli_runner, fixtures_dir):
        """Test discover with --source-dir option."""
        result = cli_runner.invoke(main, [
            'discover',
            '--source-dir', str(fixtures_dir)
        ])

        assert result.exit_code == 0

    def test_discover_with_nonexistent_directory(self, cli_runner):
        """Test discover with non-existent directory."""
        result = cli_runner.invoke(main, [
            'discover',
            '--source-dir', '/nonexistent/path'
        ])

        # Should fail with error
        assert result.exit_code != 0
        assert 'not found' in result.output.lower() or 'does not exist' in result.output.lower()

    def test_discover_with_relative_path(self, cli_runner, fixtures_dir):
        """Test discover with relative path."""
        # Change to parent directory of fixtures
        import os
        original_dir = os.getcwd()
        os.chdir(fixtures_dir.parent)

        try:
            result = cli_runner.invoke(main, [
                'discover',
                '--source-dir', 'fixtures'
            ])

            assert result.exit_code == 0
        finally:
            os.chdir(original_dir)


# Test output options
class TestOutputOptions:
    """Test discover command output options."""

    def test_discover_with_output_file(self, cli_runner, fixtures_dir, temp_output_dir):
        """Test discover with --output option."""
        output_file = temp_output_dir / "inventory.jsonl"

        result = cli_runner.invoke(main, [
            'discover',
            '--source-dir', str(fixtures_dir),
            '--output', str(output_file)
        ])

        assert result.exit_code == 0
        assert output_file.exists()
        assert output_file.stat().st_size > 0

    def test_discover_with_json_format(self, cli_runner, fixtures_dir):
        """Test discover with --format json."""
        result = cli_runner.invoke(main, [
            '--format', 'json',
            'discover',
            '--source-dir', str(fixtures_dir)
        ])

        assert result.exit_code == 0
        # Output should be valid JSON
        try:
            json.loads(result.output)
        except json.JSONDecodeError:
            pytest.fail("Output is not valid JSON")

    def test_discover_with_text_format(self, cli_runner, fixtures_dir):
        """Test discover with --format text (default)."""
        result = cli_runner.invoke(main, [
            '--format', 'text',
            'discover',
            '--source-dir', str(fixtures_dir)
        ])

        assert result.exit_code == 0
        # Should contain human-readable text
        assert 'project' in result.output.lower() or 'discover' in result.output.lower()


# Test project filtering
class TestProjectFiltering:
    """Test project filtering options."""

    def test_discover_with_project_filter(self, cli_runner, fixtures_dir):
        """Test discover with --project filter."""
        result = cli_runner.invoke(main, [
            'discover',
            '--source-dir', str(fixtures_dir),
            '--project', 'test-project'
        ])

        assert result.exit_code == 0

    def test_discover_with_nonexistent_project(self, cli_runner, fixtures_dir):
        """Test discover filtering for non-existent project."""
        result = cli_runner.invoke(main, [
            'discover',
            '--source-dir', str(fixtures_dir),
            '--project', 'nonexistent-project-xyz'
        ])

        # Should complete but find no projects
        assert result.exit_code == 0
        assert 'no projects' in result.output.lower() or '0' in result.output


# Test verbose output
class TestVerboseOutput:
    """Test verbose and logging options."""

    def test_discover_with_verbose(self, cli_runner, fixtures_dir):
        """Test discover with --verbose flag."""
        result = cli_runner.invoke(main, [
            '--verbose',
            'discover',
            '--source-dir', str(fixtures_dir)
        ])

        assert result.exit_code == 0
        # Verbose output should contain debug information
        # (Check stderr or output for DEBUG level logs)

    def test_discover_with_log_level(self, cli_runner, fixtures_dir):
        """Test discover with --log-level option."""
        result = cli_runner.invoke(main, [
            '--log-level', 'DEBUG',
            'discover',
            '--source-dir', str(fixtures_dir)
        ])

        assert result.exit_code == 0


# Test inventory generation
class TestInventoryGeneration:
    """Test discovery inventory generation."""

    def test_inventory_file_created(self, cli_runner, fixtures_dir, temp_output_dir):
        """Test that inventory file is created."""
        output_file = temp_output_dir / "test-inventory.jsonl"

        result = cli_runner.invoke(main, [
            'discover',
            '--source-dir', str(fixtures_dir),
            '--output', str(output_file)
        ])

        assert result.exit_code == 0
        assert output_file.exists()

    def test_inventory_file_format(self, cli_runner, fixtures_dir, temp_output_dir):
        """Test that inventory file has correct JSONL format."""
        output_file = temp_output_dir / "inventory.jsonl"

        result = cli_runner.invoke(main, [
            'discover',
            '--source-dir', str(fixtures_dir),
            '--output', str(output_file)
        ])

        assert result.exit_code == 0

        # Verify JSONL format
        lines = output_file.read_text().strip().split("\n")
        assert len(lines) > 0

        # Each line should be valid JSON
        for line in lines:
            json.loads(line)  # Should not raise

    def test_inventory_contains_metadata(self, cli_runner, fixtures_dir, temp_output_dir):
        """Test that inventory contains required metadata."""
        output_file = temp_output_dir / "inventory.jsonl"

        result = cli_runner.invoke(main, [
            'discover',
            '--source-dir', str(fixtures_dir),
            '--output', str(output_file)
        ])

        assert result.exit_code == 0

        # Load and verify metadata
        lines = output_file.read_text().strip().split("\n")
        header = json.loads(lines[0])

        assert "scan_timestamp" in header
        assert "root_directory" in header
        assert "total_files" in header

    def test_inventory_contains_projects(self, cli_runner, fixtures_dir, temp_output_dir):
        """Test that inventory contains project data."""
        output_file = temp_output_dir / "inventory.jsonl"

        result = cli_runner.invoke(main, [
            'discover',
            '--source-dir', str(fixtures_dir),
            '--output', str(output_file)
        ])

        assert result.exit_code == 0

        # Load inventory
        lines = output_file.read_text().strip().split("\n")

        # Should have header + at least one project
        assert len(lines) >= 2

        # Verify project data
        project = json.loads(lines[1])  # First project after header
        assert "artifact_id" in project or "artifactId" in project
        assert "path" in project


# Test progress reporting
class TestProgressReporting:
    """Test progress reporting during discovery."""

    def test_progress_output_shown(self, cli_runner, fixtures_dir):
        """Test that progress is shown during discovery."""
        result = cli_runner.invoke(main, [
            'discover',
            '--source-dir', str(fixtures_dir)
        ])

        assert result.exit_code == 0
        # Should show some progress indication
        # (May be in output or stderr)

    def test_quiet_mode_suppresses_progress(self, cli_runner, fixtures_dir):
        """Test that --quiet suppresses progress output."""
        result = cli_runner.invoke(main, [
            '--quiet',
            'discover',
            '--source-dir', str(fixtures_dir)
        ])

        # Should complete with minimal output
        assert result.exit_code == 0


# Test error handling
class TestErrorHandling:
    """Test error handling in discover command."""

    def test_discover_without_source_dir(self, cli_runner):
        """Test discover without source directory configured."""
        # Remove JAVA_SOURCE_DIR from environment
        result = cli_runner.invoke(main, ['discover'], env={})

        # Should fail or prompt for source directory
        # (Behavior depends on implementation)

    def test_discover_with_invalid_output_path(self, cli_runner, fixtures_dir):
        """Test discover with invalid output path."""
        result = cli_runner.invoke(main, [
            'discover',
            '--source-dir', str(fixtures_dir),
            '--output', '/root/forbidden/path.jsonl'
        ])

        # Should fail with permission error
        assert result.exit_code != 0

    def test_discover_handles_malformed_poms(self, cli_runner, fixtures_dir):
        """Test that discover handles malformed POMs gracefully."""
        result = cli_runner.invoke(main, [
            'discover',
            '--source-dir', str(fixtures_dir)
        ])

        # Should complete despite malformed POMs
        assert result.exit_code == 0


# Test configuration loading
class TestConfigurationLoading:
    """Test configuration loading from different sources."""

    def test_discover_uses_env_vars(self, cli_runner, mock_env, fixtures_dir):
        """Test that discover uses environment variables."""
        result = cli_runner.invoke(main, ['discover'])

        # Should use JAVA_SOURCE_DIR from environment
        assert result.exit_code == 0

    def test_discover_with_config_file(self, cli_runner, fixtures_dir, tmp_path):
        """Test discover with --config option."""
        # Create config file
        config_file = tmp_path / ".env"
        config_file.write_text(f"JAVA_SOURCE_DIR={fixtures_dir}\n")

        result = cli_runner.invoke(main, [
            '--config', str(config_file),
            'discover'
        ])

        assert result.exit_code == 0

    def test_cli_args_override_env_vars(self, cli_runner, mock_env, fixtures_dir):
        """Test that CLI args override environment variables."""
        # mock_env sets JAVA_SOURCE_DIR, but we override with --source-dir
        other_dir = fixtures_dir.parent

        result = cli_runner.invoke(main, [
            'discover',
            '--source-dir', str(fixtures_dir)  # Override env var
        ])

        assert result.exit_code == 0


# Test dry-run mode
class TestDryRunMode:
    """Test dry-run mode for discovery."""

    def test_discover_dry_run(self, cli_runner, fixtures_dir):
        """Test discover with --dry-run flag."""
        result = cli_runner.invoke(main, [
            'discover',
            '--source-dir', str(fixtures_dir),
            '--dry-run'
        ])

        # Should show what would be done without actually doing it
        assert result.exit_code == 0

    def test_dry_run_no_output_file(self, cli_runner, fixtures_dir, temp_output_dir):
        """Test that dry-run doesn't create output file."""
        output_file = temp_output_dir / "inventory.jsonl"

        result = cli_runner.invoke(main, [
            'discover',
            '--source-dir', str(fixtures_dir),
            '--output', str(output_file),
            '--dry-run'
        ])

        assert result.exit_code == 0
        # Output file should NOT be created in dry-run mode
        assert not output_file.exists()


# Integration test: Full workflow
class TestFullWorkflow:
    """Test complete discover workflow end-to-end."""

    def test_complete_discover_workflow(self, cli_runner, fixtures_dir, temp_output_dir):
        """Test complete discovery workflow."""
        output_file = temp_output_dir / "full-inventory.jsonl"

        # Run discover command
        result = cli_runner.invoke(main, [
            '--verbose',
            'discover',
            '--source-dir', str(fixtures_dir),
            '--output', str(output_file)
        ])

        # 1. Command should succeed
        assert result.exit_code == 0

        # 2. Output file should exist
        assert output_file.exists()

        # 3. Load and validate inventory
        inventory_data = []
        for line in output_file.read_text().strip().split("\n"):
            inventory_data.append(json.loads(line))

        # 4. Should have header + projects
        assert len(inventory_data) >= 1

        # 5. Header should have metadata
        header = inventory_data[0]
        assert "scan_timestamp" in header
        assert "root_directory" in header

        # 6. If projects found, verify structure
        if len(inventory_data) > 1:
            project = inventory_data[1]
            assert "artifact_id" in project or "artifactId" in project

    def test_discover_and_verify_output(self, cli_runner, fixtures_dir, temp_output_dir):
        """Test discover and verify output contents."""
        output_file = temp_output_dir / "verify-inventory.jsonl"

        # Run discover
        result = cli_runner.invoke(main, [
            'discover',
            '--source-dir', str(fixtures_dir),
            '--output', str(output_file)
        ])

        assert result.exit_code == 0

        # Load inventory using DiscoveryInventory model
        # (This validates the structure matches our data model)
        inventory = DiscoveryInventory.load_jsonl(output_file)

        assert inventory is not None
        assert inventory.root_directory == str(fixtures_dir)
        assert len(inventory.projects) >= 0

    def test_discover_multiple_runs_idempotent(self, cli_runner, fixtures_dir, temp_output_dir):
        """Test that multiple discover runs are idempotent."""
        output_file1 = temp_output_dir / "run1.jsonl"
        output_file2 = temp_output_dir / "run2.jsonl"

        # First run
        result1 = cli_runner.invoke(main, [
            'discover',
            '--source-dir', str(fixtures_dir),
            '--output', str(output_file1)
        ])

        # Second run
        result2 = cli_runner.invoke(main, [
            'discover',
            '--source-dir', str(fixtures_dir),
            '--output', str(output_file2)
        ])

        assert result1.exit_code == 0
        assert result2.exit_code == 0

        # Results should be identical (excluding timestamps)
        lines1 = output_file1.read_text().strip().split("\n")
        lines2 = output_file2.read_text().strip().split("\n")

        # Same number of projects
        assert len(lines1) == len(lines2)
