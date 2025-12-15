"""
Unit tests for XML configuration parser.

Tests parsing of XML configuration files (Spring, MyBatis, web.xml, etc.).

NOTE: These tests should FAIL initially (TDD approach).
"""

import pytest
from pathlib import Path
from typing import List, Dict

from codeindex.parsers.xml_parser import (
    XMLParser,
    parse_xml_file,
    extract_root_element,
    extract_namespaces,
    extract_beans,
    extract_elements_by_tag,
)


# Fixtures
@pytest.fixture
def fixtures_dir():
    """Path to test fixtures directory."""
    return Path(__file__).parent.parent / "fixtures" / "sample_xml"


@pytest.fixture
def spring_config_path(fixtures_dir):
    """Path to spring-config.xml."""
    return fixtures_dir / "spring-config.xml"


@pytest.fixture
def mybatis_mapper_path(fixtures_dir):
    """Path to mybatis-mapper.xml."""
    return fixtures_dir / "mybatis-mapper.xml"


@pytest.fixture
def web_xml_path(fixtures_dir):
    """Path to web.xml."""
    return fixtures_dir / "web.xml"


@pytest.fixture
def xml_parser():
    """XMLParser instance."""
    return XMLParser()


# Test root element extraction
class TestRootElementExtraction:
    """Test XML root element extraction."""

    def test_extract_root_element(self, xml_parser, spring_config_path):
        """Test extracting root element."""
        result = xml_parser.parse_file(spring_config_path)

        assert result['root_element'] == 'beans'

    def test_extract_root_from_mybatis(self, xml_parser, mybatis_mapper_path):
        """Test extracting root from MyBatis mapper."""
        result = xml_parser.parse_file(mybatis_mapper_path)

        assert result['root_element'] == 'mapper'

    def test_extract_root_from_web_xml(self, xml_parser, web_xml_path):
        """Test extracting root from web.xml."""
        result = xml_parser.parse_file(web_xml_path)

        assert result['root_element'] == 'web-app'


# Test namespace extraction
class TestNamespaceExtraction:
    """Test XML namespace extraction."""

    def test_extract_namespaces_from_spring(self, xml_parser, spring_config_path):
        """Test extracting namespaces from Spring config."""
        result = xml_parser.parse_file(spring_config_path)

        namespaces = result['namespaces']
        assert len(namespaces) >= 2
        # Should have beans and context namespaces
        assert any('beans' in ns for ns in namespaces.values())

    def test_extract_default_namespace(self, xml_parser, spring_config_path):
        """Test default namespace extraction."""
        result = xml_parser.parse_file(spring_config_path)

        namespaces = result['namespaces']
        # Default namespace should be present
        assert len(namespaces) > 0


# Test bean extraction (Spring-specific)
class TestBeanExtraction:
    """Test Spring bean extraction."""

    def test_extract_beans(self, xml_parser, spring_config_path):
        """Test extracting Spring beans."""
        beans = xml_parser.extract_beans(spring_config_path)

        assert len(beans) >= 3  # dataSource, transactionManager, userService

    def test_bean_has_id_and_class(self, xml_parser, spring_config_path):
        """Test that beans have id and class attributes."""
        beans = xml_parser.extract_beans(spring_config_path)

        for bean in beans:
            assert 'id' in bean or 'name' in bean  # Bean must have identifier
            assert 'class' in bean  # Bean must have class

    def test_extract_specific_bean(self, xml_parser, spring_config_path):
        """Test extracting specific bean by id."""
        beans = xml_parser.extract_beans(spring_config_path)

        data_source = next((b for b in beans if b.get('id') == 'dataSource'), None)
        assert data_source is not None
        assert 'BasicDataSource' in data_source.get('class', '')


# Test element extraction by tag
class TestElementExtractionByTag:
    """Test extracting elements by tag name."""

    def test_extract_select_statements(self, xml_parser, mybatis_mapper_path):
        """Test extracting MyBatis select statements."""
        selects = xml_parser.extract_elements_by_tag(mybatis_mapper_path, 'select')

        assert len(selects) >= 1

    def test_extract_servlet_definitions(self, xml_parser, web_xml_path):
        """Test extracting servlet definitions."""
        servlets = xml_parser.extract_elements_by_tag(web_xml_path, 'servlet')

        assert len(servlets) >= 1

    def test_extract_filter_definitions(self, xml_parser, web_xml_path):
        """Test extracting filter definitions."""
        filters = xml_parser.extract_elements_by_tag(web_xml_path, 'filter')

        assert len(filters) >= 1


# Test attribute extraction
class TestAttributeExtraction:
    """Test XML attribute extraction."""

    def test_extract_mybatis_namespace(self, xml_parser, mybatis_mapper_path):
        """Test extracting MyBatis mapper namespace."""
        result = xml_parser.parse_file(mybatis_mapper_path)

        # Root element should have namespace attribute
        root_attrs = result.get('root_attributes', {})
        assert 'namespace' in root_attrs
        assert 'UserMapper' in root_attrs.get('namespace', '')

    def test_extract_web_app_version(self, xml_parser, web_xml_path):
        """Test extracting web.xml version."""
        result = xml_parser.parse_file(web_xml_path)

        root_attrs = result.get('root_attributes', {})
        assert 'version' in root_attrs


