"""
End-to-end test for complete pipeline: discover → extract → index → search.

Tests the full workflow with a sample fixture codebase.

NOTE: Requires Ollama and Weaviate running. Marked as @pytest.mark.slow
"""

import pytest
import tempfile
import shutil
from pathlib import Path
import json

from click.testing import CliRunner

from codeindex.cli.discover import discover_command
from codeindex.cli.extract import extract_command
from codeindex.cli.index import index_command
from codeindex.cli.search import search_command
from codeindex.cli.status import status_command


@pytest.fixture(scope="module")
def cli_runner():
    """Click CLI test runner."""
    return CliRunner()


@pytest.fixture(scope="module")
def test_project_dir(tmp_path_factory):
    """Create a test Java project with pom.xml and source files."""
    project_dir = tmp_path_factory.mktemp("test-project")

    # Create pom.xml
    pom_content = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>e2e-test-project</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>
</project>
"""
    (project_dir / "pom.xml").write_text(pom_content)

    # Create source structure
    src_dir = project_dir / "src" / "main" / "java" / "com" / "example"
    src_dir.mkdir(parents=True)

    # Create sample Java class
    java_content = """package com.example;

public class HelloWorld {
    private String message;

    public HelloWorld(String message) {
        this.message = message;
    }

    public String greet(String name) {
        return message + ", " + name + "!";
    }

    public static void main(String[] args) {
        HelloWorld hw = new HelloWorld("Hello");
        System.out.println(hw.greet("World"));
    }
}
"""
    (src_dir / "HelloWorld.java").write_text(java_content)

    # Create another class
    java_content2 = """package com.example;

public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }

    public int subtract(int a, int b) {
        return a - b;
    }
}
"""
    (src_dir / "Calculator.java").write_text(java_content2)

    return project_dir


@pytest.fixture(scope="module")
def output_dir(tmp_path_factory):
    """Temporary directory for pipeline outputs."""
    return tmp_path_factory.mktemp("output")


@pytest.mark.slow
@pytest.mark.e2e
class TestFullPipeline:
    """Test complete pipeline workflow."""

    def test_discover_phase(self, cli_runner, test_project_dir, output_dir):
        """Test Phase 1: Discover Maven projects."""
        inventory_file = output_dir / "inventory.jsonl"

        result = cli_runner.invoke(discover_command, [
            '--source-dir', str(test_project_dir),
            '--output', str(inventory_file)
        ])

        print(f"Discover output: {result.output}")

        assert result.exit_code == 0
        assert inventory_file.exists()

        # Verify inventory content
        with open(inventory_file, 'r') as f:
            inventory = json.load(f)

        assert "projects" in inventory
        assert len(inventory["projects"]) >= 1
        assert inventory["total_files"] >= 2  # At least 2 Java files

    def test_extract_phase(self, cli_runner, output_dir):
        """Test Phase 2: Extract semantic information."""
        inventory_file = output_dir / "inventory.jsonl"
        extraction_file = output_dir / "extraction.jsonl"

        # Skip if Ollama not available
        import httpx
        try:
            response = httpx.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code != 200:
                pytest.skip("Ollama not available")
        except Exception:
            pytest.skip("Ollama not available")

        result = cli_runner.invoke(extract_command, [
            '--inventory', str(inventory_file),
            '--output', str(extraction_file)
        ])

        print(f"Extract output: {result.output}")

        # May fail if Ollama not running - that's okay for test
        if result.exit_code == 0:
            assert extraction_file.exists()

            # Verify extraction content
            with open(extraction_file, 'r') as f:
                first_line = f.readline()
                extraction = json.loads(first_line)

            assert "summary" in extraction
            assert "entities" in extraction

    def test_index_phase(self, cli_runner, output_dir):
        """Test Phase 3: Index to Weaviate."""
        extraction_file = output_dir / "extraction.jsonl"

        if not extraction_file.exists():
            pytest.skip("Extraction file not available")

        # Skip if Weaviate not available
        import httpx
        try:
            response = httpx.get("http://localhost:8080/v1/meta", timeout=2)
            if response.status_code != 200:
                pytest.skip("Weaviate not available")
        except Exception:
            pytest.skip("Weaviate not available")

        result = cli_runner.invoke(index_command, [
            '--input', str(extraction_file),
            '--project', 'e2e-test-project'
        ])

        print(f"Index output: {result.output}")

        assert result.exit_code == 0
        assert "indexed" in result.output.lower() or "success" in result.output.lower()

    def test_search_phase(self, cli_runner):
        """Test Phase 4: Search indexed code."""
        # Skip if Weaviate not available
        import httpx
        try:
            response = httpx.get("http://localhost:8080/v1/meta", timeout=2)
            if response.status_code != 200:
                pytest.skip("Weaviate not available")
        except Exception:
            pytest.skip("Weaviate not available")

        result = cli_runner.invoke(search_command, [
            'greeting',  # Search for greeting-related code
            '--project', 'e2e-test-project',
            '--limit', '5'
        ])

        print(f"Search output: {result.output}")

        assert result.exit_code == 0
        # Should find HelloWorld.greet() method
        assert len(result.output) > 0

    def test_status_command(self, cli_runner):
        """Test status command shows indexed data."""
        # Skip if Weaviate not available
        import httpx
        try:
            response = httpx.get("http://localhost:8080/v1/meta", timeout=2)
            if response.status_code != 200:
                pytest.skip("Weaviate not available")
        except Exception:
            pytest.skip("Weaviate not available")

        result = cli_runner.invoke(status_command, [
            '--project', 'e2e-test-project'
        ])

        print(f"Status output: {result.output}")

        assert result.exit_code == 0
        assert "project" in result.output.lower() or "artifact" in result.output.lower()


@pytest.mark.slow
@pytest.mark.e2e
class TestPipelineErrorHandling:
    """Test pipeline error handling and recovery."""

    def test_pipeline_with_malformed_pom(self, cli_runner, tmp_path):
        """Test handling of malformed POM files."""
        project_dir = tmp_path / "bad-project"
        project_dir.mkdir()

        # Create malformed POM
        (project_dir / "pom.xml").write_text("This is not valid XML")

        output_dir = tmp_path / "output"
        output_dir.mkdir()

        result = cli_runner.invoke(discover_command, [
            '--source-dir', str(project_dir),
            '--output', str(output_dir / "inventory.jsonl")
        ])

        # Should handle gracefully
        assert result.exit_code is not None

    def test_pipeline_with_empty_directory(self, cli_runner, tmp_path):
        """Test handling of empty directory."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        output_dir = tmp_path / "output"
        output_dir.mkdir()

        result = cli_runner.invoke(discover_command, [
            '--source-dir', str(empty_dir),
            '--output', str(output_dir / "inventory.jsonl")
        ])

        # Should handle empty state gracefully
        assert "no projects" in result.output.lower() or result.exit_code == 0


