"""Step 3 Agents: Requirements Synthesis & Target Solution Mapping"""
import json
from typing import Dict, List, Optional
from crewai import Agent, Task
from langchain_core.tools import BaseTool
from pathlib import Path

from src.config import Config
from src.utils.logger import setup_logger
from src.utils.ollama_client import OllamaClient

logger = setup_logger("step3_agents")


class RequirementsWriterTool(BaseTool):
    """Tool for writing requirements documents"""
    name: str = "requirements_writer"
    description: str = "Writes detailed requirements documents in Markdown format"
    
    def __init__(self, ollama_client: Optional[OllamaClient] = None, **kwargs):
        super().__init__(**kwargs)
        object.__setattr__(self, '_ollama', ollama_client or OllamaClient())
    
    @property
    def ollama(self):
        """Get Ollama client"""
        if not hasattr(self, '_ollama') or self._ollama is None:
            object.__setattr__(self, '_ollama', OllamaClient())
        return self._ollama
    
    def _run(self, project: str, structured_data: Dict) -> str:
        """Write requirements document"""
        prompt = f"""Create a comprehensive requirements document for project: {project}

Based on this structured data:
{self._format_structured_data(structured_data)}

Write a detailed Markdown requirements document with the following sections:
1. Overview
2. Frontend Requirements
   - Pages and Components
   - Forms and User Interactions
   - Data Bindings
   - UI/UX Patterns
3. Backend Services
   - API Endpoints
   - Service Methods
   - Business Logic
4. Data Models
   - Entities and DTOs
   - Relationships
   - Validation Rules
5. Integration Points
   - Frontend-Backend Mappings
   - Data Flow

Be detailed and reference specific components from the structured data."""
        
        requirements_md = self.ollama.generate(prompt)
        
        # Save to file
        output_dir = Config.OUTPUT_DIR / project
        output_dir.mkdir(parents=True, exist_ok=True)
        requirements_file = output_dir / "requirements.md"
        requirements_file.write_text(requirements_md, encoding='utf-8')
        
        logger.info(f"Requirements written to {requirements_file}")
        return str(requirements_file)
    
    def _format_structured_data(self, data: Dict) -> str:
        """Format structured data for prompt"""
        import json
        return json.dumps(data, indent=2)[:4000]  # Limit size


