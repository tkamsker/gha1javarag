from codebase_processor import CodebaseProcessor
import logging
from pathlib import Path
import os
import shutil
import chromadb
from dotenv import load_dotenv
import requests
import json
import base64
import sys
from urllib.parse import urlparse

def setup_logging(debug_mode: bool):
    """Configure logging based on debug mode."""
    log_level = logging.DEBUG if debug_mode else logging.INFO
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('chroma_upload.log')
        ]
    )
    
    # Set specific loggers
    loggers = ['chromadb', 'urllib3', 'requests']
    for logger_name in loggers:
        logging.getLogger(logger_name).setLevel(log_level)
    
    return logging.getLogger(__name__)

def load_config():
    """Load configuration from environment variables."""
    load_dotenv()
    
    # Get and parse the Chroma API URL
    chroma_api_url = os.getenv('CHROMA_API_URL', 'https://chromadb.dev.motorenflug.at')
    # Remove https:// if present
    chroma_host = chroma_api_url.replace('https://', '').replace('http://', '')
    # Always use SSL for ChromaDB
    use_ssl = True
    port = 443  # Default HTTPS port
    
    # Validate required configuration
    cucocalc_path = os.getenv('CUCOCALC_PATH')
    if not cucocalc_path:
        raise ValueError("CUCOCALC_PATH environment variable is required")
    
    chroma_api_key = os.getenv('CHROMA_API_KEY')
    if not chroma_api_key:
        raise ValueError("CHROMA_API_KEY environment variable is required")
    
    return {
        'cucocalc_path': cucocalc_path,
        'local_db_path': os.getenv('LOCAL_DB_PATH', 'chroma_db'),
        'chroma_api_url': chroma_api_url,
        'chroma_host': chroma_host,
        'chroma_port': port,
        'chroma_use_ssl': use_ssl,
        'chroma_api_key': chroma_api_key,
        'collection_name': os.getenv('COLLECTION_NAME', 'cucocalc'),
        'use_remote_db': os.getenv('USE_REMOTE_DB', 'false').lower() == 'true',
        'debug': os.getenv('DEBUG', 'false').lower() == 'true'
    }

def cleanup_database(db_path: str, logger: logging.Logger):
    """Clean up the existing database."""
    try:
        if os.path.exists(db_path):
            logger.debug(f"Cleaning up database at {db_path}")
            shutil.rmtree(db_path)
            logger.info(f"Cleaned up existing database at {db_path}")
    except Exception as e:
        logger.error(f"Error cleaning up database: {str(e)}", exc_info=True)
        raise

def upload_to_remote_chroma(config: dict, logger: logging.Logger):
    """Upload codebase to remote ChromaDB instance."""
    try:
        logger.debug(f"Initializing ChromaDB client with URL: {config['chroma_api_url']}")
        logger.debug(f"Connecting to {config['chroma_host']}:{config['chroma_port']} ssl={config['chroma_use_ssl']}")
        
        # Initialize ChromaDB client with v2 API settings
        client = chromadb.HttpClient(
            host=config['chroma_host'],
            port=config['chroma_port'],
            ssl=config['chroma_use_ssl'],
            headers={
                "X-Chroma-Api-Version": "v2",
                "X-Chroma-Token": config['chroma_api_key']
            }
        )
        
        # Test connection
        try:
            test_url = f"{'https' if config['chroma_use_ssl'] else 'http'}://{config['chroma_host']}:{config['chroma_port']}/api/v2/heartbeat"
            response = requests.get(test_url, verify=config['chroma_use_ssl'])
            response.raise_for_status()
            logger.info("Successfully connected to ChromaDB server")
        except Exception as e:
            logger.error(f"Failed to connect to ChromaDB server: {str(e)}")
            raise
        
        # Create or get collection
        try:
            logger.debug(f"Creating/accessing collection: {config['collection_name']}")
            collection = client.get_or_create_collection(
                name=config['collection_name'],
                metadata={"description": "Cucocalc codebase embeddings"}
            )
            logger.info(f"Successfully created/accessed collection: {config['collection_name']}")
        except Exception as e:
            logger.error(f"Failed to create/access collection: {str(e)}", exc_info=True)
            raise

        # Process the codebase
        logger.debug(f"Initializing CodebaseProcessor with path: {config['cucocalc_path']}")
        processor = CodebaseProcessor(
            codebase_path=config['cucocalc_path'],
            collection=collection,
            batch_size=40000
        )
        
        # Process and upload
        logger.info("Starting codebase processing and upload")
        processor.process_codebase()
        
        logger.info("Successfully uploaded to remote ChromaDB")
        
    except Exception as e:
        logger.error(f"Error uploading to remote ChromaDB: {str(e)}", exc_info=True)
        raise

def upload_cucocalc():
    # Load configuration
    config = load_config()
    
    # Setup logging
    logger = setup_logging(config['debug'])
    
    # Print configuration details
    logger.info("Configuration details:")
    logger.info("-" * 50)
    logger.info(f"CUCOCALC_PATH: {config['cucocalc_path']}")
    logger.info(f"LOCAL_DB_PATH: {config['local_db_path']}")
    logger.info(f"CHROMA_API_URL: {config['chroma_api_url']}")
    logger.info(f"CHROMA_HOST: {config['chroma_host']}")
    logger.info(f"CHROMA_PORT: {config['chroma_port']}")
    logger.info(f"CHROMA_USE_SSL: {config['chroma_use_ssl']}")
    logger.info(f"COLLECTION_NAME: {config['collection_name']}")
    logger.info(f"USE_REMOTE_DB: {config['use_remote_db']}")
    logger.info(f"DEBUG: {config['debug']}")
    logger.info("-" * 50)
    
    try:
        logger.info(f"Using {'remote' if config['use_remote_db'] else 'local'} ChromaDB")
        
        if config['use_remote_db']:
            # Upload to remote ChromaDB
            upload_to_remote_chroma(config, logger)
        else:
            # Clean up existing local database
            cleanup_database(config['local_db_path'], logger)
            
            # Initialize processor with local database
            logger.debug(f"Initializing local processor with path: {config['local_db_path']}")
            processor = CodebaseProcessor(
                codebase_path=config['cucocalc_path'],
                db_path=config['local_db_path'],
                batch_size=40000
            )
            
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
        logger.error(f"Error during upload: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    upload_cucocalc() 