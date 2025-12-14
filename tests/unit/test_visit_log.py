"""
Unit tests for Visit Log Service.
"""
import json
import pytest
from pathlib import Path
from datetime import datetime

from codeindex.models.prd import FileVisitEntry, VisitStatus, AnalysisLayer
from codeindex.services.visit_log import (
    VisitLog,
    compute_file_hash,
    create_visit_entry,
    load_visit_log,
    append_visit_entry,
    check_file_visited,
    get_visit_status,
)


# ==============================================================================
# Fixtures
# ==============================================================================

@pytest.fixture
def temp_output_dir(tmp_path):
    """Temporary output directory."""
    return tmp_path / "output"


@pytest.fixture
def temp_test_file(tmp_path):
    """Temporary test file with known content."""
    test_file = tmp_path / "test_file.java"
    test_file.write_text("public class TestClass { }", encoding="utf-8")
    return test_file


@pytest.fixture
def visit_log(temp_output_dir):
    """Empty visit log instance."""
    return VisitLog(temp_output_dir)


# ==============================================================================
# Hash Computation Tests
# ==============================================================================

def test_compute_file_hash(temp_test_file):
    """Test file hash computation."""
    hash1 = compute_file_hash(temp_test_file)

    # Should be 64-character hex string (SHA-256)
    assert len(hash1) == 64
    assert all(c in "0123456789abcdef" for c in hash1)

    # Same file should produce same hash
    hash2 = compute_file_hash(temp_test_file)
    assert hash1 == hash2


def test_compute_file_hash_changed_content(temp_test_file):
    """Test hash changes when file content changes."""
    hash1 = compute_file_hash(temp_test_file)

    # Modify file
    temp_test_file.write_text("public class ModifiedClass { }", encoding="utf-8")
    hash2 = compute_file_hash(temp_test_file)

    # Hash should be different
    assert hash1 != hash2


def test_compute_file_hash_nonexistent_file(tmp_path):
    """Test hash computation for nonexistent file."""
    nonexistent = tmp_path / "nonexistent.java"

    # Should not raise exception, returns error hash
    hash_value = compute_file_hash(nonexistent)
    assert len(hash_value) == 64


# ==============================================================================
# Visit Log Creation Tests
# ==============================================================================

def test_visit_log_initialization(temp_output_dir):
    """Test VisitLog initialization."""
    log = VisitLog(temp_output_dir)

    assert log.output_dir == temp_output_dir
    assert log.log_file == temp_output_dir / ".visit_log.jsonl"
    assert len(log.entries) == 0


def test_visit_log_loads_existing_log(temp_output_dir, temp_test_file):
    """Test loading existing visit log from disk."""
    # Create log file
    log_file = temp_output_dir / ".visit_log.jsonl"
    temp_output_dir.mkdir(parents=True, exist_ok=True)

    entry1 = create_visit_entry(
        file_path=str(temp_test_file),
        status=VisitStatus.SUCCESS,
        content_hash="abc123",
        layer=AnalysisLayer.DATABASE,
        extracted_entities=["User"]
    )

    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(entry1.to_dict(), f)
        f.write("\n")

    # Load log
    log = VisitLog(temp_output_dir)

    assert len(log.entries) == 1
    assert str(temp_test_file) in log.entries


def test_visit_log_deduplicates_entries(temp_output_dir, temp_test_file):
    """Test that latest entry wins when multiple entries for same file."""
    log_file = temp_output_dir / ".visit_log.jsonl"
    temp_output_dir.mkdir(parents=True, exist_ok=True)

    # Write two entries for same file
    entry1 = create_visit_entry(
        file_path=str(temp_test_file),
        status=VisitStatus.SUCCESS,
        content_hash="hash1",
        layer=AnalysisLayer.DATABASE
    )

    entry2 = create_visit_entry(
        file_path=str(temp_test_file),
        status=VisitStatus.SUCCESS,
        content_hash="hash2",
        layer=AnalysisLayer.DATABASE
    )

    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(entry1.to_dict(), f)
        f.write("\n")
        json.dump(entry2.to_dict(), f)
        f.write("\n")

    # Load log
    log = VisitLog(temp_output_dir)

    # Should have only one entry with latest hash
    assert len(log.entries) == 1
    assert log.entries[str(temp_test_file)].content_hash == "hash2"


