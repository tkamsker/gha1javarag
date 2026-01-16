"""
Unit tests for Agent Routing Logic (T055 - US2.1).

Tests cover the routing service that determines which agent to use based on
user query content using keyword heuristics and contextual analysis.

Tests cover:
- Keyword-based routing to correct agent
- Multi-keyword ambiguous queries
- Fallback to Senior Developer for general queries
- Context-aware routing for follow-up questions
- Edge cases and error handling
"""

import pytest
from typing import List, Dict, Any, Optional
from unittest.mock import Mock, patch, MagicMock

from codeindex.web.agents.base import AgentRole


class TestAgentRoutingServiceInitialization:
    """Test AgentRoutingService initialization."""

    def test_service_initializes_with_default_routes(self):
        """Test service initialization with default routing rules."""
        from codeindex.web.services.agent_routing import AgentRoutingService

        service = AgentRoutingService()

        assert service is not None
        assert hasattr(service, 'route_query')
        assert hasattr(service, 'routing_rules')

    def test_service_initializes_with_custom_routes(self):
        """Test service initialization with custom routing rules."""
        from codeindex.web.services.agent_routing import AgentRoutingService

        custom_rules = {
            AgentRole.DATA_ANALYST: ["database", "schema", "SQL"]
        }

        service = AgentRoutingService(custom_rules=custom_rules)

        assert service.routing_rules is not None


class TestAgentRoutingKeywordDetection:
    """Test keyword-based agent routing."""

    def test_routes_database_queries_to_data_analyst(self):
        """Test database-related queries route to Data Analyst agent."""
        from codeindex.web.services.agent_routing import AgentRoutingService

        service = AgentRoutingService()

        queries = [
            "What tables are in the database?",
            "Show me the database schema",
            "Analyze the SQL queries",
            "Find foreign key relationships"
        ]

        for query in queries:
            agent_role = service.route_query(query)
            assert agent_role == AgentRole.DATA_ANALYST

    def test_routes_frontend_queries_to_frontend_specialist(self):
        """Test frontend-related queries route to Frontend Specialist agent."""
        from codeindex.web.services.agent_routing import AgentRoutingService

        service = AgentRoutingService()

        queries = [
            "How does the user interface work?",
            "Explain the GWT presenters",
            "What forms are in the UI?",
            "Analyze the JavaScript code"
        ]

        for query in queries:
            agent_role = service.route_query(query)
            assert agent_role == AgentRole.FRONTEND_SPECIALIST

    def test_routes_backend_queries_to_backend_specialist(self):
        """Test backend-related queries route to Backend Specialist agent."""
        from codeindex.web.services.agent_routing import AgentRoutingService

        service = AgentRoutingService()

        queries = [
            "How does the REST API work?",
            "Explain the service layer",
            "What endpoints are available?",
            "Analyze the business logic"
        ]

        for query in queries:
            agent_role = service.route_query(query)
            assert agent_role == AgentRole.BACKEND_SPECIALIST

    def test_routes_documentation_queries_to_prd_writer(self):
        """Test documentation-related queries route to PRD Writer agent."""
        from codeindex.web.services.agent_routing import AgentRoutingService

        service = AgentRoutingService()

        queries = [
            "Generate a PRD for this module",
            "Write product requirements",
            "Create user stories",
            "Document the requirements"
        ]

        for query in queries:
            agent_role = service.route_query(query)
            assert agent_role == AgentRole.PRD_WRITER

    def test_routes_test_queries_to_test_writer_agents(self):
        """Test test generation queries route to appropriate test writer agents."""
        from codeindex.web.services.agent_routing import AgentRoutingService

        service = AgentRoutingService()

        gherkin_queries = [
            "Generate Gherkin tests",
            "Create BDD scenarios",
            "Write Given-When-Then tests"
        ]

        playwright_queries = [
            "Generate Playwright tests",
            "Create E2E test scripts",
            "Write browser automation tests"
        ]

        for query in gherkin_queries:
            agent_role = service.route_query(query)
            assert agent_role == AgentRole.GHERKIN_TEST_WRITER

        for query in playwright_queries:
            agent_role = service.route_query(query)
            assert agent_role == AgentRole.PLAYWRIGHT_TEST_WRITER

    def test_routes_general_queries_to_senior_developer(self):
        """Test general queries route to Senior Developer (fallback)."""
        from codeindex.web.services.agent_routing import AgentRoutingService

        service = AgentRoutingService()

        queries = [
            "What does this code do?",
            "Explain the architecture",
            "How does user registration work?",
            "What are the design patterns used?"
        ]

        for query in queries:
            agent_role = service.route_query(query)
            assert agent_role == AgentRole.SENIOR_DEVELOPER


