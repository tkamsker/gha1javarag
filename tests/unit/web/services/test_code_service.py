"""
Unit tests for Code Service (T182 - US4.1).

Tests code reading, path validation, and security checks.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
from src.codeindex.web.services.code_service import (
    CodeService,
    read_source_file,
    validate_file_path,
    get_file_info,
    CodeServiceError,
    FileNotFoundError as CodeFileNotFoundError,
    FileTooLargeError,
    DirectoryTraversalError
)


@pytest.fixture
def code_service():
    """Create CodeService instance."""
    return CodeService(source_root="/test/source/root")


@pytest.fixture
def temp_source_dir(tmp_path):
    """Create temporary source directory with test files."""
    # Create test directory structure
    java_file = tmp_path / "com" / "example" / "User.java"
    java_file.parent.mkdir(parents=True, exist_ok=True)
    java_file.write_text("public class User { }")

    jsp_file = tmp_path / "webapp" / "user.jsp"
    jsp_file.parent.mkdir(parents=True, exist_ok=True)
    jsp_file.write_text("<html><body>User Page</body></html>")

    large_file = tmp_path / "large.txt"
    large_file.write_text("x" * (11 * 1024 * 1024))  # 11MB file

    return tmp_path


class TestCodeServiceInitialization:
    """Test CodeService initialization."""

    def test_init_with_source_root(self):
        """Test initialization with source root."""
        service = CodeService(source_root="/path/to/source")
        assert service.source_root == Path("/path/to/source")

    def test_init_without_source_root(self):
        """Test initialization without source root (uses config)."""
        with patch('src.codeindex.utils.config.get_config') as mock_config:
            mock_config.return_value.get.return_value = "/default/source"
            service = CodeService()
            assert service.source_root == Path("/default/source")

    def test_init_with_max_file_size(self):
        """Test initialization with custom max file size."""
        service = CodeService(source_root="/test", max_file_size_mb=20)
        assert service.max_file_size_bytes == 20 * 1024 * 1024


class TestFilePathValidation:
    """Test file path validation and security."""

    def test_validate_absolute_path_within_root(self, code_service):
        """Test validation of absolute path within root."""
        file_path = "/test/source/root/com/example/User.java"
        is_valid, resolved = validate_file_path(file_path, code_service.source_root)
        assert is_valid
        assert resolved == Path(file_path)

    def test_validate_relative_path_within_root(self, code_service):
        """Test validation of relative path within root."""
        file_path = "com/example/User.java"
        is_valid, resolved = validate_file_path(file_path, code_service.source_root)
        assert is_valid
        assert resolved == code_service.source_root / file_path

    def test_reject_directory_traversal_with_dotdot(self, code_service):
        """Test rejection of directory traversal using .."""
        file_path = "../../../etc/passwd"
        with pytest.raises(DirectoryTraversalError, match="outside source root"):
            validate_file_path(file_path, code_service.source_root)

    def test_reject_absolute_path_outside_root(self, code_service):
        """Test rejection of absolute path outside root."""
        file_path = "/etc/passwd"
        with pytest.raises(DirectoryTraversalError, match="outside source root"):
            validate_file_path(file_path, code_service.source_root)

    def test_reject_symlink_outside_root(self, tmp_path, code_service):
        """Test rejection of symlink pointing outside root."""
        # Create symlink to /etc/passwd
        source_root = tmp_path / "source"
        source_root.mkdir()
        symlink = source_root / "evil.txt"
        symlink.symlink_to("/etc/passwd")

        code_service.source_root = source_root

        with pytest.raises(DirectoryTraversalError, match="outside source root"):
            validate_file_path(str(symlink), code_service.source_root)

    def test_normalize_windows_path_separators(self, code_service):
        """Test normalization of Windows-style path separators."""
        file_path = "com\\example\\User.java"
        is_valid, resolved = validate_file_path(file_path, code_service.source_root)
        assert is_valid
        # Path should be normalized to forward slashes
        assert "com/example/User.java" in str(resolved) or "com\\example\\User.java" in str(resolved)


class TestReadSourceFile:
    """Test file reading functionality."""

    def test_read_java_file(self, temp_source_dir):
        """Test reading Java source file."""
        service = CodeService(source_root=temp_source_dir)
        file_path = "com/example/User.java"

        content = read_source_file(service.source_root / file_path)

        assert content == "public class User { }"

    def test_read_jsp_file(self, temp_source_dir):
        """Test reading JSP file."""
        service = CodeService(source_root=temp_source_dir)
        file_path = "webapp/user.jsp"

        content = read_source_file(service.source_root / file_path)

        assert "<html>" in content
        assert "User Page" in content

    def test_read_file_with_encoding_utf8(self, tmp_path):
        """Test reading file with UTF-8 encoding."""
        test_file = tmp_path / "utf8.txt"
        test_file.write_text("Hello 世界 🌍", encoding='utf-8')

        content = read_source_file(test_file, encoding='utf-8')

        assert "Hello 世界 🌍" in content

    def test_read_nonexistent_file(self, temp_source_dir):
        """Test reading non-existent file raises error."""
        service = CodeService(source_root=temp_source_dir)
        file_path = service.source_root / "nonexistent.java"

        with pytest.raises(CodeFileNotFoundError, match="File not found"):
            read_source_file(file_path)

    def test_read_file_too_large(self, temp_source_dir):
        """Test reading file larger than max size raises error."""
        service = CodeService(source_root=temp_source_dir, max_file_size_mb=10)
        file_path = service.source_root / "large.txt"

        with pytest.raises(FileTooLargeError, match="File too large"):
            service.read_file("large.txt")

    def test_read_directory_raises_error(self, temp_source_dir):
        """Test reading directory raises error."""
        service = CodeService(source_root=temp_source_dir)

        with pytest.raises(CodeServiceError, match="is a directory"):
            read_source_file(service.source_root / "com")


class TestGetFileInfo:
    """Test file information retrieval."""

    def test_get_file_info_for_existing_file(self, temp_source_dir):
        """Test getting file info for existing file."""
        file_path = temp_source_dir / "com" / "example" / "User.java"

        info = get_file_info(file_path)

        assert info["exists"] is True
        assert info["is_file"] is True
        assert info["size_bytes"] == len("public class User { }")
        assert info["extension"] == ".java"
        assert "modified_time" in info

    def test_get_file_info_for_nonexistent_file(self, temp_source_dir):
        """Test getting file info for non-existent file."""
        file_path = temp_source_dir / "nonexistent.java"

        info = get_file_info(file_path)

        assert info["exists"] is False
        assert info["is_file"] is False
        assert info["size_bytes"] == 0

    def test_get_file_info_for_directory(self, temp_source_dir):
        """Test getting file info for directory."""
        dir_path = temp_source_dir / "com"

        info = get_file_info(dir_path)

        assert info["exists"] is True
        assert info["is_file"] is False
        assert info["is_directory"] is True


class TestCodeServiceHighLevel:
    """Test CodeService high-level operations."""

    def test_read_file_success(self, temp_source_dir):
        """Test successful file reading via CodeService."""
        service = CodeService(source_root=temp_source_dir)

        content = service.read_file("com/example/User.java")

        assert content == "public class User { }"

    def test_read_file_with_validation(self, temp_source_dir):
        """Test file reading with path validation."""
        service = CodeService(source_root=temp_source_dir)

        # Should succeed for valid path
        content = service.read_file("com/example/User.java")
        assert content is not None

        # Should fail for invalid path
        with pytest.raises(DirectoryTraversalError):
            service.read_file("../../etc/passwd")

    def test_get_file_metadata(self, temp_source_dir):
        """Test getting file metadata via CodeService."""
        service = CodeService(source_root=temp_source_dir)

        metadata = service.get_file_metadata("com/example/User.java")

        assert metadata["exists"] is True
        assert metadata["is_file"] is True
        assert metadata["extension"] == ".java"
        assert metadata["relative_path"] == "com/example/User.java"

    def test_list_directory_files(self, temp_source_dir):
        """Test listing files in directory via CodeService."""
        service = CodeService(source_root=temp_source_dir)

        files = service.list_files("com/example")

        assert len(files) > 0
        assert any("User.java" in str(f) for f in files)

    def test_check_file_exists(self, temp_source_dir):
        """Test checking if file exists via CodeService."""
        service = CodeService(source_root=temp_source_dir)

        assert service.file_exists("com/example/User.java") is True
        assert service.file_exists("nonexistent.java") is False


class TestErrorHandling:
    """Test error handling in CodeService."""

    def test_handle_permission_denied(self, tmp_path):
        """Test handling of permission denied error."""
        # Create file with no read permissions (Unix only)
        import os
        if os.name != 'nt':  # Skip on Windows
            test_file = tmp_path / "nopermission.txt"
            test_file.write_text("secret")
            test_file.chmod(0o000)  # No permissions

            service = CodeService(source_root=tmp_path)

            with pytest.raises(CodeServiceError, match="Permission denied"):
                service.read_file("nopermission.txt")

    def test_handle_unicode_decode_error(self, tmp_path):
        """Test handling of unicode decode errors."""
        # Create binary file (not UTF-8)
        binary_file = tmp_path / "binary.dat"
        binary_file.write_bytes(b'\x80\x81\x82\x83')

        with pytest.raises(CodeServiceError, match="encoding error"):
            read_source_file(binary_file, encoding='utf-8')

    def test_error_includes_file_path(self, temp_source_dir):
        """Test that errors include file path in message."""
        service = CodeService(source_root=temp_source_dir)

        try:
            service.read_file("nonexistent.java")
        except CodeFileNotFoundError as e:
            assert "nonexistent.java" in str(e)


class TestCaching:
    """Test file content caching (optional optimization)."""

    def test_cache_file_content(self, temp_source_dir):
        """Test that file content is cached after first read."""
        service = CodeService(source_root=temp_source_dir, enable_cache=True)

        # First read
        content1 = service.read_file("com/example/User.java")

        # Second read (should use cache)
        content2 = service.read_file("com/example/User.java")

        assert content1 == content2

    def test_cache_invalidation_on_file_change(self, temp_source_dir):
        """Test that cache is invalidated when file changes."""
        service = CodeService(source_root=temp_source_dir, enable_cache=True)
        file_path = temp_source_dir / "com" / "example" / "User.java"

        # First read
        content1 = service.read_file("com/example/User.java")

        # Modify file
        file_path.write_text("public class User { String name; }")

        # Second read (should detect change and re-read)
        content2 = service.read_file("com/example/User.java")

        assert content1 != content2
        assert "String name" in content2
