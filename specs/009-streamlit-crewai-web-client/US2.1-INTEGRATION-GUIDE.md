# US2.1 Integration Guide - Agent Implementation Pattern

## Overview

This guide documents the integration pattern established in US2.1 (Senior Developer Agent) for implementing new AI agents in the system. Follow this pattern for US2.2 (Data Analyst), US2.3 (Multi-Agent PRD), and other agent types.

## Architecture Components

### 1. Agent Tools Framework (`src/codeindex/web/agents/tools.py`)

**Purpose**: Reusable tools for agent execution

**Available Tools**:
- `WeaviateSearchTool`: Semantic search over indexed artifacts
- `FileReadTool`: Secure file reading with security validation
- `LLMQueryTool`: Ollama LLM queries with retry logic

**Key Features**:
- Tool registry pattern (`@register_tool` decorator)
- Retry logic with exponential backoff (3 attempts, 0.5s backoff factor)
- Result caching (5-minute TTL)
- Security validation (directory traversal prevention, file size limits)
- Error handling for transient failures (ConnectionError, TimeoutError)

**Usage Example**:
```python
from codeindex.web.agents.tools import WeaviateSearchTool, FileReadTool, LLMQueryTool

# In your agent __init__:
self.search_tool = WeaviateSearchTool()
self.file_tool = FileReadTool()
self.llm_tool = LLMQueryTool()

# In your agent query execution:
artifacts = self.search_tool.search(query="database schema", limit=15)
file_content = self.file_tool.read_file("src/main/java/User.java")
response = self.llm_tool.query(prompt="Explain this code", context=file_content)
```

### 2. Agent Routing Service (`src/codeindex/web/services/agent_routing.py`)

**Purpose**: Route queries to appropriate agents based on keywords and context

**Features**:
- Keyword-based routing with confidence scoring
- Context-aware routing for follow-up questions
- Conversation history tracking
- Fallback to Senior Developer for ambiguous queries
- Custom routing rules

**Routing Rules** (extend for new agents):
```python
DEFAULT_ROUTING_RULES = {
    AgentRole.DATA_ANALYST: [
        "database", "schema", "table", "sql", "query", "foreign key",
        "dao", "entity", "relationship", "erd"
    ],
    AgentRole.FRONTEND_SPECIALIST: [
        "ui", "interface", "form", "gwt", "presenter", "view", "widget"
    ],
    # Add new agent rules here
}
```

**Usage**:
```python
from codeindex.web.services.agent_routing import get_agent_routing_service

routing_service = get_agent_routing_service()
agent_role, confidence = routing_service.route_query_with_confidence(
    query="What database tables store user data?",
    context={"previous_agent": AgentRole.DATA_ANALYST}
)
```

### 3. Agent Chat Component (`src/codeindex/web/components/agent_chat.py`)

**Purpose**: Response formatting, citation validation, and UI helpers

**Key Functions**:
- `extract_citations_from_text(response_text)`: Extract artifact references from response
- `validate_citations(citations, weaviate_store)`: Verify citations against Weaviate (FR4.11)
- `format_response_with_hyperlinks(response, weaviate_store)`: Add hyperlinks for verified citations
- `format_response_for_streaming(response_text, chunk_size)`: Split response for word-by-word display
- `render_markdown_to_html(markdown_text, sanitize)`: Convert markdown with XSS protection
- `extract_plain_text(text)`: Extract plain text for copy functionality

**Citation Patterns Supported**:
1. `artifact:id` or `ArtifactType:id` (e.g., `DaoCall:user_dao_123`)
2. Backtick file paths (e.g., `` `src/User.java` ``)
3. Plain file paths (e.g., `src/services/UserService.java`)
4. File: prefix (e.g., `File: src/main/java/User.java`)
5. Markdown links (e.g., `[Component](src/Component.java)`)

### 4. Agent Base Classes (`src/codeindex/web/agents/base.py`)

**Purpose**: Shared agent configuration and response models

**Key Classes**:
- `AgentRole`: Enum of available agent types
- `AgentConfig`: Configuration (verbosity, technical_level, citation_style, llm_model)
- `AgentResponse`: Standard response format (role, query, response_text, citations, confidence, suggested_questions)
- `Citation`: Citation metadata (artifact_id, file_path, artifact_type, confidence)

**Agent Configuration**:
```python
from codeindex.web.agents.base import get_agent_config, AgentRole, AgentResponse, Citation

# Get configuration with defaults
config = get_agent_config(AgentRole.DATA_ANALYST)

# Override settings
config = get_agent_config(
    AgentRole.DATA_ANALYST,
    verbosity="verbose",
    technical_level="senior",
    citation_style="inline"
)
```

## Implementation Steps for New Agents

### Step 1: Create Agent Implementation

