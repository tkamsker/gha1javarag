"""
Multi-agent PRD generation workflow (T090).

This workflow orchestrates multiple agents to collaboratively generate comprehensive
Product Requirements Documents from codebase analysis.

Workflow: Backend Specialist → Frontend Specialist → Data Analyst → PRD Writer
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass

from codeindex.web.agents.base import AgentResponse, AgentRole
from codeindex.web.agents.backend_specialist import get_backend_specialist_agent
from codeindex.web.agents.frontend_specialist import get_frontend_specialist_agent
from codeindex.web.agents.data_analyst import get_data_analyst_agent
from codeindex.web.agents.prd_writer import get_prd_writer_agent

logger = logging.getLogger(__name__)


@dataclass
class WorkflowStep:
    """
    Represents a step in the workflow.

    Attributes:
        agent_role: Agent role for this step
        status: Step status (pending, in_progress, completed, failed)
        start_time: When step started
        end_time: When step completed
        response: Agent response
        error: Error message if failed
    """
    agent_role: AgentRole
    status: str = "pending"  # pending, in_progress, completed, failed
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    response: Optional[AgentResponse] = None
    error: Optional[str] = None


class PrdGenerationWorkflow:
    """
    Multi-agent workflow for PRD generation.

    This workflow coordinates multiple specialized agents to analyze a codebase
    and generate a comprehensive Product Requirements Document.

    Workflow Steps:
    1. Backend Specialist: Analyzes backend services, APIs, business logic
    2. Frontend Specialist: Analyzes UI components, user flows, screens
    3. Data Analyst: Analyzes database schema, data models, relationships
    4. PRD Writer: Synthesizes all analysis into structured PRD
    """

    def __init__(self):
        """Initialize PRD generation workflow."""
        self.steps: List[WorkflowStep] = []
        self.context: Dict[str, Any] = {}
        self.is_cancelled = False

        # Initialize workflow steps
        self._initialize_steps()

    def _initialize_steps(self):
        """Initialize workflow steps."""
        self.steps = [
            WorkflowStep(agent_role=AgentRole.BACKEND_SPECIALIST),
            WorkflowStep(agent_role=AgentRole.FRONTEND_SPECIALIST),
            WorkflowStep(agent_role=AgentRole.DATA_ANALYST),
            WorkflowStep(agent_role=AgentRole.PRD_WRITER)
        ]

    def execute(
        self,
        artifacts: List[Dict[str, Any]],
        project_name: str,
        progress_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        Execute PRD generation workflow.

        Args:
            artifacts: List of artifacts to analyze
            project_name: Project name for PRD
            progress_callback: Optional callback for progress updates

        Returns:
            Dictionary with:
                - success: Boolean
                - prd_content: Generated PRD markdown
                - steps: List of workflow steps with responses
                - error: Error message if failed
        """
        logger.info(f"Starting PRD generation workflow for project: {project_name}")

        try:
            self.context = {
                "artifacts": artifacts,
                "project_name": project_name,
                "artifact_count": len(artifacts)
            }

            # Execute each step sequentially
            for i, step in enumerate(self.steps):
                if self.is_cancelled:
                    logger.warning("Workflow cancelled by user")
                    return self._create_result(success=False, error="Workflow cancelled")

                # Update progress
                if progress_callback:
                    progress_callback(i, len(self.steps), step.agent_role)

                # Execute step
                self._execute_step(step)

                # Stop on error
                if step.status == "failed":
                    logger.error(f"Workflow step failed: {step.agent_role.value}")
                    return self._create_result(
                        success=False,
                        error=f"Step {step.agent_role.value} failed: {step.error}"
                    )

            # Final progress update
            if progress_callback:
                progress_callback(len(self.steps), len(self.steps), None)

            # Extract PRD from final step
            prd_step = self.steps[-1]
            prd_content = prd_step.response.response_text if prd_step.response else ""

            logger.info("PRD generation workflow completed successfully")

            return self._create_result(success=True, prd_content=prd_content)

        except Exception as e:
            logger.error(f"Workflow execution failed: {e}", exc_info=True)
            return self._create_result(success=False, error=str(e))

    def _execute_step(self, step: WorkflowStep):
        """
        Execute a single workflow step.

        Args:
            step: Workflow step to execute
        """
        step.status = "in_progress"
        step.start_time = datetime.now().isoformat()

        try:
            logger.info(f"Executing step: {step.agent_role.value}")

            # Get appropriate agent
            agent = self._get_agent(step.agent_role)

            # Build query based on workflow context
            query = self._build_query(step.agent_role)

            # Execute agent
            response = agent.execute_query(query, context=self.context)

            # Store response
            step.response = response
            step.end_time = datetime.now().isoformat()

            if response.has_error():
                step.status = "failed"
                step.error = response.error
            else:
                step.status = "completed"

                # Add response to context for next agent
                self.context[f"{step.agent_role.value}_analysis"] = response.response_text
                self.context[f"{step.agent_role.value}_citations"] = [
                    c.to_dict() for c in response.citations
                ]

        except Exception as e:
            logger.error(f"Step execution failed: {e}", exc_info=True)
            step.status = "failed"
            step.error = str(e)
            step.end_time = datetime.now().isoformat()

    def _get_agent(self, agent_role: AgentRole):
        """
        Get agent instance for role.

        Args:
            agent_role: Agent role

        Returns:
            Agent instance
        """
        if agent_role == AgentRole.BACKEND_SPECIALIST:
            return get_backend_specialist_agent()
        elif agent_role == AgentRole.FRONTEND_SPECIALIST:
            return get_frontend_specialist_agent()
        elif agent_role == AgentRole.DATA_ANALYST:
            return get_data_analyst_agent()
        elif agent_role == AgentRole.PRD_WRITER:
            return get_prd_writer_agent()
        else:
            raise ValueError(f"Unsupported agent role: {agent_role}")

    def _build_query(self, agent_role: AgentRole) -> str:
        """
        Build query for agent based on workflow context.

        Args:
            agent_role: Agent role

        Returns:
            Query string
        """
        project_name = self.context.get("project_name", "Project")
        artifact_count = self.context.get("artifact_count", 0)

        if agent_role == AgentRole.BACKEND_SPECIALIST:
            return f"Analyze the backend architecture of {project_name}. " \
                   f"Focus on services, APIs, and business logic. " \
                   f"Analyzing {artifact_count} artifacts."

        elif agent_role == AgentRole.FRONTEND_SPECIALIST:
            return f"Analyze the frontend architecture of {project_name}. " \
                   f"Focus on UI components, user flows, and screens. " \
                   f"Analyzing {artifact_count} artifacts."

        elif agent_role == AgentRole.DATA_ANALYST:
            return f"Analyze the data architecture of {project_name}. " \
                   f"Focus on database schema, data models, and relationships. " \
                   f"Analyzing {artifact_count} artifacts."

        elif agent_role == AgentRole.PRD_WRITER:
            backend_analysis = self.context.get("Backend Specialist_analysis", "")
            frontend_analysis = self.context.get("Frontend Specialist_analysis", "")
            data_analysis = self.context.get("Data Analyst_analysis", "")

            return f"Generate a comprehensive PRD for {project_name} based on:\n\n" \
                   f"Backend Analysis:\n{backend_analysis[:500]}...\n\n" \
                   f"Frontend Analysis:\n{frontend_analysis[:500]}...\n\n" \
                   f"Data Analysis:\n{data_analysis[:500]}..."

        else:
            return f"Analyze {project_name}"

    def _create_result(
        self,
        success: bool,
        prd_content: str = "",
        error: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create workflow result dictionary.

        Args:
            success: Whether workflow succeeded
            prd_content: Generated PRD content
            error: Error message if failed

        Returns:
            Result dictionary
        """
        return {
            "success": success,
            "prd_content": prd_content,
            "steps": [
                {
                    "agent_role": step.agent_role.value,
                    "status": step.status,
                    "start_time": step.start_time,
                    "end_time": step.end_time,
                    "duration_seconds": (
                        step.response.duration_seconds if step.response else 0
                    )
                }
                for step in self.steps
            ],
            "error": error
        }

    def cancel(self):
        """Cancel workflow execution."""
        self.is_cancelled = True
        logger.info("Workflow cancellation requested")


__all__ = [
    "PrdGenerationWorkflow",
    "WorkflowStep"
]
