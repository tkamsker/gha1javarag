"""
SQL file parser.

Extracts structural information from SQL files including:
- Statement types (SELECT, INSERT, UPDATE, CREATE, etc.)
- Table names
- Query patterns
"""

import re
import logging
from pathlib import Path
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


# ==============================================================================
# Regular Expressions
# ==============================================================================

# Comments
SINGLE_LINE_COMMENT = re.compile(r'--.*?$', re.MULTILINE)
MULTI_LINE_COMMENT = re.compile(r'/\*.*?\*/', re.DOTALL)

# Statement keywords
STATEMENT_KEYWORDS = [
    'SELECT', 'INSERT', 'UPDATE', 'DELETE',
    'CREATE TABLE', 'CREATE INDEX', 'CREATE VIEW', 'CREATE',
    'ALTER TABLE', 'ALTER',
    'DROP TABLE', 'DROP INDEX', 'DROP',
    'TRUNCATE'
]

# Table name patterns
FROM_PATTERN = re.compile(
    r'\bFROM\s+([`"\[]?\w+[`"\]]?)(?:\s+(?:AS\s+)?\w+)?',
    re.IGNORECASE
)

JOIN_PATTERN = re.compile(
    r'\bJOIN\s+([`"\[]?\w+[`"\]]?)(?:\s+(?:AS\s+)?\w+)?',
    re.IGNORECASE
)

INTO_PATTERN = re.compile(
    r'\bINTO\s+([`"\[]?\w+[`"\]]?)',
    re.IGNORECASE
)

UPDATE_PATTERN = re.compile(
    r'\bUPDATE\s+([`"\[]?\w+[`"\]]?)',
    re.IGNORECASE
)

CREATE_TABLE_PATTERN = re.compile(
    r'\bCREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([`"\[]?\w+[`"\]]?)',
    re.IGNORECASE
)


# ==============================================================================
# SQLParser Class
# ==============================================================================