**File**: `src/codeindex/web/agents/<agent_name>.py`

**Template**:
```python
"""
<Agent Name> Agent implementation (T0XX - US2.X).

This agent specializes in <domain description>.
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


class <AgentName>Agent:
    """
    <Agent Name> Agent for <purpose>.

    This agent:
    - <Key feature 1>
    - <Key feature 2>
    - <Key feature 3>
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        """Initialize <Agent Name> agent."""
        if config is None:
            config = get_agent_config(AgentRole.<AGENT_ROLE>)

        self.config = config
        self.role = AgentRole.<AGENT_ROLE>

        # Initialize tools
        self.search_tool = WeaviateSearchTool()
        self.file_tool = FileReadTool()
        self.llm_tool = LLMQueryTool()

        logger.info("Initialized <Agent Name> agent with tools")

    def execute_query(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """
        Execute query with <Agent Name> agent.

        Args:
            query: User query string
            context: Optional context dictionary

        Returns:
            AgentResponse with analysis and citations
        """
        start_time = datetime.now()

        try:
            logger.info(f"<Agent Name> processing: {query[:50]}...")

            # Step 1: Search for relevant artifacts
            search_results = self._search_artifacts(query)

            # Step 2: Read relevant source files
            file_contents = self._read_source_files(search_results)

            # Step 3: Generate analysis using LLM
            analysis = self._generate_analysis(
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
                response_text=analysis,
                citations=citations,
                confidence=0.85,  # Adjust based on results
                suggested_questions=suggested_questions,
                tools_used=["WeaviateSearchTool", "FileReadTool", "LLMQueryTool"]
            )

        except Exception as e:
            logger.error(f"<Agent Name> query failed: {e}", exc_info=True)

            duration = (datetime.now() - start_time).total_seconds()

            return AgentResponse(
                agent_role=self.role,
                query=query,
                timestamp=start_time.isoformat(),
                duration_seconds=duration,
                response_text="",
                error=str(e)
            )

    def _search_artifacts(self, query: str) -> List[Dict[str, Any]]:
        """Search for relevant artifacts using WeaviateSearchTool."""
        try:
            # Customize search filters for agent domain
            artifacts = self.search_tool.search(
                query=query,
                artifact_types=["DbTable", "DaoCall"],  # Adjust for agent
                limit=15
            )
            return artifacts
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def _read_source_files(self, search_results: List[Dict[str, Any]]) -> Dict[str, str]:
        """Read source files for relevant artifacts using FileReadTool."""
        file_contents = {}
        for result in search_results[:5]:  # Limit to top 5 files
            try:
                relative_path = result.get("relativePath") or result.get("fileName", "")
                if not relative_path:
                    continue

                content = self.file_tool.read_file(relative_path)

                # Truncate if needed
                lines = content.split('\n')
                if len(lines) > 5000:
                    content = '\n'.join(lines[:5000])

                file_contents[str(relative_path)] = content

            except Exception as e:
                logger.warning(f"Failed to read file {relative_path}: {e}")
                continue

        return file_contents

    def _generate_analysis(
        self,
        query: str,
        search_results: List[Dict[str, Any]],
        file_contents: Dict[str, str],
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Generate analysis using LLMQueryTool."""
        try:
            # Build context from search results and file contents
            context_parts = []

            if search_results:
                context_parts.append("## Relevant Artifacts Found:\n")
                for i, result in enumerate(search_results[:5], 1):
                    artifact_type = result.get("artifactType", "Unknown")
                    file_path = result.get("relativePath") or result.get("fileName", "Unknown")
                    summary = result.get("summary", "No summary available")

                    context_parts.append(f"{i}. **{artifact_type}** - `{file_path}`")
                    context_parts.append(f"   {summary}\n")

            if file_contents:
                context_parts.append("\n## Source Code Context:\n")
                for file_path, content in list(file_contents.items())[:3]:
                    content_preview = content[:1000] + ("..." if len(content) > 1000 else "")
                    context_parts.append(f"### {file_path}\n```\n{content_preview}\n```\n")

            context_text = "\n".join(context_parts) if context_parts else "No specific artifacts found."

            # Create system prompt with agent-specific instructions
            system_prompt = build_agent_prompt(
                self.config,
                base_prompt="""You are a <domain> expert with expertise in <technologies>.
Analyze the provided artifacts and answer the user's question with:

1. Clear, concise explanations
2. Specific references to code components
3. Best practices and recommendations
4. Potential improvements when relevant

Keep responses focused and practical."""
            )

            # Use LLMQueryTool to generate response
            analysis = self.llm_tool.query(
                prompt=f"Question: {query}\n\nPlease analyze the artifacts and provide a comprehensive answer.",
                context=context_text,
                system_prompt=system_prompt,
                model=self.config.llm_model,
                max_retries=3,
                enable_cache=True
            )

            if not analysis:
                analysis = "Unable to generate analysis. Please try rephrasing your question."

            return analysis.strip()

        except Exception as e:
            logger.error(f"Failed to generate analysis: {e}")
            return f"Error generating analysis: {str(e)}"

    def _extract_citations(self, search_results: List[Dict[str, Any]]) -> List[Citation]:
        """Extract citations from search results."""
        citations = []

        for result in search_results[:5]:  # Limit to 5 citations
            artifact_id = result.get("_additional", {}).get("id", result.get("id", ""))
            distance = result.get("_additional", {}).get("distance", 0.0)
            confidence = 1.0 - distance if distance < 1.0 else 0.5

            citation = Citation(
                artifact_id=artifact_id,
                file_path=result.get("relativePath") or result.get("fileName", "Unknown"),
                artifact_type=result.get("artifactType", "Unknown"),
                confidence=confidence
            )
            citations.append(citation)

        return citations

    def _generate_follow_ups(
        self,
        query: str,
        search_results: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate suggested follow-up questions."""
        suggestions = []

        # Generic follow-ups
        suggestions.append("Can you explain the implementation details?")

        # Add domain-specific suggestions based on artifacts found
        if search_results:
            artifact_types = set(r.get("artifactType", "") for r in search_results[:3])

            # Customize based on agent domain
            if "DbTable" in artifact_types:
                suggestions.append("What are the foreign key relationships?")

        # Always include these
        if len(suggestions) < 3:
            suggestions.extend([
                "What are the dependencies for this component?",
                "How does this integrate with other modules?"
            ])

        return suggestions[:4]  # Limit to 4 suggestions


# Global agent instance
_<agent_name>_agent: Optional[<AgentName>Agent] = None


def get_<agent_name>_agent(config: Optional[AgentConfig] = None) -> <AgentName>Agent:
    """
    Get global <Agent Name> agent instance.

    Args:
        config: Optional agent configuration

    Returns:
        <AgentName>Agent singleton
    """
    global _<agent_name>_agent

    if _<agent_name>_agent is None:
        _<agent_name>_agent = <AgentName>Agent(config)
        logger.info("Initialized <Agent Name> agent")

    return _<agent_name>_agent


__all__ = [
    "<AgentName>Agent",
    "get_<agent_name>_agent"
]
```

