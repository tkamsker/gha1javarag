"""
Unit tests for Gherkin test generation workflow (T114 - US2.5).

Tests workflow orchestration and agent context passing for Gherkin generation.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any, List


class TestGherkinGenerationWorkflow:
    """Test suite for Gherkin generation workflow orchestration."""

    @pytest.fixture
    def mock_prd_writer_response(self) -> Dict[str, Any]:
        """Mock response from PRD Writer agent."""
        from codeindex.web.agents.base import AgentResponse, AgentRole, Citation

        return AgentResponse(
            agent_role=AgentRole.PRD_WRITER,
            query="Analyze requirements for login feature",
            timestamp="2024-01-01T00:00:00",
            duration_seconds=2.5,
            response_text="""## User Story: User Login

**As a** registered user
**I want to** log in to the application
**So that** I can access my personalized dashboard

### Acceptance Criteria:
- AC-001: User can log in with email and password
- AC-002: Invalid credentials show error message
- AC-003: Successful login redirects to dashboard
- AC-004: Email format validation
- AC-005: Password must meet security requirements""",
            citations=[
                Citation(
                    artifact_id="req-001",
                    file_path="specs/login_feature.md",
                    artifact_type="Requirement"
                )
            ],
            confidence=0.9,
            suggested_questions=["What are the validation rules?"],
            tools_used=["WeaviateSearchTool", "DocumentGeneratorTool"]
        )

    @pytest.fixture
    def mock_frontend_specialist_response(self) -> Dict[str, Any]:
        """Mock response from Frontend Specialist agent."""
        from codeindex.web.agents.base import AgentResponse, AgentRole, Citation

        return AgentResponse(
            agent_role=AgentRole.FRONTEND_SPECIALIST,
            query="Identify UI components for login",
            timestamp="2024-01-01T00:01:00",
            duration_seconds=3.2,
            response_text="""## UI Components for Login Feature

### LoginForm.jsp
- **Email field**: Text input with email validation
- **Password field**: Password input with show/hide toggle
- **Login button**: Submit button
- **Error message container**: Displays validation and authentication errors

