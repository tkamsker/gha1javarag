from sentence_transformers import SentenceTransformer
import logging
import os

# Set environment variable to avoid threadpool warning
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmbeddingEngine:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize the embedding engine with a specific model."""
        try:
            logger.info(f"Loading embedding model: {model_name}")
            self.model = SentenceTransformer(model_name)
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def generate_embedding(self, text: str) -> list:
        """Generate an embedding for a given text."""
        try:
            if not text:
                logger.warning("Empty text provided for embedding")
                return [0.0] * 384  # Return zero vector for empty text
            
            # Generate embedding
            embedding = self.model.encode(text, convert_to_tensor=False)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise

    def generate_embeddings_batch(self, texts: list, batch_size: int = 32) -> list:
        """Generate embeddings for a batch of texts."""
        try:
            if not texts:
                logger.warning("Empty text list provided for batch embedding")
                return []
            
            # Generate embeddings in batches
            embeddings = self.model.encode(texts, batch_size=batch_size, convert_to_tensor=False)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {str(e)}")
            raise 