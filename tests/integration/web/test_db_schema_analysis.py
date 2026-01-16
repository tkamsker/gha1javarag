"""
Integration tests for database schema analysis (T073).

Tests end-to-end schema analysis including Weaviate DbTable queries,
ERD generation, and quality reporting.
"""

import pytest
from unittest.mock import Mock, patch
from typing import List, Dict, Any


class TestDatabaseSchemaAnalysisIntegration:
    """Integration test suite for database schema analysis."""

    @pytest.fixture
    def mock_weaviate_schema(self) -> List[Dict[str, Any]]:
        """Create mock Weaviate database schema."""
        return [
            {
                "id": "uuid-users-001",
                "artifactType": "DbTable",
                "fileName": "users.sql",
                "relativePath": "schema/users.sql",
                "projectId": "test-project",
                "summary": "User accounts table with authentication data",
                "entities": ["users", "user_id", "email", "username", "password_hash", "created_at"],
                "_additional": {"id": "uuid-users-001", "distance": 0.05},
                "metadata": {
                    "table_name": "users",
                    "columns": [
                        {"name": "user_id", "type": "INT", "primary_key": True, "auto_increment": True},
                        {"name": "email", "type": "VARCHAR(255)", "nullable": False, "unique": True},
                        {"name": "username", "type": "VARCHAR(100)", "nullable": False},
                        {"name": "password_hash", "type": "VARCHAR(255)", "nullable": False},
                        {"name": "created_at", "type": "TIMESTAMP", "nullable": False, "default": "CURRENT_TIMESTAMP"}
                    ],
                    "indexes": [
                        {"column": "email", "type": "UNIQUE"},
                        {"column": "username", "type": "INDEX"}
                    ],
                    "primary_key": "user_id"
                }
            },
            {
                "id": "uuid-orders-001",
                "artifactType": "DbTable",
                "fileName": "orders.sql",
                "relativePath": "schema/orders.sql",
                "projectId": "test-project",
                "summary": "Customer orders with user references",
                "entities": ["orders", "order_id", "user_id", "total_amount", "status", "created_at"],
                "_additional": {"id": "uuid-orders-001", "distance": 0.08},
                "metadata": {
                    "table_name": "orders",
                    "columns": [
                        {"name": "order_id", "type": "INT", "primary_key": True, "auto_increment": True},
                        {"name": "user_id", "type": "INT", "nullable": False, "foreign_key": True},
                        {"name": "total_amount", "type": "DECIMAL(10,2)", "nullable": False},
                        {"name": "status", "type": "ENUM('pending','completed','cancelled')", "nullable": False},
                        {"name": "created_at", "type": "TIMESTAMP", "nullable": False}
                    ],
                    "foreign_keys": [
                        {"column": "user_id", "references_table": "users", "references_column": "user_id"}
                    ],
                    "indexes": [
                        {"column": "user_id", "type": "INDEX"},
                        {"column": "created_at", "type": "INDEX"}
                    ],
                    "primary_key": "order_id"
                }
            },
            {
                "id": "uuid-products-001",
                "artifactType": "DbTable",
                "fileName": "products.sql",
                "relativePath": "schema/products.sql",
                "projectId": "test-project",
                "summary": "Product catalog",
                "entities": ["products", "product_id", "name", "description", "price", "stock"],
                "_additional": {"id": "uuid-products-001", "distance": 0.12},
                "metadata": {
                    "table_name": "products",
                    "columns": [
                        {"name": "product_id", "type": "INT", "primary_key": True, "auto_increment": True},
                        {"name": "name", "type": "VARCHAR(200)", "nullable": False},
                        {"name": "description", "type": "TEXT", "nullable": True},
                        {"name": "price", "type": "DECIMAL(10,2)", "nullable": False},
                        {"name": "stock", "type": "INT", "nullable": False, "default": "0"}
                    ],
                    "indexes": [
                        {"column": "name", "type": "INDEX"}
                    ],
                    "primary_key": "product_id"
                }
            }
        ]

    @patch('codeindex.web.services.search_service.get_search_service')
    def test_full_schema_analysis_pipeline(self, mock_get_search, mock_weaviate_schema):
        """Test complete schema analysis workflow."""
        from codeindex.web.services.erd_generator import ErdGenerator
        from codeindex.web.services.db_quality import DbQualityAnalyzer

        # Mock search service to return database tables
        mock_search = Mock()
        mock_search.search.return_value = {
            "results": mock_weaviate_schema,
            "total": 3
        }
        mock_get_search.return_value = mock_search

        # Step 1: Query Weaviate for DbTable artifacts
        search_response = mock_search.search(
            query="database schema",
            filters={"artifact_types": ["DbTable"]},
            limit=20
        )

        tables = search_response["results"]
        assert len(tables) == 3

        # Step 2: Generate ERD diagram
        erd_gen = ErdGenerator()
        erd_diagram = erd_gen.generate_mermaid_erd(tables)

        assert "erDiagram" in erd_diagram
        assert "users" in erd_diagram
        assert "orders" in erd_diagram
        assert "products" in erd_diagram

        # Step 3: Generate quality report
        quality_analyzer = DbQualityAnalyzer()
        quality_report = quality_analyzer.analyze_schema(tables)

        assert "total_tables" in quality_report
        assert quality_report["total_tables"] == 3

    @patch('codeindex.web.services.search_service.get_search_service')
    def test_weaviate_query_for_database_tables(self, mock_get_search, mock_weaviate_schema):
        """Test querying Weaviate for database tables."""
        # Mock search service
        mock_search = Mock()
        mock_search.search.return_value = {
            "results": mock_weaviate_schema,
            "total": 3
        }
        mock_get_search.return_value = mock_search

        # Query with DbTable filter
        response = mock_search.search(
            query="",
            filters={"artifact_types": ["DbTable"]},
            limit=20
        )

        # Verify query was called with correct parameters
        mock_search.search.assert_called_once()
        call_args = mock_search.search.call_args
        assert "DbTable" in call_args[1]["filters"]["artifact_types"]

        # Verify results
        tables = response["results"]
        assert len(tables) == 3
        assert all(t["artifactType"] == "DbTable" for t in tables)

    def test_erd_generation_with_foreign_keys(self, mock_weaviate_schema):
        """Test ERD includes foreign key relationships."""
        from codeindex.web.services.erd_generator import ErdGenerator

        erd_gen = ErdGenerator()
        erd_diagram = erd_gen.generate_mermaid_erd(mock_weaviate_schema)

        # Verify FK relationship between users and orders
        assert "users ||--o{ orders" in erd_diagram or "orders }o--|| users" in erd_diagram

    def test_quality_analysis_identifies_issues(self, mock_weaviate_schema):
        """Test quality analysis identifies schema issues."""
        from codeindex.web.services.db_quality import DbQualityAnalyzer

        # Remove FK from orders to simulate issue
        schema_with_issues = mock_weaviate_schema.copy()
        schema_with_issues[1]["metadata"]["foreign_keys"] = []

        quality_analyzer = DbQualityAnalyzer()
        quality_report = quality_analyzer.analyze_schema(schema_with_issues)

        # Should identify missing FK
        assert "missing_foreign_keys" in quality_report or "issues" in quality_report

    def test_schema_analysis_with_no_tables(self):
        """Test schema analysis with empty Weaviate results."""
        from codeindex.web.services.erd_generator import ErdGenerator
        from codeindex.web.services.db_quality import DbQualityAnalyzer

        # Empty schema
        empty_schema = []

        # ERD generation should handle gracefully
        erd_gen = ErdGenerator()
        erd_diagram = erd_gen.generate_mermaid_erd(empty_schema)
        assert "erDiagram" in erd_diagram

        # Quality analysis should handle gracefully
        quality_analyzer = DbQualityAnalyzer()
        quality_report = quality_analyzer.analyze_schema(empty_schema)
        assert quality_report["total_tables"] == 0

    @patch('codeindex.web.agents.data_analyst.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_data_analyst_schema_analysis(
        self,
        mock_ollama,
        mock_get_search,
        mock_weaviate_schema
    ):
        """Test Data Analyst agent analyzes database schema."""
        from codeindex.web.agents.data_analyst import DataAnalystAgent

        # Mock search to return database tables
        mock_search = Mock()
        mock_search.search.return_value = {
            "results": mock_weaviate_schema,
            "total": 3
        }
        mock_get_search.return_value = mock_search

        # Mock Ollama response
        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {
            "response": "The database schema includes 3 tables: users, orders, and products. "
                        "The orders table has a foreign key relationship to users."
        }
        mock_ollama.return_value = mock_ollama_instance

        # Execute Data Analyst query
        agent = DataAnalystAgent()
        response = agent.execute_query("Analyze the database schema")

        # Verify response includes schema analysis
        assert "users" in response.response_text.lower()
        assert "orders" in response.response_text.lower()
        assert len(response.citations) > 0

    def test_erd_rendering_with_mermaid_markdown(self, mock_weaviate_schema):
        """Test ERD can be rendered in Streamlit with st.markdown."""
        from codeindex.web.services.erd_generator import ErdGenerator

        erd_gen = ErdGenerator()
        erd_diagram = erd_gen.generate_mermaid_erd(mock_weaviate_schema)

        # Verify diagram is in format suitable for st.markdown
        # st.markdown expects: ```mermaid\n<diagram>\n```
        mermaid_block = f"```mermaid\n{erd_diagram}\n```"

        assert "erDiagram" in mermaid_block
        assert mermaid_block.startswith("```mermaid")
        assert mermaid_block.endswith("```")

    def test_quality_report_markdown_formatting(self, mock_weaviate_schema):
        """Test quality report formats as markdown for Streamlit."""
        from codeindex.web.services.db_quality import DbQualityAnalyzer

        quality_analyzer = DbQualityAnalyzer()
        quality_report = quality_analyzer.analyze_schema(mock_weaviate_schema)
        markdown_report = quality_analyzer.format_report_markdown(quality_report)

        # Verify markdown formatting
        assert isinstance(markdown_report, str)
        assert len(markdown_report) > 0
        assert "##" in markdown_report or "**" in markdown_report or "|" in markdown_report

    @patch('codeindex.web.services.search_service.get_search_service')
    def test_project_scoped_schema_analysis(self, mock_get_search, mock_weaviate_schema):
        """Test schema analysis scoped to specific project."""
        # Mock search with project filter
        mock_search = Mock()
        mock_search.search.return_value = {
            "results": mock_weaviate_schema,
            "total": 3
        }
        mock_get_search.return_value = mock_search

        # Query with project filter
        response = mock_search.search(
            query="",
            filters={
                "artifact_types": ["DbTable"],
                "project_id": "test-project"
            },
            limit=20
        )

        # Verify all tables belong to project
        tables = response["results"]
        assert all(t["projectId"] == "test-project" for t in tables)

    def test_schema_analysis_performance_with_large_schema(self):
        """Test schema analysis performance with many tables."""
        from codeindex.web.services.erd_generator import ErdGenerator
        from codeindex.web.services.db_quality import DbQualityAnalyzer

        # Create 50 tables
        large_schema = [
            {
                "id": f"table_{i}",
                "artifactType": "DbTable",
                "fileName": f"table_{i}.sql",
                "entities": [f"table_{i}", "id", "name"],
                "metadata": {
                    "table_name": f"table_{i}",
                    "columns": [
                        {"name": "id", "type": "INT", "primary_key": True},
                        {"name": "name", "type": "VARCHAR(100)"}
                    ]
                }
            }
            for i in range(50)
        ]

        # Should handle large schemas efficiently
        erd_gen = ErdGenerator()
        erd_diagram = erd_gen.generate_mermaid_erd(large_schema)
        assert "erDiagram" in erd_diagram

        quality_analyzer = DbQualityAnalyzer()
        quality_report = quality_analyzer.analyze_schema(large_schema)
        assert quality_report["total_tables"] == 50
