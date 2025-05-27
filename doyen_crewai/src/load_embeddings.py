"""Script for loading code embeddings into ChromaDB."""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

from .preprocessing.xml_parser import DoxygenXMLParser
from .preprocessing.embedding_generator import OllamaEmbeddingGenerator
from .preprocessing.chroma_loader import ChromaDBLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_embeddings():
    """Load code embeddings into ChromaDB."""
    # Load environment variables
    load_dotenv()
    
    # Get configuration from environment
    xml_input_dir = os.getenv("XML_INPUT_DIR")
    ollama_api_url = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
    ollama_model = os.getenv("OLLAMA_MODEL", "all-minilm")
    chroma_persist_dir = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
    
    if not xml_input_dir:
        raise ValueError("XML_INPUT_DIR environment variable is not set")
    
    try:
        # Initialize XML parser
        logger.info("Initializing XML parser...")
        parser = DoxygenXMLParser(xml_input_dir)
        
        # Parse XML files
        logger.info("Parsing XML files...")
        entities = parser.parse_all()
        logger.info(f"Found {len(entities)} code entities")
        
        # Initialize embedding generator
        logger.info("Initializing embedding generator...")
        embedding_gen = OllamaEmbeddingGenerator(
            api_url=ollama_api_url,
            model=ollama_model
        )
        
        # Generate embeddings
        logger.info("Generating embeddings...")
        embeddings = embedding_gen.batch_generate_embeddings(entities)
        logger.info(f"Generated {len(embeddings)} embeddings")
        
        # Initialize ChromaDB loader
        logger.info("Initializing ChromaDB loader...")
        chroma_loader = ChromaDBLoader(persist_directory=chroma_persist_dir)
        
        # Clear existing data
        logger.info("Clearing existing ChromaDB data...")
        chroma_loader.clear_collection()
        
        # Load embeddings into ChromaDB
        logger.info("Loading embeddings into ChromaDB...")
        chroma_loader.load_embeddings(entities, embeddings)
        
        # Get and log collection stats
        stats = chroma_loader.get_collection_stats()
        logger.info(f"ChromaDB collection stats: {stats}")
        
        logger.info("Embedding loading complete!")
        
    except Exception as e:
        logger.error(f"Error during embedding loading: {str(e)}")
        raise

if __name__ == "__main__":
    load_embeddings() 