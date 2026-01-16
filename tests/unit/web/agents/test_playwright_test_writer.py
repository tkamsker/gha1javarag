"""
Unit tests for Playwright Test Writer agent (T126).

Tests agent configuration, Playwright test generation, page object model creation,
and TypeScript code formatting.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Any
from datetime import datetime


class TestPlaywrightTestWriterAgent:
    """Test suite for Playwright Test Writer agent."""

    @pytest.fixture
    def agent_config(self):
        """Create test agent configuration."""
        from codeindex.web.agents.base import AgentConfig, AgentRole

        return AgentConfig(
            role=AgentRole.PLAYWRIGHT_TEST_WRITER,
            goal="Generate production-ready Playwright E2E tests with Page Object Model",
            backstory="Test Playwright Test Writer agent for unit testing",
            temperature=0.3,
            max_tokens=4000
        )

    @pytest.fixture
    def playwright_writer(self, agent_config):
        """Create Playwright Test Writer agent instance."""
        from codeindex.web.agents.playwright_test_writer import PlaywrightTestWriterAgent

        return PlaywrightTestWriterAgent(agent_config)

    @pytest.fixture
    def mock_ui_artifacts(self) -> List[Dict[str, Any]]:
        """Create mock UI component artifacts."""
        return [
            {
                "id": "gwt-presenter-001",
                "artifactType": "GwtPresenter",
                "fileName": "UserPresenter.java",
                "relativePath": "src/main/java/com/example/client/UserPresenter.java",
                "summary": "User management UI presenter with form handlers",
                "entities": ["onEditUser", "onSaveUser", "onDeleteUser"],
                "_additional": {"id": "gwt-presenter-001", "distance": 0.05}
            },
            {
                "id": "gwt-view-001",
                "artifactType": "GwtView",
                "fileName": "UserView.java",
                "relativePath": "src/main/java/com/example/client/UserView.java",
                "summary": "User form view with text fields and buttons",
                "entities": ["nameField", "emailField", "saveButton"],
                "_additional": {"id": "gwt-view-001", "distance": 0.08}
            },
            {
                "id": "uibinder-001",
                "artifactType": "GwtUiBinder",
                "fileName": "UserView.ui.xml",
                "relativePath": "src/main/java/com/example/client/UserView.ui.xml",
                "summary": "User form UiBinder template",
                "entities": ["TextBox", "Button", "Label"],
                "_additional": {"id": "uibinder-001", "distance": 0.10}
            },
            {
                "id": "jsp-form-001",
                "artifactType": "JspForm",
                "fileName": "login.jsp",
                "relativePath": "src/main/webapp/login.jsp",
                "summary": "Login form with username and password fields",
                "entities": ["username", "password", "submitButton"],
                "_additional": {"id": "jsp-form-001", "distance": 0.12}
            }
        ]

    def test_agent_initialization_default_config(self):
        """Test agent initializes with default configuration."""
        from codeindex.web.agents.playwright_test_writer import PlaywrightTestWriterAgent
        from codeindex.web.agents.base import AgentRole

        agent = PlaywrightTestWriterAgent()

        assert agent.config is not None
        assert agent.role == AgentRole.PLAYWRIGHT_TEST_WRITER
        assert agent.config.role == AgentRole.PLAYWRIGHT_TEST_WRITER

    def test_agent_initialization_custom_config(self, agent_config):
        """Test agent initializes with custom configuration."""
        from codeindex.web.agents.playwright_test_writer import PlaywrightTestWriterAgent

        agent = PlaywrightTestWriterAgent(agent_config)

        assert agent.config == agent_config
        assert agent.config.temperature == 0.3
        assert agent.config.max_tokens == 4000

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_execute_query_success(
        self,
        mock_ollama,
        mock_get_search,
        playwright_writer,
        mock_ui_artifacts
    ):
        """Test successful Playwright test generation."""
        from codeindex.web.agents.base import AgentResponse

        # Mock search service
        mock_search = Mock()
        mock_search.search.return_value = {
            "results": mock_ui_artifacts,
            "total": 4
        }
        mock_get_search.return_value = mock_search

        # Mock Ollama response with Playwright code
        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {
            "response": """import { test, expect } from '@playwright/test';

