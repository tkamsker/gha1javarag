"""Step 1 Agents: Source Discovery & AI Extraction"""
from pathlib import Path
from typing import List, Dict, Optional
from crewai import Agent, Task
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from src.config import Config
from src.utils.logger import setup_logger
from src.utils.ollama_client import OllamaClient
from src.utils.weaviate_client import WeaviateClient

logger = setup_logger("step1_agents")


class ProjectDiscoveryInput(BaseModel):
    """Input for project discovery"""
    source_dir: str = Field(description="Source directory to search")


class FileExtractionInput(BaseModel):
    """Input for file extraction"""
    file_path: str = Field(description="Path to file to extract")
    project: str = Field(description="Project name")


class SourceReaderTool(BaseTool):
    """Tool for discovering source files"""
    name: str = "source_reader"
    description: str = "Discovers all source files matching patterns and determines project boundaries"
    
    def _run(self, source_dir: str) -> Dict:
        """Discover source files and projects"""
        source_path = Path(source_dir)
        projects = {}
        
        # Decide discovery mode
        root_has_pom = (source_path / "pom.xml").exists()
        force_multi = getattr(Config, "FORCE_MULTIPROJECT_DISCOVERY", False)
        if root_has_pom and not force_multi:
            # Single-project mode (root pom.xml present and not overridden)
            project_name = source_path.name or Config.DEFAULT_PROJECT_NAME
            files = self._find_files(source_path, project_name)
            projects[project_name] = files
        else:
            # Multi-project mode - each immediate directory is a project
            for dir_item in source_path.iterdir():
                if dir_item.is_dir():
                    files = self._find_files(dir_item, dir_item.name)
                    if files:
                        projects[dir_item.name] = files
        
        return {
            "projects": projects,
            "total_files": sum(len(files) for files in projects.values())
        }
    def _find_files(self, directory: Path, project: str) -> List[Dict]:
        """Find all relevant files in directory"""
        files = []
        globs = Config.get_all_globs()
        
        for glob_pattern in globs:
            try:
                # Use glob pattern as-is; do not lstrip characters (that breaks patterns like **/*.java)
                found_files = list(directory.rglob(glob_pattern))
                for file_path in found_files:
                    if file_path.is_file():
                        file_type = self._determine_file_type(file_path)
                        files.append({
                            "path": str(file_path),
                            "relative_path": str(file_path.relative_to(directory)),
                            "type": file_type,
                            "project": project
                        })
            except Exception as e:
                logger.warning(f"Error with glob {glob_pattern}: {e}")
        
        # Remove duplicates
        seen = set()
        unique_files = []
        for f in files:
            key = f["path"]
            if key not in seen:
                seen.add(key)
                unique_files.append(f)
        
        return unique_files
    
    def _determine_file_type(self, file_path: Path) -> str:
        """Determine file type from extension"""
        ext = file_path.suffix.lower()
        if ext == ".java":
            return "java"
        elif ext == ".js":
            return "javascript"
        elif ext in [".jsp", ".jspf"]:
            return "jsp"
        elif ext in [".html", ".htm"]:
            return "html"
        elif ext == ".xml":
            return "xml"
        elif ext == ".sql":
            return "sql"
        else:
            return "unknown"


class FileExtractorTool(BaseTool):
    """Tool for extracting information from files using LLM"""
    name: str = "file_extractor"
    description: str = "Extracts structured information from files using AI analysis"
    
    def __init__(self, ollama_client: Optional[OllamaClient] = None, **kwargs):
        super().__init__(**kwargs)
        # Store as private attribute to avoid Pydantic validation
        object.__setattr__(self, '_ollama', ollama_client or OllamaClient())
    
    @property
    def ollama(self):
        """Get Ollama client"""
        if not hasattr(self, '_ollama') or self._ollama is None:
            object.__setattr__(self, '_ollama', OllamaClient())
        return self._ollama
    
    def _run(self, file_path: str, project: str) -> Dict:
        """Extract information from file"""
        path = Path(file_path)
        if not path.exists():
            return {"error": f"File not found: {file_path}"}
        
        try:
            content = path.read_text(encoding='utf-8', errors='ignore')
            file_type = self._determine_file_type(path)
            
            logger.info(f"Extracting from {file_path} ({file_type})")
            extracted_info = self.ollama.extract_file_info(
                str(file_path),
                content,
                file_type
            )
            
            # Add file metadata
            extracted_info["fileSize"] = len(content)
            extracted_info["lineCount"] = len(content.splitlines())
            extracted_info["project"] = project
            
            return extracted_info
        except Exception as e:
            logger.error(f"Error extracting from {file_path}: {e}")
            return {
                "filePath": file_path,
                "project": project,
                "error": str(e),
                "extractionStatus": "failed"
            }
    
    def _determine_file_type(self, file_path: Path) -> str:
        """Determine file type"""
        ext = file_path.suffix.lower()
        type_map = {
            ".java": "java",
            ".js": "javascript",
            ".jsp": "jsp",
            ".jspf": "jsp",
            ".html": "html",
            ".htm": "html",
            ".xml": "xml",
            ".xhtml": "xml",
            ".sql": "sql"
        }
        return type_map.get(ext, "unknown")


