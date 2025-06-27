import asyncio
import os
import json
import logging
import re
from pathlib import Path
from typing import Dict, Any, List, Set
from dotenv import load_dotenv
from logger_config import setup_logging
from ai_providers import create_ai_provider
from rate_limiter import RateLimiter, RateLimitConfig
from chromadb_connector import EnhancedChromaDBConnector

logger = logging.getLogger('java_analysis.step2_test')

class RequirementsProcessor:
    def __init__(self):
        load_dotenv()
        self.processed_files: Set[str] = set()
        self.output_dir = os.getenv('OUTPUT_DIR', './output')
        self.md_dir = Path(self.output_dir) / "requirements"
        self.md_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize enhanced ChromaDB connector
        self.chromadb_connector = EnhancedChromaDBConnector()
        logger.info("Initialized enhanced ChromaDB connector with intelligent code chunking")
        
        # Enhanced rate limiting settings for test mode
        rate_config = RateLimitConfig(
            requests_per_minute=10,  # Very conservative for test mode
            requests_per_hour=500,   # Reduced for test mode
            delay_between_requests=8.0,  # Longer delay for test mode
            exponential_backoff_base=2.0,
            max_retries=5
        )
        self.rate_limiter = RateLimiter(rate_config)
        
        # Test mode settings
        self.max_files_to_process = 5  # Very limited for test mode
        
        # Initialize AI provider using the same pattern as main.py and step2.py
        self.ai_provider = create_ai_provider()
        logger.info(f"Using {self.ai_provider.get_provider_name()} provider with model: {self.ai_provider.get_model_name()}")

    def load_metadata_from_chromadb(self) -> List[Dict[str, Any]]:
        """Load metadata from ChromaDB with enhanced chunking information"""
        try:
            # Get chunk statistics to understand what's available
            stats = self.chromadb_connector.get_chunk_statistics()
            logger.info(f"ChromaDB statistics: {stats}")
            
            # Query for all chunks to get the metadata
            # We'll use a broad query to get all documents
            results = self.chromadb_connector.query_enhanced_similar(
                query="requirements analysis documentation",
                n_results=1000,  # Get a large number of results
                filters=None  # No filters to get all chunks
            )
            
            if not results or not results.get('documents') or not results['documents'][0]:
                logger.warning("No documents found in ChromaDB")
                return []
            
            # Convert ChromaDB results to metadata format
            metadata = []
            documents = results['documents'][0]
            metadatas = results['metadatas'][0]
            ids = results['ids'][0]
            
            # Group by file_path to create file-level metadata
            file_groups = {}
            for i, doc_id in enumerate(ids):
                if i < len(metadatas):
                    metadata_item = metadatas[i]
                    file_path = metadata_item.get('file_path', 'unknown')
                    
                    if file_path not in file_groups:
                        file_groups[file_path] = {
                            'file_path': file_path,
                            'file_type': self._get_file_type(file_path),
                            'content': '',
                            'chunks': [],
                            'ai_analysis': {},
                            'chromadb_status': 'loaded'
                        }
                    
                    # Add chunk information
                    chunk_info = {
                        'chunk_id': doc_id,
                        'content': documents[i] if i < len(documents) else '',
                        'language': metadata_item.get('language', 'unknown'),
                        'chunk_type': metadata_item.get('chunk_type', 'unknown'),
                        'start_line': metadata_item.get('start_line', '1'),
                        'end_line': metadata_item.get('end_line', '1'),
                        'function_name': metadata_item.get('function_name', ''),
                        'class_name': metadata_item.get('class_name', ''),
                        'complexity_score': metadata_item.get('complexity_score', '1.0')
                    }
                    file_groups[file_path]['chunks'].append(chunk_info)
                    
                    # Combine content from all chunks
                    if chunk_info['content']:
                        file_groups[file_path]['content'] += chunk_info['content'] + '\n\n'
                    
                    # Parse AI analysis if available
                    ai_analysis_str = metadata_item.get('ai_analysis', '')
                    if ai_analysis_str:
                        try:
                            ai_analysis = json.loads(ai_analysis_str)
                            if ai_analysis:
                                file_groups[file_path]['ai_analysis'] = ai_analysis
                        except json.JSONDecodeError:
                            logger.warning(f"Could not parse AI analysis for {file_path}")
            
            # Convert to list
            metadata = list(file_groups.values())
            logger.info(f"Loaded {len(metadata)} files from ChromaDB with enhanced metadata")
            return metadata
            
        except Exception as e:
            logger.error(f"Error loading metadata from ChromaDB: {e}")
            # Fallback to JSON file if ChromaDB fails
            return self._load_metadata_fallback()

    def _load_metadata_fallback(self) -> List[Dict[str, Any]]:
        """Fallback method to load metadata from JSON file"""
        metadata_file = os.path.join(self.output_dir, 'metadata.json')
        if not os.path.exists(metadata_file):
            raise FileNotFoundError(f"Metadata file not found: {metadata_file}")
            
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        logger.info(f"Loaded metadata from JSON file with {len(metadata)} entries")
        return metadata

    def _get_file_type(self, file_path: str) -> str:
        """Determine file type from extension"""
        ext = Path(file_path).suffix.lower()
        type_mapping = {
            '.java': 'Java source file',
            '.jsp': 'JSP file',
            '.xml': 'XML file',
            '.properties': 'Properties file',
            '.sql': 'SQL file',
            '.html': 'HTML file',
            '.js': 'JavaScript file',
            '.css': 'CSS file',
            '.json': 'JSON file',
            '.yaml': 'YAML file',
            '.yml': 'YAML file'
        }
        return type_mapping.get(ext, 'Unknown file type')

    def get_important_files(self, metadata: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get only the most important files to reduce API calls"""
        important_files = []
        
        # Priority order for file types
        priority_patterns = [
            r'\.jsp$',  # JSP files first
            r'index\.',  # Index files
            r'home\.',   # Home files
            r'\.java$',  # Java files
            r'pom\.xml$',  # Maven config
            r'web\.xml$',  # Web config
        ]
        
        for pattern in priority_patterns:
            for item in metadata:
                file_path = item.get('file_path', '')
                if (re.search(pattern, file_path, re.IGNORECASE) and 
                    item not in important_files and 
                    len(important_files) < self.max_files_to_process):
                    important_files.append(item)
        
        logger.info(f"Selected {len(important_files)} important files for processing")
        return important_files

    async def analyze_single_file(self, file_metadata: Dict[str, Any]) -> None:
        """Analyze a single file with enhanced rate limiting"""
        file_path = file_metadata.get('file_path', '')
        if file_path in self.processed_files:
            return

        logger.info(f"Analyzing file: {file_path}")
        
        # Wait for rate limiter before making API call
        await self.rate_limiter.wait_if_needed()
        
        # Create prompt for AI analysis with enhanced metadata
        content = file_metadata.get('content', '')
        if len(content) > 1500:  # Reduced from 2000
            content = content[:1500] + "... [truncated]"
        
        # Include chunk information if available
        chunks_info = ""
        if 'chunks' in file_metadata and file_metadata['chunks']:
            chunks_info = f"\nChunks: {len(file_metadata['chunks'])} chunks"
            for chunk in file_metadata['chunks'][:3]:  # Show first 3 chunks
                chunks_info += f"\n  - {chunk.get('chunk_type', 'unknown')}: {chunk.get('function_name', '') or chunk.get('class_name', '')}"
            
        prompt = f"""Analyze this file and provide requirements documentation:

File: {file_path}
Type: {file_metadata.get('file_type', 'Unknown')}{chunks_info}
Content: {content}

Provide a concise analysis covering:
1. Purpose and functionality
2. User interactions (if applicable)
3. Data handling
4. Business rules
5. Dependencies and relationships

Keep the analysis focused and practical."""
        
        for attempt in range(self.rate_limiter.config.max_retries):
            try:
                # Wait for rate limiter (includes exponential backoff for retries)
                if attempt > 0:
                    await self.rate_limiter.wait_if_needed()
                
                analysis = await self.ai_provider.create_chat_completion(
                    messages=[
                        {"role": "system", "content": "You are a requirements analysis expert. Provide concise but comprehensive analysis."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    max_tokens=1000  # Reduced from 1500
                )
                
                # Record successful request
                self.rate_limiter.record_request()
                
                # Create markdown file
                md_filename = f"{Path(file_path).stem}.md"
                md_path = self.md_dir / md_filename
                
                with open(md_path, 'w') as f:
                    f.write(f"# Requirements Analysis: {file_path}\n\n")
                    f.write(analysis)
                
                self.processed_files.add(file_path)
                logger.info(f"Generated requirements document: {md_path}")
                
                # Log rate limiting stats
                stats = self.rate_limiter.get_stats()
                logger.info(f"Rate limit stats: {stats['requests_last_minute']}/min, {stats['requests_last_hour']}/hour")
                
                break
                
            except Exception as e:
                logger.error(f"Error analyzing file {file_path} (attempt {attempt + 1}): {str(e)}")
                self.rate_limiter.record_failure()
                
                if attempt == self.rate_limiter.config.max_retries - 1:
                    logger.error(f"Failed to analyze {file_path} after {self.rate_limiter.config.max_retries} attempts")
                    # Mark as processed to avoid infinite retries
                    self.processed_files.add(file_path)

    async def process_important_files(self) -> None:
        """Process only the most important files"""
        metadata = self.load_metadata_from_chromadb()
        important_files = self.get_important_files(metadata)
        
        for i, file_meta in enumerate(important_files):
            await self.analyze_single_file(file_meta)
            
            # Progress update
            logger.info(f"Progress: {i + 1}/{len(important_files)} files processed")

    def generate_index(self) -> None:
        """Generate index file with links to all requirements documents"""
        index_path = self.md_dir / "step2_index.md"
        
        with open(index_path, 'w') as f:
            f.write("# Requirements Documentation Index\n\n")
            f.write(f"Total files processed: {len(self.processed_files)}\n\n")
            f.write("## Requirements Documents\n\n")
            
            # Sort files for consistent ordering
            for file_path in sorted(self.processed_files):
                md_filename = f"{Path(file_path).stem}.md"
                f.write(f"- [{file_path}](./{md_filename})\n")
        
        logger.info(f"Generated index file: {index_path}")

async def generate_requirements():
    """Main function to generate requirements documentation"""
    logger = setup_logging(level=logging.INFO)
    logger.info("Starting requirements generation process (TEST MODE)")
    
    try:
        processor = RequirementsProcessor()
        processor.load_metadata_from_chromadb()
        
        # Process only important files
        await processor.process_important_files()
        
        # Generate index
        processor.generate_index()
        
        logger.info("Requirements generation completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during requirements generation: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(generate_requirements()) 