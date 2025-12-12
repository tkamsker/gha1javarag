"""
Per-project file locking for Java Codebase Indexer Pipeline.

Prevents concurrent operations on the same project while allowing
parallel processing of different projects.
"""
import logging
from pathlib import Path
from typing import Optional
from contextlib import contextmanager
from filelock import FileLock, Timeout as FileLockTimeout

logger = logging.getLogger("codeindex.locking")


class ProjectLock:
    """
    File-based lock for project operations.

    Uses filelock library for cross-platform, cross-process locking.
    """

    def __init__(
        self,
        project_id: str,
        lock_dir: Optional[Path] = None,
        timeout: int = 5
    ):
        """
        Initialize project lock.

        Args:
            project_id: Unique project identifier
            lock_dir: Directory for lock files (default: /tmp)
            timeout: Timeout in seconds for acquiring lock (default: 5)
        """
        self.project_id = project_id
        self.timeout = timeout

        # Sanitize project_id for filename
        safe_id = project_id.replace(":", "_").replace("/", "_")

        # Determine lock file path
        if lock_dir:
            lock_dir.mkdir(parents=True, exist_ok=True)
            self.lock_path = lock_dir / f".codeindex-{safe_id}.lock"
        else:
            # Use system temp directory
            import tempfile
            temp_dir = Path(tempfile.gettempdir())
            self.lock_path = temp_dir / f".codeindex-{safe_id}.lock"

        self.lock = FileLock(str(self.lock_path), timeout=timeout)

    def acquire(self) -> bool:
        """
        Acquire lock.

        Returns:
            True if lock acquired, False if timeout

        Raises:
            ProjectLockError: If lock cannot be acquired
        """
        try:
            self.lock.acquire(timeout=self.timeout)
            logger.debug(f"Acquired lock for project: {self.project_id}")
            return True
        except FileLockTimeout:
            raise ProjectLockError(
                f"Project {self.project_id} is currently being processed by another operation. "
                f"Lock file: {self.lock_path}. "
                f"Wait for the operation to complete or remove the lock file if the process is stuck."
            )

    def release(self):
        """Release lock."""
        try:
            self.lock.release()
            logger.debug(f"Released lock for project: {self.project_id}")
        except Exception as e:
            logger.warning(f"Error releasing lock for project {self.project_id}: {e}")

    def is_locked(self) -> bool:
        """
        Check if project is currently locked.

        Returns:
            True if locked by this or another process
        """
        return self.lock.is_locked

    def __enter__(self):
        """Context manager entry."""
        self.acquire()
        return self

    def __exit__(self, *args):
        """Context manager exit."""
        self.release()


class ProjectLockError(Exception):
    """Exception raised when project lock cannot be acquired."""
    pass


@contextmanager
def project_lock(project_id: str, timeout: int = 5):
    """
    Context manager for project locking.

    Args:
        project_id: Unique project identifier
        timeout: Timeout in seconds for acquiring lock

    Yields:
        ProjectLock instance

    Raises:
        ProjectLockError: If lock cannot be acquired

    Example:
        with project_lock("com.example:myapp:1.0.0"):
            # Perform operations on project
            index_project(...)
    """
    lock = ProjectLock(project_id, timeout=timeout)
    try:
        lock.acquire()
        yield lock
    finally:
        lock.release()


def cleanup_stale_locks(lock_dir: Optional[Path] = None, max_age_hours: int = 24):
    """
    Clean up stale lock files.

    Removes lock files older than max_age_hours that are not currently held.

    Args:
        lock_dir: Directory containing lock files (default: system temp)
        max_age_hours: Maximum age in hours before considering lock stale
    """
    import time
    import tempfile

    if lock_dir is None:
        lock_dir = Path(tempfile.gettempdir())

    if not lock_dir.exists():
        return

    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    removed_count = 0

    for lock_file in lock_dir.glob(".codeindex-*.lock"):
        try:
            # Check file age
            file_age = current_time - lock_file.stat().st_mtime

            if file_age > max_age_seconds:
                # Try to acquire lock (will only succeed if not held)
                lock = FileLock(str(lock_file), timeout=0.1)
                try:
                    lock.acquire(timeout=0.1)
                    lock.release()
                    # Successfully acquired and released, safe to delete
                    lock_file.unlink()
                    removed_count += 1
                    logger.info(f"Removed stale lock file: {lock_file}")
                except FileLockTimeout:
                    # Lock is held, skip
                    logger.debug(f"Lock file still in use: {lock_file}")
        except Exception as e:
            logger.warning(f"Error checking lock file {lock_file}: {e}")

    if removed_count > 0:
        logger.info(f"Cleaned up {removed_count} stale lock file(s)")
