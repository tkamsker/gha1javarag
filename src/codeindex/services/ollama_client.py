"""
Ollama HTTP client for AI-powered semantic extraction.

Provides integration with Ollama for code understanding using local LLMs.
"""

import logging
import json
import threading
from typing import Dict, Any, Optional
from pathlib import Path

import httpx

from codeindex.utils.retry import retry
from codeindex.models import ArtifactType

logger = logging.getLogger(__name__)


# ==============================================================================
# Configuration
# ==============================================================================

# Rate limiting: max concurrent AI calls
MAX_CONCURRENT_AI_CALLS = 10
_rate_limiter = threading.Semaphore(MAX_CONCURRENT_AI_CALLS)

# HTTP timeouts
CONNECT_TIMEOUT = 10.0  # seconds
READ_TIMEOUT = 60.0     # seconds (1 minute for LLM inference, skip slow files)


# ==============================================================================
# Prompt Templates
# ==============================================================================

SYSTEM_PROMPT = """You are a code analysis expert. Analyze the provided code file and extract semantic information.

Your response must be valid JSON with these exact fields:
{
  "summary": "Brief 1-2 sentence description of what this code does",
  "roles": ["primary purpose or role of this code"],
  "entities": ["key classes, functions, or components defined"],
  "tags": ["relevant technical tags"],
  "language": "programming language",
  "frameworks": ["frameworks or libraries used"],
  "concerns": ["cross-cutting concerns like security, validation"],
  "dependencies": ["external dependencies or imports"]
}

Be concise and accurate. Focus on semantic meaning, not syntax."""


def create_extraction_prompt(
    file_path: str,
    file_content: str,
    artifact_type: ArtifactType,
    pom_context: Optional[str] = None
) -> str:
    """
    Create extraction prompt for Ollama.

    Args:
        file_path: Path to the file
        file_content: Content of the file
        artifact_type: Type of artifact
        pom_context: Optional POM context (project info)

    Returns:
        Formatted prompt string
    """
    prompt_parts = [
        f"File: {file_path}",
        f"Type: {artifact_type.value}",
    ]

    if pom_context:
        prompt_parts.append(f"Project Context: {pom_context}")

    prompt_parts.extend([
        "",
        "Code:",
        "```",
        file_content[:10000],  # Limit to first 10k chars
        "```",
        "",
        "Analyze this code and provide the JSON response."
    ])

    return "\n".join(prompt_parts)


# ==============================================================================
# Ollama HTTP Client
# ==============================================================================