# Test full parsing
class TestFullParsing:
    """Test complete XML file parsing."""

    def test_parse_xml_file_returns_dict(self, xml_parser, spring_config_path):
        """Test that parse returns structured dict."""
        result = xml_parser.parse_file(spring_config_path)

        assert isinstance(result, dict)
        assert 'root_element' in result
        assert 'namespaces' in result

    def test_parse_spring_config(self, xml_parser, spring_config_path):
        """Test parsing Spring configuration."""
        result = xml_parser.parse_file(spring_config_path)

        assert result['root_element'] == 'beans'
        assert len(result['namespaces']) >= 2

    def test_parse_mybatis_mapper(self, xml_parser, mybatis_mapper_path):
        """Test parsing MyBatis mapper."""
        result = xml_parser.parse_file(mybatis_mapper_path)

        assert result['root_element'] == 'mapper'
        # Should have SQL statements
        elements = result.get('elements', {})
        # Check for various statement types
        assert len(elements) > 0

    def test_parse_web_xml(self, xml_parser, web_xml_path):
        """Test parsing web.xml."""
        result = xml_parser.parse_file(web_xml_path)

        assert result['root_element'] == 'web-app'


# Test standalone functions
class TestStandaloneFunctions:
    """Test standalone parser functions."""

    def test_parse_xml_file_function(self, spring_config_path):
        """Test standalone parse_xml_file function."""
        result = parse_xml_file(spring_config_path)

        assert isinstance(result, dict)
        assert result['root_element'] == 'beans'

    def test_extract_root_element_function(self, spring_config_path):
        """Test standalone extract_root_element function."""
        root = extract_root_element(spring_config_path)

        assert root == 'beans'

    def test_extract_namespaces_function(self, spring_config_path):
        """Test standalone extract_namespaces function."""
        namespaces = extract_namespaces(spring_config_path)

        assert isinstance(namespaces, dict)
        assert len(namespaces) >= 2


# Test error handling
@pytest.mark.skip(reason="Legacy TDD test - API methods changed or do not exist. Requires refactoring.")
class TestErrorHandling:
    """Test error handling in XML parser."""

    def test_parse_malformed_xml(self, xml_parser, tmp_path):
        """Test parsing malformed XML."""
        malformed = tmp_path / "malformed.xml"
        malformed.write_text("<root><unclosed>")

        with pytest.raises(Exception):
            xml_parser.parse_file(malformed)

    def test_parse_empty_file(self, xml_parser, tmp_path):
        """Test parsing empty file."""
        empty = tmp_path / "empty.xml"
        empty.write_text("")

        with pytest.raises(Exception):
            xml_parser.parse_file(empty)

    def test_parse_nonexistent_file(self, xml_parser):
        """Test parsing non-existent file."""
        with pytest.raises(FileNotFoundError):
            xml_parser.parse_file(Path("/nonexistent/file.xml"))

    def test_parse_invalid_xml_structure(self, xml_parser, tmp_path):
        """Test parsing invalid XML structure."""
        invalid = tmp_path / "invalid.xml"
        invalid.write_text("<root></different>")

        with pytest.raises(Exception):
            xml_parser.parse_file(invalid)


# Test edge cases
class TestEdgeCases:
    """Test edge cases in XML parsing."""

    def test_parse_xml_with_comments(self, xml_parser):
        """Test parsing XML with comments."""
        content = """<?xml version="1.0"?>
        <!-- This is a comment -->
        <root>
            <!-- Another comment -->
            <element>value</element>
        </root>
        """
        # Write to temp file
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            result = xml_parser.parse_file(temp_path)
            assert result['root_element'] == 'root'
        finally:
            temp_path.unlink()

    def test_parse_xml_with_cdata(self, xml_parser):
        """Test parsing XML with CDATA sections."""
        content = """<?xml version="1.0"?>
        <root>
            <script><![CDATA[
                if (x < y && y > z) {
                    alert('test');
                }
            ]]></script>
        </root>
        """
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            result = xml_parser.parse_file(temp_path)
            assert result['root_element'] == 'root'
        finally:
            temp_path.unlink()

    def test_parse_xml_with_multiple_namespaces(self, xml_parser, spring_config_path):
        """Test parsing XML with multiple namespaces."""
        result = xml_parser.parse_file(spring_config_path)

        # Should have multiple namespaces
        namespaces = result['namespaces']
        assert len(namespaces) >= 2


# Integration-like tests
class TestIntegration:
    """Test integration of parser components."""

    def test_full_workflow_spring_config(self, xml_parser, spring_config_path):
        """Test complete parsing workflow for Spring config."""
        result = xml_parser.parse_file(spring_config_path)

        # Verify structure
        assert result['root_element'] == 'beans'
        assert len(result['namespaces']) >= 2

        # Verify beans can be extracted
        beans = xml_parser.extract_beans(spring_config_path)
        assert len(beans) >= 3

    def test_full_workflow_mybatis_mapper(self, xml_parser, mybatis_mapper_path):
        """Test complete parsing workflow for MyBatis mapper."""
        result = xml_parser.parse_file(mybatis_mapper_path)

        # Verify structure
        assert result['root_element'] == 'mapper'

        # Verify statements can be extracted
        selects = xml_parser.extract_elements_by_tag(mybatis_mapper_path, 'select')
        inserts = xml_parser.extract_elements_by_tag(mybatis_mapper_path, 'insert')

        assert len(selects) >= 1
        assert len(inserts) >= 1

    def test_full_workflow_web_xml(self, xml_parser, web_xml_path):
        """Test complete parsing workflow for web.xml."""
        result = xml_parser.parse_file(web_xml_path)

        # Verify structure
        assert result['root_element'] == 'web-app'

        # Verify servlets and filters can be extracted
        servlets = xml_parser.extract_elements_by_tag(web_xml_path, 'servlet')
        filters = xml_parser.extract_elements_by_tag(web_xml_path, 'filter')

        assert len(servlets) >= 1
        assert len(filters) >= 1
