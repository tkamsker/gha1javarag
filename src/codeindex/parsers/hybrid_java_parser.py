"""
Hybrid Java Parser - javalang + Regex Fallback

Provides robust Java parsing using a two-tier approach:
1. Primary: javalang AST parsing (preferred, full syntax tree)
2. Fallback: Regex parsing (when javalang fails or is unavailable)

This ensures the system can handle:
- Standard Java 8 code (javalang)
- Malformed or incomplete code (regex)
- Environments without javalang installed (regex)
"""

import logging
import re
from pathlib import Path
from typing import List, Dict, Any, Optional


logger = logging.getLogger(__name__)


# Try to import javalang, but don't fail if not available
try:
    import javalang
    JAVALANG_AVAILABLE = True
    logger.debug("javalang is available for Java parsing")
except ImportError:
    JAVALANG_AVAILABLE = False
    logger.warning("javalang not available, will use regex fallback for Java parsing")


class HybridJavaParser:
    """
    Hybrid Java parser using javalang (primary) + regex (fallback).

    Follows the hybrid parsing strategy defined in research.md:
    - Try javalang AST parsing first (preferred)
    - Fall back to regex if javalang fails
    - Log parsing method used for debugging
    """

    def __init__(self):
        """Initialize hybrid Java parser."""
        self.logger = logging.getLogger(__name__)
        self.javalang_available = JAVALANG_AVAILABLE

    def parse_method_signatures(self, file_path: Path, content: str) -> List[Dict[str, Any]]:
        """
        Extract method signatures from Java source code.

        Args:
            file_path: Path to Java file
            content: Java source code

        Returns:
            List of method signatures with name, return type, parameters, exceptions

        Example:
            [
                {
                    "name": "createUser",
                    "return_type": "UserDTO",
                    "parameters": [{"name": "dto", "type": "UserDTO"}],
                    "exceptions": ["RemoteException"],
                    "visibility": "public"
                }
            ]
        """
        if self.javalang_available:
            try:
                return self._parse_with_javalang(content)
            except Exception as e:
                self.logger.debug(f"javalang failed for {file_path}, using regex fallback: {e}")
                return self._parse_with_regex(content)
        else:
            return self._parse_with_regex(content)

    def _parse_with_javalang(self, content: str) -> List[Dict[str, Any]]:
        """
        Parse Java code using javalang AST.

        Args:
            content: Java source code

        Returns:
            List of method signatures

        Raises:
            Exception: If javalang parsing fails
        """
        tree = javalang.parse.parse(content)
        methods = []

        for path, node in tree.filter(javalang.tree.MethodDeclaration):
            # Only extract public methods
            if node.modifiers and 'public' in node.modifiers:
                method_info = {
                    "name": node.name,
                    "return_type": self._extract_type(node.return_type),
                    "parameters": self._extract_parameters(node.parameters),
                    "exceptions": self._extract_exceptions(node.throws),
                    "visibility": "public"
                }
                methods.append(method_info)

        self.logger.debug(f"javalang extracted {len(methods)} methods")
        return methods

    def _extract_type(self, type_node) -> str:
        """
        Extract type name from javalang type node.

        Args:
            type_node: javalang type node

        Returns:
            Type name as string
        """
        if type_node is None:
            return "void"

        if hasattr(type_node, 'name'):
            # Simple type
            type_name = type_node.name
        elif hasattr(type_node, 'type'):
            # Array or parameterized type
            type_name = self._extract_type(type_node.type)
            if hasattr(type_node, 'dimensions') and type_node.dimensions:
                type_name += "[]" * len(type_node.dimensions)
        else:
            type_name = str(type_node)

        # Handle generic types
        if hasattr(type_node, 'arguments') and type_node.arguments:
            args = [self._extract_type(arg.type) for arg in type_node.arguments]
            type_name += f"<{', '.join(args)}>"

        return type_name

    def _extract_parameters(self, parameters) -> List[Dict[str, Any]]:
        """
        Extract parameter information from javalang parameters.

        Args:
            parameters: List of javalang parameter nodes

        Returns:
            List of parameter dictionaries
        """
        if not parameters:
            return []

        params = []
        for param in parameters:
            param_info = {
                "name": param.name,
                "type": self._extract_type(param.type),
                "is_dto": param.type.name.endswith("DTO") if hasattr(param.type, 'name') else False
            }
            params.append(param_info)

        return params

    def _extract_exceptions(self, throws) -> List[str]:
        """
        Extract exception types from javalang throws clause.

        Args:
            throws: List of javalang exception nodes

        Returns:
            List of exception type names
        """
        if not throws:
            return []

        return [exc if isinstance(exc, str) else str(exc) for exc in throws]

    def _parse_with_regex(self, content: str) -> List[Dict[str, Any]]:
        """
        Parse Java code using regex patterns.

        This is a fallback for when javalang fails or is unavailable.
        It extracts method signatures using pattern matching.

        Args:
            content: Java source code

        Returns:
            List of method signatures
        """
        methods = []

        # Regex pattern for public method signatures
        # Matches: public ReturnType methodName(ParamType paramName, ...) throws Exception
        method_pattern = re.compile(
            r'public\s+' +                                      # public modifier
            r'(?:static\s+)?' +                                 # optional static
            r'(?:<[^>]+>\s+)?' +                                # optional generic type params
            r'(\w+(?:<[^>]+>)?(?:\[\])?)\s+' +                 # return type (group 1)
            r'(\w+)\s*' +                                       # method name (group 2)
            r'\(([^)]*)\)' +                                    # parameters (group 3)
            r'(?:\s+throws\s+([^{;]+))?' +                     # optional throws clause (group 4)
            r'\s*[{;]',                                         # method body or semicolon
            re.MULTILINE
        )

        for match in method_pattern.finditer(content):
            return_type = match.group(1).strip()
            method_name = match.group(2).strip()
            params_str = match.group(3).strip()
            throws_str = match.group(4).strip() if match.group(4) else ""

            # Parse parameters
            parameters = self._parse_parameters_regex(params_str)

            # Parse exceptions
            exceptions = [exc.strip() for exc in throws_str.split(',') if exc.strip()]

            method_info = {
                "name": method_name,
                "return_type": return_type,
                "parameters": parameters,
                "exceptions": exceptions,
                "visibility": "public"
            }
            methods.append(method_info)

        self.logger.debug(f"Regex extracted {len(methods)} methods")
        return methods

    def _parse_parameters_regex(self, params_str: str) -> List[Dict[str, Any]]:
        """
        Parse method parameters from parameter string using regex.

        Args:
            params_str: Parameter string (e.g., "UserDTO dto, String name")

        Returns:
            List of parameter dictionaries
        """
        if not params_str:
            return []

        parameters = []

        # Split by comma, but handle generics (e.g., List<String>)
        # Simple approach: split and then parse each parameter
        param_parts = []
        current_part = ""
        angle_depth = 0

        for char in params_str + ",":
            if char == '<':
                angle_depth += 1
                current_part += char
            elif char == '>':
                angle_depth -= 1
                current_part += char
            elif char == ',' and angle_depth == 0:
                param_parts.append(current_part.strip())
                current_part = ""
            else:
                current_part += char

        # Parse each parameter
        for param in param_parts:
            if not param:
                continue

            # Match: Type name or Type<Generic> name or Type[] name
            param_match = re.match(r'([\w<>\[\],\s]+)\s+(\w+)$', param.strip())
            if param_match:
                param_type = param_match.group(1).strip()
                param_name = param_match.group(2).strip()

                param_info = {
                    "name": param_name,
                    "type": param_type,
                    "is_dto": param_type.endswith("DTO")
                }
                parameters.append(param_info)

        return parameters

    def extract_class_info(self, content: str) -> Dict[str, Any]:
        """
        Extract basic class information from Java source.

        Args:
            content: Java source code

        Returns:
            Dictionary with class name, package, extends, implements
        """
        class_info = {
            "package": None,
            "class_name": None,
            "extends": None,
            "implements": []
        }

        # Extract package
        package_match = re.search(r'package\s+([\w.]+)\s*;', content)
        if package_match:
            class_info["package"] = package_match.group(1)

        # Extract class name and inheritance
        class_match = re.search(
            r'public\s+(?:class|interface)\s+(\w+)' +
            r'(?:\s+extends\s+([\w.]+))?' +
            r'(?:\s+implements\s+([\w.,\s]+))?' +
            r'\s*[{]',
            content
        )

        if class_match:
            class_info["class_name"] = class_match.group(1)

            if class_match.group(2):
                class_info["extends"] = class_match.group(2).strip()

            if class_match.group(3):
                implements_str = class_match.group(3)
                class_info["implements"] = [
                    impl.strip() for impl in implements_str.split(',')
                ]

        return class_info

    def extract_fields(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract field declarations from Java source.

        Args:
            content: Java source code

        Returns:
            List of field dictionaries with name, type, visibility
        """
        fields = []

        # Pattern for field declarations
        field_pattern = re.compile(
            r'(private|protected|public)\s+' +
            r'(?:static\s+)?(?:final\s+)?' +
            r'([\w<>\[\]]+)\s+' +
            r'(\w+)\s*[;=]',
            re.MULTILINE
        )

        for match in field_pattern.finditer(content):
            field_info = {
                "visibility": match.group(1),
                "type": match.group(2),
                "name": match.group(3)
            }
            fields.append(field_info)

        return fields

    def extract_annotations(self, content: str) -> List[str]:
        """
        Extract annotations from Java source.

        Args:
            content: Java source code

        Returns:
            List of annotation names (without @)
        """
        annotation_pattern = re.compile(r'@(\w+)(?:\([^)]*\))?')
        annotations = annotation_pattern.findall(content)
        return list(set(annotations))  # Unique annotations
