import os
from typing import Dict, Any, List
from openai import AsyncOpenAI
from dotenv import load_dotenv
import logging
from rate_limiter import RateLimiter, RateLimitConfig

logger = logging.getLogger('java_analysis.ai_analyzer')

class AIAnalyzer:
    """Handles AI-based analysis of source code files"""
    
    def __init__(self):
        load_dotenv()
        logger.debug("Environment variables loaded")
        
        # Get OpenAI settings from environment variables
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.error("OPENAI_API_KEY environment variable is not set")
            raise ValueError("OPENAI_API_KEY environment variable is not set")
            
        self.model_name = os.getenv('OPENAI_MODEL_NAME', 'gpt-4-turbo-preview')
        logger.info(f"Using OpenAI model: {self.model_name}")
        
        # Initialize rate limiter
        rate_config = RateLimitConfig(
            requests_per_minute=15,  # Conservative rate limiting
            requests_per_hour=800,
            delay_between_requests=4.0,  # 4 seconds between requests
            exponential_backoff_base=2.0,
            max_retries=5
        )
        self.rate_limiter = RateLimiter(rate_config)
        
        # Initialize AsyncOpenAI client
        self.client = AsyncOpenAI(api_key=api_key)

    def create_file_prompt(self, file_type: str, content: str) -> str:
        """Create an appropriate prompt based on file type"""
        logger.debug(f"Creating prompt for file type: {file_type}")
        
        # Limit content length to reduce token usage
        if len(content) > 2000:
            content = content[:2000] + "... [truncated]"
            
        base_prompt = f"""Analyze this {file_type} and extract the following information:
1. Main purpose and functionality
2. Key components (classes, methods, endpoints, etc.)
3. Data structures and relationships
4. Business rules and validation logic
5. Dependencies and external interactions

File content:
{content}

Please provide the analysis in JSON format with the following structure:
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
}}"""
        return base_prompt

    async def analyze_file(self, file_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single file using AI with rate limiting"""
        logger.info(f"Analyzing file: {file_metadata.get('file_path', 'unknown')}")
        
        # Wait for rate limiter before making API call
        await self.rate_limiter.wait_if_needed()
        
        prompt = self.create_file_prompt(
            file_metadata['file_type'],
            file_metadata['content']
        )

        for attempt in range(self.rate_limiter.config.max_retries):
            try:
                logger.debug("Sending request to OpenAI API")
                response = await self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": "You are a code analysis expert."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    max_tokens=1500  # Reduced from default
                )
                
                # Extract and parse the JSON response
                analysis = response.choices[0].message.content
                logger.debug("Successfully received analysis from OpenAI")
                
                # Record successful request
                self.rate_limiter.record_request()
                
                # Update the metadata with AI analysis
                file_metadata.update({
                    'ai_analysis': analysis,
                    'analysis_status': 'completed'
                })
                logger.info(f"Analysis completed for file: {file_metadata.get('file_path', 'unknown')}")
                
                # Log rate limiting stats
                stats = self.rate_limiter.get_stats()
                logger.debug(f"Rate limit stats: {stats['requests_last_minute']}/min, {stats['requests_last_hour']}/hour")
                
                break
                
            except Exception as e:
                logger.error(f"Analysis failed (attempt {attempt + 1}): {str(e)}")
                self.rate_limiter.record_failure()
                
                if attempt == self.rate_limiter.config.max_retries - 1:
                    file_metadata.update({
                        'analysis_status': 'failed',
                        'error': str(e)
                    })
        
        return file_metadata

    async def analyze_files(self, metadata_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze multiple files using AI with rate limiting"""
        logger.info(f"Starting analysis of {len(metadata_list)} files")
        analyzed_metadata = []
        
        for idx, metadata in enumerate(metadata_list, 1):
            logger.info(f"Processing file {idx}/{len(metadata_list)}")
            analyzed = await self.analyze_file(metadata)
            analyzed_metadata.append(analyzed)
        
        logger.info("Completed analysis of all files")
        return analyzed_metadata 