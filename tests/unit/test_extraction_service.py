"""
Unit tests for extraction service.

Tests semantic extraction orchestration combining parsers and AI.

NOTE: These tests should FAIL initially (TDD approach).
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from codeindex.services.extraction import (
    ExtractionService,
    extract_file,
    extract_from_inventory,
)
from codeindex.models import ArtifactType
from codeindex.models.extraction import ExtractionResult


# Fixtures
@pytest.fixture
def fixtures_dir():
    """Path to test fixtures directory."""
    return Path(__file__).parent.parent / "fixtures"


@pytest.fixture
def sample_java_path(fixtures_dir):
    """Path to sample Java file."""
    return fixtures_dir / "sample_java" / "SampleClass.java"


@pytest.fixture
def sample_jsp_path(fixtures_dir):
    """Path to sample JSP file."""
    return fixtures_dir / "sample_jsp" / "SampleForm.jsp"


@pytest.fixture
def mock_ollama_client():
    """Mock Ollama client."""
    client = Mock()
    client.extract_semantics.return_value = {
        'summary': 'Test file summary',
        'roles': ['data-access'],
        'entities': ['User', 'Order'],
        'tags': ['spring', 'hibernate'],
        'language': 'java',
        'frameworks': ['Spring'],
        'concerns': ['security'],
        'dependencies': ['spring-core']
    }
    return client


@pytest.fixture
def extraction_service(mock_ollama_client):
    """ExtractionService instance with mocked Ollama."""
    return ExtractionService(ollama_client=mock_ollama_client)


@pytest.fixture
def mock_config():
    """Mock configuration."""
    config = Mock()
    config.ollama_base_url = "http://localhost:11434"
    config.ollama_model = "gemma2:12b"
    config.extraction_batch_size = 10
    return config


# Test service initialization
class TestServiceInitialization:
    """Test extraction service initialization."""

    def test_service_initialization(self):
        """Test service can be initialized."""
        service = ExtractionService()
        assert service is not None

    def test_service_with_config(self, mock_config):
        """Test service initialization with config."""
        service = ExtractionService(config=mock_config)
        assert service.config == mock_config

    def test_service_creates_ollama_client(self):
        """Test service creates Ollama client."""
        service = ExtractionService()
        assert service.ollama_client is not None


# Test file extraction
class TestFileExtraction:
    """Test extracting single files."""

    def test_extract_java_file(self, extraction_service, sample_java_path):
        """Test extracting Java file."""
        result = extraction_service.extract_file(
            sample_java_path,
            ArtifactType.JAVA_SOURCE
        )

        assert isinstance(result, ExtractionResult)
        assert result.file_path == str(sample_java_path)
        assert result.artifact_type == ArtifactType.JAVA_SOURCE

    def test_extract_jsp_file(self, extraction_service, sample_jsp_path):
        """Test extracting JSP file."""
        result = extraction_service.extract_file(
            sample_jsp_path,
            ArtifactType.JSP_VIEW
        )

        assert isinstance(result, ExtractionResult)
        assert result.artifact_type == ArtifactType.JSP_VIEW

    def test_extraction_includes_structural_data(
        self, extraction_service, sample_java_path
    ):
        """Test that extraction includes structural information."""
        result = extraction_service.extract_file(
            sample_java_path,
            ArtifactType.JAVA_SOURCE
        )

        # Should have structural data from parser
        assert result.structural_data is not None
        assert isinstance(result.structural_data, dict)

    def test_extraction_includes_semantic_data(
        self, extraction_service, sample_java_path
    ):
        """Test that extraction includes semantic information."""
        result = extraction_service.extract_file(
            sample_java_path,
            ArtifactType.JAVA_SOURCE
        )

        # Should have semantic data from Ollama
        assert result.semantic_data is not None
        assert 'summary' in result.semantic_data

    def test_extraction_result_has_metadata(
        self, extraction_service, sample_java_path
    ):
        """Test that extraction result has metadata."""
        result = extraction_service.extract_file(
            sample_java_path,
            ArtifactType.JAVA_SOURCE
        )

        assert result.extracted_at is not None
        assert isinstance(result.extracted_at, datetime)


# Test parser selection
class TestParserSelection:
    """Test automatic parser selection."""

    def test_selects_java_parser(self, extraction_service, sample_java_path):
        """Test Java parser is selected for Java files."""
        result = extraction_service.extract_file(
            sample_java_path,
            ArtifactType.JAVA_SOURCE
        )

        # Should have Java-specific structural data
        structural = result.structural_data
        assert 'package' in structural or 'classes' in structural

    def test_selects_jsp_parser(self, extraction_service, sample_jsp_path):
        """Test JSP parser is selected for JSP files."""
        result = extraction_service.extract_file(
            sample_jsp_path,
            ArtifactType.JSP_VIEW
        )

        # Should have JSP-specific structural data
        structural = result.structural_data
        assert 'directives' in structural or 'taglibs' in structural


# Test error handling
class TestErrorHandling:
    """Test error handling in extraction."""

    def test_extract_nonexistent_file(self, extraction_service):
        """Test extracting non-existent file."""
        with pytest.raises(FileNotFoundError):
            extraction_service.extract_file(
                Path("/nonexistent/file.java"),
                ArtifactType.JAVA_SOURCE
            )

    def test_handles_ollama_unavailable(self, sample_java_path):
        """Test graceful degradation when Ollama unavailable."""
        # Create service with mock that raises ConnectionError
        mock_client = Mock()
        mock_client.extract_semantics.side_effect = ConnectionError("Ollama unavailable")

        service = ExtractionService(ollama_client=mock_client)

        # Should not crash, but fall back to structural only
        result = service.extract_file(
            sample_java_path,
            ArtifactType.JAVA_SOURCE
        )

        assert isinstance(result, ExtractionResult)
        assert result.structural_data is not None
        # Semantic data might be None or minimal fallback

    def test_handles_parser_error(self, extraction_service, tmp_path):
        """Test handling parser errors."""
        # Create malformed file
        malformed = tmp_path / "malformed.java"
        malformed.write_text("public class { broken }")

        # Should not crash
        result = extraction_service.extract_file(
            malformed,
            ArtifactType.JAVA_SOURCE
        )

        assert isinstance(result, ExtractionResult)


# Test batch extraction
class TestBatchExtraction:
    """Test batch file extraction."""

    def test_extract_multiple_files(self, extraction_service, fixtures_dir):
        """Test extracting multiple files."""
        java_dir = fixtures_dir / "sample_java"
        files = list(java_dir.glob("*.java"))

        if len(files) < 2:
            pytest.skip("Need at least 2 Java files")

        file_list = [(f, ArtifactType.JAVA_SOURCE) for f in files]
        results = extraction_service.extract_batch(file_list)

        assert len(results) >= 2
        for result in results:
            assert isinstance(result, ExtractionResult)

    def test_batch_extraction_continues_on_error(
        self, extraction_service, fixtures_dir, tmp_path
    ):
        """Test batch extraction continues despite errors."""
        java_dir = fixtures_dir / "sample_java"
        valid_file = list(java_dir.glob("*.java"))[0]

        # Create invalid file
        invalid = tmp_path / "invalid.java"
        invalid.write_text("broken")

        file_list = [
            (valid_file, ArtifactType.JAVA_SOURCE),
            (invalid, ArtifactType.JAVA_SOURCE),
        ]

        results = extraction_service.extract_batch(file_list)

        # Should have results for both (even if one has errors)
        assert len(results) == 2


# Test semantic extraction integration
class TestSemanticExtraction:
    """Test semantic extraction with Ollama."""

    def test_calls_ollama_for_semantics(
        self, mock_ollama_client, sample_java_path
    ):
        """Test that Ollama is called for semantic extraction."""
        service = ExtractionService(ollama_client=mock_ollama_client)

        result = service.extract_file(
            sample_java_path,
            ArtifactType.JAVA_SOURCE
        )

        # Verify Ollama was called
        mock_ollama_client.extract_semantics.assert_called_once()

        # Verify semantic data in result
        assert result.semantic_data is not None
        assert result.semantic_data['summary'] == 'Test file summary'

    def test_passes_file_content_to_ollama(
        self, mock_ollama_client, sample_java_path
    ):
        """Test that file content is passed to Ollama."""
        service = ExtractionService(ollama_client=mock_ollama_client)

        service.extract_file(sample_java_path, ArtifactType.JAVA_SOURCE)

        # Check call arguments
        call_args = mock_ollama_client.extract_semantics.call_args
        assert call_args is not None
        assert sample_java_path.name in call_args[0][0]  # file_path argument


# Test extraction from inventory
class TestInventoryExtraction:
    """Test extracting from discovery inventory."""

    def test_extract_from_inventory(self, extraction_service, fixtures_dir):
        """Test extracting files from inventory."""
        # This would normally load from JSONL
        # For testing, create mock inventory
        inventory_data = {
            'files': [
                {
                    'path': str(fixtures_dir / "sample_java" / "SampleClass.java"),
                    'type': 'JAVA_SOURCE'
                }
            ]
        }

        # Mock the inventory loading
        with patch('codeindex.services.extraction.load_inventory') as mock_load:
            mock_load.return_value = inventory_data

            results = extraction_service.extract_from_inventory(
                Path("/mock/inventory.jsonl")
            )

            assert len(results) >= 1


# Test result serialization
class TestResultSerialization:
    """Test extraction result serialization."""

    def test_result_to_dict(self, extraction_service, sample_java_path):
        """Test converting result to dictionary."""
        result = extraction_service.extract_file(
            sample_java_path,
            ArtifactType.JAVA_SOURCE
        )

        result_dict = result.to_dict()

        assert isinstance(result_dict, dict)
        assert 'file_path' in result_dict
        assert 'artifact_type' in result_dict
        assert 'structural_data' in result_dict
        assert 'semantic_data' in result_dict

    def test_result_serialization(self, extraction_service, sample_java_path):
        """Test result can be serialized to JSON."""
        result = extraction_service.extract_file(
            sample_java_path,
            ArtifactType.JAVA_SOURCE
        )

        import json
        result_dict = result.to_dict()

        # Should be JSON serializable
        json_str = json.dumps(result_dict, default=str)
        assert isinstance(json_str, str)


# Test standalone functions
class TestStandaloneFunctions:
    """Test standalone extraction functions."""

    @patch('codeindex.services.extraction.ExtractionService')
    def test_extract_file_function(self, mock_service_class, sample_java_path):
        """Test standalone extract_file function."""
        mock_service = Mock()
        mock_service_class.return_value = mock_service

        extract_file(sample_java_path, ArtifactType.JAVA_SOURCE)

        # Should create service and call extract_file
        mock_service.extract_file.assert_called_once()


# Integration-like tests
class TestIntegration:
    """Test integration of extraction components."""

    def test_full_extraction_workflow(
        self, extraction_service, sample_java_path
    ):
        """Test complete extraction workflow."""
        # Extract file
        result = extraction_service.extract_file(
            sample_java_path,
            ArtifactType.JAVA_SOURCE
        )

        # Verify result structure
        assert isinstance(result, ExtractionResult)

        # Verify structural data (from parser)
        structural = result.structural_data
        assert structural is not None
        assert 'package' in structural

        # Verify semantic data (from Ollama)
        semantic = result.semantic_data
        assert semantic is not None
        assert 'summary' in semantic

        # Verify metadata
        assert result.extracted_at is not None
        assert result.file_path == str(sample_java_path)
