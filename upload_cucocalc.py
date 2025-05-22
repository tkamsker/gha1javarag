from codebase_processor import CodebaseProcessor
import logging
from pathlib import Path
import os
import shutil
import chromadb

def cleanup_database(db_path: str):
    """Clean up the existing database."""
    try:
        if os.path.exists(db_path):
            shutil.rmtree(db_path)
            logging.info(f"Cleaned up existing database at {db_path}")
    except Exception as e:
        logging.error(f"Error cleaning up database: {str(e)}")
        raise

def upload_cucocalc():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    # Path to Cucocalc application
    cucocalc_path = "/Users/thomaskamsker/Desktop/AKT_Docs/2025/AI/Cucocalc/code/cuco-master@d34bb6b6d1c"
    db_path = "chroma_db_cucocalc"
    
    # Clean up existing database
    cleanup_database(db_path)
    
    # Initialize processor with a specific database name for Cucocalc
    processor = CodebaseProcessor(
        codebase_path=cucocalc_path,
        db_path=db_path,
        batch_size=40000  # Set batch size below ChromaDB's limit
    )

    try:
        logger.info("Starting Cucocalc codebase upload...")
        processor.process_codebase()
        logger.info("Cucocalc codebase upload completed!")
        
        # Test the upload with some sample queries
        test_queries = [
            "Find main application entry point",
            "Show me database connection code",
            "Find user authentication methods",
            "Show me calculation related code"
        ]
        
        logger.info("\nTesting search functionality:")
        for query in test_queries:
            logger.info(f"\nSearching for: {query}")
            results = processor.search(query, n_results=3)
            for result in results:
                logger.info(f"\nFound: {result['metadata']['path']}")
                logger.info(f"Type: {result['metadata']['type']}")
                if result['metadata']['type'] == 'method':
                    logger.info(f"Class: {result['metadata']['class']}")
                    logger.info(f"Method: {result['metadata']['name']}")
                elif result['metadata']['type'] == 'class':
                    logger.info(f"Class: {result['metadata']['name']}")

    except Exception as e:
        logger.error(f"Error during upload: {str(e)}")
        raise

if __name__ == "__main__":
    upload_cucocalc() 