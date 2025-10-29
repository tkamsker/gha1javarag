#!/usr/bin/env python3
"""Main entry point for the Requirements Extraction Pipeline"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.pipeline import RequirementsExtractionPipeline
from src.utils.logger import setup_logger

logger = setup_logger("main")


def main():
    """Main entry point"""
    try:
        pipeline = RequirementsExtractionPipeline()
        result = pipeline.run()
        
        logger.info("\nPipeline execution completed successfully!")
        logger.info(f"Projects processed: {len(result.get('projects', []))}")
        
        return 0
    except KeyboardInterrupt:
        logger.info("\nPipeline interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1
    finally:
        try:
            pipeline.close()
        except:
            pass


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

