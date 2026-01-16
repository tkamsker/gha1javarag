"""
Playwright Generation Workflow (T131 - US2.6).

Orchestrates multi-agent workflow to generate Playwright E2E tests from UI components.
Workflow: Frontend Specialist → Backend Specialist → Playwright Test Writer
"""

import logging
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime

logger = logging.getLogger(__name__)


class PlaywrightGenerationWorkflow:
    """
    Workflow for generating Playwright test code from UI artifacts.

    This workflow:
    1. Analyzes UI components with Frontend Specialist
    2. Analyzes backend APIs with Backend Specialist
    3. Generates Playwright test code with Test Writer
    4. Tracks progress through stages
    5. Passes context between agents
    """

    def __init__(self):
        """Initialize Playwright generation workflow."""
        logger.info("Initialized Playwright Generation Workflow")

    def execute(
        self,
        test_request: str,
        artifacts: List[Dict[str, Any]],
        progress_callback: Optional[Callable[[str, float], None]] = None,
        cancellation_token: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Execute Playwright test generation workflow.

        Args:
            test_request: Test automation request (e.g., "Generate tests for login")
            artifacts: List of UI artifacts to test
            progress_callback: Optional callback for progress updates (stage, progress_pct)
            cancellation_token: Optional token to check for cancellation

        Returns:
            Dictionary with:
            - test_code: Generated Playwright test code
            - frontend_analysis: Frontend Specialist analysis
            - backend_analysis: Backend Specialist analysis
            - duration_seconds: Total workflow duration
            - timestamp: Workflow start timestamp

        Raises:
            ValueError: If artifacts list is empty
            TimeoutError: If agent times out
            Exception: If workflow fails
        """
        start_time = datetime.now()

        try:
            logger.info(f"Starting Playwright generation workflow: {test_request[:50]}...")

            # Validate inputs
            if not artifacts or len(artifacts) == 0:
                raise ValueError("Artifacts list cannot be empty")

            # Check cancellation
            if cancellation_token and cancellation_token.is_cancelled():
                raise Exception("Workflow cancelled")

            # Filter to UI-only artifacts
            ui_artifacts = self._filter_ui_artifacts(artifacts)

            if len(ui_artifacts) == 0:
                logger.warning("No UI artifacts found after filtering")

            # Stage 1: Frontend Specialist - Analyze UI components
            if progress_callback:
                progress_callback("Frontend Specialist", 0.0)

            frontend_analysis = self._execute_frontend_specialist(
                test_request, ui_artifacts, cancellation_token
            )

            if progress_callback:
                progress_callback("Frontend Specialist", 33.0)

            # Stage 2: Backend Specialist - Analyze backend APIs
            if progress_callback:
                progress_callback("Backend Specialist", 33.0)

            backend_analysis = self._execute_backend_specialist(
                test_request, artifacts, frontend_analysis, cancellation_token
            )

            if progress_callback:
                progress_callback("Backend Specialist", 66.0)

            # Stage 3: Playwright Test Writer - Generate test code
            if progress_callback:
                progress_callback("Playwright Test Writer", 66.0)

            test_code = self._execute_playwright_writer(
                test_request, ui_artifacts, frontend_analysis, backend_analysis, cancellation_token
            )

            if progress_callback:
                progress_callback("Playwright Test Writer", 100.0)

            # Calculate duration
            duration = (datetime.now() - start_time).total_seconds()

            return {
                "test_code": test_code,
                "frontend_analysis": frontend_analysis,
                "backend_analysis": backend_analysis,
                "duration_seconds": duration,
                "timestamp": start_time.isoformat()
            }

        except Exception as e:
            logger.error(f"Playwright generation workflow failed: {e}", exc_info=True)
            raise

    def _filter_ui_artifacts(self, artifacts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter artifacts to UI-related types only.

        Args:
            artifacts: All artifacts

        Returns:
            Filtered list of UI artifacts
        """
        ui_types = ["GwtPresenter", "GwtView", "GwtUiBinder", "JspForm", "JsArtifact"]

        ui_artifacts = [
            artifact for artifact in artifacts
            if artifact.get("artifactType") in ui_types
        ]

        logger.info(f"Filtered {len(ui_artifacts)} UI artifacts from {len(artifacts)} total")

        return ui_artifacts

    def _execute_frontend_specialist(
        self,
        test_request: str,
        ui_artifacts: List[Dict[str, Any]],
        cancellation_token: Optional[Any]
    ) -> str:
        """
        Execute Frontend Specialist agent.

        Args:
            test_request: Test request
            ui_artifacts: UI artifacts
            cancellation_token: Cancellation token

        Returns:
            Frontend analysis text

        Raises:
            Exception: If frontend analysis fails
        """
        # Check cancellation
        if cancellation_token and cancellation_token.is_cancelled():
            raise Exception("Workflow cancelled")

        from codeindex.web.agents.frontend_specialist import get_frontend_specialist_agent

        agent = get_frontend_specialist_agent()

        # Build query with UI artifact context
        query = f"{test_request}\n\nAnalyze these UI components for testing:\n"
        for artifact in ui_artifacts[:5]:  # Limit context
            query += f"- {artifact.get('fileName', 'Unknown')}\n"

        response = agent.execute_query(query)

        if hasattr(response, 'error') and response.error and isinstance(response.error, str):
            raise Exception(f"Frontend Specialist failed: {response.error}")

        return response.response_text

    def _execute_backend_specialist(
        self,
        test_request: str,
        artifacts: List[Dict[str, Any]],
        frontend_analysis: str,
        cancellation_token: Optional[Any]
    ) -> str:
        """
        Execute Backend Specialist agent.

        Args:
            test_request: Test request
            artifacts: All artifacts
            frontend_analysis: Frontend analysis context
            cancellation_token: Cancellation token

        Returns:
            Backend analysis text

        Raises:
            Exception: If backend analysis fails
        """
        # Check cancellation
        if cancellation_token and cancellation_token.is_cancelled():
            raise Exception("Workflow cancelled")

        from codeindex.web.agents.backend_specialist import get_backend_specialist_agent

        agent = get_backend_specialist_agent()

        # Build query with frontend context
        query = f"{test_request}\n\nFrontend analysis:\n{frontend_analysis[:500]}\n\nAnalyze backend APIs for these UI components."

        # Pass frontend analysis as context
        context = {"frontend_analysis": frontend_analysis}

        response = agent.execute_query(query, context=context)

        if hasattr(response, 'error') and response.error and isinstance(response.error, str):
            raise Exception(f"Backend Specialist failed: {response.error}")

        return response.response_text

    def _execute_playwright_writer(
        self,
        test_request: str,
        ui_artifacts: List[Dict[str, Any]],
        frontend_analysis: str,
        backend_analysis: str,
        cancellation_token: Optional[Any]
    ) -> str:
        """
        Execute Playwright Test Writer agent.

        Args:
            test_request: Test request
            ui_artifacts: UI artifacts
            frontend_analysis: Frontend analysis context
            backend_analysis: Backend analysis context
            cancellation_token: Cancellation token

        Returns:
            Generated Playwright test code

        Raises:
            Exception: If test generation fails
        """
        # Check cancellation
        if cancellation_token and cancellation_token.is_cancelled():
            raise Exception("Workflow cancelled")

        from codeindex.web.agents.playwright_test_writer import get_playwright_test_writer_agent

        agent = get_playwright_test_writer_agent()

        # Build query with all context
        query = f"""{test_request}

Frontend Analysis:
{frontend_analysis[:800]}

Backend Analysis:
{backend_analysis[:800]}

Generate Playwright test code with Page Object Model for these UI components."""

        # Pass all context to test writer
        context = {
            "frontend_analysis": frontend_analysis,
            "backend_analysis": backend_analysis,
            "ui_artifacts": [a.get("fileName") for a in ui_artifacts[:10]]
        }

        response = agent.execute_query(query, context=context)

        if hasattr(response, 'error') and response.error and isinstance(response.error, str):
            raise Exception(f"Playwright Test Writer failed: {response.error}")

        return response.response_text


# Global workflow instance
_playwright_generation_workflow: Optional[PlaywrightGenerationWorkflow] = None


def get_playwright_generation_workflow() -> PlaywrightGenerationWorkflow:
    """
    Get global Playwright Generation Workflow instance.

    Returns:
        PlaywrightGenerationWorkflow singleton
    """
    global _playwright_generation_workflow

    if _playwright_generation_workflow is None:
        _playwright_generation_workflow = PlaywrightGenerationWorkflow()
        logger.info("Created global Playwright Generation Workflow instance")

    return _playwright_generation_workflow


__all__ = [
    "PlaywrightGenerationWorkflow",
    "get_playwright_generation_workflow"
]
