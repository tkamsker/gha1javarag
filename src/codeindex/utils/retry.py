"""
Retry logic with exponential backoff for Java Codebase Indexer Pipeline.

Used for handling transient failures with external services (Weaviate, Ollama).
"""
import time
import functools
import logging
from typing import Callable, TypeVar, Any, Type, Tuple, Optional

logger = logging.getLogger("codeindex.retry")

T = TypeVar('T')


def calculate_exponential_backoff(
    attempt: int,
    base_delay: float = 5.0,
    multiplier: float = 3.0
) -> float:
    """
    Calculate exponential backoff delay for retry attempts.

    Formula: delay = base_delay * (multiplier ** (attempt - 1))
    For attempt=1: 5s, attempt=2: 15s, attempt=3: 45s (with defaults)

    Args:
        attempt: Current attempt number (1-based, NOT 0-based)
        base_delay: Base delay in seconds (default: 5.0)
        multiplier: Exponential multiplier (default: 3.0)

    Returns:
        Delay in seconds for this attempt

    Raises:
        ValueError: If attempt < 1 or parameters are invalid

    Example:
        >>> calculate_exponential_backoff(1, base_delay=5.0, multiplier=3.0)
        5.0
        >>> calculate_exponential_backoff(2, base_delay=5.0, multiplier=3.0)
        15.0
        >>> calculate_exponential_backoff(3, base_delay=5.0, multiplier=3.0)
        45.0
    """
    if attempt < 1:
        raise ValueError(f"attempt must be >= 1, got {attempt}")

    if base_delay <= 0:
        raise ValueError(f"base_delay must be positive, got {base_delay}")

    if multiplier <= 1.0:
        raise ValueError(f"multiplier must be > 1.0, got {multiplier}")

    # Calculate delay: base_delay * (multiplier ** (attempt - 1))
    # attempt=1: base_delay * 1 = base_delay
    # attempt=2: base_delay * multiplier
    # attempt=3: base_delay * multiplier^2
    delay = base_delay * (multiplier ** (attempt - 1))

    return delay


def retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    exponential_base: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """
    Decorator for retrying functions with exponential backoff.

    Args:
        max_attempts: Maximum number of retry attempts (default: 3)
        base_delay: Initial delay in seconds (default: 1.0)
        max_delay: Maximum delay in seconds (default: 30.0)
        exponential_base: Base for exponential backoff (default: 2.0)
        exceptions: Tuple of exception types to catch and retry (default: all exceptions)

    Returns:
        Decorated function with retry logic

    Example:
        @retry(max_attempts=3, base_delay=1.0)
        def call_ollama(prompt: str) -> dict:
            response = httpx.post(...)
            return response.json()
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            attempt = 0
            last_exception = None

            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    last_exception = e

                    if attempt >= max_attempts:
                        logger.error(
                            f"Function {func.__name__} failed after {max_attempts} attempts: {e}"
                        )
                        raise

                    # Calculate delay with exponential backoff
                    delay = min(base_delay * (exponential_base ** (attempt - 1)), max_delay)

                    logger.warning(
                        f"Function {func.__name__} failed (attempt {attempt}/{max_attempts}): {e}. "
                        f"Retrying in {delay:.1f} seconds..."
                    )

                    time.sleep(delay)

            # This should never be reached, but satisfy type checker
            raise last_exception or Exception("Retry failed")

        return wrapper
    return decorator


class RetryContext:
    """
    Context manager for manual retry logic.

    Useful when decorator pattern is not suitable.

    Example:
        retry_ctx = RetryContext(max_attempts=3)
        while retry_ctx.should_retry():
            try:
                result = expensive_operation()
                break
            except Exception as e:
                retry_ctx.record_failure(e)
    """

    def __init__(
        self,
        max_attempts: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 30.0,
        exponential_base: float = 2.0
    ):
        """
        Initialize retry context.

        Args:
            max_attempts: Maximum number of retry attempts
            base_delay: Initial delay in seconds
            max_delay: Maximum delay in seconds
            exponential_base: Base for exponential backoff
        """
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.attempt = 0
        self.last_exception: Optional[Exception] = None

    def should_retry(self) -> bool:
        """
        Check if should attempt/retry operation.

        Returns:
            True if should attempt operation, False if max attempts reached
        """
        return self.attempt < self.max_attempts

    def record_failure(self, exception: Exception):
        """
        Record a failed attempt and sleep before next retry.

        Args:
            exception: Exception that caused the failure
        """
        self.attempt += 1
        self.last_exception = exception

        if self.attempt >= self.max_attempts:
            logger.error(
                f"Operation failed after {self.max_attempts} attempts: {exception}"
            )
            return

        # Calculate delay with exponential backoff
        delay = min(
            self.base_delay * (self.exponential_base ** (self.attempt - 1)),
            self.max_delay
        )

        logger.warning(
            f"Operation failed (attempt {self.attempt}/{self.max_attempts}): {exception}. "
            f"Retrying in {delay:.1f} seconds..."
        )

        time.sleep(delay)

    def reset(self):
        """Reset retry context for reuse."""
        self.attempt = 0
        self.last_exception = None
