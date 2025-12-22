"""
Structural analyzer service for fallback code analysis without LLM.

Provides fast, reliable structural analysis using Java AST parsing when
Ollama timeouts occur. Extracts basic metadata like class names, methods,
imports, and annotations without semantic understanding.
"""

import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)

# Try to import javalang for Java parsing
try:
    import javalang
    JAVALANG_AVAILABLE = True
except ImportError:
    JAVALANG_AVAILABLE = False
    logger.warning(
        "javalang not available - structural analysis will be limited. "
        "Install with: pip install javalang"
    )


class StructuralAnalyzer:
    """
    Provides structural code analysis without LLM.

    Uses Java AST parsing (javalang) to extract basic structural metadata
    when Ollama timeouts occur. Fast (<100ms per file) and reliable.
    """

    def __init__(self):
        """Initialize structural analyzer"""
        self.logger = logging.getLogger(__name__)

        if not JAVALANG_AVAILABLE:
            self.logger.warning(
                "Structural analyzer initialized without javalang - "
                "functionality will be limited"
            )

    def extract_basic_metadata(
        self,
        file_path: str,
        file_content: str
    ) -> Dict[str, Any]:
        """
        Extract basic structural metadata from Java code without LLM.

        Uses javalang to parse Java AST and extract:
        - Class name
        - Package name
        - Import statements
        - Method names
        - Annotations
        - Superclass
        - Implemented interfaces

        Args:
            file_path: Absolute path to source file
            file_content: Full Java source code content

        Returns:
            Dict with basic metadata:
            - class_name: str
            - package: str
            - imports: List[str]
            - methods: List[str]
            - annotations: List[str]
            - super_class: Optional[str]
            - interfaces: List[str]

        Raises:
            ParseError: If Java AST parsing fails
            ValueError: If javalang is not available
        """
        if not JAVALANG_AVAILABLE:
            return self._minimal_fallback(file_path, file_content)

        try:
            # Parse Java code to AST
            tree = javalang.parse.parse(file_content)

            # Extract metadata
            metadata = {
                'class_name': None,
                'package': None,
                'imports': [],
                'methods': [],
                'annotations': [],
                'super_class': None,
                'interfaces': [],
                'source': 'structural_analysis'
            }

            # Extract package
            if tree.package:
                metadata['package'] = tree.package.name

            # Extract imports
            if tree.imports:
                metadata['imports'] = [imp.path for imp in tree.imports]

            # Extract classes and their metadata
            for path, node in tree.filter(javalang.tree.ClassDeclaration):
                # Use first class found (main class)
                if metadata['class_name'] is None:
                    metadata['class_name'] = node.name

                    # Extract superclass
                    if node.extends:
                        metadata['super_class'] = node.extends.name

                    # Extract interfaces
                    if node.implements:
                        metadata['interfaces'] = [iface.name for iface in node.implements]

                    # Extract class annotations
                    if node.annotations:
                        metadata['annotations'].extend([ann.name for ann in node.annotations])

                    # Extract methods
                    for method_node in node.methods:
                        metadata['methods'].append(method_node.name)

                        # Extract method annotations
                        if method_node.annotations:
                            metadata['annotations'].extend([ann.name for ann in method_node.annotations])

            # Deduplicate annotations
            metadata['annotations'] = list(set(metadata['annotations']))

            self.logger.debug(
                f"Structural analysis complete: {metadata['class_name']} "
                f"with {len(metadata['methods'])} methods"
            )

            return metadata

        except javalang.parser.JavaSyntaxError as e:
            self.logger.warning(
                f"Java syntax error in {Path(file_path).name}: {e}"
            )
            raise ParseError(
                f"Failed to parse Java file {file_path}: {e}"
            ) from e

        except Exception as e:
            self.logger.error(
                f"Unexpected error during structural analysis of {Path(file_path).name}: {e}"
            )
            # Return minimal fallback rather than failing completely
            return self._minimal_fallback(file_path, file_content)

    def _minimal_fallback(
        self,
        file_path: str,
        file_content: str
    ) -> Dict[str, Any]:
        """
        Minimal fallback when javalang is unavailable or parsing fails.

        Uses simple regex patterns to extract basic information.

        Args:
            file_path: Path to file
            file_content: File content

        Returns:
            Dict with minimal metadata
        """
        import re

        metadata = {
            'class_name': None,
            'package': None,
            'imports': [],
            'methods': [],
            'annotations': [],
            'super_class': None,
            'interfaces': [],
            'source': 'minimal_fallback'
        }

        # Extract package name
        package_match = re.search(r'package\s+([\w.]+)\s*;', file_content)
        if package_match:
            metadata['package'] = package_match.group(1)

        # Extract class name
        class_match = re.search(
            r'(?:public\s+)?(?:abstract\s+)?(?:final\s+)?class\s+(\w+)',
            file_content
        )
        if class_match:
            metadata['class_name'] = class_match.group(1)
        else:
            # Use filename as fallback
            metadata['class_name'] = Path(file_path).stem

        # Extract imports (simple pattern)
        import_matches = re.findall(r'import\s+([\w.]+)\s*;', file_content)
        metadata['imports'] = import_matches

        # Extract method names (simple pattern - will miss some)
        method_matches = re.findall(
            r'(?:public|private|protected)?\s*(?:static\s+)?(?:\w+\s+)+(\w+)\s*\(',
            file_content
        )
        metadata['methods'] = list(set(method_matches))  # Deduplicate

        # Extract annotations (simple pattern)
        annotation_matches = re.findall(r'@(\w+)', file_content)
        metadata['annotations'] = list(set(annotation_matches))

        self.logger.debug(
            f"Minimal fallback analysis: {metadata['class_name']} "
            f"with {len(metadata['methods'])} methods (approximate)"
        )

        return metadata


class ParseError(Exception):
    """Exception raised when Java parsing fails"""
    pass
