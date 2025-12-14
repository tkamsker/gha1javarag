import pytest
import os
from src.common.models import CodeArtifact
from src.prd.generate_prd import generate_prd

def test_generate_prd():
    # Create some dummy artifacts
    artifacts = [
        CodeArtifact(
            artifact_id="test-project:/path/to/file1.java:UserClass",
            project_name="test-project",
            file_path="/path/to/file1.java",
            artifact_type="java_class",
            language="java",
            framework="",
            details={"class_name": "User"},
            content_for_embedding="public class ClassA { String name; }",
        ),
        CodeArtifact(
            artifact_id="test-project:/path/to/file2.jsp:LoginForm",
            project_name="test-project",
            file_path="/path/to/file2.jsp",
            artifact_type="jsp_form",
            language="jsp",
            framework="",
            details={"form_name": "loginForm"},
            content_for_embedding="<form id='loginForm'>...</form>",
        )
    ]
    
    output_dir = "output/prd"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "test-project_prd.md")

    # Call the PRD generation function
    generate_prd("test-project", artifacts, output_file, False, False) # frontend=False, include_frontend=False

    # Assert that the output file was created and has content
    assert os.path.exists(output_file)
    with open(output_file, "r") as f:
        content = f.read()
        assert len(content) > 0
    
    # Clean up
    os.remove(output_file)
