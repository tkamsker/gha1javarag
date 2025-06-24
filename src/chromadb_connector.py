import chromadb
from chromadb.config import Settings
import yaml
import os
from pathlib import Path
from dotenv import load_dotenv
import logging
from typing import List, Dict, Any
import json

logger = logging.getLogger('java_analysis.chromadb')

class ChromaDBConnector:
    def __init__(self, config_path: str = "config/app.yaml"):
        # Load environment variables
        load_dotenv()
        logger.debug("Environment variables loaded")
        
        # Ensure config directory exists
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        logger.debug(f"Ensured config directory exists: {os.path.dirname(config_path)}")
        
        # Create default config if it doesn't exist
        if not os.path.exists(config_path):
            logger.info(f"Config file not found at {config_path}, creating default config")
            default_config = {
                'chromadb': {
                    'host': 'localhost',
                    'port': 8000,
                    'collection_name': 'java_analysis'
                }
            }
            
            with open(config_path, 'w') as f:
                yaml.dump(default_config, f)
            logger.info(f"Created default config at {config_path}")
            
        # Load config
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        logger.debug("Loaded ChromaDB configuration")
        
        # Initialize ChromaDB client
        chromadb_dir = os.getenv('CHROMADB_DIR', './data/chromadb')
        self.client = chromadb.PersistentClient(path=chromadb_dir, settings=Settings(anonymized_telemetry=False))
        logger.info(f"Initialized ChromaDB client with directory: {chromadb_dir}")
        
        # Get or create collection
        collection_name = self.config['chromadb']['collection_name']
        self.collection = self.client.get_or_create_collection(name=collection_name)
        logger.info(f"Using collection: {collection_name}")

    def store_metadata(self, metadata_list: List[Dict[str, Any]]) -> None:
        """Store metadata in ChromaDB"""
        logger.info("Storing metadata in ChromaDB")
        
        try:
            # Prepare data for ChromaDB
            documents = []
            metadatas = []
            ids = []
            
            for idx, metadata in enumerate(metadata_list):
                # Convert ai_analysis to string if it's a dict
                ai_analysis = metadata.get('ai_analysis', '')
                if isinstance(ai_analysis, dict):
                    ai_analysis = json.dumps(ai_analysis, indent=2)
                elif not isinstance(ai_analysis, str):
                    ai_analysis = str(ai_analysis)
                
                # Create document from content and any analysis
                doc_content = [
                    f"File: {metadata['file_path']}",
                    f"Type: {metadata['file_type']}",
                    "Content:",
                    metadata.get('content', ''),
                    "Analysis:",
                    ai_analysis
                ]
                documents.append("\n".join(doc_content))
                
                # Prepare metadata
                meta = {
                    'file_path': metadata['file_path'],
                    'file_type': metadata['file_type'],
                    'extension': metadata.get('extension', ''),
                    'size_bytes': metadata.get('size_bytes', 0),
                    'last_modified': metadata.get('last_modified', 0)
                }
                
                # Add any additional metadata fields
                for key, value in metadata.items():
                    if key not in ['content', 'ai_analysis'] and isinstance(value, (str, int, float, bool)):
                        meta[key] = value
                
                metadatas.append(meta)
                ids.append(f"doc_{idx}")
            
            # Store in batches of 100 to avoid memory issues
            batch_size = 100
            for i in range(0, len(documents), batch_size):
                batch_end = min(i + batch_size, len(documents))
                self.collection.add(
                    documents=documents[i:batch_end],
                    metadatas=metadatas[i:batch_end],
                    ids=ids[i:batch_end]
                )
                logger.debug(f"Stored batch {i//batch_size + 1} ({batch_end - i} documents)")
            
            logger.info(f"Successfully stored {len(documents)} documents in ChromaDB")
            
        except Exception as e:
            logger.error(f"Error storing metadata in ChromaDB: {str(e)}")
            raise

    def query_similar(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Query for similar documents"""
        logger.info(f"Querying for documents similar to: {query}")
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                include=['documents', 'metadatas', 'distances']
            )
            logger.debug(f"Found {len(results['documents'][0])} matching documents")
            return results
        except Exception as e:
            logger.error(f"Error querying ChromaDB: {str(e)}")
            raise 