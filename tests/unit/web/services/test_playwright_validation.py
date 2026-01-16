"""
Unit tests for Playwright validation service (T127).

Tests .spec.ts/.spec.js parsing, syntax checking, locator validation,
and TypeScript/JavaScript validation.
"""

import pytest
from pathlib import Path
from typing import List, Dict, Any


class TestPlaywrightValidation:
    """Test suite for Playwright TypeScript/JavaScript validation."""

    @pytest.fixture
    def valid_typescript_test(self) -> str:
        """Valid Playwright TypeScript test."""
        return """import { test, expect } from '@playwright/test';
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
});"""

    @pytest.fixture
    def valid_javascript_test(self) -> str:
        """Valid Playwright JavaScript test."""
        return """const { test, expect } = require('@playwright/test');

test('basic navigation test', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await expect(page).toHaveTitle(/Example/);
});"""

    @pytest.fixture
    def invalid_syntax_test(self) -> str:
        """Test with syntax errors."""
        return """import { test, expect } from '@playwright/test';

test('broken test', async ({ page }) => {
  await page.goto('http://localhost:3000'
  // Missing closing parenthesis
  await expect(page).toBeVisible(;
});"""

    @pytest.fixture
    def missing_imports_test(self) -> str:
        """Test missing required imports."""
        return """// Missing import statement

test('test without imports', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await expect(page).toHaveTitle('Example');
});"""

    @pytest.fixture
    def invalid_locators_test(self) -> str:
        """Test with invalid locators."""
        return """import { test, expect } from '@playwright/test';

test('test with bad locators', async ({ page }) => {
  await page.goto('http://localhost:3000');

  // Invalid XPath
  await page.locator('//div[@id=unclosed').click();

  // Invalid CSS selector
  await page.locator('[data-testid=').click();
});"""

    def test_validate_valid_typescript(self, valid_typescript_test):
        """Test validation of valid TypeScript test file."""
        from codeindex.web.services.playwright_validation import validate_playwright_syntax

        is_valid, errors = validate_playwright_syntax(valid_typescript_test, language='typescript')

        assert is_valid is True
        assert len(errors) == 0

    def test_validate_valid_javascript(self, valid_javascript_test):
        """Test validation of valid JavaScript test file."""
        from codeindex.web.services.playwright_validation import validate_playwright_syntax

        is_valid, errors = validate_playwright_syntax(valid_javascript_test, language='javascript')

        assert is_valid is True
        assert len(errors) == 0

    def test_validate_syntax_errors(self, invalid_syntax_test):
        """Test detection of syntax errors."""
        from codeindex.web.services.playwright_validation import validate_playwright_syntax

        is_valid, errors = validate_playwright_syntax(invalid_syntax_test, language='typescript')

        assert is_valid is False
        assert len(errors) > 0
        # Should detect missing parenthesis/semicolon
        assert any('syntax' in err.lower() or 'parenthesis' in err.lower() for err in errors)

    def test_validate_missing_imports(self, missing_imports_test):
        """Test detection of missing imports."""
        from codeindex.web.services.playwright_validation import validate_playwright_syntax

        is_valid, errors = validate_playwright_syntax(missing_imports_test, language='typescript')

        assert is_valid is False
        assert len(errors) > 0
        # Should detect missing Playwright imports
        assert any('import' in err.lower() for err in errors)

    def test_validate_invalid_locators(self, invalid_locators_test):
        """Test detection of invalid locators."""
        from codeindex.web.services.playwright_validation import validate_playwright_syntax

        is_valid, errors = validate_playwright_syntax(invalid_locators_test, language='typescript')

        assert is_valid is False
        assert len(errors) > 0
        # Should detect invalid XPath/CSS selectors
        assert any('locator' in err.lower() or 'selector' in err.lower() for err in errors)

    def test_validate_empty_file(self):
        """Test validation of empty file."""
        from codeindex.web.services.playwright_validation import validate_playwright_syntax

        is_valid, errors = validate_playwright_syntax("", language='typescript')

        assert is_valid is False
        assert len(errors) > 0
        assert any('empty' in err.lower() for err in errors)

    def test_count_test_elements(self, valid_typescript_test):
        """Test counting test elements (describe blocks, tests, expects)."""
        from codeindex.web.services.playwright_validation import count_playwright_elements

        counts = count_playwright_elements(valid_typescript_test)

        assert counts["describe_blocks"] >= 1
        assert counts["test_cases"] >= 1
        assert counts["expectations"] >= 1
        assert counts["beforeEach_hooks"] >= 1

    def test_count_test_elements_empty(self):
        """Test counting elements in empty file."""
        from codeindex.web.services.playwright_validation import count_playwright_elements

        counts = count_playwright_elements("")

        assert counts["describe_blocks"] == 0
        assert counts["test_cases"] == 0
        assert counts["expectations"] == 0
        assert counts["beforeEach_hooks"] == 0

    def test_extract_locators(self, valid_typescript_test):
        """Test extraction of locators from test code."""
        from codeindex.web.services.playwright_validation import extract_locators

        locators = extract_locators(valid_typescript_test)

        assert len(locators) > 0
        # Should find various locator types
        assert any(loc["type"] in ["getByRole", "getByLabel", "locator", "selector"] for loc in locators)

    def test_validate_page_object_model(self):
        """Test validation of Page Object Model structure."""
        from codeindex.web.services.playwright_validation import validate_page_object_model

        pom_code = """export class LoginPage {
  constructor(private page: Page) {}

  private readonly usernameField = this.page.getByLabel('Username');
  private readonly passwordField = this.page.getByLabel('Password');
  private readonly loginButton = this.page.getByRole('button', { name: 'Login' });

  async login(username: string, password: string) {
    await this.usernameField.fill(username);
    await this.passwordField.fill(password);
    await this.loginButton.click();
  }

  async expectLoginSuccess() {
    await expect(this.page).toHaveURL(/dashboard/);
  }
}"""

        is_valid, errors = validate_page_object_model(pom_code)

        assert is_valid is True
        assert len(errors) == 0

    def test_validate_invalid_page_object_model(self):
        """Test detection of invalid Page Object Model."""
        from codeindex.web.services.playwright_validation import validate_page_object_model

        # Missing constructor
        invalid_pom = """export class LoginPage {
  private readonly usernameField = this.page.getByLabel('Username');
}"""

        is_valid, errors = validate_page_object_model(invalid_pom)

        assert is_valid is False
        assert len(errors) > 0

    def test_validate_async_await_usage(self):
        """Test validation of async/await patterns."""
        from codeindex.web.services.playwright_validation import validate_async_patterns

        # Missing await
        invalid_async = """test('missing await', async ({ page }) => {
  page.goto('http://localhost:3000');  // Missing await
  await expect(page).toHaveTitle('Example');
});"""

        issues = validate_async_patterns(invalid_async)

        assert len(issues) > 0
        assert any('await' in issue.lower() for issue in issues)

    def test_validate_proper_async_await(self):
        """Test validation of proper async/await usage."""
        from codeindex.web.services.playwright_validation import validate_async_patterns

        valid_async = """test('proper await', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await expect(page).toHaveTitle('Example');
});"""

        issues = validate_async_patterns(valid_async)

        assert len(issues) == 0

    def test_detect_deprecated_api_usage(self):
        """Test detection of deprecated Playwright APIs."""
        from codeindex.web.services.playwright_validation import detect_deprecated_apis

        # Using deprecated API
        deprecated_code = """test('deprecated API', async ({ page }) => {
  await page.waitForSelector('.element');  // Deprecated in favor of locator.waitFor()
  const element = await page.$('.element');  // Deprecated in favor of locator()
});"""

        deprecated_apis = detect_deprecated_apis(deprecated_code)

        assert len(deprecated_apis) > 0
        assert any('waitForSelector' in api or '$' in api for api in deprecated_apis)

    def test_validate_test_isolation(self):
        """Test detection of test isolation issues."""
        from codeindex.web.services.playwright_validation import validate_test_isolation

        # Shared mutable state
        isolation_issue = """let sharedState = {};

test('test 1', async ({ page }) => {
  sharedState.data = 'value';
});

test('test 2', async ({ page }) => {
  expect(sharedState.data).toBe('value');  // Bad: depends on test 1
});"""

        issues = validate_test_isolation(isolation_issue)

        assert len(issues) > 0
        assert any('isolation' in issue.lower() or 'shared' in issue.lower() for issue in issues)

    def test_validate_selector_best_practices(self):
        """Test validation of selector best practices."""
        from codeindex.web.services.playwright_validation import validate_selector_practices

        # Using fragile selectors
        bad_selectors = """test('fragile selectors', async ({ page }) => {
  await page.locator('body > div:nth-child(2) > div > button').click();  // Bad: positional
  await page.locator('.btn-primary').click();  // Bad: class-based
});"""

        issues = validate_selector_practices(bad_selectors)

        assert len(issues) > 0
        # Should recommend semantic locators
        assert any('data-testid' in issue.lower() or 'getByRole' in issue.lower() for issue in issues)

    def test_validate_good_selector_practices(self):
        """Test validation passes for good selectors."""
        from codeindex.web.services.playwright_validation import validate_selector_practices

        good_selectors = """test('good selectors', async ({ page }) => {
  await page.getByRole('button', { name: 'Submit' }).click();
  await page.getByLabel('Username').fill('user');
  await page.locator('[data-testid="login-button"]').click();
});"""

        issues = validate_selector_practices(good_selectors)

        assert len(issues) == 0

    def test_parse_typescript_file(self, tmp_path):
        """Test parsing of .spec.ts file."""
        from codeindex.web.services.playwright_validation import parse_playwright_file

        test_file = tmp_path / "example.spec.ts"
        test_file.write_text("""import { test, expect } from '@playwright/test';

test('example test', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await expect(page).toHaveTitle('Example');
});""")

        result = parse_playwright_file(test_file)

        assert result["is_valid"] is True
        assert result["language"] == "typescript"
        assert len(result["errors"]) == 0
        assert result["test_count"] >= 1

    def test_parse_javascript_file(self, tmp_path):
        """Test parsing of .spec.js file."""
        from codeindex.web.services.playwright_validation import parse_playwright_file

        test_file = tmp_path / "example.spec.js"
        test_file.write_text("""const { test, expect } = require('@playwright/test');

test('example test', async ({ page }) => {
  await page.goto('http://localhost:3000');
});""")

        result = parse_playwright_file(test_file)

        assert result["is_valid"] is True
        assert result["language"] == "javascript"
        assert len(result["errors"]) == 0

    def test_parse_nonexistent_file(self, tmp_path):
        """Test parsing of nonexistent file."""
        from codeindex.web.services.playwright_validation import parse_playwright_file

        nonexistent_file = tmp_path / "nonexistent.spec.ts"

        with pytest.raises(FileNotFoundError):
            parse_playwright_file(nonexistent_file)

    def test_validate_multiple_files(self, tmp_path):
        """Test validation of multiple test files."""
        from codeindex.web.services.playwright_validation import validate_multiple_files

        # Create test files
        file1 = tmp_path / "test1.spec.ts"
        file1.write_text("import { test, expect } from '@playwright/test';\ntest('t1', async ({page}) => {});")

        file2 = tmp_path / "test2.spec.ts"
        file2.write_text("invalid syntax here")

        results = validate_multiple_files([file1, file2])

        assert len(results) == 2
        assert results[0]["is_valid"] is True
        assert results[1]["is_valid"] is False

    def test_generate_validation_report(self, valid_typescript_test, invalid_syntax_test):
        """Test generation of comprehensive validation report."""
        from codeindex.web.services.playwright_validation import generate_validation_report

        report = generate_validation_report(invalid_syntax_test, language='typescript')

        assert "is_valid" in report
        assert "errors" in report
        assert "warnings" in report
        assert "element_counts" in report
        assert "locators" in report
        assert report["is_valid"] is False
        assert len(report["errors"]) > 0
