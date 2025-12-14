"""
Unit tests for discovery service.

Tests Maven project discovery, file scanning, and inventory generation.

NOTE: These tests should FAIL initially (TDD approach).
"""

import pytest
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

from codeindex.services.discovery import (
    DiscoveryService,
    discover_projects,
    scan_directory,
    generate_project_id,
    create_project_from_pom,
)
from codeindex.models.project import Project
from codeindex.models.inventory import DiscoveryInventory
from codeindex.models import ArtifactType


# Fixtures
@pytest.fixture
def discovery_service():
    """DiscoveryService instance."""
    return DiscoveryService()


@pytest.fixture
def fixtures_dir():
    """Path to test fixtures directory."""
    return Path(__file__).parent.parent / "fixtures"


@pytest.fixture
def sample_pom_path(fixtures_dir):
    """Path to valid sample POM."""
    return fixtures_dir / "sample_pom.xml"


@pytest.fixture
def mock_config():
    """Mock configuration."""
    config = Mock()
    config.java_source_dir = Path("/mock/source")
    config.discovery_follow_symlinks = False
    config.discovery_max_depth = 10
    return config


# Test project discovery
class TestProjectDiscovery:
    """Test Maven project discovery."""

    def test_discover_projects_finds_pom(self, discovery_service, fixtures_dir):
        """Test that discover finds pom.xml files."""
        projects = list(discovery_service.discover_projects(fixtures_dir))

        assert len(projects) > 0
        # Should find at least the test-project
        assert any("test" in p.name.lower() for p in projects)

    def test_discover_projects_creates_project_objects(self, discovery_service, fixtures_dir):
        """Test that discovered projects are Project objects."""
        projects = list(discovery_service.discover_projects(fixtures_dir))

        for project in projects:
            assert isinstance(project, Project)
            assert project.artifact_id is not None
            assert project.path != ""

    def test_discover_projects_excludes_target_dirs(self, discovery_service, tmp_path):
        """Test that target/ directories are excluded."""
        # Create test structure
        (tmp_path / "pom.xml").write_text("""<?xml version="1.0"?>
        <project><modelVersion>4.0.0</modelVersion>
        <groupId>com.test</groupId><artifactId>main</artifactId><version>1.0</version>
        </project>""")

        target_dir = tmp_path / "target"
        target_dir.mkdir()
        (target_dir / "pom.xml").write_text("""<?xml version="1.0"?>
        <project><modelVersion>4.0.0</modelVersion>
        <groupId>com.test</groupId><artifactId>generated</artifactId><version>1.0</version>
        </project>""")

        projects = list(discovery_service.discover_projects(tmp_path))

        # Should only find main pom.xml, not the one in target/
        assert len(projects) == 1
        assert projects[0].artifact_id == "main"

    def test_discover_projects_handles_nested_modules(self, discovery_service, tmp_path):
        """Test discovery of nested module structure."""
        # Parent POM
        (tmp_path / "pom.xml").write_text("""<?xml version="1.0"?>
        <project><modelVersion>4.0.0</modelVersion>
        <groupId>com.test</groupId><artifactId>parent</artifactId><version>1.0</version>
        <modules><module>module-a</module></modules>
        </project>""")

        # Child module
        module_dir = tmp_path / "module-a"
        module_dir.mkdir()
        (module_dir / "pom.xml").write_text("""<?xml version="1.0"?>
        <project><modelVersion>4.0.0</modelVersion>
        <groupId>com.test</groupId><artifactId>module-a</artifactId><version>1.0</version>
        </project>""")

        projects = list(discovery_service.discover_projects(tmp_path))

        # Should find both parent and child
        assert len(projects) == 2
        artifact_ids = {p.artifact_id for p in projects}
        assert "parent" in artifact_ids
        assert "module-a" in artifact_ids


