"""
Agent service for routing queries to appropriate agents and managing agent execution.

This service provides the core agent orchestration logic including query routing,
agent initialization, and response formatting.
"""

import time
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

from codeindex.web.agents.base import (
    AgentRole,
    AgentConfig,
    AgentResponse,
    Citation,
    get_agent_config
)

logger = logging.getLogger(__name__)


class AgentService:
    """
    Service for managing and routing queries to CrewAI agents.

    Features:
    - Query routing based on keyword heuristics
    - Agent initialization with configuration
    - Response formatting and citation extraction
    - Error handling and retries
    """

    def __init__(self):
        """Initialize agent service."""
        self.routing_keywords = self._initialize_routing_keywords()

    def _initialize_routing_keywords(self) -> Dict[AgentRole, List[str]]:
        """
        Initialize keyword mappings for agent routing.

        Returns:
            Dictionary mapping agent roles to keyword lists
        """
        return {
            AgentRole.DATA_ANALYST: [
                "database", "schema", "table", "column", "foreign key",
                "index", "sql", "query", "entity", "relationship", "erd"
            ],
            AgentRole.FRONTEND_SPECIALIST: [
                "ui", "view", "presenter", "form", "widget", "jsp", "gwt",
                "template", "frontend", "user interface", "screen", "page"
            ],
            AgentRole.BACKEND_SPECIALIST: [
                "service", "dao", "api", "endpoint", "rest", "rpc", "servlet",
                "backend", "business logic", "controller", "repository"
            ],
            AgentRole.PRD_WRITER: [
                "prd", "requirements", "user story", "feature", "requirement",
                "specification", "document"
            ],
            AgentRole.SPECKIT_WRITER: [
                "spec", "specification", "technical spec", "design doc",
                "implementation plan", "architecture doc"
            ],
            AgentRole.GHERKIN_TEST_WRITER: [
                "gherkin", "bdd", "given when then", "scenario", "feature file",
                "acceptance criteria", "cucumber"
            ],
            AgentRole.PLAYWRIGHT_TEST_WRITER: [
                "playwright", "e2e", "end to end", "browser test", "ui test",
                "selenium", "test automation"
            ],
            AgentRole.SENIOR_DEVELOPER: [
                "architecture", "design pattern", "explain", "how does",
                "what is", "code", "class", "method"
            ]
        }

    def route_query(self, query: str) -> AgentRole:
        """
        Route query to appropriate agent based on keyword matching.

        Args:
            query: User query string

        Returns:
            AgentRole for the most appropriate agent
        """
        query_lower = query.lower()
        scores = {}

        # Calculate keyword match scores for each agent
        for role, keywords in self.routing_keywords.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            if score > 0:
                scores[role] = score

        # Return agent with highest score, or Senior Developer as fallback
        if scores:
            return max(scores, key=scores.get)
        else:
            logger.info("No keyword matches, routing to Senior Developer as fallback")
            return AgentRole.SENIOR_DEVELOPER

    def create_agent_response(
        self,
        agent_role: AgentRole,
        query: str,
        response_text: str,
        duration: float,
        citations: Optional[List[Citation]] = None,
        confidence: float = 0.8,
        suggested_questions: Optional[List[str]] = None,
        error: Optional[str] = None
    ) -> AgentResponse:
        """
        Create standardized agent response object.

        Args:
            agent_role: Agent role that generated the response
            query: Original user query
            response_text: Agent's response text
            duration: Response generation duration in seconds
            citations: Optional list of citations
            confidence: Confidence score (0.0 to 1.0)
            suggested_questions: Optional list of follow-up questions
            error: Optional error message

        Returns:
            AgentResponse object
        """
        return AgentResponse(
            agent_role=agent_role,
            query=query,
            timestamp=datetime.now().isoformat(),
            duration_seconds=duration,
            response_text=response_text,
            citations=citations or [],
            confidence=confidence,
            suggested_questions=suggested_questions or [],
            error=error
        )

    def execute_query(
        self,
        query: str,
        agent_role: Optional[AgentRole] = None,
        agent_settings: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """
        Execute query with appropriate agent.

        Args:
            query: User query string
            agent_role: Optional specific agent role (otherwise auto-routed)
            agent_settings: Optional agent configuration overrides

        Returns:
            AgentResponse object
        """
        start_time = time.time()

        try:
            # Route query to appropriate agent if not specified
            if agent_role is None:
                agent_role = self.route_query(query)

            logger.info(f"Routing query to {agent_role.value}: {query[:50]}...")

            # Get agent configuration with any overrides
            config = get_agent_config(agent_role, **(agent_settings or {}))

            # Execute with specific agent (T061-T064)
            if agent_role == AgentRole.SENIOR_DEVELOPER:
                # Use Senior Developer agent
                from codeindex.web.agents.senior_developer import get_senior_developer_agent
                agent = get_senior_developer_agent(config)
                return agent.execute_query(query)

            elif agent_role == AgentRole.DATA_ANALYST:
                # Use Data Analyst agent (T064)
                from codeindex.web.agents.data_analyst import get_data_analyst_agent
                agent = get_data_analyst_agent(config)
                return agent.execute_query(query)

            elif agent_role == AgentRole.FRONTEND_SPECIALIST:
                # Use Frontend Specialist agent (T062)
                from codeindex.web.agents.frontend_specialist import get_frontend_specialist_agent
                agent = get_frontend_specialist_agent(config)
                return agent.execute_query(query)

            elif agent_role == AgentRole.BACKEND_SPECIALIST:
                # Use Backend Specialist agent (T063)
                from codeindex.web.agents.backend_specialist import get_backend_specialist_agent
                agent = get_backend_specialist_agent(config)
                return agent.execute_query(query)

            elif agent_role == AgentRole.PRD_WRITER:
                # Use PRD Writer agent (T065)
                from codeindex.web.agents.prd_writer import get_prd_writer_agent
                agent = get_prd_writer_agent(config)
                return agent.execute_query(query, context=context if 'context' in locals() else None)

            elif agent_role == AgentRole.SPECKIT_WRITER:
                # Use Spec-Kit Writer agent (T065)
                from codeindex.web.agents.speckit_writer import get_speckit_writer_agent
                agent = get_speckit_writer_agent(config)
                return agent.execute_query(query, context=context if 'context' in locals() else None)

            elif agent_role == AgentRole.GHERKIN_TEST_WRITER:
                # Use Gherkin Test Writer agent (T065)
                from codeindex.web.agents.gherkin_test_writer import get_gherkin_test_writer_agent
                agent = get_gherkin_test_writer_agent(config)
                return agent.execute_query(query, context=context if 'context' in locals() else None)

            elif agent_role == AgentRole.PLAYWRIGHT_TEST_WRITER:
                # Use Playwright Test Writer agent (T065)
                from codeindex.web.agents.playwright_test_writer import get_playwright_test_writer_agent
                agent = get_playwright_test_writer_agent(config)
                return agent.execute_query(query, context=context if 'context' in locals() else None)

            else:
                # Fallback for any unhandled agents
                response_text = self._generate_placeholder_response(agent_role, query)

                duration = time.time() - start_time

                return self.create_agent_response(
                    agent_role=agent_role,
                    query=query,
                    response_text=response_text,
                    duration=duration,
                    confidence=0.8,
                    suggested_questions=self._generate_follow_ups(query)
                )

        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Agent query failed: {e}", exc_info=True)

            return self.create_agent_response(
                agent_role=agent_role or AgentRole.SENIOR_DEVELOPER,
                query=query,
                response_text="",
                duration=duration,
                error=str(e)
            )

    def _generate_placeholder_response(self, agent_role: AgentRole, query: str) -> str:
        """
        Generate placeholder response for testing (until actual agents are implemented).

        Args:
            agent_role: Agent role
            query: User query

        Returns:
            Placeholder response text
        """
        return f"""
**{agent_role.value} Response** (Placeholder - Agent implementation pending)

Your query: "{query}"

This is a placeholder response. The actual {agent_role.value} agent will be
implemented in the user story phases. The agent will:

1. Search the Weaviate vector database for relevant artifacts
2. Analyze the code and extract insights
3. Generate a comprehensive response with citations
4. Provide follow-up questions for further exploration

**Note**: Full agent implementation is scheduled for Phase 6 (US2.1) and beyond.
        """

    def _generate_follow_ups(self, query: str) -> List[str]:
        """
        Generate suggested follow-up questions.

        Args:
            query: Original query

        Returns:
            List of suggested follow-up questions
        """
        # TODO: Implement intelligent follow-up generation in Phase 6 (US2.1)
        return [
            "Can you show me the implementation details?",
            "What are the dependencies for this component?",
            "Are there any related artifacts I should review?"
        ]


# Global service instance
_agent_service: Optional[AgentService] = None


def get_agent_service() -> AgentService:
    """
    Get global agent service instance.

    Returns:
        AgentService singleton
    """
    global _agent_service

    if _agent_service is None:
        _agent_service = AgentService()
        logger.info("Initialized agent service")

    return _agent_service
