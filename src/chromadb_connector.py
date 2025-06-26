import chromadb
from chromadb.config import Settings
import yaml
import os
from pathlib import Path
from dotenv import load_dotenv
import logging
from typing import List, Dict, Any, Optional
import json
from code_chunker import IntelligentCodeChunker, CodeChunk

logger = logging.getLogger('java_analysis.chromadb')

class EnhancedChromaDBConnector:
    def __init__(self, config_path: str = "config/app.yaml"):
        # Load environment variables
        load_dotenv()
        logger.debug("Environment variables loaded")
        
        # Initialize code chunker
        self.chunker = IntelligentCodeChunker()
        
        # Ensure config directory exists
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        logger.debug(f"Ensured config directory exists: {os.path.dirname(config_path)}")
        
        # Create default config if it doesn't exist
        if not os.path.exists(config_path):
            logger.info(f"Config file not found at {config_path}, creating default config")
            default_config = {
                'chromadb': {
                    'host': 'localhost',
                    'port': 8000,
                    'collection_name': 'enhanced_java_analysis'
                }
            }
            
            with open(config_path, 'w') as f:
                yaml.dump(default_config, f)
            logger.info(f"Created default config at {config_path}")
            
        # Load config
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        logger.debug("Loaded ChromaDB configuration")
        
        # Initialize ChromaDB client
        chromadb_dir = os.getenv('CHROMADB_DIR', './data/chromadb')
        self.client = chromadb.PersistentClient(path=chromadb_dir, settings=Settings(anonymized_telemetry=False))
        logger.info(f"Initialized ChromaDB client with directory: {chromadb_dir}")
        
        # Get or create collection
        collection_name = self.config['chromadb']['collection_name']
        self.collection = self.client.get_or_create_collection(name=collection_name)
        logger.info(f"Using collection: {collection_name}")

    def store_enhanced_metadata(self, file_path: str, content: str, ai_analysis: Dict[str, Any] = None) -> None:
        """Store enhanced metadata using intelligent code chunking"""
        logger.info(f"Storing enhanced metadata for: {file_path}")
        
        try:
            # Use intelligent chunking to create code chunks
            chunks = self.chunker.chunk_code(content, file_path)
            logger.info(f"Created {len(chunks)} chunks for {file_path}")
            
            # Prepare data for ChromaDB
            documents = []
            metadatas = []
            ids = []
            
            for chunk in chunks:
                # Create enhanced document content
                doc_content = [
                    f"File: {chunk.file_path}",
                    f"Type: {chunk.chunk_type}",
                    f"Language: {chunk.language}",
                ]
                
                # Add specific metadata based on chunk type
                if chunk.function_name:
                    doc_content.append(f"Function: {chunk.function_name}")
                if chunk.class_name:
                    doc_content.append(f"Class: {chunk.class_name}")
                if chunk.parent_context:
                    doc_content.append(f"Parent: {chunk.parent_context}")
                
                doc_content.extend([
                    "Content:",
                    chunk.content,
                ])
                
                # Add AI analysis if available
                if ai_analysis:
                    doc_content.extend([
                        "Analysis:",
                        json.dumps(ai_analysis, indent=2) if isinstance(ai_analysis, dict) else str(ai_analysis)
                    ])
                
                documents.append("\n".join(doc_content))
                
                # Prepare enhanced metadata
                meta = {
                    'file_path': chunk.file_path,
                    'chunk_type': chunk.chunk_type,
                    'language': chunk.language,
                    'start_line': chunk.start_line,
                    'end_line': chunk.end_line,
                    'complexity_score': chunk.complexity_score,
                    'chunk_id': chunk.chunk_id,
                }
                
                # Add optional fields
                if chunk.function_name:
                    meta['function_name'] = chunk.function_name
                if chunk.class_name:
                    meta['class_name'] = chunk.class_name
                if chunk.parent_context:
                    meta['parent_context'] = chunk.parent_context
                if chunk.imports:
                    meta['imports'] = ', '.join(chunk.imports) if chunk.imports else ''
                if chunk.dependencies:
                    meta['dependencies'] = ', '.join(chunk.dependencies) if chunk.dependencies else ''
                if chunk.metadata:
                    # Ensure all metadata values are ChromaDB-compatible
                    for key, value in chunk.metadata.items():
                        if isinstance(value, list):
                            meta[key] = ', '.join(str(v) for v in value) if value else ''
                        elif isinstance(value, (str, int, float, bool)):
                            meta[key] = value
                        else:
                            meta[key] = str(value) if value is not None else ''
                
                # Add file-level metadata
                file_stats = os.stat(file_path)
                meta.update({
                    'file_size_bytes': file_stats.st_size,
                    'file_last_modified': file_stats.st_mtime,
                    'file_extension': Path(file_path).suffix,
                })
                
                metadatas.append(meta)
                ids.append(chunk.chunk_id)
            
            # Store in batches of 100 to avoid memory issues
            batch_size = 100
            for i in range(0, len(documents), batch_size):
                batch_end = min(i + batch_size, len(documents))
                self.collection.add(
                    documents=documents[i:batch_end],
                    metadatas=metadatas[i:batch_end],
                    ids=ids[i:batch_end]
                )
                logger.debug(f"Stored batch {i//batch_size + 1} ({batch_end - i} chunks)")
            
            logger.info(f"Successfully stored {len(documents)} enhanced chunks in ChromaDB")
            
        except Exception as e:
            logger.error(f"Error storing enhanced metadata in ChromaDB: {str(e)}")
            raise

    def query_enhanced_similar(self, query: str, n_results: int = 5, 
                             filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Query for similar documents with enhanced filtering"""
        logger.info(f"Querying for enhanced documents similar to: {query}")
        
        try:
            # Build where clause for filtering
            where_clause = {}
            if filters:
                for key, value in filters.items():
                    if isinstance(value, list):
                        where_clause[key] = {"$in": value}
                    else:
                        where_clause[key] = value
            
            # Perform query
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where_clause if where_clause else None,
                include=['documents', 'metadatas', 'distances']
            )
            
            logger.debug(f"Found {len(results['documents'][0])} matching chunks")
            return results
            
        except Exception as e:
            logger.error(f"Error querying enhanced ChromaDB: {str(e)}")
            raise

    def query_by_chunk_type(self, chunk_type: str, n_results: int = 10) -> Dict[str, Any]:
        """Query documents by chunk type (function, class, method, etc.)"""
        return self.query_enhanced_similar("", n_results, filters={'chunk_type': chunk_type})

    def query_by_language(self, language: str, n_results: int = 10) -> Dict[str, Any]:
        """Query documents by programming language"""
        return self.query_enhanced_similar("", n_results, filters={'language': language})

    def query_by_function_name(self, function_name: str, n_results: int = 5) -> Dict[str, Any]:
        """Query documents by function name"""
        return self.query_enhanced_similar(f"function {function_name}", n_results, 
                                         filters={'function_name': function_name})

    def query_by_class_name(self, class_name: str, n_results: int = 5) -> Dict[str, Any]:
        """Query documents by class name"""
        return self.query_enhanced_similar(f"class {class_name}", n_results, 
                                         filters={'class_name': class_name})

    def get_chunk_statistics(self) -> Dict[str, Any]:
        """Get statistics about stored chunks"""
        try:
            # Get all documents to analyze
            results = self.collection.get(include=['metadatas'])
            
            if not results['metadatas']:
                return {'total_chunks': 0}
            
            stats = {
                'total_chunks': len(results['metadatas']),
                'languages': {},
                'chunk_types': {},
                'files': set(),
                'complexity_scores': []
            }
            
            for metadata in results['metadatas']:
                # Count languages
                lang = metadata.get('language', 'unknown')
                stats['languages'][lang] = stats['languages'].get(lang, 0) + 1
                
                # Count chunk types
                chunk_type = metadata.get('chunk_type', 'unknown')
                stats['chunk_types'][chunk_type] = stats['chunk_types'].get(chunk_type, 0) + 1
                
                # Count unique files
                stats['files'].add(metadata.get('file_path', ''))
                
                # Collect complexity scores
                if 'complexity_score' in metadata:
                    stats['complexity_scores'].append(metadata['complexity_score'])
            
            # Convert set to list for JSON serialization
            stats['files'] = list(stats['files'])
            stats['unique_files'] = len(stats['files'])
            
            # Calculate complexity statistics
            if stats['complexity_scores']:
                stats['avg_complexity'] = sum(stats['complexity_scores']) / len(stats['complexity_scores'])
                stats['max_complexity'] = max(stats['complexity_scores'])
                stats['min_complexity'] = min(stats['complexity_scores'])
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting chunk statistics: {str(e)}")
            return {'error': str(e)}

# Backward compatibility - keep the old function names
def store_metadata(metadata_list: List[Dict[str, Any]]) -> None:
    """Legacy function for backward compatibility"""
    connector = EnhancedChromaDBConnector()
    
    for metadata in metadata_list:
        file_path = metadata['file_path']
        content = metadata.get('content', '')
        ai_analysis = metadata.get('ai_analysis')
        
        # Read file content if not provided
        if not content and os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        
        connector.store_enhanced_metadata(file_path, content, ai_analysis)

def _format_enhanced_results(results: Dict[str, Any]) -> str:
    """Format enhanced query results for display"""
    if not results or not results.get('documents') or not results['documents'][0]:
        return "No relevant documents found in ChromaDB."
    
    context_parts = []
    for i, doc in enumerate(results['documents'][0]):
        metadata = results['metadatas'][0][i] if results['metadatas'] and results['metadatas'][0] else {}
        distance = results['distances'][0][i] if results['distances'] and results['distances'][0] else 0
        
        # Enhanced context formatting
        context_parts.append(f"=== Chunk {i+1} (similarity: {1-distance:.3f}) ===")
        context_parts.append(f"File: {metadata.get('file_path', 'Unknown')}")
        context_parts.append(f"Type: {metadata.get('chunk_type', 'Unknown')}")
        context_parts.append(f"Language: {metadata.get('language', 'Unknown')}")
        
        if metadata.get('function_name'):
            context_parts.append(f"Function: {metadata['function_name']}")
        if metadata.get('class_name'):
            context_parts.append(f"Class: {metadata['class_name']}")
        if metadata.get('parent_context'):
            context_parts.append(f"Parent: {metadata['parent_context']}")
        if metadata.get('start_line') and metadata.get('end_line'):
            context_parts.append(f"Lines: {metadata['start_line']}-{metadata['end_line']}")
        
        # Add complexity score if available
        if metadata.get('complexity_score'):
            context_parts.append(f"Complexity: {metadata['complexity_score']:.2f}")
        
        context_parts.append("Content:")
        context_parts.append(doc[:800] + "..." if len(doc) > 800 else doc)
        context_parts.append("---")
    
    return "\n".join(context_parts)

def query_chromadb(question: str, n_results: int = 5) -> str:
    """Enhanced query function that returns detailed chunk information"""
    try:
        # Create enhanced ChromaDB connector instance
        connector = EnhancedChromaDBConnector()
        
        # Query for similar documents
        results = connector.query_enhanced_similar(question, n_results)
        
        # Format the results with enhanced information
        return _format_enhanced_results(results)
            
    except Exception as e:
        logger.error(f"Error in enhanced query_chromadb: {str(e)}")
        return f"Error querying ChromaDB: {str(e)}"

# Legacy class for backward compatibility
class ChromaDBConnector(EnhancedChromaDBConnector):
    """Legacy class name for backward compatibility"""
    pass 