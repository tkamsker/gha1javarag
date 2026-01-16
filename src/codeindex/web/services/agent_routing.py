"""
Agent Routing Service (T063 - US2.1).

Routes user queries to appropriate AI agents based on keyword analysis,
context awareness, and confidence scoring.

Routing Strategy:
- Keyword-based routing with configurable rules
- Context-aware routing for follow-up questions
- Confidence scoring for ambiguous queries
- Fallback to Senior Developer for general questions
"""

import logging
import re
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
from datetime import datetime

from codeindex.web.agents.base import AgentRole

logger = logging.getLogger(__name__)


# Default routing rules (keyword → agent role)
DEFAULT_ROUTING_RULES = {
    AgentRole.DATA_ANALYST: [
        "database", "schema", "table", "sql", "query", "foreign key", "index",
        "dao", "entity", "hibernate", "jpa", "ibatis", "mybatis", "relationship"
    ],
    AgentRole.FRONTEND_SPECIALIST: [
        "ui", "interface", "form", "gwt", "presenter", "view", "widget",
        "javascript", "js", "css", "html", "jsp", "uibinder", "component"
    ],
    AgentRole.BACKEND_SPECIALIST: [
        "api", "rest", "endpoint", "service", "controller", "servlet",
        "business logic", "dto", "validation", "authentication", "authorization"
    ],
    AgentRole.PRD_WRITER: [
        "prd", "product requirements", "requirements document", "requirement",
        "user story", "user stories", "specification", "feature", "document the"
    ],
    AgentRole.GHERKIN_TEST_WRITER: [
        "gherkin", "bdd", "cucumber", "given when then", "given-when-then",
        "scenario", "feature test"
    ],
    AgentRole.PLAYWRIGHT_TEST_WRITER: [
        "playwright", "e2e", "end-to-end", "browser test", "automation test",
        "ui test", "browser automation"
    ]
}