### Step 2: Add Routing Rules

**File**: `src/codeindex/web/services/agent_routing.py`

Add keywords for your agent:

```python
DEFAULT_ROUTING_RULES = {
    # ... existing rules ...
    AgentRole.<AGENT_ROLE>: [
        "keyword1", "keyword2", "keyword3", ...
    ]
}
```

### Step 3: Integrate with Agent Service

**File**: `src/codeindex/web/services/agent_service.py`

Add agent execution case:

```python
def execute_query(self, query: str, agent_role: Optional[AgentRole] = None, agent_settings: Optional[Dict[str, Any]] = None) -> AgentResponse:
    # ... existing code ...

    elif agent_role == AgentRole.<AGENT_ROLE>:
        from codeindex.web.agents.<agent_name> import get_<agent_name>_agent
        agent = get_<agent_name>_agent(config)
        return agent.execute_query(query)
```

### Step 4: Create Tests (TDD Approach)

**File**: `tests/unit/web/agents/test_<agent_name>.py`

Follow the test structure from `test_senior_developer.py`:
1. Initialization tests (config, tools, role)
2. Query execution tests (basic, with context)
3. Search and file reading tests
4. LLM generation tests
5. Citation extraction tests
6. Error handling tests
7. Output formatting tests
8. Performance tests

**Example Test**:
```python
import pytest
from unittest.mock import Mock, patch
from codeindex.web.agents.<agent_name> import <AgentName>Agent, get_<agent_name>_agent
from codeindex.web.agents.base import AgentRole, AgentResponse, Citation

class Test<AgentName>AgentInitialization:
    def test_agent_initializes_with_default_config(self):
        agent = <AgentName>Agent()
        assert agent.role == AgentRole.<AGENT_ROLE>
        assert agent.search_tool is not None
        assert agent.file_tool is not None
        assert agent.llm_tool is not None

    # More tests...

class Test<AgentName>AgentQueryExecution:
    @patch('codeindex.web.agents.tools.WeaviateSearchTool.search')
    @patch('codeindex.web.agents.tools.FileReadTool.read_file')
    @patch('codeindex.web.agents.tools.LLMQueryTool.query')
    def test_execute_query_returns_agent_response(
        self, mock_llm_query, mock_file_read, mock_search
    ):
        # Setup mocks
        mock_search.return_value = [{"id": "artifact_123", "relativePath": "src/Foo.java"}]
        mock_file_read.return_value = "class Foo {}"
        mock_llm_query.return_value = "This is a Foo class"

        # Execute
        agent = <AgentName>Agent()
        response = agent.execute_query("What is Foo?")

        # Assert
        assert isinstance(response, AgentResponse)
        assert response.agent_role == AgentRole.<AGENT_ROLE>
        assert response.response_text == "This is a Foo class"
        assert len(response.citations) > 0

    # More tests...
```