class OllamaClient:
    """
    HTTP client for Ollama API.

    Handles connection pooling, rate limiting, and retry logic.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "gemma2:12b",
        max_retries: int = 3
    ):
        """
        Initialize Ollama client.

        Args:
            base_url: Ollama server base URL
            model: Model name to use
            max_retries: Maximum retry attempts
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.max_retries = max_retries

        # Create HTTP client with connection pooling
        limits = httpx.Limits(
            max_keepalive_connections=MAX_CONCURRENT_AI_CALLS,
            max_connections=MAX_CONCURRENT_AI_CALLS,
        )

        timeout = httpx.Timeout(
            connect=CONNECT_TIMEOUT,
            read=READ_TIMEOUT,
            write=30.0,
            pool=10.0
        )

        self.client = httpx.Client(
            base_url=self.base_url,
            limits=limits,
            timeout=timeout,
            follow_redirects=True
        )

        self.logger = logging.getLogger(__name__)

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, *args):
        """Context manager exit - close HTTP client."""
        self.close()

    def close(self):
        """Close HTTP client."""
        if self.client:
            self.client.close()

    @retry(max_attempts=3, base_delay=2.0, exponential_base=2.0, exceptions=(ConnectionError, httpx.HTTPStatusError))
    def call_ollama(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.1,
        format_json: bool = True
    ) -> Dict[str, Any]:
        """
        Call Ollama API with retry and rate limiting.

        Retries on connection errors and HTTP errors, but NOT on timeouts
        (timeouts are raised immediately to avoid long delays).

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature (0.0-1.0)
            format_json: Whether to request JSON format

        Returns:
            Response dict with 'response' key

        Raises:
            httpx.HTTPError: On HTTP errors
            ValueError: On invalid response
            TimeoutError: On timeout (not retried)
        """
        # Acquire rate limiter
        with _rate_limiter:
            self.logger.debug(f"Calling Ollama with model {self.model}")

            # Build request payload
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                }
            }

            if system_prompt:
                payload["system"] = system_prompt

            if format_json:
                payload["format"] = "json"

            # Make HTTP request
            try:
                response = self.client.post(
                    "/api/generate",
                    json=payload
                )
                response.raise_for_status()

                # Parse response
                result = response.json()

                if "response" not in result:
                    raise ValueError(f"Invalid Ollama response: missing 'response' field")

                self.logger.debug("Ollama call successful")
                return result

            except httpx.ConnectError as e:
                self.logger.error(f"Cannot connect to Ollama at {self.base_url}: {e}")
                raise ConnectionError(
                    f"Ollama is not available at {self.base_url}. "
                    f"Make sure Ollama is running: ollama serve"
                ) from e

            except httpx.TimeoutException as e:
                self.logger.warning(f"Ollama timeout after {READ_TIMEOUT}s: {e}")
                raise TimeoutError(f"Ollama request timed out: {e}") from e

            except httpx.HTTPStatusError as e:
                self.logger.error(f"Ollama HTTP error {e.response.status_code}: {e}")
                raise

    def extract_semantics(
        self,
        file_path: str,
        file_content: str,
        artifact_type: ArtifactType,
        pom_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Extract semantic information from code file.

        Args:
            file_path: Path to file
            file_content: File content
            artifact_type: Type of artifact
            pom_context: Optional POM context

        Returns:
            Dict with extracted semantics (summary, entities, tags, etc.)

        Raises:
            ConnectionError: If Ollama is unavailable
            TimeoutError: If request times out
            ValueError: If response is malformed
        """
        # Create prompt
        prompt = create_extraction_prompt(
            file_path,
            file_content,
            artifact_type,
            pom_context
        )

        # Call Ollama
        try:
            response = self.call_ollama(
                prompt=prompt,
                system_prompt=SYSTEM_PROMPT,
                temperature=0.1,
                format_json=True
            )

            # Parse JSON response
            response_text = response["response"]

            try:
                extracted = json.loads(response_text)
            except json.JSONDecodeError as e:
                self.logger.warning(f"Failed to parse Ollama JSON response: {e}")
                # Return minimal fallback
                extracted = {
                    "summary": f"Code file: {Path(file_path).name}",
                    "roles": [],
                    "entities": [],
                    "tags": [],
                    "language": artifact_type.value,
                    "frameworks": [],
                    "concerns": [],
                    "dependencies": []
                }

            # Validate required fields
            required_fields = ["summary", "roles", "entities", "tags", "language", "frameworks", "concerns", "dependencies"]
            for field in required_fields:
                if field not in extracted:
                    extracted[field] = [] if field != "summary" and field != "language" else ""

            return extracted

        except (ConnectionError, TimeoutError) as e:
            # Re-raise connection/timeout errors for graceful degradation
            raise

        except Exception as e:
            self.logger.error(f"Unexpected error in semantic extraction: {e}")
            # Return minimal fallback
            return {
                "summary": f"Code file: {Path(file_path).name}",
                "roles": [],
                "entities": [],
                "tags": [],
                "language": artifact_type.value,
                "frameworks": [],
                "concerns": [],
                "dependencies": []
            }

    def health_check(self) -> bool:
        """
        Check if Ollama is available and responsive.

        Returns:
            True if Ollama is healthy, False otherwise
        """
        try:
            response = self.client.get("/api/tags", timeout=5.0)
            response.raise_for_status()
            return True
        except Exception as e:
            self.logger.warning(f"Ollama health check failed: {e}")
            return False


# ==============================================================================
# Convenience Functions
# ==============================================================================

def create_ollama_client(
    base_url: Optional[str] = None,
    model: Optional[str] = None
) -> OllamaClient:
    """
    Create Ollama client with configuration from environment.

    Args:
        base_url: Optional override for Ollama URL
        model: Optional override for model name

    Returns:
        Configured OllamaClient instance
    """
    import os

    if not base_url:
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    if not model:
        model = os.getenv("OLLAMA_MODEL_NAME", "gemma2:12b")

    return OllamaClient(base_url=base_url, model=model)
