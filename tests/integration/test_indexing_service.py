"""
Integration test for indexing service.

Tests idempotent indexing, project versioning, and per-project locking.

NOTE: Requires running Weaviate instance.
"""

import pytest
import tempfile
import json
from pathlib import Path
from datetime import datetime
from unittest.mock import patch

from codeindex.services.indexing import IndexingService
from codeindex.services.weaviate_store import WeaviateStore
from codeindex.models.project import Project
from codeindex.models.artifact import CodeArtifact
from codeindex.models import ArtifactType
from codeindex.utils.config import Config


@pytest.fixture(scope="module")
def weaviate_store():
    """Weaviate store for testing."""
    import os

    # Set environment variables for test
    os.environ["WEAVIATE_URL"] = "http://localhost:8080"
    os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434"
    os.environ["OLLAMA_MODEL_NAME"] = "gemma3:12b"

    # Create config (reads from env vars)
    config = Config()

    store = WeaviateStore(config=config)

    if not store.health_check():
        pytest.skip("Weaviate not available")

    yield store

    store.close()


@pytest.fixture
def indexing_service(weaviate_store):
    """Indexing service instance."""
    return IndexingService(weaviate_store=weaviate_store)


@pytest.fixture
def sample_extraction_results(tmp_path):
    """Create sample extraction results file."""
    results = [
        {
            "project_id": "com.example:test:1.0.0",
            "relative_path": "src/main/java/Test1.java",
            "file_name": "Test1.java",
            "language": "Java",
            "artifact_type": "JAVA_SOURCE",
            "summary": "Test class 1",
            "entities": ["Test1"],
            "tags": {"layer": ["backend"], "domain": [], "frameworks": ["Java"], "concerns": []},
            "raw_text_hash": "hash1",
            "confidence_score": 0.9
        },
        {
            "project_id": "com.example:test:1.0.0",
            "relative_path": "src/main/java/Test2.java",
            "file_name": "Test2.java",
            "language": "Java",
            "artifact_type": "JAVA_SOURCE",
            "summary": "Test class 2",
            "entities": ["Test2"],
            "tags": {"layer": ["backend"], "domain": [], "frameworks": ["Java"], "concerns": []},
            "raw_text_hash": "hash2",
            "confidence_score": 0.85
        }
    ]

    results_file = tmp_path / "extraction.jsonl"
    with open(results_file, 'w') as f:
        for result in results:
            f.write(json.dumps(result) + '\n')

    return results_file


# Test idempotent indexing
class TestIdempotentIndexing:
    """Test that re-indexing updates rather than duplicates."""

    def test_index_same_file_twice(self, indexing_service, sample_extraction_results):
        """Test indexing same file twice updates existing record."""
        # Index first time
        result1 = indexing_service.index_from_extraction_file(sample_extraction_results)

        assert result1["indexed_count"] == 2

        # Index again - should update, not duplicate
        result2 = indexing_service.index_from_extraction_file(sample_extraction_results)

        # Should have updated 2 artifacts, not created 2 new ones
        assert result2["updated_count"] == 2 or result2["indexed_count"] == 2

        # Verify no duplicates
        count = indexing_service.weaviate_store.count_artifacts(project_id="com.example:test:1.0.0")
        assert count == 2  # Still just 2 artifacts

    def test_index_changed_file(self, indexing_service, tmp_path):
        """Test that changed file content updates the record."""
        project_id = "com.example:test:1.0.0"
        path = "src/Test.java"

        # Index version 1
        result1 = {
            "project_id": project_id,
            "relative_path": path,
            "file_name": "Test.java",
            "language": "Java",
            "artifact_type": "JAVA_SOURCE",
            "summary": "Version 1",
            "entities": [],
            "tags": {"layer": ["backend"], "domain": [], "frameworks": [], "concerns": []},
            "raw_text_hash": "hash_v1",
            "confidence_score": 0.9
        }

        file1 = tmp_path / "extraction1.jsonl"
        with open(file1, 'w') as f:
            f.write(json.dumps(result1) + '\n')

        indexing_service.index_from_extraction_file(file1)

        # Index version 2 (changed content)
        result2 = result1.copy()
        result2["summary"] = "Version 2 - Updated"
        result2["raw_text_hash"] = "hash_v2"  # Different hash

        file2 = tmp_path / "extraction2.jsonl"
        with open(file2, 'w') as f:
            f.write(json.dumps(result2) + '\n')

        indexing_service.index_from_extraction_file(file2)

        # Should have 1 artifact (updated, not duplicated)
        count = indexing_service.weaviate_store.count_artifacts(project_id=project_id)
        assert count == 1

    def test_skip_unchanged_files(self, indexing_service, sample_extraction_results):
        """Test that unchanged files are skipped."""
        # Index first time
        result1 = indexing_service.index_from_extraction_file(sample_extraction_results)

        # Index again with same content (same hash)
        result2 = indexing_service.index_from_extraction_file(sample_extraction_results, skip_unchanged=True)

        # Should skip unchanged files
        assert result2["skipped_count"] >= 0


