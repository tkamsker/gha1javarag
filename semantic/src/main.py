import os
import logging
import yaml
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any

from doxygen_parser import parse_doxygen_xml
from embedder import CodeEmbedder
from chroma_connector import ChromaConnector
from cluster_engine import ClusterEngine
from requirement_gen import RequirementGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_config() -> Dict[str, Any]:
    """Load configuration from YAML file."""
    config_path = Path(__file__).parent.parent / 'config' / 'app.yaml'
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    # Load environment variables
    load_dotenv()
    
    # Load configuration
    config = load_config()
    
    # Get environment variables
    xml_input_dir = os.getenv('XML_INPUT_DIR')
    java_source_dir = os.getenv('JAVA_SOURCE_DIR')
    
    if not xml_input_dir or not java_source_dir:
        raise ValueError("XML_INPUT_DIR and JAVA_SOURCE_DIR must be set in .env file")
    
    try:
        # Initialize components
        embedder = CodeEmbedder(model_name=config['embedding_model'])
        chroma = ChromaConnector(
            persist_directory=config['chroma']['persist_directory'],
            collection_name=config['chroma']['collection_name']
        )
        cluster_engine = ClusterEngine(
            n_clusters=config['clustering']['n_clusters'],
            random_state=config['clustering']['random_state']
        )
        requirement_gen = RequirementGenerator(
            config_path=Path(__file__).parent.parent / 'config' / 'app.yaml'
        )
        
        # Parse Doxygen XML
        logger.info("Parsing Doxygen XML files...")
        artifacts = parse_doxygen_xml(xml_input_dir)
        logger.info(f"Parsed {len(artifacts)} artifacts")
        
        # Generate embeddings
        logger.info("Generating embeddings...")
        artifacts = embedder.embed_artifacts(artifacts)
        
        # Store in ChromaDB
        logger.info("Storing artifacts in ChromaDB...")
        chroma.store_artifacts(artifacts)
        
        # Cluster artifacts
        logger.info("Clustering artifacts...")
        artifacts = cluster_engine.cluster_artifacts(artifacts)
        
        # Generate requirements
        logger.info("Generating requirements...")
        cluster_requirements = requirement_gen.generate_cluster_requirements(artifacts)
        
        # Save results
        output_dir = Path(__file__).parent.parent / 'data' / 'output'
        output_dir.mkdir(exist_ok=True)
        
        # Save cluster requirements
        with open(output_dir / 'cluster_requirements.txt', 'w') as f:
            for cluster_id, requirement in cluster_requirements.items():
                f.write(f"Cluster {cluster_id}:\n{requirement}\n\n")
        
        # Save individual requirements
        with open(output_dir / 'artifact_requirements.txt', 'w') as f:
            for artifact in artifacts:
                requirement = requirement_gen.generate_requirement(artifact)
                f.write(f"Artifact: {artifact['id']}\n")
                f.write(f"Cluster: {artifact['cluster']}\n")
                f.write(f"Requirement: {requirement}\n\n")
        
        logger.info("Processing completed successfully")
        
    except Exception as e:
        logger.error(f"Error in main workflow: {str(e)}")
        raise

if __name__ == "__main__":
    main() 