"""
Frontend Specialist Agent for UI/UX and client-side code analysis.

This agent specializes in:
- GWT application architecture
- JSP form analysis
- JavaScript/client-side code
- UI component patterns
- Frontend-backend integration
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


class FrontendSpecialistAgent:
    """
    Frontend Specialist Agent for UI/UX analysis.

    Specializes in:
    - GWT Presenter-View patterns (MVP architecture)
    - GWT UiBinder templates
    - JSP forms and UI components
    - JavaScript client-side logic
    - Frontend-backend RPC integration
    - UI navigation flows
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        """Initialize Frontend Specialist agent."""
        if config is None:
            config = get_agent_config(AgentRole.FRONTEND_SPECIALIST)

        self.config = config
        self.role = AgentRole.FRONTEND_SPECIALIST

        logger.info(f"Initialized Frontend Specialist agent")

    def execute_query(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """
        Execute query with Frontend Specialist agent.

        Args:
            query: User question about frontend/UI
            context: Optional context from previous interactions

        Returns:
            AgentResponse with frontend analysis
        """
        start_time = datetime.now()

        try:
            logger.info(f"Frontend Specialist processing: {query[:50]}...")

            # Step 1: Search for frontend artifacts
            frontend_artifacts = self._search_frontend_artifacts(query)

            # Step 2: Generate frontend analysis using LLM
            analysis = self._generate_frontend_analysis(
                query, frontend_artifacts, context
            )

            # Step 3: Extract citations
            citations = self._extract_citations(frontend_artifacts)

            # Step 4: Generate follow-up questions
            suggested_questions = self._generate_follow_ups(query, frontend_artifacts)

            duration = (datetime.now() - start_time).total_seconds()

            return AgentResponse(
                agent_role=self.role,
                query=query,
                timestamp=start_time.isoformat(),
                duration_seconds=duration,
                response_text=analysis,
                citations=citations,
                confidence=0.83,
                suggested_questions=suggested_questions,
                tools_used=["WeaviateSearchTool", "LLMQueryTool", "GwtAnalyzer"]
            )

        except Exception as e:
            logger.error(f"Frontend Specialist query failed: {e}", exc_info=True)
            duration = (datetime.now() - start_time).total_seconds()

            return AgentResponse(
                agent_role=self.role,
                query=query,
                timestamp=start_time.isoformat(),
                duration_seconds=duration,
                response_text="",
                error=str(e)
            )

    def _search_frontend_artifacts(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for frontend-related artifacts.

        Searches for:
        - GwtPresenter artifacts
        - GwtView artifacts
        - GwtUiBinder templates
        - JspForm artifacts
        - JsArtifact (JavaScript files)

        Args:
            query: Search query

        Returns:
            List of frontend artifacts

        Raises:
            Exception: If search fails (propagates to execute_query)
        """
        logger.debug(f"Searching frontend artifacts for: {query}")

        # Use SearchService to query Weaviate with frontend-specific filters
        from codeindex.web.services.search_service import get_search_service
        search_service = get_search_service()

        # Search with frontend-related artifact types
        search_response = search_service.search(
            query=query,
            filters={
                "artifact_types": ["GwtPresenter", "GwtView", "GwtUiBinder", "JspForm", "JsArtifact"]
            },
            limit=15  # Get more results for comprehensive frontend analysis
        )

        artifacts = search_response.get("results", [])
        logger.info(f"Found {len(artifacts)} frontend artifacts")

        return artifacts

    def _generate_frontend_analysis(
        self,
        query: str,
        artifacts: List[Dict[str, Any]],
        context: Optional[Dict[str, Any]]
    ) -> str:
        """
        Generate frontend analysis using LLM.

        Args:
            query: User query
            artifacts: Frontend artifacts
            context: Optional context

        Returns:
            Analysis text
        """
        try:
            logger.debug("Generating frontend analysis with Ollama LLM")

            # Import Ollama client
            from codeindex.services.ollama_client import OllamaClient

            # Build context from frontend artifacts
            context_parts = []

            # Add artifact summaries grouped by type
            if artifacts:
                # Group artifacts by type
                presenters = [a for a in artifacts if a.get("artifactType") == "GwtPresenter"]
                views = [a for a in artifacts if a.get("artifactType") == "GwtView"]
                ui_binders = [a for a in artifacts if a.get("artifactType") == "GwtUiBinder"]
                jsp_forms = [a for a in artifacts if a.get("artifactType") == "JspForm"]
                js_artifacts = [a for a in artifacts if a.get("artifactType") == "JsArtifact"]

                # Add GWT Presenters section
                if presenters:
                    context_parts.append("## GWT Presenters:\n")
                    for i, artifact in enumerate(presenters[:5], 1):
                        file_path = artifact.get("relativePath") or artifact.get("fileName", "Unknown")
                        summary = artifact.get("summary", "")
                        entities = artifact.get("entities", [])

                        context_parts.append(f"{i}. `{file_path}`")
                        if entities:
                            context_parts.append(f"   Entities: {', '.join(entities[:5])}")
                        if summary:
                            context_parts.append(f"   {summary}")
                        context_parts.append("")

                # Add GWT Views section
                if views:
                    context_parts.append("\n## GWT Views:\n")
                    for i, artifact in enumerate(views[:5], 1):
                        file_path = artifact.get("relativePath") or artifact.get("fileName", "Unknown")
                        summary = artifact.get("summary", "")

                        context_parts.append(f"{i}. `{file_path}`")
                        if summary:
                            context_parts.append(f"   {summary}")
                        context_parts.append("")

                # Add UiBinder templates section
                if ui_binders:
                    context_parts.append("\n## UiBinder Templates:\n")
                    for i, artifact in enumerate(ui_binders[:5], 1):
                        file_path = artifact.get("relativePath") or artifact.get("fileName", "Unknown")
                        context_parts.append(f"{i}. `{file_path}`")

                # Add JSP Forms section
                if jsp_forms:
                    context_parts.append("\n## JSP Forms:\n")
                    for i, artifact in enumerate(jsp_forms[:3], 1):
                        file_path = artifact.get("relativePath") or artifact.get("fileName", "Unknown")
                        summary = artifact.get("summary", "")

                        context_parts.append(f"{i}. `{file_path}`")
                        if summary:
                            context_parts.append(f"   {summary}")

                # Add JavaScript artifacts section
                if js_artifacts:
                    context_parts.append("\n## JavaScript Files:\n")
                    for i, artifact in enumerate(js_artifacts[:3], 1):
                        file_path = artifact.get("relativePath") or artifact.get("fileName", "Unknown")
                        context_parts.append(f"{i}. `{file_path}`")

            context_text = "\n".join(context_parts) if context_parts else "No frontend artifacts found."

            # Create system prompt
            system_prompt = """You are a Frontend Specialist with expertise in GWT, JSP, and JavaScript.
Analyze the provided UI artifacts and answer the user's question with:

1. Clear explanations of UI components and patterns
2. GWT MVP (Model-View-Presenter) architecture insights
3. Widget hierarchies and UiBinder template structures
4. Form validation and user interaction flows
5. Navigation patterns and RPC integration
6. Specific references to presenters, views, and UI components

Keep responses focused on frontend/UI aspects and user experience."""

            # Create user prompt
            user_prompt = f"""Question: {query}

{context_text}

Please analyze the frontend artifacts and provide a comprehensive answer focused on UI components, user flows, and MVP patterns."""

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
                analysis = "Unable to generate frontend analysis. Please try rephrasing your question."

            logger.info(f"Generated frontend analysis ({len(analysis)} chars)")
            return analysis.strip()

        except Exception as e:
            logger.error(f"Failed to generate frontend analysis: {e}")

            # Fallback response with structured info
            fallback = [
                f"I encountered an error while analyzing the frontend: {str(e)}\n",
                f"However, I found {len(artifacts)} frontend artifacts:\n"
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
            fallback.append("2. Weaviate has indexed frontend artifacts")

            return "\n".join(fallback)

    def _extract_citations(self, artifacts: List[Dict[str, Any]]) -> List[Citation]:
        """
        Extract citations from frontend artifacts.

        Args:
            artifacts: Frontend artifacts

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
        Generate follow-up questions based on frontend analysis.

        Args:
            query: Original query
            artifacts: Frontend artifacts

        Returns:
            List of suggested questions
        """
        suggestions = []

        # Analyze what artifacts were found
        artifact_types = set(a.get("artifactType", "") for a in artifacts[:10])

        # Add context-specific suggestions
        if "GwtPresenter" in artifact_types:
            suggestions.append("What event handlers are defined in this presenter?")
            suggestions.append("What RPC services does this presenter call?")

        if "GwtView" in artifact_types or "GwtUiBinder" in artifact_types:
            suggestions.append("How does this view bind to the presenter?")
            suggestions.append("What UI fields are defined in the UiBinder template?")

        if "JspForm" in artifact_types:
            suggestions.append("What form validation is implemented in this JSP?")

        # Add generic frontend questions
        if len(suggestions) < 3:
            suggestions.extend([
                "Show me the navigation flow for this UI component",
                "How does this frontend integrate with the backend?",
                "What widgets are used in this UI?"
            ])

        return suggestions[:4]  # Limit to 4 suggestions


# Global instance (singleton pattern)
_frontend_specialist_agent: Optional[FrontendSpecialistAgent] = None


def get_frontend_specialist_agent(config: Optional[AgentConfig] = None) -> FrontendSpecialistAgent:
    """
    Get global Frontend Specialist agent instance.

    Args:
        config: Optional agent configuration

    Returns:
        FrontendSpecialistAgent singleton
    """
    global _frontend_specialist_agent

    if _frontend_specialist_agent is None:
        _frontend_specialist_agent = FrontendSpecialistAgent(config)
        logger.info("Created global Frontend Specialist agent instance")

    return _frontend_specialist_agent


__all__ = [
    "FrontendSpecialistAgent",
    "get_frontend_specialist_agent"
]
