"""Weaviate vector database client - gracefully handles failures and cluster issues"""
from typing import Dict, List, Optional
import weaviate
import httpx
from weaviate.classes.config import Configure, Property, DataType
from src.config import Config
from src.utils.logger import setup_logger

logger = setup_logger("weaviate_client")


class WeaviateClient:
    """Client for Weaviate vector database - gracefully handles failures"""
    
    def __init__(self):
        self.client = None
        self.base_url = Config.WEAVIATE_URL.rstrip('/')
        self._connection_healthy = False
        
        try:
            # Test basic connectivity first via REST
            try:
                response = httpx.get(f"{self.base_url}/v1/meta", timeout=3.0)
                if response.status_code not in [200, 503]:
                    logger.debug(f"Weaviate returned status {response.status_code}, marking as unavailable")
                    return
            except Exception as test_error:
                logger.debug(f"Weaviate health check failed: {test_error}. Will use fallback storage.")
                return
            
            # Parse Weaviate URL
            url = Config.WEAVIATE_URL.replace("http://", "").replace("https://", "")
            if ":" in url:
                host, port_str = url.split(":")
                port = int(port_str)
            else:
                host = url
                port = 8080
            
            # Connect to Weaviate (non-blocking, fail gracefully)
            try:
                if Config.WEAVIATE_API_KEY:
                    self.client = weaviate.connect_to_custom(
                        http_host=host,
                        http_port=port,
                        http_secure=False,
                        grpc_host=Config.WEAVIATE_GRPC_URL.split(":")[0] if ":" in Config.WEAVIATE_GRPC_URL else Config.WEAVIATE_GRPC_URL,
                        grpc_port=int(Config.WEAVIATE_GRPC_URL.split(":")[-1]) if ":" in Config.WEAVIATE_GRPC_URL else 50051,
                        auth_credentials=weaviate.auth.AuthApiKey(api_key=Config.WEAVIATE_API_KEY),
                        timeout=5.0
                    )
                else:
                    self.client = weaviate.connect_to_local(
                        host=host,
                        port=port,
                        timeout=5.0
                    )
                
                # Try to ensure collection via REST (more reliable for cluster issues)
                self._ensure_collection_via_rest()
            except Exception as conn_error:
                logger.debug(f"Could not connect to Weaviate: {conn_error}. Will use fallback storage.")
                self.client = None
        except Exception as e:
            logger.debug(f"Weaviate initialization failed: {e}. Pipeline will use fallback storage.")
            self.client = None
    
    def _ensure_collection_via_rest(self):
        """Create collection using REST API (more reliable than Python client for cluster issues)"""
        collection_name = "FileExtraction"
        try:
            # Check if collection exists via REST
            response = httpx.get(f"{self.base_url}/v1/schema/{collection_name}", timeout=5.0)
            
            if response.status_code == 404:
                # Collection doesn't exist, create it
                logger.info(f"Creating collection {collection_name} via REST API...")
                schema = {
                    "class": collection_name,
                    "description": "File extraction storage",
                    "vectorizer": "none",  # No vectorizer - we provide embeddings manually
                    "properties": [
                        {"name": "filePath", "dataType": ["text"]},
                        {"name": "project", "dataType": ["text"]},
                        {"name": "fileType", "dataType": ["text"]},
                        {"name": "extractedInfo", "dataType": ["text"]},
                        {"name": "metadata", "dataType": ["text"]},
                        {"name": "processed", "dataType": ["boolean"]}
                    ]
                }
                
                create_response = httpx.post(
                    f"{self.base_url}/v1/schema",
                    json=schema,
                    timeout=10.0
                )
                
                if create_response.status_code in [200, 201]:
                    logger.info(f"Successfully created collection {collection_name} via REST")
                    self._connection_healthy = True
                else:
                    logger.debug(f"Could not create collection via REST: {create_response.status_code} - {create_response.text}")
                    self._connection_healthy = False
            elif response.status_code == 200:
                logger.debug(f"Collection {collection_name} already exists")
                self._connection_healthy = True
            else:
                logger.debug(f"Unexpected status checking collection: {response.status_code}")
                self._connection_healthy = False
        except Exception as e:
            logger.debug(f"Could not ensure collection via REST API: {e}. Will use fallback storage.")
            self._connection_healthy = False
    
    def store_file_extraction(self, file_path: str, project: str, file_type: str, 
                             extracted_info: Dict, embedding: Optional[List[float]] = None) -> str:
        """Store file extraction in Weaviate - gracefully handles failures"""
        import json
        # REST fallback if SDK client is unavailable
        if not self.client:
            try:
                props = {
                    "filePath": file_path,
                    "project": project,
                    "fileType": file_type,
                    "extractedInfo": json.dumps(extracted_info),
                    "metadata": str(extracted_info.get("extractionStatus", "complete")),
                    "processed": True,
                }
                payload = {"class": "FileExtraction", "properties": props}
                # Try vectors if embedding provided
                if embedding and len(embedding) > 0:
                    with_vectors = dict(payload)
                    with_vectors["vectors"] = {"default": embedding}
                    r = httpx.post(f"{self.base_url}/v1/objects", json=with_vectors, timeout=15.0)
                    if r.status_code in (200, 201):
                        return str(r.json().get("id", ""))
                    # fallback to legacy 'vector'
                    with_vector = dict(payload)
                    with_vector["vector"] = embedding
                    r = httpx.post(f"{self.base_url}/v1/objects", json=with_vector, timeout=15.0)
                    if r.status_code in (200, 201):
                        return str(r.json().get("id", ""))
                    logger.debug(f"REST insert with vector failed: {r.status_code} {r.text}")
                    return ""
                # No vector
                r = httpx.post(f"{self.base_url}/v1/objects", json=payload, timeout=15.0)
                if r.status_code in (200, 201):
                    return str(r.json().get("id", ""))
                logger.debug(f"REST insert failed: {r.status_code} {r.text}")
                return ""
            except Exception as e:
                logger.debug(f"REST insert exception: {e}")
                return ""
        
        try:
            collection = self.client.collections.get("FileExtraction", timeout=5.0)
            # Serialize metadata as JSON string if it's a dict
            metadata = extracted_info.get("extractionStatus", "complete")
            if isinstance(metadata, dict):
                metadata = json.dumps(metadata)
            
            # Prepare properties
            props = {
                "filePath": file_path,
                "project": project,
                "fileType": file_type,
                "extractedInfo": json.dumps(extracted_info),
                "metadata": str(metadata),
                "processed": True,
            }
            
            # Insert with or without vector (only if we have a valid embedding)
            try:
                if embedding and len(embedding) > 0:
                    uuid = collection.data.insert(
                        properties=props,
                        vector=embedding,
                        timeout=10.0
                    )
                else:
                    # Insert without vector (works with vectorizer=none)
                    uuid = collection.data.insert(
                        properties=props,
                        timeout=10.0
                    )
                logger.debug(f"Stored extraction for {file_path} in Weaviate")
                return str(uuid)
            except Exception as insert_error:
                # Mark connection as unhealthy if insert fails
                logger.debug(f"Failed to store in Weaviate: {insert_error}. Will use fallback storage.")
                self._connection_healthy = False
                return ""
        except Exception as e:
            # Don't log as error - Weaviate is optional
            logger.debug(f"Weaviate storage unavailable: {e}. Will use fallback storage.")
            self._connection_healthy = False
            return ""
    
    def query_by_project(self, project: str) -> List[Dict]:
        """Query all files for a project - gracefully handles failures"""
        # If SDK client unavailable, try REST fallback to list objects
        if not self.client:
            try:
                import json as _json
                # Fetch objects via REST and filter in Python
                resp = httpx.get(f"{self.base_url}/v1/objects?class=FileExtraction&limit=10000", timeout=10.0)
                if resp.status_code != 200:
                    return []
                data = resp.json()
                objs = (data or {}).get("objects", []) or []
                files: List[Dict] = []
                for obj in objs:
                    props = (obj or {}).get("properties", {}) or {}
                    if props.get("project") != project:
                        continue
                    extracted_info_str = props.get("extractedInfo", "{}")
                    if isinstance(extracted_info_str, str):
                        try:
                            extracted_info = _json.loads(extracted_info_str)
                        except Exception:
                            extracted_info = {}
                    else:
                        extracted_info = extracted_info_str or {}
                    files.append({
                        "filePath": props.get("filePath"),
                        "fileType": props.get("fileType"),
                        "extractedInfo": extracted_info,
                        "metadata": props.get("metadata", {}),
                    })
                return files
            except Exception:
                return []
        
        try:
            from weaviate.classes.query import Filter
            collection = self.client.collections.get("FileExtraction", timeout=5.0)
            
            # Try using where filter first (Weaviate v4 API)
            try:
                results = collection.query.fetch_objects(
                    where=Filter.by_property("project").equal(project),
                    limit=10000,
                    timeout=10.0
                )
            except (TypeError, Exception) as filter_error:
                # Fallback: fetch all and filter in Python
                try:
                    results = collection.query.fetch_objects(limit=10000, timeout=10.0)
                except Exception:
                    logger.debug(f"Could not query Weaviate: {filter_error}. Will use fallback storage.")
                    self._connection_healthy = False
                    return []
            
            files = []
            for obj in results.objects:
                import json
                # Filter by project if we fetched all
                obj_project = obj.properties.get("project")
                if obj_project != project:
                    continue
                    
                extracted_info_str = obj.properties.get("extractedInfo", "{}")
                if isinstance(extracted_info_str, str):
                    try:
                        extracted_info = json.loads(extracted_info_str)
                    except (json.JSONDecodeError, TypeError):
                        extracted_info = extracted_info_str if extracted_info_str else {}
                else:
                    extracted_info = extracted_info_str if extracted_info_str else {}
                    
                files.append({
                    "filePath": obj.properties.get("filePath"),
                    "fileType": obj.properties.get("fileType"),
                    "extractedInfo": extracted_info,
                    "metadata": obj.properties.get("metadata", {}),
                })
            return files
        except Exception as e:
            # Don't log as error - Weaviate is optional
            logger.debug(f"Weaviate query unavailable: {e}. Will use fallback storage.")
            self._connection_healthy = False
            return []
    
    def query_similar(self, text: str, limit: int = 10) -> List[Dict]:
        """Query similar files by semantic similarity"""
        # This would require embedding the query text first
        # For now, return empty
        return []
    
    def close(self):
        """Close Weaviate connection"""
        if self.client:
            try:
                self.client.close()
            except Exception:
                pass  # Ignore close errors
