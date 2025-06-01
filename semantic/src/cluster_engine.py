from sklearn.cluster import KMeans
from typing import List, Dict, Any
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClusterEngine:
    def __init__(self, n_clusters: int = 10, random_state: int = 42):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.model = KMeans(
            n_clusters=n_clusters,
            random_state=random_state,
            n_init=10
        )
        logger.info(f"Initialized clustering engine with {n_clusters} clusters")

    def cluster_artifacts(self, artifacts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Cluster artifacts based on their embeddings."""
        try:
            # Extract embeddings
            embeddings = np.array([artifact['embedding'] for artifact in artifacts])
            
            # Perform clustering
            logger.info("Performing clustering on artifacts")
            cluster_labels = self.model.fit_predict(embeddings)
            
            # Add cluster information to artifacts
            for artifact, label in zip(artifacts, cluster_labels):
                artifact['cluster'] = int(label)
            
            # Calculate cluster statistics
            cluster_stats = self._calculate_cluster_stats(artifacts)
            logger.info(f"Cluster statistics: {cluster_stats}")
            
            return artifacts
        except Exception as e:
            logger.error(f"Error clustering artifacts: {str(e)}")
            raise

    def _calculate_cluster_stats(self, artifacts: List[Dict[str, Any]]) -> Dict[int, Dict[str, Any]]:
        """Calculate statistics for each cluster."""
        cluster_stats = {}
        
        for artifact in artifacts:
            cluster_id = artifact['cluster']
            if cluster_id not in cluster_stats:
                cluster_stats[cluster_id] = {
                    'size': 0,
                    'classes': set(),
                    'methods': set()
                }
            
            stats = cluster_stats[cluster_id]
            stats['size'] += 1
            stats['classes'].add(artifact['class'])
            stats['methods'].add(artifact['name'])
        
        # Convert sets to lists for JSON serialization
        for stats in cluster_stats.values():
            stats['classes'] = list(stats['classes'])
            stats['methods'] = list(stats['methods'])
        
        return cluster_stats

    def get_cluster_centers(self) -> np.ndarray:
        """Get the cluster centers."""
        return self.model.cluster_centers_

    def predict_cluster(self, embedding: np.ndarray) -> int:
        """Predict the cluster for a single embedding."""
        return int(self.model.predict([embedding])[0]) 