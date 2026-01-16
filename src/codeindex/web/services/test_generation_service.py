"""
Test Generation Service (T117 - US2.5, T129 - US2.6).

Provides high-level interface for generating Gherkin test scenarios and
Playwright E2E tests with syntax validation and file generation.
"""

import logging
from typing import Dict, Any, Tuple, List, Optional
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class TestGenerationService:
    """
    Service for generating BDD test cases in Gherkin format and Playwright E2E tests.

    This service:
    - Generates Gherkin feature files from user stories
    - Generates Playwright E2E tests from UI artifacts
    - Validates Gherkin and TypeScript/JavaScript syntax before output
    - Creates .feature and .spec.ts files for download
    - Provides test coverage summaries
    - Integrates with Gherkin Test Writer agent and Playwright Generation Workflow
    """

    def __init__(self):
        """Initialize test generation service."""
        logger.info("Initialized Test Generation Service")

    def generate_gherkin_with_summary(
        self,
        user_story: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate Gherkin test scenarios with coverage summary.

        Args:
            user_story: User story or test request
            context: Optional context (PRD requirements, UI components)

        Returns:
            Dictionary with:
            - gherkin_content: Generated Gherkin feature file
            - summary: Test coverage summary (scenario count, step count, example count)
            - citations: Source artifact citations
            - validation: Syntax validation results

        Raises:
            Exception: If generation fails
        """
        try:
            logger.info(f"Generating Gherkin tests for: {user_story[:50]}...")

            # Step 1: Generate Gherkin using agent
            from codeindex.web.agents.gherkin_test_writer import get_gherkin_test_writer_agent
            agent = get_gherkin_test_writer_agent()

            response = agent.execute_query(user_story, context=context)

            if response.has_error():
                raise Exception(f"Gherkin generation failed: {response.error}")

            gherkin_content = response.response_text

            # Step 2: Validate Gherkin syntax
            from codeindex.web.services.gherkin_validation import validate_gherkin_syntax
            is_valid, errors = validate_gherkin_syntax(gherkin_content)

            validation_result = {
                "is_valid": is_valid,
                "errors": errors
            }

            # Step 3: Generate coverage summary
            from codeindex.web.services.gherkin_validation import count_gherkin_elements
            element_counts = count_gherkin_elements(gherkin_content)

            summary = {
                "scenario_count": element_counts.get("scenarios", 0),
                "step_count": element_counts.get("steps", 0),
                "example_count": element_counts.get("examples", 0),
                "background_steps": element_counts.get("background_steps", 0)
            }

            return {
                "gherkin_content": gherkin_content,
                "summary": summary,
                "citations": response.citations,
                "validation": validation_result,
                "duration_seconds": response.duration_seconds,
                "timestamp": response.timestamp
            }

        except Exception as e:
            logger.error(f"Failed to generate Gherkin with summary: {e}", exc_info=True)
            raise

    def generate_feature_file(
        self,
        user_story: str,
        output_dir: Path,
        context: Optional[Dict[str, Any]] = None,
        validate_before_save: bool = True
    ) -> Path:
        """
        Generate .feature file for download.

        Args:
            user_story: User story or test request
            output_dir: Directory to save .feature file
            context: Optional context
            validate_before_save: If True, validates syntax before saving (per FR8.8)

        Returns:
            Path to generated .feature file

        Raises:
            ValueError: If validation fails and validate_before_save=True
            Exception: If generation fails
        """
        try:
            logger.info(f"Generating .feature file for: {user_story[:50]}...")

            # Generate Gherkin with summary
            result = self.generate_gherkin_with_summary(user_story, context=context)

            gherkin_content = result["gherkin_content"]
            is_valid = result["validation"]["is_valid"]
            errors = result["validation"]["errors"]

            # Validate before saving (per FR8.8: block download on critical errors)
            if validate_before_save and not is_valid:
                error_msg = f"Gherkin syntax validation failed. Cannot generate .feature file. Errors: {', '.join(errors)}"
                logger.error(error_msg)
                raise ValueError(error_msg)

            # Create output directory if needed
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            # Generate feature file name from user story
            feature_name = self._sanitize_feature_name(user_story)
            feature_file_path = output_dir / f"{feature_name}.feature"

            # Write .feature file
            feature_file_path.write_text(gherkin_content, encoding='utf-8')

            logger.info(f"Generated .feature file: {feature_file_path}")

            return feature_file_path

        except ValueError:
            # Re-raise validation errors
            raise
        except Exception as e:
            logger.error(f"Failed to generate .feature file: {e}", exc_info=True)
            raise

    def generate_multiple_feature_files(
        self,
        user_stories: List[str],
        output_dir: Path,
        context: Optional[Dict[str, Any]] = None
    ) -> List[Path]:
        """
        Generate multiple .feature files from list of user stories.

        Args:
            user_stories: List of user stories or test requests
            output_dir: Directory to save .feature files
            context: Optional context

        Returns:
            List of paths to generated .feature files

        Raises:
            Exception: If any generation fails
        """
        try:
            logger.info(f"Generating {len(user_stories)} .feature files...")

            feature_files = []

            for user_story in user_stories:
                try:
                    feature_file = self.generate_feature_file(
                        user_story=user_story,
                        output_dir=output_dir,
                        context=context
                    )
                    feature_files.append(feature_file)

                except ValueError as e:
                    # Log validation error but continue with other files
                    logger.warning(f"Skipping feature due to validation error: {e}")
                    continue

            logger.info(f"Generated {len(feature_files)} .feature files")

            return feature_files

        except Exception as e:
            logger.error(f"Failed to generate multiple .feature files: {e}", exc_info=True)
            raise

    def generate_playwright_file(
        self,
        test_request: str,
        output_dir: Path,
        artifacts: List[Dict[str, Any]],
        validate_before_save: bool = True,
        language: str = 'typescript'
    ) -> Path:
        """
        Generate .spec.ts/.spec.js file for download.

        Args:
            test_request: Test automation request (e.g., "Generate tests for login")
            output_dir: Directory to save .spec.ts file
            artifacts: List of UI artifacts to test
            validate_before_save: If True, validates syntax before saving (per FR8.8)
            language: 'typescript' or 'javascript' (default: typescript)

        Returns:
            Path to generated .spec.ts or .spec.js file

        Raises:
            ValueError: If validation fails and validate_before_save=True
            Exception: If generation fails
        """
        try:
            logger.info(f"Generating Playwright test file for: {test_request[:50]}...")

            # Step 1: Generate Playwright tests using workflow
            from codeindex.web.workflows.playwright_generation import get_playwright_generation_workflow
            workflow = get_playwright_generation_workflow()

            result = workflow.execute(
                test_request=test_request,
                artifacts=artifacts
            )

            test_code = result["test_code"]

            # Step 2: Validate TypeScript/JavaScript syntax
            from codeindex.web.services.playwright_validation import validate_playwright_syntax
            is_valid, errors = validate_playwright_syntax(test_code, language=language)

            # Step 3: Validate before saving (per FR8.8: block download on critical errors)
            if validate_before_save and not is_valid:
                error_msg = f"Playwright syntax validation failed. Cannot generate .spec file. Errors: {', '.join(errors)}"
                logger.error(error_msg)
                raise ValueError(error_msg)

            # Step 4: Create output directory if needed
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            # Step 5: Generate test file name from request
            test_name = self._sanitize_feature_name(test_request)
            extension = ".ts" if language == 'typescript' else ".js"
            test_file_path = output_dir / f"{test_name}.spec{extension}"

            # Step 6: Write .spec.ts/.spec.js file
            test_file_path.write_text(test_code, encoding='utf-8')

            logger.info(f"Generated Playwright test file: {test_file_path}")

            return test_file_path

        except ValueError:
            # Re-raise validation errors
            raise
        except Exception as e:
            logger.error(f"Failed to generate Playwright test file: {e}", exc_info=True)
            raise

    def generate_multiple_playwright_files(
        self,
        test_requests: List[str],
        output_dir: Path,
        artifacts: List[Dict[str, Any]],
        language: str = 'typescript'
    ) -> List[Path]:
        """
        Generate multiple .spec.ts/.spec.js files from list of test requests.

        Args:
            test_requests: List of test automation requests
            output_dir: Directory to save .spec files
            artifacts: List of UI artifacts to test
            language: 'typescript' or 'javascript' (default: typescript)

        Returns:
            List of paths to generated .spec files

        Raises:
            Exception: If any generation fails
        """
        try:
            logger.info(f"Generating {len(test_requests)} Playwright test files...")

            test_files = []

            for test_request in test_requests:
                try:
                    test_file = self.generate_playwright_file(
                        test_request=test_request,
                        output_dir=output_dir,
                        artifacts=artifacts,
                        language=language
                    )
                    test_files.append(test_file)

                except ValueError as e:
                    # Log validation error but continue with other files
                    logger.warning(f"Skipping test file due to validation error: {e}")
                    continue

            logger.info(f"Generated {len(test_files)} Playwright test files")

            return test_files

        except Exception as e:
            logger.error(f"Failed to generate multiple Playwright test files: {e}", exc_info=True)
            raise

    def _sanitize_feature_name(self, user_story: str) -> str:
        """
        Sanitize user story text to create valid feature file name.

        Args:
            user_story: User story text

        Returns:
            Sanitized feature name suitable for file name
        """
        import re

        # Extract feature name from user story
        # Remove common prefixes
        name = user_story.replace("Generate Gherkin tests for", "")
        name = name.replace("Generate tests for", "")
        name = name.replace("Create tests for", "")
        name = name.strip()

        # Convert to snake_case
        name = name.lower()
        name = re.sub(r'[^\w\s-]', '', name)  # Remove special characters
        name = re.sub(r'[\s-]+', '_', name)  # Replace spaces/hyphens with underscores
        name = re.sub(r'_+', '_', name)  # Remove duplicate underscores

        # Truncate if too long
        if len(name) > 50:
            name = name[:50]

        # Ensure name is not empty
        if not name:
            name = f"feature_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        return name


# Global service instance
_test_generation_service: Optional[TestGenerationService] = None


def get_test_generation_service() -> TestGenerationService:
    """
    Get global Test Generation Service instance.

    Returns:
        TestGenerationService singleton
    """
    global _test_generation_service

    if _test_generation_service is None:
        _test_generation_service = TestGenerationService()
        logger.info("Created global Test Generation Service instance")

    return _test_generation_service


__all__ = [
    "TestGenerationService",
    "get_test_generation_service"
]
