"""
Unit tests for Database Analyzer Service.
"""
import json
import pytest
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

from codeindex.models.prd import (
    DatabaseEntity,
    BusinessRule,
    Column,
    ForeignKey,
    SourceType,
    RuleLayer,
    RuleScope,
    RuleType,
    VisitStatus,
    AnalysisLayer,
)
from codeindex.services.db_analyzer import DatabaseAnalyzer


# ==============================================================================
# Fixtures
# ==============================================================================

@pytest.fixture
def mock_ollama_client():
    """Mock Ollama client."""
    client = Mock()
    return client


@pytest.fixture
def temp_output_dir(tmp_path):
    """Temporary output directory."""
    return tmp_path / "output"


@pytest.fixture
def temp_source_dir(tmp_path):
    """Temporary source directory with test files."""
    source_dir = tmp_path / "source"
    source_dir.mkdir()

    # Create a sample DAO file
    dao_file = source_dir / "UserDAO.java"
    dao_file.write_text("""
package com.example.dao;

import javax.persistence.*;

@Entity
@Table(name = "user")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 255)
    private String email;

    @Column(nullable = false)
    private String passwordHash;

    // Getters and setters
}
""", encoding="utf-8")

    return source_dir


@pytest.fixture
def sample_llm_response():
    """Sample LLM response for entity extraction."""
    return {
        "response": json.dumps({
            "entity_name": "user",
            "qualified_name": "public.user",
            "columns": [
                {
                    "name": "id",
                    "data_type": "BIGINT",
                    "nullable": False,
                    "default_value": None,
                    "description": "Primary key, auto-generated"
                },
                {
                    "name": "email",
                    "data_type": "VARCHAR(255)",
                    "nullable": False,
                    "default_value": None,
                    "description": "User email address, must be unique"
                },
                {
                    "name": "password_hash",
                    "data_type": "VARCHAR(255)",
                    "nullable": False,
                    "default_value": None,
                    "description": "Bcrypt hashed password"
                }
            ],
            "primary_key": ["id"],
            "foreign_keys": [],
            "indexes": [
                {
                    "name": "idx_user_email",
                    "columns": ["email"],
                    "unique": True,
                    "index_type": "BTREE"
                }
            ],
            "constraints": [],
            "business_rules": [
                {
                    "name": "Email Uniqueness",
                    "description": "Each user must have a unique email address",
                    "enforcement": "Unique index on email column"
                }
            ],
            "description": "Stores user account information including credentials and profile data.",
            "estimated_row_count": "medium",
            "domain": "auth"
        })
    }


# ==============================================================================
# Model Tests
# ==============================================================================

def test_column_creation():
    """Test Column model creation."""
    col = Column(
        name="id",
        data_type="BIGINT",
        nullable=False,
        description="Primary key"
    )

    assert col.name == "id"
    assert col.data_type == "BIGINT"
    assert col.nullable is False
    assert col.description == "Primary key"

    # Test to_dict
    col_dict = col.to_dict()
    assert col_dict["name"] == "id"
    assert col_dict["nullable"] is False

    # Test from_dict
    col2 = Column.from_dict(col_dict)
    assert col2.name == col.name
    assert col2.nullable == col.nullable


def test_database_entity_creation():
    """Test DatabaseEntity model creation."""
    entity = DatabaseEntity(
        id="user",
        name="user",
        qualified_name="public.user",
        source_type=SourceType.JPA_ANNOTATION,
        source_files=["/path/to/User.java"],
        columns=[
            Column(name="id", data_type="BIGINT", nullable=False),
            Column(name="email", data_type="VARCHAR(255)", nullable=False)
        ],
        primary_key=["id"],
        created_at=datetime.now()
    )

    assert entity.id == "user"
    assert entity.name == "user"
    assert len(entity.columns) == 2
    assert entity.primary_key == ["id"]

    # Test to_dict
    entity_dict = entity.to_dict()
    assert entity_dict["id"] == "user"
    assert len(entity_dict["columns"]) == 2

    # Test from_dict
    entity2 = DatabaseEntity.from_dict(entity_dict)
    assert entity2.id == entity.id
    assert len(entity2.columns) == len(entity.columns)


