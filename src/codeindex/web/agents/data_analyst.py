"""
Data Analyst Agent for database schema and data flow analysis.

This agent specializes in:
- Database schema understanding
- Data flow analysis
- DAO/iBATIS statement analysis
- Table relationship discovery
- Data transformation pipelines
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


class DataAnalystAgent:
    """
    Data Analyst Agent for database schema and data flow analysis.

    Specializes in:
    - Database schema understanding (tables, columns, relationships)
    - DAO call patterns and database access
    - iBATIS/MyBatis statement analysis
    - Foreign key relationships
    - Data transformation and ETL flows
    - Query optimization insights
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        """Initialize Data Analyst agent."""
        if config is None:
            config = get_agent_config(AgentRole.DATA_ANALYST)

        self.config = config
        self.role = AgentRole.DATA_ANALYST

        logger.info(f"Initialized Data Analyst agent")

    def execute_query(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """
        Execute query with Data Analyst agent.

        Args:
            query: User question about database schema or data flow
            context: Optional context from previous interactions

        Returns:
            AgentResponse with database analysis
        """
        start_time = datetime.now()

        try:
            logger.info(f"Data Analyst processing: {query[:50]}...")

            # Step 1: Search for relevant database artifacts
            db_artifacts = self._search_database_artifacts(query)

            # Step 2: Analyze DAO calls and iBATIS statements
            dao_analysis = self._analyze_dao_patterns(db_artifacts)

            # Step 3: Extract table schemas and relationships
            schema_info = self._extract_schema_info(db_artifacts)

            # Step 4: Generate data flow explanation
            analysis = self._generate_data_analysis(
                query, db_artifacts, dao_analysis, schema_info, context
            )

            # Step 5: Extract citations from database artifacts
            citations = self._extract_citations(db_artifacts)

            # Step 6: Generate follow-up questions
            suggested_questions = self._generate_follow_ups(query, db_artifacts)

            duration = (datetime.now() - start_time).total_seconds()

            return AgentResponse(
                agent_role=self.role,
                query=query,
                timestamp=start_time.isoformat(),
                duration_seconds=duration,
                response_text=analysis,
                citations=citations,
                confidence=0.82,
                suggested_questions=suggested_questions,
                tools_used=["WeaviateSearchTool", "DbSchemaAnalyzer", "DaoPatternAnalyzer"]
            )

        except Exception as e:
            logger.error(f"Data Analyst query failed: {e}", exc_info=True)
            duration = (datetime.now() - start_time).total_seconds()

            return AgentResponse(
                agent_role=self.role,
                query=query,
                timestamp=start_time.isoformat(),
                duration_seconds=duration,
                response_text="",
                error=str(e)
            )

    def _search_database_artifacts(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for database-related artifacts.

        Searches for:
        - DbTable artifacts
        - DaoCall artifacts
        - IbatisStatement artifacts
        - DtoArtifact with database relationships

        Args:
            query: Search query

        Returns:
            List of database artifacts
        """
        try:
            logger.debug(f"Searching database artifacts for: {query}")

            # Use SearchService to query Weaviate with database-specific filters
            from codeindex.web.services.search_service import get_search_service
            search_service = get_search_service()

            # Search with database-related artifact types
            search_response = search_service.search(
                query=query,
                filters={
                    "artifact_types": ["DbTable", "DaoCall", "IbatisStatement", "DtoArtifact"]
                },
                limit=15  # Get more results for comprehensive database analysis
            )

            artifacts = search_response.get("results", [])
            logger.info(f"Found {len(artifacts)} database artifacts")

            return artifacts

        except Exception as e:
            logger.error(f"Database artifact search failed: {e}")
            return []

    def _analyze_dao_patterns(self, artifacts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze DAO call patterns and data access.

        Args:
            artifacts: Database artifacts

        Returns:
            DAO pattern analysis
        """
        logger.debug("Analyzing DAO patterns")

        # Filter by artifact type (Weaviate uses "artifactType" field)
        dao_calls = [a for a in artifacts if a.get("artifactType") == "DaoCall"]
        ibatis_stmts = [a for a in artifacts if a.get("artifactType") == "IbatisStatement"]

        # Extract method names from entities field
        dao_methods = []
        for dao in dao_calls:
            entities = dao.get("entities", [])
            dao_methods.extend(entities)

        return {
            "dao_count": len(dao_calls),
            "ibatis_count": len(ibatis_stmts),
            "dao_methods": dao_methods[:10],  # Sample of methods
            "patterns": ["CRUD", "Repository Pattern", "DAO Pattern"]
        }

    def _extract_schema_info(self, artifacts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extract database schema information.

        Args:
            artifacts: Database artifacts

        Returns:
            Schema information
        """
        logger.debug("Extracting schema information")

        # Filter by artifact type (Weaviate uses "artifactType" field)
        tables = [a for a in artifacts if a.get("artifactType") == "DbTable"]
        dtos = [a for a in artifacts if a.get("artifactType") == "DtoArtifact"]

        # Extract table names from entities field
        table_names = []
        for table in tables:
            entities = table.get("entities", [])
            table_names.extend(entities)

        # Extract DTO names
        dto_names = []
        for dto in dtos:
            entities = dto.get("entities", [])
            dto_names.extend(entities)

        return {
            "table_count": len(tables),
            "tables": table_names[:20],  # Sample of tables
            "dto_count": len(dtos),
            "dtos": dto_names[:10],  # Sample of DTOs
            "relationships": []  # Would be extracted from foreign keys in real artifacts
        }

    def _generate_data_analysis(
        self,
        query: str,
        artifacts: List[Dict[str, Any]],
        dao_analysis: Dict[str, Any],
        schema_info: Dict[str, Any],
        context: Optional[Dict[str, Any]]
    ) -> str:
        """
        Generate data flow analysis using LLM.

        Args:
            query: User query
            artifacts: Database artifacts
            dao_analysis: DAO pattern analysis
            schema_info: Schema information
            context: Optional context

        Returns:
            Analysis text
        """
        try:
            logger.debug("Generating data analysis with Ollama LLM")

            # Import Ollama client
            from codeindex.services.ollama_client import OllamaClient

            # Build context from database artifacts
            context_parts = []

            # Add schema summary
            if schema_info["table_count"] > 0:
                context_parts.append("## Database Schema:\n")
                context_parts.append(f"**Tables ({schema_info['table_count']}):**")
                context_parts.append(", ".join(schema_info["tables"][:20]))
                if schema_info["dto_count"] > 0:
                    context_parts.append(f"\n**DTOs ({schema_info['dto_count']}):**")
                    context_parts.append(", ".join(schema_info["dtos"][:10]))
                context_parts.append("\n")

            # Add DAO analysis
            if dao_analysis["dao_count"] > 0:
                context_parts.append("\n## Data Access Layer:\n")
                context_parts.append(f"**DAO Methods ({dao_analysis['dao_count']}):**")
                if dao_analysis["dao_methods"]:
                    context_parts.append(", ".join(dao_analysis["dao_methods"][:10]))
                context_parts.append(f"\n**iBATIS Statements:** {dao_analysis['ibatis_count']}")
                context_parts.append(f"\n**Patterns:** {', '.join(dao_analysis['patterns'])}")
                context_parts.append("\n")

            # Add artifact details
            if artifacts:
                context_parts.append("\n## Relevant Artifacts:\n")
                for i, artifact in enumerate(artifacts[:5], 1):
                    artifact_type = artifact.get("artifactType", "Unknown")
                    file_path = artifact.get("relativePath") or artifact.get("fileName", "Unknown")
                    summary = artifact.get("summary", "")

                    context_parts.append(f"{i}. **{artifact_type}** - `{file_path}`")
                    if summary:
                        context_parts.append(f"   {summary}")

            context_text = "\n".join(context_parts) if context_parts else "No database artifacts found."

            # Create system prompt
            system_prompt = """You are a Data Analyst with expertise in database design, data modeling,
and data access patterns. Analyze the provided database artifacts and answer the user's question with:

1. Clear database schema explanations
2. Data flow and entity relationships
3. DAO/iBATIS usage patterns
4. Potential data quality or performance insights
5. Specific references to tables and methods

Keep responses focused on data and database aspects."""

            # Create user prompt
            user_prompt = f"""Question: {query}

{context_text}

Please analyze the database structure and data access patterns, then provide a comprehensive answer."""

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
                analysis = "Unable to generate database analysis. Please try rephrasing your question."

            logger.info(f"Generated data analysis ({len(analysis)} chars)")
            return analysis.strip()

        except Exception as e:
            logger.error(f"Failed to generate data analysis: {e}")

            # Fallback response with structured info
            fallback = [
                f"I encountered an error while analyzing the database: {str(e)}\n",
                f"However, I found {len(artifacts)} database artifacts:\n"
            ]

            if schema_info["table_count"] > 0:
                fallback.append(f"\n**Database Tables ({schema_info['table_count']}):**")
                fallback.append(", ".join(schema_info["tables"][:10]))

            if dao_analysis["dao_count"] > 0:
                fallback.append(f"\n\n**DAO Methods ({dao_analysis['dao_count']}):**")
                if dao_analysis["dao_methods"]:
                    fallback.append(", ".join(dao_analysis["dao_methods"][:5]))

            fallback.append("\n\nPlease ensure:")
            fallback.append("1. Ollama is running (http://localhost:11434)")
            fallback.append("2. Weaviate has indexed database artifacts")

            return "\n".join(fallback)

    def _extract_citations(self, artifacts: List[Dict[str, Any]]) -> List[Citation]:
        """
        Extract citations from database artifacts.

        Args:
            artifacts: Database artifacts

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
        Generate follow-up questions based on database analysis.

        Args:
            query: Original query
            artifacts: Database artifacts

        Returns:
            List of suggested questions
        """
        suggestions = []

        # Analyze what artifacts were found
        artifact_types = set(a.get("artifactType", "") for a in artifacts[:10])

        # Add context-specific suggestions
        if "DbTable" in artifact_types:
            suggestions.append("What are the foreign key relationships in this schema?")

        if "DaoCall" in artifact_types:
            suggestions.append("Show me the DAO methods that access this table")

        if "IbatisStatement" in artifact_types:
            suggestions.append("Explain the iBATIS queries for this entity")

        if "DtoArtifact" in artifact_types:
            suggestions.append("What validation rules are defined on these DTOs?")

        # Add generic database questions
        if len(suggestions) < 3:
            suggestions.extend([
                "Are there any N+1 query issues in this data access pattern?",
                "What indexes are defined on these tables?",
                "How is this data transformed between layers?"
            ])

        return suggestions[:4]  # Limit to 4 suggestions


# Global instance (singleton pattern)
_data_analyst_agent: Optional[DataAnalystAgent] = None


def get_data_analyst_agent(config: Optional[AgentConfig] = None) -> DataAnalystAgent:
    """
    Get global Data Analyst agent instance.

    Args:
        config: Optional agent configuration

    Returns:
        DataAnalystAgent singleton
    """
    global _data_analyst_agent

    if _data_analyst_agent is None:
        _data_analyst_agent = DataAnalystAgent(config)
        logger.info("Created global Data Analyst agent instance")

    return _data_analyst_agent


__all__ = [
    "DataAnalystAgent",
    "get_data_analyst_agent"
]
