"""Unit tests for ProjectConfiguration model (T067-T069)."""

import pytest
from pathlib import Path
from src.codeindex.models.project_configuration import ProjectConfiguration


class TestProjectConfigurationBasics:
    """Test basic ProjectConfiguration functionality (T067)."""

    def test_project_configuration_with_subdirectory(self, tmp_path):
        """
        Test ProjectConfiguration with project_subdirectory (T067).

        Verifies that project_subdirectory is properly stored and accessible.
        """
        # Arrange - Create test directory structure
        base_dir = tmp_path / "source"
        base_dir.mkdir()
        project_dir = base_dir / "myproject"
        project_dir.mkdir()

        # Act
        config = ProjectConfiguration(
            java_source_dir=base_dir,
            project_subdirectory="myproject"
        )

        # Assert
        assert config.project_subdirectory == "myproject"
        assert config.has_project_scope is True
        assert config.get_project_name() == "myproject"

    def test_project_configuration_without_subdirectory(self, tmp_path):
        """
        Test ProjectConfiguration without project_subdirectory (T067).

        Verifies that configuration works without project scoping.
        """
        # Arrange
        base_dir = tmp_path / "source"
        base_dir.mkdir()

        # Act
        config = ProjectConfiguration(
            java_source_dir=base_dir,
            project_subdirectory=None
        )

        # Assert
        assert config.project_subdirectory is None
        assert config.has_project_scope is False
        assert config.get_project_name() == "source"

    def test_project_configuration_dependency_depth(self, tmp_path):
        """Test that dependency_depth is properly set (T067)."""
        # Arrange
        base_dir = tmp_path / "source"
        base_dir.mkdir()

        # Act
        config = ProjectConfiguration(
            java_source_dir=base_dir,
            dependency_depth=2
        )

        # Assert
        assert config.dependency_depth == 2

    def test_project_configuration_default_values(self, tmp_path):
        """Test that ProjectConfiguration has proper defaults (T067)."""
        # Arrange
        base_dir = tmp_path / "source"
        base_dir.mkdir()

        # Act
        config = ProjectConfiguration(java_source_dir=base_dir)

        # Assert
        assert config.dependency_depth == 1
        assert config.resolve_transitive is True
        assert config.continue_on_error is True
        assert config.log_level == "INFO"
        assert config.output_dir == Path("./output")


class TestEffectiveBaseDirComputation:
    """Test effective_base_dir computation (T068)."""

    def test_effective_base_dir_without_project(self, tmp_path):
        """
        Test effective_base_dir equals java_source_dir without project (T068).

        When no project_subdirectory is specified, effective_base_dir should
        equal java_source_dir.
        """
        # Arrange
        base_dir = tmp_path / "source"
        base_dir.mkdir()

        # Act
        config = ProjectConfiguration(java_source_dir=base_dir)

        # Assert
        assert config.effective_base_dir == base_dir
        assert config.effective_base_dir.exists()
        assert config.effective_base_dir.is_dir()

    def test_effective_base_dir_with_project(self, tmp_path):
        """
        Test effective_base_dir with project_subdirectory (T068).

        When project_subdirectory is specified, effective_base_dir should
        be java_source_dir / project_subdirectory.
        """
        # Arrange
        base_dir = tmp_path / "source"
        base_dir.mkdir()
        project_dir = base_dir / "myproject"
        project_dir.mkdir()

        # Act
        config = ProjectConfiguration(
            java_source_dir=base_dir,
            project_subdirectory="myproject"
        )

        # Assert
        assert config.effective_base_dir == base_dir / "myproject"
        assert config.effective_base_dir.exists()
        assert config.effective_base_dir.is_dir()

    def test_effective_base_dir_with_nested_project(self, tmp_path):
        """
        Test effective_base_dir with nested project path (T068).

        Should support nested paths like "parent/child".
        """
        # Arrange
        base_dir = tmp_path / "source"
        base_dir.mkdir()
        parent_dir = base_dir / "parent"
        parent_dir.mkdir()
        child_dir = parent_dir / "child"
        child_dir.mkdir()

        # Act
        config = ProjectConfiguration(
            java_source_dir=base_dir,
            project_subdirectory="parent/child"
        )

        # Assert
        assert config.effective_base_dir == base_dir / "parent" / "child"
        assert config.effective_base_dir.exists()

    def test_effective_base_dir_computation_is_automatic(self, tmp_path):
        """
        Test that effective_base_dir is computed automatically (T068).

        Should be set in __post_init__ without manual intervention.
        """
        # Arrange
        base_dir = tmp_path / "source"
        base_dir.mkdir()
        project_dir = base_dir / "project"
        project_dir.mkdir()

        # Act - effective_base_dir should be computed automatically
        config = ProjectConfiguration(
            java_source_dir=base_dir,
            project_subdirectory="project"
        )

        # Assert - effective_base_dir should be set
        assert hasattr(config, 'effective_base_dir')
        assert config.effective_base_dir is not None


