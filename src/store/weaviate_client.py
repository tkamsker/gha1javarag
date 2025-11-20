"""
Weaviate client wrapper: schema management, indexing, and semantic search.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

import weaviate
# Note: Using weaviate-client 3.x schema API (dict-based),
# avoid imports from weaviate.classes (which are for 4.x).

from config.settings import settings

logger = logging.getLogger(__name__)


class WeaviateClient:
    """Thin wrapper around weaviate-client with project-aware helpers."""

    def __init__(self, ensure_schema: bool = True) -> None:
        self._client = weaviate.Client(
            url=settings.weaviate_url,
            additional_headers={
                "X-OpenAI-Api-Key": settings.weaviate_api_key or "",
            } if settings.weaviate_api_key else None,
        )
        # quick connectivity check
        try:
            meta = self._client.get_meta()
            logger.info("Connected to Weaviate %s", meta.get("version", "unknown"))
        except Exception as e:
            logger.warning("Weaviate meta failed: %s", e)
        if ensure_schema:
            self.ensure_schema()

    def ensure_schema(self) -> None:
        """Ensure expected classes exist with text2vec-ollama vectorization on 'text'."""
        # On Linux with host networking, Weaviate container uses 127.0.0.1:11434 (from container env vars)
        # On macOS with bridge networking, Weaviate container uses host.docker.internal:11434
        # We should let Weaviate use its container's environment variables by default.
        # Only set apiEndpoint in schema if explicitly needed to override container defaults.
        import os
        api_endpoint = (
            os.getenv("TEXT2VEC_OLLAMA_API_ENDPOINT")
            or os.getenv("OLLAMA_API_ENDPOINT")
            or os.getenv("GENERATIVE_OLLAMA_API_ENDPOINT")
        )
        # Don't use settings.ollama_base_url as it's for Python app, not Weaviate container
        # Let Weaviate use its container's OLLAMA_API_ENDPOINT environment variable
        
        module_config = {
            "text2vec-ollama": {
                "vectorizeClassName": True,
            }
        }
        # Only set apiEndpoint if explicitly provided via environment variable
        # This allows Weaviate to use its container's OLLAMA_API_ENDPOINT env var by default
        if api_endpoint:
            module_config["text2vec-ollama"]["apiEndpoint"] = api_endpoint
            logger.info("Using explicit Ollama endpoint in schema: %s", api_endpoint)
        else:
            logger.info("Using Weaviate container's OLLAMA_API_ENDPOINT environment variable")
        
        for class_name, expected_properties in self._expected_classes().items():
            try:
                if not self._client.schema.exists(class_name):
                    # Create new class
                    cfg = {
                        "class": class_name,
                        "vectorizer": "text2vec-ollama",
                        "moduleConfig": module_config,
                        "properties": [{"name": p, "dataType": ["text"]} for p in expected_properties]
                    }
                    self._client.schema.create_class(cfg)
                    logger.info("Created Weaviate class: %s", class_name)
                else:
                    # Check if schema needs updating (e.g., missing 'meta' field)
                    try:
                        existing_schema = self._client.schema.get(class_name)
                        existing_props = {p.get('name') for p in existing_schema.get('properties', [])}
                        expected_props = set(expected_properties)
                        
                        # Check if we need to add missing properties
                        missing_props = expected_props - existing_props
                        if missing_props:
                            logger.info(f"Updating class {class_name}: adding missing properties: {missing_props}")
                            for prop_name in missing_props:
                                try:
                                    self._client.schema.property.create(class_name, {
                                        "name": prop_name,
                                        "dataType": ["text"]
                                    })
                                    logger.info(f"Added property '{prop_name}' to class {class_name}")
                                except Exception as prop_e:
                                    logger.warning(f"Failed to add property '{prop_name}' to {class_name}: {prop_e}")
                    except Exception as schema_check_e:
                        logger.warning(f"Could not check schema for {class_name}: {schema_check_e}")
            except Exception as e:
                logger.warning("Failed ensuring class %s: %s", class_name, e)

    def _expected_classes(self) -> Dict[str, List[str]]:
        return {
            "IbatisStatement": ["project", "path", "text", "statementId", "statementType", "sqlContent", "meta"],
            "DaoCall": ["project", "path", "text", "daoClass", "methodName", "meta"],
            "JspForm": ["project", "path", "text", "formAction", "formMethod", "meta"],
            "DbTable": ["project", "path", "text", "tableName", "meta"],
            "GwtModule": ["project", "path", "text", "moduleName", "meta"],
            "GwtUiBinder": ["project", "path", "text", "ownerType", "meta"],
            "GwtActivityPlace": ["project", "path", "text", "placeClass", "activityClass", "meta"],
            "GwtEndpoint": ["project", "path", "text", "style", "serviceInterface", "endpointPath", "meta"],
            "JsArtifact": ["project", "path", "text", "scriptPath", "meta"],
            "BackendDoc": ["project", "path", "text", "summary", "language", "meta"],
        }

    def index_artifact(self, class_name: str, artifact: Dict[str, Any]) -> Optional[str]:
        """Create or update an object for the artifact. Returns object id or None."""
        import json as _json
        data: Dict[str, Any] = {}
        # flatten basic fields used across modules
        for key in ["project", "path", "text", "summary", "language",
                    "statementId", "statementType", "sqlContent",
                    "daoClass", "methodName", "formAction", "formMethod",
                    "tableName", "moduleName", "ownerType", "placeClass",
                    "activityClass", "style", "serviceInterface", "endpointPath",
                    "scriptPath"]:
            if key in artifact:
                data[key] = artifact[key]
        
        # Store meta as JSON string for full metadata preservation
        if 'meta' in artifact and artifact['meta']:
            try:
                data['meta'] = _json.dumps(artifact['meta'], ensure_ascii=False) if isinstance(artifact['meta'], dict) else str(artifact['meta'])
            except Exception as e:
                logger.warning(f"Failed to serialize meta for {class_name}: {e}")
                data['meta'] = str(artifact['meta'])
        
        try:
            uuid = self._client.data_object.create(data_object=data, class_name=class_name)
            return uuid
        except Exception as e:
            logger.error("Indexing failed for %s: %s", class_name, e)
            return None

    def search_artifacts(self, class_name: str, query: str, project: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Semantic search over 'text' with optional project filter."""
        import json as _json
        try:
            # Include meta field in search results
            builder = self._client.query.get(class_name, [
                "project", "path", "text", "summary", "language", "meta",
                "statementId", "statementType", "sqlContent",
                "daoClass", "methodName", "formAction", "formMethod",
                "tableName", "moduleName", "ownerType", "placeClass",
                "activityClass", "style", "serviceInterface", "endpointPath",
                "scriptPath"
            ])
            
            # Build where clause if project filter is specified
            where_clause = None
            if project:
                where_clause = {
                    "path": ["project"],
                    "operator": "Equal",
                    "valueText": project,
                }
            
            # Try vector search first, fall back to text search if vectors don't exist
            try:
                if where_clause:
                    builder = builder.with_where(where_clause)
                builder = builder.with_near_text({"concepts": [query]}).with_limit(limit)
                result = builder.do()
                objects = result.get("data", {}).get("Get", {}).get(class_name, [])
            except Exception as vector_error:
                # If vector search fails, try bm25 text search
                logger.warning(f"Vector search failed for {class_name}, trying bm25: {vector_error}")
                try:
                    builder = self._client.query.get(class_name, [
                        "project", "path", "text", "summary", "language", "meta",
                        "statementId", "statementType", "sqlContent",
                        "daoClass", "methodName", "formAction", "formMethod",
                        "tableName", "moduleName", "ownerType", "placeClass",
                        "activityClass", "style", "serviceInterface", "endpointPath",
                        "scriptPath"
                    ])
                    if where_clause:
                        builder = builder.with_where(where_clause)
                    builder = builder.with_bm25(query=query).with_limit(limit)
                    result = builder.do()
                    objects = result.get("data", {}).get("Get", {}).get(class_name, [])
                except Exception as bm25_error:
                    # Last resort: just get objects with where clause
                    logger.warning(f"BM25 search also failed for {class_name}, trying simple query: {bm25_error}")
                    builder = self._client.query.get(class_name, [
                        "project", "path", "text", "summary", "language", "meta",
                        "statementId", "statementType", "sqlContent",
                        "daoClass", "methodName", "formAction", "formMethod",
                        "tableName", "moduleName", "ownerType", "placeClass",
                        "activityClass", "style", "serviceInterface", "endpointPath",
                        "scriptPath"
                    ])
                    if where_clause:
                        builder = builder.with_where(where_clause)
                    builder = builder.with_limit(limit)
                    result = builder.do()
                    objects = result.get("data", {}).get("Get", {}).get(class_name, [])
            
            # normalize to list of dicts and parse meta JSON
            normalized = []
            for o in objects:
                if isinstance(o, dict):
                    # Parse meta JSON string back to dict if present
                    if 'meta' in o and isinstance(o['meta'], str):
                        try:
                            o['meta'] = _json.loads(o['meta'])
                        except (ValueError, TypeError):
                            pass  # Keep as string if not valid JSON
                    normalized.append(o)
            return normalized
        except Exception as e:
            logger.error("Search failed for %s: %s", class_name, e)
            import traceback
            logger.debug(traceback.format_exc())
            return []


