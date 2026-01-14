"""
Unit tests for base agent configuration (T018).

Tests the agent data structures and configurations including:
- AgentRole enum
- AgentConfig dataclass
- AgentResponse dataclass
- Citation dataclass
- Default agent configurations
- Config override mechanism
"""

import pytest
from dataclasses import FrozenInstanceError
from datetime import datetime

from codeindex.web.agents.base import (
    AgentRole,
    AgentConfig,
    AgentResponse,
    Citation,
    DEFAULT_AGENT_CONFIGS,
    get_agent_config
)


class TestAgentRole:
    """Test AgentRole enum."""

    def test_all_roles_defined(self):
        """Test that all 8 agent roles are defined."""
        roles = list(AgentRole)

        assert len(roles) == 8
        assert AgentRole.SENIOR_DEVELOPER in roles
        assert AgentRole.DATA_ANALYST in roles
        assert AgentRole.FRONTEND_SPECIALIST in roles
        assert AgentRole.BACKEND_SPECIALIST in roles
        assert AgentRole.PRD_WRITER in roles
        assert AgentRole.SPECKIT_WRITER in roles
        assert AgentRole.GHERKIN_TEST_WRITER in roles
        assert AgentRole.PLAYWRIGHT_TEST_WRITER in roles

    def test_role_values(self):
        """Test that role values are human-readable strings."""
        assert AgentRole.SENIOR_DEVELOPER.value == "Senior Developer"
        assert AgentRole.DATA_ANALYST.value == "Data Analyst"
        assert AgentRole.PRD_WRITER.value == "PRD Writer"

    def test_role_comparison(self):
        """Test role equality comparison."""
        role1 = AgentRole.SENIOR_DEVELOPER
        role2 = AgentRole.SENIOR_DEVELOPER
        role3 = AgentRole.DATA_ANALYST

        assert role1 == role2
        assert role1 != role3


class TestCitation:
    """Test Citation dataclass."""

    def test_citation_creation(self):
        """Test creating a citation."""
        citation = Citation(
            artifact_id="art-123",
            file_path="/path/to/file.java",
            line_start=10,
            line_end=20,
            artifact_type="DaoCall",
            confidence=0.95
        )

        assert citation.artifact_id == "art-123"
        assert citation.file_path == "/path/to/file.java"
        assert citation.line_start == 10
        assert citation.line_end == 20
        assert citation.artifact_type == "DaoCall"
        assert citation.confidence == 0.95

    def test_citation_minimal(self):
        """Test creating citation with required fields only."""
        citation = Citation(
            artifact_id="art-123",
            file_path="/path/to/file.java"
        )

        assert citation.artifact_id == "art-123"
        assert citation.file_path == "/path/to/file.java"
        assert citation.line_start is None
        assert citation.line_end is None
        assert citation.artifact_type is None
        assert citation.confidence == 1.0  # Default

    def test_citation_to_dict(self):
        """Test citation serialization to dict."""
        citation = Citation(
            artifact_id="art-123",
            file_path="/path/to/file.java",
            line_start=10,
            artifact_type="DaoCall"
        )

        result = citation.to_dict()

        assert result == {
            "artifact_id": "art-123",
            "file_path": "/path/to/file.java",
            "line_start": 10,
            "line_end": None,
            "artifact_type": "DaoCall",
            "confidence": 1.0
        }


