"""
Unit tests for Gherkin syntax validation (T113 - US2.5).

Tests .feature file parsing, Gherkin syntax checking, and error detection.
"""

import pytest
from unittest.mock import Mock, patch, mock_open
from typing import List, Dict, Any, Tuple


class TestGherkinValidation:
    """Test suite for Gherkin syntax validation."""

    @pytest.fixture
    def valid_gherkin_content(self) -> str:
        """Valid Gherkin feature file content."""
        return """Feature: User Login
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

  Scenario Outline: Login validation errors
    Given I am on the login page
    When I enter "<email>" in the email field
    And I enter "<password>" in the password field
    And I click the "Login" button
    Then I should see an error message "<error>"

    Examples:
      | email              | password   | error                    |
      | invalid-email      | Pass123!   | Invalid email format     |
      | user@example.com   |            | Password is required     |"""

    @pytest.fixture
    def invalid_gherkin_missing_feature(self) -> str:
        """Invalid Gherkin - missing Feature keyword."""
        return """User Login

  Scenario: Successful login
    Given I am on the login page
    When I enter credentials
    Then I should see the dashboard"""

    @pytest.fixture
    def invalid_gherkin_bad_keyword(self) -> str:
        """Invalid Gherkin - invalid keyword."""
        return """Feature: User Login

  Scenario: Successful login
    Given I am on the login page
    WhenWhat I enter credentials
    Then I should see the dashboard"""

    @pytest.fixture
    def invalid_gherkin_malformed_outline(self) -> str:
        """Invalid Gherkin - malformed Scenario Outline (missing Examples)."""
        return """Feature: User Login

  Scenario Outline: Login validation
    Given I am on the login page
    When I enter "<email>" in the email field
    Then I should see an error"""

    @pytest.fixture
    def invalid_gherkin_bad_table(self) -> str:
        """Invalid Gherkin - malformed table (inconsistent columns)."""
        return """Feature: User Login

  Scenario Outline: Login validation
    Given I am on the login page
    When I enter "<email>" in the email field
    Then I should see an error "<error>"

    Examples:
      | email              | password   | error                    |
      | invalid-email      | Pass123!   |"""

    def test_validate_valid_gherkin_syntax(self, valid_gherkin_content):
        """Test validation of syntactically correct Gherkin."""
        from codeindex.web.services.gherkin_validation import validate_gherkin_syntax

        is_valid, errors = validate_gherkin_syntax(valid_gherkin_content)

        assert is_valid is True
        assert len(errors) == 0

    def test_validate_gherkin_missing_feature_keyword(self, invalid_gherkin_missing_feature):
        """Test validation detects missing Feature keyword."""
        from codeindex.web.services.gherkin_validation import validate_gherkin_syntax

        is_valid, errors = validate_gherkin_syntax(invalid_gherkin_missing_feature)

        assert is_valid is False
        assert len(errors) > 0
        assert any("feature" in err.lower() for err in errors)

    def test_validate_gherkin_invalid_keyword(self, invalid_gherkin_bad_keyword):
        """Test validation detects invalid keywords."""
        from codeindex.web.services.gherkin_validation import validate_gherkin_syntax

        is_valid, errors = validate_gherkin_syntax(invalid_gherkin_bad_keyword)

        assert is_valid is False
        assert len(errors) > 0

    def test_validate_gherkin_malformed_scenario_outline(self, invalid_gherkin_malformed_outline):
        """Test validation detects Scenario Outline without Examples."""
        from codeindex.web.services.gherkin_validation import validate_gherkin_syntax

        is_valid, errors = validate_gherkin_syntax(invalid_gherkin_malformed_outline)

        assert is_valid is False
        assert len(errors) > 0
        assert any("example" in err.lower() or "outline" in err.lower() for err in errors)

    def test_validate_gherkin_malformed_table(self, invalid_gherkin_bad_table):
        """Test validation detects malformed data tables."""
        from codeindex.web.services.gherkin_validation import validate_gherkin_syntax

        is_valid, errors = validate_gherkin_syntax(invalid_gherkin_bad_table)

        assert is_valid is False
        assert len(errors) > 0

    def test_validation_returns_error_with_line_numbers(self, invalid_gherkin_bad_keyword):
        """Test validation errors include line numbers."""
        from codeindex.web.services.gherkin_validation import validate_gherkin_syntax

        is_valid, errors = validate_gherkin_syntax(invalid_gherkin_bad_keyword)

        assert is_valid is False
        # At least one error should contain line number reference
        assert any(any(char.isdigit() for char in err) for err in errors)

    def test_parse_feature_file_with_valid_syntax(self, valid_gherkin_content):
        """Test parsing valid .feature file."""
        from codeindex.web.services.gherkin_validation import parse_feature_file

        feature = parse_feature_file(valid_gherkin_content)

        assert feature is not None
        assert feature["name"] == "User Login"
        assert len(feature["scenarios"]) >= 2

    def test_parse_feature_file_extracts_feature_name(self, valid_gherkin_content):
        """Test parsing extracts feature name."""
        from codeindex.web.services.gherkin_validation import parse_feature_file

        feature = parse_feature_file(valid_gherkin_content)

        assert feature["name"] == "User Login"

    def test_parse_feature_file_extracts_scenarios(self, valid_gherkin_content):
        """Test parsing extracts scenarios."""
        from codeindex.web.services.gherkin_validation import parse_feature_file

        feature = parse_feature_file(valid_gherkin_content)

        assert "scenarios" in feature
        assert len(feature["scenarios"]) > 0
        assert any(s["name"] == "Successful login with valid credentials" for s in feature["scenarios"])

    def test_parse_feature_file_extracts_background(self, valid_gherkin_content):
        """Test parsing extracts Background section."""
        from codeindex.web.services.gherkin_validation import parse_feature_file

        feature = parse_feature_file(valid_gherkin_content)

        assert "background" in feature
        assert feature["background"] is not None
        assert len(feature["background"]["steps"]) > 0

    def test_parse_feature_file_extracts_scenario_steps(self, valid_gherkin_content):
        """Test parsing extracts scenario steps (Given/When/Then)."""
        from codeindex.web.services.gherkin_validation import parse_feature_file

        feature = parse_feature_file(valid_gherkin_content)

        first_scenario = feature["scenarios"][0]
        assert "steps" in first_scenario
        assert len(first_scenario["steps"]) > 0

        # Check step keywords
        step_keywords = [step["keyword"] for step in first_scenario["steps"]]
        assert "Given" in step_keywords
        assert "When" in step_keywords or "And" in step_keywords
        assert "Then" in step_keywords or "And" in step_keywords

    def test_parse_feature_file_extracts_scenario_outline(self, valid_gherkin_content):
        """Test parsing extracts Scenario Outline."""
        from codeindex.web.services.gherkin_validation import parse_feature_file

        feature = parse_feature_file(valid_gherkin_content)

        # Find Scenario Outline
        outlines = [s for s in feature["scenarios"] if s.get("is_outline", False)]
        assert len(outlines) > 0

    def test_parse_feature_file_extracts_examples_table(self, valid_gherkin_content):
        """Test parsing extracts Examples table from Scenario Outline."""
        from codeindex.web.services.gherkin_validation import parse_feature_file

        feature = parse_feature_file(valid_gherkin_content)

        # Find Scenario Outline
        outlines = [s for s in feature["scenarios"] if s.get("is_outline", False)]
        assert len(outlines) > 0

        outline = outlines[0]
        assert "examples" in outline
        assert len(outline["examples"]) > 0

        # Check table structure
        examples = outline["examples"][0]
        assert "header" in examples
        assert "rows" in examples
        assert len(examples["rows"]) > 0

    def test_validate_feature_file_from_path(self, tmp_path, valid_gherkin_content):
        """Test validation of .feature file from file path."""
        from codeindex.web.services.gherkin_validation import validate_feature_file

        # Write feature file
        feature_file = tmp_path / "login.feature"
        feature_file.write_text(valid_gherkin_content)

        is_valid, errors = validate_feature_file(str(feature_file))

        assert is_valid is True
        assert len(errors) == 0

    def test_validate_feature_file_detects_syntax_errors(self, tmp_path, invalid_gherkin_bad_keyword):
        """Test validation detects syntax errors in .feature file."""
        from codeindex.web.services.gherkin_validation import validate_feature_file

        # Write invalid feature file
        feature_file = tmp_path / "invalid.feature"
        feature_file.write_text(invalid_gherkin_bad_keyword)

        is_valid, errors = validate_feature_file(str(feature_file))

        assert is_valid is False
        assert len(errors) > 0

    def test_validate_feature_file_handles_missing_file(self):
        """Test validation handles missing .feature file."""
        from codeindex.web.services.gherkin_validation import validate_feature_file

        is_valid, errors = validate_feature_file("/nonexistent/file.feature")

        assert is_valid is False
        assert len(errors) > 0
        assert any("file" in err.lower() or "not found" in err.lower() for err in errors)

    def test_check_valid_gherkin_keywords(self):
        """Test validation recognizes valid Gherkin keywords."""
        from codeindex.web.services.gherkin_validation import is_valid_gherkin_keyword

        valid_keywords = ["Feature:", "Scenario:", "Scenario Outline:", "Background:",
                         "Given", "When", "Then", "And", "But", "Examples:"]

        for keyword in valid_keywords:
            assert is_valid_gherkin_keyword(keyword) is True

    def test_check_invalid_gherkin_keywords(self):
        """Test validation rejects invalid Gherkin keywords."""
        from codeindex.web.services.gherkin_validation import is_valid_gherkin_keyword

        invalid_keywords = ["WhenWhat", "ThenIf", "GivenMaybe", "RandomKeyword"]

        for keyword in invalid_keywords:
            assert is_valid_gherkin_keyword(keyword) is False

    def test_validate_gherkin_detects_empty_content(self):
        """Test validation detects empty Gherkin content."""
        from codeindex.web.services.gherkin_validation import validate_gherkin_syntax

        is_valid, errors = validate_gherkin_syntax("")

        assert is_valid is False
        assert len(errors) > 0
        assert any("empty" in err.lower() for err in errors)

    def test_validate_gherkin_detects_missing_scenarios(self):
        """Test validation detects Feature without scenarios."""
        from codeindex.web.services.gherkin_validation import validate_gherkin_syntax

        content = """Feature: User Login
  As a user I want to log in"""

        is_valid, errors = validate_gherkin_syntax(content)

        assert is_valid is False
        assert len(errors) > 0
        assert any("scenario" in err.lower() for err in errors)

    def test_get_syntax_error_details(self, invalid_gherkin_bad_keyword):
        """Test getting detailed syntax error information."""
        from codeindex.web.services.gherkin_validation import get_syntax_errors

        errors = get_syntax_errors(invalid_gherkin_bad_keyword)

        assert len(errors) > 0
        for error in errors:
            assert "line" in error
            assert "message" in error
            assert isinstance(error["line"], int)
            assert isinstance(error["message"], str)

    def test_validate_scenario_outline_has_examples(self):
        """Test validation ensures Scenario Outline has Examples."""
        from codeindex.web.services.gherkin_validation import validate_scenario_outline

        # Valid outline with examples
        valid_outline = {
            "name": "Test outline",
            "steps": [{"keyword": "When", "text": "I do <action>"}],
            "examples": [{"header": ["action"], "rows": [["click"]]}]
        }

        is_valid, errors = validate_scenario_outline(valid_outline)
        assert is_valid is True
        assert len(errors) == 0

        # Invalid outline without examples
        invalid_outline = {
            "name": "Test outline",
            "steps": [{"keyword": "When", "text": "I do <action>"}],
            "examples": []
        }

        is_valid, errors = validate_scenario_outline(invalid_outline)
        assert is_valid is False
        assert len(errors) > 0

    def test_validate_examples_table_structure(self):
        """Test validation of Examples table structure."""
        from codeindex.web.services.gherkin_validation import validate_examples_table

        # Valid table
        valid_table = {
            "header": ["email", "password", "error"],
            "rows": [
                ["test@example.com", "pass123", "Invalid"],
                ["user@test.com", "short", "Too short"]
            ]
        }

        is_valid, errors = validate_examples_table(valid_table)
        assert is_valid is True
        assert len(errors) == 0

        # Invalid table - inconsistent columns
        invalid_table = {
            "header": ["email", "password", "error"],
            "rows": [
                ["test@example.com", "pass123"],  # Missing column
                ["user@test.com", "short", "Too short"]
            ]
        }

        is_valid, errors = validate_examples_table(invalid_table)
        assert is_valid is False
        assert len(errors) > 0

    def test_validate_step_syntax(self):
        """Test validation of individual step syntax."""
        from codeindex.web.services.gherkin_validation import validate_step_syntax

        # Valid steps
        valid_steps = [
            "Given I am on the login page",
            "When I click the button",
            "Then I should see a message",
            "And I wait for the page to load",
            "But I should not see an error"
        ]

        for step in valid_steps:
            is_valid, error = validate_step_syntax(step)
            assert is_valid is True
            assert error is None

        # Invalid steps
        invalid_steps = [
            "NotAKeyword I do something",
            "Given",  # No step text
            "",  # Empty
        ]

        for step in invalid_steps:
            is_valid, error = validate_step_syntax(step)
            assert is_valid is False
            assert error is not None

    def test_extract_feature_metadata(self, valid_gherkin_content):
        """Test extraction of feature metadata."""
        from codeindex.web.services.gherkin_validation import extract_feature_metadata

        metadata = extract_feature_metadata(valid_gherkin_content)

        assert metadata["feature_name"] == "User Login"
        assert metadata["scenario_count"] >= 2
        assert metadata["step_count"] > 0
        assert "has_background" in metadata
        assert "has_scenario_outline" in metadata

    def test_count_gherkin_elements(self, valid_gherkin_content):
        """Test counting Gherkin elements for coverage summary."""
        from codeindex.web.services.gherkin_validation import count_gherkin_elements

        counts = count_gherkin_elements(valid_gherkin_content)

        assert counts["scenarios"] >= 2
        assert counts["steps"] > 0
        assert counts["examples"] >= 1  # One Scenario Outline with Examples
        assert counts["background_steps"] >= 2
