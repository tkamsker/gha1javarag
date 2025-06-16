from chromadb_connector import ChromaDBConnector
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    # Initialize ChromaDB connector
    db_connector = ChromaDBConnector()
    
    # Get collection info
    collection = db_connector.get_collection()
    count = collection.count()
    logger.info(f"Total documents in collection: {count}")
    
    # Query example
    results = db_connector.query("class", n_results=3)
    
    # Print results
    logger.info("\nQuery Results:")
    for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
        logger.info(f"\nResult {i+1}:")
        logger.info(f"Source: {metadata['source']}")
        logger.info(f"Type: {metadata['file_type']}")
        logger.info(f"Preview: {doc[:200]}...")

if __name__ == "__main__":
    main() 