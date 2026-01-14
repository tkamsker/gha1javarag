"""
Unit tests for SQLite connection management (T016).

Tests the SQLiteConnectionManager class including:
- Connection creation and WAL mode configuration
- Context manager behavior (commit/rollback)
- Schema initialization
- Migration support
- Connection pooling and reuse
- Error handling
"""

import pytest
import sqlite3
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from codeindex.web.database.connection import (
    SQLiteConnectionManager,
    get_workspace_manager,
    get_annotations_manager
)


class TestSQLiteConnectionManager:
    """Test SQLiteConnectionManager class."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test databases."""
        temp_path = tempfile.mkdtemp()
        yield Path(temp_path)
        shutil.rmtree(temp_path)

    @pytest.fixture
    def db_path(self, temp_dir):
        """Create temporary database path."""
        return str(temp_dir / "test.db")

    @pytest.fixture
    def schema_path(self, temp_dir):
        """Create temporary schema file."""
        schema_file = temp_dir / "schema.sql"
        schema_file.write_text("""
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );
        """)
        return str(schema_file)

    @pytest.fixture
    def manager(self, db_path, schema_path):
        """Create SQLiteConnectionManager instance."""
        return SQLiteConnectionManager(db_path, schema_path)

    def test_initialization(self, db_path, schema_path):
        """Test manager initialization."""
        manager = SQLiteConnectionManager(db_path, schema_path)

        assert manager.db_path == db_path
        assert manager.schema_path == schema_path
        assert Path(db_path).exists()

    def test_initialization_without_schema(self, db_path):
        """Test manager initialization without schema."""
        manager = SQLiteConnectionManager(db_path)

        assert manager.db_path == db_path
        assert manager.schema_path is None
        assert Path(db_path).exists()

    def test_wal_mode_configured(self, manager, db_path):
        """Test that WAL mode is properly configured."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode")
        mode = cursor.fetchone()[0]
        conn.close()

        assert mode.upper() == "WAL"

    def test_schema_applied(self, manager, db_path):
        """Test that schema is applied on initialization."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check that test_table exists
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='test_table'
        """)
        result = cursor.fetchone()
        conn.close()

        assert result is not None
        assert result[0] == "test_table"

    def test_context_manager_successful_commit(self, manager):
        """Test context manager commits on success."""
        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO test_table (name) VALUES (?)", ("test",))

        # Verify data was committed
        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM test_table")
            count = cursor.fetchone()[0]

        assert count == 1

    def test_context_manager_rollback_on_error(self, manager):
        """Test context manager rolls back on error."""
        try:
            with manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO test_table (name) VALUES (?)", ("test",))
                raise ValueError("Simulated error")
        except ValueError:
            pass

        # Verify data was rolled back
        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM test_table")
            count = cursor.fetchone()[0]

        assert count == 0

    def test_row_factory_returns_dicts(self, manager):
        """Test that connections use row_factory for dict results."""
        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO test_table (name) VALUES (?)", ("test",))

        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM test_table")
            row = cursor.fetchone()

        # sqlite3.Row allows dict-like access
        assert row["name"] == "test"
        assert row["id"] == 1

    def test_busy_timeout_configured(self, manager, db_path):
        """Test that busy timeout is configured."""
        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA busy_timeout")
            timeout = cursor.fetchone()[0]

        assert timeout == 5000  # 5 seconds in milliseconds

    def test_apply_schema_creates_tables(self, db_path, schema_path):
        """Test apply_schema method creates tables."""
        manager = SQLiteConnectionManager(db_path, schema_path=None)
        manager.apply_schema(schema_path)

        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name='test_table'
            """)
            result = cursor.fetchone()

        assert result is not None

    def test_apply_migrations(self, manager, temp_dir):
        """Test apply_migrations method."""
        # Create migrations directory
        migrations_dir = temp_dir / "migrations"
        migrations_dir.mkdir()

        # Create migration file
        migration_file = migrations_dir / "001_add_column.sql"
        migration_file.write_text("""
            ALTER TABLE test_table ADD COLUMN email TEXT;
        """)

        manager.apply_migrations(str(migrations_dir))

        # Verify column was added
        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(test_table)")
            columns = [col[1] for col in cursor.fetchall()]

        assert "email" in columns

    def test_generate_uuid(self, manager):
        """Test UUID generation."""
        uuid1 = manager.generate_uuid()
        uuid2 = manager.generate_uuid()

        assert len(uuid1) == 36
        assert len(uuid2) == 36
        assert uuid1 != uuid2

    def test_concurrent_connections(self, manager):
        """Test multiple concurrent connections."""
        # This tests that WAL mode allows concurrent reads
        with manager.get_connection() as conn1:
            cursor1 = conn1.cursor()
            cursor1.execute("INSERT INTO test_table (name) VALUES (?)", ("test1",))

            # Open second connection while first is still open
            with manager.get_connection() as conn2:
                cursor2 = conn2.cursor()
                cursor2.execute("INSERT INTO test_table (name) VALUES (?)", ("test2",))

        # Verify both inserts succeeded
        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM test_table")
            count = cursor.fetchone()[0]

        assert count == 2

    def test_get_workspace_manager_singleton(self):
        """Test get_workspace_manager returns singleton."""
        manager1 = get_workspace_manager()
        manager2 = get_workspace_manager()

        assert manager1 is manager2

    def test_get_annotations_manager_singleton(self):
        """Test get_annotations_manager returns singleton."""
        manager1 = get_annotations_manager()
        manager2 = get_annotations_manager()

        assert manager1 is manager2

    def test_schema_file_not_found(self, db_path):
        """Test handling of missing schema file."""
        with pytest.raises(FileNotFoundError):
            manager = SQLiteConnectionManager(db_path, "/nonexistent/schema.sql")

    def test_invalid_sql_in_schema(self, db_path, temp_dir):
        """Test handling of invalid SQL in schema."""
        bad_schema = temp_dir / "bad_schema.sql"
        bad_schema.write_text("INVALID SQL SYNTAX;")

        with pytest.raises(sqlite3.OperationalError):
            manager = SQLiteConnectionManager(db_path, str(bad_schema))

    def test_connection_close_on_context_exit(self, manager):
        """Test that connections are closed when context exits."""
        with manager.get_connection() as conn:
            pass

        # Attempting to use the connection should raise an error
        with pytest.raises(sqlite3.ProgrammingError):
            conn.execute("SELECT 1")


