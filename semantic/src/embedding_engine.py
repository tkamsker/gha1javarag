import requests
import logging
import os
import numpy as np
import json

# Set environment variable to avoid threadpool warning
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmbeddingEngine:
    def __init__(self, config_path: str = "config/config.json"):
        """Initialize the embedding engine with the model from configuration."""
        try:
            # Load configuration
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Get model name from config
            self.model_name = config.get('embedding', {}).get('model', 'all-minilm')
            logger.info(f"Using embedding model: {self.model_name}")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def generate_embedding(self, text):
        """Generate embedding for the given text using Ollama API.
        
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
            
            # Call Ollama API for embeddings
            response = requests.post('http://localhost:11434/api/embeddings', json={'model': self.model_name, 'prompt': text})
            response.raise_for_status()
            embedding = response.json()['embedding']
            
            return embedding
            
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise

    def generate_embeddings_batch(self, texts: list, batch_size: int = 32) -> list:
        """Generate embeddings for a batch of texts using Ollama API."""
        try:
            if not texts:
                logger.warning("Empty text list provided for batch embedding")
                return []
            
            # Ensure all texts are strings
            texts = [str(text) for text in texts]
            
            # Generate embeddings in batches
            embeddings = []
            for text in texts:
                embedding = self.generate_embedding(text)
                embeddings.append(embedding)
            
            return embeddings
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {str(e)}")
            raise 