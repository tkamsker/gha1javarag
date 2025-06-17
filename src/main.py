import asyncio
from file_processor import FileProcessor
from ai_analyzer import AIAnalyzer
from chromadb_connector import ChromaDBConnector
from requirements_analyzer import RequirementsAnalyzer
import json
import os
from typing import Dict, Any, List
from dotenv import load_dotenv
from logger_config import setup_logging
import logging

async def process_codebase():
    """Main function to process and analyze the codebase"""
    # Set up logging
    logger = setup_logging(level=logging.DEBUG)
    logger.info("Starting codebase analysis process")
    
    # Load environment variables
    load_dotenv()
    logger.debug("Environment variables loaded")
    
    try:
        # Initialize components
        logger.info("Initializing components...")
        file_processor = FileProcessor()
        ai_analyzer = AIAnalyzer()
        chroma_connector = ChromaDBConnector()
        output_dir = os.getenv('OUTPUT_DIR', './output')
        req_analyzer = RequirementsAnalyzer(output_dir)
        
        # Step 1: Process and analyze files
        logger.info("Step 1: Processing and analyzing files...")
        
        # 1.1 Process files and extract metadata
        logger.info("1.1 Processing files and extracting metadata...")
        files_metadata = file_processor.process_files()
        
        # 1.2 Analyze files with AI
        logger.info("1.2 Analyzing files with AI...")
        analyzed_metadata = await ai_analyzer.analyze_files(files_metadata)
        
        # 1.3 Save raw metadata to JSON
        logger.info("1.3 Saving raw metadata to JSON...")
        metadata_file = os.path.join(output_dir, 'metadata.json')
        file_processor.save_metadata(analyzed_metadata, metadata_file)
        
        # 1.4 Store in ChromaDB
        logger.info("1.4 Storing in ChromaDB...")
        chroma_connector.store_metadata(analyzed_metadata)
        
        # Step 2: Generate requirements documentation
        logger.info("Step 2: Generating requirements documentation...")
        req_analyzer.analyze_and_generate(analyzed_metadata)
        
        logger.info("Process completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during processing: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(process_codebase()) 