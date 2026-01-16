"""
Unit tests for Gherkin Test Writer agent (T112 - US2.5).

Tests agent configuration, Gherkin syntax generation, and scenario creation.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from typing import Dict, Any, List


class TestGherkinTestWriterAgent:
    """Test suite for Gherkin Test Writer agent."""

    @pytest.fixture
    def mock_search_results(self) -> List[Dict[str, Any]]:
        """Create mock Weaviate search results."""
        return [
            {
                "id": "user-story-001",
                "artifactType": "UserStory",
                "fileName": "login_feature.md",
                "relativePath": "specs/login_feature.md",
                "summary": "User login with email and password validation",
                "entities": ["login", "authentication", "validation"],
                "_additional": {"id": "user-story-001", "distance": 0.1}
            },
            {
                "id": "ui-form-001",
                "artifactType": "JspForm",
                "fileName": "LoginForm.jsp",
                "relativePath": "src/main/webapp/forms/LoginForm.jsp",
                "summary": "Login form with email and password fields",
                "entities": ["email", "password", "submit"],
                "_additional": {"id": "ui-form-001", "distance": 0.15}
            }
        ]

    @pytest.fixture
    def mock_ollama_gherkin_response(self) -> Dict[str, Any]:
        """Create mock Ollama response with Gherkin feature file."""
        return {
            "response": """Feature: User Login
  As a registered user
  I want to log in to the application
  So that I can access my account

  Background:
    Given the application is running
    And the login page is displayed

  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter "user@example.com" in the email field
    And I enter "ValidPass123!" in the password field
    And I click the "Login" button
    Then I should see the dashboard page
    And I should see my username "John Doe"

  Scenario: Failed login with invalid password
    Given I am on the login page
    When I enter "user@example.com" in the email field
    And I enter "WrongPassword" in the password field
    And I click the "Login" button
    Then I should see an error message "Invalid credentials"
    And I should remain on the login page

  Scenario Outline: Login validation errors
    Given I am on the login page
    When I enter "<email>" in the email field
    And I enter "<password>" in the password field
    And I click the "Login" button
    Then I should see an error message "<error>"

    Examples:
      | email              | password   | error                    |
      |                    | Pass123!   | Email is required        |
      | invalid-email      | Pass123!   | Invalid email format     |
      | user@example.com   |            | Password is required     |
      | user@example.com   | short      | Password too short       |"""
        }

    def test_agent_initialization_with_default_config(self):
        """Test agent initializes with default configuration."""
        from codeindex.web.agents.gherkin_test_writer import GherkinTestWriterAgent
        from codeindex.web.agents.base import AgentRole

        agent = GherkinTestWriterAgent()

        assert agent.config is not None
        assert agent.role == AgentRole.GHERKIN_TEST_WRITER
        assert agent.config.role == AgentRole.GHERKIN_TEST_WRITER
        assert "WeaviateSearchTool" in agent.config.tools
        assert "FileReadTool" in agent.config.tools
        assert "DocumentGeneratorTool" in agent.config.tools

    def test_agent_initialization_with_custom_config(self):
        """Test agent initializes with custom configuration."""
        from codeindex.web.agents.gherkin_test_writer import GherkinTestWriterAgent
        from codeindex.web.agents.base import AgentConfig, AgentRole

        custom_config = AgentConfig(
            role=AgentRole.GHERKIN_TEST_WRITER,
            goal="Custom goal",
            backstory="Custom backstory",
            verbosity="verbose",
            technical_level="junior"
        )

        agent = GherkinTestWriterAgent(config=custom_config)

        assert agent.config.verbosity == "verbose"
        assert agent.config.technical_level == "junior"
        assert agent.config.goal == "Custom goal"

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_generate_gherkin_feature_file_structure(
        self,
        mock_ollama,
        mock_search_service,
        mock_search_results,
        mock_ollama_gherkin_response
    ):
        """Test Gherkin feature file generation with proper structure."""
        from codeindex.web.agents.gherkin_test_writer import GherkinTestWriterAgent

        # Mock search service
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_search_results}
        mock_search_service.return_value = mock_search

        # Mock Ollama
        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = mock_ollama_gherkin_response
        mock_ollama.return_value = mock_ollama_instance

        # Execute query
        agent = GherkinTestWriterAgent()
        response = agent.execute_query("Generate Gherkin tests for user login")

        # Verify feature file structure
        assert "Feature:" in response.response_text
        assert "Scenario:" in response.response_text
        assert "Given" in response.response_text
        assert "When" in response.response_text
        assert "Then" in response.response_text

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_gherkin_includes_background_steps(
        self,
        mock_ollama,
        mock_search_service,
        mock_search_results,
        mock_ollama_gherkin_response
    ):
        """Test Gherkin generation includes Background for common setup."""
        from codeindex.web.agents.gherkin_test_writer import GherkinTestWriterAgent

        # Mock services
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_search_results}
        mock_search_service.return_value = mock_search

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = mock_ollama_gherkin_response
        mock_ollama.return_value = mock_ollama_instance

        # Execute query
        agent = GherkinTestWriterAgent()
        response = agent.execute_query("Generate Gherkin tests for user login")

        # Verify Background section exists
        assert "Background:" in response.response_text

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_gherkin_includes_scenario_outlines(
        self,
        mock_ollama,
        mock_search_service,
        mock_search_results,
        mock_ollama_gherkin_response
    ):
        """Test Gherkin generation includes Scenario Outlines with Examples."""
        from codeindex.web.agents.gherkin_test_writer import GherkinTestWriterAgent

        # Mock services
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_search_results}
        mock_search_service.return_value = mock_search

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = mock_ollama_gherkin_response
        mock_ollama.return_value = mock_ollama_instance

        # Execute query
        agent = GherkinTestWriterAgent()
        response = agent.execute_query("Generate Gherkin tests for login validation")

        # Verify Scenario Outline and Examples
        assert "Scenario Outline:" in response.response_text
        assert "Examples:" in response.response_text
        assert "|" in response.response_text  # Table format

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_gherkin_covers_happy_path_scenarios(
        self,
        mock_ollama,
        mock_search_service,
        mock_search_results,
        mock_ollama_gherkin_response
    ):
        """Test Gherkin generation includes happy path scenarios."""
        from codeindex.web.agents.gherkin_test_writer import GherkinTestWriterAgent

        # Mock services
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_search_results}
        mock_search_service.return_value = mock_search

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = mock_ollama_gherkin_response
        mock_ollama.return_value = mock_ollama_instance

        # Execute query
        agent = GherkinTestWriterAgent()
        response = agent.execute_query("Generate Gherkin tests for user login")

        # Verify happy path scenario exists
        response_lower = response.response_text.lower()
        assert "successful" in response_lower or "valid" in response_lower

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_gherkin_covers_error_scenarios(
        self,
        mock_ollama,
        mock_search_service,
        mock_search_results,
        mock_ollama_gherkin_response
    ):
        """Test Gherkin generation includes error scenarios."""
        from codeindex.web.agents.gherkin_test_writer import GherkinTestWriterAgent

        # Mock services
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_search_results}
        mock_search_service.return_value = mock_search

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = mock_ollama_gherkin_response
        mock_ollama.return_value = mock_ollama_instance

        # Execute query
        agent = GherkinTestWriterAgent()
        response = agent.execute_query("Generate Gherkin tests for user login")

        # Verify error scenarios exist
        response_lower = response.response_text.lower()
        assert "failed" in response_lower or "invalid" in response_lower or "error" in response_lower

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_agent_uses_weaviate_search_tool(
        self,
        mock_ollama,
        mock_search_service,
        mock_search_results,
        mock_ollama_gherkin_response
    ):
        """Test agent uses WeaviateSearchTool to find relevant artifacts."""
        from codeindex.web.agents.gherkin_test_writer import GherkinTestWriterAgent

        # Mock services
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_search_results}
        mock_search_service.return_value = mock_search

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = mock_ollama_gherkin_response
        mock_ollama.return_value = mock_ollama_instance

        # Execute query
        agent = GherkinTestWriterAgent()
        response = agent.execute_query("Generate Gherkin tests for login")

        # Verify search was called
        mock_search.search.assert_called_once()
        assert "WeaviateSearchTool" in response.tools_used

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_agent_extracts_citations_from_search_results(
        self,
        mock_ollama,
        mock_search_service,
        mock_search_results,
        mock_ollama_gherkin_response
    ):
        """Test agent extracts citations from search results."""
        from codeindex.web.agents.gherkin_test_writer import GherkinTestWriterAgent

        # Mock services
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_search_results}
        mock_search_service.return_value = mock_search

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = mock_ollama_gherkin_response
        mock_ollama.return_value = mock_ollama_instance

        # Execute query
        agent = GherkinTestWriterAgent()
        response = agent.execute_query("Generate Gherkin tests")

        # Verify citations exist
        assert len(response.citations) > 0
        assert any(c.artifact_id == "user-story-001" for c in response.citations)
        assert any(c.file_path == "specs/login_feature.md" for c in response.citations)

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_agent_generates_follow_up_questions(
        self,
        mock_ollama,
        mock_search_service,
        mock_search_results,
        mock_ollama_gherkin_response
    ):
        """Test agent generates relevant follow-up questions."""
        from codeindex.web.agents.gherkin_test_writer import GherkinTestWriterAgent

        # Mock services
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_search_results}
        mock_search_service.return_value = mock_search

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = mock_ollama_gherkin_response
        mock_ollama.return_value = mock_ollama_instance

        # Execute query
        agent = GherkinTestWriterAgent()
        response = agent.execute_query("Generate Gherkin tests")

        # Verify follow-up questions exist
        assert len(response.suggested_questions) > 0
        assert all(isinstance(q, str) for q in response.suggested_questions)

    @patch('codeindex.web.services.search_service.get_search_service')
    def test_agent_handles_search_failure_gracefully(
        self,
        mock_search_service
    ):
        """Test agent handles Weaviate search failures gracefully."""
        from codeindex.web.agents.gherkin_test_writer import GherkinTestWriterAgent

        # Mock search to raise exception
        mock_search = Mock()
        mock_search.search.side_effect = Exception("Weaviate connection failed")
        mock_search_service.return_value = mock_search

        # Execute query
        agent = GherkinTestWriterAgent()
        response = agent.execute_query("Generate Gherkin tests")

        # Verify error handling
        assert response.has_error()
        assert "Weaviate connection failed" in response.error

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_agent_handles_ollama_failure_gracefully(
        self,
        mock_ollama,
        mock_search_service,
        mock_search_results
    ):
        """Test agent handles Ollama LLM failures gracefully."""
        from codeindex.web.agents.gherkin_test_writer import GherkinTestWriterAgent

        # Mock search service
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_search_results}
        mock_search_service.return_value = mock_search

        # Mock Ollama to raise exception
        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.side_effect = Exception("Ollama timeout")
        mock_ollama.return_value = mock_ollama_instance

        # Execute query
        agent = GherkinTestWriterAgent()
        response = agent.execute_query("Generate Gherkin tests")

        # Verify error handling
        assert response.has_error()
        assert "Ollama" in response.error or "timeout" in response.error.lower()

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_agent_response_includes_metadata(
        self,
        mock_ollama,
        mock_search_service,
        mock_search_results,
        mock_ollama_gherkin_response
    ):
        """Test agent response includes required metadata."""
        from codeindex.web.agents.gherkin_test_writer import GherkinTestWriterAgent
        from codeindex.web.agents.base import AgentRole

        # Mock services
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_search_results}
        mock_search_service.return_value = mock_search

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = mock_ollama_gherkin_response
        mock_ollama.return_value = mock_ollama_instance

        # Execute query
        agent = GherkinTestWriterAgent()
        query = "Generate Gherkin tests for login"
        response = agent.execute_query(query)

        # Verify metadata
        assert response.agent_role == AgentRole.GHERKIN_TEST_WRITER
        assert response.query == query
        assert response.timestamp is not None
        assert response.duration_seconds > 0
        assert response.confidence >= 0.0 and response.confidence <= 1.0

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_gherkin_includes_user_story_references(
        self,
        mock_ollama,
        mock_search_service,
        mock_search_results,
        mock_ollama_gherkin_response
    ):
        """Test Gherkin generation references user stories and acceptance criteria."""
        from codeindex.web.agents.gherkin_test_writer import GherkinTestWriterAgent

        # Mock services
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_search_results}
        mock_search_service.return_value = mock_search

        # Add user story context to response
        response_with_reference = mock_ollama_gherkin_response.copy()
        response_with_reference["response"] = """Feature: User Login
  As a registered user
  I want to log in to the application
  So that I can access my account

  # References:
  # - User Story: login_feature.md
  # - Acceptance Criteria: AC-001, AC-002

  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter valid credentials
    Then I should see the dashboard"""

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = response_with_reference
        mock_ollama.return_value = mock_ollama_instance

        # Execute query
        agent = GherkinTestWriterAgent()
        response = agent.execute_query("Generate Gherkin tests for login")

        # Verify references are included or citations exist
        assert len(response.citations) > 0 or "Reference" in response.response_text

    def test_get_gherkin_test_writer_agent_singleton(self):
        """Test global agent singleton pattern."""
        from codeindex.web.agents.gherkin_test_writer import get_gherkin_test_writer_agent

        agent1 = get_gherkin_test_writer_agent()
        agent2 = get_gherkin_test_writer_agent()

        assert agent1 is agent2  # Same instance

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_agent_generates_test_data_tables(
        self,
        mock_ollama,
        mock_search_service,
        mock_search_results,
        mock_ollama_gherkin_response
    ):
        """Test agent generates test data tables in Examples section."""
        from codeindex.web.agents.gherkin_test_writer import GherkinTestWriterAgent

        # Mock services
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_search_results}
        mock_search_service.return_value = mock_search

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = mock_ollama_gherkin_response
        mock_ollama.return_value = mock_ollama_instance

        # Execute query
        agent = GherkinTestWriterAgent()
        response = agent.execute_query("Generate Gherkin tests with test data")

        # Verify data tables exist
        assert "Examples:" in response.response_text
        # Check for table rows (at least header and one data row)
        table_rows = [line for line in response.response_text.split('\n') if line.strip().startswith('|')]
        assert len(table_rows) >= 2  # Header + at least one data row
