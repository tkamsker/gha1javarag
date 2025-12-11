import os
import tempfile
import pytest
from src.discovery.discover_files import discover_files

@pytest.fixture
def temp_project():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create some dummy files
        with open(os.path.join(tmpdir, "file1.java"), "w") as f:
            f.write("test")
        with open(os.path.join(tmpdir, "file2.jsp"), "w") as f:
            f.write("test")
        os.makedirs(os.path.join(tmpdir, "subdir"))
        with open(os.path.join(tmpdir, "subdir", "file3.js"), "w") as f:
            f.write("test")
        yield tmpdir

def test_discover_files(temp_project):
    discovered_files = discover_files("test-project", temp_project)
    assert len(discovered_files) == 3
    file_names = {os.path.basename(f.file_path) for f in discovered_files}
    assert "file1.java" in file_names
    assert "file2.jsp" in file_names
    assert "file3.js" in file_names
