import os
import json
import logging
from typing import Dict, List, Any
from dotenv import load_dotenv
from src.chroma_connector import ChromaConnector
from src.llm_provider import LLMProviderFactory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PersistenceAnalyzer:
    def __init__(self):
        """Initialize the persistence analyzer with ChromaDB and LLM connections."""
        # Load environment variables
        load_dotenv()
        
        # Initialize ChromaDB connection
        self.chroma = ChromaConnector(
            collection_name="artifacts",
            db_path=os.getenv('CHROMA_DB_DIR', 'data/chroma')
        )
        
        # Initialize LLM provider
        self.llm_provider = LLMProviderFactory.create_provider()
        
        logger.info("Initialized PersistenceAnalyzer")

    def load_cluster_data(self) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        """Load cluster data from the JSON file."""
        try:
            with open('data/results/clusters_by_class.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading cluster data: {str(e)}")
            raise

    def analyze_persistence(self, artifact: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze persistence information in the source code using LLM."""
        # Use ChromaDB to find source code references
        xml_input_dir = os.getenv('XML_INPUT_DIR', 'data/doxygen_xml')
        artifact_id = os.path.join(xml_input_dir, artifact['id'])
        source_code = self.chroma.get_artifact_by_id(artifact_id)
        if not source_code:
            logger.warning(f"No source code found for artifact ID: {artifact_id}")
            return {}

        # Access the file to generate persistence information
        persistence_info = self._generate_persistence_info(source_code)
        return persistence_info

    def _generate_persistence_info(self, source_code: str) -> Dict[str, Any]:
        # Placeholder for generating persistence information from source code
        # This could involve parsing the source code to extract relevant information
        return {"persistence_info": "Sample persistence information"}

    def process_clusters(self, clusters_by_class: Dict[str, Dict[str, List[Dict[str, Any]]]]):
        """Process each cluster and analyze persistence information."""
        try:
            # Create results directory if it doesn't exist
            os.makedirs('data/results/persistence', exist_ok=True)
            
            # Process each cluster
            for cluster_id, classes in clusters_by_class.items():
                logger.info(f"Processing cluster {cluster_id}")
                
                # Process each class in the cluster
                for class_name, artifacts in classes.items():
                    logger.info(f"Analyzing class: {class_name}")
                    
                    # Process each artifact in the class
                    for artifact in artifacts:
                        try:
                            persistence_info = self.analyze_persistence(artifact)
                            if persistence_info:
                                # Save persistence analysis for each artifact
                                self._save_persistence_analysis(cluster_id, class_name, artifact, persistence_info)
                        except Exception as e:
                            logger.error(f"Error processing artifact {artifact}: {str(e)}")
            
            # Generate summary report
            self.generate_summary_report()
            
        except Exception as e:
            logger.error(f"Error processing clusters: {str(e)}")
            raise

    def _save_persistence_analysis(self, cluster_id: str, class_name: str, artifact: Dict[str, Any], persistence_info: Dict[str, Any]):
        output_dir = 'data/results/persistence'
        os.makedirs(output_dir, exist_ok=True)
        output_file = f"{output_dir}/cluster_{cluster_id}_analysis.json"
        with open(output_file, 'w') as f:
            json.dump({"class": class_name, "artifact": artifact, "persistence_info": persistence_info}, f, indent=2)
        logger.info(f"Saved persistence analysis for cluster {cluster_id} to {output_file}")

    def generate_summary_report(self):
        """Generate a summary report of persistence analysis."""
        try:
            # Placeholder for generating a summary report
            logger.info("Generated persistence analysis summary report")
            
        except Exception as e:
            logger.error(f"Error generating summary report: {str(e)}")
            raise

def main():
    """Main entry point for the persistence analysis."""
    try:
        analyzer = PersistenceAnalyzer()
        clusters_by_class = analyzer.load_cluster_data()
        analyzer.process_clusters(clusters_by_class)
        logger.info("Persistence analysis completed successfully")
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise

def get_persistence(db_path: str = "data/chroma"):
    return ChromaConnector(collection_name="artifacts", db_path=db_path)

if __name__ == "__main__":
    main() 