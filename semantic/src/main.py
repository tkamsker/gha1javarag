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
        # Get ChromaDB path from environment or config
        chroma_db_path = os.getenv('CHROMA_DB_DIR') or self.config.get('chromadb', {}).get('db_path', 'data/chroma_db')
        self.chroma = ChromaConnector(db_path=chroma_db_path)
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

    def _generate_markdown_report(self, results: Dict[str, Any], clusters_by_class: Dict[int, Dict[str, List[Dict[str, Any]]]]) -> str:
        """Generate a Markdown report of the analysis results."""
        report = ["# Semantic Code Analysis Report\n"]
        
        # Add statistics
        report.append("## Statistics")
        report.append(f"- Total Artifacts: {results['statistics']['total_artifacts']}")
        report.append(f"- Number of Clusters: {results['statistics']['total_clusters']}\n")
        
        # Add cluster details
        report.append("## Cluster Details")
        for cluster_id, classes in clusters_by_class.items():
            report.append(f"\n### Cluster {cluster_id}")
            report.append(f"**Requirement:** {results['requirements'].get(cluster_id, 'N/A')}")
            report.append("\n**Classes and Methods:**")
            
            for class_name, artifacts in classes.items():
                report.append(f"\n#### {class_name}")
                for artifact in artifacts:
                    report.append(f"- {artifact['name']}")
                    if artifact.get('description'):
                        report.append(f"  - Description: {artifact['description']}")
                    if artifact.get('definition'):
                        report.append(f"  - Definition: {artifact['definition']}")
        
        return "\n".join(report)

    def analyze_project(self, project_path: str, force_reanalysis: bool = False) -> Dict[str, Any]:
        """Analyze a Java project using semantic clustering. Groups artifacts by cluster and class, and documents every persistence step."""
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
            logger.info("Storing artifacts in ChromaDB (persistence step)")
            self.chroma.store_artifacts(artifacts)
            logger.info("Artifacts persisted in ChromaDB")

            # Cluster artifacts
            logger.info("Clustering artifacts")
            clustered_artifacts = self.cluster_engine.cluster_artifacts(artifacts)

            # Calculate cluster statistics
            cluster_stats = self.cluster_engine._calculate_cluster_stats(clustered_artifacts)
            logger.info("Cluster statistics calculated")

            # Group artifacts by cluster and class
            logger.info("Grouping artifacts by cluster and class")
            clusters_by_class = {}
            for artifact in clustered_artifacts:
                cluster_id = artifact['cluster']
                class_name = artifact['class']
                if cluster_id not in clusters_by_class:
                    clusters_by_class[cluster_id] = {}
                if class_name not in clusters_by_class[cluster_id]:
                    clusters_by_class[cluster_id][class_name] = []
                clusters_by_class[cluster_id][class_name].append({
                    'name': artifact['name'],
                    'description': artifact['description'],
                    'definition': artifact.get('definition', ''),
                    'args': artifact.get('args', ''),
                    'kind': artifact.get('kind', '')
                })

            # Create output directory
            output_dir = Path('data/results')
            output_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created output directory: {output_dir}")

            # Persist the cluster-class grouping
            cluster_class_path = output_dir / 'clusters_by_class.json'
            with open(cluster_class_path, 'w') as f:
                json.dump(clusters_by_class, f, indent=2)
            logger.info(f"Cluster-class grouping persisted to {cluster_class_path}")

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
                    'total_clusters': self.cluster_engine.n_clusters,
                    'cluster_stats': cluster_stats
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

            # Persist the main clustering results
            clustering_results_path = output_dir / 'clustering_results.json'
            with open(clustering_results_path, 'w') as f:
                json.dump(results, f, indent=2)
            logger.info(f"Clustering results persisted to {clustering_results_path}")

            # Generate and persist Markdown report
            markdown_report = self._generate_markdown_report(results, clusters_by_class)
            report_path = output_dir / 'analysis_report.md'
            with open(report_path, 'w') as f:
                f.write(markdown_report)
            logger.info(f"Markdown report persisted to {report_path}")

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
        
        # Print summary
        print("\nAnalysis Summary:")
        print(f"Total artifacts analyzed: {results['statistics']['total_artifacts']}")
        print(f"Number of clusters: {results['statistics']['total_clusters']}")
        
        print("\nCluster Statistics:")
        for cluster_id, stats in results['statistics']['cluster_stats'].items():
            print(f"\nCluster {cluster_id}:")
            print(f"- Size: {stats['size']}")
            print(f"- Classes: {', '.join(stats['classes'])}")
            print(f"- Methods: {len(stats['methods'])}")
        
        print("\nResults have been saved to:")
        print("- data/results/clustering_results.json")
        print("- data/results/clusters_by_class.json")
        print("- data/results/analysis_report.md")

    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main() 