class TestAgentRoutingAmbiguousQueries:
    """Test routing for ambiguous queries with multiple keywords."""

    def test_routes_ambiguous_query_to_most_specific_agent(self):
        """Test ambiguous query routes to most specific agent."""
        from codeindex.web.services.agent_routing import AgentRoutingService

        service = AgentRoutingService()

        # Query mentions both database and UI - database is more specific
        query = "How does the UI connect to the database?"
        agent_role = service.route_query(query)

        # Should prioritize Data Analyst for database-specific questions
        assert agent_role in [AgentRole.DATA_ANALYST, AgentRole.SENIOR_DEVELOPER]

    def test_routes_ambiguous_query_based_on_keyword_frequency(self):
        """Test ambiguous query routes based on keyword frequency."""
        from codeindex.web.services.agent_routing import AgentRoutingService

        service = AgentRoutingService()

        # Multiple database keywords
        query = "Analyze the database schema, tables, and SQL queries"
        agent_role = service.route_query(query)

        assert agent_role == AgentRole.DATA_ANALYST

    def test_routes_ambiguous_query_with_confidence_score(self):
        """Test routing returns confidence score for ambiguous queries."""
        from codeindex.web.services.agent_routing import AgentRoutingService

        service = AgentRoutingService()

        query = "How does the system work?"
        agent_role, confidence = service.route_query_with_confidence(query)

        assert agent_role == AgentRole.SENIOR_DEVELOPER  # Fallback
        assert 0.0 <= confidence <= 1.0
        assert confidence < 0.7  # Low confidence for ambiguous query


class TestAgentRoutingContextAware:
    """Test context-aware routing for follow-up questions."""

    def test_routes_follow_up_question_to_same_agent(self):
        """Test follow-up question routes to same agent as previous query."""
        from codeindex.web.services.agent_routing import AgentRoutingService

        service = AgentRoutingService()

        # First query
        query1 = "What tables are in the database?"
        agent1 = service.route_query(query1)

        # Follow-up query (ambiguous without context)
        query2 = "How are they related?"
        context = {"previous_agent": agent1}
        agent2 = service.route_query(query2, context=context)

        # Should use same agent (Data Analyst) due to context
        assert agent2 == agent1 == AgentRole.DATA_ANALYST

    def test_routes_with_conversation_history(self):
        """Test routing considers conversation history."""
        from codeindex.web.services.agent_routing import AgentRoutingService

        service = AgentRoutingService()

        conversation_history = [
            {"query": "Explain the database schema", "agent": AgentRole.DATA_ANALYST},
            {"query": "What about foreign keys?", "agent": AgentRole.DATA_ANALYST}
        ]

        # New query continues database discussion
        query = "And the indexes?"
        context = {"conversation_history": conversation_history}
        agent_role = service.route_query(query, context=context)

        # Should continue with Data Analyst
        assert agent_role == AgentRole.DATA_ANALYST

    def test_routes_context_switch_to_different_agent(self):
        """Test routing switches agent when context clearly changes."""
        from codeindex.web.services.agent_routing import AgentRoutingService

        service = AgentRoutingService()

        context = {"previous_agent": AgentRole.DATA_ANALYST}

        # Explicit switch to frontend question
        query = "Now explain the UI components"
        agent_role = service.route_query(query, context=context)

        # Should switch to Frontend Specialist despite previous context
        assert agent_role == AgentRole.FRONTEND_SPECIALIST


class TestAgentRoutingEdgeCases:
    """Test routing edge cases and error handling."""

    def test_handles_empty_query(self):
        """Test routing handles empty query gracefully."""
        from codeindex.web.services.agent_routing import AgentRoutingService

        service = AgentRoutingService()

        agent_role = service.route_query("")

        # Should fallback to Senior Developer
        assert agent_role == AgentRole.SENIOR_DEVELOPER

    def test_handles_very_short_query(self):
        """Test routing handles very short queries."""
        from codeindex.web.services.agent_routing import AgentRoutingService

        service = AgentRoutingService()

        agent_role = service.route_query("Help")

        assert agent_role == AgentRole.SENIOR_DEVELOPER

    def test_handles_query_with_special_characters(self):
        """Test routing handles queries with special characters."""
        from codeindex.web.services.agent_routing import AgentRoutingService

        service = AgentRoutingService()

        query = "What's the @Entity annotation? #database"
        agent_role = service.route_query(query)

        # Should still detect database keyword
        assert agent_role in [AgentRole.DATA_ANALYST, AgentRole.SENIOR_DEVELOPER]

    def test_handles_case_insensitive_keywords(self):
        """Test routing is case-insensitive."""
        from codeindex.web.services.agent_routing import AgentRoutingService

        service = AgentRoutingService()

        queries = [
            "What DATABASE tables exist?",
            "Explain the Database SCHEMA",
            "analyze the sql QUERIES"
        ]

        for query in queries:
            agent_role = service.route_query(query)
            assert agent_role == AgentRole.DATA_ANALYST

    def test_handles_multilingual_queries(self):
        """Test routing handles non-English queries gracefully."""
        from codeindex.web.services.agent_routing import AgentRoutingService

        service = AgentRoutingService()

        # Query in another language (fallback expected)
        query = "Was macht dieser Code?"  # German: "What does this code do?"
        agent_role = service.route_query(query)

        # Should fallback to Senior Developer (keywords not matched)
        assert agent_role == AgentRole.SENIOR_DEVELOPER


