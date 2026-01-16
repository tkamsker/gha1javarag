"""
Unit tests for Frontend Specialist agent (T082).

Tests agent configuration, frontend artifact search, GWT/JSP analysis,
and response generation.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Any
from datetime import datetime


class TestFrontendSpecialistAgent:
    """Test suite for Frontend Specialist agent."""

    @pytest.fixture
    def agent_config(self):
        """Create test agent configuration."""
        from codeindex.web.agents.base import AgentConfig, AgentRole

        return AgentConfig(
            role=AgentRole.FRONTEND_SPECIALIST,
            goal="Analyze frontend UI, GWT applications, and client-side code",
            backstory="Test Frontend Specialist agent for unit testing",
            temperature=0.3,
            max_tokens=2000
        )

    @pytest.fixture
    def frontend_specialist(self, agent_config):
        """Create Frontend Specialist agent instance."""
        from codeindex.web.agents.frontend_specialist import FrontendSpecialistAgent

        return FrontendSpecialistAgent(agent_config)

    @pytest.fixture
    def mock_frontend_artifacts(self) -> List[Dict[str, Any]]:
        """Create mock frontend artifacts."""
        return [
            {
                "id": "presenter-001",
                "artifactType": "GwtPresenter",
                "fileName": "UserPresenter.java",
                "relativePath": "src/main/java/com/example/client/presenter/UserPresenter.java",
                "summary": "GWT Presenter for user management with event handlers",
                "entities": ["onEditUser", "onSaveUser", "onDeleteUser"],
                "_additional": {"id": "presenter-001", "distance": 0.05}
            },
            {
                "id": "view-001",
                "artifactType": "GwtView",
                "fileName": "UserView.java",
                "relativePath": "src/main/java/com/example/client/view/UserView.java",
                "summary": "GWT View interface with UI widgets",
                "entities": ["getUserName", "getEmail", "getSaveButton"],
                "_additional": {"id": "view-001", "distance": 0.08}
            },
            {
                "id": "uibinder-001",
                "artifactType": "GwtUiBinder",
                "fileName": "UserView.ui.xml",
                "relativePath": "src/main/java/com/example/client/view/UserView.ui.xml",
                "summary": "UiBinder template with form fields",
                "entities": ["userNameField", "emailField", "saveButton"],
                "_additional": {"id": "uibinder-001", "distance": 0.10}
            },
            {
                "id": "jsp-001",
                "artifactType": "JspForm",
                "fileName": "login.jsp",
                "relativePath": "src/main/webapp/login.jsp",
                "summary": "Login form with username and password fields",
                "entities": ["username", "password", "loginButton"],
                "_additional": {"id": "jsp-001", "distance": 0.12}
            }
        ]

    def test_agent_initialization_default_config(self):
        """Test agent initializes with default configuration."""
        from codeindex.web.agents.frontend_specialist import FrontendSpecialistAgent
        from codeindex.web.agents.base import AgentRole

        agent = FrontendSpecialistAgent()

        assert agent.config is not None
        assert agent.role == AgentRole.FRONTEND_SPECIALIST
        assert agent.config.role == AgentRole.FRONTEND_SPECIALIST

    def test_agent_initialization_custom_config(self, agent_config):
        """Test agent initializes with custom configuration."""
        from codeindex.web.agents.frontend_specialist import FrontendSpecialistAgent

        agent = FrontendSpecialistAgent(agent_config)

        assert agent.config == agent_config
        assert agent.config.temperature == 0.3
        assert agent.config.max_tokens == 2000

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_execute_query_success(
        self,
        mock_ollama,
        mock_get_search,
        frontend_specialist,
        mock_frontend_artifacts
    ):
        """Test successful query execution."""
        from codeindex.web.agents.base import AgentResponse

        # Mock search service
        mock_search = Mock()
        mock_search.search.return_value = {
            "results": mock_frontend_artifacts,
            "total": 4
        }
        mock_get_search.return_value = mock_search

        # Mock Ollama response
        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {
            "response": "The UserPresenter follows the GWT MVP pattern with event handlers..."
        }
        mock_ollama.return_value = mock_ollama_instance

        response = frontend_specialist.execute_query("Explain the user presenter architecture")

        assert isinstance(response, AgentResponse)
        assert len(response.response_text) > 0
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
        frontend_specialist
    ):
        """Test query execution with error handling."""
        # Mock search to fail
        mock_search = Mock()
        mock_search.search.side_effect = Exception("Weaviate connection failed")
        mock_get_search.return_value = mock_search

        response = frontend_specialist.execute_query("What frontend components exist?")

        assert response.error is not None
        assert "Weaviate connection failed" in response.error
        assert response.response_text == ""

    @patch('codeindex.web.services.search_service.get_search_service')
    def test_search_frontend_artifacts(self, mock_get_search, frontend_specialist, mock_frontend_artifacts):
        """Test frontend artifact search."""
        # Mock search service
        mock_search = Mock()
        mock_search.search.return_value = {
            "results": mock_frontend_artifacts,
            "total": 4
        }
        mock_get_search.return_value = mock_search

        artifacts = frontend_specialist._search_frontend_artifacts("user presenter")

        assert len(artifacts) == 4
        assert any(a["artifactType"] == "GwtPresenter" for a in artifacts)
        assert any(a["artifactType"] == "GwtView" for a in artifacts)
        assert any(a["artifactType"] == "GwtUiBinder" for a in artifacts)
        assert any(a["artifactType"] == "JspForm" for a in artifacts)

        # Verify search was called with correct parameters
        mock_search.search.assert_called_once()
        call_args = mock_search.search.call_args
        assert "GwtPresenter" in call_args[1]["filters"]["artifact_types"]
        assert "GwtView" in call_args[1]["filters"]["artifact_types"]
        assert "GwtUiBinder" in call_args[1]["filters"]["artifact_types"]
        assert "JspForm" in call_args[1]["filters"]["artifact_types"]

    @patch('codeindex.web.services.search_service.get_search_service')
    def test_search_frontend_artifacts_empty_results(self, mock_get_search, frontend_specialist):
        """Test frontend artifact search with no results."""
        # Mock empty search results
        mock_search = Mock()
        mock_search.search.return_value = {"results": [], "total": 0}
        mock_get_search.return_value = mock_search

        artifacts = frontend_specialist._search_frontend_artifacts("nonexistent component")

        assert len(artifacts) == 0

    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_generate_frontend_analysis(self, mock_ollama, frontend_specialist, mock_frontend_artifacts):
        """Test frontend analysis generation."""
        # Mock Ollama response
        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {
            "response": "The frontend architecture follows the GWT MVP pattern with Presenters, Views, and UiBinder templates..."
        }
        mock_ollama.return_value = mock_ollama_instance

        analysis = frontend_specialist._generate_frontend_analysis(
            "Explain the frontend architecture",
            mock_frontend_artifacts,
            None
        )

        assert len(analysis) > 0
        assert "frontend" in analysis.lower() or "gwt" in analysis.lower() or "mvp" in analysis.lower()

        # Verify Ollama was called with correct prompts
        mock_ollama_instance.call_ollama.assert_called_once()
        call_args = mock_ollama_instance.call_ollama.call_args
        assert "frontend" in call_args[1]["prompt"].lower() or "gwt" in call_args[1]["prompt"].lower()
        assert "Frontend Specialist" in call_args[1]["system_prompt"]

    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_generate_frontend_analysis_with_context(
        self,
        mock_ollama,
        frontend_specialist,
        mock_frontend_artifacts
    ):
        """Test frontend analysis with context."""
        # Mock Ollama response
        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {
            "response": "Based on the previous analysis, the presenter implements event handlers..."
        }
        mock_ollama.return_value = mock_ollama_instance

        context = {"previous_analysis": "User management UI"}

        analysis = frontend_specialist._generate_frontend_analysis(
            "Continue analysis",
            mock_frontend_artifacts,
            context
        )

        assert len(analysis) > 0

    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_generate_frontend_analysis_fallback(self, mock_ollama, frontend_specialist, mock_frontend_artifacts):
        """Test fallback when Ollama fails."""
        # Mock Ollama to fail
        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.side_effect = Exception("Connection timeout")
        mock_ollama.return_value = mock_ollama_instance

        analysis = frontend_specialist._generate_frontend_analysis(
            "Explain presenters",
            mock_frontend_artifacts,
            None
        )

        assert len(analysis) > 0
        assert "error" in analysis.lower() or "ensure" in analysis.lower()
        assert "GwtPresenter" in analysis or "GwtView" in analysis

    def test_extract_citations(self, frontend_specialist, mock_frontend_artifacts):
        """Test citation extraction."""
        citations = frontend_specialist._extract_citations(mock_frontend_artifacts)

        assert len(citations) == 4
        assert all(c.artifact_id for c in citations)
        assert all(c.file_path for c in citations)
        assert all(c.artifact_type in ["GwtPresenter", "GwtView", "GwtUiBinder", "JspForm"] for c in citations)
        assert all(0.0 <= c.confidence <= 1.0 for c in citations)

    def test_extract_citations_limits_to_ten(self, frontend_specialist):
        """Test citation extraction limits to 10 citations."""
        # Create 15 mock artifacts
        many_artifacts = [
            {
                "id": f"artifact-{i}",
                "artifactType": "GwtPresenter",
                "fileName": f"Presenter{i}.java",
                "relativePath": f"src/Presenter{i}.java",
                "_additional": {"id": f"artifact-{i}", "distance": 0.05}
            }
            for i in range(15)
        ]

        citations = frontend_specialist._extract_citations(many_artifacts)

        assert len(citations) == 10

    def test_generate_follow_ups_with_presenters(self, frontend_specialist):
        """Test follow-up question generation with presenters."""
        artifacts = [
            {"artifactType": "GwtPresenter", "fileName": "UserPresenter.java"}
        ]

        questions = frontend_specialist._generate_follow_ups("user presenter", artifacts)

        assert len(questions) > 0
        assert len(questions) <= 4
        assert any("event" in q.lower() or "view" in q.lower() or "bind" in q.lower() for q in questions)

    def test_generate_follow_ups_with_views(self, frontend_specialist):
        """Test follow-up question generation with views."""
        artifacts = [
            {"artifactType": "GwtView", "fileName": "UserView.java"}
        ]

        questions = frontend_specialist._generate_follow_ups("user view", artifacts)

        assert len(questions) > 0
        assert any("widget" in q.lower() or "ui" in q.lower() or "presenter" in q.lower() for q in questions)

    def test_generate_follow_ups_with_uibinder(self, frontend_specialist):
        """Test follow-up question generation with UiBinder."""
        artifacts = [
            {"artifactType": "GwtUiBinder", "fileName": "UserView.ui.xml"}
        ]

        questions = frontend_specialist._generate_follow_ups("ui template", artifacts)

        assert len(questions) > 0
        assert any("template" in q.lower() or "field" in q.lower() or "widget" in q.lower() for q in questions)

    def test_generate_follow_ups_with_jsp(self, frontend_specialist):
        """Test follow-up question generation with JSP forms."""
        artifacts = [
            {"artifactType": "JspForm", "fileName": "login.jsp"}
        ]

        questions = frontend_specialist._generate_follow_ups("jsp form", artifacts)

        assert len(questions) > 0
        assert any("form" in q.lower() or "field" in q.lower() or "submit" in q.lower() for q in questions)

    def test_generate_follow_ups_generic(self, frontend_specialist):
        """Test generic follow-up questions."""
        artifacts = [
            {"artifactType": "Unknown", "fileName": "Unknown.java"}
        ]

        questions = frontend_specialist._generate_follow_ups("frontend code", artifacts)

        assert len(questions) > 0
        assert len(questions) <= 4

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_response_structure(
        self,
        mock_ollama,
        mock_get_search,
        frontend_specialist,
        mock_frontend_artifacts
    ):
        """Test response has all required fields."""
        # Mock dependencies
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_frontend_artifacts, "total": 4}
        mock_get_search.return_value = mock_search

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {"response": "Frontend analysis..."}
        mock_ollama.return_value = mock_ollama_instance

        response = frontend_specialist.execute_query("Analyze frontend")

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
        """Test global Frontend Specialist agent singleton."""
        from codeindex.web.agents.frontend_specialist import get_frontend_specialist_agent

        agent1 = get_frontend_specialist_agent()
        agent2 = get_frontend_specialist_agent()

        assert agent1 is agent2
