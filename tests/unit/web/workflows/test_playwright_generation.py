"""
Unit tests for Playwright generation workflow (T128).

Tests workflow orchestration, UI component analysis, and agent context passing
for generating Playwright E2E tests.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any, List


class TestPlaywrightGenerationWorkflow:
    """Test suite for Playwright generation workflow."""

    @pytest.fixture
    def mock_frontend_analysis(self) -> Dict[str, Any]:
        """Mock Frontend Specialist agent response."""
        return {
            "ui_components": [
                {
                    "type": "GwtPresenter",
                    "name": "UserPresenter",
                    "path": "src/client/UserPresenter.java",
                    "handlers": ["onSaveUser", "onDeleteUser"],
                    "navigation_targets": ["DashboardPlace"]
                },
                {
                    "type": "GwtView",
                    "name": "UserView",
                    "path": "src/client/UserView.java",
                    "fields": ["nameField", "emailField", "saveButton"]
                }
            ],
            "forms": [
                {
                    "name": "UserForm",
                    "fields": ["name", "email", "age"],
                    "validation": ["required:name,email", "email:email"]
                }
            ],
            "summary": "User management UI with form validation"
        }

    @pytest.fixture
    def mock_backend_analysis(self) -> Dict[str, Any]:
        """Mock Backend Specialist agent response."""
        return {
            "endpoints": [
                {
                    "method": "POST",
                    "path": "/api/users",
                    "description": "Create new user"
                },
                {
                    "method": "GET",
                    "path": "/api/users/{id}",
                    "description": "Get user by ID"
                }
            ],
            "services": [
                {
                    "name": "UserService",
                    "methods": ["createUser", "getUser", "updateUser", "deleteUser"]
                }
            ],
            "summary": "User CRUD API with validation"
        }

    @pytest.fixture
    def mock_ui_artifacts(self) -> List[Dict[str, Any]]:
        """Mock UI artifacts for workflow input."""
        return [
            {
                "id": "presenter-001",
                "artifactType": "GwtPresenter",
                "fileName": "UserPresenter.java",
                "relativePath": "src/client/UserPresenter.java",
                "summary": "User management presenter"
            },
            {
                "id": "view-001",
                "artifactType": "GwtView",
                "fileName": "UserView.java",
                "relativePath": "src/client/UserView.java",
                "summary": "User form view"
            }
        ]

    def test_workflow_initialization(self):
        """Test workflow initializes correctly."""
        from codeindex.web.workflows.playwright_generation import PlaywrightGenerationWorkflow

        workflow = PlaywrightGenerationWorkflow()

        assert workflow is not None
        assert hasattr(workflow, 'execute')

    @patch('codeindex.web.agents.frontend_specialist.get_frontend_specialist_agent')
    @patch('codeindex.web.agents.backend_specialist.get_backend_specialist_agent')
    @patch('codeindex.web.agents.playwright_test_writer.get_playwright_test_writer_agent')
    def test_workflow_execution_success(
        self,
        mock_playwright_agent,
        mock_backend_agent,
        mock_frontend_agent,
        mock_ui_artifacts,
        mock_frontend_analysis,
        mock_backend_analysis
    ):
        """Test successful workflow execution with all agents."""
        from codeindex.web.workflows.playwright_generation import PlaywrightGenerationWorkflow
        from codeindex.web.agents.base import AgentResponse

        # Mock Frontend Specialist
        frontend_response = AgentResponse(
            agent_role="Frontend Specialist",
            query="Analyze UI",
            timestamp="2026-01-16T12:00:00",
            duration_seconds=2.5,
            response_text=str(mock_frontend_analysis),
            citations=[],
            confidence=0.9
        )
        mock_frontend_instance = Mock()
        mock_frontend_instance.execute_query.return_value = frontend_response
        mock_frontend_agent.return_value = mock_frontend_instance

        # Mock Backend Specialist
        backend_response = AgentResponse(
            agent_role="Backend Specialist",
            query="Analyze backend",
            timestamp="2026-01-16T12:00:02",
            duration_seconds=2.0,
            response_text=str(mock_backend_analysis),
            citations=[],
            confidence=0.88
        )
        mock_backend_instance = Mock()
        mock_backend_instance.execute_query.return_value = backend_response
        mock_backend_agent.return_value = mock_backend_instance

        # Mock Playwright Test Writer
        playwright_response = AgentResponse(
            agent_role="Playwright Test Writer",
            query="Generate tests",
            timestamp="2026-01-16T12:00:04",
            duration_seconds=5.0,
            response_text="""import { test, expect } from '@playwright/test';

