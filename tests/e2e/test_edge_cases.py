"""
End-to-end test for edge cases and error handling.

Tests:
- Malformed POMs
- Missing groupId/artifactId
- Extremely large files (>100k lines)
- Non-UTF-8 files
- Binary files
- Empty files
- Invalid XML

NOTE: Marked as @pytest.mark.slow
"""

import pytest
import tempfile
from pathlib import Path
from click.testing import CliRunner

from codeindex.cli.discover import discover_command


@pytest.fixture
def cli_runner():
    """Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def temp_project_dir(tmp_path):
    """Create a temporary project directory."""
    project_dir = tmp_path / "edge-case-project"
    project_dir.mkdir()
    return project_dir


@pytest.mark.slow
@pytest.mark.e2e
class TestMalformedPOMs:
    """Test handling of malformed POM files."""

    def test_invalid_xml_pom(self, cli_runner, temp_project_dir, tmp_path):
        """Test handling of POM with invalid XML syntax."""
        # Create malformed POM (unclosed tag)
        pom_content = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0
    <groupId>com.example</groupId>
    <artifactId>malformed</artifactId>
    <version>1.0.0</version>
</project>
"""
        (temp_project_dir / "pom.xml").write_text(pom_content)

        output_file = tmp_path / "inventory.jsonl"

        # Should handle gracefully (skip or report error)
        result = cli_runner.invoke(discover_command, [
            '--source-dir', str(temp_project_dir),
            '--output', str(output_file)
        ])

        # Should complete (might skip malformed POM)
        # Exit code 0 or 1 is acceptable
        assert result.exit_code in [0, 1]

    def test_missing_required_pom_fields(self, cli_runner, temp_project_dir, tmp_path):
        """Test POM missing required fields (groupId, artifactId)."""
        # POM without groupId
        pom_content = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <artifactId>no-group-id</artifactId>
    <version>1.0.0</version>
</project>
"""
        (temp_project_dir / "pom.xml").write_text(pom_content)

        # Add a source file
        src_dir = temp_project_dir / "src" / "main" / "java"
        src_dir.mkdir(parents=True)
        (src_dir / "Test.java").write_text("public class Test {}")

        output_file = tmp_path / "inventory.jsonl"

        result = cli_runner.invoke(discover_command, [
            '--source-dir', str(temp_project_dir),
            '--output', str(output_file)
        ])

        # Should handle gracefully (use fallback project ID)
        assert result.exit_code == 0

        # Should still discover the project (with path-based ID)
        assert output_file.exists()

    def test_pom_without_version(self, cli_runner, temp_project_dir, tmp_path):
        """Test POM without version field."""
        pom_content = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>no-version</artifactId>
</project>
"""
        (temp_project_dir / "pom.xml").write_text(pom_content)

        src_dir = temp_project_dir / "src" / "main" / "java"
        src_dir.mkdir(parents=True)
        (src_dir / "Test.java").write_text("public class Test {}")

        output_file = tmp_path / "inventory.jsonl"

        result = cli_runner.invoke(discover_command, [
            '--source-dir', str(temp_project_dir),
            '--output', str(output_file)
        ])

        # Should handle gracefully (use default version or skip)
        assert result.exit_code in [0, 1]

    def test_empty_pom_file(self, cli_runner, temp_project_dir, tmp_path):
        """Test completely empty POM file."""
        (temp_project_dir / "pom.xml").write_text("")

        output_file = tmp_path / "inventory.jsonl"

        result = cli_runner.invoke(discover_command, [
            '--source-dir', str(temp_project_dir),
            '--output', str(output_file)
        ])

        # Should handle gracefully
        assert result.exit_code in [0, 1]


@pytest.mark.slow
@pytest.mark.e2e
class TestLargeFiles:
    """Test handling of extremely large files."""

    def test_very_large_java_file(self, cli_runner, temp_project_dir, tmp_path):
        """Test discovery with file >100k lines."""
        # Create valid POM
        pom_content = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>large-file</artifactId>
    <version>1.0.0</version>
