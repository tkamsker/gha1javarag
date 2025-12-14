"""
Unit tests for Maven POM parser.

Tests Maven POM parsing functionality including coordinate extraction,
module parsing, dependency extraction, and error handling.

NOTE: These tests should FAIL initially (TDD approach).
"""

import pytest
from pathlib import Path
from lxml import etree

from codeindex.services.maven import (
    MavenParser,
    POMParseError,
    extract_maven_coordinates,
    extract_modules,
    extract_dependencies,
    extract_build_config,
)


# Fixtures
@pytest.fixture
def sample_pom_path():
    """Path to valid sample POM file."""
    return Path(__file__).parent.parent / "fixtures" / "sample_pom.xml"


@pytest.fixture
def broken_pom_path():
    """Path to malformed POM file."""
    return Path(__file__).parent.parent / "fixtures" / "malformed" / "broken_pom.xml"


@pytest.fixture
def sample_pom_tree(sample_pom_path):
    """Parsed XML tree of sample POM."""
    return etree.parse(str(sample_pom_path))


@pytest.fixture
def maven_parser():
    """MavenParser instance."""
    return MavenParser()


# Test coordinate extraction
class TestCoordinateExtraction:
    """Test Maven coordinate extraction."""

    def test_extract_basic_coordinates(self, sample_pom_tree):
        """Test extraction of groupId, artifactId, version."""
        coords = extract_maven_coordinates(sample_pom_tree)

        assert coords is not None
        assert coords["groupId"] == "com.example"
        assert coords["artifactId"] == "test-project"
        assert coords["version"] == "1.0.0-SNAPSHOT"

    def test_extract_packaging(self, sample_pom_tree):
        """Test extraction of packaging type."""
        coords = extract_maven_coordinates(sample_pom_tree)

        assert coords["packaging"] == "jar"

    def test_extract_name_and_description(self, sample_pom_tree):
        """Test extraction of project name and description."""
        coords = extract_maven_coordinates(sample_pom_tree)

        assert coords["name"] == "Test Project"
        assert coords["description"] == "Sample Maven project for testing"

    def test_missing_groupid(self, broken_pom_path):
        """Test handling of missing groupId."""
        tree = etree.parse(str(broken_pom_path))

        coords = extract_maven_coordinates(tree)
        assert coords["groupId"] is None

    def test_default_packaging(self):
        """Test default packaging when not specified."""
        minimal_pom = """<?xml version="1.0"?>
        <project xmlns="http://maven.apache.org/POM/4.0.0">
            <modelVersion>4.0.0</modelVersion>
            <groupId>com.test</groupId>
            <artifactId>minimal</artifactId>
            <version>1.0</version>
        </project>
        """
        tree = etree.fromstring(minimal_pom.encode())
        coords = extract_maven_coordinates(tree)

        assert coords["packaging"] == "jar"  # Maven default


# Test module extraction
class TestModuleExtraction:
    """Test Maven module extraction."""

    def test_extract_modules(self, sample_pom_tree):
        """Test extraction of module list."""
        modules = extract_modules(sample_pom_tree)

        assert modules is not None
        assert len(modules) == 2
        assert "test-module-a" in modules
        assert "test-module-b" in modules

    def test_no_modules(self):
        """Test POM without modules section."""
        pom_without_modules = """<?xml version="1.0"?>
        <project xmlns="http://maven.apache.org/POM/4.0.0">
            <modelVersion>4.0.0</modelVersion>
            <groupId>com.test</groupId>
            <artifactId>single</artifactId>
            <version>1.0</version>
        </project>
        """
        tree = etree.fromstring(pom_without_modules.encode())
        modules = extract_modules(tree)

        assert modules == []

    def test_empty_modules_section(self):
        """Test POM with empty modules section."""
        pom_empty_modules = """<?xml version="1.0"?>
        <project xmlns="http://maven.apache.org/POM/4.0.0">
            <modelVersion>4.0.0</modelVersion>
            <groupId>com.test</groupId>
            <artifactId>single</artifactId>
            <version>1.0</version>
            <modules></modules>
        </project>
        """
        tree = etree.fromstring(pom_empty_modules.encode())
        modules = extract_modules(tree)

        assert modules == []


