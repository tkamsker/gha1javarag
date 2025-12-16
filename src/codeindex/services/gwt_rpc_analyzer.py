"""
GWT RPC Servlet Analyzer

Analyzes GWT RPC servlet implementations to extract:
- RPC method signatures (parameters, return types, exceptions)
- Service interface references
- Referenced DTOs

Implements FR-002 and FR-003 from the specification.
"""

import logging
import re
from pathlib import Path
from typing import List, Dict, Any, Optional

from codeindex.parsers.hybrid_java_parser import HybridJavaParser
from codeindex.utils.gwt_patterns import (
    GwtRole,
    is_gwt_rpc_servlet,
    contains_remote_service_servlet
)


logger = logging.getLogger(__name__)


class GwtRpcAnalyzer:
    """
    Analyzer for GWT RPC servlet implementations.

    Extracts RPC method signatures, service interfaces, and DTO references
    using hybrid parsing (javalang + regex fallback).
    """

    def __init__(self):
        """Initialize GWT RPC analyzer."""
        self.logger = logging.getLogger(__name__)
        self.parser = HybridJavaParser()

    def can_analyze(self, file_path: Path) -> bool:
        """
        Check if this analyzer can handle the file.

        Args:
            file_path: Path to Java file

        Returns:
            True if file is a GWT RPC servlet
        """
        is_servlet, confidence = is_gwt_rpc_servlet(file_path)
        return is_servlet

    def get_gwt_role(self) -> GwtRole:
        """
        Return the GWT role this analyzer produces.

        Returns:
            GwtRole.RPC_SERVLET
        """
        return GwtRole.RPC_SERVLET

    def analyze(
        self,
        file_path: Path,
        content: str,
        semantic_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze GWT RPC servlet and extract metadata.

        Args:
            file_path: Path to servlet file
            content: Java source code
            semantic_data: Optional LLM-extracted semantic data (not used yet)

        Returns:
            Dictionary with GWT RPC metadata matching data-model.md schema
        """
        self.logger.debug(f"Analyzing GWT RPC servlet: {file_path.name}")

        try:
            # Extract class information
            class_info = self.parser.extract_class_info(content)

            # Extract RPC methods using hybrid parser
            rpc_methods = self.extract_rpc_methods(file_path, content)

            # Identify service interface
            service_interface = self.identify_service_interface(file_path, content)

            # Extract DTOs/DAOs from imports and method signatures
            imported_dtos = self._extract_dtos_from_imports(content)
            imported_daos = self._extract_daos_from_imports(content)

            # Extract referenced DTOs from method signatures
            referenced_dtos = self.extract_referenced_dtos(rpc_methods, imported_dtos)

            # Build metadata matching data-model.md schema
            metadata = {
                'gwt_role': GwtRole.RPC_SERVLET.value,
                'servlet_name': class_info.get('class_name', file_path.stem),
                'service_interface': service_interface,
                'async_interface': f"{service_interface}Async" if service_interface else None,
                'url_mapping': self._extract_url_mapping(content),
                'base_class': class_info.get('extends', 'RemoteServiceServlet'),
                'rpc_methods': rpc_methods,
                'referenced_dtos': referenced_dtos,
                'referenced_daos': sorted(list(imported_daos)),
                'spring_annotations': self._extract_spring_annotations(content)
            }

            self.logger.info(
                f"Extracted {len(rpc_methods)} RPC methods from {file_path.name}, "
                f"{len(referenced_dtos)} DTOs referenced, {len(imported_daos)} DAOs referenced"
            )

            return metadata

        except Exception as e:
            self.logger.error(f"Error analyzing GWT RPC servlet {file_path}: {e}", exc_info=True)
            # Return minimal valid metadata
            return {
                'gwt_role': GwtRole.RPC_SERVLET.value,
                'servlet_name': file_path.stem,
                'service_interface': None,
                'async_interface': None,
                'url_mapping': None,
                'base_class': 'RemoteServiceServlet',
                'rpc_methods': [],
                'referenced_dtos': [],
                'referenced_daos': [],
                'spring_annotations': [],
                'error': str(e)
            }

    def extract_rpc_methods(self, file_path: Path, content: str) -> List[Dict[str, Any]]:
        """
        Extract all public RPC methods from servlet implementation.

        Uses hybrid approach:
        1. Try javalang AST parsing (preferred)
        2. Fall back to regex parsing if javalang fails

        Args:
            file_path: Path to servlet file
            content: Java source code

        Returns:
            List of RPC method dictionaries with name, return_type, parameters, exceptions
        """
        try:
            # Use hybrid parser's parse_method_signatures
            methods = self.parser.parse_method_signatures(file_path, content)

            self.logger.debug(f"Extracted {len(methods)} public methods from {file_path.name}")
            return methods

        except Exception as e:
            self.logger.error(f"Error extracting RPC methods: {e}", exc_info=True)
            return []

    def identify_service_interface(self, file_path: Path, content: str) -> Optional[str]:
        """
        Identify the service interface this servlet implements.

        Looks for:
        1. implements clause in class declaration
        2. Class name pattern (*ServiceImpl implements *Service)

        Args:
            file_path: Path to servlet file
            content: Java source code

        Returns:
            Service interface name or None
        """
        try:
            # Extract class info
            class_info = self.parser.extract_class_info(content)

            # Check implements clause
            implements = class_info.get('implements', [])

            # Filter out RemoteService (base interface)
            service_interfaces = [
                iface for iface in implements
                if iface != 'RemoteService' and not iface.startswith('com.google.gwt')
            ]

            if service_interfaces:
                # Return first non-base interface
                return service_interfaces[0]

            # Fallback: Try naming convention
            # *ServletImpl → *Service
            class_name = class_info.get('class_name', '')
            if class_name.endswith('ServletImpl'):
                service_name = class_name[:-10] + 'Service'
                return service_name
            elif class_name.endswith('Impl'):
                service_name = class_name[:-4]
                return service_name

            return None

        except Exception as e:
            self.logger.warning(f"Could not identify service interface: {e}")
            return None

    def extract_referenced_dtos(
        self,
        rpc_methods: List[Dict[str, Any]],
        imported_dtos: set
    ) -> List[str]:
        """
        Extract all DTO class names used in RPC methods.

        Args:
            rpc_methods: List of extracted RPC methods
            imported_dtos: Set of DTO class names from imports

        Returns:
            List of unique DTO class names
        """
        dto_set = set()

        for method in rpc_methods:
            # Extract from return type
            return_type = method.get('return_type', '')
            dto_set.update(self._extract_dto_from_type(return_type, imported_dtos))

            # Extract from parameters
            parameters = method.get('parameters', [])
            for param in parameters:
                param_type = param.get('type', '')
                dto_set.update(self._extract_dto_from_type(param_type, imported_dtos))

        # Return sorted list
        return sorted(list(dto_set))

    def _extract_dto_from_type(self, type_string: str, imported_dtos: set) -> set:
        """
        Extract DTO class names from a type string.

        Handles:
        - Simple types: UserDTO, InventoryProductGroup
        - Generic types: List<UserDTO>, ArrayList<Product>
        - Nested generics: Map<String, List<UserDTO>>

        Args:
            type_string: Java type string
            imported_dtos: Set of known DTO class names from imports

        Returns:
            Set of DTO class names
        """
        dtos = set()

        # Pattern 1: Match class names ending with DTO
        dto_pattern = re.compile(r'\b(\w+DTO)\b')
        for match in dto_pattern.finditer(type_string):
            dto_name = match.group(1)
            dtos.add(dto_name)

        # Pattern 2: Match any class name from imported DTOs
        # Extract all capitalized class names from type string
        class_pattern = re.compile(r'\b([A-Z][a-zA-Z0-9]*)\b')
        for match in class_pattern.finditer(type_string):
            class_name = match.group(1)
            # Check if this class is in the imported DTOs
            if class_name in imported_dtos:
                dtos.add(class_name)

        return dtos

    def _extract_dtos_from_imports(self, content: str) -> set:
        """
        Extract DTO class names from import statements.

        Looks for imports from packages containing .dto. or .shared.dto.

        Args:
            content: Java source code

        Returns:
            Set of DTO class names (simple names, not fully qualified)
        """
        dto_classes = set()

        # Pattern to match imports from .dto. or .shared.dto. packages
        import_pattern = re.compile(
            r'import\s+[\w.]+\.(?:shared\.)?dto\.(\w+)\s*;',
            re.MULTILINE
        )

        for match in import_pattern.finditer(content):
            class_name = match.group(1)
            dto_classes.add(class_name)

        return dto_classes

    def _extract_daos_from_imports(self, content: str) -> set:
        """
        Extract DAO class names from import statements.

        Looks for imports from packages containing .dao. or ending with DAO.

        Args:
            content: Java source code

        Returns:
            Set of DAO class names (simple names, not fully qualified)
        """
        dao_classes = set()

        # Pattern 1: Match imports from .dao. packages
        dao_package_pattern = re.compile(
            r'import\s+[\w.]+\.dao\.(?:\w+\.)?(\w+)\s*;',
            re.MULTILINE
        )

        for match in dao_package_pattern.finditer(content):
            class_name = match.group(1)
            dao_classes.add(class_name)

        # Pattern 2: Match imports of classes ending with DAO
        dao_suffix_pattern = re.compile(
            r'import\s+[\w.]+\.(\w+DAO)\s*;',
            re.MULTILINE
        )

        for match in dao_suffix_pattern.finditer(content):
            class_name = match.group(1)
            dao_classes.add(class_name)

        return dao_classes

    def _extract_url_mapping(self, content: str) -> Optional[str]:
        """
        Extract servlet URL mapping from annotations or comments.

        Args:
            content: Java source code

        Returns:
            URL mapping string or None
        """
        # Look for @RemoteServiceRelativePath annotation
        mapping_pattern = re.compile(r'@RemoteServiceRelativePath\s*\(\s*"([^"]+)"\s*\)')
        match = mapping_pattern.search(content)

        if match:
            return match.group(1)

        # Look for @WebServlet annotation
        web_servlet_pattern = re.compile(r'@WebServlet\s*\(\s*[^)]*urlPatterns\s*=\s*["{]([^"}]+)["}]')
        match = web_servlet_pattern.search(content)

        if match:
            return match.group(1)

        return None

    def _extract_spring_annotations(self, content: str) -> List[str]:
        """
        Extract Spring annotations if present.

        Args:
            content: Java source code

        Returns:
            List of Spring annotation names
        """
        spring_annotations = []

        # Common Spring annotations
        patterns = [
            r'@Service',
            r'@Component',
            r'@Controller',
            r'@RestController',
            r'@RequestMapping',
            r'@Autowired',
            r'@Transactional'
        ]

        for pattern in patterns:
            if re.search(pattern, content):
                annotation = pattern[1:]  # Remove @ prefix
                spring_annotations.append(annotation)

        return spring_annotations

    def _parse_with_regex(self, content: str) -> List[Dict[str, Any]]:
        """
        Expose regex parsing method for testing.

        Args:
            content: Java source code

        Returns:
            List of method signatures
        """
        return self.parser._parse_with_regex(content)
