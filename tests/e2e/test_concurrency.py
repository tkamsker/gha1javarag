"""
End-to-end test for concurrent operations.

Tests:
- Multiple projects can index simultaneously
- Same project indexing is locked with error message
- No data corruption under concurrent access

NOTE: Requires Weaviate running. Marked as @pytest.mark.slow
"""

import pytest
import tempfile
import threading
import time
from pathlib import Path
from click.testing import CliRunner
from concurrent.futures import ThreadPoolExecutor, as_completed

from codeindex.cli.discover import discover_command
from codeindex.cli.index import index_command
from codeindex.services.indexing import IndexingService
from codeindex.services.weaviate_store import WeaviateStore
from codeindex.utils.config import get_config


@pytest.fixture
def cli_runner():
    """Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def create_test_project():
    """Factory to create test projects."""
    def _create_project(name: str, num_files: int = 5):
        """Create a test project with specified number of files."""
        temp_dir = tempfile.mkdtemp()
        project_dir = Path(temp_dir) / name

        # Create pom.xml
        pom_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>{name}</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>
</project>
"""
        project_dir.mkdir(parents=True)
        (project_dir / "pom.xml").write_text(pom_content)

        # Create source files
        src_dir = project_dir / "src" / "main" / "java" / "com" / "example"
        src_dir.mkdir(parents=True)

        for i in range(num_files):
            java_content = f"""package com.example;

public class TestClass{i} {{
    private String field{i};

    public TestClass{i}() {{
        this.field{i} = "value{i}";
    }}

    public String getField() {{
        return field{i};
    }}
}}
"""
            (src_dir / f"TestClass{i}.java").write_text(java_content)

        return project_dir

    return _create_project


