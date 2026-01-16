"""
Gherkin Syntax Validation Service (T122 - US2.5).

Provides Gherkin syntax validation using regex patterns to check for proper
structure, keywords, and formatting per FR8.8.
"""

import logging
import re
from typing import Tuple, List, Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


# Valid Gherkin keywords
VALID_KEYWORDS = {
    "Feature:", "Background:", "Scenario:", "Scenario Outline:", "Examples:",
    "Given", "When", "Then", "And", "But", "*"
}

STEP_KEYWORDS = {"Given", "When", "Then", "And", "But", "*"}


def validate_gherkin_syntax(content: str) -> Tuple[bool, List[str]]:
    """
    Validate Gherkin syntax for .feature file content.

    Validates:
    - Feature keyword present
    - Valid Gherkin keywords used
    - Scenario Outline has Examples
    - Proper structure and formatting

    Args:
        content: Gherkin feature file content

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    try:
        # Check for empty content
        if not content or not content.strip():
            errors.append("Empty Gherkin content")
            return False, errors

        lines = content.split('\n')

        # Check for Feature keyword
        has_feature = any(line.strip().startswith("Feature:") for line in lines)
        if not has_feature:
            errors.append("Missing Feature: keyword. All Gherkin files must start with Feature:")

        # Check for at least one Scenario
        has_scenario = any(
            line.strip().startswith("Scenario:") or line.strip().startswith("Scenario Outline:")
            for line in lines
        )
        if not has_scenario:
            errors.append("No Scenario or Scenario Outline found. Feature must have at least one scenario")

        # Validate keywords on each line
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith('#'):
                continue

            # Check for invalid keywords (e.g., "WhenWhat", "ThenIf")
            for keyword in VALID_KEYWORDS:
                if keyword in stripped and not stripped.startswith(keyword):
                    # Check if it's a malformed keyword
                    words = stripped.split()
                    if words and any(word.startswith(keyword.rstrip(':')) and word != keyword for word in words):
                        errors.append(f"Line {line_num}: Invalid keyword usage. Found malformed keyword near '{keyword}'")
                        break

        # Validate Scenario Outline has Examples
        in_scenario_outline = False
        scenario_outline_line = 0
        has_examples_for_outline = False

        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()

            if stripped.startswith("Scenario Outline:"):
                # Check previous Scenario Outline had Examples
                if in_scenario_outline and not has_examples_for_outline:
                    errors.append(f"Line {scenario_outline_line}: Scenario Outline missing Examples section")

                in_scenario_outline = True
                scenario_outline_line = line_num
                has_examples_for_outline = False

            elif stripped.startswith("Examples:"):
                if in_scenario_outline:
                    has_examples_for_outline = True

            elif stripped.startswith("Scenario:") or stripped.startswith("Feature:"):
                # Check previous Scenario Outline had Examples
                if in_scenario_outline and not has_examples_for_outline:
                    errors.append(f"Line {scenario_outline_line}: Scenario Outline missing Examples section")

                in_scenario_outline = False

        # Check last Scenario Outline
        if in_scenario_outline and not has_examples_for_outline:
            errors.append(f"Line {scenario_outline_line}: Scenario Outline missing Examples section")

        is_valid = len(errors) == 0
        return is_valid, errors

    except Exception as e:
        logger.error(f"Gherkin validation failed: {e}", exc_info=True)
        errors.append(f"Validation error: {str(e)}")
        return False, errors


def validate_feature_file(file_path: str) -> Tuple[bool, List[str]]:
    """
    Validate Gherkin syntax for .feature file at given path.

    Args:
        file_path: Path to .feature file

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    try:
        feature_file = Path(file_path)

        if not feature_file.exists():
            return False, [f"File not found: {file_path}"]

        content = feature_file.read_text(encoding='utf-8')

        return validate_gherkin_syntax(content)

    except Exception as e:
        logger.error(f"Failed to validate feature file {file_path}: {e}")
        return False, [f"Failed to read file: {str(e)}"]