### UserPresenter.java
- Handles form submission
- Validates input fields
- Calls authentication service
- Navigates to dashboard on success""",
            citations=[
                Citation(
                    artifact_id="form-001",
                    file_path="src/main/webapp/forms/LoginForm.jsp",
                    artifact_type="JspForm"
                ),
                Citation(
                    artifact_id="presenter-001",
                    file_path="src/main/java/com/app/client/UserPresenter.java",
                    artifact_type="GwtPresenter"
                )
            ],
            confidence=0.85,
            suggested_questions=["How does validation work?"],
            tools_used=["WeaviateSearchTool", "FileReadTool"]
        )

    @pytest.fixture
    def mock_gherkin_writer_response(self) -> Dict[str, Any]:
        """Mock response from Gherkin Test Writer agent."""
        from codeindex.web.agents.base import AgentResponse, AgentRole, Citation

        return AgentResponse(
            agent_role=AgentRole.GHERKIN_TEST_WRITER,
            query="Generate Gherkin tests for login",
            timestamp="2024-01-01T00:02:00",
            duration_seconds=4.8,
            response_text="""Feature: User Login
  As a registered user
  I want to log in to the application
  So that I can access my personalized dashboard

  Background:
    Given the application is running
    And the login page is displayed

  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter "user@example.com" in the email field
    And I enter "ValidPass123!" in the password field
    And I click the "Login" button
    Then I should see the dashboard page
    And I should see my username

  Scenario: Failed login with invalid credentials
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
      | invalid-email      | Pass123!   | Invalid email format     |
      | user@example.com   |            | Password is required     |""",
            citations=[
                Citation(
                    artifact_id="req-001",
                    file_path="specs/login_feature.md",
                    artifact_type="Requirement"
                ),
                Citation(
                    artifact_id="form-001",
                    file_path="src/main/webapp/forms/LoginForm.jsp",
                    artifact_type="JspForm"
                )
            ],
            confidence=0.92,
            suggested_questions=["Should I add more edge cases?"],
            tools_used=["WeaviateSearchTool", "FileReadTool", "DocumentGeneratorTool"]
        )

    def test_workflow_initialization(self):
        """Test workflow initializes correctly."""
        from codeindex.web.workflows.gherkin_generation import GherkinGenerationWorkflow

        workflow = GherkinGenerationWorkflow()

        assert workflow is not None
        assert hasattr(workflow, 'execute')

    def test_workflow_executes_agents_in_sequence(
        self,
        mock_prd_writer_response,
        mock_frontend_specialist_response,
        mock_gherkin_writer_response
    ):
        """Test workflow executes agents in correct sequence: PRD Writer → Frontend Specialist → Gherkin Writer."""
        from codeindex.web.workflows.gherkin_generation import GherkinGenerationWorkflow

        with patch('codeindex.web.agents.prd_writer.get_prd_writer_agent') as mock_prd_agent_fn, \
             patch('codeindex.web.agents.frontend_specialist.get_frontend_specialist_agent') as mock_frontend_agent_fn, \
             patch('codeindex.web.agents.gherkin_test_writer.get_gherkin_test_writer_agent') as mock_gherkin_agent_fn:

            # Mock agents
            mock_prd_agent = Mock()
            mock_prd_agent.execute_query.return_value = mock_prd_writer_response
            mock_prd_agent_fn.return_value = mock_prd_agent

            mock_frontend_agent = Mock()
            mock_frontend_agent.execute_query.return_value = mock_frontend_specialist_response
            mock_frontend_agent_fn.return_value = mock_frontend_agent

            mock_gherkin_agent = Mock()
            mock_gherkin_agent.execute_query.return_value = mock_gherkin_writer_response
            mock_gherkin_agent_fn.return_value = mock_gherkin_agent

            # Execute workflow
            workflow = GherkinGenerationWorkflow()
            result = workflow.execute("Generate tests for user login")

            # Verify agents called in sequence
            mock_prd_agent.execute_query.assert_called_once()
            mock_frontend_agent.execute_query.assert_called_once()
            mock_gherkin_agent.execute_query.assert_called_once()

    def test_workflow_passes_context_between_agents(
        self,
        mock_prd_writer_response,
        mock_frontend_specialist_response,
        mock_gherkin_writer_response
    ):
        """Test workflow passes context from one agent to the next."""
        from codeindex.web.workflows.gherkin_generation import GherkinGenerationWorkflow

        with patch('codeindex.web.agents.prd_writer.get_prd_writer_agent') as mock_prd_agent_fn, \
             patch('codeindex.web.agents.frontend_specialist.get_frontend_specialist_agent') as mock_frontend_agent_fn, \
             patch('codeindex.web.agents.gherkin_test_writer.get_gherkin_test_writer_agent') as mock_gherkin_agent_fn:

            # Mock agents
            mock_prd_agent = Mock()
            mock_prd_agent.execute_query.return_value = mock_prd_writer_response
            mock_prd_agent_fn.return_value = mock_prd_agent

            mock_frontend_agent = Mock()
            mock_frontend_agent.execute_query.return_value = mock_frontend_specialist_response
            mock_frontend_agent_fn.return_value = mock_frontend_agent

            mock_gherkin_agent = Mock()
            mock_gherkin_agent.execute_query.return_value = mock_gherkin_writer_response
            mock_gherkin_agent_fn.return_value = mock_gherkin_agent

            # Execute workflow
            workflow = GherkinGenerationWorkflow()
            result = workflow.execute("Generate tests for user login")

            # Verify context was passed
            # Frontend Specialist should receive PRD Writer output
            frontend_call_args = mock_frontend_agent.execute_query.call_args
            assert frontend_call_args is not None
            context = frontend_call_args.kwargs.get("context", {})
            assert "prd_requirements" in context or len(frontend_call_args.args) > 0

            # Gherkin Writer should receive both PRD and Frontend output
            gherkin_call_args = mock_gherkin_agent.execute_query.call_args
            assert gherkin_call_args is not None
            context = gherkin_call_args.kwargs.get("context", {})
            assert "prd_requirements" in context or "ui_components" in context or len(gherkin_call_args.args) > 0

    def test_workflow_returns_final_gherkin_response(
        self,
        mock_prd_writer_response,
        mock_frontend_specialist_response,
        mock_gherkin_writer_response
    ):
        """Test workflow returns final Gherkin response."""
        from codeindex.web.workflows.gherkin_generation import GherkinGenerationWorkflow

        with patch('codeindex.web.agents.prd_writer.get_prd_writer_agent') as mock_prd_agent_fn, \
             patch('codeindex.web.agents.frontend_specialist.get_frontend_specialist_agent') as mock_frontend_agent_fn, \
             patch('codeindex.web.agents.gherkin_test_writer.get_gherkin_test_writer_agent') as mock_gherkin_agent_fn:

            # Mock agents
            mock_prd_agent = Mock()
            mock_prd_agent.execute_query.return_value = mock_prd_writer_response
            mock_prd_agent_fn.return_value = mock_prd_agent

            mock_frontend_agent = Mock()
            mock_frontend_agent.execute_query.return_value = mock_frontend_specialist_response
            mock_frontend_agent_fn.return_value = mock_frontend_agent

            mock_gherkin_agent = Mock()
            mock_gherkin_agent.execute_query.return_value = mock_gherkin_writer_response
            mock_gherkin_agent_fn.return_value = mock_gherkin_agent

            # Execute workflow
            workflow = GherkinGenerationWorkflow()
            result = workflow.execute("Generate tests for user login")

            # Verify result is from Gherkin Writer
            assert result is not None
            assert "Feature:" in result["gherkin_content"]
            assert "Scenario:" in result["gherkin_content"]

    def test_workflow_aggregates_citations_from_all_agents(
        self,
        mock_prd_writer_response,
        mock_frontend_specialist_response,
        mock_gherkin_writer_response
    ):
        """Test workflow aggregates citations from all agents."""
        from codeindex.web.workflows.gherkin_generation import GherkinGenerationWorkflow

        with patch('codeindex.web.agents.prd_writer.get_prd_writer_agent') as mock_prd_agent_fn, \
             patch('codeindex.web.agents.frontend_specialist.get_frontend_specialist_agent') as mock_frontend_agent_fn, \
             patch('codeindex.web.agents.gherkin_test_writer.get_gherkin_test_writer_agent') as mock_gherkin_agent_fn:

            # Mock agents
            mock_prd_agent = Mock()
            mock_prd_agent.execute_query.return_value = mock_prd_writer_response
            mock_prd_agent_fn.return_value = mock_prd_agent

            mock_frontend_agent = Mock()
            mock_frontend_agent.execute_query.return_value = mock_frontend_specialist_response
            mock_frontend_agent_fn.return_value = mock_frontend_agent

            mock_gherkin_agent = Mock()
            mock_gherkin_agent.execute_query.return_value = mock_gherkin_writer_response
            mock_gherkin_agent_fn.return_value = mock_gherkin_agent

            # Execute workflow
            workflow = GherkinGenerationWorkflow()
            result = workflow.execute("Generate tests for user login")

            # Verify citations aggregated
            assert "citations" in result
            assert len(result["citations"]) >= 2  # At least from PRD and Frontend agents

    def test_workflow_handles_prd_writer_failure(self):
        """Test workflow handles PRD Writer agent failure."""
        from codeindex.web.workflows.gherkin_generation import GherkinGenerationWorkflow

        with patch('codeindex.web.agents.prd_writer.get_prd_writer_agent') as mock_prd_agent_fn:

            # Mock PRD Writer to fail
            mock_prd_agent = Mock()
            mock_prd_agent.execute_query.side_effect = Exception("PRD Writer failed")
            mock_prd_agent_fn.return_value = mock_prd_agent

            # Execute workflow
            workflow = GherkinGenerationWorkflow()
            result = workflow.execute("Generate tests for user login")

            # Verify error handling
            assert result is not None
            assert "error" in result
            assert "PRD Writer" in result["error"]

    def test_workflow_handles_frontend_specialist_failure(
        self,
        mock_prd_writer_response
    ):
        """Test workflow handles Frontend Specialist agent failure."""
        from codeindex.web.workflows.gherkin_generation import GherkinGenerationWorkflow

        with patch('codeindex.web.agents.prd_writer.get_prd_writer_agent') as mock_prd_agent_fn, \
             patch('codeindex.web.agents.frontend_specialist.get_frontend_specialist_agent') as mock_frontend_agent_fn:

            # Mock PRD Writer success
            mock_prd_agent = Mock()
            mock_prd_agent.execute_query.return_value = mock_prd_writer_response
            mock_prd_agent_fn.return_value = mock_prd_agent

            # Mock Frontend Specialist to fail
            mock_frontend_agent = Mock()
            mock_frontend_agent.execute_query.side_effect = Exception("Frontend analysis failed")
            mock_frontend_agent_fn.return_value = mock_frontend_agent

            # Execute workflow
            workflow = GherkinGenerationWorkflow()
            result = workflow.execute("Generate tests for user login")

            # Verify error handling
            assert result is not None
            assert "error" in result
            assert "Frontend" in result["error"]

    def test_workflow_handles_gherkin_writer_failure(
        self,
        mock_prd_writer_response,
        mock_frontend_specialist_response
    ):
        """Test workflow handles Gherkin Writer agent failure."""
        from codeindex.web.workflows.gherkin_generation import GherkinGenerationWorkflow

        with patch('codeindex.web.agents.prd_writer.get_prd_writer_agent') as mock_prd_agent_fn, \
             patch('codeindex.web.agents.frontend_specialist.get_frontend_specialist_agent') as mock_frontend_agent_fn, \
             patch('codeindex.web.agents.gherkin_test_writer.get_gherkin_test_writer_agent') as mock_gherkin_agent_fn:

            # Mock PRD Writer and Frontend Specialist success
            mock_prd_agent = Mock()
            mock_prd_agent.execute_query.return_value = mock_prd_writer_response
            mock_prd_agent_fn.return_value = mock_prd_agent

            mock_frontend_agent = Mock()
            mock_frontend_agent.execute_query.return_value = mock_frontend_specialist_response
            mock_frontend_agent_fn.return_value = mock_frontend_agent

            # Mock Gherkin Writer to fail
            mock_gherkin_agent = Mock()
            mock_gherkin_agent.execute_query.side_effect = Exception("Gherkin generation failed")
            mock_gherkin_agent_fn.return_value = mock_gherkin_agent

            # Execute workflow
            workflow = GherkinGenerationWorkflow()
            result = workflow.execute("Generate tests for user login")

            # Verify error handling
            assert result is not None
            assert "error" in result
            assert "Gherkin" in result["error"]

    def test_workflow_calculates_total_duration(
        self,
        mock_prd_writer_response,
        mock_frontend_specialist_response,
        mock_gherkin_writer_response
    ):
        """Test workflow calculates total duration across all agents."""
        from codeindex.web.workflows.gherkin_generation import GherkinGenerationWorkflow

        with patch('codeindex.web.agents.prd_writer.get_prd_writer_agent') as mock_prd_agent_fn, \
             patch('codeindex.web.agents.frontend_specialist.get_frontend_specialist_agent') as mock_frontend_agent_fn, \
             patch('codeindex.web.agents.gherkin_test_writer.get_gherkin_test_writer_agent') as mock_gherkin_agent_fn:

            # Mock agents
            mock_prd_agent = Mock()
            mock_prd_agent.execute_query.return_value = mock_prd_writer_response
            mock_prd_agent_fn.return_value = mock_prd_agent

            mock_frontend_agent = Mock()
            mock_frontend_agent.execute_query.return_value = mock_frontend_specialist_response
            mock_frontend_agent_fn.return_value = mock_frontend_agent

            mock_gherkin_agent = Mock()
            mock_gherkin_agent.execute_query.return_value = mock_gherkin_writer_response
            mock_gherkin_agent_fn.return_value = mock_gherkin_agent

            # Execute workflow
            workflow = GherkinGenerationWorkflow()
            result = workflow.execute("Generate tests for user login")

            # Verify total duration calculated
            assert "total_duration_seconds" in result
            # Should be sum of all agent durations (2.5 + 3.2 + 4.8 = 10.5)
            expected_duration = 2.5 + 3.2 + 4.8
            assert abs(result["total_duration_seconds"] - expected_duration) < 1.0  # Allow small variance

    def test_workflow_includes_agent_execution_details(
        self,
        mock_prd_writer_response,
        mock_frontend_specialist_response,
        mock_gherkin_writer_response
    ):
        """Test workflow includes execution details for each agent."""
        from codeindex.web.workflows.gherkin_generation import GherkinGenerationWorkflow

        with patch('codeindex.web.agents.prd_writer.get_prd_writer_agent') as mock_prd_agent_fn, \
             patch('codeindex.web.agents.frontend_specialist.get_frontend_specialist_agent') as mock_frontend_agent_fn, \
             patch('codeindex.web.agents.gherkin_test_writer.get_gherkin_test_writer_agent') as mock_gherkin_agent_fn:

            # Mock agents
            mock_prd_agent = Mock()
            mock_prd_agent.execute_query.return_value = mock_prd_writer_response
            mock_prd_agent_fn.return_value = mock_prd_agent

            mock_frontend_agent = Mock()
            mock_frontend_agent.execute_query.return_value = mock_frontend_specialist_response
            mock_frontend_agent_fn.return_value = mock_frontend_agent

            mock_gherkin_agent = Mock()
            mock_gherkin_agent.execute_query.return_value = mock_gherkin_writer_response
            mock_gherkin_agent_fn.return_value = mock_gherkin_agent

            # Execute workflow
            workflow = GherkinGenerationWorkflow()
            result = workflow.execute("Generate tests for user login")

            # Verify agent execution details
            assert "agent_executions" in result
            assert len(result["agent_executions"]) == 3  # PRD Writer, Frontend Specialist, Gherkin Writer

            agent_names = [exec["agent"] for exec in result["agent_executions"]]
            assert "PRD Writer" in agent_names
            assert "Frontend Specialist" in agent_names
            assert "Gherkin Test Writer" in agent_names

    def test_workflow_supports_context_injection(self):
        """Test workflow supports injecting initial context."""
        from codeindex.web.workflows.gherkin_generation import GherkinGenerationWorkflow

        with patch('codeindex.web.agents.prd_writer.get_prd_writer_agent') as mock_prd_agent_fn:

            mock_prd_agent = Mock()
            mock_prd_agent.execute_query.return_value = Mock()
            mock_prd_agent_fn.return_value = mock_prd_agent

            # Execute workflow with initial context
            workflow = GherkinGenerationWorkflow()
            initial_context = {
                "user_stories": ["US-001: User login"],
                "artifacts": ["LoginForm.jsp", "UserPresenter.java"]
            }
            result = workflow.execute("Generate tests", context=initial_context)

            # Verify initial context was passed to first agent
            call_args = mock_prd_agent.execute_query.call_args
            context = call_args.kwargs.get("context", {})
            assert "user_stories" in context or "artifacts" in context

    def test_workflow_validates_gherkin_syntax_before_returning(
        self,
        mock_prd_writer_response,
        mock_frontend_specialist_response,
        mock_gherkin_writer_response
    ):
        """Test workflow validates Gherkin syntax before returning results."""
        from codeindex.web.workflows.gherkin_generation import GherkinGenerationWorkflow

        with patch('codeindex.web.agents.prd_writer.get_prd_writer_agent') as mock_prd_agent_fn, \
             patch('codeindex.web.agents.frontend_specialist.get_frontend_specialist_agent') as mock_frontend_agent_fn, \
             patch('codeindex.web.agents.gherkin_test_writer.get_gherkin_test_writer_agent') as mock_gherkin_agent_fn, \
             patch('codeindex.web.services.gherkin_validation.validate_gherkin_syntax') as mock_validate:

            # Mock agents
            mock_prd_agent = Mock()
            mock_prd_agent.execute_query.return_value = mock_prd_writer_response
            mock_prd_agent_fn.return_value = mock_prd_agent

            mock_frontend_agent = Mock()
            mock_frontend_agent.execute_query.return_value = mock_frontend_specialist_response
            mock_frontend_agent_fn.return_value = mock_frontend_agent

            mock_gherkin_agent = Mock()
            mock_gherkin_agent.execute_query.return_value = mock_gherkin_writer_response
            mock_gherkin_agent_fn.return_value = mock_gherkin_agent

            # Mock validation
            mock_validate.return_value = (True, [])  # Valid syntax

            # Execute workflow
            workflow = GherkinGenerationWorkflow()
            result = workflow.execute("Generate tests for user login")

            # Verify validation was called
            mock_validate.assert_called_once()

            # Verify validation result included
            assert "validation" in result
            assert result["validation"]["is_valid"] is True
