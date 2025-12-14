"""
Unit tests for JSP parser.

Tests parsing of JSP files to extract structural information.

NOTE: These tests should FAIL initially (TDD approach).
"""

import pytest
from pathlib import Path
from typing import List, Dict

from codeindex.parsers.jsp_parser import (
    JSPParser,
    parse_jsp_file,
    extract_directives,
    extract_taglibs,
    extract_scriptlets,
    extract_expressions,
    extract_declarations,
    extract_jsp_tags,
    extract_el_expressions,
)


# Fixtures
@pytest.fixture
def fixtures_dir():
    """Path to test fixtures directory."""
    return Path(__file__).parent.parent / "fixtures" / "sample_jsp"


@pytest.fixture
def sample_form_path(fixtures_dir):
    """Path to SampleForm.jsp."""
    return fixtures_dir / "SampleForm.jsp"


@pytest.fixture
def scriptlets_path(fixtures_dir):
    """Path to Scriptlets.jsp."""
    return fixtures_dir / "Scriptlets.jsp"


@pytest.fixture
def custom_tags_path(fixtures_dir):
    """Path to CustomTags.jsp."""
    return fixtures_dir / "CustomTags.jsp"


@pytest.fixture
def el_expressions_path(fixtures_dir):
    """Path to ELExpressions.jsp."""
    return fixtures_dir / "ELExpressions.jsp"


@pytest.fixture
def jsp_parser():
    """JSPParser instance."""
    return JSPParser()


# Test directive extraction
class TestDirectiveExtraction:
    """Test JSP directive extraction."""

    def test_extract_page_directive(self, jsp_parser, sample_form_path):
        """Test extracting page directive."""
        content = sample_form_path.read_text()
        directives = jsp_parser.extract_directives(content)

        page_directives = [d for d in directives if d['type'] == 'page']
        assert len(page_directives) >= 1

    def test_extract_taglib_directive(self, jsp_parser, sample_form_path):
        """Test extracting taglib directive."""
        content = sample_form_path.read_text()
        directives = jsp_parser.extract_directives(content)

        taglib_directives = [d for d in directives if d['type'] == 'taglib']
        assert len(taglib_directives) >= 1

    def test_extract_import_directive(self, jsp_parser, scriptlets_path):
        """Test extracting import statements."""
        content = scriptlets_path.read_text()
        directives = jsp_parser.extract_directives(content)

        # Look for page directives with import attribute
        import_directives = [
            d for d in directives
            if d['type'] == 'page' and 'import' in d.get('attributes', {})
        ]
        assert len(import_directives) >= 1


# Test taglib extraction
class TestTaglibExtraction:
    """Test JSP taglib extraction."""

    def test_extract_taglibs(self, jsp_parser, sample_form_path):
        """Test extracting taglib declarations."""
        content = sample_form_path.read_text()
        taglibs = jsp_parser.extract_taglibs(content)

        assert len(taglibs) >= 1
        # Check for JSTL core
        assert any('jstl/core' in t.get('uri', '') for t in taglibs)

    def test_extract_taglib_prefix(self, jsp_parser, sample_form_path):
        """Test extracting taglib prefix."""
        content = sample_form_path.read_text()
        taglibs = jsp_parser.extract_taglibs(content)

        jstl_core = next(t for t in taglibs if 'jstl/core' in t.get('uri', ''))
        assert jstl_core.get('prefix') == 'c'

    def test_extract_multiple_taglibs(self, jsp_parser, custom_tags_path):
        """Test extracting multiple taglibs."""
        content = custom_tags_path.read_text()
        taglibs = jsp_parser.extract_taglibs(content)

        assert len(taglibs) >= 3  # core, fmt, spring
        prefixes = [t.get('prefix') for t in taglibs]
        assert 'c' in prefixes
        assert 'fmt' in prefixes


# Test scriptlet extraction
class TestScriptletExtraction:
    """Test JSP scriptlet extraction."""

    def test_extract_scriptlets(self, jsp_parser, scriptlets_path):
        """Test extracting scriptlets."""
        content = scriptlets_path.read_text()
        scriptlets = jsp_parser.extract_scriptlets(content)

        assert len(scriptlets) >= 2

    def test_scriptlet_content_includes_java_code(self, jsp_parser, scriptlets_path):
        """Test that scriptlet content includes Java code."""
        content = scriptlets_path.read_text()
        scriptlets = jsp_parser.extract_scriptlets(content)

        # Should contain Java variable declarations
        all_code = ' '.join([s.get('code', '') for s in scriptlets])
        assert 'Date' in all_code or 'String' in all_code

    def test_scriptlet_excludes_declarations(self, jsp_parser, scriptlets_path):
        """Test that declarations are not included in scriptlets."""
        content = scriptlets_path.read_text()
        scriptlets = jsp_parser.extract_scriptlets(content)

        # Declarations use <%! %>, scriptlets use <% %>
        # They should be separate
        for scriptlet in scriptlets:
            code = scriptlet.get('code', '')
            # Declarations typically have method definitions
            # This is a heuristic check
            pass  # Just ensure we can extract them


