# Agent Tool Interfaces Contract

**Feature**: 009-streamlit-crewai-web-client
**Version**: 1.0.0
**Date**: 2026-01-14

## Overview

This document defines the interfaces for custom CrewAI tools that agents use to interact with the codebase analysis system. All tools must implement the `Tool` interface from `crewai_tools` and provide consistent error handling, input validation, and output formatting.

---

## Base Tool Interface

All custom tools inherit from CrewAI's `Tool` class:

```python
from crewai_tools import Tool
from typing import Any, Callable, Optional
from pydantic import BaseModel, Field

class BaseAgentTool(Tool):
    """Base class for all agent tools."""

    name: str = Field(..., description="Tool name (unique identifier)")
    description: str = Field(..., description="Tool description for LLM context")
    func: Callable[[str], Any] = Field(..., description="Tool execution function")
    return_direct: bool = Field(default=False, description="Return result directly to user")
    verbose: bool = Field(default=True, description="Enable verbose logging")

    class Config:
        arbitrary_types_allowed = True
```

---

## 1. WeaviateSearchTool

### Purpose

Search the Weaviate vector database for artifacts using natural language queries. Returns structured artifact metadata with relevance scores.

### Interface Definition

```python
from crewai_tools import Tool
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class SearchResult:
    """Single search result from Weaviate."""
    artifact_id: str
    artifact_type: str
    confidence_score: float
    file_path: str
    preview: str
    metadata: Dict[str, Any]

class WeaviateSearchTool(Tool):
    """Tool for semantic search over Weaviate artifact database."""

    name: str = "semantic_search"
    description: str = """
    Search the codebase artifacts using natural language queries.
    Use this tool to find: DAOs, Services, Presenters, Views, DTOs, database tables, endpoints.

    Input: Natural language search query (e.g., "user authentication services")
    Output: List of relevant artifacts with metadata and confidence scores
    """

    def __init__(self, weaviate_store: 'WeaviateStore', max_results: int = 10):
        self.weaviate_store = weaviate_store
        self.max_results = max_results
        super().__init__(
            name=self.name,
            description=self.description,
            func=self._search
        )

    def _search(self, query: str) -> List[SearchResult]:
        """Execute search query against Weaviate."""
        try:
            # Validate input
            if not query or len(query.strip()) < 3:
                raise ValueError("Query must be at least 3 characters")

            # Execute Weaviate search
            results = self.weaviate_store.search(
                query_text=query,
                limit=self.max_results,
                include_metadata=True
            )

            # Format results
            return [
                SearchResult(
                    artifact_id=r['id'],
                    artifact_type=r['artifact_type'],
                    confidence_score=r['_additional']['certainty'],
                    file_path=r['file_path'],
                    preview=r['content'][:200],
                    metadata=r
                )
                for r in results
            ]

        except Exception as e:
            logger.error(f"WeaviateSearchTool error: {e}")
            return []  # Return empty list on error (graceful degradation)
```

### Input Schema

```python
{
    "type": "string",
    "minLength": 3,
    "maxLength": 500,
    "description": "Natural language search query",
    "examples": [
        "user authentication services",
        "database tables with foreign keys",
        "GWT presenters for admin panel",
        "DAO classes that access customer data"
    ]
}
```

### Output Schema

```python
{
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "artifact_id": {
                "type": "string",
                "format": "uuid",
                "description": "Weaviate artifact UUID"
            },
            "artifact_type": {
                "type": "string",
                "enum": ["DaoCall", "GwtPresenter", "GwtView", "DtoArtifact", "DbTable", "BackendDoc"],
                "description": "Artifact type classification"
            },
            "confidence_score": {
                "type": "number",
                "minimum": 0.0,
                "maximum": 1.0,
                "description": "Relevance score from vector search"
            },
            "file_path": {
                "type": "string",
                "description": "Absolute path to source file"
            },
            "preview": {
                "type": "string",
                "maxLength": 200,
                "description": "First 200 characters of artifact content"
            },
            "metadata": {
                "type": "object",
                "description": "Full artifact metadata from Weaviate"
            }
        },
        "required": ["artifact_id", "artifact_type", "confidence_score", "file_path"]
    },
    "maxItems": 10
}
```

### Error Handling

```python
# Error Types and Handling Strategy

1. ConnectionError (Weaviate unavailable):
   - Log error with context
   - Return empty array []
   - Agent receives: "No results found" (graceful degradation)

2. ValidationError (invalid query):
   - Raise ValueError with descriptive message
   - Agent receives: Error message to rephrase query

3. TimeoutError (query too slow):
   - Log warning with query details
   - Return partial results (if any)
   - Agent receives: Partial results with warning

4. EmptyResultError (no matches):
   - Return empty array []
   - Agent receives: "No artifacts matched your query"
```

