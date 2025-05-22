import os
from pathlib import Path
from typing import List, Dict, Any
from tree_sitter import Language, Parser
import chromadb
from chromadb.config import Settings
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JavaCodeProcessor:
    def __init__(self, java_so_path: str = "build/my-languages.so", max_retries: int = 3):
        """Initialize the Java code processor with tree-sitter."""
        try:
            # Initialize tree-sitter
            if not os.path.exists(java_so_path):
                raise FileNotFoundError(f"Tree-sitter library not found at {java_so_path}")
            
            self.language = Language(java_so_path, 'java')
            self.parser = Parser()
            self.parser.set_language(self.language)
            
            # Initialize ChromaDB client with v2 API settings
            self.client = chromadb.HttpClient(
                host="chromadb.dev.motorenflug.at",
                port=443,
                ssl=True,
                settings=Settings(
                    allow_reset=True,
                    anonymized_telemetry=False,
                    is_persistent=True,
                    persist_directory="chroma_db",
                    chroma_api_impl="rest",
                    chroma_server_host="chromadb.dev.motorenflug.at",
                    chroma_server_http_port=443,
                    chroma_server_ssl_enabled=True
                )
            )
            
            # Retry logic for collection creation
            retry_count = 0
            while retry_count < max_retries:
                try:
                    # Create or get collection with proper metadata
                    self.collection = self.client.get_or_create_collection(
                        name="java_code",
                        metadata={
                            "description": "Java code snippets with semantic search",
                            "type": "code_search"
                        }
                    )
                    logger.info("Successfully initialized JavaCodeProcessor")
                    break
                except Exception as e:
                    retry_count += 1
                    if retry_count == max_retries:
                        raise
                    logger.warning(f"Failed to connect to ChromaDB, retrying ({retry_count}/{max_retries})...")
                    time.sleep(2 ** retry_count)  # Exponential backoff
            
        except Exception as e:
            logger.error(f"Failed to initialize JavaCodeProcessor: {str(e)}")
            raise

    def parse_java_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Parse a Java file and extract meaningful code segments."""
        try:
            with open(file_path, 'rb') as f:
                source_code = f.read()
            
            tree = self.parser.parse(source_code)
            if not tree:
                logger.warning(f"Failed to parse file: {file_path}")
                return []
                
            code_segments = []
            
            def extract_node(node):
                if node.type in ['class_declaration', 'method_declaration', 'interface_declaration']:
                    start_line = node.start_point[0] + 1
                    end_line = node.end_point[0] + 1
                    code = source_code[node.start_byte:node.end_byte].decode('utf-8')
                    
                    # Extract method/class name
                    name_node = node.child_by_field_name('name')
                    name = name_node.text.decode('utf-8') if name_node else 'Unknown'
                    
                    code_segments.append({
                        'name': name,
                        'type': node.type,
                        'code': code,
                        'start_line': start_line,
                        'end_line': end_line,
                        'file_path': file_path
                    })
                
                for child in node.children:
                    extract_node(child)
            
            extract_node(tree.root_node)
            logger.info(f"Successfully parsed {len(code_segments)} segments from {file_path}")
            return code_segments
            
        except Exception as e:
            logger.error(f"Error parsing file {file_path}: {str(e)}")
            return []

    def process_directory(self, directory_path: str) -> None:
        """Process all Java files in a directory and its subdirectories."""
        try:
            if not os.path.exists(directory_path):
                raise FileNotFoundError(f"Directory not found: {directory_path}")
                
            java_files = list(Path(directory_path).rglob("*.java"))
            if not java_files:
                logger.warning(f"No Java files found in {directory_path}")
                return
                
            total_segments = 0
            for file_path in java_files:
                logger.info(f"Processing {file_path}...")
                segments = self.parse_java_file(str(file_path))
                
                if not segments:
                    continue
                    
                # Prepare data for ChromaDB
                ids = [f"{file_path.name}_{i}" for i in range(len(segments))]
                documents = [seg['code'] for seg in segments]
                metadatas = [{
                    'name': seg['name'],
                    'type': seg['type'],
                    'start_line': seg['start_line'],
                    'end_line': seg['end_line'],
                    'file_path': str(file_path)
                } for seg in segments]
                
                # Add to ChromaDB with retry logic
                retry_count = 0
                while retry_count < 3:
                    try:
                        self.collection.add(
                            ids=ids,
                            documents=documents,
                            metadatas=metadatas
                        )
                        break
                    except Exception as e:
                        retry_count += 1
                        if retry_count == 3:
                            logger.error(f"Failed to add segments to ChromaDB after 3 retries: {str(e)}")
                            raise
                        logger.warning(f"Failed to add segments, retrying ({retry_count}/3)...")
                        time.sleep(2 ** retry_count)
                
                total_segments += len(segments)
                logger.info(f"Added {len(segments)} segments from {file_path.name}")
                
            logger.info(f"Successfully processed {len(java_files)} files with {total_segments} total segments")
            
        except Exception as e:
            logger.error(f"Error processing directory {directory_path}: {str(e)}")
            raise

    def search_code(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search for code segments using semantic similarity."""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            if not results['documents'] or not results['documents'][0]:
                logger.warning(f"No results found for query: {query}")
                return []
                
            return [{
                'code': doc,
                'metadata': meta
            } for doc, meta in zip(results['documents'][0], results['metadatas'][0])]
            
        except Exception as e:
            logger.error(f"Error searching code: {str(e)}")
            raise 