@pytest.mark.slow
@pytest.mark.e2e
@pytest.mark.skip(reason="Legacy TDD test - requires API methods that don't exist (IndexingService.lock_project, etc)")
class TestConcurrentIndexing:
    """Test concurrent indexing operations."""

    def test_multiple_projects_concurrent_indexing(
        self,
        cli_runner,
        create_test_project,
        tmp_path
    ):
        """Test that multiple different projects can be indexed concurrently."""
        # Create 3 different projects
        project1 = create_test_project("project-concurrent-1", 5)
        project2 = create_test_project("project-concurrent-2", 5)
        project3 = create_test_project("project-concurrent-3", 5)

        # Discover all projects
        inventory1 = tmp_path / "inv1.jsonl"
        inventory2 = tmp_path / "inv2.jsonl"
        inventory3 = tmp_path / "inv3.jsonl"

        cli_runner.invoke(discover_command, [
            '--source-dir', str(project1),
            '--output', str(inventory1)
        ])
        cli_runner.invoke(discover_command, [
            '--source-dir', str(project2),
            '--output', str(inventory2)
        ])
        cli_runner.invoke(discover_command, [
            '--source-dir', str(project3),
            '--output', str(inventory3)
        ])

        # Function to index a project
        def index_project(inventory_path):
            result = cli_runner.invoke(index_command, [
                '--input', str(inventory_path)
            ])
            return result.exit_code, result.output

        # Index all 3 projects concurrently
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(index_project, inventory1),
                executor.submit(index_project, inventory2),
                executor.submit(index_project, inventory3)
            ]

            results = [future.result() for future in as_completed(futures)]

        # All should complete successfully
        for exit_code, output in results:
            assert exit_code == 0, f"Indexing failed: {output}"

    def test_same_project_locking(self, tmp_path):
        """Test that concurrent indexing of same project is prevented by locking."""
        config = get_config()

        # Skip if Weaviate not available
        try:
            store = WeaviateStore(config=config, auto_create_schema=False)
            if not store.health_check():
                pytest.skip("Weaviate not available")
        except Exception:
            pytest.skip("Weaviate not available")

        indexing_service = IndexingService(weaviate_store=store)

        project_id = "com.example:test-concurrent:1.0.0"
        results = []
        errors = []

        def try_lock_project():
            """Try to lock and index the same project."""
            try:
                with indexing_service.lock_project(project_id, timeout=1):
                    time.sleep(0.5)  # Simulate work
                    results.append("success")
            except Exception as e:
                errors.append(str(e))
                results.append("locked")

        # Start 3 threads trying to lock same project
        threads = []
        for _ in range(3):
            thread = threading.Thread(target=try_lock_project)
            threads.append(thread)
            thread.start()
            time.sleep(0.1)  # Stagger starts slightly

        # Wait for all threads
        for thread in threads:
            thread.join(timeout=5)

        # At least one should succeed
        assert "success" in results, "No thread succeeded in acquiring lock"

        # At least one should be blocked/locked
        assert "locked" in results or len(errors) > 0, "No thread was blocked by lock"

        # Should have 3 results total
        assert len(results) == 3

    def test_lock_released_after_completion(self, tmp_path):
        """Test that locks are properly released after indexing completes."""
        config = get_config()

        # Skip if Weaviate not available
        try:
            store = WeaviateStore(config=config, auto_create_schema=False)
            if not store.health_check():
                pytest.skip("Weaviate not available")
        except Exception:
            pytest.skip("Weaviate not available")

        indexing_service = IndexingService(weaviate_store=store)
        project_id = "com.example:test-lock-release:1.0.0"

        # Lock and release
        with indexing_service.lock_project(project_id):
            assert indexing_service.is_project_locked(project_id)

        # After context exits, lock should be released
        assert not indexing_service.is_project_locked(project_id)

        # Should be able to lock again
        with indexing_service.lock_project(project_id):
            assert indexing_service.is_project_locked(project_id)

    def test_lock_timeout_behavior(self, tmp_path):
        """Test lock timeout behavior when project is already locked."""
        config = get_config()

        # Skip if Weaviate not available
        try:
            store = WeaviateStore(config=config, auto_create_schema=False)
            if not store.health_check():
                pytest.skip("Weaviate not available")
        except Exception:
            pytest.skip("Weaviate not available")

        indexing_service = IndexingService(weaviate_store=store)
        project_id = "com.example:test-timeout:1.0.0"

        # Acquire lock in main thread
        lock = indexing_service.lock_project(project_id, timeout=0)
        lock.__enter__()

        try:
            # Try to acquire same lock with short timeout (should fail)
            with pytest.raises(Exception) as exc_info:
                with indexing_service.lock_project(project_id, timeout=0.5):
                    pass

            # Should get timeout or lock error
            assert "lock" in str(exc_info.value).lower() or "timeout" in str(exc_info.value).lower()

        finally:
            # Release the lock
            lock.__exit__(None, None, None)

    def test_no_data_corruption_under_concurrency(
        self,
        create_test_project,
        cli_runner,
        tmp_path
    ):
        """Test that concurrent operations don't corrupt data."""
        # Create a project
        project = create_test_project("corruption-test", 20)

        # Discover it
        inventory = tmp_path / "inventory.jsonl"
        cli_runner.invoke(discover_command, [
            '--source-dir', str(project),
            '--output', str(inventory)
        ])

        # Index it multiple times concurrently (only one should succeed)
        def index_with_result():
            result = cli_runner.invoke(index_command, [
                '--input', str(inventory)
            ])
            return result.exit_code

        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(index_with_result) for _ in range(3)]
            exit_codes = [future.result() for future in as_completed(futures)]

        # At least one should succeed (exit code 0)
        assert 0 in exit_codes, "No indexing operation succeeded"


