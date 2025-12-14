"""
Visit Log Service for PRD Generation.

This module provides visit log tracking functionality to enable incremental
processing. It tracks which files have been analyzed, their content hashes,
and analysis results to avoid re-processing unchanged files.

The visit log uses JSONL (JSON Lines) format with one entry per line for
efficient append-only writes and streaming reads.
"""
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict

from codeindex.models.prd import FileVisitEntry, VisitStatus, AnalysisLayer


class VisitLog:
    """
    Manages visit log for incremental PRD generation.

    The visit log tracks analyzed files with content hashes to enable
    skipping unchanged files on subsequent runs.
    """

    def __init__(self, output_dir: Path):
        """
        Initialize visit log.

        Args:
            output_dir: Output directory where .visit_log.jsonl is stored
        """
        self.output_dir = Path(output_dir)
        self.log_file = self.output_dir / ".visit_log.jsonl"
        self.entries: Dict[str, FileVisitEntry] = {}

        # Load existing log if present
        self._load()

    def _load(self) -> None:
        """Load existing visit log from disk."""
        if not self.log_file.exists():
            return

        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    entry_dict = json.loads(line)
                    entry = FileVisitEntry.from_dict(entry_dict)

                    # Keep latest entry for each file (deduplication)
                    self.entries[entry.file_path] = entry
        except Exception as e:
            # If log is corrupted, start fresh
            print(f"Warning: Failed to load visit log: {e}. Starting fresh.")
            self.entries = {}

    def append_entry(self, entry: FileVisitEntry) -> None:
        """
        Append a visit entry to the log.

        Args:
            entry: FileVisitEntry to append
        """
        # Update in-memory cache
        self.entries[entry.file_path] = entry

        # Append to JSONL file
        self.output_dir.mkdir(parents=True, exist_ok=True)

        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                json.dump(entry.to_dict(), f)
                f.write("\n")
        except Exception as e:
            print(f"Warning: Failed to append to visit log: {e}")

    def check_file_visited(
        self,
        file_path: str,
        content_hash: str,
        layer: Optional[AnalysisLayer] = None
    ) -> bool:
        """
        Check if file has been visited with matching content hash.

        Args:
            file_path: Absolute or relative path to file
            content_hash: SHA-256 hash of file contents
            layer: Optional layer filter (only check visits for specific layer)

        Returns:
            True if file has been successfully visited with same content hash
        """
        if file_path not in self.entries:
            return False

        entry = self.entries[file_path]

        # Check layer filter if specified
        if layer is not None and entry.layer != layer:
            return False

        # Check content hash and success status
        return (
            entry.content_hash == content_hash and
            entry.status == VisitStatus.SUCCESS
        )

    def get_visit_status(
        self,
        file_path: str
    ) -> Optional[FileVisitEntry]:
        """
        Get visit entry for a file.

        Args:
            file_path: Absolute or relative path to file

        Returns:
            FileVisitEntry if file has been visited, None otherwise
        """
        return self.entries.get(file_path)

    def get_all_entries(
        self,
        layer: Optional[AnalysisLayer] = None,
        status: Optional[VisitStatus] = None
    ) -> List[FileVisitEntry]:
        """
        Get all visit entries, optionally filtered by layer and/or status.

        Args:
            layer: Optional layer filter
            status: Optional status filter

        Returns:
            List of FileVisitEntry matching filters
        """
        entries = list(self.entries.values())

        if layer is not None:
            entries = [e for e in entries if e.layer == layer]

        if status is not None:
            entries = [e for e in entries if e.status == status]

        return entries

    def get_visited_files(
        self,
        layer: Optional[AnalysisLayer] = None
    ) -> Set[str]:
        """
        Get set of file paths that have been visited.

        Args:
            layer: Optional layer filter

        Returns:
            Set of file paths
        """
        entries = self.get_all_entries(layer=layer)
        return {e.file_path for e in entries}

    def get_stats(self) -> Dict[str, int]:
        """
        Get statistics about visit log.

        Returns:
            Dictionary with counts by status and layer
        """
        stats = {
            "total": len(self.entries),
            "success": 0,
            "failed": 0,
            "skipped": 0,
            "by_layer": {}
        }

        for entry in self.entries.values():
            # Count by status
            if entry.status == VisitStatus.SUCCESS:
                stats["success"] += 1
            elif entry.status == VisitStatus.FAILED:
                stats["failed"] += 1
            elif entry.status == VisitStatus.SKIPPED:
                stats["skipped"] += 1

            # Count by layer
            layer_name = entry.layer.value if entry.layer else "unknown"
            if layer_name not in stats["by_layer"]:
                stats["by_layer"][layer_name] = 0
            stats["by_layer"][layer_name] += 1

        return stats

    def clear(self) -> None:
        """Clear all visit log entries (for testing or --force-refresh)."""
        self.entries = {}

        # Remove log file
        if self.log_file.exists():
            self.log_file.unlink()


