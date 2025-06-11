from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import logging
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CodeEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        logger.info(f"Initialized embedder with model: {model_name}")

    def embed_artifacts(self, artifacts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate embeddings for a list of code artifacts."""
        try:
            # Prepare texts for embedding
            texts = []
            for artifact in artifacts:
                text = self._prepare_text(artifact)
                texts.append(text)

            # Generate embeddings
            logger.info(f"Generating embeddings for {len(texts)} artifacts")
            embeddings = self.model.encode(texts, show_progress_bar=True)

            # Add embeddings to artifacts
            for artifact, embedding in zip(artifacts, embeddings):
                artifact['embedding'] = embedding.tolist()

            return artifacts
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise

    def _prepare_text(self, artifact: Dict[str, Any]) -> str:
        """Prepare text for embedding by combining relevant artifact information."""
        components = [
            artifact.get('class', ''),
            artifact.get('name', ''),
            artifact.get('definition', ''),
            artifact.get('args', ''),
            artifact.get('doc', ''),
            artifact.get('class_doc', '')
        ]
        return " ".join(filter(None, components))

    def embed_query(self, query: str) -> np.ndarray:
        """Generate embedding for a single query string."""
        try:
            return self.model.encode([query])[0]
        except Exception as e:
            logger.error(f"Error generating query embedding: {str(e)}")
            raise 