import pytest
import weaviate
from src.common.models import CodeArtifact
from src.indexing.index_artifacts import get_weaviate_client, index_artifacts
from src.search.search_artifacts import search_artifacts
import weaviate.classes as wvc
import weaviate.classes.query as wc_query

@pytest.fixture(scope="module")
def weaviate_client_with_data():
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
    
    # Ensure existing data is cleared for a clean test run
    code_artifact_collection.data.delete_many(
        where=wc_query.Filter.by_property("_id").not_equal("")
    )

    artifacts_to_index = [
        CodeArtifact(
            artifact_id="test-project:/path/to/file1.java:UserClass",
            project_name="test-project",
            file_path="/path/to/file1.java",
            artifact_type="java_class",
            language="java",
            content_for_embedding="public class ClassA { ... }",
            details={"class_name": "User"}
        ),
        CodeArtifact(
            artifact_id="test-project:/path/to/file2.jsp:LoginForm",
            project_name="test-project",
            file_path="/path/to/file2.jsp",
            artifact_type="jsp_form",
            language="jsp",
            content_for_embedding="<form id='loginForm'>...</form>",
            details={"form_name": "loginForm"}
        )
    ]
    index_artifacts("test-project", artifacts_to_index, client)
    yield client
    if client.collections.exists("CodeArtifact"):
        client.collections.delete("CodeArtifact")