# Test file scanning
class TestFileScanning:
    """Test file scanning within projects."""

    def test_scan_directory_finds_java_files(self, discovery_service, fixtures_dir):
        """Test scanning finds Java files."""
        java_dir = fixtures_dir / "sample_java"
        if not java_dir.exists():
            pytest.skip("sample_java directory not found")

        files = list(discovery_service.scan_files(java_dir))

        java_files = [f for f in files if f.suffix == ".java"]
        assert len(java_files) > 0

    def test_scan_directory_classifies_files(self, discovery_service, fixtures_dir):
        """Test that scanned files are classified."""
        java_dir = fixtures_dir / "sample_java"
        if not java_dir.exists():
            pytest.skip("sample_java directory not found")

        files_with_types = list(discovery_service.scan_and_classify(java_dir))

        for file_path, artifact_type in files_with_types:
            assert isinstance(file_path, Path)
            assert isinstance(artifact_type, ArtifactType)

    def test_scan_directory_excludes_hidden_files(self, discovery_service, tmp_path):
        """Test that hidden files are excluded."""
        (tmp_path / "visible.java").touch()
        (tmp_path / ".hidden.java").touch()

        files = list(discovery_service.scan_files(tmp_path))
        file_names = [f.name for f in files]

        assert "visible.java" in file_names
        assert ".hidden.java" not in file_names

    def test_scan_directory_respects_max_depth(self, discovery_service, tmp_path):
        """Test that max depth is respected."""
        # Create nested structure
        deep = tmp_path / "a" / "b" / "c" / "d" / "e"
        deep.mkdir(parents=True)
        (deep / "deep.java").touch()

        # Scan with max depth 3
        files = list(discovery_service.scan_files(tmp_path, max_depth=3))

        # Should not find files deeper than 3 levels
        assert not any("deep.java" in str(f) for f in files)


# Test project ID generation
class TestProjectIDGeneration:
    """Test project ID generation."""

    def test_generate_project_id_with_coordinates(self):
        """Test ID generation with full Maven coordinates."""
        project_id = generate_project_id(
            group_id="com.example",
            artifact_id="my-app",
            version="1.0.0"
        )

        assert project_id == "com.example:my-app:1.0.0"

    def test_generate_project_id_without_group(self):
        """Test ID generation without groupId."""
        project_id = generate_project_id(
            group_id=None,
            artifact_id="my-app",
            version="1.0.0"
        )

        assert "my-app" in project_id
        assert "1.0.0" in project_id

    def test_generate_project_id_from_path(self):
        """Test fallback ID generation from path."""
        project_id = generate_project_id(
            group_id=None,
            artifact_id=None,
            version=None,
            path=Path("/projects/my-app")
        )

        assert project_id is not None
        assert len(project_id) > 0
        # Should use path hash or name

    def test_generate_project_id_deterministic(self):
        """Test that ID generation is deterministic."""
        id1 = generate_project_id("com.example", "app", "1.0.0")
        id2 = generate_project_id("com.example", "app", "1.0.0")

        assert id1 == id2


# Test project creation from POM
class TestCreateProjectFromPOM:
    """Test creating Project objects from POM files."""

    def test_create_project_from_valid_pom(self, sample_pom_path):
        """Test creating project from valid POM."""
        project = create_project_from_pom(sample_pom_path)

        assert isinstance(project, Project)
        assert project.group_id == "com.example"
        assert project.artifact_id == "test-project"
        assert project.version == "1.0.0-SNAPSHOT"
        assert project.packaging == "jar"

    def test_create_project_extracts_modules(self, sample_pom_path):
        """Test that modules are extracted."""
        project = create_project_from_pom(sample_pom_path)

        assert len(project.modules) == 2
        assert "test-module-a" in project.modules
        assert "test-module-b" in project.modules

    def test_create_project_extracts_dependencies(self, sample_pom_path):
        """Test that dependencies are extracted."""
        project = create_project_from_pom(sample_pom_path)

        assert len(project.dependencies) > 0
        # Check for Spring dependency
        assert any("spring" in dep.lower() for dep in project.dependencies)

    def test_create_project_extracts_source_roots(self, sample_pom_path):
        """Test that source roots are extracted."""
        project = create_project_from_pom(sample_pom_path)

        assert len(project.source_roots) > 0
        assert "src/main/java" in project.source_roots

    def test_create_project_sets_path(self, sample_pom_path):
        """Test that project path is set."""
        project = create_project_from_pom(sample_pom_path)

        assert project.path != ""
        assert sample_pom_path.parent.name in project.path


