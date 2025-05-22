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

class CodebaseProcessor:
    def __init__(self, codebase_path: str, db_path: str = "chroma_db"):
        """Initialize the codebase processor."""
        self.codebase_path = Path(codebase_path)
        self.parser = JavaParser()
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(
            name="java_code",
            metadata={"description": "Java codebase embeddings"}
        )
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

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

    def process_codebase(self, max_workers: int = 4):
        """Process the entire codebase and store in vector database."""
        java_files = self.find_java_files()
        self.logger.info(f"Found {len(java_files)} Java files")

        # Process files in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(tqdm(
                executor.map(self.process_file, java_files),
                total=len(java_files),
                desc="Processing files"
            ))

        # Filter out None results and create embeddings
        valid_results = [r for r in results if r is not None]
        all_embeddings = []
        
        for result in tqdm(valid_results, desc="Creating embeddings"):
            embeddings = self.create_embeddings(result)
            all_embeddings.extend(embeddings)

        # Store in vector database
        self.logger.info(f"Storing {len(all_embeddings)} embeddings in vector database")
        
        # Prepare data for ChromaDB
        ids = [f"{i}" for i in range(len(all_embeddings))]
        documents = [e['content'] for e in all_embeddings]
        metadatas = [{
            'type': e['type'],
            'path': e['path'],
            'name': e.get('name', ''),
            'class': e.get('class', '')
        } for e in all_embeddings]

        # Add to collection
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

    def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search the codebase using natural language."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results['documents'][0])):
            result = {
                'content': json.loads(results['documents'][0][i]),
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i] if 'distances' in results else None
            }
            formatted_results.append(result)
        
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