class TestProjectDirectoryValidation:
    """Test project directory validation (T069)."""

    def test_validation_fails_for_nonexistent_java_source_dir(self, tmp_path):
        """
        Test that nonexistent java_source_dir raises error (T069).

        Should raise ValueError with clear message.
        """
        # Arrange
        nonexistent_dir = tmp_path / "nonexistent"

        # Act & Assert
        with pytest.raises(ValueError, match="JAVA_SOURCE_DIR does not exist"):
            ProjectConfiguration(java_source_dir=nonexistent_dir)

    def test_validation_fails_for_java_source_dir_not_directory(self, tmp_path):
        """
        Test that java_source_dir must be a directory (T069).

        Should raise ValueError if java_source_dir is a file.
        """
        # Arrange
        file_path = tmp_path / "file.txt"
        file_path.write_text("not a directory")

        # Act & Assert
        with pytest.raises(ValueError, match="is not a directory"):
            ProjectConfiguration(java_source_dir=file_path)

    def test_validation_fails_for_nonexistent_project_directory(self, tmp_path):
        """
        Test that nonexistent project directory raises error (T069).

        When project_subdirectory is specified but doesn't exist,
        should raise ValueError with clear message including both paths.
        """
        # Arrange
        base_dir = tmp_path / "source"
        base_dir.mkdir()

        # Act & Assert
        with pytest.raises(ValueError, match="Project directory does not exist"):
            ProjectConfiguration(
                java_source_dir=base_dir,
                project_subdirectory="nonexistent"
            )

    def test_validation_fails_for_project_path_not_directory(self, tmp_path):
        """
        Test that project path must be a directory (T069).

        If project subdirectory exists but is a file, should raise error.
        """
        # Arrange
        base_dir = tmp_path / "source"
        base_dir.mkdir()
        file_path = base_dir / "file.txt"
        file_path.write_text("not a directory")

        # Act & Assert
        with pytest.raises(ValueError, match="is not a directory"):
            ProjectConfiguration(
                java_source_dir=base_dir,
                project_subdirectory="file.txt"
            )

    def test_validation_error_includes_helpful_context(self, tmp_path):
        """
        Test that validation errors include helpful context (T069, FR-024).

        Error messages should include both JAVA_SOURCE_DIR and
        project_subdirectory for debugging.
        """
        # Arrange
        base_dir = tmp_path / "source"
        base_dir.mkdir()

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            ProjectConfiguration(
                java_source_dir=base_dir,
                project_subdirectory="nonexistent"
            )

        error_message = str(exc_info.value)
        assert "JAVA_SOURCE_DIR" in error_message
        assert "project_subdirectory" in error_message
        assert str(base_dir) in error_message
        assert "nonexistent" in error_message

    def test_validation_fails_for_negative_dependency_depth(self, tmp_path):
        """
        Test that negative dependency_depth raises error (T069).

        dependency_depth must be >= 0.
        """
        # Arrange
        base_dir = tmp_path / "source"
        base_dir.mkdir()

        # Act & Assert
        with pytest.raises(ValueError, match="dependency_depth must be >= 0"):
            ProjectConfiguration(
                java_source_dir=base_dir,
                dependency_depth=-1
            )

    def test_validation_fails_for_invalid_log_level(self, tmp_path):
        """
        Test that invalid log_level raises error (T069).

        log_level must be one of DEBUG, INFO, WARNING, ERROR.
        """
        # Arrange
        base_dir = tmp_path / "source"
        base_dir.mkdir()

        # Act & Assert
        with pytest.raises(ValueError, match="Invalid log_level"):
            ProjectConfiguration(
                java_source_dir=base_dir,
                log_level="INVALID"
            )

    def test_validation_accepts_valid_log_levels(self, tmp_path):
        """
        Test that all valid log levels are accepted (T069).

        Should accept DEBUG, INFO, WARNING, ERROR.
        """
        # Arrange
        base_dir = tmp_path / "source"
        base_dir.mkdir()
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR"]

        # Act & Assert
        for level in valid_levels:
            config = ProjectConfiguration(
                java_source_dir=base_dir,
                log_level=level
            )
            assert config.log_level == level


class TestProjectConfigurationRepr:
    """Test string representation for debugging."""

    def test_repr_includes_key_fields(self, tmp_path):
        """Test that __repr__ includes key configuration fields."""
        # Arrange
        base_dir = tmp_path / "source"
        base_dir.mkdir()
        project_dir = base_dir / "myproject"
        project_dir.mkdir()

        # Act
        config = ProjectConfiguration(
            java_source_dir=base_dir,
            project_subdirectory="myproject",
            dependency_depth=2
        )

        repr_str = repr(config)

        # Assert
        assert "ProjectConfiguration" in repr_str
        assert str(base_dir) in repr_str
        assert "myproject" in repr_str
        assert "depth=2" in repr_str