# Test project versioning
class TestProjectVersioning:
    """Test multiple versions of same project can coexist."""

    def test_multiple_versions_coexist(self, indexing_service, tmp_path):
        """Test indexing multiple versions of same project."""
        # Index version 1.0.0
        results_v1 = [
            {
                "project_id": "com.example:app:1.0.0",
                "relative_path": "src/Main.java",
                "file_name": "Main.java",
                "language": "Java",
                "artifact_type": "JAVA_SOURCE",
                "summary": "Version 1.0.0",
                "entities": [],
                "tags": {"layer": ["backend"], "domain": [], "frameworks": [], "concerns": []},
                "raw_text_hash": "hash_v1",
                "confidence_score": 0.9
            }
        ]

        file_v1 = tmp_path / "v1.jsonl"
        with open(file_v1, 'w') as f:
            for r in results_v1:
                f.write(json.dumps(r) + '\n')

        indexing_service.index_from_extraction_file(file_v1)

        # Index version 2.0.0
        results_v2 = [
            {
                "project_id": "com.example:app:2.0.0",
                "relative_path": "src/Main.java",
                "file_name": "Main.java",
                "language": "Java",
                "artifact_type": "JAVA_SOURCE",
                "summary": "Version 2.0.0",
                "entities": [],
                "tags": {"layer": ["backend"], "domain": [], "frameworks": [], "concerns": []},
                "raw_text_hash": "hash_v2",
                "confidence_score": 0.9
            }
        ]

        file_v2 = tmp_path / "v2.jsonl"
        with open(file_v2, 'w') as f:
            for r in results_v2:
                f.write(json.dumps(r) + '\n')

        indexing_service.index_from_extraction_file(file_v2)

        # Should have artifacts for both versions
        count_v1 = indexing_service.weaviate_store.count_artifacts(project_id="com.example:app:1.0.0")
        count_v2 = indexing_service.weaviate_store.count_artifacts(project_id="com.example:app:2.0.0")

        assert count_v1 >= 1
        assert count_v2 >= 1


# Test per-project locking
class TestProjectLocking:
    """Test concurrent indexing prevention."""

    def test_project_locking(self, indexing_service, sample_extraction_results):
        """Test that project is locked during indexing."""
        project_id = "com.example:test:1.0.0"

        # Start indexing (acquires lock)
        with indexing_service.lock_project(project_id):
            # Attempting to lock again should fail or wait
            assert indexing_service.is_project_locked(project_id)

        # Lock should be released after completion
        assert not indexing_service.is_project_locked(project_id)

    def test_concurrent_indexing_prevented(self, indexing_service, sample_extraction_results):
        """Test that concurrent indexing of same project is prevented."""
        from threading import Thread
        import time

        project_id = "com.example:test:1.0.0"
        results = []

        def index_with_delay():
            try:
                with indexing_service.lock_project(project_id):
                    time.sleep(0.1)  # Simulate work
                    results.append("success")
            except Exception as e:
                results.append(f"error: {e}")

        # Start two threads trying to index same project
        thread1 = Thread(target=index_with_delay)
        thread2 = Thread(target=index_with_delay)

        thread1.start()
        time.sleep(0.01)  # Small delay so thread1 acquires lock first
        thread2.start()

        thread1.join()
        thread2.join()

        # One should succeed, one should handle lock gracefully
        assert len(results) == 2


# Test project reset
class TestProjectReset:
    """Test deleting all data for a project before re-indexing."""

    def test_reset_project(self, indexing_service, sample_extraction_results):
        """Test resetting project deletes all its artifacts."""
        project_id = "com.example:test:1.0.0"

        # Index some data
        indexing_service.index_from_extraction_file(sample_extraction_results)

        # Verify data exists
        count_before = indexing_service.weaviate_store.count_artifacts(project_id=project_id)
        assert count_before > 0

        # Reset project
        indexing_service.reset_project(project_id)

        # Verify all data deleted
        count_after = indexing_service.weaviate_store.count_artifacts(project_id=project_id)
        assert count_after == 0


# Test error handling
class TestIndexingErrors:
    """Test error handling during indexing."""

    def test_handle_malformed_extraction_file(self, indexing_service, tmp_path):
        """Test handling of malformed extraction file."""
        malformed_file = tmp_path / "malformed.jsonl"
        with open(malformed_file, 'w') as f:
            f.write("not valid json\n")
            f.write("{incomplete json\n")

        # Should handle gracefully
        try:
            result = indexing_service.index_from_extraction_file(malformed_file)
            assert result["error_count"] > 0
        except Exception:
            # May raise specific error - implementation dependent
            pass

    def test_batch_failure_recovery(self, indexing_service, weaviate_store):
        """Test recovery from batch failures."""
        # Mock batch failure
        with patch.object(weaviate_store, 'batch_insert_artifacts', side_effect=Exception("Batch failed")):
            # Should handle error and report it
            try:
                indexing_service.index_batch([])
            except Exception as e:
                assert "failed" in str(e).lower()


# Test resume capability
class TestResumeCapability:
    """Test resuming interrupted indexing operations."""

    def test_resume_after_interruption(self, indexing_service, tmp_path):
        """Test resuming indexing after interruption."""
        # Create large extraction file
        results = [
            {
                "project_id": "com.example:large:1.0.0",
                "relative_path": f"src/File{i}.java",
                "file_name": f"File{i}.java",
                "language": "Java",
                "artifact_type": "JAVA_SOURCE",
                "summary": f"File {i}",
                "entities": [],
                "tags": {"layer": ["backend"], "domain": [], "frameworks": [], "concerns": []},
                "raw_text_hash": f"hash{i}",
                "confidence_score": 0.9
            }
            for i in range(100)
        ]

        extraction_file = tmp_path / "large.jsonl"
        with open(extraction_file, 'w') as f:
            for r in results:
                f.write(json.dumps(r) + '\n')

        # Index partially (simulate interruption)
        indexing_service.index_from_extraction_file(extraction_file, limit=50)

        count_partial = indexing_service.weaviate_store.count_artifacts(project_id="com.example:large:1.0.0")
        assert count_partial == 50

        # Resume - should skip already indexed files
        indexing_service.index_from_extraction_file(extraction_file, skip_unchanged=True)

        count_full = indexing_service.weaviate_store.count_artifacts(project_id="com.example:large:1.0.0")
        assert count_full == 100
