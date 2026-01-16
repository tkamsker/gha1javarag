"""
Code Viewer Component (T188, T189 - US4.1).

Provides syntax-highlighted code viewing with line numbers, search, and controls.
"""

import logging
import re
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


# Custom exceptions
class LanguageNotSupportedError(Exception):
    """Language not supported error."""
    pass


# Supported languages mapping (extension -> language name)
LANGUAGE_MAP = {
    ".java": "java",
    ".jsp": "jsp",
    ".js": "javascript",
    ".ts": "typescript",
    ".xml": "xml",
    ".sql": "sql",
    ".md": "markdown",
    ".py": "python",
    ".yml": "yaml",
    ".yaml": "yaml",
    ".properties": "properties",
    ".json": "json",
    ".html": "html",
    ".css": "css",
    ".sh": "bash",
    ".txt": "text"
}


@dataclass
class SearchMatch:
    """Search match result."""
    line_number: int
    line_content: str
    match_start: int
    match_end: int


class CodeViewer:
    """
    Code viewer component with syntax highlighting and controls.

    Features:
    - Syntax highlighting for multiple languages
    - Line numbers with custom start line
    - Line highlighting for specific lines or ranges
    - Search within code
    - Copy to clipboard support
    - Download file support
    """

    def __init__(
        self,
        content: Optional[str] = None,
        file_path: Optional[str] = None,
        language: Optional[str] = None,
        show_line_numbers: bool = True,
        highlighted_lines: Optional[List[int]] = None
    ):
        """
        Initialize code viewer.

        Args:
            content: Code content to display
            file_path: Path to source file (will load content)
            language: Language for syntax highlighting (auto-detected if not provided)
            show_line_numbers: Show line numbers (default: True)
            highlighted_lines: List of line numbers to highlight
        """
        if content is None and not file_path:
            raise ValueError("Either content or file_path must be provided")

        if file_path:
            from src.codeindex.web.services.code_service import read_source_file
            self.content = read_source_file(Path(file_path))
            self.file_path = file_path
        else:
            self.content = content if content is not None else ""
            self.file_path = file_path

        # Auto-detect language if not provided
        if language:
            self.language = language
        elif file_path:
            self.language = detect_language_from_extension(file_path)
        else:
            self.language = detect_language_from_content(content)

        self.show_line_numbers = show_line_numbers
        self.highlighted_lines = highlighted_lines or []

        logger.debug(f"CodeViewer initialized: language={self.language}, lines={len(self.content.splitlines())}")

    def render(self) -> str:
        """
        Render code viewer as HTML.

        Returns:
            HTML string with syntax-highlighted code
        """
        if not self.content:
            return ""

        content = self.content

        # Apply line highlighting
        if self.highlighted_lines:
            content = highlight_lines(content, lines=self.highlighted_lines)

        # Apply line numbers
        if self.show_line_numbers:
            content = format_line_numbers(content, show_line_numbers=True)

        return content

    def render_streamlit(self):
        """
        Render code viewer using Streamlit code component.

        This method uses Streamlit's native code display with syntax highlighting.
        """
        import streamlit as st

        if not self.content:
            st.info("No content to display")
            return

        # Streamlit code component with syntax highlighting
        st.code(
            self.content,
            language=self.language if self.language != "text" else None,
            line_numbers=self.show_line_numbers
        )

    def set_highlighted_lines(self, lines: List[int]):
        """
        Set lines to highlight.

        Args:
            lines: List of line numbers (1-indexed)
        """
        self.highlighted_lines = lines

    def set_line_range(self, start: int, end: int):
        """
        Set range of lines to highlight.

        Args:
            start: Start line number (1-indexed, inclusive)
            end: End line number (1-indexed, inclusive)
        """
        self.highlighted_lines = list(range(start, end + 1))

    def search(self, query: str, case_sensitive: bool = False) -> List[SearchMatch]:
        """
        Search for text in code content.

        Args:
            query: Search query
            case_sensitive: Case-sensitive search (default: False)

        Returns:
            List of search matches with line numbers
        """
        if not query:
            return []

        matches = []
        flags = 0 if case_sensitive else re.IGNORECASE

        for line_num, line_content in enumerate(self.content.splitlines(), 1):
            for match in re.finditer(re.escape(query), line_content, flags):
                matches.append(SearchMatch(
                    line_number=line_num,
                    line_content=line_content,
                    match_start=match.start(),
                    match_end=match.end()
                ))

        return matches

    def get_copy_content(self) -> str:
        """
        Get content for copying to clipboard.

        Returns:
            Code content as plain text
        """
        return self.content

    def get_download_data(self) -> Dict[str, Any]:
        """
        Get data for downloading file.

        Returns:
            Dictionary with content, filename, and mime type
        """
        # Determine filename
        if self.file_path:
            # Use original filename from file_path
            filename = Path(self.file_path).name
        else:
            # Generate filename based on language
            ext = _get_extension_for_language(self.language)
            filename = f"code{ext}"

        return {
            "content": self.content,
            "filename": filename,
            "mime_type": "text/plain"
        }


