"""Script for loading code embeddings into ChromaDB."""

import logging
import os
from pathlib import Path
import traceback

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
    try:
        load_dotenv()
        xml_input_dir = os.getenv("XML_INPUT_DIR")
        ollama_api_url = os.getenv("OLLAMA_API_URL")
        ollama_model = os.getenv("OLLAMA_MODEL", "all-minilm")
        chroma_persist_dir = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
        if not xml_input_dir:
            logging.error("XML_INPUT_DIR is not set in the environment.")
            raise ValueError("XML_INPUT_DIR is not set.")
        logging.info(f"Initializing XML parser...")
        parser = DoxygenXMLParser(xml_input_dir)
        logging.info(f"Parsing XML files...")
        entities = parser.parse_all()
        logging.info(f"Found {len(entities)} code entities: {list(entities.keys())}")
        logging.debug(f"Entity sample: {list(entities.values())[0] if entities else 'None'}")
        logging.info(f"Initializing embedding generator...")
        embedding_generator = OllamaEmbeddingGenerator(ollama_api_url, ollama_model)
        logging.info(f"Generating embeddings...")
        try:
            embeddings = embedding_generator.generate_embeddings(entities)
        except Exception as e:
            logging.error(f"Error generating embeddings: {e}\n{traceback.format_exc()}")
            raise
        logging.info(f"Generated {len(embeddings)} embeddings")
        logging.info(f"Initializing ChromaDB loader...")
        chroma_loader = ChromaDBLoader(persist_directory=chroma_persist_dir)
        logging.info(f"Clearing existing ChromaDB data...")
        try:
            chroma_loader.clear_collection()
        except Exception as e:
            logging.error(f"Error clearing ChromaDB collection: {e}\n{traceback.format_exc()}")
        logging.info(f"Loading embeddings into ChromaDB...")
        try:
            chroma_loader.load_embeddings(entities, embeddings)
        except Exception as e:
            logging.error(f"Error during embedding loading: {e}\n{traceback.format_exc()}")
        stats = chroma_loader.get_collection_stats()
        logging.info(f"ChromaDB collection stats: {stats}")
    except Exception as e:
        logging.error(f"Fatal error in load_embeddings: {e}\n{traceback.format_exc()}")

if __name__ == "__main__":
    load_embeddings() 