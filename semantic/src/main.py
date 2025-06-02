import os
import logging
from pathlib import Path
from typing import Dict, Any, List
import json
from dotenv import load_dotenv

from src.doxygen_parser import DoxygenParser
from src.embedding_engine import EmbeddingEngine
from src.cluster_engine import ClusterEngine
from src.chroma_connector import ChromaConnector
from src.requirement_gen import RequirementGenerator

# Load environment variables from .env if present
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SemanticAnalyzer:
    def __init__(self, config_path: str = "config/config.json"):
        self.config = self._load_config(config_path)
        self.parser = DoxygenParser()
        self.embedding_engine = EmbeddingEngine()
        self.cluster_engine = ClusterEngine(
            n_clusters=self.config.get('clustering', {}).get('n_clusters', 10)
        )
        self.chroma = ChromaConnector()
        self.requirement_gen = RequirementGenerator()
        logger.info("Initialized SemanticAnalyzer")

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            return {}

    def _check_existing_analysis(self) -> bool:
        """Check if analysis results already exist."""
        output_path = Path('data/results/clustering_results.json')
        return output_path.exists()

    def analyze_project(self, project_path: str, force_reanalysis: bool = False) -> Dict[str, Any]:
        """Analyze a Java project using semantic clustering."""
        try:
            # Check if analysis already exists
            if not force_reanalysis and self._check_existing_analysis():
                logger.info("Loading existing analysis results")
                with open('data/results/clustering_results.json', 'r') as f:
                    return json.load(f)

            # Parse Doxygen XML files
            logger.info(f"Parsing Doxygen XML files in {project_path}")
            artifacts = self.parser.parse_directory(project_path)
            if not artifacts:
                logger.warning("No artifacts found in the project")
                return {}

            # Generate embeddings
            logger.info("Generating embeddings for artifacts")
            for artifact in artifacts:
                artifact['embedding'] = self.embedding_engine.generate_embedding(
                    artifact['description']
                )

            # Store in ChromaDB
            logger.info("Storing artifacts in ChromaDB")
            self.chroma.store_artifacts(artifacts)

            # Cluster artifacts
            logger.info("Clustering artifacts")
            clustered_artifacts = self.cluster_engine.cluster_artifacts(artifacts)

            # Generate requirements
            logger.info("Generating requirements")
            cluster_requirements = {}
            for cluster_id, cluster_artifacts in self._group_by_cluster(clustered_artifacts).items():
                requirement = self.requirement_gen.generate_cluster_requirements(cluster_artifacts)
                cluster_requirements[cluster_id] = requirement

            # Prepare results
            results = {
                'clusters': {},
                'statistics': {
                    'total_artifacts': len(clustered_artifacts),
                    'total_clusters': self.cluster_engine.n_clusters
                },
                'requirements': cluster_requirements
            }

            # Organize artifacts by cluster
            for artifact in clustered_artifacts:
                cluster_id = artifact['cluster']
                if cluster_id not in results['clusters']:
                    results['clusters'][cluster_id] = []
                results['clusters'][cluster_id].append({
                    'name': artifact['name'],
                    'class': artifact['class'],
                    'description': artifact['description']
                })

            return results

        except Exception as e:
            logger.error(f"Error analyzing project: {str(e)}")
            raise

    def _group_by_cluster(self, artifacts: List[Dict[str, Any]]) -> Dict[int, List[Dict[str, Any]]]:
        """Group artifacts by their cluster ID."""
        clusters = {}
        for artifact in artifacts:
            cluster_id = artifact['cluster']
            if cluster_id not in clusters:
                clusters[cluster_id] = []
            clusters[cluster_id].append(artifact)
        return clusters

    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Perform semantic search on the codebase."""
        try:
            # Generate embedding for the query
            query_embedding = self.embedding_engine.generate_embedding(query)
            
            # Search in ChromaDB
            results = self.chroma.semantic_search(query, query_embedding, top_k)
            
            return results
        except Exception as e:
            logger.error(f"Error performing semantic search: {str(e)}")
            raise

def main():
    try:
        # Get project path from environment variable XML_INPUT_DIR
        project_path = os.getenv('XML_INPUT_DIR')
        if not project_path:
            raise ValueError("XML_INPUT_DIR is not set in the environment or .env file.")
        if not os.path.exists(project_path):
            raise FileNotFoundError(f"Project path not found: {project_path}")

        # Initialize analyzer
        analyzer = SemanticAnalyzer()
        
        # Analyze project (force reanalysis to ensure fresh data)
        logger.info(f"Starting analysis of project at {project_path}")
        results = analyzer.analyze_project(project_path, force_reanalysis=True)
        
        # Check if results are empty
        if not results:
            logger.warning("No results generated. Exiting.")
            return
        
        # Save results
        output_path = Path('data/results')
        output_path.mkdir(parents=True, exist_ok=True)
        
        with open(output_path / 'clustering_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Analysis complete. Results saved to {output_path}/clustering_results.json")
        
        # Print summary
        print("\nAnalysis Summary:")
        print(f"Total artifacts analyzed: {results['statistics']['total_artifacts']}")
        print(f"Number of clusters: {results['statistics']['total_clusters']}")
        
        print("\nCluster Requirements:")
        for cluster_id, requirement in results['requirements'].items():
            print(f"\nCluster {cluster_id}:")
            print(f"Requirement: {requirement}")
            print(f"Number of artifacts: {len(results['clusters'][cluster_id])}")
            print("Artifacts:")
            for artifact in results['clusters'][cluster_id]:
                print(f"- {artifact['name']} ({artifact['class']})")

        # Example semantic search
        print("\nPerforming example semantic search...")
        search_results = analyzer.semantic_search("database connection", top_k=3)
        print("\nSearch Results:")
        for result in search_results:
            print(f"\nID: {result['id']}")
            print(f"Class: {result['metadata']['class']}")
            print(f"Name: {result['metadata']['name']}")
            print(f"Document: {result['document']}")
            print(f"Distance: {result['distance']:.4f}")

    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main() 