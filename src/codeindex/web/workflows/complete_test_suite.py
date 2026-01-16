"""
Complete Test Suite Workflow (T138 - US2.6).

Orchestrates generation of complete test suite including both Gherkin
feature files and Playwright E2E tests for comprehensive test coverage.
"""

import logging
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class CompleteTestSuiteWorkflow:
    """
    Workflow for generating complete test suite (Gherkin + Playwright).

    This workflow:
    1. Generates Gherkin feature files for BDD scenarios
    2. Generates Playwright E2E tests for UI automation
    3. Coordinates both generation processes
    4. Returns paths to all generated test files
    5. Provides unified progress tracking
    """

    def __init__(self):
        """Initialize complete test suite workflow."""
        logger.info("Initialized Complete Test Suite Workflow")

    def execute(
        self,
        test_request: str,
        artifacts: List[Dict[str, Any]],
        output_dir: Path,
        progress_callback: Optional[Callable[[str, float], None]] = None,
        cancellation_token: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Execute complete test suite generation workflow.

        Args:
            test_request: Test generation request
            artifacts: List of artifacts to generate tests for
            output_dir: Directory to save generated files
            progress_callback: Optional callback for progress updates (stage, progress_pct)
            cancellation_token: Optional token to check for cancellation

        Returns:
            Dictionary with:
            - gherkin_files: List of generated .feature file paths
            - playwright_files: List of generated .spec.ts file paths
            - duration_seconds: Total workflow duration
            - timestamp: Workflow start timestamp

        Raises:
            ValueError: If artifacts list is empty
            Exception: If workflow fails
        """
        start_time = datetime.now()

        try:
            logger.info(f"Starting complete test suite generation: {test_request[:50]}...")

            # Validate inputs
            if not artifacts or len(artifacts) == 0:
                raise ValueError("Artifacts list cannot be empty")

            # Check cancellation
            if cancellation_token and cancellation_token.is_cancelled():
                raise Exception("Workflow cancelled")

            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            # Stage 1: Generate Gherkin feature files
            if progress_callback:
                progress_callback("Generating Gherkin Tests", 0.0)

            gherkin_files = self._generate_gherkin_tests(
                test_request, artifacts, output_dir, cancellation_token
            )

            if progress_callback:
                progress_callback("Generating Gherkin Tests", 50.0)

            # Stage 2: Generate Playwright E2E tests
            if progress_callback:
                progress_callback("Generating Playwright Tests", 50.0)

            playwright_files = self._generate_playwright_tests(
                test_request, artifacts, output_dir, cancellation_token
            )

            if progress_callback:
                progress_callback("Generating Playwright Tests", 100.0)

            # Calculate duration
            duration = (datetime.now() - start_time).total_seconds()

            logger.info(f"Complete test suite generation completed: {len(gherkin_files)} Gherkin + {len(playwright_files)} Playwright files")

            return {
                "gherkin_files": gherkin_files,
                "playwright_files": playwright_files,
                "duration_seconds": duration,
                "timestamp": start_time.isoformat()
            }

        except Exception as e:
            logger.error(f"Complete test suite workflow failed: {e}", exc_info=True)
            raise

    def _generate_gherkin_tests(
        self,
        test_request: str,
        artifacts: List[Dict[str, Any]],
        output_dir: Path,
        cancellation_token: Optional[Any]
    ) -> List[Path]:
        """
        Generate Gherkin feature files.

        Args:
            test_request: Test request
            artifacts: Artifacts for context
            output_dir: Output directory
            cancellation_token: Cancellation token

        Returns:
            List of generated .feature file paths

        Raises:
            Exception: If Gherkin generation fails
        """
        # Check cancellation
        if cancellation_token and cancellation_token.is_cancelled():
            raise Exception("Workflow cancelled")

        from codeindex.web.services.test_generation_service import get_test_generation_service

        service = get_test_generation_service()

        # Create context from artifacts
        context = {
            "artifacts": artifacts,
            "artifact_count": len(artifacts)
        }

        try:
            # Generate single Gherkin feature file
            feature_file = service.generate_feature_file(
                user_story=test_request,
                output_dir=output_dir,
                context=context
            )

            return [feature_file]

        except Exception as e:
            logger.error(f"Gherkin test generation failed: {e}")
            raise

    def _generate_playwright_tests(
        self,
        test_request: str,
        artifacts: List[Dict[str, Any]],
        output_dir: Path,
        cancellation_token: Optional[Any]
    ) -> List[Path]:
        """
        Generate Playwright E2E test files.

        Args:
            test_request: Test request
            artifacts: UI artifacts to test
            output_dir: Output directory
            cancellation_token: Cancellation token

        Returns:
            List of generated .spec.ts file paths

        Raises:
            Exception: If Playwright generation fails
        """
        # Check cancellation
        if cancellation_token and cancellation_token.is_cancelled():
            raise Exception("Workflow cancelled")

        from codeindex.web.services.test_generation_service import get_test_generation_service

        service = get_test_generation_service()

        try:
            # Generate single Playwright test file
            test_file = service.generate_playwright_file(
                test_request=test_request,
                output_dir=output_dir,
                artifacts=artifacts
            )

            return [test_file]

        except Exception as e:
            logger.error(f"Playwright test generation failed: {e}")
            raise


# Global workflow instance
_complete_test_suite_workflow: Optional[CompleteTestSuiteWorkflow] = None


def get_complete_test_suite_workflow() -> CompleteTestSuiteWorkflow:
    """
    Get global Complete Test Suite Workflow instance.

    Returns:
        CompleteTestSuiteWorkflow singleton
    """
    global _complete_test_suite_workflow

    if _complete_test_suite_workflow is None:
        _complete_test_suite_workflow = CompleteTestSuiteWorkflow()
        logger.info("Created global Complete Test Suite Workflow instance")

    return _complete_test_suite_workflow


__all__ = [
    "CompleteTestSuiteWorkflow",
    "get_complete_test_suite_workflow"
]
