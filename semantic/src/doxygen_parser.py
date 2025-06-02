import os
from pathlib import Path
from lxml import etree
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DoxygenParser:
    def __init__(self):
        """Initialize the Doxygen parser."""
        pass

    def parse_directory(self, xml_dir: str) -> List[Dict[str, Any]]:
        """Parse all XML files in a directory and extract code artifacts."""
        try:
            artifacts = []
            xml_path = Path(xml_dir)
            
            if not xml_path.exists():
                logger.error(f"Directory not found: {xml_dir}")
                return artifacts
            
            # Find all XML files recursively
            xml_files = list(xml_path.glob("**/*.xml"))
            logger.info(f"Found {len(xml_files)} XML files in {xml_dir}")
            
            for xml_file in xml_files:
                try:
                    artifacts.extend(self._parse_file(xml_file))
                except Exception as e:
                    logger.error(f"Error parsing {xml_file}: {str(e)}")
                    continue
            
            logger.info(f"Extracted {len(artifacts)} artifacts from XML files")
            return artifacts
            
        except Exception as e:
            logger.error(f"Error parsing directory: {str(e)}")
            raise

    def _parse_file(self, xml_file: Path) -> List[Dict[str, Any]]:
        """Parse a single XML file and extract code artifacts."""
        artifacts = []
        
        try:
            # Parse XML file
            tree = etree.parse(str(xml_file))
            root = tree.getroot()
            
            # Extract compound definitions (classes, structs, etc.)
            for compound in root.xpath("//compounddef"):
                compound_name = compound.findtext("compoundname", "")
                compound_kind = compound.get("kind", "")
                
                # Extract member definitions (methods, functions, etc.)
                for member in compound.xpath(".//memberdef"):
                    try:
                        artifact = {
                            "id": member.findtext("id", ""),
                            "name": member.findtext("name", ""),
                            "definition": member.findtext("definition", ""),
                            "args": member.findtext("argsstring", ""),
                            "description": self._extract_description(member),
                            "class": compound_name,
                            "kind": compound_kind
                        }
                        
                        # Only add if we have essential information
                        if artifact["name"] and artifact["class"]:
                            artifacts.append(artifact)
                            
                    except Exception as e:
                        logger.warning(f"Error parsing member in {xml_file}: {str(e)}")
                        continue
            
            return artifacts
            
        except Exception as e:
            logger.error(f"Error parsing file {xml_file}: {str(e)}")
            return []

    def _extract_description(self, member: etree._Element) -> str:
        """Extract and clean the description from a member element."""
        try:
            # Get detailed description
            detailed = member.find(".//detaileddescription")
            if detailed is not None:
                # Extract text content
                text = " ".join(detailed.xpath(".//text()"))
                if text.strip():
                    return text.strip()
            
            # Fallback to brief description
            brief = member.find(".//briefdescription")
            if brief is not None:
                text = " ".join(brief.xpath(".//text()"))
                if text.strip():
                    return text.strip()
            
            # Fallback to method name and args
            name = member.findtext("name", "")
            args = member.findtext("argsstring", "")
            if name or args:
                return f"{name}{args}".strip()
            
            return ""
            
        except Exception as e:
            logger.warning(f"Error extracting description: {str(e)}")
            return ""

def parse_doxygen_xml(xml_dir: str) -> List[Dict[str, Any]]:
    """Main function to parse Doxygen XML files."""
    parser = DoxygenParser()
    return parser.parse_directory(xml_dir) 