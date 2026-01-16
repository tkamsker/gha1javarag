"""
Unit tests for ERD (Entity-Relationship Diagram) generation (T071).

Tests Mermaid ER diagram syntax generation, table/column extraction, and
foreign key relationship formatting.
"""

import pytest
from typing import List, Dict, Any


class TestErdGenerator:
    """Test suite for ERD generation service."""

    @pytest.fixture
    def sample_tables(self) -> List[Dict[str, Any]]:
        """Create sample database tables for testing."""
        return [
            {
                "id": "table_users",
                "artifactType": "DbTable",
                "fileName": "users.sql",
                "relativePath": "schema/users.sql",
                "entities": ["users", "user_id", "email", "username", "created_at"],
                "summary": "User accounts table",
                "metadata": {
                    "columns": [
                        {"name": "user_id", "type": "INT", "primary_key": True},
                        {"name": "email", "type": "VARCHAR(255)", "nullable": False},
                        {"name": "username", "type": "VARCHAR(100)", "nullable": False},
                        {"name": "created_at", "type": "TIMESTAMP", "nullable": True}
                    ],
                    "primary_key": "user_id"
                }
            },
            {
                "id": "table_orders",
                "artifactType": "DbTable",
                "fileName": "orders.sql",
                "relativePath": "schema/orders.sql",
                "entities": ["orders", "order_id", "user_id", "total_amount"],
                "summary": "Customer orders table",
                "metadata": {
                    "columns": [
                        {"name": "order_id", "type": "INT", "primary_key": True},
                        {"name": "user_id", "type": "INT", "foreign_key": {"table": "users", "column": "user_id"}},
                        {"name": "total_amount", "type": "DECIMAL(10,2)", "nullable": False}
                    ],
                    "primary_key": "order_id",
                    "foreign_keys": [
                        {"column": "user_id", "references_table": "users", "references_column": "user_id"}
                    ]
                }
            },
            {
                "id": "table_products",
                "artifactType": "DbTable",
                "fileName": "products.sql",
                "relativePath": "schema/products.sql",
                "entities": ["products", "product_id", "name", "price"],
                "summary": "Product catalog table",
                "metadata": {
                    "columns": [
                        {"name": "product_id", "type": "INT", "primary_key": True},
                        {"name": "name", "type": "VARCHAR(200)", "nullable": False},
                        {"name": "price", "type": "DECIMAL(10,2)", "nullable": False}
                    ],
                    "primary_key": "product_id"
                }
            }
        ]

    def test_generate_mermaid_erd_basic(self, sample_tables):
        """Test basic Mermaid ERD generation."""
        from codeindex.web.services.erd_generator import ErdGenerator

        erd_gen = ErdGenerator()
        mermaid_diagram = erd_gen.generate_mermaid_erd(sample_tables)

        # Verify Mermaid syntax
        assert mermaid_diagram.startswith("erDiagram")
        assert "users" in mermaid_diagram
        assert "orders" in mermaid_diagram
        assert "products" in mermaid_diagram

    def test_generate_table_definitions(self, sample_tables):
        """Test table definition generation."""
        from codeindex.web.services.erd_generator import ErdGenerator

        erd_gen = ErdGenerator()
        mermaid_diagram = erd_gen.generate_mermaid_erd(sample_tables)

        # Verify table structure
        assert "users {" in mermaid_diagram
        assert "INT user_id PK" in mermaid_diagram or "user_id INT PK" in mermaid_diagram
        assert "VARCHAR(255) email" in mermaid_diagram or "email VARCHAR" in mermaid_diagram

    def test_generate_foreign_key_relationships(self, sample_tables):
        """Test foreign key relationship generation."""
        from codeindex.web.services.erd_generator import ErdGenerator

        erd_gen = ErdGenerator()
        mermaid_diagram = erd_gen.generate_mermaid_erd(sample_tables)

        # Verify FK relationships (Mermaid uses ||--o{, }o--||, etc.)
        assert "users ||--o{ orders" in mermaid_diagram or "orders }o--|| users" in mermaid_diagram

    def test_generate_column_types(self, sample_tables):
        """Test column type extraction."""
        from codeindex.web.services.erd_generator import ErdGenerator

        erd_gen = ErdGenerator()
        mermaid_diagram = erd_gen.generate_mermaid_erd(sample_tables)

        # Verify data types are included
        assert "INT" in mermaid_diagram
        assert "VARCHAR" in mermaid_diagram or "VARCHAR(255)" in mermaid_diagram
        assert "DECIMAL" in mermaid_diagram or "DECIMAL(10,2)" in mermaid_diagram

    def test_handle_empty_schema(self):
        """Test handling of empty schema."""
        from codeindex.web.services.erd_generator import ErdGenerator

        erd_gen = ErdGenerator()
        mermaid_diagram = erd_gen.generate_mermaid_erd([])

        # Should return valid but empty ERD
        assert mermaid_diagram.startswith("erDiagram")
        assert len(mermaid_diagram.split("\n")) <= 3  # Just header and maybe comment

    def test_handle_table_without_foreign_keys(self):
        """Test table with no foreign keys."""
        from codeindex.web.services.erd_generator import ErdGenerator

        tables = [
            {
                "id": "table_logs",
                "artifactType": "DbTable",
                "fileName": "logs.sql",
                "entities": ["logs", "log_id", "message"],
                "metadata": {
                    "columns": [
                        {"name": "log_id", "type": "INT", "primary_key": True},
                        {"name": "message", "type": "TEXT"}
                    ],
                    "primary_key": "log_id"
                }
            }
        ]

        erd_gen = ErdGenerator()
        mermaid_diagram = erd_gen.generate_mermaid_erd(tables)

        # Should generate table without relationships
        assert "logs {" in mermaid_diagram
        assert "log_id" in mermaid_diagram
        assert "message" in mermaid_diagram

    def test_extract_columns_from_metadata(self, sample_tables):
        """Test column extraction from artifact metadata."""
        from codeindex.web.services.erd_generator import ErdGenerator

        erd_gen = ErdGenerator()
        users_table = sample_tables[0]

        columns = erd_gen._extract_columns(users_table)

        assert len(columns) == 4
        assert any(col["name"] == "user_id" for col in columns)
        assert any(col["name"] == "email" for col in columns)

    def test_extract_columns_from_entities_fallback(self):
        """Test column extraction fallback from entities field."""
        from codeindex.web.services.erd_generator import ErdGenerator

        table_without_metadata = {
            "id": "table_simple",
            "artifactType": "DbTable",
            "fileName": "simple.sql",
            "entities": ["simple", "id", "name", "value"]
        }

        erd_gen = ErdGenerator()
        columns = erd_gen._extract_columns(table_without_metadata)

        # Should extract from entities field
        assert len(columns) > 0
        assert any(col["name"] == "id" for col in columns)

    def test_format_column_definition(self):
        """Test column definition formatting."""
        from codeindex.web.services.erd_generator import ErdGenerator

        erd_gen = ErdGenerator()

        # Test primary key formatting
        pk_column = {"name": "user_id", "type": "INT", "primary_key": True}
        pk_def = erd_gen._format_column(pk_column)
        assert "PK" in pk_def or "PRIMARY KEY" in pk_def

        # Test foreign key formatting
        fk_column = {"name": "user_id", "type": "INT", "foreign_key": True}
        fk_def = erd_gen._format_column(fk_column)
        assert "FK" in fk_def or "FOREIGN KEY" in fk_def

    def test_extract_foreign_keys(self, sample_tables):
        """Test foreign key extraction."""
        from codeindex.web.services.erd_generator import ErdGenerator

        erd_gen = ErdGenerator()
        orders_table = sample_tables[1]

        fks = erd_gen._extract_foreign_keys(orders_table)

        assert len(fks) > 0
        assert any(fk["references_table"] == "users" for fk in fks)

    def test_mermaid_relationship_syntax(self):
        """Test Mermaid relationship syntax generation."""
        from codeindex.web.services.erd_generator import ErdGenerator

        erd_gen = ErdGenerator()

        # Test one-to-many relationship
        relationship = erd_gen._format_relationship(
            from_table="users",
            to_table="orders",
            relationship_type="one-to-many"
        )

        # Should use Mermaid ERD relationship syntax
        assert "||--o{" in relationship or "}o--||" in relationship

    def test_handle_circular_relationships(self):
        """Test handling of circular relationships (e.g., self-referencing)."""
        from codeindex.web.services.erd_generator import ErdGenerator

        tables = [
            {
                "id": "table_employees",
                "artifactType": "DbTable",
                "fileName": "employees.sql",
                "entities": ["employees", "employee_id", "manager_id"],
                "metadata": {
                    "columns": [
                        {"name": "employee_id", "type": "INT", "primary_key": True},
                        {"name": "manager_id", "type": "INT", "foreign_key": {"table": "employees", "column": "employee_id"}}
                    ],
                    "foreign_keys": [
                        {"column": "manager_id", "references_table": "employees", "references_column": "employee_id"}
                    ]
                }
            }
        ]

        erd_gen = ErdGenerator()
        mermaid_diagram = erd_gen.generate_mermaid_erd(tables)

        # Should handle self-referencing FK without errors
        assert "employees" in mermaid_diagram
        assert "manager_id" in mermaid_diagram

    def test_table_name_sanitization(self):
        """Test that table names are sanitized for Mermaid."""
        from codeindex.web.services.erd_generator import ErdGenerator

        tables = [
            {
                "id": "table_test",
                "artifactType": "DbTable",
                "fileName": "user-accounts.sql",  # Hyphen should be handled
                "entities": ["user-accounts", "id"],
                "metadata": {
                    "columns": [{"name": "id", "type": "INT", "primary_key": True}]
                }
            }
        ]

        erd_gen = ErdGenerator()
        mermaid_diagram = erd_gen.generate_mermaid_erd(tables)

        # Should not break Mermaid syntax
        assert "erDiagram" in mermaid_diagram

    def test_get_table_name(self, sample_tables):
        """Test table name extraction."""
        from codeindex.web.services.erd_generator import ErdGenerator

        erd_gen = ErdGenerator()
        users_table = sample_tables[0]

        table_name = erd_gen._get_table_name(users_table)

        assert table_name == "users"

    def test_generate_with_indexes(self):
        """Test ERD generation with index information."""
        from codeindex.web.services.erd_generator import ErdGenerator

        tables = [
            {
                "id": "table_users",
                "artifactType": "DbTable",
                "fileName": "users.sql",
                "entities": ["users", "user_id", "email"],
                "metadata": {
                    "columns": [
                        {"name": "user_id", "type": "INT", "primary_key": True},
                        {"name": "email", "type": "VARCHAR(255)", "indexed": True}
                    ],
                    "indexes": [
                        {"column": "email", "type": "UNIQUE"}
                    ]
                }
            }
        ]

        erd_gen = ErdGenerator()
        mermaid_diagram = erd_gen.generate_mermaid_erd(tables)

        # Should include index information in comments or column definitions
        assert "users" in mermaid_diagram
        assert "email" in mermaid_diagram

    def test_singleton_pattern(self):
        """Test global ERD generator singleton."""
        from codeindex.web.services.erd_generator import get_erd_generator

        gen1 = get_erd_generator()
        gen2 = get_erd_generator()

        assert gen1 is gen2
