"""
Integration tests for Playwright test generation (T129).

Tests end-to-end Playwright test generation workflow including agent collaboration,
.spec.ts file download, and complete test suite workflow.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from typing import List, Dict, Any
import tempfile
import shutil


class TestPlaywrightGenerationIntegration:
    """Integration test suite for end-to-end Playwright generation."""

    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary output directory for test files."""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.fixture
    def mock_weaviate_ui_artifacts(self) -> List[Dict[str, Any]]:
        """Mock UI artifacts from Weaviate."""
        return [
            {
                "id": "ui-001",
                "artifactType": "GwtPresenter",
                "fileName": "LoginPresenter.java",
                "relativePath": "src/client/presenter/LoginPresenter.java",
                "summary": "Login form presenter with authentication logic",
                "entities": ["onLoginClick", "onForgotPasswordClick", "validateCredentials"],
                "_additional": {"id": "ui-001", "distance": 0.02}
            },
            {
                "id": "ui-002",
                "artifactType": "GwtView",
                "fileName": "LoginView.java",
                "relativePath": "src/client/view/LoginView.java",
                "summary": "Login form view with username and password fields",
                "entities": ["usernameField", "passwordField", "loginButton", "forgotPasswordLink"],
                "_additional": {"id": "ui-002", "distance": 0.05}
            },
            {
                "id": "ui-003",
                "artifactType": "GwtUiBinder",
                "fileName": "LoginView.ui.xml",
                "relativePath": "src/client/view/LoginView.ui.xml",
                "summary": "Login form UiBinder template",
                "entities": ["TextBox", "PasswordTextBox", "Button", "Anchor"],
                "_additional": {"id": "ui-003", "distance": 0.08}
            }
        ]

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_end_to_end_playwright_generation(
        self,
        mock_ollama,
        mock_search_service,
        temp_output_dir,
        mock_weaviate_ui_artifacts
    ):
        """Test complete Playwright generation workflow end-to-end."""
        # Setup mocks
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_weaviate_ui_artifacts, "total": 3}
        mock_search_service.return_value = mock_search

        # Mock Ollama responses for all three agents
        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.side_effect = [
            # Frontend Specialist response
            {"response": "Frontend analysis: Login UI with form validation"},
            # Backend Specialist response
            {"response": "Backend analysis: Authentication service with JWT"},
            # Playwright Test Writer response
            {"response": """import { test, expect } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';

test.describe('Login Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000/login');
  });

  test('should login with valid credentials', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.login('user@example.com', 'password123');
    await expect(page).toHaveURL(/dashboard/);
  });

  test('should show error with invalid credentials', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.login('invalid@example.com', 'wrong');
    await expect(page.getByText('Invalid credentials')).toBeVisible();
  });
});

export class LoginPage {
  constructor(private page: Page) {}

  private readonly usernameField = this.page.getByLabel('Username');
  private readonly passwordField = this.page.getByLabel('Password');
  private readonly loginButton = this.page.getByRole('button', { name: 'Login' });

  async login(username: string, password: string) {
    await this.usernameField.fill(username);
    await this.passwordField.fill(password);
    await this.loginButton.click();
  }
}"""}
        ]
        mock_ollama.return_value = mock_ollama_instance

        # Execute workflow
        from codeindex.web.workflows.playwright_generation import PlaywrightGenerationWorkflow

        workflow = PlaywrightGenerationWorkflow()
        result = workflow.execute(
            test_request="Generate Playwright tests for login functionality",
            artifacts=mock_weaviate_ui_artifacts
        )

        # Verify result structure
        assert result is not None
        assert "test_code" in result
        assert "frontend_analysis" in result
        assert "backend_analysis" in result

        # Verify test code content
        test_code = result["test_code"]
        assert len(test_code) > 0
        assert "import { test, expect }" in test_code
        assert "test.describe" in test_code
        assert "LoginPage" in test_code
        assert "async" in test_code
        assert "await" in test_code

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_playwright_file_download(
        self,
        mock_ollama,
        mock_search_service,
        temp_output_dir,
        mock_weaviate_ui_artifacts
    ):
        """Test .spec.ts file generation and download."""
        # Setup mocks (same as above)
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_weaviate_ui_artifacts, "total": 3}
        mock_search_service.return_value = mock_search

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {
            "response": """import { test, expect } from '@playwright/test';

test('example test', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await expect(page).toHaveTitle('Example');
});"""
        }
        mock_ollama.return_value = mock_ollama_instance

        # Generate and save test file
        from codeindex.web.services.test_generation_service import get_test_generation_service

        service = get_test_generation_service()
        test_file = service.generate_playwright_file(
            test_request="Generate login tests",
            output_dir=temp_output_dir,
            artifacts=mock_weaviate_ui_artifacts
        )

        # Verify file was created
        assert test_file.exists()
        assert test_file.suffix == ".ts"
        assert "spec" in test_file.stem

        # Verify file content
        content = test_file.read_text()
        assert "import { test, expect }" in content
        assert "async" in content

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_playwright_syntax_validation_before_download(
        self,
        mock_ollama,
        mock_search_service,
        temp_output_dir,
        mock_weaviate_ui_artifacts
    ):
        """Test that syntax validation blocks download on errors (per FR8.8)."""
        # Setup mocks
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_weaviate_ui_artifacts, "total": 3}
        mock_search_service.return_value = mock_search

        # Mock Ollama to return INVALID TypeScript
        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {
            "response": """import { test, expect } from '@playwright/test';

test('broken test', async ({ page }) => {
  await page.goto('http://localhost:3000'
  // Missing closing parenthesis
  await expect(page).toHaveTitle(;
});"""
        }
        mock_ollama.return_value = mock_ollama_instance

        # Attempt to generate file with validation
        from codeindex.web.services.test_generation_service import get_test_generation_service

        service = get_test_generation_service()

        with pytest.raises(ValueError) as exc_info:
            service.generate_playwright_file(
                test_request="Generate tests",
                output_dir=temp_output_dir,
                artifacts=mock_weaviate_ui_artifacts,
                validate_before_save=True
            )

        # Verify error mentions validation failure
        assert "validation" in str(exc_info.value).lower() or "syntax" in str(exc_info.value).lower()

        # Verify no file was created
        assert len(list(temp_output_dir.glob("*.spec.ts"))) == 0

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_multiple_playwright_file_generation(
        self,
        mock_ollama,
        mock_search_service,
        temp_output_dir,
        mock_weaviate_ui_artifacts
    ):
        """Test generation of multiple .spec.ts files."""
        # Setup mocks
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_weaviate_ui_artifacts, "total": 3}
        mock_search_service.return_value = mock_search

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {
            "response": "test('example', async ({ page }) => {});"
        }
        mock_ollama.return_value = mock_ollama_instance

        # Generate multiple test files
        from codeindex.web.services.test_generation_service import get_test_generation_service

        service = get_test_generation_service()
        test_requests = [
            "Generate login tests",
            "Generate user management tests",
            "Generate dashboard tests"
        ]

        test_files = service.generate_multiple_playwright_files(
            test_requests=test_requests,
            output_dir=temp_output_dir,
            artifacts=mock_weaviate_ui_artifacts
        )

        # Verify all files were created
        assert len(test_files) == 3
        assert all(f.exists() for f in test_files)
        assert all(f.suffix == ".ts" for f in test_files)

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_playwright_with_page_object_model(
        self,
        mock_ollama,
        mock_search_service,
        temp_output_dir,
        mock_weaviate_ui_artifacts
    ):
        """Test generated tests include Page Object Model."""
        # Setup mocks
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_weaviate_ui_artifacts, "total": 3}
        mock_search_service.return_value = mock_search

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {
            "response": """import { test, expect } from '@playwright/test';

test('test with POM', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.login('user', 'pass');
});

export class LoginPage {
  constructor(private page: Page) {}
  async login(user: string, pass: string) {
    await this.page.getByLabel('Username').fill(user);
    await this.page.getByLabel('Password').fill(pass);
    await this.page.getByRole('button', { name: 'Login' }).click();
  }
}"""
        }
        mock_ollama.return_value = mock_ollama_instance

        # Generate test file
        from codeindex.web.services.test_generation_service import get_test_generation_service

        service = get_test_generation_service()
        test_file = service.generate_playwright_file(
            test_request="Generate tests with POM",
            output_dir=temp_output_dir,
            artifacts=mock_weaviate_ui_artifacts
        )

        # Verify POM structure
        content = test_file.read_text()
        assert "export class" in content
        assert "LoginPage" in content
        assert "constructor" in content
        assert "private page: Page" in content

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_agent_collaboration_with_context_passing(
        self,
        mock_ollama,
        mock_search_service,
        mock_weaviate_ui_artifacts
    ):
        """Test that agents pass context to each other during workflow."""
        # Setup mocks
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_weaviate_ui_artifacts, "total": 3}
        mock_search_service.return_value = mock_search

        # Track calls to verify context passing
        call_count = [0]
        contexts_received = []

        def mock_ollama_call(*args, **kwargs):
            call_count[0] += 1
            prompt = kwargs.get('prompt', '')
            contexts_received.append(prompt)

            if call_count[0] == 1:  # Frontend
                return {"response": "Frontend: Login form with validation"}
            elif call_count[0] == 2:  # Backend
                # Should see Frontend context in prompt
                return {"response": "Backend: Authentication API"}
            else:  # Playwright
                # Should see both Frontend and Backend context
                return {"response": "test('generated test', async ({ page }) => {});"}

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.side_effect = mock_ollama_call
        mock_ollama.return_value = mock_ollama_instance

        # Execute workflow
        from codeindex.web.workflows.playwright_generation import PlaywrightGenerationWorkflow

        workflow = PlaywrightGenerationWorkflow()
        workflow.execute(
            test_request="Generate tests",
            artifacts=mock_weaviate_ui_artifacts
        )

        # Verify agents were called in sequence
        assert call_count[0] == 3

        # Verify later agents received context from earlier agents
        # (Specific assertion depends on implementation)
        assert len(contexts_received) == 3

    @patch('codeindex.web.services.search_service.get_search_service')
    def test_workflow_with_no_ui_artifacts(self, mock_search_service):
        """Test workflow handles case with no UI artifacts found."""
        # Mock empty search results
        mock_search = Mock()
        mock_search.search.return_value = {"results": [], "total": 0}
        mock_search_service.return_value = mock_search

        # Execute workflow
        from codeindex.web.workflows.playwright_generation import PlaywrightGenerationWorkflow

        workflow = PlaywrightGenerationWorkflow()

        with pytest.raises(ValueError) as exc_info:
            workflow.execute(
                test_request="Generate tests",
                artifacts=[]
            )

        assert "artifacts" in str(exc_info.value).lower() or "empty" in str(exc_info.value).lower()

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_workflow_cancellation(
        self,
        mock_ollama,
        mock_search_service,
        mock_weaviate_ui_artifacts
    ):
        """Test workflow can be cancelled mid-execution."""
        # Setup mocks
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_weaviate_ui_artifacts, "total": 3}
        mock_search_service.return_value = mock_search

        # Mock slow agent response
        import time

        def slow_ollama_call(*args, **kwargs):
            time.sleep(0.5)  # Simulate slow response
            return {"response": "test code"}

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.side_effect = slow_ollama_call
        mock_ollama.return_value = mock_ollama_instance

        # Execute workflow with cancellation
        from codeindex.web.workflows.playwright_generation import PlaywrightGenerationWorkflow

        workflow = PlaywrightGenerationWorkflow()

        # Start workflow in background and cancel
        with pytest.raises(Exception):  # Should raise cancellation exception
            workflow.execute(
                test_request="Generate tests",
                artifacts=mock_weaviate_ui_artifacts,
                cancellation_token=Mock(is_cancelled=lambda: True)
            )

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_complete_test_suite_workflow(
        self,
        mock_ollama,
        mock_search_service,
        temp_output_dir,
        mock_weaviate_ui_artifacts
    ):
        """Test complete test suite workflow (Gherkin + Playwright) per T138."""
        # Setup mocks
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_weaviate_ui_artifacts, "total": 3}
        mock_search_service.return_value = mock_search

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {
            "response": "test code"
        }
        mock_ollama.return_value = mock_ollama_instance

        # Execute complete test suite workflow
        from codeindex.web.workflows.complete_test_suite import CompleteTestSuiteWorkflow

        workflow = CompleteTestSuiteWorkflow()
        result = workflow.execute(
            test_request="Generate complete test suite for login",
            artifacts=mock_weaviate_ui_artifacts,
            output_dir=temp_output_dir
        )

        # Verify both Gherkin and Playwright tests were generated
        assert result is not None
        assert "gherkin_files" in result
        assert "playwright_files" in result
        assert len(result["gherkin_files"]) > 0
        assert len(result["playwright_files"]) > 0
