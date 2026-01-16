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

from codeindex.utils.retry import retry, calculate_exponential_backoff
from codeindex.utils.timeout_calculator import TimeoutCalculator
from codeindex.models import ArtifactType
from codeindex.models.metrics import TimeoutMetric
from codeindex.utils.metrics import get_metrics_collector

logger = logging.getLogger(__name__)


# ==============================================================================
# Configuration
# ==============================================================================

# Rate limiting: max concurrent AI calls
# Feature 008 T002: Reduced from 10 to 5 to prevent Ollama overload
# Production issue: 11.5% timeout rate with 10 workers
# Target: <2% timeout rate with 5 workers
MAX_CONCURRENT_AI_CALLS = 5
_rate_limiter = threading.Semaphore(MAX_CONCURRENT_AI_CALLS)

# HTTP timeouts (defaults, can be overridden in OllamaClient constructor)
DEFAULT_CONNECT_TIMEOUT = 10.0  # seconds
DEFAULT_READ_TIMEOUT = 240.0    # seconds (base timeout for adaptive calculation)


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
        max_retries: int = 3,
        connect_timeout: float = DEFAULT_CONNECT_TIMEOUT,
        read_timeout: float = DEFAULT_READ_TIMEOUT
    ):
        """
        Initialize Ollama client with adaptive timeout support.

        Args:
            base_url: Ollama server base URL
            model: Model name to use
            max_retries: Maximum retry attempts
            connect_timeout: Connection timeout in seconds
            read_timeout: Base read timeout in seconds (used as base for adaptive calculation)

        Note:
            Feature 008 T002: Adaptive timeouts are calculated using TimeoutCalculator
            based on file size. The read_timeout parameter serves as the base timeout.
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.max_retries = max_retries
        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout

        # Initialize adaptive timeout calculator (Feature 008 T002)
        # Use read_timeout as base, with scaling factor of 10s per 100 lines
        self.timeout_calculator = TimeoutCalculator(
            base=int(read_timeout),  # Use read_timeout as base (default 240s)
            scale=10,                 # Add 10s per 100 lines
            min_timeout=60,           # Minimum 1 minute
            max_timeout=600           # Maximum 10 minutes
        )

        # Log initialization
        logger.info(
            f"OllamaClient initialized: model={model}, "
            f"base_timeout={read_timeout}s, connect_timeout={connect_timeout}s, "
            f"adaptive_timeouts=enabled"
        )

        # Create HTTP client with connection pooling
        limits = httpx.Limits(
            max_keepalive_connections=MAX_CONCURRENT_AI_CALLS,
            max_connections=MAX_CONCURRENT_AI_CALLS,
        )

        timeout = httpx.Timeout(
            connect=self.connect_timeout,
            read=self.read_timeout,
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

    def _calculate_timeout(self, file_lines: int) -> float:
        """
        Calculate adaptive timeout based on file size using TimeoutCalculator.

        Feature 008 T002: New adaptive timeout algorithm
        Formula: timeout = base + (lines / 100) * scale
        Capped at: max(min_timeout, min(timeout, max_timeout))

        For small files (100 lines): 250s
        For medium files (500 lines): 290s
        For large files (1000 lines): 340s
        For very large files (5000 lines): 600s (capped)

        Args:
            file_lines: Number of lines in the file

        Returns:
            Adaptive timeout in seconds

        Examples:
            >>> client = OllamaClient()
            >>> client._calculate_timeout(100)
            250.0
            >>> client._calculate_timeout(1000)
            340.0
            >>> client._calculate_timeout(5000)
            600.0  # Capped at max_timeout
        """
        # Use TimeoutCalculator for consistent timeout calculation
        timeout = self.timeout_calculator.calculate_for_lines(file_lines)

        logger.debug(
            f"Calculated adaptive timeout: {timeout}s "
            f"for file with {file_lines} lines "
            f"(base={self.timeout_calculator.base}s, "
            f"scale={self.timeout_calculator.scale}s/100lines)"
        )

        return float(timeout)

    def _clean_json_response(self, response_text: str) -> str:
        """
        Clean common JSON formatting issues from LLM responses.

        Args:
            response_text: Raw LLM response

        Returns:
            Cleaned JSON string

        Examples:
            - Strips markdown code fences: ```json ... ```
            - Removes trailing commas: {"a": 1,} → {"a": 1}
            - Strips whitespace
        """
        import re

        # Strip markdown code fences
        if response_text.strip().startswith("```"):
            lines = response_text.strip().split('\n')
            # Remove first line if it's a code fence
            if lines[0].startswith("```"):
                lines = lines[1:]
            # Remove last line if it's a code fence
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            response_text = '\n'.join(lines)

        # Strip leading/trailing whitespace
        response_text = response_text.strip()

        # Remove trailing commas before closing braces/brackets
        # Handles: {"a": 1,} and ["a",]
        response_text = re.sub(r',(\s*[}\]])', r'\1', response_text)

        return response_text

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
                self.logger.warning(f"Ollama timeout after {self.read_timeout}s: {e}")
                raise TimeoutError(f"Ollama request timed out: {e}") from e

            except httpx.HTTPStatusError as e:
                self.logger.error(f"Ollama HTTP error {e.response.status_code}: {e}")
                raise

    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate text response from Ollama (simplified interface for web agents).

        Args:
            prompt: User prompt
            model: Model name (uses instance model if not specified)
            system_prompt: Optional system prompt
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens (not used with Ollama, kept for API compatibility)

        Returns:
            Generated text response as string

        Raises:
            httpx.HTTPError: On HTTP errors
            ValueError: On invalid response
            TimeoutError: On timeout
        """
        # Use specified model or fall back to instance model
        if model and model != self.model:
            # Temporarily override model for this call
            original_model = self.model
            self.model = model
            try:
                result = self.call_ollama(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    format_json=False  # Web agents expect plain text, not JSON
                )
            finally:
                self.model = original_model
        else:
            result = self.call_ollama(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=temperature,
                format_json=False  # Web agents expect plain text, not JSON
            )

        # Extract response text from result dict
        return result.get("response", "")

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

            # Clean JSON response to handle common LLM formatting issues
            cleaned_text = self._clean_json_response(response_text)

            try:
                extracted = json.loads(cleaned_text)
            except json.JSONDecodeError as e:
                # Log error with response preview for debugging
                response_preview = cleaned_text[:500] if len(cleaned_text) > 500 else cleaned_text
                self.logger.warning(
                    f"Failed to parse Ollama JSON response for {Path(file_path).name}: {e}\n"
                    f"Response preview (first 500 chars): {response_preview}"
                )
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

    def extract_with_timeout(
        self,
        file_path: str,
        file_content: str,
        artifact_type: ArtifactType,
        file_lines: int,
        pom_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Extract metadata with adaptive timeout, exponential backoff retry, and structural fallback.

        Implements Feature 007 US1 requirements:
        - Adaptive timeout based on file size
        - 3 retry attempts with exponential backoff [5s, 15s, 45s]
        - Structural analysis fallback when retries exhausted
        - Detailed timeout metrics logging

        Args:
            file_path: Absolute path to source file
            file_content: Full source code content
            artifact_type: Type of artifact (service, dao, presenter, etc.)
            file_lines: Number of lines in file (for timeout calculation)
            pom_context: Optional POM context

        Returns:
            ExtractionResult with metadata or fallback indicators

        Raises:
            ConnectionError: If Ollama is completely unavailable (not retried)
        """
        import time
        from codeindex.services.structural_analyzer import StructuralAnalyzer

        # Calculate adaptive timeout
        adaptive_timeout = self._calculate_timeout(file_lines)

        # Update HTTP client timeout for this request
        original_timeout = self.read_timeout
        self.read_timeout = adaptive_timeout
        self.client = httpx.Client(
            base_url=self.base_url,
            limits=httpx.Limits(
                max_keepalive_connections=MAX_CONCURRENT_AI_CALLS,
                max_connections=MAX_CONCURRENT_AI_CALLS
            ),
            timeout=httpx.Timeout(
                connect=self.connect_timeout,
                read=adaptive_timeout,
                write=30.0,
                pool=10.0
            ),
            follow_redirects=True
        )

        # Retry loop with exponential backoff
        max_attempts = 3
        retry_count = 0
        fallback_used = False
        extraction_quality = 'failed'
        timeout_duration = 0.0
        last_error = None
        result = None

        for attempt in range(1, max_attempts + 1):
            try:
                logger.info(
                    f"Extraction attempt {attempt}/{max_attempts} for {Path(file_path).name} "
                    f"(timeout={adaptive_timeout:.1f}s)"
                )

                start_time = time.time()

                # Attempt LLM extraction
                result = self.extract_semantics(
                    file_path=file_path,
                    file_content=file_content,
                    artifact_type=artifact_type,
                    pom_context=pom_context
                )

                elapsed = time.time() - start_time

                # Success - no timeout
                extraction_quality = 'full'
                logger.info(
                    f"Extraction succeeded on attempt {attempt} "
                    f"in {elapsed:.1f}s for {Path(file_path).name}"
                )
                break

            except TimeoutError as e:
                elapsed = time.time() - start_time
                timeout_duration = elapsed
                retry_count = attempt
                last_error = e

                logger.warning(
                    f"Timeout on attempt {attempt}/{max_attempts} for {Path(file_path).name} "
                    f"after {elapsed:.1f}s (threshold={adaptive_timeout:.1f}s)"
                )

                # If not last attempt, wait with exponential backoff
                if attempt < max_attempts:
                    delay = calculate_exponential_backoff(
                        attempt=attempt,
                        base_delay=5.0,
                        multiplier=3.0
                    )
                    logger.info(f"Retrying in {delay:.1f}s...")
                    time.sleep(delay)
                    continue
                else:
                    # Last attempt failed - trigger fallback
                    logger.warning(
                        f"All {max_attempts} attempts failed for {Path(file_path).name}, "
                        f"using structural fallback"
                    )
                    fallback_used = True

            except ConnectionError as e:
                # Ollama unavailable - don't retry, raise immediately
                logger.error(f"Ollama unavailable: {e}")
                raise

            except Exception as e:
                # Other errors - log and continue to fallback
                logger.error(
                    f"Unexpected error on attempt {attempt} for {Path(file_path).name}: {e}"
                )
                retry_count = attempt
                last_error = e
                if attempt >= max_attempts:
                    fallback_used = True

        # If fallback needed, use structural analyzer
        if fallback_used:
            try:
                logger.info(f"Using structural fallback for {Path(file_path).name}")
                analyzer = StructuralAnalyzer()
                structural_metadata = analyzer.extract_basic_metadata(
                    file_path=file_path,
                    file_content=file_content
                )

                # Convert structural metadata to extraction format
                result = {
                    "summary": f"Java class: {structural_metadata.get('class_name', Path(file_path).stem)}",
                    "roles": ["structural_analysis_fallback"],
                    "entities": [structural_metadata.get('class_name', '')],
                    "tags": ["fallback", "structural"],
                    "language": artifact_type.value,
                    "frameworks": [],
                    "concerns": [],
                    "dependencies": structural_metadata.get('imports', [])[:10],  # Limit to 10
                    "metadata": structural_metadata
                }

                extraction_quality = 'structural'
                logger.info(
                    f"Structural fallback successful for {Path(file_path).name}: "
                    f"class={structural_metadata.get('class_name')}, "
                    f"methods={len(structural_metadata.get('methods', []))}"
                )

            except Exception as e:
                logger.error(f"Structural fallback also failed for {Path(file_path).name}: {e}")
                # Return minimal fallback
                result = {
                    "summary": f"Code file: {Path(file_path).name}",
                    "roles": ["fallback_failed"],
                    "entities": [],
                    "tags": ["error"],
                    "language": artifact_type.value,
                    "frameworks": [],
                    "concerns": [],
                    "dependencies": []
                }
                extraction_quality = 'failed'

        # Log timeout metric
        metric = TimeoutMetric(
            file_path=file_path,
            timeout_threshold=adaptive_timeout,
            retry_count=retry_count,
            fallback_used=fallback_used,
            extraction_quality=extraction_quality,
            file_lines=file_lines,
            timeout_duration=timeout_duration,
            error_message=str(last_error) if last_error else None
        )

        # Add metric to global collector
        metrics_collector = get_metrics_collector()
        metrics_collector.add_timeout_metric(metric)

        # Restore original timeout
        self.read_timeout = original_timeout

        return result

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
    model: Optional[str] = None,
    connect_timeout: Optional[float] = None,
    read_timeout: Optional[float] = None
) -> OllamaClient:
    """
    Create Ollama client with configuration from environment.

    Args:
        base_url: Optional override for Ollama URL
        model: Optional override for model name
        connect_timeout: Optional override for connection timeout
        read_timeout: Optional override for read timeout

    Returns:
        Configured OllamaClient instance
    """
    from codeindex.utils.config import get_config

    config = get_config()

    if not base_url:
        base_url = config.ollama_base_url

    if not model:
        model = config.ollama_model_name

    if connect_timeout is None:
        connect_timeout = float(config.ollama_connect_timeout)

    if read_timeout is None:
        read_timeout = float(config.ollama_read_timeout)

    return OllamaClient(
        base_url=base_url,
        model=model,
        connect_timeout=connect_timeout,
        read_timeout=read_timeout
    )