class TestAgentConfig:
    """Test AgentConfig dataclass."""

    def test_config_creation_minimal(self):
        """Test creating config with required fields."""
        config = AgentConfig(
            role=AgentRole.SENIOR_DEVELOPER,
            goal="Test goal",
            backstory="Test backstory"
        )

        assert config.role == AgentRole.SENIOR_DEVELOPER
        assert config.goal == "Test goal"
        assert config.backstory == "Test backstory"

    def test_config_creation_full(self):
        """Test creating config with all fields."""
        config = AgentConfig(
            role=AgentRole.SENIOR_DEVELOPER,
            goal="Test goal",
            backstory="Test backstory",
            verbose=False,
            max_iterations=5,
            allow_delegation=True,
            llm_model="test-model",
            temperature=0.5,
            max_tokens=1000,
            tools=["Tool1", "Tool2"],
            output_format="json",
            citation_style="footnotes",
            technical_level="junior"
        )

        assert config.verbose is False
        assert config.max_iterations == 5
        assert config.allow_delegation is True
        assert config.llm_model == "test-model"
        assert config.temperature == 0.5
        assert config.max_tokens == 1000
        assert config.tools == ["Tool1", "Tool2"]
        assert config.output_format == "json"
        assert config.citation_style == "footnotes"
        assert config.technical_level == "junior"

    def test_config_defaults(self):
        """Test default values for config fields."""
        config = AgentConfig(
            role=AgentRole.SENIOR_DEVELOPER,
            goal="Test goal",
            backstory="Test backstory"
        )

        assert config.verbose is True
        assert config.max_iterations == 10
        assert config.allow_delegation is False
        assert config.llm_model == "gemma3:12b"
        assert config.temperature == 0.7
        assert config.max_tokens == 2000
        assert config.tools == []
        assert config.output_format == "markdown"
        assert config.citation_style == "inline"
        assert config.technical_level == "senior"

    def test_config_to_dict(self):
        """Test config serialization to dict."""
        config = AgentConfig(
            role=AgentRole.DATA_ANALYST,
            goal="Analyze data",
            backstory="Expert analyst",
            tools=["Tool1"]
        )

        result = config.to_dict()

        assert result["role"] == "Data Analyst"
        assert result["goal"] == "Analyze data"
        assert result["backstory"] == "Expert analyst"
        assert result["tools"] == ["Tool1"]
        assert "verbose" in result
        assert "llm_model" in result


class TestAgentResponse:
    """Test AgentResponse dataclass."""

    def test_response_creation_minimal(self):
        """Test creating response with required fields."""
        response = AgentResponse(
            agent_role=AgentRole.SENIOR_DEVELOPER,
            query="Test query",
            timestamp="2024-01-01T00:00:00",
            duration_seconds=1.5,
            response_text="Test response"
        )

        assert response.agent_role == AgentRole.SENIOR_DEVELOPER
        assert response.query == "Test query"
        assert response.timestamp == "2024-01-01T00:00:00"
        assert response.duration_seconds == 1.5
        assert response.response_text == "Test response"

    def test_response_creation_full(self):
        """Test creating response with all fields."""
        citation = Citation(
            artifact_id="art-123",
            file_path="/path/to/file.java"
        )

        response = AgentResponse(
            agent_role=AgentRole.SENIOR_DEVELOPER,
            query="Test query",
            timestamp="2024-01-01T00:00:00",
            duration_seconds=1.5,
            response_text="Test response",
            citations=[citation],
            confidence=0.9,
            tokens_used=100,
            suggested_questions=["Question 1", "Question 2"],
            tools_used=["Tool1"],
            error=None,
            retry_count=0
        )

        assert len(response.citations) == 1
        assert response.confidence == 0.9
        assert response.tokens_used == 100
        assert len(response.suggested_questions) == 2
        assert response.tools_used == ["Tool1"]
        assert response.error is None
        assert response.retry_count == 0

    def test_response_defaults(self):
        """Test default values for response fields."""
        response = AgentResponse(
            agent_role=AgentRole.SENIOR_DEVELOPER,
            query="Test query",
            timestamp="2024-01-01T00:00:00",
            duration_seconds=1.5,
            response_text="Test response"
        )

        assert response.citations == []
        assert response.confidence == 0.8
        assert response.tokens_used == 0
        assert response.suggested_questions == []
        assert response.tools_used == []
        assert response.error is None
        assert response.retry_count == 0

    def test_response_to_dict(self):
        """Test response serialization to dict."""
        citation = Citation(
            artifact_id="art-123",
            file_path="/path/to/file.java"
        )

        response = AgentResponse(
            agent_role=AgentRole.DATA_ANALYST,
            query="Test query",
            timestamp="2024-01-01T00:00:00",
            duration_seconds=2.0,
            response_text="Test response",
            citations=[citation],
            suggested_questions=["Q1"]
        )

        result = response.to_dict()

        assert result["agent_role"] == "Data Analyst"
        assert result["query"] == "Test query"
        assert result["response_text"] == "Test response"
        assert len(result["citations"]) == 1
        assert result["citations"][0]["artifact_id"] == "art-123"
        assert result["suggested_questions"] == ["Q1"]

    def test_response_has_error(self):
        """Test has_error method."""
        response_no_error = AgentResponse(
            agent_role=AgentRole.SENIOR_DEVELOPER,
            query="Test",
            timestamp="2024-01-01T00:00:00",
            duration_seconds=1.0,
            response_text="OK"
        )

        response_with_error = AgentResponse(
            agent_role=AgentRole.SENIOR_DEVELOPER,
            query="Test",
            timestamp="2024-01-01T00:00:00",
            duration_seconds=1.0,
            response_text="",
            error="Something went wrong"
        )

        assert response_no_error.has_error() is False
        assert response_with_error.has_error() is True


