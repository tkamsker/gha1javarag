"""
DiscoveryInventory model for Java Codebase Indexer Pipeline.

Intermediate data structure capturing file system scan results before extraction.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict
from pathlib import Path
import json


@dataclass
class DiscoveryInventory:
    """
    Discovery inventory entity.

    Intermediate structure capturing file system scan results.
    Stored as JSONL (one project per line for streaming).
    """

    # Scan metadata
    scan_timestamp: datetime  # When discovery was run
    root_directory: str  # Scanned directory path

    # Discovered data
    projects: list[dict] = field(default_factory=list)  # Partial Project data
    total_files: int = 0  # Total files discovered
    files_by_type: Dict[str, int] = field(default_factory=dict)  # Count per artifact type
    scan_duration_seconds: float = 0.0  # Time taken for discovery

    def add_project(self, project_data: dict):
        """
        Add a discovered project to inventory.

        Args:
            project_data: Partial project data (project_id, name, path, files, etc.)
        """
        self.projects.append(project_data)

    def update_file_counts(self, artifact_type: str, count: int = 1):
        """
        Update file type counts.

        Args:
            artifact_type: Type of artifact (java_source, jsp_view, etc.)
            count: Number of files to add (default: 1)
        """
        self.files_by_type[artifact_type] = self.files_by_type.get(artifact_type, 0) + count
        self.total_files += count

    def to_dict(self) -> dict:
        """
        Convert to dictionary for serialization.

        Returns:
            Dictionary representation
        """
        return {
            "scan_timestamp": self.scan_timestamp.isoformat(),
            "root_directory": self.root_directory,
            "projects": self.projects,
            "total_files": self.total_files,
            "files_by_type": self.files_by_type,
            "scan_duration_seconds": self.scan_duration_seconds,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "DiscoveryInventory":
        """
        Create DiscoveryInventory from dictionary.

        Args:
            data: Dictionary with inventory data

        Returns:
            DiscoveryInventory instance
        """
        # Convert scan_timestamp string to datetime if needed
        if isinstance(data.get("scan_timestamp"), str):
            data["scan_timestamp"] = datetime.fromisoformat(data["scan_timestamp"])

        return cls(**data)

    def save_jsonl(self, output_path: Path):
        """
        Save inventory to JSONL file (one project per line for streaming).

        Args:
            output_path: Path to output file
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("w") as f:
            # Write header with metadata
            header = {
                "scan_timestamp": self.scan_timestamp.isoformat(),
                "root_directory": self.root_directory,
                "total_files": self.total_files,
                "files_by_type": self.files_by_type,
                "scan_duration_seconds": self.scan_duration_seconds,
            }
            f.write(json.dumps(header) + "\n")

            # Write each project on separate line
            for project in self.projects:
                f.write(json.dumps(project) + "\n")

    @classmethod
    def load_jsonl(cls, input_path: Path) -> "DiscoveryInventory":
        """
        Load inventory from JSONL file.

        Args:
            input_path: Path to input file

        Returns:
            DiscoveryInventory instance
        """
        with input_path.open("r") as f:
            # Read header (first line)
            header = json.loads(f.readline())

            # Read projects (remaining lines)
            projects = []
            for line in f:
                if line.strip():
                    projects.append(json.loads(line))

        return cls(
            scan_timestamp=datetime.fromisoformat(header["scan_timestamp"]),
            root_directory=header["root_directory"],
            projects=projects,
            total_files=header["total_files"],
            files_by_type=header.get("files_by_type", {}),
            scan_duration_seconds=header.get("scan_duration_seconds", 0.0),
        )

    def get_project_by_id(self, project_id: str) -> Optional[dict]:
        """
        Get project data by ID.

        Args:
            project_id: Project identifier

        Returns:
            Project data dict or None if not found
        """
        for project in self.projects:
            if project.get("project_id") == project_id:
                return project
        return None

    def summary_text(self) -> str:
        """
        Get human-readable summary.

        Returns:
            Summary string
        """
        lines = [
            f"Scanned: {self.root_directory}",
            f"Projects: {len(self.projects)}",
            f"Total files: {self.total_files}",
            f"Duration: {self.scan_duration_seconds:.1f}s",
        ]

        if self.files_by_type:
            lines.append("Files by type:")
            for artifact_type, count in sorted(self.files_by_type.items(), key=lambda x: x[1], reverse=True):
                lines.append(f"  - {artifact_type}: {count}")

        return "\n".join(lines)