def compute_file_hash(file_path: Path) -> str:
    """
    Compute SHA-256 hash of file contents.

    Args:
        file_path: Path to file

    Returns:
        Hex string of SHA-256 hash
    """
    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as f:
            # Read in chunks for memory efficiency
            while chunk := f.read(8192):
                sha256.update(chunk)
    except Exception as e:
        # Return hash of error message if file cannot be read
        error_msg = f"ERROR_READING_FILE: {e}"
        sha256.update(error_msg.encode("utf-8"))

    return sha256.hexdigest()


def create_visit_entry(
    file_path: str,
    status: VisitStatus,
    content_hash: str,
    layer: AnalysisLayer,
    analysis_type: Optional[str] = None,
    duration_seconds: Optional[float] = None,
    extracted_entities: Optional[List[str]] = None,
    error_message: Optional[str] = None
) -> FileVisitEntry:
    """
    Create a FileVisitEntry with current timestamp.

    Args:
        file_path: Absolute or relative path to file
        status: Visit status (success/failed/skipped)
        content_hash: SHA-256 hash of file contents
        layer: Analysis layer
        analysis_type: Optional type of analysis performed
        duration_seconds: Optional duration of analysis in seconds
        extracted_entities: Optional list of entity names extracted
        error_message: Optional error message if status is FAILED

    Returns:
        FileVisitEntry instance
    """
    return FileVisitEntry(
        file_path=file_path,
        timestamp=datetime.now(),
        status=status,
        content_hash=content_hash,
        layer=layer,
        analysis_type=analysis_type,
        duration_seconds=duration_seconds,
        extracted_entities=extracted_entities or [],
        error_message=error_message
    )


# Convenience functions for backward compatibility

def load_visit_log(output_dir: Path) -> VisitLog:
    """
    Load visit log from output directory.

    Args:
        output_dir: Output directory path

    Returns:
        VisitLog instance
    """
    return VisitLog(output_dir)


def append_visit_entry(
    visit_log: VisitLog,
    file_path: str,
    timestamp: datetime,
    status: VisitStatus,
    content_hash: str,
    layer: AnalysisLayer,
    analysis_type: Optional[str] = None,
    duration: Optional[float] = None,
    entities: Optional[List[str]] = None,
    error_message: Optional[str] = None
) -> None:
    """
    Append a visit entry to the log.

    Args:
        visit_log: VisitLog instance
        file_path: File path
        timestamp: Timestamp
        status: Visit status
        content_hash: Content hash
        layer: Analysis layer
        analysis_type: Analysis type
        duration: Duration in seconds
        entities: Extracted entities
        error_message: Error message
    """
    entry = FileVisitEntry(
        file_path=file_path,
        timestamp=timestamp,
        status=status,
        content_hash=content_hash,
        layer=layer,
        analysis_type=analysis_type,
        duration_seconds=duration,
        extracted_entities=entities or [],
        error_message=error_message
    )
    visit_log.append_entry(entry)


def check_file_visited(
    visit_log: VisitLog,
    file_path: str,
    content_hash: str
) -> bool:
    """
    Check if file has been visited with matching content hash.

    Args:
        visit_log: VisitLog instance
        file_path: File path
        content_hash: Content hash

    Returns:
        True if visited with matching hash
    """
    return visit_log.check_file_visited(file_path, content_hash)


def get_visit_status(
    visit_log: VisitLog,
    file_path: str
) -> Optional[FileVisitEntry]:
    """
    Get visit status for a file.

    Args:
        visit_log: VisitLog instance
        file_path: File path

    Returns:
        FileVisitEntry if visited, None otherwise
    """
    return visit_log.get_visit_status(file_path)
