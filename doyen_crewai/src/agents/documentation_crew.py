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
from langchain_community.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

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
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.Client(Settings(
            persist_directory=str(xml_input_dir / "chroma_db")
        ))
        self.collection = self.chroma_client.get_or_create_collection("code_entities")
        
        # Initialize tools
        self.parse_xml_tool = parse_xml_tool
        self.extract_entities_tool = extract_entities_tool
        self.build_call_graph_tool = build_call_graph_tool
        
        # Get OpenAI configuration from environment variables
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        model_name = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        temperature = float(os.getenv('TEMPERATURE', '0'))
        
        # Initialize agents with environment variables
        self.parser_agent = Agent(
            role="Parser Agent",
            goal="Extract entities and relationships from XML files",
            backstory="Expert at parsing XML documentation and extracting meaningful information",
            verbose=True,
            llm=ChatOpenAI(
                model=model_name,
                temperature=temperature,
                openai_api_key=openai_api_key
            ),
            tools=[self.parse_xml_tool, self.extract_entities_tool, self.build_call_graph_tool]
        )
        
        self.modeling_agent = Agent(
            role="Modeling Agent",
            goal="Group related entities and identify patterns",
            backstory="Expert at analyzing code structure and relationships",
            verbose=True,
            llm=ChatOpenAI(
                model=model_name,
                temperature=temperature,
                openai_api_key=openai_api_key
            ),
            tools=[self.build_call_graph_tool]
        )

        self.verification_agent = Agent(
            role="Verification Agent",
            goal="Verify requirements and relationships",
            backstory="Expert at validating code documentation and requirements",
            verbose=True,
            llm=ChatOpenAI(
                model=model_name,
                temperature=temperature,
                openai_api_key=openai_api_key
            ),
            tools=[self.build_call_graph_tool]
        )

        self.specification_agent = Agent(
            role="Specification Agent",
            goal="Generate comprehensive documentation",
            backstory="Expert at creating clear and detailed documentation",
            verbose=True,
            llm=ChatOpenAI(
                model=model_name,
                temperature=temperature,
                openai_api_key=openai_api_key
            ),
            tools=[self.build_call_graph_tool]
        )

    def _extract_requirements_from_source(self, source_path: Path) -> List[str]:
        """Extract requirements from source code files."""
        requirements = []
        try:
            with open(source_path, 'r') as f:
                content = f.read()
                # Look for requirement patterns in comments
                requirement_patterns = [
                    r'@requirement\s+(.*?)(?=\n|$)',
                    r'#\s*requirement:\s*(.*?)(?=\n|$)',
                    r'//\s*requirement:\s*(.*?)(?=\n|$)'
                ]
                for pattern in requirement_patterns:
                    matches = re.finditer(pattern, content, re.MULTILINE)
                    requirements.extend(match.group(1).strip() for match in matches)
        except Exception as e:
            logger.error(f"Error extracting requirements from {source_path}: {str(e)}")
        return requirements

    def _extract_tests_from_source(self, source_path: Path) -> List[Dict[str, Any]]:
        """Extract test cases from source code files."""
        tests = []
        try:
            with open(source_path, 'r') as f:
                content = f.read()
                # Look for test patterns in comments
                test_patterns = [
                    r'@test\s+(.*?)(?=\n|$)',
                    r'#\s*test:\s*(.*?)(?=\n|$)',
                    r'//\s*test:\s*(.*?)(?=\n|$)'
                ]
                for pattern in test_patterns:
                    matches = re.finditer(pattern, content, re.MULTILINE)
                    for match in matches:
                        test_desc = match.group(1).strip()
                        tests.append({
                            "description": test_desc,
                            "source_file": str(source_path)
                        })
        except Exception as e:
            logger.error(f"Error extracting tests from {source_path}: {str(e)}")
        return tests

    def _get_related_entities_from_chroma(self, entity_name: str) -> List[Dict[str, Any]]:
        """Get related entities from ChromaDB."""
        try:
            results = self.collection.query(
                query_texts=[entity_name],
                n_results=5
            )
            return results['documents'][0] if results['documents'] else []
        except Exception as e:
            logger.error(f"Error querying ChromaDB for {entity_name}: {str(e)}")
            return []

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
                if refid:
                    xml_refs.append(f"{refid}.xml")
            
            logger.info(f"Found {len(xml_refs)} XML references in index.xml: {xml_refs}")
            
            # Process each XML file
            for xml_ref in xml_refs:
                xml_path = self.xml_input_dir / xml_ref
                if not xml_path.exists():
                    logger.warning(f"XML file not found: {xml_path}")
                    continue
                
                logger.info(f"Processing XML file: {xml_path}")
                
                # Parse XML and extract entities
                parse_result = self.parse_xml_tool._run(str(xml_path))
                if parse_result["status"] != "success":
                    logger.error(f"Failed to parse {xml_path}: {parse_result['message']}")
                    continue
                
                # Extract entities
                entities = self.extract_entities_tool._run(parse_result)
                
                # Get source file path from XML
                source_path = None
                try:
                    tree = ET.parse(str(xml_path))
                    root = tree.getroot()
                    location = root.find(".//location")
                    if location is not None:
                        source_path = Path(location.get("file", ""))
                except Exception as e:
                    logger.error(f"Error getting source path from {xml_path}: {str(e)}")
                
                # Extract requirements and tests if source file exists
                requirements = []
                tests = []
                if source_path and source_path.exists():
                    requirements = self._extract_requirements_from_source(source_path)
                    tests = self._extract_tests_from_source(source_path)
                
                # Get related entities from ChromaDB
                related_entities = []
                for entity in entities:
                    related = self._get_related_entities_from_chroma(entity["name"])
                    related_entities.extend(related)
                
                # Create tasks for the crew (context as list of dicts with description and value)
                parser_task = Task(
                    description=f"Parse Doxygen XML and extract code entities from {xml_path}",
                    agent=self.parser_agent,
                    expected_output="List of code entities with their descriptions and relationships",
                    context=[
                        {"description": "Path to the XML file", "value": str(xml_path)},
                        {"description": "Extracted entities", "value": entities},
                        {"description": "Extracted requirements", "value": requirements},
                        {"description": "Extracted tests", "value": tests},
                        {"description": "Related entities from ChromaDB", "value": related_entities}
                    ]
                )
                
                modeling_task = Task(
                    description="Group related entities and identify patterns",
                    agent=self.modeling_agent,
                    expected_output="Grouped entities and identified patterns",
                    context=[
                        {"description": "Entities to group and analyze", "value": entities}
                    ]
                )
                
                verification_task = Task(
                    description="Verify requirements and relationships",
                    agent=self.verification_agent,
                    expected_output="Verified requirements and relationships",
                    context=[
                        {"description": "Entities to verify", "value": entities},
                        {"description": "Requirements to verify", "value": requirements},
                        {"description": "Tests to verify", "value": tests}
                    ]
                )
                
                specification_task = Task(
                    description="Generate documentation based on verified requirements",
                    agent=self.specification_agent,
                    expected_output="Generated documentation",
                    context=[
                        {"description": "Entities for documentation", "value": entities},
                        {"description": "Requirements for documentation", "value": requirements},
                        {"description": "Tests for documentation", "value": tests},
                        {"description": "Related entities for documentation", "value": related_entities}
                    ]
                )
                
                # Run the crew
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