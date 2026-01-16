"""
Integration tests for Code Viewer (T185 - US4.1).

Tests end-to-end code viewing functionality with real files.
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.codeindex.web.components.code_viewer import CodeViewer
from src.codeindex.web.services.code_service import CodeService, get_code_service
from src.codeindex.web.services.code_lazy_loading import LazyCodeLoader, should_use_lazy_loading


@pytest.fixture
def test_files_dir(tmp_path):
    """Create test files directory with sample source files."""
    # Java file
    java_file = tmp_path / "User.java"
    java_file.write_text("""public class User {
    private String name;
    private String email;

    public User(String name, String email) {
        this.name = name;
        this.email = email;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}""")

    # JSP file
    jsp_file = tmp_path / "user.jsp"
    jsp_file.write_text("""<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>User Profile</title>
</head>
<body>
    <h1>Welcome <%= user.getName() %></h1>
    <p>Email: <%= user.getEmail() %></p>
</body>
</html>""")

    # JavaScript file
    js_file = tmp_path / "app.js"
    js_file.write_text("""function initApp() {
    console.log('App initialized');
    loadUserData();
}

function loadUserData() {
    fetch('/api/user')
        .then(response => response.json())
        .then(data => displayUser(data))
        .catch(error => console.error('Error:', error));
}

function displayUser(user) {
    document.getElementById('username').textContent = user.name;
    document.getElementById('email').textContent = user.email;
}

initApp();""")

    # Large file for lazy loading test
    large_file = tmp_path / "large.txt"
    large_file.write_text("\n".join([f"Line {i}: Some content here" for i in range(1, 6001)]))

    return tmp_path


class TestCodeViewerIntegration:
    """Test code viewer with real files."""

    def test_view_java_file_with_syntax_highlighting(self, test_files_dir):
        """Test viewing Java file with syntax highlighting."""
        service = CodeService(source_root=test_files_dir)
        java_file = test_files_dir / "User.java"

        # Read file
        content = service.read_file("User.java")

        # Create viewer
        viewer = CodeViewer(content=content, file_path=str(java_file))

        assert viewer.language == "java"
        assert "public class User" in viewer.content
        assert len(viewer.content.splitlines()) > 0

    def test_view_jsp_file_with_syntax_highlighting(self, test_files_dir):
        """Test viewing JSP file with syntax highlighting."""
        service = CodeService(source_root=test_files_dir)

        content = service.read_file("user.jsp")
        viewer = CodeViewer(content=content, language="jsp")

        assert viewer.language == "jsp"
        assert "<%@" in viewer.content
        assert "Welcome" in viewer.content

    def test_view_javascript_file_with_syntax_highlighting(self, test_files_dir):
        """Test viewing JavaScript file."""
        service = CodeService(source_root=test_files_dir)

        content = service.read_file("app.js")
        viewer = CodeViewer(content=content, language="javascript")

        assert viewer.language == "javascript"
        assert "function" in viewer.content
        assert "console.log" in viewer.content

    def test_view_file_with_line_highlighting(self, test_files_dir):
        """Test viewing file with specific lines highlighted."""
        service = CodeService(source_root=test_files_dir)
        content = service.read_file("User.java")

        viewer = CodeViewer(content=content, language="java")
        viewer.set_highlighted_lines([5, 6])  # Constructor lines

        rendered = viewer.render()

        assert ">>>" in rendered  # Highlight marker
        assert "User(String name" in content

    def test_search_in_viewed_file(self, test_files_dir):
        """Test searching within viewed file."""
        service = CodeService(source_root=test_files_dir)
        content = service.read_file("User.java")

        viewer = CodeViewer(content=content, language="java")
        matches = viewer.search("name")

        assert len(matches) > 0
        assert any("name" in match.line_content for match in matches)

    def test_copy_and_download_viewed_file(self, test_files_dir):
        """Test copy and download functionality."""
        service = CodeService(source_root=test_files_dir)
        content = service.read_file("User.java")

        viewer = CodeViewer(content=content, language="java")

        # Test copy
        copy_content = viewer.get_copy_content()
        assert copy_content == content

        # Test download
        download_data = viewer.get_download_data()
        assert download_data["content"] == content
        assert download_data["filename"].endswith(".java")


class TestLazyLoadingIntegration:
    """Test lazy loading with large files."""

    def test_lazy_load_large_file(self, test_files_dir):
        """Test lazy loading for large file (>5000 lines)."""
        service = CodeService(source_root=test_files_dir)
        large_file = test_files_dir / "large.txt"

        # Check if file qualifies for lazy loading
        content = service.read_file("large.txt")
        total_lines = len(content.splitlines())
        assert should_use_lazy_loading(total_lines) is True

        # Create lazy loader
        loader = LazyCodeLoader(chunk_size=1000)

        # Load first chunk
        chunk = loader.load_chunk(content, chunk_index=0)

        assert chunk is not None
        assert chunk.start_line == 1
        assert chunk.end_line == 1000
        assert len(chunk.lines) == 1000

    def test_lazy_load_multiple_chunks(self, test_files_dir):
        """Test loading multiple chunks from large file."""
        service = CodeService(source_root=test_files_dir)
        content = service.read_file("large.txt")

        loader = LazyCodeLoader(chunk_size=1000)

        # Load first 3 chunks
        chunks = []
        for i in range(3):
            chunk = loader.load_chunk(content, chunk_index=i)
            chunks.append(chunk)

        assert len(chunks) == 3
        assert chunks[0].end_line == 1000
        assert chunks[1].start_line == 1001
        assert chunks[2].start_line == 2001

    def test_lazy_loading_performance(self, test_files_dir):
        """Test lazy loading performance vs full load."""
        service = CodeService(source_root=test_files_dir)
        content = service.read_file("large.txt")

        # Measure chunk loading time
        import time
        loader = LazyCodeLoader(chunk_size=1000)

        start = time.time()
        chunk = loader.load_chunk(content, chunk_index=0)
        chunk_time = time.time() - start

        # Chunk loading should be fast (<0.1s)
        assert chunk_time < 0.1
        assert chunk is not None


class TestCodeServiceIntegration:
    """Test code service integration."""

    def test_read_and_validate_file_path(self, test_files_dir):
        """Test reading file with path validation."""
        service = CodeService(source_root=test_files_dir)

        # Valid file
        content = service.read_file("User.java")
        assert "public class User" in content

        # Invalid file (directory traversal)
        with pytest.raises(Exception):  # DirectoryTraversalError
            service.read_file("../../etc/passwd")

    def test_file_metadata_retrieval(self, test_files_dir):
        """Test getting file metadata."""
        service = CodeService(source_root=test_files_dir)

        metadata = service.get_file_metadata("User.java")

        assert metadata["exists"] is True
        assert metadata["is_file"] is True
        assert metadata["extension"] == ".java"
        assert metadata["size_bytes"] > 0

    def test_list_files_in_directory(self, test_files_dir):
        """Test listing files in directory."""
        service = CodeService(source_root=test_files_dir)

        files = service.list_files("")

        assert len(files) >= 4  # User.java, user.jsp, app.js, large.txt
        assert any("User.java" in str(f) for f in files)


class TestEndToEndCodeViewing:
    """Test complete end-to-end code viewing workflow."""

    def test_complete_workflow_java_file(self, test_files_dir):
        """Test complete workflow: read → view → highlight → search → download."""
        # Step 1: Initialize service
        service = CodeService(source_root=test_files_dir)

        # Step 2: Read file
        content = service.read_file("User.java")
        assert content is not None

        # Step 3: Create viewer with syntax highlighting
        viewer = CodeViewer(content=content, language="java", show_line_numbers=True)
        assert viewer.language == "java"

        # Step 4: Highlight specific lines (constructor)
        viewer.set_highlighted_lines([5, 6, 7, 8])
        rendered = viewer.render()
        assert ">>>" in rendered

        # Step 5: Search for "getName"
        matches = viewer.search("getName")
        assert len(matches) > 0

        # Step 6: Get download data
        download_data = viewer.get_download_data()
        assert download_data["content"] == content
        assert download_data["filename"].endswith(".java")  # Should be code.java since no file_path provided

    def test_complete_workflow_large_file_with_lazy_loading(self, test_files_dir):
        """Test complete workflow with lazy loading for large file."""
        # Step 1: Initialize service
        service = CodeService(source_root=test_files_dir)

        # Step 2: Read large file
        content = service.read_file("large.txt")
        total_lines = len(content.splitlines())

        # Step 3: Check if lazy loading recommended
        assert should_use_lazy_loading(total_lines) is True

        # Step 4: Create lazy loader
        loader = LazyCodeLoader(chunk_size=1000)

        # Step 5: Load visible chunk (e.g., user scrolled to line 3000)
        chunk_index = 3  # Lines 3001-4000
        chunk = loader.load_chunk(content, chunk_index=chunk_index)

        assert chunk is not None
        assert chunk.start_line == 3001
        assert "Line 3001" in chunk.lines[0]

        # Step 6: Create viewer for chunk
        chunk_content = "\n".join(chunk.lines)
        viewer = CodeViewer(content=chunk_content, language="text")

        # Step 7: Search within chunk
        matches = viewer.search("Line 3500")
        assert len(matches) > 0


class TestStreamlitIntegration:
    """Test Streamlit integration (mocked)."""

    def test_render_with_streamlit_code_component(self, test_files_dir):
        """Test rendering with Streamlit code component."""
        with patch('streamlit.code') as mock_st_code:
            service = CodeService(source_root=test_files_dir)
            content = service.read_file("User.java")

            viewer = CodeViewer(content=content, language="java")
            viewer.render_streamlit()

            # Verify Streamlit code was called
            mock_st_code.assert_called_once()
            args, kwargs = mock_st_code.call_args
            assert "public class User" in args[0]
            assert kwargs.get("language") == "java"

    def test_render_large_file_with_lazy_loading_in_streamlit(self, test_files_dir):
        """Test rendering large file with lazy loading in Streamlit."""
        with patch('streamlit.code') as mock_st_code:
            service = CodeService(source_root=test_files_dir)
            content = service.read_file("large.txt")

            # Use lazy loading
            loader = LazyCodeLoader(chunk_size=1000)
            chunk = loader.load_chunk(content, chunk_index=0)

            # Render chunk in Streamlit
            chunk_content = "\n".join(chunk.lines)
            viewer = CodeViewer(content=chunk_content, language="text")
            viewer.render_streamlit()

            mock_st_code.assert_called_once()


class TestErrorHandlingIntegration:
    """Test error handling in integration scenarios."""

    def test_handle_file_not_found(self, test_files_dir):
        """Test handling of non-existent file."""
        service = CodeService(source_root=test_files_dir)

        with pytest.raises(Exception):  # FileNotFoundError
            service.read_file("nonexistent.java")

    def test_handle_directory_traversal_attack(self, test_files_dir):
        """Test handling of directory traversal attack."""
        service = CodeService(source_root=test_files_dir)

        with pytest.raises(Exception):  # DirectoryTraversalError
            service.read_file("../../../etc/passwd")

    def test_handle_empty_file(self, test_files_dir):
        """Test handling of empty file."""
        empty_file = test_files_dir / "empty.txt"
        empty_file.write_text("")

        service = CodeService(source_root=test_files_dir)
        content = service.read_file("empty.txt")

        viewer = CodeViewer(content=content, language="text")
        rendered = viewer.render()

        assert rendered == ""

    def test_handle_binary_file(self, test_files_dir):
        """Test handling of binary file (should fail gracefully)."""
        binary_file = test_files_dir / "image.png"
        binary_file.write_bytes(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR')

        service = CodeService(source_root=test_files_dir)

        # Should raise error or return garbled text
        try:
            content = service.read_file("image.png")
            # If it doesn't raise, content should be detected as non-text
            assert isinstance(content, str)
        except Exception:
            # Expected to fail for binary files
            pass


class TestCodeViewerWithRealSourceFiles:
    """Test code viewer with real project source files."""

    def test_view_actual_python_file(self):
        """Test viewing actual Python source file from project."""
        # Use this test file itself
        this_file = Path(__file__)

        viewer = CodeViewer(file_path=str(this_file))

        assert viewer.language == "python"
        assert "import pytest" in viewer.content
        assert "TestCodeViewerIntegration" in viewer.content

    def test_search_in_actual_source_file(self):
        """Test searching in actual source file."""
        this_file = Path(__file__)
        viewer = CodeViewer(file_path=str(this_file))

        matches = viewer.search("test_view")

        assert len(matches) > 0
        assert all("test_view" in match.line_content.lower() for match in matches)