class TestAgentRoutingConfiguration:
    """Test routing configuration and customization."""

    def test_add_custom_routing_rule(self):
        """Test adding custom routing rules."""
        from codeindex.web.services.agent_routing import AgentRoutingService

        service = AgentRoutingService()

        # Add custom rule
        service.add_routing_rule(AgentRole.DATA_ANALYST, ["postgres", "mysql"])

        query = "Connect to postgres database"
        agent_role = service.route_query(query)

        assert agent_role == AgentRole.DATA_ANALYST

    def test_override_default_routing_rule(self):
        """Test overriding default routing rules."""
        from codeindex.web.services.agent_routing import AgentRoutingService

        service = AgentRoutingService()

        # Override default rule
        service.override_routing_rule(AgentRole.BACKEND_SPECIALIST, ["database", "SQL"])

        query = "What database tables exist?"
        agent_role = service.route_query(query)

        # Should now route to Backend Specialist instead of Data Analyst
        assert agent_role == AgentRole.BACKEND_SPECIALIST

    def test_disable_agent_routing(self):
        """Test disabling routing for specific agent."""
        from codeindex.web.services.agent_routing import AgentRoutingService

        service = AgentRoutingService()

        # Disable Data Analyst routing
        service.disable_agent(AgentRole.DATA_ANALYST)

        query = "What database tables exist?"
        agent_role = service.route_query(query)

        # Should fallback to Senior Developer (Data Analyst disabled)
        assert agent_role != AgentRole.DATA_ANALYST
        assert agent_role == AgentRole.SENIOR_DEVELOPER


class TestAgentRoutingMetrics:
    """Test routing metrics and logging."""

    def test_tracks_routing_decisions(self):
        """Test routing tracks decision history."""
        from codeindex.web.services.agent_routing import AgentRoutingService

        service = AgentRoutingService()

        queries = [
            "What database tables exist?",
            "Explain the UI",
            "How does authentication work?"
        ]

        for query in queries:
            service.route_query(query)

        # Should have routing history
        history = service.get_routing_history()
        assert len(history) == 3

    def test_provides_routing_statistics(self):
        """Test routing provides statistics."""
        from codeindex.web.services.agent_routing import AgentRoutingService

        service = AgentRoutingService()

        # Execute multiple queries
        service.route_query("Database schema")  # Data Analyst
        service.route_query("Database tables")  # Data Analyst
        service.route_query("UI components")    # Frontend Specialist
        service.route_query("General question") # Senior Developer

        stats = service.get_routing_statistics()

        assert stats[AgentRole.DATA_ANALYST] == 2
        assert stats[AgentRole.FRONTEND_SPECIALIST] == 1
        assert stats[AgentRole.SENIOR_DEVELOPER] >= 1

    def test_logs_routing_decisions(self, caplog):
        """Test routing logs decisions for debugging."""
        from codeindex.web.services.agent_routing import AgentRoutingService

        service = AgentRoutingService()

        query = "What database tables exist?"
        agent_role = service.route_query(query)

        # Should have logged routing decision
        assert any("route" in record.message.lower() or "agent" in record.message.lower() for record in caplog.records)


# Test routing service singleton

def test_get_agent_routing_service():
    """Test get_agent_routing_service returns singleton."""
    from codeindex.web.services.agent_routing import get_agent_routing_service

    service1 = get_agent_routing_service()
    service2 = get_agent_routing_service()

    assert service1 is service2  # Same instance


def test_routing_service_thread_safe():
    """Test routing service is thread-safe for concurrent requests."""
    from codeindex.web.services.agent_routing import get_agent_routing_service
    import threading

    service = get_agent_routing_service()
    results = []

    def route_query(query):
        agent_role = service.route_query(query)
        results.append(agent_role)

    threads = [
        threading.Thread(target=route_query, args=("Database schema",))
        for _ in range(10)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    # All threads should complete successfully
    assert len(results) == 10
    assert all(r == AgentRole.DATA_ANALYST for r in results)
