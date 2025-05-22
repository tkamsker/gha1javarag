import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Generator
import logging
import json
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import sqlparse
from tree_sitter import Language, Parser
import chromadb
from chromadb.config import Settings
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
import hashlib
from itertools import islice

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileProcessor:
    def __init__(self, java_so_path: str = "build/my-languages.so", max_retries: int = 3,
                 max_workers: int = 4, batch_size: int = 100, chunk_size: int = 1000,
                 chunk_overlap: int = 100):
        """Initialize the file processor with support for multiple file types."""
        try:
            # Initialize tree-sitter for Java files
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
            
            # Configuration parameters
            self.max_workers = max_workers
            self.batch_size = batch_size
            self.chunk_size = chunk_size
            self.chunk_overlap = chunk_overlap
            self.max_retries = max_retries
            
            # Create collections for different file types
            self.collections = {}
            for file_type in ['java', 'xml', 'json', 'html', 'sql']:
                retry_count = 0
                while retry_count < max_retries:
                    try:
                        self.collections[file_type] = self.client.get_or_create_collection(
                            name=f"{file_type}_code",
                            metadata={
                                "description": f"{file_type.upper()} code snippets with semantic search",
                                "type": "code_search"
                            }
                        )
                        break
                    except Exception as e:
                        retry_count += 1
                        if retry_count == max_retries:
                            raise
                        logger.warning(f"Failed to create collection for {file_type}, retrying ({retry_count}/{max_retries})...")
                        time.sleep(2 ** retry_count)
            
            logger.info("Successfully initialized FileProcessor")
            
        except Exception as e:
            logger.error(f"Failed to initialize FileProcessor: {str(e)}")
            raise

    @lru_cache(maxsize=1000)
    def _get_file_hash(self, file_path: str) -> str:
        """Get the hash of a file for caching purposes."""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return ""

    def _chunk_text(self, text: str, chunk_size: int, overlap: int) -> Generator[str, None, None]:
        """Split text into overlapping chunks."""
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = min(start + chunk_size, text_len)
            # Try to find a good breaking point (newline or space)
            if end < text_len:
                # Look for newline first
                newline_pos = text.rfind('\n', start, end)
                if newline_pos != -1:
                    end = newline_pos + 1
                else:
                    # Look for space
                    space_pos = text.rfind(' ', start, end)
                    if space_pos != -1:
                        end = space_pos + 1
            
            yield text[start:end]
            start = end - overlap

    def _batch_iterator(self, items: List[Any], batch_size: int) -> Generator[List[Any], None, None]:
        """Split items into batches."""
        iterator = iter(items)
        while batch := list(islice(iterator, batch_size)):
            yield batch

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
                    
                    # Split large code segments into chunks
                    if len(code) > self.chunk_size:
                        for i, chunk in enumerate(self._chunk_text(code, self.chunk_size, self.chunk_overlap)):
                            name_node = node.child_by_field_name('name')
                            name = name_node.text.decode('utf-8') if name_node else 'Unknown'
                            
                            code_segments.append({
                                'name': f"{name}_chunk_{i}",
                                'type': node.type,
                                'code': chunk,
                                'start_line': start_line,
                                'end_line': end_line,
                                'file_path': file_path,
                                'chunk_index': i
                            })
                    else:
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
            return code_segments
            
        except Exception as e:
            logger.error(f"Error parsing Java file {file_path}: {str(e)}")
            return []

    def parse_xml_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Parse an XML file and extract meaningful segments."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            root = ET.fromstring(content)
            segments = []
            
            def extract_element(element, path=""):
                current_path = f"{path}/{element.tag}"
                
                # Extract element attributes
                if element.attrib:
                    code = ET.tostring(element, encoding='unicode')
                    if len(code) > self.chunk_size:
                        for i, chunk in enumerate(self._chunk_text(code, self.chunk_size, self.chunk_overlap)):
                            segments.append({
                                'name': f"{element.tag}_chunk_{i}",
                                'type': 'element',
                                'code': chunk,
                                'path': current_path,
                                'file_path': file_path,
                                'chunk_index': i
                            })
                    else:
                        segments.append({
                            'name': element.tag,
                            'type': 'element',
                            'code': code,
                            'path': current_path,
                            'file_path': file_path
                        })
                
                # Process child elements
                for child in element:
                    extract_element(child, current_path)
            
            extract_element(root)
            return segments
            
        except Exception as e:
            logger.error(f"Error parsing XML file {file_path}: {str(e)}")
            return []

    def parse_json_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Parse a JSON file and extract meaningful segments."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
            
            segments = []
            
            def extract_json(obj, path=""):
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        current_path = f"{path}/{key}"
                        if isinstance(value, (dict, list)):
                            extract_json(value, current_path)
                        else:
                            code = json.dumps({key: value}, indent=2)
                            if len(code) > self.chunk_size:
                                for i, chunk in enumerate(self._chunk_text(code, self.chunk_size, self.chunk_overlap)):
                                    segments.append({
                                        'name': f"{key}_chunk_{i}",
                                        'type': 'json_field',
                                        'code': chunk,
                                        'path': current_path,
                                        'file_path': file_path,
                                        'chunk_index': i
                                    })
                            else:
                                segments.append({
                                    'name': key,
                                    'type': 'json_field',
                                    'code': code,
                                    'path': current_path,
                                    'file_path': file_path
                                })
                elif isinstance(obj, list):
                    for i, item in enumerate(obj):
                        current_path = f"{path}[{i}]"
                        if isinstance(item, (dict, list)):
                            extract_json(item, current_path)
                        else:
                            code = json.dumps(item, indent=2)
                            if len(code) > self.chunk_size:
                                for j, chunk in enumerate(self._chunk_text(code, self.chunk_size, self.chunk_overlap)):
                                    segments.append({
                                        'name': f"item_{i}_chunk_{j}",
                                        'type': 'json_array_item',
                                        'code': chunk,
                                        'path': current_path,
                                        'file_path': file_path,
                                        'chunk_index': j
                                    })
                            else:
                                segments.append({
                                    'name': f"item_{i}",
                                    'type': 'json_array_item',
                                    'code': code,
                                    'path': current_path,
                                    'file_path': file_path
                                })
            
            extract_json(content)
            return segments
            
        except Exception as e:
            logger.error(f"Error parsing JSON file {file_path}: {str(e)}")
            return []

    def parse_html_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Parse an HTML file and extract meaningful segments."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            segments = []
            
            def extract_element(element):
                if element.name:
                    # Extract meaningful elements
                    if element.name in ['div', 'section', 'article', 'form', 'table']:
                        code = str(element)
                        if len(code) > self.chunk_size:
                            for i, chunk in enumerate(self._chunk_text(code, self.chunk_size, self.chunk_overlap)):
                                segments.append({
                                    'name': f"{element.get('id', element.name)}_chunk_{i}",
                                    'type': 'html_element',
                                    'code': chunk,
                                    'path': element.get('id', ''),
                                    'file_path': file_path,
                                    'chunk_index': i
                                })
                        else:
                            segments.append({
                                'name': element.get('id', element.name),
                                'type': 'html_element',
                                'code': code,
                                'path': element.get('id', ''),
                                'file_path': file_path
                            })
                    
                    # Process child elements
                    for child in element.children:
                        if hasattr(child, 'name'):
                            extract_element(child)
            
            extract_element(soup)
            return segments
            
        except Exception as e:
            logger.error(f"Error parsing HTML file {file_path}: {str(e)}")
            return []

    def parse_sql_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Parse a SQL file and extract meaningful segments."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split into individual statements
            statements = sqlparse.split(content)
            segments = []
            
            for i, statement in enumerate(statements):
                if statement.strip():
                    # Parse the statement to get its type
                    parsed = sqlparse.parse(statement)[0]
                    stmt_type = parsed.get_type().lower()
                    
                    code = statement.strip()
                    if len(code) > self.chunk_size:
                        for j, chunk in enumerate(self._chunk_text(code, self.chunk_size, self.chunk_overlap)):
                            segments.append({
                                'name': f"{stmt_type}_{i}_chunk_{j}",
                                'type': 'sql_statement',
                                'code': chunk,
                                'statement_type': stmt_type,
                                'file_path': file_path,
                                'chunk_index': j
                            })
                    else:
                        segments.append({
                            'name': f"{stmt_type}_{i}",
                            'type': 'sql_statement',
                            'code': code,
                            'statement_type': stmt_type,
                            'file_path': file_path
                        })
            
            return segments
            
        except Exception as e:
            logger.error(f"Error parsing SQL file {file_path}: {str(e)}")
            return []

    def process_file(self, file_path: str) -> None:
        """Process a single file based on its type."""
        try:
            # Check if file has changed using hash
            current_hash = self._get_file_hash(file_path)
            if not current_hash:
                logger.warning(f"Could not compute hash for {file_path}")
                return

            file_extension = Path(file_path).suffix.lower()
            segments = []
            
            if file_extension == '.java':
                segments = self.parse_java_file(file_path)
            elif file_extension == '.xml':
                segments = self.parse_xml_file(file_path)
            elif file_extension == '.json':
                segments = self.parse_json_file(file_path)
            elif file_extension in ['.html', '.htm']:
                segments = self.parse_html_file(file_path)
            elif file_extension == '.sql':
                segments = self.parse_sql_file(file_path)
            else:
                logger.warning(f"Unsupported file type: {file_extension}")
                return
            
            if not segments:
                return
            
            # Determine collection based on file type
            collection_type = file_extension.lstrip('.').lower()
            if collection_type in ['htm', 'html']:
                collection_type = 'html'
            
            collection = self.collections.get(collection_type)
            if not collection:
                logger.warning(f"No collection found for file type: {collection_type}")
                return
            
            # Process segments in batches
            for batch in self._batch_iterator(segments, self.batch_size):
                # Prepare data for ChromaDB
                ids = [f"{Path(file_path).name}_{i}" for i in range(len(batch))]
                documents = [seg['code'] for seg in batch]
                metadatas = [{
                    'name': seg['name'],
                    'type': seg['type'],
                    'file_path': str(file_path),
                    'file_hash': current_hash,
                    **{k: v for k, v in seg.items() if k not in ['code', 'name', 'type']}
                } for seg in batch]
                
                # Add to ChromaDB with retry logic
                retry_count = 0
                while retry_count < self.max_retries:
                    try:
                        collection.add(
                            ids=ids,
                            documents=documents,
                            metadatas=metadatas
                        )
                        break
                    except Exception as e:
                        retry_count += 1
                        if retry_count == self.max_retries:
                            logger.error(f"Failed to add segments to ChromaDB after {self.max_retries} retries: {str(e)}")
                            raise
                        logger.warning(f"Failed to add segments, retrying ({retry_count}/{self.max_retries})...")
                        time.sleep(2 ** retry_count)
            
            logger.info(f"Successfully processed {file_path} with {len(segments)} segments")
            
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            raise

    def process_directory(self, directory_path: str) -> None:
        """Process all supported files in a directory and its subdirectories."""
        try:
            if not os.path.exists(directory_path):
                raise FileNotFoundError(f"Directory not found: {directory_path}")
            
            # Define supported file extensions
            supported_extensions = {'.java', '.xml', '.json', '.html', '.htm', '.sql'}
            
            # Find all supported files
            files = []
            for ext in supported_extensions:
                files.extend(Path(directory_path).rglob(f"*{ext}"))
            
            if not files:
                logger.warning(f"No supported files found in {directory_path}")
                return
            
            total_files = len(files)
            processed_files = 0
            
            # Process files in parallel
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_file = {executor.submit(self.process_file, str(file_path)): file_path for file_path in files}
                
                for future in as_completed(future_to_file):
                    file_path = future_to_file[future]
                    try:
                        future.result()
                        processed_files += 1
                        logger.info(f"Processed {file_path} ({processed_files}/{total_files})")
                    except Exception as e:
                        logger.error(f"Failed to process {file_path}: {str(e)}")
                        continue
            
            logger.info(f"Successfully processed {processed_files}/{total_files} files")
            
        except Exception as e:
            logger.error(f"Error processing directory {directory_path}: {str(e)}")
            raise

    def search_code(self, query: str, file_types: Optional[List[str]] = None, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search for code segments across all or specified file types."""
        try:
            results = []
            
            # Determine which collections to search
            collections_to_search = []
            if file_types:
                for file_type in file_types:
                    if file_type in self.collections:
                        collections_to_search.append(self.collections[file_type])
            else:
                collections_to_search = list(self.collections.values())
            
            # Search each collection
            for collection in collections_to_search:
                try:
                    collection_results = collection.query(
                        query_texts=[query],
                        n_results=n_results
                    )
                    
                    if collection_results['documents'] and collection_results['documents'][0]:
                        for doc, meta in zip(collection_results['documents'][0], collection_results['metadatas'][0]):
                            results.append({
                                'code': doc,
                                'metadata': meta
                            })
                except Exception as e:
                    logger.error(f"Error searching collection {collection.name}: {str(e)}")
                    continue
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching code: {str(e)}")
            raise 