def parse_feature_file(content: str) -> Dict[str, Any]:
    """
    Parse Gherkin feature file content into structured data.

    Args:
        content: Gherkin feature file content

    Returns:
        Dictionary with:
        - name: Feature name
        - description: Feature description
        - background: Background section (if present)
        - scenarios: List of scenarios
    """
    try:
        lines = content.split('\n')

        feature = {
            "name": "",
            "description": "",
            "background": None,
            "scenarios": []
        }

        current_section = None
        current_scenario = None
        current_examples = None

        for line in lines:
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith('#'):
                continue

            # Feature
            if stripped.startswith("Feature:"):
                feature["name"] = stripped.replace("Feature:", "").strip()
                current_section = "feature"

            # Background
            elif stripped.startswith("Background:"):
                current_section = "background"
                feature["background"] = {"steps": []}
                current_scenario = None

            # Scenario
            elif stripped.startswith("Scenario:"):
                current_section = "scenario"
                current_scenario = {
                    "name": stripped.replace("Scenario:", "").strip(),
                    "is_outline": False,
                    "steps": []
                }
                feature["scenarios"].append(current_scenario)

            # Scenario Outline
            elif stripped.startswith("Scenario Outline:"):
                current_section = "scenario"
                current_scenario = {
                    "name": stripped.replace("Scenario Outline:", "").strip(),
                    "is_outline": True,
                    "steps": [],
                    "examples": []
                }
                feature["scenarios"].append(current_scenario)

            # Examples
            elif stripped.startswith("Examples:"):
                if current_scenario and current_scenario.get("is_outline"):
                    current_section = "examples"
                    current_examples = {"header": [], "rows": []}
                    current_scenario["examples"].append(current_examples)

            # Steps (Given/When/Then/And/But)
            elif any(stripped.startswith(kw) for kw in STEP_KEYWORDS):
                for keyword in STEP_KEYWORDS:
                    if stripped.startswith(keyword):
                        step_text = stripped[len(keyword):].strip()
                        step = {"keyword": keyword, "text": step_text}

                        if current_section == "background" and feature["background"]:
                            feature["background"]["steps"].append(step)
                        elif current_section == "scenario" and current_scenario:
                            current_scenario["steps"].append(step)
                        break

            # Examples table rows
            elif current_section == "examples" and stripped.startswith("|"):
                # Parse table row
                cells = [cell.strip() for cell in stripped.split("|")[1:-1]]

                if not current_examples["header"]:
                    # First row is header
                    current_examples["header"] = cells
                else:
                    # Subsequent rows are data
                    current_examples["rows"].append(cells)

        return feature

    except Exception as e:
        logger.error(f"Failed to parse feature file: {e}")
        return {"name": "", "description": "", "background": None, "scenarios": []}


def is_valid_gherkin_keyword(keyword: str) -> bool:
    """
    Check if keyword is a valid Gherkin keyword.

    Args:
        keyword: Keyword to check

    Returns:
        True if valid Gherkin keyword
    """
    return keyword.strip() in VALID_KEYWORDS or any(keyword.strip().startswith(kw) for kw in STEP_KEYWORDS)


def get_syntax_errors(content: str) -> List[Dict[str, Any]]:
    """
    Get detailed syntax error information with line numbers.

    Args:
        content: Gherkin feature file content

    Returns:
        List of error dictionaries with line numbers and messages
    """
    _, error_messages = validate_gherkin_syntax(content)

    errors = []
    for error_msg in error_messages:
        # Extract line number if present
        match = re.search(r'Line (\d+):', error_msg)
        if match:
            line_num = int(match.group(1))
            message = error_msg.replace(f"Line {line_num}:", "").strip()
            errors.append({"line": line_num, "message": message})
        else:
            errors.append({"line": 0, "message": error_msg})

    return errors


