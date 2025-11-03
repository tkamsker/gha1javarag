"""Step 2 Agents: Project Structuring & Deep Analysis"""
import json
from typing import Dict, List, Optional
from crewai import Agent, Task
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from src.config import Config
from src.utils.logger import setup_logger
from src.utils.weaviate_client import WeaviateClient
from src.utils.ollama_client import OllamaClient

logger = setup_logger("step2_agents")


class ProjectStructureTool(BaseTool):
    """Tool for structuring project data"""
    name: str = "project_structurer"
    description: str = "Queries Weaviate for all files in a project and builds structured tree"
    
    def __init__(self, weaviate_client: Optional[WeaviateClient] = None, **kwargs):
        super().__init__(**kwargs)
        object.__setattr__(self, '_weaviate', weaviate_client or WeaviateClient())
    
    @property
    def weaviate(self):
        """Get Weaviate client"""
        if not hasattr(self, '_weaviate') or self._weaviate is None:
            object.__setattr__(self, '_weaviate', WeaviateClient())
        return self._weaviate
    
    def _run(self, project: str) -> Dict:
        """Structure project data"""
        files = self.weaviate.query_by_project(project)
        
        structure = {
            "project": project,
            "files": files,
            "entities": {
                "daos": [],
                "dtos": [],
                "services": [],
                "controllers": [],
                "entities": [],
                "ui_files": [],
                "sql_files": []
            },
            "relationships": []
        }
        
        # Categorize files
        dao_names: List[str] = []
        service_names: List[str] = []
        controller_names: List[str] = []
        entity_names: List[str] = []
        for file_info in files:
            file_type = file_info.get("fileType", "")
            extracted = file_info.get("extractedInfo", {})
            
            if file_type == "java":
                classes = extracted.get("classes", [])
                if not classes:
                    logger.debug(f"No classes extracted from {file_info.get('filePath')}")
                
                for cls in classes:
                    class_name = cls.get("name", "").lower()
                    purpose = str(cls.get("purpose", "")).upper()
                    
                    # Enhanced categorization using purpose field and name patterns
                    entity_data = {
                        "className": cls.get("name", ""),
                        "purpose": cls.get("purpose", ""),
                        "filePath": file_info.get("filePath", ""),
                        "methods": cls.get("methods", []),
                        "fields": cls.get("fields", []),
                        "annotations": cls.get("annotations", []),
                        "imports": extracted.get("imports", [])
                    }
                    
                    if purpose == "DAO" or "dao" in class_name or class_name.endswith("dao"):
                        structure["entities"]["daos"].append(entity_data)
                        if entity_data["className"]:
                            dao_names.append(entity_data["className"])
                    elif purpose == "DTO" or "dto" in class_name or class_name.endswith("dto"):
                        structure["entities"]["dtos"].append(entity_data)
                    elif purpose == "SERVICE" or "service" in class_name:
                        structure["entities"]["services"].append(entity_data)
                        if entity_data["className"]:
                            service_names.append(entity_data["className"])
                    elif purpose == "CONTROLLER" or "controller" in class_name:
                        structure["entities"]["controllers"].append(entity_data)
                        if entity_data["className"]:
                            controller_names.append(entity_data["className"])
                    elif purpose == "ENTITY" or "@Entity" in str(cls.get("annotations", [])) or "@entity" in str(cls.get("annotations", [])).lower():
                        structure["entities"]["entities"].append(entity_data)
                        if entity_data["className"]:
                            entity_names.append(entity_data["className"])
                    else:
                        structure["entities"]["entities"].append(entity_data)
                        if entity_data["className"]:
                            entity_names.append(entity_data["className"])
            elif file_type in ["jsp", "html"]:
                structure["entities"]["ui_files"].append(extracted)
            elif file_type == "sql":
                structure["entities"]["sql_files"].append(extracted)

        # Build simple relationships using imports/name hints
        relationships: List[Dict] = []
        dao_set = set(dao_names)
        service_set = set(service_names)
        controller_set = set(controller_names)

        # Map services -> DAOs
        for svc in structure["entities"]["services"]:
            imports = [str(i) for i in (svc.get("imports") or [])]
            targets = set()
            for dao in dao_set:
                if any(dao in imp for imp in imports):
                    targets.add(dao)
            # name-based heuristic
            for dao in dao_set:
                if dao.lower().replace("dao", "") in svc.get("className", "").lower():
                    targets.add(dao)
            for tgt in targets:
                relationships.append({
                    "type": "service_to_dao",
                    "from": svc.get("className"),
                    "to": tgt
                })

        # Map controllers -> Services
        for ctrl in structure["entities"]["controllers"]:
            imports = [str(i) for i in (ctrl.get("imports") or [])]
            targets = set()
            for svc in service_set:
                if any(svc in imp for imp in imports):
                    targets.add(svc)
            for tgt in targets:
                relationships.append({
                    "type": "controller_to_service",
                    "from": ctrl.get("className"),
                    "to": tgt
                })

        structure["relationships"] = relationships
        return structure