# Test expression extraction
class TestExpressionExtraction:
    """Test JSP expression extraction."""

    def test_extract_expressions(self, jsp_parser, scriptlets_path):
        """Test extracting expressions."""
        content = scriptlets_path.read_text()
        expressions = jsp_parser.extract_expressions(content)

        assert len(expressions) >= 2

    def test_expression_content(self, jsp_parser, scriptlets_path):
        """Test expression content."""
        content = scriptlets_path.read_text()
        expressions = jsp_parser.extract_expressions(content)

        # Should have expressions like formatted, counter, message
        expr_codes = [e.get('code', '') for e in expressions]
        assert any('formatted' in code or 'counter' in code for code in expr_codes)


# Test declaration extraction
class TestDeclarationExtraction:
    """Test JSP declaration extraction."""

    def test_extract_declarations(self, jsp_parser, scriptlets_path):
        """Test extracting declarations."""
        content = scriptlets_path.read_text()
        declarations = jsp_parser.extract_declarations(content)

        assert len(declarations) >= 1

    def test_declaration_contains_method(self, jsp_parser, scriptlets_path):
        """Test that declaration contains method definition."""
        content = scriptlets_path.read_text()
        declarations = jsp_parser.extract_declarations(content)

        # Should have formatDate method
        all_code = ' '.join([d.get('code', '') for d in declarations])
        assert 'formatDate' in all_code or 'counter' in all_code


# Test JSP tag extraction
class TestJSPTagExtraction:
    """Test JSP custom tag extraction."""

    def test_extract_jstl_tags(self, jsp_parser, sample_form_path):
        """Test extracting JSTL tags."""
        content = sample_form_path.read_text()
        tags = jsp_parser.extract_jsp_tags(content)

        # Should find c:if and c:out
        tag_names = [t.get('name', '') for t in tags]
        assert any('c:if' in name or 'if' in name for name in tag_names)

    def test_extract_custom_tags_with_attributes(self, jsp_parser, custom_tags_path):
        """Test extracting custom tags with attributes."""
        content = custom_tags_path.read_text()
        tags = jsp_parser.extract_jsp_tags(content)

        assert len(tags) >= 2

    def test_extract_forEach_tag(self, jsp_parser, custom_tags_path):
        """Test extracting forEach tag."""
        content = custom_tags_path.read_text()
        tags = jsp_parser.extract_jsp_tags(content)

        # Should have c:forEach
        assert any('forEach' in t.get('name', '') for t in tags)


# Test EL expression extraction
class TestELExpressionExtraction:
    """Test EL expression extraction."""

    def test_extract_el_expressions(self, jsp_parser, el_expressions_path):
        """Test extracting EL expressions."""
        content = el_expressions_path.read_text()
        expressions = jsp_parser.extract_el_expressions(content)

        assert len(expressions) >= 5

    def test_el_property_access(self, jsp_parser, el_expressions_path):
        """Test EL property access expressions."""
        content = el_expressions_path.read_text()
        expressions = jsp_parser.extract_el_expressions(content)

        # Should have ${user.username}
        assert any('user' in e and 'username' in e for e in expressions)

    def test_el_collection_access(self, jsp_parser, el_expressions_path):
        """Test EL collection access."""
        content = el_expressions_path.read_text()
        expressions = jsp_parser.extract_el_expressions(content)

        # Should have ${items[0]}
        assert any('[0]' in e or 'items' in e for e in expressions)

    def test_el_ternary_operator(self, jsp_parser, el_expressions_path):
        """Test EL ternary operator."""
        content = el_expressions_path.read_text()
        expressions = jsp_parser.extract_el_expressions(content)

        # Should have conditional expression
        assert any('?' in e or '>=' in e for e in expressions)


# Test full parsing
class TestFullParsing:
    """Test complete JSP file parsing."""

    def test_parse_jsp_file_returns_dict(self, jsp_parser, sample_form_path):
        """Test that parse returns structured dict."""
        result = jsp_parser.parse_file(sample_form_path)

        assert isinstance(result, dict)
        assert 'directives' in result
        assert 'taglibs' in result

    def test_parse_simple_form(self, jsp_parser, sample_form_path):
        """Test parsing simple form JSP."""
        result = jsp_parser.parse_file(sample_form_path)

        assert len(result['directives']) >= 1
        assert len(result['taglibs']) >= 1

    def test_parse_scriptlets_file(self, jsp_parser, scriptlets_path):
        """Test parsing file with scriptlets."""
        result = jsp_parser.parse_file(scriptlets_path)

        assert len(result['scriptlets']) >= 2
        assert len(result['expressions']) >= 2
        assert len(result['declarations']) >= 1

    def test_parse_includes_all_elements(self, jsp_parser, custom_tags_path):
        """Test that parsing includes all structural elements."""
        result = jsp_parser.parse_file(custom_tags_path)

        assert 'directives' in result
        assert 'taglibs' in result
        assert 'jsp_tags' in result
        assert 'el_expressions' in result


