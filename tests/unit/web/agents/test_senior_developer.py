"""
Unit tests for Senior Developer Agent (T053 - US2.1).

Tests cover:
- Agent initialization with default and custom configuration
- Query execution and response generation
- Artifact search and context building
- LLM integration for code analysis
- Citation extraction and validation
- Error handling for service failures
- Follow-up question generation
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Any

from codeindex.web.agents.base import (
    AgentRole,
    AgentConfig,
    AgentResponse,
    Citation
)


@pytest.fixture
def mock_search_service():
    """Mock SearchService for Weaviate queries."""
    with patch('codeindex.web.services.search_service.get_search_service') as mock:
        service = MagicMock()
        mock.return_value = service
        yield service


@pytest.fixture
def mock_ollama_client():
    """Mock Ollama client for LLM queries."""
    with patch('codeindex.services.ollama_client.OllamaClient') as mock:
        client = MagicMock()
        mock.return_value = client
        yield client


@pytest.fixture
def sample_artifacts() -> List[Dict[str, Any]]:
    """Sample artifacts for testing."""
    return [
        {
            "artifactType": "BackendDoc",
            "id": "service_123",
            "relativePath": "src/services/UserService.java",
            "fileName": "UserService.java",
            "summary": "User management service with authentication and profile operations",
            "entities": ["User", "UserProfile", "AuthToken"],
            "confidence": 0.95
        },
        {
            "artifactType": "DaoCall",
            "id": "dao_456",
            "relativePath": "src/dao/UserDao.java",
            "fileName": "UserDao.java",
            "summary": "User data access object for database operations",
            "entities": ["User"],
            "confidence": 0.92
        },
        {
            "artifactType": "GwtPresenter",
            "id": "presenter_789",
            "relativePath": "src/client/UserPresenter.java",
            "fileName": "UserPresenter.java",
            "summary": "User management UI presenter with CRUD operations",
            "entities": ["UserPresenter", "UserDisplay"],
            "confidence": 0.89
        }
    ]


@pytest.fixture
def sample_llm_response() -> str:
    """Sample LLM response for code analysis."""
    return """## User Registration Module Overview

The user registration module is implemented using a multi-tier architecture:

### Components

1. **UserService** (`src/services/UserService.java`):
   - Handles user authentication and profile management
   - Implements validation logic for user data
   - Manages session tokens and security

2. **UserDao** (`src/dao/UserDao.java`):
   - Provides database access layer for user data
   - Implements CRUD operations
   - Handles transaction management

3. **UserPresenter** (`src/client/UserPresenter.java`):
   - GWT MVP presenter for user management UI
   - Coordinates between UI and backend services
   - Handles user interactions and validation

### Data Flow

1. User submits registration form → UserPresenter
2. UserPresenter validates input → calls UserService RPC
3. UserService validates business rules → calls UserDao
4. UserDao persists user to database → returns User entity
5. UserService generates AuthToken → returns to UserPresenter
6. UserPresenter updates UI with success/error message

### Design Patterns

- **MVP Pattern**: Separation of UI logic (Presenter) from view (Display interface)
- **DAO Pattern**: Abstraction of database access
- **Service Layer**: Business logic isolation

### Dependencies

