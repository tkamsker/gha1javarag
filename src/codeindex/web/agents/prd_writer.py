"""
PRD Writer Agent for generating Product Requirements Documents.

This agent specializes in:
- Writing comprehensive PRDs from codebase analysis
- Defining objectives, stakeholders, success metrics
- Creating user stories and acceptance criteria
- Documenting functional and non-functional requirements
- Identifying out-of-scope items
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


class PrdWriterAgent:
    """
    PRD Writer Agent for generating Product Requirements Documents.

    Specializes in:
    - Analyzing codebase to understand features
    - Writing clear product requirements
    - Defining user stories with acceptance criteria
    - Documenting technical constraints
    - Setting success metrics and KPIs
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        """Initialize PRD Writer agent."""
        if config is None:
            config = get_agent_config(AgentRole.PRD_WRITER)

        self.config = config
        self.role = AgentRole.PRD_WRITER

        logger.info("Initialized PRD Writer agent")

    def execute_query(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """
        Execute query with PRD Writer agent.

        Args:
            query: Feature description or PRD request
            context: Optional context from previous interactions

        Returns:
            AgentResponse with generated PRD
        """
        start_time = datetime.now()

        try:
            logger.info(f"PRD Writer processing: {query[:50]}...")

            # Step 1: Search for relevant artifacts (comprehensive, no filters)
            artifacts = self._search_relevant_artifacts(query)

            # Step 2: Generate PRD using LLM
            prd_document = self._generate_document(query, artifacts, context)

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
                response_text=prd_document,
                citations=citations,
                confidence=0.85,
                suggested_questions=suggested_questions,
                tools_used=["WeaviateSearchTool", "LLMGenerationTool", "PrdFormatter"]
            )

        except Exception as e:
            logger.error(f"PRD Writer query failed: {e}", exc_info=True)
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
        Search for relevant artifacts (comprehensive, no type filters).

        Args:
            query: Search query

        Returns:
            List of relevant artifacts

        Raises:
            Exception: If search fails (propagates to execute_query)
        """
        logger.debug(f"Searching artifacts for PRD: {query}")

        from codeindex.web.services.search_service import get_search_service
        search_service = get_search_service()

        # Search with NO artifact type filters to get comprehensive context
        search_response = search_service.search(
            query=query,
            limit=20  # Get more artifacts for comprehensive PRD
        )

        artifacts = search_response.get("results", [])
        logger.info(f"Found {len(artifacts)} artifacts for PRD generation")

        return artifacts

    def _generate_document(
        self,
        query: str,
        artifacts: List[Dict[str, Any]],
        context: Optional[Dict[str, Any]]
    ) -> str:
        """
        Generate PRD using LLM.

        Args:
            query: Feature description
            artifacts: Relevant artifacts
            context: Optional context

        Returns:
            Generated PRD document
        """
        try:
            logger.debug("Generating PRD with Ollama LLM")

            from codeindex.services.ollama_client import OllamaClient

            # Build context from artifacts
            context_parts = []

            # Group artifacts by type
            artifact_types = {}
            for artifact in artifacts:
                artifact_type = artifact.get("artifactType", "Unknown")
                if artifact_type not in artifact_types:
                    artifact_types[artifact_type] = []
                artifact_types[artifact_type].append(artifact)

            # Add artifact summary by type
            if artifact_types:
                context_parts.append("## Codebase Components:\n")
                for artifact_type, items in artifact_types.items():
                    context_parts.append(f"\n**{artifact_type} ({len(items)}):**")
                    for item in items[:5]:  # Max 5 per type
                        file_path = item.get("relativePath") or item.get("fileName", "Unknown")
                        summary = item.get("summary", "")
                        context_parts.append(f"- `{file_path}`")
                        if summary:
                            context_parts.append(f"  {summary}")

            context_text = "\n".join(context_parts) if context_parts else "No specific artifacts found."

            # Create system prompt
            system_prompt = """You are a Technical Product Manager who writes clear, comprehensive Product Requirements Documents (PRDs).
Your PRDs follow industry best practices and include:

1. **Overview**: Feature purpose and business value
2. **Objectives**: Clear, measurable goals
3. **Stakeholders**: Who's involved and impacted
4. **User Stories**: As a [user], I want to [action], so that [benefit]
5. **Requirements**:
   - Functional requirements (what it must do)
   - Non-functional requirements (performance, security, usability)
