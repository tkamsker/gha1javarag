"""CrewAI implementation for documentation generation."""

from typing import List, Dict, Any, Optional, Set, Type
from pathlib import Path
import logging
import json
from crewai import Agent, Task, Crew, Process
from langchain.tools import BaseTool, tool, Tool
from pydantic import BaseModel, Field
import lxml.etree as ET
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import chromadb
from chromadb.config import Settings
import re
from dataclasses import dataclass
from enum import Enum
from jinja2 import Environment, FileSystemLoader
from .documentation_tools import parse_xml_tool, extract_entities_tool, build_call_graph_tool
from langchain.chat_models import ChatOpenAI

logger = logging.getLogger(__name__)

class EntityType(Enum):
    CLASS = "class"
    FUNCTION = "function"
    VARIABLE = "variable"
    NAMESPACE = "namespace"
    FILE = "file"

@dataclass
class CodeEntity:
    """Represents a code entity extracted from XML."""
    type: EntityType
    name: str
    description: str
    path: str
    dependencies: List[str]
    parameters: List[Dict[str, str]]
    return_type: Optional[str]
    modifiers: List[str]
    children: List[str]
    metrics: Dict[str, float]

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
    name = "extract_entities"
    description = "Extract code entities from parsed XML."
    args_schema: Type[BaseModel] = ExtractEntitiesInput
    def _run(self, xml_content: dict) -> list:
        if xml_content["status"] != "success":
            return []
        return [xml_content["entity"]]
    def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async not implemented")

class BuildCallGraphTool(BaseTool):
    name = "build_call_graph"
    description = "Build call graph from extracted entities."
    args_schema: Type[BaseModel] = BuildCallGraphInput
    def _run(self, entities: list) -> dict:
        graph = {}
        for entity in entities:
            graph[entity["name"]] = {"calls": [], "called_by": []}
        return {"graph": graph}
    def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async not implemented")

