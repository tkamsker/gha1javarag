"""Tools for documentation generation."""

from typing import Dict, List, Any
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import lxml.etree as ET
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

# Define input schemas for each tool
class ParseXMLInput(BaseModel):
    xml_path: str = Field(..., description="Path to the XML file to parse")

class ExtractEntitiesInput(BaseModel):
    xml_content: dict = Field(..., description="Parsed XML content to extract entities from")

class BuildCallGraphInput(BaseModel):
    entities: list = Field(..., description="List of entities to build call graph from")

# Define minimal custom BaseTool implementations with args_schema
class ParseXMLTool(BaseTool):
    name = "parse_xml"
    description = "Parse Doxygen XML files and extract entity details."
    args_schema: type[BaseModel] = ParseXMLInput

    def _run(self, xml_path: str) -> dict:
        """Parse XML file and extract entity details."""
        try:
            logger.info(f"Attempting to parse XML file: {xml_path}")
            if not os.path.exists(xml_path):
                logger.error(f"XML file does not exist: {xml_path}")
                return {"status": "error", "message": f"XML file does not exist: {xml_path}"}

            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            # Extract compound information
            compound = root.find(".//compounddef")
            if compound is None:
                return {"status": "error", "message": "No compounddef found"}
            
            # Get basic entity information
            name_elem = compound.find("compoundname")
            name = name_elem.text if name_elem is not None else ""
            
            # Get description
            desc_elem = compound.find("briefdescription")
            description = ET.tostring(desc_elem, encoding="unicode", method="text") if desc_elem is not None else ""
            
            # Get location
            location = compound.find("location")
            file_path = location.get("file", "") if location is not None else ""
            
            # Get dependencies
            dependencies = []
            for base in compound.findall(".//basecompoundref"):
                if base.text:
                    dependencies.append(base.text)
            
            # Get parameters for functions
            parameters = []
            for param in compound.findall(".//param"):
                param_dict = {}
                name_elem = param.find("paramname")
                type_elem = param.find("type")
                if name_elem is not None and type_elem is not None:
                    param_dict["name"] = name_elem.text
                    param_dict["type"] = ET.tostring(type_elem, encoding="unicode", method="text")
                    parameters.append(param_dict)
            
            # Get return type
            return_type = None
            type_elem = compound.find(".//type")
            if type_elem is not None:
                return_type = ET.tostring(type_elem, encoding="unicode", method="text")
            
            # Get modifiers
            modifiers = []
            if compound.get("prot", ""):
                modifiers.append(compound.get("prot"))
            if compound.get("virt", "") == "virtual":
                modifiers.append("virtual")
            if compound.get("static", "") == "yes":
                modifiers.append("static")
            
            return {
                "status": "success",
                "entity": {
                    "name": name,
                    "description": description,
                    "file_path": file_path,
                    "dependencies": dependencies,
                    "parameters": parameters,
                    "return_type": return_type,
                    "modifiers": modifiers
                }
            }
        except Exception as e:
            logger.error(f"Error parsing XML {xml_path}: {str(e)} | CWD: {os.getcwd()}")
            return {"status": "error", "message": str(e)}

    def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async not implemented")

class ExtractEntitiesTool(BaseTool):
    name = "extract_entities"
    description = "Extract code entities from parsed XML."
    args_schema: type[BaseModel] = ExtractEntitiesInput

    def _run(self, xml_content: dict) -> list:
        """Extract entities from parsed XML content."""
        if xml_content["status"] != "success":
            return []
        
        entity = xml_content["entity"]
        return [{
            "name": entity["name"],
            "description": entity["description"],
            "type": "class" if "class" in entity["name"].lower() else "function",
            "dependencies": entity["dependencies"],
            "parameters": entity["parameters"],
            "return_type": entity["return_type"],
            "modifiers": entity["modifiers"]
        }]

    def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async not implemented")

class BuildCallGraphTool(BaseTool):
    name = "build_call_graph"
    description = "Build call graph from extracted entities."
    args_schema: type[BaseModel] = BuildCallGraphInput

    def _run(self, entities: list) -> dict:
        """Build call graph from entities."""
        graph = {}
        
        # Initialize graph with all entities
        for entity in entities:
            graph[entity["name"]] = {
                "calls": [],
                "called_by": []
            }
        
        # Build relationships
        for entity in entities:
            # Add dependencies as calls
            for dep in entity.get("dependencies", []):
                if dep in graph:
                    graph[entity["name"]]["calls"].append(dep)
                    graph[dep]["called_by"].append(entity["name"])
        
        return {"graph": graph}

    def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async not implemented")

# Create tool instances
parse_xml_tool = ParseXMLTool()
extract_entities_tool = ExtractEntitiesTool()
build_call_graph_tool = BuildCallGraphTool() 