# ==============================================================================
# Append Entry Tests
# ==============================================================================

def test_append_entry(visit_log, temp_test_file):
    """Test appending visit entry."""
    entry = create_visit_entry(
        file_path=str(temp_test_file),
        status=VisitStatus.SUCCESS,
        content_hash="abc123",
        layer=AnalysisLayer.DATABASE,
        extracted_entities=["User", "Account"]
    )

    visit_log.append_entry(entry)

    # Should be in memory
    assert len(visit_log.entries) == 1
    assert str(temp_test_file) in visit_log.entries

    # Should be in file
    assert visit_log.log_file.exists()
    with open(visit_log.log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        assert len(lines) == 1
        loaded_entry = json.loads(lines[0])
        assert loaded_entry["file_path"] == str(temp_test_file)
        assert loaded_entry["content_hash"] == "abc123"
        assert len(loaded_entry["extracted_entities"]) == 2


def test_append_multiple_entries(visit_log, tmp_path):
    """Test appending multiple entries."""
    file1 = tmp_path / "file1.java"
    file2 = tmp_path / "file2.java"

    entry1 = create_visit_entry(
        file_path=str(file1),
        status=VisitStatus.SUCCESS,
        content_hash="hash1",
        layer=AnalysisLayer.DATABASE
    )

    entry2 = create_visit_entry(
        file_path=str(file2),
        status=VisitStatus.SUCCESS,
        content_hash="hash2",
        layer=AnalysisLayer.SERVICE
    )

    visit_log.append_entry(entry1)
    visit_log.append_entry(entry2)

    assert len(visit_log.entries) == 2

    # Verify JSONL file
    with open(visit_log.log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        assert len(lines) == 2


# ==============================================================================
# Check File Visited Tests
# ==============================================================================

def test_check_file_visited_success(visit_log, temp_test_file):
    """Test checking if file has been visited."""
    content_hash = "abc123"

    entry = create_visit_entry(
        file_path=str(temp_test_file),
        status=VisitStatus.SUCCESS,
        content_hash=content_hash,
        layer=AnalysisLayer.DATABASE
    )
    visit_log.append_entry(entry)

    # Should return True for matching hash
    assert visit_log.check_file_visited(str(temp_test_file), content_hash) is True


def test_check_file_visited_different_hash(visit_log, temp_test_file):
    """Test that different hash returns False."""
    entry = create_visit_entry(
        file_path=str(temp_test_file),
        status=VisitStatus.SUCCESS,
        content_hash="hash1",
        layer=AnalysisLayer.DATABASE
    )
    visit_log.append_entry(entry)

    # Different hash should return False
    assert visit_log.check_file_visited(str(temp_test_file), "hash2") is False


def test_check_file_visited_failed_status(visit_log, temp_test_file):
    """Test that failed status returns False."""
    content_hash = "abc123"

    entry = create_visit_entry(
        file_path=str(temp_test_file),
        status=VisitStatus.FAILED,
        content_hash=content_hash,
        layer=AnalysisLayer.DATABASE,
        error_message="LLM timeout"
    )
    visit_log.append_entry(entry)

    # Failed status should return False even with matching hash
    assert visit_log.check_file_visited(str(temp_test_file), content_hash) is False


def test_check_file_visited_layer_filter(visit_log, temp_test_file):
    """Test layer filtering in check_file_visited."""
    content_hash = "abc123"

    entry = create_visit_entry(
        file_path=str(temp_test_file),
        status=VisitStatus.SUCCESS,
        content_hash=content_hash,
        layer=AnalysisLayer.DATABASE
    )
    visit_log.append_entry(entry)

    # Same layer should return True
    assert visit_log.check_file_visited(
        str(temp_test_file), content_hash, layer=AnalysisLayer.DATABASE
    ) is True

    # Different layer should return False
    assert visit_log.check_file_visited(
        str(temp_test_file), content_hash, layer=AnalysisLayer.SERVICE
    ) is False


def test_check_file_not_visited(visit_log, temp_test_file):
    """Test checking file that hasn't been visited."""
    assert visit_log.check_file_visited(str(temp_test_file), "any_hash") is False


# ==============================================================================
# Get Visit Status Tests
# ==============================================================================

def test_get_visit_status(visit_log, temp_test_file):
    """Test getting visit status for a file."""
    entry = create_visit_entry(
        file_path=str(temp_test_file),
        status=VisitStatus.SUCCESS,
        content_hash="abc123",
        layer=AnalysisLayer.DATABASE
    )
    visit_log.append_entry(entry)

    result = visit_log.get_visit_status(str(temp_test_file))

    assert result is not None
    assert result.file_path == str(temp_test_file)
    assert result.status == VisitStatus.SUCCESS
    assert result.content_hash == "abc123"


def test_get_visit_status_not_found(visit_log, temp_test_file):
    """Test getting visit status for unvisited file."""
    result = visit_log.get_visit_status(str(temp_test_file))
    assert result is None


# ==============================================================================
# Get All Entries Tests
# ==============================================================================

def test_get_all_entries(visit_log, tmp_path):
    """Test getting all entries."""
    file1 = tmp_path / "file1.java"
    file2 = tmp_path / "file2.java"

    entry1 = create_visit_entry(
        file_path=str(file1),
        status=VisitStatus.SUCCESS,
        content_hash="hash1",
        layer=AnalysisLayer.DATABASE
    )

    entry2 = create_visit_entry(
        file_path=str(file2),
        status=VisitStatus.SUCCESS,
        content_hash="hash2",
        layer=AnalysisLayer.SERVICE
    )

    visit_log.append_entry(entry1)
    visit_log.append_entry(entry2)

    entries = visit_log.get_all_entries()
    assert len(entries) == 2


def test_get_all_entries_layer_filter(visit_log, tmp_path):
    """Test getting entries filtered by layer."""
    file1 = tmp_path / "file1.java"
    file2 = tmp_path / "file2.java"

    entry1 = create_visit_entry(
        file_path=str(file1),
        status=VisitStatus.SUCCESS,
        content_hash="hash1",
        layer=AnalysisLayer.DATABASE
    )

    entry2 = create_visit_entry(
        file_path=str(file2),
        status=VisitStatus.SUCCESS,
        content_hash="hash2",
        layer=AnalysisLayer.SERVICE
    )

    visit_log.append_entry(entry1)
    visit_log.append_entry(entry2)

    # Filter by DATABASE layer
    db_entries = visit_log.get_all_entries(layer=AnalysisLayer.DATABASE)
    assert len(db_entries) == 1
    assert db_entries[0].layer == AnalysisLayer.DATABASE


def test_get_all_entries_status_filter(visit_log, tmp_path):
    """Test getting entries filtered by status."""
    file1 = tmp_path / "file1.java"
    file2 = tmp_path / "file2.java"

    entry1 = create_visit_entry(
        file_path=str(file1),
        status=VisitStatus.SUCCESS,
        content_hash="hash1",
        layer=AnalysisLayer.DATABASE
    )

    entry2 = create_visit_entry(
        file_path=str(file2),
        status=VisitStatus.FAILED,
        content_hash="hash2",
        layer=AnalysisLayer.SERVICE,
        error_message="Timeout"
    )

    visit_log.append_entry(entry1)
    visit_log.append_entry(entry2)

    # Filter by SUCCESS status
    success_entries = visit_log.get_all_entries(status=VisitStatus.SUCCESS)
    assert len(success_entries) == 1
    assert success_entries[0].status == VisitStatus.SUCCESS


# ==============================================================================
# Statistics Tests
# ==============================================================================

def test_get_stats(visit_log, tmp_path):
    """Test getting visit log statistics."""
    file1 = tmp_path / "file1.java"
    file2 = tmp_path / "file2.java"
    file3 = tmp_path / "file3.java"

    entry1 = create_visit_entry(
        file_path=str(file1),
        status=VisitStatus.SUCCESS,
        content_hash="hash1",
        layer=AnalysisLayer.DATABASE
    )

    entry2 = create_visit_entry(
        file_path=str(file2),
        status=VisitStatus.FAILED,
        content_hash="hash2",
        layer=AnalysisLayer.SERVICE,
        error_message="Error"
    )

    entry3 = create_visit_entry(
        file_path=str(file3),
        status=VisitStatus.SKIPPED,
        content_hash="hash3",
        layer=AnalysisLayer.FRONTEND
    )

    visit_log.append_entry(entry1)
    visit_log.append_entry(entry2)
    visit_log.append_entry(entry3)

    stats = visit_log.get_stats()

    assert stats["total"] == 3
    assert stats["success"] == 1
    assert stats["failed"] == 1
    assert stats["skipped"] == 1
    assert stats["by_layer"]["database"] == 1
    assert stats["by_layer"]["service"] == 1
    assert stats["by_layer"]["frontend"] == 1


def test_get_visited_files(visit_log, tmp_path):
    """Test getting set of visited file paths."""
    file1 = tmp_path / "file1.java"
    file2 = tmp_path / "file2.java"

    entry1 = create_visit_entry(
        file_path=str(file1),
        status=VisitStatus.SUCCESS,
        content_hash="hash1",
        layer=AnalysisLayer.DATABASE
    )

    entry2 = create_visit_entry(
        file_path=str(file2),
        status=VisitStatus.SUCCESS,
        content_hash="hash2",
        layer=AnalysisLayer.SERVICE
    )

    visit_log.append_entry(entry1)
    visit_log.append_entry(entry2)

    visited = visit_log.get_visited_files()

    assert len(visited) == 2
    assert str(file1) in visited
    assert str(file2) in visited


# ==============================================================================
# Clear Tests
# ==============================================================================

def test_clear(visit_log, temp_test_file):
    """Test clearing visit log."""
    entry = create_visit_entry(
        file_path=str(temp_test_file),
        status=VisitStatus.SUCCESS,
        content_hash="abc123",
        layer=AnalysisLayer.DATABASE
    )
    visit_log.append_entry(entry)

    assert len(visit_log.entries) == 1
    assert visit_log.log_file.exists()

    # Clear log
    visit_log.clear()

    assert len(visit_log.entries) == 0
    assert not visit_log.log_file.exists()


# ==============================================================================
# Convenience Function Tests
# ==============================================================================

def test_create_visit_entry():
    """Test create_visit_entry convenience function."""
    entry = create_visit_entry(
        file_path="/path/to/file.java",
        status=VisitStatus.SUCCESS,
        content_hash="abc123",
        layer=AnalysisLayer.DATABASE,
        analysis_type="dao_extraction",
        duration_seconds=2.5,
        extracted_entities=["User", "Account"]
    )

    assert entry.file_path == "/path/to/file.java"
    assert entry.status == VisitStatus.SUCCESS
    assert entry.content_hash == "abc123"
    assert entry.layer == AnalysisLayer.DATABASE
    assert entry.analysis_type == "dao_extraction"
    assert entry.duration_seconds == 2.5
    assert len(entry.extracted_entities) == 2
    assert entry.timestamp is not None


def test_backward_compatibility_functions(temp_output_dir, temp_test_file):
    """Test backward compatibility convenience functions."""
    # Load log
    log = load_visit_log(temp_output_dir)
    assert log is not None

    # Append entry
    append_visit_entry(
        visit_log=log,
        file_path=str(temp_test_file),
        timestamp=datetime.now(),
        status=VisitStatus.SUCCESS,
        content_hash="abc123",
        layer=AnalysisLayer.DATABASE,
        entities=["User"]
    )

    # Check visited
    assert check_file_visited(log, str(temp_test_file), "abc123") is True

    # Get status
    status = get_visit_status(log, str(temp_test_file))
    assert status is not None
    assert status.content_hash == "abc123"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
