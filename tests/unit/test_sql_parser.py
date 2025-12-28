"""
Unit tests for SQL parser.

Tests parsing of SQL files to extract structural information.

NOTE: These tests should FAIL initially (TDD approach).
"""

import pytest
from pathlib import Path
from typing import List, Dict

from codeindex.parsers.sql_parser import (
    SQLParser,
    parse_sql_file,
    extract_statements,
    extract_tables,
    extract_statement_types,
)


# Fixtures
@pytest.fixture
def fixtures_dir():
    """Path to test fixtures directory."""
    return Path(__file__).parent.parent / "fixtures" / "sample_sql"


@pytest.fixture
def schema_sql_path(fixtures_dir):
    """Path to schema.sql."""
    return fixtures_dir / "schema.sql"


@pytest.fixture
def queries_sql_path(fixtures_dir):
    """Path to queries.sql."""
    return fixtures_dir / "queries.sql"


@pytest.fixture
def sql_parser():
    """SQLParser instance."""
    return SQLParser()


# Test statement extraction
class TestStatementExtraction:
    """Test SQL statement extraction."""

    def test_extract_statements_from_schema(self, sql_parser, schema_sql_path):
        """Test extracting statements from schema file."""
        statements = sql_parser.extract_statements(schema_sql_path)

        assert len(statements) >= 5  # CREATE TABLE, INDEX, INSERT

    def test_extract_statements_from_queries(self, sql_parser, queries_sql_path):
        """Test extracting statements from queries file."""
        statements = sql_parser.extract_statements(queries_sql_path)

        assert len(statements) >= 4  # Multiple SELECT, UPDATE

    def test_statements_split_by_semicolon(self, sql_parser):
        """Test that statements are split by semicolon."""
        content = """
        SELECT * FROM users;
        SELECT * FROM roles;
        INSERT INTO users VALUES (1, 'test');
        """
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            statements = sql_parser.extract_statements(temp_path)
            assert len(statements) == 3
        finally:
            temp_path.unlink()


# Test statement type extraction
class TestStatementTypeExtraction:
    """Test SQL statement type extraction."""

    def test_extract_select_statements(self, sql_parser, queries_sql_path):
        """Test extracting SELECT statements."""
        types = sql_parser.extract_statement_types(queries_sql_path)

        assert 'SELECT' in types
        assert types['SELECT'] >= 3  # Multiple SELECT statements

    def test_extract_create_statements(self, sql_parser, schema_sql_path):
        """Test extracting CREATE statements."""
        types = sql_parser.extract_statement_types(schema_sql_path)

        assert 'CREATE' in types or 'CREATE TABLE' in types or 'CREATE INDEX' in types
        assert sum(v for k, v in types.items() if 'CREATE' in k) >= 3

    def test_extract_insert_statements(self, sql_parser, schema_sql_path):
        """Test extracting INSERT statements."""
        types = sql_parser.extract_statement_types(schema_sql_path)

        assert 'INSERT' in types
        assert types['INSERT'] >= 1

    def test_extract_update_statements(self, sql_parser, queries_sql_path):
        """Test extracting UPDATE statements."""
        types = sql_parser.extract_statement_types(queries_sql_path)

        assert 'UPDATE' in types
        assert types['UPDATE'] >= 1


# Test table extraction
class TestTableExtraction:
    """Test SQL table name extraction."""

    def test_extract_tables_from_schema(self, sql_parser, schema_sql_path):
        """Test extracting table names from schema."""
        tables = sql_parser.extract_tables(schema_sql_path)

        assert 'users' in tables
        assert 'roles' in tables
        assert 'user_roles' in tables

    def test_extract_tables_from_queries(self, sql_parser, queries_sql_path):
        """Test extracting table names from queries."""
        tables = sql_parser.extract_tables(queries_sql_path)

        assert 'users' in tables
        assert 'roles' in tables

    def test_extract_tables_from_join(self, sql_parser):
        """Test extracting tables from JOIN statements."""
        content = """
        SELECT *
        FROM users u
        INNER JOIN orders o ON u.id = o.user_id
        LEFT JOIN products p ON o.product_id = p.id;
        """
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            tables = sql_parser.extract_tables(temp_path)
            assert 'users' in tables
            assert 'orders' in tables
            assert 'products' in tables
        finally:
            temp_path.unlink()


