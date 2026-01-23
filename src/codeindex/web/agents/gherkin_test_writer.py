"""
Gherkin Test Writer Agent for generating BDD test scenarios.

This agent specializes in:
- Writing Gherkin syntax (Given-When-Then)
- Creating scenario outlines with examples
- Defining acceptance criteria
- Generating comprehensive test coverage
- BDD best practices
"""

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


class GherkinTestWriterAgent:
    """
    Gherkin Test Writer Agent for BDD test scenarios.

    Specializes in:
    - Gherkin syntax (Feature, Scenario, Given-When-Then)
    - Scenario outlines with data tables
    - Background sections for common setup
    - Tags for test organization
    - Clear, testable acceptance criteria
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        """Initialize Gherkin Test Writer agent."""
        if config is None:
            config = get_agent_config(AgentRole.GHERKIN_TEST_WRITER)

        self.config = config
        self.role = AgentRole.GHERKIN_TEST_WRITER

        logger.info("Initialized Gherkin Test Writer agent")

    def execute_query(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """
        Execute query with Gherkin Test Writer agent.

        Args:
            query: Test scenario request
            context: Optional context from previous interactions

        Returns:
            AgentResponse with generated Gherkin scenarios
        """
        start_time = datetime.now()

        try:
            logger.info(f"Gherkin Test Writer processing: {query[:50]}...")

            # Step 1: Search for relevant artifacts (comprehensive)
            artifacts = self._search_relevant_artifacts(query)

            # Step 2: Generate Gherkin scenarios using LLM
            gherkin_scenarios = self._generate_document(query, artifacts, context)

            # Step 3: Extract citations
            citations = self._extract_citations(artifacts)

            # Step 4: Generate follow-up questions
            suggested_questions = self._generate_follow_ups(query, artifacts)

            duration = (datetime.now() - start_time).total_seconds()

            return AgentResponse(
                agent_role=self.role,
                query=query,
                timestamp=start_time.isoformat(),
                duration_seconds=duration,
                response_text=gherkin_scenarios,
                citations=citations,
                confidence=0.90,
                suggested_questions=suggested_questions,
                tools_used=["WeaviateSearchTool", "LLMGenerationTool", "GherkinFormatter"]
            )

        except Exception as e:
            logger.error(f"Gherkin Test Writer query failed: {e}", exc_info=True)
            duration = (datetime.now() - start_time).total_seconds()

            return AgentResponse(
                agent_role=self.role,
                query=query,
                timestamp=start_time.isoformat(),
                duration_seconds=duration,
                response_text="",
                error=str(e)
            )

    def _search_relevant_artifacts(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for relevant artifacts (comprehensive).

        Args:
            query: Search query

        Returns:
            List of relevant artifacts
        """
        try:
            logger.debug(f"Searching artifacts for Gherkin tests: {query}")

            from codeindex.web.services.search_service import get_search_service
            search_service = get_search_service()

            # Comprehensive search with NO type filters
            search_response = search_service.search(
                query=query,
                limit=15
            )

            artifacts = search_response.get("results", [])
            logger.info(f"Found {len(artifacts)} artifacts for test generation")

            return artifacts

        except Exception as e:
            logger.error(f"Artifact search failed: {e}")
            return []

    def _generate_document(
        self,
        query: str,
        artifacts: List[Dict[str, Any]],
        context: Optional[Dict[str, Any]]
    ) -> str:
        """
        Generate Gherkin test scenarios using LLM.

        Args:
            query: Test scenario request
            artifacts: Relevant artifacts
            context: Optional context

        Returns:
            Generated Gherkin scenarios
        """
        try:
            logger.debug("Generating Gherkin scenarios with Ollama LLM")

            from codeindex.services.ollama_client import OllamaClient

            # Build context from artifacts
            context_parts = []

            # Add artifacts for test context
            if artifacts:
                context_parts.append("## Components to Test:\n")
                for i, artifact in enumerate(artifacts[:10], 1):
                    artifact_type = artifact.get("artifactType", "Unknown")
                    file_path = artifact.get("relativePath") or artifact.get("fileName", "Unknown")
                    summary = artifact.get("summary", "")
                    entities = artifact.get("entities", [])

                    context_parts.append(f"{i}. **{artifact_type}** - `{file_path}`")
                    if summary:
                        context_parts.append(f"   {summary}")
                    if entities:
                        context_parts.append(f"   Entities: {', '.join(entities[:3])}")

            context_text = "\n".join(context_parts) if context_parts else "No specific components found."

            # Create system prompt
            system_prompt = """You are a QA Engineer expert in Behavior-Driven Development (BDD) and Gherkin syntax.
Generate comprehensive test scenarios following these guidelines:

**Gherkin Format:**
```gherkin
Feature: <Feature name>
  As a <user type>
  I want to <action>
  So that <benefit>

  Background:
    Given <common precondition>

  @tag
  Scenario: <Scenario name>
    Given <precondition>
    And <additional precondition>
    When <action>
    And <additional action>
    Then <expected result>
    And <additional result>

  @tag
  Scenario Outline: <Parameterized scenario>
    Given <precondition with <parameter>>
    When <action with <parameter>>
    Then <result with <parameter>>

    Examples:
      | parameter | expected |
      | value1    | result1  |
      | value2    | result2  |
```

**Best Practices:**
1. Use clear, business-readable language
2. Each step should be atomic and testable
3. Use scenario outlines for data-driven tests
4. Add tags for test organization (@smoke, @regression, @integration)
5. Include both positive and negative test cases
6. Cover edge cases and error conditions

Base scenarios on the actual codebase components provided."""

            # Create user prompt
            user_prompt = f"""Test Request: {query}

{context_text}

Please generate comprehensive Gherkin test scenarios covering this functionality."""

            # Call Ollama with configured client
            from codeindex.web.agents import get_configured_ollama_client
            ollama_client = get_configured_ollama_client()
            response = ollama_client.call_ollama(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.2,  # Very structured, specific syntax
                format_json=False
            )

            gherkin = response.get("response", "")

            if not gherkin:
                gherkin = self._generate_fallback_gherkin(query, artifacts)

            logger.info(f"Generated Gherkin scenarios ({len(gherkin)} chars)")
            return gherkin.strip()

        except Exception as e:
            logger.error(f"Failed to generate Gherkin scenarios: {e}")
            return self._generate_fallback_gherkin(query, artifacts)

    def _generate_fallback_gherkin(self, query: str, artifacts: List[Dict[str, Any]]) -> str:
        """
        Generate basic Gherkin template when LLM fails.

        Args:
            query: Test request
            artifacts: Found artifacts

        Returns:
            Basic Gherkin template
        """
        lines = [
            f"Feature: {query}",
            "  As a user",
            "  I want to test this functionality",
            "  So that I can ensure it works correctly\n",
            "  Background:",
            "    Given the system is initialized",
            "    And the database is seeded with test data\n"
        ]

        # Add scenarios based on artifacts
        if artifacts:
            lines.append("  @smoke")
            lines.append("  Scenario: Basic functionality test")

            for artifact in artifacts[:3]:
                artifact_type = artifact.get("artifactType", "Unknown")
                file_path = artifact.get("relativePath") or artifact.get("fileName", "Unknown")

                lines.append(f"    Given the {artifact_type} is available")
                lines.append(f"    # Component: {file_path}")

            lines.extend([
                "    When I perform the action",
                "    Then the system should respond correctly",
                "    And the result should be validated\n"
            ])

        lines.extend([
            "  @regression",
            "  Scenario Outline: Parameterized test",
            "    Given the system state is <state>",
            "    When I execute with <input>",
            "    Then I should see <output>",
            "    ",
            "    Examples:",
            "      | state    | input   | output  |",
            "      | ready    | valid   | success |",
            "      | busy     | valid   | retry   |",
            "      | ready    | invalid | error   |\n",
            "  # Note: LLM generation failed. Please ensure Ollama is running."
        ])

        return "\n".join(lines)

    def _extract_citations(self, artifacts: List[Dict[str, Any]]) -> List[Citation]:
        """
        Extract citations from artifacts.

        Args:
            artifacts: Found artifacts

        Returns:
            List of citations
        """
        citations = []

        for artifact in artifacts[:10]:
            artifact_id = artifact.get("_additional", {}).get("id", artifact.get("id", ""))
            distance = artifact.get("_additional", {}).get("distance", 0.0)
            confidence = 1.0 - distance if distance < 1.0 else 0.5

            citations.append(Citation(
                artifact_id=artifact_id,
                file_path=artifact.get("relativePath") or artifact.get("fileName", "Unknown"),
                artifact_type=artifact.get("artifactType", "Unknown"),
                confidence=confidence
            ))

        return citations

    def _generate_follow_ups(
        self,
        query: str,
        artifacts: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Generate follow-up suggestions for test refinement.

        Args:
            query: Original query
            artifacts: Found artifacts

        Returns:
            List of suggested questions
        """
        suggestions = [
            "Can you add negative test cases?",
            "What edge cases should we test?",
            "Can you add more scenario outlines with examples?",
            "What integration tests should we include?"
        ]

        return suggestions[:4]


# Global instance
_gherkin_test_writer_agent: Optional[GherkinTestWriterAgent] = None


def get_gherkin_test_writer_agent(config: Optional[AgentConfig] = None) -> GherkinTestWriterAgent:
    """
    Get global Gherkin Test Writer agent instance.

    Args:
        config: Optional agent configuration

    Returns:
        GherkinTestWriterAgent singleton
    """
    global _gherkin_test_writer_agent

    if _gherkin_test_writer_agent is None:
        _gherkin_test_writer_agent = GherkinTestWriterAgent(config)
        logger.info("Created global Gherkin Test Writer agent instance")

    return _gherkin_test_writer_agent


__all__ = [
    "GherkinTestWriterAgent",
    "get_gherkin_test_writer_agent"
]
