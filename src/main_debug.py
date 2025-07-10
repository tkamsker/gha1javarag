import asyncio
from debug_file_processor import DebugFileProcessor
from ai_analyzer import AIAnalyzer
from chromadb_connector import EnhancedChromaDBConnector
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

class DebugBatchAIAnalyzer:
    """Enhanced batch AI analyzer for debug mode with pom.xml analysis"""
    
    def __init__(self):
        load_dotenv()
        self.output_dir = os.getenv('OUTPUT_DIR', './output')
        
        # Initialize AI provider
        self.ai_provider = create_ai_provider()
        logger.info(f"Using {self.ai_provider.get_provider_name()} provider with model: {self.ai_provider.get_model_name()}")
        
        # Initialize enhanced ChromaDB connector
        self.chromadb_connector = EnhancedChromaDBConnector()
        logger.info("Initialized enhanced ChromaDB connector with intelligent code chunking")
        
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
        
        # Debug mode configuration
        self.debug_file = os.getenv('DEBUGFILE')
        self.debug_mode = bool(self.debug_file and os.path.exists(self.debug_file))
        
        # Batch processing configuration (smaller batches for debug mode)
        self.max_files_per_batch = 2  # Process 2 files per API call for debug
        self.max_files_to_process = 100  # Limit total files to process in debug mode

    def prioritize_files(self, files_metadata: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritize files based on importance and type for debug mode"""
        if not self.debug_mode:
            # Use normal prioritization for non-debug mode
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
        else:
            # Debug mode: prioritize files with pom.xml analysis
            priority_order = [
                lambda f: f.get('pom_analysis') is not None,  # Files with pom.xml analysis first
                lambda f: f.get('file_path', '').endswith('.java'),
                lambda f: f.get('file_path', '').endswith('.jsp'),
                lambda f: f.get('file_path', '').endswith('.xml'),
                lambda f: True
            ]
        
        prioritized = []
        for priority_func in priority_order:
            for item in files_metadata:
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

    async def analyze_files_batch(self, files_batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze multiple files in a single API call with enhanced debug information"""
        if not files_batch:
            return []
            
        logger = logging.getLogger('java_analysis.debug_batch_analyzer')
        logger.info(f"Analyzing batch of {len(files_batch)} files in debug mode")
        
        # Check if we should continue making requests (only for OpenAI)
        if self.ai_provider.get_provider_name() == "OpenAI":
            if not self.rate_limiter.should_continue_requests():
                stats = self.rate_limiter.get_stats()
                if stats.get('quota_exceeded'):
                    logger.error("Cannot continue analysis due to quota exceeded. Please check your OpenAI billing.")
                    for file_meta in files_batch:
                        file_meta.update({
                            'analysis_status': 'failed',
                            'error': 'OpenAI API quota exceeded. Please check billing and plan details.'
                        })
                    return files_batch
        
        # Wait for rate limiter before making API call
        await self.rate_limiter.wait_if_needed()
        
        # Create a combined prompt for all files with enhanced debug information
        files_content = []
        for file_meta in files_batch:
            file_path = file_meta.get('file_path', '')
            file_type = file_meta.get('file_type', 'Unknown')
            content = file_meta.get('content', '')[:1000]  # More content for debug mode
            
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
Content Preview: {content[:600]}...
POM Info: {pom_info}
Debug Info: {debug_info}
---""")
        
        combined_content = "\n".join(files_content)
        
        # Enhanced prompt for debug mode
        prompt = f"""Analyze the following files in debug mode and provide comprehensive requirements documentation for each:

{combined_content}

For each file, provide detailed analysis in JSON format with the following enhanced structure:
{{
    "purpose": "string",
    "components": [
        {{
            "name": "string",
            "type": "string",
            "description": "string",
            "complexity": "string (low/medium/high)"
        }}
    ],
    "data_structures": [
        {{
            "name": "string",
            "fields": ["string"],
            "relationships": ["string"],
            "usage_patterns": ["string"]
        }}
    ],
    "business_rules": [
        {{
            "description": "string",
            "location": "string",
            "priority": "string (high/medium/low)"
        }}
    ],
    "dependencies": ["string"],
    "integration_points": ["string"],
    "security_considerations": ["string"],
    "performance_notes": ["string"],
    "debug_insights": {{
        "code_quality": "string",
        "potential_issues": ["string"],
        "improvement_suggestions": ["string"]
    }}
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
                    {"role": "system", "content": "You are an expert Java enterprise application analyst with deep knowledge of Maven projects, Spring frameworks, and enterprise architecture patterns. Provide detailed, accurate analysis for debug mode processing."},
                    {"role": "user", "content": prompt}
                ]
                
                # Get analysis from AI provider
                analysis = await self.ai_provider.create_chat_completion(
                    messages=messages,
                    temperature=0.3,
                    max_tokens=2000
                )
                
                # Parse the response
                return await self.parse_batch_response(analysis, files_batch)
                
            except Exception as e:
                logger.error(f"Error in batch analysis attempt {attempt + 1}: {str(e)}")
                if attempt == self.rate_limiter.config.max_retries - 1:
                    # Mark files as failed
                    for file_meta in files_batch:
                        file_meta.update({
                            'analysis_status': 'failed',
                            'error': f'Analysis failed after {self.rate_limiter.config.max_retries} attempts: {str(e)}'
                        })
                    return files_batch
                
                # Wait before retry
                await asyncio.sleep(self.rate_limiter.config.delay_between_requests * (2 ** attempt))

    async def parse_batch_response(self, analysis: str, files_batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Parse AI response and update file metadata with enhanced debug information"""
        logger = logging.getLogger('java_analysis.debug_batch_analyzer')
        
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
                        # Extract JSON from section
                        json_start = matching_section.find('{')
                        json_end = matching_section.rfind('}') + 1
                        
                        if json_start != -1 and json_end > json_start:
                            json_str = matching_section[json_start:json_end]
                            ai_analysis = json.loads(json_str)
                            
                            # Update file metadata with enhanced analysis
                            file_meta.update({
                                'ai_analysis': ai_analysis,
                                'analysis_status': 'completed',
                                'debug_analysis_timestamp': asyncio.get_event_loop().time()
                            })
                            
                            logger.info(f"Successfully analyzed {file_path}")
                        else:
                            file_meta.update({
                                'analysis_status': 'failed',
                                'error': 'Could not extract JSON from AI response'
                            })
                            logger.warning(f"Could not extract JSON for {file_path}")
                            
                    except json.JSONDecodeError as e:
                        file_meta.update({
                            'analysis_status': 'failed',
                            'error': f'JSON parsing error: {str(e)}'
                        })
                        logger.error(f"JSON parsing error for {file_path}: {str(e)}")
                else:
                    file_meta.update({
                        'analysis_status': 'failed',
                        'error': 'No matching section found in AI response'
                    })
                    logger.warning(f"No matching section found for {file_path}")
            
            return files_batch
            
        except Exception as e:
            logger.error(f"Error parsing batch response: {str(e)}")
            # Mark all files as failed
            for file_meta in files_batch:
                file_meta.update({
                    'analysis_status': 'failed',
                    'error': f'Response parsing error: {str(e)}'
                })
            return files_batch

    async def analyze_files(self, files_metadata: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze files in batches with enhanced debug processing"""
        logger = logging.getLogger('java_analysis.debug_batch_analyzer')
        
        # Prioritize files
        prioritized_files = self.prioritize_files(files_metadata)
        logger.info(f"Prioritized {len(prioritized_files)} files for analysis")
        
        # Process in batches
        analyzed_files = []
        for i in range(0, len(prioritized_files), self.max_files_per_batch):
            batch = prioritized_files[i:i + self.max_files_per_batch]
            logger.info(f"Processing batch {i//self.max_files_per_batch + 1}/{(len(prioritized_files) + self.max_files_per_batch - 1)//self.max_files_per_batch}")
            
            analyzed_batch = await self.analyze_files_batch(batch)
            analyzed_files.extend(analyzed_batch)
            
            # Add remaining files that weren't prioritized
            if i + self.max_files_per_batch >= len(prioritized_files):
                remaining_files = [f for f in files_metadata if f not in analyzed_files]
                analyzed_files.extend(remaining_files)
        
        return analyzed_files

async def process_codebase_debug():
    """Main function for debug mode processing"""
    logger = logging.getLogger('java_analysis.debug_main')
    logger.info("Starting debug mode codebase processing")
    
    try:
        # Initialize debug file processor
        file_processor = DebugFileProcessor()
        
        # Process files
        logger.info("Processing files with debug file processor")
        files_metadata = file_processor.process_files()
        
        if not files_metadata:
            logger.warning("No files to process")
            return
        
        logger.info(f"Processed {len(files_metadata)} files")
        
        # Initialize batch analyzer
        batch_analyzer = DebugBatchAIAnalyzer()
        
        # Analyze files
        logger.info("Starting AI analysis of files")
        analyzed_metadata = await batch_analyzer.analyze_files(files_metadata)
        
        # Save metadata
        metadata_file = os.path.join(file_processor.output_dir, 'debug_metadata.json')
        file_processor.save_metadata(analyzed_metadata, metadata_file)
        logger.info(f"Saved debug metadata to {metadata_file}")
        
        # Store in ChromaDB with enhanced information
        logger.info("Storing enhanced metadata in ChromaDB")
        for file_meta in analyzed_metadata:
            if file_meta.get('analysis_status') == 'completed':
                file_path = file_meta.get('file_path', '')
                content = file_meta.get('content', '')
                ai_analysis = file_meta.get('ai_analysis', {})
                
                # Add debug information to ChromaDB
                if 'pom_analysis' in file_meta:
                    ai_analysis['pom_analysis'] = file_meta['pom_analysis']
                
                batch_analyzer.chromadb_connector.store_enhanced_metadata(
                    file_path, content, ai_analysis
                )
        
        logger.info("Debug mode processing completed successfully")
        
    except Exception as e:
        logger.error(f"Error in debug mode processing: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(process_codebase_debug()) 