# Test full parsing
class TestFullParsing:
    """Test complete SQL file parsing."""

    def test_parse_sql_file_returns_dict(self, sql_parser, schema_sql_path):
        """Test that parse returns structured dict."""
        result = sql_parser.parse_file(schema_sql_path)

        assert isinstance(result, dict)
        assert 'statements' in result
        assert 'tables' in result
        assert 'statement_types' in result

    def test_parse_schema_file(self, sql_parser, schema_sql_path):
        """Test parsing schema file."""
        result = sql_parser.parse_file(schema_sql_path)

        assert len(result['statements']) >= 5
        assert 'users' in result['tables']
        assert 'CREATE' in str(result['statement_types'])

    def test_parse_queries_file(self, sql_parser, queries_sql_path):
        """Test parsing queries file."""
        result = sql_parser.parse_file(queries_sql_path)

        assert len(result['statements']) >= 4
        assert 'users' in result['tables']
        assert 'SELECT' in result['statement_types']


# Test standalone functions
class TestStandaloneFunctions:
    """Test standalone parser functions."""

    def test_parse_sql_file_function(self, schema_sql_path):
        """Test standalone parse_sql_file function."""
        result = parse_sql_file(schema_sql_path)

        assert isinstance(result, dict)
        assert 'statements' in result

    def test_extract_statements_function(self, schema_sql_path):
        """Test standalone extract_statements function."""
        statements = extract_statements(schema_sql_path)

        assert isinstance(statements, list)
        assert len(statements) >= 5

    def test_extract_tables_function(self, schema_sql_path):
        """Test standalone extract_tables function."""
        tables = extract_tables(schema_sql_path)

        assert isinstance(tables, list)
        assert 'users' in tables


# Test error handling
class TestErrorHandling:
    """Test error handling in SQL parser."""

    def test_parse_empty_file(self, sql_parser, tmp_path):
        """Test parsing empty file."""
        empty = tmp_path / "empty.sql"
        empty.write_text("")

        result = sql_parser.parse_file(empty)
        assert isinstance(result, dict)
        assert len(result['statements']) == 0

    def test_parse_nonexistent_file(self, sql_parser):
        """Test parsing non-existent file."""
        with pytest.raises(FileNotFoundError):
            sql_parser.parse_file(Path("/nonexistent/file.sql"))

    def test_parse_malformed_sql(self, sql_parser, tmp_path):
        """Test parsing malformed SQL."""
        malformed = tmp_path / "malformed.sql"
        malformed.write_text("SELECT * FROM WHERE;")

        # Should not crash
        result = sql_parser.parse_file(malformed)
        assert isinstance(result, dict)


# Test comment handling
class TestCommentHandling:
    """Test SQL comment handling."""

    def test_statements_exclude_comments(self, sql_parser):
        """Test that comments are handled properly."""
        content = """
        -- This is a comment
        SELECT * FROM users;
        /* Multi-line
           comment */
        SELECT * FROM roles;
        """
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            statements = sql_parser.extract_statements(temp_path)
            # Should have 2 SELECT statements, not count comments
            assert len(statements) == 2
        finally:
            temp_path.unlink()

    def test_inline_comments_preserved(self, sql_parser, schema_sql_path):
        """Test that inline comments are handled."""
        # schema.sql has comments
        result = sql_parser.parse_file(schema_sql_path)

        # Should still extract statements despite comments
        assert len(result['statements']) >= 5


# Test edge cases
class TestEdgeCases:
    """Test edge cases in SQL parsing."""

    def test_parse_case_insensitive(self, sql_parser):
        """Test parsing with different case."""
        content = """
        select * from USERS;
        SELECT * FROM users;
        SeLeCt * FrOm Users;
        """
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            result = sql_parser.parse_file(temp_path)
            # Should recognize all as SELECT
            assert result['statement_types'].get('SELECT', 0) == 3
            # Should find users table
            assert 'users' in [t.lower() for t in result['tables']]
        finally:
            temp_path.unlink()

    def test_parse_complex_query(self, sql_parser):
        """Test parsing complex query."""
        content = """
        WITH active_users AS (
            SELECT id FROM users WHERE is_active = TRUE
        )
        SELECT u.username, COUNT(o.id) as order_count
        FROM users u
        INNER JOIN orders o ON u.id = o.user_id
        WHERE u.id IN (SELECT id FROM active_users)
        GROUP BY u.username
        HAVING COUNT(o.id) > 5
        ORDER BY order_count DESC
        LIMIT 10;
        """
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            result = sql_parser.parse_file(temp_path)
            # Should find tables even in complex query
            tables = [t.lower() for t in result['tables']]
            assert 'users' in tables
            assert 'orders' in tables
        finally:
            temp_path.unlink()