### Usage Example

```python
# In agent definition
from codeindex.web.services.weaviate_search_tool import WeaviateSearchTool

weaviate_tool = WeaviateSearchTool(
    weaviate_store=get_weaviate_client(),
    max_results=10
)

senior_dev_agent = Agent(
    role="Senior Developer",
    goal="Explain code architecture",
    tools=[weaviate_tool],
    llm=ollama_llm
)

# Agent uses tool in conversation
# User: "Find all DAOs that access user tables"
# Agent thinks: I should use semantic_search tool
# Agent calls: weaviate_tool._search("DAO user table access")
# Agent receives: [SearchResult(...), SearchResult(...)]
# Agent responds: "I found 5 DAOs that access user tables: UserDAO.java, ..."
```

---

## 2. FileReadTool

### Purpose

Read source code files from disk with encoding detection and syntax validation. Returns file content with metadata for agent analysis.

### Interface Definition

```python
from crewai_tools import Tool
from pathlib import Path
from typing import Optional
from dataclasses import dataclass
import chardet

@dataclass
class FileContent:
    """File content with metadata."""
    file_path: str
    content: str
    encoding: str
    line_count: int
    language: str
    size_bytes: int

class FileReadTool(Tool):
    """Tool for reading source code files from disk."""

    name: str = "read_source_file"
    description: str = """
    Read source code file from disk.
    Use this tool to examine actual code implementation, method bodies, or detailed logic.

    Input: Absolute file path (must be within JAVA_SOURCE_DIR)
    Output: File content as string with metadata
    """

    def __init__(self, source_dir: Path, max_file_size_mb: int = 10):
        self.source_dir = source_dir
        self.max_file_size_bytes = max_file_size_mb * 1024 * 1024
        super().__init__(
            name=self.name,
            description=self.description,
            func=self._read_file
        )

    def _read_file(self, file_path: str) -> FileContent:
        """Read file with encoding detection and validation."""
        try:
            path = Path(file_path)

            # Security: Validate path is within source directory
            if not self._is_safe_path(path):
                raise PermissionError(f"File access denied: {file_path}")

            # Validate file exists and is file (not directory)
            if not path.is_file():
                raise FileNotFoundError(f"File not found: {file_path}")

            # Validate file size
            size = path.stat().st_size
            if size > self.max_file_size_bytes:
                raise ValueError(f"File too large: {size} bytes (max: {self.max_file_size_bytes})")

            # Detect encoding
            with open(path, 'rb') as f:
                raw_content = f.read()
                detected = chardet.detect(raw_content)
                encoding = detected['encoding'] or 'utf-8'

            # Read file with detected encoding
            content = raw_content.decode(encoding, errors='replace')

            # Detect language from extension
            language = self._detect_language(path)

            return FileContent(
                file_path=str(path),
                content=content,
                encoding=encoding,
                line_count=len(content.splitlines()),
                language=language,
                size_bytes=size
            )

        except Exception as e:
            logger.error(f"FileReadTool error: {e}")
            raise  # Re-raise for agent to handle

    def _is_safe_path(self, path: Path) -> bool:
        """Validate path is within source directory (prevent directory traversal)."""
        try:
            resolved = path.resolve()
            return str(resolved).startswith(str(self.source_dir.resolve()))
        except Exception:
            return False

    def _detect_language(self, path: Path) -> str:
        """Detect programming language from file extension."""
        ext_map = {
            '.java': 'java',
            '.jsp': 'jsp',
            '.js': 'javascript',
            '.xml': 'xml',
            '.sql': 'sql',
            '.properties': 'properties',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.json': 'json'
        }
        return ext_map.get(path.suffix.lower(), 'text')
```

### Input Schema

```python
{
    "type": "string",
    "pattern": "^/.+",
    "description": "Absolute file path",
    "examples": [
        "/path/to/project/src/main/java/UserService.java",
        "/path/to/project/src/main/webapp/login.jsp",
        "/path/to/project/src/main/resources/config.xml"
    ]
}
```

### Output Schema