def detect_language_from_extension(file_path: str) -> str:
    """
    Detect language from file extension.

    Args:
        file_path: File path or extension

    Returns:
        Language name (e.g., "java", "javascript", "python")
    """
    # Extract extension
    if file_path.startswith("."):
        ext = file_path
    else:
        ext = Path(file_path).suffix

    # Normalize to lowercase
    ext = ext.lower()

    # Look up in language map
    language = LANGUAGE_MAP.get(ext, "text")

    logger.debug(f"Detected language '{language}' from extension '{ext}'")
    return language


def detect_language_from_content(content: str) -> str:
    """
    Detect language from file content using heuristics.

    Args:
        content: File content

    Returns:
        Language name or "text" if unable to detect
    """
    if not content:
        return "text"

    content_lower = content.lower()

    # Java detection
    if "public class" in content_lower or "private class" in content_lower:
        return "java"

    # XML detection
    if content.strip().startswith("<?xml") or ("<" in content and ">" in content and "/" in content):
        return "xml"

    # SQL detection
    if any(keyword in content_lower for keyword in ["select ", "insert ", "update ", "delete ", "create table"]):
        return "sql"

    # JavaScript detection
    if any(keyword in content for keyword in ["function ", "const ", "let ", "console.log"]):
        return "javascript"

    # Python detection
    if any(keyword in content for keyword in ["def ", "import ", "print("]):
        return "python"

    # Default to text
    return "text"


def highlight_lines(content: str, lines: Optional[List[int]] = None, line_range: Optional[Tuple[int, int]] = None) -> str:
    """
    Highlight specific lines in content.

    Args:
        content: Code content
        lines: List of line numbers to highlight (1-indexed)
        line_range: Tuple of (start, end) line numbers to highlight

    Returns:
        Content with highlighted lines marked
    """
    if not lines and not line_range:
        return content

    # Build set of lines to highlight
    lines_to_highlight = set()

    if lines:
        lines_to_highlight.update(lines)

    if line_range:
        start, end = line_range
        lines_to_highlight.update(range(start, end + 1))

    # Process content line by line
    highlighted_lines = []
    for line_num, line_content in enumerate(content.splitlines(), 1):
        if line_num in lines_to_highlight:
            # Mark highlighted line with >>> prefix
            highlighted_lines.append(f">>> {line_content}")
        else:
            highlighted_lines.append(f"    {line_content}")

    return "\n".join(highlighted_lines)


def format_line_numbers(
    content: str,
    show_line_numbers: bool = True,
    start_line: int = 1
) -> str:
    """
    Format content with line numbers.

    Args:
        content: Code content
        show_line_numbers: Show line numbers (default: True)
        start_line: Starting line number (default: 1)

    Returns:
        Content with line numbers
    """
    if not show_line_numbers:
        return content

    lines = content.splitlines()
    total_lines = len(lines)

    # Calculate padding for line numbers
    max_line_num = start_line + total_lines - 1
    padding = len(str(max_line_num))

    # Format each line with line number
    formatted_lines = []
    for i, line_content in enumerate(lines):
        line_num = start_line + i
        formatted_lines.append(f"{line_num:>{padding}} | {line_content}")

    return "\n".join(formatted_lines)


def get_supported_languages() -> List[str]:
    """
    Get list of supported languages.

    Returns:
        List of language names
    """
    return sorted(set(LANGUAGE_MAP.values()))


def is_language_supported(language: str) -> bool:
    """
    Check if language is supported.

    Args:
        language: Language name

    Returns:
        True if supported, False otherwise
    """
    return language.lower() in [lang.lower() for lang in LANGUAGE_MAP.values()]


def _get_extension_for_language(language: str) -> str:
    """
    Get file extension for language.

    Args:
        language: Language name

    Returns:
        File extension with leading dot
    """
    # Reverse lookup in LANGUAGE_MAP
    for ext, lang in LANGUAGE_MAP.items():
        if lang == language:
            return ext

    return ".txt"


__all__ = [
    "CodeViewer",
    "detect_language_from_extension",
    "detect_language_from_content",
    "highlight_lines",
    "format_line_numbers",
    "get_supported_languages",
    "is_language_supported",
    "LanguageNotSupportedError",
    "SearchMatch"
]
