import asyncio
from file_processor import FileProcessor
from ai_analyzer import AIAnalyzer
from chromadb_connector import ChromaDBConnector, EnhancedChromaDBConnector
from requirements_analyzer import RequirementsAnalyzer
import json
import os
from typing import Dict, Any, List
from dotenv import load_dotenv
from logger_config import setup_logging
import logging
from rate_limiter import RateLimiter, RateLimitConfig
from ai_providers import create_ai_provider

class TestBatchAIAnalyzer:
    """Test batch AI analyzer with very conservative rate limiting"""
    
    def __init__(self):
        load_dotenv()
        self.output_dir = os.getenv('OUTPUT_DIR', './output')
        
        # Initialize AI provider
        self.ai_provider = create_ai_provider()
        logger = logging.getLogger('java_analysis.test_analyzer')
        logger.info(f"Using {self.ai_provider.get_provider_name()} provider with model: {self.ai_provider.get_model_name()}")
        
        # Rate limiting configuration based on provider
        if self.ai_provider.get_provider_name() == "OpenAI":
            # Very conservative rate limiting for OpenAI
            self.rate_config = RateLimitConfig(
                requests_per_minute=5,  # Very conservative
                requests_per_hour=200,  # Very conservative
                delay_between_requests=10.0,  # Long delays
                exponential_backoff_base=2.0,
                max_retries=5
            )
        else:
            # More relaxed rate limiting for Ollama (local)
            self.rate_config = RateLimitConfig(
                requests_per_minute=20,  # Higher limit for local
                requests_per_hour=500,
                delay_between_requests=2.0,  # Shorter delays for local
                exponential_backoff_base=2.0,
                max_retries=3
            )
        
        self.rate_limiter = RateLimiter(self.rate_config)
        
        # Very limited batch processing for testing
        self.max_files_per_batch = 2  # Only 2 files per API call
        self.max_files_to_process = 20  # Only 10 files total

    def get_important_files(self, files_metadata: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get only the most important files for testing"""
        import re
        
        # Priority order for file types
        priority_patterns = [
            r'\.jsp$',  # JSP files first
            r'index\.',  # Index files
            r'home\.',   # Home files
            r'\.java$',  # Java files
            r'pom\.xml$',  # Maven config
            r'web\.xml$',  # Web config
        ]
        
        important_files = []
        for pattern in priority_patterns:
            for item in files_metadata:
                file_path = item.get('file_path', '')
                if (re.search(pattern, file_path, re.IGNORECASE) and 
                    item not in important_files and 
                    len(important_files) < self.max_files_to_process):
                    important_files.append(item)
        
        logging.getLogger('java_analysis.test_analyzer').info(f"Selected {len(important_files)} important files for testing")
        return important_files

    def should_skip_file(self, file_path: str) -> bool:
        """Determine if a file should be skipped"""
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
        
        for pattern in skip_patterns:
            if re.search(pattern, file_path, re.IGNORECASE):
                return True
        return False

    async def analyze_files_batch(self, files_batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze multiple files in a single API call"""
        if not files_batch:
            return []
            
        logger = logging.getLogger('java_analysis.test_analyzer')
        logger.info(f"Analyzing batch of {len(files_batch)} files (TEST MODE)")
        
        # Check if we should continue making requests (only for OpenAI)
        if self.ai_provider.get_provider_name() == "OpenAI":
            if not self.rate_limiter.should_continue_requests():
                stats = self.rate_limiter.get_stats()
                if stats.get('quota_exceeded'):
                    logger.error("Cannot continue analysis due to quota exceeded. Please check your OpenAI billing.")
                    # Mark files as failed due to quota
                    for file_meta in files_batch:
                        file_meta.update({
                            'analysis_status': 'failed',
                            'error': 'OpenAI API quota exceeded. Please check billing and plan details.'
                        })
                    return files_batch
        
        # Wait for rate limiter before making API call
        await self.rate_limiter.wait_if_needed()
        
        # Create a combined prompt for all files
        files_content = []
        for file_meta in files_batch:
            file_path = file_meta.get('file_path', '')
            file_type = file_meta.get('file_type', 'Unknown')
            content = file_meta.get('content', '')[:600]  # Very limited content
            
            files_content.append(f"""
File: {file_path}
Type: {file_type}
Content Preview: {content[:300]}...
---""")
        
        combined_content = "\n".join(files_content)
        
        prompt = f"""Analyze the following files and provide requirements documentation for each:

{combined_content}

For each file, provide analysis in JSON format with the following structure:
{{
    "purpose": "string",
    "components": [
        {{
            "name": "string",
            "type": "string",
            "description": "string"
        }}
    ],
    "data_structures": [
        {{
            "name": "string",
            "fields": ["string"],
            "relationships": ["string"]
        }}
    ],
    "business_rules": [
        {{
            "description": "string",
            "location": "string"
        }}
    ],
    "dependencies": ["string"]
}}

Format your response as:
## File: [filename]
{{JSON analysis for this file}}

## File: [filename]
{{JSON analysis for this file}}
..."""
        
        for attempt in range(self.rate_limiter.config.max_retries):
            try:
                # Check if we should continue before each attempt (only for OpenAI)
                if self.ai_provider.get_provider_name() == "OpenAI":
                    if not self.rate_limiter.should_continue_requests():
                        stats = self.rate_limiter.get_stats()
                        if stats.get('quota_exceeded'):
                            logger.error("Cannot continue analysis due to quota exceeded. Please check your OpenAI billing.")
                            # Mark files as failed due to quota
                            for file_meta in files_batch:
                                file_meta.update({
                                    'analysis_status': 'failed',
                                    'error': 'OpenAI API quota exceeded. Please check billing and plan details.'
                                })
                            return files_batch
                
                # Wait for rate limiter (includes exponential backoff for retries)
                if attempt > 0:
                    await self.rate_limiter.wait_if_needed()
                
                # Create messages for the AI provider
                messages = [
                    {"role": "system", "content": "You are a code analysis expert. Provide concise but comprehensive analysis in the requested JSON format."},
                    {"role": "user", "content": prompt}
                ]
                
                # Get response from AI provider
                analysis = await self.ai_provider.create_chat_completion(
                    messages=messages,
                    temperature=0.2,
                    max_tokens=1500
                )
                
                # Record successful request
                self.rate_limiter.record_request()
                
                # Parse the response and update files
                analyzed_files = await self.parse_batch_response(analysis, files_batch)
                
                # Log rate limiting stats
                stats = self.rate_limiter.get_stats()
                logger.info(f"Rate limit stats: {stats['requests_last_minute']}/min, {stats['requests_last_hour']}/hour")
                
                logger.info(f"Successfully analyzed batch of {len(files_batch)} files")
                return analyzed_files
                
            except Exception as e:
                logger.error(f"Error analyzing batch (attempt {attempt + 1}): {str(e)}")
                self.rate_limiter.record_failure(e)
                
                # Check if this is a quota exceeded error (only for OpenAI)
                if self.ai_provider.get_provider_name() == "OpenAI":
                    if 'insufficient_quota' in str(e).lower() or 'quota' in str(e).lower():
                        logger.error("QUOTA EXCEEDED: Stopping all analysis. Please check your OpenAI billing.")
                        # Mark all remaining files as failed
                        for file_meta in files_batch:
                            file_meta.update({
                                'analysis_status': 'failed',
                                'error': 'OpenAI API quota exceeded. Please check billing and plan details.'
                            })
                        return files_batch
                
                if attempt == self.rate_limiter.config.max_retries - 1:
                    logger.error(f"Failed to analyze batch after {self.rate_limiter.config.max_retries} attempts")
                    # Mark files as failed but return them
                    for file_meta in files_batch:
                        file_meta.update({
                            'analysis_status': 'failed',
                            'error': str(e)
                        })
                    return files_batch

    async def parse_batch_response(self, analysis: str, files_batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Parse the batch response and update file metadata"""
        import re
        
        # Split by file sections
        sections = re.split(r'## File:\s*', analysis)
        
        for i, file_meta in enumerate(files_batch):
            # Get the corresponding section content
            if i + 1 < len(sections):
                section_content = sections[i + 1].strip()
                # Try to extract JSON from the section
                try:
                    # Look for JSON content in the section
                    json_match = re.search(r'\{.*\}', section_content, re.DOTALL)
                    if json_match:
                        import json
                        ai_analysis = json.loads(json_match.group())
                        file_meta.update({
                            'ai_analysis': ai_analysis,
                            'analysis_status': 'completed'
                        })
                    else:
                        file_meta.update({
                            'ai_analysis': section_content,
                            'analysis_status': 'completed'
                        })
                except Exception as e:
                    file_meta.update({
                        'ai_analysis': section_content,
                        'analysis_status': 'completed'
                    })
            else:
                file_meta.update({
                    'analysis_status': 'failed',
                    'error': 'Analysis not available for this file.'
                })
        
        return files_batch

    async def analyze_files(self, files_metadata: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze files in batches with very conservative rate limiting"""
        logger = logging.getLogger('java_analysis.test_analyzer')
        logger.info(f"Starting test batch analysis of {len(files_metadata)} files")
        
        # Get only important files for testing
        important_files = self.get_important_files(files_metadata)
        
        # Filter out files to skip
        files_to_process = [
            f for f in important_files 
            if not self.should_skip_file(f.get('file_path', ''))
        ]
        
        logger.info(f"Processing {len(files_to_process)} files in batches of {self.max_files_per_batch} (TEST MODE)")
        
        # Process files in batches
        analyzed_metadata = []
        for i in range(0, len(files_to_process), self.max_files_per_batch):
            batch = files_to_process[i:i + self.max_files_per_batch]
            analyzed_batch = await self.analyze_files_batch(batch)
            analyzed_metadata.extend(analyzed_batch)
            
            # Progress update
            logger.info(f"Progress: {len(analyzed_metadata)}/{len(files_to_process)} files processed")
        
        # Add unprocessed files with skipped status
        processed_paths = {f.get('file_path', '') for f in analyzed_metadata}
        for file_meta in files_metadata:
            if file_meta.get('file_path', '') not in processed_paths:
                file_meta.update({
                    'analysis_status': 'skipped',
                    'error': 'File not selected for processing in test mode'
                })
                analyzed_metadata.append(file_meta)
        
        logger.info("Completed test batch analysis of all files")
        return analyzed_metadata

async def process_codebase_test():
    """Test function to process and analyze the codebase with conservative settings"""
    # Set up logging
    logger = setup_logging(level=logging.INFO)
    logger.info("Starting codebase analysis process (TEST MODE)")
    
    # Load environment variables
    load_dotenv()
    logger.debug("Environment variables loaded")
    
    try:
        # Initialize components
        logger.info("Initializing components...")
        file_processor = FileProcessor()
        test_analyzer = TestBatchAIAnalyzer()  # Use test analyzer
        chroma_connector = ChromaDBConnector()
        output_dir = os.getenv('OUTPUT_DIR', './output')
        req_analyzer = RequirementsAnalyzer(output_dir)
        
        # Step 1: Process and analyze files
        logger.info("Step 1: Processing and analyzing files...")
        
        # 1.1 Process files and extract metadata
        logger.info("1.1 Processing files and extracting metadata...")
        files_metadata = file_processor.process_files()
        
        # 1.2 Analyze files with AI using test batch processing
        logger.info("1.2 Analyzing files with AI (test batch processing)...")
        analyzed_metadata = await test_analyzer.analyze_files(files_metadata)
        
        # 1.3 Save raw metadata to JSON
        logger.info("1.3 Saving raw metadata to JSON...")
        metadata_file = os.path.join(output_dir, 'metadata.json')
        file_processor.save_metadata(analyzed_metadata, metadata_file)
        
        # 1.4 Store in ChromaDB with enhanced chunking
        logger.info("1.4 Storing in ChromaDB with enhanced chunking...")
        try:
            # Try to use enhanced connector
            enhanced_connector = EnhancedChromaDBConnector()
            
            # Get the source directory from environment variable
            java_source_dir = os.getenv('JAVA_SOURCE_DIR', '.')
            logger.info(f"Using JAVA_SOURCE_DIR: {java_source_dir}")
            
            for file_meta in analyzed_metadata:
                file_path = file_meta.get('file_path', '')
                content = file_meta.get('content', '')
                ai_analysis = file_meta.get('ai_analysis', {})
                
                if file_path and content:
                    try:
                        enhanced_connector.store_enhanced_metadata(file_path, content, ai_analysis)
                        logger.debug(f"Stored enhanced metadata for: {file_path}")
                        file_meta['chromadb_status'] = 'success'
                    except Exception as e:
                        logger.error(f"Error storing enhanced metadata for {file_path}: {e}")
                        file_meta['chromadb_status'] = 'failed'
                        file_meta['chromadb_error'] = str(e)
                else:
                    logger.warning(f"Skipping ChromaDB storage for {file_path}: missing content")
                    file_meta['chromadb_status'] = 'skipped'
                    
        except ImportError:
            # Fallback to legacy connector
            logger.warning("EnhancedChromaDBConnector not available, using legacy connector")
            chroma_connector = ChromaDBConnector()
            chroma_connector.store_metadata(analyzed_metadata)
        except Exception as e:
            logger.error(f"Error initializing ChromaDB connector: {e}")
            # Continue without ChromaDB storage
            for file_meta in analyzed_metadata:
                file_meta['chromadb_status'] = 'failed'
                file_meta['chromadb_error'] = str(e)
        
        # Step 2: Generate requirements documentation
        logger.info("Step 2: Generating requirements documentation...")
        req_analyzer.analyze_and_generate(analyzed_metadata)
        
        logger.info("Test process completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during test processing: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(process_codebase_test()) 