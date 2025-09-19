"""
Small Test of Fresh Java Analysis
Process a small subset of files to validate the approach
"""

import asyncio
import logging
import json
import sys
import os
import time
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set up path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

async def main():
    """Test fresh analysis with a small subset"""
    logger.info("🧪 Testing Fresh Java Analysis (Small Subset)")
    logger.info("=" * 50)
    
    try:
        from src.fresh_java_processor import FreshJavaProcessor
        from src.weaviate_connector import WeaviateConfig
        from src.ollama_integration import OllamaIntegration
        
        # Initialize components
        weaviate_config = WeaviateConfig(host='localhost', port=8080, scheme='http')
        ollama = OllamaIntegration()
        
        # Check health first
        logger.info("🏥 Checking system health...")
        
        ollama_health = await ollama.health_check()
        if not ollama_health:
            logger.error("❌ Ollama health check failed")
            return False
        
        logger.info("✅ Ollama is healthy")
        
        # Initialize processor
        java_root_path = "/Users/thomaskamsker/Documents/Atom/vron.one/playground/java"
        processor = FreshJavaProcessor(java_root_path, weaviate_config, ollama)
        
        # Check Weaviate health
        await processor._initialize_weaviate()
        logger.info("✅ Weaviate is healthy and schemas ready")
        
        # Discover files (but limit to first 10 Java files for testing)
        logger.info("🔍 Discovering files...")
        all_files = processor._discover_files()
        
        # Filter to just Java files and take first 10
        java_files = [f for f in all_files if f.file_type == 'java'][:10]
        xml_files = [f for f in all_files if f.file_type == 'xml'][:5]
        sql_files = [f for f in all_files if f.file_type == 'sql'][:3]
        
        test_files = java_files + xml_files + sql_files
        
        logger.info(f"📊 Selected {len(test_files)} files for testing:")
        logger.info(f"   - {len(java_files)} Java files")
        logger.info(f"   - {len(xml_files)} XML files") 
        logger.info(f"   - {len(sql_files)} SQL files")
        
        # Show some sample file paths
        for i, file_info in enumerate(test_files[:5]):
            logger.info(f"   {i+1}. {Path(file_info.file_path).name} ({file_info.file_type}) - {file_info.module_name}")
        
        # Process the test batch
        logger.info("⚙️ Processing test batch...")
        start_time = time.time()
        
        await processor._process_file_batch(test_files)
        
        processing_time = time.time() - start_time
        
        logger.info(f"✅ Test batch processed in {processing_time:.2f}s")
        
        # Test semantic search
        logger.info("🔍 Testing semantic search...")
        search_result = await processor.weaviate.semantic_search(
            query="java class service controller",
            limit=5,
            certainty=0.3
        )
        
        logger.info(f"📊 Search found {search_result.total_count} results")
        for i, obj in enumerate(search_result.objects[:3]):
            props = obj['properties']
            certainty = obj['metadata'].get('certainty', 0)
            file_path = Path(props.get('file_path', 'unknown')).name
            logger.info(f"   {i+1}. {file_path} (certainty: {certainty:.2f})")
        
        # Test simple analysis with one file
        if java_files:
            logger.info("🧠 Testing Qwen analysis with sample file...")
            sample_file = java_files[0]
            
            with open(sample_file.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                sample_content = f.read()[:2000]  # First 2000 chars
            
            analysis_result = await ollama.analyze_code_repository(
                repository_context=f"Sample Java file analysis:\n{sample_content}",
                analysis_type="single_file_test"
            )
            
            logger.info(f"✅ Analysis completed: {analysis_result.tokens_used} tokens, "
                       f"{analysis_result.processing_time:.2f}s")
            logger.info(f"📝 Analysis preview: {analysis_result.content[:200]}...")
        
        # Get stats
        stats = processor.get_processing_summary()
        
        logger.info("=" * 50)
        logger.info("✅ SMALL TEST COMPLETED SUCCESSFULLY")
        logger.info("=" * 50)
        logger.info(f"📊 Files tested: {len(test_files)}")
        logger.info(f"⏱️ Processing time: {processing_time:.2f}s")
        logger.info(f"🔍 Search results: {search_result.total_count}")
        logger.info("=" * 50)
        
        # Cleanup
        await processor.cleanup()
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Small test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)