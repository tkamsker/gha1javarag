"""Ollama LLM client for semantic extraction"""
import json
from typing import Dict, Optional
import httpx
from src.config import Config
from src.utils.logger import setup_logger

logger = setup_logger("ollama_client")


class OllamaClient:
    """Client for interacting with Ollama LLM"""
    
    def __init__(self):
        self.base_url = Config.OLLAMA_BASE_URL
        self.model = Config.OLLAMA_MODEL_NAME
        self.embed_model = Config.OLLAMA_EMBED_MODEL_NAME
        
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate text using Ollama LLM"""
        try:
            url = f"{self.base_url}/api/generate"
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
            if system_prompt:
                payload["system"] = system_prompt
                
            response = httpx.post(url, json=payload, timeout=300.0)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
        except Exception as e:
            logger.error(f"Error generating text with Ollama: {e}")
            return ""
    
    def extract_file_info(self, file_path: str, content: str, file_type: str) -> Dict:
        """Extract structured information from a file using LLM"""
        # Enhanced system prompt for Java files
        if file_type == "java":
            system_prompt = """You are an expert Java code analyzer. Extract detailed structural information.
Identify classes as DAO, DTO, Service, Controller, or Entity based on naming patterns and annotations.
Extract ALL methods with complete signatures and ALL fields with types and annotations.
Return structured JSON with complete class information."""
        else:
            system_prompt = """You are an expert code analyzer. Extract maximum information from code files including:
- Classes, methods, fields, and their relationships
- Business logic, rules, and constraints
- Dependencies and imports
- API endpoints and routes
- Forms, UI elements, and data bindings
- Comments and documentation
- Data models and validation rules

Return your analysis as a JSON object with structured fields."""
        
        # Enhanced prompt for Java files
        if file_type == "java":
            prompt = f"""Analyze this Java file and extract complete structural information:

File Path: {file_path}

File Content:
```
{content[:12000]}
```

Return ONLY valid JSON (no markdown blocks) with this structure:
{{
  "filePath": "{file_path}",
  "fileType": "java",
  "classes": [
    {{
      "name": "FullClassName",
      "type": "class|interface|enum",
      "purpose": "DAO|DTO|Service|Controller|Entity|Other",
      "extends": "SuperClass or null",
      "implements": ["Interface"] or [],
      "annotations": ["@Entity", "@Service", etc.],
      "fields": [
        {{"name": "fieldName", "type": "FieldType", "accessModifier": "private|public", "annotations": []}}
      ],
      "methods": [
        {{"name": "methodName", "returnType": "ReturnType", "parameters": [{{"name": "p", "type": "T"}}], "accessModifier": "public", "annotations": []}}
      ],
      "comment": ""
    }}
  ],
  "imports": [],
  "endpoints": [],
  "businessRules": [],
  "dataModels": [],
  "dependencies": [],
  "comments": []
}}

CRITICAL: Identify class purpose - DAO if name contains "Dao"/"DAO", DTO if ends with "DTO"/"Dto", Service if ends with "Service", Controller if ends with "Controller", Entity if has @Entity. Extract ALL methods and fields."""
        else:
            prompt = f"""Analyze this {file_type} file and extract all relevant information:

File Path: {file_path}

File Content:
```
{content[:8000]}
```

Extract and return a JSON object with:
- filePath: the file path
- fileType: the file type
- classes: list of classes with methods and fields
- imports: list of imports/dependencies
- endpoints: list of API endpoints or routes
- forms: list of forms with fields and validation rules
- businessRules: list of business rules found
- dataModels: list of data models/structures
- uiElements: list of UI elements (for frontend files)
- comments: important comments or documentation
- dependencies: dependencies between components
- metadata: any other relevant metadata

Return only valid JSON, no markdown formatting."""
        
        response = self.generate(prompt, system_prompt)
        
        # Try to extract JSON from response
        try:
            # Remove markdown code blocks if present
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()
            
            extracted_info = json.loads(response)
            extracted_info["filePath"] = file_path
            extracted_info["fileType"] = file_type
            return extracted_info
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse LLM response as JSON for {file_path}")
            # Return a basic structure
            return {
                "filePath": file_path,
                "fileType": file_type,
                "rawAnalysis": response,
                "extractionStatus": "partial"
            }
    
    def get_embedding(self, text: str) -> Optional[list]:
        """Get embedding vector for text using Ollama embeddings API"""
        try:
            if not text or not text.strip():
                logger.warning("Empty text provided for embedding")
                return None
                
            url = f"{self.base_url}/api/embeddings"
            # Ollama embeddings API uses "input" (not "prompt") and accepts string or array
            # Ensure model name includes tag if not present
            model_name = self.embed_model
            if ":" not in model_name:
                model_name = f"{model_name}:latest"
            
            payload = {
                "model": model_name,
                "input": text[:8192]  # Limit text size, use "input" field
            }
            
            response = httpx.post(
                url, 
                json=payload, 
                headers={"Content-Type": "application/json"},
                timeout=60.0
            )
            response.raise_for_status()
            result = response.json()
            
            # Ollama returns embedding in "embedding" field (array of floats)
            embedding = result.get("embedding")
            if embedding and len(embedding) > 0:
                return embedding
            else:
                logger.warning(f"Empty embedding returned from Ollama for model {model_name}")
                # Some versions might return it differently
                if result.get("data") and len(result["data"]) > 0:
                    return result["data"][0].get("embedding")
                return None
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error getting embedding: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"Error getting embedding: {e}")
            return None