# Test dependency extraction
class TestDependencyExtraction:
    """Test Maven dependency extraction."""

    def test_extract_dependencies(self, sample_pom_tree):
        """Test extraction of dependency list."""
        deps = extract_dependencies(sample_pom_tree)

        assert deps is not None
        assert len(deps) == 2

    def test_dependency_coordinates(self, sample_pom_tree):
        """Test dependency coordinate format."""
        deps = extract_dependencies(sample_pom_tree)

        # Check Spring dependency
        spring_dep = next(d for d in deps if "spring-core" in d)
        assert "org.springframework:spring-core:5.3.20" in spring_dep

        # Check JUnit dependency
        junit_dep = next(d for d in deps if "junit" in d)
        assert "junit:junit:4.13.2" in junit_dep

    def test_dependency_scope(self, sample_pom_tree):
        """Test dependency scope extraction."""
        deps = extract_dependencies(sample_pom_tree, include_scope=True)

        junit_dep = next(d for d in deps if "junit" in d)
        assert "test" in junit_dep or "scope=test" in junit_dep

    def test_no_dependencies(self):
        """Test POM without dependencies."""
        pom_no_deps = """<?xml version="1.0"?>
        <project xmlns="http://maven.apache.org/POM/4.0.0">
            <modelVersion>4.0.0</modelVersion>
            <groupId>com.test</groupId>
            <artifactId>standalone</artifactId>
            <version>1.0</version>
        </project>
        """
        tree = etree.fromstring(pom_no_deps.encode())
        deps = extract_dependencies(tree)

        assert deps == []


# Test build configuration extraction
class TestBuildConfigExtraction:
    """Test build configuration extraction."""

    def test_extract_source_directory(self, sample_pom_tree):
        """Test extraction of source directory."""
        build_config = extract_build_config(sample_pom_tree)

        assert build_config is not None
        assert build_config["sourceDirectory"] == "src/main/java"

    def test_extract_test_directory(self, sample_pom_tree):
        """Test extraction of test directory."""
        build_config = extract_build_config(sample_pom_tree)

        assert build_config["testSourceDirectory"] == "src/test/java"

    def test_extract_resource_directories(self, sample_pom_tree):
        """Test extraction of resource directories."""
        build_config = extract_build_config(sample_pom_tree)

        assert "resources" in build_config
        assert len(build_config["resources"]) == 1
        assert build_config["resources"][0]["directory"] == "src/main/resources"

    def test_default_build_config(self):
        """Test default build configuration when not specified."""
        minimal_pom = """<?xml version="1.0"?>
        <project xmlns="http://maven.apache.org/POM/4.0.0">
            <modelVersion>4.0.0</modelVersion>
            <groupId>com.test</groupId>
            <artifactId>minimal</artifactId>
            <version>1.0</version>
        </project>
        """
        tree = etree.fromstring(minimal_pom.encode())
        build_config = extract_build_config(tree)

        # Maven defaults
        assert build_config["sourceDirectory"] == "src/main/java"
        assert build_config["testSourceDirectory"] == "src/test/java"


