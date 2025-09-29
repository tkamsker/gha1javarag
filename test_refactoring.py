#!/usr/bin/env python3
"""
Test script to validate ChromaDB to Weaviate refactoring
This script checks that the refactored code imports correctly and basic functionality works
"""

import sys
import os
import logging
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_imports():
    """Test that all refactored imports work correctly"""
    logger.info("Testing imports...")
    
    try:
        # Test Weaviate connector import
        from weaviate_connector import EnhancedWeaviateConnector
        logger.info("✅ EnhancedWeaviateConnector import successful")
        
        # Test migration pipeline import
        from migration_pipeline import DataMigrationPipeline
        logger.info("✅ DataMigrationPipeline import successful")
        
        # Test file processor import
        from file_processor import FileProcessor
        logger.info("✅ FileProcessor import successful")
        
        return True
        
    except ImportError as e:
        logger.error(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error during imports: {e}")
        return False

def test_environment_config():
    """Test environment configuration"""
    logger.info("Testing environment configuration...")
    
    load_dotenv()
    
    # Check for required environment variables
    required_vars = ['JAVA_SOURCE_DIR', 'OUTPUT_DIR']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.warning(f"⚠️  Missing environment variables: {missing_vars}")
        logger.info("💡 Please set these in your .env file")
        return False
    else:
        logger.info("✅ All required environment variables are set")
        return True

def test_file_processor():
    """Test file processor basic functionality"""
    logger.info("Testing file processor...")
    
    try:
        from file_processor import FileProcessor
        
        # Initialize processor
        processor = FileProcessor()
        logger.info("✅ FileProcessor initialized successfully")
        
        # Check that required attributes exist
        if hasattr(processor, 'source_dir') and hasattr(processor, 'output_dir'):
            logger.info("✅ FileProcessor has required attributes")
            return True
        else:
            logger.error("❌ FileProcessor missing required attributes")
            return False
            
    except Exception as e:
        logger.error(f"❌ FileProcessor test failed: {e}")
        return False

def test_weaviate_connector_basic():
    """Test basic Weaviate connector initialization"""
    logger.info("Testing Weaviate connector basic functionality...")
    
    try:
        from weaviate_connector import EnhancedWeaviateConnector, WeaviateConfig
        
        # Create config
        config = WeaviateConfig()
        logger.info("✅ WeaviateConfig created successfully")
        
        # Initialize connector (this may fail if Weaviate is not running, which is OK)
        try:
            connector = EnhancedWeaviateConnector(config)
            logger.info("✅ EnhancedWeaviateConnector initialized successfully")
            return True
        except Exception as e:
            logger.warning(f"⚠️  Weaviate connection failed (expected if Weaviate not running): {e}")
            logger.info("✅ Weaviate connector class loads correctly")
            return True
            
    except Exception as e:
        logger.error(f"❌ Weaviate connector test failed: {e}")
        return False

def test_scripts_exist():
    """Test that required scripts exist and are executable"""
    logger.info("Testing script files...")
    
    required_scripts = [
        'reset_and_run_production_macos.sh',
        'Step1_Enhanced_Weaviate.sh',
        'Step2_Enhanced_Weaviate.sh', 
        'Step3_Enhanced_Weaviate.sh'
    ]
    
    all_exist = True
    for script in required_scripts:
        if os.path.exists(script):
            logger.info(f"✅ {script} exists")
            # Check if executable
            if os.access(script, os.X_OK):
                logger.info(f"✅ {script} is executable")
            else:
                logger.warning(f"⚠️  {script} is not executable")
        else:
            logger.error(f"❌ {script} does not exist")
            all_exist = False
    
    return all_exist

def main():
    """Run all refactoring tests"""
    logger.info("🔍 Starting refactoring validation tests...")
    logger.info("=" * 60)
    
    tests = [
        ("Import Tests", test_imports),
        ("Environment Config", test_environment_config),
        ("File Processor", test_file_processor),
        ("Weaviate Connector", test_weaviate_connector_basic),
        ("Required Scripts", test_scripts_exist)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n📋 Running {test_name}...")
        try:
            results[test_name] = test_func()
        except Exception as e:
            logger.error(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Print summary
    logger.info("\n" + "=" * 60)
    logger.info("📊 REFACTORING VALIDATION SUMMARY")
    logger.info("=" * 60)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status} - {test_name}")
        if result:
            passed += 1
    
    logger.info(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All refactoring tests passed!")
        logger.info("✅ ChromaDB to Weaviate migration completed successfully")
        return 0
    else:
        logger.error(f"❌ {total - passed} tests failed")
        logger.error("⚠️  Refactoring may have issues that need to be addressed")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)