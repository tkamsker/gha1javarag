import asyncio
import os
import logging
from pathlib import Path
from typing import Dict, Any, List
from dotenv import load_dotenv
from logger_config import setup_logging
from requirements_generator import RequirementsGenerator

async def generate_requirements():
    """Main function to generate requirements documentation from existing metadata"""
    # Set up logging
    logger = setup_logging(level=logging.DEBUG)
    logger.info("Starting requirements generation process")
    
    # Load environment variables
    load_dotenv()
    logger.debug("Environment variables loaded")
    
    try:
        # Get configuration from environment variables
        output_dir = os.getenv('OUTPUT_DIR', './output')
        metadata_file = os.path.join(output_dir, 'metadata.json')
        
        # Verify metadata file exists
        if not os.path.exists(metadata_file):
            logger.error(f"Metadata file not found: {metadata_file}")
            raise FileNotFoundError(f"Metadata file not found: {metadata_file}")
            
        # Initialize requirements generator
        logger.info("Initializing requirements generator...")
        req_generator = RequirementsGenerator(metadata_file, output_dir)
        
        # Generate documentation with AI enrichment
        logger.info("Generating documentation with AI enrichment...")
        await req_generator.generate_documentation()
        
        logger.info("Requirements generation completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during requirements generation: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(generate_requirements()) 