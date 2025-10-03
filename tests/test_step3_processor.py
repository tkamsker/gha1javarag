"""
Test suite for Step3Processor
"""

import json
import pytest
import tempfile
import threading
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from src.step3_processor import Step3Processor, Step3Config, Step3ProcessingError
from src.env_loader import Config


@pytest.fixture
def mock_config():
    """Create mock configuration for testing."""
    config = Mock(spec=Config)
    config.output_dir = "/tmp/test_output"
    config.weaviate_url = "http://localhost:8080"
    config.weaviate_api_key = None
    config.ai_provider = "openai"
    config.openai_model_name = "gpt-4"
    return config


@pytest.fixture
def temp_dir():
    """Create temporary directory for test outputs."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def sample_intermediate_data():
    """Sample intermediate data for testing."""
    return {
        "generation": "step2_intermediate",
        "projects": {
            "test_project": {
                "name": "test_project",
                "path": "/path/to/test_project",
                "total_files": 10,
                "file_list": [
                    {
                        "path": "src/main/Main.java",
                        "language": "java",
                        "size_bytes": 1024,
                        "enhanced_ai_analysis": {
                            "file_classification": {
                                "architectural_layer": "backend_service",
                                "component_type": "service_class",
                                "confidence": 0.85
                            }
                        },
                        "llm_metadata": {
                            "primary_purpose": "REST API endpoint"
                        }
                    },
                    {
                        "path": "src/ui/Component.tsx",
                        "language": "typescript",
                        "size_bytes": 2048,
                        "enhanced_ai_analysis": {
                            "file_classification": {
                                "architectural_layer": "frontend",
                                "component_type": "ui_component",
                                "confidence": 0.90
                            }
                        }
                    }
                ]
            }
        }
    }


@pytest.fixture
def sample_weaviate_stats():
    """Sample Weaviate statistics for testing."""
    return {
        "JavaCodeChunks": {"count": 150},
        "UIComponents": {"count": 25},
        "BusinessRules": {"count": 30},
        "total_count": 205,
        "timestamp": "2024-01-01T12:00:00Z"
    }


class TestStep3Config:
    """Test Step3Config validation."""
    
    def test_valid_config(self, mock_config):
        """Test valid configuration passes validation."""
        config = Step3Config(mock_config)
        assert config.config == mock_config
    
    def test_missing_weaviate_url(self, mock_config):
        """Test missing WEAVIATE_URL raises error."""
        mock_config.weaviate_url = None
        with pytest.raises(ValueError, match="Missing required environment variables"):
            Step3Config(mock_config)
    
    def test_missing_output_dir(self, mock_config):
        """Test missing OUTPUT_DIR raises error."""
        mock_config.output_dir = None
        with pytest.raises(ValueError, match="Missing required environment variables"):
            Step3Config(mock_config)
    
    def test_nonexistent_output_dir(self, mock_config):
        """Test nonexistent output directory raises error."""
        mock_config.output_dir = "/nonexistent/path"
        with pytest.raises(FileNotFoundError):
            Step3Config(mock_config)


class TestStep3Processor:
    """Test Step3Processor functionality."""
    
    def test_initialization(self, mock_config, temp_dir):
        """Test processor initialization."""
        mock_config.output_dir = str(temp_dir)
        processor = Step3Processor(mock_config)
        
        assert processor.base_config == mock_config
        assert processor.requirements_dir == temp_dir / 'requirements'
        assert processor.projects_dir == temp_dir / 'requirements' / 'projects'
    
    @patch('src.step3_processor.LLMClient')
    @patch('src.step3_processor.WeaviateClient')
    @patch('src.step3_processor.ReportingManager')
    def test_initialize_components_success(self, mock_reporting, mock_weaviate, mock_llm, 
                                         mock_config, temp_dir):
        """Test successful component initialization."""
        mock_config.output_dir = str(temp_dir)
        
        # Mock Weaviate connectivity test
        mock_weaviate_instance = Mock()
        mock_weaviate_instance.get_all_collection_stats.return_value = {"total_count": 100}
        mock_weaviate.return_value = mock_weaviate_instance
        
        processor = Step3Processor(mock_config)
        processor.initialize_components()
        
        assert processor.llm_client is not None
        assert processor.weaviate_client is not None
        assert processor.reporting is not None
    
    @patch('src.step3_processor.WeaviateClient')
    def test_initialize_components_weaviate_failure(self, mock_weaviate, mock_config, temp_dir):
        """Test component initialization with Weaviate failure."""
        mock_config.output_dir = str(temp_dir)
        
        # Mock Weaviate connectivity failure
        mock_weaviate_instance = Mock()
        mock_weaviate_instance.get_all_collection_stats.side_effect = Exception("Connection failed")
        mock_weaviate.return_value = mock_weaviate_instance
        
        processor = Step3Processor(mock_config)
        
        with pytest.raises(Step3ProcessingError, match="Weaviate connectivity failed"):
            processor.initialize_components()
    
    def test_load_intermediate_data_primary(self, mock_config, temp_dir, sample_intermediate_data):
        """Test loading primary intermediate data source."""
        mock_config.output_dir = str(temp_dir)
        
        # Create primary data file
        primary_file = temp_dir / 'intermediate_step2.json'
        with open(primary_file, 'w') as f:
            json.dump(sample_intermediate_data, f)
        
        processor = Step3Processor(mock_config)
        data = processor.load_intermediate_data()
        
        assert data == sample_intermediate_data
        assert len(data['projects']) == 1
    
    def test_load_intermediate_data_fallback(self, mock_config, temp_dir, sample_intermediate_data):
        """Test loading fallback data source."""
        mock_config.output_dir = str(temp_dir)
        
        # Create only fallback file
        fallback_file = temp_dir / 'consolidated_metadata.json'
        with open(fallback_file, 'w') as f:
            json.dump(sample_intermediate_data, f)
        
        processor = Step3Processor(mock_config)
        data = processor.load_intermediate_data()
        
        assert data == sample_intermediate_data
    
    def test_load_intermediate_data_missing(self, mock_config, temp_dir):
        """Test error when no data files exist."""
        mock_config.output_dir = str(temp_dir)
        
        processor = Step3Processor(mock_config)
        
        with pytest.raises(Step3ProcessingError, match="No intermediate data found"):
            processor.load_intermediate_data()
    
    def test_load_intermediate_data_invalid_json(self, mock_config, temp_dir):
        """Test error with invalid JSON."""
        mock_config.output_dir = str(temp_dir)
        
        # Create file with invalid JSON
        primary_file = temp_dir / 'intermediate_step2.json'
        with open(primary_file, 'w') as f:
            f.write("invalid json content")
        
        processor = Step3Processor(mock_config)
        
        with pytest.raises(Step3ProcessingError, match="Invalid JSON"):
            processor.load_intermediate_data()
    
    def test_validate_data_structure_valid(self, mock_config, temp_dir, sample_intermediate_data):
        """Test data structure validation with valid data."""
        mock_config.output_dir = str(temp_dir)
        
        processor = Step3Processor(mock_config)
        # Should not raise exception
        processor._validate_data_structure(sample_intermediate_data)
    
    def test_validate_data_structure_invalid(self, mock_config, temp_dir):
        """Test data structure validation with invalid data."""
        mock_config.output_dir = str(temp_dir)
        
        processor = Step3Processor(mock_config)
        
        # Test non-dict data
        with pytest.raises(Step3ProcessingError, match="Data must be a dictionary"):
            processor._validate_data_structure("invalid")
        
        # Test invalid projects structure
        with pytest.raises(Step3ProcessingError, match="'projects' must be a dictionary"):
            processor._validate_data_structure({"projects": "invalid"})
    
    def test_collect_weaviate_statistics_success(self, mock_config, temp_dir, sample_weaviate_stats):
        """Test successful Weaviate statistics collection."""
        mock_config.output_dir = str(temp_dir)
        
        processor = Step3Processor(mock_config)
        
        # Mock Weaviate client
        processor.weaviate_client = Mock()
        processor.weaviate_client.get_all_collection_stats.return_value = sample_weaviate_stats
        
        stats = processor.collect_weaviate_statistics()
        
        assert stats == sample_weaviate_stats
        assert processor._stats_cache == sample_weaviate_stats
    
    def test_collect_weaviate_statistics_cached(self, mock_config, temp_dir, sample_weaviate_stats):
        """Test cached statistics return."""
        mock_config.output_dir = str(temp_dir)
        
        processor = Step3Processor(mock_config)
        processor._stats_cache = sample_weaviate_stats
        
        # Mock should not be called due to cache
        processor.weaviate_client = Mock()
        
        stats = processor.collect_weaviate_statistics()
        
        assert stats == sample_weaviate_stats
        processor.weaviate_client.get_all_collection_stats.assert_not_called()
    
    def test_collect_weaviate_statistics_failure(self, mock_config, temp_dir):
        """Test Weaviate statistics collection failure handling."""
        mock_config.output_dir = str(temp_dir)
        
        processor = Step3Processor(mock_config)
        
        # Mock Weaviate client failure
        processor.weaviate_client = Mock()
        processor.weaviate_client.get_all_collection_stats.side_effect = Exception("API Error")
        
        stats = processor.collect_weaviate_statistics()
        
        assert 'error' in stats
        assert stats['total_count'] == 0
    
    def test_analyze_file_types(self, mock_config, temp_dir):
        """Test file type analysis."""
        mock_config.output_dir = str(temp_dir)
        
        processor = Step3Processor(mock_config)
        
        project_data = {
            'file_list': [
                {'language': 'java'},
                {'language': 'java'},
                {'language': 'typescript'},
                {'language': 'python'}
            ]
        }
        
        file_types = processor._analyze_file_types(project_data)
        
        assert file_types == {'java': 2, 'typescript': 1, 'python': 1}
    
    def test_analyze_architectural_layers(self, mock_config, temp_dir):
        """Test architectural layer analysis."""
        mock_config.output_dir = str(temp_dir)
        
        processor = Step3Processor(mock_config)
        
        project_data = {
            'file_list': [
                {
                    'enhanced_ai_analysis': {
                        'file_classification': {
                            'architectural_layer': 'backend_service'
                        }
                    }
                },
                {
                    'enhanced_ai_analysis': {
                        'file_classification': {
                            'architectural_layer': 'frontend'
                        }
                    }
                },
                {
                    'enhanced_ai_analysis': {
                        'file_classification': {
                            'architectural_layer': 'backend_service'
                        }
                    }
                }
            ]
        }
        
        layers = processor._analyze_architectural_layers(project_data)
        
        assert layers == {'backend_service': 2, 'frontend': 1}
    
    def test_synthesize_requirements_success(self, mock_config, temp_dir, sample_weaviate_stats):
        """Test successful requirements synthesis."""
        mock_config.output_dir = str(temp_dir)
        
        processor = Step3Processor(mock_config)
        
        # Mock LLM client
        processor.llm_client = Mock()
        processor.llm_client._complete_text.return_value = "# Generated Requirements\n\nTest content"
        
        project_data = {
            'name': 'test_project',
            'path': '/test/path',
            'total_files': 5,
            'file_list': []
        }
        
        requirements = processor.synthesize_requirements('test_project', project_data, sample_weaviate_stats)
        
        assert requirements == "# Generated Requirements\n\nTest content"
        processor.llm_client._complete_text.assert_called_once()
    
    def test_synthesize_requirements_llm_failure(self, mock_config, temp_dir, sample_weaviate_stats):
        """Test requirements synthesis with LLM failure."""
        mock_config.output_dir = str(temp_dir)
        
        processor = Step3Processor(mock_config)
        
        # Mock LLM client failure
        processor.llm_client = Mock()
        processor.llm_client._complete_text.side_effect = Exception("LLM Error")
        
        project_data = {
            'name': 'test_project',
            'path': '/test/path',
            'total_files': 5,
            'file_list': []
        }
        
        requirements = processor.synthesize_requirements('test_project', project_data, sample_weaviate_stats)
        
        # Should return fallback requirements
        assert "Requirements for test_project" in requirements
        assert "fallback method" in requirements
    
    def test_generate_output_files(self, mock_config, temp_dir):
        """Test output file generation."""
        mock_config.output_dir = str(temp_dir)
        
        processor = Step3Processor(mock_config)
        processor.requirements_dir = temp_dir / 'requirements'
        processor.projects_dir = temp_dir / 'requirements' / 'projects'
        
        requirements_content = "# Test Requirements\n\n## Technical Architecture\nTest architecture content"
        
        processor.generate_output_files('test_project', requirements_content)
        
        # Check files were created
        project_dir = temp_dir / 'requirements' / 'projects' / 'test_project'
        assert project_dir.exists()
        assert (project_dir / 'requirements.md').exists()
        assert (project_dir / 'architecture.md').exists()
        assert (project_dir / 'dependencies.md').exists()
        
        # Check content
        with open(project_dir / 'requirements.md', 'r') as f:
            assert f.read() == requirements_content
    
    def test_generate_executive_summary(self, mock_config, temp_dir):
        """Test executive summary generation."""
        mock_config.output_dir = str(temp_dir)
        
        processor = Step3Processor(mock_config)
        processor.requirements_dir = temp_dir / 'requirements'
        processor.requirements_dir.mkdir(parents=True, exist_ok=True)
        
        projects = {
            'project1': '# Project 1\n\nProject 1 description and requirements',
            'project2': '# Project 2\n\nProject 2 description and requirements'
        }
        
        processor.generate_executive_summary(projects)
        
        summary_file = temp_dir / 'requirements' / '_step3_overview.md'
        assert summary_file.exists()
        
        with open(summary_file, 'r') as f:
            content = f.read()
            assert 'Step 3: Requirements Synthesis Overview' in content
            assert 'project1' in content
            assert 'project2' in content
            assert '2 projects' in content
    
    def test_thread_safety(self, mock_config, temp_dir, sample_weaviate_stats):
        """Test thread safety of statistics collection."""
        mock_config.output_dir = str(temp_dir)
        
        processor = Step3Processor(mock_config)
        
        # Mock Weaviate client
        processor.weaviate_client = Mock()
        processor.weaviate_client.get_all_collection_stats.return_value = sample_weaviate_stats
        
        results = []
        exceptions = []
        
        def collect_stats():
            try:
                stats = processor.collect_weaviate_statistics()
                results.append(stats)
            except Exception as e:
                exceptions.append(e)
        
        # Run multiple threads
        threads = [threading.Thread(target=collect_stats) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        # All should succeed and return cached results
        assert len(exceptions) == 0
        assert len(results) == 5
        assert all(result == sample_weaviate_stats for result in results)
        
        # Weaviate should be called only once due to caching
        processor.weaviate_client.get_all_collection_stats.assert_called_once()


class TestIntegration:
    """Integration tests for Step3Processor."""
    
    @patch('src.step3_processor.LLMClient')
    @patch('src.step3_processor.WeaviateClient')
    @patch('src.step3_processor.ReportingManager')
    def test_full_run_sequential(self, mock_reporting, mock_weaviate, mock_llm,
                                mock_config, temp_dir, sample_intermediate_data, sample_weaviate_stats):
        """Test full run in sequential mode."""
        mock_config.output_dir = str(temp_dir)
        
        # Setup mocks
        mock_weaviate_instance = Mock()
        mock_weaviate_instance.get_all_collection_stats.return_value = sample_weaviate_stats
        mock_weaviate_instance.close = Mock()
        mock_weaviate.return_value = mock_weaviate_instance
        
        mock_llm_instance = Mock()
        mock_llm_instance._complete_text.return_value = "# Generated Requirements\n\nTest requirements content"
        mock_llm.return_value = mock_llm_instance
        
        # Create data file
        data_file = temp_dir / 'intermediate_step2.json'
        with open(data_file, 'w') as f:
            json.dump(sample_intermediate_data, f)
        
        processor = Step3Processor(mock_config)
        processor.run(parallel=False)
        
        # Verify output structure
        requirements_dir = temp_dir / 'requirements'
        assert requirements_dir.exists()
        
        projects_dir = requirements_dir / 'projects'
        assert projects_dir.exists()
        
        project_dir = projects_dir / 'test_project'
        assert project_dir.exists()
        
        assert (project_dir / 'requirements.md').exists()
        assert (project_dir / 'architecture.md').exists()
        assert (project_dir / 'dependencies.md').exists()
        
        summary_file = requirements_dir / '_step3_overview.md'
        assert summary_file.exists()
        
        # Verify mocks were called
        mock_weaviate_instance.get_all_collection_stats.assert_called()
        mock_llm_instance._complete_text.assert_called()
        mock_weaviate_instance.close.assert_called()
    
    @patch('src.step3_processor.LLMClient')
    @patch('src.step3_processor.WeaviateClient')
    @patch('src.step3_processor.ReportingManager')
    def test_incremental_run_no_existing_files(self, mock_reporting, mock_weaviate, mock_llm,
                                             mock_config, temp_dir, sample_intermediate_data, 
                                             sample_weaviate_stats):
        """Test incremental run with no existing files."""
        mock_config.output_dir = str(temp_dir)
        
        # Setup mocks
        mock_weaviate_instance = Mock()
        mock_weaviate_instance.get_all_collection_stats.return_value = sample_weaviate_stats
        mock_weaviate_instance.close = Mock()
        mock_weaviate.return_value = mock_weaviate_instance
        
        mock_llm_instance = Mock()
        mock_llm_instance._complete_text.return_value = "# Generated Requirements\n\nTest content"
        mock_llm.return_value = mock_llm_instance
        
        # Create data file
        data_file = temp_dir / 'intermediate_step2.json'
        with open(data_file, 'w') as f:
            json.dump(sample_intermediate_data, f)
        
        processor = Step3Processor(mock_config)
        processor.run_incremental()
        
        # Should process the project since no files exist
        project_dir = temp_dir / 'requirements' / 'projects' / 'test_project'
        assert (project_dir / 'requirements.md').exists()
        
        # Verify LLM was called
        mock_llm_instance._complete_text.assert_called()
    
    @patch('src.step3_processor.LLMClient')
    @patch('src.step3_processor.WeaviateClient')
    @patch('src.step3_processor.ReportingManager')
    def test_incremental_run_with_existing_files(self, mock_reporting, mock_weaviate, mock_llm,
                                               mock_config, temp_dir, sample_intermediate_data,
                                               sample_weaviate_stats):
        """Test incremental run with existing files."""
        mock_config.output_dir = str(temp_dir)
        
        # Create existing files
        project_dir = temp_dir / 'requirements' / 'projects' / 'test_project'
        project_dir.mkdir(parents=True, exist_ok=True)
        
        requirements_file = project_dir / 'requirements.md'
        with open(requirements_file, 'w') as f:
            f.write("# Existing Requirements\n\nExisting content")
        
        # Create data file
        data_file = temp_dir / 'intermediate_step2.json'
        with open(data_file, 'w') as f:
            json.dump(sample_intermediate_data, f)
        
        processor = Step3Processor(mock_config)
        processor.run_incremental()
        
        # Should not process the project since files exist
        with open(requirements_file, 'r') as f:
            content = f.read()
            assert "Existing Requirements" in content
            assert "Generated Requirements" not in content
        
        # Executive summary should still be generated
        summary_file = temp_dir / 'requirements' / '_step3_overview.md'
        assert summary_file.exists()


if __name__ == '__main__':
    pytest.main([__file__])