class TestDefaultAgentConfigs:
    """Test default agent configurations."""

    def test_all_roles_have_configs(self):
        """Test that all agent roles have default configs."""
        assert len(DEFAULT_AGENT_CONFIGS) == 8

        for role in AgentRole:
            assert role in DEFAULT_AGENT_CONFIGS

    def test_senior_developer_config(self):
        """Test Senior Developer default config."""
        config = DEFAULT_AGENT_CONFIGS[AgentRole.SENIOR_DEVELOPER]

        assert config.role == AgentRole.SENIOR_DEVELOPER
        assert "architecture" in config.goal.lower() or "explain" in config.goal.lower()
        assert "senior" in config.backstory.lower()
        assert "WeaviateSearchTool" in config.tools
        assert "FileReadTool" in config.tools

    def test_data_analyst_config(self):
        """Test Data Analyst default config."""
        config = DEFAULT_AGENT_CONFIGS[AgentRole.DATA_ANALYST]

        assert config.role == AgentRole.DATA_ANALYST
        assert "database" in config.goal.lower() or "schema" in config.goal.lower()
        assert "database" in config.backstory.lower()
        assert "WeaviateSearchTool" in config.tools

    def test_prd_writer_config(self):
        """Test PRD Writer default config."""
        config = DEFAULT_AGENT_CONFIGS[AgentRole.PRD_WRITER]

        assert config.role == AgentRole.PRD_WRITER
        assert "prd" in config.goal.lower() or "requirements" in config.goal.lower()
        assert "product" in config.backstory.lower()
        assert "DocumentGeneratorTool" in config.tools

    def test_gherkin_test_writer_config(self):
        """Test Gherkin Test Writer default config."""
        config = DEFAULT_AGENT_CONFIGS[AgentRole.GHERKIN_TEST_WRITER]

        assert config.role == AgentRole.GHERKIN_TEST_WRITER
        assert "gherkin" in config.goal.lower() or "bdd" in config.goal.lower()
        assert "qa" in config.backstory.lower() or "test" in config.backstory.lower()
        assert "DocumentGeneratorTool" in config.tools

    def test_playwright_test_writer_config(self):
        """Test Playwright Test Writer default config."""
        config = DEFAULT_AGENT_CONFIGS[AgentRole.PLAYWRIGHT_TEST_WRITER]

        assert config.role == AgentRole.PLAYWRIGHT_TEST_WRITER
        assert "playwright" in config.goal.lower() or "e2e" in config.goal.lower()
        assert "automation" in config.backstory.lower() or "playwright" in config.backstory.lower()
        assert "DocumentGeneratorTool" in config.tools

    def test_all_configs_have_tools(self):
        """Test that all configs define tools."""
        for role, config in DEFAULT_AGENT_CONFIGS.items():
            assert len(config.tools) > 0, f"{role} has no tools defined"

    def test_all_configs_have_backstory(self):
        """Test that all configs have meaningful backstories."""
        for role, config in DEFAULT_AGENT_CONFIGS.items():
            assert len(config.backstory) > 50, f"{role} backstory too short"
            assert len(config.backstory.split()) > 10, f"{role} backstory needs more detail"


