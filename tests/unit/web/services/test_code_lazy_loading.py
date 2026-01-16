"""
Unit tests for Code Lazy Loading (T184 - US4.1).

Tests lazy loading functionality for large files.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from src.codeindex.web.services.code_lazy_loading import (
    LazyCodeLoader,
    CodeChunk,
    calculate_chunk_boundaries,
    load_file_chunk,
    get_visible_lines,
    estimate_chunk_count,
    LazyLoadingError
)


@pytest.fixture
def large_file_content():
    """Create large file content for testing."""
    return "\n".join([f"Line {i}: Some code content here" for i in range(1, 10001)])


@pytest.fixture
def lazy_loader():
    """Create LazyCodeLoader instance."""
    return LazyCodeLoader(chunk_size=1000)


class TestLazyCodeLoader:
    """Test LazyCodeLoader class."""

    def test_init_with_default_chunk_size(self):
        """Test initialization with default chunk size."""
        loader = LazyCodeLoader()
        assert loader.chunk_size == 1000

    def test_init_with_custom_chunk_size(self):
        """Test initialization with custom chunk size."""
        loader = LazyCodeLoader(chunk_size=500)
        assert loader.chunk_size == 500

    def test_load_first_chunk(self, lazy_loader, large_file_content):
        """Test loading first chunk of large file."""
        chunk = lazy_loader.load_chunk(large_file_content, chunk_index=0)

        assert chunk.start_line == 1
        assert chunk.end_line == 1000
        assert len(chunk.lines) == 1000
        assert chunk.lines[0] == "Line 1: Some code content here"

    def test_load_middle_chunk(self, lazy_loader, large_file_content):
        """Test loading middle chunk of large file."""
        chunk = lazy_loader.load_chunk(large_file_content, chunk_index=5)

        assert chunk.start_line == 5001
        assert chunk.end_line == 6000
        assert len(chunk.lines) == 1000

    def test_load_last_chunk(self, lazy_loader, large_file_content):
        """Test loading last chunk (partial)."""
        chunk = lazy_loader.load_chunk(large_file_content, chunk_index=9)

        assert chunk.start_line == 9001
        assert chunk.end_line == 10000
        assert len(chunk.lines) == 1000

    def test_load_chunk_out_of_bounds(self, lazy_loader, large_file_content):
        """Test loading chunk beyond file bounds."""
        chunk = lazy_loader.load_chunk(large_file_content, chunk_index=100)

        assert chunk is None or len(chunk.lines) == 0

    def test_load_multiple_chunks_sequentially(self, lazy_loader, large_file_content):
        """Test loading multiple chunks in sequence."""
        chunks = []
        for i in range(3):
            chunk = lazy_loader.load_chunk(large_file_content, chunk_index=i)
            chunks.append(chunk)

        assert len(chunks) == 3
        assert chunks[0].end_line == 1000
        assert chunks[1].start_line == 1001
        assert chunks[2].start_line == 2001

    def test_get_total_lines(self, lazy_loader, large_file_content):
        """Test getting total line count."""
        total = lazy_loader.get_total_lines(large_file_content)

        assert total == 10000

    def test_get_total_chunks(self, lazy_loader, large_file_content):
        """Test calculating total chunk count."""
        total_chunks = lazy_loader.get_total_chunks(large_file_content)

        assert total_chunks == 10  # 10000 lines / 1000 per chunk


class TestCalculateChunkBoundaries:
    """Test chunk boundary calculations."""

    def test_calculate_first_chunk_boundaries(self):
        """Test first chunk boundaries."""
        start, end = calculate_chunk_boundaries(
            chunk_index=0,
            chunk_size=1000,
            total_lines=10000
        )

        assert start == 1
        assert end == 1000

    def test_calculate_middle_chunk_boundaries(self):
        """Test middle chunk boundaries."""
        start, end = calculate_chunk_boundaries(
            chunk_index=5,
            chunk_size=1000,
            total_lines=10000
        )

        assert start == 5001
        assert end == 6000

    def test_calculate_last_chunk_boundaries_full(self):
        """Test last chunk boundaries when exactly divisible."""
        start, end = calculate_chunk_boundaries(
            chunk_index=9,
            chunk_size=1000,
            total_lines=10000
        )

        assert start == 9001
        assert end == 10000

    def test_calculate_last_chunk_boundaries_partial(self):
        """Test last chunk boundaries with partial chunk."""
        start, end = calculate_chunk_boundaries(
            chunk_index=5,
            chunk_size=1000,
            total_lines=5500
        )

        assert start == 5001
        assert end == 5500

    def test_calculate_boundaries_small_file(self):
        """Test boundaries for file smaller than chunk size."""
        start, end = calculate_chunk_boundaries(
            chunk_index=0,
            chunk_size=1000,
            total_lines=500
        )

        assert start == 1
        assert end == 500


class TestLoadFileChunk:
    """Test file chunk loading."""

    def test_load_chunk_from_content(self, large_file_content):
        """Test loading chunk from content string."""
        lines = load_file_chunk(
            content=large_file_content,
            start_line=1,
            end_line=100
        )

        assert len(lines) == 100
        assert lines[0] == "Line 1: Some code content here"
        assert lines[99] == "Line 100: Some code content here"

    def test_load_chunk_from_middle(self, large_file_content):
        """Test loading chunk from middle of file."""
        lines = load_file_chunk(
            content=large_file_content,
            start_line=5000,
            end_line=5100
        )

        assert len(lines) == 101
        assert "Line 5000:" in lines[0]

    def test_load_chunk_from_file_path(self, tmp_path):
        """Test loading chunk directly from file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("\n".join([f"Line {i}" for i in range(1, 1001)]))

        lines = load_file_chunk(
            file_path=test_file,
            start_line=1,
            end_line=100
        )

        assert len(lines) == 100
        assert lines[0] == "Line 1"

    def test_load_chunk_end_exceeds_file(self, large_file_content):
        """Test loading chunk when end exceeds file length."""
        lines = load_file_chunk(
            content=large_file_content,
            start_line=9900,
            end_line=11000  # Exceeds 10000
        )

        assert len(lines) == 101  # Only 9900-10000


