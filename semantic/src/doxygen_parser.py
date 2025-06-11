import os
from pathlib import Path
from lxml import etree
from typing import List, Dict, Any, Optional
import logging
import re

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DoxygenParser:
    def __init__(self, java_source_dir: Optional[str] = None):
        """Initialize the Doxygen parser.
        
        Args:
            java_source_dir: Optional path to Java source code directory
        """
        self.java_source_dir = java_source_dir
        if java_source_dir:
            self.java_source_dir = Path(java_source_dir)
            if not self.java_source_dir.exists():
                logger.warning(f"Java source directory not found: {java_source_dir}")
        
        # Create a custom XML parser that can handle @ symbols
        self.parser = etree.XMLParser(recover=True, encoding='utf-8')

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
                    # Skip non-relevant XML files
                    if xml_file.name.startswith("dir_") or xml_file.name == "index.xml" or xml_file.name == "Doxyfile.xml":
                        logger.warning(f"Skipping non-relevant file: {xml_file}")
                        continue
                    
                    # Log the first few lines of the file for debugging
                    with open(xml_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()[:5]
                        logger.debug(f"First few lines of {xml_file}: {''.join(lines)}")
                    
                    # Skip files that do not contain the expected structure
                    if not self._is_valid_doxygen_xml(xml_file):
                        logger.warning(f"Skipping file {xml_file} as it does not contain the expected structure.")
                        continue
                    
                    artifacts.extend(self._parse_file(xml_file))
                except Exception as e:
                    logger.error(f"Error parsing {xml_file}: {str(e)}")
                    continue
            
            logger.info(f"Extracted {len(artifacts)} artifacts from XML files")
            return artifacts
            
        except Exception as e:
            logger.error(f"Error parsing directory: {str(e)}")
            raise

    def _preprocess_xml(self, xml_file: Path) -> str:
        """Preprocess XML file content to remove stray '@' symbols outside of tags and after the root element."""
        try:
            with open(xml_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Debug print original content
            logger.debug(f"[DEBUG] Original content for {xml_file}:\n{content[:1000]}...")
            
            # Remove everything after the LAST closing root tag (e.g., </doxygen>)
            matches = list(re.finditer(r'(</[a-zA-Z0-9:_-]+>)', content))
            if matches:
                end_idx = matches[-1].end(1)
                content = content[:end_idx]
                logger.debug(f"[DEBUG] Content after slicing at last root tag:\n{content[-1000:]}")
            
            # Remove everything before the XML declaration if present
            xml_decl = re.search(r'<\?xml[^>]*\?>', content)
            if xml_decl:
                content = content[xml_decl.start():]
            
            # Process content character by character to handle @ symbols
            result = []
            in_tag = False
            in_attribute = False
            in_cdata = False
            in_comment = False
            i = 0
            
            while i < len(content):
                char = content[i]
                
                # Handle CDATA sections
                if content[i:i+9] == '<![CDATA[':
                    in_cdata = True
                    result.append(char)
                    i += 1
                    continue
                elif content[i:i+3] == ']]>':
                    in_cdata = False
                    result.append(char)
                    i += 1
                    continue
                
                # Handle comments
                if content[i:i+4] == '<!--':
                    in_comment = True
                    result.append(char)
                    i += 1
                    continue
                elif content[i:i+3] == '-->':
                    in_comment = False
                    result.append(char)
                    i += 1
                    continue
                
                # Handle tags and attributes
                if char == '<' and not in_cdata and not in_comment:
                    in_tag = True
                    result.append(char)
                elif char == '>' and not in_cdata and not in_comment:
                    in_tag = False
                    in_attribute = False
                    result.append(char)
                elif char == '"' and in_tag and not in_cdata and not in_comment:
                    in_attribute = not in_attribute
                    result.append(char)
                elif char == '@' and not in_tag and not in_cdata and not in_comment:
                    # Remove stray @ symbol
                    logger.debug(f"[DEBUG] Removed stray '@' at position {i}")
                else:
                    result.append(char)
                
                i += 1
            
            cleaned = ''.join(result)
            
            # Final sweep: find any remaining stray '@' symbols
            stray_at_positions = [m.start() for m in re.finditer(r'@', cleaned)]
            for pos in stray_at_positions:
                # Show context around the stray '@'
                context = cleaned[max(0, pos-20):pos+21]
                logger.error(f"[FINAL SWEEP] Stray '@' at position {pos}: ...{context}...")
            if stray_at_positions:
                # Remove all remaining '@' symbols
                cleaned = cleaned.replace('@', '')
                logger.error(f"[FINAL SWEEP] Removed {len(stray_at_positions)} stray '@' symbols in final sweep.")
            
            # Debug print final cleaned content
            logger.debug(f"[DEBUG] Final cleaned content for {xml_file}:\n{cleaned[:1000]}...")
            
            return cleaned
            
        except Exception as e:
            logger.error(f"Error preprocessing file {xml_file}: {str(e)}")
            raise

    def _is_valid_doxygen_xml(self, xml_file: Path) -> bool:
        """Check if the XML file contains the expected Doxygen structure."""
        try:
            xml_content = self._preprocess_xml(xml_file)
            tree = etree.fromstring(xml_content.encode('utf-8'), parser=self.parser)
            return tree.xpath("//compounddef") is not None
        except Exception as e:
            import traceback
            logger.error(f"Error checking validity of {xml_file}: {repr(e)}\n{traceback.format_exc()}")
            # Log Unicode code points around the error if possible
            if hasattr(e, 'position'):
                pos = e.position[1] if isinstance(e.position, tuple) else e.position
                context = xml_content[max(0, pos-20):pos+21]
                codepoints = ' '.join(f'U+{ord(c):04X}' for c in context)
                logger.error(f"[UNICODE] Context around error at {pos}: {context}\nCodepoints: {codepoints}")
            return False

    def _parse_file(self, xml_file: Path) -> List[Dict[str, Any]]:
        """Parse a single XML file and extract code artifacts."""
        artifacts = []
        
        try:
            # Preprocess and parse XML file
            xml_content = self._preprocess_xml(xml_file)
            tree = etree.fromstring(xml_content.encode('utf-8'), parser=self.parser)
            root = tree
            
            # Check if the file contains the expected structure based on XSD
            if not root.xpath("//compounddef"):
                logger.warning(f"Skipping file {xml_file} as it does not contain the expected structure.")
                return artifacts
            
            # Extract compound definitions (classes, structs, etc.)
            for compound in root.xpath("//compounddef"):
                compound_name = compound.findtext("compoundname", "")
                compound_kind = compound.get("kind", "")
                
                # Get source file location if available
                location_elem = compound.find(".//location")
                source_file = location_elem.get("file", "") if location_elem is not None else ""
                source_code = self._get_source_code(source_file) if source_file else ""
                
                # Get location information
                location = compound.find(".//location")
                location_info = {}
                if location is not None:
                    location_info = {
                        "file": location.get("file", ""),
                        "line": location.get("line", ""),
                        "column": location.get("column", ""),
                        "declfile": location.get("declfile", ""),
                        "declline": location.get("declline", ""),
                        "declcolumn": location.get("declcolumn", ""),
                        "bodyfile": location.get("bodyfile", ""),
                        "bodystart": location.get("bodystart", ""),
                        "bodyend": location.get("bodyend", "")
                    }
                
                # Extract member definitions (methods, functions, etc.)
                for member in compound.xpath(".//memberdef"):
                    try:
                        # Get member location
                        member_location = member.find(".//location")
                        line_start = member_location.get("bodystart", "") if member_location is not None else ""
                        line_end = member_location.get("bodyend", "") if member_location is not None else ""
                        
                        artifact = {
                            "id": member.get("id", ""),
                            "name": member.findtext("name", ""),
                            "definition": member.findtext("definition", ""),
                            "args": member.findtext("argsstring", ""),
                            "description": self._extract_description(member),
                            "class": compound_name,
                            "kind": compound_kind,
                            "source_file": source_file,
                            "source_code": self._extract_source_code(source_code, line_start, line_end),
                            "metadata": {
                                "line_start": line_start,
                                "line_end": line_end,
                                "is_public": member.get("prot", "") == "public",
                                "is_static": member.get("static", "") == "yes",
                                "is_virtual": member.get("virtual", "") == "virtual",
                                "is_const": member.get("const", "") == "yes",
                                "return_type": member.findtext("type", ""),
                                "parameters": self._extract_parameters(member),
                                "location": location_info
                            }
                        }
                        
                        # Only add if we have essential information
                        if artifact["name"] and artifact["class"]:
                            artifacts.append(artifact)
                            
                    except Exception as e:
                        logger.warning(f"Error parsing member in {xml_file}: {str(e)}")
                        continue
                
                # Extract code from programlisting for embedding
                for programlisting in compound.xpath(".//programlisting"):
                    code = "".join(programlisting.xpath(".//text()"))
                    if code.strip():
                        artifacts.append({
                            "id": f"{compound_name}_programlisting",
                            "name": compound_name,
                            "description": "Code from programlisting",
                            "class": compound_name,
                            "kind": compound_kind,
                            "source_code": code.strip(),
                            "metadata": {
                                "location": location_info
                            }
                        })
            
            return artifacts
            
        except Exception as e:
            import traceback
            logger.error(f"Error parsing file {xml_file}: {repr(e)}\n{traceback.format_exc()}")
            # Log the first few lines of the failing file for debugging
            try:
                with open(xml_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()[:5]
                    logger.error(f"First few lines of {xml_file}: {''.join(lines)}")
            except Exception as read_error:
                logger.error(f"Error reading file {xml_file} for debugging: {str(read_error)}")
            # Log Unicode code points around the error if possible
            if hasattr(e, 'position'):
                pos = e.position[1] if isinstance(e.position, tuple) else e.position
                context = xml_content[max(0, pos-20):pos+21]
                codepoints = ' '.join(f'U+{ord(c):04X}' for c in context)
                logger.error(f"[UNICODE] Context around error at {pos}: {context}\nCodepoints: {codepoints}")
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

    def _get_source_code(self, source_file: str) -> str:
        """Get source code content from file."""
        if not self.java_source_dir or not source_file:
            return ""
            
        try:
            file_path = self.java_source_dir / source_file
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            return ""
        except Exception as e:
            logger.warning(f"Error reading source file {source_file}: {str(e)}")
            return ""

    def _extract_source_code(self, source_code: str, line_start: str, line_end: str) -> str:
        """Extract relevant source code section based on line numbers."""
        if not source_code or not line_start or not line_end:
            return ""
            
        try:
            lines = source_code.splitlines()
            start = int(line_start) - 1
            end = int(line_end)
            return "\n".join(lines[start:end])
        except Exception as e:
            logger.warning(f"Error extracting source code section: {str(e)}")
            return ""

    def _extract_parameters(self, member: etree._Element) -> List[Dict[str, str]]:
        """Extract parameter information from member element."""
        parameters = []
        for param in member.xpath(".//param"):
            param_name = param.findtext("declname", "")
            param_type = param.findtext("type", "")
            param_desc = " ".join(param.xpath(".//text()"))
            if param_name:
                parameters.append({
                    "name": param_name,
                    "type": param_type,
                    "description": param_desc.strip()
                })
        return parameters

def parse_doxygen_xml(xml_dir: str, java_source_dir: Optional[str] = None) -> List[Dict[str, Any]]:
    """Main function to parse Doxygen XML files.
    
    Args:
        xml_dir: Directory containing Doxygen XML files
        java_source_dir: Optional path to Java source code directory
    """
    parser = DoxygenParser(java_source_dir)
    return parser.parse_directory(xml_dir) 