"""
XML configuration file parser.

Extracts structural information from XML configuration files including:
- Spring configuration (beans)
- MyBatis mappers
- web.xml descriptors
- Generic XML structure
"""

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from lxml import etree

logger = logging.getLogger(__name__)


# ==============================================================================
# XMLParser Class
# ==============================================================================

class XMLParser:
    """
    Parser for XML configuration files.

    Uses lxml for robust XML parsing with namespace support.
    """

    def __init__(self):
        """Initialize XML parser."""
        self.logger = logging.getLogger(__name__)

    def parse_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Parse an XML file.

        Args:
            file_path: Path to XML file

        Returns:
            Dictionary with parsed elements

        Raises:
            FileNotFoundError: If file doesn't exist
            etree.XMLSyntaxError: If XML is malformed
        """
        if not file_path.exists():
            raise FileNotFoundError(f"XML file not found: {file_path}")

        try:
            # Parse XML with lxml
            tree = etree.parse(str(file_path))
            return self.parse_tree(tree)

        except etree.XMLSyntaxError as e:
            self.logger.error(f"XML syntax error in {file_path}: {e}")
            raise

        except Exception as e:
            self.logger.error(f"Error parsing XML file {file_path}: {e}", exc_info=True)
            raise

    def parse_tree(self, tree: etree._ElementTree) -> Dict[str, Any]:
        """
        Parse an XML tree.

        Args:
            tree: lxml ElementTree

        Returns:
            Dictionary with structural information
        """
        root = tree.getroot()

        # Extract basic information
        result = {
            'root_element': self._strip_namespace(root.tag),
            'root_attributes': dict(root.attrib),
            'namespaces': self._extract_namespaces(root),
            'elements': self._count_elements_by_tag(root),
        }

        return result

    def extract_beans(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Extract Spring bean definitions.

        Args:
            file_path: Path to Spring XML config

        Returns:
            List of bean information
        """
        try:
            tree = etree.parse(str(file_path))
            root = tree.getroot()

            beans = []

            # Find all bean elements (with namespace support)
            # Try common Spring namespaces
            bean_elements = root.xpath(
                '//bean | //ns:bean',
                namespaces={'ns': 'http://www.springframework.org/schema/beans'}
            )

            for bean_elem in bean_elements:
                bean_info = {
                    'id': bean_elem.get('id'),
                    'name': bean_elem.get('name'),
                    'class': bean_elem.get('class'),
                    'scope': bean_elem.get('scope'),
                }

                # Remove None values
                bean_info = {k: v for k, v in bean_info.items() if v is not None}

                if bean_info:
                    beans.append(bean_info)

            return beans

        except Exception as e:
            self.logger.error(f"Error extracting beans: {e}", exc_info=True)
            return []

    def extract_elements_by_tag(
        self,
        file_path: Path,
        tag_name: str,
        namespace: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Extract elements by tag name.

        Args:
            file_path: Path to XML file
            tag_name: Tag name to search for
            namespace: Optional namespace URI

        Returns:
            List of element information
        """
        try:
            tree = etree.parse(str(file_path))
            root = tree.getroot()

            elements = []

            # Build XPath expression
            if namespace:
                xpath = f'//ns:{tag_name}'
                namespaces = {'ns': namespace}
            else:
                # Search with and without namespace
                xpath = f'//{tag_name} | //*[local-name()="{tag_name}"]'
                namespaces = None

            matching_elements = root.xpath(xpath, namespaces=namespaces) if namespaces else root.xpath(xpath)

            for elem in matching_elements:
                elem_info = {
                    'tag': self._strip_namespace(elem.tag),
                    'attributes': dict(elem.attrib),
                    'text': elem.text.strip() if elem.text else None,
                }

                # Add child elements summary
                elem_info['children'] = [
                    self._strip_namespace(child.tag)
                    for child in elem
                ]

                elements.append(elem_info)

            return elements

        except Exception as e:
            self.logger.error(f"Error extracting elements by tag: {e}", exc_info=True)
            return []

    def _strip_namespace(self, tag: str) -> str:
        """
        Strip namespace from tag.

        Args:
            tag: Tag name (possibly with namespace)

        Returns:
            Tag name without namespace
        """
        # Ensure tag is a string
        tag_str = str(tag) if not isinstance(tag, str) else tag

        if '}' in tag_str:
            return tag_str.split('}', 1)[1]
        return tag_str

    def _extract_namespaces(self, root: etree._Element) -> Dict[str, str]:
        """
        Extract namespaces from root element.

        Args:
            root: Root XML element

        Returns:
            Dictionary of prefix -> URI mappings
        """
        return dict(root.nsmap) if hasattr(root, 'nsmap') else {}

    def _count_elements_by_tag(self, root: etree._Element) -> Dict[str, int]:
        """
        Count elements by tag name.

        Args:
            root: Root XML element

        Returns:
            Dictionary of tag -> count mappings
        """
        counts = {}

        for elem in root.iter():
            # Skip non-Element nodes (comments, processing instructions, etc.)
            if not isinstance(elem.tag, str) and not isinstance(elem.tag, bytes):
                continue

            tag = self._strip_namespace(elem.tag)
            counts[tag] = counts.get(tag, 0) + 1

        return counts


# ==============================================================================
# Standalone Functions
# ==============================================================================

def parse_xml_file(file_path: Path) -> Dict[str, Any]:
    """
    Parse an XML file (convenience function).

    Args:
        file_path: Path to XML file

    Returns:
        Dictionary with parsed elements
    """
    parser = XMLParser()
    return parser.parse_file(file_path)


def extract_root_element(file_path: Path) -> str:
    """
    Extract root element name (convenience function).

    Args:
        file_path: Path to XML file

    Returns:
        Root element name
    """
    parser = XMLParser()
    result = parser.parse_file(file_path)
    return result['root_element']


def extract_namespaces(file_path: Path) -> Dict[str, str]:
    """
    Extract namespaces (convenience function).

    Args:
        file_path: Path to XML file

    Returns:
        Dictionary of namespaces
    """
    parser = XMLParser()
    result = parser.parse_file(file_path)
    return result['namespaces']


def extract_beans(file_path: Path) -> List[Dict[str, Any]]:
    """
    Extract Spring beans (convenience function).

    Args:
        file_path: Path to Spring XML config

    Returns:
        List of bean information
    """
    parser = XMLParser()
    return parser.extract_beans(file_path)


def extract_elements_by_tag(
    file_path: Path,
    tag_name: str,
    namespace: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Extract elements by tag (convenience function).

    Args:
        file_path: Path to XML file
        tag_name: Tag name to search for
        namespace: Optional namespace URI

    Returns:
        List of element information
    """
    parser = XMLParser()
    return parser.extract_elements_by_tag(file_path, tag_name, namespace)
