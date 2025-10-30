"""Configuration management for the pipeline"""
import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Pipeline configuration from environment variables"""
    
    # Source Discovery
    JAVA_SOURCE_DIR: Path = Path(os.getenv("JAVA_SOURCE_DIR", "."))
    JS_INCLUDE_GLOBS: List[str] = os.getenv("JS_INCLUDE_GLOBS", "**/*.js").split(",")
    GWT_INCLUDE_GLOBS: List[str] = os.getenv("GWT_INCLUDE_GLOBS", "").split(",") if os.getenv("GWT_INCLUDE_GLOBS") else []
    JSP_INCLUDE_GLOBS: List[str] = os.getenv("JSP_INCLUDE_GLOBS", "**/*.jsp,**/*.jspf").split(",")
    JAVA_INCLUDE_GLOBS: List[str] = os.getenv("JAVA_INCLUDE_GLOBS", "**/*.java").split(",")
    HTML_INCLUDE_GLOBS: List[str] = os.getenv("HTML_INCLUDE_GLOBS", "**/*.htm,**/*.html").split(",") if os.getenv("HTML_INCLUDE_GLOBS") else []
    XML_INCLUDE_GLOBS: List[str] = os.getenv("XML_INCLUDE_GLOBS", "**/*.xml,**/*.xhtml").split(",") if os.getenv("XML_INCLUDE_GLOBS") else []
    SQL_INCLUDE_GLOBS: List[str] = os.getenv("SQL_INCLUDE_GLOBS", "**/*.sql").split(",") if os.getenv("SQL_INCLUDE_GLOBS") else []
    
    # Ollama Configuration
    OLLAMA_MODEL_NAME: str = os.getenv("OLLAMA_MODEL_NAME", "gemma3:12b")
    OLLAMA_EMBED_MODEL_NAME: str = os.getenv("OLLAMA_EMBED_MODEL_NAME", "nomic-embed-text")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    # Weaviate Configuration
    WEAVIATE_URL: str = os.getenv("WEAVIATE_URL", "http://localhost:8080")
    WEAVIATE_API_KEY: str = os.getenv("WEAVIATE_API_KEY", "")
    WEAVIATE_GRPC_URL: str = os.getenv("WEAVIATE_GRPC_URL", "localhost:50051")
    
    # Heuristics
    GWT_RPC_DEFAULT_PATH: str = os.getenv("GWT_RPC_DEFAULT_PATH", "/gwt.rpc")
    GWT_RF_DEFAULT_PATH: str = os.getenv("GWT_RF_DEFAULT_PATH", "/gwtRequest")
    JS_ROUTE_HINTS: List[str] = os.getenv("JS_ROUTE_HINTS", "#/,#/.*,/,/app/.*").split(",")
    JS_HTTP_METHOD_HINTS: List[str] = os.getenv("JS_HTTP_METHOD_HINTS", "GET,POST,PUT,DELETE,PATCH").split(",")
    
    # Output Configuration
    OUTPUT_DIR: Path = Path(os.getenv("OUTPUT_DIR", "./data/output"))
    BUILD_DIR: Path = Path(os.getenv("BUILD_DIR", "./data/build"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Project Configuration
    DEFAULT_PROJECT_NAME: str = os.getenv("DEFAULT_PROJECT_NAME", "default-project")
    # If true, treat each immediate subdirectory of JAVA_SOURCE_DIR as a separate project,
    # even if the root contains a pom.xml
    FORCE_MULTIPROJECT_DISCOVERY: bool = os.getenv("FORCE_MULTIPROJECT_DISCOVERY", "false").lower() in ("1", "true", "yes", "on")
    
    @classmethod
    def get_all_globs(cls) -> List[str]:
        """Get all file glob patterns to search"""
        all_globs = []
        all_globs.extend(cls.JAVA_INCLUDE_GLOBS)
        all_globs.extend(cls.JS_INCLUDE_GLOBS)
        all_globs.extend(cls.GWT_INCLUDE_GLOBS)
        all_globs.extend(cls.JSP_INCLUDE_GLOBS)
        all_globs.extend(cls.HTML_INCLUDE_GLOBS)
        all_globs.extend(cls.XML_INCLUDE_GLOBS)
        all_globs.extend(cls.SQL_INCLUDE_GLOBS)
        return [g.strip() for g in all_globs if g.strip()]
    
    @classmethod
    def ensure_output_dirs(cls):
        """Create output directories if they don't exist"""
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        cls.BUILD_DIR.mkdir(parents=True, exist_ok=True)
        (cls.OUTPUT_DIR / "logs").mkdir(exist_ok=True)

