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
import asyncio

# Load environment variables
load_dotenv()

class TestRequirementsProcessor:
    def __init__(self):
        self.web_files: List[str] = []
        self.other_files: List[str] = []
        self.processed_content: Dict[str, dict] = {}
        self.output_dir = os.getenv("OUTPUT_DIR", "./output")
        self.requirements_dir = os.path.join(self.output_dir, "requirements")
        self.requirements_file = os.path.join(self.output_dir, "modern_requirements_test.md")
        
        # Initialize AI provider using the same pattern as main.py
        self.ai_provider = create_ai_provider()
        print(f"Using {self.ai_provider.get_provider_name()} provider with model: {self.ai_provider.get_model_name()}")
        print("Running in TEST mode with conservative settings")
        
    def load_index(self, index_file: str) -> None:
        """Load and parse the step2 index file"""
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
    
    async def modernize_requirements(self, content: dict, file_path: str = "") -> dict:
        """Use AI to modernize requirements for cloud architecture with test mode optimizations"""
        # Simplified prompt for test mode
        prompt = f"""
        Convert these Java/JSP requirements into modern cloud architecture requirements using React and Node.js.
        
        File: {file_path}
        Mode: TEST (use simplified analysis)
        
        Focus on:
        1. Basic microservices architecture
        2. React frontend components
        3. Node.js backend services
        4. Simple API endpoints
        5. Basic data models
        
        Original requirements:
        {json.dumps(content, indent=2)}
        
        Provide a structured response with:
        1. Modern Architecture Overview
        2. Frontend Components (React)
        3. Backend Services (Node.js)
        4. API Endpoints
        5. Data Models
        """
        
        try:
            analysis = await self.ai_provider.create_chat_completion(
                messages=[
                    {"role": "system", "content": "You are an expert in modern cloud architecture. Provide simplified analysis for test mode."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1500  # Reduced for test mode
            )
            
            # Try to parse as JSON first
            try:
                return json.loads(analysis)
            except json.JSONDecodeError:
                # If JSON parsing fails, create a structured response from the text
                print(f"Warning: AI response is not valid JSON, creating structured response from text")
                return {
                    "Modern Architecture Overview": "Generated from AI analysis (test mode)",
                    "Frontend Components (React)": "Generated from AI analysis (test mode)", 
                    "Backend Services (Node.js)": "Generated from AI analysis (test mode)",
                    "API Endpoints": "Generated from AI analysis (test mode)",
                    "Data Models": "Generated from AI analysis (test mode)",
                    "Raw AI Response": analysis
                }
                
        except Exception as e:
            print(f"Error modernizing requirements: {str(e)}")
            # Return original content as fallback
            return {
                "Modern Architecture Overview": "Error occurred during modernization (test mode)",
                "Frontend Components (React)": "Error occurred during modernization (test mode)",
                "Backend Services (Node.js)": "Error occurred during modernization (test mode)", 
                "API Endpoints": "Error occurred during modernization (test mode)",
                "Data Models": "Error occurred during modernization (test mode)",
                "Original Content": content
            }
    
    async def generate_requirements_document(self) -> None:
        """Generate the final requirements document with test mode information"""
        with open(self.requirements_file, 'w', encoding='utf-8') as f:
            f.write("# Modern Cloud Architecture Requirements (Test Mode)\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("**Mode:** TEST (simplified analysis)\n\n")
            
            f.write("## Summary\n\n")
            f.write(f"- **Total Files Processed:** {len(self.processed_content)}\n")
            f.write(f"- **Web Files:** {len(self.web_files)}\n")
            f.write(f"- **Other Files:** {len(self.other_files)}\n\n")
            
            # Process web files first (limit to first 2 for test mode)
            f.write("## Web Application Components\n\n")
            for i, file in enumerate(self.web_files[:2]):  # Limit to 2 files in test mode
                if file in self.processed_content:
                    content = self.processed_content[file]
                    modernized = await self.modernize_requirements(content, file)
                    
                    f.write(f"### {os.path.basename(file)}\n\n")
                    f.write(f"**Source File:** `{file}`\n\n")
                    
                    for section, content in modernized.items():
                        if section != "Raw AI Response":  # Skip raw response in main document
                            f.write(f"#### {section}\n\n")
                            f.write(f"{content}\n\n")
            
            # Process other files (limit to first 2 for test mode)
            f.write("## Additional Components\n\n")
            for i, file in enumerate(self.other_files[:2]):  # Limit to 2 files in test mode
                if file in self.processed_content:
                    content = self.processed_content[file]
                    modernized = await self.modernize_requirements(content, file)
                    
                    f.write(f"### {os.path.basename(file)}\n\n")
                    f.write(f"**Source File:** `{file}`\n\n")
                    
                    for section, content in modernized.items():
                        if section != "Raw AI Response":  # Skip raw response in main document
                            f.write(f"#### {section}\n\n")
                            f.write(f"{content}\n\n")
            
            # Add test mode information
            f.write("## Test Mode Information\n\n")
            f.write("This analysis was performed in TEST mode with the following optimizations:\n\n")
            f.write("- **Simplified Analysis:** Reduced complexity for faster processing\n")
            f.write("- **Limited Files:** Processed only first 2 files from each category\n")
            f.write("- **Reduced Tokens:** Lower token limits for cost efficiency\n")
            f.write("- **Conservative Settings:** Optimized for testing and development\n\n")
    
    async def process_all_files(self) -> None:
        """Process all markdown files and generate requirements with test mode limits"""
        # Process web files first (limit to first 2 for test mode)
        for i, file in enumerate(self.web_files[:2]):
            full_path = os.path.join(self.requirements_dir, file)
            if os.path.exists(full_path):
                self.processed_content[file] = self.process_markdown_file(full_path)
                print(f"Processed web file {i+1}/2: {file}")
        
        # Process other files (limit to first 2 for test mode)
        for i, file in enumerate(self.other_files[:2]):
            full_path = os.path.join(self.requirements_dir, file)
            if os.path.exists(full_path):
                self.processed_content[file] = self.process_markdown_file(full_path)
                print(f"Processed other file {i+1}/2: {file}")
        
        # Generate final requirements document
        await self.generate_requirements_document()

async def main():
    processor = TestRequirementsProcessor()
    
    # Load the index file (try debug index first, then fallback to regular index)
    debug_index_file = os.path.join(processor.requirements_dir, "step2_debug_index.md")
    regular_index_file = os.path.join(processor.requirements_dir, "step2_index.md")
    
    if os.path.exists(debug_index_file):
        print(f"Loading debug index file: {debug_index_file}")
        processor.load_index(debug_index_file)
    elif os.path.exists(regular_index_file):
        print(f"Loading regular index file: {regular_index_file}")
        processor.load_index(regular_index_file)
    else:
        print(f"Error: No index file found at {debug_index_file} or {regular_index_file}")
        return
        
    await processor.process_all_files()
    
    print(f"Test requirements document generated at: {processor.requirements_file}")

if __name__ == "__main__":
    asyncio.run(main()) 