import os
import tempfile
import pytest
from src.common.models import DiscoveredFile
from src.extraction.extract_artifacts import extract_artifacts

@pytest.fixture
def temp_project_with_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        java_content = "public class MyClass { public void myMethod() {} }"
        java_path = os.path.join(tmpdir, "MyClass.java")
        with open(java_path, "w") as f:
            f.write(java_content)

        jsp_content = "<form action='/submit'></form>"
        jsp_path = os.path.join(tmpdir, "myform.jsp")
        with open(jsp_path, "w") as f:
            f.write(jsp_content)
            
        discovered_files = [
            DiscoveredFile("test-project", java_path, "java"),
            DiscoveredFile("test-project", jsp_path, "jsp"),
        ]
        yield discovered_files

def test_extract_artifacts(temp_project_with_files):
    artifacts = extract_artifacts("test-project", temp_project_with_files)
    assert len(artifacts) > 0
    # Add more specific assertions here based on expected artifacts
