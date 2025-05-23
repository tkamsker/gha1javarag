from codebase_processor import CodebaseProcessor
import logging
import os
from dotenv import load_dotenv
import argparse

def setup_logging():
    """Configure logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def load_config():
    """Load configuration from environment variables."""
    load_dotenv()
    
    return {
        'local_db_path': os.getenv('LOCAL_DB_PATH', 'chroma_db'),
        'debug': os.getenv('DEBUG', 'false').lower() == 'true'
    }

def search_codebase(query: str, n_results: int = 5):
    """Search the codebase for relevant code."""
    # Load configuration
    config = load_config()
    
    # Setup logging
    logger = setup_logging()
    
    try:
        # Initialize processor
        processor = CodebaseProcessor(
            codebase_path="java_codebase",  # This is just a placeholder since we're only searching
            db_path=config['local_db_path'],
            batch_size=40000
        )
        
        # Perform search
        logger.info(f"Searching for: {query}")
        results = processor.search(query, n_results=n_results)
        
        # Print results
        if not results:
            logger.info("No results found.")
            return
        
        logger.info(f"\nFound {len(results)} results:")
        for i, result in enumerate(results, 1):
            logger.info(f"\nResult {i}:")
            logger.info(f"Path: {result['metadata']['path']}")
            logger.info(f"Type: {result['metadata']['type']}")
            if result['metadata']['type'] == 'method':
                logger.info(f"Class: {result['metadata']['class']}")
                logger.info(f"Method: {result['metadata']['name']}")
            elif result['metadata']['type'] == 'class':
                logger.info(f"Class: {result['metadata']['name']}")
            logger.info(f"Content: {result['code']}")
            
    except Exception as e:
        logger.error(f"Error searching codebase: {str(e)}", exc_info=True)
        raise

def main():
    parser = argparse.ArgumentParser(description='Search the Java codebase using semantic search.')
    parser.add_argument('query', help='The search query')
    parser.add_argument('--results', '-n', type=int, default=5, help='Number of results to return (default: 5)')
    
    args = parser.parse_args()
    search_codebase(args.query, args.results)

if __name__ == "__main__":
    main() 