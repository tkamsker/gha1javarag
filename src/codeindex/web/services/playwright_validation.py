"""
Playwright Validation Service (T127).

Provides TypeScript/JavaScript syntax validation, locator validation,
and best practices checking for Playwright test code.
"""

import logging
import re
from typing import List, Dict, Any, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)


def validate_playwright_syntax(code: str, language: str = 'typescript') -> Tuple[bool, List[str]]:
    """
    Validate Playwright test syntax.

    Args:
        code: Playwright test code
        language: 'typescript' or 'javascript'

    Returns:
        Tuple of (is_valid, errors)
    """
    errors = []

    # Check if empty
    if not code or not code.strip():
        errors.append("Empty test file")
        return False, errors

    # Check for required imports
    if language == 'typescript':
        if "import { test, expect }" not in code and "import { test" not in code:
            errors.append("Missing Playwright imports: import { test, expect } from '@playwright/test'")
    else:  # javascript
        if "require('@playwright/test')" not in code and "const { test" not in code:
            errors.append("Missing Playwright imports: require('@playwright/test')")

    # Check for syntax errors (basic patterns)
    # Unmatched parentheses
    if code.count('(') != code.count(')'):
        errors.append("Syntax error: Unmatched parentheses")

    # Unmatched brackets
    if code.count('[') != code.count(']'):
        errors.append("Syntax error: Unmatched brackets")

    # Unmatched braces
    if code.count('{') != code.count('}'):
        errors.append("Syntax error: Unmatched braces")

    # Check for invalid locators
    locator_errors = _check_invalid_locators(code)
    errors.extend(locator_errors)

    is_valid = len(errors) == 0
    return is_valid, errors


def count_playwright_elements(code: str) -> Dict[str, int]:
    """
    Count test elements in Playwright code.

    Args:
        code: Playwright test code

    Returns:
        Dictionary with counts: describe_blocks, test_cases, expectations, beforeEach_hooks
    """
    return {
        "describe_blocks": len(re.findall(r'test\.describe\s*\(', code)),
        "test_cases": len(re.findall(r'\btest\s*\(', code)),
        "expectations": len(re.findall(r'\bexpect\s*\(', code)),
        "beforeEach_hooks": len(re.findall(r'test\.beforeEach\s*\(', code)),
        "afterEach_hooks": len(re.findall(r'test\.afterEach\s*\(', code)),
        "beforeAll_hooks": len(re.findall(r'test\.beforeAll\s*\(', code)),
        "afterAll_hooks": len(re.findall(r'test\.afterAll\s*\(', code))
    }


def extract_locators(code: str) -> List[Dict[str, Any]]:
    """
    Extract locators from Playwright test code.

    Args:
        code: Playwright test code

    Returns:
        List of locator dictionaries with type and selector
    """
    locators = []

    # getByRole locators
    for match in re.finditer(r'getByRole\s*\(\s*[\'"](\w+)[\'"]', code):
        locators.append({"type": "getByRole", "selector": match.group(1)})

    # getByLabel locators
    for match in re.finditer(r'getByLabel\s*\(\s*[\'"]([^\'"]+)[\'"]', code):
        locators.append({"type": "getByLabel", "selector": match.group(1)})

    # getByText locators
    for match in re.finditer(r'getByText\s*\(\s*[\'"]([^\'"]+)[\'"]', code):
        locators.append({"type": "getByText", "selector": match.group(1)})

    # locator() with CSS/XPath
    for match in re.finditer(r'\.locator\s*\(\s*[\'"]([^\'"]+)[\'"]', code):
        selector = match.group(1)
        locators.append({"type": "locator", "selector": selector})

    # page.goto() - navigation selectors
    for match in re.finditer(r'page\.goto\s*\(\s*[\'"]([^\'"]+)[\'"]', code):
        locators.append({"type": "selector", "selector": match.group(1)})

    # toHaveURL() - URL assertions as selectors
    for match in re.finditer(r'toHaveURL\s*\(([^)]+)\)', code):
        locators.append({"type": "selector", "selector": match.group(1).strip()})

    return locators