```python
{
    "type": "object",
    "properties": {
        "file_path": {
            "type": "string",
            "description": "Absolute path to file"
        },
        "content": {
            "type": "string",
            "description": "File content as text"
        },
        "encoding": {
            "type": "string",
            "description": "Detected character encoding (e.g., utf-8, iso-8859-1)"
        },
        "line_count": {
            "type": "integer",
            "minimum": 0,
            "description": "Number of lines in file"
        },
        "language": {
            "type": "string",
            "enum": ["java", "jsp", "javascript", "xml", "sql", "properties", "yaml", "json", "text"],
            "description": "Detected programming language"
        },
        "size_bytes": {
            "type": "integer",
            "minimum": 0,
            "description": "File size in bytes"
        }
    },
    "required": ["file_path", "content", "encoding", "language"]
}
```

### Error Handling

```python
# Error Types and Handling Strategy

1. FileNotFoundError:
   - Raise with descriptive message
   - Agent receives: "File not found: {path}. Check artifact metadata for correct path."

2. PermissionError (path outside source_dir):
   - Raise with security message
   - Agent receives: "Access denied. File must be within project directory."

3. ValueError (file too large >10MB):
   - Raise with size info
   - Agent receives: "File too large ({size}MB). Use search tool to get summary instead."

4. UnicodeDecodeError:
   - Fallback to 'replace' error handling
   - Return content with replacement characters (�)
   - Log warning with encoding details
```

### Usage Example

```python
# In agent definition
from codeindex.web.services.file_read_tool import FileReadTool

file_tool = FileReadTool(
    source_dir=Path(config.JAVA_SOURCE_DIR),
    max_file_size_mb=10
)

backend_specialist = Agent(
    role="Backend Specialist",
    goal="Analyze service layer logic",
    tools=[file_tool],
    llm=ollama_llm
)

# Agent uses tool in conversation
# User: "Explain the authentication logic in UserService.java"
# Agent thinks: I need to read the file to see implementation
# Agent calls: file_tool._read_file("/path/to/UserService.java")
# Agent receives: FileContent(content="public class UserService {...}", ...)
# Agent responds: "The UserService class implements authentication via..."
```

---

## 3. LLMQueryTool

### Purpose

Make additional LLM queries for deep analysis or synthesis. Allows agents to delegate complex reasoning to the underlying LLM without executing tasks.

### Interface Definition

```python
from crewai_tools import Tool
from typing import Optional
from dataclasses import dataclass

@dataclass
class LLMResponse:
    """Response from LLM query."""
    prompt: str
    response: str
    model: str
    tokens_used: int

class LLMQueryTool(Tool):
    """Tool for making additional LLM queries for deep analysis."""

    name: str = "llm_query"
    description: str = """
    Query the language model for additional reasoning or synthesis.
    Use this tool for: summarizing large text, extracting patterns, comparing code snippets.

    Input: Question or analysis prompt
    Output: LLM-generated response
    """

    def __init__(self, ollama_client: 'OllamaClient', max_tokens: int = 1000):
        self.ollama_client = ollama_client
        self.max_tokens = max_tokens
        super().__init__(
            name=self.name,
            description=self.description,
            func=self._query_llm
        )

    def _query_llm(self, prompt: str) -> LLMResponse:
        """Execute LLM query via Ollama."""
        try:
            # Validate input
            if not prompt or len(prompt.strip()) < 10:
                raise ValueError("Prompt must be at least 10 characters")

            if len(prompt) > 4000:
                raise ValueError("Prompt too long (max 4000 chars). Break into smaller queries.")

            # Execute LLM query
            response = self.ollama_client.generate(
                prompt=prompt,
                max_tokens=self.max_tokens,
                temperature=0.7
            )

            return LLMResponse(
                prompt=prompt,
                response=response['text'],
                model=response['model'],
                tokens_used=response['usage']['total_tokens']
            )

        except Exception as e:
            logger.error(f"LLMQueryTool error: {e}")
            raise  # Re-raise for agent to handle
```

### Input Schema

```python
{
    "type": "string",
    "minLength": 10,
    "maxLength": 4000,
    "description": "Question or analysis prompt for LLM",
    "examples": [
        "Summarize the key responsibilities of this UserService class",
        "Compare the authentication approaches in these two code snippets",
        "What design patterns are evident in this code?",
        "Extract all database table names mentioned in this SQL file"
    ]
}
```

### Output Schema

```python
{
    "type": "object",
    "properties": {
        "prompt": {
            "type": "string",
            "description": "Original prompt sent to LLM"
        },
        "response": {
            "type": "string",
            "description": "LLM-generated response text"
        },
        "model": {
            "type": "string",
            "description": "Model used for generation (e.g., gemma3:12b)"
        },
        "tokens_used": {
            "type": "integer",
            "minimum": 0,
            "description": "Total tokens consumed (prompt + response)"
        }
    },
    "required": ["prompt", "response", "model"]
}
```

