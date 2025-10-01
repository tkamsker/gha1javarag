"""
Environment configuration loader for the Java codebase analysis tool.
Loads and validates configuration from .env file.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv


class Config:
    """Configuration class that loads and validates environment variables."""
    
    def __init__(self, env_file: Optional[str] = None):
        """Initialize configuration from environment file."""
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()
        
        self._load_config()
        self._validate_config()
    
    def _load_config(self) -> None:
        """Load all configuration values from environment variables."""
        # Core Paths
        self.java_source_dir = os.getenv('JAVA_SOURCE_DIR', '')
        self.output_dir = os.getenv('OUTPUT_DIR', './output')
        
        # Weaviate Configuration
        self.weaviate_url = os.getenv('WEAVIATE_URL', 'http://localhost:8080')
        self.weaviate_api_key = os.getenv('WEAVIATE_API_KEY', '')
        self.weaviate_timeout = int(os.getenv('WEAVIATE_TIMEOUT', '60'))
        self.weaviate_batch_size = int(os.getenv('WEAVIATE_BATCH_SIZE', '256'))
        
        # Embedding Configuration
        self.embedding_provider = os.getenv('EMBEDDING_PROVIDER', 'weaviate_ollama')
        self.embedding_model = os.getenv('EMBEDDING_MODEL', 'nomic-embed-text')
        
        # AI Provider Configuration
        self.ai_provider = os.getenv('AI_PROVIDER', 'ollama')
        
        # OpenAI Configuration
        self.openai_api_key = os.getenv('OPENAI_API_KEY', '')
        self.openai_api_base = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')
        self.openai_api_type = os.getenv('OPENAI_API_TYPE', 'openai')
        self.openai_api_version = os.getenv('OPENAI_API_VERSION', '2024-02-15-preview')
        self.openai_model_name = os.getenv('OPENAI_MODEL_NAME', 'gpt-4o')
        self.openai_embed_model = os.getenv('OPENAI_EMBED_MODEL', 'text-embedding-3-large')
        
        # Ollama Configuration
        self.ollama_base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.ollama_model_name = os.getenv('OLLAMA_MODEL_NAME', 'danielsheep/Qwen3-Coder-30B-A3B-Instruct-1M-Unsloth')
        self.ollama_timeout = int(os.getenv('OLLAMA_TIMEOUT', '240'))
        self.local_embed_url = os.getenv('LOCAL_EMBED_URL', 'http://localhost:11435/embed')
        self.local_embed_model = os.getenv('LOCAL_EMBED_MODEL', 'nomic-embed-text')
        
        # Anthropic Configuration
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY', '')
        self.anthropic_api_base = os.getenv('ANTHROPIC_API_BASE', 'https://api.anthropic.com')
        self.anthropic_model_name = os.getenv('ANTHROPIC_MODEL_NAME', 'claude-3-5-sonnet-20240620')
        
        # Processing Controls
        self.max_file_bytes = int(os.getenv('MAX_FILE_BYTES', '2000000'))
        self.include_file_types = os.getenv('INCLUDE_FILE_TYPES', 
            '.java,.jsp,.tsp,.xml,.html,.js,.sql,.properties,.json,.md,.css,.ui.xml,.gwt.xml').split(',')
        self.exclude_dirs = os.getenv('EXCLUDE_DIRS', 
            '.git,node_modules,build,out,target,dist,.idea,.vscode,.gradle').split(',')
        
        # Rate Limiting
        self.rate_limit_env = os.getenv('RATE_LIMIT_ENV', 'development')
        
        # Logging
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.verbose_logging = os.getenv('VERBOSE_LOGGING', 'false').lower() == 'true'
        
        # Performance Tuning
        self.max_workers = int(os.getenv('MAX_WORKERS', '4'))
        self.chunk_overlap_percent = int(os.getenv('CHUNK_OVERLAP_PERCENT', '15'))
        self.max_retries = int(os.getenv('MAX_RETRIES', '3'))
        
        # Development/Testing
        self.dry_run = os.getenv('DRY_RUN', 'false').lower() == 'true'
        self.skip_schema_creation = os.getenv('SKIP_SCHEMA_CREATION', 'false').lower() == 'true'
        self.generate_sample_data = os.getenv('GENERATE_SAMPLE_DATA', 'false').lower() == 'true'
    
    def _validate_config(self) -> None:
        """Validate required configuration values."""
        if not self.java_source_dir:
            raise ValueError("JAVA_SOURCE_DIR is required but not set")
        
        if not Path(self.java_source_dir).exists():
            raise ValueError(f"JAVA_SOURCE_DIR does not exist: {self.java_source_dir}")
        
        if self.embedding_provider not in ['weaviate_ollama', 'client']:
            raise ValueError(f"Invalid EMBEDDING_PROVIDER: {self.embedding_provider}")
        
        if self.ai_provider not in ['openai', 'ollama', 'anthropic']:
            raise ValueError(f"Invalid AI_PROVIDER: {self.ai_provider}")
        
        if self.rate_limit_env not in ['production', 'development', 'test', 'emergency']:
            raise ValueError(f"Invalid RATE_LIMIT_ENV: {self.rate_limit_env}")
    
    def get_weaviate_config(self) -> Dict[str, Any]:
        """Get Weaviate-specific configuration."""
        config = {
            'url': self.weaviate_url,
            'timeout': self.weaviate_timeout,
            'batch_size': self.weaviate_batch_size
        }
        if self.weaviate_api_key:
            config['api_key'] = self.weaviate_api_key
        return config
    
    def get_ai_config(self) -> Dict[str, Any]:
        """Get AI provider-specific configuration."""
        if self.ai_provider == 'openai':
            return {
                'provider': 'openai',
                'api_key': self.openai_api_key,
                'api_base': self.openai_api_base,
                'api_type': self.openai_api_type,
                'api_version': self.openai_api_version,
                'model_name': self.openai_model_name,
                'embed_model': self.openai_embed_model
            }
        elif self.ai_provider == 'ollama':
            return {
                'provider': 'ollama',
                'base_url': self.ollama_base_url,
                'model_name': self.ollama_model_name,
                'timeout': self.ollama_timeout,
                'embed_url': self.local_embed_url,
                'embed_model': self.local_embed_model
            }
        elif self.ai_provider == 'anthropic':
            return {
                'provider': 'anthropic',
                'api_key': self.anthropic_api_key,
                'api_base': self.anthropic_api_base,
                'model_name': self.anthropic_model_name
            }
        else:
            raise ValueError(f"Unsupported AI provider: {self.ai_provider}")
    
    def get_embedding_config(self) -> Dict[str, Any]:
        """Get embedding-specific configuration."""
        if self.embedding_provider == 'weaviate_ollama':
            return {
                'provider': 'weaviate_ollama',
                'model': self.embedding_model
            }
        elif self.embedding_provider == 'client':
            ai_config = self.get_ai_config()
            return {
                'provider': 'client',
                'embed_url': ai_config.get('embed_url', ''),
                'embed_model': ai_config.get('embed_model', ''),
                'api_key': ai_config.get('api_key', '')
            }
        else:
            raise ValueError(f"Unsupported embedding provider: {self.embedding_provider}")


def load_config(env_file: Optional[str] = None) -> Config:
    """Load and return configuration instance."""
    return Config(env_file)
