import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DoxygenParser:
    def __init__(self, xml_dir: str):
        self.xml_dir = Path(xml_dir)
        self.classes: Dict[str, Dict] = {}
        self.methods: Dict[str, Dict] = {}

    def parse_xml_files(self) -> Dict:
        """Parse all XML files in the directory."""
        index_file = self.xml_dir / "index.xml"
        if not index_file.exists():
            logger.error(f"Index file not found at {index_file}")
            raise FileNotFoundError(f"Index file not found at {index_file}")
        
        logger.debug(f"Parsing index file: {index_file}")
        tree = ET.parse(index_file)
        root = tree.getroot()
        
        logger.debug(f"Root tag: {root.tag}")
        for compound in root.findall(".//compound"):
            kind = compound.get("kind")
            logger.debug(f"Found compound of kind: {kind}")
            if kind == "class":
                self._process_class(compound)
            elif kind == "namespace":
                self._process_namespace(compound)
        
        logger.debug(f"Parsed classes: {self.classes}")
        logger.debug(f"Parsed methods: {self.methods}")
        return {"classes": self.classes, "methods": self.methods}

    def _process_class(self, compound: ET.Element) -> None:
        """Process a class compound element."""
        class_name = compound.find("name").text
        class_refid = compound.get("refid")
        
        # Load the detailed class file
        class_file = self.xml_dir / f"{class_refid}.xml"
        if not class_file.exists():
            return

        class_tree = ET.parse(class_file)
        class_root = class_tree.getroot()
        
        class_info = {
            "name": class_name,
            "methods": [],
            "attributes": [],
            "documentation": self._get_documentation(class_root)
        }

        # Process methods
        for member in class_root.findall(".//memberdef[@kind='function']"):
            method_info = self._process_method(member)
            if method_info:
                class_info["methods"].append(method_info)
                self.methods[f"{class_name}.{method_info['name']}"] = method_info

        self.classes[class_name] = class_info

    def _process_method(self, member: ET.Element) -> Optional[Dict]:
        """Process a method member element."""
        try:
            name = member.find("name").text
            return_type = member.find("type").text
            args = member.find("argsstring").text
            
            method_info = {
                "name": name,
                "return_type": return_type,
                "parameters": args,
                "documentation": self._get_documentation(member)
            }
            
            return method_info
        except Exception as e:
            logger.warning(f"Error processing method: {str(e)}")
            return None

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
        return {
            "classes": self.classes,
            "methods": self.methods
        } 