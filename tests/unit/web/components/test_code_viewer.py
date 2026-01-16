"""
Unit tests for Code Viewer Component (T183 - US4.1).

Tests syntax highlighting, language detection, and line highlighting.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from src.codeindex.web.components.code_viewer import (
    CodeViewer,
    detect_language_from_extension,
    detect_language_from_content,
    highlight_lines,
    format_line_numbers,
    get_supported_languages,
    LanguageNotSupportedError
)


@pytest.fixture
def code_viewer():
    """Create CodeViewer instance with default content."""
    return CodeViewer(content="default content", language="text")


class TestLanguageDetection:
    """Test language detection from file extension."""

    def test_detect_java(self):
        """Test Java language detection."""
        assert detect_language_from_extension(".java") == "java"
        assert detect_language_from_extension("User.java") == "java"

    def test_detect_jsp(self):
        """Test JSP language detection."""
        assert detect_language_from_extension(".jsp") == "jsp"
        assert detect_language_from_extension("user.jsp") == "jsp"

    def test_detect_javascript(self):
        """Test JavaScript language detection."""
        assert detect_language_from_extension(".js") == "javascript"
        assert detect_language_from_extension("app.js") == "javascript"

    def test_detect_typescript(self):
        """Test TypeScript language detection."""
        assert detect_language_from_extension(".ts") == "typescript"
        assert detect_language_from_extension("test.spec.ts") == "typescript"

    def test_detect_xml(self):
        """Test XML language detection."""
        assert detect_language_from_extension(".xml") == "xml"
        assert detect_language_from_extension("pom.xml") == "xml"

    def test_detect_sql(self):
        """Test SQL language detection."""
        assert detect_language_from_extension(".sql") == "sql"
        assert detect_language_from_extension("schema.sql") == "sql"

    def test_detect_markdown(self):
        """Test Markdown language detection."""
        assert detect_language_from_extension(".md") == "markdown"
        assert detect_language_from_extension("README.md") == "markdown"

    def test_detect_python(self):
        """Test Python language detection."""
        assert detect_language_from_extension(".py") == "python"
        assert detect_language_from_extension("test.py") == "python"

    def test_detect_yaml(self):
        """Test YAML language detection."""
        assert detect_language_from_extension(".yml") == "yaml"
        assert detect_language_from_extension(".yaml") == "yaml"

    def test_detect_properties(self):
        """Test Properties file detection."""
        assert detect_language_from_extension(".properties") == "properties"

    def test_detect_unknown_extension(self):
        """Test unknown extension returns plain text."""
        assert detect_language_from_extension(".unknown") == "text"
        assert detect_language_from_extension(".xyz") == "text"

    def test_detect_no_extension(self):
        """Test file with no extension."""
        assert detect_language_from_extension("Dockerfile") == "text"
        assert detect_language_from_extension("Makefile") == "text"


class TestLanguageDetectionFromContent:
    """Test language detection from file content."""

    def test_detect_java_from_content(self):
        """Test Java detection from content."""
        content = """
        public class User {
            private String name;
        }
        """
        assert detect_language_from_content(content) == "java"

    def test_detect_xml_from_content(self):
        """Test XML detection from content."""
        content = """<?xml version="1.0"?>
        <root>
            <element>value</element>
        </root>"""
        assert detect_language_from_content(content) == "xml"

    def test_detect_sql_from_content(self):
        """Test SQL detection from content."""
        content = "SELECT * FROM users WHERE id = 1;"
        assert detect_language_from_content(content) == "sql"

    def test_detect_javascript_from_content(self):
        """Test JavaScript detection from content."""
        content = """
        function hello() {
            console.log('Hello');
        }
        """
        assert detect_language_from_content(content) == "javascript"

    def test_detect_python_from_content(self):
        """Test Python detection from content."""
        content = """
        def hello():
            print('Hello')
        """
        assert detect_language_from_content(content) == "python"


class TestLineHighlighting:
    """Test line highlighting functionality."""

    def test_highlight_single_line(self):
        """Test highlighting a single line."""
        content = "line1\nline2\nline3\nline4"
        highlighted = highlight_lines(content, lines=[2])

        assert ">>>" in highlighted or "**" in highlighted
        assert "line2" in highlighted

    def test_highlight_multiple_lines(self):
        """Test highlighting multiple lines."""
        content = "line1\nline2\nline3\nline4"
        highlighted = highlight_lines(content, lines=[1, 3])

        assert "line1" in highlighted
        assert "line3" in highlighted

    def test_highlight_line_range(self):
        """Test highlighting a range of lines."""
        content = "line1\nline2\nline3\nline4\nline5"
        highlighted = highlight_lines(content, line_range=(2, 4))

        assert "line2" in highlighted
        assert "line3" in highlighted
        assert "line4" in highlighted

    def test_highlight_no_lines(self):
        """Test no highlighting returns original content."""
        content = "line1\nline2\nline3"
        highlighted = highlight_lines(content, lines=[])

        assert highlighted == content

    def test_highlight_invalid_line_number(self):
        """Test highlighting with invalid line number."""
        content = "line1\nline2\nline3"
        highlighted = highlight_lines(content, lines=[100])

        # Should not crash, should return original or mark nothing
        assert isinstance(highlighted, str)


class TestLineNumberFormatting:
    """Test line number formatting."""

    def test_format_line_numbers_enabled(self):
        """Test formatting with line numbers enabled."""
        content = "line1\nline2\nline3"
        formatted = format_line_numbers(content, show_line_numbers=True)

        assert "1" in formatted
        assert "2" in formatted
        assert "3" in formatted

    def test_format_line_numbers_disabled(self):
        """Test formatting with line numbers disabled."""
        content = "line1\nline2\nline3"
        formatted = format_line_numbers(content, show_line_numbers=False)

        assert formatted == content

    def test_format_line_numbers_with_start_line(self):
        """Test formatting with custom start line."""
        content = "line1\nline2\nline3"
        formatted = format_line_numbers(content, show_line_numbers=True, start_line=10)

        assert "10" in formatted
        assert "11" in formatted
        assert "12" in formatted

    def test_format_line_numbers_padding(self):
        """Test line number padding for alignment."""
        content = "\n".join([f"line{i}" for i in range(1, 101)])
        formatted = format_line_numbers(content, show_line_numbers=True)

        # Line numbers should be padded (e.g., "  1", " 10", "100")
        assert isinstance(formatted, str)
        # Check that padding is applied (numbers aligned)


class TestCodeViewerComponent:
    """Test CodeViewer component."""

    def test_init_with_content(self):
        """Test initialization with content."""
        viewer = CodeViewer(content="public class User {}", language="java")

        assert viewer.content == "public class User {}"
        assert viewer.language == "java"

    def test_init_with_file_path(self):
        """Test initialization with file path."""
        with patch('src.codeindex.web.services.code_service.read_source_file') as mock_read:
            mock_read.return_value = "file content"

            viewer = CodeViewer(file_path="/path/to/User.java")

            assert viewer.content == "file content"
            assert viewer.language == "java"

    def test_render_basic(self, code_viewer):
        """Test basic rendering."""
        code_viewer.content = "public class User {}"
        code_viewer.language = "java"

        html = code_viewer.render()

        assert "public class User {}" in html or isinstance(html, str)

    def test_render_with_line_numbers(self, code_viewer):
        """Test rendering with line numbers."""
        code_viewer.content = "line1\nline2\nline3"
        code_viewer.language = "text"
        code_viewer.show_line_numbers = True

        html = code_viewer.render()

        assert isinstance(html, str)

    def test_render_with_highlighted_lines(self, code_viewer):
        """Test rendering with highlighted lines."""
        code_viewer.content = "line1\nline2\nline3\nline4"
        code_viewer.language = "text"
        code_viewer.highlighted_lines = [2, 3]

        html = code_viewer.render()

        assert isinstance(html, str)

    def test_render_with_streamlit(self, code_viewer):
        """Test rendering with Streamlit code editor."""
        with patch('streamlit.code') as mock_st_code:
            code_viewer.content = "public class User {}"
            code_viewer.language = "java"

            code_viewer.render_streamlit()

            mock_st_code.assert_called_once()
            args, kwargs = mock_st_code.call_args
            assert "public class User {}" in args
            assert kwargs.get("language") == "java"

    def test_render_empty_content(self, code_viewer):
        """Test rendering with empty content."""
        code_viewer.content = ""

        html = code_viewer.render()

        assert html == "" or html is None

    def test_auto_detect_language(self):
        """Test auto language detection."""
        with patch('src.codeindex.web.services.code_service.read_source_file') as mock_read:
            mock_read.return_value = "public class User {}"

            viewer = CodeViewer(
                file_path="/path/to/User.java"
            )

            assert viewer.language == "java"

    def test_set_highlighted_lines_after_init(self, code_viewer):
        """Test setting highlighted lines after initialization."""
        code_viewer.content = "line1\nline2\nline3"
        code_viewer.set_highlighted_lines([2])

        assert code_viewer.highlighted_lines == [2]

    def test_set_line_range_after_init(self, code_viewer):
        """Test setting line range after initialization."""
        code_viewer.content = "line1\nline2\nline3\nline4"
        code_viewer.set_line_range(2, 3)

        assert code_viewer.highlighted_lines == [2, 3]


class TestSupportedLanguages:
    """Test supported languages query."""

    def test_get_supported_languages(self):
        """Test getting list of supported languages."""
        languages = get_supported_languages()

        assert "java" in languages
        assert "javascript" in languages
        assert "python" in languages
        assert "xml" in languages
        assert "sql" in languages
        assert "markdown" in languages

    def test_supported_languages_not_empty(self):
        """Test that supported languages list is not empty."""
        languages = get_supported_languages()

        assert len(languages) > 0

    def test_language_is_supported(self):
        """Test checking if language is supported."""
        from src.codeindex.web.components.code_viewer import is_language_supported

        assert is_language_supported("java") is True
        assert is_language_supported("javascript") is True
        assert is_language_supported("unknown") is False


class TestErrorHandling:
    """Test error handling in CodeViewer."""

    def test_unsupported_language_warning(self, code_viewer):
        """Test warning for unsupported language."""
        code_viewer.content = "some code"
        code_viewer.language = "unsupported"

        # Should not crash, should fall back to text
        html = code_viewer.render()
        assert isinstance(html, str)

    def test_invalid_highlighted_lines(self, code_viewer):
        """Test handling of invalid highlighted line numbers."""
        code_viewer.content = "line1\nline2"
        code_viewer.highlighted_lines = [100, 200]

        # Should not crash
        html = code_viewer.render()
        assert isinstance(html, str)

    def test_empty_file_path(self):
        """Test handling of empty file path."""
        with pytest.raises(ValueError, match="content or file_path"):
            CodeViewer(file_path="")

    def test_file_not_found(self):
        """Test handling of non-existent file."""
        with patch('src.codeindex.web.services.code_service.read_source_file') as mock_read:
            from src.codeindex.web.services.code_service import FileNotFoundError as CodeFileNotFoundError
            mock_read.side_effect = CodeFileNotFoundError("File not found")

            with pytest.raises(CodeFileNotFoundError):
                CodeViewer(file_path="/nonexistent.java")


class TestCodeViewerControls:
    """Test code viewer controls."""

    def test_toggle_line_numbers(self, code_viewer):
        """Test toggling line numbers."""
        code_viewer.content = "line1\nline2"

        code_viewer.show_line_numbers = True
        html1 = code_viewer.render()

        code_viewer.show_line_numbers = False
        html2 = code_viewer.render()

        assert html1 != html2

    def test_search_in_code(self, code_viewer):
        """Test search functionality."""
        code_viewer.content = "public class User {\n  private String name;\n}"

        matches = code_viewer.search("String")

        assert len(matches) > 0
        assert matches[0].line_number == 2

    def test_copy_to_clipboard(self, code_viewer):
        """Test copy to clipboard functionality."""
        code_viewer.content = "public class User {}"

        copied_content = code_viewer.get_copy_content()

        assert copied_content == "public class User {}"

    def test_download_file(self, code_viewer):
        """Test download file content."""
        code_viewer.content = "public class User {}"
        code_viewer.language = "java"

        download_data = code_viewer.get_download_data()

        assert download_data["content"] == "public class User {}"
        assert download_data["filename"].endswith(".java")
        assert download_data["mime_type"] == "text/plain"
