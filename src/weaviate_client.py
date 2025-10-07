"""
Weaviate client module for vector database operations.
Handles schema creation, data upsertion, and querying.
"""

import weaviate
from typing import Dict, List, Any, Optional
import logging
import time
from datetime import datetime


class WeaviateClient:
    """Client for Weaviate vector database operations."""
    
    def __init__(self, config):
        """Initialize Weaviate client with configuration."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.client = None
        self._connect()
    
    def _connect(self):
        """Establish connection to Weaviate."""
        try:
            weaviate_config = self.config.get_weaviate_config()
            
            # Create client configuration for v4 API
            if 'api_key' in weaviate_config and weaviate_config['api_key']:
                self.client = weaviate.connect_to_weaviate_cloud(
                    cluster_url=weaviate_config['url'],
                    auth_credentials=weaviate.AuthApiKey(api_key=weaviate_config['api_key'])
                )
            else:
                # Extract host and port from URL
                url = weaviate_config['url']
                if url.startswith('http://'):
                    url = url[7:]  # Remove 'http://'
                elif url.startswith('https://'):
                    url = url[8:]  # Remove 'https://'
                
                # Split host and port
                if ':' in url:
                    host, port = url.split(':', 1)
                    self.client = weaviate.connect_to_local(host=host, port=int(port))
                else:
                    self.client = weaviate.connect_to_local(host=url)
            
            # Test connection
            self.client.get_meta()
            self.logger.info(f"Connected to Weaviate at {weaviate_config['url']}")
        
        except Exception as e:
            self.logger.error(f"Failed to connect to Weaviate: {e}")
            raise
    
    def create_schemas(self):
        """Create Weaviate schemas for all collections."""
        if self.config.skip_schema_creation:
            self.logger.info("Skipping schema creation as configured")
            return
        
        schemas = self._get_schemas()
        
        for schema in schemas:
            try:
                class_name = schema['class']
                
                # Check if class already exists
                if self.client.collections.exists(class_name):
                    self.logger.info(f"Schema {class_name} already exists, skipping")
                    continue
                
                # Create class using v4 API
                self.client.collections.create_from_dict(schema)
                self.logger.info(f"Created schema for {class_name}")
            
            except Exception as e:
                self.logger.error(f"Error creating schema {class_name}: {e}")
                raise
    
    def _get_schemas(self) -> List[Dict[str, Any]]:
        """Get all Weaviate schemas."""
        return [
            {
                "class": "JavaCodeChunks",
                "description": "Code/config chunks with rich metadata",
                "vectorizer": "text2vec-ollama",
                "moduleConfig": {
                    "text2vec-ollama": {
                        "model": self.config.embedding_model,
                        "vectorizeClassName": False,
                        "apiEndpoint": "http://host.docker.internal:11434"
                    }
                },
                "properties": [
                    {"name": "projectName", "dataType": ["text"]},
                    {"name": "filePath", "dataType": ["text"]},
                    {"name": "chunkKind", "dataType": ["text"]},
                    {"name": "language", "dataType": ["text"]},
                    {"name": "content", "dataType": ["text"]},
                    {"name": "className", "dataType": ["text"]},
                    {"name": "functionName", "dataType": ["text"]},
                    {"name": "architecturalLayer", "dataType": ["text"]},
                    {"name": "businessDomain", "dataType": ["text"]},
                    {"name": "complexityScore", "dataType": ["number"]},
                    {"name": "startLine", "dataType": ["int"]},
                    {"name": "endLine", "dataType": ["int"]},
                    {"name": "parentRefs", "dataType": ["text[]"]},
                    {"name": "childRefs", "dataType": ["text[]"]},
                    {"name": "repositoryContext", "dataType": ["text"]}
                ]
            },
            {
                "class": "DocumentationChunks",
                "description": "Comments, README, markdown, docstrings",
                "vectorizer": "text2vec-ollama",
                "moduleConfig": {
                    "text2vec-ollama": {
                        "model": self.config.embedding_model,
                        "vectorizeClassName": False,
                        "apiEndpoint": "http://host.docker.internal:11434"
                    }
                },
                "properties": [
                    {"name": "projectName", "dataType": ["text"]},
                    {"name": "filePath", "dataType": ["text"]},
                    {"name": "content", "dataType": ["text"]},
                    {"name": "language", "dataType": ["text"]},
                    {"name": "section", "dataType": ["text"]}
                ]
            },
            {
                "class": "BusinessRules",
                "description": "Validation, workflows, domain entities",
                "vectorizer": "text2vec-ollama",
                "moduleConfig": {
                    "text2vec-ollama": {
                        "model": self.config.embedding_model,
                        "vectorizeClassName": False,
                        "apiEndpoint": "http://host.docker.internal:11434"
                    }
                },
                "properties": [
                    {"name": "projectName", "dataType": ["text"]},
                    {"name": "filePath", "dataType": ["text"]},
                    {"name": "content", "dataType": ["text"]},
                    {"name": "domainEntities", "dataType": ["text[]"]},
                    {"name": "dataFlows", "dataType": ["text[]"]}
                ]
            },
            {
                "class": "IntegrationPoints",
                "description": "APIs, DB interactions, external systems",
                "vectorizer": "text2vec-ollama",
                "moduleConfig": {
                    "text2vec-ollama": {
                        "model": self.config.embedding_model,
                        "vectorizeClassName": False,
                        "apiEndpoint": "http://host.docker.internal:11434"
                    }
                },
                "properties": [
                    {"name": "projectName", "dataType": ["text"]},
                    {"name": "filePath", "dataType": ["text"]},
                    {"name": "content", "dataType": ["text"]},
                    {"name": "endpoint", "dataType": ["text"]},
                    {"name": "protocol", "dataType": ["text"]},
                    {"name": "databaseObjects", "dataType": ["text[]"]}
                ]
            },
            {
                "class": "UIComponents",
                "description": "GWT & general UI components",
                "vectorizer": "text2vec-ollama",
                "moduleConfig": {
                    "text2vec-ollama": {
                        "model": self.config.embedding_model,
                        "vectorizeClassName": False,
                        "apiEndpoint": "http://host.docker.internal:11434"
                    }
                },
                "properties": [
                    {"name": "projectName", "dataType": ["text"]},
                    {"name": "componentName", "dataType": ["text"]},
                    {"name": "componentType", "dataType": ["text"]},
                    {"name": "filePath", "dataType": ["text"]},
                    {"name": "packageName", "dataType": ["text"]},
                    {"name": "sourceCode", "dataType": ["text"]},
                    {"name": "uiTemplate", "dataType": ["text"]},
                    {"name": "gwtWidgets", "dataType": ["text[]"]},
                    {"name": "businessDomains", "dataType": ["text[]"]},
                    {"name": "userRoles", "dataType": ["text[]"]},
                    {"name": "navigationTargets", "dataType": ["text[]"]},
                    {"name": "eventHandlers", "dataType": ["text[]"]},
                    {"name": "complexityScore", "dataType": ["int"]},
                    {"name": "accessibilityScore", "dataType": ["int"]},
                    {"name": "responsiveCapability", "dataType": ["boolean"]}
                ]
            },
            {
                "class": "NavigationFlows",
                "description": "Navigation flows and user journeys",
                "vectorizer": "text2vec-ollama",
                "moduleConfig": {
                    "text2vec-ollama": {
                        "model": self.config.embedding_model,
                        "vectorizeClassName": False,
                        "apiEndpoint": "http://host.docker.internal:11434"
                    }
                },
                "properties": [
                    {"name": "projectName", "dataType": ["text"]},
                    {"name": "flowName", "dataType": ["text"]},
                    {"name": "flowDescription", "dataType": ["text"]},
                    {"name": "sourceComponent", "dataType": ["text"]},
                    {"name": "targetComponent", "dataType": ["text"]},
                    {"name": "transitionTrigger", "dataType": ["text"]},
                    {"name": "userRole", "dataType": ["text"]},
                    {"name": "businessProcess", "dataType": ["text"]}
                ]
            }
        ]
    
    def upsert_chunks(self, chunks: List[Dict[str, Any]], collection_name: str) -> Dict[str, Any]:
        """Upsert chunks to Weaviate collection."""
        if not chunks:
            return {'success': True, 'count': 0, 'errors': []}
        
        if self.config.dry_run:
            self.logger.info(f"DRY RUN: Would upsert {len(chunks)} chunks to {collection_name}")
            return {'success': True, 'count': len(chunks), 'errors': []}
        
        try:
            # Get collection
            collection = self.client.collections.get(collection_name)
            
            # Insert data using v4 API
            collection.data.insert_many(chunks)
            
            self.logger.info(f"Successfully upserted {len(chunks)} chunks to {collection_name}")
            return {'success': True, 'count': len(chunks), 'errors': []}
        
        except Exception as e:
            self.logger.error(f"Error upserting chunks to {collection_name}: {e}")
            return {'success': False, 'count': 0, 'errors': [str(e)]}
    
    def query_chunks(self, collection_name: str, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Query chunks from Weaviate collection."""
        try:
            collection = self.client.collections.get(collection_name)
            
            result = collection.query.near_text(
                query=query,
                limit=limit,
                return_metadata=["score"]
            )
            # Normalize v4 result objects to plain dictionaries expected by callers
            normalized: List[Dict[str, Any]] = []
            objects = result.objects if hasattr(result, 'objects') else []
            for obj in objects:
                # v4 returns objects with `.properties` and `.metadata`
                props = getattr(obj, 'properties', {}) or {}
                meta = getattr(obj, 'metadata', {}) or {}
                normalized.append({
                    'filePath': props.get('filePath', ''),
                    'content': props.get('content', ''),
                    'chunkKind': props.get('chunkKind', ''),
                    'language': props.get('language', ''),
                    'className': props.get('className', ''),
                    'functionName': props.get('functionName', ''),
                    '_additional': {
                        'score': getattr(meta, 'score', None) if hasattr(meta, 'score') else meta.get('score', None),
                        'distance': getattr(meta, 'distance', None) if hasattr(meta, 'distance') else meta.get('distance', None)
                    }
                })
            return normalized
        
        except Exception as e:
            self.logger.error(f"Error querying {collection_name}: {e}")
            return []
    
    def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """Get statistics for a collection."""
        try:
            collection = self.client.collections.get(collection_name)
            count = collection.aggregate.over_all(total_count=True).total_count
            
            return {
                'collection': collection_name,
                'count': count,
                'timestamp': datetime.now().isoformat()
            }
        
        except Exception as e:
            self.logger.error(f"Error getting stats for {collection_name}: {e}")
            return {
                'collection': collection_name,
                'count': 0,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_all_collection_stats(self) -> Dict[str, Any]:
        """Get statistics for all collections."""
        collections = ['JavaCodeChunks', 'DocumentationChunks', 'BusinessRules', 
                      'IntegrationPoints', 'UIComponents', 'NavigationFlows']
        
        stats = {}
        total_count = 0
        
        for collection in collections:
            collection_stats = self.get_collection_stats(collection)
            stats[collection] = collection_stats
            total_count += collection_stats.get('count', 0)
        
        stats['total_count'] = total_count
        stats['timestamp'] = datetime.now().isoformat()
        
        return stats
    
    def delete_collection(self, collection_name: str) -> bool:
        """Delete a collection (use with caution)."""
        try:
            self.client.collections.delete(collection_name)
            self.logger.info(f"Deleted collection {collection_name}")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting collection {collection_name}: {e}")
            return False
    
    def close(self):
        """Close the Weaviate client connection."""
        if self.client:
            # Properly close v4 client if possible to avoid resource warnings
            try:
                close_method = getattr(self.client, 'close', None)
                if callable(close_method):
                    close_method()
            finally:
                self.client = None
            self.logger.info("Closed Weaviate client connection")
