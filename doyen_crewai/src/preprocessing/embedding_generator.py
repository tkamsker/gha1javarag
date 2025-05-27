"""Module for generating embeddings using Ollama API."""

import json
import logging
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
    
    def generate_embeddings(self, entities: Dict[str, CodeEntity]) -> Dict[str, List[float]]:
        """Generate embeddings for all code entities.
        
        Args:
            entities: Dictionary of code entities to generate embeddings for
            
        Returns:
            Dictionary mapping entity names to their embeddings
        """
        embeddings = {}
        
        for name, entity in entities.items():
            try:
                # Combine relevant information for embedding
                text = f"{entity.name}\n{entity.description}\n{entity.documentation}"
                
                # Generate embedding
                embedding = self._get_embedding(text)
                if embedding:
                    embeddings[name] = embedding
                else:
                    logger.warning(f"Failed to generate embedding for entity: {name}")
            
            except Exception as e:
                logger.error(f"Error generating embedding for {name}: {str(e)}")
        
        return embeddings
    
    def _get_embedding(self, text: str) -> Optional[List[float]]:
        """Get embedding for a single text using Ollama API.
        
        Args:
            text: Text to generate embedding for
            
        Returns:
            List of floats representing the embedding, or None if failed
        """
        try:
            response = requests.post(
                self.embeddings_endpoint,
                json={
                    "model": self.model,
                    "prompt": text
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("embedding")
            else:
                logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error calling Ollama API: {str(e)}")
            return None
    
    def batch_generate_embeddings(self, entities: Dict[str, CodeEntity], batch_size: int = 10) -> Dict[str, List[float]]:
        """Generate embeddings in batches to avoid overwhelming the API.
        
        Args:
            entities: Dictionary of code entities to generate embeddings for
            batch_size: Number of entities to process in each batch
            
        Returns:
            Dictionary mapping entity names to their embeddings
        """
        embeddings = {}
        entity_items = list(entities.items())
        
        for i in range(0, len(entity_items), batch_size):
            batch = entity_items[i:i + batch_size]
            batch_embeddings = self.generate_embeddings(dict(batch))
            embeddings.update(batch_embeddings)
            
            logger.info(f"Processed batch {i//batch_size + 1}/{(len(entity_items) + batch_size - 1)//batch_size}")
        
        return embeddings 