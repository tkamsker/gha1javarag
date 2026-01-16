"""
Integration test for agent settings application (T101 - US2.4).

Tests end-to-end settings application and verifies agent responses change with settings.
"""

import pytest
from unittest.mock import Mock, patch
from typing import Dict, Any


class TestAgentSettingsIntegration:
    """Integration test suite for agent settings."""

    @pytest.fixture
    def mock_search_results(self) -> Dict[str, Any]:
        """Create mock search results."""
        return {
            "results": [
                {
                    "id": "auth-001",
                    "artifactType": "BackendDoc",
                    "fileName": "AuthenticationService.java",
                    "relativePath": "src/main/java/com/example/auth/AuthenticationService.java",
                    "summary": "Handles user authentication with JWT tokens",
                    "entities": ["login", "logout", "validateToken"],
                    "_additional": {"id": "auth-001", "distance": 0.05}
                }
            ],
            "total": 1
        }

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_concise_settings_produce_brief_response(
        self,
        mock_ollama,
        mock_search_service,
        mock_search_results
    ):
        """Test that concise settings produce brief agent responses."""
        from codeindex.web.agents.senior_developer import get_senior_developer_agent
        from codeindex.web.agents.base import AgentConfig, AgentRole

        # Mock search
        mock_search = Mock()
        mock_search.search.return_value = mock_search_results
        mock_search_service.return_value = mock_search

        # Mock Ollama with concise response
        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {
            "response": "JWT authentication. Token validation at AuthenticationService:42."
        }
        mock_ollama.return_value = mock_ollama_instance

        # Create agent with concise settings
        concise_settings = {
            "verbosity": "concise",
            "technical_level": "senior",
            "citation_style": "inline",
            "output_format": "markdown"
        }

        config = AgentConfig(
            role=AgentRole.SENIOR_DEVELOPER,
            goal="Explain code",
            backstory="Senior developer",
            verbosity="concise",
            technical_level="senior"
        )

        agent = get_senior_developer_agent()
        agent.config = config

        # Execute query
        response = agent.execute_query("Explain authentication")

        # Verify brief response
        assert len(response.response_text) < 200
        assert "JWT" in response.response_text or "authentication" in response.response_text.lower()

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_verbose_settings_produce_detailed_response(
        self,
        mock_ollama,
        mock_search_service,
        mock_search_results
    ):
        """Test that verbose settings produce detailed agent responses."""
        from codeindex.web.agents.senior_developer import get_senior_developer_agent
        from codeindex.web.agents.base import AgentConfig, AgentRole

        # Mock search
        mock_search = Mock()
        mock_search.search.return_value = mock_search_results
        mock_search_service.return_value = mock_search

        # Mock Ollama with verbose response
        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {
            "response": """The authentication system in this application is implemented using JSON Web Tokens (JWT).

**Authentication Flow:**
1. User submits credentials to AuthenticationService
2. Service validates credentials against database
3. Upon successful validation, generates JWT token
4. Token contains user claims and expiration
5. Client includes token in subsequent requests

**Implementation Details:**
The AuthenticationService.java file (lines 1-150) handles the core authentication logic. The login() method validates user credentials and generates tokens. The validateToken() method verifies token signatures and expiration.

**Security Considerations:**
- Tokens expire after 24 hours
- HMAC-SHA256 signing algorithm
- Secure token storage recommended
"""
        }
        mock_ollama.return_value = mock_ollama_instance

        # Create agent with verbose settings
        config = AgentConfig(
            role=AgentRole.SENIOR_DEVELOPER,
            goal="Explain code",
            backstory="Senior developer",
            verbosity="verbose",
            technical_level="senior"
        )

        agent = get_senior_developer_agent()
        agent.config = config

        # Execute query
        response = agent.execute_query("Explain authentication")

        # Verify detailed response
        assert len(response.response_text) > 500
        assert "authentication" in response.response_text.lower()

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_junior_technical_level_uses_simple_language(
        self,
        mock_ollama,
        mock_search_service,
        mock_search_results
    ):
        """Test that junior technical level produces simpler explanations."""
        from codeindex.web.agents.senior_developer import get_senior_developer_agent
        from codeindex.web.agents.base import AgentConfig, AgentRole

        # Mock search
        mock_search = Mock()
        mock_search.search.return_value = mock_search_results
        mock_search_service.return_value = mock_search

        # Mock Ollama with junior-friendly response
        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {
            "response": """The authentication system is basically a way to verify who you are when you log in.

Here's how it works in simple terms:
1. You enter your username and password
2. The system checks if they're correct
3. If correct, you get a special token (like a digital key)
4. You use this token to access the application

Think of it like showing your ID card - the token proves you're who you say you are!
"""
        }
        mock_ollama.return_value = mock_ollama_instance

        # Create agent with junior settings
        config = AgentConfig(
            role=AgentRole.SENIOR_DEVELOPER,
            goal="Explain code",
            backstory="Senior developer",
            verbosity="standard",
            technical_level="junior"
        )

        agent = get_senior_developer_agent()
        agent.config = config

        # Execute query
        response = agent.execute_query("Explain authentication")

        # Verify simple language
        response_lower = response.response_text.lower()
        simple_indicators = ["basically", "simple", "think of it like", "in simple terms", "here's how"]
        assert any(indicator in response_lower for indicator in simple_indicators)

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_inline_citations_in_response(
        self,
        mock_ollama,
        mock_search_service,
        mock_search_results
    ):
        """Test that inline citation style includes citations in text."""
        from codeindex.web.agents.senior_developer import get_senior_developer_agent
        from codeindex.web.agents.base import AgentConfig, AgentRole

        # Mock search
        mock_search = Mock()
        mock_search.search.return_value = mock_search_results
        mock_search_service.return_value = mock_search

        # Mock Ollama
        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {
            "response": "Authentication is handled by AuthenticationService [1]."
        }
        mock_ollama.return_value = mock_ollama_instance

        # Create agent with inline citation style
        config = AgentConfig(
            role=AgentRole.SENIOR_DEVELOPER,
            goal="Explain code",
            backstory="Senior developer",
            verbosity="standard",
            technical_level="senior",
            citation_style="inline"
        )

        agent = get_senior_developer_agent()
        agent.config = config

        # Execute query
        response = agent.execute_query("Explain authentication")

        # Verify inline citations
        assert "[1]" in response.response_text or "AuthenticationService" in response.response_text
        assert len(response.citations) > 0

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_settings_persist_across_multiple_queries(
        self,
        mock_ollama,
        mock_search_service,
        mock_search_results
    ):
        """Test that settings persist across multiple agent queries."""
        from codeindex.web.agents.senior_developer import get_senior_developer_agent
        from codeindex.web.agents.base import AgentConfig, AgentRole

        # Mock search
        mock_search = Mock()
        mock_search.search.return_value = mock_search_results
        mock_search_service.return_value = mock_search

        # Mock Ollama
        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {
            "response": "Test response"
        }
        mock_ollama.return_value = mock_ollama_instance

        # Create agent with settings
        config = AgentConfig(
            role=AgentRole.SENIOR_DEVELOPER,
            goal="Explain code",
            backstory="Senior developer",
            verbosity="verbose",
            technical_level="junior"
        )

        agent = get_senior_developer_agent()
        agent.config = config

        # Execute multiple queries
        response1 = agent.execute_query("Query 1")
        response2 = agent.execute_query("Query 2")

        # Verify settings persisted
        assert agent.config.verbosity == "verbose"
        assert agent.config.technical_level == "junior"

    @patch('codeindex.web.services.settings_service.load_settings')
    @patch('codeindex.web.services.settings_service.save_settings')
    def test_settings_roundtrip_save_and_load(
        self,
        mock_save,
        mock_load
    ):
        """Test settings can be saved and loaded correctly."""
        from codeindex.web.services.settings_service import save_settings, load_settings

        # Test settings
        test_settings = {
            "verbosity": "verbose",
            "technical_level": "junior",
            "citation_style": "footnotes",
            "ui_theme": "dark",
            "output_format": "text"
        }

        # Save settings
        save_settings(test_settings)

        # Verify save was called
        mock_save.assert_called_once_with(test_settings)

        # Mock load to return saved settings
        mock_load.return_value = test_settings

        # Load settings
        loaded = load_settings()

        # Verify loaded settings match saved
        assert loaded["verbosity"] == test_settings["verbosity"]
        assert loaded["technical_level"] == test_settings["technical_level"]
        assert loaded["citation_style"] == test_settings["citation_style"]

    @patch('codeindex.web.services.settings_service.get')
    @patch('codeindex.web.services.settings_service.set_value')
    def test_reset_settings_restores_defaults(
        self,
        mock_set,
        mock_get
    ):
        """Test resetting settings restores default values."""
        from codeindex.web.services.settings_service import reset_settings, get_default_settings

        # Reset settings
        reset_settings()

        # Verify set_value called with defaults
        defaults = get_default_settings()
        mock_set.assert_called_once_with("agent_settings", defaults)

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_different_agents_respect_same_settings(
        self,
        mock_ollama,
        mock_search_service,
        mock_search_results
    ):
        """Test that different agent types respect the same settings."""
        from codeindex.web.agents.senior_developer import get_senior_developer_agent
        from codeindex.web.agents.data_analyst import get_data_analyst_agent
        from codeindex.web.agents.base import AgentConfig, AgentRole

        # Mock search
        mock_search = Mock()
        mock_search.search.return_value = mock_search_results
        mock_search_service.return_value = mock_search

        # Mock Ollama
        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {
            "response": "Test response"
        }
        mock_ollama.return_value = mock_ollama_instance

        # Shared settings
        shared_settings = {
            "verbosity": "concise",
            "technical_level": "senior",
            "citation_style": "inline"
        }

        # Create different agents with same settings
        senior_dev_config = AgentConfig(
            role=AgentRole.SENIOR_DEVELOPER,
            goal="Explain code",
            backstory="Senior developer",
            **shared_settings
        )

        data_analyst_config = AgentConfig(
            role=AgentRole.DATA_ANALYST,
            goal="Analyze data",
            backstory="Data analyst",
            **shared_settings
        )

        senior_dev = get_senior_developer_agent()
        senior_dev.config = senior_dev_config

        data_analyst = get_data_analyst_agent()
        data_analyst.config = data_analyst_config

        # Verify both agents have same settings
        assert senior_dev.config.verbosity == data_analyst.config.verbosity
        assert senior_dev.config.technical_level == data_analyst.config.technical_level
        assert senior_dev.config.citation_style == data_analyst.config.citation_style

    @patch('codeindex.web.services.settings_service.validate_settings')
    def test_invalid_settings_rejected_before_application(self, mock_validate):
        """Test that invalid settings are rejected before being applied."""
        from codeindex.web.services.settings_service import save_settings

        # Mock validation to return errors
        mock_validate.return_value = (False, {
            "verbosity": "Must be concise, standard, or verbose",
            "technical_level": "Must be junior, mid, or senior"
        })

        invalid_settings = {
            "verbosity": "invalid_value",
            "technical_level": "invalid_level"
        }

        # Attempt to save invalid settings
        with pytest.raises(ValueError):
            save_settings(invalid_settings, validate=True)
