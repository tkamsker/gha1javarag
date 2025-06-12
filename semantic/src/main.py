import os
import logging
from pathlib import Path
from typing import Dict, Any, List
import json
from dotenv import load_dotenv
import argparse

from src.doxygen_parser import DoxygenParser
from src.embedding_engine import EmbeddingEngine
from src.cluster_engine import ClusterEngine
from src.get_persistence import get_persistence
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
        # Get Java source directory from environment or config
        java_source_dir = os.getenv('JAVA_SOURCE_DIR') or self.config.get('java', {}).get('source_dir')
        self.parser = DoxygenParser(java_source_dir=java_source_dir)
        self.embedding_engine = EmbeddingEngine(config_path=config_path)
        self.cluster_engine = ClusterEngine(
            n_clusters=self.config.get('clustering', {}).get('n_clusters', 10)
        )
        # Get ChromaDB path from environment or config
        chroma_db_path = os.getenv('CHROMA_DB_DIR') or self.config.get('chromadb', {}).get('db_path', 'data/chroma_db')
        self.chroma = get_persistence(db_path=chroma_db_path)
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
                    if artifact.get('source_file'):
                        report.append(f"  - Source File: {artifact['source_file']}")
                    if artifact.get('source_code'):
                        report.append("  - Source Code:")
                        report.append("```java")
                        report.append(artifact['source_code'])
                        report.append("```")
        
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
                # Combine description and source code for better semantic understanding
                text_to_embed = f"{artifact['description']}\n{artifact.get('source_code', '')}"
                artifact['embedding'] = self.embedding_engine.generate_embedding(text_to_embed)

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
                    'id': artifact['id'],
                    'name': artifact['name'],
                    'description': artifact['description'],
                    'definition': artifact.get('definition', ''),
                    'args': artifact.get('args', ''),
                    'kind': artifact.get('kind', ''),
                    'source_file': artifact.get('source_file', ''),
                    'source_code': artifact.get('source_code', ''),
                    'metadata': artifact.get('metadata', {})
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
                    'description': artifact['description'],
                    'source_file': artifact.get('source_file', ''),
                    'metadata': artifact.get('metadata', {})
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
            # Generate query embedding
            query_embedding = self.embedding_engine.generate_embedding(query)
            
            # Search in ChromaDB
            results = self.chroma.search(query_embedding, top_k=top_k)
            
            return results
        except Exception as e:
            logger.error(f"Error performing semantic search: {str(e)}")
            return []

def main():
    """Main entry point for the semantic analyzer."""
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser(description='Semantic Code Analysis')
        parser.add_argument('--force-reanalysis', action='store_true', help='Force reanalysis of the project')
        args = parser.parse_args()
        
        # Initialize analyzer
        analyzer = SemanticAnalyzer()
        
        # Get project path from environment variable XML_INPUT_DIR or use default
        project_path = os.getenv('XML_INPUT_DIR', 'data/hotel_docs_doxygen2/xml')
        
        # Analyze project
        results = analyzer.analyze_project(project_path, force_reanalysis=args.force_reanalysis)
        
        logger.info("Analysis completed successfully")
        return results
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main() 