from tree_sitter import Language, Parser
import os
from typing import Dict, List, Optional, Any
import json

class JavaParser:
    def __init__(self, grammar_path: str = 'build/java.so'):
        """Initialize the Java parser with the grammar file."""
        self.language = Language(grammar_path, 'java')
        self.parser = Parser()
        self.parser.set_language(self.language)

    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """Parse a Java file and extract its structure."""
        with open(file_path, 'rb') as f:
            source_code = f.read()
        
        tree = self.parser.parse(source_code)
        return self._extract_structure(tree.root_node, source_code)

    def _extract_structure(self, node: Any, source_code: bytes) -> Dict[str, Any]:
        """Extract the structure of a Java file."""
        result = {
            'classes': [],
            'imports': [],
            'package': None
        }

        # Process all top-level nodes
        for child in node.children:
            if child.type == 'package_declaration':
                result['package'] = self._get_text(child, source_code)
            elif child.type == 'import_declaration':
                result['imports'].append(self._get_text(child, source_code))
            elif child.type == 'class_declaration':
                result['classes'].append(self._extract_class(child, source_code))

        return result

    def _extract_class(self, node: Any, source_code: bytes) -> Dict[str, Any]:
        """Extract information about a Java class."""
        class_info = {
            'name': '',
            'modifiers': [],
            'fields': [],
            'methods': [],
            'constructors': [],
            'documentation': self._get_documentation(node, source_code)
        }

        # Extract class name and modifiers
        for child in node.children:
            if child.type == 'modifiers':
                class_info['modifiers'] = self._get_modifiers(child, source_code)
            elif child.type == 'identifier':
                class_info['name'] = self._get_text(child, source_code)
            elif child.type == 'class_body':
                self._extract_class_members(child, class_info, source_code)

        return class_info

    def _extract_class_members(self, node: Any, class_info: Dict[str, Any], source_code: bytes):
        """Extract members (fields, methods, constructors) from a class body."""
        for child in node.children:
            if child.type == 'field_declaration':
                class_info['fields'].append(self._extract_field(child, source_code))
            elif child.type == 'method_declaration':
                class_info['methods'].append(self._extract_method(child, source_code))
            elif child.type == 'constructor_declaration':
                class_info['constructors'].append(self._extract_constructor(child, source_code))

    def _extract_field(self, node: Any, source_code: bytes) -> Dict[str, Any]:
        """Extract information about a field."""
        field_info = {
            'name': '',
            'type': '',
            'modifiers': [],
            'documentation': self._get_documentation(node, source_code)
        }

        for child in node.children:
            if child.type == 'modifiers':
                field_info['modifiers'] = self._get_modifiers(child, source_code)
            elif child.type == 'type_identifier':
                field_info['type'] = self._get_text(child, source_code)
            elif child.type == 'variable_declarator':
                field_info['name'] = self._get_text(child.children[0], source_code)

        return field_info

    def _extract_method(self, node: Any, source_code: bytes) -> Dict[str, Any]:
        """Extract information about a method."""
        method_info = {
            'name': '',
            'return_type': '',
            'modifiers': [],
            'parameters': [],
            'documentation': self._get_documentation(node, source_code)
        }

        for child in node.children:
            if child.type == 'modifiers':
                method_info['modifiers'] = self._get_modifiers(child, source_code)
            elif child.type == 'type_identifier':
                method_info['return_type'] = self._get_text(child, source_code)
            elif child.type == 'identifier':
                method_info['name'] = self._get_text(child, source_code)
            elif child.type == 'formal_parameters':
                method_info['parameters'] = self._extract_parameters(child, source_code)

        return method_info

    def _extract_constructor(self, node: Any, source_code: bytes) -> Dict[str, Any]:
        """Extract information about a constructor."""
        constructor_info = {
            'name': '',
            'modifiers': [],
            'parameters': [],
            'documentation': self._get_documentation(node, source_code)
        }

        for child in node.children:
            if child.type == 'modifiers':
                constructor_info['modifiers'] = self._get_modifiers(child, source_code)
            elif child.type == 'identifier':
                constructor_info['name'] = self._get_text(child, source_code)
            elif child.type == 'formal_parameters':
                constructor_info['parameters'] = self._extract_parameters(child, source_code)

        return constructor_info

    def _extract_parameters(self, node: Any, source_code: bytes) -> List[Dict[str, str]]:
        """Extract method/constructor parameters."""
        parameters = []
        for child in node.children:
            if child.type == 'formal_parameter':
                param_info = {
                    'type': '',
                    'name': ''
                }
                for param_child in child.children:
                    if param_child.type == 'type_identifier':
                        param_info['type'] = self._get_text(param_child, source_code)
                    elif param_child.type == 'identifier':
                        param_info['name'] = self._get_text(param_child, source_code)
                parameters.append(param_info)
        return parameters

    def _get_modifiers(self, node: Any, source_code: bytes) -> List[str]:
        """Extract modifiers from a node."""
        return [self._get_text(child, source_code) for child in node.children]

    def _get_documentation(self, node: Any, source_code: bytes) -> Optional[str]:
        """Extract documentation comments from a node."""
        if node.prev_sibling and node.prev_sibling.type == 'comment':
            return self._get_text(node.prev_sibling, source_code)
        return None

    def _get_text(self, node: Any, source_code: bytes) -> str:
        """Get the text content of a node."""
        return source_code[node.start_byte:node.end_byte].decode('utf-8')

def main():
    # Example usage
    parser = JavaParser()
    
    # Test with a sample Java file
    java_code = """
    /**
     * A sample test class
     */
    public class TestClass {
        private String name;
        
        /**
         * Constructor for TestClass
         * @param name The name to set
         */
        public TestClass(String name) {
            this.name = name;
        }
        
        /**
         * Gets the name
         * @return The current name
         */
        public String getName() {
            return name;
        }
    }
    """
    
    # Create a temporary file for testing
    with open('test.java', 'w') as f:
        f.write(java_code)
    
    # Parse the file
    result = parser.parse_file('test.java')
    
    # Print the result in a readable format
    print(json.dumps(result, indent=2))
    
    # Clean up
    os.remove('test.java')

if __name__ == "__main__":
    main() 