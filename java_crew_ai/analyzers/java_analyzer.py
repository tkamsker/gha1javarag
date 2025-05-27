import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from tree_sitter import Language, Parser
import logging
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add file handler for logging
log_file = 'java_processing.log'
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class ComponentType(Enum):
    CLASS = "class"
    INTERFACE = "interface"
    ENUM = "enum"
    METHOD = "method"
    FIELD = "field"

@dataclass
class Component:
    name: str
    type: ComponentType
    path: str
    parent: Optional[str] = None
    children: List['Component'] = None
    dependencies: List[str] = None
    documentation: str = ""
    modifiers: List[str] = None
    return_type: Optional[str] = None
    parameters: List[Dict[str, str]] = None

class JavaCodeAnalyzer:
    def __init__(self, base_path: str):
        """Initialize the Java code analyzer."""
        self.base_path = Path(base_path)
        self.parser = self._initialize_parser()
        self.components: Dict[str, Component] = {}
        self.directory_structure: Dict[str, List[str]] = {}
        
    def _initialize_parser(self) -> Parser:
        """Initialize the tree-sitter parser for Java."""
        try:
            # Create build directory if it doesn't exist
            os.makedirs('build', exist_ok=True)
            
            # Build the Java grammar if it doesn't exist
            if not os.path.exists('build/my-languages.so'):
                Language.build_library(
                    'build/my-languages.so',
                    ['vendor/tree-sitter-java']
                )
            
            # Initialize parser
            parser = Parser()
            # Load the language from the shared library
            JAVA_LANGUAGE = Language('build/my-languages.so', 'java')
            # Set the language for the parser
            parser.set_language(JAVA_LANGUAGE)
            return parser
        except Exception as e:
            logger.error(f"Failed to initialize parser: {str(e)}")
            raise

    def analyze_codebase(self) -> Dict[str, Any]:
        """Analyze the entire codebase and return structured information."""
        try:
            # Scan directory structure
            self._scan_directory_structure()
            
            # Analyze each Java file
            for file_path in self._find_java_files():
                self._analyze_file(file_path)
            
            return {
                'directory_structure': self.directory_structure,
                'components': self._serialize_components()
            }
        except Exception as e:
            logger.error(f"Failed to analyze codebase: {str(e)}")
            raise

    def _scan_directory_structure(self):
        """Scan and map the directory structure."""
        for root, dirs, files in os.walk(self.base_path):
            relative_path = os.path.relpath(root, self.base_path)
            if relative_path == '.':
                relative_path = ''
            
            java_files = [f for f in files if f.endswith('.java')]
            if java_files:
                self.directory_structure[relative_path] = java_files

    def _find_java_files(self) -> List[Path]:
        """Find all Java files in the codebase."""
        java_files = []
        logger.info(f"Starting Java file search in base path: {self.base_path}")
        
        for path in self.base_path.rglob("*.java"):
            full_path = str(path.absolute())
            relative_path = str(path.relative_to(self.base_path))
            logger.info(f"Found Java file - Full path: {full_path}, Relative path: {relative_path}")
            java_files.append(path)
            
        logger.info(f"Total Java files found: {len(java_files)}")
        return java_files

    def _analyze_file(self, file_path: Path):
        """Analyze a single Java file and extract its components."""
        try:
            full_path = str(file_path.absolute())
            relative_path = str(file_path.relative_to(self.base_path))
            logger.info(f"Processing Java file - Full path: {full_path}, Relative path: {relative_path}")
            
            with open(file_path, 'rb') as f:
                source_code = f.read()
            
            tree = self.parser.parse(source_code)
            if not tree:
                logger.warning(f"Failed to parse file: {file_path}")
                return
            
            self._extract_components(tree.root_node, source_code, relative_path)
            logger.info(f"Successfully processed file: {relative_path}")
            
        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {str(e)}")

    def _extract_components(self, node, source_code: bytes, file_path: str):
        """Extract components from the AST."""
        if node.type in ['class_declaration', 'interface_declaration', 'enum_declaration']:
            self._extract_type_declaration(node, source_code, file_path)
        elif node.type == 'method_declaration':
            self._extract_method(node, source_code, file_path)
        elif node.type == 'field_declaration':
            self._extract_field(node, source_code, file_path)
        
        for child in node.children:
            self._extract_components(child, source_code, file_path)

    def _extract_type_declaration(self, node, source_code: bytes, file_path: str):
        """Extract class, interface, or enum declaration."""
        component_type = ComponentType.CLASS
        if node.type == 'interface_declaration':
            component_type = ComponentType.INTERFACE
        elif node.type == 'enum_declaration':
            component_type = ComponentType.ENUM
        
        name_node = node.child_by_field_name('name')
        if not name_node:
            return
        
        name = source_code[name_node.start_byte:name_node.end_byte].decode('utf-8')
        component = Component(
            name=name,
            type=component_type,
            path=file_path,
            children=[],
            dependencies=[],
            modifiers=self._extract_modifiers(node, source_code),
            documentation=self._extract_documentation(node, source_code)
        )
        
        self.components[f"{file_path}:{name}"] = component

    def _extract_method(self, node, source_code: bytes, file_path: str):
        """Extract method declaration."""
        name_node = node.child_by_field_name('name')
        if not name_node:
            return
        
        name = source_code[name_node.start_byte:name_node.end_byte].decode('utf-8')
        component = Component(
            name=name,
            type=ComponentType.METHOD,
            path=file_path,
            children=[],
            dependencies=[],
            modifiers=self._extract_modifiers(node, source_code),
            documentation=self._extract_documentation(node, source_code),
            return_type=self._extract_return_type(node, source_code),
            parameters=self._extract_parameters(node, source_code)
        )
        
        self.components[f"{file_path}:{name}"] = component

    def _extract_field(self, node, source_code: bytes, file_path: str):
        """Extract field declaration."""
        for child in node.children:
            if child.type == 'variable_declarator':
                name_node = child.child_by_field_name('name')
                if not name_node:
                    continue
                
                name = source_code[name_node.start_byte:name_node.end_byte].decode('utf-8')
                component = Component(
                    name=name,
                    type=ComponentType.FIELD,
                    path=file_path,
                    children=[],
                    dependencies=[],
                    modifiers=self._extract_modifiers(node, source_code),
                    documentation=self._extract_documentation(node, source_code)
                )
                
                self.components[f"{file_path}:{name}"] = component

    def _extract_modifiers(self, node, source_code: bytes) -> List[str]:
        """Extract modifiers from a node."""
        modifiers = []
        for child in node.children:
            if child.type == 'modifiers':
                for modifier in child.children:
                    modifiers.append(source_code[modifier.start_byte:modifier.end_byte].decode('utf-8'))
        return modifiers

    def _extract_documentation(self, node, source_code: bytes) -> str:
        """Extract documentation comments from a node."""
        if node.prev_sibling and node.prev_sibling.type == 'comment':
            return source_code[node.prev_sibling.start_byte:node.prev_sibling.end_byte].decode('utf-8')
        return ""

    def _extract_return_type(self, node, source_code: bytes) -> Optional[str]:
        """Extract return type from a method declaration."""
        type_node = node.child_by_field_name('type')
        if type_node:
            return source_code[type_node.start_byte:type_node.end_byte].decode('utf-8')
        return None

    def _extract_parameters(self, node, source_code: bytes) -> List[Dict[str, str]]:
        """Extract parameters from a method declaration."""
        parameters = []
        params_node = node.child_by_field_name('parameters')
        if params_node:
            for param in params_node.children:
                if param.type == 'formal_parameter':
                    param_info = {}
                    type_node = param.child_by_field_name('type')
                    name_node = param.child_by_field_name('name')
                    if type_node:
                        param_info['type'] = source_code[type_node.start_byte:type_node.end_byte].decode('utf-8')
                    if name_node:
                        param_info['name'] = source_code[name_node.start_byte:name_node.end_byte].decode('utf-8')
                    parameters.append(param_info)
        return parameters

    def _serialize_components(self) -> Dict[str, Dict]:
        """Convert components to a serializable format."""
        return {
            key: {
                'name': comp.name,
                'type': comp.type.value,
                'path': comp.path,
                'parent': comp.parent,
                'children': [c.name for c in (comp.children or [])],
                'dependencies': comp.dependencies,
                'documentation': comp.documentation,
                'modifiers': comp.modifiers,
                'return_type': comp.return_type,
                'parameters': comp.parameters
            }
            for key, comp in self.components.items()
        } 