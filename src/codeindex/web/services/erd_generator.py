"""
ERD (Entity-Relationship Diagram) generator for database schema visualization.

Generates Mermaid ER diagrams from database table artifacts extracted from Weaviate.
"""

import logging
import re
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class ErdGenerator:
    """
    Generator for Entity-Relationship Diagrams in Mermaid format.

    Features:
    - Converts database table artifacts to Mermaid ER syntax
    - Extracts columns, types, primary keys, foreign keys
    - Formats relationships between tables
    - Handles edge cases (empty schema, circular dependencies)
    """

    def generate_mermaid_erd(self, tables: List[Dict[str, Any]]) -> str:
        """
        Generate Mermaid ER diagram from database tables.

        Args:
            tables: List of database table artifacts

        Returns:
            Mermaid ER diagram syntax as string
        """
        if not tables:
            logger.info("No tables provided for ERD generation")
            return "erDiagram\n    %% No tables found"

        logger.info(f"Generating ERD for {len(tables)} tables")

        diagram_lines = ["erDiagram"]

        # Track processed relationships to avoid duplicates
        processed_relationships = set()

        # Generate table definitions
        for table in tables:
            table_name = self._get_table_name(table)
            table_name_safe = self._sanitize_name(table_name)

            # Add table definition
            diagram_lines.append(f"    {table_name_safe} {{")

            # Extract and format columns
            columns = self._extract_columns(table)
            for column in columns:
                column_def = self._format_column(column)
                diagram_lines.append(f"        {column_def}")

            diagram_lines.append("    }")

        # Generate relationships (foreign keys)
        for table in tables:
            table_name = self._get_table_name(table)
            table_name_safe = self._sanitize_name(table_name)

            foreign_keys = self._extract_foreign_keys(table)
            for fk in foreign_keys:
                ref_table = fk.get("references_table", "")
                ref_table_safe = self._sanitize_name(ref_table)

                # Create unique key for this relationship
                rel_key = tuple(sorted([table_name_safe, ref_table_safe]))

                if rel_key not in processed_relationships and ref_table:
                    # Format relationship (many-to-one from current table to referenced table)
                    relationship = self._format_relationship(
                        from_table=table_name_safe,
                        to_table=ref_table_safe,
                        relationship_type="many-to-one"
                    )
                    diagram_lines.append(f"    {relationship}")
                    processed_relationships.add(rel_key)

        result = "\n".join(diagram_lines)
        logger.info(f"Generated ERD with {len(tables)} tables and {len(processed_relationships)} relationships")

        return result

    def _get_table_name(self, table: Dict[str, Any]) -> str:
        """
        Extract table name from artifact.

        Args:
            table: Table artifact

        Returns:
            Table name
        """
        # Try metadata first
        if "metadata" in table and "table_name" in table["metadata"]:
            return table["metadata"]["table_name"]

        # Try entities field (first entity is usually table name)
        if "entities" in table and len(table["entities"]) > 0:
            return table["entities"][0]

        # Fallback to filename without extension
        filename = table.get("fileName", "unknown")
        return filename.replace(".sql", "").replace(".SQL", "")

    def _sanitize_name(self, name: str) -> str:
        """
        Sanitize table/column name for Mermaid syntax.

        Args:
            name: Raw name

        Returns:
            Sanitized name safe for Mermaid
        """
        # Replace hyphens and spaces with underscores
        name = name.replace("-", "_").replace(" ", "_")

        # Remove special characters except underscores
        name = re.sub(r'[^\w]', '', name)

        return name

    def _extract_columns(self, table: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract columns from table artifact.

        Args:
            table: Table artifact

        Returns:
            List of column definitions
        """
        columns = []

        # Try metadata columns first
        if "metadata" in table and "columns" in table["metadata"]:
            return table["metadata"]["columns"]

        # Fallback: extract from entities field
        if "entities" in table:
            entities = table["entities"]
            # Skip first entity (table name)
            for entity in entities[1:]:
                columns.append({
                    "name": entity,
                    "type": "VARCHAR",  # Default type
                    "nullable": True
                })

        return columns

    def _format_column(self, column: Dict[str, Any]) -> str:
        """
        Format column definition for Mermaid ER syntax.

        Args:
            column: Column definition

        Returns:
            Formatted column string (e.g., "int user_id PK")
        """
        col_name = column.get("name", "unknown")
        col_type = column.get("type", "VARCHAR").upper()

        # Keep full type including length specifiers for detail
        # (e.g., VARCHAR(255) instead of just VARCHAR)

        # Add markers
        markers = []
        if column.get("primary_key"):
            markers.append("PK")
        elif column.get("foreign_key"):
            markers.append("FK")

        if column.get("unique"):
            markers.append("UK")

        # Format: type name [markers]
        parts = [col_type, col_name]
        if markers:
            parts.extend(markers)

        return " ".join(parts)

    def _extract_foreign_keys(self, table: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract foreign key relationships from table.

        Args:
            table: Table artifact

        Returns:
            List of foreign key definitions
        """
        foreign_keys = []

        # Try metadata foreign_keys first
        if "metadata" in table and "foreign_keys" in table["metadata"]:
            return table["metadata"]["foreign_keys"]

        # Fallback: Look for FK in column definitions
        if "metadata" in table and "columns" in table["metadata"]:
            columns = table["metadata"]["columns"]
            for col in columns:
                if col.get("foreign_key"):
                    fk_info = col.get("foreign_key")
                    if isinstance(fk_info, dict):
                        foreign_keys.append({
                            "column": col["name"],
                            "references_table": fk_info.get("table", ""),
                            "references_column": fk_info.get("column", "")
                        })
                    elif col["name"].endswith("_id"):
                        # Infer FK from naming convention
                        ref_table = col["name"][:-3]  # Remove _id suffix
                        foreign_keys.append({
                            "column": col["name"],
                            "references_table": ref_table,
                            "references_column": col["name"]
                        })

        return foreign_keys

    def _format_relationship(
        self,
        from_table: str,
        to_table: str,
        relationship_type: str = "many-to-one"
    ) -> str:
        """
        Format relationship in Mermaid ER syntax.

        Args:
            from_table: Source table name
            to_table: Target table name
            relationship_type: Type of relationship

        Returns:
            Formatted relationship string

        Mermaid relationship syntax:
        - ||--o{ : one to many
        - }o--|| : many to one
        - ||--|| : one to one
        - }o--o{ : many to many
        """
        # Map relationship types to Mermaid syntax
        if relationship_type == "one-to-many":
            return f"{from_table} ||--o{{ {to_table} : has"
        elif relationship_type == "many-to-one":
            return f"{from_table} }}o--|| {to_table} : references"
        elif relationship_type == "one-to-one":
            return f"{from_table} ||--|| {to_table} : links"
        elif relationship_type == "many-to-many":
            return f"{from_table} }}o--o{{ {to_table} : relates"
        else:
            # Default to many-to-one
            return f"{from_table} }}o--|| {to_table} : references"


# Global singleton instance
_erd_generator: Optional[ErdGenerator] = None


def get_erd_generator() -> ErdGenerator:
    """
    Get global ERD generator instance.

    Returns:
        ErdGenerator singleton
    """
    global _erd_generator

    if _erd_generator is None:
        _erd_generator = ErdGenerator()
        logger.info("Initialized ERD generator")

    return _erd_generator


__all__ = [
    "ErdGenerator",
    "get_erd_generator"
]