class DAODTOAnalyzerTool(BaseTool):
    """Tool for analyzing DAOs and DTOs"""
    name: str = "dao_dto_analyzer"
    description: str = "Extracts data models, constraints, and business rules from DAOs and DTOs"
    
    def __init__(self, ollama_client: Optional[OllamaClient] = None, **kwargs):
        super().__init__(**kwargs)
        object.__setattr__(self, '_ollama', ollama_client or OllamaClient())
    
    @property
    def ollama(self):
        """Get Ollama client"""
        if not hasattr(self, '_ollama') or self._ollama is None:
            object.__setattr__(self, '_ollama', OllamaClient())
        return self._ollama
    
    def _run(self, project_structure: Dict) -> Dict:
        """Analyze DAOs and DTOs"""
        analysis = {
            "dataModels": [],
            "constraints": [],
            "businessRules": [],
            "relationships": []
        }
        
        daos = project_structure.get("entities", {}).get("daos", [])
        dtos = project_structure.get("entities", {}).get("dtos", [])
        
        # Analyze DTOs
        for dto_info in dtos:
            classes = dto_info.get("classes", [])
            for cls in classes:
                model = {
                    "name": cls.get("name", ""),
                    "fields": cls.get("fields", []),
                    "methods": cls.get("methods", []),
                    "annotations": cls.get("annotations", []),
                    "sourceFile": dto_info.get("filePath", "")
                }
                analysis["dataModels"].append(model)
                
                # Extract constraints from annotations
                for annotation in model["annotations"]:
                    if "validation" in str(annotation).lower() or "constraint" in str(annotation).lower():
                        analysis["constraints"].append({
                            "model": model["name"],
                            "constraint": annotation
                        })
        
        # Analyze DAOs
        for dao_info in daos:
            classes = dao_info.get("classes", [])
            for cls in classes:
                methods = cls.get("methods", [])
                for method in methods:
                    # Extract business rules from method names/comments
                    method_name = method.get("name", "").lower()
                    if any(keyword in method_name for keyword in ["validate", "check", "rule", "constraint"]):
                        analysis["businessRules"].append({
                            "source": cls.get("name", ""),
                            "method": method.get("name", ""),
                            "description": method.get("comment", "")
                        })
        
        return analysis


class ServiceLinkerTool(BaseTool):
    """Tool for linking services to DAOs and DTOs"""
    name: str = "service_linker"
    description: str = "Maps service dependencies to DAOs/DTOs and prepares API summaries"
    
    def _run(self, project_structure: Dict, dao_dto_analysis: Dict) -> Dict:
        """Link services to data layer"""
        services = project_structure.get("entities", {}).get("services", [])
        data_models = {m["name"]: m for m in dao_dto_analysis.get("dataModels", [])}
        
        api_summary = {
            "services": [],
            "endpoints": [],
            "dependencies": []
        }
        
        for service_info in services:
            classes = service_info.get("classes", [])
            for cls in classes:
                service = {
                    "name": cls.get("name", ""),
                    "methods": cls.get("methods", []),
                    "dependencies": [],
                    "dataModels": []
                }
                
                # Find dependencies
                imports = service_info.get("imports", [])
                for imp in imports:
                    if any(keyword in imp.lower() for keyword in ["dao", "dto", "model", "entity"]):
                        service["dependencies"].append(imp)
                        
                        # Link to data models
                        for model_name, model in data_models.items():
                            if model_name in imp:
                                service["dataModels"].append(model)
                
                # Extract endpoints from methods
                for method in cls.get("methods", []):
                    annotations = method.get("annotations", [])
                    for annotation in annotations:
                        if "mapping" in str(annotation).lower() or "request" in str(annotation).lower():
                            endpoint = {
                                "service": service["name"],
                                "method": method.get("name", ""),
                                "annotation": str(annotation),
                                "dataModels": service["dataModels"]
                            }
                            api_summary["endpoints"].append(endpoint)
                
                api_summary["services"].append(service)
        
        return api_summary


