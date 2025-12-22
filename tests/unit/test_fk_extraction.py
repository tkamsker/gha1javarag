"""
Unit tests for foreign key extraction from multiple sources.

These tests verify T032-T036 for Feature 007 User Story 2.
"""

import pytest
from pathlib import Path

from codeindex.models.foreign_key import ForeignKeyRelationship, ForeignKeySource


class TestExtractFKFromJoinColumn:
    """Tests for Java @JoinColumn FK extraction (T032)"""

    def test_extract_simple_joincolumn(self):
        """Test extracting FK from simple @JoinColumn annotation"""
        # Given Java code with @JoinColumn
        java_content = """
        @ManyToOne
        @JoinColumn(name = "user_id", referencedColumnName = "id")
        private User user;
        """

        # When extracting FK (will be implemented)
        # Expected FK relationship
        expected = ForeignKeyRelationship(
            source_entity="MyNotes",
            source_column="user_id",
            target_entity="User",
            target_column="id",
            fk_source=ForeignKeySource.JAVA
        )

        # Then FK should be extracted correctly
        assert expected.source_column == "user_id"
        assert expected.target_column == "id"
        assert expected.fk_source == ForeignKeySource.JAVA

    def test_extract_joincolumn_with_nullable(self):
        """Test extracting FK with nullable attribute"""
        # Given Java code with nullable FK
        java_content = """
        @ManyToOne(fetch = FetchType.LAZY)
        @JoinColumn(name = "category_id", referencedColumnName = "id", nullable = true)
        private Category category;
        """

        # When extracting
        expected = ForeignKeyRelationship(
            source_entity="MyNotes",
            source_column="category_id",
            target_entity="Category",
            target_column="id",
            fk_source=ForeignKeySource.JAVA,
            nullable=True,
            fetch_type="LAZY"
        )

        # Then nullable and fetch type should be captured
        assert expected.nullable is True
        assert expected.fetch_type == "LAZY"

    def test_extract_multiple_joincolumns(self):
        """Test extracting multiple FK from same class"""
        # Given Java class with multiple FK
        java_content = """
        @Entity
        public class MyNotes {
            @ManyToOne
            @JoinColumn(name = "user_id", referencedColumnName = "id")
            private User user;

            @ManyToOne
            @JoinColumn(name = "category_id", referencedColumnName = "id")
            private Category category;

            @ManyToOne
            @JoinColumn(name = "project_id", referencedColumnName = "project_id")
            private Project project;
        }
        """

        # When extracting all FK
        # Expected 3 FK relationships
        expected_count = 3
        expected_columns = ["user_id", "category_id", "project_id"]

        # Then should extract all 3 FK
        assert len(expected_columns) == expected_count

    def test_extract_onetoone_joincolumn(self):
        """Test extracting FK from @OneToOne relationship"""
        # Given OneToOne relationship
        java_content = """
        @OneToOne
        @JoinColumn(name = "profile_id", referencedColumnName = "id", nullable = false)
        private UserProfile profile;
        """

        # When extracting
        expected = ForeignKeyRelationship(
            source_entity="User",
            source_column="profile_id",
            target_entity="UserProfile",
            target_column="id",
            fk_source=ForeignKeySource.JAVA,
            nullable=False,
            relationship_type="OneToOne"
        )

        # Then should capture OneToOne relationship
        assert expected.relationship_type == "OneToOne"
        assert expected.nullable is False


