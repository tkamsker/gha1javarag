import weaviate
from typing import List, Dict, Any
from src.common.models import CodeArtifact
import logging
import os
import weaviate.classes as wvc
import uuid # Re-add uuid import

logger = logging.getLogger(__name__)

def get_weaviate_client() -> weaviate.WeaviateClient:
    return weaviate.connect_to_local()

def index_artifacts(project_name: str, artifacts: List[CodeArtifact], client: weaviate.WeaviateClient):
    """
    Indexes a list of CodeArtifacts into Weaviate.
    """
    collection_name = "CodeArtifact"
    try:
        code_artifact_collection = client.collections.get(collection_name)
    except weaviate.exceptions.ObjectNotFoundException:
        logger.info(f"Collection '{collection_name}' not found, creating it.")
        code_artifact_collection = client.collections.create(
            collection_name,
            vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_huggingface(
                model="sentence-transformers/all-MiniLM-L6-v2",
                vectorize_collection_name=False
            ),
            properties=[
                wvc.config.Property(name="artifact_id", data_type=weaviate.classes.config.DataType.TEXT),
                wvc.config.Property(name="project_name", data_type=weaviate.classes.config.DataType.TEXT),
                wvc.config.Property(name="file_path", data_type=weaviate.classes.config.DataType.TEXT),
                wvc.config.Property(name="artifact_type", data_type=weaviate.classes.config.DataType.TEXT),
                wvc.config.Property(name="language", data_type=weaviate.classes.config.DataType.TEXT),
                wvc.config.Property(name="framework", data_type=weaviate.classes.config.DataType.TEXT),
                wvc.config.Property(name="details", data_type=weaviate.classes.config.DataType.TEXT),
                wvc.config.Property(name="content_for_embedding", data_type=weaviate.classes.config.DataType.TEXT),
            ]
        )

    with code_artifact_collection.batch.dynamic() as batch:
        for artifact in artifacts:
            data_object = {
                "artifact_id": artifact.artifact_id,
                "project_name": artifact.project_name,
                "file_path": artifact.file_path,
                "artifact_type": artifact.artifact_type,
                "language": artifact.language,
                "framework": artifact.framework,
                "details": str(artifact.details),
                "content_for_embedding": artifact.content_for_embedding,
            }
            try:
                # Generate a deterministic UUID from the artifact's ID string
                # Weaviate expects a UUID string for the uuid parameter
                batch.add_object(properties=data_object, uuid=str(uuid.uuid5(uuid.NAMESPACE_DNS, artifact.artifact_id)))
            except Exception as e:
                logger.error(f"Error indexing artifact {artifact.artifact_id}: {e}")
    logger.info(f"Indexed {len(artifacts)} artifacts for project {project_name}.")
