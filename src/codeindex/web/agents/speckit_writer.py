"""
Spec-Kit Writer Agent for generating technical specifications.

This agent specializes in:
- Writing detailed technical specifications
- Defining architecture and component design
- Documenting data models and API contracts
- Creating implementation plans
- Spec-Kit format compatibility
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


class SpeckitWriterAgent:
    """
    Spec-Kit Writer Agent for generating technical specifications.

    Specializes in:
    - Technical architecture documentation
    - Component and module design
    - Data models and schemas
    - API contracts and interfaces
    - Implementation planning
    - Spec-Kit format compliance
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        """Initialize Spec-Kit Writer agent."""
        if config is None:
            config = get_agent_config(AgentRole.SPECKIT_WRITER)

        self.config = config
        self.role = AgentRole.SPECKIT_WRITER

        logger.info("Initialized Spec-Kit Writer agent")

    def execute_query(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """
        Execute query with Spec-Kit Writer agent.

        Args:
            query: Specification request
            context: Optional context from previous interactions

        Returns:
            AgentResponse with generated specification
        """
        start_time = datetime.now()

        try:
            logger.info(f"Spec-Kit Writer processing: {query[:50]}...")

            # Step 1: Search for relevant artifacts (comprehensive)
            artifacts = self._search_relevant_artifacts(query)

            # Step 2: Generate specification using LLM
            spec_document = self._generate_document(query, artifacts, context)

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
                response_text=spec_document,
                citations=citations,
                confidence=0.88,
                suggested_questions=suggested_questions,
                tools_used=["WeaviateSearchTool", "LLMGenerationTool", "SpecKitFormatter"]
            )

        except Exception as e:
            logger.error(f"Spec-Kit Writer query failed: {e}", exc_info=True)
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
            logger.debug(f"Searching artifacts for specification: {query}")

            from codeindex.web.services.search_service import get_search_service
            search_service = get_search_service()

            # Comprehensive search with NO type filters
            search_response = search_service.search(
                query=query,
                limit=20
            )

            artifacts = search_response.get("results", [])
            logger.info(f"Found {len(artifacts)} artifacts for specification")

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
        Generate technical specification using LLM.

        Args:
            query: Specification request
            artifacts: Relevant artifacts
            context: Optional context

        Returns:
            Generated specification document
        """
        try:
            logger.debug("Generating specification with Ollama LLM")

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

            # Add artifact details
            if artifact_types:
                context_parts.append("## Codebase Architecture:\n")
                for artifact_type, items in artifact_types.items():
                    context_parts.append(f"\n**{artifact_type} ({len(items)}):**")
                    for item in items[:5]:
                        file_path = item.get("relativePath") or item.get("fileName", "Unknown")
                        summary = item.get("summary", "")
                        entities = item.get("entities", [])

                        context_parts.append(f"- `{file_path}`")
                        if summary:
                            context_parts.append(f"  {summary}")
                        if entities:
                            context_parts.append(f"  Entities: {', '.join(entities[:5])}")

            context_text = "\n".join(context_parts) if context_parts else "No specific artifacts found."

            # Create system prompt
            system_prompt = """You are a Software Architect who creates detailed technical specifications.
Your specifications follow Spec-Kit format and include:

1. **Overview**: High-level technical summary
2. **Architecture**: System design, components, layers
3. **Components**: Detailed component specifications
   - Responsibilities
   - Interfaces
   - Dependencies
4. **Data Models**: Schemas, entities, relationships
5. **API Contracts**: Endpoints, request/response formats
6. **Implementation Plan**: Phased approach, tasks, priorities
7. **Technical Decisions**: Architecture choices and rationale
8. **Dependencies**: External libraries, services, integrations
9. **Testing Strategy**: Unit, integration, E2E testing approach

Use precise technical language. Include diagrams (Mermaid format) where appropriate.
Base your specification on the actual codebase structure."""

            # Create user prompt
            user_prompt = f"""Specification Request: {query}

{context_text}

Please generate a comprehensive technical specification based on the codebase architecture."""

            # Call Ollama with configured client
            from codeindex.web.agents import get_configured_ollama_client
            ollama_client = get_configured_ollama_client()
            response = ollama_client.call_ollama(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.3,  # Precise technical language
                format_json=False
            )

            spec = response.get("response", "")

            if not spec:
                spec = self._generate_fallback_spec(query, artifacts)

            logger.info(f"Generated specification ({len(spec)} chars)")
            return spec.strip()

        except Exception as e:
            logger.error(f"Failed to generate specification: {e}")
            return self._generate_fallback_spec(query, artifacts)

    def _generate_fallback_spec(self, query: str, artifacts: List[Dict[str, Any]]) -> str:
        """
        Generate basic specification when LLM fails.

        Args:
            query: Specification request
            artifacts: Found artifacts

        Returns:
            Basic spec template
        """
        sections = [
            f"# Technical Specification\n",
            f"## Feature: {query}\n",
            f"**Status**: Draft",
            f"**Author**: Spec-Kit Writer Agent",
            f"**Date**: {datetime.now().strftime('%Y-%m-%d')}\n",
            "## Overview",
            f"Technical specification for: {query}\n",
            "## Architecture",
            f"Based on {len(artifacts)} codebase components:\n"
        ]

        # Group artifacts
        artifact_types = {}
        for artifact in artifacts[:15]:
            artifact_type = artifact.get("artifactType", "Unknown")
            if artifact_type not in artifact_types:
                artifact_types[artifact_type] = []
            artifact_types[artifact_type].append(artifact)

        # Add by type
        for artifact_type, items in artifact_types.items():
            sections.append(f"\n### {artifact_type} Layer ({len(items)} components)")
            for item in items[:5]:
                file_path = item.get("relativePath") or item.get("fileName", "Unknown")
                sections.append(f"- `{file_path}`")

        sections.extend([
            "\n## Components",
            "[Define component responsibilities and interfaces]",
            "\n## Data Models",
            "[Document data schemas and entity relationships]",
            "\n## API Contracts",
            "[Define API endpoints and formats]",
            "\n## Implementation Plan",
            "1. Phase 1: [Define phases]",
            "2. Phase 2: [...]",
            "\n## Testing Strategy",
            "- Unit tests: [Define approach]",
            "- Integration tests: [Define approach]",
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

        for artifact in artifacts[:15]:  # More citations for technical specs
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
        Generate follow-up suggestions for spec refinement.

        Args:
            query: Original query
            artifacts: Found artifacts

        Returns:
            List of suggested questions
        """
        suggestions = [
            "Can you add sequence diagrams for key flows?",
            "What are the API endpoint specifications?",
            "Can you detail the data model schemas?",
            "What are the component dependencies?"
        ]

        return suggestions[:4]


# Global instance
_speckit_writer_agent: Optional[SpeckitWriterAgent] = None


def get_speckit_writer_agent(config: Optional[AgentConfig] = None) -> SpeckitWriterAgent:
    """
    Get global Spec-Kit Writer agent instance.

    Args:
        config: Optional agent configuration

    Returns:
        SpeckitWriterAgent singleton
    """
    global _speckit_writer_agent

    if _speckit_writer_agent is None:
        _speckit_writer_agent = SpeckitWriterAgent(config)
        logger.info("Created global Spec-Kit Writer agent instance")

    return _speckit_writer_agent


__all__ = [
    "SpeckitWriterAgent",
    "get_speckit_writer_agent"
]
