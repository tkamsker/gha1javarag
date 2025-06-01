import os
from pathlib import Path
from lxml import etree
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DoxygenParser:
    def __init__(self, xml_dir: str):
        self.xml_dir = xml_dir
        self.artifacts = []

    def parse_xml_files(self) -> List[Dict[str, Any]]:
        """Parse all XML files in the specified directory."""
        try:
            xml_files = list(Path(self.xml_dir).glob("**/*.xml"))
            logger.info(f"Found {len(xml_files)} XML files to process")
            
            for xml_file in xml_files:
                self._process_xml_file(xml_file)
            
            return self.artifacts
        except Exception as e:
            logger.error(f"Error parsing XML files: {str(e)}")
            raise

    def _process_xml_file(self, xml_file: Path):
        """Process a single XML file and extract artifacts."""
        try:
            tree = etree.parse(str(xml_file))
            root = tree.getroot()

            # Process classes
            for compound in root.xpath("//compounddef[@kind='class']"):
                class_name = compound.findtext("compoundname")
                class_doc = self._get_documentation(compound)
                
                # Process methods within the class
                for member in compound.xpath(".//memberdef[@kind='function']"):
                    artifact = self._create_artifact(member, class_name, class_doc)
                    if artifact:
                        self.artifacts.append(artifact)

        except Exception as e:
            logger.error(f"Error processing file {xml_file}: {str(e)}")

    def _create_artifact(self, member: etree._Element, class_name: str, class_doc: str) -> Dict[str, Any]:
        """Create an artifact dictionary from a member element."""
        try:
            return {
                "id": f"{class_name}.{member.findtext('name')}",
                "name": member.findtext("name"),
                "definition": member.findtext("definition"),
                "args": member.findtext("argsstring"),
                "doc": self._get_documentation(member),
                "class": class_name,
                "class_doc": class_doc,
                "type": "method"
            }
        except Exception as e:
            logger.error(f"Error creating artifact: {str(e)}")
            return None

    def _get_documentation(self, element: etree._Element) -> str:
        """Extract documentation from an element."""
        try:
            detailed = element.find("detaileddescription")
            if detailed is not None:
                return " ".join(detailed.itertext()).strip()
            return ""
        except Exception:
            return ""

def parse_doxygen_xml(xml_dir: str) -> List[Dict[str, Any]]:
    """Main function to parse Doxygen XML files."""
    parser = DoxygenParser(xml_dir)
    return parser.parse_xml_files() 