### Error Handling

```python
# Error Types and Handling Strategy

1. TimeoutError (Ollama timeout):
   - Retry with exponential backoff (existing retry logic)
   - If all retries fail, raise with message
   - Agent receives: "LLM query timed out. Try a shorter or simpler prompt."

2. ValueError (prompt too long/short):
   - Raise with validation message
   - Agent receives: "Invalid prompt length. Must be 10-4000 characters."

3. ConnectionError (Ollama unavailable):
   - Raise with service status
   - Agent receives: "LLM service unavailable. Check Ollama connection."

4. ContentFilterError (inappropriate content):
   - Log warning with prompt hash
   - Raise with generic message
   - Agent receives: "Query cannot be processed. Rephrase your prompt."
```

### Usage Example

```python
# In agent definition
from codeindex.web.services.llm_query_tool import LLMQueryTool

llm_tool = LLMQueryTool(
    ollama_client=get_ollama_client(),
    max_tokens=1000
)

data_analyst = Agent(
    role="Data Analyst",
    goal="Analyze database schemas",
    tools=[llm_tool],
    llm=ollama_llm
)

# Agent uses tool in conversation
# User: "What foreign keys exist in the user management module?"
# Agent thinks: I need to analyze SQL files to extract FK definitions
# Agent calls: llm_tool._query_llm("Extract foreign key definitions from: <SQL content>")
# Agent receives: LLMResponse(response="The SQL defines 3 FKs: user_id->users.id, ...")
# Agent responds: "The user management module has 3 foreign keys: ..."
```

---

## Tool Registration

All tools must be registered with agents during initialization:

```python
from crewai import Agent
from codeindex.web.services.weaviate_search_tool import WeaviateSearchTool
from codeindex.web.services.file_read_tool import FileReadTool
from codeindex.web.services.llm_query_tool import LLMQueryTool

# Initialize tools
weaviate_tool = WeaviateSearchTool(weaviate_store=get_weaviate_client())
file_tool = FileReadTool(source_dir=Path(config.JAVA_SOURCE_DIR))
llm_tool = LLMQueryTool(ollama_client=get_ollama_client())

# Register with agent
agent = Agent(
    role="Senior Developer",
    goal="Explain code architecture",
    backstory="15+ years Java enterprise experience",
    tools=[weaviate_tool, file_tool, llm_tool],
    llm=ollama_llm,
    verbose=True
)
```

---

## Validation Rules

All tool implementations MUST:

1. **Type Safety**: Use type hints for all parameters and return values
2. **Input Validation**: Validate inputs before execution (length, format, permissions)
3. **Error Handling**: Catch all exceptions and provide meaningful error messages
4. **Logging**: Log all tool invocations with context (agent, query, execution time)
5. **Performance**: Execute in <2 seconds for 95% of queries (p95 latency)
6. **Security**: Validate file paths to prevent directory traversal attacks
7. **Documentation**: Include docstrings with examples for all public methods

---

## Testing Requirements

Each tool MUST have:

1. **Unit Tests**: Mock external dependencies (Weaviate, file I/O, Ollama)
2. **Integration Tests**: Test with real Weaviate, files, and Ollama
3. **Error Tests**: Validate error handling for all error types
4. **Performance Tests**: Validate p95 latency <2 seconds

Example test structure:

```python
# tests/unit/test_weaviate_search_tool.py

def test_search_returns_results(mock_weaviate_store):
    """Test successful search returns formatted results."""
    tool = WeaviateSearchTool(weaviate_store=mock_weaviate_store)
    results = tool._search("user authentication")
    assert len(results) > 0
    assert all(isinstance(r, SearchResult) for r in results)

def test_search_invalid_query_raises_error():
    """Test short query raises ValueError."""
    tool = WeaviateSearchTool(weaviate_store=mock_weaviate_store)
    with pytest.raises(ValueError, match="at least 3 characters"):
        tool._search("ab")

def test_search_weaviate_unavailable_returns_empty():
    """Test graceful degradation when Weaviate down."""
    mock_store = Mock(side_effect=ConnectionError("Weaviate unavailable"))
    tool = WeaviateSearchTool(weaviate_store=mock_store)
    results = tool._search("user authentication")
    assert results == []  # Graceful degradation
```

---

**Version**: 1.0.0
**Last Updated**: 2026-01-14
**Status**: Final - Ready for Implementation