class TestConnectionManagerIntegration:
    """Integration tests for connection manager with actual database operations."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test databases."""
        temp_path = tempfile.mkdtemp()
        yield Path(temp_path)
        shutil.rmtree(temp_path)

    @pytest.fixture
    def full_schema_path(self):
        """Get path to actual schema.sql file."""
        return Path(__file__).parent.parent.parent.parent.parent / "src" / "codeindex" / "web" / "database" / "schema.sql"

    def test_full_schema_initialization(self, temp_dir, full_schema_path):
        """Test initialization with full production schema."""
        if not full_schema_path.exists():
            pytest.skip("Production schema.sql not found")

        db_path = str(temp_dir / "test.db")
        manager = SQLiteConnectionManager(db_path, str(full_schema_path))

        # Verify key tables exist
        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table'
                ORDER BY name
            """)
            tables = [row[0] for row in cursor.fetchall()]

        assert "workspaces" in tables
        assert "annotations" in tables
        assert "annotations_fts" in tables

    def test_workspace_crud_operations(self, temp_dir, full_schema_path):
        """Test CRUD operations on workspaces table."""
        if not full_schema_path.exists():
            pytest.skip("Production schema.sql not found")

        db_path = str(temp_dir / "test.db")
        manager = SQLiteConnectionManager(db_path, str(full_schema_path))

        workspace_id = manager.generate_uuid()

        # Create
        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO workspaces (id, name, description, state_json)
                VALUES (?, ?, ?, ?)
            """, (workspace_id, "Test Workspace", "Test Description", "{}"))

        # Read
        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM workspaces WHERE id = ?", (workspace_id,))
            workspace = cursor.fetchone()

        assert workspace["name"] == "Test Workspace"
        assert workspace["description"] == "Test Description"

        # Update
        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE workspaces SET name = ? WHERE id = ?
            """, ("Updated Workspace", workspace_id))

        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM workspaces WHERE id = ?", (workspace_id,))
            updated_name = cursor.fetchone()["name"]

        assert updated_name == "Updated Workspace"

        # Delete
        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM workspaces WHERE id = ?", (workspace_id,))

        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM workspaces WHERE id = ?", (workspace_id,))
            count = cursor.fetchone()[0]

        assert count == 0
