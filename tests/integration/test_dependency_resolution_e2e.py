"""Integration tests for end-to-end dependency resolution (T022)."""

import pytest
import tempfile
import shutil
from pathlib import Path
from src.codeindex.services.dependency_resolver import resolve_dependencies
from src.codeindex.services.discovery import DiscoveryService
from src.codeindex.utils.config import Config


class TestDependencyResolutionE2E:
    """End-to-end integration tests for dependency resolution."""

    @pytest.fixture
    def temp_maven_workspace(self):
        """
        Create a temporary Maven workspace with multiple projects.

        Structure:
            workspace/
              ├─ project-a/
              │  └─ pom.xml (depends on project-b)
              ├─ project-b/
              │  └─ pom.xml (depends on project-c)
              └─ project-c/
                 └─ pom.xml (no dependencies)
        """
        # Create temporary directory
        temp_dir = Path(tempfile.mkdtemp())

        try:
            # Create project-c (leaf dependency)
            project_c = temp_dir / "project-c"
            project_c.mkdir()
            (project_c / "pom.xml").write_text("""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.test</groupId>
    <artifactId>project-c</artifactId>
    <version>1.0.0</version>
    <dependencies>
        <!-- No dependencies -->
    </dependencies>
</project>
""")

            # Create project-b (depends on project-c)
            project_b = temp_dir / "project-b"
            project_b.mkdir()
            (project_b / "pom.xml").write_text("""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.test</groupId>
    <artifactId>project-b</artifactId>
    <version>1.0.0</version>
    <dependencies>
        <dependency>
            <groupId>com.test</groupId>
            <artifactId>project-c</artifactId>
            <version>1.0.0</version>
        </dependency>
    </dependencies>
</project>
""")

            # Create project-a (depends on project-b)
            project_a = temp_dir / "project-a"
            project_a.mkdir()
            (project_a / "pom.xml").write_text("""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.test</groupId>
    <artifactId>project-a</artifactId>
    <version>1.0.0</version>
    <dependencies>
        <dependency>
            <groupId>com.test</groupId>
            <artifactId>project-b</artifactId>
            <version>1.0.0</version>
        </dependency>
    </dependencies>
</project>
""")

            yield temp_dir

        finally:
            # Cleanup
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_e2e_dependency_resolution_depth_0(self, temp_maven_workspace):
        """Test end-to-end resolution with depth=0 (direct dependencies only)."""
        # Arrange
        project_a_pom = temp_maven_workspace / "project-a" / "pom.xml"

        # Act
        graph = resolve_dependencies(
            root_pom=project_a_pom,
            base_dir=temp_maven_workspace,
            max_depth=0,
            project_name="project-a"
        )

        # Assert
        assert graph.project_name == "project-a"
        assert graph.total_dependencies >= 1  # At least project-b
        assert graph.max_depth <= 0  # Should not exceed requested depth

        # Check that project-b is resolved
        all_deps = graph.get_all_dependencies()
        artifact_ids = [dep.artifact_id for dep in all_deps]
        assert "project-b" in artifact_ids

    def test_e2e_dependency_resolution_depth_1(self, temp_maven_workspace):
        """Test end-to-end resolution with depth=1 (transitive dependencies)."""
        # Arrange
        project_a_pom = temp_maven_workspace / "project-a" / "pom.xml"

        # Act
        graph = resolve_dependencies(
            root_pom=project_a_pom,
            base_dir=temp_maven_workspace,
            max_depth=1,
            project_name="project-a"
        )

        # Assert
        assert graph.project_name == "project-a"
        assert graph.total_dependencies >= 2  # At least project-b and project-c

        # Check that both project-b and project-c are resolved
        all_deps = graph.get_all_dependencies()
        artifact_ids = [dep.artifact_id for dep in all_deps]
        assert "project-b" in artifact_ids
        assert "project-c" in artifact_ids

        # Verify dependency depths
        project_b_dep = next((d for d in all_deps if d.artifact_id == "project-b"), None)
        project_c_dep = next((d for d in all_deps if d.artifact_id == "project-c"), None)

        assert project_b_dep is not None
        assert project_c_dep is not None
        assert project_b_dep.depth == 0  # Direct dependency
        assert project_c_dep.depth == 1  # Transitive dependency

    def test_e2e_discovery_with_dependency_resolution(self, temp_maven_workspace):
        """Test full discovery service integration with dependency resolution."""
        # Arrange
        config = Config()
        service = DiscoveryService(config=config, dependency_depth=1)

        # Act
        inventory = service.generate_inventory(temp_maven_workspace)

        # Assert
        assert inventory is not None
        assert len(inventory.projects) == 3  # project-a, project-b, project-c

        # Check that dependency resolution was performed
        for project_dict in inventory.projects:
            if project_dict.get('artifact_id') in ['project-a', 'project-b']:
                # These projects have dependencies
                assert 'dependency_resolution' in project_dict
                dep_res = project_dict['dependency_resolution']
                assert dep_res['total'] >= 0
                assert dep_res['resolved'] >= 0
                assert 'success_rate' in dep_res

    def test_e2e_circular_dependency_handling(self):
        """Test handling of circular dependencies in real workspace."""
        # Create temporary workspace with circular dependencies
        temp_dir = Path(tempfile.mkdtemp())

        try:
            # Create project-x (depends on project-y)
            project_x = temp_dir / "project-x"
            project_x.mkdir()
            (project_x / "pom.xml").write_text("""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.test</groupId>
    <artifactId>project-x</artifactId>
    <version>1.0.0</version>
    <dependencies>
        <dependency>
            <groupId>com.test</groupId>
            <artifactId>project-y</artifactId>
            <version>1.0.0</version>
        </dependency>
    </dependencies>
</project>
""")

            # Create project-y (depends on project-x - circular!)
            project_y = temp_dir / "project-y"
            project_y.mkdir()
            (project_y / "pom.xml").write_text("""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.test</groupId>
    <artifactId>project-y</artifactId>
    <version>1.0.0</version>
    <dependencies>
        <dependency>
            <groupId>com.test</groupId>
            <artifactId>project-x</artifactId>
            <version>1.0.0</version>
        </dependency>
    </dependencies>
</project>
""")

            # Act
            graph = resolve_dependencies(
                root_pom=project_x / "pom.xml",
                base_dir=temp_dir,
                max_depth=3,
                project_name="project-x"
            )

            # Assert - resolution should complete without hanging
            assert graph is not None
            assert graph.project_name == "project-x"

            # Circular dependencies should be detected
            assert graph.circular_count > 0
            assert len(graph.circular_paths) > 0

        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_e2e_performance_within_limit(self, temp_maven_workspace):
        """Test that dependency resolution completes within performance limit (T037)."""
        # Arrange
        project_a_pom = temp_maven_workspace / "project-a" / "pom.xml"

        # Act
        graph = resolve_dependencies(
            root_pom=project_a_pom,
            base_dir=temp_maven_workspace,
            max_depth=2,
            project_name="project-a"
        )

        # Assert - should complete within 10 seconds for small workspace
        # (This workspace has only 3 projects with 2 dependencies)
        assert graph.resolution_duration is not None
        assert graph.resolution_duration < 10.0, (
            f"Resolution took {graph.resolution_duration:.2f}s, "
            f"exceeding 10s limit (FR-010)"
        )

    def test_e2e_missing_dependencies(self):
        """Test handling of missing dependencies in real scenario."""
        # Create temporary workspace
        temp_dir = Path(tempfile.mkdtemp())

        try:
            # Create project with missing dependency
            project = temp_dir / "test-project"
            project.mkdir()
            (project / "pom.xml").write_text("""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.test</groupId>
    <artifactId>test-project</artifactId>
    <version>1.0.0</version>
    <dependencies>
        <dependency>
            <groupId>com.test</groupId>
            <artifactId>missing-dependency</artifactId>
            <version>1.0.0</version>
        </dependency>
    </dependencies>
</project>
""")

            # Act
            graph = resolve_dependencies(
                root_pom=project / "pom.xml",
                base_dir=temp_dir,
                max_depth=1,
                project_name="test-project"
            )

            # Assert
            assert graph is not None
            assert graph.not_found_count >= 1
            assert len(graph.resolution_errors) >= 1

            # Check unresolved dependencies
            unresolved = graph.get_unresolved_dependencies()
            assert len(unresolved) >= 1
            assert any(dep.artifact_id == "missing-dependency" for dep in unresolved)

        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