def test_database_entity_validation():
    """Test DatabaseEntity validation."""
    # Missing required fields
    with pytest.raises(ValueError, match="id is required"):
        DatabaseEntity(
            id="",
            name="user",
            source_type=SourceType.JPA_ANNOTATION,
            source_files=["/path/to/User.java"],
            columns=[Column(name="id", data_type="BIGINT")],
            created_at=datetime.now()
        )

    # No columns
    with pytest.raises(ValueError, match="columns is required"):
        DatabaseEntity(
            id="user",
            name="user",
            source_type=SourceType.JPA_ANNOTATION,
            source_files=["/path/to/User.java"],
            columns=[],
            created_at=datetime.now()
        )

    # Invalid primary key column
    with pytest.raises(ValueError, match="Primary key column.*not in columns"):
        DatabaseEntity(
            id="user",
            name="user",
            source_type=SourceType.JPA_ANNOTATION,
            source_files=["/path/to/User.java"],
            columns=[Column(name="id", data_type="BIGINT")],
            primary_key=["invalid_column"],
            created_at=datetime.now()
        )


def test_business_rule_creation():
    """Test BusinessRule model creation."""
    rule = BusinessRule(
        id="BR_001",
        name="Email Validation",
        layer=RuleLayer.DATABASE,
        scope=RuleScope.FIELD,
        rule_type=RuleType.VALIDATION,
        description="Email must be valid format",
        source_files=["/path/to/User.java"],
        created_at=datetime.now()
    )

    assert rule.id == "BR_001"
    assert rule.layer == RuleLayer.DATABASE
    assert rule.scope == RuleScope.FIELD

    # Test to_dict
    rule_dict = rule.to_dict()
    assert rule_dict["id"] == "BR_001"
    assert rule_dict["layer"] == "database"

    # Test from_dict
    rule2 = BusinessRule.from_dict(rule_dict)
    assert rule2.id == rule.id
    assert rule2.layer == rule.layer


# ==============================================================================
# Database Analyzer Tests
# ==============================================================================

def test_database_analyzer_init(mock_ollama_client, temp_output_dir, temp_source_dir):
    """Test DatabaseAnalyzer initialization."""
    analyzer = DatabaseAnalyzer(
        ollama_client=mock_ollama_client,
        output_dir=temp_output_dir,
        source_dir=temp_source_dir
    )

    assert analyzer.output_dir == temp_output_dir
    assert analyzer.source_dir == temp_source_dir
    assert analyzer.max_workers == 10
    assert analyzer.db_entities_dir.exists()
    assert analyzer.business_rules_dir.exists()


def test_find_dao_files(mock_ollama_client, temp_output_dir, temp_source_dir):
    """Test finding DAO files."""
    analyzer = DatabaseAnalyzer(
        ollama_client=mock_ollama_client,
        output_dir=temp_output_dir,
        source_dir=temp_source_dir
    )

    files = analyzer.find_dao_files()

    # Should find the UserDAO.java file
    assert len(files) >= 1
    assert any("UserDAO.java" in str(f) or "User.java" in str(f) for f in files)


def test_detect_framework(mock_ollama_client, temp_output_dir, temp_source_dir):
    """Test framework detection."""
    analyzer = DatabaseAnalyzer(
        ollama_client=mock_ollama_client,
        output_dir=temp_output_dir,
        source_dir=temp_source_dir
    )

    # JPA
    jpa_content = "@Entity\n@Table(name='user')\npublic class User {}"
    assert analyzer._detect_framework(jpa_content) == "JPA"

    # iBATIS/MyBatis
    ibatis_content = "<mapper namespace='com.example.UserMapper'>"
    assert "MyBatis" in analyzer._detect_framework(ibatis_content)

    # SQL
    sql_content = "CREATE TABLE user (id BIGINT)"
    assert analyzer._detect_framework(sql_content) == "SQL DDL"