class TestGetAgentConfig:
    """Test get_agent_config function."""

    def test_get_config_no_overrides(self):
        """Test getting config without overrides."""
        config = get_agent_config(AgentRole.SENIOR_DEVELOPER)

        assert config.role == AgentRole.SENIOR_DEVELOPER
        assert config.llm_model == "gemma3:12b"  # Default

    def test_get_config_with_overrides(self):
        """Test getting config with overrides."""
        config = get_agent_config(
            AgentRole.SENIOR_DEVELOPER,
            verbose=False,
            llm_model="custom-model",
            temperature=0.5
        )

        assert config.role == AgentRole.SENIOR_DEVELOPER
        assert config.verbose is False
        assert config.llm_model == "custom-model"
        assert config.temperature == 0.5

    def test_get_config_preserves_unmodified(self):
        """Test that overrides don't affect unspecified fields."""
        config = get_agent_config(
            AgentRole.DATA_ANALYST,
            temperature=0.9
        )

        assert config.temperature == 0.9  # Override
        assert config.max_iterations == 10  # Default preserved
        assert config.llm_model == "gemma3:12b"  # Default preserved

    def test_get_config_invalid_role(self):
        """Test getting config for invalid role raises error."""
        # Create a mock invalid role (this is for testing error handling)
        with pytest.raises((ValueError, KeyError)):
            # Try to get config for a role not in DEFAULT_AGENT_CONFIGS
            get_agent_config(None)

    def test_get_config_override_tools(self):
        """Test overriding tools list."""
        config = get_agent_config(
            AgentRole.SENIOR_DEVELOPER,
            tools=["CustomTool1", "CustomTool2"]
        )

        assert config.tools == ["CustomTool1", "CustomTool2"]

    def test_get_config_does_not_mutate_defaults(self):
        """Test that getting config doesn't mutate default configs."""
        original_config = DEFAULT_AGENT_CONFIGS[AgentRole.SENIOR_DEVELOPER]
        original_model = original_config.llm_model

        # Get config with override
        modified_config = get_agent_config(
            AgentRole.SENIOR_DEVELOPER,
            llm_model="different-model"
        )

        # Check that default wasn't mutated
        assert DEFAULT_AGENT_CONFIGS[AgentRole.SENIOR_DEVELOPER].llm_model == original_model
        assert modified_config.llm_model == "different-model"


class TestAgentConfigIntegration:
    """Integration tests for agent configuration."""

    def test_create_response_from_config(self):
        """Test creating a response using a config."""
        config = get_agent_config(AgentRole.SENIOR_DEVELOPER)

        response = AgentResponse(
            agent_role=config.role,
            query="How does this work?",
            timestamp=datetime.now().isoformat(),
            duration_seconds=2.5,
            response_text="Here's how it works...",
            confidence=0.85
        )

        assert response.agent_role == AgentRole.SENIOR_DEVELOPER
        assert response.confidence == 0.85

    def test_multiple_configs_independent(self):
        """Test that multiple configs are independent."""
        config1 = get_agent_config(
            AgentRole.SENIOR_DEVELOPER,
            temperature=0.3
        )

        config2 = get_agent_config(
            AgentRole.DATA_ANALYST,
            temperature=0.9
        )

        assert config1.role != config2.role
        assert config1.temperature == 0.3
        assert config2.temperature == 0.9

    def test_config_dict_roundtrip(self):
        """Test config can be converted to dict and back."""
        original = get_agent_config(
            AgentRole.PRD_WRITER,
            temperature=0.6,
            max_tokens=1500
        )

        config_dict = original.to_dict()

        # Recreate config from dict (manually since we don't have from_dict method)
        recreated = AgentConfig(
            role=AgentRole(config_dict["role"]),
            goal=config_dict["goal"],
            backstory=config_dict["backstory"],
            temperature=config_dict["temperature"],
            max_tokens=config_dict["max_tokens"]
        )

        assert recreated.role == original.role
        assert recreated.temperature == original.temperature
        assert recreated.max_tokens == original.max_tokens
