"""
Unit tests for Backend Specialist agent (T081).

Tests agent configuration, backend artifact search, service analysis,
and response generation.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Any
from datetime import datetime


class TestBackendSpecialistAgent:
    """Test suite for Backend Specialist agent."""

    @pytest.fixture
    def agent_config(self):
        """Create test agent configuration."""
        from codeindex.web.agents.base import AgentConfig, AgentRole

        return AgentConfig(
            role=AgentRole.BACKEND_SPECIALIST,
            goal="Analyze backend services, business logic, and APIs",
            backstory="Test Backend Specialist agent for unit testing",
            temperature=0.3,
            max_tokens=2000
        )

    @pytest.fixture
    def backend_specialist(self, agent_config):
        """Create Backend Specialist agent instance."""
        from codeindex.web.agents.backend_specialist import BackendSpecialistAgent

        return BackendSpecialistAgent(agent_config)

    @pytest.fixture
    def mock_backend_artifacts(self) -> List[Dict[str, Any]]:
        """Create mock backend artifacts."""
        return [
            {
                "id": "service-001",
                "artifactType": "BackendDoc",
                "fileName": "UserService.java",
                "relativePath": "src/main/java/com/example/service/UserService.java",
                "summary": "User management service with CRUD operations",
                "entities": ["createUser", "updateUser", "deleteUser", "findUser"],
                "_additional": {"id": "service-001", "distance": 0.05}
            },
            {
                "id": "endpoint-001",
                "artifactType": "GwtEndpoint",
                "fileName": "UserServlet.java",
                "relativePath": "src/main/java/com/example/servlet/UserServlet.java",
                "summary": "GWT RPC servlet for user operations",
                "entities": ["getUserData", "saveUser", "deleteUser"],
                "_additional": {"id": "endpoint-001", "distance": 0.08}
            },
            {
                "id": "dao-001",
                "artifactType": "DaoCall",
                "fileName": "UserDAO.java",
                "relativePath": "src/main/java/com/example/dao/UserDAO.java",
                "summary": "Data access object for user table",
                "entities": ["findById", "save", "delete", "findAll"],
                "_additional": {"id": "dao-001", "distance": 0.10}
            }
        ]

    def test_agent_initialization_default_config(self):
        """Test agent initializes with default configuration."""
        from codeindex.web.agents.backend_specialist import BackendSpecialistAgent
        from codeindex.web.agents.base import AgentRole

        agent = BackendSpecialistAgent()

        assert agent.config is not None
        assert agent.role == AgentRole.BACKEND_SPECIALIST
        assert agent.config.role == AgentRole.BACKEND_SPECIALIST

    def test_agent_initialization_custom_config(self, agent_config):
        """Test agent initializes with custom configuration."""
        from codeindex.web.agents.backend_specialist import BackendSpecialistAgent

        agent = BackendSpecialistAgent(agent_config)

        assert agent.config == agent_config
        assert agent.config.temperature == 0.3
        assert agent.config.max_tokens == 2000

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_execute_query_success(
        self,
        mock_ollama,
        mock_get_search,
        backend_specialist,
        mock_backend_artifacts
    ):
        """Test successful query execution."""
        from codeindex.web.agents.base import AgentResponse

        # Mock search service
        mock_search = Mock()
        mock_search.search.return_value = {
            "results": mock_backend_artifacts,
            "total": 3
        }
        mock_get_search.return_value = mock_search

        # Mock Ollama response
        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {
            "response": "The UserService provides CRUD operations for user management..."
        }
        mock_ollama.return_value = mock_ollama_instance

        response = backend_specialist.execute_query("Explain the user service architecture")

        assert isinstance(response, AgentResponse)
        assert "UserService" in response.response_text or "CRUD" in response.response_text
        assert len(response.citations) > 0
        assert response.confidence > 0.0
        assert len(response.suggested_questions) > 0
        assert "WeaviateSearchTool" in response.tools_used

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_execute_query_with_error(
        self,
        mock_ollama,
        mock_get_search,
        backend_specialist
    ):
        """Test query execution with error handling."""
        # Mock search to fail
        mock_search = Mock()
        mock_search.search.side_effect = Exception("Weaviate connection failed")
        mock_get_search.return_value = mock_search

        response = backend_specialist.execute_query("What backend services exist?")

        assert response.error is not None
        assert "Weaviate connection failed" in response.error
        assert response.response_text == ""

    @patch('codeindex.web.services.search_service.get_search_service')
    def test_search_backend_artifacts(self, mock_get_search, backend_specialist, mock_backend_artifacts):
        """Test backend artifact search."""
        # Mock search service
        mock_search = Mock()
        mock_search.search.return_value = {
            "results": mock_backend_artifacts,
            "total": 3
        }
        mock_get_search.return_value = mock_search

        artifacts = backend_specialist._search_backend_artifacts("user service")

        assert len(artifacts) == 3
        assert any(a["artifactType"] == "BackendDoc" for a in artifacts)
        assert any(a["artifactType"] == "GwtEndpoint" for a in artifacts)
        assert any(a["artifactType"] == "DaoCall" for a in artifacts)

        # Verify search was called with correct parameters
        mock_search.search.assert_called_once()
        call_args = mock_search.search.call_args
        assert "BackendDoc" in call_args[1]["filters"]["artifact_types"]
        assert "GwtEndpoint" in call_args[1]["filters"]["artifact_types"]
        assert "DaoCall" in call_args[1]["filters"]["artifact_types"]

    @patch('codeindex.web.services.search_service.get_search_service')
    def test_search_backend_artifacts_empty_results(self, mock_get_search, backend_specialist):
        """Test backend artifact search with no results."""
        # Mock empty search results
        mock_search = Mock()
        mock_search.search.return_value = {"results": [], "total": 0}
        mock_get_search.return_value = mock_search

        artifacts = backend_specialist._search_backend_artifacts("nonexistent service")

        assert len(artifacts) == 0

    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_generate_backend_analysis(self, mock_ollama, backend_specialist, mock_backend_artifacts):
        """Test backend analysis generation."""
        # Mock Ollama response
        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {
            "response": "The backend architecture follows a layered pattern with services, controllers, and DAOs..."
        }
        mock_ollama.return_value = mock_ollama_instance

        analysis = backend_specialist._generate_backend_analysis(
            "Explain the backend architecture",
            mock_backend_artifacts,
            None
        )

        assert len(analysis) > 0
        assert "backend" in analysis.lower() or "architecture" in analysis.lower()

        # Verify Ollama was called with correct prompts
        mock_ollama_instance.call_ollama.assert_called_once()
        call_args = mock_ollama_instance.call_ollama.call_args
        assert "backend" in call_args[1]["prompt"].lower() or "service" in call_args[1]["prompt"].lower()
        assert "Backend Specialist" in call_args[1]["system_prompt"]

    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_generate_backend_analysis_with_context(
        self,
        mock_ollama,
        backend_specialist,
        mock_backend_artifacts
    ):
        """Test backend analysis with context."""
        # Mock Ollama response
        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {
            "response": "Based on the previous analysis, the service layer implements..."
        }
        mock_ollama.return_value = mock_ollama_instance

        context = {"previous_analysis": "User management module"}

        analysis = backend_specialist._generate_backend_analysis(
            "Continue analysis",
            mock_backend_artifacts,
            context
        )

        assert len(analysis) > 0

    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_generate_backend_analysis_fallback(self, mock_ollama, backend_specialist, mock_backend_artifacts):
        """Test fallback when Ollama fails."""
        # Mock Ollama to fail
        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.side_effect = Exception("Connection timeout")
        mock_ollama.return_value = mock_ollama_instance

        analysis = backend_specialist._generate_backend_analysis(
            "Explain services",
            mock_backend_artifacts,
            None
        )

        assert len(analysis) > 0
        assert "error" in analysis.lower() or "ensure" in analysis.lower()
        assert "BackendDoc" in analysis or "GwtEndpoint" in analysis

    def test_extract_citations(self, backend_specialist, mock_backend_artifacts):
        """Test citation extraction."""
        citations = backend_specialist._extract_citations(mock_backend_artifacts)

        assert len(citations) == 3
        assert all(c.artifact_id for c in citations)
        assert all(c.file_path for c in citations)
        assert all(c.artifact_type in ["BackendDoc", "GwtEndpoint", "DaoCall"] for c in citations)
        assert all(0.0 <= c.confidence <= 1.0 for c in citations)

    def test_extract_citations_limits_to_ten(self, backend_specialist):
        """Test citation extraction limits to 10 citations."""
        # Create 15 mock artifacts
        many_artifacts = [
            {
                "id": f"artifact-{i}",
                "artifactType": "BackendDoc",
                "fileName": f"Service{i}.java",
                "relativePath": f"src/Service{i}.java",
                "_additional": {"id": f"artifact-{i}", "distance": 0.05}
            }
            for i in range(15)
        ]

        citations = backend_specialist._extract_citations(many_artifacts)

        assert len(citations) == 10

    def test_generate_follow_ups_with_services(self, backend_specialist):
        """Test follow-up question generation with services."""
        artifacts = [
            {"artifactType": "BackendDoc", "fileName": "UserService.java"}
        ]

        questions = backend_specialist._generate_follow_ups("user service", artifacts)

        assert len(questions) > 0
        assert len(questions) <= 4
        assert any("transaction" in q.lower() or "validation" in q.lower() for q in questions)

    def test_generate_follow_ups_with_endpoints(self, backend_specialist):
        """Test follow-up question generation with endpoints."""
        artifacts = [
            {"artifactType": "GwtEndpoint", "fileName": "UserServlet.java"}
        ]

        questions = backend_specialist._generate_follow_ups("RPC endpoint", artifacts)

        assert len(questions) > 0
        assert any("rpc" in q.lower() or "dto" in q.lower() or "error" in q.lower() for q in questions)

    def test_generate_follow_ups_with_dao(self, backend_specialist):
        """Test follow-up question generation with DAOs."""
        artifacts = [
            {"artifactType": "DaoCall", "fileName": "UserDAO.java"}
        ]

        questions = backend_specialist._generate_follow_ups("data access", artifacts)

        assert len(questions) > 0
        assert any("dao" in q.lower() or "database" in q.lower() for q in questions)

    def test_generate_follow_ups_generic(self, backend_specialist):
        """Test generic follow-up questions."""
        artifacts = [
            {"artifactType": "Unknown", "fileName": "Unknown.java"}
        ]

        questions = backend_specialist._generate_follow_ups("backend code", artifacts)

        assert len(questions) > 0
        assert len(questions) <= 4

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_response_structure(
        self,
        mock_ollama,
        mock_get_search,
        backend_specialist,
        mock_backend_artifacts
    ):
        """Test response has all required fields."""
        # Mock dependencies
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_backend_artifacts, "total": 3}
        mock_get_search.return_value = mock_search

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {"response": "Backend analysis..."}
        mock_ollama.return_value = mock_ollama_instance

        response = backend_specialist.execute_query("Analyze backend")

        assert hasattr(response, "agent_role")
        assert hasattr(response, "query")
        assert hasattr(response, "timestamp")
        assert hasattr(response, "duration_seconds")
        assert hasattr(response, "response_text")
        assert hasattr(response, "citations")
        assert hasattr(response, "confidence")
        assert hasattr(response, "suggested_questions")
        assert hasattr(response, "tools_used")

    def test_singleton_pattern(self):
        """Test global Backend Specialist agent singleton."""
        from codeindex.web.agents.backend_specialist import get_backend_specialist_agent

        agent1 = get_backend_specialist_agent()
        agent2 = get_backend_specialist_agent()

        assert agent1 is agent2