# Test inventory generation
class TestInventoryGeneration:
    """Test discovery inventory generation."""

    def test_generate_inventory(self, discovery_service, fixtures_dir):
        """Test generating discovery inventory."""
        inventory = discovery_service.generate_inventory(fixtures_dir)

        assert isinstance(inventory, DiscoveryInventory)
        assert inventory.root_directory == str(fixtures_dir)
        assert len(inventory.projects) > 0

    def test_inventory_contains_metadata(self, discovery_service, fixtures_dir):
        """Test that inventory contains metadata."""
        inventory = discovery_service.generate_inventory(fixtures_dir)

        assert inventory.scan_timestamp is not None
        assert isinstance(inventory.scan_timestamp, datetime)
        assert inventory.total_files >= 0
        assert inventory.scan_duration_seconds >= 0

    def test_inventory_contains_file_stats(self, discovery_service, fixtures_dir):
        """Test that inventory contains file type statistics."""
        inventory = discovery_service.generate_inventory(fixtures_dir)

        assert isinstance(inventory.files_by_type, dict)
        # Should have counts for different file types
        if inventory.total_files > 0:
            assert len(inventory.files_by_type) > 0

    def test_inventory_serialization(self, discovery_service, fixtures_dir, tmp_path):
        """Test inventory JSONL serialization."""
        inventory = discovery_service.generate_inventory(fixtures_dir)

        output_path = tmp_path / "inventory.jsonl"
        inventory.save_jsonl(output_path)

        assert output_path.exists()
        assert output_path.stat().st_size > 0

        # Verify it's valid JSONL
        lines = output_path.read_text().strip().split("\n")
        assert len(lines) > 0

        import json
        # First line should be header
        header = json.loads(lines[0])
        assert "scan_timestamp" in header
        assert "root_directory" in header