def test_compute_file_hash(mock_ollama_client, temp_output_dir, temp_source_dir):
    """Test file hash computation."""
    analyzer = DatabaseAnalyzer(
        ollama_client=mock_ollama_client,
        output_dir=temp_output_dir,
        source_dir=temp_source_dir
    )

    # Find a test file
    files = analyzer.find_dao_files()
    if files:
        test_file = files[0]
        hash1 = analyzer._compute_file_hash(test_file)

        assert len(hash1) == 64  # SHA-256 hex string
        assert all(c in "0123456789abcdef" for c in hash1)

        # Same file should produce same hash
        hash2 = analyzer._compute_file_hash(test_file)
        assert hash1 == hash2


def test_analyze_file_with_mock_llm(
    mock_ollama_client,
    temp_output_dir,
    temp_source_dir,
    sample_llm_response
):
    """Test analyzing a single file with mocked LLM."""
    # Mock LLM response
    mock_ollama_client.call_ollama.return_value = sample_llm_response

    analyzer = DatabaseAnalyzer(
        ollama_client=mock_ollama_client,
        output_dir=temp_output_dir,
        source_dir=temp_source_dir
    )

    # Find test file
    files = analyzer.find_dao_files()
    assert len(files) > 0

    test_file = files[0]

    # Analyze file
    result = analyzer.analyze_file(test_file)

    # Verify result
    assert result is not None
    assert result["status"] == "success"
    assert "entity" in result
    assert "rules" in result

    # Verify entity
    entity = result["entity"]
    assert entity.name == "user"
    assert len(entity.columns) == 3
    assert entity.primary_key == ["id"]

    # Verify rules
    rules = result["rules"]
    assert len(rules) == 1
    assert rules[0].name == "Email Uniqueness"

    # Verify output files were created
    entity_file = temp_output_dir / "database" / "entities" / "user.json"
    assert entity_file.exists()

    rule_file = temp_output_dir / "business_rules" / rules[0].id / ".json"
    # Note: Exact rule ID format depends on implementation


def test_visit_log_tracking(mock_ollama_client, temp_output_dir, temp_source_dir):
    """Test visit log tracking."""
    analyzer = DatabaseAnalyzer(
        ollama_client=mock_ollama_client,
        output_dir=temp_output_dir,
        source_dir=temp_source_dir
    )

    # Initially empty
    assert len(analyzer.visit_log) == 0

    # Find test file
    files = analyzer.find_dao_files()
    test_file = files[0]

    # Should analyze (not in log)
    assert analyzer._should_analyze_file(test_file) is True

    # Mock successful analysis
    from codeindex.models.prd import FileVisitEntry

    content_hash = analyzer._compute_file_hash(test_file)
    entry = FileVisitEntry(
        file_path=str(test_file),
        timestamp=datetime.now(),
        status=VisitStatus.SUCCESS,
        content_hash=content_hash,
        layer=AnalysisLayer.DATABASE
    )

    analyzer._append_visit_log(entry)

    # Verify appended
    assert len(analyzer.visit_log) == 1
    assert str(test_file) in analyzer.visit_log

    # Should skip (unchanged file)
    assert analyzer._should_analyze_file(test_file) is False


def test_force_refresh_ignores_visit_log(
    mock_ollama_client,
    temp_output_dir,
    temp_source_dir
):
    """Test that force_refresh re-analyzes all files."""
    # Create analyzer with force_refresh
    analyzer = DatabaseAnalyzer(
        ollama_client=mock_ollama_client,
        output_dir=temp_output_dir,
        source_dir=temp_source_dir,
        force_refresh=True
    )

    # Add entry to visit log
    files = analyzer.find_dao_files()
    test_file = files[0]

    from codeindex.models.prd import FileVisitEntry

    content_hash = analyzer._compute_file_hash(test_file)
    entry = FileVisitEntry(
        file_path=str(test_file),
        timestamp=datetime.now(),
        status=VisitStatus.SUCCESS,
        content_hash=content_hash,
        layer=AnalysisLayer.DATABASE
    )

    analyzer._append_visit_log(entry)

    # Even with entry in log, should still analyze due to force_refresh
    assert analyzer._should_analyze_file(test_file) is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
