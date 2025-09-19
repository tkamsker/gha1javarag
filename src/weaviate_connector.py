"""
Enhanced Weaviate Connector with Local Ollama Integration
Optimized for 1M token context window and repository-scale analysis
"""

import weaviate
try:
    import weaviate.classes as wvc
    from weaviate.auth import AuthApiKey
except ImportError:
    # Fallback for older weaviate-client versions
    import weaviate.auth as auth
    wvc = None
    AuthApiKey = auth.AuthApiKey if hasattr(auth, 'AuthApiKey') else None
import json
import uuid
import logging
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime
import asyncio
import os
from dotenv import load_dotenv

try:
    from weaviate_schemas import SchemaManager, WeaviateSchemas, ChunkType, ArchitecturalLayer
    from ollama_integration import OllamaIntegration, QwenAnalysisResult
    from code_chunker import CodeChunk
except ImportError:
    from .weaviate_schemas import SchemaManager, WeaviateSchemas, ChunkType, ArchitecturalLayer
    from .ollama_integration import OllamaIntegration, QwenAnalysisResult
    from .code_chunker import CodeChunk

logger = logging.getLogger('java_analysis.weaviate_connector')

@dataclass
class WeaviateConfig:
    """Configuration for Weaviate connection"""
    host: str = "localhost"
    port: int = 8080
    scheme: str = "http"
    timeout_config: tuple = (60, 120)  # (connect, read) timeouts
    additional_headers: Dict[str, str] = None
    auth_client_secret: str = None
    use_embedded: bool = False

@dataclass 
class QueryResult:
    """Result from Weaviate query with enhanced metadata"""
    objects: List[Dict[str, Any]]
    total_count: int
    query_time: float
    certainty_threshold: float
    context_utilization: float

