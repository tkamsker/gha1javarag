"""
Integration Test for Iteration 13 Components
Tests Ollama integration, Weaviate connector, and basic migration functionality
"""

import asyncio
import logging
import json
import sys
import time
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    from ollama_integration import OllamaIntegration
    from weaviate_connector import EnhancedWeaviateConnector, WeaviateConfig
    from weaviate_schemas import SchemaManager
    from code_chunker import CodeChunk, ChunkType
except ImportError as e:
    logger.error(f"Import error: {e}")
    sys.exit(1)

class Iteration13Tester:
    """Test suite for Iteration 13 components"""
    
    def __init__(self):
        self.ollama = None
        self.weaviate = None
        self.test_results = {}
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all integration tests"""
        logger.info("Starting Iteration 13 integration tests...")
        
        test_results = {
            'ollama_tests': await self.test_ollama_integration(),
            'weaviate_tests': await self.test_weaviate_integration(),
            'schema_tests': await self.test_weaviate_schemas(),
            'integration_tests': await self.test_ollama_weaviate_integration(),
            'performance_tests': await self.test_performance()
        }
        
        # Summary
        all_passed = all(
            result.get('success', False) 
            for test_suite in test_results.values() 
            for result in test_suite.values()
        )
        
        test_results['summary'] = {
            'all_tests_passed': all_passed,
            'timestamp': time.time()
        }
        
        logger.info(f"All tests completed. Success: {all_passed}")
        return test_results
    
    async def test_ollama_integration(self) -> Dict[str, Any]:
        """Test Ollama integration functionality"""
        logger.info("Testing Ollama integration...")
        results = {}
        
        try:
            self.ollama = OllamaIntegration()
            
            # Test 1: Health check
            try:
                health = await self.ollama.health_check()
                results['health_check'] = {
                    'success': health,
                    'message': 'Ollama health check passed' if health else 'Ollama health check failed'
                }
            except Exception as e:
                results['health_check'] = {
                    'success': False,
                    'message': f'Health check error: {e}'
                }
            
            # Test 2: List models
            try:
                models = await self.ollama.list_models()
                qwen_model_found = any('qwen3-coder' in model.name.lower() for model in models)
                embedding_model_found = any('nomic-embed' in model.name.lower() for model in models)
                
                results['list_models'] = {
                    'success': len(models) > 0,
                    'message': f'Found {len(models)} models',
                    'qwen_model_available': qwen_model_found,
                    'embedding_model_available': embedding_model_found,
                    'models': [model.name for model in models[:5]]  # First 5 models
                }
            except Exception as e:
                results['list_models'] = {
                    'success': False,
                    'message': f'List models error: {e}'
                }
            
            # Test 3: Model loading
            try:
                loaded = await self.ollama.ensure_model_loaded()
                results['model_loading'] = {
                    'success': loaded,
                    'message': 'Model loaded successfully' if loaded else 'Failed to load model'
                }
            except Exception as e:
                results['model_loading'] = {
                    'success': False,
                    'message': f'Model loading error: {e}'
                }
            
            # Test 4: Simple code analysis
            if results.get('model_loading', {}).get('success', False):
                try:
                    test_code = """
                    public class TestClass {
                        private String name;
                        
                        public TestClass(String name) {
                            this.name = name;
                        }
                        
                        public String getName() {
                            return name;
                        }
                    }
                    """
                    
                    start_time = time.time()
                    result = await self.ollama.analyze_code_repository(
                        repository_context=test_code,
                        analysis_type="simple_test"
                    )
                    analysis_time = time.time() - start_time
                    
                    results['code_analysis'] = {
                        'success': len(result.content) > 0,
                        'message': f'Analysis completed in {analysis_time:.2f}s',
                        'tokens_used': result.tokens_used,
                        'context_utilization': result.context_utilization,
                        'processing_time': result.processing_time,
                        'confidence_score': result.confidence_score,
                        'analysis_preview': result.content[:200] + '...' if len(result.content) > 200 else result.content
                    }
                except Exception as e:
                    results['code_analysis'] = {
                        'success': False,
                        'message': f'Code analysis error: {e}'
                    }
            
            # Test 5: Embedding generation
            try:
                test_texts = [
                    "public class Example { }",
                    "function calculateTotal() { return sum; }",
                    "SELECT * FROM users WHERE id = ?"
                ]
                
                embeddings = await self.ollama.generate_embeddings(test_texts)
                results['embeddings'] = {
                    'success': len(embeddings) == len(test_texts) and all(len(emb) > 0 for emb in embeddings),
                    'message': f'Generated {len(embeddings)} embeddings',
                    'embedding_dimensions': len(embeddings[0]) if embeddings and embeddings[0] else 0
                }
            except Exception as e:
                results['embeddings'] = {
                    'success': False,
                    'message': f'Embedding generation error: {e}'
                }
            
        except Exception as e:
            logger.error(f"Ollama integration test failed: {e}")
            results['general_error'] = {
                'success': False,
                'message': f'General Ollama test error: {e}'
            }
        
        return results
    
    async def test_weaviate_integration(self) -> Dict[str, Any]:
        """Test Weaviate integration functionality"""
        logger.info("Testing Weaviate integration...")
        results = {}
        
        try:
            config = WeaviateConfig(
                host='localhost',
                port=8080,
                scheme='http'
            )
            self.weaviate = EnhancedWeaviateConnector(config)
            
            # Test 1: Health check
            try:
                health = await self.weaviate.health_check()
                results['health_check'] = {
                    'success': health['overall'],
                    'message': f'Weaviate health: {health}',
                    'weaviate_ready': health.get('weaviate', False),
                    'ollama_ready': health.get('ollama', False),
                    'schemas_ready': health.get('schemas', False)
                }
            except Exception as e:
                results['health_check'] = {
                    'success': False,
                    'message': f'Health check error: {e}'
                }
            
            # Test 2: Schema management
            try:
                schema_info = self.weaviate.schema_manager.get_schema_info()
                results['schema_info'] = {
                    'success': schema_info.get('classes', 0) > 0,
                    'message': f'Found {schema_info.get("classes", 0)} schema classes',
                    'class_names': schema_info.get('class_names', [])
                }
            except Exception as e:
                results['schema_info'] = {
                    'success': False,
                    'message': f'Schema info error: {e}'
                }
            
        except Exception as e:
            logger.error(f"Weaviate integration test failed: {e}")
            results['general_error'] = {
                'success': False,
                'message': f'General Weaviate test error: {e}'
            }
        
        return results
    
    async def test_weaviate_schemas(self) -> Dict[str, Any]:
        """Test Weaviate schema creation and management"""
        logger.info("Testing Weaviate schemas...")
        results = {}
        
        if not self.weaviate:
            return {'error': {'success': False, 'message': 'Weaviate not initialized'}}
        
        try:
            # Test schema creation
            schema_created = self.weaviate.schema_manager.create_all_schemas()
            results['schema_creation'] = {
                'success': schema_created,
                'message': 'Schemas created successfully' if schema_created else 'Schema creation failed'
            }
            
            # Test schema information retrieval
            schema_info = self.weaviate.schema_manager.get_schema_info()
            expected_classes = ['JavaCodeChunk', 'ArchitecturalPattern', 'BusinessRule', 'IntegrationPoint']
            found_classes = schema_info.get('class_names', [])
            
            results['schema_validation'] = {
                'success': all(cls in found_classes for cls in expected_classes),
                'message': f'Found classes: {found_classes}',
                'expected_classes': expected_classes,
                'missing_classes': [cls for cls in expected_classes if cls not in found_classes]
            }
            
        except Exception as e:
            results['schema_error'] = {
                'success': False,
                'message': f'Schema test error: {e}'
            }
        
        return results
    
    async def test_ollama_weaviate_integration(self) -> Dict[str, Any]:
        """Test integration between Ollama and Weaviate"""
        logger.info("Testing Ollama-Weaviate integration...")
        results = {}
        
        if not self.ollama or not self.weaviate:
            return {'error': {'success': False, 'message': 'Components not initialized'}}
        
        try:
            # Test 1: Create a test code chunk
            test_chunk = CodeChunk(
                content="""
                public class CustomerService {
                    private CustomerRepository repository;
                    
                    @Autowired
                    public CustomerService(CustomerRepository repository) {
                        this.repository = repository;
                    }
                    
                    public Customer findById(Long id) {
                        return repository.findById(id)
                            .orElseThrow(() -> new CustomerNotFoundException(id));
                    }
                    
                    public List<Customer> findAll() {
                        return repository.findAll();
                    }
                }
                """,
                file_path="src/main/java/com/example/service/CustomerService.java",
                start_line=1,
                end_line=20,
                language="java",
                chunk_type=ChunkType.CLASS,
                chunk_id="test_customer_service",
                class_name="CustomerService",
                method_name=None,
                complexity_score=3.5
            )
            
            # Test 2: Insert chunk into Weaviate
            try:
                object_id = self.weaviate.insert_code_chunk(test_chunk, "Test repository context")
                results['chunk_insertion'] = {
                    'success': object_id is not None,
                    'message': f'Chunk inserted with ID: {object_id}',
                    'object_id': object_id
                }
            except Exception as e:
                results['chunk_insertion'] = {
                    'success': False,
                    'message': f'Chunk insertion error: {e}'
                }
            
            # Test 3: Semantic search
            if results.get('chunk_insertion', {}).get('success', False):
                try:
                    search_result = await self.weaviate.semantic_search(
                        query="customer service repository pattern",
                        limit=5,
                        certainty=0.5
                    )
                    
                    results['semantic_search'] = {
                        'success': search_result.total_count > 0,
                        'message': f'Found {search_result.total_count} results in {search_result.query_time:.3f}s',
                        'query_time': search_result.query_time,
                        'context_utilization': search_result.context_utilization,
                        'results_preview': [
                            {
                                'id': obj['id'][:8] + '...',
                                'certainty': obj['metadata'].get('certainty', 0),
                                'file_path': obj['properties'].get('file_path', 'N/A')
                            }
                            for obj in search_result.objects[:3]
                        ]
                    }
                except Exception as e:
                    results['semantic_search'] = {
                        'success': False,
                        'message': f'Semantic search error: {e}'
                    }
            
        except Exception as e:
            results['integration_error'] = {
                'success': False,
                'message': f'Integration test error: {e}'
            }
        
        return results
    
    async def test_performance(self) -> Dict[str, Any]:
        """Test performance characteristics"""
        logger.info("Testing performance...")
        results = {}
        
        if not self.ollama or not self.weaviate:
            return {'error': {'success': False, 'message': 'Components not initialized'}}
        
        try:
            # Performance test 1: Ollama response time
            if self.ollama:
                perf_stats = self.ollama.get_performance_stats()
                results['ollama_performance'] = {
                    'success': True,
                    'message': 'Ollama performance stats retrieved',
                    'stats': perf_stats
                }
            
            # Performance test 2: Weaviate performance
            if self.weaviate:
                perf_stats = self.weaviate.get_performance_stats()
                results['weaviate_performance'] = {
                    'success': True,
                    'message': 'Weaviate performance stats retrieved',
                    'stats': perf_stats
                }
            
        except Exception as e:
            results['performance_error'] = {
                'success': False,
                'message': f'Performance test error: {e}'
            }
        
        return results
    
    async def cleanup(self):
        """Cleanup test resources"""
        try:
            if self.ollama:
                await self.ollama.cleanup()
            if self.weaviate:
                self.weaviate.close()
        except Exception as e:
            logger.error(f"Cleanup error: {e}")

async def main():
    """Run the integration tests"""
    tester = Iteration13Tester()
    
    try:
        results = await tester.run_all_tests()
        
        # Print detailed results
        print("\n" + "="*80)
        print("ITERATION 13 INTEGRATION TEST RESULTS")
        print("="*80)
        
        for test_suite, test_results in results.items():
            if test_suite == 'summary':
                continue
                
            print(f"\n{test_suite.upper().replace('_', ' ')}:")
            print("-" * 40)
            
            for test_name, result in test_results.items():
                status = "✅ PASS" if result.get('success', False) else "❌ FAIL"
                print(f"{status} {test_name}: {result.get('message', 'No message')}")
                
                # Print additional details for some tests
                if test_name == 'code_analysis' and result.get('success'):
                    print(f"      Tokens: {result.get('tokens_used', 0)}")
                    print(f"      Time: {result.get('processing_time', 0):.2f}s")
                    print(f"      Context utilization: {result.get('context_utilization', 0):.1%}")
                elif test_name == 'semantic_search' and result.get('success'):
                    print(f"      Query time: {result.get('query_time', 0):.3f}s")
                    print(f"      Results: {len(result.get('results_preview', []))}")
        
        # Summary
        summary = results.get('summary', {})
        print(f"\n{'='*80}")
        print(f"OVERALL RESULT: {'✅ ALL TESTS PASSED' if summary.get('all_tests_passed') else '❌ SOME TESTS FAILED'}")
        print(f"{'='*80}")
        
        # Save results to file
        with open('test_results_iteration13.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\nDetailed results saved to: test_results_iteration13.json")
        
        return summary.get('all_tests_passed', False)
        
    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        return False
    finally:
        await tester.cleanup()

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)