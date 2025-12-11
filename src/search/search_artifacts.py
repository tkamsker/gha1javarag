import weaviate
from typing import List
from src.common.models import CodeArtifact
import logging

logger = logging.getLogger(__name__)

def search_artifacts(project_name: str, query: str, client: weaviate.WeaviateClient) -> List[CodeArtifact]:
    """
    Searches for artifacts in Weaviate based on a natural language query.
    """
    try:
        code_artifacts_collection = client.collections.get("CodeArtifact")
        response = code_artifacts_collection.query.near_text(
            query=query,
            limit=5,
            filters=weaviate.classes.query.Filter.by_property("project_name").equal(project_name),
            return_properties=[
                "artifact_id", "project_name", "file_path", "artifact_type",
                "language", "framework", "details", "content_for_embedding"
            ]
        )
        
        artifacts = []
        for o in response.objects:
            # Reconstruct CodeArtifact object
            properties = o.properties
            artifacts.append(CodeArtifact(
                artifact_id=properties["artifact_id"],
                project_name=properties["project_name"],
                file_path=properties["file_path"],
                artifact_type=properties["artifact_type"],
                language=properties["language"],
                framework=properties["framework"],
                details=eval(properties["details"]) if properties["details"] else {}, # Assuming details stored as string
                content_for_embedding=properties["content_for_embedding"]
            ))
        return artifacts
    except Exception as e:
        logger.error(f"Error searching Weaviate: {e}")
        return []
