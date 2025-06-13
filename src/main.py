import os
import logging
from pathlib import Path
from dotenv import load_dotenv
import yaml
from doxygen_parser import DoxygenParser
from embedder import CodeEmbedder
from chromadb_connector import ChromaDBConnector
from clustering_engine import ClusteringEngine
from requirement_generator import RequirementGenerator
import re

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent

def ensure_directories() -> None:
    """Ensure all required directories exist."""
    directories = {
        'XML_INPUT_DIR': os.getenv('XML_INPUT_DIR', './data/hotel_docs_doxygen2/xml'),
        'JAVA_SOURCE_DIR': os.getenv('JAVA_SOURCE_DIR', './data/java_source'),
        'CHROMADB_DIR': os.getenv('CHROMADB_DIR', './data/chromadb'),
        'OUTPUT_DIR': os.getenv('OUTPUT_DIR', './output')
    }
    
    for dir_name, dir_path in directories.items():
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        logger.info(f"Ensured directory exists: {dir_path}")

def load_config() -> dict:
    """Load configuration from YAML file."""
    config_path = get_project_root() / "config" / "app.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def interpolate_env_vars(config):
    if isinstance(config, dict):
        return {k: interpolate_env_vars(v) for k, v in config.items()}
    elif isinstance(config, list):
        return [interpolate_env_vars(i) for i in config]
    elif isinstance(config, str):
        # Replace ${VAR} with the value from the environment
        return re.sub(r'\$\{([^}]+)\}', lambda m: os.getenv(m.group(1), m.group(0)), config)
    else:
        return config

def main():
    """Main execution function."""
    try:
        # Load environment variables
        load_dotenv()
        
        # Ensure directories exist
        ensure_directories()
        
        # Load configuration
        config = load_config()
        config = interpolate_env_vars(config)
        
        # Get directory paths from environment
        xml_input_dir = os.getenv('XML_INPUT_DIR', './data/hotel_docs_doxygen2/xml')
        java_source_dir = os.getenv('JAVA_SOURCE_DIR', './data/java_source')
        chromadb_dir = os.getenv('CHROMADB_DIR', './data/chromadb')
        output_dir = os.getenv('OUTPUT_DIR', './output')
        
        logger.info(f"Using XML_INPUT_DIR from .env: {xml_input_dir}")
        logger.info(f"Using JAVA_SOURCE_DIR from .env: {java_source_dir}")
        
        # Parse code artifacts
        logger.info("Parsing code artifacts...")
        parser = DoxygenParser(xml_input_dir)
        artifacts = parser.parse_xml_files()
        
        # Generate embeddings
        logger.info("Generating embeddings...")
        embedder = CodeEmbedder(os.getenv('OPENAI_API_KEY'))
        embeddings = embedder.generate_embeddings(artifacts)
        
        # Store embeddings in ChromaDB
        logger.info("Storing embeddings in ChromaDB...")
        db = ChromaDBConnector(chromadb_dir)
        db.store_embeddings(embeddings, artifacts)
        
        # Save embeddings to file
        embedder.save_embeddings(str(Path(output_dir) / "embeddings.json"))
        
        # Perform clustering
        logger.info("Clustering embeddings...")
        clustering = ClusteringEngine(config["clustering"])
        clusters = clustering.cluster_embeddings(embeddings)
        
        # Generate requirements
        logger.info("Generating requirements...")
        generator = RequirementGenerator(os.getenv('OPENAI_API_KEY'), os.getenv('LLM_MODEL'))
        requirements = generator.generate_requirements(clusters, artifacts)
        
        # Save requirements to file
        generator.save_requirements(requirements, str(Path(output_dir) / "requirements.json"))
        
        # Save clusters to file
        clustering.save_clusters(str(Path(output_dir) / "clusters.json"))
        
        logger.info("Processing completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main() 