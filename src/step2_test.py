import asyncio
import os
import json
import logging
import re
from pathlib import Path
from typing import Dict, Any, List, Set
from dotenv import load_dotenv
from logger_config import setup_logging
from openai import AsyncOpenAI
from rate_limiter import RateLimiter, RateLimitConfig

logger = logging.getLogger('java_analysis.step2_test')

class RequirementsProcessor:
    def __init__(self):
        load_dotenv()
        self.metadata = None
        self.processed_files: Set[str] = set()
        self.output_dir = os.getenv('OUTPUT_DIR', './output')
        self.md_dir = Path(self.output_dir) / "requirements"
        self.md_dir.mkdir(parents=True, exist_ok=True)
        
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
        
        # Initialize OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.error("OPENAI_API_KEY environment variable is not set")
            raise ValueError("OPENAI_API_KEY environment variable is not set")
            
        self.model_name = os.getenv('OPENAI_MODEL_NAME', 'gpt-4-turbo-preview')
        self.client = AsyncOpenAI(api_key=api_key)

    def load_metadata(self) -> None:
        """Load metadata from JSON file"""
        metadata_file = os.path.join(self.output_dir, 'metadata.json')
        if not os.path.exists(metadata_file):
            raise FileNotFoundError(f"Metadata file not found: {metadata_file}")
            
        with open(metadata_file, 'r') as f:
            self.metadata = json.load(f)
        logger.info(f"Loaded metadata with {len(self.metadata)} entries")

    def get_important_files(self) -> List[Dict[str, Any]]:
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
            for item in self.metadata:
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
        
        # Create prompt for AI analysis
        content = file_metadata.get('content', '')
        if len(content) > 1500:  # Reduced from 2000
            content = content[:1500] + "... [truncated]"
            
        prompt = f"""Analyze this file and provide requirements documentation:

File: {file_path}
Type: {file_metadata.get('file_type', 'Unknown')}
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
                
                response = await self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": "You are a requirements analysis expert. Provide concise but comprehensive analysis."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    max_tokens=1000  # Reduced from 1500
                )
                
                analysis = response.choices[0].message.content
                
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
        important_files = self.get_important_files()
        
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
        processor.load_metadata()
        
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