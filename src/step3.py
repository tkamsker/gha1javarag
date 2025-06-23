import os
import json
import re
from pathlib import Path
from typing import Dict, List, Set
import markdown
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from ai_providers import create_ai_provider
from datetime import datetime

# Load environment variables
load_dotenv()

class RequirementsProcessor:
    def __init__(self):
        self.web_files: List[str] = []
        self.other_files: List[str] = []
        self.processed_content: Dict[str, dict] = {}
        self.output_dir = os.getenv("OUTPUT_DIR", "./output")
        self.requirements_dir = os.path.join(self.output_dir, "requirements")
        self.requirements_file = os.path.join(self.output_dir, "modern_requirements.md")
        
        # Initialize AI provider using the same pattern as main.py
        self.ai_provider = create_ai_provider()
        print(f"Using {self.ai_provider.get_provider_name()} provider with model: {self.ai_provider.get_model_name()}")
        
    def load_index(self, index_file: str) -> None:
        """Load and parse the step2_index.md file"""
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Parse markdown to find file references
        html = markdown.markdown(content)
        soup = BeautifulSoup(html, 'html.parser')
        
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.endswith('.md'):
                # Skip XML-derived files
                if 'xml' in href.lower():
                    continue
                    
                # Prioritize web/ directory files
                if 'web/' in href:
                    self.web_files.append(href)
                else:
                    self.other_files.append(href)
    
    def process_markdown_file(self, file_path: str) -> dict:
        """Process a single markdown file and extract requirements"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Convert markdown to HTML for better parsing
        html = markdown.markdown(content)
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract sections
        sections = {}
        current_section = None
        current_content = []
        
        for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'ol']):
            if element.name in ['h1', 'h2', 'h3']:
                if current_section:
                    sections[current_section] = '\n'.join(current_content)
                current_section = element.get_text().strip()
                current_content = []
            else:
                current_content.append(element.get_text().strip())
                
        if current_section:
            sections[current_section] = '\n'.join(current_content)
            
        return sections
    
    async def modernize_requirements(self, content: dict) -> dict:
        """Use AI to modernize requirements for cloud architecture"""
        prompt = f"""
        Convert these Java/JSP requirements into modern cloud architecture requirements using React and Node.js.
        Focus on:
        1. Microservices architecture
        2. React frontend components
        3. Node.js backend services
        4. Cloud-native features
        5. Modern security practices
        
        Original requirements:
        {json.dumps(content, indent=2)}
        
        Provide a structured response with:
        1. Modern Architecture Overview
        2. Frontend Components (React)
        3. Backend Services (Node.js)
        4. API Endpoints
        5. Data Models
        6. Security Considerations
        """
        
        try:
            analysis = await self.ai_provider.create_chat_completion(
                messages=[
                    {"role": "system", "content": "You are an expert in modern cloud architecture and application modernization."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return json.loads(analysis)
        except Exception as e:
            print(f"Error modernizing requirements: {str(e)}")
            return content
    
    async def generate_requirements_document(self) -> None:
        """Generate the final requirements document"""
        with open(self.requirements_file, 'w', encoding='utf-8') as f:
            f.write("# Modern Cloud Architecture Requirements\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Process web files first
            f.write("## Web Application Components\n\n")
            for file in self.web_files:
                if file in self.processed_content:
                    content = self.processed_content[file]
                    modernized = await self.modernize_requirements(content)
                    
                    f.write(f"### {os.path.basename(file)}\n\n")
                    for section, content in modernized.items():
                        f.write(f"#### {section}\n\n")
                        f.write(f"{content}\n\n")
            
            # Process other files
            f.write("## Additional Components\n\n")
            for file in self.other_files:
                if file in self.processed_content:
                    content = self.processed_content[file]
                    modernized = await self.modernize_requirements(content)
                    
                    f.write(f"### {os.path.basename(file)}\n\n")
                    for section, content in modernized.items():
                        f.write(f"#### {section}\n\n")
                        f.write(f"{content}\n\n")
    
    async def process_all_files(self) -> None:
        """Process all markdown files and generate requirements"""
        # Process web files first
        for file in self.web_files:
            full_path = os.path.join(self.requirements_dir, file)
            if os.path.exists(full_path):
                self.processed_content[file] = self.process_markdown_file(full_path)
        
        # Process other files
        for file in self.other_files:
            full_path = os.path.join(self.requirements_dir, file)
            if os.path.exists(full_path):
                self.processed_content[file] = self.process_markdown_file(full_path)
        
        # Generate final requirements document
        await self.generate_requirements_document()

async def main():
    processor = RequirementsProcessor()
    
    # Load the index file
    index_file = os.path.join(processor.requirements_dir, "step2_index.md")
    if not os.path.exists(index_file):
        print(f"Error: Index file not found at {index_file}")
        return
        
    processor.load_index(index_file)
    await processor.process_all_files()
    
    print(f"Requirements document generated at: {processor.requirements_file}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 