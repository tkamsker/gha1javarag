"""
JSP (JavaServer Pages) file parser.

Extracts structural information from JSP files including:
- Page directives
- Taglib declarations
- Scriptlets, expressions, declarations
- JSP custom tags
- EL (Expression Language) expressions
"""

import re
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


# ==============================================================================
# Regular Expressions
# ==============================================================================

# JSP Directives: <%@ directive attr="value" %>
DIRECTIVE_PATTERN = re.compile(
    r'<%@\s*(\w+)\s+(.*?)\s*%>',
    re.DOTALL
)

# Taglib directive specifically
TAGLIB_PATTERN = re.compile(
    r'<%@\s*taglib\s+uri="([^"]+)"\s+prefix="([^"]+)"\s*%>',
    re.DOTALL
)

# JSP Declarations: <%! ... %>
DECLARATION_PATTERN = re.compile(
    r'<%!\s*(.*?)\s*%>',
    re.DOTALL
)

# JSP Scriptlets: <% ... %> (but not <%@ or <%! or <%=)
SCRIPTLET_PATTERN = re.compile(
    r'<%(?![@!=])\s*(.*?)\s*%>',
    re.DOTALL
)

# JSP Expressions: <%= ... %>
EXPRESSION_PATTERN = re.compile(
    r'<%=\s*(.*?)\s*%>',
    re.DOTALL
)

# JSP Comments: <%-- ... --%>
COMMENT_PATTERN = re.compile(
    r'<%--.*?--%>',
    re.DOTALL
)

# EL Expressions: ${...}
EL_EXPRESSION_PATTERN = re.compile(
    r'\$\{([^}]+)\}',
    re.DOTALL
)

# JSP Custom Tags: <prefix:tagname ...>
JSP_TAG_PATTERN = re.compile(
    r'<([\w]+):([\w]+)([^>]*)(?:/>|>)',
    re.DOTALL
)


# ==============================================================================
# JSPParser Class
# ==============================================================================

