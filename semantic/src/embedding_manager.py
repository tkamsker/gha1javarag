import os
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
import logging
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class EmbeddingManager:
    def __init__(self, persist_directory: str = "chroma_db"):
        """Initialize the embedding manager.
        
        Args:
            persist_directory: Directory to persist ChromaDB data
        """
        self.persist_directory = Path(persist_directory)
        # Ensure directory exists with proper permissions
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        os.chmod(self.persist_directory, 0o777)  # Give full permissions
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True,
                is_persistent=True
            )
        )
        
        # Initialize sentence transformer model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Create or get collection
        try:
            self.collection = self.client.get_or_create_collection(
                name="code_artifacts",
                metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            logger.error(f"Error creating collection: {str(e)}")
            # Try to delete and recreate the collection
            try:
                self.client.delete_collection("code_artifacts")
                self.collection = self.client.create_collection(
                    name="code_artifacts",
                    metadata={"hnsw:space": "cosine"}
                )
            except Exception as e2:
                logger.error(f"Error recreating collection: {str(e2)}")
                raise
        
    def create_embeddings(self, artifacts: List[Dict[str, Any]]) -> None:
        """Create embeddings for code artifacts and store them in ChromaDB.
        
        Args:
            artifacts: List of code artifacts from DoxygenParser
        """
        try:
            # Prepare data for batch processing
            ids = []
            documents = []
            metadatas = []
            
            for artifact in artifacts:
                # Create a unique ID if not present
                artifact_id = artifact.get("id", f"{artifact['name']}_{len(ids)}")
                
                # Prepare document text
                doc_parts = []
                if artifact.get("name"):
                    doc_parts.append(f"Name: {artifact['name']}")
                if artifact.get("description"):
                    doc_parts.append(f"Description: {artifact['description']}")
                if artifact.get("source_code"):
                    doc_parts.append(f"Code:\n{artifact['source_code']}")
                
                document = "\n".join(doc_parts)
                
                # Prepare metadata
                metadata = {
                    "name": artifact.get("name", ""),
                    "class": artifact.get("class", ""),
                    "kind": artifact.get("kind", ""),
                    "source_file": artifact.get("source_file", ""),
                }
                
                # Add additional metadata if available
                if "metadata" in artifact:
                    metadata.update(artifact["metadata"])
                
                ids.append(artifact_id)
                documents.append(document)
                metadatas.append(metadata)
            
            # Create embeddings in batches
            batch_size = 100
            for i in range(0, len(documents), batch_size):
                batch_ids = ids[i:i + batch_size]
                batch_docs = documents[i:i + batch_size]
                batch_metadatas = metadatas[i:i + batch_size]
                
                # Create embeddings
                embeddings = self.model.encode(batch_docs)
                
                # Add to ChromaDB
                try:
                    self.collection.add(
                        ids=batch_ids,
                        embeddings=embeddings.tolist(),
                        documents=batch_docs,
                        metadatas=batch_metadatas
                    )
                except Exception as e:
                    logger.error(f"Error adding batch to collection: {str(e)}")
                    # Try to reset collection and retry
                    self.reset_collection()
                    self.collection.add(
                        ids=batch_ids,
                        embeddings=embeddings.tolist(),
                        documents=batch_docs,
                        metadatas=batch_metadatas
                    )
                
            logger.info(f"Successfully created embeddings for {len(artifacts)} artifacts")
            
        except Exception as e:
            logger.error(f"Error creating embeddings: {str(e)}")
            raise
    
    def search_similar(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search for similar code artifacts using semantic similarity.
        
        Args:
            query: Search query
            n_results: Number of results to return
            
        Returns:
            List of similar artifacts with their metadata
        """
        try:
            # Create query embedding
            query_embedding = self.model.encode(query)
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=n_results
            )
            
            # Format results
            similar_artifacts = []
            for i in range(len(results["ids"][0])):
                artifact = {
                    "id": results["ids"][0][i],
                    "document": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i] if "distances" in results else None
                }
                similar_artifacts.append(artifact)
            
            return similar_artifacts
            
        except Exception as e:
            logger.error(f"Error searching similar artifacts: {str(e)}")
            raise
    
    def reset_collection(self) -> None:
        """Reset the ChromaDB collection."""
        try:
            self.client.delete_collection("code_artifacts")
            self.collection = self.client.create_collection(
                name="code_artifacts",
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("Successfully reset ChromaDB collection")
        except Exception as e:
            logger.error(f"Error resetting collection: {str(e)}")
            raise

    def close(self):
        """Close the ChromaDB client and release resources."""
        try:
            if hasattr(self.client, 'close'):
                self.client.close()
            logger.info("Closed ChromaDB client.")
        except Exception as e:
            logger.error(f"Error closing ChromaDB client: {str(e)}") 