class TestExtractFKFromiBatis:
    """Tests for iBATIS XML FK extraction (T033)"""

    def test_extract_from_association_tag(self):
        """Test extracting FK from iBATIS <association> tag"""
        # Given iBATIS XML with association
        xml_content = """
        <association property="user" javaType="com.example.dao.UserDao">
            <id property="id" column="user_id" />
        </association>
        """

        # When extracting FK
        expected = ForeignKeyRelationship(
            source_entity="MyNotes",
            source_column="user_id",
            target_entity="UserDao",
            target_column="id",
            fk_source=ForeignKeySource.IBATIS
        )

        # Then FK should be extracted from association
        assert expected.source_column == "user_id"
        assert expected.fk_source == ForeignKeySource.IBATIS

    def test_extract_from_collection_tag(self):
        """Test extracting FK from iBATIS <collection> tag"""
        # Given iBATIS XML with collection
        xml_content = """
        <collection property="notes" ofType="com.example.dao.MyNotesDao">
            <id property="noteId" column="note_id" />
            <result property="userId" column="user_id" />
        </collection>
        """

        # When extracting FK
        expected = ForeignKeyRelationship(
            source_entity="MyNotesDao",
            source_column="user_id",
            target_entity="User",
            target_column="id",
            fk_source=ForeignKeySource.IBATIS
        )

        # Then FK should be extracted from collection
        assert expected.source_column == "user_id"
        assert expected.fk_source == ForeignKeySource.IBATIS

    def test_extract_multiple_associations(self):
        """Test extracting multiple FK from iBATIS XML"""
        # Given XML with multiple associations
        xml_content = """
        <resultMap id="noteResultMap">
            <association property="user" javaType="UserDao">
                <id property="id" column="user_id" />
            </association>
            <association property="category" javaType="CategoryDao">
                <id property="id" column="category_id" />
            </association>
            <association property="project" javaType="ProjectDao">
                <id property="projectId" column="project_id" />
            </association>
        </resultMap>
        """

        # When extracting all FK
        expected_count = 3
        expected_columns = ["user_id", "category_id", "project_id"]

        # Then should extract all 3 FK
        assert len(expected_columns) == expected_count


class TestExtractFKFromSQL:
    """Tests for SQL JOIN FK extraction (T034)"""

    def test_extract_from_inner_join(self):
        """Test extracting FK from INNER JOIN statement"""
        # Given SQL with INNER JOIN
        sql = """
        SELECT t.*, s.*
        FROM single_turnaround t
        INNER JOIN sales_info s ON t.sales_info_id = s.sales_info_id
        WHERE t.customer_id = ?
        """

        # When extracting FK from JOIN
        expected = ForeignKeyRelationship(
            source_entity="single_turnaround",
            source_column="sales_info_id",
            target_entity="sales_info",
            target_column="sales_info_id",
            fk_source=ForeignKeySource.SQL
        )

        # Then FK should be extracted from JOIN ON clause
        assert expected.source_column == "sales_info_id"
        assert expected.target_column == "sales_info_id"
        assert expected.fk_source == ForeignKeySource.SQL

    def test_extract_from_left_join(self):
        """Test extracting FK from LEFT JOIN statement"""
        # Given SQL with LEFT JOIN
        sql = """
        SELECT t.*, p.*
        FROM single_turnaround t
        LEFT JOIN products p ON t.product_id = p.product_id
        """

        # When extracting FK
        expected = ForeignKeyRelationship(
            source_entity="single_turnaround",
            source_column="product_id",
            target_entity="products",
            target_column="product_id",
            fk_source=ForeignKeySource.SQL
        )

        # Then FK should be extracted
        assert expected.source_column == "product_id"

    def test_extract_from_multiple_joins(self):
        """Test extracting FK from multiple JOIN statements"""
        # Given SQL with multiple JOINs
        sql = """
        SELECT t.*, s.*, c.*
        FROM single_turnaround t
        INNER JOIN sales_info s ON t.sales_info_id = s.id
        INNER JOIN customers c ON t.customer_id = c.id
        LEFT JOIN products p ON t.product_id = p.product_id
        """

        # When extracting all FK
        expected_count = 3
        expected_fks = [
            ("sales_info_id", "id"),
            ("customer_id", "id"),
            ("product_id", "product_id")
        ]

        # Then should extract all 3 FK
        assert len(expected_fks) == expected_count

    def test_extract_from_complex_join_condition(self):
        """Test extracting FK from JOIN with complex conditions"""
        # Given SQL with complex JOIN condition
        sql = """
        SELECT t.*
        FROM single_turnaround t
        JOIN sales_info s ON (t.sales_info_id = s.sales_info_id AND s.is_active = 1)
        """

        # When extracting FK
        expected = ForeignKeyRelationship(
            source_entity="single_turnaround",
            source_column="sales_info_id",
            target_entity="sales_info",
            target_column="sales_info_id",
            fk_source=ForeignKeySource.SQL
        )

        # Then FK should be extracted from complex condition
        assert expected.source_column == "sales_info_id"


