from java_parser import JavaParser
import os
from typing import List, Dict, Any
import json
from pathlib import Path
import logging
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import concurrent.futures
from tree_sitter import Language, Parser
from chroma_manager import ChromaManager

class CodebaseProcessor:
    def __init__(self, codebase_path: str, db_path: str = "chroma_db", batch_size: int = 40000, use_remote: bool = False):
        """Initialize the codebase processor."""
        self.codebase_path = Path(codebase_path)
        self.parser = JavaParser()
        self.chroma_manager = ChromaManager(persist_directory=db_path, use_remote=use_remote)
        
        # Initialize Tree-sitter parser
        self.tree_sitter_parser = Parser()
        self.tree_sitter_parser.set_language(Language('build/my-languages.so', 'java'))
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        self.batch_size = batch_size

    def find_java_files(self) -> List[Path]:
        """Find all Java files in the codebase."""
        java_files = []
        for path in self.codebase_path.rglob("*.java"):
            java_files.append(path)
        return java_files

    def process_file(self, file_path: Path) -> Dict[str, Any]:
        """Process a single Java file and return its structure."""
        try:
            result = self.parser.parse_file(str(file_path))
            result['file_path'] = str(file_path)
            return result
        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {str(e)}")
            return None

    def create_snippets(self, file_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create code snippets for different code elements."""
        snippets = []
        
        # Create snippet for the entire file
        file_snippet = {
            'id': f"{Path(file_data['file_path']).stem}_file",
            'code': json.dumps(file_data),
            'metadata': {
                'type': 'file',
                'path': file_data['file_path']
            }
        }
        snippets.append(file_snippet)

        # Create snippets for each class
        for class_data in file_data.get('classes', []):
            class_snippet = {
                'id': f"{Path(file_data['file_path']).stem}_{class_data['name']}_class",
                'code': json.dumps(class_data),
                'metadata': {
                    'type': 'class',
                    'path': file_data['file_path'],
                    'name': class_data['name']
                }
            }
            snippets.append(class_snippet)

            # Create snippets for methods
            for method in class_data.get('methods', []):
                method_snippet = {
                    'id': f"{Path(file_data['file_path']).stem}_{class_data['name']}_{method['name']}_method",
                    'code': json.dumps(method),
                    'metadata': {
                        'type': 'method',
                        'path': file_data['file_path'],
                        'class': class_data['name'],
                        'name': method['name']
                    }
                }
                snippets.append(method_snippet)

        return snippets

    def process_codebase(self):
        """Process the entire codebase and store embeddings."""
        # Find all Java files
        java_files = list(Path(self.codebase_path).rglob("*.java"))
        self.logger.info(f"Found {len(java_files)} Java files")
        
        # Process files in parallel
        all_snippets = []
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self._process_file, file) for file in java_files]
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Processing files"):
                result = future.result()
                if result:
                    all_snippets.extend(result)
        
        # Process in batches
        total_items = len(all_snippets)
        for i in range(0, total_items, self.batch_size):
            end_idx = min(i + self.batch_size, total_items)
            self.logger.info(f"Processing batch {i//self.batch_size + 1} of {(total_items + self.batch_size - 1)//self.batch_size}")
            
            batch_snippets = all_snippets[i:end_idx]
            self.chroma_manager.add_code_snippets(batch_snippets)
        
        self.logger.info(f"Stored {total_items} code snippets in vector database")

    def _process_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Process a single Java file and return its snippets."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the file
            tree = self.tree_sitter_parser.parse(bytes(content, 'utf8'))
            
            # Extract code elements
            elements = self._extract_elements(tree.root_node, content)
            
            if not elements:
                return []
            
            # Create snippets
            snippets = []
            for element in elements:
                snippet = {
                    'id': f"{file_path.stem}_{element.get('name', '')}_{element['type']}",
                    'code': element['content'],
                    'metadata': {
                        'path': str(file_path),
                        'type': element['type'],
                        'name': element.get('name', ''),
                        'class': element.get('class', '')
                    }
                }
                snippets.append(snippet)
            
            return snippets
            
        except Exception as e:
            self.logger.error(f"Error processing file {file_path}: {str(e)}")
            return []

    def _extract_elements(self, node, content: str) -> List[Dict[str, Any]]:
        """Extract code elements from the AST."""
        elements = []
        
        def traverse(node, class_name=None):
            if node.type == 'class_declaration':
                class_name = self._get_node_text(node.child_by_field_name('name'), content)
                elements.append({
                    'type': 'class',
                    'name': class_name,
                    'content': self._get_node_text(node, content)
                })
            
            elif node.type == 'method_declaration' and class_name:
                method_name = self._get_node_text(node.child_by_field_name('name'), content)
                elements.append({
                    'type': 'method',
                    'name': method_name,
                    'class': class_name,
                    'content': self._get_node_text(node, content)
                })
            
            # Recursively process child nodes
            for child in node.children:
                traverse(child, class_name)
        
        traverse(node)
        return elements

    def _get_node_text(self, node, content: str) -> str:
        """Get the text content of a node."""
        return content[node.start_byte:node.end_byte]

    def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search the codebase for relevant code."""
        return self.chroma_manager.search_similar_code(query, n_results)

def main():
    # Example usage
    processor = CodebaseProcessor("java_codebase")
    
    # Process the codebase
    processor.process_codebase()
    
    # Example search
    results = processor.search("Find classes that handle user authentication")
    print("\nSearch Results:")
    for result in results:
        print(f"\nType: {result['metadata']['type']}")
        print(f"Path: {result['metadata']['path']}")
        if result['metadata']['type'] == 'method':
            print(f"Class: {result['metadata']['class']}")
            print(f"Method: {result['metadata']['name']}")
        elif result['metadata']['type'] == 'class':
            print(f"Class: {result['metadata']['name']}")
        print(f"Content: {result['code']}")

if __name__ == "__main__":
    main() 