#!/usr/bin/env python3

"""
Test script for enhanced AI classification system.
Tests all components of the AI-Enhanced Metadata Classification system.
"""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.metadata_schemas import (
    EnhancedFileClassification, 
    EnhancedAIAnalysis, 
    ArchitecturalLayer, 
    ComponentType,
    TechnologyStack,
    DesignPattern
)
from src.classification_prompts import ClassificationPromptBuilder
from src.enhanced_ai_analyzer import EnhancedAIAnalyzer
from src.chromadb_connector import EnhancedChromaDBConnector
from src.metadata_grouping import MetadataGrouper
from src.enhanced_requirements_generator import EnhancedRequirementsGenerator

def test_metadata_schemas():
    """Test metadata schemas and validation"""
    print("🧪 Testing metadata schemas...")
    
    try:
        # Test basic classification
        classification = EnhancedFileClassification(
            architectural_layer=ArchitecturalLayer.BACKEND_SERVICE,
            component_type=ComponentType.REST_CONTROLLER,
            confidence_score=0.9,
            technology_stack=[TechnologyStack.SPRING_FRAMEWORK],
            design_patterns=[DesignPattern.MVC],
            primary_purpose="Handle REST API endpoints"
        )
        
        # Test full enhanced analysis
        analysis = EnhancedAIAnalysis(
            purpose="REST controller for user management",
            file_classification=classification
        )
        
        print("✅ Metadata schemas validation passed")
        return True
        
    except Exception as e:
        print(f"❌ Metadata schemas test failed: {e}")
        return False

def test_classification_prompts():
    """Test classification prompt builder"""
    print("🧪 Testing classification prompt builder...")
    
    try:
        builder = ClassificationPromptBuilder()
        
        # Test single file prompt
        sample_code = """
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    @Autowired
    private UserService userService;
    
    @GetMapping
    public List<User> getAllUsers() {
        return userService.findAll();
    }
}
"""
        
        prompt = builder.create_classification_prompt(
            file_path="src/main/java/com/example/UserController.java",
            content=sample_code,
            file_type="Java"
        )
        
        # Validate prompt contains required elements
        assert "architectural_layer" in prompt
        assert "component_type" in prompt
        assert "technology_stack" in prompt
        assert "design_patterns" in prompt
        
        print("✅ Classification prompt builder test passed")
        return True
        
    except Exception as e:
        print(f"❌ Classification prompt builder test failed: {e}")
        return False

async def test_enhanced_ai_analyzer():
    """Test enhanced AI analyzer"""
    print("🧪 Testing enhanced AI analyzer...")
    
    try:
        analyzer = EnhancedAIAnalyzer()
        
        # Test file metadata structure
        file_metadata = {
            'file_path': 'src/test/java/TestController.java',
            'file_type': 'Java',
            'content': '''
@RestController
public class TestController {
    @GetMapping("/test")
    public String test() {
        return "Hello World";
    }
}
''',
            'size': 500
        }
        
        # Test fallback analysis (when AI parsing fails)
        fallback_analysis = analyzer.create_fallback_analysis("Sample analysis text", file_metadata['file_path'])
        
        # Validate fallback structure
        assert 'file_classification' in fallback_analysis
        assert 'architectural_layer' in fallback_analysis['file_classification']
        assert 'component_type' in fallback_analysis['file_classification']
        
        print("✅ Enhanced AI analyzer test passed")
        return True
        
    except Exception as e:
        print(f"❌ Enhanced AI analyzer test failed: {e}")
        return False

def test_chromadb_connector():
    """Test ChromaDB connector with enhanced metadata"""
    print("🧪 Testing ChromaDB connector...")
    
    try:
        # Use test ChromaDB directory
        os.environ['CHROMADB_DIR'] = './data/test_chromadb'
        
        connector = EnhancedChromaDBConnector()
        
        # Test enhanced metadata storage
        sample_enhanced_analysis = {
            'purpose': 'Test controller for API endpoints',
            'file_classification': {
                'architectural_layer': 'backend_service',
                'component_type': 'rest_controller',
                'confidence_score': 0.9,
                'technology_stack': ['spring_framework'],
                'design_patterns': ['mvc'],
                'primary_purpose': 'Handle REST requests',
                'exposes_api': True,
                'database_interactions': False
            }
        }
        
        connector.store_enhanced_metadata(
            file_path='test/TestController.java',
            content='// Test controller content',
            enhanced_analysis=sample_enhanced_analysis
        )
        
        # Test enhanced queries
        layer_results = connector.query_by_architectural_layer('backend_service', n_results=5)
        api_results = connector.query_files_with_api_exposure(n_results=5)
        
        print("✅ ChromaDB connector test passed")
        return True
        
    except Exception as e:
        print(f"❌ ChromaDB connector test failed: {e}")
        return False

