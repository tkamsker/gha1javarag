"""
Maven POM parser service.

Parses Maven pom.xml files to extract project metadata, dependencies,
modules, and build configuration.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from lxml import etree

logger = logging.getLogger(__name__)


class POMParseError(Exception):
    """Exception raised when POM parsing fails."""
    pass


# XML namespace handling
MAVEN_NS = {
    'mvn': 'http://maven.apache.org/POM/4.0.0'
}


def _get_text(element: etree._Element, xpath: str, namespaces: Optional[Dict] = None) -> Optional[str]:
    """
    Extract text from XML element using XPath.

    Args:
        element: XML element to search
        xpath: XPath expression
        namespaces: XML namespaces (optional)

    Returns:
        Text content or None if not found
    """
    if namespaces:
        result = element.xpath(xpath, namespaces=namespaces)
    else:
        result = element.xpath(xpath)

    if result and len(result) > 0:
        if isinstance(result[0], str):
            return result[0].strip()
        elif hasattr(result[0], 'text'):
            return result[0].text.strip() if result[0].text else None
    return None


def _get_elements(element: etree._Element, xpath: str, namespaces: Optional[Dict] = None) -> List[etree._Element]:
    """
    Get list of XML elements using XPath.

    Args:
        element: XML element to search
        xpath: XPath expression
        namespaces: XML namespaces (optional)

    Returns:
        List of matching elements
    """
    if namespaces:
        return element.xpath(xpath, namespaces=namespaces)
    else:
        return element.xpath(xpath)


def extract_maven_coordinates(tree: etree._ElementTree) -> Dict[str, Any]:
    """
    Extract Maven coordinates from POM XML tree.

    Args:
        tree: Parsed XML tree or root element

    Returns:
        Dictionary with groupId, artifactId, version, packaging, name, description
    """
    if isinstance(tree, etree._ElementTree):
        root = tree.getroot()
    else:
        root = tree

    # Try with namespace first, then without
    coords = {}

    # Try with namespace - use ./ to only match direct children of project root
    # This avoids matching groupId/artifactId from dependencies or parent sections
    group_id = _get_text(root, './mvn:groupId', MAVEN_NS)
    artifact_id = _get_text(root, './mvn:artifactId', MAVEN_NS)
    version = _get_text(root, './mvn:version', MAVEN_NS)
    packaging = _get_text(root, './mvn:packaging', MAVEN_NS)
    name = _get_text(root, './mvn:name', MAVEN_NS)
    description = _get_text(root, './mvn:description', MAVEN_NS)

    # Try without namespace if not found
    if not artifact_id:
        group_id = _get_text(root, './groupId')
        artifact_id = _get_text(root, './artifactId')
        version = _get_text(root, './version')
        packaging = _get_text(root, './packaging')
        name = _get_text(root, './name')
        description = _get_text(root, './description')

    # Check for parent coordinates (may inherit groupId/version from parent)
    parent_group_id = _get_text(root, './/mvn:parent/mvn:groupId', MAVEN_NS)
    parent_version = _get_text(root, './/mvn:parent/mvn:version', MAVEN_NS)

    if not parent_group_id:
        parent_group_id = _get_text(root, './/parent/groupId')
        parent_version = _get_text(root, './/parent/version')

    coords['groupId'] = group_id
    coords['artifactId'] = artifact_id
    coords['version'] = version
    coords['packaging'] = packaging or 'jar'  # Maven default
    coords['name'] = name
    coords['description'] = description

    if parent_group_id:
        coords['parentGroupId'] = parent_group_id
    if parent_version:
        coords['parentVersion'] = parent_version

    return coords


def extract_modules(tree: etree._ElementTree) -> List[str]:
    """
    Extract module list from POM XML tree.

    Args:
        tree: Parsed XML tree or root element

    Returns:
        List of module names
    """
    if isinstance(tree, etree._ElementTree):
        root = tree.getroot()
    else:
        root = tree

    modules = []

    # Try with namespace
    module_elements = _get_elements(root, './/mvn:modules/mvn:module', MAVEN_NS)

    # Try without namespace if not found
    if not module_elements:
        module_elements = _get_elements(root, './/modules/module')

    for module_elem in module_elements:
        if module_elem.text:
            modules.append(module_elem.text.strip())

    return modules


def extract_dependencies(
    tree: etree._ElementTree,
    include_scope: bool = False
) -> List[str]:
    """
    Extract dependency list from POM XML tree.

    Args:
        tree: Parsed XML tree or root element
        include_scope: Whether to include scope in output

    Returns:
        List of dependency coordinates (groupId:artifactId:version)
    """
    if isinstance(tree, etree._ElementTree):
        root = tree.getroot()
    else:
        root = tree

    dependencies = []

    # Try with namespace
    dep_elements = _get_elements(root, './/mvn:dependencies/mvn:dependency', MAVEN_NS)

    # Try without namespace if not found
    if not dep_elements:
        dep_elements = _get_elements(root, './/dependencies/dependency')

    for dep_elem in dep_elements:
        # Extract coordinates
        if MAVEN_NS:
            group_id = _get_text(dep_elem, './mvn:groupId', MAVEN_NS)
            artifact_id = _get_text(dep_elem, './mvn:artifactId', MAVEN_NS)
            version = _get_text(dep_elem, './mvn:version', MAVEN_NS)
            scope = _get_text(dep_elem, './mvn:scope', MAVEN_NS)

        if not group_id:
            group_id = _get_text(dep_elem, './groupId')
            artifact_id = _get_text(dep_elem, './artifactId')
            version = _get_text(dep_elem, './version')
            scope = _get_text(dep_elem, './scope')

        if artifact_id:
            # Build coordinate string
            coord = f"{group_id}:{artifact_id}" if group_id else artifact_id
            if version:
                coord += f":{version}"

            if include_scope and scope:
                coord += f" (scope={scope})"

            dependencies.append(coord)

    return dependencies


def extract_build_config(tree: etree._ElementTree) -> Dict[str, Any]:
    """
    Extract build configuration from POM XML tree.

    Args:
        tree: Parsed XML tree or root element

    Returns:
        Dictionary with sourceDirectory, testSourceDirectory, resources
    """
    if isinstance(tree, etree._ElementTree):
        root = tree.getroot()
    else:
        root = tree

    config = {}

    # Try with namespace
    source_dir = _get_text(root, './/mvn:build/mvn:sourceDirectory', MAVEN_NS)
    test_dir = _get_text(root, './/mvn:build/mvn:testSourceDirectory', MAVEN_NS)

    # Try without namespace
    if not source_dir:
        source_dir = _get_text(root, './/build/sourceDirectory')
        test_dir = _get_text(root, './/build/testSourceDirectory')

    # Maven defaults
    config['sourceDirectory'] = source_dir or 'src/main/java'
    config['testSourceDirectory'] = test_dir or 'src/test/java'

    # Extract resource directories
    resources = []
    resource_elements = _get_elements(root, './/mvn:build/mvn:resources/mvn:resource', MAVEN_NS)

    if not resource_elements:
        resource_elements = _get_elements(root, './/build/resources/resource')

    for resource_elem in resource_elements:
        resource_dir = _get_text(resource_elem, './mvn:directory', MAVEN_NS)
        if not resource_dir:
            resource_dir = _get_text(resource_elem, './directory')

        if resource_dir:
            resources.append({'directory': resource_dir})

    # Default resource directory if none specified
    if not resources:
        resources.append({'directory': 'src/main/resources'})

    config['resources'] = resources

    return config


class MavenParser:
    """
    Maven POM parser.

    Parses Maven pom.xml files to extract project metadata, dependencies,
    modules, and build configuration.
    """

    def __init__(self):
        """Initialize Maven parser."""
        self.logger = logging.getLogger(__name__)

    def parse_pom(self, pom_path: Path) -> Dict[str, Any]:
        """
        Parse a Maven POM file.

        Args:
            pom_path: Path to pom.xml file

        Returns:
            Dictionary with all extracted POM data

        Raises:
            FileNotFoundError: If POM file doesn't exist
            POMParseError: If POM parsing fails
        """
        if not pom_path.exists():
            raise FileNotFoundError(f"POM file not found: {pom_path}")

        try:
            # Parse XML
            tree = etree.parse(str(pom_path))

            # Extract all components
            result = {}

            # Coordinates
            coords = extract_maven_coordinates(tree)
            result.update(coords)

            # Validate required fields
            if not result.get('artifactId'):
                raise POMParseError(f"POM missing required field: artifactId")

            # Modules
            modules = extract_modules(tree)
            result['modules'] = modules

            # Dependencies
            dependencies = extract_dependencies(tree)
            result['dependencies'] = dependencies

            # Build config
            build_config = extract_build_config(tree)
            result.update(build_config)

            self.logger.debug(
                f"Parsed POM {pom_path}: {result.get('artifactId')} "
                f"with {len(modules)} modules, {len(dependencies)} dependencies"
            )

            return result

        except etree.XMLSyntaxError as e:
            raise POMParseError(f"Invalid XML in POM {pom_path}: {e}")
        except Exception as e:
            if isinstance(e, (FileNotFoundError, POMParseError)):
                raise
            raise POMParseError(f"Failed to parse POM {pom_path}: {e}")


# Convenience functions for external use
def parse_pom_file(pom_path: Path) -> Dict[str, Any]:
    """
    Parse a Maven POM file (convenience function).

    Args:
        pom_path: Path to pom.xml file

    Returns:
        Dictionary with all extracted POM data
    """
    parser = MavenParser()
    return parser.parse_pom(pom_path)