class SolutionMappingTool(BaseTool):
    """Tool for mapping requirements to target solution"""
    name: str = "solution_mapper"
    description: str = "Maps legacy requirements to Next.js/NestJS microservices architecture"
    
    def __init__(self, ollama_client: Optional[OllamaClient] = None, **kwargs):
        super().__init__(**kwargs)
        object.__setattr__(self, '_ollama', ollama_client or OllamaClient())
    
    @property
    def ollama(self):
        """Get Ollama client"""
        if not hasattr(self, '_ollama') or self._ollama is None:
            object.__setattr__(self, '_ollama', OllamaClient())
        return self._ollama
    
    def _run(self, project: str, requirements_file: str) -> str:
        """Create solution mapping document"""
        requirements_content = Path(requirements_file).read_text(encoding='utf-8')
        
        # Load structured JSON data for comprehensive mapping
        requirements_json_file = Config.OUTPUT_DIR / project / "requirements_json.json"
        structured_data = {}
        if requirements_json_file.exists():
            try:
                structured_data = json.loads(requirements_json_file.read_text(encoding='utf-8'))
            except Exception as e:
                logger.warning(f"Could not load structured data: {e}")
        
        # Extract all entities from structured data
        structure = structured_data.get("structure", {})
        entities = structure.get("entities", {})
        
        # Build comprehensive entity lists
        daos = entities.get("daos", [])
        dtos = entities.get("dtos", [])
        services = entities.get("services", [])
        controllers = entities.get("controllers", [])
        entity_classes = entities.get("entities", [])
        ui_files = entities.get("ui_files", [])
        sql_files = entities.get("sql_files", [])
        
        # Format entity information for prompt
        entity_summary = []
        
        if daos:
            entity_summary.append(f"\n## DAOs ({len(daos)} found):")
            for dao in daos:
                name = dao.get("className", "Unknown")
                methods = dao.get("methods", [])
                entity_summary.append(f"- {name}: {len(methods)} methods")
                for method in methods[:5]:  # Show first 5 methods
                    params = ", ".join([p.get("name", "") for p in method.get("parameters", [])])
                    entity_summary.append(f"  * {method.get('name', '')}({params}): {method.get('returnType', 'void')}")
        
        if dtos:
            entity_summary.append(f"\n## DTOs ({len(dtos)} found):")
            for dto in dtos:
                name = dto.get("className", "Unknown")
                fields = dto.get("fields", [])
                entity_summary.append(f"- {name}: {len(fields)} fields")
                for field in fields[:5]:  # Show first 5 fields
                    entity_summary.append(f"  * {field.get('name', '')}: {field.get('type', '')}")
        
        if services:
            entity_summary.append(f"\n## Services ({len(services)} found):")
            for svc in services:
                name = svc.get("className", "Unknown")
                methods = svc.get("methods", [])
                entity_summary.append(f"- {name}: {len(methods)} methods")
                for method in methods[:5]:
                    params = ", ".join([p.get("name", "") for p in method.get("parameters", [])])
                    entity_summary.append(f"  * {method.get('name', '')}({params}): {method.get('returnType', 'void')}")
        
        if controllers:
            entity_summary.append(f"\n## Controllers ({len(controllers)} found):")
            for ctrl in controllers:
                name = ctrl.get("className", "Unknown")
                methods = ctrl.get("methods", [])
                entity_summary.append(f"- {name}: {len(methods)} methods")
        
        if entity_classes:
            entity_summary.append(f"\n## Other Entities ({len(entity_classes)} found):")
            for ent in entity_classes[:10]:  # Limit to first 10
                name = ent.get("className", "Unknown")
                entity_summary.append(f"- {name}")
        
        if ui_files:
            entity_summary.append(f"\n## UI Files ({len(ui_files)} found):")
            for ui_file in ui_files[:10]:
                path = ui_file.get("filePath", "Unknown")
                entity_summary.append(f"- {path}")
        
        if sql_files:
            entity_summary.append(f"\n## SQL Files ({len(sql_files)} found):")
            for sql_file in sql_files[:10]:
                path = sql_file.get("filePath", "Unknown")
                entity_summary.append(f"- {path}")
        
        entity_list_text = "\n".join(entity_summary) if entity_summary else "\nNo entities extracted from structured data."
        
        prompt = f"""Analyze these requirements and create a COMPREHENSIVE migration mapping to Next.js + NestJS microservices.

Requirements Document:
{requirements_content[:8000]}

Extracted System Components (YOU MUST MAP ALL OF THESE):
{entity_list_text}

Create a detailed mapping document that covers ALL components listed above. The document must include:

1. Frontend Migration (Next.js React)
   - Map EACH JSP/GWT page/component to Next.js React components
   - List ALL forms and their React equivalents
   - Map ALL data bindings to React hooks and API calls
   - Include component hierarchy and relationships
   
2. Backend Migration (NestJS Microservices)
   - Map EACH Service class to NestJS service modules
   - Map EACH DAO to NestJS repositories (currently {len(daos)} DAOs found)
   - Map EACH Controller to NestJS controllers
   - Define API endpoints for ALL service methods from ALL DAOs
   - Create RESTful API contracts for each endpoint
   
3. Data Layer Migration
   - Map EACH DTO ({len(dtos)} found) to TypeScript interfaces
   - Map EACH Entity ({len(entity_classes)} found) to TypeORM entities
   - Define database relationships and constraints
   - Include data transformation logic
   
4. Complete API Mapping
   - For EACH DAO method, define:
     * HTTP method (GET, POST, PUT, DELETE)
     * Endpoint path
     * Request/Response DTOs
     * Error handling
   - List ALL endpoints, don't stop after one or two
   
5. Security & Authentication
   - OAuth 2.0 implementation strategy
   - JWT token handling for all endpoints
   - API security policies
   - Authorization rules per endpoint

CRITICAL REQUIREMENTS:
- Do NOT stop after mapping one component. You MUST map ALL {len(daos)} DAOs, ALL {len(dtos)} DTOs, ALL {len(services)} Services, and ALL {len(controllers)} Controllers.
- Create a complete mapping table for ALL DAO methods to REST endpoints
- List ALL components systematically, one by one
- Be comprehensive - if there are multiple similar components, map each one individually"""
        
        mapping_md = self.ollama.generate(prompt)
        
        # Save to file
        output_dir = Config.OUTPUT_DIR / project
        mapping_file = output_dir / "mapping.md"
        mapping_file.write_text(mapping_md, encoding='utf-8')
        
        logger.info(f"Mapping document written to {mapping_file}")
        return str(mapping_file)


class ReviewTool(BaseTool):
    """Tool for reviewing requirements completeness"""
    name: str = "requirements_reviewer"
    description: str = "Reviews requirements for completeness and consistency"
    
    def __init__(self, ollama_client: Optional[OllamaClient] = None, **kwargs):
        super().__init__(**kwargs)
        object.__setattr__(self, '_ollama', ollama_client or OllamaClient())
    
    @property
    def ollama(self):
        """Get Ollama client"""
        if not hasattr(self, '_ollama') or self._ollama is None:
            object.__setattr__(self, '_ollama', OllamaClient())
        return self._ollama
    
    def _run(self, requirements_file: str, mapping_file: str) -> Dict:
        """Review requirements and mapping"""
        requirements_content = Path(requirements_file).read_text(encoding='utf-8')
        mapping_content = Path(mapping_file).read_text(encoding='utf-8')
        
        prompt = f"""Review these requirements and mapping documents for completeness and consistency:

Requirements:
{requirements_content[:4000]}

Mapping:
{mapping_content[:4000]}

Identify:
1. Missing components or endpoints
2. Inconsistencies between requirements and mapping
3. Unclear or ambiguous sections
4. Security concerns
5. Gaps in data flow documentation

Return a structured review with issues and recommendations."""
        
        review = self.ollama.generate(prompt)
        
        return {
            "review": review,
            "requirements_file": requirements_file,
            "mapping_file": mapping_file
        }


def create_step3_agents(ollama_client: Optional[OllamaClient] = None):
    """Create Step 3 CrewAI agents"""
    
    ollama = ollama_client or OllamaClient()
    
    requirements_writer_tool = RequirementsWriterTool(ollama_client=ollama)
    solution_mapper_tool = SolutionMappingTool(ollama_client=ollama)
    review_tool = ReviewTool(ollama_client=ollama)
    
    # Skip CrewAI Agent creation - tools are used directly in pipeline
    return {
        "tools": {
            "requirements_writer": requirements_writer_tool,
            "solution_mapper": solution_mapper_tool,
            "reviewer": review_tool
        }
    }

