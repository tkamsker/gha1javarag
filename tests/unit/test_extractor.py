"""
Unit tests for extraction service.

Tests file reading, chunking logic, entity extraction, tag generation,
and error handling for malformed files.

NOTE: These tests should FAIL initially (TDD approach).
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile

from codeindex.services.extractor import (
    ExtractionService,
    chunk_file,
    extract_entities,
    generate_tags,
    normalize_tags,
    ExtractionError,
)
from codeindex.models.extraction import ExtractionResult
from codeindex.models import ArtifactType


# Fixtures
@pytest.fixture
def extractor_service():
    """ExtractionService instance."""
    return ExtractionService(max_concurrent=5)


@pytest.fixture
def sample_java_file():
    """Path to sample Java file."""
    return Path(__file__).parent.parent / "fixtures" / "sample_java" / "SampleClass.java"


@pytest.fixture
def large_file_content():
    """Generate content for a large file (>100k lines)."""
    return "\n".join([f"// Line {i}" for i in range(150000)])


# Test file reading
class TestFileReading:
    """Test file reading and content extraction."""

    def test_read_valid_file(self, extractor_service, sample_java_file):
        """Test reading a valid file."""
        if sample_java_file.exists():
            content = extractor_service.read_file(sample_java_file)

            assert content is not None
            assert isinstance(content, str)
            assert len(content) > 0

    def test_read_nonexistent_file(self, extractor_service):
        """Test reading non-existent file raises error."""
        with pytest.raises(FileNotFoundError):
            extractor_service.read_file(Path("/nonexistent/file.java"))

    def test_read_binary_file(self, extractor_service):
        """Test handling of binary files."""
        # Create a temporary binary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as f:
            f.write(b'\x00\x01\x02\x03\x04')
            temp_path = Path(f.name)

        try:
            with pytest.raises(ExtractionError, match="binary|encode"):
                extractor_service.read_file(temp_path)
        finally:
            temp_path.unlink()

    def test_read_file_with_encoding_issues(self, extractor_service):
        """Test handling files with encoding problems."""
        # Create file with mixed encodings
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix=".txt") as f:
            f.write(b'Valid UTF-8 text\n')
            f.write(b'\xff\xfe Invalid bytes\n')
            temp_path = Path(f.name)

        try:
            # Should handle gracefully or raise clear error
            content = extractor_service.read_file(temp_path, encoding='utf-8', errors='replace')
            assert isinstance(content, str)
        finally:
            temp_path.unlink()


# Test chunking logic
class TestChunkingLogic:
    """Test file chunking for large files."""

    def test_chunk_small_file(self):
        """Test that small files are not chunked."""
        content = "\n".join([f"line {i}" for i in range(100)])

        chunks = chunk_file(content, max_lines=1000)

        assert len(chunks) == 1
        assert chunks[0] == content

    def test_chunk_large_file(self, large_file_content):
        """Test chunking of large file (>100k lines)."""
        chunks = chunk_file(large_file_content, max_lines=50000)

        assert len(chunks) > 1
        assert len(chunks) >= 3  # 150k lines / 50k = 3 chunks

    def test_chunk_preserves_content(self, large_file_content):
        """Test that chunking preserves all content."""
        chunks = chunk_file(large_file_content, max_lines=50000)

        # Rejoin chunks and compare
        rejoined = "\n".join(chunks)
        assert rejoined == large_file_content

    def test_chunk_by_class_boundaries(self):
        """Test intelligent chunking at class boundaries."""
        java_content = """
        package com.example;

        public class Class1 {
            void method1() {}
        }

        public class Class2 {
            void method2() {}
        }
        """

        # Should try to chunk at class boundaries
        chunks = chunk_file(java_content, max_lines=5, smart_chunk=True)
        # Implementation should preserve class boundaries when possible
        assert len(chunks) >= 1

    def test_chunk_indices(self):
        """Test that chunk indices are tracked correctly."""
        content = "\n".join([f"line {i}" for i in range(10000)])

        chunks = list(chunk_file(content, max_lines=3000, with_indices=True))

        # Should return (chunk_index, total_chunks, chunk_content) tuples
        assert len(chunks) > 1
        if len(chunks) > 1:
            assert chunks[0][0] == 0  # First chunk index
            assert chunks[-1][0] == len(chunks) - 1  # Last chunk index


# Test entity extraction
class TestEntityExtraction:
    """Test entity extraction from parsed code."""

    def test_extract_java_entities(self):
        """Test extracting entities from Java code."""
        java_content = """
        package com.example;

        public class UserService {
            private UserRepository repo;

            public User findById(Long id) {
                return repo.findById(id);
            }
        }
        """

        entities = extract_entities(java_content, "java_source")

        assert isinstance(entities, list)
        assert "UserService" in entities
        assert "findById" in entities or "findById(Long)" in entities

    def test_extract_sql_entities(self):
        """Test extracting entities from SQL."""
        sql_content = """
        CREATE TABLE users (
            id BIGINT PRIMARY KEY,
            username VARCHAR(50),
            email VARCHAR(100)
        );
        """

        entities = extract_entities(sql_content, "sql_schema")

        assert "users" in entities
        assert "id" in entities or any("id" in e for e in entities)

    def test_extract_jsp_entities(self):
        """Test extracting entities from JSP."""
        jsp_content = """
        <form action="submitUser" method="post">
            <input type="text" name="username" />
            <input type="email" name="email" />
        </form>
        """

        entities = extract_entities(jsp_content, "jsp_view")

        assert isinstance(entities, list)
        assert "username" in entities or "email" in entities

    def test_entity_deduplication(self):
        """Test that duplicate entities are removed."""
        content = """
        public class Test {
            void method() {}
            void method() {}
        }
        """

        entities = extract_entities(content, "java_source")

        # Should not have duplicates
        assert len(entities) == len(set(entities))


# Test tag generation
class TestTagGeneration:
    """Test automated tag generation."""

    def test_generate_layer_tags(self):
        """Test generation of layer tags based on path."""
        # Test file path
        test_path = Path("/project/src/test/java/TestClass.java")
        tags = generate_tags(test_path, "java_test")

        assert "test" in tags.get("layer", [])

    def test_generate_backend_tags(self):
        """Test backend layer tag generation."""
        path = Path("/project/src/main/java/service/UserService.java")
        tags = generate_tags(path, "java_source")

        assert "backend" in tags.get("layer", [])

    def test_generate_frontend_tags(self):
        """Test frontend layer tag generation."""
        path = Path("/project/webapp/views/user.jsp")
        tags = generate_tags(path, "jsp_view")

        assert "frontend" in tags.get("layer", [])

    def test_generate_framework_tags(self):
        """Test framework detection from content."""
        spring_content = """
        @Service
        @Transactional
        public class UserService {}
        """

        tags = generate_tags(Path("UserService.java"), "java_source", content=spring_content)

        frameworks = tags.get("frameworks", [])
        assert "Spring" in frameworks or any("spring" in f.lower() for f in frameworks)

    def test_generate_concern_tags(self):
        """Test concern tag generation."""
        security_content = """
        public class AuthenticationFilter {
            void checkPermissions() {}
        }
        """

        tags = generate_tags(Path("AuthenticationFilter.java"), "java_source", content=security_content)

        concerns = tags.get("concerns", [])
        assert "security" in concerns or any("security" in c.lower() for c in concerns)


# Test tag normalization
class TestTagNormalization:
    """Test tag normalization against controlled vocabularies."""

    def test_normalize_layer_tags(self):
        """Test normalizing layer tags."""
        tags = {
            "layer": ["backend", "FRONTEND", "Back-End"],
            "domain": ["user"],
            "frameworks": [],
            "concerns": []
        }

        normalized = normalize_tags(tags)

        # Should be lowercase and deduplicated
        layer_tags = normalized.get("layer", [])
        assert "backend" in layer_tags
        assert "frontend" in layer_tags
        assert len([t for t in layer_tags if "backend" in t.lower()]) == 1  # No duplicates

    def test_normalize_framework_tags(self):
        """Test normalizing framework tags."""
        tags = {
            "layer": [],
            "domain": [],
            "frameworks": ["spring", "Spring Framework", "SPRING"],
            "concerns": []
        }

        normalized = normalize_tags(tags)

        frameworks = normalized.get("frameworks", [])
        # Should consolidate to single "Spring" tag
        spring_count = len([f for f in frameworks if "spring" in f.lower()])
        assert spring_count <= 1

    def test_filter_invalid_tags(self):
        """Test filtering of invalid tags."""
        tags = {
            "layer": ["backend", "invalid_layer", "frontend"],
            "domain": ["user"],
            "frameworks": ["ValidFramework", ""],
            "concerns": ["security"]
        }

        normalized = normalize_tags(tags)

        # Should remove empty and invalid tags
        assert "" not in normalized.get("frameworks", [])


# Test error handling
class TestErrorHandling:
    """Test error handling for various failure modes."""

    def test_handle_malformed_java(self, extractor_service):
        """Test handling of malformed Java code."""
        malformed = "public class { invalid syntax here"

        # Should not crash, may return partial results or error
        try:
            result = extractor_service.extract(malformed, "java_source", Path("test.java"))
            assert isinstance(result, ExtractionResult)
        except ExtractionError as e:
            assert "malformed" in str(e).lower() or "parse" in str(e).lower()

    def test_handle_empty_file(self, extractor_service):
        """Test handling of empty file."""
        result = extractor_service.extract("", "java_source", Path("empty.java"))

        assert isinstance(result, ExtractionResult)
        assert result.summary is not None  # Should have some default

    def test_handle_very_long_lines(self, extractor_service):
        """Test handling of files with very long lines."""
        long_line = "// " + "x" * 1000000  # 1M character line

        result = extractor_service.extract(long_line, "java_source", Path("long.java"))

        assert isinstance(result, ExtractionResult)

    def test_extraction_timeout(self, extractor_service):
        """Test handling of extraction timeout."""
        with patch('codeindex.services.ollama_client.OllamaClient.extract', side_effect=TimeoutError("Timeout")):
            with pytest.raises(ExtractionError, match="timeout|timed out"):
                extractor_service.extract("content", "java_source", Path("test.java"))

    def test_ai_service_unavailable(self, extractor_service):
        """Test graceful degradation when AI service unavailable."""
        with patch('codeindex.services.ollama_client.OllamaClient.extract', side_effect=ConnectionError("Unavailable")):
            # Should fall back to basic extraction without AI
            result = extractor_service.extract_fallback("content", "java_source", Path("test.java"))

            assert isinstance(result, ExtractionResult)
            assert result.confidence is None or result.confidence < 0.5


# Test integration scenarios
class TestExtractionIntegration:
    """Test realistic extraction scenarios."""

    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_extract_with_ai(self, mock_ollama, extractor_service, sample_java_file):
        """Test extraction using AI service."""
        # Mock Ollama response
        mock_instance = Mock()
        mock_ollama.return_value = mock_instance
        mock_instance.extract.return_value = {
            "summary": "Test class summary",
            "classification": "java_source",
            "entities": ["TestClass"],
            "tags": {"layer": ["backend"], "frameworks": ["Java"]},
            "confidence": 0.9
        }

        if sample_java_file.exists():
            with open(sample_java_file, 'r') as f:
                content = f.read()

            result = extractor_service.extract(content, "java_source", sample_java_file)

            assert isinstance(result, ExtractionResult)
            assert result.summary is not None
            assert len(result.entities) > 0

    def test_batch_extraction(self, extractor_service):
        """Test extracting multiple files concurrently."""
        files = [
            ("file1.java", "public class A {}"),
            ("file2.java", "public class B {}"),
            ("file3.java", "public class C {}"),
        ]

        results = extractor_service.extract_batch(files)

        assert len(results) == 3
        assert all(isinstance(r, ExtractionResult) for r in results)

    def test_extraction_with_chunking(self, extractor_service, large_file_content):
        """Test extraction of large file with chunking."""
        # Should chunk the file and extract from each chunk
        results = extractor_service.extract_chunked(
            large_file_content,
            "java_source",
            Path("large.java")
        )

        assert isinstance(results, list)
        assert len(results) > 1
        # Each chunk should have chunk_index and chunk_count
        assert all(hasattr(r, 'chunk_index') for r in results)
