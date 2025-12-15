"""Project configuration model for dependency resolution and discovery."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class ProjectConfiguration:
    """
    Configuration for Maven dependency resolution and discovery.

    Manages base directory resolution with optional project subdirectory.
    Validates paths exist before processing.
    """

    # Base paths (required)
    java_source_dir: Path
    project_subdirectory: Optional[str] = None

    # Computed paths (set in __post_init__)
    effective_base_dir: Path = field(init=False)

    # Dependency resolution settings
    dependency_depth: int = 1
    resolve_transitive: bool = True

    # Error handling
    continue_on_error: bool = True
    log_level: str = "INFO"

    # Output paths
    output_dir: Path = field(default_factory=lambda: Path("./output"))

    def __post_init__(self):
        """
        Compute effective base directory after initialization.

        Validates that java_source_dir exists and computes effective_base_dir
        based on project_subdirectory if provided.
        """
        # Ensure paths are Path objects
        self.java_source_dir = Path(self.java_source_dir)
        self.output_dir = Path(self.output_dir)

        # Compute effective base directory
        if self.project_subdirectory:
            self.effective_base_dir = self.java_source_dir / self.project_subdirectory
        else:
            self.effective_base_dir = self.java_source_dir

        # Validate paths exist
        if not self.java_source_dir.exists():
            raise ValueError(
                f"JAVA_SOURCE_DIR does not exist: {self.java_source_dir}"
            )

        if not self.java_source_dir.is_dir():
            raise ValueError(
                f"JAVA_SOURCE_DIR is not a directory: {self.java_source_dir}"
            )

        if self.project_subdirectory and not self.effective_base_dir.exists():
            raise ValueError(
                f"Project directory does not exist: {self.effective_base_dir}\n"
                f"  JAVA_SOURCE_DIR: {self.java_source_dir}\n"
                f"  project_subdirectory: {self.project_subdirectory}"
            )

        if self.project_subdirectory and not self.effective_base_dir.is_dir():
            raise ValueError(
                f"Project path is not a directory: {self.effective_base_dir}"
            )

        # Validate dependency depth
        if self.dependency_depth < 0:
            raise ValueError(
                f"dependency_depth must be >= 0, got: {self.dependency_depth}"
            )

        # Validate log level
        valid_log_levels = {"DEBUG", "INFO", "WARNING", "ERROR"}
        if self.log_level not in valid_log_levels:
            raise ValueError(
                f"Invalid log_level: {self.log_level}. "
                f"Must be one of: {valid_log_levels}"
            )

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"ProjectConfiguration("
            f"java_source_dir={self.java_source_dir}, "
            f"project={self.project_subdirectory}, "
            f"effective_base={self.effective_base_dir}, "
            f"depth={self.dependency_depth})"
        )

    @property
    def has_project_scope(self) -> bool:
        """Check if project-scoped analysis is configured."""
        return self.project_subdirectory is not None

    def get_project_name(self) -> str:
        """
        Get the project name for this configuration.

        Returns the project_subdirectory if set, otherwise the directory name
        of java_source_dir.
        """
        if self.project_subdirectory:
            return self.project_subdirectory
        return self.java_source_dir.name