class SQLParser:
    """
    Parser for SQL files.

    Extracts structural information using regex patterns.
    """

    def __init__(self):
        """Initialize SQL parser."""
        self.logger = logging.getLogger(__name__)

    def parse_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Parse a SQL file.

        Args:
            file_path: Path to SQL file

        Returns:
            Dictionary with parsed elements

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        if not file_path.exists():
            raise FileNotFoundError(f"SQL file not found: {file_path}")

        content = file_path.read_text(encoding='utf-8')
        return self.parse(content)

    def parse(self, content: str) -> Dict[str, Any]:
        """
        Parse SQL source code.

        Args:
            content: SQL source code as string

        Returns:
            Dictionary with structural information
        """
        try:
            # Extract statements
            statements = self._extract_statements_from_content(content)

            # Extract tables and statement types
            tables = set()
            statement_types = {}

            for stmt in statements:
                # Extract statement type
                stmt_type = self._get_statement_type(stmt)
                if stmt_type:
                    statement_types[stmt_type] = statement_types.get(stmt_type, 0) + 1

                # Extract tables from statement
                stmt_tables = self._extract_tables_from_statement(stmt)
                tables.update(stmt_tables)

            result = {
                'statements': statements,
                'tables': sorted(list(tables)),
                'statement_types': statement_types,
                'statement_count': len(statements)
            }

            return result

        except Exception as e:
            self.logger.error(f"Error parsing SQL code: {e}", exc_info=True)
            # Return minimal result on error
            return {
                'statements': [],
                'tables': [],
                'statement_types': {},
                'statement_count': 0,
                'parse_error': str(e)
            }

    def extract_statements(self, file_path: Path) -> List[str]:
        """
        Extract SQL statements from file.

        Args:
            file_path: Path to SQL file

        Returns:
            List of SQL statements
        """
        if not file_path.exists():
            raise FileNotFoundError(f"SQL file not found: {file_path}")

        content = file_path.read_text(encoding='utf-8')
        return self._extract_statements_from_content(content)

    def extract_tables(self, file_path: Path) -> List[str]:
        """
        Extract table names from SQL file.

        Args:
            file_path: Path to SQL file

        Returns:
            List of table names
        """
        result = self.parse_file(file_path)
        return result['tables']

    def extract_statement_types(self, file_path: Path) -> Dict[str, int]:
        """
        Extract statement types and counts.

        Args:
            file_path: Path to SQL file

        Returns:
            Dictionary of statement type -> count
        """
        result = self.parse_file(file_path)
        return result['statement_types']

    def _extract_statements_from_content(self, content: str) -> List[str]:
        """
        Extract statements from SQL content.

        Args:
            content: SQL source code

        Returns:
            List of SQL statements
        """
        # Remove comments
        content = self._remove_comments(content)

        # Split by semicolon
        statements = []
        for stmt in content.split(';'):
            stmt = stmt.strip()
            if stmt and len(stmt) > 5:  # Skip very short fragments
                statements.append(stmt)

        return statements

    def _remove_comments(self, content: str) -> str:
        """
        Remove comments from SQL code.

        Args:
            content: SQL source code

        Returns:
            Code without comments
        """
        # Remove single-line comments
        content = SINGLE_LINE_COMMENT.sub('', content)
        # Remove multi-line comments
        content = MULTI_LINE_COMMENT.sub('', content)

        return content

    def _get_statement_type(self, statement: str) -> str:
        """
        Get statement type.

        Args:
            statement: SQL statement

        Returns:
            Statement type (e.g., 'SELECT', 'INSERT')
        """
        statement_upper = statement.upper().strip()

        # Check for specific multi-word keywords first
        for keyword in STATEMENT_KEYWORDS:
            if statement_upper.startswith(keyword):
                # Return simple type
                return keyword.split()[0]  # e.g., "CREATE TABLE" -> "CREATE"

        # Default: extract first word
        words = statement_upper.split()
        if words:
            return words[0]

        return 'UNKNOWN'

    def _extract_tables_from_statement(self, statement: str) -> List[str]:
        """
        Extract table names from a SQL statement.

        Args:
            statement: SQL statement

        Returns:
            List of table names
        """
        tables = set()

        # FROM clause
        for match in FROM_PATTERN.finditer(statement):
            table = self._clean_table_name(match.group(1))
            if table:
                tables.add(table)

        # JOIN clause
        for match in JOIN_PATTERN.finditer(statement):
            table = self._clean_table_name(match.group(1))
            if table:
                tables.add(table)

        # INTO clause (INSERT)
        for match in INTO_PATTERN.finditer(statement):
            table = self._clean_table_name(match.group(1))
            if table:
                tables.add(table)

        # UPDATE statement
        for match in UPDATE_PATTERN.finditer(statement):
            table = self._clean_table_name(match.group(1))
            if table:
                tables.add(table)

        # CREATE TABLE
        for match in CREATE_TABLE_PATTERN.finditer(statement):
            table = self._clean_table_name(match.group(1))
            if table:
                tables.add(table)

        return list(tables)

    def _clean_table_name(self, table: str) -> str:
        """
        Clean table name (remove quotes, brackets).

        Args:
            table: Raw table name

        Returns:
            Cleaned table name
        """
        # Remove quotes and brackets
        table = table.strip('`"\'"[]')
        return table


# ==============================================================================
# Standalone Functions
# ==============================================================================

def parse_sql_file(file_path: Path) -> Dict[str, Any]:
    """
    Parse a SQL file (convenience function).

    Args:
        file_path: Path to SQL file

    Returns:
        Dictionary with parsed elements
    """
    parser = SQLParser()
    return parser.parse_file(file_path)


def extract_statements(file_path: Path) -> List[str]:
    """
    Extract SQL statements (convenience function).

    Args:
        file_path: Path to SQL file

    Returns:
        List of SQL statements
    """
    parser = SQLParser()
    return parser.extract_statements(file_path)


def extract_tables(file_path: Path) -> List[str]:
    """
    Extract table names (convenience function).

    Args:
        file_path: Path to SQL file

    Returns:
        List of table names
    """
    parser = SQLParser()
    return parser.extract_tables(file_path)


def extract_statement_types(file_path: Path) -> Dict[str, int]:
    """
    Extract statement types (convenience function).

    Args:
        file_path: Path to SQL file

    Returns:
        Dictionary of statement type -> count
    """
    parser = SQLParser()
    return parser.extract_statement_types(file_path)
