"""
Backend Specialist Agent for server-side architecture analysis.

This agent specializes in:
- Service layer architecture
- Business logic patterns
- REST/RPC endpoints
- Backend integration patterns
- Transaction management
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


class BackendSpecialistAgent:
    """
    Backend Specialist Agent for server-side architecture.

    Specializes in:
    - Service layer design patterns
    - Business logic organization
    - GWT RPC servlet implementation
    - REST endpoint analysis
    - Transaction boundaries
    - Backend integration (DAO, services, controllers)
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        """Initialize Backend Specialist agent."""
        if config is None:
            config = get_agent_config(AgentRole.BACKEND_SPECIALIST)

        self.config = config
        self.role = AgentRole.BACKEND_SPECIALIST

        logger.info(f"Initialized Backend Specialist agent")

    def execute_query(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """
        Execute query with Backend Specialist agent.

        Args:
            query: User question about backend/server-side code
            context: Optional context from previous interactions

        Returns:
            AgentResponse with backend analysis
        """
        start_time = datetime.now()

        try:
            logger.info(f"Backend Specialist processing: {query[:50]}...")

            # Step 1: Search for backend artifacts
            backend_artifacts = self._search_backend_artifacts(query)

            # Step 2: Generate backend analysis using LLM
            analysis = self._generate_backend_analysis(
                query, backend_artifacts, context
            )

            # Step 3: Extract citations
            citations = self._extract_citations(backend_artifacts)

            # Step 4: Generate follow-up questions
            suggested_questions = self._generate_follow_ups(query, backend_artifacts)

            duration = (datetime.now() - start_time).total_seconds()

            return AgentResponse(
                agent_role=self.role,
                query=query,
                timestamp=start_time.isoformat(),
                duration_seconds=duration,
                response_text=analysis,
                citations=citations,
                confidence=0.84,
                suggested_questions=suggested_questions,
                tools_used=["WeaviateSearchTool", "LLMQueryTool", "ServiceAnalyzer"]
            )

        except Exception as e:
            logger.error(f"Backend Specialist query failed: {e}", exc_info=True)
            duration = (datetime.now() - start_time).total_seconds()

            return AgentResponse(
                agent_role=self.role,
                query=query,
                timestamp=start_time.isoformat(),
                duration_seconds=duration,
                response_text="",
                error=str(e)
            )

    def _search_backend_artifacts(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for backend-related artifacts.

        Searches for:
        - BackendDoc artifacts (services, controllers)
        - GwtEndpoint artifacts (RPC servlets)
        - DaoCall artifacts

        Args:
            query: Search query

        Returns:
            List of backend artifacts
        """
        try:
            logger.debug(f"Searching backend artifacts for: {query}")

            # Use SearchService to query Weaviate with backend-specific filters
            from codeindex.web.services.search_service import get_search_service
            search_service = get_search_service()

            # Search with backend-related artifact types
            search_response = search_service.search(
                query=query,
                filters={
                    "artifact_types": ["BackendDoc", "GwtEndpoint", "DaoCall"]
                },
                limit=15  # Get more results for comprehensive backend analysis
            )

            artifacts = search_response.get("results", [])
            logger.info(f"Found {len(artifacts)} backend artifacts")

            return artifacts

        except Exception as e:
            logger.error(f"Backend artifact search failed: {e}")
            return []

    def _generate_backend_analysis(
        self,
        query: str,
        artifacts: List[Dict[str, Any]],
        context: Optional[Dict[str, Any]]
    ) -> str:
        """
        Generate backend analysis using LLM.

        Args:
            query: User query
            artifacts: Backend artifacts
            context: Optional context

        Returns:
            Analysis text
        """
        try:
            logger.debug("Generating backend analysis with Ollama LLM")

            # Import Ollama client
            from codeindex.services.ollama_client import OllamaClient

            # Build context from backend artifacts
            context_parts = []

            # Add artifact summaries grouped by type
            if artifacts:
                # Group artifacts by type
                services = [a for a in artifacts if a.get("artifactType") == "BackendDoc"]
                endpoints = [a for a in artifacts if a.get("artifactType") == "GwtEndpoint"]
                dao_calls = [a for a in artifacts if a.get("artifactType") == "DaoCall"]

                # Add Services section
                if services:
                    context_parts.append("## Backend Services:\n")
                    for i, artifact in enumerate(services[:5], 1):
                        file_path = artifact.get("relativePath") or artifact.get("fileName", "Unknown")
                        summary = artifact.get("summary", "")
                        entities = artifact.get("entities", [])

                        context_parts.append(f"{i}. `{file_path}`")
                        if entities:
                            context_parts.append(f"   Methods: {', '.join(entities[:10])}")
                        if summary:
                            context_parts.append(f"   {summary}")
                        context_parts.append("")

                # Add GWT RPC Endpoints section
                if endpoints:
                    context_parts.append("\n## GWT RPC Endpoints:\n")
                    for i, artifact in enumerate(endpoints[:5], 1):
                        file_path = artifact.get("relativePath") or artifact.get("fileName", "Unknown")
                        summary = artifact.get("summary", "")
                        entities = artifact.get("entities", [])

                        context_parts.append(f"{i}. `{file_path}`")
                        if entities:
                            context_parts.append(f"   RPC Methods: {', '.join(entities[:10])}")
                        if summary:
                            context_parts.append(f"   {summary}")
                        context_parts.append("")

                # Add DAO Calls section
                if dao_calls:
                    context_parts.append("\n## Data Access Layer:\n")
                    for i, artifact in enumerate(dao_calls[:5], 1):
                        file_path = artifact.get("relativePath") or artifact.get("fileName", "Unknown")
                        summary = artifact.get("summary", "")
                        entities = artifact.get("entities", [])

                        context_parts.append(f"{i}. `{file_path}`")
                        if entities:
                            context_parts.append(f"   DAO Methods: {', '.join(entities[:10])}")
                        if summary:
                            context_parts.append(f"   {summary}")
                        context_parts.append("")

            context_text = "\n".join(context_parts) if context_parts else "No backend artifacts found."

            # Create system prompt
            system_prompt = """You are a Backend Specialist with expertise in service layers, APIs, and business logic.
Analyze the provided backend artifacts and answer the user's question with:

1. Clear explanations of service architecture and design patterns
2. Business logic flow and transaction boundaries
3. API contract analysis (GWT RPC, REST endpoints)
4. Service-to-DAO integration patterns
5. Error handling and validation strategies
6. Specific references to services, endpoints, and methods

Keep responses focused on backend/server-side aspects and business logic."""

            # Create user prompt
            user_prompt = f"""Question: {query}

{context_text}

Please analyze the backend artifacts and provide a comprehensive answer focused on service architecture, business logic, and API contracts."""

            # Call Ollama
            ollama_client = OllamaClient()
            response = ollama_client.call_ollama(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.3,
                format_json=False
            )

            analysis = response.get("response", "")

            if not analysis:
                analysis = "Unable to generate backend analysis. Please try rephrasing your question."

            logger.info(f"Generated backend analysis ({len(analysis)} chars)")
            return analysis.strip()

        except Exception as e:
            logger.error(f"Failed to generate backend analysis: {e}")

            # Fallback response with structured info
            fallback = [
                f"I encountered an error while analyzing the backend: {str(e)}\n",
                f"However, I found {len(artifacts)} backend artifacts:\n"
            ]

            # Group artifacts by type for fallback
            artifact_counts = {}
            for artifact in artifacts:
                artifact_type = artifact.get("artifactType", "Unknown")
                artifact_counts[artifact_type] = artifact_counts.get(artifact_type, 0) + 1

            for artifact_type, count in artifact_counts.items():
                fallback.append(f"\n**{artifact_type}**: {count} found")

            fallback.append("\n\nPlease ensure:")
            fallback.append("1. Ollama is running (http://localhost:11434)")
            fallback.append("2. Weaviate has indexed backend artifacts")

            return "\n".join(fallback)

    def _extract_citations(self, artifacts: List[Dict[str, Any]]) -> List[Citation]:
        """
        Extract citations from backend artifacts.

        Args:
            artifacts: Backend artifacts

        Returns:
            List of citations
        """
        citations = []

        for artifact in artifacts[:10]:  # Limit to 10 citations
            # Get ID from _additional if present (Weaviate format)
            artifact_id = artifact.get("_additional", {}).get("id", artifact.get("id", ""))

            # Get distance/confidence from _additional
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
        Generate follow-up questions based on backend analysis.

        Args:
            query: Original query
            artifacts: Backend artifacts

        Returns:
            List of suggested questions
        """
        suggestions = []

        # Analyze what artifacts were found
        artifact_types = set(a.get("artifactType", "") for a in artifacts[:10])

        # Add context-specific suggestions
        if "BackendDoc" in artifact_types:
            suggestions.append("What are the transaction boundaries in this service?")
            suggestions.append("What validation logic exists in this service layer?")

        if "GwtEndpoint" in artifact_types:
            suggestions.append("How does this RPC servlet handle errors?")
            suggestions.append("What DTOs are used in this endpoint?")

        if "DaoCall" in artifact_types:
            suggestions.append("Show me the DAO methods called by this service")
            suggestions.append("What database operations does this perform?")

        # Add generic backend questions
        if len(suggestions) < 3:
            suggestions.extend([
                "How is dependency injection configured in this service?",
                "What design patterns are used in this backend code?",
                "Explain the service-to-database flow"
            ])

        return suggestions[:4]  # Limit to 4 suggestions


# Global instance (singleton pattern)
_backend_specialist_agent: Optional[BackendSpecialistAgent] = None


def get_backend_specialist_agent(config: Optional[AgentConfig] = None) -> BackendSpecialistAgent:
    """
    Get global Backend Specialist agent instance.

    Args:
        config: Optional agent configuration

    Returns:
        BackendSpecialistAgent singleton
    """
    global _backend_specialist_agent

    if _backend_specialist_agent is None:
        _backend_specialist_agent = BackendSpecialistAgent(config)
        logger.info("Created global Backend Specialist agent instance")

    return _backend_specialist_agent


__all__ = [
    "BackendSpecialistAgent",
    "get_backend_specialist_agent"
]