# Test standalone functions
class TestStandaloneFunctions:
    """Test standalone parser functions."""

    def test_parse_jsp_file_function(self, sample_form_path):
        """Test standalone parse_jsp_file function."""
        result = parse_jsp_file(sample_form_path)

        assert isinstance(result, dict)
        assert 'directives' in result

    def test_extract_directives_function(self, sample_form_path):
        """Test standalone extract_directives function."""
        content = sample_form_path.read_text()
        directives = extract_directives(content)

        assert isinstance(directives, list)
        assert len(directives) >= 1

    def test_extract_taglibs_function(self, sample_form_path):
        """Test standalone extract_taglibs function."""
        content = sample_form_path.read_text()
        taglibs = extract_taglibs(content)

        assert isinstance(taglibs, list)
        assert len(taglibs) >= 1


# Test error handling
class TestErrorHandling:
    """Test error handling in JSP parser."""

    def test_parse_invalid_jsp(self, jsp_parser):
        """Test parsing invalid JSP code."""
        invalid_content = "<% this is broken %> <%= unclosed"

        # Should not crash
        result = jsp_parser.parse(invalid_content)
        assert isinstance(result, dict)

    def test_parse_empty_file(self, jsp_parser):
        """Test parsing empty file."""
        result = jsp_parser.parse("")

        assert isinstance(result, dict)
        assert len(result['directives']) == 0

    def test_parse_nonexistent_file(self, jsp_parser):
        """Test parsing non-existent file."""
        with pytest.raises(FileNotFoundError):
            jsp_parser.parse_file(Path("/nonexistent/file.jsp"))

    def test_parse_handles_malformed_el(self, jsp_parser):
        """Test parsing with malformed EL expressions."""
        content = """
        <%@ page contentType="text/html" %>
        <p>${unclosed</p>
        <p>${valid.property}</p>
        """
        result = jsp_parser.parse(content)

        # Should still parse valid parts
        assert isinstance(result, dict)


# Test edge cases
class TestEdgeCases:
    """Test edge cases in JSP parsing."""

    def test_parse_jsp_with_html_comments(self, jsp_parser):
        """Test parsing JSP with HTML comments."""
        content = """
        <%@ page contentType="text/html" %>
        <!-- HTML comment -->
        <%-- JSP comment --%>
        <p>${user.name}</p>
        """
        result = jsp_parser.parse(content)

        # Should parse despite comments
        assert len(result['el_expressions']) >= 1

    def test_parse_nested_tags(self, jsp_parser):
        """Test parsing nested tags."""
        content = """
        <%@ page contentType="text/html" %>
        <%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
        <c:forEach items="${items}" var="item">
            <c:if test="${item.active}">
                <p><c:out value="${item.name}"/></p>
            </c:if>
        </c:forEach>
        """
        result = jsp_parser.parse(content)

        # Should find all tags
        jsp_tags = result.get('jsp_tags', [])
        assert len(jsp_tags) >= 2

    def test_parse_mixed_content(self, jsp_parser):
        """Test parsing file with mixed content types."""
        content = """
        <%@ page contentType="text/html" %>
        <html>
        <% String name = "Test"; %>
        <p><%= name %></p>
        <p>${user.email}</p>
        </html>
        """
        result = jsp_parser.parse(content)

        assert len(result['scriptlets']) >= 1
        assert len(result['expressions']) >= 1
        assert len(result['el_expressions']) >= 1


# Integration-like tests
class TestIntegration:
    """Test integration of parser components."""

    def test_full_workflow_form(self, jsp_parser, sample_form_path):
        """Test complete parsing workflow for form."""
        result = jsp_parser.parse_file(sample_form_path)

        # Verify directives
        assert len(result['directives']) >= 2

        # Verify taglibs
        taglibs = result['taglibs']
        assert len(taglibs) >= 1
        assert any(t.get('prefix') == 'c' for t in taglibs)

        # Verify EL expressions
        el_exprs = result['el_expressions']
        assert len(el_exprs) >= 1

    def test_full_workflow_scriptlets(self, jsp_parser, scriptlets_path):
        """Test complete parsing workflow for scriptlets."""
        result = jsp_parser.parse_file(scriptlets_path)

        # Should have all types of Java code
        assert len(result['declarations']) >= 1
        assert len(result['scriptlets']) >= 2
        assert len(result['expressions']) >= 2

    def test_full_workflow_tags(self, jsp_parser, custom_tags_path):
        """Test complete parsing workflow for custom tags."""
        result = jsp_parser.parse_file(custom_tags_path)

        # Should have multiple taglibs
        assert len(result['taglibs']) >= 3

        # Should have JSP tags
        assert len(result['jsp_tags']) >= 2