class AgentRoutingService:
    """
    Service for routing user queries to appropriate AI agents.

    Features:
    - Keyword-based routing with confidence scoring
    - Context-aware routing for follow-up questions
    - Conversation history tracking
    - Custom routing rules
    - Routing metrics and statistics
    """

    def __init__(self, custom_rules: Optional[Dict[AgentRole, List[str]]] = None):
        """
        Initialize routing service.

        Args:
            custom_rules: Optional custom routing rules to override defaults
        """
        self.routing_rules = DEFAULT_ROUTING_RULES.copy()
        if custom_rules:
            self.routing_rules.update(custom_rules)

        # Disabled agents
        self._disabled_agents = set()

        # Routing history for metrics
        self._routing_history: List[Dict] = []
        self._routing_stats: Dict[AgentRole, int] = defaultdict(int)

        logger.info("Initialized AgentRoutingService with routing rules")

    def route_query(
        self,
        query: str,
        context: Optional[Dict] = None
    ) -> AgentRole:
        """
        Route query to appropriate agent.

        Args:
            query: User query string
            context: Optional context with previous_agent, conversation_history

        Returns:
            AgentRole for handling the query
        """
        agent_role, _ = self.route_query_with_confidence(query, context)
        return agent_role

    def route_query_with_confidence(
        self,
        query: str,
        context: Optional[Dict] = None
    ) -> Tuple[AgentRole, float]:
        """
        Route query with confidence score.

        Args:
            query: User query string
            context: Optional context

        Returns:
            Tuple of (AgentRole, confidence_score)
        """
        if not query or len(query.strip()) == 0:
            return AgentRole.SENIOR_DEVELOPER, 0.0

        # Normalize query
        normalized_query = query.lower()

        # Check for context-based routing (follow-up questions)
        if context:
            previous_agent = context.get("previous_agent")
            conversation_history = context.get("conversation_history", [])

            # If previous agent exists and query is ambiguous, use same agent
            if previous_agent and self._is_follow_up_query(normalized_query):
                logger.info(f"Context-aware routing: Using previous agent {previous_agent}")
                self._track_routing(query, previous_agent, 0.9, "context_aware")
                return previous_agent, 0.9

            # Check conversation history for domain consistency
            if conversation_history and len(conversation_history) >= 2:
                # If last 2 queries used same agent, continue with it for ambiguous queries
                recent_agents = [h.get("agent") for h in conversation_history[-2:]]
                if len(set(recent_agents)) == 1 and self._is_ambiguous_query(normalized_query):
                    consistent_agent = recent_agents[0]
                    logger.info(f"Conversation history routing: Using consistent agent {consistent_agent}")
                    self._track_routing(query, consistent_agent, 0.8, "history_consistent")
                    return consistent_agent, 0.8

        # Score each agent based on keyword matches
        agent_scores: Dict[AgentRole, float] = {}

        for agent_role, keywords in self.routing_rules.items():
            # Skip disabled agents
            if agent_role in self._disabled_agents:
                continue

            # Count keyword matches
            matches = sum(1 for keyword in keywords if keyword in normalized_query)

            if matches > 0:
                # Calculate confidence: matches / total keywords
                confidence = min(matches / len(keywords), 1.0)
                agent_scores[agent_role] = confidence

        # If no matches, fallback to Senior Developer
        if not agent_scores:
            logger.info(f"No keyword matches, fallback to Senior Developer")
            self._track_routing(query, AgentRole.SENIOR_DEVELOPER, 0.5, "fallback")
            return AgentRole.SENIOR_DEVELOPER, 0.5

        # Get agent with highest score
        best_agent = max(agent_scores.items(), key=lambda x: x[1])
        agent_role, confidence = best_agent

        logger.info(f"Routed to {agent_role} with confidence {confidence:.2f}")
        self._track_routing(query, agent_role, confidence, "keyword_match")

        return agent_role, confidence

    def add_routing_rule(self, agent_role: AgentRole, keywords: List[str]):
        """
        Add custom routing rule.

        Args:
            agent_role: Agent role to add rules for
            keywords: List of keywords to trigger this agent
        """
        if agent_role not in self.routing_rules:
            self.routing_rules[agent_role] = []

        self.routing_rules[agent_role].extend(keywords)
        logger.info(f"Added {len(keywords)} keywords to {agent_role}")

    def override_routing_rule(self, agent_role: AgentRole, keywords: List[str]):
        """
        Override default routing rule completely.

        Args:
            agent_role: Agent role to override
            keywords: New list of keywords (replaces existing)
        """
        self.routing_rules[agent_role] = keywords
        logger.info(f"Overridden routing rules for {agent_role} with {len(keywords)} keywords")

    def disable_agent(self, agent_role: AgentRole):
        """
        Disable routing to specific agent.

        Args:
            agent_role: Agent to disable
        """
        self._disabled_agents.add(agent_role)
        logger.info(f"Disabled agent: {agent_role}")

    def enable_agent(self, agent_role: AgentRole):
        """
        Enable previously disabled agent.

        Args:
            agent_role: Agent to enable
        """
        self._disabled_agents.discard(agent_role)
        logger.info(f"Enabled agent: {agent_role}")

    def get_routing_history(self) -> List[Dict]:
        """
        Get routing decision history.

        Returns:
            List of routing decisions with timestamps
        """
        return self._routing_history.copy()

    def get_routing_statistics(self) -> Dict[AgentRole, int]:
        """
        Get routing statistics (count by agent).

        Returns:
            Dictionary of agent role → count
        """
        return dict(self._routing_stats)

    def _is_follow_up_query(self, normalized_query: str) -> bool:
        """
        Check if query is a follow-up question.

        Args:
            normalized_query: Lowercased query

        Returns:
            True if query appears to be follow-up
        """
        follow_up_patterns = [
            r"^(how|what|why|when|where|who|can|does|is|are)\s+(they|it|that|this|those)",
            r"^(and|also|additionally|furthermore)",
            r"^(tell me more|explain|elaborate|details about)",
            r"(related|connection|relationship)",
        ]

        for pattern in follow_up_patterns:
            if re.search(pattern, normalized_query):
                return True

        # Short queries (<20 chars) are likely follow-ups
        if len(normalized_query) < 20:
            return True

        return False

    def _is_ambiguous_query(self, normalized_query: str) -> bool:
        """
        Check if query is ambiguous (no clear keywords).

        Args:
            normalized_query: Lowercased query

        Returns:
            True if query is ambiguous
        """
        # Count keyword matches across all agents
        total_matches = 0
        for keywords in self.routing_rules.values():
            total_matches += sum(1 for keyword in keywords if keyword in normalized_query)

        # If fewer than 2 keyword matches, query is ambiguous
        return total_matches < 2

    def _track_routing(
        self,
        query: str,
        agent_role: AgentRole,
        confidence: float,
        reason: str
    ):
        """
        Track routing decision for metrics.

        Args:
            query: Original query
            agent_role: Selected agent
            confidence: Confidence score
            reason: Routing reason (keyword_match, context_aware, fallback)
        """
        self._routing_history.append({
            "timestamp": datetime.now().isoformat(),
            "query": query[:100],  # Truncate for privacy
            "agent": agent_role,
            "confidence": confidence,
            "reason": reason
        })

        self._routing_stats[agent_role] += 1


# Global routing service instance
_routing_service: Optional[AgentRoutingService] = None


def get_agent_routing_service(
    custom_rules: Optional[Dict[AgentRole, List[str]]] = None
) -> AgentRoutingService:
    """
    Get global routing service instance (singleton).

    Args:
        custom_rules: Optional custom routing rules (only used on first call)

    Returns:
        AgentRoutingService singleton
    """
    global _routing_service

    if _routing_service is None:
        _routing_service = AgentRoutingService(custom_rules)
        logger.info("Initialized global routing service")

    return _routing_service


__all__ = [
    "AgentRoutingService",
    "get_agent_routing_service",
    "DEFAULT_ROUTING_RULES"
]
