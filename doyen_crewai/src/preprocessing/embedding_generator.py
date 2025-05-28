"""Module for generating embeddings using Ollama API."""

import json
import logging
import time
from typing import Dict, List, Optional

import requests
from dotenv import load_dotenv

from .xml_parser import CodeEntity

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaEmbeddingGenerator:
    """Generates embeddings for code entities using Ollama API."""
    
    def __init__(self, api_url: str = "http://localhost:11434", model: str = "all-minilm"):
        """Initialize the embedding generator.
        
        Args:
            api_url: URL of the Ollama API
            model: Name of the Ollama model to use
        """
        self.api_url = api_url.rstrip("/")
        self.model = model
        self.embeddings_endpoint = f"{self.api_url}/api/embeddings"
    
    def generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding for a single text.
        
        Args:
            text: Text to generate embedding for
            
        Returns:
            Embedding vector or None if generation fails
        """
        try:
            response = requests.post(
                f"{self.api_url}/api/embeddings",
                json={"model": self.model, "prompt": text},
                timeout=30
            )
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:
                    logger.error("Rate limit exceeded while generating embedding")
                    return None
                else:
                    raise
            return response.json()["embedding"]
        except requests.exceptions.Timeout:
            logger.error("Timeout while generating embedding")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Error generating embedding: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error generating embedding: {str(e)}")
            return None
    
    def generate_embeddings_batch(self, texts: List[str]) -> Dict[str, List[float]]:
        """Generate embeddings for a batch of texts.
        
        Args:
            texts: List of texts to generate embeddings for
            
        Returns:
            Dictionary mapping texts to their embeddings
        """
        embeddings = {}
        max_retries = 3
        retry_delay = 1  # seconds
        
        for text in texts:
            retries = 0
            while retries < max_retries:
                embedding = self.generate_embedding(text)
                if embedding is not None:
                    embeddings[text] = embedding
                    break
                retries += 1
                if retries < max_retries:
                    logger.info(f"Retrying embedding generation (attempt {retries + 1}/{max_retries})")
                    time.sleep(retry_delay * retries)  # Exponential backoff
            
            if retries == max_retries:
                logger.error(f"Failed to generate embedding after {max_retries} attempts")
        
        return embeddings
    
    def generate_entity_embeddings(self, entities: Dict[str, CodeEntity]) -> Dict[str, List[float]]:
        """Generate embeddings for code entities.
        
        Args:
            entities: Dictionary mapping entity names to CodeEntity objects
            
        Returns:
            Dictionary mapping entity names to their embeddings
        """
        # Prepare texts for embedding
        texts = {}
        for name, entity in entities.items():
            # Combine relevant entity information for embedding
            text = f"{entity.name} {entity.kind} {entity.description} {entity.documentation}"
            texts[name] = text
        
        # Generate embeddings in batches
        return self.generate_embeddings_batch(list(texts.values()))
    
    def batch_generate_embeddings(self, entities: Dict[str, CodeEntity]) -> Dict[str, Optional[List[float]]]:
        """Batch generate embeddings for code entities (returns mapping of name to embedding or None)."""
        embeddings = {}
        for name, entity in entities.items():
            embedding = self.generate_embedding(f"{entity.name} {entity.kind} {entity.description} {entity.documentation}")
            embeddings[name] = embedding
        return embeddings 