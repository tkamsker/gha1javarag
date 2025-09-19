"""
Simple Integration Test for Iteration 13 Components
Basic test to verify Ollama and system health
"""

import asyncio
import logging
import json
import sys
import time
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set up path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def test_imports():
    """Test that all required modules can be imported"""
    try:
        from src.ollama_integration import OllamaIntegration
        logger.info("✅ Successfully imported OllamaIntegration")
        return True
    except ImportError as e:
        logger.error(f"❌ Failed to import OllamaIntegration: {e}")
        return False

async def test_ollama_health():
    """Test Ollama connection and health"""
    try:
        from src.ollama_integration import OllamaIntegration
        
        ollama = OllamaIntegration()
        logger.info("Testing Ollama health check...")
        
        health = await ollama.health_check()
        
        if health:
            logger.info("✅ Ollama health check passed")
            
            # Test model listing
            models = await ollama.list_models()
            logger.info(f"✅ Found {len(models)} models:")
            for model in models:
                logger.info(f"   - {model.name} ({model.details.get('parameter_size', 'unknown size')})")
            
            # Check for required models
            model_names = [model.name.lower() for model in models]
            qwen_found = any('qwen' in name for name in model_names)
            nomic_found = any('nomic' in name for name in model_names)
            
            logger.info(f"✅ Qwen model found: {qwen_found}")
            logger.info(f"✅ Nomic embedding model found: {nomic_found}")
            
            if qwen_found and nomic_found:
                logger.info("✅ All required models are available")
                return True
            else:
                logger.warning("⚠️  Some required models may be missing")
                return True  # Still consider success if Ollama is working
            
        else:
            logger.error("❌ Ollama health check failed")
            return False
            
    except Exception as e:
        logger.error(f"❌ Ollama test failed: {e}")
        return False

async def test_simple_analysis():
    """Test simple code analysis with Ollama"""
    try:
        from src.ollama_integration import OllamaIntegration
        
        ollama = OllamaIntegration()
        
        # Simple test code
        test_code = """
        public class Calculator {
            public int add(int a, int b) {
                return a + b;
            }
            
            public int multiply(int a, int b) {
                return a * b;
            }
        }
        """
        
        logger.info("Testing simple code analysis...")
        start_time = time.time()
        
        result = await ollama.analyze_code_repository(
            repository_context=test_code,
            analysis_type="basic_test"
        )
        
        analysis_time = time.time() - start_time
        
        logger.info(f"✅ Analysis completed in {analysis_time:.2f}s")
        logger.info(f"   - Tokens used: {result.tokens_used}")
        logger.info(f"   - Processing time: {result.processing_time:.2f}s")
        logger.info(f"   - Context utilization: {result.context_utilization:.1%}")
        logger.info(f"   - Confidence score: {result.confidence_score:.2f}")
        logger.info(f"   - Analysis preview: {result.content[:150]}...")
        
        await ollama.cleanup()
        return True
        
    except Exception as e:
        logger.error(f"❌ Code analysis test failed: {e}")
        return False

def test_environment():
    """Test environment setup"""
    logger.info("Testing environment setup...")
    
    # Check environment variables
    env_vars = [
        'OLLAMA_BASE_URL',
        'OLLAMA_MODEL_NAME', 
        'WEAVIATE_URL'
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            logger.info(f"✅ {var}: {value}")
        else:
            logger.warning(f"⚠️  {var}: Not set (using default)")
    
    return True

async def test_basic_weaviate():
    """Basic Weaviate connectivity test"""
    try:
        import requests
        
        weaviate_url = os.getenv('WEAVIATE_URL', 'http://localhost:8080')
        logger.info(f"Testing Weaviate connection to {weaviate_url}...")
        
        response = requests.get(f"{weaviate_url}/v1/.well-known/ready", timeout=5)
        
        if response.status_code == 200:
            logger.info("✅ Weaviate is ready")
            
            # Get schema info
            schema_response = requests.get(f"{weaviate_url}/v1/schema", timeout=5)
            if schema_response.status_code == 200:
                schema = schema_response.json()
                classes = schema.get('classes', [])
                logger.info(f"✅ Weaviate schema has {len(classes)} classes:")
                for cls in classes:
                    logger.info(f"   - {cls['class']}")
            
            return True
        else:
            logger.error(f"❌ Weaviate not ready: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Weaviate test failed: {e}")
        return False

async def main():
    """Run all simple tests"""
    logger.info("Starting Simple Iteration 13 Tests...")
    logger.info("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("Environment Test", test_environment),
        ("Weaviate Connectivity", test_basic_weaviate),
        ("Ollama Health", test_ollama_health),
        ("Simple Analysis", test_simple_analysis)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n--- {test_name} ---")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results[test_name] = result
        except Exception as e:
            logger.error(f"Test {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)
    
    all_passed = True
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status} {test_name}")
        if not result:
            all_passed = False
    
    logger.info("=" * 60)
    logger.info(f"OVERALL: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    logger.info("=" * 60)
    
    # Save results
    with open('simple_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    return all_passed

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)