class JSPParser:
    """
    Parser for JSP files.

    Extracts structural information using regex patterns.
    """

    def __init__(self):
        """Initialize JSP parser."""
        self.logger = logging.getLogger(__name__)

    def parse_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Parse a JSP file.

        Args:
            file_path: Path to JSP file

        Returns:
            Dictionary with parsed elements

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        if not file_path.exists():
            raise FileNotFoundError(f"JSP file not found: {file_path}")

        content = file_path.read_text(encoding='utf-8')
        return self.parse(content)

    def parse(self, content: str) -> Dict[str, Any]:
        """
        Parse JSP source code.

        Args:
            content: JSP source code as string

        Returns:
            Dictionary with structural information
        """
        try:
            # Extract all elements
            result = {
                'directives': self.extract_directives(content),
                'taglibs': self.extract_taglibs(content),
                'declarations': self.extract_declarations(content),
                'scriptlets': self.extract_scriptlets(content),
                'expressions': self.extract_expressions(content),
                'jsp_tags': self.extract_jsp_tags(content),
                'el_expressions': self.extract_el_expressions(content),
            }

            return result

        except Exception as e:
            self.logger.error(f"Error parsing JSP code: {e}", exc_info=True)
            # Return minimal result on error
            return {
                'directives': [],
                'taglibs': [],
                'declarations': [],
                'scriptlets': [],
                'expressions': [],
                'jsp_tags': [],
                'el_expressions': [],
                'parse_error': str(e)
            }

    def extract_directives(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract JSP directives (page, include, taglib).

        Args:
            content: JSP source code

        Returns:
            List of directive information
        """
        directives = []

        for match in DIRECTIVE_PATTERN.finditer(content):
            directive_type = match.group(1)
            attributes_str = match.group(2)

            # Parse attributes
            attributes = self._parse_attributes(attributes_str)

            directive = {
                'type': directive_type,
                'attributes': attributes,
                'raw': match.group(0)
            }

            directives.append(directive)

        return directives

    def extract_taglibs(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract taglib declarations.

        Args:
            content: JSP source code

        Returns:
            List of taglib information
        """
        taglibs = []

        for match in TAGLIB_PATTERN.finditer(content):
            uri = match.group(1)
            prefix = match.group(2)

            taglib = {
                'uri': uri,
                'prefix': prefix,
                'raw': match.group(0)
            }

            taglibs.append(taglib)

        return taglibs

    def extract_declarations(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract JSP declarations (<%! ... %>).

        Args:
            content: JSP source code

        Returns:
            List of declaration information
        """
        declarations = []

        for match in DECLARATION_PATTERN.finditer(content):
            code = match.group(1).strip()

            declaration = {
                'code': code,
                'raw': match.group(0)
            }

            declarations.append(declaration)

        return declarations

    def extract_scriptlets(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract JSP scriptlets (<% ... %>).

        Args:
            content: JSP source code

        Returns:
            List of scriptlet information
        """
        scriptlets = []

        for match in SCRIPTLET_PATTERN.finditer(content):
            code = match.group(1).strip()

            scriptlet = {
                'code': code,
                'raw': match.group(0)
            }

            scriptlets.append(scriptlet)

        return scriptlets

    def extract_expressions(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract JSP expressions (<%= ... %>).

        Args:
            content: JSP source code

        Returns:
            List of expression information
        """
        expressions = []

        for match in EXPRESSION_PATTERN.finditer(content):
            code = match.group(1).strip()

            expression = {
                'code': code,
                'raw': match.group(0)
            }

            expressions.append(expression)

        return expressions

    def extract_jsp_tags(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract JSP custom tags (<prefix:tagname>).

        Args:
            content: JSP source code

        Returns:
            List of tag information
        """
        tags = []
        seen = set()  # Avoid duplicates

        for match in JSP_TAG_PATTERN.finditer(content):
            prefix = match.group(1)
            tag_name = match.group(2)
            attributes_str = match.group(3)

            # Create unique key
            tag_key = f"{prefix}:{tag_name}"

            if tag_key not in seen:
                seen.add(tag_key)

                # Parse attributes
                attributes = self._parse_attributes(attributes_str)

                tag = {
                    'prefix': prefix,
                    'name': f"{prefix}:{tag_name}",
                    'tag': tag_name,
                    'attributes': attributes,
                    'raw': match.group(0)
                }

                tags.append(tag)

        return tags

    def extract_el_expressions(self, content: str) -> List[str]:
        """
        Extract EL (Expression Language) expressions.

        Args:
            content: JSP source code

        Returns:
            List of EL expressions (without ${})
        """
        expressions = []

        for match in EL_EXPRESSION_PATTERN.finditer(content):
            expr = match.group(1).strip()
            expressions.append(expr)

        return expressions

    def _parse_attributes(self, attributes_str: str) -> Dict[str, str]:
        """
        Parse attribute string into dict.

        Args:
            attributes_str: Attribute string (key="value" ...)

        Returns:
            Dictionary of attributes
        """
        attributes = {}

        # Pattern: name="value" or name='value'
        attr_pattern = re.compile(r'(\w+)\s*=\s*["\']([^"\']*)["\']')

        for match in attr_pattern.finditer(attributes_str):
            attr_name = match.group(1)
            attr_value = match.group(2)
            attributes[attr_name] = attr_value

        return attributes


# ==============================================================================
# Standalone Functions
# ==============================================================================

def parse_jsp_file(file_path: Path) -> Dict[str, Any]:
    """
    Parse a JSP file (convenience function).

    Args:
        file_path: Path to JSP file

    Returns:
        Dictionary with parsed elements
    """
    parser = JSPParser()
    return parser.parse_file(file_path)


def extract_directives(content: str) -> List[Dict[str, Any]]:
    """
    Extract JSP directives (convenience function).

    Args:
        content: JSP source code

    Returns:
        List of directive information
    """
    parser = JSPParser()
    return parser.extract_directives(content)


def extract_taglibs(content: str) -> List[Dict[str, Any]]:
    """
    Extract taglib declarations (convenience function).

    Args:
        content: JSP source code

    Returns:
        List of taglib information
    """
    parser = JSPParser()
    return parser.extract_taglibs(content)


def extract_scriptlets(content: str) -> List[Dict[str, Any]]:
    """
    Extract JSP scriptlets (convenience function).

    Args:
        content: JSP source code

    Returns:
        List of scriptlet information
    """
    parser = JSPParser()
    return parser.extract_scriptlets(content)


def extract_expressions(content: str) -> List[Dict[str, Any]]:
    """
    Extract JSP expressions (convenience function).

    Args:
        content: JSP source code

    Returns:
        List of expression information
    """
    parser = JSPParser()
    return parser.extract_expressions(content)


def extract_declarations(content: str) -> List[Dict[str, Any]]:
    """
    Extract JSP declarations (convenience function).

    Args:
        content: JSP source code

    Returns:
        List of declaration information
    """
    parser = JSPParser()
    return parser.extract_declarations(content)


def extract_jsp_tags(content: str) -> List[Dict[str, Any]]:
    """
    Extract JSP custom tags (convenience function).

    Args:
        content: JSP source code

    Returns:
        List of tag information
    """
    parser = JSPParser()
    return parser.extract_jsp_tags(content)


def extract_el_expressions(content: str) -> List[str]:
    """
    Extract EL expressions (convenience function).

    Args:
        content: JSP source code

    Returns:
        List of EL expressions
    """
    parser = JSPParser()
    return parser.extract_el_expressions(content)
