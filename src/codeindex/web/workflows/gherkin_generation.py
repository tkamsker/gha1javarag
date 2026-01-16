"""
Gherkin Test Generation Workflow (T118 - US2.5).

Multi-agent workflow that orchestrates PRD Writer → Frontend Specialist → Gherkin Test Writer
to generate comprehensive BDD test scenarios from user stories and requirements.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from codeindex.web.agents.base import AgentResponse, Citation

logger = logging.getLogger(__name__)


class GherkinGenerationWorkflow:
    """
    Multi-agent workflow for Gherkin test generation.

    Workflow steps:
    1. PRD Writer: Analyzes requirements and extracts user stories/acceptance criteria
    2. Frontend Specialist: Identifies UI components and validation rules
    3. Gherkin Test Writer: Generates comprehensive Gherkin test scenarios

    Context flows from one agent to the next, building comprehensive test coverage.
    """

    def __init__(self):
        """Initialize Gherkin generation workflow."""
        logger.info("Initialized Gherkin Generation Workflow")

    def execute(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute multi-agent Gherkin generation workflow.

        Args:
            query: User request (e.g., "Generate Gherkin tests for login feature")
            context: Optional initial context (user stories, artifacts, etc.)

        Returns:
            Dictionary with:
            - gherkin_content: Generated Gherkin feature file
            - citations: Aggregated citations from all agents
            - agent_executions: Details of each agent execution
            - total_duration_seconds: Total workflow duration
            - validation: Gherkin syntax validation results
            - error: Error message if workflow failed
        """
        start_time = datetime.now()
        agent_executions = []
        all_citations = []

        try:
            logger.info(f"Starting Gherkin generation workflow: {query[:50]}...")

            if context is None:
                context = {}

            # ========================================
            # Step 1: PRD Writer - Analyze requirements
            # ========================================
            logger.info("Step 1: Invoking PRD Writer agent...")

            from codeindex.web.agents.prd_writer import get_prd_writer_agent
            prd_agent = get_prd_writer_agent()

            prd_query = f"Analyze requirements and user stories for: {query}"
            prd_response = prd_agent.execute_query(prd_query, context=context)

            agent_executions.append({
                "agent": "PRD Writer",
                "query": prd_query,
                "duration_seconds": prd_response.duration_seconds,
                "confidence": prd_response.confidence,
                "has_error": prd_response.has_error()
            })

            all_citations.extend(prd_response.citations)

            if prd_response.has_error():
                raise Exception(f"PRD Writer failed: {prd_response.error}")

            # Extract requirements from PRD Writer response
            prd_requirements = prd_response.response_text

            # ========================================
            # Step 2: Frontend Specialist - Identify UI components
            # ========================================
            logger.info("Step 2: Invoking Frontend Specialist agent...")

            from codeindex.web.agents.frontend_specialist import get_frontend_specialist_agent
            frontend_agent = get_frontend_specialist_agent()

            frontend_query = f"Identify UI components and validation rules for: {query}"
            frontend_context = {
                **context,
                "prd_requirements": prd_requirements
            }
            frontend_response = frontend_agent.execute_query(frontend_query, context=frontend_context)

            agent_executions.append({
                "agent": "Frontend Specialist",
                "query": frontend_query,
                "duration_seconds": frontend_response.duration_seconds,
                "confidence": frontend_response.confidence,
                "has_error": frontend_response.has_error()
            })

            all_citations.extend(frontend_response.citations)

            if frontend_response.has_error():
                raise Exception(f"Frontend Specialist failed: {frontend_response.error}")

            # Extract UI components from Frontend Specialist response
            ui_components = frontend_response.response_text

            # ========================================
            # Step 3: Gherkin Test Writer - Generate test scenarios
            # ========================================
            logger.info("Step 3: Invoking Gherkin Test Writer agent...")

            from codeindex.web.agents.gherkin_test_writer import get_gherkin_test_writer_agent
            gherkin_agent = get_gherkin_test_writer_agent()

            gherkin_query = query  # Use original query
            gherkin_context = {
                **context,
                "prd_requirements": prd_requirements,
                "ui_components": ui_components
            }
            gherkin_response = gherkin_agent.execute_query(gherkin_query, context=gherkin_context)

            agent_executions.append({
                "agent": "Gherkin Test Writer",
                "query": gherkin_query,
                "duration_seconds": gherkin_response.duration_seconds,
                "confidence": gherkin_response.confidence,
                "has_error": gherkin_response.has_error()
            })

            all_citations.extend(gherkin_response.citations)

            if gherkin_response.has_error():
                raise Exception(f"Gherkin Test Writer failed: {gherkin_response.error}")

            # Extract Gherkin content
            gherkin_content = gherkin_response.response_text

            # ========================================
            # Step 4: Validate Gherkin syntax
            # ========================================
            logger.info("Step 4: Validating Gherkin syntax...")

            from codeindex.web.services.gherkin_validation import validate_gherkin_syntax
            is_valid, errors = validate_gherkin_syntax(gherkin_content)

            validation_result = {
                "is_valid": is_valid,
                "errors": errors
            }

            # ========================================
            # Step 5: Calculate total duration
            # ========================================
            total_duration = sum(exec["duration_seconds"] for exec in agent_executions)

            logger.info(f"Workflow completed in {total_duration:.2f} seconds")

            return {
                "gherkin_content": gherkin_content,
                "citations": all_citations,
                "agent_executions": agent_executions,
                "total_duration_seconds": total_duration,
                "validation": validation_result,
                "timestamp": start_time.isoformat()
            }

        except Exception as e:
            logger.error(f"Gherkin generation workflow failed: {e}", exc_info=True)

            # Calculate duration up to failure point
            total_duration = (datetime.now() - start_time).total_seconds()

            return {
                "gherkin_content": "",
                "citations": all_citations,
                "agent_executions": agent_executions,
                "total_duration_seconds": total_duration,
                "validation": {"is_valid": False, "errors": ["Workflow failed"]},
                "error": str(e),
                "timestamp": start_time.isoformat()
            }


# Global workflow instance
_gherkin_generation_workflow: Optional[GherkinGenerationWorkflow] = None


def get_gherkin_generation_workflow() -> GherkinGenerationWorkflow:
    """
    Get global Gherkin Generation Workflow instance.

    Returns:
        GherkinGenerationWorkflow singleton
    """
    global _gherkin_generation_workflow

    if _gherkin_generation_workflow is None:
        _gherkin_generation_workflow = GherkinGenerationWorkflow()
        logger.info("Created global Gherkin Generation Workflow instance")

    return _gherkin_generation_workflow


__all__ = [
    "GherkinGenerationWorkflow",
    "get_gherkin_generation_workflow"
]