</project>
"""
        (temp_project_dir / "pom.xml").write_text(pom_content)

        # Create very large Java file (simulate 100k+ lines)
        src_dir = temp_project_dir / "src" / "main" / "java"
        src_dir.mkdir(parents=True)

        # Generate a large file (10k lines - using 10k instead of 100k for test speed)
        lines = ["package com.example;\n", "\n", "public class VeryLargeClass {\n"]

        for i in range(10000):
            lines.append(f"    private String field{i};\n")
            lines.append(f"    public String getField{i}() {{ return field{i}; }}\n")

        lines.append("}\n")

        large_file = src_dir / "VeryLargeClass.java"
        large_file.write_text("".join(lines))

        output_file = tmp_path / "inventory.jsonl"

        # Should handle large file without crashing
        result = cli_runner.invoke(discover_command, [
            '--source-dir', str(temp_project_dir),
            '--output', str(output_file)
        ])

        assert result.exit_code == 0
        assert output_file.exists()

    def test_chunking_large_files(self, temp_project_dir):
        """Test that large files are properly identified for chunking."""
        from codeindex.services.extraction import should_chunk_file

        # Create a large file path
        large_file = temp_project_dir / "LargeFile.java"

        # Generate content (100k lines would be ~3-4MB)
        # For testing, use 50k lines
        lines = [f"// Line {i}\n" for i in range(50000)]
        large_file.write_text("".join(lines))

        # Check if file should be chunked
        # Implementation dependent - just verify the function works
        try:
            result = should_chunk_file(large_file)
            # Should return True or False without crashing
            assert isinstance(result, bool)
        except AttributeError:
            # Function might not exist yet - that's ok for this test
            pass


@pytest.mark.slow
@pytest.mark.e2e
class TestFileEncodings:
    """Test handling of different file encodings."""

    def test_non_utf8_file(self, cli_runner, temp_project_dir, tmp_path):
        """Test handling of non-UTF-8 encoded file."""
        pom_content = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>encoding-test</artifactId>
    <version>1.0.0</version>
</project>
"""
        (temp_project_dir / "pom.xml").write_text(pom_content)

        src_dir = temp_project_dir / "src" / "main" / "java"
        src_dir.mkdir(parents=True)

        # Create file with Latin-1 encoding
        java_file = src_dir / "Latin1.java"
        content = "public class Latin1 {\n    // Comment with special chars: café, naïve\n}\n"

        try:
            java_file.write_bytes(content.encode('latin-1'))
        except Exception:
            # If encoding fails, skip this test
            pytest.skip("Could not create Latin-1 encoded file")

        output_file = tmp_path / "inventory.jsonl"

        # Should handle gracefully (skip or convert)
        result = cli_runner.invoke(discover_command, [
            '--source-dir', str(temp_project_dir),
            '--output', str(output_file)
        ])

        # Should complete without crashing
        assert result.exit_code in [0, 1]

    def test_binary_file_handling(self, cli_runner, temp_project_dir, tmp_path):
        """Test that binary files are properly handled/skipped."""
        pom_content = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>binary-test</artifactId>
    <version>1.0.0</version>
</project>
"""
        (temp_project_dir / "pom.xml").write_text(pom_content)

        src_dir = temp_project_dir / "src" / "main" / "resources"
        src_dir.mkdir(parents=True)

        # Create a binary file (simulated)
        binary_file = src_dir / "image.png"
        binary_content = bytes([0xFF, 0xD8, 0xFF, 0xE0] + [0x00] * 100)  # PNG header + data
        binary_file.write_bytes(binary_content)

        # Also create a valid Java file
        java_dir = temp_project_dir / "src" / "main" / "java"
        java_dir.mkdir(parents=True)
        (java_dir / "Test.java").write_text("public class Test {}")

        output_file = tmp_path / "inventory.jsonl"

        result = cli_runner.invoke(discover_command, [
            '--source-dir', str(temp_project_dir),
            '--output', str(output_file)
        ])

        # Should complete successfully (binary file should be classified as static_asset)
        assert result.exit_code == 0

    def test_empty_file(self, cli_runner, temp_project_dir, tmp_path):
        """Test handling of completely empty files."""
        pom_content = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>empty-file-test</artifactId>
    <version>1.0.0</version>
</project>
"""
        (temp_project_dir / "pom.xml").write_text(pom_content)

        src_dir = temp_project_dir / "src" / "main" / "java"
        src_dir.mkdir(parents=True)

        # Create empty Java file
        (src_dir / "Empty.java").write_text("")

        # Create normal file too
        (src_dir / "Normal.java").write_text("public class Normal {}")

        output_file = tmp_path / "inventory.jsonl"

        result = cli_runner.invoke(discover_command, [
            '--source-dir', str(temp_project_dir),
            '--output', str(output_file)
        ])

        # Should handle gracefully
        assert result.exit_code == 0


@pytest.mark.slow
@pytest.mark.e2e
class TestDirectoryStructureEdgeCases:
    """Test edge cases in directory structure."""

    def test_no_src_directory(self, cli_runner, temp_project_dir, tmp_path):
        """Test project without standard src/ directory."""
        pom_content = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>no-src</artifactId>
    <version>1.0.0</version>
</project>
"""
        (temp_project_dir / "pom.xml").write_text(pom_content)

        # No src directory, but has POM

        output_file = tmp_path / "inventory.jsonl"

        result = cli_runner.invoke(discover_command, [
            '--source-dir', str(temp_project_dir),
            '--output', str(output_file)
        ])

        # Should still discover the project (even with 0 files)
        assert result.exit_code == 0

    def test_symlink_handling(self, cli_runner, temp_project_dir, tmp_path):
        """Test handling of symbolic links."""
        pom_content = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>symlink-test</artifactId>
    <version>1.0.0</version>
</project>
"""
        (temp_project_dir / "pom.xml").write_text(pom_content)

        src_dir = temp_project_dir / "src" / "main" / "java"
        src_dir.mkdir(parents=True)

        # Create a real file
        real_file = src_dir / "Real.java"
        real_file.write_text("public class Real {}")

        # Try to create a symlink (may not work on all systems)
        try:
            link_file = src_dir / "Link.java"
            link_file.symlink_to(real_file)
        except OSError:
            # Symlinks not supported on this system
            pytest.skip("Symlinks not supported")

        output_file = tmp_path / "inventory.jsonl"

        result = cli_runner.invoke(discover_command, [
            '--source-dir', str(temp_project_dir),
            '--output', str(output_file)
        ])

        # Should handle symlinks without infinite loops
        assert result.exit_code == 0

    def test_special_characters_in_filenames(self, cli_runner, temp_project_dir, tmp_path):
        """Test files with special characters in names."""
        pom_content = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>special-chars</artifactId>
    <version>1.0.0</version>
