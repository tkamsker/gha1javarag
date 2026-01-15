"""
Configuration management for Java Codebase Indexer Pipeline.

Priority hierarchy: CLI args > environment variables > .env file > defaults
"""
import os
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv


class Config:
    """Central configuration management with priority hierarchy."""

    def __init__(self, config_file: Optional[Path] = None):
        """
        Initialize configuration.

        Args:
            config_file: Path to .env file (default: .env in current directory)
        """
        # Load .env file (doesn't override existing environment variables)
        if config_file and config_file.exists():
            load_dotenv(dotenv_path=config_file, override=False)
        else:
            load_dotenv(override=False)  # Load .env from current directory

    # Required Configuration

    @property
    def java_source_dir(self) -> Optional[Path]:
        """Root directory containing Java source code to analyze."""
        path_str = os.getenv("JAVA_SOURCE_DIR")
        return Path(path_str) if path_str else None

    @property
    def project_subdirectory(self) -> Optional[str]:
        """Project subdirectory within JAVA_SOURCE_DIR for scoped analysis."""
        return os.getenv("PROJECT_SUBDIRECTORY") or None

    @property
    def dependency_depth(self) -> int:
        """Maximum dependency depth to resolve (0=no dependencies, 1=direct only, 2+=transitive)."""
        return int(os.getenv("DEPENDENCY_DEPTH", "1"))

    # Weaviate Configuration

    @property
    def weaviate_url(self) -> str:
        """Weaviate instance URL."""
        return os.getenv("WEAVIATE_URL", "http://localhost:8080")

    @property
    def weaviate_api_key(self) -> Optional[str]:
        """Weaviate API key (optional, for authenticated instances)."""
        return os.getenv("WEAVIATE_API_KEY") or None

    @property
    def weaviate_timeout(self) -> int:
        """Weaviate connection timeout in seconds."""
        return int(os.getenv("WEAVIATE_TIMEOUT", "60"))

    @property
    def weaviate_batch_size(self) -> int:
        """Batch size for Weaviate indexing operations."""
        return int(os.getenv("WEAVIATE_BATCH_SIZE", "50"))

    # Ollama Configuration

    @property
    def ollama_base_url(self) -> str:
        """Ollama base URL."""
        return os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    @property
    def ollama_model_name(self) -> str:
        """Ollama model name for semantic understanding."""
        return os.getenv("OLLAMA_MODEL_NAME", "gemma3:12b")

    @property
    def ollama_timeout(self) -> int:
        """Ollama request timeout in seconds (deprecated, use ollama_read_timeout)."""
        return int(os.getenv("OLLAMA_TIMEOUT", "240"))

    @property
    def ollama_read_timeout(self) -> int:
        """Ollama read timeout for long-running requests in seconds."""
        return int(os.getenv("OLLAMA_READ_TIMEOUT", os.getenv("OLLAMA_TIMEOUT", "240")))

    @property
    def ollama_connect_timeout(self) -> int:
        """Ollama connection timeout in seconds."""
        return int(os.getenv("OLLAMA_CONNECT_TIMEOUT", "10"))

    # Performance Tuning

    @property
    def max_concurrent_ai_calls(self) -> int:
        """Maximum concurrent AI calls to Ollama."""
        return int(os.getenv("MAX_CONCURRENT_AI_CALLS", "10"))

    @property
    def output_dir(self) -> Path:
        """Output directory for intermediate files."""
        path_str = os.getenv("OUTPUT_DIR", "./data")
        return Path(path_str)

    # Logging Configuration

    @property
    def log_level(self) -> str:
        """Logging level (DEBUG, INFO, WARNING, ERROR)."""
        return os.getenv("LOG_LEVEL", "INFO").upper()

    @property
    def verbose_logging(self) -> bool:
        """Enable verbose logging."""
        return os.getenv("VERBOSE_LOGGING", "false").lower() in ("true", "1", "yes")

    # Optional Processing Controls

    @property
    def dry_run(self) -> bool:
        """Enable dry-run mode (process but don't index)."""
        return os.getenv("DRY_RUN", "false").lower() in ("true", "1", "yes")

    @property
    def skip_schema_creation(self) -> bool:
        """Skip Weaviate schema creation (assumes schema exists)."""
        return os.getenv("SKIP_SCHEMA_CREATION", "false").lower() in ("true", "1", "yes")

    @property
    def max_file_bytes(self) -> int:
        """Maximum file size in bytes to process."""
        return int(os.getenv("MAX_FILE_BYTES", "2000000"))

    @property
    def include_file_types(self) -> list[str]:
        """File extensions to include in processing."""
        extensions_str = os.getenv(
            "INCLUDE_FILE_TYPES",
            ".java,.jsp,.xml,.html,.js,.sql,.properties,.json,.md"
        )
        return [ext.strip() for ext in extensions_str.split(",")]

    @property
    def exclude_dirs(self) -> list[str]:
        """Directories to exclude from discovery."""
        dirs_str = os.getenv(
            "EXCLUDE_DIRS",
            ".git,node_modules,build,out,target,dist,.idea,.vscode"
        )
        return [d.strip() for d in dirs_str.split(",")]

    # Embedding Configuration (future use)

    @property
    def embedding_provider(self) -> str:
        """Embedding provider (weaviate_ollama or client)."""
        return os.getenv("EMBEDDING_PROVIDER", "weaviate_ollama")

    @property
    def embedding_model(self) -> str:
        """Model for text2vec-ollama module."""
        return os.getenv("EMBEDDING_MODEL", "nomic-embed-text")

    # Web UI Configuration (Feature 009)

    @property
    def workspace_db_path(self) -> Path:
        """SQLite database path for workspace storage."""
        path_str = os.getenv("WORKSPACE_DB_PATH", "data/workspaces.db")
        return Path(path_str)

    @property
    def annotations_db_path(self) -> Path:
        """SQLite database path for annotations storage."""
        path_str = os.getenv("ANNOTATIONS_DB_PATH", "data/annotations.db")
        return Path(path_str)

    @property
    def export_dir(self) -> Path:
        """Directory for exported reports (PRD, specs, tests)."""
        path_str = os.getenv("EXPORT_DIR", "data/exports")
        return Path(path_str)

    @property
    def streamlit_port(self) -> int:
        """Streamlit server port."""
        return int(os.getenv("STREAMLIT_PORT", "8501"))

    @property
    def streamlit_host(self) -> str:
        """Streamlit server host."""
        return os.getenv("STREAMLIT_HOST", "localhost")

    @property
    def max_concurrent_agents(self) -> int:
        """Maximum concurrent agents for multi-agent workflows."""
        return int(os.getenv("MAX_CONCURRENT_AGENTS", "3"))

    @property
    def auth_enabled(self) -> bool:
        """Enable authentication for web UI."""
        return os.getenv("AUTH_ENABLED", "false").lower() in ("true", "1", "yes")

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary for debugging."""
        return {
            "java_source_dir": str(self.java_source_dir) if self.java_source_dir else None,
            "project_subdirectory": self.project_subdirectory,
            "dependency_depth": self.dependency_depth,
            "weaviate_url": self.weaviate_url,
            "weaviate_batch_size": self.weaviate_batch_size,
            "ollama_base_url": self.ollama_base_url,
            "ollama_model_name": self.ollama_model_name,
            "max_concurrent_ai_calls": self.max_concurrent_ai_calls,
            "output_dir": str(self.output_dir),
            "log_level": self.log_level,
            "dry_run": self.dry_run,
        }

    def validate_required(self) -> list[str]:
        """
        Validate required configuration.

        Returns:
            List of missing required configuration keys (empty if all present)
        """
        missing = []

        if not self.java_source_dir:
            missing.append("JAVA_SOURCE_DIR")
        elif not self.java_source_dir.exists():
            missing.append(f"JAVA_SOURCE_DIR (path does not exist: {self.java_source_dir})")

        return missing


# Global configuration instance
_config: Optional[Config] = None


def get_config(config_file: Optional[Path] = None) -> Config:
    """
    Get global configuration instance.

    Args:
        config_file: Path to .env file (only used on first call)

    Returns:
        Global Config instance
    """
    global _config
    if _config is None:
        _config = Config(config_file)
    return _config


def reset_config():
    """Reset global configuration (useful for testing)."""
    global _config
    _config = None