class TestGetVisibleLines:
    """Test visible lines calculation."""

    def test_get_visible_lines_top_of_file(self):
        """Test visible lines at top of file."""
        visible = get_visible_lines(
            scroll_position=0,
            viewport_height=50,
            line_height=20
        )

        assert visible["start_line"] == 1
        assert visible["end_line"] <= 50

    def test_get_visible_lines_middle_of_file(self):
        """Test visible lines in middle of file."""
        visible = get_visible_lines(
            scroll_position=5000,
            viewport_height=50,
            line_height=20
        )

        assert visible["start_line"] > 1
        assert visible["end_line"] > visible["start_line"]

    def test_get_visible_lines_bottom_of_file(self):
        """Test visible lines at bottom of file."""
        visible = get_visible_lines(
            scroll_position=9500,
            viewport_height=50,
            line_height=20,
            total_lines=10000
        )

        assert visible["end_line"] <= 10000

    def test_get_visible_lines_with_buffer(self):
        """Test visible lines with buffer for smooth scrolling."""
        visible = get_visible_lines(
            scroll_position=1000,
            viewport_height=50,
            line_height=20,
            buffer_lines=10
        )

        # Should include buffer lines before and after
        assert visible["buffer_start"] < visible["start_line"]
        assert visible["buffer_end"] > visible["end_line"]


class TestEstimateChunkCount:
    """Test chunk count estimation."""

    def test_estimate_small_file(self):
        """Test estimation for small file."""
        chunks = estimate_chunk_count(total_lines=500, chunk_size=1000)

        assert chunks == 1

    def test_estimate_exact_chunks(self):
        """Test estimation when exactly divisible."""
        chunks = estimate_chunk_count(total_lines=5000, chunk_size=1000)

        assert chunks == 5

    def test_estimate_partial_chunk(self):
        """Test estimation with partial last chunk."""
        chunks = estimate_chunk_count(total_lines=5500, chunk_size=1000)

        assert chunks == 6

    def test_estimate_very_large_file(self):
        """Test estimation for very large file."""
        chunks = estimate_chunk_count(total_lines=100000, chunk_size=1000)

        assert chunks == 100