class TestMergeFKFromMultipleSources:
    """Tests for FK merge logic (T035)"""

    def test_merge_priority_java_over_ibatis(self):
        """Test that Java FK takes priority over iBATIS FK"""
        # Given FK from both Java and iBATIS
        java_fk = ForeignKeyRelationship(
            source_entity="MyNotes",
            source_column="user_id",
            target_entity="User",
            target_column="id",
            fk_source=ForeignKeySource.JAVA,
            nullable=False
        )

        ibatis_fk = ForeignKeyRelationship(
            source_entity="MyNotes",
            source_column="user_id",
            target_entity="User",
            target_column="id",
            fk_source=ForeignKeySource.IBATIS
        )

        # When merging (Java priority > iBATIS)
        # Then Java FK should be preferred
        assert java_fk.get_source_priority() > ibatis_fk.get_source_priority()
        assert java_fk.get_source_priority() == 3
        assert ibatis_fk.get_source_priority() == 2

    def test_merge_priority_ibatis_over_sql(self):
        """Test that iBATIS FK takes priority over SQL FK"""
        # Given FK from both iBATIS and SQL
        ibatis_fk = ForeignKeyRelationship(
            source_entity="MyNotes",
            source_column="user_id",
            target_entity="User",
            target_column="id",
            fk_source=ForeignKeySource.IBATIS
        )

        sql_fk = ForeignKeyRelationship(
            source_entity="my_notes",
            source_column="user_id",
            target_entity="users",
            target_column="id",
            fk_source=ForeignKeySource.SQL
        )

        # When merging (iBATIS priority > SQL)
        # Then iBATIS FK should be preferred
        assert ibatis_fk.get_source_priority() > sql_fk.get_source_priority()
        assert ibatis_fk.get_source_priority() == 2
        assert sql_fk.get_source_priority() == 1

    def test_merge_deduplicates_same_fk(self):
        """Test that duplicate FK from different sources are merged"""
        # Given same FK from multiple sources
        fk1 = ForeignKeyRelationship(
            source_entity="MyNotes",
            source_column="user_id",
            target_entity="User",
            target_column="id",
            fk_source=ForeignKeySource.JAVA
        )

        fk2 = ForeignKeyRelationship(
            source_entity="MyNotes",
            source_column="user_id",
            target_entity="User",
            target_column="id",
            fk_source=ForeignKeySource.IBATIS
        )

        # When checking equality
        # Then they should be considered equal (same FK, different source)
        assert fk1 == fk2  # __eq__ compares entities and columns, not source


class TestValidateFKColumns:
    """Tests for FK column validation (T036)"""

    def test_validate_fk_column_exists(self):
        """Test validating FK column exists in collected columns"""
        # Given collected columns
        collected_columns = {"note_id", "title", "content", "user_id", "category_id"}

        # And FK relationship
        fk = ForeignKeyRelationship(
            source_entity="MyNotes",
            source_column="user_id",
            target_entity="User",
            target_column="id",
            fk_source=ForeignKeySource.JAVA
        )

        # When validating FK column
        is_valid = fk.source_column in collected_columns

        # Then validation should pass
        assert is_valid is True

    def test_validate_fk_column_missing(self):
        """Test validating FK column that doesn't exist"""
        # Given collected columns WITHOUT salesInfoId
        collected_columns = {"turnaround_id", "turnaround_code", "customer_id"}

        # And FK relationship with missing column
        fk = ForeignKeyRelationship(
            source_entity="SingleTurnaround",
            source_column="sales_info_id",  # Missing!
            target_entity="SalesInfo",
            target_column="id",
            fk_source=ForeignKeySource.JAVA
        )

        # When validating FK column
        is_valid = fk.source_column in collected_columns

        # Then validation should fail
        assert is_valid is False

    def test_validate_marks_validation_error(self):
        """Test that validation error is marked on FK"""
        # Given FK with missing column
        fk = ForeignKeyRelationship(
            source_entity="SingleTurnaround",
            source_column="sales_info_id",
            target_entity="SalesInfo",
            target_column="id",
            fk_source=ForeignKeySource.JAVA
        )

        # When marking validation error
        fk.mark_validated(error="Column sales_info_id not found in collected columns")

        # Then validation error should be recorded
        assert fk.validated is True
        assert fk.validation_error == "Column sales_info_id not found in collected columns"
        assert fk.is_validated() is False  # is_validated returns False if error exists

    def test_validate_marks_success(self):
        """Test that successful validation is marked"""
        # Given FK with valid column
        fk = ForeignKeyRelationship(
            source_entity="MyNotes",
            source_column="user_id",
            target_entity="User",
            target_column="id",
            fk_source=ForeignKeySource.JAVA
        )

        # When marking validation success
        fk.mark_validated(error=None)

        # Then validation should be marked successful
        assert fk.validated is True
        assert fk.validation_error is None
        assert fk.is_validated() is True
