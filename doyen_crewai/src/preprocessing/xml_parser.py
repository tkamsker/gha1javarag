"""Doxygen XML parser module for extracting code documentation and relationships."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional
from xml.etree import ElementTree

@dataclass
class CodeEntity:
    """Represents a code entity (class, function, etc.) extracted from Doxygen XML."""
    name: str
    kind: str  # class, function, file, etc.
    description: str
    source_file: str
    calls: List[str]
    documentation: str

class DoxygenXMLParser:
    """Parser for Doxygen XML documentation files."""
    
    def __init__(self, xml_dir: str):
        """Initialize the parser with the XML directory path.
        
        Args:
            xml_dir: Path to the directory containing Doxygen XML files
        """
        self.xml_dir = Path(xml_dir)
        if not self.xml_dir.exists():
            raise ValueError(f"XML directory does not exist: {xml_dir}")
    
    def parse_all(self) -> Dict[str, CodeEntity]:
        """Parse all XML files in the directory and return a dictionary of code entities.
        
        Returns:
            Dictionary mapping entity names to CodeEntity objects
        """
        entities = {}
        
        # Parse compound files (classes, namespaces, etc.)
        for xml_file in self.xml_dir.glob("*.xml"):
            if xml_file.name.startswith("class") or xml_file.name.startswith("namespace"):
                self._parse_compound_file(xml_file, entities)
        
        # Parse member files (functions, variables, etc.)
        for xml_file in self.xml_dir.glob("*.xml"):
            if xml_file.name.startswith("member"):
                self._parse_member_file(xml_file, entities)
        
        return entities
    
    def _parse_compound_file(self, xml_file: Path, entities: Dict[str, CodeEntity]) -> None:
        """Parse a compound XML file (class, namespace, etc.).
        
        Args:
            xml_file: Path to the XML file
            entities: Dictionary to store parsed entities
        """
        tree = ElementTree.parse(xml_file)
        root = tree.getroot()
        
        for compound in root.findall(".//compounddef"):
            name = compound.find("compoundname").text
            kind = compound.get("kind")
            description = self._get_description(compound)
            source_file = self._get_source_file(compound)
            
            entity = CodeEntity(
                name=name,
                kind=kind,
                description=description,
                source_file=source_file,
                calls=self._get_calls(compound),
                documentation=self._get_documentation(compound)
            )
            
            entities[name] = entity
    
    def _parse_member_file(self, xml_file: Path, entities: Dict[str, CodeEntity]) -> None:
        """Parse a member XML file (functions, variables, etc.).
        
        Args:
            xml_file: Path to the XML file
            entities: Dictionary to store parsed entities
        """
        tree = ElementTree.parse(xml_file)
        root = tree.getroot()
        
        for member in root.findall(".//memberdef"):
            name = member.find("name").text
            kind = member.get("kind")
            description = self._get_description(member)
            source_file = self._get_source_file(member)
            
            entity = CodeEntity(
                name=name,
                kind=kind,
                description=description,
                source_file=source_file,
                calls=self._get_calls(member),
                documentation=self._get_documentation(member)
            )
            
            entities[name] = entity
    
    def _get_description(self, element: ElementTree.Element) -> str:
        """Extract description from an XML element.
        
        Args:
            element: XML element to extract description from
            
        Returns:
            Description text or empty string if not found
        """
        brief = element.find("briefdescription")
        if brief is not None:
            return brief.text or ""
        return ""
    
    def _get_source_file(self, element: ElementTree.Element) -> str:
        """Extract source file path from an XML element.
        
        Args:
            element: XML element to extract source file from
            
        Returns:
            Source file path or empty string if not found
        """
        location = element.find("location")
        if location is not None:
            return location.get("file", "")
        return ""
    
    def _get_calls(self, element: ElementTree.Element) -> List[str]:
        """Extract function calls from an XML element.
        
        Args:
            element: XML element to extract calls from
            
        Returns:
            List of called function names
        """
        calls = []
        for ref in element.findall(".//ref"):
            if ref.text:
                calls.append(ref.text)
        return calls
    
    def _get_documentation(self, element: ElementTree.Element) -> str:
        """Extract full documentation from an XML element.
        
        Args:
            element: XML element to extract documentation from
            
        Returns:
            Full documentation text or empty string if not found
        """
        detailed = element.find("detaileddescription")
        if detailed is not None:
            return detailed.text or ""
        return "" 