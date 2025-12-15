"""Unit tests for Maven POM parser."""

import pytest
import xml.etree.ElementTree as ET
from pathlib import Path
from src.codeindex.services.maven_parser import parse_pom
from src.codeindex.models.maven_dependency import MavenDependency


class TestParsePom:
    """Test suite for parse_pom function."""

    def test_parse_simple_pom(self):
        """Test parsing simple pom.xml with single dependency."""
        pom_path = Path("tests/fixtures/pom-files/simple.xml")
        dependencies = parse_pom(pom_path)

        assert len(dependencies) == 1
        dep = dependencies[0]
        assert dep.group_id == "at.a1ta.cuco"
        assert dep.artifact_id == "cuco-cct-core"
        assert dep.version == "1.0.0"
        assert dep.scope == "compile"
        assert dep.depth == 0

    def test_parse_multi_module_pom(self):
        """Test parsing multi-module pom.xml with multiple dependencies."""
        pom_path = Path("tests/fixtures/pom-files/multi-module.xml")
        dependencies = parse_pom(pom_path)

        # Should have 4 dependencies (3 cuco + 1 junit)
        assert len(dependencies) == 4

        # Check test scope dependency
        junit_dep = next(d for d in dependencies if d.artifact_id == "junit")
        assert junit_dep.scope == "test"

    def test_parse_nonexistent_pom(self):
        """Test parsing non-existent pom.xml raises FileNotFoundError."""
        pom_path = Path("tests/fixtures/pom-files/nonexistent.xml")
        with pytest.raises(FileNotFoundError):
            parse_pom(pom_path)

    def test_parse_malformed_xml(self, tmp_path):
        """Test parsing malformed XML raises ParseError."""
        malformed_pom = tmp_path / "malformed.xml"
        malformed_pom.write_text("<?xml version='1.0'?><project><unclosed>")

        with pytest.raises(ET.ParseError):
            parse_pom(malformed_pom)
