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
        # Allow overriding Ollama endpoint at class-level to avoid localhost defaults inside container
        import os
        api_endpoint = (
            os.getenv("TEXT2VEC_OLLAMA_API_ENDPOINT")
            or os.getenv("OLLAMA_API_ENDPOINT")
            or os.getenv("GENERATIVE_OLLAMA_API_ENDPOINT")
            or settings.ollama_base_url  # fallback to app config
        )
        for class_name, properties in self._expected_classes().items():
            try:
                if not self._client.schema.exists(class_name):
                    cfg = {
                        "class": class_name,
                        "vectorizer": "text2vec-ollama",
                        "moduleConfig": {
                            "text2vec-ollama": {
                                "vectorizeClassName": True,
                                **({"apiEndpoint": api_endpoint} if api_endpoint else {})
                            }
                        },
                        "properties": [{"name": p, "dataType": ["text"]} for p in properties]
                    }
                    self._client.schema.create_class(cfg)
                    logger.info("Created Weaviate class: %s", class_name)
            except Exception as e:
                logger.warning("Failed ensuring class %s: %s", class_name, e)

    def _expected_classes(self) -> Dict[str, List[str]]:
        return {
            "IbatisStatement": ["project", "path", "text", "statementId", "statementType", "sqlContent"],
            "DaoCall": ["project", "path", "text", "daoClass", "methodName"],
            "JspForm": ["project", "path", "text", "formAction", "formMethod"],
            "DbTable": ["project", "path", "text", "tableName"],
            "GwtModule": ["project", "path", "text", "moduleName"],
            "GwtUiBinder": ["project", "path", "text", "ownerType"],
            "GwtActivityPlace": ["project", "path", "text", "placeClass", "activityClass"],
            "GwtEndpoint": ["project", "path", "text", "style", "serviceInterface", "endpointPath"],
            "JsArtifact": ["project", "path", "text", "scriptPath"],
            "BackendDoc": ["project", "path", "text", "summary", "language"],
        }

    def index_artifact(self, class_name: str, artifact: Dict[str, Any]) -> Optional[str]:
        """Create or update an object for the artifact. Returns object id or None."""
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
        try:
            uuid = self._client.data_object.create(data_object=data, class_name=class_name)
            return uuid
        except Exception as e:
            logger.error("Indexing failed for %s: %s", class_name, e)
            return None

    def search_artifacts(self, class_name: str, query: str, project: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Semantic search over 'text' with optional project filter."""
        try:
            builder = self._client.query.get(class_name, [
                "project", "path", "text", "summary", "language"
            ])
            if project:
                builder = builder.with_where({
                    "path": ["project"],
                    "operator": "Equal",
                    "valueText": project,
                })
            builder = builder.with_near_text({"concepts": [query]}).with_limit(limit)
            result = builder.do()
            objects = result.get("data", {}).get("Get", {}).get(class_name, [])
            # normalize to list of dicts
            return [o for o in objects if isinstance(o, dict)]
        except Exception as e:
            logger.error("Search failed for %s: %s", class_name, e)
            return []


