import pytest
import weaviate
from src.common.models import CodeArtifact
from src.indexing.index_artifacts import index_artifacts, get_weaviate_client
import weaviate.classes as wvc
import weaviate.classes.query as wc_query

# This test requires a running Weaviate instance
# To run Weaviate, use: docker-compose -f docker-compose.macos.yml up -d

@pytest.fixture(scope="module")
def weaviate_client():
    client = get_weaviate_client()
    collection_name = "CodeArtifact"

    # Ensure a clean state before tests
    if client.collections.exists(collection_name):
        client.collections.delete(collection_name)
    
    # Create the collection
    code_artifact_collection = client.collections.create(
        collection_name,
        vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_huggingface(
            model="sentence-transformers/all-MiniLM-L6-v2",
            vectorize_collection_name=False
        ),
        properties=[
            wvc.config.Property(name="artifact_id", data_type=wvc.config.DataType.TEXT),
            wvc.config.Property(name="project_name", data_type=wvc.config.DataType.TEXT),
            wvc.config.Property(name="file_path", data_type=wvc.config.DataType.TEXT),
            wvc.config.Property(name="artifact_type", data_type=wvc.config.DataType.TEXT),
            wvc.config.Property(name="language", data_type=wvc.config.DataType.TEXT),
            wvc.config.Property(name="framework", data_type=wvc.config.DataType.TEXT),
            wvc.config.Property(name="details", data_type=wvc.config.DataType.TEXT),
            wvc.config.Property(name="content_for_embedding", data_type=wvc.config.DataType.TEXT),
        ]
    )

    yield client
    # Clean up after tests
    if client.collections.exists(collection_name):
        client.collections.delete(collection_name)
    client.close()
