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
    root = get_project_root()
    directories = [
        root / "data" / "doxygen_xml",
        root / "data" / "java_source",
        root / "data" / "chromadb",
        root / "output"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"Ensured directory exists: {directory}")

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
        
        # Use .env variables if set, otherwise fall back to config
        xml_input_dir = os.getenv("XML_INPUT_DIR") or str(get_project_root() / config["data"]["doxygen_xml_dir"])
        java_source_dir = os.getenv("JAVA_SOURCE_DIR") or str(get_project_root() / config["data"]["java_source_dir"])
        chroma_db_dir = str(get_project_root() / config["data"]["chroma_db_dir"])

        if os.getenv("XML_INPUT_DIR"):
            logger.info(f"Using XML_INPUT_DIR from .env: {xml_input_dir}")
        else:
            logger.info(f"Using XML input dir from config: {xml_input_dir}")
        if os.getenv("JAVA_SOURCE_DIR"):
            logger.info(f"Using JAVA_SOURCE_DIR from .env: {java_source_dir}")
        else:
            logger.info(f"Using Java source dir from config: {java_source_dir}")

        # Initialize components
        parser = DoxygenParser(xml_input_dir)
        embedder = CodeEmbedder(os.getenv('OPENAI_API_KEY'))
        db = ChromaDBConnector(chroma_db_dir)
        clustering = ClusteringEngine(config["clustering"])
        generator = RequirementGenerator(os.getenv('OPENAI_API_KEY'), config["llm"]["model"])
        
        # Parse code artifacts
        logger.info("Parsing code artifacts...")
        code_artifacts = parser.parse_xml_files()
        
        # Generate embeddings
        logger.info("Generating embeddings...")
        embeddings = embedder.generate_embeddings(code_artifacts)
        
        # Store in ChromaDB
        logger.info("Storing embeddings in ChromaDB...")
        db.store_embeddings(embeddings, code_artifacts)
        
        # Cluster embeddings
        logger.info("Clustering embeddings...")
        clusters = clustering.cluster_embeddings(embeddings)
        
        # Generate requirements
        logger.info("Generating requirements...")
        requirements = generator.generate_requirements(clusters, code_artifacts)
        
        # Save results
        output_dir = get_project_root() / "output"
        embedder.save_embeddings(str(output_dir / "embeddings.json"))
        clustering.save_clusters(str(output_dir / "clusters.json"))
        generator.save_requirements(requirements, str(output_dir / "requirements.json"))
        
        logger.info("Processing completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main() 