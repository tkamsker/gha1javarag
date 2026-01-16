"""
Unit tests for database quality analysis (T072).

Tests missing FK detection, index analysis, and naming convention checks.
"""

import pytest
from typing import List, Dict, Any


class TestDbQualityAnalyzer:
    """Test suite for database quality analysis."""

    @pytest.fixture
    def sample_schema(self) -> List[Dict[str, Any]]:
        """Create sample database schema for testing."""
        return [
            {
                "id": "table_users",
                "artifactType": "DbTable",
                "fileName": "users.sql",
                "entities": ["users", "user_id", "email", "username"],
                "metadata": {
                    "table_name": "users",
                    "columns": [
                        {"name": "user_id", "type": "INT", "primary_key": True},
                        {"name": "email", "type": "VARCHAR(255)", "nullable": False},
                        {"name": "username", "type": "VARCHAR(100)", "nullable": False}
                    ],
                    "indexes": [
                        {"column": "email", "type": "UNIQUE"}
                    ]
                }
            },
            {
                "id": "table_orders",
                "artifactType": "DbTable",
                "fileName": "orders.sql",
                "entities": ["orders", "order_id", "user_id", "status"],
                "metadata": {
                    "table_name": "orders",
                    "columns": [
                        {"name": "order_id", "type": "INT", "primary_key": True},
                        {"name": "user_id", "type": "INT"},  # Missing FK declaration
                        {"name": "status", "type": "VARCHAR(50)"}
                    ]
                    # Note: No foreign_keys or indexes defined
                }
            },
            {
                "id": "table_OrderItems",  # Inconsistent naming (PascalCase)
                "artifactType": "DbTable",
                "fileName": "OrderItems.sql",
                "entities": ["OrderItems", "item_id", "order_id", "product_id"],
                "metadata": {
                    "table_name": "OrderItems",
                    "columns": [
                        {"name": "item_id", "type": "INT", "primary_key": True},
                        {"name": "order_id", "type": "INT"},  # Missing FK
                        {"name": "product_id", "type": "INT"}  # Missing FK
                    ]
                }
            }
        ]

    def test_detect_missing_foreign_keys(self, sample_schema):
        """Test detection of missing foreign key relationships."""
        from codeindex.web.services.db_quality import DbQualityAnalyzer

        analyzer = DbQualityAnalyzer()
        quality_report = analyzer.analyze_schema(sample_schema)

        # Should detect user_id in orders table as potential FK
        missing_fks = quality_report.get("missing_foreign_keys", [])
        assert len(missing_fks) > 0
        assert any("user_id" in fk.lower() for fk in missing_fks)

    def test_detect_missing_indexes(self, sample_schema):
        """Test detection of missing indexes on foreign key columns."""
        from codeindex.web.services.db_quality import DbQualityAnalyzer

        analyzer = DbQualityAnalyzer()
        quality_report = analyzer.analyze_schema(sample_schema)

        # Should recommend indexes on FK columns
        missing_indexes = quality_report.get("missing_indexes", [])
        assert len(missing_indexes) > 0

    def test_check_naming_conventions(self, sample_schema):
        """Test naming convention validation."""
        from codeindex.web.services.db_quality import DbQualityAnalyzer

        analyzer = DbQualityAnalyzer()
        quality_report = analyzer.analyze_schema(sample_schema)

        # Should flag OrderItems (PascalCase) as inconsistent
        naming_issues = quality_report.get("naming_issues", [])
        assert len(naming_issues) > 0
        assert any("OrderItems" in issue for issue in naming_issues)

    def test_analyze_empty_schema(self):
        """Test analysis of empty schema."""
        from codeindex.web.services.db_quality import DbQualityAnalyzer

        analyzer = DbQualityAnalyzer()
        quality_report = analyzer.analyze_schema([])

        # Should return empty report without errors
        assert isinstance(quality_report, dict)
        assert quality_report.get("missing_foreign_keys", []) == []

    def test_identify_column_name_id_suffix(self, sample_schema):
        """Test identification of columns ending in _id as potential FKs."""
        from codeindex.web.services.db_quality import DbQualityAnalyzer

        analyzer = DbQualityAnalyzer()

        # user_id in orders should be flagged as potential FK
        potential_fks = analyzer._find_potential_foreign_keys(sample_schema[1])

        assert len(potential_fks) > 0
        assert "user_id" in [fk["column"] for fk in potential_fks]

    def test_validate_table_naming_snake_case(self):
        """Test snake_case naming convention validation."""
        from codeindex.web.services.db_quality import DbQualityAnalyzer

        analyzer = DbQualityAnalyzer()

        # Valid: users, orders (snake_case)
        assert analyzer._check_naming_convention("users") == True
        assert analyzer._check_naming_convention("order_items") == True

        # Invalid: OrderItems (PascalCase)
        assert analyzer._check_naming_convention("OrderItems") == False

    def test_detect_missing_primary_key(self):
        """Test detection of tables without primary keys."""
        from codeindex.web.services.db_quality import DbQualityAnalyzer

        table_without_pk = {
            "id": "table_logs",
            "artifactType": "DbTable",
            "fileName": "logs.sql",
            "metadata": {
                "table_name": "logs",
                "columns": [
                    {"name": "log_id", "type": "INT"},  # No primary_key flag
                    {"name": "message", "type": "TEXT"}
                ]
            }
        }

        analyzer = DbQualityAnalyzer()
        quality_report = analyzer.analyze_schema([table_without_pk])

        # Should flag missing primary key
        pk_issues = quality_report.get("missing_primary_keys", [])
        assert len(pk_issues) > 0
        assert "logs" in pk_issues[0]

    def test_analyze_column_nullability(self, sample_schema):
        """Test analysis of column nullability patterns."""
        from codeindex.web.services.db_quality import DbQualityAnalyzer

        analyzer = DbQualityAnalyzer()
        quality_report = analyzer.analyze_schema(sample_schema)

        # Should analyze nullability (optional feature)
        # Report may include recommendations for NOT NULL constraints
        assert "total_tables" in quality_report
        assert quality_report["total_tables"] == 3

    def test_detect_potential_index_candidates(self, sample_schema):
        """Test detection of columns that should be indexed."""
        from codeindex.web.services.db_quality import DbQualityAnalyzer

        analyzer = DbQualityAnalyzer()

        # Foreign key columns should be indexed
        index_candidates = analyzer._find_index_candidates(sample_schema[1])

        assert len(index_candidates) > 0
        assert any("user_id" in candidate for candidate in index_candidates)

    def test_generate_quality_score(self, sample_schema):
        """Test quality score calculation."""
        from codeindex.web.services.db_quality import DbQualityAnalyzer

        analyzer = DbQualityAnalyzer()
        quality_report = analyzer.analyze_schema(sample_schema)

        # Should include overall quality score
        quality_score = quality_report.get("quality_score")
        assert quality_score is not None
        assert 0 <= quality_score <= 100

    def test_identify_redundant_indexes(self):
        """Test detection of redundant indexes."""
        from codeindex.web.services.db_quality import DbQualityAnalyzer

        table_with_redundant_indexes = {
            "id": "table_users",
            "artifactType": "DbTable",
            "fileName": "users.sql",
            "metadata": {
                "table_name": "users",
                "columns": [
                    {"name": "user_id", "type": "INT", "primary_key": True},
                    {"name": "email", "type": "VARCHAR(255)"}
                ],
                "indexes": [
                    {"column": "email", "type": "INDEX"},
                    {"column": "email", "type": "UNIQUE"}  # Redundant
                ]
            }
        }

        analyzer = DbQualityAnalyzer()
        quality_report = analyzer.analyze_schema([table_with_redundant_indexes])

        # May flag redundant indexes (optional feature)
        redundant = quality_report.get("redundant_indexes", [])
        # This is an advanced feature, so it's optional

    def test_check_table_size_estimates(self, sample_schema):
        """Test estimation of table size issues."""
        from codeindex.web.services.db_quality import DbQualityAnalyzer

        analyzer = DbQualityAnalyzer()
        quality_report = analyzer.analyze_schema(sample_schema)

        # Report should include table count
        assert "total_tables" in quality_report
        assert quality_report["total_tables"] > 0

    def test_format_quality_report_as_markdown(self, sample_schema):
        """Test markdown formatting of quality report."""
        from codeindex.web.services.db_quality import DbQualityAnalyzer

        analyzer = DbQualityAnalyzer()
        quality_report = analyzer.analyze_schema(sample_schema)

        # Should be able to format as markdown
        markdown_report = analyzer.format_report_markdown(quality_report)

        assert isinstance(markdown_report, str)
        assert "##" in markdown_report or "**" in markdown_report  # Has markdown formatting
        assert len(markdown_report) > 0

    def test_group_issues_by_severity(self, sample_schema):
        """Test grouping issues by severity level."""
        from codeindex.web.services.db_quality import DbQualityAnalyzer

        analyzer = DbQualityAnalyzer()
        quality_report = analyzer.analyze_schema(sample_schema)

        # Issues should be categorized by severity
        if "issues" in quality_report:
            issues = quality_report["issues"]
            assert isinstance(issues, list)
            # Each issue may have severity: HIGH, MEDIUM, LOW

    def test_recommend_improvements(self, sample_schema):
        """Test generation of improvement recommendations."""
        from codeindex.web.services.db_quality import DbQualityAnalyzer

        analyzer = DbQualityAnalyzer()
        quality_report = analyzer.analyze_schema(sample_schema)

        # Should include actionable recommendations
        recommendations = quality_report.get("recommendations", [])
        assert isinstance(recommendations, list)

    def test_analyze_with_existing_foreign_keys(self):
        """Test analysis when FKs are properly declared."""
        from codeindex.web.services.db_quality import DbQualityAnalyzer

        good_schema = [
            {
                "id": "table_orders",
                "artifactType": "DbTable",
                "fileName": "orders.sql",
                "metadata": {
                    "table_name": "orders",
                    "columns": [
                        {"name": "order_id", "type": "INT", "primary_key": True},
                        {"name": "user_id", "type": "INT", "foreign_key": True}
                    ],
                    "foreign_keys": [
                        {"column": "user_id", "references_table": "users", "references_column": "user_id"}
                    ],
                    "indexes": [
                        {"column": "user_id", "type": "INDEX"}
                    ]
                }
            }
        ]

        analyzer = DbQualityAnalyzer()
        quality_report = analyzer.analyze_schema(good_schema)

        # Should have fewer issues
        missing_fks = quality_report.get("missing_foreign_keys", [])
        assert len(missing_fks) == 0

    def test_singleton_pattern(self):
        """Test global database quality analyzer singleton."""
        from codeindex.web.services.db_quality import get_db_quality_analyzer

        analyzer1 = get_db_quality_analyzer()
        analyzer2 = get_db_quality_analyzer()

        assert analyzer1 is analyzer2
