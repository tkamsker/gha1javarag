"""
Maven POM parser service.

Parses Maven pom.xml files to extract dependency declarations.
Uses xml.etree.ElementTree for parsing (stdlib, no external dependencies).
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List
import logging

from ..models.maven_dependency import MavenDependency

log = logging.getLogger(__name__)

# Maven POM namespace
MAVEN_NS = {"mvn": "http://maven.apache.org/POM/4.0.0"}


def parse_pom(pom_path: Path, depth: int = 0) -> List[MavenDependency]:
    """
    Parse Maven pom.xml and extract dependency declarations.

    Implements FR-001: Parse pom.xml files to extract dependency declarations.
    Uses xml.etree.ElementTree per research.md decision.

    Args:
        pom_path: Absolute path to pom.xml file
        depth: Current dependency depth (0=direct, 1+=transitive)

    Returns:
        List of MavenDependency objects with group_id, artifact_id, version, scope

    Raises:
        FileNotFoundError: If pom.xml doesn't exist
        ET.ParseError: If XML is malformed

    Example:
        >>> from pathlib import Path
        >>> deps = parse_pom(Path("project/pom.xml"))
        >>> len(deps)
        3
        >>> deps[0].artifact_id
        'cuco-cct-core'
    """
    # Validate file exists
    if not pom_path.exists():
        raise FileNotFoundError(f"pom.xml not found: {pom_path}")

    try:
        # Parse XML with namespace handling
        tree = ET.parse(pom_path)
        root = tree.getroot()

        dependencies = []

        # Find all <dependency> elements
        # Try with namespace first, then without for compatibility
        dep_elements = root.findall(".//mvn:dependency", MAVEN_NS)
        if not dep_elements:
            # Fallback: try without namespace
            dep_elements = root.findall(".//dependency")

        for dep_elem in dep_elements:
            # Extract groupId and artifactId (required)
            # Note: Must check 'is not None' explicitly because ElementTree elements
            # with no children evaluate to False in boolean context
            group_id_elem = dep_elem.find("mvn:groupId", MAVEN_NS)
            if group_id_elem is None:
                group_id_elem = dep_elem.find("groupId")

            artifact_id_elem = dep_elem.find("mvn:artifactId", MAVEN_NS)
            if artifact_id_elem is None:
                artifact_id_elem = dep_elem.find("artifactId")

            # Skip if missing required fields
            if group_id_elem is None or artifact_id_elem is None:
                log.warning(
                    f"Incomplete dependency in {pom_path}: missing groupId or artifactId"
                )
                continue

            if not group_id_elem.text or not artifact_id_elem.text:
                log.warning(
                    f"Empty groupId or artifactId in {pom_path}"
                )
                continue

            # Extract version and scope (optional)
            version_elem = dep_elem.find("mvn:version", MAVEN_NS)
            if version_elem is None:
                version_elem = dep_elem.find("version")

            scope_elem = dep_elem.find("mvn:scope", MAVEN_NS)
            if scope_elem is None:
                scope_elem = dep_elem.find("scope")

            version = version_elem.text if version_elem is not None else None
            scope = scope_elem.text if scope_elem is not None else "compile"

            # Create dependency object
            dependency = MavenDependency(
                group_id=group_id_elem.text,
                artifact_id=artifact_id_elem.text,
                version=version,
                scope=scope,
                declared_in=pom_path,
                depth=depth
            )

            dependencies.append(dependency)

        log.info(f"Parsed {len(dependencies)} dependencies from {pom_path}")
        return dependencies

    except ET.ParseError as e:
        log.error(f"XML parse error in {pom_path}: {e}")
        raise
