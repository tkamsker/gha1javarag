"""
Senior Developer Agent implementation (T060 - US2.1).

This agent specializes in explaining code architecture, design patterns,
and best practices. It uses the agent tools framework (WeaviateSearchTool,
FileReadTool, LLMQueryTool) to provide comprehensive code explanations.
"""

import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

from codeindex.web.agents.base import (
    AgentRole,
    AgentConfig,
    AgentResponse,
    Citation,
    get_agent_config,
    build_agent_prompt
)
from codeindex.web.agents.tools import (
    WeaviateSearchTool,
    FileReadTool,
    LLMQueryTool
)

logger = logging.getLogger(__name__)


class SeniorDeveloperAgent:
    """
    Senior Developer Agent for code architecture explanations.

    This agent:
    - Searches the codebase using Weaviate
    - Reads relevant source files
    - Explains architecture and design patterns
    - Provides best practice recommendations
    - Generates citations for all references
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        """
        Initialize Senior Developer agent.

        Args:
            config: Optional agent configuration (uses default if not provided)
        """
        if config is None:
            config = get_agent_config(AgentRole.SENIOR_DEVELOPER)

        self.config = config
        self.role = AgentRole.SENIOR_DEVELOPER

        # Initialize tools
        self.search_tool = WeaviateSearchTool()
        self.file_tool = FileReadTool()
        self.llm_tool = LLMQueryTool()

        logger.info("Initialized Senior Developer agent with tools")

    def execute_query(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """
        Execute query with Senior Developer agent.

        Args:
            query: User query string
            context: Optional context dictionary

        Returns:
            AgentResponse with explanation and citations
        """
        start_time = datetime.now()

        try:
            logger.info(f"Senior Developer processing: {query[:50]}...")

            # Step 1: Search Weaviate for relevant artifacts
            search_results = self._search_codebase(query)

            # Step 2: Read relevant source files
            file_contents = self._read_source_files(search_results)

            # Step 3: Generate explanation using LLM
            explanation = self._generate_explanation(
                query,
                search_results,
                file_contents,
                context
            )

            # Step 4: Extract citations
            citations = self._extract_citations(search_results)

            # Step 5: Generate follow-up questions
            suggested_questions = self._generate_follow_ups(query, search_results)

            # Calculate duration
            duration = (datetime.now() - start_time).total_seconds()

            return AgentResponse(
                agent_role=self.role,
                query=query,
                timestamp=start_time.isoformat(),
                duration_seconds=duration,
                response_text=explanation,
                citations=citations,
                confidence=0.85,  # Placeholder - would be calculated from LLM
                suggested_questions=suggested_questions,
                tools_used=["WeaviateSearchTool", "FileReadTool", "LLMQueryTool"]
            )

        except Exception as e:
            logger.error(f"Senior Developer query failed: {e}", exc_info=True)

            duration = (datetime.now() - start_time).total_seconds()

            return AgentResponse(
                agent_role=self.role,
                query=query,
                timestamp=start_time.isoformat(),
                duration_seconds=duration,
                response_text="",
                error=str(e)
            )

    def _search_codebase(self, query: str) -> List[Dict[str, Any]]:
        """
        Search Weaviate for relevant artifacts using WeaviateSearchTool.

        Args:
            query: Search query

        Returns:
            List of search results
        """
        try:
            logger.debug(f"Searching codebase for: {query}")

            # Use WeaviateSearchTool to query Weaviate
            artifacts = self.search_tool.search(
                query=query,
                limit=15  # Get comprehensive results
            )

            logger.info(f"Found {len(artifacts)} artifacts for query")
            return artifacts

        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def _read_source_files(self, search_results: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        Read source files for relevant artifacts using FileReadTool.

        Args:
            search_results: Search results from Weaviate

        Returns:
            Dictionary mapping file paths to file contents
        """
        file_contents = {}

        logger.debug(f"Reading {len(search_results)} source files")

        for result in search_results[:5]:  # Limit to top 5 files to avoid context overflow
            try:
                # Get relative path from result
                relative_path = result.get("relativePath") or result.get("fileName", "")
                if not relative_path:
                    continue

                # Use FileReadTool to read file with security validation
                content = self.file_tool.read_file(relative_path)

                # Truncate to first 5000 lines if needed
                lines = content.split('\n')
                if len(lines) > 5000:
                    content = '\n'.join(lines[:5000])
                    logger.debug(f"Truncated {relative_path} to 5000 lines")

                file_contents[str(relative_path)] = content
                logger.debug(f"Read {len(lines)} lines from {relative_path}")

            except FileNotFoundError:
                logger.warning(f"File not found: {relative_path}")
                continue
            except ValueError as e:
                logger.warning(f"Invalid file path {relative_path}: {e}")
                continue
            except Exception as e:
                logger.warning(f"Failed to read file {relative_path}: {e}")
                continue

        return file_contents

    def _generate_explanation(
        self,
        query: str,
        search_results: List[Dict[str, Any]],
        file_contents: Dict[str, str],
        context: Optional[Dict[str, Any]]
    ) -> str:
        """
        Generate explanation using LLMQueryTool.

        Args:
            query: User query
            search_results: Search results
            file_contents: Source file contents
            context: Optional context

        Returns:
            Explanation text
        """
        try:
            logger.debug("Generating explanation with LLM")

            # Build context from search results and file contents
            context_parts = []

            # Add artifact summaries from search results
            if search_results:
                context_parts.append("## Relevant Artifacts Found:\n")
                for i, result in enumerate(search_results[:5], 1):
                    artifact_type = result.get("artifactType", "Unknown")
                    file_path = result.get("relativePath") or result.get("fileName", "Unknown")
                    summary = result.get("summary", "No summary available")

                    context_parts.append(f"{i}. **{artifact_type}** - `{file_path}`")
                    context_parts.append(f"   {summary}\n")

            # Add file content snippets
            if file_contents:
                context_parts.append("\n## Source Code Context:\n")
                for file_path, content in list(file_contents.items())[:3]:  # Max 3 files
                    # Truncate content to first 1000 characters
                    content_preview = content[:1000] + ("..." if len(content) > 1000 else "")
                    context_parts.append(f"### {file_path}\n```\n{content_preview}\n```\n")

            context_text = "\n".join(context_parts) if context_parts else "No specific code artifacts found."

            # Create system prompt with verbosity level from config
            system_prompt = build_agent_prompt(
                self.config,
                base_prompt="""You are a Senior Software Developer with expertise in Java enterprise applications,
GWT, and modern web architectures. Analyze the provided code artifacts and answer the user's question with:

1. Clear, concise explanations
2. Specific references to code components
3. Best practices and design patterns
4. Potential improvements when relevant

Keep responses focused and practical."""
            )

            # Create formatted query
            formatted_query = f"""Question: {query}

Please analyze the artifacts and provide a comprehensive answer to the question."""

            # Use LLMQueryTool to generate response
            explanation = self.llm_tool.query(
                prompt=formatted_query,
                context=context_text,
                system_prompt=system_prompt,
                model=self.config.llm_model,
                max_retries=3,
                enable_cache=True
            )

            if not explanation:
                explanation = "Unable to generate explanation. Please try rephrasing your question."

            logger.info(f"Generated explanation ({len(explanation)} chars)")
            return explanation.strip()

        except Exception as e:
            logger.error(f"Failed to generate explanation: {e}")

            # Fallback response
            return f"""I encountered an error while generating an explanation: {str(e)}

However, I found {len(search_results)} relevant artifacts in the codebase:

{self._format_search_results_fallback(search_results)}

Please ensure:
1. Ollama is running (http://localhost:11434)
2. Weaviate has indexed artifacts
3. The model 'gemma3:12b' is available"""

    def _extract_citations(self, search_results: List[Dict[str, Any]]) -> List[Citation]:
        """
        Extract citations from search results.

        Args:
            search_results: Search results

        Returns:
            List of Citation objects
        """
        citations = []

        for result in search_results[:5]:  # Limit to 5 citations
            # Get ID from _additional if present (Weaviate format)
            artifact_id = result.get("_additional", {}).get("id", result.get("id", ""))

            # Get distance/confidence from _additional
            distance = result.get("_additional", {}).get("distance", 0.0)
            confidence = 1.0 - distance if distance < 1.0 else 0.5  # Convert distance to confidence

            citation = Citation(
                artifact_id=artifact_id,
                file_path=result.get("relativePath") or result.get("fileName", "Unknown"),
                artifact_type=result.get("artifactType", "Unknown"),
                confidence=confidence
            )
            citations.append(citation)

        return citations

    def _format_search_results_fallback(self, search_results: List[Dict[str, Any]]) -> str:
        """
        Format search results as fallback text when LLM fails.

        Args:
            search_results: Search results from Weaviate

        Returns:
            Formatted text listing artifacts
        """
        if not search_results:
            return "No artifacts found in the codebase."

        lines = []
        for i, result in enumerate(search_results[:5], 1):
            artifact_type = result.get("artifactType", "Unknown")
            file_path = result.get("relativePath") or result.get("fileName", "Unknown")
            summary = result.get("summary", "")

            lines.append(f"{i}. **{artifact_type}**: `{file_path}`")
            if summary:
                lines.append(f"   {summary}")

        return "\n".join(lines)

    def _generate_follow_ups(
        self,
        query: str,
        search_results: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Generate suggested follow-up questions based on search results.

        Args:
            query: Original query
            search_results: Search results

        Returns:
            List of suggested questions
        """
        suggestions = []

        # Generic follow-ups
        suggestions.append("Can you explain the implementation details?")

        # Add artifact-specific suggestions based on what was found
        if search_results:
            artifact_types = set(r.get("artifactType", "") for r in search_results[:3])

            if "GwtPresenter" in artifact_types:
                suggestions.append("How does this presenter handle user interactions?")
            if "BackendDoc" in artifact_types or "DaoCall" in artifact_types:
                suggestions.append("What database operations does this use?")
            if "DtoArtifact" in artifact_types:
                suggestions.append("What validation rules are applied to this data?")

        # Always include these
        if len(suggestions) < 3:
            suggestions.extend([
                "What are the dependencies for this component?",
                "How does this integrate with other modules?"
            ])

        return suggestions[:4]  # Limit to 4 suggestions


# Global agent instance
_senior_developer_agent: Optional[SeniorDeveloperAgent] = None


def get_senior_developer_agent(config: Optional[AgentConfig] = None) -> SeniorDeveloperAgent:
    """
    Get global Senior Developer agent instance.

    Args:
        config: Optional agent configuration

    Returns:
        SeniorDeveloperAgent singleton
    """
    global _senior_developer_agent

    if _senior_developer_agent is None:
        _senior_developer_agent = SeniorDeveloperAgent(config)
        logger.info("Initialized Senior Developer agent")

    return _senior_developer_agent


__all__ = [
    "SeniorDeveloperAgent",
    "get_senior_developer_agent"
]