def test_metadata_grouping():
    """Test metadata grouping and filtering utilities"""
    print("🧪 Testing metadata grouping...")
    
    try:
        grouper = MetadataGrouper()
        
        # Sample metadata list
        sample_metadata = [
            {
                'file_path': 'UserController.java',
                'enhanced_ai_analysis': {
                    'file_classification': {
                        'architectural_layer': 'backend_service',
                        'component_type': 'rest_controller',
                        'technology_stack': ['spring_framework'],
                        'exposes_api': True,
                        'database_interactions': False
                    }
                }
            },
            {
                'file_path': 'UserService.java',
                'enhanced_ai_analysis': {
                    'file_classification': {
                        'architectural_layer': 'backend_service',
                        'component_type': 'service_layer',
                        'technology_stack': ['spring_framework'],
                        'exposes_api': False,
                        'database_interactions': True
                    }
                }
            },
            {
                'file_path': 'index.jsp',
                'enhanced_ai_analysis': {
                    'file_classification': {
                        'architectural_layer': 'frontend',
                        'component_type': 'jsp_page',
                        'technology_stack': ['jsp'],
                        'exposes_api': False,
                        'database_interactions': False
                    }
                }
            }
        ]
        
        # Test grouping functions
        layer_groups = grouper.group_by_architectural_layer(sample_metadata)
        component_groups = grouper.group_by_component_type(sample_metadata)
        
        # Test filtering functions
        api_files = grouper.filter_api_exposing_files(sample_metadata)
        db_files = grouper.filter_database_interacting_files(sample_metadata)
        spring_files = grouper.filter_by_technology_stack(sample_metadata, 'spring_framework')
        
        # Validate results
        assert 'backend_service' in layer_groups
        assert 'frontend' in layer_groups
        assert len(layer_groups['backend_service']) == 2
        assert len(layer_groups['frontend']) == 1
        
        assert len(api_files) == 1
        assert len(db_files) == 1
        assert len(spring_files) == 2
        
        # Test architecture report
        report = grouper.generate_architecture_report(sample_metadata)
        assert 'summary' in report
        assert 'architectural_distribution' in report
        assert 'technology_analysis' in report
        
        print("✅ Metadata grouping test passed")
        return True
        
    except Exception as e:
        print(f"❌ Metadata grouping test failed: {e}")
        return False

def test_requirements_generator():
    """Test enhanced requirements generator"""
    print("🧪 Testing requirements generator...")
    
    try:
        output_dir = './test_output'
        os.makedirs(output_dir, exist_ok=True)
        
        generator = EnhancedRequirementsGenerator(output_dir)
        
        # Sample metadata with successful analysis
        sample_metadata = [
            {
                'file_path': 'UserController.java',
                'analysis_status': 'completed_enhanced',
                'enhanced_ai_analysis': {
                    'purpose': 'REST controller for user management',
                    'file_classification': {
                        'architectural_layer': 'backend_service',
                        'component_type': 'rest_controller',
                        'primary_purpose': 'Handle user API endpoints',
                        'technology_stack': ['spring_framework'],
                        'design_patterns': ['mvc'],
                        'exposes_api': True,
                        'database_interactions': False
                    }
                }
            }
        ]
        
        # Test requirements generation
        generator.generate_grouped_requirements(sample_metadata)
        
        # Check if files were created
        requirements_dir = os.path.join(output_dir, 'requirements_enhanced')
        assert os.path.exists(requirements_dir)
        
        print("✅ Requirements generator test passed")
        return True
        
    except Exception as e:
        print(f"❌ Requirements generator test failed: {e}")
        return False