def validate_page_object_model(code: str) -> Tuple[bool, List[str]]:
    """
    Validate Page Object Model structure.

    Args:
        code: Page Object Model code

    Returns:
        Tuple of (is_valid, errors)
    """
    errors = []

    # Check for class definition
    if "export class" not in code and "class" not in code:
        errors.append("Page Object Model must be defined as a class")

    # Check for constructor
    if "constructor" not in code:
        errors.append("Page Object Model must have a constructor")

    # Check for page parameter
    if "private page" not in code and "this.page" not in code:
        errors.append("Page Object Model constructor must accept page parameter")

    is_valid = len(errors) == 0
    return is_valid, errors


def validate_async_patterns(code: str) -> List[str]:
    """
    Validate async/await usage patterns.

    Args:
        code: Playwright test code

    Returns:
        List of issues found
    """
    issues = []

    # Check if code has any async functions
    if 'async' not in code:
        return issues

    # Check for common Playwright actions without await
    # This is a simplified check - full analysis would require AST parsing
    playwright_actions = [
        'page.goto', 'page.click', 'page.fill', 'page.type',
        'page.waitFor', 'page.locator', '.click()', '.fill(',
        '.waitFor(', 'expect(page)'
    ]

    lines = code.split('\n')
    in_async_context = False

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Track async context
        if 'async' in line and ('=>' in line or 'function' in line):
            in_async_context = True

        # Skip comments
        if stripped.startswith('//') or stripped.startswith('/*'):
            continue

        # Remove inline comments to check for await in code (not in comments)
        code_part = line.split('//')[0] if '//' in line else line

        # Skip lines with await in the code (not in comments)
        if 'await' in code_part:
            continue

        # Check if line has Playwright action without await in async context
        if in_async_context:
            for action in playwright_actions:
                if action in code_part:
                    issues.append(f"Line {i}: Missing 'await' for async operation: {stripped[:60]}")
                    break

    return issues


def detect_deprecated_apis(code: str) -> List[str]:
    """
    Detect deprecated Playwright APIs.

    Args:
        code: Playwright test code

    Returns:
        List of deprecated API usages
    """
    deprecated_apis = []

    # waitForSelector (deprecated in favor of locator().waitFor())
    if 'waitForSelector' in code:
        deprecated_apis.append("waitForSelector() is deprecated - use locator().waitFor() instead")

    # $ and $$ (deprecated in favor of locator())
    if re.search(r'page\.\$\(', code):
        deprecated_apis.append("page.$() is deprecated - use page.locator() instead")

    if re.search(r'page\.\$\$\(', code):
        deprecated_apis.append("page.$$() is deprecated - use page.locator().all() instead")

    # waitForTimeout (discouraged)
    if 'waitForTimeout' in code:
        deprecated_apis.append("waitForTimeout() is discouraged - use explicit waits with locator().waitFor() instead")

    return deprecated_apis


def validate_test_isolation(code: str) -> List[str]:
    """
    Validate test isolation (no shared mutable state).

    Args:
        code: Playwright test code

    Returns:
        List of isolation issues
    """
    issues = []

    # Check for variables declared outside test blocks
    lines = code.split('\n')
    in_test = False
    test_depth = 0

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Track when we're inside test blocks
        if 'test(' in stripped or 'test.describe(' in stripped:
            in_test = True
            test_depth += 1

        if in_test and stripped.startswith('}'):
            test_depth -= 1
            if test_depth == 0:
                in_test = False

        # Check for variable declarations outside tests
        if not in_test and (re.match(r'^let\s+\w+', stripped) or re.match(r'^var\s+\w+', stripped)):
            if '=' in stripped:  # Mutable declaration with assignment
                issues.append(f"Line {i}: Shared mutable state detected - use test fixtures or beforeEach instead")

    return issues


def validate_selector_practices(code: str) -> List[str]:
    """
    Validate selector best practices.

    Args:
        code: Playwright test code

    Returns:
        List of selector practice issues
    """
    issues = []

    # Check for fragile positional selectors
    if re.search(r':nth-child\(\d+\)', code):
        issues.append("Avoid positional selectors (:nth-child) - use semantic locators (getByRole, getByLabel, data-testid)")

    # Check for class-based selectors (brittle)
    class_selectors = re.findall(r'\.locator\s*\(\s*[\'"]\.[\w-]+[\'"]', code)
    if class_selectors and 'data-testid' not in code and 'getByRole' not in code:
        issues.append("Prefer semantic locators (getByRole, getByLabel, data-testid) over class-based selectors")

    # Check for good practices present
    has_semantic = bool(re.search(r'getByRole|getByLabel|getByText|data-testid', code))

    if not has_semantic and '.locator(' in code:
        issues.append("Consider using semantic locators: getByRole(), getByLabel(), getByText(), or [data-testid]")

    return issues


