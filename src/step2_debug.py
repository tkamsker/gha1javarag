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

logger = logging.getLogger('java_analysis.step2_debug')

class DebugRequirementsProcessor:
    def __init__(self):
        load_dotenv()
        self.processed_files: Set[str] = set()
        self.output_dir = os.getenv('OUTPUT_DIR', './output')
        self.md_dir = Path(self.output_dir) / "requirements"
        self.md_dir.mkdir(parents=True, exist_ok=True)
        
        # Debug mode configuration
        self.debug_file = os.getenv('DEBUGFILE')
        self.debug_mode = bool(self.debug_file and os.path.exists(self.debug_file))
        
        # StrictDoc configuration
        self.strictdoc_enabled = os.getenv('STRICTDOC', 'false').lower() == 'true'
        if self.strictdoc_enabled:
            self.strictdoc_dir = Path(self.output_dir) / "strictdoc"
            self.strictdoc_dir.mkdir(parents=True, exist_ok=True)
            logger.info("StrictDoc generation enabled")
        
        # Initialize enhanced ChromaDB connector
        self.chromadb_connector = EnhancedChromaDBConnector()
        logger.info("Initialized enhanced ChromaDB connector with intelligent code chunking")
        
        # Enhanced rate limiting settings for debug mode
        rate_config = RateLimitConfig(
            requests_per_minute=10,  # More conservative for debug
            requests_per_hour=600,   # More conservative for debug
            delay_between_requests=6.0,  # Longer delays for debug
            exponential_backoff_base=2.0,
            max_retries=5
        )
        self.rate_limiter = RateLimiter(rate_config)
        
        # Batch processing settings for debug mode
        self.max_files_per_batch = 2  # Smaller batches for debug
        self.max_files_to_process = 50  # Limit total files to process in debug
        
        # Initialize AI provider using the same pattern as main.py
        self.ai_provider = create_ai_provider()
        logger.info(f"Using {self.ai_provider.get_provider_name()} provider with model: {self.ai_provider.get_model_name()}")
        logger.info(f"Debug mode: {'enabled' if self.debug_mode else 'disabled'}")

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
        """Convert markdown content to StrictDoc format with debug enhancements"""
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
        """Load metadata from ChromaDB with enhanced debug information"""
        try:
            # Get chunk statistics to understand what's available
            stats = self.chromadb_connector.get_chunk_statistics()
            logger.info(f"ChromaDB statistics: {stats}")
            
            # In debug mode, try to load from debug metadata file first
            if self.debug_mode:
                debug_metadata_file = os.path.join(self.output_dir, 'debug_metadata.json')
                if os.path.exists(debug_metadata_file):
                    logger.info(f"Loading debug metadata from {debug_metadata_file}")
                    try:
                        with open(debug_metadata_file, 'r', encoding='utf-8') as f:
                            debug_metadata = json.load(f)
                        
                        # Filter for files that were successfully analyzed
                        analyzed_files = [f for f in debug_metadata if f.get('analysis_status') == 'completed']
                        logger.info(f"Loaded {len(analyzed_files)} analyzed files from debug metadata")
                        return analyzed_files
                    except Exception as e:
                        logger.warning(f"Error loading debug metadata: {e}")
            
            # Use multiple generic queries to get all documents
            # This approach ensures we get files from different categories
            all_results = []
            queries = [
                "java code",  # Java files
                "xml configuration",  # Configuration files
                "sql database",  # Database files
                "html web",  # Web files
                "javascript",  # JS files
                "properties",  # Properties files
                "test",  # Test files
            ]
            
            for query in queries:
                try:
                    results = self.chromadb_connector.search_documents(query, n_results=50)
                    all_results.extend(results)
                    logger.debug(f"Query '{query}' returned {len(results)} results")
                except Exception as e:
                    logger.warning(f"Error querying ChromaDB with '{query}': {e}")
                    continue
            
            # Remove duplicates based on file_path
            unique_results = []
            seen_paths = set()
            for result in all_results:
                file_path = result.get('file_path', '')
                if file_path and file_path not in seen_paths:
                    unique_results.append(result)
                    seen_paths.add(file_path)
            
            logger.info(f"Retrieved {len(unique_results)} unique files from ChromaDB")
            return unique_results
            
        except Exception as e:
            logger.error(f"Error loading metadata from ChromaDB: {e}")
            return self._load_metadata_fallback()

    def _load_metadata_fallback(self) -> List[Dict[str, Any]]:
        """Fallback method to load metadata from JSON file"""
        try:
            metadata_file = os.path.join(self.output_dir, 'metadata.json')
            if os.path.exists(metadata_file):
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                logger.info(f"Loaded {len(metadata)} files from fallback metadata file")
                return metadata
            else:
                logger.warning("No metadata file found for fallback")
                return []
        except Exception as e:
            logger.error(f"Error loading fallback metadata: {e}")
            return []

    def _get_file_type(self, file_path: str) -> str:
        """Get file type based on extension"""
        ext = Path(file_path).suffix.lower()
        type_mapping = {
            '.java': 'Java source file',
            '.jsp': 'Java Server Page',
            '.xml': 'XML configuration',
            '.html': 'HTML file',
            '.js': 'JavaScript file',
            '.sql': 'SQL script'
        }
        return type_mapping.get(ext, 'Unknown file type')

    def prioritize_files(self, metadata: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritize files for debug mode processing"""
        if self.debug_mode:
            # Debug mode: prioritize files with pom.xml analysis and debug metadata
            priority_order = [
                lambda f: f.get('pom_analysis') is not None,  # Files with pom.xml analysis first
                lambda f: f.get('debug_mode') is True,  # Debug mode files
                lambda f: f.get('file_path', '').endswith('.java'),
                lambda f: f.get('file_path', '').endswith('.jsp'),
                lambda f: f.get('file_path', '').endswith('.xml'),
                lambda f: True
            ]
        else:
            # Normal mode prioritization
            priority_order = [
                lambda f: f.get('file_path', '').endswith('.java'),
                lambda f: f.get('file_path', '').endswith('.jsp'),
                lambda f: 'index' in f.get('file_path', '').lower(),
                lambda f: 'home' in f.get('file_path', '').lower(),
                lambda f: 'main' in f.get('file_path', '').lower(),
                lambda f: f.get('file_path', '').endswith('.xml'),
                lambda f: f.get('file_path', '').endswith('.xsd'),
                lambda f: f.get('file_path', '').endswith('.wsdl'),
                lambda f: f.get('file_path', '').endswith('.xslt'),
                lambda f: f.get('file_path', '').endswith('.properties'),
                lambda f: f.get('file_path', '').endswith('.sql'),
                lambda f: True
            ]
        
        prioritized = []
        for priority_func in priority_order:
            for item in metadata:
                if priority_func(item) and item not in prioritized:
                    prioritized.append(item)
                    if len(prioritized) >= self.max_files_to_process:
                        break
            if len(prioritized) >= self.max_files_to_process:
                break
        
        return prioritized

    def should_skip_file(self, file_path: str) -> bool:
        """Determine if a file should be skipped (more permissive in debug mode)"""
        import re
        skip_patterns = [
            r'\.git/',
            r'node_modules/',
            r'\.DS_Store',
            r'\.log$',
            r'\.tmp$',
            r'\.bak$',
            r'\.swp$',
            r'\.swo$',
            r'\.class$',
            r'\.jar$',
            r'\.war$',
            r'\.ear$',
            r'package-info\.java$',
        ]
        
        # In debug mode, be more permissive
        if self.debug_mode:
            skip_patterns = [
                r'\.git/',
                r'node_modules/',
                r'\.DS_Store',
                r'\.class$',
                r'\.jar$',
                r'\.war$',
                r'\.ear$',
            ]
        
        for pattern in skip_patterns:
            if re.search(pattern, file_path, re.IGNORECASE):
                return True
        return False

    async def analyze_files_batch(self, files_batch: List[Dict[str, Any]]) -> None:
        """Analyze multiple files in a single API call with enhanced debug information"""
        if not files_batch:
            return
            
        logger = logging.getLogger('java_analysis.debug_step2')
        logger.info(f"Analyzing batch of {len(files_batch)} files in debug mode")
        
        # Check if we should continue making requests (only for OpenAI)
        if self.ai_provider.get_provider_name() == "OpenAI":
            if not self.rate_limiter.should_continue_requests():
                stats = self.rate_limiter.get_stats()
                if stats.get('quota_exceeded'):
                    logger.error("Cannot continue analysis due to quota exceeded. Please check your OpenAI billing.")
                    return
        
        # Wait for rate limiter before making API call
        await self.rate_limiter.wait_if_needed()
        
        # Create a combined prompt for all files with enhanced debug information
        files_content = []
        for file_meta in files_batch:
            file_path = file_meta.get('file_path', '')
            file_type = file_meta.get('file_type', 'Unknown')
            content = file_meta.get('content', '')[:800]
            
            # Add pom.xml analysis if available
            pom_info = ""
            if 'pom_analysis' in file_meta:
                pom_analysis = file_meta['pom_analysis']
                pom_info = f"\nPOM Analysis: {json.dumps(pom_analysis.get('ai_analysis', {}), indent=2)}"
            
            # Add debug metadata
            debug_info = ""
            if file_meta.get('debug_mode'):
                debug_info = f"\nDebug Info: Processed from {file_meta.get('debug_file_source', 'unknown')}"
            
            files_content.append(f"""
File: {file_path}
Type: {file_type}
Content Preview: {content[:400]}...
POM Info: {pom_info}
Debug Info: {debug_info}
---""")
        
        combined_content = "\n".join(files_content)
        
        # Enhanced prompt for debug mode
        prompt = f"""Analyze the following files and generate detailed requirements documentation for each:

{combined_content}

For each file, provide requirements in the following format:

## File: [filename]

1. **Purpose and Overview**
   - Describe the main purpose of this file
   - Explain its role in the overall system

2. **Key Components**
   - List and describe the main components/classes/functions
   - Explain their responsibilities

3. **Data Structures**
   - Identify important data structures
   - Describe their relationships and usage

4. **Business Rules**
   - Extract business logic and rules
   - Identify validation and processing requirements

5. **Integration Points**
   - Describe how this file integrates with other components
   - Identify external dependencies and APIs

6. **Security Considerations**
   - Identify security-related code and requirements
   - Note authentication and authorization patterns

7. **Performance Notes**
   - Identify performance-critical sections
   - Note optimization opportunities

8. **Debug Insights**
   - Code quality assessment
   - Potential issues and improvements
   - Architecture recommendations

Format your response as:
## File: [filename]
[detailed requirements for this file]

## File: [filename]
[detailed requirements for this file]
..."""
        
        for attempt in range(self.rate_limiter.config.max_retries):
            try:
                # Wait for rate limiter (includes exponential backoff for retries)
                if attempt > 0:
                    await self.rate_limiter.wait_if_needed()
                
                # Create messages for the AI provider
                messages = [
                    {"role": "system", "content": "You are an expert requirements analyst specializing in Java enterprise applications. Provide detailed, structured requirements documentation with focus on business logic, technical architecture, and implementation details."},
                    {"role": "user", "content": prompt}
                ]
                
                # Get analysis from AI provider
                analysis = await self.ai_provider.create_chat_completion(
                    messages=messages,
                    temperature=0.4,
                    max_tokens=2500
                )
                
                # Parse the response
                await self.parse_batch_response(analysis, files_batch)
                return
                
            except Exception as e:
                logger.error(f"Error in batch analysis attempt {attempt + 1}: {str(e)}")
                if attempt == self.rate_limiter.config.max_retries - 1:
                    logger.error(f"Failed to analyze batch after {self.rate_limiter.config.max_retries} attempts")
                    return
                
                # Wait before retry
                await asyncio.sleep(self.rate_limiter.config.delay_between_requests * (2 ** attempt))

    async def parse_batch_response(self, analysis: str, files_batch: List[Dict[str, Any]]) -> None:
        """Parse AI response and generate markdown files with enhanced debug information"""
        logger = logging.getLogger('java_analysis.debug_step2')
        
        try:
            # Split response by file sections
            sections = analysis.split('## File:')
            
            for file_meta in files_batch:
                file_path = file_meta.get('file_path', '')
                file_name = os.path.basename(file_path)
                
                # Find matching section
                matching_section = None
                for section in sections[1:]:  # Skip first empty section
                    if file_name in section or file_path in section:
                        matching_section = section
                        break
                
                if matching_section:
                    try:
                        # Generate markdown content
                        markdown_content = f"# Requirements Analysis: {file_name}\n\n"
                        markdown_content += f"**File Path:** `{file_path}`\n\n"
                        
                        # Add debug information
                        if file_meta.get('debug_mode'):
                            markdown_content += f"**Debug Mode:** Enabled\n"
                            markdown_content += f"**Debug Source:** {file_meta.get('debug_file_source', 'unknown')}\n\n"
                        
                        # Add pom.xml information if available
                        if 'pom_analysis' in file_meta:
                            pom_analysis = file_meta['pom_analysis']
                            markdown_content += "## POM.xml Analysis\n\n"
                            if 'ai_analysis' in pom_analysis:
                                ai_pom = pom_analysis['ai_analysis']
                                markdown_content += f"**Project Type:** {ai_pom.get('project_type', 'Unknown')}\n\n"
                                markdown_content += f"**Technology Stack:** {', '.join(ai_pom.get('technology_stack', []))}\n\n"
                                markdown_content += f"**Architecture Patterns:** {', '.join(ai_pom.get('architecture_patterns', []))}\n\n"
                        
                        # Add the AI analysis content
                        markdown_content += matching_section.strip()
                        
                        # Save markdown file
                        subdir = self.get_subdirectory_for_file(file_path)
                        subdir_path = self.md_dir / subdir
                        subdir_path.mkdir(parents=True, exist_ok=True)
                        
                        filename = self.get_unique_filename(subdir_path, Path(file_name).stem)
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(markdown_content)
                        
                        # Generate StrictDoc if enabled
                        if self.strictdoc_enabled:
                            strictdoc_content = self.convert_to_strictdoc(markdown_content, file_path)
                            strictdoc_filename = filename.with_suffix('.sdoc')
                            with open(strictdoc_filename, 'w', encoding='utf-8') as f:
                                f.write(strictdoc_content)
                        
                        self.processed_files.add(file_path)
                        logger.info(f"Generated requirements for {file_path}")
                        
                    except Exception as e:
                        logger.error(f"Error processing requirements for {file_path}: {str(e)}")
                else:
                    logger.warning(f"No matching section found for {file_path}")
            
        except Exception as e:
            logger.error(f"Error parsing batch response: {str(e)}")

    async def process_files_with_batching(self) -> None:
        """Process files in batches with enhanced debug processing"""
        logger = logging.getLogger('java_analysis.debug_step2')
        
        # Load metadata from ChromaDB
        metadata = self.load_metadata_from_chromadb()
        if not metadata:
            logger.warning("No metadata found to process")
            return
        
        logger.info(f"Loaded {len(metadata)} files for processing")
        
        # Prioritize files
        prioritized_files = self.prioritize_files(metadata)
        logger.info(f"Prioritized {len(prioritized_files)} files for analysis")
        
        # Process in batches
        for i in range(0, len(prioritized_files), self.max_files_per_batch):
            batch = prioritized_files[i:i + self.max_files_per_batch]
            logger.info(f"Processing batch {i//self.max_files_per_batch + 1}/{(len(prioritized_files) + self.max_files_per_batch - 1)//self.max_files_per_batch}")
            
            await self.analyze_files_batch(batch)
            
            # Add delay between batches
            if i + self.max_files_per_batch < len(prioritized_files):
                await asyncio.sleep(self.rate_limiter.config.delay_between_requests)

    def generate_index(self) -> None:
        """Generate index file with debug information"""
        logger = logging.getLogger('java_analysis.debug_step2')
        
        try:
            index_file = self.md_dir / "step2_debug_index.md"
            
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write("# Requirements Analysis Index (Debug Mode)\n\n")
                f.write(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                if self.debug_mode:
                    f.write(f"**Debug Mode:** Enabled\n")
                    f.write(f"**Debug File:** {self.debug_file}\n\n")
                
                # Group files by subdirectory
                subdir_files = {}
                for file_path in sorted(self.processed_files):
                    subdir = self.get_subdirectory_for_file(file_path)
                    if subdir not in subdir_files:
                        subdir_files[subdir] = []
                    subdir_files[subdir].append(file_path)
                
                # Write index by subdirectory
                for subdir in sorted(subdir_files.keys()):
                    f.write(f"## {subdir}\n\n")
                    for file_path in sorted(subdir_files[subdir]):
                        file_name = os.path.basename(file_path)
                        relative_path = os.path.join(subdir, f"{Path(file_name).stem}.md")
                        f.write(f"- [{file_name}]({relative_path})\n")
                    f.write("\n")
                
                # Add StrictDoc section if enabled
                if self.strictdoc_enabled:
                    f.write("## StrictDoc Files\n\n")
                    strictdoc_dir = self.strictdoc_dir
                    if strictdoc_dir.exists():
                        for sdoc_file in sorted(strictdoc_dir.glob("**/*.sdoc")):
                            relative_path = sdoc_file.relative_to(self.output_dir)
                            f.write(f"- [{sdoc_file.name}]({relative_path})\n")
            
            logger.info(f"Generated debug index at {index_file}")
            
        except Exception as e:
            logger.error(f"Error generating debug index: {str(e)}")

async def generate_requirements_debug():
    """Main function for debug mode requirements generation"""
    logger = logging.getLogger('java_analysis.debug_step2')
    logger.info("Starting debug mode requirements generation")
    
    try:
        processor = DebugRequirementsProcessor()
        
        # Process files with batching
        await processor.process_files_with_batching()
        
        # Generate index
        processor.generate_index()
        
        logger.info("Debug mode requirements generation completed successfully")
        
    except Exception as e:
        logger.error(f"Error in debug mode requirements generation: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(generate_requirements_debug()) 