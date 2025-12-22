"""
SQL file parser.

Extracts structural information from SQL files including:
- Statement types (SELECT, INSERT, UPDATE, CREATE, etc.)
- Table names
- Query patterns
- Foreign key relationships from JOIN statements
"""

import re
import logging
from pathlib import Path
from typing import Dict, List, Any

from codeindex.models.foreign_key import ForeignKeyRelationship, ForeignKeySource

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

    def extract_foreign_keys_from_joins(self, content: str) -> List[ForeignKeyRelationship]:
        """
        Extract foreign key relationships from SQL JOIN ON clauses.

        Implements Feature 007 US2 T041.

        Supports patterns:
        - INNER JOIN table2 ON table1.col1 = table2.col2
        - LEFT JOIN table2 ON table1.col1 = table2.col2
        - JOIN table2 t2 ON t1.col1 = t2.col2 (with aliases)
        - Complex conditions: ON (table1.col1 = table2.col2 AND ...)

        Args:
            content: SQL source code or statement

        Returns:
            List of ForeignKeyRelationship extracted from JOIN clauses
        """
        fk_relationships: List[ForeignKeyRelationship] = []

        # Remove comments first
        content = self._remove_comments(content)

        # Pattern: JOIN table_name [alias] ON table1.column1 = table2.column2
        # Supports: INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL JOIN, JOIN
        # Handles aliases and complex ON conditions with parentheses
        join_pattern = re.compile(
            r'\b(?:INNER\s+|LEFT\s+|RIGHT\s+|FULL\s+)?JOIN\s+'  # JOIN keyword
            r'([`"\[]?\w+[`"\]]?)\s*'  # Table name
            r'(?:(?:AS\s+)?(\w+)\s*)?'  # Optional alias
            r'ON\s+'  # ON keyword
            r'\(?\s*'  # Optional opening parenthesis
            r'([`"\[]?\w+[`"\]]?)\.([`"\[]?\w+[`"\]]?)'  # Left side: table.column
            r'\s*=\s*'  # Equals sign
            r'([`"\[]?\w+[`"\]]?)\.([`"\[]?\w+[`"\]]?)'  # Right side: table.column
            r'\s*\)?',  # Optional closing parenthesis
            re.IGNORECASE
        )

        for match in join_pattern.finditer(content):
            joined_table = self._clean_table_name(match.group(1))
            table_alias = match.group(2)  # May be None
            left_table = self._clean_table_name(match.group(3))
            left_column = self._clean_table_name(match.group(4))
            right_table = self._clean_table_name(match.group(5))
            right_column = self._clean_table_name(match.group(6))

            # Resolve aliases to actual table names
            # Build alias map from FROM and JOIN clauses
            alias_map = self._build_alias_map(content)

            # Resolve left table (might be alias)
            source_table = alias_map.get(left_table, left_table)
            target_table = alias_map.get(right_table, right_table)

            # Determine which table is the source (has the FK column)
            # Convention: The table being joined is typically the target (referenced table)
            # The table in the FROM clause or left side is typically the source
            #
            # Example: FROM orders o JOIN customers c ON o.customer_id = c.id
            # - orders is source (has FK customer_id)
            # - customers is target (has PK id)

            # Check if joined_table matches right_table or its alias
            if joined_table == right_table or joined_table == table_alias:
                # Standard case: joined table is on the right side of ON clause
                fk = ForeignKeyRelationship(
                    source_entity=source_table,
                    source_column=left_column,
                    target_entity=target_table,
                    target_column=right_column,
                    fk_source=ForeignKeySource.SQL
                )
            else:
                # Reversed case: joined table is on the left side
                fk = ForeignKeyRelationship(
                    source_entity=target_table,
                    source_column=right_column,
                    target_entity=source_table,
                    target_column=left_column,
                    fk_source=ForeignKeySource.SQL
                )

            fk_relationships.append(fk)
            logger.debug(
                f"Extracted SQL FK: {fk.source_entity}.{fk.source_column} -> "
                f"{fk.target_entity}.{fk.target_column}"
            )

        return fk_relationships

    def _build_alias_map(self, content: str) -> Dict[str, str]:
        """
        Build mapping of table aliases to actual table names.

        Args:
            content: SQL source code

        Returns:
            Dict mapping alias -> table_name
        """
        alias_map: Dict[str, str] = {}

        # Pattern: FROM table_name [AS] alias
        from_alias_pattern = re.compile(
            r'\bFROM\s+([`"\[]?\w+[`"\]]?)\s+(?:AS\s+)?(\w+)\b',
            re.IGNORECASE
        )

        for match in from_alias_pattern.finditer(content):
            table_name = self._clean_table_name(match.group(1))
            alias = match.group(2)
            alias_map[alias] = table_name

        # Pattern: JOIN table_name [AS] alias
        join_alias_pattern = re.compile(
            r'\bJOIN\s+([`"\[]?\w+[`"\]]?)\s+(?:AS\s+)?(\w+)\b',
            re.IGNORECASE
        )

        for match in join_alias_pattern.finditer(content):
            table_name = self._clean_table_name(match.group(1))
            alias = match.group(2)
            alias_map[alias] = table_name

        return alias_map


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
