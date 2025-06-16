from ast_processor import ASTProcessor
from chromadb_connector import ChromaDBConnector
import logging
import os
from dotenv import load_dotenv
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize components
    doxygen_xml_dir = os.getenv('XML_INPUT_DIR')
    if not doxygen_xml_dir:
        logger.error("XML_INPUT_DIR environment variable is not set")
        sys.exit(1)
        
    if not os.path.exists(doxygen_xml_dir):
        logger.error(f"Doxygen XML directory not found: {doxygen_xml_dir}")
        sys.exit(1)
        
    db_connector = ChromaDBConnector()
    
    try:
        # Process AST data
        logger.info("Processing AST data...")
        ast_processor = ASTProcessor(doxygen_xml_dir)
        ast_processor.process_and_store()
        
        # Test queries
        logger.info("\nTesting queries...")
        
        # Query for classes
        class_results = db_connector.query("class", n_results=3)
        logger.info("\nClass Query Results:")
        for i, (doc, metadata) in enumerate(zip(class_results['documents'][0], class_results['metadatas'][0])):
            if metadata['type'] == 'class':
                logger.info(f"\nResult {i+1}:")
                logger.info(f"Name: {metadata['name']}")
                logger.info(f"Preview: {doc[:200]}...")
        
        # Query for methods
        method_results = db_connector.query("method", n_results=3)
        logger.info("\nMethod Query Results:")
        for i, (doc, metadata) in enumerate(zip(method_results['documents'][0], method_results['metadatas'][0])):
            if metadata['type'] == 'method':
                logger.info(f"\nResult {i+1}:")
                logger.info(f"Class: {metadata['class']}")
                logger.info(f"Method: {metadata['name']}")
                logger.info(f"Preview: {doc[:200]}...")
        
    except Exception as e:
        logger.error(f"Error during testing: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 