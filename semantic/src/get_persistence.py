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
        self.llm = LLMProviderFactory.create_provider()
        
        logger.info("Initialized PersistenceAnalyzer")

    def load_cluster_data(self) -> Dict[str, Any]:
        """Load cluster data from the JSON file."""
        try:
            with open('data/results/clusters_by_class.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading cluster data: {str(e)}")
            raise

    def analyze_persistence(self, source_code: str) -> str:
        """Analyze persistence information in the source code using LLM."""
        prompt = f"""Analyze the following source code and identify:
1. Data Access Objects (DAOs)
2. Database-related data structures
3. Persistence patterns and mechanisms
4. Any database connection handling

Source code:
{source_code}

Provide a detailed analysis focusing on persistence-related aspects."""

        try:
            return self.llm.generate_text(prompt)
        except Exception as e:
            logger.error(f"Error analyzing persistence: {str(e)}")
            return f"Error analyzing persistence: {str(e)}"

    def process_clusters(self):
        """Process each cluster and analyze persistence information."""
        try:
            # Load cluster data
            cluster_data = self.load_cluster_data()
            
            # Create results directory if it doesn't exist
            os.makedirs('data/results/persistence', exist_ok=True)
            
            # Process each cluster
            for cluster_id, classes in cluster_data.items():
                logger.info(f"Processing cluster {cluster_id}")
                cluster_results = []
                
                # Process each class in the cluster
                for class_name, artifacts in classes.items():
                    logger.info(f"Analyzing class: {class_name}")
                    
                    # Process each artifact in the class
                    for artifact in artifacts:
                        try:
                            if isinstance(artifact, dict):
                                # Try common ID fields
                                artifact_id = artifact.get('id') or artifact.get('artifact_id')
                                if not artifact_id:
                                    logger.error(f"Artifact dict missing 'id' or 'artifact_id': {artifact}")
                                    continue
                            else:
                                artifact_id = artifact
                            # Retrieve artifact from ChromaDB
                            artifact_data = self.chroma.get_artifact_by_id(artifact_id)
                            if artifact_data and 'source_code' in artifact_data:
                                # Analyze persistence information
                                analysis = self.analyze_persistence(artifact_data['source_code'])
                                # Store results
                                cluster_results.append({
                                    'class_name': class_name,
                                    'artifact_id': artifact_id,
                                    'analysis': analysis
                                })
                        except Exception as e:
                            logger.error(f"Error processing artifact {artifact}: {str(e)}")
                
                # Save cluster results
                output_file = f'data/results/persistence/cluster_{cluster_id}_analysis.json'
                with open(output_file, 'w') as f:
                    json.dump(cluster_results, f, indent=2)
                logger.info(f"Saved persistence analysis for cluster {cluster_id} to {output_file}")
            
            # Generate summary report
            self.generate_summary_report(cluster_data)
            
        except Exception as e:
            logger.error(f"Error processing clusters: {str(e)}")
            raise

    def generate_summary_report(self, cluster_data: Dict[str, Any]):
        """Generate a summary report of persistence analysis."""
        try:
            summary = []
            
            # Process each cluster's results
            for cluster_id in cluster_data.keys():
                try:
                    with open(f'data/results/persistence/cluster_{cluster_id}_analysis.json', 'r') as f:
                        cluster_results = json.load(f)
                        
                        # Add cluster summary
                        summary.append({
                            'cluster_id': cluster_id,
                            'classes_analyzed': len(set(r['class_name'] for r in cluster_results)),
                            'artifacts_analyzed': len(cluster_results)
                        })
                except Exception as e:
                    logger.error(f"Error processing cluster {cluster_id} summary: {str(e)}")
            
            # Save summary report
            with open('data/results/persistence/summary_report.json', 'w') as f:
                json.dump(summary, f, indent=2)
            logger.info("Generated persistence analysis summary report")
            
        except Exception as e:
            logger.error(f"Error generating summary report: {str(e)}")
            raise

def main():
    """Main entry point for the persistence analysis."""
    try:
        analyzer = PersistenceAnalyzer()
        analyzer.process_clusters()
        logger.info("Persistence analysis completed successfully")
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main() 