def test_end_to_end_integration():
    """Test end-to-end integration of all components"""
    print("🧪 Testing end-to-end integration...")
    
    try:
        # This would test the full pipeline but without making actual AI API calls
        # Instead, we test the integration points
        
        # Test that all imports work together
        from src.enhanced_main import EnhancedBatchAIAnalyzer
        
        analyzer = EnhancedBatchAIAnalyzer()
        
        # Test file prioritization
        sample_files = [
            {'file_path': 'test.java', 'size': 1000},
            {'file_path': 'config.xml', 'size': 500},
            {'file_path': 'index.jsp', 'size': 800}
        ]
        
        prioritized = analyzer.prioritize_files(sample_files)
        
        # Java file should be first
        assert prioritized[0]['file_path'] == 'test.java'
        
        print("✅ End-to-end integration test passed")
        return True
        
    except Exception as e:
        print(f"❌ End-to-end integration test failed: {e}")
        return False

async def run_all_tests():
    """Run all tests"""
    print("🚀 Starting enhanced classification system tests...\n")
    
    test_results = []
    
    # Run all tests
    test_results.append(("Metadata Schemas", test_metadata_schemas()))
    test_results.append(("Classification Prompts", test_classification_prompts()))
    test_results.append(("Enhanced AI Analyzer", await test_enhanced_ai_analyzer()))
    test_results.append(("ChromaDB Connector", test_chromadb_connector()))
    test_results.append(("Metadata Grouping", test_metadata_grouping()))
    test_results.append(("Requirements Generator", test_requirements_generator()))
    test_results.append(("End-to-End Integration", test_end_to_end_integration()))
    
    # Print results summary
    print(f"\n{'='*50}")
    print("TEST RESULTS SUMMARY")
    print(f"{'='*50}")
    
    passed = 0
    failed = 0
    
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:.<30} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotal Tests: {len(test_results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {passed/len(test_results)*100:.1f}%")
    
    if failed == 0:
        print(f"\n🎉 All tests passed! Enhanced classification system is ready for use.")
        return True
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review and fix issues before using the system.")
        return False

def print_usage_instructions():
    """Print usage instructions for the enhanced system"""
    print(f"\n{'='*60}")
    print("ENHANCED CLASSIFICATION SYSTEM - USAGE INSTRUCTIONS")
    print(f"{'='*60}")
    
    print(f"""
📋 QUICK START:

1. Set up your environment:
   export AI_PROVIDER=ollama  # or openai/anthropic
   export OLLAMA_MODEL_NAME=deepseek-r1:32b
   export OUTPUT_DIR=./output
   export CHROMADB_DIR=./data/chromadb

2. Run enhanced analysis:
   python src/enhanced_main.py

3. Generate enhanced requirements:
   python -c "
   from src.enhanced_requirements_generator import EnhancedRequirementsGenerator
   import json
   
   # Load analyzed metadata
   with open('./output/enhanced_metadata.json', 'r') as f:
       metadata = json.load(f)
   
   # Generate requirements
   generator = EnhancedRequirementsGenerator('./output')
   generator.generate_grouped_requirements(metadata)
   "

📁 OUTPUT FILES:
- enhanced_metadata.json          - Enhanced analysis results
- enhanced_architecture_report.json - Architecture overview
- layer_summary_*.json           - Layer-specific summaries
- requirements_enhanced/         - Organized requirements docs
  ├── by_layer/                 - Requirements by architectural layer
  ├── by_component/            - Requirements by component type
  ├── by_domain/               - Requirements by business domain
  └── analysis/                - Cross-cutting analysis reports

🔍 KEY FEATURES:
- Architectural layer classification (frontend, backend_service, etc.)
- Component type identification (rest_controller, service_layer, etc.)
- Technology stack detection (Spring, Hibernate, etc.)
- Design pattern recognition (MVC, Repository, etc.)
- Business domain grouping
- Quality metrics and complexity analysis
- Enhanced ChromaDB storage with semantic search
- Structured requirements documentation

🎯 CLASSIFICATION LAYERS:
- frontend: JSP, HTML, CSS, JavaScript
- backend_service: Controllers, Services, Business Logic
- data_access: DAOs, Repositories
- persistence: Entities, Database Mappings
- configuration: XML configs, Properties
- test: Unit tests, Integration tests
- utility: Helper classes, Common libraries
- security: Authentication, Authorization
- integration: External APIs, Message handlers
""")

if __name__ == "__main__":
    print("Enhanced AI Classification System - Test Suite")
    print("=" * 50)
    
    # Run tests
    success = asyncio.run(run_all_tests())
    
    # Print usage instructions
    if success:
        print_usage_instructions()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)