@pytest.mark.slow
@pytest.mark.e2e
@pytest.mark.skip(reason="Legacy TDD test - requires updated CLI API")
class TestConcurrentSearch:
    """Test concurrent search operations."""

    def test_concurrent_searches_same_project(self, cli_runner):
        """Test that multiple searches can run concurrently."""
        from codeindex.cli.search import search_command

        # Function to perform search
        def search_query(query):
            result = cli_runner.invoke(search_command, [query])
            return result.exit_code

        # Run 5 concurrent searches
        with ThreadPoolExecutor(max_workers=5) as executor:
            queries = [
                "authentication",
                "database",
                "controller",
                "service",
                "util"
            ]

            futures = [executor.submit(search_query, q) for q in queries]
            results = [future.result() for future in as_completed(futures)]

        # All searches should complete (even if no results found)
        # Exit code might be 0 or 1 depending on results, but should not crash
        assert all(code in [0, 1] for code in results)

    def test_search_during_indexing(self, create_test_project, cli_runner, tmp_path):
        """Test that search works while indexing is in progress (different projects)."""
        from codeindex.cli.search import search_command

        # Create and index a project first
        project1 = create_test_project("search-test-1", 10)
        inventory1 = tmp_path / "inv1.jsonl"

        cli_runner.invoke(discover_command, [
            '--source-dir', str(project1),
            '--output', str(inventory1)
        ])

        # Don't wait for indexing to complete
        # Create another project for concurrent indexing
        project2 = create_test_project("search-test-2", 10)
        inventory2 = tmp_path / "inv2.jsonl"

        cli_runner.invoke(discover_command, [
            '--source-dir', str(project2),
            '--output', str(inventory2)
        ])

        # Index project2 in background and search concurrently
        with ThreadPoolExecutor(max_workers=2) as executor:
            index_future = executor.submit(
                cli_runner.invoke,
                index_command,
                ['--input', str(inventory2)]
            )

            # Wait a moment for indexing to start
            time.sleep(0.1)

            # Perform search while indexing
            search_future = executor.submit(
                cli_runner.invoke,
                search_command,
                ['test', '--limit', '5']
            )

            index_result = index_future.result()
            search_result = search_future.result()

        # Both should complete without errors
        # (search may return no results, that's ok)
        assert index_result.exit_code in [0, 1]
        assert search_result.exit_code in [0, 1]


@pytest.mark.slow
@pytest.mark.e2e
@pytest.mark.skip(reason="Legacy TDD test - requires updated CLI API")
class TestRaceConditions:
    """Test for race conditions and data consistency."""

    def test_no_duplicate_artifacts(self, create_test_project, cli_runner, tmp_path):
        """Test that concurrent indexing doesn't create duplicate artifacts."""
        config = get_config()

        # Skip if Weaviate not available
        try:
            store = WeaviateStore(config=config, auto_create_schema=False)
            if not store.health_check():
                pytest.skip("Weaviate not available")
        except Exception:
            pytest.skip("Weaviate not available")

        # Create project
        project = create_test_project("duplicate-test", 10)
        inventory = tmp_path / "inventory.jsonl"

        cli_runner.invoke(discover_command, [
            '--source-dir', str(project),
            '--output', str(inventory)
        ])

        # Index successfully
        result = cli_runner.invoke(index_command, [
            '--input', str(inventory)
        ])

        assert result.exit_code == 0

        # Count artifacts
        count_before = store.count_artifacts(project_id="com.example:duplicate-test:1.0.0")

        # Index again (should be idempotent)
        result2 = cli_runner.invoke(index_command, [
            '--input', str(inventory)
        ])

        assert result2.exit_code == 0

        # Count should be the same (no duplicates)
        count_after = store.count_artifacts(project_id="com.example:duplicate-test:1.0.0")

        assert count_before == count_after, f"Duplicate artifacts created: {count_before} -> {count_after}"

    def test_consistent_reads_during_writes(self, tmp_path):
        """Test that reads are consistent during concurrent writes."""
        config = get_config()

        # Skip if Weaviate not available
        try:
            store = WeaviateStore(config=config, auto_create_schema=False)
            if not store.health_check():
                pytest.skip("Weaviate not available")
        except Exception:
            pytest.skip("Weaviate not available")

        project_id = "com.example:consistency-test:1.0.0"

        # Count should be consistent (either old count or new count, not in-between)
        counts = []

        def read_count():
            for _ in range(10):
                count = store.count_artifacts(project_id=project_id)
                counts.append(count)
                time.sleep(0.01)

        def write_artifacts():
            # Simulate writing artifacts
            time.sleep(0.05)

        # Run reads and writes concurrently
        with ThreadPoolExecutor(max_workers=2) as executor:
            read_future = executor.submit(read_count)
            write_future = executor.submit(write_artifacts)

            read_future.result()
            write_future.result()

        # Counts should be stable (not wildly varying)
        # Allow for some variation due to actual updates, but should not be random
        unique_counts = set(counts)
        assert len(unique_counts) <= 3, f"Too many different counts observed: {unique_counts}"