6. **Success Metrics**: How to measure success (KPIs, metrics)
7. **Out of Scope**: What's explicitly NOT included
8. **Technical Considerations**: Architecture, dependencies, constraints

Write in clear, concise language. Use bullet points and structured sections.
Base your PRD on the actual codebase artifacts provided."""

            # Create user prompt
            user_prompt = f"""Feature Request: {query}

{context_text}

Please generate a comprehensive Product Requirements Document (PRD) for this feature based on the codebase context."""

            # Call Ollama
            ollama_client = OllamaClient()
            response = ollama_client.call_ollama(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.4,  # Slightly creative for business language
                format_json=False
            )

            prd = response.get("response", "")

            if not prd:
                prd = self._generate_fallback_prd(query, artifacts)

            logger.info(f"Generated PRD ({len(prd)} chars)")
            return prd.strip()

        except Exception as e:
            logger.error(f"Failed to generate PRD: {e}")
            return self._generate_fallback_prd(query, artifacts)

    def _generate_fallback_prd(self, query: str, artifacts: List[Dict[str, Any]]) -> str:
        """
        Generate basic PRD structure when LLM fails.

        Args:
            query: Feature request
            artifacts: Found artifacts

        Returns:
            Basic PRD template
        """
        sections = [
            f"# Product Requirements Document\n",
            f"## Feature: {query}\n",
            f"**Status**: Draft",
            f"**Author**: PRD Writer Agent",
            f"**Date**: {datetime.now().strftime('%Y-%m-%d')}\n",
            "## Overview",
            f"This PRD defines requirements for: {query}\n",
            "## Codebase Context",
            f"Found {len(artifacts)} relevant components in the codebase:\n"
        ]

        # Add artifacts
        for i, artifact in enumerate(artifacts[:10], 1):
            artifact_type = artifact.get("artifactType", "Unknown")
            file_path = artifact.get("relativePath") or artifact.get("fileName", "Unknown")
            sections.append(f"{i}. **{artifact_type}**: `{file_path}`")

        sections.extend([
            "\n## Objectives",
            "- [Define clear, measurable objectives]",
            "\n## User Stories",
            "- As a [user type], I want to [action], so that [benefit]",
            "\n## Requirements",
            "### Functional Requirements",
            "- [List specific functional requirements]",
            "### Non-Functional Requirements",
            "- Performance: [Define performance criteria]",
            "- Security: [Define security requirements]",
            "- Usability: [Define usability standards]",
            "\n## Success Metrics",
            "- [Define KPIs and success criteria]",
            "\n## Out of Scope",
            "- [List what is NOT included]",
            "\n**Note**: LLM generation failed. Please ensure Ollama is running."
        ])

        return "\n".join(sections)

    def _extract_citations(self, artifacts: List[Dict[str, Any]]) -> List[Citation]:
        """
        Extract citations from artifacts.

        Args:
            artifacts: Found artifacts

        Returns:
            List of citations
        """
        citations = []

        for artifact in artifacts[:10]:  # Limit to 10
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
        Generate follow-up suggestions for PRD refinement.

        Args:
            query: Original query
            artifacts: Found artifacts

        Returns:
            List of suggested questions
        """
        suggestions = [
            "Can you add more detailed acceptance criteria?",
            "What are the functional requirements for this feature?",
            "Can you expand the technical constraints section?",
            "What stakeholders should be involved in this feature?"
        ]

        return suggestions[:4]


# Global instance
_prd_writer_agent: Optional[PrdWriterAgent] = None


def get_prd_writer_agent(config: Optional[AgentConfig] = None) -> PrdWriterAgent:
    """
    Get global PRD Writer agent instance.

    Args:
        config: Optional agent configuration

    Returns:
        PrdWriterAgent singleton
    """
    global _prd_writer_agent

    if _prd_writer_agent is None:
        _prd_writer_agent = PrdWriterAgent(config)
        logger.info("Created global PRD Writer agent instance")

    return _prd_writer_agent


__all__ = [
    "PrdWriterAgent",
    "get_prd_writer_agent"
]