- User entity depends on: UserProfile, AuthToken
- UserService depends on: UserDao, ValidationService
- UserPresenter depends on: UserService (via GWT RPC)
"""


class TestSeniorDeveloperAgentInitialization:
    """Test agent initialization and configuration."""

    def test_agent_initializes_with_default_config(self):
        """Test agent initialization with default configuration."""
        from codeindex.web.agents.senior_developer import SeniorDeveloperAgent

        agent = SeniorDeveloperAgent()

        assert agent.role == AgentRole.SENIOR_DEVELOPER
        assert agent.config is not None
        assert agent.config.role == AgentRole.SENIOR_DEVELOPER
        assert "architecture" in agent.config.goal.lower()
        assert "15+ years" in agent.config.backstory

    def test_agent_initializes_with_custom_config(self):
        """Test agent initialization with custom configuration."""
        from codeindex.web.agents.senior_developer import SeniorDeveloperAgent
        from codeindex.web.agents.base import get_agent_config

        custom_config = get_agent_config(
            AgentRole.SENIOR_DEVELOPER,
            verbosity="verbose",
            technical_level="junior",
            temperature=0.5
        )

        agent = SeniorDeveloperAgent(config=custom_config)

        assert agent.config.verbosity == "verbose"
        assert agent.config.technical_level == "junior"
        assert agent.config.temperature == 0.5

    def test_agent_config_has_correct_tools(self):
        """Test agent configuration includes required tools."""
        from codeindex.web.agents.senior_developer import SeniorDeveloperAgent

        agent = SeniorDeveloperAgent()

        assert "WeaviateSearchTool" in agent.config.tools
        assert "FileReadTool" in agent.config.tools
        assert "LLMQueryTool" in agent.config.tools


class TestSeniorDeveloperAgentQueryExecution:
    """Test agent query execution and response generation."""

    def test_execute_query_returns_agent_response(
        self,
        mock_search_service,
        mock_ollama_client,
        sample_artifacts,
        sample_llm_response
    ):
        """Test basic query execution returns AgentResponse."""
        from codeindex.web.agents.senior_developer import SeniorDeveloperAgent

        # Mock search results
        mock_search_service.search.return_value = {
            "results": sample_artifacts,
            "total": 3
        }

        # Mock Ollama response
        mock_ollama_client.generate.return_value = sample_llm_response

        agent = SeniorDeveloperAgent()
        response = agent.execute_query("What does the user registration module do?")

        assert isinstance(response, AgentResponse)
        assert response.agent_role == AgentRole.SENIOR_DEVELOPER
        assert response.query == "What does the user registration module do?"
        assert response.response_text == sample_llm_response
        assert response.duration_seconds > 0
        assert response.error is None

    def test_execute_query_searches_for_artifacts(
        self,
        mock_search_service,
        mock_ollama_client,
        sample_llm_response
    ):
        """Test query execution searches for relevant artifacts."""
        from codeindex.web.agents.senior_developer import SeniorDeveloperAgent

        mock_search_service.search.return_value = {
            "results": [],
            "total": 0
        }
        mock_ollama_client.generate.return_value = sample_llm_response

        agent = SeniorDeveloperAgent()
        agent.execute_query("Explain authentication flow")

        # Verify search was called with query
        mock_search_service.search.assert_called_once()
        call_args = mock_search_service.search.call_args
        assert call_args[1]["query"] == "Explain authentication flow"
        assert call_args[1]["limit"] >= 10  # Should get multiple results

    def test_execute_query_generates_llm_analysis(
        self,
        mock_search_service,
        mock_ollama_client,
        sample_artifacts,
        sample_llm_response
    ):
        """Test query execution generates analysis using LLM."""
        from codeindex.web.agents.senior_developer import SeniorDeveloperAgent

        mock_search_service.search.return_value = {
            "results": sample_artifacts,
            "total": 3
        }
        mock_ollama_client.generate.return_value = sample_llm_response

        agent = SeniorDeveloperAgent()
        agent.execute_query("Analyze user service architecture")

        # Verify LLM was called
        mock_ollama_client.generate.assert_called_once()

        # Verify LLM prompt includes artifacts
        call_args = mock_ollama_client.generate.call_args[0][0]
        assert "UserService" in call_args
        assert "architecture" in call_args.lower()

    def test_execute_query_extracts_citations(
        self,
        mock_search_service,
        mock_ollama_client,
        sample_artifacts,
        sample_llm_response
    ):
        """Test query execution extracts citations from artifacts."""
        from codeindex.web.agents.senior_developer import SeniorDeveloperAgent

        mock_search_service.search.return_value = {
            "results": sample_artifacts,
            "total": 3
        }
        mock_ollama_client.generate.return_value = sample_llm_response

        agent = SeniorDeveloperAgent()
        response = agent.execute_query("Explain user module")

        # Verify citations extracted
        assert len(response.citations) > 0
        assert any(c.file_path == "src/services/UserService.java" for c in response.citations)
        assert any(c.artifact_id == "service_123" for c in response.citations)

    def test_execute_query_generates_follow_up_questions(
        self,
        mock_search_service,
        mock_ollama_client,
        sample_artifacts,
        sample_llm_response
    ):
        """Test query execution generates follow-up questions."""
        from codeindex.web.agents.senior_developer import SeniorDeveloperAgent

        mock_search_service.search.return_value = {
            "results": sample_artifacts,
            "total": 3
        }
        mock_ollama_client.generate.return_value = sample_llm_response

        agent = SeniorDeveloperAgent()
        response = agent.execute_query("What does the user service do?")

        # Verify follow-up questions generated
        assert len(response.suggested_questions) > 0
        assert any("authentication" in q.lower() or "security" in q.lower() for q in response.suggested_questions)

    def test_execute_query_includes_tools_used(
        self,
        mock_search_service,
        mock_ollama_client,
        sample_artifacts,
        sample_llm_response
    ):
        """Test query execution tracks tools used."""
        from codeindex.web.agents.senior_developer import SeniorDeveloperAgent

        mock_search_service.search.return_value = {
            "results": sample_artifacts,
            "total": 3
        }
        mock_ollama_client.generate.return_value = sample_llm_response

        agent = SeniorDeveloperAgent()
        response = agent.execute_query("Analyze code structure")

        # Verify tools tracked
        assert len(response.tools_used) > 0
        assert "WeaviateSearchTool" in response.tools_used
        assert "LLMQueryTool" in response.tools_used


class TestSeniorDeveloperAgentContextHandling:
    """Test agent context passing and conversation continuity."""

    def test_execute_query_with_context(
        self,
        mock_search_service,
        mock_ollama_client,
        sample_artifacts,
        sample_llm_response
    ):
        """Test query execution with conversation context."""
        from codeindex.web.agents.senior_developer import SeniorDeveloperAgent

        mock_search_service.search.return_value = {
            "results": sample_artifacts,
            "total": 3
        }
        mock_ollama_client.generate.return_value = sample_llm_response

        agent = SeniorDeveloperAgent()

        context = {
            "previous_query": "What does UserService do?",
            "previous_response": "UserService manages authentication and profiles",
            "artifacts": sample_artifacts[:2]
        }

        response = agent.execute_query("How does it handle authentication?", context=context)

        # Verify response generated with context
        assert response.error is None
        assert len(response.response_text) > 0

        # Verify LLM prompt included context
        call_args = mock_ollama_client.generate.call_args[0][0]
        assert "authentication" in call_args.lower()


class TestSeniorDeveloperAgentErrorHandling:
    """Test agent error handling for service failures."""

    def test_execute_query_handles_search_service_error(
        self,
        mock_search_service,
        mock_ollama_client
    ):
        """Test query execution handles search service errors gracefully."""
        from codeindex.web.agents.senior_developer import SeniorDeveloperAgent

        # Mock search service error
        mock_search_service.search.side_effect = Exception("Weaviate unavailable")

        agent = SeniorDeveloperAgent()
        response = agent.execute_query("Analyze user module")

        # Verify error response
        assert response.has_error()
        assert "Weaviate" in response.error or "unavailable" in response.error.lower()
        assert response.response_text == ""

    def test_execute_query_handles_ollama_error(
        self,
        mock_search_service,
        mock_ollama_client,
        sample_artifacts
    ):
        """Test query execution handles Ollama errors gracefully."""
        from codeindex.web.agents.senior_developer import SeniorDeveloperAgent

        mock_search_service.search.return_value = {
            "results": sample_artifacts,
            "total": 3
        }

        # Mock Ollama error
        mock_ollama_client.generate.side_effect = Exception("Ollama timeout")

        agent = SeniorDeveloperAgent()
        response = agent.execute_query("Explain code architecture")

        # Verify error response
        assert response.has_error()
        assert "Ollama" in response.error or "timeout" in response.error.lower()
        assert response.response_text == ""

    def test_execute_query_handles_empty_search_results(
        self,
        mock_search_service,
        mock_ollama_client
    ):
        """Test query execution handles empty search results gracefully."""
        from codeindex.web.agents.senior_developer import SeniorDeveloperAgent

        # Mock empty search results
        mock_search_service.search.return_value = {
            "results": [],
            "total": 0
        }

        mock_ollama_client.generate.return_value = "No relevant artifacts found in codebase."

        agent = SeniorDeveloperAgent()
        response = agent.execute_query("Find nonexistent module")

        # Verify response with no artifacts
        assert not response.has_error()
        assert len(response.citations) == 0
        assert "No relevant artifacts" in response.response_text or len(response.response_text) > 0


class TestSeniorDeveloperAgentOutputFormatting:
    """Test agent output formatting based on configuration."""

    def test_execute_query_respects_verbosity_setting(
        self,
        mock_search_service,
        mock_ollama_client,
        sample_artifacts
    ):
        """Test query execution respects verbosity setting."""
        from codeindex.web.agents.senior_developer import SeniorDeveloperAgent
        from codeindex.web.agents.base import get_agent_config

        mock_search_service.search.return_value = {
            "results": sample_artifacts,
            "total": 3
        }
        mock_ollama_client.generate.return_value = "Brief response."

        # Test concise verbosity
        config = get_agent_config(AgentRole.SENIOR_DEVELOPER, verbosity="concise")
        agent = SeniorDeveloperAgent(config=config)
        agent.execute_query("Explain UserService")

        # Verify prompt includes verbosity instructions
        call_args = mock_ollama_client.generate.call_args[0][0]
        assert "concise" in call_args.lower() or "brief" in call_args.lower()

    def test_execute_query_respects_technical_level_setting(
        self,
        mock_search_service,
        mock_ollama_client,
        sample_artifacts
    ):
        """Test query execution respects technical level setting."""
        from codeindex.web.agents.senior_developer import SeniorDeveloperAgent
        from codeindex.web.agents.base import get_agent_config

        mock_search_service.search.return_value = {
            "results": sample_artifacts,
            "total": 3
        }
        mock_ollama_client.generate.return_value = "Junior-friendly explanation."

        # Test junior technical level
        config = get_agent_config(AgentRole.SENIOR_DEVELOPER, technical_level="junior")
        agent = SeniorDeveloperAgent(config=config)
        agent.execute_query("What is UserService?")

        # Verify prompt includes technical level instructions
        call_args = mock_ollama_client.generate.call_args[0][0]
        assert "junior" in call_args.lower() or "beginner" in call_args.lower() or "simple" in call_args.lower()


class TestSeniorDeveloperAgentPerformance:
    """Test agent performance and efficiency."""

    def test_execute_query_completes_within_timeout(
        self,
        mock_search_service,
        mock_ollama_client,
        sample_artifacts,
        sample_llm_response
    ):
        """Test query execution completes within reasonable time."""
        from codeindex.web.agents.senior_developer import SeniorDeveloperAgent

        mock_search_service.search.return_value = {
            "results": sample_artifacts,
            "total": 3
        }
        mock_ollama_client.generate.return_value = sample_llm_response

        agent = SeniorDeveloperAgent()
        response = agent.execute_query("Analyze UserService")

        # Verify reasonable duration (mocked, so should be very fast)
        assert response.duration_seconds < 60  # Max 60 seconds (lenient for tests)
        assert response.duration_seconds >= 0

    def test_execute_query_tracks_confidence_score(
        self,
        mock_search_service,
        mock_ollama_client,
        sample_artifacts,
        sample_llm_response
    ):
        """Test query execution tracks confidence score."""
        from codeindex.web.agents.senior_developer import SeniorDeveloperAgent

        mock_search_service.search.return_value = {
            "results": sample_artifacts,
            "total": 3
        }
        mock_ollama_client.generate.return_value = sample_llm_response

        agent = SeniorDeveloperAgent()
        response = agent.execute_query("Explain architecture")

        # Verify confidence score
        assert 0.0 <= response.confidence <= 1.0
        assert response.confidence > 0.5  # Should have reasonable confidence with artifacts


# Test fixtures and helpers

def test_sample_artifacts_fixture_structure(sample_artifacts):
    """Test sample_artifacts fixture has correct structure."""
    assert len(sample_artifacts) == 3
    assert all("artifactType" in a for a in sample_artifacts)
    assert all("id" in a for a in sample_artifacts)
    assert all("relativePath" in a for a in sample_artifacts)


def test_sample_llm_response_fixture_content(sample_llm_response):
    """Test sample_llm_response fixture has expected content."""
    assert len(sample_llm_response) > 100
    assert "UserService" in sample_llm_response
    assert "architecture" in sample_llm_response.lower()
    assert "Data Flow" in sample_llm_response or "data flow" in sample_llm_response.lower()
