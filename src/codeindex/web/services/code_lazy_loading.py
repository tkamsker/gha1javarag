"""
Code Lazy Loading Service (T193 - US4.1).

Provides lazy loading functionality for large files to improve performance.
"""

import logging
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass
import hashlib

logger = logging.getLogger(__name__)


# Custom exceptions
class LazyLoadingError(Exception):
    """Lazy loading error."""
    pass


@dataclass
class CodeChunk:
    """
    Represents a chunk of code lines.

    Attributes:
        start_line: Starting line number (1-indexed)
        end_line: Ending line number (1-indexed, inclusive)
        lines: List of code lines
        total_lines: Total lines in file
    """
    start_line: int
    end_line: int
    lines: List[str]
    total_lines: int

    def is_first(self) -> bool:
        """Check if this is the first chunk."""
        return self.start_line == 1

    def is_last(self) -> bool:
        """Check if this is the last chunk."""
        return self.end_line >= self.total_lines

    def has_next(self) -> bool:
        """Check if there is a next chunk."""
        return not self.is_last()

    def has_previous(self) -> bool:
        """Check if there is a previous chunk."""
        return not self.is_first()


class LazyCodeLoader:
    """
    Lazy loader for large code files.

    Features:
    - Load files in chunks to reduce memory usage
    - Cache loaded chunks for performance
    - Calculate visible lines for viewport
    - Support for smooth scrolling with buffer
    """

    def __init__(self, chunk_size: int = 1000, enable_cache: bool = True):
        """
        Initialize lazy code loader.

        Args:
            chunk_size: Number of lines per chunk (default: 1000)
            enable_cache: Enable chunk caching (default: True)
        """
        self.chunk_size = chunk_size
        self.enable_cache = enable_cache
        self._cache: Dict[str, CodeChunk] = {}

        logger.debug(f"LazyCodeLoader initialized: chunk_size={chunk_size}, cache={enable_cache}")

    def load_chunk(
        self,
        content: str,
        chunk_index: int,
        file_path: Optional[Path] = None
    ) -> Optional[CodeChunk]:
        """
        Load a specific chunk of code.

        Args:
            content: Full file content
            chunk_index: Chunk index (0-based)
            file_path: Optional file path for cache key

        Returns:
            CodeChunk or None if out of bounds
        """
        if chunk_index < 0:
            logger.warning(f"Invalid chunk index: {chunk_index}")
            return None

        if not content:
            return None

        # Check cache
        if self.enable_cache:
            cache_key = self._get_cache_key(content, chunk_index, file_path)
            if cache_key in self._cache:
                logger.debug(f"Cache hit for chunk {chunk_index}")
                return self._cache[cache_key]

        # Split content into lines
        lines = content.splitlines()
        total_lines = len(lines)

        # Calculate boundaries
        start_line, end_line = calculate_chunk_boundaries(
            chunk_index=chunk_index,
            chunk_size=self.chunk_size,
            total_lines=total_lines
        )

        # Check if chunk is out of bounds
        if start_line > total_lines:
            return None

        # Extract chunk lines (convert to 0-indexed for array access)
        chunk_lines = lines[start_line - 1:end_line]

        # Create chunk
        chunk = CodeChunk(
            start_line=start_line,
            end_line=min(end_line, total_lines),
            lines=chunk_lines,
            total_lines=total_lines
        )

        # Cache chunk
        if self.enable_cache:
            self._cache[cache_key] = chunk

        logger.debug(f"Loaded chunk {chunk_index}: lines {start_line}-{end_line}")
        return chunk

    def get_total_lines(self, content: str) -> int:
        """
        Get total line count.

        Args:
            content: File content

        Returns:
            Total number of lines
        """
        return len(content.splitlines())

    def get_total_chunks(self, content: str) -> int:
        """
        Calculate total number of chunks.

        Args:
            content: File content

        Returns:
            Total chunk count
        """
        total_lines = self.get_total_lines(content)
        return estimate_chunk_count(total_lines, self.chunk_size)

    def clear_cache(self):
        """Clear chunk cache."""
        self._cache.clear()
        logger.debug("Chunk cache cleared")

    def _get_cache_key(
        self,
        content: str,
        chunk_index: int,
        file_path: Optional[Path] = None
    ) -> str:
        """
        Generate cache key for chunk.

        Args:
            content: File content
            chunk_index: Chunk index
            file_path: Optional file path

        Returns:
            Cache key string
        """
        # Use content hash + chunk index as key
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        if file_path:
            return f"{file_path}:{content_hash}:{chunk_index}"
        return f"{content_hash}:{chunk_index}"