class EnhancedWeaviateConnector:
    """
    Enhanced Weaviate connector with Ollama integration
    Supports 1M token context window optimization and repository-scale analysis
    """
    
    def __init__(self, config: WeaviateConfig = None, ollama_integration: OllamaIntegration = None):
        load_dotenv()
        
        # Initialize configuration
        self.config = config or WeaviateConfig(
            host=os.getenv('WEAVIATE_HOST', 'localhost'),
            port=int(os.getenv('WEAVIATE_PORT', '8080')),
            scheme=os.getenv('WEAVIATE_SCHEME', 'http')
        )
        
        # Initialize Ollama integration
        self.ollama = ollama_integration or OllamaIntegration()
        
        # Initialize Weaviate client
        self.client = None
        self.schema_manager = None
        self._connect()
        
        # Performance tracking
        self._performance_stats = {
            'queries_executed': 0,
            'objects_inserted': 0,
            'average_query_time': 0.0,
            'average_context_utilization': 0.0
        }
        
        logger.info(f"Enhanced Weaviate connector initialized: {self.config.scheme}://{self.config.host}:{self.config.port}")

    def _connect(self):
        """Establish connection to Weaviate"""
        try:
            weaviate_url = f"{self.config.scheme}://{self.config.host}:{self.config.port}"
            
            # Configure authentication if provided
            auth_config = None
            if self.config.auth_client_secret:
                auth_config = AuthApiKey(api_key=self.config.auth_client_secret)
            
            # Create client with optimized settings
            additional_config = wvc.init.AdditionalConfig(
                timeout=wvc.init.Timeout(
                    init=self.config.timeout_config[0],
                    query=self.config.timeout_config[1],
                    insert=120
                )
            )
            
            if auth_config:
                self.client = weaviate.connect_to_custom(
                    http_host=self.config.host,
                    http_port=self.config.port,
                    http_secure=(self.config.scheme == 'https'),
                    auth_credentials=auth_config,
                    additional_config=additional_config
                )
            else:
                self.client = weaviate.connect_to_custom(
                    http_host=self.config.host,
                    http_port=self.config.port,
                    http_secure=(self.config.scheme == 'https'),
                    additional_config=additional_config
                )
            
            # Test connection
            if self.client.is_ready():
                logger.info("Successfully connected to Weaviate")
                
                # Initialize schema manager
                ollama_url = f"http://{self.config.host}:11434" if self.config.host != 'localhost' else "http://host.docker.internal:11434"
                self.schema_manager = SchemaManager(self.client, ollama_url)
                
                # Ensure schemas exist
                self._ensure_schemas()
            else:
                raise ConnectionError("Weaviate is not ready")
                
        except Exception as e:
            logger.error(f"Failed to connect to Weaviate: {e}")
            raise

    def _ensure_schemas(self):
        """Ensure all required schemas exist"""
        try:
            if not self.schema_manager.create_all_schemas():
                logger.warning("Some schemas failed to create, but continuing...")
        except Exception as e:
            logger.error(f"Failed to ensure schemas: {e}")
            # Continue anyway - schemas might already exist

    async def health_check(self) -> Dict[str, Any]:
        """Check health of Weaviate and Ollama integration"""
        health_status = {
            'weaviate': False,
            'ollama': False,
            'schemas': False,
            'overall': False
        }
        
        try:
            # Check Weaviate
            health_status['weaviate'] = self.client.is_ready()
            
            # Check Ollama
            health_status['ollama'] = await self.ollama.health_check()
            
            # Check schemas
            schema_info = self.schema_manager.get_schema_info()
            health_status['schemas'] = len(schema_info.get('class_names', [])) >= 4
            
            # Overall health
            health_status['overall'] = all([
                health_status['weaviate'],
                health_status['ollama'],
                health_status['schemas']
            ])
            
            logger.info(f"Health check completed: {health_status}")
            return health_status
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return health_status

    def insert_code_chunk(self, chunk: CodeChunk, repository_context: str = "") -> str:
        """Insert a code chunk with enhanced metadata"""
        try:
            # Prepare properties for Weaviate
            properties = {
                'content': chunk.content,
                'file_path': chunk.file_path,
                'chunk_id': chunk.chunk_id,
                'chunk_type': chunk.chunk_type.value if hasattr(chunk.chunk_type, 'value') else str(chunk.chunk_type),
                'language': chunk.language,
                'parent_chunk_id': getattr(chunk, 'parent_chunk_id', ''),
                'child_chunk_ids': getattr(chunk, 'child_chunk_ids', []),
                'sibling_chunk_ids': getattr(chunk, 'sibling_chunk_ids', []),
                'repository_context': repository_context,
                'class_name': chunk.class_name or '',
                'method_name': chunk.method_name or '',
                'package_name': getattr(chunk, 'package_name', ''),
                'imports': getattr(chunk, 'imports', []),
                'annotations': getattr(chunk, 'annotations', []),
                'architectural_layer': getattr(chunk, 'architectural_layer', 'unknown'),
                'business_domain': getattr(chunk, 'business_domain', 'general'),
                'design_patterns': getattr(chunk, 'design_patterns', []),
                'integration_points': getattr(chunk, 'integration_points', []),
                'complexity_score': float(chunk.complexity_score) if chunk.complexity_score else 0.0,
                'lines_of_code': chunk.end_line - chunk.start_line if chunk.end_line and chunk.start_line else 0,
                'technical_debt_score': getattr(chunk, 'technical_debt_score', 0.0),
                'maintainability_index': getattr(chunk, 'maintainability_index', 50.0),
                'qwen_analysis_score': getattr(chunk, 'qwen_analysis_score', 0.0),
                'modernization_opportunities': getattr(chunk, 'modernization_opportunities', []),
                'performance_insights': getattr(chunk, 'performance_insights', []),
                'security_concerns': getattr(chunk, 'security_concerns', []),
                'jsp_elements': getattr(chunk, 'jsp_elements', []),
                'servlet_mappings': getattr(chunk, 'servlet_mappings', []),
                'legacy_patterns': getattr(chunk, 'legacy_patterns', []),
                'token_count': len(chunk.content) // 3,  # Rough estimation
                'context_weight': getattr(chunk, 'context_weight', 1.0),
                'semantic_importance': getattr(chunk, 'semantic_importance', 0.5),
                'created_at': datetime.now(),
                'last_analyzed': datetime.now(),
                'analysis_version': '1.0'
            }
            
            # Insert into Weaviate
            collection = self.client.collections.get("JavaCodeChunk")
            object_id = collection.data.insert(
                properties=properties
            )
            
            self._performance_stats['objects_inserted'] += 1
            logger.debug(f"Inserted code chunk: {chunk.chunk_id} -> {object_id}")
            
            return str(object_id)
            
        except Exception as e:
            logger.error(f"Failed to insert code chunk {chunk.chunk_id}: {e}")
            raise

    def batch_insert_chunks(self, chunks: List[CodeChunk], repository_context: str = "") -> List[str]:
        """Batch insert multiple code chunks for improved performance"""
        try:
            collection = self.client.collections.get("JavaCodeChunk")
            object_ids = []
            
            # Prepare batch data
            batch_objects = []
            for chunk in chunks:
                properties = self._prepare_chunk_properties(chunk, repository_context)
                batch_objects.append(wvc.data.DataObject(properties=properties))
            
            # Execute batch insert
            response = collection.data.insert_many(batch_objects)
            
            # Process results
            for i, result in enumerate(response.objects):
                if result.uuid:
                    object_ids.append(str(result.uuid))
                    self._performance_stats['objects_inserted'] += 1
                else:
                    logger.error(f"Failed to insert chunk {chunks[i].chunk_id}: {result.error}")
                    object_ids.append(None)
            
            logger.info(f"Batch inserted {len([id for id in object_ids if id])} of {len(chunks)} chunks")
            return object_ids
            
        except Exception as e:
            logger.error(f"Batch insert failed: {e}")
            return [None] * len(chunks)

    def _prepare_chunk_properties(self, chunk: CodeChunk, repository_context: str) -> Dict[str, Any]:
        """Prepare chunk properties for insertion"""
        return {
            'content': chunk.content,
            'file_path': chunk.file_path,
            'chunk_id': chunk.chunk_id,
            'chunk_type': chunk.chunk_type.value if hasattr(chunk.chunk_type, 'value') else str(chunk.chunk_type),
            'language': chunk.language,
            'repository_context': repository_context,
            'class_name': chunk.class_name or '',
            'method_name': chunk.method_name or '',
            'complexity_score': float(chunk.complexity_score) if chunk.complexity_score else 0.0,
            'lines_of_code': chunk.end_line - chunk.start_line if chunk.end_line and chunk.start_line else 0,
            'token_count': len(chunk.content) // 3,
            'created_at': datetime.now(),
            'last_analyzed': datetime.now(),
            'analysis_version': '1.0'
        }

    async def semantic_search(self, 
                            query: str, 
                            limit: int = 10, 
                            certainty: float = 0.7,
                            use_1m_context: bool = True) -> QueryResult:
        """
        Perform semantic search with optional 1M token context assembly
        """
        start_time = time.time()
        
        try:
            collection = self.client.collections.get("JavaCodeChunk")
            
            # Perform semantic search
            response = collection.query.near_text(
                query=query,
                limit=limit,
                certainty=certainty,
                return_metadata=wvc.query.MetadataQuery(
                    certainty=True,
                    distance=True
                )
            )
            
            # Convert results
            objects = []
            for obj in response.objects:
                obj_dict = {
                    'id': str(obj.uuid),
                    'properties': obj.properties,
                    'metadata': {
                        'certainty': obj.metadata.certainty,
                        'distance': obj.metadata.distance
                    }
                }
                objects.append(obj_dict)
            
            query_time = time.time() - start_time
            
            # Assemble 1M token context if requested
            context_utilization = 0.0
            if use_1m_context and objects:
                context_utilization = await self._assemble_1m_context(objects)
            
            # Update performance stats
            self._performance_stats['queries_executed'] += 1
            current_avg = self._performance_stats['average_query_time']
            total_queries = self._performance_stats['queries_executed']
            self._performance_stats['average_query_time'] = (
                (current_avg * (total_queries - 1) + query_time) / total_queries
            )
            
            result = QueryResult(
                objects=objects,
                total_count=len(objects),
                query_time=query_time,
                certainty_threshold=certainty,
                context_utilization=context_utilization
            )
            
            logger.info(f"Semantic search completed: {len(objects)} results in {query_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Semantic search failed: {e}")
            raise

    async def _assemble_1m_context(self, objects: List[Dict[str, Any]]) -> float:
        """Assemble hierarchical context for 1M token window utilization"""
        try:
            total_tokens = 0
            max_tokens = 1_000_000  # 1M token limit
            
            # Collect related chunks through hierarchical relationships
            expanded_context = []
            
            for obj in objects:
                props = obj['properties']
                
                # Add current chunk
                chunk_tokens = props.get('token_count', 0)
                if total_tokens + chunk_tokens < max_tokens:
                    expanded_context.append(obj)
                    total_tokens += chunk_tokens
                
                # Add parent context
                parent_id = props.get('parent_chunk_id')
                if parent_id and total_tokens < max_tokens * 0.8:
                    parent_obj = await self._get_chunk_by_id(parent_id)
                    if parent_obj:
                        parent_tokens = parent_obj['properties'].get('token_count', 0)
                        if total_tokens + parent_tokens < max_tokens:
                            expanded_context.append(parent_obj)
                            total_tokens += parent_tokens
                
                # Add child contexts
                child_ids = props.get('child_chunk_ids', [])
                for child_id in child_ids:
                    if total_tokens >= max_tokens * 0.9:
                        break
                    child_obj = await self._get_chunk_by_id(child_id)
                    if child_obj:
                        child_tokens = child_obj['properties'].get('token_count', 0)
                        if total_tokens + child_tokens < max_tokens:
                            expanded_context.append(child_obj)
                            total_tokens += child_tokens
            
            context_utilization = total_tokens / max_tokens
            logger.debug(f"Assembled 1M context: {total_tokens} tokens ({context_utilization:.1%} utilization)")
            
            return context_utilization
            
        except Exception as e:
            logger.error(f"Context assembly failed: {e}")
            return 0.0

    async def _get_chunk_by_id(self, chunk_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific chunk by its chunk_id"""
        try:
            collection = self.client.collections.get("JavaCodeChunk")
            
            response = collection.query.fetch_object_by_id(
                chunk_id,
                return_metadata=wvc.query.MetadataQuery(
                    certainty=True,
                    distance=True
                )
            )
            
            if response:
                return {
                    'id': str(response.uuid),
                    'properties': response.properties,
                    'metadata': {
                        'certainty': response.metadata.certainty if response.metadata else None,
                        'distance': response.metadata.distance if response.metadata else None
                    }
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get chunk by ID {chunk_id}: {e}")
            return None

    async def analyze_repository_with_qwen(self, repository_chunks: List[Dict[str, Any]]) -> QwenAnalysisResult:
        """
        Analyze entire repository using Qwen3-Coder with 1M token context
        """
        try:
            # Assemble repository context
            repository_content = []
            total_tokens = 0
            max_tokens = 900_000  # Leave some headroom for prompt
            
            for chunk in repository_chunks:
                chunk_content = chunk['properties']['content']
                chunk_tokens = len(chunk_content) // 3
                
                if total_tokens + chunk_tokens < max_tokens:
                    file_path = chunk['properties']['file_path']
                    repository_content.append(f"// File: {file_path}\n{chunk_content}\n")
                    total_tokens += chunk_tokens
                else:
                    break
            
            full_context = "\n".join(repository_content)
            
            # Analyze with Qwen3-Coder
            result = await self.ollama.analyze_code_repository(
                repository_context=full_context,
                analysis_type="comprehensive"
            )
            
            logger.info(f"Repository analysis completed with {total_tokens} tokens")
            return result
            
        except Exception as e:
            logger.error(f"Repository analysis failed: {e}")
            raise

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get connector performance statistics"""
        stats = self._performance_stats.copy()
        
        # Add Ollama stats
        ollama_stats = self.ollama.get_performance_stats()
        stats['ollama'] = ollama_stats
        
        # Add Weaviate specific stats
        try:
            schema_info = self.schema_manager.get_schema_info()
            stats['weaviate'] = {
                'schema_classes': schema_info.get('classes', 0),
                'connection_status': self.client.is_ready()
            }
        except:
            stats['weaviate'] = {'error': 'Could not get Weaviate stats'}
        
        return stats

    def close(self):
        """Close connections and cleanup resources"""
        try:
            if self.client:
                self.client.close()
            logger.info("Weaviate connector closed successfully")
        except Exception as e:
            logger.error(f"Error closing Weaviate connector: {e}")

    async def __aenter__(self):
        """Async context manager entry"""
        await self.health_check()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.ollama.cleanup()
        self.close()

# Convenience factory function
def create_weaviate_connector(config: WeaviateConfig = None, ollama_integration: OllamaIntegration = None) -> EnhancedWeaviateConnector:
    """Factory function to create configured Weaviate connector"""
    return EnhancedWeaviateConnector(config, ollama_integration)