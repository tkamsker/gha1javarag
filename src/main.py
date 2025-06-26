import asyncio
from file_processor import FileProcessor
from ai_analyzer import AIAnalyzer
from chromadb_connector import ChromaDBConnector
from requirements_analyzer import RequirementsAnalyzer
import json
import os
from typing import Dict, Any, List
from dotenv import load_dotenv
from logger_config import setup_logging
import logging
from rate_limiter import RateLimiter, RateLimitConfig
from ai_providers import create_ai_provider

logger = setup_logging()

class BatchAIAnalyzer:
    """Batch AI analyzer for processing multiple files efficiently"""
    
    def __init__(self):
        load_dotenv()
        self.output_dir = os.getenv('OUTPUT_DIR', './output')
        
        # Initialize AI provider
        self.ai_provider = create_ai_provider()
        logger.info(f"Using {self.ai_provider.get_provider_name()} provider with model: {self.ai_provider.get_model_name()}")
        
        # Rate limiting configuration based on provider
        if self.ai_provider.get_provider_name() == "OpenAI":
            # Conservative rate limiting for OpenAI
            self.rate_config = RateLimitConfig(
                requests_per_minute=15,
                requests_per_hour=800,
                delay_between_requests=4.0,
                exponential_backoff_base=2.0,
                max_retries=5
            )
        else:
            # More relaxed rate limiting for Ollama (local)
            self.rate_config = RateLimitConfig(
                requests_per_minute=60,
                requests_per_hour=1000,
                delay_between_requests=1.0,
                exponential_backoff_base=2.0,
                max_retries=3
            )
        
        self.rate_limiter = RateLimiter(self.rate_config)
        
        # Batch processing configuration
        self.max_files_per_batch = 3  # Process 3 files per API call
        self.max_files_to_process = 500000  # Limit total files to process

    def prioritize_files(self, files_metadata: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritize files based on importance and type"""
        priority_order = [
            # High priority - core application files
            lambda f: f.get('file_path', '').endswith('.java'),
            lambda f: f.get('file_path', '').endswith('.jsp'),
            lambda f: 'index' in f.get('file_path', '').lower(),
            lambda f: 'home' in f.get('file_path', '').lower(),
            lambda f: 'main' in f.get('file_path', '').lower(),
            # Medium priority - configuration files
            lambda f: f.get('file_path', '').endswith('.xml'),
            lambda f: f.get('file_path', '').endswith('.xsd'),
            lambda f: f.get('file_path', '').endswith('.wsdl'),
            lambda f: f.get('file_path', '').endswith('.xslt'),
            lambda f: f.get('file_path', '').endswith('.properties'),
            lambda f: f.get('file_path', '').endswith('.sql'),
            # Lower priority - other files
            lambda f: True  # Catch all remaining files
        ]
        
        prioritized = []
        for priority_func in priority_order:
            for item in files_metadata:
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
            r'\.class$',  # Compiled Java files
            r'\.jar$',    # JAR files
            r'\.war$',    # WAR files
            r'\.ear$',    # EAR files
            r'package-info\.java$',  # Package info files
        ]
        
        for pattern in skip_patterns:
            if re.search(pattern, file_path, re.IGNORECASE):
                return True
        return False

    async def analyze_files_batch(self, files_batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze multiple files in a single API call"""
        if not files_batch:
            return []
            
        logger = logging.getLogger('java_analysis.batch_analyzer')
        logger.info(f"Analyzing batch of {len(files_batch)} files")
        
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
            content = file_meta.get('content', '')[:800]  # Limit content length
            
            files_content.append(f"""
File: {file_path}
Type: {file_type}
Content Preview: {content[:400]}...
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
                    max_tokens=2000
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
        """Analyze files in batches with rate limiting"""
        logger = logging.getLogger('java_analysis.batch_analyzer')
        logger.info(f"Starting batch analysis of {len(files_metadata)} files")
        
        # Prioritize and filter files
        prioritized_files = self.prioritize_files(files_metadata)
        
        # Filter out files to skip
        files_to_process = [
            f for f in prioritized_files 
            if not self.should_skip_file(f.get('file_path', ''))
        ]
        
        logger.info(f"Processing {len(files_to_process)} files in batches of {self.max_files_per_batch}")
        
        # Process files in batches
        analyzed_metadata = []
        for i in range(0, len(files_to_process), self.max_files_per_batch):
            batch = files_to_process[i:i + self.max_files_per_batch]
            analyzed_batch = await self.analyze_files_batch(batch)
            analyzed_metadata.extend(analyzed_batch)
            
            # Progress update
            logger.info(f"Progress: {len(analyzed_metadata)}/{len(files_to_process)} files processed")
        
        # Add unprocessed files with failed status
        processed_paths = {f.get('file_path', '') for f in analyzed_metadata}
        for file_meta in files_metadata:
            if file_meta.get('file_path', '') not in processed_paths:
                file_meta.update({
                    'analysis_status': 'skipped',
                    'error': 'File not selected for processing due to rate limiting'
                })
                analyzed_metadata.append(file_meta)
        
        logger.info("Completed batch analysis of all files")
        return analyzed_metadata

async def process_codebase():
    """Main function to process and analyze the codebase"""
    # Set up logging
    logger = setup_logging(level=logging.INFO)  # Reduced logging level
    logger.info("Starting codebase analysis process")
    
    # Load environment variables
    load_dotenv()
    logger.debug("Environment variables loaded")
    
    try:
        # Initialize components
        logger.info("Initializing components...")
        file_processor = FileProcessor()
        batch_analyzer = BatchAIAnalyzer()  # Use new batch analyzer
        chroma_connector = ChromaDBConnector()
        output_dir = os.getenv('OUTPUT_DIR', './output')
        req_analyzer = RequirementsAnalyzer(output_dir)
        
        # Step 1: Process and analyze files
        logger.info("Step 1: Processing and analyzing files...")
        
        # 1.1 Process files and extract metadata
        logger.info("1.1 Processing files and extracting metadata...")
        files_metadata = file_processor.process_files()
        
        # 1.2 Analyze files with AI using batch processing
        logger.info("1.2 Analyzing files with AI (batch processing)...")
        analyzed_metadata = await batch_analyzer.analyze_files(files_metadata)
        
        # 1.3 Save raw metadata to JSON
        logger.info("1.3 Saving raw metadata to JSON...")
        metadata_file = os.path.join(output_dir, 'metadata.json')
        file_processor.save_metadata(analyzed_metadata, metadata_file)
        
        # 1.4 Store in ChromaDB
        logger.info("1.4 Storing in ChromaDB...")
        chroma_connector.store_metadata(analyzed_metadata)
        
        # Step 2: Generate requirements documentation
        logger.info("Step 2: Generating requirements documentation...")
        req_analyzer.analyze_and_generate(analyzed_metadata)
        
        logger.info("Process completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during processing: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(process_codebase()) 