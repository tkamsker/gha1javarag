from java_parser import JavaParser
import os
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
import json
from pathlib import Path
import logging
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import concurrent.futures
from tree_sitter import Language, Parser
import numpy as np
from sentence_transformers import SentenceTransformer

class CodebaseProcessor:
    def __init__(self, codebase_path: str, db_path: str = "chroma_db", batch_size: int = 40000):
        """Initialize the codebase processor."""
        self.codebase_path = Path(codebase_path)
        self.parser = JavaParser()
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(
            name="java_code",
            metadata={"description": "Java codebase embeddings"}
        )
        
        # Initialize Tree-sitter parser
        self.tree_sitter_parser = Parser()
        self.tree_sitter_parser.set_language(Language('build/my-languages.so', 'java'))
        
        # Initialize sentence transformer model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
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

    def create_embeddings(self, file_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create embeddings for different code elements."""
        embeddings = []
        
        # Create embedding for the entire file
        file_content = {
            'type': 'file',
            'path': file_data['file_path'],
            'content': json.dumps(file_data)
        }
        embeddings.append(file_content)

        # Create embeddings for each class
        for class_data in file_data.get('classes', []):
            class_content = {
                'type': 'class',
                'path': file_data['file_path'],
                'name': class_data['name'],
                'content': json.dumps(class_data)
            }
            embeddings.append(class_content)

            # Create embeddings for methods
            for method in class_data.get('methods', []):
                method_content = {
                    'type': 'method',
                    'path': file_data['file_path'],
                    'class': class_data['name'],
                    'name': method['name'],
                    'content': json.dumps(method)
                }
                embeddings.append(method_content)

        return embeddings

    def process_codebase(self):
        """Process the entire codebase and store embeddings."""
        # Find all Java files
        java_files = list(Path(self.codebase_path).rglob("*.java"))
        self.logger.info(f"Found {len(java_files)} Java files")
        
        # Process files in parallel
        all_embeddings = []
        all_metadatas = []
        all_documents = []
        all_ids = []
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self._process_file, file) for file in java_files]
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Processing files"):
                result = future.result()
                if result:
                    embeddings, metadata, document, doc_id = result
                    all_embeddings.extend(embeddings)
                    all_metadatas.extend(metadata)
                    all_documents.extend(document)
                    all_ids.extend(doc_id)
        
        # Process in batches
        total_items = len(all_embeddings)
        for i in range(0, total_items, self.batch_size):
            end_idx = min(i + self.batch_size, total_items)
            self.logger.info(f"Processing batch {i//self.batch_size + 1} of {(total_items + self.batch_size - 1)//self.batch_size}")
            
            batch_embeddings = all_embeddings[i:end_idx]
            batch_metadatas = all_metadatas[i:end_idx]
            batch_documents = all_documents[i:end_idx]
            batch_ids = all_ids[i:end_idx]
            
            self.collection.add(
                embeddings=batch_embeddings,
                metadatas=batch_metadatas,
                documents=batch_documents,
                ids=batch_ids
            )
        
        self.logger.info(f"Stored {total_items} embeddings in vector database")

    def _process_file(self, file_path: Path) -> tuple:
        """Process a single Java file and return its embeddings."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the file
            tree = self.tree_sitter_parser.parse(bytes(content, 'utf8'))
            
            # Extract code elements
            elements = self._extract_elements(tree.root_node, content)
            
            if not elements:
                return None
            
            # Create embeddings and metadata
            embeddings = []
            metadatas = []
            documents = []
            ids = []
            
            for i, element in enumerate(elements):
                doc_id = f"{file_path.stem}_{i}"
                embeddings.append(self._create_embedding(element['content']))
                metadatas.append({
                    'path': str(file_path),
                    'type': element['type'],
                    'name': element.get('name', ''),
                    'class': element.get('class', '')
                })
                documents.append(element['content'])
                ids.append(doc_id)
            
            return embeddings, metadatas, documents, ids
            
        except Exception as e:
            self.logger.error(f"Error processing file {file_path}: {str(e)}")
            return None

    def _extract_elements(self, node, content: str) -> List[Dict[str, Any]]:
        """Extract code elements from the AST."""
        elements = []
        
        if node.type == 'class_declaration':
            class_name = self._get_node_text(node.child_by_field_name('name'), content)
            elements.append({
                'type': 'class',
                'name': class_name,
                'content': self._get_node_text(node, content)
            })
            
            # Extract methods
            for child in node.children:
                if child.type == 'method_declaration':
                    method_name = self._get_node_text(child.child_by_field_name('name'), content)
                    elements.append({
                        'type': 'method',
                        'name': method_name,
                        'class': class_name,
                        'content': self._get_node_text(child, content)
                    })
        
        return elements

    def _get_node_text(self, node, content: str) -> str:
        """Get the text content of a node."""
        return content[node.start_byte:node.end_byte]

    def _create_embedding(self, text: str) -> List[float]:
        """Create an embedding for the given text using sentence-transformers."""
        # Encode the text and convert to list
        embedding = self.model.encode(text)
        return embedding.tolist()

    def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search the codebase for relevant code."""
        # Create query embedding
        query_embedding = self._create_embedding(query)
        
        # Search the collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i]
            })
        
        return formatted_results

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
        print(f"Content: {json.dumps(result['content'], indent=2)}")

if __name__ == "__main__":
    main() 