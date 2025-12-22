"""
Integration tests for complete DAO analysis with FK extraction.

Tests T037 for Feature 007 User Story 2.
"""

import pytest
from pathlib import Path
from typing import List

from codeindex.models.foreign_key import ForeignKeyRelationship, ForeignKeySource
from codeindex.services.db_analyzer import DbAnalyzer


class TestDaoAnalysisWithMultipleFKSources:
    """Integration tests for DAO analysis combining Java, iBATIS, and SQL FK sources"""

    @pytest.fixture
    def db_analyzer(self):
        """Create DbAnalyzer instance"""
        return DbAnalyzer()

    @pytest.fixture
    def my_notes_dao_path(self) -> Path:
        """Path to MyNotesDao fixture"""
        return Path(__file__).parent.parent / "fixtures" / "dao" / "MyNotesDao.java"

    @pytest.fixture
    def my_notes_ibatis_path(self) -> Path:
        """Path to notes.ibatis.xml fixture"""
        return Path(__file__).parent.parent / "fixtures" / "dao" / "notes.ibatis.xml"

    @pytest.fixture
    def single_turnaround_dao_path(self) -> Path:
        """Path to SingleTurnaroundDao fixture"""
        return Path(__file__).parent.parent / "fixtures" / "dao" / "SingleTurnaroundDao.java"

    @pytest.fixture
    def inventory_product_group_dao_path(self) -> Path:
        """Path to InventoryProductGroupDao fixture"""
        return Path(__file__).parent.parent / "fixtures" / "dao" / "InventoryProductGroupDao.java"

    def test_analyze_my_notes_dao_java_fk(self, db_analyzer, my_notes_dao_path):
        """Test extracting FK from MyNotesDao Java @JoinColumn annotations"""
        # Given MyNotesDao with 3 @JoinColumn FK
        assert my_notes_dao_path.exists()

        # When analyzing the DAO
        fk_relationships = db_analyzer.extract_foreign_keys_from_file(my_notes_dao_path)

        # Then should extract all 3 FK
        assert len(fk_relationships) >= 3

        # Check specific FK extracted
        fk_columns = [fk.source_column for fk in fk_relationships]
        assert "user_id" in fk_columns
        assert "category_id" in fk_columns
        assert "project_id" in fk_columns

        # Check FK source is Java
        for fk in fk_relationships:
            if fk.source_column in ["user_id", "category_id", "project_id"]:
                assert fk.fk_source == ForeignKeySource.JAVA

    def test_analyze_ibatis_xml_fk(self, db_analyzer, my_notes_ibatis_path):
        """Test extracting FK from iBATIS XML associations"""
        # Given notes.ibatis.xml with multiple associations
        assert my_notes_ibatis_path.exists()

        # When analyzing the XML file
        fk_relationships = db_analyzer.extract_foreign_keys_from_file(my_notes_ibatis_path)

        # Then should extract FK from associations
        assert len(fk_relationships) >= 2

        # Check FK source is iBATIS
        for fk in fk_relationships:
            assert fk.fk_source == ForeignKeySource.IBATIS

    def test_analyze_sql_join_fk(self, db_analyzer, single_turnaround_dao_path):
        """Test extracting FK from SQL JOIN statements"""
        # Given SingleTurnaroundDao with SQL JOIN statements
        assert single_turnaround_dao_path.exists()

        # When analyzing the DAO
        fk_relationships = db_analyzer.extract_foreign_keys_from_file(single_turnaround_dao_path)

        # Then should extract FK from JOIN ON clauses
        assert len(fk_relationships) >= 2

        # Check specific FK from JOIN statements
        fk_pairs = [(fk.source_column, fk.target_column) for fk in fk_relationships]
        assert ("sales_info_id", "sales_info_id") in fk_pairs or ("sales_info_id", "id") in fk_pairs
        assert ("customer_id", "customer_id") in fk_pairs or ("customer_id", "id") in fk_pairs

        # Check FK source is SQL
        for fk in fk_relationships:
            if fk.source_column in ["sales_info_id", "customer_id"]:
                assert fk.fk_source == ForeignKeySource.SQL

    def test_merge_fk_from_multiple_sources(self, db_analyzer, my_notes_dao_path, my_notes_ibatis_path):
        """Test merging FK from both Java and iBATIS for same entity"""
        # Given FK from both Java and iBATIS sources
        java_fk = db_analyzer.extract_foreign_keys_from_file(my_notes_dao_path)
        ibatis_fk = db_analyzer.extract_foreign_keys_from_file(my_notes_ibatis_path)

        # When merging FK from multiple sources
        merged_fk = db_analyzer.merge_foreign_keys([java_fk, ibatis_fk])

        # Then should deduplicate same FK
        # user_id FK appears in both Java and iBATIS - should merge to single entry
        user_fk_list = [fk for fk in merged_fk if fk.source_column == "user_id"]

        # Should have exactly 1 user_id FK (deduplicated)
        assert len(user_fk_list) == 1

        # Java should take priority over iBATIS
        user_fk = user_fk_list[0]
        assert user_fk.fk_source == ForeignKeySource.JAVA
        assert user_fk.get_source_priority() == 3

    def test_validate_fk_against_collected_columns(self, db_analyzer, my_notes_dao_path):
        """Test FK validation against collected columns"""
        # Given FK extracted from DAO
        fk_relationships = db_analyzer.extract_foreign_keys_from_file(my_notes_dao_path)

        # And collected columns from the entity
        collected_columns = {
            "note_id", "title", "content", "created_at", "updated_at",
            "user_id", "category_id", "project_id"
        }

        # When validating FK columns
        validation_results = db_analyzer.validate_foreign_keys(fk_relationships, collected_columns)

        # Then all FK columns should be valid (present in collected columns)
        assert all(result.is_valid for result in validation_results)

        # Check specific FK are validated
        validated_columns = [result.fk.source_column for result in validation_results if result.is_valid]
        assert "user_id" in validated_columns
        assert "category_id" in validated_columns
        assert "project_id" in validated_columns

    def test_validate_fk_missing_column_error(self, db_analyzer, my_notes_dao_path):
        """Test FK validation fails gracefully for missing columns"""
        # Given FK extracted from DAO
        fk_relationships = db_analyzer.extract_foreign_keys_from_file(my_notes_dao_path)

        # And collected columns WITHOUT some FK columns (simulating validation error)
        collected_columns = {
            "note_id", "title", "content", "created_at", "updated_at",
            "user_id"  # Missing: category_id, project_id
        }

        # When validating FK columns
        validation_results = db_analyzer.validate_foreign_keys(fk_relationships, collected_columns)

        # Then validation should fail for missing columns
        failed_validations = [result for result in validation_results if not result.is_valid]
        assert len(failed_validations) >= 2

        # Check missing columns are identified
        failed_columns = [result.fk.source_column for result in failed_validations]
        assert "category_id" in failed_columns
        assert "project_id" in failed_columns

        # Check error messages are set
        for result in failed_validations:
            assert result.error_message is not None
            assert "not found" in result.error_message.lower()

    def test_analyze_inventory_product_group_dao(self, db_analyzer, inventory_product_group_dao_path):
        """Test analyzing InventoryProductGroupDao with complex FK relationships"""
        # Given InventoryProductGroupDao fixture
        assert inventory_product_group_dao_path.exists()

        # When analyzing the DAO
        fk_relationships = db_analyzer.extract_foreign_keys_from_file(inventory_product_group_dao_path)

        # Then should extract FK relationships
        assert len(fk_relationships) >= 1

        # Check FK extracted from SQL or Java annotations
        for fk in fk_relationships:
            assert fk.fk_source in [ForeignKeySource.JAVA, ForeignKeySource.SQL]
            assert fk.source_column is not None
            assert fk.target_column is not None

    def test_complete_dao_analysis_pipeline(self, db_analyzer, my_notes_dao_path, my_notes_ibatis_path):
        """Test complete DAO analysis pipeline from discovery to validation"""
        # Given DAO files from multiple sources
        dao_files = [my_notes_dao_path, my_notes_ibatis_path]

        # When running complete analysis
        all_fk = []
        for dao_file in dao_files:
            fk_list = db_analyzer.extract_foreign_keys_from_file(dao_file)
            all_fk.extend(fk_list)

        # Merge FK from all sources
        merged_fk = db_analyzer.merge_foreign_keys([all_fk])

        # Collect columns (simulated)
        collected_columns = {
            "note_id", "title", "content", "user_id", "category_id", "project_id"
        }

        # Validate merged FK
        validation_results = db_analyzer.validate_foreign_keys(merged_fk, collected_columns)

        # Then pipeline should complete successfully
        assert len(merged_fk) >= 3
        assert all(result.is_valid for result in validation_results)

        # Check FK priority is respected
        java_fk_count = len([fk for fk in merged_fk if fk.fk_source == ForeignKeySource.JAVA])
        assert java_fk_count >= 3  # MyNotesDao has 3 Java FK

    def test_fk_metrics_logging(self, db_analyzer, my_notes_dao_path):
        """Test that FK extraction logs metrics for monitoring"""
        # Given DAO file
        # When extracting FK
        fk_relationships = db_analyzer.extract_foreign_keys_from_file(my_notes_dao_path)

        # Then should log FK metrics
        from codeindex.utils.metrics import get_metrics_collector
        metrics_collector = get_metrics_collector()

        # Check FK metrics were recorded
        fk_summary = metrics_collector.get_fk_summary()
        assert fk_summary is not None
        assert fk_summary.get('total_extracted', 0) >= len(fk_relationships)
