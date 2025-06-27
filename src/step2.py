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
import uuid

logger = logging.getLogger('java_analysis.step2')

class RequirementsProcessor:
    def __init__(self):
        load_dotenv()
        self.processed_files: Set[str] = set()
        self.output_dir = os.getenv('OUTPUT_DIR', './output')
        self.md_dir = Path(self.output_dir) / "requirements"
        self.md_dir.mkdir(parents=True, exist_ok=True)
        
        # StrictDoc configuration
        self.strictdoc_enabled = os.getenv('STRICTDOC', 'false').lower() == 'true'
        if self.strictdoc_enabled:
            self.strictdoc_dir = Path(self.output_dir) / "strictdoc"
            self.strictdoc_dir.mkdir(parents=True, exist_ok=True)
            logger.info("StrictDoc generation enabled")
        
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

    def get_subdirectory_for_file(self, file_path: str) -> str:
        """Get subdirectory name based on first directory in file path relative to JAVA_SOURCE_DIR"""
        try:
            java_source_dir = os.getenv('JAVA_SOURCE_DIR', '.')
            java_source_path = Path(java_source_dir).resolve()
            file_path_obj = Path(file_path).resolve()
            
            # Try to make file path relative to JAVA_SOURCE_DIR
            try:
                relative_path = file_path_obj.relative_to(java_source_path)
            except ValueError:
                # If file is not under JAVA_SOURCE_DIR, use the first directory in the path
                relative_path = Path(file_path)
            
            # Get the first directory component
            path_parts = relative_path.parts
            if len(path_parts) > 0:
                return path_parts[0]
            else:
                return "unknown"
                
        except Exception as e:
            logger.warning(f"Error determining subdirectory for {file_path}: {e}")
            return "unknown"

    def get_unique_filename(self, base_dir: Path, filename: str, extension: str = '.md') -> Path:
        """Get unique filename with numbering if file exists"""
        base_name = filename
        counter = 0
        
        while True:
            if counter == 0:
                full_filename = f"{base_name}{extension}"
            else:
                full_filename = f"{base_name}-{counter}{extension}"
            
            file_path = base_dir / full_filename
            if not file_path.exists():
                return file_path
            
            counter += 1

    def convert_to_strictdoc(self, markdown_content: str, file_path: str) -> str:
        """Convert markdown content to StrictDoc format"""
        # Extract title from markdown
        title_match = re.search(r'^#\s+(.+)$', markdown_content, re.MULTILINE)
        title = title_match.group(1) if title_match else f"Requirements Analysis: {file_path}"
        
        # Remove the first heading line
        content_without_title = re.sub(r'^#\s+.+$', '', markdown_content, count=1, flags=re.MULTILINE).strip()
        
        # Generate a unique UID for the document
        uid = Path(file_path).stem.lower().replace('_', '-').replace('.', '-')
        
        # Parse the content to extract different sections
        sections = self._parse_content_sections(content_without_title)
        
        # Convert markdown to proper StrictDoc format
        # Using only valid StrictDoc fields with proper order
        strictdoc_content = f"""[DOCUMENT]
TITLE: {title}
UID: REQ-ANALYSIS-{uid.upper()}

"""
        
        # Add requirements based on parsed sections
        req_counter = 1
        for section_name, section_content in sections.items():
            if section_content.strip():
                req_uid = f"REQ-{req_counter:03d}"
                
                # Clean up the content to avoid parsing issues
                clean_content = section_content.strip().replace('\n', ' ').replace('  ', ' ')
                if len(clean_content) > 150:
                    clean_content = clean_content[:150] + "..."
                
                # Generate a simple MID (Machine ID)
                mid = str(uuid.uuid4()).replace('-', '')[:16]
                
                # Use heredoc format for STATEMENT to handle multi-line content properly
                strictdoc_content += f"""[REQUIREMENT]
MID: {mid}
UID: {req_uid}
TITLE: {section_name}
STATEMENT: >>>
{clean_content}
<<<
[/REQUIREMENT]

"""
                req_counter += 1
        
        strictdoc_content += "[/DOCUMENT]"
        return strictdoc_content
    
    def _parse_content_sections(self, content: str) -> dict:
        """Parse content into sections based on numbered lists and headers"""
        sections = {}
        
        # Split by numbered sections (1., 2., 3., etc.)
        lines = content.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            # Check for numbered section headers
            section_match = re.match(r'^(\d+)\.\s+(.+)$', line.strip())
            if section_match:
                # Save previous section
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                
                # Start new section
                current_section = section_match.group(2).strip()
                current_content = []
            elif current_section:
                current_content.append(line)
        
        # Save last section
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()
        
        # If no sections found, create a default one
        if not sections:
            sections["General Requirements"] = content
        
        return sections

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
        """Parse the batch response and create individual markdown files with subdirectory structure"""
        # Split by file sections
        sections = re.split(r'## File:\s*', analysis)
        
        for i, file_meta in enumerate(files_batch):
            file_path = file_meta.get('file_path', '')
            
            # Get subdirectory based on file path
            subdir_name = self.get_subdirectory_for_file(file_path)
            subdir_path = self.md_dir / subdir_name
            subdir_path.mkdir(parents=True, exist_ok=True)
            
            # Get unique filename
            base_filename = Path(file_path).stem
            md_file_path = self.get_unique_filename(subdir_path, base_filename, '.md')
            
            # Get the corresponding section content
            if i + 1 < len(sections):
                section_content = sections[i + 1].strip()
            else:
                section_content = "Analysis not available for this file."
            
            # Create markdown content
            markdown_content = f"# Requirements Analysis: {file_path}\n\n{section_content}"
            
            # Write markdown file
            with open(md_file_path, 'w') as f:
                f.write(markdown_content)
            
            logger.debug(f"Generated requirements document: {md_file_path}")
            
            # Generate StrictDoc version if enabled
            if self.strictdoc_enabled:
                strictdoc_subdir_path = self.strictdoc_dir / subdir_name
                strictdoc_subdir_path.mkdir(parents=True, exist_ok=True)
                
                strictdoc_file_path = self.get_unique_filename(strictdoc_subdir_path, base_filename, '.sdoc')
                strictdoc_content = self.convert_to_strictdoc(markdown_content, file_path)
                
                with open(strictdoc_file_path, 'w') as f:
                    f.write(strictdoc_content)
                
                logger.debug(f"Generated StrictDoc document: {strictdoc_file_path}")

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
            f.write("## Requirements Documents by Subdirectory\n\n")
            
            # Group files by subdirectory
            subdir_files = {}
            for file_path in sorted(self.processed_files):
                subdir_name = self.get_subdirectory_for_file(file_path)
                if subdir_name not in subdir_files:
                    subdir_files[subdir_name] = []
                subdir_files[subdir_name].append(file_path)
            
            # Write index by subdirectory
            for subdir_name in sorted(subdir_files.keys()):
                f.write(f"### {subdir_name}\n\n")
                for file_path in subdir_files[subdir_name]:
                    md_filename = f"{Path(file_path).stem}.md"
                    f.write(f"- [{file_path}](./{subdir_name}/{md_filename})\n")
                f.write("\n")
        
        logger.info(f"Generated index file: {index_path}")
        
        # Generate StrictDoc index if enabled
        if self.strictdoc_enabled:
            strictdoc_index_path = self.strictdoc_dir / "step2_strictdoc_index.md"
            
            with open(strictdoc_index_path, 'w') as f:
                f.write("# StrictDoc Documentation Index\n\n")
                f.write(f"Total files processed: {len(self.processed_files)}\n\n")
                f.write("## StrictDoc Documents by Subdirectory\n\n")
                
                # Group files by subdirectory
                for subdir_name in sorted(subdir_files.keys()):
                    f.write(f"### {subdir_name}\n\n")
                    for file_path in subdir_files[subdir_name]:
                        sdoc_filename = f"{Path(file_path).stem}.sdoc"
                        f.write(f"- [{file_path}](./{subdir_name}/{sdoc_filename})\n")
                    f.write("\n")
            
            logger.info(f"Generated StrictDoc index file: {strictdoc_index_path}")

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