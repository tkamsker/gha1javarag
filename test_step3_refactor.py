#!/usr/bin/env python3
"""
Test runner for Step3 refactored implementation
This script validates the refactored step3 processor without requiring full environment setup
"""

import json
import logging
import sys
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to path for imports
src_path = str(Path(__file__).parent / 'src')
sys.path.insert(0, src_path)

try:
    import step3_processor
    import env_loader
    
    Step3Processor = step3_processor.Step3Processor
    Step3Config = step3_processor.Step3Config
    Step3ProcessingError = step3_processor.Step3ProcessingError
    Config = env_loader.Config
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print(f"Checked path: {src_path}")
    print("Make sure all required modules are available")
    sys.exit(1)


def setup_logging():
    """Setup basic logging for testing"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def create_mock_config(temp_dir: Path) -> Mock:
    """Create mock configuration for testing"""
    config = Mock(spec=Config)
    config.output_dir = str(temp_dir)
    config.weaviate_url = "http://localhost:8080"
    config.weaviate_api_key = None
    config.ai_provider = "openai"
    config.openai_model_name = "gpt-4"
    return config


def create_sample_data() -> dict:
    """Create sample intermediate data"""
    return {
        "generation": "step2_intermediate",
        "projects": {
            "sample_project": {
                "name": "sample_project",
                "path": "/path/to/sample_project",
                "total_files": 15,
                "file_list": [
                    {
                        "path": "src/main/java/Main.java",
                        "language": "java",
                        "size_bytes": 2048,
                        "enhanced_ai_analysis": {
                            "file_classification": {
                                "architectural_layer": "backend_service",
                                "component_type": "service_class",
                                "confidence": 0.87
                            }
                        },
                        "llm_metadata": {
                            "primary_purpose": "Application entry point",
                            "design_patterns": ["Singleton", "Factory"]
                        }
                    },
                    {
                        "path": "src/web/components/UserForm.tsx",
                        "language": "typescript",
                        "size_bytes": 3072,
                        "enhanced_ai_analysis": {
                            "file_classification": {
                                "architectural_layer": "frontend",
                                "component_type": "ui_component",
                                "confidence": 0.92
                            }
                        }
                    },
                    {
                        "path": "config/database.xml",
                        "language": "xml",
                        "size_bytes": 1024,
                        "enhanced_ai_analysis": {
                            "file_classification": {
                                "architectural_layer": "configuration",
                                "component_type": "config_file",
                                "confidence": 0.95
                            }
                        }
                    }
                ]
            },
            "api_service": {
                "name": "api_service",
                "path": "/path/to/api_service",
                "total_files": 8,
                "file_list": [
                    {
                        "path": "src/controllers/UserController.java",
                        "language": "java",
                        "size_bytes": 4096,
                        "enhanced_ai_analysis": {
                            "file_classification": {
                                "architectural_layer": "backend_service",
                                "component_type": "controller",
                                "confidence": 0.90
                            }
                        }
                    }
                ]
            }
        }
    }


def create_sample_weaviate_stats() -> dict:
    """Create sample Weaviate statistics"""
    return {
        "JavaCodeChunks": {"count": 120},
        "UIComponents": {"count": 35},
        "BusinessRules": {"count": 28},
        "IntegrationPoints": {"count": 15},
        "DocumentationChunks": {"count": 42},
        "NavigationFlows": {"count": 8},
        "total_count": 248,
        "timestamp": "2024-01-01T15:30:00Z"
    }


def test_step3_config_validation():
    """Test Step3Config validation"""
    print("🧪 Testing Step3Config validation...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Valid config
        mock_config = create_mock_config(temp_path)
        try:
            config = Step3Config(mock_config)
            print("✅ Valid config validation passed")
        except Exception as e:
            print(f"❌ Valid config validation failed: {e}")
            return False
        
        # Invalid config - missing weaviate_url
        mock_config.weaviate_url = None
        try:
            Step3Config(mock_config)
            print("❌ Invalid config validation should have failed")
            return False
        except ValueError:
            print("✅ Invalid config validation correctly failed")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    return True


def test_data_loading():
    """Test data loading functionality"""
    print("🧪 Testing data loading...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        mock_config = create_mock_config(temp_path)
        
        processor = Step3Processor(mock_config)
        
        # Test primary data source
        sample_data = create_sample_data()
        primary_file = temp_path / 'intermediate_step2.json'
        with open(primary_file, 'w') as f:
            json.dump(sample_data, f)
        
        try:
            data = processor.load_intermediate_data()
            if data == sample_data:
                print("✅ Primary data loading passed")
            else:
                print("❌ Primary data loading failed - data mismatch")
                return False
        except Exception as e:
            print(f"❌ Primary data loading failed: {e}")
            return False
        
        # Test fallback data source
        primary_file.unlink()
        fallback_file = temp_path / 'consolidated_metadata.json'
        with open(fallback_file, 'w') as f:
            json.dump(sample_data, f)
        
        try:
            data = processor.load_intermediate_data()
            if data == sample_data:
                print("✅ Fallback data loading passed")
            else:
                print("❌ Fallback data loading failed - data mismatch")
                return False
        except Exception as e:
            print(f"❌ Fallback data loading failed: {e}")
            return False
    
    return True


def test_file_analysis():
    """Test file analysis methods"""
    print("🧪 Testing file analysis...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        mock_config = create_mock_config(temp_path)
        
        processor = Step3Processor(mock_config)
        sample_data = create_sample_data()
        project_data = sample_data['projects']['sample_project']
        
        # Test file type analysis
        file_types = processor._analyze_file_types(project_data)
        expected_types = {'java': 1, 'typescript': 1, 'xml': 1}
        
        if file_types == expected_types:
            print("✅ File type analysis passed")
        else:
            print(f"❌ File type analysis failed: expected {expected_types}, got {file_types}")
            return False
        
        # Test architectural layer analysis
        layers = processor._analyze_architectural_layers(project_data)
        expected_layers = {'backend_service': 1, 'frontend': 1, 'configuration': 1}
        
        if layers == expected_layers:
            print("✅ Architectural layer analysis passed")
        else:
            print(f"❌ Architectural layer analysis failed: expected {expected_layers}, got {layers}")
            return False
    
    return True


def test_output_generation():
    """Test output file generation"""
    print("🧪 Testing output generation...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        mock_config = create_mock_config(temp_path)
        
        processor = Step3Processor(mock_config)
        processor.requirements_dir = temp_path / 'requirements'
        processor.projects_dir = temp_path / 'requirements' / 'projects'
        
        test_requirements = """# Test Project Requirements