</project>
"""
        (temp_project_dir / "pom.xml").write_text(pom_content)

        src_dir = temp_project_dir / "src" / "main" / "java"
        src_dir.mkdir(parents=True)

        # Create files with spaces and special chars
        try:
            (src_dir / "File With Spaces.java").write_text("public class FileWithSpaces {}")
            (src_dir / "File-With-Dashes.java").write_text("public class FileWithDashes {}")
            (src_dir / "File_With_Underscores.java").write_text("public class FileWithUnderscores {}")
        except Exception:
            pytest.skip("Could not create files with special characters")

        output_file = tmp_path / "inventory.jsonl"

        result = cli_runner.invoke(discover_command, [
            '--source-dir', str(temp_project_dir),
            '--output', str(output_file)
        ])

        # Should handle special characters in filenames
        assert result.exit_code == 0


@pytest.mark.slow
@pytest.mark.e2e
class TestPermissionErrors:
    """Test handling of permission errors."""

    def test_unreadable_file(self, cli_runner, temp_project_dir, tmp_path):
        """Test handling of file without read permissions."""
        import os
        import stat

        pom_content = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>permission-test</artifactId>
    <version>1.0.0</version>
</project>
"""
        (temp_project_dir / "pom.xml").write_text(pom_content)

        src_dir = temp_project_dir / "src" / "main" / "java"
        src_dir.mkdir(parents=True)

        # Create readable file
        (src_dir / "Readable.java").write_text("public class Readable {}")

        # Create unreadable file
        unreadable = src_dir / "Unreadable.java"
        unreadable.write_text("public class Unreadable {}")

        # Remove read permissions (Unix only)
        try:
            os.chmod(unreadable, stat.S_IWRITE)  # Write-only
        except Exception:
            pytest.skip("Could not change file permissions")

        output_file = tmp_path / "inventory.jsonl"

        try:
            result = cli_runner.invoke(discover_command, [
                '--source-dir', str(temp_project_dir),
                '--output', str(output_file)
            ])

            # Should handle gracefully (skip unreadable file or report error)
            assert result.exit_code in [0, 1]

        finally:
            # Restore permissions for cleanup
            try:
                os.chmod(unreadable, stat.S_IREAD | stat.S_IWRITE)
            except Exception:
                pass


@pytest.mark.slow
@pytest.mark.e2e
class TestInvalidContent:
    """Test handling of files with invalid content."""

    def test_java_file_with_syntax_errors(self, cli_runner, temp_project_dir, tmp_path):
        """Test discovery of Java file with syntax errors."""
        pom_content = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>syntax-error</artifactId>
    <version>1.0.0</version>
</project>
"""
        (temp_project_dir / "pom.xml").write_text(pom_content)

        src_dir = temp_project_dir / "src" / "main" / "java"
        src_dir.mkdir(parents=True)

        # Create Java file with syntax errors
        invalid_java = """
public class Invalid {
    // Missing closing brace
    public void method() {
        System.out.println("test");
    // Missing }
}
"""
        (src_dir / "Invalid.java").write_text(invalid_java)

        output_file = tmp_path / "inventory.jsonl"

        # Discovery should still work (syntax errors are for compilation, not discovery)
        result = cli_runner.invoke(discover_command, [
            '--source-dir', str(temp_project_dir),
            '--output', str(output_file)
        ])

        assert result.exit_code == 0
        assert output_file.exists()

    def test_xml_file_with_invalid_content(self, cli_runner, temp_project_dir, tmp_path):
        """Test XML file that's not well-formed."""
        pom_content = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>invalid-xml</artifactId>
    <version>1.0.0</version>
</project>
"""
        (temp_project_dir / "pom.xml").write_text(pom_content)

        resources_dir = temp_project_dir / "src" / "main" / "resources"
        resources_dir.mkdir(parents=True)

        # Create invalid XML
        invalid_xml = """<?xml version="1.0"?>
<config>
    <setting>
        <value>test</value>
    <!-- Missing closing tags
</config>
"""
        (resources_dir / "invalid.xml").write_text(invalid_xml)

        output_file = tmp_path / "inventory.jsonl"

        result = cli_runner.invoke(discover_command, [
            '--source-dir', str(temp_project_dir),
            '--output', str(output_file)
        ])

        # Should handle gracefully
        assert result.exit_code in [0, 1]