### Step 5: UI Integration

The Chat page (`src/codeindex/web/pages/2_💬_Chat.py`) is already integrated with:
- Agent selection dropdown in sidebar
- Agent service execution
- Response display with citations
- Streaming effect
- Copy functionality
- Error handling

**No UI changes needed** - just add your agent to the AgentRole enum and routing rules.

## Testing Checklist

- [ ] Unit tests for agent initialization
- [ ] Unit tests for query execution
- [ ] Unit tests for artifact search
- [ ] Unit tests for file reading
- [ ] Unit tests for LLM generation
- [ ] Unit tests for citation extraction
- [ ] Unit tests for error handling
- [ ] Integration test with live Weaviate and Ollama
- [ ] UI test with agent selection
- [ ] Performance test (<30s response time)

## Best Practices

### Security
- Always use `FileReadTool` for file access (includes path validation)
- Sanitize user inputs before passing to LLM
- Validate citations against Weaviate (FR4.11)
- Use XSS protection in UI rendering

### Performance
- Limit artifact search results (recommended: 10-15)
- Limit file reads (recommended: 5 files max)
- Truncate file contents (recommended: 5000 lines max)
- Enable caching for repeated queries
- Use retry logic for transient failures

### Error Handling
- Return AgentResponse with error field instead of raising exceptions
- Log errors with context for debugging
- Provide fallback responses when LLM fails
- Handle Weaviate connection errors gracefully

### Citation Quality
- Extract citations from search results
- Include file paths and artifact types
- Calculate confidence scores (1.0 - distance)
- Limit to 5 citations per response
- Validate against Weaviate before displaying

### User Experience
- Generate suggested follow-up questions
- Display agent role and confidence in UI
- Show streaming effect for long responses
- Provide copy functionality for responses
- Handle conversation context for follow-ups

## Integration Points Summary

| Component | Purpose | Location | Usage |
|-----------|---------|----------|-------|
| Agent Tools | Reusable execution tools | `src/codeindex/web/agents/tools.py` | Import and instantiate in agent `__init__` |
| Agent Routing | Query routing | `src/codeindex/web/services/agent_routing.py` | Add keywords to `DEFAULT_ROUTING_RULES` |
| Agent Service | Orchestration | `src/codeindex/web/services/agent_service.py` | Add execution case in `execute_query` |
| Agent Chat Component | Response formatting | `src/codeindex/web/components/agent_chat.py` | Auto-used by Chat page |
| Chat Page | UI | `src/codeindex/web/pages/2_💬_Chat.py` | No changes needed |
| Base Classes | Shared models | `src/codeindex/web/agents/base.py` | Import `AgentRole`, `AgentConfig`, `AgentResponse`, `Citation` |

## Common Issues and Solutions

### Issue: Agent not routing correctly
- **Solution**: Add more specific keywords to routing rules, ensure no keyword overlap with other agents

### Issue: Citations not validating
- **Solution**: Check Weaviate connection, ensure artifacts have IDs in `_additional.id` field

### Issue: File reading fails
- **Solution**: Use relative paths from `JAVA_SOURCE_DIR`, check file permissions

### Issue: LLM timeout
- **Solution**: Already handled by retry logic, increase timeout in config if needed

### Issue: Tests failing with mocks
- **Solution**: Ensure mock return values match actual tool signatures, check error handling paths

## Useful Commands

```bash
# Run agent tests
pytest tests/unit/web/agents/test_<agent_name>.py -v

# Run all US2.X tests
pytest tests/unit/web/agents/ tests/unit/web/services/test_agent_routing.py tests/unit/web/components/test_agent_chat.py -v

# Run integration tests (requires Weaviate + Ollama)
pytest tests/integration/web/test_agent_chat.py -v

# Check test coverage
pytest tests/unit/web/agents/test_<agent_name>.py --cov=src/codeindex/web/agents/<agent_name> --cov-report=html

# Start Streamlit UI for manual testing
streamlit run src/codeindex/web/app.py
```

## Contact

For questions about this integration pattern, refer to:
- US2.1 implementation: `src/codeindex/web/agents/senior_developer.py`
- US2.1 tests: `tests/unit/web/agents/test_senior_developer.py`
- This guide: `specs/009-streamlit-crewai-web-client/US2.1-INTEGRATION-GUIDE.md`
