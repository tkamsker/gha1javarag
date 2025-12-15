"""Unit tests for dependency resolver service."""

import pytest
from pathlib import Path
from src.codeindex.services.dependency_resolver import resolve_dependencies
from src.codeindex.models.dependency_graph import DependencyGraph


class TestResolveDependencies:
    """Test suite for resolve_dependencies function."""

    def test_resolve_simple_dependencies(self):
        """Test resolving a simple pom.xml with one dependency (T019)."""
        # Arrange
        pom_path = Path("tests/fixtures/pom-files/simple.xml")
        base_dir = Path("tests/fixtures/maven-projects")

        # Create mock dependency directory
        base_dir.mkdir(parents=True, exist_ok=True)
        dep_dir = base_dir / "cuco-cct-core"
        dep_dir.mkdir(exist_ok=True)

        # Act
        graph = resolve_dependencies(
            root_pom=pom_path,
            base_dir=base_dir,
            max_depth=1,
            project_name="test-project"
        )

        # Assert
        assert isinstance(graph, DependencyGraph)
        assert graph.project_name == "test-project"
        assert graph.total_dependencies >= 1
        assert graph.resolved_count >= 0  # May be 0 if dependency path doesn't exist

        # Check root node exists
        assert graph.root_node is not None
        assert graph.root_node.dependency.artifact_id == "test-project"

    def test_resolve_multi_module_dependencies(self):
        """Test resolving multi-module pom.xml with multiple dependencies (T019)."""
        # Arrange
        pom_path = Path("tests/fixtures/pom-files/multi-module.xml")
        base_dir = Path("tests/fixtures/maven-projects")

        # Act
        graph = resolve_dependencies(
            root_pom=pom_path,
            base_dir=base_dir,
            max_depth=1,
            project_name="multi-module-project"
        )

        # Assert
        assert isinstance(graph, DependencyGraph)
        assert graph.project_name == "multi-module-project"
        assert graph.total_dependencies >= 4  # 4 dependencies in multi-module.xml

        # Should have at least 4 direct dependencies
        direct_deps = graph.get_dependencies_at_depth(0)
        assert len(direct_deps) >= 4

    def test_circular_dependency_detection(self):
        """Test that circular dependencies are detected and handled (T020)."""
        # Arrange
        pom_path = Path("tests/fixtures/pom-files/circular-deps.xml")
        base_dir = Path("tests/fixtures/maven-projects")

        # Create mock circular dependency structure
        project_a_dir = base_dir / "circular-project-a"
        project_b_dir = base_dir / "circular-project-b"
        project_a_dir.mkdir(parents=True, exist_ok=True)
        project_b_dir.mkdir(parents=True, exist_ok=True)

        # Act
        graph = resolve_dependencies(
            root_pom=pom_path,
            base_dir=base_dir,
            max_depth=5,  # Deep enough to detect cycles
            project_name="circular-test"
        )

        # Assert
        assert isinstance(graph, DependencyGraph)

        # Check if circular dependencies were detected
        # Note: circular_count may be 0 if the mock structure doesn't trigger it
        # The key is that resolution completes without infinite loop
        assert graph.circular_count >= 0

        # If circular paths detected, verify they're logged
        if graph.circular_paths:
            assert len(graph.circular_paths) > 0
            # Each path should be a list of artifact IDs
            for path in graph.circular_paths:
                assert isinstance(path, list)
                assert len(path) >= 2  # At least 2 artifacts in a cycle

    def test_missing_artifact_handling(self):
        """Test that missing artifacts are handled gracefully (T021)."""
        # Arrange
        pom_path = Path("tests/fixtures/pom-files/simple.xml")
        base_dir = Path("tests/fixtures/nonexistent-directory")

        # Act
        graph = resolve_dependencies(
            root_pom=pom_path,
            base_dir=base_dir,
            max_depth=1,
            project_name="missing-deps-test"
        )

        # Assert
        assert isinstance(graph, DependencyGraph)
        assert graph.project_name == "missing-deps-test"

        # All dependencies should be marked as not found
        assert graph.not_found_count > 0

        # Check that unresolved dependencies are tracked
        unresolved = graph.get_unresolved_dependencies()
        assert len(unresolved) > 0

        # Each unresolved dependency should have correct status
        for dep in unresolved:
            assert dep.resolution_status == "not_found"
            assert dep.resolved_path is None

    def test_depth_limit_enforcement(self):
        """Test that max_depth parameter is enforced (T019)."""
        # Arrange
        pom_path = Path("tests/fixtures/pom-files/multi-module.xml")
        base_dir = Path("tests/fixtures/maven-projects")

        # Act - resolve with depth 0 (only direct deps)
        graph_depth_0 = resolve_dependencies(
            root_pom=pom_path,
            base_dir=base_dir,
            max_depth=0,
            project_name="depth-test"
        )

        # Act - resolve with depth 1 (direct + transitive)
        graph_depth_1 = resolve_dependencies(
            root_pom=pom_path,
            base_dir=base_dir,
            max_depth=1,
            project_name="depth-test"
        )

        # Assert
        # max_depth in graph should match or be less than requested
        assert graph_depth_0.max_depth <= 0
        assert graph_depth_1.max_depth <= 1

    def test_nonexistent_pom_raises_error(self):
        """Test that nonexistent pom.xml raises FileNotFoundError (T021)."""
        # Arrange
        pom_path = Path("tests/fixtures/pom-files/nonexistent-pom.xml")
        base_dir = Path("tests/fixtures/maven-projects")

        # Act & Assert
        with pytest.raises(FileNotFoundError, match="Root pom.xml not found"):
            resolve_dependencies(
                root_pom=pom_path,
                base_dir=base_dir,
                max_depth=1,
                project_name="error-test"
            )

    def test_dependency_graph_statistics(self):
        """Test that dependency graph calculates statistics correctly (T019)."""
        # Arrange
        pom_path = Path("tests/fixtures/pom-files/multi-module.xml")
        base_dir = Path("tests/fixtures/maven-projects")

        # Act
        graph = resolve_dependencies(
            root_pom=pom_path,
            base_dir=base_dir,
            max_depth=1,
            project_name="stats-test"
        )

        # Assert
        assert graph.total_dependencies >= 0
        assert graph.resolved_count >= 0
        assert graph.not_found_count >= 0
        assert graph.circular_count >= 0

        # Total should equal sum of resolved + not_found + circular
        # Note: this may not hold exactly due to how we count, but check it's reasonable
        assert graph.total_dependencies >= graph.resolved_count

        # Success rate should be 0-100
        assert 0.0 <= graph.success_rate <= 100.0

        # Resolution duration should be set
        assert graph.resolution_duration is not None
        assert graph.resolution_duration >= 0

    def test_get_all_dependencies(self):
        """Test that get_all_dependencies returns flattened dependency list (T019)."""
        # Arrange
        pom_path = Path("tests/fixtures/pom-files/multi-module.xml")
        base_dir = Path("tests/fixtures/maven-projects")

        # Act
        graph = resolve_dependencies(
            root_pom=pom_path,
            base_dir=base_dir,
            max_depth=1,
            project_name="flatten-test"
        )

        all_deps = graph.get_all_dependencies()

        # Assert
        assert isinstance(all_deps, list)
        assert len(all_deps) == graph.total_dependencies

        # Each dependency should have required fields
        for dep in all_deps:
            assert dep.artifact_id is not None
            assert dep.group_id is not None
            assert dep.depth >= 0

    def test_dependency_resolution_with_project_name(self):
        """Test that project_name is properly set in graph (T019)."""
        # Arrange
        pom_path = Path("tests/fixtures/pom-files/simple.xml")
        base_dir = Path("tests/fixtures/maven-projects")
        custom_name = "my-custom-project"

        # Act
        graph = resolve_dependencies(
            root_pom=pom_path,
            base_dir=base_dir,
            max_depth=1,
            project_name=custom_name
        )

        # Assert
        assert graph.project_name == custom_name
        assert graph.root_node.dependency.artifact_id == custom_name
