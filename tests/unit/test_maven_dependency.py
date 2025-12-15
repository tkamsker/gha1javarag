"""Unit tests for MavenDependency model."""

import pytest
from pathlib import Path
from src.codeindex.models.maven_dependency import MavenDependency


class TestMavenDependency:
    """Test suite for MavenDependency model validation and properties."""

    def test_create_valid_dependency(self):
        """Test creating a valid Maven dependency."""
        dep = MavenDependency(
            group_id="com.example",
            artifact_id="test-artifact",
            version="1.0.0",
            scope="compile"
        )

        assert dep.group_id == "com.example"
        assert dep.artifact_id == "test-artifact"
        assert dep.version == "1.0.0"
        assert dep.scope == "compile"
        assert dep.resolution_status == "pending"
        assert dep.depth == 0

    def test_missing_group_id(self):
        """Test that missing group_id raises ValueError."""
        with pytest.raises(ValueError, match="group_id and artifact_id are required"):
            MavenDependency(group_id="", artifact_id="test")

    def test_missing_artifact_id(self):
        """Test that missing artifact_id raises ValueError."""
        with pytest.raises(ValueError, match="group_id and artifact_id are required"):
            MavenDependency(group_id="com.example", artifact_id="")

    def test_invalid_scope(self):
        """Test that invalid scope raises ValueError."""
        with pytest.raises(ValueError, match="Invalid scope"):
            MavenDependency(
                group_id="com.example",
                artifact_id="test",
                scope="invalid_scope"
            )

    def test_valid_scopes(self):
        """Test that all valid scopes are accepted."""
        valid_scopes = ["compile", "test", "provided", "runtime", "system"]
        for scope in valid_scopes:
            dep = MavenDependency(
                group_id="com.example",
                artifact_id="test",
                scope=scope
            )
            assert dep.scope == scope

    def test_invalid_resolution_status(self):
        """Test that invalid resolution_status raises ValueError."""
        with pytest.raises(ValueError, match="Invalid resolution_status"):
            MavenDependency(
                group_id="com.example",
                artifact_id="test",
                resolution_status="invalid"
            )

    def test_valid_resolution_statuses(self):
        """Test that all valid resolution statuses are accepted."""
        valid_statuses = ["pending", "resolved", "not_found", "circular"]
        for status in valid_statuses:
            dep = MavenDependency(
                group_id="com.example",
                artifact_id="test",
                resolution_status=status
            )
            assert dep.resolution_status == status

    def test_negative_depth(self):
        """Test that depth < -1 raises ValueError."""
        with pytest.raises(ValueError, match="Depth must be >= -1"):
            MavenDependency(
                group_id="com.example",
                artifact_id="test",
                depth=-2
            )

    def test_coordinates_with_version(self):
        """Test coordinates property with version."""
        dep = MavenDependency(
            group_id="com.example",
            artifact_id="test-artifact",
            version="2.0.0"
        )
        assert dep.coordinates == "com.example:test-artifact:2.0.0"

    def test_coordinates_without_version(self):
        """Test coordinates property without version."""
        dep = MavenDependency(
            group_id="com.example",
            artifact_id="test-artifact"
        )
        assert dep.coordinates == "com.example:test-artifact"

    def test_is_resolved_property(self):
        """Test is_resolved property."""
        dep = MavenDependency(
            group_id="com.example",
            artifact_id="test",
            resolution_status="resolved"
        )
        assert dep.is_resolved is True

        dep.resolution_status = "pending"
        assert dep.is_resolved is False

    def test_is_circular_property(self):
        """Test is_circular property."""
        dep = MavenDependency(
            group_id="com.example",
            artifact_id="test",
            resolution_status="circular"
        )
        assert dep.is_circular is True

        dep.resolution_status = "resolved"
        assert dep.is_circular is False

    def test_is_not_found_property(self):
        """Test is_not_found property."""
        dep = MavenDependency(
            group_id="com.example",
            artifact_id="test",
            resolution_status="not_found"
        )
        assert dep.is_not_found is True

        dep.resolution_status="resolved"
        assert dep.is_not_found is False

    def test_repr(self):
        """Test string representation."""
        dep = MavenDependency(
            group_id="com.example",
            artifact_id="test-artifact",
            version="1.0.0",
            resolution_status="resolved"
        )
        repr_str = repr(dep)
        assert "MavenDependency" in repr_str
        assert "com.example" in repr_str
        assert "test-artifact" in repr_str
        assert "resolved" in repr_str

    def test_resolved_path(self):
        """Test resolved_path assignment."""
        dep = MavenDependency(
            group_id="com.example",
            artifact_id="test"
        )

        assert dep.resolved_path is None

        dep.resolved_path = Path("/workspace/test")
        assert dep.resolved_path == Path("/workspace/test")

    def test_declared_in_path(self):
        """Test declared_in path tracking."""
        pom_path = Path("/workspace/project/pom.xml")
        dep = MavenDependency(
            group_id="com.example",
            artifact_id="test",
            declared_in=pom_path
        )

        assert dep.declared_in == pom_path

    def test_depth_tracking(self):
        """Test dependency depth tracking."""
        # Direct dependency
        direct_dep = MavenDependency(
            group_id="com.example",
            artifact_id="direct",
            depth=0
        )
        assert direct_dep.depth == 0

        # Transitive dependency
        trans_dep = MavenDependency(
            group_id="com.example",
            artifact_id="transitive",
            depth=2
        )
        assert trans_dep.depth == 2