## Project Overview
This is a test project for validation.

## Technical Architecture
- Backend: Java Spring Boot
- Frontend: React TypeScript
- Database: PostgreSQL

## Functional Requirements
1. User authentication
2. Data processing
3. Report generation
"""
        
        try:
            processor.generate_output_files('test_project', test_requirements)
            
            # Check files were created
            project_dir = temp_path / 'requirements' / 'projects' / 'test_project'
            if not project_dir.exists():
                print("❌ Project directory not created")
                return False
            
            required_files = ['requirements.md', 'architecture.md', 'dependencies.md']
            for filename in required_files:
                file_path = project_dir / filename
                if not file_path.exists():
                    print(f"❌ Required file not created: {filename}")
                    return False
            
            # Check requirements content
            with open(project_dir / 'requirements.md', 'r') as f:
                content = f.read()
                if content == test_requirements:
                    print("✅ Output generation passed")
                else:
                    print("❌ Requirements content mismatch")
                    return False
        
        except Exception as e:
            print(f"❌ Output generation failed: {e}")
            return False
    
    return True


def test_executive_summary():
    """Test executive summary generation"""
    print("🧪 Testing executive summary generation...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        mock_config = create_mock_config(temp_path)
        
        processor = Step3Processor(mock_config)
        processor.requirements_dir = temp_path / 'requirements'
        processor.requirements_dir.mkdir(parents=True, exist_ok=True)
        
        test_projects = {
            'project1': '# Project 1\n\nProject 1 requirements and specifications',
            'project2': '# Project 2\n\nProject 2 requirements and specifications'
        }
        
        try:
            processor.generate_executive_summary(test_projects)
            
            summary_file = temp_path / 'requirements' / '_step3_overview.md'
            if not summary_file.exists():
                print("❌ Executive summary file not created")
                return False
            
            with open(summary_file, 'r') as f:
                content = f.read()
                if 'Step 3: Requirements Synthesis Overview' in content and '2 projects' in content:
                    print("✅ Executive summary generation passed")
                else:
                    print("❌ Executive summary content validation failed")
                    return False
        
        except Exception as e:
            print(f"❌ Executive summary generation failed: {e}")
            return False
    
    return True


def test_mocked_full_run():
    """Test full run with mocked dependencies"""
    print("🧪 Testing mocked full run...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        mock_config = create_mock_config(temp_path)
        
        # Create data file
        sample_data = create_sample_data()
        data_file = temp_path / 'intermediate_step2.json'
        with open(data_file, 'w') as f:
            json.dump(sample_data, f)
        
        # Mock all external dependencies
        with patch('step3_processor.LLMClient') as mock_llm, \
             patch('step3_processor.WeaviateClient') as mock_weaviate, \
             patch('step3_processor.ReportingManager') as mock_reporting:
            
            # Setup mocks
            mock_weaviate_instance = Mock()
            mock_weaviate_instance.get_all_collection_stats.return_value = create_sample_weaviate_stats()
            mock_weaviate_instance.close = Mock()
            mock_weaviate.return_value = mock_weaviate_instance
            
            mock_llm_instance = Mock()
            mock_llm_instance._complete_text.return_value = """# Generated Requirements