# Test MavenParser class
class TestMavenParser:
    """Test MavenParser high-level API."""

    def test_parse_valid_pom(self, maven_parser, sample_pom_path):
        """Test parsing valid POM file."""
        result = maven_parser.parse_pom(sample_pom_path)

        assert result is not None
        assert result["groupId"] == "com.example"
        assert result["artifactId"] == "test-project"
        assert result["version"] == "1.0.0-SNAPSHOT"
        assert len(result["modules"]) == 2
        assert len(result["dependencies"]) == 2

    def test_parse_malformed_pom(self, maven_parser):
        """Test parsing malformed POM file (invalid XML)."""
        invalid_xml_path = Path(__file__).parent.parent / "fixtures" / "malformed" / "invalid_xml.xml"
        with pytest.raises(POMParseError):
            maven_parser.parse_pom(invalid_xml_path)

    def test_parse_nonexistent_file(self, maven_parser):
        """Test parsing non-existent file."""
        with pytest.raises(FileNotFoundError):
            maven_parser.parse_pom(Path("/nonexistent/pom.xml"))

    def test_parse_with_parent(self, maven_parser):
        """Test parsing POM with parent reference."""
        pom_with_parent = """<?xml version="1.0"?>
        <project xmlns="http://maven.apache.org/POM/4.0.0">
            <modelVersion>4.0.0</modelVersion>

            <parent>
                <groupId>com.example</groupId>
                <artifactId>parent-pom</artifactId>
                <version>2.0.0</version>
            </parent>

            <artifactId>child-project</artifactId>
        </project>
        """
        # Write temp file
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            f.write(pom_with_parent)
            temp_path = Path(f.name)

        try:
            result = maven_parser.parse_pom(temp_path)

            # Should inherit groupId and version from parent
            assert result["parentGroupId"] == "com.example"
            assert result["parentVersion"] == "2.0.0"
        finally:
            temp_path.unlink()


# Test error handling
class TestErrorHandling:
    """Test error handling in Maven parsing."""

    def test_invalid_xml(self, maven_parser):
        """Test handling of invalid XML."""
        import tempfile
        invalid_xml = "This is not XML"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            f.write(invalid_xml)
            temp_path = Path(f.name)

        try:
            with pytest.raises(POMParseError):
                maven_parser.parse_pom(temp_path)
        finally:
            temp_path.unlink()

    def test_missing_required_fields(self, maven_parser):
        """Test handling of POM missing required fields."""
        incomplete_pom = """<?xml version="1.0"?>
        <project xmlns="http://maven.apache.org/POM/4.0.0">
            <modelVersion>4.0.0</modelVersion>
            <!-- Missing artifactId -->
            <groupId>com.test</groupId>
            <version>1.0</version>
        </project>
        """

        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            f.write(incomplete_pom)
            temp_path = Path(f.name)

        try:
            with pytest.raises(POMParseError, match="artifactId"):
                maven_parser.parse_pom(temp_path)
        finally:
            temp_path.unlink()


# Test namespace handling
class TestNamespaceHandling:
    """Test XML namespace handling."""

    def test_pom_with_namespace(self, maven_parser):
        """Test parsing POM with namespace prefixes."""
        pom_with_ns = """<?xml version="1.0"?>
        <project xmlns="http://maven.apache.org/POM/4.0.0"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                                     http://maven.apache.org/xsd/maven-4.0.0.xsd">
            <modelVersion>4.0.0</modelVersion>
            <groupId>com.test</groupId>
            <artifactId>ns-project</artifactId>
            <version>1.0</version>
        </project>
        """

        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            f.write(pom_with_ns)
            temp_path = Path(f.name)

        try:
            result = maven_parser.parse_pom(temp_path)
            assert result["artifactId"] == "ns-project"
        finally:
            temp_path.unlink()

    def test_pom_without_namespace(self, maven_parser):
        """Test parsing POM without namespace (should still work)."""
        pom_no_ns = """<?xml version="1.0"?>
        <project>
            <modelVersion>4.0.0</modelVersion>
            <groupId>com.test</groupId>
            <artifactId>no-ns</artifactId>
            <version>1.0</version>
        </project>
        """

        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            f.write(pom_no_ns)
            temp_path = Path(f.name)

        try:
            result = maven_parser.parse_pom(temp_path)
            assert result["artifactId"] == "no-ns"
        finally:
            temp_path.unlink()