test.describe('User Management', () => {
  test('should create new user', async ({ page }) => {
    await page.goto('/users');
    await page.getByLabel('Name').fill('John Doe');
    await page.getByLabel('Email').fill('john@example.com');
    await page.getByRole('button', { name: 'Save' }).click();
    await expect(page.getByText('User created')).toBeVisible();
  });
});
"""
        }
        mock_ollama.return_value = mock_ollama_instance

        response = playwright_writer.execute_query("Generate Playwright tests for user management")

        assert isinstance(response, AgentResponse)
        assert len(response.response_text) > 0
        assert "test" in response.response_text or "playwright" in response.response_text.lower()
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
        playwright_writer
    ):
        """Test query execution with error handling."""
        # Mock search to fail
        mock_search = Mock()
        mock_search.search.side_effect = Exception("Weaviate connection failed")
        mock_get_search.return_value = mock_search

        response = playwright_writer.execute_query("Generate tests")

        assert response.error is not None
        assert "Weaviate connection failed" in response.error
        assert response.response_text == ""

    @patch('codeindex.web.services.search_service.get_search_service')
    def test_search_relevant_artifacts_no_filters(
        self,
        mock_get_search,
        playwright_writer,
        mock_ui_artifacts
    ):
        """Test artifact search without type filters (comprehensive)."""
        # Mock search service
        mock_search = Mock()
        mock_search.search.return_value = {
            "results": mock_ui_artifacts,
            "total": 4
        }
        mock_get_search.return_value = mock_search

        artifacts = playwright_writer._search_relevant_artifacts("user interface")

        assert len(artifacts) == 4
        # Should include multiple artifact types
        artifact_types = set(a["artifactType"] for a in artifacts)
        assert len(artifact_types) > 1
        assert "GwtPresenter" in artifact_types or "GwtView" in artifact_types

        # Verify search was called WITHOUT artifact type filters
        mock_search.search.assert_called_once()
        call_args = mock_search.search.call_args
        # Should NOT have filters parameter or filters should not include artifact_types
        if "filters" in call_args[1]:
            assert "artifact_types" not in call_args[1].get("filters", {})

    @patch('codeindex.web.services.search_service.get_search_service')
    def test_search_relevant_artifacts_empty_results(self, mock_get_search, playwright_writer):
        """Test artifact search with no results."""
        # Mock empty search results
        mock_search = Mock()
        mock_search.search.return_value = {"results": [], "total": 0}
        mock_get_search.return_value = mock_search

        artifacts = playwright_writer._search_relevant_artifacts("nonexistent feature")

        assert len(artifacts) == 0

    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_generate_playwright_code(self, mock_ollama, playwright_writer, mock_ui_artifacts):
        """Test Playwright test code generation."""
        # Mock Ollama response
        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {
            "response": """import { test, expect } from '@playwright/test';
import { UserPage } from './pages/UserPage';

test.describe('User Management Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/users');
  });

  test('should display user form', async ({ page }) => {
    const userPage = new UserPage(page);
    await expect(userPage.nameField).toBeVisible();
    await expect(userPage.emailField).toBeVisible();
  });
});

export class UserPage {
  constructor(private page: Page) {}

