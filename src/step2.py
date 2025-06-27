import asyncio
import os
import json
import logging
import re
import time
from pathlib import Path
from typing import Dict, Any, List, Set
from dotenv import load_dotenv
from logger_config import setup_logging
from ai_providers import create_ai_provider
from rate_limiter import RateLimiter, RateLimitConfig
from chromadb_connector import EnhancedChromaDBConnector

logger = logging.getLogger('java_analysis.step2')

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
        
        # Enhanced rate limiting settings
        rate_config = RateLimitConfig(
            requests_per_minute=15,  # Reduced from 20
            requests_per_hour=800,   # Reduced from 1000
            delay_between_requests=5.0,  # Increased from 2.0
            exponential_backoff_base=2.0,
            max_retries=5
        )
        self.rate_limiter = RateLimiter(rate_config)
        
        # Batch processing settings
        self.max_files_per_batch = 3  # Reduced from 5
        self.max_files_to_process = 500000  # Limit total files to process
        
        # Initialize AI provider using the same pattern as main.py
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

    def prioritize_files(self, metadata: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritize files based on importance and type"""
        priority_order = [
            # High priority - core application files
            lambda f: f.get('file_path', '').endswith('.jsp'),
            lambda f: f.get('file_path', '').endswith('.java'),
            lambda f: 'index' in f.get('file_path', '').lower(),
            lambda f: 'home' in f.get('file_path', '').lower(),
            lambda f: 'main' in f.get('file_path', '').lower(),
            # Medium priority - configuration files
            lambda f: f.get('file_path', '').endswith('.xml'),
            lambda f: f.get('file_path', '').endswith('.properties'),
            # Lower priority - other files
            lambda f: True  # Catch all remaining files
        ]
        
        prioritized = []
        for priority_func in priority_order:
            for item in metadata:
                if priority_func(item) and item not in prioritized:
                    prioritized.append(item)
                    # Limit total files to process
                    if len(prioritized) >= self.max_files_to_process:
                        break
            if len(prioritized) >= self.max_files_to_process:
                break
        
        return prioritized

    def should_skip_file(self, file_path: str) -> bool:
        """Determine if a file should be skipped to reduce API calls"""
        skip_patterns = [
            r'\.git/',
            r'node_modules/',
            r'\.DS_Store',
            r'\.log$',
            r'\.tmp$',
            r'\.bak$',
            r'\.swp$',
            r'\.swo$',
            r'\.class$',  # Compiled Java files
            r'\.jar$',    # JAR files
            r'\.war$',    # WAR files
            r'\.ear$',    # EAR files
        ]
        
        for pattern in skip_patterns:
            if re.search(pattern, file_path, re.IGNORECASE):
                return True
        return False

    async def analyze_files_batch(self, files_batch: List[Dict[str, Any]]) -> None:
        """Analyze multiple files in a single API call with enhanced rate limiting"""
        if not files_batch:
            return
            
        logger.info(f"Analyzing batch of {len(files_batch)} files")
        
        # Wait for rate limiter before making API call
        await self.rate_limiter.wait_if_needed()
        
        # Create a combined prompt for all files with enhanced metadata
        files_content = []
        for file_meta in files_batch:
            file_path = file_meta.get('file_path', '')
            file_type = file_meta.get('file_type', 'Unknown')
            content = file_meta.get('content', '')[:800]  # Reduced content length
            
            # Include chunk information if available
            chunks_info = ""
            if 'chunks' in file_meta and file_meta['chunks']:
                chunks_info = f"\nChunks: {len(file_meta['chunks'])} chunks"
                for chunk in file_meta['chunks'][:3]:  # Show first 3 chunks
                    chunks_info += f"\n  - {chunk.get('chunk_type', 'unknown')}: {chunk.get('function_name', '') or chunk.get('class_name', '')}"
            
            files_content.append(f"""
File: {file_path}
Type: {file_type}{chunks_info}
Content Preview: {content[:400]}...
---""")
        
        combined_content = "\n".join(files_content)
        
        prompt = f"""Analyze the following files and provide requirements documentation for each:

{combined_content}

For each file, provide:
1. Purpose and functionality
2. User interactions (if applicable)
3. Data handling
4. Business rules
5. Dependencies and relationships

Format your response as:
## File: [filename]
[analysis for this file]

## File: [filename]
[analysis for this file]
..."""
        
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
                    max_tokens=2000  # Reduced from 3000
                )
                
                # Record successful request
                self.rate_limiter.record_request()
                
                # Parse the response and create individual files
                await self.parse_batch_response(analysis, files_batch)
                
                # Mark files as processed
                for file_meta in files_batch:
                    self.processed_files.add(file_meta.get('file_path', ''))
                
                logger.info(f"Successfully analyzed batch of {len(files_batch)} files")
                
                # Log rate limiting stats
                stats = self.rate_limiter.get_stats()
                logger.info(f"Rate limit stats: {stats['requests_last_minute']}/min, {stats['requests_last_hour']}/hour")
                
                break
                
            except Exception as e:
                logger.error(f"Error analyzing batch (attempt {attempt + 1}): {str(e)}")
                self.rate_limiter.record_failure()
                
                if attempt == self.rate_limiter.config.max_retries - 1:
                    logger.error(f"Failed to analyze batch after {self.rate_limiter.config.max_retries} attempts")
                    # Mark files as processed to avoid infinite retries
                    for file_meta in files_batch:
                        self.processed_files.add(file_meta.get('file_path', ''))

    async def parse_batch_response(self, analysis: str, files_batch: List[Dict[str, Any]]) -> None:
        """Parse the batch response and create individual markdown files"""
        # Split by file sections
        sections = re.split(r'## File:\s*', analysis)
        
        for i, file_meta in enumerate(files_batch):
            file_path = file_meta.get('file_path', '')
            md_filename = f"{Path(file_path).stem}.md"
            md_path = self.md_dir / md_filename
            
            # Get the corresponding section content
            if i + 1 < len(sections):
                section_content = sections[i + 1].strip()
            else:
                section_content = "Analysis not available for this file."
            
            with open(md_path, 'w') as f:
                f.write(f"# Requirements Analysis: {file_path}\n\n")
                f.write(section_content)
            
            logger.debug(f"Generated requirements document: {md_path}")

    async def process_files_with_batching(self) -> None:
        """Process files in batches to reduce API calls"""
        metadata = self.load_metadata_from_chromadb()
        
        prioritized_files = self.prioritize_files(metadata)
        
        # Filter out files to skip
        files_to_process = [
            f for f in prioritized_files 
            if not self.should_skip_file(f.get('file_path', ''))
        ]
        
        logger.info(f"Processing {len(files_to_process)} files in batches of {self.max_files_per_batch}")
        
        # Process files in batches
        for i in range(0, len(files_to_process), self.max_files_per_batch):
            batch = files_to_process[i:i + self.max_files_per_batch]
            await self.analyze_files_batch(batch)
            
            # Progress update
            processed_count = len(self.processed_files)
            total_count = len(files_to_process)
            logger.info(f"Progress: {processed_count}/{total_count} files processed")

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
    logger = setup_logging(level=logging.INFO)  # Reduced logging level
    logger.info("Starting requirements generation process")
    
    try:
        processor = RequirementsProcessor()
        
        # Process files with batching
        await processor.process_files_with_batching()
        
        # Generate index
        processor.generate_index()
        
        logger.info("Requirements generation completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during requirements generation: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(generate_requirements()) 