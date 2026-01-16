"""
Code Service for reading and validating source files (T186 - US4.1).

Provides secure file reading with path validation and error handling.
"""

import logging
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


# Custom exceptions
class CodeServiceError(Exception):
    """Base exception for code service errors."""
    pass


class FileNotFoundError(CodeServiceError):
    """File not found error."""
    pass


class FileTooLargeError(CodeServiceError):
    """File too large error."""
    pass


class DirectoryTraversalError(CodeServiceError):
    """Directory traversal attempt error."""
    pass


class CodeService:
    """
    Service for reading source code files with validation and caching.

    Provides:
    - Secure file reading with path validation
    - Directory traversal prevention
    - File size limits
    - Optional caching for performance
    """

    def __init__(
        self,
        source_root: Optional[str] = None,
        max_file_size_mb: int = 10,
        enable_cache: bool = False
    ):
        """
        Initialize code service.

        Args:
            source_root: Root directory for source files (defaults to JAVA_SOURCE_DIR from config)
            max_file_size_mb: Maximum file size in MB (default: 10MB)
            enable_cache: Enable file content caching (default: False)
        """
        if source_root:
            self.source_root = Path(source_root).resolve()
        else:
            from src.codeindex.utils.config import get_config
            config = get_config()
            self.source_root = Path(config.get('JAVA_SOURCE_DIR', '.')).resolve()

        self.max_file_size_bytes = max_file_size_mb * 1024 * 1024
        self.enable_cache = enable_cache
        self._cache: Dict[str, Tuple[str, float]] = {}  # path -> (content, mtime)

        logger.info(f"CodeService initialized with source_root={self.source_root}, max_size={max_file_size_mb}MB")

    def read_file(self, file_path: str, encoding: str = 'utf-8') -> str:
        """
        Read source file with validation and caching.

        Args:
            file_path: Relative or absolute path to file
            encoding: File encoding (default: utf-8)

        Returns:
            File content as string

        Raises:
            DirectoryTraversalError: If path is outside source root
            FileNotFoundError: If file does not exist
            FileTooLargeError: If file exceeds max size
            CodeServiceError: For other errors
        """
        # Validate path
        is_valid, resolved_path = validate_file_path(file_path, self.source_root)
        if not is_valid:
            raise DirectoryTraversalError(f"Invalid file path: {file_path}")

        # Check file size
        file_size = resolved_path.stat().st_size if resolved_path.exists() else 0
        if file_size > self.max_file_size_bytes:
            raise FileTooLargeError(
                f"File too large: {file_size / (1024 * 1024):.1f}MB exceeds {self.max_file_size_bytes / (1024 * 1024):.0f}MB limit"
            )

        # Check cache
        if self.enable_cache:
            cache_key = str(resolved_path)
            if cache_key in self._cache:
                cached_content, cached_mtime = self._cache[cache_key]
                current_mtime = resolved_path.stat().st_mtime
                if current_mtime == cached_mtime:
                    logger.debug(f"Cache hit for {file_path}")
                    return cached_content

        # Read file
        try:
            content = read_source_file(resolved_path, encoding=encoding)

            # Update cache
            if self.enable_cache:
                mtime = resolved_path.stat().st_mtime
                self._cache[str(resolved_path)] = (content, mtime)

            return content

        except Exception as e:
            if isinstance(e, (FileNotFoundError, FileTooLargeError, DirectoryTraversalError)):
                raise
            raise CodeServiceError(f"Failed to read file {file_path}: {e}")

    def get_file_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Get file metadata.

        Args:
            file_path: Relative or absolute path to file

        Returns:
            Dictionary with file metadata

        Raises:
            DirectoryTraversalError: If path is outside source root
        """
        is_valid, resolved_path = validate_file_path(file_path, self.source_root)
        if not is_valid:
            raise DirectoryTraversalError(f"Invalid file path: {file_path}")

        info = get_file_info(resolved_path)
        info['relative_path'] = str(Path(file_path))
        info['absolute_path'] = str(resolved_path)

        return info

    def list_files(self, directory_path: str = "", pattern: str = "*") -> List[Path]:
        """
        List files in directory.

        Args:
            directory_path: Relative directory path (default: root)
            pattern: Glob pattern (default: *)

        Returns:
            List of file paths

        Raises:
            DirectoryTraversalError: If path is outside source root
        """
        if directory_path:
            is_valid, resolved_path = validate_file_path(directory_path, self.source_root)
            if not is_valid:
                raise DirectoryTraversalError(f"Invalid directory path: {directory_path}")
        else:
            resolved_path = self.source_root

        if not resolved_path.is_dir():
            raise CodeServiceError(f"Path is not a directory: {directory_path}")

        return list(resolved_path.glob(pattern))

    def file_exists(self, file_path: str) -> bool:
        """
        Check if file exists.

        Args:
            file_path: Relative or absolute path to file

        Returns:
            True if file exists, False otherwise
        """
        try:
            is_valid, resolved_path = validate_file_path(file_path, self.source_root)
            return is_valid and resolved_path.exists() and resolved_path.is_file()
        except Exception:
            return False


def validate_file_path(file_path: str, source_root: Path) -> Tuple[bool, Path]:
    """
    Validate file path to prevent directory traversal attacks.

    Args:
        file_path: File path to validate (relative or absolute)
        source_root: Source root directory

    Returns:
        Tuple of (is_valid, resolved_path)

    Raises:
        DirectoryTraversalError: If path attempts directory traversal
    """
    try:
        # Normalize path separators
        file_path = str(file_path).replace('\\', '/')

        # Convert to Path
        path = Path(file_path)

        # Resolve to absolute path
        if path.is_absolute():
            resolved = path.resolve()
        else:
            resolved = (source_root / path).resolve()

        # Check if resolved path is within source root
        try:
            resolved.relative_to(source_root)
        except ValueError:
            raise DirectoryTraversalError(f"Path {file_path} is outside source root {source_root}")

        # Check for symlinks pointing outside source root
        if resolved.is_symlink():
            target = resolved.readlink()
            if target.is_absolute():
                try:
                    target.resolve().relative_to(source_root)
                except ValueError:
                    raise DirectoryTraversalError(f"Symlink {file_path} points outside source root")

        return True, resolved

    except DirectoryTraversalError:
        raise
    except Exception as e:
        logger.warning(f"Path validation failed for {file_path}: {e}")
        return False, Path()


def read_source_file(file_path: Path, encoding: str = 'utf-8') -> str:
    """
    Read source file content.

    Args:
        file_path: Absolute path to file
        encoding: File encoding (default: utf-8)

    Returns:
        File content as string

    Raises:
        FileNotFoundError: If file does not exist
        CodeServiceError: For other errors
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.is_dir():
        raise CodeServiceError(f"Path is a directory: {file_path}")

    try:
        return file_path.read_text(encoding=encoding)
    except PermissionError as e:
        raise CodeServiceError(f"Permission denied: {file_path}") from e
    except UnicodeDecodeError as e:
        raise CodeServiceError(f"File encoding error: {file_path}") from e
    except Exception as e:
        raise CodeServiceError(f"Failed to read file {file_path}: {e}") from e


