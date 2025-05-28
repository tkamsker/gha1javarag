import logging
from typing import Type
from crewai.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
import lxml.etree as ET

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
    name: str = "parse_xml"
    description: str = "Parse Doxygen XML files and extract entities"
    args_schema: Type[BaseModel] = ParseXMLInput
    def _run(self, xml_path: str) -> dict:
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            compound = root.find(".//compounddef")
            if compound is None:
                return {"status": "error", "message": "No compounddef found"}
            name_elem = compound.find("compoundname")
            name = name_elem.text if name_elem is not None else ""
            return {"status": "success", "entity": {"name": name}}
        except Exception as e:
            logger.error(f"Error parsing XML {xml_path}: {str(e)}")
            return {"status": "error", "message": str(e)}
    def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async not implemented")

class ExtractEntitiesTool(BaseTool):
    name: str = "extract_entities"
    description: str = "Extract entities from parsed XML"
    args_schema: Type[BaseModel] = ExtractEntitiesInput
    def _run(self, xml_content: dict) -> list:
        if xml_content["status"] != "success":
            return []
        return [xml_content["entity"]]
    def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async not implemented")

class BuildCallGraphTool(BaseTool):
    name: str = "build_call_graph"
    description: str = "Build call graph from extracted entities"
    args_schema: Type[BaseModel] = BuildCallGraphInput
    def _run(self, entities: list) -> dict:
        graph = {}
        for entity in entities:
            graph[entity["name"]] = {"calls": [], "called_by": []}
        return {"graph": graph}
    def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async not implemented")

# Instantiate tools at module level
parse_xml_tool = ParseXMLTool()
extract_entities_tool = ExtractEntitiesTool()
build_call_graph_tool = BuildCallGraphTool() 