def calculate_chunk_boundaries(
    chunk_index: int,
    chunk_size: int,
    total_lines: int
) -> Tuple[int, int]:
    """
    Calculate chunk boundaries.

    Args:
        chunk_index: Chunk index (0-based)
        chunk_size: Lines per chunk
        total_lines: Total lines in file

    Returns:
        Tuple of (start_line, end_line) - both 1-indexed, inclusive

    Raises:
        ValueError: If chunk_size is invalid
    """
    if chunk_size <= 0:
        raise ValueError(f"Invalid chunk size: {chunk_size}")

    start_line = (chunk_index * chunk_size) + 1
    end_line = min(start_line + chunk_size - 1, total_lines)

    return start_line, end_line


def load_file_chunk(
    content: Optional[str] = None,
    file_path: Optional[Path] = None,
    start_line: int = 1,
    end_line: int = 1000
) -> List[str]:
    """
    Load specific lines from file or content.

    Args:
        content: File content (if already loaded)
        file_path: Path to file (if not loaded)
        start_line: Start line number (1-indexed)
        end_line: End line number (1-indexed, inclusive)

    Returns:
        List of lines

    Raises:
        LazyLoadingError: If neither content nor file_path provided
    """
    if content is None and file_path is None:
        raise LazyLoadingError("Either content or file_path must be provided")

    # Load from file if needed
    if content is None:
        content = file_path.read_text(encoding='utf-8')

    # Split and extract lines
    lines = content.splitlines()
    total_lines = len(lines)

    # Adjust end_line if it exceeds file length
    end_line = min(end_line, total_lines)

    # Extract lines (convert to 0-indexed)
    return lines[start_line - 1:end_line]


def get_visible_lines(
    scroll_position: int,
    viewport_height: int,
    line_height: int = 20,
    total_lines: Optional[int] = None,
    buffer_lines: int = 10
) -> Dict[str, int]:
    """
    Calculate visible lines based on scroll position.

    Args:
        scroll_position: Current scroll position in pixels
        viewport_height: Viewport height in pixels
        line_height: Height of one line in pixels (default: 20)
        total_lines: Total lines in file (optional, for bounds checking)
        buffer_lines: Buffer lines before/after visible area (default: 10)

    Returns:
        Dictionary with visible line range:
        - start_line: First visible line
        - end_line: Last visible line
        - buffer_start: First line including buffer
        - buffer_end: Last line including buffer
    """
    # Calculate visible line range
    start_line = max(1, (scroll_position // line_height) + 1)
    visible_line_count = (viewport_height // line_height) + 1
    end_line = start_line + visible_line_count - 1

    # Add buffer for smooth scrolling
    buffer_start = max(1, start_line - buffer_lines)
    buffer_end = end_line + buffer_lines

    # Apply bounds if total_lines provided
    if total_lines:
        end_line = min(end_line, total_lines)
        buffer_end = min(buffer_end, total_lines)

    return {
        "start_line": start_line,
        "end_line": end_line,
        "buffer_start": buffer_start,
        "buffer_end": buffer_end
    }


def estimate_chunk_count(total_lines: int, chunk_size: int) -> int:
    """
    Estimate number of chunks needed.

    Args:
        total_lines: Total lines in file
        chunk_size: Lines per chunk

    Returns:
        Estimated chunk count
    """
    if total_lines == 0:
        return 0

    # Calculate chunks (ceiling division)
    chunks = (total_lines + chunk_size - 1) // chunk_size
    return chunks


def should_use_lazy_loading(total_lines: int, threshold: int = 5000) -> bool:
    """
    Determine if lazy loading should be used.

    Args:
        total_lines: Total lines in file
        threshold: Line threshold for lazy loading (default: 5000)

    Returns:
        True if lazy loading recommended
    """
    return total_lines > threshold


__all__ = [
    "LazyCodeLoader",
    "CodeChunk",
    "calculate_chunk_boundaries",
    "load_file_chunk",
    "get_visible_lines",
    "estimate_chunk_count",
    "should_use_lazy_loading",
    "LazyLoadingError"
]
