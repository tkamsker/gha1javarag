"""
Integration test for end-to-end Gherkin test generation (T115 - US2.5).

Tests complete workflow from user story input to .feature file generation,
including syntax validation and download functionality.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from typing import Dict, Any, List
import tempfile
import zipfile


class TestGherkinGenerationIntegration:
    """Integration test suite for complete Gherkin generation workflow."""

    @pytest.fixture
    def mock_search_results(self) -> List[Dict[str, Any]]:
        """Mock Weaviate search results for login feature."""
        return [
            {
                "id": "req-001",
                "artifactType": "Requirement",
                "fileName": "login_feature.md",
                "relativePath": "specs/login_feature.md",
                "summary": "User login with email and password validation",
                "entities": ["login", "authentication", "email", "password"],
                "_additional": {"id": "req-001", "distance": 0.05}
            },
            {
                "id": "form-001",
                "artifactType": "JspForm",
                "fileName": "LoginForm.jsp",
                "relativePath": "src/main/webapp/forms/LoginForm.jsp",
                "summary": "Login form with email and password fields",
                "entities": ["email", "password", "submit", "validation"],
                "_additional": {"id": "form-001", "distance": 0.08}
            },
            {
                "id": "presenter-001",
                "artifactType": "GwtPresenter",
                "fileName": "UserPresenter.java",
                "relativePath": "src/main/java/com/app/client/UserPresenter.java",
                "summary": "Handles login form submission and navigation",
                "entities": ["login", "validate", "authenticate"],
                "_additional": {"id": "presenter-001", "distance": 0.10}
            }
        ]

    @pytest.fixture
    def complete_gherkin_feature(self) -> str:
        """Complete valid Gherkin feature file."""
        return """Feature: User Login
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
    And I should see my username "John Doe"
    And I should see the logout button

  Scenario: Failed login with invalid email
    Given I am on the login page
    When I enter "invalid@example.com" in the email field
    And I enter "ValidPass123!" in the password field
    And I click the "Login" button
    Then I should see an error message "Invalid credentials"
    And I should remain on the login page
    And the password field should be cleared

  Scenario: Failed login with invalid password
    Given I am on the login page
    When I enter "user@example.com" in the email field
    And I enter "WrongPassword" in the password field
    And I click the "Login" button
    Then I should see an error message "Invalid credentials"
    And I should remain on the login page
    And the password field should be cleared

  Scenario Outline: Login validation errors
    Given I am on the login page
    When I enter "<email>" in the email field
    And I enter "<password>" in the password field
    And I click the "Login" button
    Then I should see an error message "<error>"
    And I should remain on the login page

    Examples:
      | email              | password   | error                       |
      |                    | Pass123!   | Email is required           |
      | invalid-email      | Pass123!   | Invalid email format        |
      | user@example.com   |            | Password is required        |
      | user@example.com   | short      | Password must be at least 8 characters |

  Scenario: Account lockout after multiple failed attempts
    Given I am on the login page
    When I enter "user@example.com" in the email field
    And I enter an incorrect password 5 times
    Then I should see an error message "Account locked. Please try again in 15 minutes"
    And the login form should be disabled

  Scenario: Password visibility toggle
    Given I am on the login page
    When I enter "MySecretPassword" in the password field
    Then the password should be hidden
    When I click the "Show password" button
    Then the password should be visible
    When I click the "Hide password" button
    Then the password should be hidden"""

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_end_to_end_gherkin_generation(
        self,
        mock_ollama,
        mock_search_service,
        mock_search_results,
        complete_gherkin_feature
    ):
        """Test complete end-to-end Gherkin generation workflow."""
        from codeindex.web.workflows.gherkin_generation import GherkinGenerationWorkflow

        # Mock search service
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_search_results}
        mock_search_service.return_value = mock_search

        # Mock Ollama to return complete Gherkin feature
        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {"response": complete_gherkin_feature}
        mock_ollama.return_value = mock_ollama_instance

        # Execute workflow
        workflow = GherkinGenerationWorkflow()
        result = workflow.execute("Generate Gherkin tests for user login feature")

        # Verify complete workflow execution
        assert result is not None
        assert "gherkin_content" in result
        assert "Feature: User Login" in result["gherkin_content"]
        assert "Scenario:" in result["gherkin_content"]
        assert "Background:" in result["gherkin_content"]
        assert "Scenario Outline:" in result["gherkin_content"]
        assert "Examples:" in result["gherkin_content"]

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_gherkin_generation_with_syntax_validation(
        self,
        mock_ollama,
        mock_search_service,
        mock_search_results,
        complete_gherkin_feature
    ):
        """Test Gherkin generation includes syntax validation."""
        from codeindex.web.workflows.gherkin_generation import GherkinGenerationWorkflow

        # Mock services
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_search_results}
        mock_search_service.return_value = mock_search

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {"response": complete_gherkin_feature}
        mock_ollama.return_value = mock_ollama_instance

        # Execute workflow
        workflow = GherkinGenerationWorkflow()
        result = workflow.execute("Generate tests for login")

        # Verify syntax validation performed
        assert "validation" in result
        assert result["validation"]["is_valid"] is True
        assert len(result["validation"]["errors"]) == 0

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_feature_file_download_generation(
        self,
        mock_ollama,
        mock_search_service,
        mock_search_results,
        complete_gherkin_feature,
        tmp_path
    ):
        """Test .feature file can be generated for download."""
        from codeindex.web.services.test_generation_service import TestGenerationService

        # Mock services
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_search_results}
        mock_search_service.return_value = mock_search

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {"response": complete_gherkin_feature}
        mock_ollama.return_value = mock_ollama_instance

        # Generate and save feature file
        service = TestGenerationService()
        feature_file_path = service.generate_feature_file(
            user_story="User login",
            output_dir=tmp_path
        )

        # Verify file created
        assert feature_file_path.exists()
        assert feature_file_path.suffix == ".feature"

        # Verify file content
        content = feature_file_path.read_text()
        assert "Feature: User Login" in content
        assert "Scenario:" in content

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_invalid_gherkin_blocks_download(
        self,
        mock_ollama,
        mock_search_service,
        mock_search_results,
        tmp_path
    ):
        """Test invalid Gherkin syntax blocks download (per FR8.8)."""
        from codeindex.web.services.test_generation_service import TestGenerationService

        # Mock services
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_search_results}
        mock_search_service.return_value = mock_search

        # Mock Ollama to return INVALID Gherkin
        invalid_gherkin = """User Login
  Scenario: Login
    WhenWhat I enter credentials
    Then I see dashboard"""

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {"response": invalid_gherkin}
        mock_ollama.return_value = mock_ollama_instance

        # Attempt to generate feature file
        service = TestGenerationService()

        with pytest.raises(ValueError) as exc_info:
            service.generate_feature_file(
                user_story="User login",
                output_dir=tmp_path
            )

        # Verify error mentions syntax validation
        assert "syntax" in str(exc_info.value).lower() or "invalid" in str(exc_info.value).lower()

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_multiple_feature_files_zip_download(
        self,
        mock_ollama,
        mock_search_service,
        mock_search_results,
        complete_gherkin_feature,
        tmp_path
    ):
        """Test multiple .feature files can be zipped for download."""
        from codeindex.web.services.test_generation_service import TestGenerationService

        # Mock services
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_search_results}
        mock_search_service.return_value = mock_search

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {"response": complete_gherkin_feature}
        mock_ollama.return_value = mock_ollama_instance

        # Generate multiple feature files
        service = TestGenerationService()
        feature_files = []
        for story in ["Login", "Registration", "Password Reset"]:
            feature_file = service.generate_feature_file(
                user_story=story,
                output_dir=tmp_path
            )
            feature_files.append(feature_file)

        # Create zip file
        zip_path = tmp_path / "gherkin_tests.zip"
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for feature_file in feature_files:
                zipf.write(feature_file, feature_file.name)

        # Verify zip file created and contains all files
        assert zip_path.exists()

        with zipfile.ZipFile(zip_path, 'r') as zipf:
            file_list = zipf.namelist()
            assert len(file_list) == 3
            assert all(name.endswith('.feature') for name in file_list)

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_gherkin_generation_under_2_minutes(
        self,
        mock_ollama,
        mock_search_service,
        mock_search_results,
        complete_gherkin_feature
    ):
        """Test Gherkin generation completes in under 2 minutes (per acceptance criteria)."""
        from codeindex.web.workflows.gherkin_generation import GherkinGenerationWorkflow
        import time

        # Mock services
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_search_results}
        mock_search_service.return_value = mock_search

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {"response": complete_gherkin_feature}
        mock_ollama.return_value = mock_ollama_instance

        # Execute workflow with timing
        workflow = GherkinGenerationWorkflow()
        start_time = time.time()
        result = workflow.execute("Generate tests for login")
        end_time = time.time()

        # Verify completion time (should be much faster with mocks, but check structure is correct)
        duration = end_time - start_time
        assert duration < 120.0  # 2 minutes

        # Verify duration is tracked in result
        assert "total_duration_seconds" in result

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_gherkin_includes_all_scenario_types(
        self,
        mock_ollama,
        mock_search_service,
        mock_search_results,
        complete_gherkin_feature
    ):
        """Test generated Gherkin includes all scenario types (happy path, errors, edge cases)."""
        from codeindex.web.workflows.gherkin_generation import GherkinGenerationWorkflow

        # Mock services
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_search_results}
        mock_search_service.return_value = mock_search

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {"response": complete_gherkin_feature}
        mock_ollama.return_value = mock_ollama_instance

        # Execute workflow
        workflow = GherkinGenerationWorkflow()
        result = workflow.execute("Generate comprehensive tests for login")

        gherkin_content = result["gherkin_content"]

        # Verify happy path scenario
        assert "Successful login" in gherkin_content

        # Verify error scenarios
        assert "Failed login" in gherkin_content or "invalid" in gherkin_content.lower()

        # Verify edge cases (validation errors, boundary conditions)
        assert "validation" in gherkin_content.lower() or "Scenario Outline:" in gherkin_content

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_test_coverage_summary_generation(
        self,
        mock_ollama,
        mock_search_service,
        mock_search_results,
        complete_gherkin_feature
    ):
        """Test generation includes test coverage summary."""
        from codeindex.web.services.test_generation_service import TestGenerationService

        # Mock services
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_search_results}
        mock_search_service.return_value = mock_search

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {"response": complete_gherkin_feature}
        mock_ollama.return_value = mock_ollama_instance

        # Generate and analyze
        service = TestGenerationService()
        result = service.generate_gherkin_with_summary("Generate tests for login")

        # Verify summary exists
        assert "summary" in result
        assert "scenario_count" in result["summary"]
        assert "step_count" in result["summary"]
        assert "example_count" in result["summary"]

        # Verify counts are correct
        assert result["summary"]["scenario_count"] >= 4  # Should have multiple scenarios
        assert result["summary"]["step_count"] > 0
        assert result["summary"]["example_count"] >= 1  # Has Scenario Outline with Examples

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_gherkin_references_source_artifacts(
        self,
        mock_ollama,
        mock_search_service,
        mock_search_results,
        complete_gherkin_feature
    ):
        """Test generated Gherkin references source artifacts (forms, presenters, requirements)."""
        from codeindex.web.workflows.gherkin_generation import GherkinGenerationWorkflow

        # Mock services
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_search_results}
        mock_search_service.return_value = mock_search

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {"response": complete_gherkin_feature}
        mock_ollama.return_value = mock_ollama_instance

        # Execute workflow
        workflow = GherkinGenerationWorkflow()
        result = workflow.execute("Generate tests for login")

        # Verify citations reference source artifacts
        assert "citations" in result
        assert len(result["citations"]) > 0

        # Check that citations include expected artifact types
        artifact_types = [c.artifact_type for c in result["citations"]]
        assert "Requirement" in artifact_types or "JspForm" in artifact_types or "GwtPresenter" in artifact_types

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_workflow_completes_despite_partial_search_results(
        self,
        mock_ollama,
        mock_search_service,
        complete_gherkin_feature
    ):
        """Test workflow completes successfully even with limited search results."""
        from codeindex.web.workflows.gherkin_generation import GherkinGenerationWorkflow

        # Mock search with limited results
        mock_search = Mock()
        mock_search.search.return_value = {
            "results": [
                {
                    "id": "req-001",
                    "artifactType": "Requirement",
                    "fileName": "login.md",
                    "relativePath": "specs/login.md",
                    "summary": "User login requirement",
                    "_additional": {"id": "req-001", "distance": 0.2}
                }
            ]
        }
        mock_search_service.return_value = mock_search

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {"response": complete_gherkin_feature}
        mock_ollama.return_value = mock_ollama_instance

        # Execute workflow
        workflow = GherkinGenerationWorkflow()
        result = workflow.execute("Generate tests")

        # Verify workflow completed successfully
        assert result is not None
        assert "gherkin_content" in result
        assert "Feature:" in result["gherkin_content"]

    @patch('codeindex.web.services.search_service.get_search_service')
    @patch('codeindex.services.ollama_client.OllamaClient')
    def test_gherkin_generation_includes_background_for_common_setup(
        self,
        mock_ollama,
        mock_search_service,
        mock_search_results,
        complete_gherkin_feature
    ):
        """Test generated Gherkin includes Background section for common setup steps."""
        from codeindex.web.workflows.gherkin_generation import GherkinGenerationWorkflow

        # Mock services
        mock_search = Mock()
        mock_search.search.return_value = {"results": mock_search_results}
        mock_search_service.return_value = mock_search

        mock_ollama_instance = Mock()
        mock_ollama_instance.call_ollama.return_value = {"response": complete_gherkin_feature}
        mock_ollama.return_value = mock_ollama_instance

        # Execute workflow
        workflow = GherkinGenerationWorkflow()
        result = workflow.execute("Generate tests for login")

        # Verify Background section exists
        assert "Background:" in result["gherkin_content"]

        # Verify Background has setup steps
        lines = result["gherkin_content"].split('\n')
        background_idx = next(i for i, line in enumerate(lines) if "Background:" in line)
        # Next few lines after Background should be steps (Given/And)
        assert any("Given" in lines[background_idx + i] or "And" in lines[background_idx + i]
                   for i in range(1, 5))