## Project Overview
This project was analyzed using AI-powered code analysis.

## Technical Architecture
- Multi-layer architecture detected
- Backend services with REST APIs
- Frontend components with TypeScript
- Configuration management

## Functional Requirements
1. Core business logic processing
2. User interface interactions
3. Data persistence and retrieval
4. System configuration management
"""
            mock_llm.return_value = mock_llm_instance
            
            processor = Step3Processor(mock_config)
            
            try:
                processor.run(parallel=False)  # Sequential for predictable testing
                
                # Verify output structure
                requirements_dir = temp_path / 'requirements'
                if not requirements_dir.exists():
                    print("❌ Requirements directory not created")
                    return False
                
                projects_dir = requirements_dir / 'projects'
                if not projects_dir.exists():
                    print("❌ Projects directory not created")
                    return False
                
                # Check both projects were processed
                for project_name in ['sample_project', 'api_service']:
                    project_dir = projects_dir / project_name
                    if not project_dir.exists():
                        print(f"❌ Project directory not created for {project_name}")
                        return False
                    
                    req_file = project_dir / 'requirements.md'
                    if not req_file.exists():
                        print(f"❌ Requirements file not created for {project_name}")
                        return False
                
                # Check executive summary
                summary_file = requirements_dir / '_step3_overview.md'
                if not summary_file.exists():
                    print("❌ Executive summary not created")
                    return False
                
                print("✅ Mocked full run passed")
                return True
                
            except Exception as e:
                print(f"❌ Mocked full run failed: {e}")
                return False


def main():
    """Run all tests"""
    setup_logging()
    
    print("🚀 Starting Step3 Refactor Validation Tests")
    print("=" * 50)
    
    tests = [
        test_step3_config_validation,
        test_data_loading,
        test_file_analysis,
        test_output_generation,
        test_executive_summary,
        test_mocked_full_run
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test_func.__name__} crashed: {e}")
            failed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! Step3 refactoring is ready for testing.")
        return 0
    else:
        print("⚠️  Some tests failed. Please review and fix issues before deployment.")
        return 1


if __name__ == '__main__':
    sys.exit(main())