# Test DiscoveryService class
class TestDiscoveryService:
    """Test DiscoveryService class methods."""

    def test_service_initialization(self):
        """Test service initialization."""
        service = DiscoveryService()
        assert service is not None

    def test_service_with_config(self, mock_config):
        """Test service initialization with config."""
        service = DiscoveryService(config=mock_config)
        assert service.config == mock_config

    def test_discover_with_progress_callback(self, discovery_service, fixtures_dir):
        """Test discovery with progress callback."""
        progress_calls = []

        def progress_callback(current, total, message):
            progress_calls.append((current, total, message))

        projects = list(discovery_service.discover_projects(
            fixtures_dir,
            progress_callback=progress_callback
        ))

        # Should have called progress callback
        assert len(progress_calls) > 0

    def test_discover_handles_empty_directory(self, discovery_service, tmp_path):
        """Test discovery of empty directory."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        projects = list(discovery_service.discover_projects(empty_dir))

        assert len(projects) == 0


# Test error handling
class TestErrorHandling:
    """Test error handling in discovery."""

    def test_discover_nonexistent_directory(self, discovery_service):
        """Test discovery of non-existent directory."""
        with pytest.raises(FileNotFoundError):
            list(discovery_service.discover_projects(Path("/nonexistent")))

    def test_discover_file_not_directory(self, discovery_service, sample_pom_path):
        """Test discovery on a file (not directory)."""
        with pytest.raises((ValueError, NotADirectoryError)):
            list(discovery_service.discover_projects(sample_pom_path))

    def test_discover_continues_on_malformed_pom(self, discovery_service, fixtures_dir):
        """Test that discovery continues despite malformed POMs."""
        # Should find valid POMs even if some are malformed
        projects = list(discovery_service.discover_projects(fixtures_dir))

        # Should have found at least the valid sample_pom.xml
        assert len(projects) > 0

    def test_scan_handles_permission_errors(self, discovery_service, tmp_path, monkeypatch):
        """Test scanning handles permission errors gracefully."""
        # Create a file and simulate permission error
        test_file = tmp_path / "restricted.java"
        test_file.touch()

        def mock_iterdir():
            raise PermissionError("Access denied")

        monkeypatch.setattr(Path, "iterdir", mock_iterdir)

        # Should not crash, but may return empty list
        try:
            files = list(discovery_service.scan_files(tmp_path))
            assert isinstance(files, list)
        except PermissionError:
            # Also acceptable to propagate
            pass


# Test discover_projects standalone function
class TestDiscoverProjectsFunction:
    """Test discover_projects standalone function."""

    def test_discover_projects_function_exists(self):
        """Test that discover_projects function exists."""
        assert callable(discover_projects)

    def test_discover_projects_returns_generator(self, fixtures_dir):
        """Test that function returns generator."""
        result = discover_projects(fixtures_dir)

        # Should be generator or iterable
        projects = list(result)
        assert isinstance(projects, list)

    def test_discover_projects_with_filter(self, fixtures_dir):
        """Test discovery with project name filter."""
        # Filter to specific artifact
        projects = list(discover_projects(
            fixtures_dir,
            artifact_filter="test-project"
        ))

        for project in projects:
            assert "test-project" in project.artifact_id


# Test scan_directory standalone function
class TestScanDirectoryFunction:
    """Test scan_directory standalone function."""

    def test_scan_directory_function_exists(self):
        """Test that scan_directory function exists."""
        assert callable(scan_directory)

    def test_scan_directory_returns_paths(self, fixtures_dir):
        """Test that function returns file paths."""
        files = list(scan_directory(fixtures_dir))

        assert isinstance(files, list)
        for file_path in files:
            assert isinstance(file_path, Path)

    def test_scan_directory_with_pattern(self, fixtures_dir):
        """Test scanning with file pattern filter."""
        java_files = list(scan_directory(
            fixtures_dir,
            pattern="*.java"
        ))

        for file_path in java_files:
            assert file_path.suffix == ".java"


# Integration-like tests (still unit tests, but test multiple components)
class TestIntegration:
    """Test integration of discovery components."""

    def test_full_discovery_workflow(self, discovery_service, fixtures_dir, tmp_path):
        """Test complete discovery workflow."""
        # 1. Discover projects
        projects = list(discovery_service.discover_projects(fixtures_dir))
        assert len(projects) > 0

        # 2. Generate inventory
        inventory = discovery_service.generate_inventory(fixtures_dir)
        assert len(inventory.projects) == len(projects)

        # 3. Save inventory
        output_path = tmp_path / "test-inventory.jsonl"
        inventory.save_jsonl(output_path)
        assert output_path.exists()

        # 4. Verify contents
        import json
        lines = output_path.read_text().strip().split("\n")
        assert len(lines) >= len(projects)  # Header + projects

    def test_project_file_scanning_workflow(self, discovery_service, fixtures_dir):
        """Test workflow of discovering project and scanning its files."""
        # Discover projects
        projects = list(discovery_service.discover_projects(fixtures_dir))

        if len(projects) == 0:
            pytest.skip("No projects found")

        # For each project, scan files
        for project in projects:
            project_path = Path(project.path)
            if project_path.exists():
                files = list(discovery_service.scan_files(project_path))
                # Update file count
                project.file_count = len(files)

        # Verify at least one project has files
        total_files = sum(p.file_count for p in projects)
        assert total_files > 0
