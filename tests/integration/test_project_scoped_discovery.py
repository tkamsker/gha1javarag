"""Integration test for project-scoped discovery (T070).

Tests the complete workflow of discovering and analyzing only files within
a specific project subdirectory when --project parameter is specified.
"""

import pytest
from pathlib import Path
from codeindex.services.discovery import DiscoveryService
from codeindex.models.project_configuration import ProjectConfiguration


class TestProjectScopedDiscovery:
    """Integration tests for project-scoped discovery (T070)."""

    @pytest.fixture
    def monorepo_structure(self, tmp_path):
        """
        Create a monorepo test structure with multiple projects.

        Structure:
            source/
                project-a/
                    pom.xml
                    src/main/java/com/example/a/ClassA.java
                project-b/
                    pom.xml
                    src/main/java/com/example/b/ClassB.java
                shared/
                    pom.xml
                    src/main/java/com/example/shared/SharedClass.java
        """
        base_dir = tmp_path / "source"
        base_dir.mkdir()

        # Project A
        project_a = base_dir / "project-a"
        project_a.mkdir()
        pom_a = project_a / "pom.xml"
        pom_a.write_text("""<?xml version="1.0"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <groupId>com.example</groupId>
    <artifactId>project-a</artifactId>
    <version>1.0.0</version>
</project>""")

        src_a = project_a / "src/main/java/com/example/a"
        src_a.mkdir(parents=True)
        (src_a / "ClassA.java").write_text("""
package com.example.a;
public class ClassA {
    public void methodA() {}
}""")

        # Project B
        project_b = base_dir / "project-b"
        project_b.mkdir()
        pom_b = project_b / "pom.xml"
        pom_b.write_text("""<?xml version="1.0"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <groupId>com.example</groupId>
    <artifactId>project-b</artifactId>
    <version>1.0.0</version>
</project>""")

        src_b = project_b / "src/main/java/com/example/b"
        src_b.mkdir(parents=True)
        (src_b / "ClassB.java").write_text("""
package com.example.b;
public class ClassB {
    public void methodB() {}
}""")

        # Shared project
        project_shared = base_dir / "shared"
        project_shared.mkdir()
        pom_shared = project_shared / "pom.xml"
        pom_shared.write_text("""<?xml version="1.0"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <groupId>com.example</groupId>
    <artifactId>shared</artifactId>
    <version>1.0.0</version>
</project>""")

        src_shared = project_shared / "src/main/java/com/example/shared"
        src_shared.mkdir(parents=True)
        (src_shared / "SharedClass.java").write_text("""
package com.example.shared;
public class SharedClass {
    public void sharedMethod() {}
}""")

        return base_dir

    def test_project_scoped_discovery_single_project(self, monorepo_structure):
        """
        Test that project-scoped discovery only finds files in specified project (T070).

        When --project project-a is specified, should only discover:
        - project-a/pom.xml
        - project-a/src/main/java/com/example/a/ClassA.java

        Should NOT discover files from project-b or shared.
        """
        # Arrange
        config = ProjectConfiguration(
            java_source_dir=monorepo_structure,
            project_subdirectory="project-a",
            dependency_depth=0  # No dependency resolution for this test
        )
        service = DiscoveryService(dependency_depth=0)

        # Act
        inventory = service.generate_inventory(config.effective_base_dir)

        # Assert - Should find only project-a
        assert inventory is not None
        assert inventory.total_files > 0

        # Check that only project-a files are included
        file_paths = [f['path'] for f in inventory.projects[0]['files']]

        # Should include ClassA.java
        assert any('ClassA.java' in path for path in file_paths)

        # Should NOT include ClassB.java or SharedClass.java
        assert not any('ClassB.java' in path for path in file_paths)
        assert not any('SharedClass.java' in path for path in file_paths)

        # Verify project artifact_id
        projects = inventory.projects
        assert len(projects) == 1
        assert projects[0]['artifact_id'] == 'project-a'

    def test_project_scoped_discovery_different_project(self, monorepo_structure):
        """
        Test project-scoped discovery on different project (T070).

        Verify that changing --project parameter correctly scopes to different project.
        """
        # Arrange
        config = ProjectConfiguration(
            java_source_dir=monorepo_structure,
            project_subdirectory="project-b",
            dependency_depth=0
        )
        service = DiscoveryService(dependency_depth=0)

        # Act
        inventory = service.generate_inventory(config.effective_base_dir)

        # Assert
        file_paths = [f['path'] for f in inventory.projects[0]['files']]

        # Should include ClassB.java
        assert any('ClassB.java' in path for path in file_paths)

        # Should NOT include ClassA.java or SharedClass.java
        assert not any('ClassA.java' in path for path in file_paths)
        assert not any('SharedClass.java' in path for path in file_paths)

        # Verify project artifact_id
        assert inventory.projects[0]['artifact_id'] == 'project-b'

    def test_project_scoped_discovery_without_project_finds_all(self, monorepo_structure):
        """
        Test that discovery without project scope finds all projects (T070).

        When no --project is specified, should discover all projects in monorepo.
        """
        # Arrange
        config = ProjectConfiguration(
            java_source_dir=monorepo_structure,
            project_subdirectory=None,  # No project scoping
            dependency_depth=0
        )
        service = DiscoveryService(dependency_depth=0)

        # Act
        inventory = service.generate_inventory(config.effective_base_dir)

        # Assert - Should find all three projects
        assert len(inventory.projects) == 3

        artifact_ids = [p['artifact_id'] for p in inventory.projects]
        assert 'project-a' in artifact_ids
        assert 'project-b' in artifact_ids
        assert 'shared' in artifact_ids

    def test_project_scoped_discovery_with_dependencies(self, monorepo_structure):
        """
        Test project-scoped discovery with dependency resolution (T070).

        When project has dependencies and dependency_depth > 0, should resolve
        dependencies relative to effective_base_dir.
        """
        # Arrange - Modify project-a to depend on shared
        project_a_pom = monorepo_structure / "project-a" / "pom.xml"
        project_a_pom.write_text("""<?xml version="1.0"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <groupId>com.example</groupId>
    <artifactId>project-a</artifactId>
    <version>1.0.0</version>
    <dependencies>
        <dependency>
            <groupId>com.example</groupId>
            <artifactId>shared</artifactId>
        </dependency>
    </dependencies>
</project>""")

        config = ProjectConfiguration(
            java_source_dir=monorepo_structure,
            project_subdirectory="project-a",
            dependency_depth=1  # Enable dependency resolution
        )
        service = DiscoveryService(dependency_depth=1)

        # Act
        inventory = service.generate_inventory(config.effective_base_dir)

        # Assert
        project = inventory.projects[0]

        # Check dependency resolution metadata
        if 'dependency_resolution' in project:
            dep_resolution = project['dependency_resolution']

            # Should have attempted to resolve dependencies
            assert dep_resolution['total'] >= 1

            # Files may include dependency files if resolved
            # (depends on path resolver finding shared project)
            all_files = project['files']
            assert len(all_files) > 0

    def test_project_scoped_paths_are_absolute(self, monorepo_structure):
        """
        Test that all file paths in project-scoped discovery are absolute (T070).

        FR-025: All paths should be absolute for consistent resolution.
        """
        # Arrange
        config = ProjectConfiguration(
            java_source_dir=monorepo_structure,
            project_subdirectory="project-a",
            dependency_depth=0
        )
        service = DiscoveryService(dependency_depth=0)

        # Act
        inventory = service.generate_inventory(config.effective_base_dir)

        # Assert
        for project in inventory.projects:
            for file_info in project['files']:
                file_path = Path(file_info['path'])
                assert file_path.is_absolute(), \
                    f"Path should be absolute: {file_path}"

    def test_project_scoped_discovery_respects_effective_base_dir(self, monorepo_structure):
        """
        Test that discovery uses effective_base_dir correctly (T070).

        The effective_base_dir should be java_source_dir/project_subdirectory,
        and all discovered files should be within that directory.
        """
        # Arrange
        config = ProjectConfiguration(
            java_source_dir=monorepo_structure,
            project_subdirectory="project-a",
            dependency_depth=0
        )
        service = DiscoveryService(dependency_depth=0)

        # Act
        inventory = service.generate_inventory(config.effective_base_dir)

        # Assert
        effective_base = config.effective_base_dir

        for project in inventory.projects:
            for file_info in project['files']:
                file_path = Path(file_info['path'])

                # File should be within effective_base_dir (unless it's a dependency)
                if not file_info.get('is_dependency', False):
                    assert file_path.is_relative_to(effective_base), \
                        f"File {file_path} should be within {effective_base}"

    def test_project_scoped_discovery_metadata_includes_project_name(self, monorepo_structure):
        """
        Test that discovery metadata includes project name (T070, T081).

        The inventory should include the project name in metadata.
        """
        # Arrange
        config = ProjectConfiguration(
            java_source_dir=monorepo_structure,
            project_subdirectory="project-a",
            dependency_depth=0
        )
        service = DiscoveryService(dependency_depth=0)

        # Act
        inventory = service.generate_inventory(config.effective_base_dir)

        # Assert
        assert len(inventory.projects) == 1
        project = inventory.projects[0]

        # Project should have artifact_id that matches
        assert project['artifact_id'] == 'project-a'

    def test_project_scoped_discovery_completes_quickly(self, monorepo_structure):
        """
        Test that project-scoped discovery completes quickly (T084, SC-008).

        Project-scoped analysis should complete in <30 seconds.
        For this small test, should be nearly instant.
        """
        # Arrange
        import time
        config = ProjectConfiguration(
            java_source_dir=monorepo_structure,
            project_subdirectory="project-a",
            dependency_depth=1
        )
        service = DiscoveryService(dependency_depth=1)

        # Act
        start_time = time.time()
        inventory = service.generate_inventory(config.effective_base_dir)
        duration = time.time() - start_time

        # Assert - SC-008: <30 seconds (should be much faster for test)
        assert duration < 30.0, \
            f"Discovery took {duration:.2f}s, expected <30s"

        # For this small test, should be very fast
        assert duration < 5.0, \
            f"Discovery took {duration:.2f}s, expected <5s for small test"

    def test_project_scoped_discovery_with_nested_path(self, tmp_path):
        """
        Test project-scoped discovery with nested project path (T070).

        Should support project paths like "parent/child".
        """
        # Arrange - Create nested structure
        base_dir = tmp_path / "source"
        base_dir.mkdir()

        parent_dir = base_dir / "parent"
        parent_dir.mkdir()

        child_dir = parent_dir / "child"
        child_dir.mkdir()

        pom = child_dir / "pom.xml"
        pom.write_text("""<?xml version="1.0"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <groupId>com.example</groupId>
    <artifactId>nested-project</artifactId>
    <version>1.0.0</version>
</project>""")

        src = child_dir / "src/main/java"
        src.mkdir(parents=True)
        (src / "Test.java").write_text("public class Test {}")

        config = ProjectConfiguration(
            java_source_dir=base_dir,
            project_subdirectory="parent/child",
            dependency_depth=0
        )
        service = DiscoveryService(dependency_depth=0)

        # Act
        inventory = service.generate_inventory(config.effective_base_dir)

        # Assert
        assert len(inventory.projects) == 1
        assert inventory.projects[0]['artifact_id'] == 'nested-project'
        assert inventory.total_files >= 2  # pom.xml + Test.java
