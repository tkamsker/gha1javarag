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

class DebugRequirementsProcessor:
    def __init__(self):
        self.web_files: List[str] = []
        self.other_files: List[str] = []
        self.processed_content: Dict[str, dict] = {}
        self.output_dir = os.getenv("OUTPUT_DIR", "./output")
        self.requirements_dir = os.path.join(self.output_dir, "requirements")
        self.requirements_file = os.path.join(self.output_dir, "modern_requirements_debug.md")
        
        # Debug mode configuration
        self.debug_file = os.getenv('DEBUGFILE')
        self.debug_mode = bool(self.debug_file and os.path.exists(self.debug_file))
        
        # Initialize AI provider using the same pattern as main.py
        self.ai_provider = create_ai_provider()
        print(f"Using {self.ai_provider.get_provider_name()} provider with model: {self.ai_provider.get_model_name()}")
        print(f"Debug mode: {'enabled' if self.debug_mode else 'disabled'}")
        
    def load_index(self, index_file: str) -> None:
        """Load and parse the step2 debug index file"""
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
        """Process a single markdown file and extract requirements with debug enhancements"""
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
        """Use AI to modernize requirements for cloud architecture with debug enhancements"""
        # Enhanced prompt for debug mode
        prompt = f"""
        Convert these Java/JSP requirements into modern cloud architecture requirements using React and Node.js.
        
        File: {file_path}
        Debug Mode: {'Enabled' if self.debug_mode else 'Disabled'}
        
        Focus on:
        1. Microservices architecture
        2. React frontend components
        3. Node.js backend services
        4. Cloud-native features
        5. Modern security practices
        6. Debug and monitoring considerations
        7. Performance optimization
        8. Scalability patterns
        
        Original requirements:
        {json.dumps(content, indent=2)}
        
        Provide a structured response with:
        1. Modern Architecture Overview
        2. Frontend Components (React)
        3. Backend Services (Node.js)
        4. API Endpoints
        5. Data Models
        6. Security Considerations
        7. Debug and Monitoring
        8. Performance Optimization
        9. Deployment Strategy
        10. Testing Strategy
        """
        
        try:
            analysis = await self.ai_provider.create_chat_completion(
                messages=[
                    {"role": "system", "content": "You are an expert in modern cloud architecture, application modernization, and debugging enterprise applications. Provide comprehensive analysis with focus on maintainability and observability."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2500
            )
            
            # Try to parse as JSON first
            try:
                return json.loads(analysis)
            except json.JSONDecodeError:
                # If JSON parsing fails, create a structured response from the text
                print(f"Warning: AI response is not valid JSON, creating structured response from text")
                return {
                    "Modern Architecture Overview": "Generated from AI analysis",
                    "Frontend Components (React)": "Generated from AI analysis", 
                    "Backend Services (Node.js)": "Generated from AI analysis",
                    "API Endpoints": "Generated from AI analysis",
                    "Data Models": "Generated from AI analysis",
                    "Security Considerations": "Generated from AI analysis",
                    "Debug and Monitoring": "Generated from AI analysis",
                    "Performance Optimization": "Generated from AI analysis",
                    "Deployment Strategy": "Generated from AI analysis",
                    "Testing Strategy": "Generated from AI analysis",
                    "Raw AI Response": analysis
                }
                
        except Exception as e:
            print(f"Error modernizing requirements: {str(e)}")
            # Return original content as fallback
            return {
                "Modern Architecture Overview": "Error occurred during modernization",
                "Frontend Components (React)": "Error occurred during modernization",
                "Backend Services (Node.js)": "Error occurred during modernization", 
                "API Endpoints": "Error occurred during modernization",
                "Data Models": "Error occurred during modernization",
                "Security Considerations": "Error occurred during modernization",
                "Debug and Monitoring": "Error occurred during modernization",
                "Performance Optimization": "Error occurred during modernization",
                "Deployment Strategy": "Error occurred during modernization",
                "Testing Strategy": "Error occurred during modernization",
                "Original Content": content
            }
    
    async def generate_requirements_document(self) -> None:
        """Generate the final requirements document with debug information"""
        with open(self.requirements_file, 'w', encoding='utf-8') as f:
            f.write("# Modern Cloud Architecture Requirements (Debug Mode)\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Add debug information
            if self.debug_mode:
                f.write(f"**Debug Mode:** Enabled\n")
                f.write(f"**Debug File:** {self.debug_file}\n\n")
            
            f.write("## Summary\n\n")
            f.write(f"- **Total Files Processed:** {len(self.processed_content)}\n")
            f.write(f"- **Web Files:** {len(self.web_files)}\n")
            f.write(f"- **Other Files:** {len(self.other_files)}\n\n")
            
            # Process web files first
            f.write("## Web Application Components\n\n")
            for file in self.web_files:
                if file in self.processed_content:
                    content = self.processed_content[file]
                    modernized = await self.modernize_requirements(content, file)
                    
                    f.write(f"### {os.path.basename(file)}\n\n")
                    f.write(f"**Source File:** `{file}`\n\n")
                    
                    for section, content in modernized.items():
                        if section != "Raw AI Response":  # Skip raw response in main document
                            f.write(f"#### {section}\n\n")
                            f.write(f"{content}\n\n")
            
            # Process other files
            f.write("## Additional Components\n\n")
            for file in self.other_files:
                if file in self.processed_content:
                    content = self.processed_content[file]
                    modernized = await self.modernize_requirements(content, file)
                    
                    f.write(f"### {os.path.basename(file)}\n\n")
                    f.write(f"**Source File:** `{file}`\n\n")
                    
                    for section, content in modernized.items():
                        if section != "Raw AI Response":  # Skip raw response in main document
                            f.write(f"#### {section}\n\n")
                            f.write(f"{content}\n\n")
            
            # Add debug insights section
            if self.debug_mode:
                f.write("## Debug Insights\n\n")
                f.write("### Processing Summary\n\n")
                f.write(f"- **Debug Mode:** Enabled\n")
                f.write(f"- **Debug File:** {self.debug_file}\n")
                f.write(f"- **Files with Enhanced Metadata:** {len([f for f in self.processed_content.keys() if 'pom_analysis' in f])}\n\n")
                
                f.write("### Recommendations for Debug Mode\n\n")
                f.write("1. **Enhanced Monitoring:** Implement comprehensive logging and monitoring\n")
                f.write("2. **Debug Tools:** Use debugging tools and profilers\n")
                f.write("3. **Error Handling:** Implement robust error handling and recovery\n")
                f.write("4. **Testing:** Focus on unit and integration testing\n")
                f.write("5. **Documentation:** Maintain detailed documentation for debugging\n\n")
    
    async def process_all_files(self) -> None:
        """Process all markdown files and generate requirements with debug enhancements"""
        # Process web files first
        for file in self.web_files:
            full_path = os.path.join(self.requirements_dir, file)
            if os.path.exists(full_path):
                self.processed_content[file] = self.process_markdown_file(full_path)
                print(f"Processed web file: {file}")
        
        # Process other files
        for file in self.other_files:
            full_path = os.path.join(self.requirements_dir, file)
            if os.path.exists(full_path):
                self.processed_content[file] = self.process_markdown_file(full_path)
                print(f"Processed other file: {file}")
        
        # Generate final requirements document
        await self.generate_requirements_document()

async def main():
    processor = DebugRequirementsProcessor()
    
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
    
    print(f"Debug requirements document generated at: {processor.requirements_file}")

if __name__ == "__main__":
    asyncio.run(main()) 