"""
Agent Tools Implementation (T061 - US2.1).

Implements the three core tools used by AI agents:
1. WeaviateSearchTool: Search artifacts in Weaviate vector database
2. FileReadTool: Read source files from JAVA_SOURCE_DIR with security validation
3. LLMQueryTool: Query Ollama LLM for text generation with retry logic

Each tool includes:
- Error handling and retry logic
- Input validation
- Performance optimizations
- Security checks
"""

import logging
import os
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


# Tool Registry
AVAILABLE_TOOLS = {}


def register_tool(name: str):
    """Decorator to register tools in the global registry."""
    def decorator(cls):
        AVAILABLE_TOOLS[name] = cls
        return cls
    return decorator


def get_tool_by_name(name: str):
    """Get tool instance by name."""
    tool_class = AVAILABLE_TOOLS.get(name)
    if tool_class is None:
        raise ValueError(f"Tool '{name}' not found in registry. Available tools: {list(AVAILABLE_TOOLS.keys())}")

    return tool_class()


# ========================================
# WeaviateSearchTool
# ========================================

@register_tool("WeaviateSearchTool")
class WeaviateSearchTool:
    """
    Tool for searching artifacts in Weaviate vector database.

    Features:
    - Semantic search over indexed artifacts
    - Filter by artifact type and project
    - Retry logic for transient errors
    - Result caching for performance
    """

    def __init__(self, weaviate_store=None):
        """
        Initialize Weaviate search tool.

        Args:
            weaviate_store: Optional WeaviateStore instance. If None, creates default.
        """
        self.name = "WeaviateSearchTool"
        self.description = "Search for code artifacts in Weaviate vector database using semantic search"

        if weaviate_store is None:
            from codeindex.services.weaviate_store import WeaviateStore
            self.weaviate_store = WeaviateStore()
        else:
            self.weaviate_store = weaviate_store

        # Cache for search results (5-minute TTL)
        self._cache: Dict[str, tuple] = {}  # key -> (results, timestamp)
        self._cache_ttl = timedelta(minutes=5)

    def search(
        self,
        query: str,
        artifact_types: Optional[List[str]] = None,
        project: Optional[str] = None,
        limit: int = 10,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
        enable_cache: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Search for artifacts in Weaviate.

        Args:
            query: Search query (natural language)
            artifact_types: Optional filter by artifact types
            project: Optional filter by project
            limit: Maximum results to return
            max_retries: Maximum retry attempts on transient errors
            backoff_factor: Exponential backoff factor for retries
            enable_cache: Whether to use result caching

        Returns:
            List of artifact dictionaries

        Raises:
            ConnectionError: If Weaviate is unavailable after retries
            TimeoutError: If request times out
        """
        # Check cache
        if enable_cache:
            cache_key = f"{query}:{artifact_types}:{project}:{limit}"
            cached_result = self._get_from_cache(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for query: {query[:50]}")
                return cached_result

        # Execute search with retry logic
        last_error = None
        for attempt in range(max_retries):
            try:
                logger.debug(f"Searching Weaviate (attempt {attempt + 1}/{max_retries}): {query[:50]}")

                # Build filters
                filters = {}
                if artifact_types:
                    filters["artifact_types"] = artifact_types
                if project:
                    filters["project"] = project

                # Execute search
                results = self.weaviate_store.search_artifacts(
                    query,
                    limit=limit,
                    **filters
                )

                # Filter out invalid artifacts (missing required fields)
                valid_results = [
                    r for r in results
                    if r and isinstance(r, dict) and "id" in r
                ]

                logger.info(f"Found {len(valid_results)} valid artifacts for query: {query[:50]}")

                # Cache results
                if enable_cache:
                    self._add_to_cache(cache_key, valid_results)

                return valid_results

            except (ConnectionError, TimeoutError) as e:
                last_error = e
                logger.warning(f"Weaviate search failed (attempt {attempt + 1}/{max_retries}): {e}")

                if attempt < max_retries - 1:
                    # Exponential backoff
                    sleep_time = backoff_factor * (2 ** attempt)
                    logger.debug(f"Retrying in {sleep_time}s...")
                    time.sleep(sleep_time)
                continue

            except Exception as e:
                logger.error(f"Weaviate search failed with unexpected error: {e}", exc_info=True)
                raise

        # All retries exhausted
        logger.error(f"Weaviate search failed after {max_retries} attempts: {last_error}")
        raise last_error

    def _get_from_cache(self, key: str) -> Optional[List[Dict[str, Any]]]:
        """Get results from cache if not expired."""
        if key in self._cache:
            results, timestamp = self._cache[key]
            if datetime.now() - timestamp < self._cache_ttl:
                return results
            else:
                # Expired, remove from cache
                del self._cache[key]
        return None

    def _add_to_cache(self, key: str, results: List[Dict[str, Any]]):
        """Add results to cache with timestamp."""
        self._cache[key] = (results, datetime.now())

    def clear_cache(self):
        """Clear all cached results."""
        self._cache.clear()


# ========================================
# FileReadTool
# ========================================

@register_tool("FileReadTool")
class FileReadTool:
    """
    Tool for reading source files with security validation.

    Features:
    - Read files from JAVA_SOURCE_DIR
    - Directory traversal attack prevention
    - File size limits
    - Encoding error handling with fallback
    """

    def __init__(self, source_dir: Optional[str] = None, max_file_size_mb: int = 10):
        """
        Initialize file read tool.

        Args:
            source_dir: Source directory root. If None, uses JAVA_SOURCE_DIR env variable.
            max_file_size_mb: Maximum file size to read (MB)
        """
        self.name = "FileReadTool"
        self.description = "Read source code files from project directory with security validation"

        # Determine source directory
        if source_dir is None:
            source_dir = os.getenv("JAVA_SOURCE_DIR")
            if not source_dir:
                raise ValueError("JAVA_SOURCE_DIR environment variable not set and source_dir not provided")

        self.source_dir = Path(source_dir).resolve()
        self.max_file_size_bytes = max_file_size_mb * 1024 * 1024

        logger.info(f"Initialized FileReadTool with source_dir: {self.source_dir}")

    def read_file(
        self,
        file_path: str,
        fallback_encoding: str = "latin-1"
    ) -> str:
        """
        Read file content with security validation.

        Args:
            file_path: Relative path from source_dir
            fallback_encoding: Encoding to try if UTF-8 fails

        Returns:
            File content as string

        Raises:
            ValueError: If path is invalid or file too large
            FileNotFoundError: If file doesn't exist
            PermissionError: If file is not readable
        """
        # Construct absolute path
        absolute_path = (self.source_dir / file_path).resolve()

        # Security: Validate path is within source_dir (prevent directory traversal)
        try:
            absolute_path.relative_to(self.source_dir)
        except ValueError:
            raise ValueError(f"Invalid file path: directory traversal not allowed. Path: {file_path}")

        # Check file exists
        if not absolute_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Check is file (not directory)
        if not absolute_path.is_file():
            raise ValueError(f"Path is not a file (directory?): {file_path}")

        # Check file size
        file_size = absolute_path.stat().st_size
        if file_size > self.max_file_size_bytes:
            raise ValueError(
                f"File too large: {file_size / (1024 * 1024):.1f}MB "
                f"(max: {self.max_file_size_bytes / (1024 * 1024):.1f}MB). File: {file_path}"
            )

        # Read file with encoding fallback
        try:
            content = absolute_path.read_text(encoding='utf-8')
            logger.debug(f"Read file ({len(content)} chars): {file_path}")
            return content
        except UnicodeDecodeError:
            logger.warning(f"UTF-8 decode failed for {file_path}, trying fallback encoding: {fallback_encoding}")
            try:
                content = absolute_path.read_text(encoding=fallback_encoding)
                logger.debug(f"Read file with {fallback_encoding} ({len(content)} chars): {file_path}")
                return content
            except Exception as e:
                logger.error(f"Failed to read file with fallback encoding: {e}")
                raise


# ========================================
# LLMQueryTool
# ========================================

@register_tool("LLMQueryTool")
class LLMQueryTool:
    """
    Tool for querying Ollama LLM with retry logic.

    Features:
    - Generate text using Ollama LLM
    - Retry logic for timeouts and connection errors
    - Exponential backoff
    - Result caching for repeated queries
    """

    def __init__(self, ollama_client=None):
        """
        Initialize LLM query tool.

        Args:
            ollama_client: Optional OllamaClient instance. If None, creates default.
        """
        self.name = "LLMQueryTool"
        self.description = "Query Ollama LLM for text generation and reasoning"

        if ollama_client is None:
            from codeindex.services.ollama_client import OllamaClient
            self.ollama_client = OllamaClient()
        else:
            self.ollama_client = ollama_client

        # Cache for query results (5-minute TTL)
        self._cache: Dict[str, tuple] = {}  # key -> (result, timestamp)
        self._cache_ttl = timedelta(minutes=5)

    def query(
        self,
        prompt: str,
        context: Optional[str] = None,
        system_prompt: Optional[str] = None,
        model: str = "gemma3:12b",
        max_retries: int = 3,
        backoff_factor: float = 0.5,
        enable_cache: bool = True
    ) -> str:
        """
        Query Ollama LLM for text generation.

        Args:
            prompt: User prompt
            context: Optional additional context
            system_prompt: Optional system prompt for agent role
            model: Model name
            max_retries: Maximum retry attempts on transient errors
            backoff_factor: Exponential backoff factor
            enable_cache: Whether to use result caching

        Returns:
            Generated text

        Raises:
            TimeoutError: If request times out after retries
            ConnectionError: If Ollama is unavailable after retries
            ValueError: If model not found or context too long
        """
        # Build full prompt
        full_prompt_parts = []
        if system_prompt:
            full_prompt_parts.append(f"System: {system_prompt}\n")
        if context:
            full_prompt_parts.append(f"Context: {context}\n")
        full_prompt_parts.append(f"Query: {prompt}")

        full_prompt = "\n".join(full_prompt_parts)

        # Check cache
        if enable_cache:
            cache_key = f"{full_prompt}:{model}"
            cached_result = self._get_from_cache(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for LLM query: {prompt[:50]}")
                return cached_result

        # Execute query with retry logic
        last_error = None
        for attempt in range(max_retries):
            try:
                logger.debug(f"Querying Ollama (attempt {attempt + 1}/{max_retries}): {prompt[:50]}")

                # Generate response
                response = self.ollama_client.generate(full_prompt, model=model)

                # Handle unexpected response types
                if not isinstance(response, str):
                    logger.warning(f"Ollama returned unexpected type: {type(response)}")
                    response = str(response)

                logger.info(f"Ollama response generated ({len(response)} chars)")

                # Cache result
                if enable_cache:
                    self._add_to_cache(cache_key, response)

                return response

            except TimeoutError as e:
                last_error = e
                logger.warning(f"Ollama query timed out (attempt {attempt + 1}/{max_retries}): {e}")

                if attempt < max_retries - 1:
                    # Exponential backoff
                    sleep_time = backoff_factor * (2 ** attempt)
                    logger.debug(f"Retrying in {sleep_time}s...")
                    time.sleep(sleep_time)
                continue

            except ConnectionError as e:
                last_error = e
                logger.warning(f"Ollama connection failed (attempt {attempt + 1}/{max_retries}): {e}")

                if attempt < max_retries - 1:
                    # Exponential backoff
                    sleep_time = backoff_factor * (2 ** attempt)
                    logger.debug(f"Retrying in {sleep_time}s...")
                    time.sleep(sleep_time)
                continue

            except ValueError as e:
                # Model not found or context too long - don't retry
                logger.error(f"Ollama query failed with ValueError: {e}")
                raise

            except Exception as e:
                logger.error(f"Ollama query failed with unexpected error: {e}", exc_info=True)
                raise

        # All retries exhausted
        logger.error(f"Ollama query failed after {max_retries} attempts: {last_error}")
        raise last_error

    def _get_from_cache(self, key: str) -> Optional[str]:
        """Get result from cache if not expired."""
        if key in self._cache:
            result, timestamp = self._cache[key]
            if datetime.now() - timestamp < self._cache_ttl:
                return result
            else:
                # Expired, remove from cache
                del self._cache[key]
        return None

    def _add_to_cache(self, key: str, result: str):
        """Add result to cache with timestamp."""
        self._cache[key] = (result, datetime.now())

    def clear_cache(self):
        """Clear all cached results."""
        self._cache.clear()


# Export all tools
__all__ = [
    "WeaviateSearchTool",
    "FileReadTool",
    "LLMQueryTool",
    "AVAILABLE_TOOLS",
    "get_tool_by_name"
]