def parse_playwright_file(file_path: Path) -> Dict[str, Any]:
    """
    Parse Playwright test file and validate.

    Args:
        file_path: Path to .spec.ts or .spec.js file

    Returns:
        Dictionary with validation results

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Determine language from extension
    language = 'typescript' if file_path.suffix == '.ts' else 'javascript'

    # Read file content
    content = file_path.read_text(encoding='utf-8')

    # Validate syntax
    is_valid, errors = validate_playwright_syntax(content, language=language)

    # Count elements
    counts = count_playwright_elements(content)

    return {
        "is_valid": is_valid,
        "language": language,
        "errors": errors,
        "test_count": counts["test_cases"],
        "describe_count": counts["describe_blocks"],
        "element_counts": counts
    }


def validate_multiple_files(file_paths: List[Path]) -> List[Dict[str, Any]]:
    """
    Validate multiple Playwright test files.

    Args:
        file_paths: List of file paths to validate

    Returns:
        List of validation results for each file
    """
    results = []

    for file_path in file_paths:
        try:
            result = parse_playwright_file(file_path)
            result["file_path"] = str(file_path)
            results.append(result)
        except Exception as e:
            results.append({
                "file_path": str(file_path),
                "is_valid": False,
                "errors": [str(e)],
                "language": "unknown"
            })

    return results


def generate_validation_report(code: str, language: str = 'typescript') -> Dict[str, Any]:
    """
    Generate comprehensive validation report.

    Args:
        code: Playwright test code
        language: 'typescript' or 'javascript'

    Returns:
        Dictionary with comprehensive validation results
    """
    # Run all validations
    is_valid, errors = validate_playwright_syntax(code, language=language)
    element_counts = count_playwright_elements(code)
    locators = extract_locators(code)
    async_issues = validate_async_patterns(code)
    deprecated = detect_deprecated_apis(code)
    isolation_issues = validate_test_isolation(code)
    selector_issues = validate_selector_practices(code)

    # Combine warnings
    warnings = []
    warnings.extend(async_issues)
    warnings.extend(deprecated)
    warnings.extend(isolation_issues)
    warnings.extend(selector_issues)

    return {
        "is_valid": is_valid,
        "errors": errors,
        "warnings": warnings,
        "element_counts": element_counts,
        "locators": locators,
        "test_count": element_counts["test_cases"],
        "describe_count": element_counts["describe_blocks"],
        "locator_count": len(locators),
        "language": language
    }


def _check_invalid_locators(code: str) -> List[str]:
    """
    Check for invalid XPath and CSS selectors.

    Args:
        code: Playwright test code

    Returns:
        List of locator errors
    """
    errors = []

    # Find all locator calls
    locator_patterns = [
        r'\.locator\s*\(\s*[\'"]([^\'"]+)[\'"]',
        r'page\.waitForSelector\s*\(\s*[\'"]([^\'"]+)[\'"]'
    ]

    for pattern in locator_patterns:
        for match in re.finditer(pattern, code):
            selector = match.group(1)

            # Check for unclosed XPath predicates
            if selector.startswith('//') or selector.startswith('/'):
                if '[' in selector and ']' not in selector:
                    errors.append(f"Invalid XPath selector: Unclosed predicate in '{selector}'")
                if selector.count('[') != selector.count(']'):
                    errors.append(f"Invalid XPath selector: Mismatched brackets in '{selector}'")

            # Check for unclosed CSS attribute selectors
            if '[' in selector and '=' in selector:
                if selector.count('[') != selector.count(']'):
                    errors.append(f"Invalid CSS selector: Unclosed attribute selector in '{selector}'")
                # Check for unclosed quotes in attribute
                attr_part = selector[selector.find('['):]
                if attr_part.count('"') % 2 != 0 or attr_part.count("'") % 2 != 0:
                    errors.append(f"Invalid CSS selector: Unclosed quote in attribute '{selector}'")

    return errors


__all__ = [
    "validate_playwright_syntax",
    "count_playwright_elements",
    "extract_locators",
    "validate_page_object_model",
    "validate_async_patterns",
    "detect_deprecated_apis",
    "validate_test_isolation",
    "validate_selector_practices",
    "parse_playwright_file",
    "validate_multiple_files",
    "generate_validation_report"
]
