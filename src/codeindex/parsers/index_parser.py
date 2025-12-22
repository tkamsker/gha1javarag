"""
Index HTML/JSP parser for extracting GWT module references.

Implements Feature 007 US3 T053-T055.

Extracts GWT module names from:
- HTML <script src="Module/Module.nocache.js"> tags
- Inline JavaScript __gwt_activeModules declarations
- JSP include directives and scriptlets
"""

import re
import logging
from pathlib import Path
from typing import List, Set
from lxml import html, etree

logger = logging.getLogger(__name__)


class IndexParser:
    """
    Parser for index.html and index.jsp files to extract GWT module references.

    Supports multiple detection methods:
    - XPath queries for <script> tags
    - Regex patterns for inline scripts and JSP directives
    """

    def __init__(self):
        """Initialize index parser."""
        self.logger = logging.getLogger(__name__)

    def extract_gwt_modules(self, index_file: Path) -> List[str]:
        """
        Extract GWT module names from index.html or index.jsp.

        Implements T053, T054, T055.

        Args:
            index_file: Path to index.html or index.jsp

        Returns:
            List of GWT module names (e.g., ['com.example.Application'])

        Raises:
            FileNotFoundError: If index file doesn't exist
        """
        if not index_file.exists():
            raise FileNotFoundError(f"Index file not found: {index_file}")

        self.logger.info(f"Parsing index file: {index_file.name}")

        # Read file content
        try:
            with open(index_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            self.logger.error(f"Failed to read {index_file}: {e}")
            return []

        modules: Set[str] = set()

        # Method 1: XPath queries for <script> tags (T053)
        html_modules = self._extract_from_html_script_tags(content)
        modules.update(html_modules)

        # Method 2: Regex for inline __gwt_activeModules (T054)
        inline_modules = self._extract_from_inline_scripts(content)
        modules.update(inline_modules)

        # Method 3: JSP include/directive parsing (T055)
        if index_file.suffix == '.jsp':
            jsp_modules = self._extract_from_jsp_directives(content)
            modules.update(jsp_modules)

        self.logger.info(f"Extracted {len(modules)} GWT modules from {index_file.name}")
        return sorted(list(modules))

    def _extract_from_html_script_tags(self, content: str) -> List[str]:
        """
        Extract GWT modules from <script src="..."> tags using XPath.

        Implements T053.

        Args:
            content: HTML content

        Returns:
            List of module names extracted from script tags
        """
        modules: List[str] = []

        try:
            # Parse HTML with lxml
            doc = html.fromstring(content)

            # XPath: Find all <script> tags with src attribute
            script_elements = doc.xpath('//script[@src]')

            for script in script_elements:
                src = script.get('src', '')

                # Extract module name from script src
                # Pattern: "Module/Module.nocache.js" or "path/Module/Module.nocache.js"
                module_name = self._extract_module_name_from_script_src(src)

                if module_name:
                    modules.append(module_name)
                    self.logger.debug(f"Found GWT module from script tag: {module_name}")

        except etree.ParserError as e:
            self.logger.warning(f"HTML parsing failed, falling back to regex: {e}")
            # Fallback to regex if lxml fails
            modules.extend(self._extract_script_tags_with_regex(content))

        except Exception as e:
            self.logger.error(f"Error parsing HTML script tags: {e}")

        return modules

    def _extract_module_name_from_script_src(self, src: str) -> str:
        """
        Extract GWT module name from script src attribute.

        Handles patterns:
        - "com.example.Application/com.example.Application.nocache.js"
        - "../modules/com.example.App/com.example.App.nocache.js"
        - "Application/Application.nocache.js"

        Args:
            src: Script src attribute value

        Returns:
            Module name or empty string if not a GWT module
        """
        # Check if this is a GWT module script (ends with .nocache.js)
        if not src.endswith('.nocache.js'):
            return ''

        # Extract module name from path
        # Pattern: ModuleName/ModuleName.nocache.js
        match = re.search(r'([a-zA-Z0-9._]+)/\1\.nocache\.js', src)
        if match:
            return match.group(1)

        # Alternative pattern: just extract from filename
        # com.example.Application.nocache.js → com.example.Application
        match = re.search(r'([a-zA-Z0-9._]+)\.nocache\.js$', src)
        if match:
            return match.group(1)

        return ''

    def _extract_script_tags_with_regex(self, content: str) -> List[str]:
        """
        Fallback regex extraction for script tags if lxml fails.

        Args:
            content: HTML content

        Returns:
            List of module names
        """
        modules: List[str] = []

        # Pattern: <script src="...nocache.js">
        script_pattern = re.compile(
            r'<script[^>]*src\s*=\s*["\']([^"\']*\.nocache\.js)["\']',
            re.IGNORECASE
        )

        for match in script_pattern.finditer(content):
            src = match.group(1)
            module_name = self._extract_module_name_from_script_src(src)

            if module_name:
                modules.append(module_name)
                self.logger.debug(f"Found GWT module via regex: {module_name}")

        return modules

    def _extract_from_inline_scripts(self, content: str) -> List[str]:
        """
        Extract GWT modules from inline __gwt_activeModules JavaScript.

        Implements T054.

        Handles patterns:
        - __gwt_activeModules['com.example.Application'] = {...}
        - __gwt_activeModules["com.example.Application"] = {...}
        - __gwt_activeModules.com_example_Application = {...}

        Args:
            content: HTML/JavaScript content

        Returns:
            List of module names from inline scripts
        """
        modules: List[str] = []

        # Pattern 1: __gwt_activeModules['moduleName']
        pattern1 = re.compile(
            r'__gwt_activeModules\s*\[\s*["\']([a-zA-Z0-9._]+)["\']\s*\]',
            re.MULTILINE
        )

        for match in pattern1.finditer(content):
            module_name = match.group(1)
            modules.append(module_name)
            self.logger.debug(f"Found GWT module from __gwt_activeModules: {module_name}")

        # Pattern 2: __gwt_activeModules.com_example_Application (property access)
        pattern2 = re.compile(
            r'__gwt_activeModules\.([a-zA-Z0-9_]+)',
            re.MULTILINE
        )

        for match in pattern2.finditer(content):
            property_name = match.group(1)
            # Convert property format to module format: com_example_App → com.example.App
            module_name = property_name.replace('_', '.')
            modules.append(module_name)
            self.logger.debug(f"Found GWT module from property access: {module_name}")

        return modules

    def _extract_from_jsp_directives(self, content: str) -> List[str]:
        """
        Extract GWT modules from JSP include directives and scriptlets.

        Implements T055.

        Handles patterns:
        - <%@ include file="/path/to/com.example.Application.jsp" %>
        - <%@ page import="com.example.client.Application" %>
        - <% String moduleName = "com.example.Application"; %>

        Args:
            content: JSP content

        Returns:
            List of module names from JSP directives
        """
        modules: List[str] = []

        # Pattern 1: JSP include directives
        # <%@ include file="/path/to/ModuleName.jsp" %>
        include_pattern = re.compile(
            r'<%@\s*include\s+file\s*=\s*"[^"]*?([a-zA-Z0-9._]+)\.jsp"',
            re.IGNORECASE | re.MULTILINE
        )

        for match in include_pattern.finditer(content):
            module_name = match.group(1)
            # Filter out common JSP includes (header, footer, etc.)
            if not module_name.lower() in ['header', 'footer', 'nav', 'sidebar', 'common']:
                modules.append(module_name)
                self.logger.debug(f"Found GWT module from JSP include: {module_name}")

        # Pattern 2: JSP page import directives
        # <%@ page import="com.example.client.Application" %>
        import_pattern = re.compile(
            r'<%@\s*page\s+import\s*=\s*"([a-zA-Z0-9._]+\.client\.[a-zA-Z0-9._]+)"',
            re.IGNORECASE | re.MULTILINE
        )

        for match in import_pattern.finditer(content):
            full_class = match.group(1)
            # Extract package as module name (e.g., com.example.client.Application → com.example.Application)
            parts = full_class.split('.')
            if len(parts) >= 3:
                # Assume module name is package up to 'client'
                client_index = parts.index('client') if 'client' in parts else -1
                if client_index > 0:
                    module_name = '.'.join(parts[:client_index] + [parts[-1]])
                    modules.append(module_name)
                    self.logger.debug(f"Found GWT module from JSP import: {module_name}")

        # Pattern 3: JSP scriptlet with string literals
        # <% String moduleName = "com.example.Application"; %>
        scriptlet_pattern = re.compile(
            r'<%[^%]*["\']([a-zA-Z0-9._]{3,})["\'][^%]*%>',
            re.MULTILINE
        )

        for match in scriptlet_pattern.finditer(content):
            potential_module = match.group(1)
            # Only consider strings that look like module names (at least 2 dots)
            if potential_module.count('.') >= 2:
                modules.append(potential_module)
                self.logger.debug(f"Found potential GWT module from JSP scriptlet: {potential_module}")

        return modules


# ==============================================================================
# Standalone Functions
# ==============================================================================

def extract_gwt_modules(index_file: Path) -> List[str]:
    """
    Extract GWT modules from index file (convenience function).

    Args:
        index_file: Path to index.html or index.jsp

    Returns:
        List of GWT module names
    """
    parser = IndexParser()
    return parser.extract_gwt_modules(index_file)
