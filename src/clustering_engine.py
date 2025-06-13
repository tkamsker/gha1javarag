from typing import Dict, List, Any
import numpy as np
from sklearn.cluster import DBSCAN
import logging
from pathlib import Path
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClusteringEngine:
    def __init__(self, config=None):
        self.config = config or {}
        self.clusters = {}
        self.noise_points = []

    def cluster_embeddings(self, embeddings: List[Dict[str, Any]]) -> Dict:
        """Cluster embeddings using DBSCAN and return cluster assignments."""
        try:
            if not embeddings:
                logger.warning("No embeddings provided for clustering.")
                return {}

            # Extract vectors and IDs from the list of embedding dicts
            ids = [emb['id'] for emb in embeddings]
            vectors = np.array([emb['embedding'] for emb in embeddings])

            # DBSCAN parameters
            eps = self.config.get('eps', 0.5)
            min_samples = self.config.get('min_samples', 2)

            db = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine').fit(vectors)
            labels = db.labels_

            clusters = {}
            noise_points = []
            for idx, label in enumerate(labels):
                if label == -1:
                    noise_points.append(ids[idx])
                else:
                    clusters.setdefault(label, []).append(ids[idx])

            self.clusters = clusters
            self.noise_points = noise_points
            logger.info(f"Found {len(clusters)} clusters and {len(noise_points)} noise points")
            return clusters
        except Exception as e:
            logger.error(f"Error clustering embeddings: {str(e)}")
            raise

    def get_cluster_centers(self, embeddings: Dict[str, List[float]]) -> Dict[int, List[float]]:
        """Calculate the center of each cluster."""
        try:
            centers = {}
            for cluster_id, cluster_ids in self.clusters.items():
                cluster_embeddings = [embeddings[id] for id in cluster_ids]
                centers[cluster_id] = np.mean(cluster_embeddings, axis=0).tolist()
            return centers

        except Exception as e:
            logger.error(f"Error calculating cluster centers: {str(e)}")
            raise

    def save_clusters(self, output_path: str) -> None:
        """Save clustering results to a JSON file."""
        try:
            output_file = Path(output_path)
            with open(output_file, 'w') as f:
                clusters_dict = {str(k): v for k, v in self.clusters.items()}
                json.dump({
                    "clusters": clusters_dict,
                    "noise_points": self.noise_points
                }, f, indent=2)
            logger.info(f"Clustering results saved to {output_path}")
        except Exception as e:
            logger.error(f"Error saving clustering results: {str(e)}")
            raise

    def load_clusters(self, input_path: str) -> None:
        """Load clustering results from a JSON file."""
        try:
            input_file = Path(input_path)
            if input_file.exists():
                with open(input_file, 'r') as f:
                    data = json.load(f)
                    self.clusters = data["clusters"]
                    self.noise_points = data["noise_points"]
                logger.info(f"Clustering results loaded from {input_path}")
        except Exception as e:
            logger.error(f"Error loading clustering results: {str(e)}")
            raise 