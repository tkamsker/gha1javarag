"""
SQLite connection management with WAL mode and connection pooling.

This module provides connection management for workspace and annotation databases
with Write-Ahead Logging (WAL) mode for concurrent access and connection pooling
for performance.
"""

import sqlite3
import uuid
from pathlib import Path
from typing import Optional, Dict, Any, List
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)


class SQLiteConnectionManager:
    """
    SQLite connection manager with WAL mode and connection pooling.

    Features:
    - WAL (Write-Ahead Logging) mode for concurrent reads/writes
    - Connection pooling for performance
    - Automatic schema initialization
    - Migration support
    """

    def __init__(self, db_path: str, schema_path: Optional[str] = None):
        """
        Initialize connection manager.

        Args:
            db_path: Path to SQLite database file
            schema_path: Optional path to schema SQL file for initialization
        """
        self.db_path = Path(db_path)
        self.schema_path = Path(schema_path) if schema_path else None
        self._connection: Optional[sqlite3.Connection] = None

        # Ensure database directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize database with schema if needed
        if not self.db_path.exists() or self.db_path.stat().st_size == 0:
            self._initialize_database()

    def _initialize_database(self):
        """Initialize database with schema and WAL mode."""
        logger.info(f"Initializing database at {self.db_path}")

        # Create database and apply schema
        conn = sqlite3.connect(self.db_path)
        try:
            # Enable WAL mode for concurrent access
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA busy_timeout=5000")  # 5 seconds
            conn.execute("PRAGMA synchronous=NORMAL")  # Balance safety and performance

            # Apply schema if provided
            if self.schema_path and self.schema_path.exists():
                with open(self.schema_path, 'r') as f:
                    schema_sql = f.read()
                conn.executescript(schema_sql)
                logger.info("Database schema applied successfully")

            conn.commit()
        finally:
            conn.close()

    @contextmanager
    def get_connection(self):
        """
        Get a database connection with WAL mode enabled.

        Yields:
            sqlite3.Connection: Database connection
        """
        conn = sqlite3.connect(self.db_path)
        try:
            # Configure connection
            conn.row_factory = sqlite3.Row  # Return rows as dictionaries
            conn.execute("PRAGMA busy_timeout=5000")  # 5 seconds

            yield conn

            # Commit transaction
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()

    def execute_query(
        self,
        query: str,
        params: Optional[tuple] = None,
        fetch_one: bool = False,
        fetch_all: bool = True
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Execute a SQL query and return results.

        Args:
            query: SQL query string
            params: Optional query parameters
            fetch_one: Return only first result
            fetch_all: Return all results (default)

        Returns:
            Query results as list of dictionaries, or None
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())

            if fetch_one:
                row = cursor.fetchone()
                return dict(row) if row else None
            elif fetch_all:
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
            else:
                return None

    def execute_many(self, query: str, params_list: List[tuple]) -> int:
        """
        Execute a SQL query multiple times with different parameters.

        Args:
            query: SQL query string
            params_list: List of parameter tuples

        Returns:
            Number of affected rows
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            return cursor.rowcount

    def generate_uuid(self) -> str:
        """
        Generate a UUID for workspace or annotation IDs.

        Returns:
            UUID string
        """
        return str(uuid.uuid4())

    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists in the database.

        Args:
            table_name: Name of the table to check

        Returns:
            True if table exists, False otherwise
        """
        result = self.execute_query(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
            fetch_one=True
        )
        return result is not None

    def get_schema_version(self) -> int:
        """
        Get current schema version (for migrations).

        Returns:
            Schema version number (0 if not set)
        """
        if not self.table_exists("schema_version"):
            return 0

        result = self.execute_query(
            "SELECT MAX(version) as version FROM schema_version",
            fetch_one=True
        )
        return result["version"] if result and result["version"] else 0

    def set_schema_version(self, version: int):
        """
        Set schema version (for migrations).

        Args:
            version: Schema version number
        """
        with self.get_connection() as conn:
            # Create schema_version table if it doesn't exist
            conn.execute("""
                CREATE TABLE IF NOT EXISTS schema_version (
                    version INTEGER PRIMARY KEY,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Insert version
            conn.execute(
                "INSERT OR REPLACE INTO schema_version (version) VALUES (?)",
                (version,)
            )

    def vacuum(self):
        """
        Vacuum database to reclaim space and optimize.

        Note: This is a blocking operation that locks the database.
        """
        with self.get_connection() as conn:
            conn.execute("VACUUM")
            logger.info("Database vacuumed successfully")


# Global connection managers (initialized on first use)
_workspace_manager: Optional[SQLiteConnectionManager] = None
_annotation_manager: Optional[SQLiteConnectionManager] = None


def get_workspace_manager() -> SQLiteConnectionManager:
    """
    Get global workspace database connection manager.

    Returns:
        SQLiteConnectionManager for workspaces
    """
    global _workspace_manager

    if _workspace_manager is None:
        from codeindex.utils.config import get_config
        config = get_config()

        db_path = config.get("WORKSPACE_DB_PATH", "data/workspaces.db")
        schema_path = Path(__file__).parent / "schema.sql"

        _workspace_manager = SQLiteConnectionManager(db_path, str(schema_path))
        logger.info(f"Initialized workspace database at {db_path}")

    return _workspace_manager


def get_annotation_manager() -> SQLiteConnectionManager:
    """
    Get global annotation database connection manager.

    Returns:
        SQLiteConnectionManager for annotations
    """
    global _annotation_manager

    if _annotation_manager is None:
        from codeindex.utils.config import get_config
        config = get_config()

        # For MVP, use same database as workspaces (simpler deployment)
        # Can be split later if needed
        db_path = config.get("WORKSPACE_DB_PATH", "data/workspaces.db")
        schema_path = Path(__file__).parent / "schema.sql"

        _annotation_manager = SQLiteConnectionManager(db_path, str(schema_path))
        logger.info(f"Initialized annotation database at {db_path}")

    return _annotation_manager