# Integration-like tests
class TestIntegration:
    """Test integration of parser components."""

    def test_full_workflow_schema(self, sql_parser, schema_sql_path):
        """Test complete parsing workflow for schema."""
        result = sql_parser.parse_file(schema_sql_path)

        # Verify structure
        assert len(result['statements']) >= 5

        # Verify tables
        tables = [t.lower() for t in result['tables']]
        assert 'users' in tables
        assert 'roles' in tables
        assert 'user_roles' in tables

        # Verify statement types
        types = result['statement_types']
        assert 'INSERT' in types

    def test_full_workflow_queries(self, sql_parser, queries_sql_path):
        """Test complete parsing workflow for queries."""
        result = sql_parser.parse_file(queries_sql_path)

        # Verify statements
        assert len(result['statements']) >= 4

        # Verify tables
        tables = [t.lower() for t in result['tables']]
        assert 'users' in tables

        # Verify statement types
        types = result['statement_types']
        assert 'SELECT' in types
        assert 'UPDATE' in types


# Test FK extraction from JOIN statements (T034)
class TestExtractFKFromJoinStatements:
    """Test extracting foreign key relationships from SQL JOIN ON clauses."""

    def test_extract_fk_from_inner_join_simple(self):
        """Test extracting FK from simple INNER JOIN"""
        from codeindex.parsers.sql_parser import extract_foreign_keys_from_joins

        sql = """
        SELECT t.*, s.*
        FROM single_turnaround t
        INNER JOIN sales_info s ON t.sales_info_id = s.sales_info_id
        """

        # When extracting FK
        fks = extract_foreign_keys_from_joins(sql)

        # Then should extract 1 FK
        assert len(fks) == 1
        assert fks[0].source_entity == "single_turnaround"
        assert fks[0].source_column == "sales_info_id"
        assert fks[0].target_entity == "sales_info"
        assert fks[0].target_column == "sales_info_id"

    def test_extract_fk_from_left_join(self):
        """Test extracting FK from LEFT JOIN"""
        from codeindex.parsers.sql_parser import extract_foreign_keys_from_joins

        sql = """
        SELECT t.*, p.*
        FROM single_turnaround t
        LEFT JOIN products p ON t.product_id = p.product_id
        """

        # When extracting FK
        fks = extract_foreign_keys_from_joins(sql)

        # Then should extract 1 FK
        assert len(fks) == 1
        assert fks[0].source_column == "product_id"
        assert fks[0].target_column == "product_id"

    def test_extract_fk_from_multiple_joins(self):
        """Test extracting FK from multiple JOIN statements"""
        from codeindex.parsers.sql_parser import extract_foreign_keys_from_joins

        sql = """
        SELECT t.*, s.*, c.*
        FROM single_turnaround t
        INNER JOIN sales_info s ON t.sales_info_id = s.id
        INNER JOIN customers c ON t.customer_id = c.id
        LEFT JOIN products p ON t.product_id = p.product_id
        """

        # When extracting all FK
        fks = extract_foreign_keys_from_joins(sql)

        # Then should extract 3 FK
        assert len(fks) == 3
        fk_columns = [(fk.source_column, fk.target_column) for fk in fks]
        assert ("sales_info_id", "id") in fk_columns
        assert ("customer_id", "id") in fk_columns
        assert ("product_id", "product_id") in fk_columns

    def test_extract_fk_with_table_aliases(self):
        """Test extracting FK when tables use aliases"""
        from codeindex.parsers.sql_parser import extract_foreign_keys_from_joins

        sql = """
        SELECT t.turnaround_id, s.sales_name
        FROM single_turnaround AS t
        JOIN sales_info AS s ON t.sales_info_id = s.sales_info_id
        """

        # When extracting FK
        fks = extract_foreign_keys_from_joins(sql)

        # Then should extract FK with original table names
        assert len(fks) == 1
        assert fks[0].source_entity == "single_turnaround"
        assert fks[0].target_entity == "sales_info"

    def test_extract_fk_from_complex_join_condition(self):
        """Test extracting FK from JOIN with complex conditions"""
        from codeindex.parsers.sql_parser import extract_foreign_keys_from_joins

        sql = """
        SELECT t.*
        FROM single_turnaround t
        JOIN sales_info s ON (t.sales_info_id = s.sales_info_id AND s.is_active = 1)
        """

        # When extracting FK
        fks = extract_foreign_keys_from_joins(sql)

        # Then should extract FK from equality condition only
        assert len(fks) == 1
        assert fks[0].source_column == "sales_info_id"
        assert fks[0].target_column == "sales_info_id"
