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
    """Load configuration from .env file."""
    load_dotenv()
    
    # Get the base URL and ensure it's properly formatted
    chroma_api_url = os.getenv('CHROMA_API_URL', 'https://chromadb.dev.motorenflug.at')
    if not chroma_api_url.startswith(('http://', 'https://')):
        chroma_api_url = f'https://{chroma_api_url}'
    
    # Remove any port from the URL
    if ':' in chroma_api_url:
        chroma_api_url = chroma_api_url.split(':')[0]
    
    config = {
        'cucocalc_path': os.getenv('CUCOCALC_PATH'),
        'local_db_path': os.getenv('LOCAL_DB_PATH'),
        'chroma_api_url': chroma_api_url,
        'use_remote_db': os.getenv('USE_REMOTE_DB', 'false').lower() == 'true',
        'chroma_api_key': os.getenv('CHROMA_API_KEY', ''),
        'collection_name': os.getenv('COLLECTION_NAME', 'cucocalc_codebase'),
        'debug': os.getenv('DEBUG', 'false').lower() == 'true'
    }
    
    # Validate required configuration
    if not config['cucocalc_path']:
        raise ValueError("CUCOCALC_PATH not set in .env file")
    
    if config['use_remote_db'] and not config['chroma_api_key']:
        raise ValueError("CHROMA_API_KEY required for remote ChromaDB")
    
    return config

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
        
        # Get the plain hostname without any protocol or port
        base_url = config['chroma_api_url'].replace('https://', '').replace('http://', '').split(':')[0]
        logger.debug(f"Using base URL: {base_url}")
        
        # Initialize ChromaDB client with remote settings
        client = chromadb.HttpClient(
            host=base_url,
            ssl=True,
            headers={
                "X-Chroma-Token": config['chroma_api_key'],
                "X-Chroma-Api-Version": "v2"
            },
            settings=chromadb.Settings(
                chroma_api_impl="rest",
                chroma_server_host=base_url,
                allow_reset=True,
                anonymized_telemetry=False,
                chroma_server_cors_allow_origins=["*"]
            )
        )
        
        # Test connection before proceeding
        try:
            logger.debug("Testing connection to ChromaDB server")
            response = requests.get(
                f"https://{base_url}/api/v2",
                headers={
                    "X-Chroma-Token": config['chroma_api_key'],
                    "X-Chroma-Api-Version": "v2"
                },
                verify=True
            )
            response.raise_for_status()
            logger.info("Successfully connected to ChromaDB server")
            logger.debug(f"Server response: {response.text}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect to ChromaDB server: {str(e)}", exc_info=True)
            raise

        # Get or create collection with v2 API
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