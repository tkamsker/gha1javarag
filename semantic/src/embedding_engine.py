from sentence_transformers import SentenceTransformer
import logging
import os
import numpy as np

# Set environment variable to avoid threadpool warning
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmbeddingEngine:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """Initialize the embedding engine with the specified model."""
        logger.info(f"Loading embedding model: {model_name}")
        try:
            self.model = SentenceTransformer(model_name)
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def generate_embedding(self, text):
        """Generate embedding for the given text.
        
        Args:
            text (str or dict): If str, the text to embed. If dict, should contain 'text' key.
            
        Returns:
            numpy.ndarray: The embedding vector
        """
        try:
            # Handle both string and dictionary inputs
            if isinstance(text, dict):
                text = text['text']
            
            # Ensure text is a string
            if not isinstance(text, str):
                raise ValueError("Input must be a string or a dictionary with 'text' key")
            
            # Ensure text is not empty
            if not text.strip():
                raise ValueError("Input text cannot be empty")
            
            # Generate embedding
            embeddings = self.model.encode([text], convert_to_tensor=False)
            if len(embeddings) == 0:
                raise ValueError("No embedding generated")
            
            return embeddings[0]
            
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise

    def generate_embeddings_batch(self, texts: list, batch_size: int = 32) -> list:
        """Generate embeddings for a batch of texts."""
        try:
            if not texts:
                logger.warning("Empty text list provided for batch embedding")
                return []
            
            # Ensure all texts are strings
            texts = [str(text) for text in texts]
            
            # Generate embeddings in batches
            embeddings = self.model.encode(texts, batch_size=batch_size, convert_to_tensor=False)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {str(e)}")
            raise 