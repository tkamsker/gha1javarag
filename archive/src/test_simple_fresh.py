"""
Test Simple Fresh Java Analysis
Process Java enterprise application with simplified approach
"""

import asyncio
import logging
import sys
import os
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set up path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

async def main():
    """Run the simple fresh analysis"""
    logger.info("🚀 Simple Fresh Java Analysis")
    logger.info("=" * 50)
    
    java_root_path = "/Users/thomaskamsker/Documents/Atom/vron.one/playground/java"
    
    try:
        from src.simple_fresh_processor import process_java_sample
        
        logger.info(f"📁 Processing Java repository: {java_root_path}")
        logger.info(f"🎯 Sample size: 30 files maximum")
        
        start_time = time.time()
        
        # Process sample
        results = await process_java_sample(
            java_root_path=java_root_path,
            max_files=30  # Small sample for testing
        )
        
        total_time = time.time() - start_time
        
        # Display results
        logger.info("=" * 50)
        logger.info("✅ ANALYSIS COMPLETE")
        logger.info("=" * 50)
        logger.info(f"📊 Files processed: {results.processed_files}/{results.total_files}")
        logger.info(f"📁 Java files: {results.java_files}")
        logger.info(f"📄 XML files: {results.xml_files}")
        logger.info(f"🗃️ SQL files: {results.sql_files}")
        logger.info(f"⏱️ Total time: {total_time:.2f}s")
        logger.info(f"⚡ Processing time: {results.processing_time:.2f}s")
        
        success_rate = (results.processed_files / results.total_files * 100) if results.total_files > 0 else 0
        logger.info(f"✅ Success rate: {success_rate:.1f}%")
        
        # Show some analysis highlights
        if results.analysis_results:
            qwen_analyses = [r for r in results.analysis_results if 'qwen_analysis' in r]
            logger.info(f"🧠 Qwen analyses: {len(qwen_analyses)}")
            
            if qwen_analyses:
                avg_tokens = sum(r['qwen_analysis'].get('tokens_used', 0) for r in qwen_analyses) / len(qwen_analyses)
                avg_time = sum(r['qwen_analysis'].get('processing_time', 0) for r in qwen_analyses) / len(qwen_analyses)
                logger.info(f"📊 Average tokens per analysis: {avg_tokens:.0f}")
                logger.info(f"⏱️ Average analysis time: {avg_time:.2f}s")
        
        # Show repository analysis preview
        if results.repository_analysis:
            preview_length = min(300, len(results.repository_analysis))
            logger.info(f"🏗️ Repository analysis preview:")
            logger.info(f"   {results.repository_analysis[:preview_length]}...")
        
        logger.info("=" * 50)
        logger.info("📁 Results saved to output/ directory")
        logger.info("=" * 50)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)