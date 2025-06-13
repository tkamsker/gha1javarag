from typing import Dict, List
import numpy as np
from sklearn.cluster import DBSCAN
import logging
from pathlib import Path
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClusteringEngine:
    def __init__(self, config: dict):
        """Initialize the clustering engine with DBSCAN parameters."""
        self.config = config
        self.clusters: Dict[int, List[str]] = {}
        self.noise_points: List[str] = []

    def cluster_embeddings(self, embeddings: Dict[str, List[float]]) -> Dict[int, List[str]]:
        """Cluster the embeddings using DBSCAN."""
        try:
            # Convert embeddings to numpy array
            ids = list(embeddings.keys())
            embedding_matrix = np.array([embeddings[id] for id in ids])

            # Perform clustering
            dbscan = DBSCAN(
                eps=self.config["eps"],
                min_samples=self.config["min_samples"]
            ).fit(embedding_matrix)

            # Process results
            self.clusters = {}
            self.noise_points = []

            for idx, label in enumerate(dbscan.labels_):
                if label == -1:
                    self.noise_points.append(ids[idx])
                else:
                    if label not in self.clusters:
                        self.clusters[label] = []
                    self.clusters[label].append(ids[idx])

            logger.info(f"Found {len(self.clusters)} clusters and {len(self.noise_points)} noise points")
            return self.clusters

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
                json.dump({
                    "clusters": {str(k): v for k, v in self.clusters.items()},
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