def validate_scenario_outline(scenario: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate Scenario Outline has Examples section.

    Args:
        scenario: Scenario dictionary

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    if not scenario.get("is_outline"):
        return True, errors

    if not scenario.get("examples") or len(scenario["examples"]) == 0:
        errors.append("Scenario Outline must have Examples section")

    is_valid = len(errors) == 0
    return is_valid, errors


def validate_examples_table(examples: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate Examples table structure (header and rows have consistent columns).

    Args:
        examples: Examples dictionary with header and rows

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    header = examples.get("header", [])
    rows = examples.get("rows", [])

    if not header:
        errors.append("Examples table missing header row")
        return False, errors

    header_col_count = len(header)

    for row_idx, row in enumerate(rows, 1):
        if len(row) != header_col_count:
            errors.append(f"Row {row_idx} has {len(row)} columns, expected {header_col_count}")

    is_valid = len(errors) == 0
    return is_valid, errors


def validate_step_syntax(step: str) -> Tuple[bool, Optional[str]]:
    """
    Validate individual step syntax.

    Args:
        step: Step text (e.g., "Given I am on the login page")

    Returns:
        Tuple of (is_valid, error_message)
    """
    stripped = step.strip()

    if not stripped:
        return False, "Empty step"

    # Check if step starts with valid keyword
    has_valid_keyword = any(stripped.startswith(kw) for kw in STEP_KEYWORDS)
    if not has_valid_keyword:
        return False, f"Step must start with valid keyword (Given/When/Then/And/But). Found: {stripped[:20]}"

    # Check if step has text after keyword
    for keyword in STEP_KEYWORDS:
        if stripped.startswith(keyword):
            step_text = stripped[len(keyword):].strip()
            if not step_text:
                return False, f"Step keyword '{keyword}' must be followed by step text"
            break

    return True, None


def extract_feature_metadata(content: str) -> Dict[str, Any]:
    """
    Extract metadata from feature file (name, scenario count, step count, etc.).

    Args:
        content: Gherkin feature file content

    Returns:
        Dictionary with metadata
    """
    feature = parse_feature_file(content)

    scenario_count = len(feature.get("scenarios", []))
    step_count = sum(len(scenario.get("steps", [])) for scenario in feature.get("scenarios", []))

    has_background = feature.get("background") is not None
    has_scenario_outline = any(scenario.get("is_outline", False) for scenario in feature.get("scenarios", []))

    return {
        "feature_name": feature.get("name", ""),
        "scenario_count": scenario_count,
        "step_count": step_count,
        "has_background": has_background,
        "has_scenario_outline": has_scenario_outline
    }


def count_gherkin_elements(content: str) -> Dict[str, int]:
    """
    Count Gherkin elements for coverage summary.

    Args:
        content: Gherkin feature file content

    Returns:
        Dictionary with counts:
        - scenarios: Number of scenarios
        - steps: Total number of steps
        - examples: Number of scenario outlines with examples
        - background_steps: Number of background steps
    """
    feature = parse_feature_file(content)

    scenario_count = len(feature.get("scenarios", []))
    step_count = sum(len(scenario.get("steps", [])) for scenario in feature.get("scenarios", []))

    example_count = sum(1 for scenario in feature.get("scenarios", [])
                       if scenario.get("is_outline", False) and scenario.get("examples"))

    background_steps = 0
    if feature.get("background"):
        background_steps = len(feature["background"].get("steps", []))

    return {
        "scenarios": scenario_count,
        "steps": step_count,
        "examples": example_count,
        "background_steps": background_steps
    }


__all__ = [
    "validate_gherkin_syntax",
    "validate_feature_file",
    "parse_feature_file",
    "is_valid_gherkin_keyword",
    "get_syntax_errors",
    "validate_scenario_outline",
    "validate_examples_table",
    "validate_step_syntax",
    "extract_feature_metadata",
    "count_gherkin_elements"
]