class DocumentationCrew:
    """Crew for generating documentation from codebase."""
    
    def __init__(self, xml_input_dir: Path):
        """Initialize the documentation crew with the path to Doxygen XML files."""
        self.xml_input_dir = xml_input_dir
        logger.info(f"XML input directory: {self.xml_input_dir}")
        
        # Initialize tools
        self.parse_xml_tool = ParseXMLTool()
        self.extract_entities_tool = ExtractEntitiesTool()
        self.build_call_graph_tool = BuildCallGraphTool()
        
        # Initialize agents with mock responses
        self.parser_agent = Agent(
            role="Parser Agent",
            goal="Extract entities and relationships from XML files",
            backstory="Expert at parsing XML documentation and extracting meaningful information",
            verbose=True,
            llm=ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0,
                openai_api_key="mock-key-for-testing",
                mock_response="Mock response for parser agent"
            ),
            tools=[self.parse_xml_tool, self.extract_entities_tool, self.build_call_graph_tool]
        )
        
        self.modeling_agent = Agent(
            role="Modeling Agent",
            goal="Group related entities and identify patterns",
            backstory="Expert at analyzing code structure and relationships",
            verbose=True,
            llm=ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0,
                openai_api_key="mock-key-for-testing",
                mock_response="Mock response for modeling agent"
            ),
            tools=[self.build_call_graph_tool]
        )
        
        self.verification_agent = Agent(
            role="Verification Agent",
            goal="Verify requirements and relationships",
            backstory="Expert at validating code documentation and requirements",
            verbose=True,
            llm=ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0,
                openai_api_key="mock-key-for-testing",
                mock_response="Mock response for verification agent"
            ),
            tools=[self.build_call_graph_tool]
        )
        
        self.specification_agent = Agent(
            role="Specification Agent",
            goal="Generate comprehensive documentation",
            backstory="Expert at creating clear and detailed documentation",
            verbose=True,
            llm=ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0,
                openai_api_key="mock-key-for-testing",
                mock_response="Mock response for specification agent"
            ),
            tools=[self.build_call_graph_tool]
        )
    
    def _get_entity_type(self, compound: ET.Element) -> EntityType:
        """Get entity type from compound element.
        
        Args:
            compound: Compound element
            
        Returns:
            Entity type
        """
        kind = compound.get("kind", "")
        if kind == "class":
            return EntityType.CLASS
        elif kind == "function":
            return EntityType.FUNCTION
        elif kind == "variable":
            return EntityType.VARIABLE
        elif kind == "namespace":
            return EntityType.NAMESPACE
        else:
            return EntityType.FILE
    
    def _get_entity_name(self, compound: ET.Element) -> str:
        """Get entity name from compound element.
        
        Args:
            compound: Compound element
            
        Returns:
            Entity name
        """
        name_elem = compound.find("compoundname")
        if name_elem is not None:
            return name_elem.text
        return ""
    
    def _get_entity_description(self, compound: ET.Element) -> str:
        """Get entity description from compound element.
        
        Args:
            compound: Compound element
            
        Returns:
            Entity description
        """
        desc_elem = compound.find("briefdescription")
        if desc_elem is not None:
            return ET.tostring(desc_elem, encoding="unicode", method="text")
        return ""
    
    def _get_entity_path(self, compound: ET.Element) -> str:
        """Get entity path from compound element.
        
        Args:
            compound: Compound element
            
        Returns:
            Entity path
        """
        location = compound.find("location")
        if location is not None:
            return location.get("file", "")
        return ""
    
    def _get_entity_dependencies(self, compound: ET.Element) -> List[str]:
        """Get entity dependencies from compound element.
        
        Args:
            compound: Compound element
            
        Returns:
            List of dependencies
        """
        dependencies = set()
        
        # Get base classes
        for base in compound.findall(".//basecompoundref"):
            dependencies.add(base.text)
        
        # Get included files
        for inc in compound.findall(".//includes"):
            dependencies.add(inc.text)
        
        # Get used types
        for type_elem in compound.findall(".//type"):
            if type_elem.text:
                dependencies.add(type_elem.text)
        
        return list(dependencies)
    
    def _get_entity_parameters(self, compound: ET.Element) -> List[Dict[str, str]]:
        """Get entity parameters from compound element.
        
        Args:
            compound: Compound element
            
        Returns:
            List of parameters
        """
        parameters = []
        for param in compound.findall(".//param"):
            param_dict = {}
            
            # Get parameter name
            name_elem = param.find("paramname")
            if name_elem is not None:
                param_dict["name"] = name_elem.text
            
            # Get parameter type
            type_elem = param.find("type")
            if type_elem is not None:
                param_dict["type"] = ET.tostring(type_elem, encoding="unicode", method="text")
            
            # Get parameter description
            desc_elem = param.find("briefdescription")
            if desc_elem is not None:
                param_dict["description"] = ET.tostring(desc_elem, encoding="unicode", method="text")
            
            if param_dict:
                parameters.append(param_dict)
        
        return parameters
    
    def _get_entity_return_type(self, compound: ET.Element) -> Optional[str]:
        """Get entity return type from compound element.
        
        Args:
            compound: Compound element
            
        Returns:
            Return type if available
        """
        type_elem = compound.find(".//type")
        if type_elem is not None:
            return ET.tostring(type_elem, encoding="unicode", method="text")
        return None
    
    def _get_entity_modifiers(self, compound: ET.Element) -> List[str]:
        """Get entity modifiers from compound element.
        
        Args:
            compound: Compound element
            
        Returns:
            List of modifiers
        """
        modifiers = []
        
        # Get access specifier
        access = compound.get("prot", "")
        if access:
            modifiers.append(access)
        
        # Get virtual status
        if compound.get("virt", "") == "virtual":
            modifiers.append("virtual")
        
        # Get static status
        if compound.get("static", "") == "yes":
            modifiers.append("static")
        
        return modifiers
    
    def _get_entity_children(self, compound: ET.Element) -> List[str]:
        """Get entity children from compound element.
        
        Args:
            compound: Compound element
            
        Returns:
            List of child names
        """
        children = []
        
        # Get member functions
        for member in compound.findall(".//memberdef[@kind='function']"):
            name_elem = member.find("name")
            if name_elem is not None:
                children.append(name_elem.text)
        
        # Get member variables
        for member in compound.findall(".//memberdef[@kind='variable']"):
            name_elem = member.find("name")
            if name_elem is not None:
                children.append(name_elem.text)
        
        return children
    
    def _calculate_entity_metrics(self, compound: ET.Element) -> Dict[str, float]:
        """Calculate metrics for an entity.
        
        Args:
            compound: Compound element
            
        Returns:
            Dictionary of metrics
        """
        metrics = {
            "complexity": 0.0,
            "lines": 0,
            "dependencies": 0,
            "children": 0
        }
        
        # Calculate cyclomatic complexity
        for member in compound.findall(".//memberdef[@kind='function']"):
            metrics["complexity"] += self._calculate_function_complexity(member)
        
        # Count lines
        location = compound.find("location")
        if location is not None:
            start = int(location.get("bodystart", 0))
            end = int(location.get("bodyend", 0))
            metrics["lines"] = end - start
        
        # Count dependencies
        metrics["dependencies"] = len(self._get_entity_dependencies(compound))
        
        # Count children
        metrics["children"] = len(self._get_entity_children(compound))
        
        return metrics
    
    def _calculate_function_complexity(self, function: ET.Element) -> float:
        """Calculate cyclomatic complexity of a function.
        
        Args:
            function: Function element
            
        Returns:
            Complexity score
        """
        complexity = 1.0  # Base complexity
        
        # Count control structures
        for elem in function.iter():
            if elem.tag in ["if", "for", "while", "switch", "case", "catch"]:
                complexity += 1
            elif elem.tag == "operator" and elem.text in ["&&", "||"]:
                complexity += 1
        
        return complexity
    
    def _find_function_calls(self, text: str) -> Set[str]:
        """Find function calls in text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Set of function names
        """
        # Simple regex to find function calls
        # This could be made more sophisticated with proper parsing
        pattern = r'(\w+)\s*\('
        matches = re.finditer(pattern, text)
        return {match.group(1) for match in matches}
    
    def generate_documentation(self) -> str:
        """Generate documentation for the codebase."""
        try:
            # Parse index.xml to get references to other XML files
            index_path = self.xml_input_dir / "index.xml"
            if not index_path.exists():
                logger.error(f"index.xml not found at {index_path}")
                return "Error: index.xml not found"
            
            tree = ET.parse(str(index_path))
            root = tree.getroot()
            
            # Get all compound references
            xml_refs = []
            for compound in root.findall(".//compound"):
                refid = compound.get("refid")
                if refid and refid.endswith(".xml"):
                    xml_refs.append(refid)
            
            logger.info(f"Found {len(xml_refs)} XML references in index.xml: {xml_refs}")
            
            # Process each XML file
            for xml_ref in xml_refs:
                xml_path = self.xml_input_dir / xml_ref
                if not xml_path.exists():
                    logger.warning(f"XML file not found: {xml_path}")
                    continue
                
                logger.info(f"Processing XML file: {xml_path}")
                
                # Mock response for testing
                mock_entities = [
                    {
                        "name": "MockEntity",
                        "description": "This is a mock entity for testing.",
                        "type": "class",
                        "dependencies": ["OtherEntity"]
                    }
                ]
                
                mock_call_graph = {
                    "graph": {
                        "MockEntity": {
                            "calls": ["OtherEntity"],
                            "called_by": ["ParentEntity"]
                        }
                    }
                }
                
                # Create tasks with mock data
                parser_task = Task(
                    description=f"Parse Doxygen XML and extract code entities from {xml_path}",
                    agent=self.parser_agent,
                    expected_output="List of code entities with their descriptions and relationships",
                    context={"xml_path": str(xml_path)},
                    output=mock_entities
                )
                
                modeling_task = Task(
                    description="Group related entities and identify patterns",
                    agent=self.modeling_agent,
                    expected_output="Grouped entities and identified patterns",
                    context={"entities": mock_entities},
                    output={"groups": [{"name": "MockGroup", "entities": mock_entities}]}
                )
                
                verification_task = Task(
                    description="Verify requirements and relationships",
                    agent=self.verification_agent,
                    expected_output="Verified requirements and relationships",
                    context={"groups": [{"name": "MockGroup", "entities": mock_entities}]},
                    output={"verified": True, "requirements": ["Mock requirement"]}
                )
                
                specification_task = Task(
                    description="Generate documentation based on verified requirements",
                    agent=self.specification_agent,
                    expected_output="Generated documentation",
                    context={
                        "requirements": ["Mock requirement"],
                        "call_graph": mock_call_graph
                    },
                    output={"documentation": "Mock documentation content"}
                )
                
                # Run the crew with mock data
                crew = Crew(
                    agents=[self.parser_agent, self.modeling_agent, self.verification_agent, self.specification_agent],
                    tasks=[parser_task, modeling_task, verification_task, specification_task],
                    verbose=True
                )
                
                result = crew.kickoff()
                logger.info(f"Documentation generated for {xml_path}: {result}")
            
            return "Documentation generation completed successfully"
            
        except Exception as e:
            logger.error(f"Error during documentation generation: {str(e)}")
            return f"Error: {str(e)}" 