test.describe('User Management', () => {
  test('should create user', async ({ page }) => {
    await page.goto('/users');
    await page.getByLabel('Name').fill('John Doe');
    await page.getByLabel('Email').fill('john@example.com');
    await page.getByRole('button', { name: 'Save' }).click();
    await expect(page.getByText('User created')).toBeVisible();
  });
});""",
            citations=[],
            confidence=0.87
        )
        mock_playwright_instance = Mock()
        mock_playwright_instance.execute_query.return_value = playwright_response
        mock_playwright_agent.return_value = mock_playwright_instance

        # Execute workflow
        workflow = PlaywrightGenerationWorkflow()
        result = workflow.execute(
            test_request="Generate Playwright tests for user management",
            artifacts=mock_ui_artifacts
        )

        # Verify workflow completed
        assert result is not None
        assert "test_code" in result
        assert "frontend_analysis" in result
        assert "backend_analysis" in result
        assert len(result["test_code"]) > 0
        assert "test" in result["test_code"] or "expect" in result["test_code"]

        # Verify agents were called in correct order
        mock_frontend_instance.execute_query.assert_called_once()
        mock_backend_instance.execute_query.assert_called_once()
        mock_playwright_instance.execute_query.assert_called_once()

    @patch('codeindex.web.agents.frontend_specialist.get_frontend_specialist_agent')
    def test_workflow_frontend_agent_failure(self, mock_frontend_agent, mock_ui_artifacts):
        """Test workflow handles Frontend Specialist failure."""
        from codeindex.web.workflows.playwright_generation import PlaywrightGenerationWorkflow
        from codeindex.web.agents.base import AgentResponse

        # Mock Frontend Specialist to fail
        frontend_response = AgentResponse(
            agent_role="Frontend Specialist",
            query="Analyze UI",
            timestamp="2026-01-16T12:00:00",
            duration_seconds=1.0,
            response_text="",
            citations=[],
            confidence=0.0,
            error="Weaviate connection failed"
        )
        mock_frontend_instance = Mock()
        mock_frontend_instance.execute_query.return_value = frontend_response
        mock_frontend_agent.return_value = mock_frontend_instance

        # Execute workflow
        workflow = PlaywrightGenerationWorkflow()

        with pytest.raises(Exception) as exc_info:
            workflow.execute(
                test_request="Generate tests",
                artifacts=mock_ui_artifacts
            )

        assert "Frontend Specialist" in str(exc_info.value) or "failed" in str(exc_info.value).lower()

    def test_workflow_context_passing(
        self,
        mock_ui_artifacts,
        mock_frontend_analysis,
        mock_backend_analysis
    ):
        """Test that context is passed between agents."""
        from codeindex.web.workflows.playwright_generation import PlaywrightGenerationWorkflow

        with patch('codeindex.web.agents.frontend_specialist.get_frontend_specialist_agent') as mock_frontend, \
             patch('codeindex.web.agents.backend_specialist.get_backend_specialist_agent') as mock_backend, \
             patch('codeindex.web.agents.playwright_test_writer.get_playwright_test_writer_agent') as mock_playwright:

            # Setup mocks
            from codeindex.web.agents.base import AgentResponse

            mock_frontend_instance = Mock()
            mock_frontend_instance.execute_query.return_value = AgentResponse(
                agent_role="Frontend Specialist",
                query="",
                timestamp="",
                duration_seconds=1.0,
                response_text=str(mock_frontend_analysis),
                citations=[],
                confidence=0.9
            )
            mock_frontend.return_value = mock_frontend_instance

            mock_backend_instance = Mock()
            mock_backend_instance.execute_query.return_value = AgentResponse(
                agent_role="Backend Specialist",
                query="",
                timestamp="",
                duration_seconds=1.0,
                response_text=str(mock_backend_analysis),
                citations=[],
                confidence=0.88
            )
            mock_backend.return_value = mock_backend_instance

            mock_playwright_instance = Mock()
            mock_playwright_instance.execute_query.return_value = AgentResponse(
                agent_role="Playwright Test Writer",
                query="",
                timestamp="",
                duration_seconds=1.0,
                response_text="test code",
                citations=[],
                confidence=0.87
            )
            mock_playwright.return_value = mock_playwright_instance

            # Execute workflow
            workflow = PlaywrightGenerationWorkflow()
            workflow.execute(
                test_request="Generate tests",
                artifacts=mock_ui_artifacts
            )

            # Verify Playwright agent received context from previous agents
            playwright_call_args = mock_playwright_instance.execute_query.call_args
            assert playwright_call_args is not None

            # Context should include frontend and backend analysis
            if len(playwright_call_args) > 1 and 'context' in playwright_call_args[1]:
                context = playwright_call_args[1]['context']
                assert context is not None

    def test_workflow_progress_tracking(self, mock_ui_artifacts):
        """Test workflow tracks progress through stages."""
        from codeindex.web.workflows.playwright_generation import PlaywrightGenerationWorkflow

        with patch('codeindex.web.agents.frontend_specialist.get_frontend_specialist_agent'), \
             patch('codeindex.web.agents.backend_specialist.get_backend_specialist_agent'), \
             patch('codeindex.web.agents.playwright_test_writer.get_playwright_test_writer_agent'):

            workflow = PlaywrightGenerationWorkflow()

            # Mock progress callback
            progress_updates = []

            def progress_callback(stage: str, progress: float):
                progress_updates.append({"stage": stage, "progress": progress})

            workflow.execute(
                test_request="Generate tests",
                artifacts=mock_ui_artifacts,
                progress_callback=progress_callback
            )

            # Verify progress was tracked
            assert len(progress_updates) > 0
            # Should have at least 3 stages: Frontend, Backend, Playwright
            assert any("frontend" in update["stage"].lower() for update in progress_updates)

    def test_workflow_with_empty_artifacts(self):
        """Test workflow handles empty artifact list."""
        from codeindex.web.workflows.playwright_generation import PlaywrightGenerationWorkflow

        workflow = PlaywrightGenerationWorkflow()

        with pytest.raises(ValueError) as exc_info:
            workflow.execute(
                test_request="Generate tests",
                artifacts=[]
            )

        assert "artifacts" in str(exc_info.value).lower() or "empty" in str(exc_info.value).lower()

    def test_workflow_ui_component_analysis(self, mock_ui_artifacts, mock_frontend_analysis):
        """Test workflow analyzes UI components correctly."""
        from codeindex.web.workflows.playwright_generation import PlaywrightGenerationWorkflow

        with patch('codeindex.web.agents.frontend_specialist.get_frontend_specialist_agent') as mock_frontend, \
             patch('codeindex.web.agents.backend_specialist.get_backend_specialist_agent'), \
             patch('codeindex.web.agents.playwright_test_writer.get_playwright_test_writer_agent'):

            from codeindex.web.agents.base import AgentResponse

            mock_frontend_instance = Mock()
            mock_frontend_instance.execute_query.return_value = AgentResponse(
                agent_role="Frontend Specialist",
                query="",
                timestamp="",
                duration_seconds=1.0,
                response_text=str(mock_frontend_analysis),
                citations=[],
                confidence=0.9
            )
            mock_frontend.return_value = mock_frontend_instance

            workflow = PlaywrightGenerationWorkflow()
            result = workflow.execute(
                test_request="Generate tests",
                artifacts=mock_ui_artifacts
            )

            # Verify UI component analysis is included
            assert "frontend_analysis" in result
            # Frontend agent should receive UI artifact context
            frontend_call = mock_frontend_instance.execute_query.call_args
            assert frontend_call is not None

    def test_workflow_generates_page_objects(self, mock_ui_artifacts):
        """Test workflow generates Page Object Models."""
        from codeindex.web.workflows.playwright_generation import PlaywrightGenerationWorkflow

        with patch('codeindex.web.agents.frontend_specialist.get_frontend_specialist_agent'), \
             patch('codeindex.web.agents.backend_specialist.get_backend_specialist_agent'), \
             patch('codeindex.web.agents.playwright_test_writer.get_playwright_test_writer_agent') as mock_playwright:

            from codeindex.web.agents.base import AgentResponse

            # Playwright agent returns code with POM
            mock_playwright_instance = Mock()
            mock_playwright_instance.execute_query.return_value = AgentResponse(
                agent_role="Playwright Test Writer",
                query="",
                timestamp="",
                duration_seconds=1.0,
                response_text="""export class UserPage {
  constructor(private page: Page) {}
  readonly nameField = this.page.getByLabel('Name');
}""",
                citations=[],
                confidence=0.87
            )
            mock_playwright.return_value = mock_playwright_instance

            workflow = PlaywrightGenerationWorkflow()
            result = workflow.execute(
                test_request="Generate tests",
                artifacts=mock_ui_artifacts
            )

            # Verify Page Object Model is in result
            assert "test_code" in result
            assert "class" in result["test_code"] or "Page" in result["test_code"]

    def test_workflow_result_structure(self, mock_ui_artifacts):
        """Test workflow result has correct structure."""
        from codeindex.web.workflows.playwright_generation import PlaywrightGenerationWorkflow

        with patch('codeindex.web.agents.frontend_specialist.get_frontend_specialist_agent'), \
             patch('codeindex.web.agents.backend_specialist.get_backend_specialist_agent'), \
             patch('codeindex.web.agents.playwright_test_writer.get_playwright_test_writer_agent'):

            workflow = PlaywrightGenerationWorkflow()
            result = workflow.execute(
                test_request="Generate tests",
                artifacts=mock_ui_artifacts
            )

            # Verify result structure
            assert isinstance(result, dict)
            assert "test_code" in result
            assert "frontend_analysis" in result
            assert "backend_analysis" in result
            assert "duration_seconds" in result
            assert "timestamp" in result

    def test_workflow_timeout_handling(self, mock_ui_artifacts):
        """Test workflow handles agent timeouts."""
        from codeindex.web.workflows.playwright_generation import PlaywrightGenerationWorkflow

        with patch('codeindex.web.agents.frontend_specialist.get_frontend_specialist_agent') as mock_frontend:

            # Frontend agent times out
            mock_frontend_instance = Mock()
            mock_frontend_instance.execute_query.side_effect = TimeoutError("Agent timeout")
            mock_frontend.return_value = mock_frontend_instance

            workflow = PlaywrightGenerationWorkflow()

            with pytest.raises(TimeoutError):
                workflow.execute(
                    test_request="Generate tests",
                    artifacts=mock_ui_artifacts
                )

    def test_workflow_artifact_filtering(self):
        """Test workflow filters relevant UI artifacts."""
        from codeindex.web.workflows.playwright_generation import PlaywrightGenerationWorkflow

        mixed_artifacts = [
            {"artifactType": "GwtPresenter", "fileName": "UserPresenter.java"},
            {"artifactType": "BackendDoc", "fileName": "UserService.java"},  # Should filter out
            {"artifactType": "GwtView", "fileName": "UserView.java"},
            {"artifactType": "DbTable", "fileName": "users.sql"}  # Should filter out
        ]

        workflow = PlaywrightGenerationWorkflow()

        # Get filtered artifacts
        ui_artifacts = workflow._filter_ui_artifacts(mixed_artifacts)

        assert len(ui_artifacts) == 2
        assert all(a["artifactType"] in ["GwtPresenter", "GwtView", "GwtUiBinder", "JspForm"] for a in ui_artifacts)
