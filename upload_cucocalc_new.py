import chromadb
import logging
import os
import requests
from dotenv import load_dotenv
from pathlib import Path

def setup_logging(debug_mode: bool):
    """Configure logging based on debug mode."""
    log_level = logging.DEBUG if debug_mode else logging.INFO
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=log_level, format=log_format)
    return logging.getLogger(__name__)

def load_config():
    """Load configuration from environment variables."""
    load_dotenv()
    chroma_api_url = os.getenv('CHROMA_API_URL', 'https://chromadb.dev.motorenflug.at')
    chroma_api_key = os.getenv('CHROMA_API_KEY')
    tenant = os.getenv('CHROMA_TENANT', 'default_tenant')
    database = os.getenv('CHROMA_DATABASE', 'default_database')
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    return {
        'chroma_api_url': chroma_api_url,
        'chroma_api_key': chroma_api_key,
        'tenant': tenant,
        'database': database,
        'debug': debug
    }

def test_connection(config, logger):
    """Test connection to ChromaDB server and verify tenant/database existence."""
    try:
        # Test heartbeat
        heartbeat_url = f"{config['chroma_api_url']}/api/v2/heartbeat"
        response = requests.get(heartbeat_url, headers={"X-Chroma-Token": config['chroma_api_key']})
        response.raise_for_status()
        logger.info("Successfully connected to ChromaDB server")

        # Test tenant existence
        tenant_url = f"{config['chroma_api_url']}/api/v2/tenants/{config['tenant']}"
        response = requests.get(tenant_url, headers={"X-Chroma-Token": config['chroma_api_key']})
        response.raise_for_status()
        logger.info(f"Tenant {config['tenant']} exists")

        # Test database existence
        db_url = f"{config['chroma_api_url']}/api/v2/tenants/{config['tenant']}/databases"
        response = requests.get(db_url, headers={"X-Chroma-Token": config['chroma_api_key']})
        response.raise_for_status()
        logger.info(f"Database {config['database']} exists under tenant {config['tenant']}")

    except Exception as e:
        logger.error(f"Connection test failed: {str(e)}")
        raise

def upload_to_remote_chroma(config, logger):
    """Upload codebase to remote ChromaDB instance using a simplified client initialization."""
    try:
        # Test connection and tenant/database existence
        test_connection(config, logger)

        # Initialize ChromaDB client with direct host, port, and API key
        parsed_url = urlparse(config['chroma_api_url'])
        host = parsed_url.hostname
        port = 443

        client = chromadb.HttpClient(
            host=host,
            port=port,
            headers={"X-Chroma-Token": config['chroma_api_key']},
            tenant=config['tenant'],
            database=config['database']
        )

        # Example: Get or create a collection
        collection = client.get_or_create_collection(
            name="cucocalc",
            metadata={"description": "Java code snippets and their embeddings"}
        )

        # TODO: Add your codebase processing and upload logic here
        logger.info("ChromaDB client initialized successfully. Ready for upload.")

    except Exception as e:
        logger.error(f"Error uploading to remote ChromaDB: {str(e)}", exc_info=True)
        raise

def main():
    config = load_config()
    logger = setup_logging(config['debug'])
    upload_to_remote_chroma(config, logger)

if __name__ == "__main__":
    main() 