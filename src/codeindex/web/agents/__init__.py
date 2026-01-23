"""
Web agents for AI-powered analysis and generation.

This module provides specialized AI agents that use CrewAI for codebase analysis,
documentation generation, and test creation.
"""

from codeindex.services.ollama_client import OllamaClient
from codeindex.utils.config import Config


def get_configured_ollama_client() -> OllamaClient:
    """
    Create an OllamaClient instance with configuration from .env file.

    This ensures all agents use the correct Ollama model and settings
    defined in the .env file (OLLAMA_MODEL_NAME, OLLAMA_BASE_URL, etc.)

    Returns:
        Configured OllamaClient instance

    Example:
        >>> client = get_configured_ollama_client()
        >>> response = client.generate("Explain this code")
    """
    config = Config()
    return OllamaClient(
        base_url=config.ollama_base_url,
        model=config.ollama_model_name,
        connect_timeout=config.ollama_connect_timeout,
        read_timeout=config.ollama_read_timeout
    )


__all__ = [
    "get_configured_ollama_client",
]
