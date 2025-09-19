"""
Run Fresh Java Analysis
Process the Java enterprise application dataset directly into Weaviate
"""

import asyncio
import logging
import json
import sys
import os
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('fresh_analysis.log')
    ]
)
logger = logging.getLogger(__name__)

# Set up path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

async def main():
    """Run the fresh analysis on Java dataset"""
    logger.info("🚀 Starting Fresh Java Analysis")
    logger.info("=" * 60)
    
    # Configuration
    java_root_path = "/Users/thomaskamsker/Documents/Atom/vron.one/playground/java"
    
    if not Path(java_root_path).exists():
        logger.error(f"❌ Java root path does not exist: {java_root_path}")
        return False
    
    try:
        from src.fresh_java_processor import process_java_repository
        from src.weaviate_connector import WeaviateConfig
        
        # Configure Weaviate
        weaviate_config = WeaviateConfig(
            host='localhost',
            port=8080,
            scheme='http'
        )
        
        logger.info(f"📁 Processing Java repository: {java_root_path}")
        
        # Process the repository
        stats = await process_java_repository(
            java_root_path=java_root_path,
            weaviate_config=weaviate_config,
            batch_size=30  # Smaller batches for development
        )
        
        # Save results
        results = {
            'repository_path': java_root_path,
            'processing_stats': {
                'total_files': stats.total_files,
                'processed_files': stats.processed_files,
                'failed_files': stats.failed_files,
                'java_files': stats.java_files,
                'xml_files': stats.xml_files,
                'sql_files': stats.sql_files,
                'total_lines': stats.total_lines,
                'total_size_bytes': stats.total_size_bytes,
                'processing_time': stats.processing_time,
                'qwen_analysis_time': stats.qwen_analysis_time,
                'weaviate_insertion_time': stats.weaviate_insertion_time
            },
            'success_metrics': {
                'success_rate': (stats.processed_files / stats.total_files * 100) if stats.total_files > 0 else 0,
                'files_per_second': stats.processed_files / stats.processing_time if stats.processing_time > 0 else 0,
                'repository_size_mb': stats.total_size_bytes / 1024 / 1024
            }
        }
        
        # Save to file
        timestamp = int(time.time())
        results_file = f'fresh_analysis_results_{timestamp}.json'
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.info("=" * 60)
        logger.info("🎉 FRESH JAVA ANALYSIS COMPLETE")
        logger.info("=" * 60)
        logger.info(f"📊 Processed: {stats.processed_files}/{stats.total_files} files")
        logger.info(f"✅ Success Rate: {results['success_metrics']['success_rate']:.1f}%")
        logger.info(f"⚡ Performance: {results['success_metrics']['files_per_second']:.1f} files/sec")
        logger.info(f"📁 Repository Size: {results['success_metrics']['repository_size_mb']:.1f} MB")
        logger.info(f"⏱️ Total Time: {stats.processing_time:.2f}s")
        logger.info(f"🧠 Qwen Analysis: {stats.qwen_analysis_time:.2f}s")
        logger.info(f"💾 Weaviate Insertion: {stats.weaviate_insertion_time:.2f}s")
        logger.info(f"💼 Java Files: {stats.java_files}")
        logger.info(f"📄 XML Files: {stats.xml_files}")
        logger.info(f"🗃️ SQL Files: {stats.sql_files}")
        logger.info(f"📝 Total Lines: {stats.total_lines:,}")
        logger.info(f"📋 Results saved to: {results_file}")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Fresh analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import time
    success = asyncio.run(main())
    sys.exit(0 if success else 1)