class DataStoreTool(BaseTool):
    """Tool for storing extracted data in Weaviate"""
    name: str = "data_store"
    description: str = "Stores extracted file information in Weaviate vector database"
    
    def __init__(self, weaviate_client: Optional[WeaviateClient] = None,
                 ollama_client: Optional[OllamaClient] = None, **kwargs):
        super().__init__(**kwargs)
        # Store as private attributes to avoid Pydantic validation
        object.__setattr__(self, '_weaviate', weaviate_client or WeaviateClient())
        object.__setattr__(self, '_ollama', ollama_client or OllamaClient())
    
    @property
    def weaviate(self):
        """Get Weaviate client"""
        if not hasattr(self, '_weaviate') or self._weaviate is None:
            object.__setattr__(self, '_weaviate', WeaviateClient())
        return self._weaviate
    
    @property
    def ollama(self):
        """Get Ollama client"""
        if not hasattr(self, '_ollama') or self._ollama is None:
            object.__setattr__(self, '_ollama', OllamaClient())
        return self._ollama
    
    def _run(self, file_path: str, project: str, file_type: str, extracted_info: Dict) -> str:
        """Store extracted information"""
        try:
            # Generate embedding for the file
            content_for_embedding = self._prepare_content_for_embedding(extracted_info, file_path)
            embedding = self.ollama.get_embedding(content_for_embedding)
            
            uuid = self.weaviate.store_file_extraction(
                file_path=file_path,
                project=project,
                file_type=file_type,
                extracted_info=extracted_info,
                embedding=embedding
            )
            
            logger.info(f"Stored {file_path} in Weaviate with UUID: {uuid}")
            return uuid
        except Exception as e:
            logger.error(f"Error storing {file_path}: {e}")
            return ""
    
    def _prepare_content_for_embedding(self, extracted_info: Dict, file_path: str) -> str:
        """Prepare rich, code-aware content for embedding.
        Prefers structured data; falls back to file head if sparse.
        """
        parts: List[str] = []
        # Always include basics
        try:
            parts.append(f"filePath: {extracted_info.get('filePath') or file_path}")
            if extracted_info.get("fileType"):
                parts.append(f"fileType: {extracted_info.get('fileType')}")
        except Exception:
            parts.append(f"filePath: {file_path}")

        # Classes, annotations, methods
        classes = extracted_info.get("classes") or []
        if isinstance(classes, list) and classes:
            for cls in classes[:8]:  # cap per-file to keep payload compact
                name = cls.get("name") if isinstance(cls, dict) else None
                ctype = cls.get("type") if isinstance(cls, dict) else None
                purpose = cls.get("purpose") if isinstance(cls, dict) else None
                ann = cls.get("annotations") if isinstance(cls, dict) else None
                if name:
                    parts.append(f"class: {name} type:{ctype or ''} purpose:{purpose or ''} ann:{','.join(ann or [])}")
                methods = cls.get("methods") if isinstance(cls, dict) else None
                if isinstance(methods, list) and methods:
                    for m in methods[:12]:
                        mname = m.get("name")
                        rtype = m.get("returnType")
                        params = m.get("parameters") or []
                        pstr = ",".join([f"{p.get('type')} {p.get('name')}" for p in params if isinstance(p, dict)])
                        parts.append(f"method: {mname} returns:{rtype} params:{pstr}")

        # Imports / dependencies if present
        imports = extracted_info.get("imports")
        if isinstance(imports, list) and imports:
            parts.append("imports: " + ",".join(imports[:20]))

        # Business rules / data models (concise)
        if extracted_info.get("businessRules"):
            parts.append(f"businessRules: {str(extracted_info.get('businessRules'))[:512]}")
        if extracted_info.get("dataModels"):
            parts.append(f"dataModels: {str(extracted_info.get('dataModels'))[:512]}")

        # If still sparse, fallback to file head content
        combined = "\n".join([p for p in parts if p])
        if len(combined) < 64:
            try:
                head = Path(file_path).read_text(encoding='utf-8', errors='ignore')[:8192]
                combined = f"filePath: {file_path}\n{head}"
            except Exception:
                pass
        return combined


def create_step1_agents(ollama_client: Optional[OllamaClient] = None,
                        weaviate_client: Optional[WeaviateClient] = None):
    """Create Step 1 CrewAI agents"""
    
    ollama = ollama_client or OllamaClient()
    weaviate = weaviate_client or WeaviateClient()
    
    source_reader_tool = SourceReaderTool()
    file_extractor_tool = FileExtractorTool(ollama_client=ollama)
    data_store_tool = DataStoreTool(weaviate_client=weaviate, ollama_client=ollama)
    
    # Skip CrewAI Agent creation - tools are used directly in pipeline
    # Agent creation has version compatibility issues, but tools work fine
    return {
        "tools": {
            "source_reader": source_reader_tool,
            "file_extractor": file_extractor_tool,
            "data_store": data_store_tool
        }
    }

