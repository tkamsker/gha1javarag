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

logger = logging.getLogger('java_analysis.step2')

class RequirementsProcessor:
    def __init__(self):
        load_dotenv()
        self.metadata = None
        self.processed_files: Set[str] = set()
        self.output_dir = os.getenv('OUTPUT_DIR', './output')
        self.md_dir = Path(self.output_dir) / "requirements"
        self.md_dir.mkdir(parents=True, exist_ok=True)
        
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

    def find_landing_page(self) -> Dict[str, Any]:
        """Find the landing page (index.jsp or home.jsp)"""
        landing_page = None
        for item in self.metadata:
            file_path = item.get('file_path', '').lower()
            if file_path.endswith('index.jsp') or file_path.endswith('home.jsp'):
                landing_page = item
                break
        return landing_page

    def extract_references(self, content: str) -> List[str]:
        """Extract file and function references from content"""
        # Look for common patterns in JSP/HTML files
        patterns = [
            r'include\s+file=["\']([^"\']+)["\']',  # JSP includes
            r'href=["\']([^"\']+)["\']',  # Links
            r'src=["\']([^"\']+)["\']',  # Script sources
            r'action=["\']([^"\']+)["\']',  # Form actions
            r'@include\s+([^\s]+)',  # JSP directives
            r'jsp:include\s+page=["\']([^"\']+)["\']',  # JSP tags
            r'function\s+([a-zA-Z0-9_]+)\s*\('  # Function calls
        ]
        
        references = set()
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                ref = match.group(1)
                # Clean up the reference
                ref = ref.split('?')[0]  # Remove query parameters
                ref = ref.split('#')[0]  # Remove anchors
                if ref:
                    references.add(ref)
        
        return list(references)

    async def analyze_file(self, file_metadata: Dict[str, Any]) -> None:
        """Analyze a single file and generate requirements documentation"""
        file_path = file_metadata.get('file_path', '')
        if file_path in self.processed_files:
            return

        logger.info(f"Analyzing file: {file_path}")
        
        try:
            # Create prompt for AI analysis
            prompt = f"""We have a requirement, please explain in detail:
            File: {file_path}
            Type: {file_metadata.get('file_type', 'Unknown')}
            Content: {file_metadata.get('content', '')}
            
            Please provide a detailed analysis of the requirements this file implements.
            Include:
            1. Purpose and functionality
            2. User interactions
            3. Data handling
            4. Business rules
            5. Dependencies and relationships
            """
            
            # Get AI analysis
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a requirements analysis expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            
            analysis = response.choices[0].message.content
            
            # Create markdown file
            md_filename = f"{Path(file_path).stem}.md"
            md_path = self.md_dir / md_filename
            
            with open(md_path, 'w') as f:
                f.write(f"# Requirements Analysis: {file_path}\n\n")
                f.write(analysis)
            
            self.processed_files.add(file_path)
            logger.info(f"Generated requirements document: {md_path}")
            
            # Extract and process references
            references = self.extract_references(file_metadata.get('content', ''))
            for ref in references:
                # Find referenced file in metadata
                for item in self.metadata:
                    if item.get('file_path', '').endswith(ref):
                        await self.analyze_file(item)
                        break
            
        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {str(e)}")

    async def process_remaining_files(self) -> None:
        """Process any remaining files that weren't referenced"""
        for item in self.metadata:
            if item.get('file_path') not in self.processed_files:
                await self.analyze_file(item)

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
    logger = setup_logging(level=logging.DEBUG)
    logger.info("Starting requirements generation process")
    
    try:
        processor = RequirementsProcessor()
        processor.load_metadata()
        
        # Start with landing page
        landing_page = processor.find_landing_page()
        if landing_page:
            logger.info(f"Found landing page: {landing_page.get('file_path')}")
            await processor.analyze_file(landing_page)
        else:
            logger.warning("No landing page found, starting with first file")
            if processor.metadata:
                await processor.analyze_file(processor.metadata[0])
        
        # Process remaining files
        await processor.process_remaining_files()
        
        # Generate index
        processor.generate_index()
        
        logger.info("Requirements generation completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during requirements generation: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(generate_requirements()) 