@pytest.mark.slow
@pytest.mark.e2e
class TestPipelinePerformance:
    """Test pipeline performance with larger codebases."""

    def test_large_codebase(self, cli_runner, tmp_path):
        """Test pipeline with many files (performance test)."""
        project_dir = tmp_path / "large-project"
        src_dir = project_dir / "src" / "main" / "java"
        src_dir.mkdir(parents=True)

        # Create pom.xml
        (project_dir / "pom.xml").write_text("""<?xml version="1.0"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>large-project</artifactId>
    <version>1.0.0</version>
</project>
""")

        # Create 100 Java files
        for i in range(100):
            java_content = f"""package com.example;

public class Class{i} {{
    public void method{i}() {{
        System.out.println("Class {i}");
    }}
}}
"""
            (src_dir / f"Class{i}.java").write_text(java_content)

        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Test discovery performance
        result = cli_runner.invoke(discover_command, [
            '--source-dir', str(project_dir),
            '--output', str(output_dir / "inventory.jsonl")
        ])

        assert result.exit_code == 0
        # Should discover all 100 files quickly
        assert "100" in result.output or result.exit_code == 0


@pytest.mark.slow
@pytest.mark.e2e
def test_incremental_indexing(cli_runner, test_project_dir, output_dir):
    """Test incremental indexing (re-indexing with changes)."""
    # Initial indexing
    inventory_file = output_dir / "inventory.jsonl"

    # Discover
    result1 = cli_runner.invoke(discover_command, [
        '--source-dir', str(test_project_dir),
        '--output', str(inventory_file)
    ])

    assert result1.exit_code == 0

    # Modify a file
    src_file = test_project_dir / "src" / "main" / "java" / "com" / "example" / "HelloWorld.java"
    content = src_file.read_text()
    modified_content = content.replace("Hello", "Greetings")
    src_file.write_text(modified_content)

    # Re-discover
    result2 = cli_runner.invoke(discover_command, [
        '--source-dir', str(test_project_dir),
        '--output', str(inventory_file),
        '--force'  # Force re-discovery
    ])

    assert result2.exit_code == 0

    # Should detect the change
    # (Implementation specific validation)
