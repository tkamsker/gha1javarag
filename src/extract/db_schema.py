"""
Database schema extraction from SQL files and DDL statements.
"""
import os
import json
import logging
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
import sqlparse
from sqlparse.sql import Statement, TokenList, Token

from config.settings import settings

logger = logging.getLogger(__name__)

class DatabaseSchemaExtractor:
    """Extracts database schema information from SQL files."""
    
    def __init__(self):
        """Initialize database schema extractor."""
        self.output_dir = settings.build_dir / "db_schema"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_database_schema(self, sql_files: List[str]) -> List[Dict[str, Any]]:
        """Extract database schema from SQL files."""
        tables = []
        
        for sql_file in sql_files:
            try:
                logger.info(f"Processing SQL file: {sql_file}")
                file_tables = self._extract_from_single_sql(sql_file)
                tables.extend(file_tables)
                
            except Exception as e:
                logger.error(f"Failed to process SQL file {sql_file}: {e}")
                continue
        
        # Save all tables JSON
        self._save_all_tables_json(tables)
        
        logger.info(f"Extracted {len(tables)} database tables")
        return tables
    
    def _extract_from_single_sql(self, sql_file: str) -> List[Dict[str, Any]]:
        """Extract schema from a single SQL file."""
        tables = []
        
        try:
            with open(sql_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse SQL statements
            statements = sqlparse.parse(content)
            
            for statement in statements:
                if self._is_create_table_statement(statement):
                    table = self._extract_table_from_statement(statement, sql_file)
                    if table:
                        tables.append(table)
                        
                        # Save individual table JSON
                        self._save_table_json(table)
            
        except Exception as e:
            logger.error(f"Failed to extract schema from SQL file {sql_file}: {e}")
        
        return tables
    
    def _is_create_table_statement(self, statement: Statement) -> bool:
        """Check if statement is a CREATE TABLE statement."""
        statement_str = str(statement).upper().strip()
        return statement_str.startswith('CREATE TABLE')
    
    def _extract_table_from_statement(self, statement: Statement, sql_file: str) -> Optional[Dict[str, Any]]:
        """Extract table information from CREATE TABLE statement."""
        try:
            statement_str = str(statement)
            
            # Extract table name
            table_name = self._extract_table_name(statement_str)
            if not table_name:
                return None
            
            # Extract columns
            columns = self._extract_columns(statement_str)
            
            # Extract constraints
            constraints = self._extract_constraints(statement_str)
            
            # Extract indexes
            indexes = self._extract_indexes(statement_str)
            
            # Create table artifact
            table = {
                'project': self._get_project_name(sql_file),
                'path': sql_file,
                'lineStart': 1,  # Would need to track line numbers
                'lineEnd': len(statement_str.splitlines()),
                'text': f"[DB Table] {table_name}",
                'meta': {
                    'fileName': Path(sql_file).name,
                    'statementType': 'CREATE TABLE'
                },
                'tableName': table_name,
                'columns': columns,
                'constraints': constraints,
                'indexes': indexes
            }
            
            return table
            
        except Exception as e:
            logger.error(f"Failed to extract table from statement: {e}")
            return None
    
    def _extract_table_name(self, statement_str: str) -> Optional[str]:
        """Extract table name from CREATE TABLE statement."""
        # Look for CREATE TABLE table_name pattern
        match = re.search(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(?:`)?(\w+)(?:`)?', statement_str, re.IGNORECASE)
        if match:
            return match.group(1)
        return None
    
    def _extract_columns(self, statement_str: str) -> List[Dict[str, Any]]:
        """Extract column definitions from CREATE TABLE statement."""
        columns = []
        
        # Find the column definitions between parentheses
        column_match = re.search(r'\(\s*(.*?)\s*\)', statement_str, re.DOTALL)
        if not column_match:
            return columns
        
        column_definitions = column_match.group(1)
        
        # Split by comma, but be careful about commas inside parentheses
        column_parts = self._split_column_definitions(column_definitions)
        
        for part in column_parts:
            part = part.strip()
            if part and not part.upper().startswith(('PRIMARY KEY', 'FOREIGN KEY', 'UNIQUE', 'INDEX', 'KEY')):
                column = self._parse_column_definition(part)
                if column:
                    columns.append(column)
        
        return columns
    
    def _split_column_definitions(self, column_definitions: str) -> List[str]:
        """Split column definitions by comma, respecting parentheses."""
        parts = []
        current_part = ""
        paren_count = 0
        
        for char in column_definitions:
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
            elif char == ',' and paren_count == 0:
                parts.append(current_part.strip())
                current_part = ""
                continue
            
            current_part += char
        
        if current_part.strip():
            parts.append(current_part.strip())
        
        return parts
    
    def _parse_column_definition(self, column_def: str) -> Optional[Dict[str, Any]]:
        """Parse a single column definition."""
        try:
            # Split by whitespace
            parts = column_def.split()
            if not parts:
                return None
            
            column_name = parts[0].strip('`"\'')
            column_type = parts[1] if len(parts) > 1 else 'VARCHAR'
            
            # Extract additional attributes
            attributes = {
                'name': column_name,
                'type': column_type,
                'nullable': True,
                'default': None,
                'auto_increment': False,
                'primary_key': False,
                'unique': False
            }
            
            # Check for additional attributes
            column_def_upper = column_def.upper()
            
            if 'NOT NULL' in column_def_upper:
                attributes['nullable'] = False
            
            if 'AUTO_INCREMENT' in column_def_upper:
                attributes['auto_increment'] = True
            
            if 'PRIMARY KEY' in column_def_upper:
                attributes['primary_key'] = True
            
            if 'UNIQUE' in column_def_upper:
                attributes['unique'] = True
            
            # Extract default value
            default_match = re.search(r'DEFAULT\s+([^\s,]+)', column_def_upper)
            if default_match:
                attributes['default'] = default_match.group(1)
            
            return attributes
            
        except Exception as e:
            logger.error(f"Failed to parse column definition '{column_def}': {e}")
            return None
    
    def _extract_constraints(self, statement_str: str) -> List[Dict[str, Any]]:
        """Extract constraints from CREATE TABLE statement."""
        constraints = []
        
        # Extract PRIMARY KEY constraints
        pk_matches = re.finditer(r'PRIMARY\s+KEY\s*\([^)]+\)', statement_str, re.IGNORECASE)
        for match in pk_matches:
            constraint_def = match.group(0)
            columns = self._extract_constraint_columns(constraint_def)
            constraints.append({
                'type': 'PRIMARY KEY',
                'columns': columns,
                'definition': constraint_def
            })
        
        # Extract FOREIGN KEY constraints
        fk_matches = re.finditer(r'FOREIGN\s+KEY\s*\([^)]+\)\s*REFERENCES\s+\w+\s*\([^)]+\)', statement_str, re.IGNORECASE)
        for match in fk_matches:
            constraint_def = match.group(0)
            columns = self._extract_constraint_columns(constraint_def)
            referenced_table = self._extract_referenced_table(constraint_def)
            constraints.append({
                'type': 'FOREIGN KEY',
                'columns': columns,
                'referencedTable': referenced_table,
                'definition': constraint_def
            })
        
        # Extract UNIQUE constraints
        unique_matches = re.finditer(r'UNIQUE\s*\([^)]+\)', statement_str, re.IGNORECASE)
        for match in unique_matches:
            constraint_def = match.group(0)
            columns = self._extract_constraint_columns(constraint_def)
            constraints.append({
                'type': 'UNIQUE',
                'columns': columns,
                'definition': constraint_def
            })
        
        return constraints
    
    def _extract_constraint_columns(self, constraint_def: str) -> List[str]:
        """Extract column names from constraint definition."""
        # Find content between parentheses
        match = re.search(r'\(([^)]+)\)', constraint_def)
        if match:
            columns_str = match.group(1)
            # Split by comma and clean up
            columns = [col.strip().strip('`"\'') for col in columns_str.split(',')]
            return columns
        return []
    
    def _extract_referenced_table(self, constraint_def: str) -> Optional[str]:
        """Extract referenced table name from FOREIGN KEY constraint."""
        match = re.search(r'REFERENCES\s+(\w+)', constraint_def, re.IGNORECASE)
        if match:
            return match.group(1)
        return None
    
    def _extract_indexes(self, statement_str: str) -> List[Dict[str, Any]]:
        """Extract indexes from CREATE TABLE statement."""
        indexes = []
        
        # Look for INDEX definitions
        index_matches = re.finditer(r'(?:KEY|INDEX)\s+(\w+)?\s*\([^)]+\)', statement_str, re.IGNORECASE)
        for match in index_matches:
            index_def = match.group(0)
            index_name = match.group(1) if match.group(1) else 'unnamed'
            columns = self._extract_constraint_columns(index_def)
            
            indexes.append({
                'name': index_name,
                'columns': columns,
                'definition': index_def
            })
        
        return indexes
    
    def _get_project_name(self, file_path: str) -> str:
        """Extract project name from file path."""
        path_parts = Path(file_path).parts
        
        for part in path_parts:
            if part in ['src', 'main', 'java', 'webapp', 'resources', 'sql', 'database', 'schema']:
                continue
            if '.' in part and len(part) > 3:
                return part.split('.')[0]
            if part and not part.startswith('.') and len(part) > 2:
                return part
        
        return settings.default_project_name
    
    def _save_table_json(self, table: Dict[str, Any]):
        """Save individual table as JSON."""
        table_name = table.get('tableName', 'unknown')
        safe_name = table_name.replace('.', '_').replace('/', '_')
        output_file = self.output_dir / f"{safe_name}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(table, f, indent=2, ensure_ascii=False)
    
    def _save_all_tables_json(self, tables: List[Dict[str, Any]]):
        """Save all tables as a single JSON file."""
        output_file = self.output_dir / "all_tables.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(tables, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(tables)} database tables to {output_file}")