class FrontendAnalyzerTool(BaseTool):
    """Tool for analyzing frontend files"""
    name: str = "frontend_analyzer"
    description: str = "Analyzes JSP/HTML files to understand forms, layout, and data flow"
    
    def _run(self, project_structure: Dict, service_api: Dict) -> Dict:
        """Analyze frontend files"""
        ui_files = project_structure.get("entities", {}).get("ui_files", [])
        
        frontend_analysis = {
            "pages": [],
            "forms": [],
            "dataBindings": [],
            "uiComponents": []
        }
        
        for ui_file in ui_files:
            extracted = ui_file.get("extractedInfo", {})
            forms = extracted.get("forms", [])
            ui_elements = extracted.get("uiElements", [])
            
            page = {
                "filePath": extracted.get("filePath", ""),
                "forms": forms,
                "uiElements": ui_elements,
                "dataBindings": []
            }
            
            # Link forms to data models
            for form in forms:
                form_fields = form.get("fields", [])
                # Try to match form fields to data models
                for service in service_api.get("services", []):
                    for data_model in service.get("dataModels", []):
                        model_fields = [f.get("name", "") for f in data_model.get("fields", [])]
                        matching_fields = [f for f in form_fields if f.get("name", "") in model_fields]
                        if matching_fields:
                            binding = {
                                "form": form.get("name", ""),
                                "dataModel": data_model["name"],
                                "fields": matching_fields
                            }
                            page["dataBindings"].append(binding)
            
            frontend_analysis["pages"].append(page)
            frontend_analysis["forms"].extend(forms)
            frontend_analysis["uiComponents"].extend(ui_elements)
        
        return frontend_analysis


class LinkageAgentTool(BaseTool):
    """Tool for resolving cross-references"""
    name: str = "linkage_resolver"
    description: str = "Finds and resolves unresolved cross-references between frontend and backend"
    
    def __init__(self, weaviate_client: Optional[WeaviateClient] = None, **kwargs):
        super().__init__(**kwargs)
        object.__setattr__(self, '_weaviate', weaviate_client or WeaviateClient())
    
    @property
    def weaviate(self):
        """Get Weaviate client"""
        if not hasattr(self, '_weaviate') or self._weaviate is None:
            object.__setattr__(self, '_weaviate', WeaviateClient())
        return self._weaviate
    
    def _run(self, project_structure: Dict, frontend_analysis: Dict, service_api: Dict) -> Dict:
        """Resolve linkages"""
        unresolved = []
        resolved = []
        
        # Check for forms without backend mappings
        for page in frontend_analysis.get("pages", []):
            for form in page.get("forms", []):
                form_name = form.get("name", "")
                has_binding = any(b["form"] == form_name for b in page.get("dataBindings", []))
                if not has_binding:
                    unresolved.append({
                        "type": "form_without_backend",
                        "form": form_name,
                        "file": page.get("filePath", "")
                    })
        
        # Try to resolve by searching Weaviate
        for item in unresolved:
            if item["type"] == "form_without_backend":
                # Search for similar patterns in the codebase
                resolved.append({
                    "unresolved": item,
                    "resolution": "requires_manual_review",
                    "confidence": "low"
                })
        
        return {
            "unresolved": unresolved,
            "resolved": resolved,
            "resolution_rate": len(resolved) / len(unresolved) if unresolved else 1.0
        }


def create_step2_agents(weaviate_client: Optional[WeaviateClient] = None,
                        ollama_client: Optional[OllamaClient] = None):
    """Create Step 2 CrewAI agents"""
    
    weaviate = weaviate_client or WeaviateClient()
    ollama = ollama_client or OllamaClient()
    
    project_structurer_tool = ProjectStructureTool(weaviate_client=weaviate)
    dao_dto_analyzer_tool = DAODTOAnalyzerTool(ollama_client=ollama)
    service_linker_tool = ServiceLinkerTool()
    frontend_analyzer_tool = FrontendAnalyzerTool()
    linkage_tool = LinkageAgentTool(weaviate_client=weaviate)
    
    # Skip CrewAI Agent creation - tools are used directly in pipeline
    return {
        "tools": {
            "project_structurer": project_structurer_tool,
            "dao_dto_analyzer": dao_dto_analyzer_tool,
            "service_linker": service_linker_tool,
            "frontend_analyzer": frontend_analyzer_tool,
            "linkage": linkage_tool
        }
    }

