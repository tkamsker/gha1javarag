import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DoxygenParser:
    def __init__(self, xml_dir: str):
        """Initialize the parser with the directory containing Doxygen XML files."""
        self.xml_dir = Path(xml_dir)
        self.namespace = {'doxygen': 'http://www.doxygen.org/xml/1.0'}
        self.classes: Dict[str, Dict] = {}
        self.methods: Dict[str, Dict] = {}

    def parse_xml_files(self) -> List[Dict[str, Any]]:
        """Parse all XML files in the directory and extract code artifacts."""
        artifacts = []
        
        # First, find and parse the index.xml file
        index_file = self.xml_dir / "index.xml"
        if not index_file.exists():
            raise FileNotFoundError(f"Index file not found at {index_file}")
        
        # Parse index.xml to get all compound files
        index_tree = ET.parse(index_file)
        index_root = index_tree.getroot()
        
        # Get all compound files from index
        compound_files = []
        for compound in index_root.findall('.//doxygen:compound', self.namespace):
            refid = compound.get('refid')
            if refid:
                compound_file = self.xml_dir / f"{refid}.xml"
                if compound_file.exists():
                    compound_files.append(compound_file)
        
        logger.info(f"Found {len(compound_files)} compound files to process")
        
        # Process each compound file
        for compound_file in compound_files:
            try:
                tree = ET.parse(compound_file)
                root = tree.getroot()
                
                # Process each compounddef element
                for compounddef in root.findall('.//doxygen:compounddef', self.namespace):
                    kind = compounddef.get('kind')
                    if kind in ['class', 'struct']:
                        # Process class/struct
                        class_artifact = self._process_class(compounddef)
                        if class_artifact:
                            artifacts.append(class_artifact)
                            
                        # Process all members (methods, fields) within the class
                        for member in compounddef.findall('.//doxygen:memberdef', self.namespace):
                            member_artifact = self._process_member(member, class_artifact['name'])
                            if member_artifact:
                                artifacts.append(member_artifact)
            
            except Exception as e:
                logger.error(f"Error processing file {compound_file}: {str(e)}")
                continue
        
        logger.info(f"Successfully parsed {len(artifacts)} artifacts")
        return artifacts

    def _process_class(self, compounddef: ET.Element) -> Dict[str, Any]:
        """Process a class or struct definition."""
        try:
            name = compounddef.find('.//doxygen:compoundname', self.namespace).text
            brief = compounddef.find('.//doxygen:briefdescription', self.namespace)
            detailed = compounddef.find('.//doxygen:detaileddescription', self.namespace)
            
            # Get all fields (member variables)
            fields = []
            for member in compounddef.findall('.//doxygen:memberdef[@kind="variable"]', self.namespace):
                field = self._process_field(member)
                if field:
                    fields.append(field)
            
            return {
                'type': 'class',
                'name': name,
                'brief': self._get_text(brief) if brief is not None else '',
                'detailed': self._get_text(detailed) if detailed is not None else '',
                'fields': fields
            }
        except Exception as e:
            logger.error(f"Error processing class: {str(e)}")
            return None

    def _process_member(self, member: ET.Element, class_name: str) -> Dict[str, Any]:
        """Process a class member (method or field)."""
        try:
            kind = member.get('kind')
            name = member.find('.//doxygen:name', self.namespace).text
            brief = member.find('.//doxygen:briefdescription', self.namespace)
            detailed = member.find('.//doxygen:detaileddescription', self.namespace)
            
            # Get parameters for methods
            params = []
            if kind == 'function':
                for param in member.findall('.//doxygen:param', self.namespace):
                    param_name = param.find('.//doxygen:declname', self.namespace)
                    param_type = param.find('.//doxygen:type', self.namespace)
                    if param_name is not None and param_type is not None:
                        params.append({
                            'name': param_name.text,
                            'type': self._get_text(param_type)
                        })
            
            return {
                'type': kind,
                'name': f"{class_name}::{name}",
                'brief': self._get_text(brief) if brief is not None else '',
                'detailed': self._get_text(detailed) if detailed is not None else '',
                'parameters': params if kind == 'function' else []
            }
        except Exception as e:
            logger.error(f"Error processing member: {str(e)}")
            return None

    def _process_field(self, member: ET.Element) -> Dict[str, Any]:
        """Process a class field (member variable)."""
        try:
            name = member.find('.//doxygen:name', self.namespace).text
            type_elem = member.find('.//doxygen:type', self.namespace)
            brief = member.find('.//doxygen:briefdescription', self.namespace)
            
            return {
                'name': name,
                'type': self._get_text(type_elem) if type_elem is not None else '',
                'description': self._get_text(brief) if brief is not None else ''
            }
        except Exception as e:
            logger.error(f"Error processing field: {str(e)}")
            return None

    def _get_text(self, element: ET.Element) -> str:
        """Extract text content from an XML element, including nested elements."""
        if element is None:
            return ''
        
        text_parts = []
        if element.text:
            text_parts.append(element.text.strip())
        
        for child in element:
            if child.text:
                text_parts.append(child.text.strip())
            if child.tail:
                text_parts.append(child.tail.strip())
        
        return ' '.join(text_parts)

    def _process_namespace(self, compound: ET.Element) -> None:
        """Process a namespace compound element."""
        # Similar to _process_class but for namespaces
        pass

    def _get_documentation(self, element: ET.Element) -> str:
        """Extract documentation from an element."""
        doc = element.find(".//detaileddescription")
        if doc is not None:
            return " ".join(doc.itertext()).strip()
        return ""

    def get_code_artifacts(self) -> Dict:
        """Return all extracted code artifacts."""
        return {"classes": self.classes, "methods": self.methods} 