  readonly nameField = this.page.getByLabel('Name');
  readonly emailField = this.page.getByLabel('Email');
  readonly saveButton = this.page.getByRole('button', { name: 'Save' });
}
"""
        }
        mock_ollama.return_value = mock_ollama_instance

        test_code = playwright_writer._generate_document(
            "Generate Playwright tests for user form",
            mock_ui_artifacts,
            None
        )

        assert len(test_code) > 0
        assert "test" in test_code or "playwright" in test_code.lower() or "expect" in test_code
        # Should include Page Object Model
        assert "class" in test_code or "page" in test_code.lower()

        # Verify Ollama was called with correct prompts
        mock_ollama_instance.call_ollama.assert_called_once()
        call_args = mock_ollama_instance.call_ollama.call_args
        assert "playwright" in call_args[1]["prompt"].lower() or "test" in call_args[1]["prompt"].lower()
        assert "Automation Engineer" in call_args[1]["system_prompt"] or "Playwright" in call_args[1]["system_prompt"]

    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_generate_playwright_with_context(
        self,
        mock_ollama,
        playwright_writer,
        mock_ui_artifacts
    ):
        """Test Playwright generation with context from other agents."""
        # Mock Ollama response
        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {
            "response": "test('context-aware test', async ({ page }) => { /* test */ });"
        }
        mock_ollama.return_value = mock_ollama_instance

        context = {
            "frontend_analysis": "UserPresenter manages form interactions",
            "backend_analysis": "UserService handles CRUD operations"
        }

        test_code = playwright_writer._generate_document(
            "Generate tests",
            mock_ui_artifacts,
            context
        )

        assert len(test_code) > 0

    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_generate_playwright_fallback(self, mock_ollama, playwright_writer, mock_ui_artifacts):
        """Test fallback when Ollama fails."""
        # Mock Ollama to fail
        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.side_effect = Exception("Connection timeout")
        mock_ollama.return_value = mock_ollama_instance

        test_code = playwright_writer._generate_document(
            "Generate tests",
            mock_ui_artifacts,
            None
        )

        assert len(test_code) > 0
        # Fallback should include basic Playwright structure
        assert "import" in test_code and "test" in test_code
        assert "describe" in test_code or "test(" in test_code
        # Should mention LLM failure
        assert "LLM generation failed" in test_code or "Ollama" in test_code

    def test_extract_citations(self, playwright_writer, mock_ui_artifacts):
        """Test citation extraction."""
        citations = playwright_writer._extract_citations(mock_ui_artifacts)

        assert len(citations) == 4
        assert all(c.artifact_id for c in citations)
        assert all(c.file_path for c in citations)
        # Should include UI artifact types
        artifact_types = set(c.artifact_type for c in citations)
        assert len(artifact_types) > 1

    def test_extract_citations_limits_to_ten(self, playwright_writer):
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

        citations = playwright_writer._extract_citations(many_artifacts)

        assert len(citations) == 10

    def test_generate_follow_ups_for_playwright(self, playwright_writer, mock_ui_artifacts):
        """Test follow-up question generation for Playwright tests."""
        questions = playwright_writer._generate_follow_ups(
            "Generate Playwright tests for user management",
            mock_ui_artifacts
        )

        assert len(questions) > 0
        assert len(questions) <= 4
        # Should suggest test improvements or extensions
        assert any(
            "test" in q.lower() or
            "error" in q.lower() or
            "mock" in q.lower() or
            "accessibility" in q.lower() or
            "regression" in q.lower()
            for q in questions
        )

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_response_structure(
        self,
        mock_ollama,
        mock_get_search,
        playwright_writer,
        mock_ui_artifacts
    ):
        """Test response has all required fields."""
        # Mock dependencies
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_ui_artifacts, "total": 4}
        mock_get_search.return_value = mock_search

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {"response": "test code..."}
        mock_ollama.return_value = mock_ollama_instance

        response = playwright_writer.execute_query("Generate tests")

        assert hasattr(response, "agent_role")
        assert hasattr(response, "query")
        assert hasattr(response, "timestamp")
        assert hasattr(response, "duration_seconds")
        assert hasattr(response, "response_text")
        assert hasattr(response, "citations")
        assert hasattr(response, "confidence")
        assert hasattr(response, "suggested_questions")
        assert hasattr(response, "tools_used")

    def test_page_object_model_in_fallback(self, playwright_writer):
        """Test fallback includes Page Object Model structure."""
        artifacts = []  # Empty to test basic template

        fallback = playwright_writer._generate_fallback_test("Generate tests", artifacts)

        assert len(fallback) > 0
        # Should include POM class definition
        assert "class" in fallback or "export class" in fallback
        # Should include locators
        assert "locator" in fallback.lower() or "getByRole" in fallback or "getByLabel" in fallback
        # Should include async/await
        assert "async" in fallback and "await" in fallback
        # Should include Playwright imports
        assert "import" in fallback and ("@playwright/test" in fallback or "playwright" in fallback.lower())

    def test_singleton_pattern(self):
        """Test global Playwright Test Writer agent singleton."""
        from codeindex.web.agents.playwright_test_writer import get_playwright_test_writer_agent

        agent1 = get_playwright_test_writer_agent()
        agent2 = get_playwright_test_writer_agent()

        assert agent1 is agent2
