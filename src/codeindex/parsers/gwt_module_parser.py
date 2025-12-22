"""
GWT module XML parser for extracting entry points and inherited modules.

Implements Feature 007 US3 T056-T058.

Parses *.gwt.xml files to extract:
- Entry point classes
- Inherited module names
- Module rename-to attribute
- Source paths and public paths
"""

import logging
from pathlib import Path
from typing import List, Optional
from lxml import etree

from codeindex.models.gwt_module import GWTModule

logger = logging.getLogger(__name__)


class GWTModuleParser:
    """
    Parser for GWT module XML files (*.gwt.xml).

    Uses lxml with namespace-aware XPath queries to extract module metadata.
    """

    # GWT module XML namespace (optional in many modules)
    GWT_NAMESPACE = "http://www.gwtproject.org/schema/gwt-module"

    def __init__(self):
        """Initialize GWT module parser."""
        self.logger = logging.getLogger(__name__)

    def parse_module(self, xml_file: Path) -> Optional[GWTModule]:
        """
        Parse a GWT module XML file.

        Implements T056, T057, T058.

        Args:
            xml_file: Path to *.gwt.xml file

        Returns:
            GWTModule object or None on parse failure

        Raises:
            FileNotFoundError: If XML file doesn't exist
        """
        if not xml_file.exists():
            raise FileNotFoundError(f"GWT module file not found: {xml_file}")

        self.logger.info(f"Parsing GWT module: {xml_file.name}")

        try:
            # Parse XML file
            tree = etree.parse(str(xml_file))
            root = tree.getroot()

            # Extract module metadata
            module_name = self._extract_module_name_from_file(xml_file)
            rename_to = root.get('rename-to')

            # Extract entry points (T057)
            entry_points = self._extract_entry_points(root)

            # Extract inherited modules (T058)
            inherits = self._extract_inherits(root)

            # Extract source and public paths
            source_paths = self._extract_source_paths(root)
            public_paths = self._extract_public_paths(root)

            # Create GWTModule object
            module = GWTModule(
                module_name=module_name,
                module_file=str(xml_file),
                rename_to=rename_to,
                entry_point_classes=entry_points,
                inherits=inherits,
                source_paths=source_paths,
                public_paths=public_paths
            )

            self.logger.info(
                f"Parsed GWT module '{module_name}': "
                f"{len(entry_points)} entry points, {len(inherits)} inherits"
            )

            return module

        except etree.XMLSyntaxError as e:
            self.logger.error(f"XML syntax error in {xml_file.name}: {e}")
            return None

        except Exception as e:
            self.logger.error(f"Failed to parse {xml_file.name}: {e}", exc_info=True)
            return None

    def _extract_module_name_from_file(self, xml_file: Path) -> str:
        """
        Extract module name from file path.

        Converts file path to module name:
        - src/com/example/Application.gwt.xml → com.example.Application
        - com/example/App.gwt.xml → com.example.App

        Args:
            xml_file: Path to GWT module XML

        Returns:
            Module name in dot notation
        """
        # Get relative path components
        parts = xml_file.parts

        # Find 'src' or 'java' directory as base
        try:
            if 'src' in parts:
                base_index = parts.index('src') + 1
            elif 'java' in parts:
                base_index = parts.index('java') + 1
            else:
                # No standard base, use last few components
                base_index = max(0, len(parts) - 4)
        except ValueError:
            base_index = 0

        # Extract package path
        package_parts = parts[base_index:]

        # Remove filename and .gwt.xml extension
        module_name_parts = list(package_parts[:-1])  # Remove filename
        module_name_parts.append(xml_file.stem.replace('.gwt', ''))  # Add module name without .gwt

        # Join with dots
        module_name = '.'.join(module_name_parts)

        return module_name

    def _extract_entry_points(self, root: etree._Element) -> List[str]:
        """
        Extract entry-point classes from GWT module.

        Implements T057.

        Uses XPath: //entry-point/@class

        Args:
            root: XML root element

        Returns:
            List of fully-qualified entry-point class names
        """
        entry_points: List[str] = []

        try:
            # XPath without namespace
            elements = root.xpath('//entry-point[@class]')

            for element in elements:
                entry_class = element.get('class')
                if entry_class:
                    entry_points.append(entry_class)
                    self.logger.debug(f"Found entry-point: {entry_class}")

            # Try with namespace if no results
            if not entry_points:
                namespaces = {'gwt': self.GWT_NAMESPACE}
                elements = root.xpath('//gwt:entry-point[@class]', namespaces=namespaces)

                for element in elements:
                    entry_class = element.get('class')
                    if entry_class:
                        entry_points.append(entry_class)
                        self.logger.debug(f"Found entry-point (with namespace): {entry_class}")

        except Exception as e:
            self.logger.error(f"Error extracting entry points: {e}")

        return entry_points

    def _extract_inherits(self, root: etree._Element) -> List[str]:
        """
        Extract inherited module names from GWT module.

        Implements T058.

        Uses XPath: //inherits/@name

        Args:
            root: XML root element

        Returns:
            List of inherited module names
        """
        inherits: List[str] = []

        try:
            # XPath without namespace
            elements = root.xpath('//inherits[@name]')

            for element in elements:
                module_name = element.get('name')
                if module_name:
                    inherits.append(module_name)
                    self.logger.debug(f"Found inherits: {module_name}")

            # Try with namespace if no results
            if not inherits:
                namespaces = {'gwt': self.GWT_NAMESPACE}
                elements = root.xpath('//gwt:inherits[@name]', namespaces=namespaces)

                for element in elements:
                    module_name = element.get('name')
                    if module_name:
                        inherits.append(module_name)
                        self.logger.debug(f"Found inherits (with namespace): {module_name}")

        except Exception as e:
            self.logger.error(f"Error extracting inherits: {e}")

        return inherits

    def _extract_source_paths(self, root: etree._Element) -> List[str]:
        """
        Extract source paths from GWT module.

        Uses XPath: //source/@path

        Args:
            root: XML root element

        Returns:
            List of source path names
        """
        source_paths: List[str] = []

        try:
            # XPath without namespace
            elements = root.xpath('//source[@path]')

            for element in elements:
                path = element.get('path')
                if path:
                    source_paths.append(path)
                    self.logger.debug(f"Found source path: {path}")

            # Try with namespace if no results
            if not source_paths:
                namespaces = {'gwt': self.GWT_NAMESPACE}
                elements = root.xpath('//gwt:source[@path]', namespaces=namespaces)

                for element in elements:
                    path = element.get('path')
                    if path:
                        source_paths.append(path)

        except Exception as e:
            self.logger.debug(f"Error extracting source paths: {e}")

        return source_paths

    def _extract_public_paths(self, root: etree._Element) -> List[str]:
        """
        Extract public paths from GWT module.

        Uses XPath: //public/@path

        Args:
            root: XML root element

        Returns:
            List of public path names
        """
        public_paths: List[str] = []

        try:
            # XPath without namespace
            elements = root.xpath('//public[@path]')

            for element in elements:
                path = element.get('path')
                if path:
                    public_paths.append(path)
                    self.logger.debug(f"Found public path: {path}")

            # Try with namespace if no results
            if not public_paths:
                namespaces = {'gwt': self.GWT_NAMESPACE}
                elements = root.xpath('//gwt:public[@path]', namespaces=namespaces)

                for element in elements:
                    path = element.get('path')
                    if path:
                        public_paths.append(path)

        except Exception as e:
            self.logger.debug(f"Error extracting public paths: {e}")

        return public_paths


# ==============================================================================
# Standalone Functions
# ==============================================================================

def parse_module(xml_file: Path) -> Optional[GWTModule]:
    """
    Parse GWT module XML file (convenience function).

    Args:
        xml_file: Path to *.gwt.xml file

    Returns:
        GWTModule object or None on failure
    """
    parser = GWTModuleParser()
    return parser.parse_module(xml_file)