class TestCodeChunk:
    """Test CodeChunk dataclass."""

    def test_chunk_creation(self):
        """Test creating chunk."""
        chunk = CodeChunk(
            start_line=1,
            end_line=100,
            lines=["line1", "line2"],
            total_lines=10000
        )

        assert chunk.start_line == 1
        assert chunk.end_line == 100
        assert len(chunk.lines) == 2

    def test_chunk_is_first(self):
        """Test checking if chunk is first."""
        chunk = CodeChunk(start_line=1, end_line=100, lines=[], total_lines=1000)

        assert chunk.is_first() is True

    def test_chunk_is_last(self):
        """Test checking if chunk is last."""
        chunk = CodeChunk(start_line=9001, end_line=10000, lines=[], total_lines=10000)

        assert chunk.is_last() is True

    def test_chunk_has_next(self):
        """Test checking if chunk has next."""
        chunk = CodeChunk(start_line=1, end_line=1000, lines=[], total_lines=10000)

        assert chunk.has_next() is True

    def test_chunk_has_previous(self):
        """Test checking if chunk has previous."""
        chunk = CodeChunk(start_line=1001, end_line=2000, lines=[], total_lines=10000)

        assert chunk.has_previous() is True


class TestLazyLoadingPerformance:
    """Test lazy loading performance characteristics."""

    def test_load_chunk_performance(self, lazy_loader):
        """Test chunk loading performance."""
        content = "\n".join([f"Line {i}" for i in range(1, 10001)])

        # Test loading a chunk completes quickly
        import time
        start = time.time()
        result = lazy_loader.load_chunk(content, chunk_index=0)
        duration = time.time() - start

        assert result is not None
        assert duration < 1.0  # Should complete in less than 1 second

    def test_memory_efficiency_large_file(self, lazy_loader):
        """Test that lazy loading uses less memory than full load."""
        content = "\n".join([f"Line {i}" for i in range(1, 50001)])

        # Load only one chunk
        chunk = lazy_loader.load_chunk(content, chunk_index=0)

        # Chunk should be much smaller than full content
        import sys
        chunk_size = sys.getsizeof(chunk.lines)
        content_size = sys.getsizeof(content)

        assert chunk_size < content_size / 10

    def test_sequential_chunk_loading_performance(self, lazy_loader, large_file_content):
        """Test loading multiple chunks sequentially."""
        chunks_loaded = 0

        for i in range(5):
            chunk = lazy_loader.load_chunk(large_file_content, chunk_index=i)
            if chunk:
                chunks_loaded += 1

        assert chunks_loaded == 5


class TestLazyLoadingCaching:
    """Test lazy loading with caching."""

    def test_cache_loaded_chunks(self, lazy_loader, large_file_content):
        """Test caching of loaded chunks."""
        lazy_loader.enable_cache = True

        # Load same chunk twice
        chunk1 = lazy_loader.load_chunk(large_file_content, chunk_index=0)
        chunk2 = lazy_loader.load_chunk(large_file_content, chunk_index=0)

        # Should return same chunk from cache
        assert chunk1.lines == chunk2.lines

    def test_cache_invalidation_on_content_change(self, lazy_loader):
        """Test cache invalidation when content changes."""
        lazy_loader.enable_cache = True

        content1 = "\n".join([f"Line {i}" for i in range(1, 1001)])
        content2 = "\n".join([f"Modified Line {i}" for i in range(1, 1001)])

        chunk1 = lazy_loader.load_chunk(content1, chunk_index=0)
        chunk2 = lazy_loader.load_chunk(content2, chunk_index=0)

        assert chunk1.lines[0] != chunk2.lines[0]


class TestErrorHandling:
    """Test error handling in lazy loading."""

    def test_handle_invalid_chunk_index(self, lazy_loader, large_file_content):
        """Test handling of invalid chunk index."""
        chunk = lazy_loader.load_chunk(large_file_content, chunk_index=-1)

        assert chunk is None or len(chunk.lines) == 0

    def test_handle_empty_content(self, lazy_loader):
        """Test handling of empty content."""
        chunk = lazy_loader.load_chunk("", chunk_index=0)

        assert chunk is None or len(chunk.lines) == 0

    def test_handle_invalid_boundaries(self):
        """Test handling of invalid boundaries."""
        with pytest.raises(ValueError):
            calculate_chunk_boundaries(
                chunk_index=0,
                chunk_size=0,  # Invalid
                total_lines=1000
            )

    def test_handle_corrupt_file_content(self, lazy_loader):
        """Test handling of corrupt file content."""
        # Content with mixed line endings
        content = "line1\r\nline2\nline3\rline4"

        chunk = lazy_loader.load_chunk(content, chunk_index=0)

        # Should handle gracefully
        assert chunk is not None