def get_file_info(file_path: Path) -> Dict[str, Any]:
    """
    Get file information.

    Args:
        file_path: Path to file

    Returns:
        Dictionary with file info:
        - exists: bool
        - is_file: bool
        - is_directory: bool
        - size_bytes: int
        - extension: str
        - modified_time: str (ISO format)
    """
    info = {
        "exists": file_path.exists(),
        "is_file": file_path.is_file() if file_path.exists() else False,
        "is_directory": file_path.is_dir() if file_path.exists() else False,
        "size_bytes": file_path.stat().st_size if file_path.exists() else 0,
        "extension": file_path.suffix if file_path.exists() else "",
    }

    if file_path.exists():
        mtime = file_path.stat().st_mtime
        info["modified_time"] = datetime.fromtimestamp(mtime).isoformat()

    return info


# Global service instance
_code_service: Optional[CodeService] = None


def get_code_service() -> CodeService:
    """
    Get global CodeService instance.

    Returns:
        CodeService singleton
    """
    global _code_service

    if _code_service is None:
        _code_service = CodeService()
        logger.info("Created global CodeService instance")

    return _code_service


__all__ = [
    "CodeService",
    "CodeServiceError",
    "FileNotFoundError",
    "FileTooLargeError",
    "DirectoryTraversalError",
    "validate_file_path",
    "read_source_file",
    "get_file_info",
    "get_code_service"
]
