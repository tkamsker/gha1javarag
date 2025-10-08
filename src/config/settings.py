"""
Configuration management for the Java/JSP/GWT/JS → PRD pipeline.
"""
import os
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Source Discovery
    java_source_dir: str = Field(default="/path/to/java/source", env="JAVA_SOURCE_DIR")
    js_include_globs: str = Field(default="**/*.js", env="JS_INCLUDE_GLOBS")
    gwt_include_globs: str = Field(
        default="**/*.gwt.xml,**/*.ui.xml,**/*EntryPoint*.java,**/*Activity*.java,**/*Place*.java,**/*Service*.java,**/*RequestFactory*.java", 
        env="GWT_INCLUDE_GLOBS"
    )
    jsp_include_globs: str = Field(default="**/*.jsp,**/*.jspf", env="JSP_INCLUDE_GLOBS")
    java_include_globs: str = Field(default="**/*.java", env="JAVA_INCLUDE_GLOBS")
    
    # Ollama Configuration
    ollama_model_name: str = Field(default="llama3.1:8b", env="OLLAMA_MODEL_NAME")
    ollama_embed_model_name: str = Field(default="nomic-embed-text", env="OLLAMA_EMBED_MODEL_NAME")
    ollama_base_url: str = Field(default="http://localhost:11434", env="OLLAMA_BASE_URL")
    
    # Weaviate Configuration
    weaviate_url: str = Field(default="http://localhost:8080", env="WEAVIATE_URL")
    weaviate_api_key: Optional[str] = Field(default=None, env="WEAVIATE_API_KEY")
    weaviate_grpc_url: str = Field(default="localhost:50051", env="WEAVIATE_GRPC_URL")
    
    # Heuristics
    gwt_rpc_default_path: str = Field(default="/gwt.rpc", env="GWT_RPC_DEFAULT_PATH")
    gwt_rf_default_path: str = Field(default="/gwtRequest", env="GWT_RF_DEFAULT_PATH")
    js_route_hints: str = Field(default="#/,#/.*,/,/app/.*", env="JS_ROUTE_HINTS")
    js_http_method_hints: str = Field(default="GET,POST,PUT,DELETE,PATCH", env="JS_HTTP_METHOD_HINTS")
    
    # Output Configuration
    output_dir: Path = Field(default=Path("./data/output"), env="OUTPUT_DIR")
    build_dir: Path = Field(default=Path("./data/build"), env="BUILD_DIR")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Project Configuration
    default_project_name: str = Field(default="default-project", env="DEFAULT_PROJECT_NAME")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure output directories exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.build_dir.mkdir(parents=True, exist_ok=True)
    
    def get_js_include_globs(self) -> List[str]:
        """Get JavaScript include globs as a list."""
        return [g.strip() for g in self.js_include_globs.split(',')]
    
    def get_gwt_include_globs(self) -> List[str]:
        """Get GWT include globs as a list."""
        return [g.strip() for g in self.gwt_include_globs.split(',')]
    
    def get_jsp_include_globs(self) -> List[str]:
        """Get JSP include globs as a list."""
        return [g.strip() for g in self.jsp_include_globs.split(',')]
    
    def get_java_include_globs(self) -> List[str]:
        """Get Java include globs as a list."""
        return [g.strip() for g in self.java_include_globs.split(',')]
    
    def get_js_route_hints(self) -> List[str]:
        """Get JavaScript route hints as a list."""
        return [h.strip() for h in self.js_route_hints.split(',')]
    
    def get_js_http_method_hints(self) -> List[str]:
        """Get JavaScript HTTP method hints as a list."""
        return [h.strip() for h in self.js_http_method_hints.split(',')]
        
    def get_java_source_path(self) -> Path:
        """Get the Java source directory as a Path object."""
        return Path(self.java_source_dir)
        
    def is_java_source_valid(self) -> bool:
        """Check if the Java source directory is valid and exists."""
        return self.get_java_source_path().exists() and self.get_java_source_path().is_dir()

# Global settings instance
settings = Settings()
