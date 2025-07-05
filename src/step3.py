import os
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Any
import markdown
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from ai_providers import create_ai_provider
from datetime import datetime
import time

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
        
        # Define metadata categories for grouping
        self.metadata_categories = {
            'backend': {
                'keywords': ['service', 'controller', 'dao', 'repository', 'manager', 'handler'],
                'files': [],
                'requirements': []
            },
            'frontend': {
                'keywords': ['jsp', 'html', 'css', 'js', 'view', 'page', 'form', 'component'],
                'files': [],
                'requirements': []
            },
            'data_structures': {
                'keywords': ['entity', 'model', 'dto', 'vo', 'bean', 'class', 'interface'],
                'files': [],
                'requirements': []
            },
            'testing': {
                'keywords': ['test', 'spec', 'mock', 'stub', 'fixture'],
                'files': [],
                'requirements': []
            },
            'batch_processing': {
                'keywords': ['batch', 'job', 'scheduler', 'cron', 'task'],
                'files': [],
                'requirements': []
            },
            'operational': {
                'keywords': ['log', 'monitor', 'admin', 'ops', 'config', 'properties'],
                'files': [],
                'requirements': []
            }
        }
        
        # Initialize AI provider lazily (only when needed)
        self.ai_provider = None
        
    def _get_ai_provider(self):
        """Get AI provider, initializing it if needed"""
        if self.ai_provider is None:
            try:
                self.ai_provider = create_ai_provider()
                print(f"Using {self.ai_provider.get_provider_name()} provider with model: {self.ai_provider.get_model_name()}")
            except Exception as e:
                print(f"Warning: Could not initialize AI provider: {str(e)}")
                print("Will generate requirements without AI modernization")
                return None
        return self.ai_provider
        
    def categorize_file(self, file_path: str) -> str:
        """Categorize a file based on its path and content"""
        file_path_lower = file_path.lower()
        
        for category, config in self.metadata_categories.items():
            for keyword in config['keywords']:
                if keyword in file_path_lower:
                    return category
        
        return 'other'
    
    def load_index(self, index_file: str) -> None:
        """Load and parse the step2_index.md file with categorization"""
        if not os.path.exists(index_file):
            print(f"Warning: Index file not found at {index_file}")
            return
            
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
                
                # Categorize the file
                category = self.categorize_file(href)
                if category in self.metadata_categories:
                    self.metadata_categories[category]['files'].append(href)
                else:
                    self.other_files.append(href)
    
    def process_markdown_file(self, file_path: str) -> dict:
        """Process a single markdown file and extract requirements"""
        try:
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
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")
            return {"Error": f"Could not process file: {str(e)}"}
    
    def deduplicate_requirements(self, requirements_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate requirements based on content similarity"""
        unique_requirements = []
        seen_content = set()
        
        for req in requirements_list:
            # Create a normalized version of the requirement for comparison
            content_key = req.get('content', '').lower().strip()
            content_key = re.sub(r'\s+', ' ', content_key)  # Normalize whitespace
            
            if content_key and content_key not in seen_content:
                seen_content.add(content_key)
                unique_requirements.append(req)
        
        return unique_requirements
    
    async def modernize_requirements_by_category(self, category: str, requirements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Use AI to modernize requirements for a specific category"""
        if not requirements:
            return {}
        
        # Deduplicate requirements first
        unique_requirements = self.deduplicate_requirements(requirements)
        
        # Check if AI provider is available
        ai_provider = self._get_ai_provider()
        if ai_provider is None:
            # Fallback: create basic structure without AI
            return {
                "Modern Architecture Overview": f"Basic modernization for {category} (AI not available)",
                "Key Components": f"Components from {len(unique_requirements)} files in {category}",
                "Implementation Guidelines": "Review original requirements for implementation details",
                "Best Practices": "Follow modern development practices for the technology stack",
                "Technology Stack Recommendations": "Consider React/Node.js for modernization"
            }
        
        # Create category-specific prompt
        category_prompts = {
            'backend': """
                Convert these backend Java requirements into modern Node.js/Express backend requirements.
                Focus on:
                1. RESTful API design
                2. Service layer architecture
                3. Database integration (MongoDB/PostgreSQL)
                4. Authentication and authorization
                5. Error handling and validation
                6. Microservices patterns
            """,
            'frontend': """
                Convert these JSP/frontend requirements into modern React frontend requirements.
                Focus on:
                1. React component architecture
                2. State management (Redux/Context)
                3. Routing and navigation
                4. Form handling and validation
                5. API integration
                6. Responsive design
            """,
            'data_structures': """
                Convert these Java data structures into modern data models.
                Focus on:
                1. MongoDB schemas or PostgreSQL tables
                2. TypeScript interfaces
                3. Data validation schemas
                4. API request/response models
                5. Database relationships
            """,
            'testing': """
                Convert these testing requirements into modern testing approaches.
                Focus on:
                1. Unit testing (Jest/Mocha)
                2. Integration testing
                3. E2E testing (Cypress/Playwright)
                4. Test data management
                5. CI/CD testing pipelines
            """,
            'batch_processing': """
                Convert these batch processing requirements into modern cloud-native approaches.
                Focus on:
                1. Cloud functions (AWS Lambda/Azure Functions)
                2. Message queues (RabbitMQ/AWS SQS)
                3. Scheduled jobs (Cron jobs/Cloud Scheduler)
                4. Event-driven architecture
                5. Data processing pipelines
            """,
            'operational': """
                Convert these operational requirements into modern DevOps practices.
                Focus on:
                1. Containerization (Docker)
                2. Orchestration (Kubernetes)
                3. Monitoring and logging (Prometheus/ELK)
                4. CI/CD pipelines
                5. Infrastructure as Code
                6. Security best practices
            """
        }
        
        prompt = f"""
        {category_prompts.get(category, 'Convert these requirements into modern cloud architecture requirements.')}
        
        Original requirements for {category}:
        {json.dumps(unique_requirements, indent=2)}
        
        Provide a structured response with:
        1. Modern Architecture Overview
        2. Key Components
        3. Implementation Guidelines
        4. Best Practices
        5. Technology Stack Recommendations
        """
        
        try:
            analysis = await ai_provider.create_chat_completion(
                messages=[
                    {"role": "system", "content": f"You are an expert in modern {category} architecture and application modernization."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Try to parse as JSON first
            try:
                return json.loads(analysis)
            except json.JSONDecodeError:
                # If JSON parsing fails, create a structured response from the text
                print(f"Warning: AI response for {category} is not valid JSON, creating structured response from text")
                return {
                    "Modern Architecture Overview": f"Generated from AI analysis for {category}",
                    "Key Components": f"Generated from AI analysis for {category}",
                    "Implementation Guidelines": f"Generated from AI analysis for {category}",
                    "Best Practices": f"Generated from AI analysis for {category}",
                    "Technology Stack Recommendations": f"Generated from AI analysis for {category}",
                    "Raw AI Response": analysis
                }
                
        except Exception as e:
            print(f"Error modernizing {category} requirements: {str(e)}")
            return {
                "Modern Architecture Overview": f"Error occurred during {category} modernization",
                "Key Components": f"Error occurred during {category} modernization",
                "Implementation Guidelines": f"Error occurred during {category} modernization",
                "Best Practices": f"Error occurred during {category} modernization",
                "Technology Stack Recommendations": f"Error occurred during {category} modernization",
                "Original Content": unique_requirements
            }
    
    async def generate_requirements_document(self) -> None:
        """Generate the final requirements document organized by categories"""
        with open(self.requirements_file, 'w', encoding='utf-8') as f:
            f.write("# Modern Cloud Architecture Requirements\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## Executive Summary\n\n")
            f.write("This document provides modern cloud architecture requirements derived from legacy Java/JSP application analysis.\n\n")
            
            # Generate summary statistics
            total_files = sum(len(config['files']) for config in self.metadata_categories.values())
            f.write(f"**Total Files Analyzed:** {total_files}\n\n")
            
            for category, config in self.metadata_categories.items():
                if config['files']:
                    f.write(f"- **{category.title()}:** {len(config['files'])} files\n")
            
            f.write("\n---\n\n")
            
            # Process each category
            for category, config in self.metadata_categories.items():
                if not config['files']:
                    continue
                
                f.write(f"## {category.title()} Architecture\n\n")
                f.write(f"**Files in this category:** {len(config['files'])}\n\n")
                
                # Modernize requirements for this category
                modernized = await self.modernize_requirements_by_category(category, config['requirements'])
                
                for section, content in modernized.items():
                    if section != "Raw AI Response":  # Skip raw response in main document
                        f.write(f"### {section}\n\n")
                        f.write(f"{content}\n\n")
                
                f.write("---\n\n")
            
            # Add technology stack summary
            f.write("## Technology Stack Summary\n\n")
            f.write("### Recommended Modern Stack\n\n")
            f.write("- **Frontend:** React.js with TypeScript\n")
            f.write("- **Backend:** Node.js with Express.js\n")
            f.write("- **Database:** MongoDB or PostgreSQL\n")
            f.write("- **Authentication:** JWT with OAuth2\n")
            f.write("- **Containerization:** Docker\n")
            f.write("- **Orchestration:** Kubernetes\n")
            f.write("- **CI/CD:** GitHub Actions or GitLab CI\n")
            f.write("- **Monitoring:** Prometheus + Grafana\n")
            f.write("- **Logging:** ELK Stack\n")
            f.write("- **Testing:** Jest, Cypress\n")
            f.write("- **API Documentation:** Swagger/OpenAPI\n\n")
            
            f.write("### Migration Strategy\n\n")
            f.write("1. **Phase 1:** Set up modern development environment\n")
            f.write("2. **Phase 2:** Migrate data models and APIs\n")
            f.write("3. **Phase 3:** Develop new frontend components\n")
            f.write("4. **Phase 4:** Implement testing and CI/CD\n")
            f.write("5. **Phase 5:** Deploy to cloud infrastructure\n")
    
    async def process_all_files(self) -> None:
        """Process all markdown files and categorize requirements"""
        # Process files by category
        for category, config in self.metadata_categories.items():
            print(f"Processing {category} category...")
            
            for file in config['files']:
                full_path = os.path.join(self.requirements_dir, file)
                if os.path.exists(full_path):
                    content = self.process_markdown_file(full_path)
                    config['requirements'].append({
                        'file': file,
                        'content': content,
                        'category': category
                    })
        
        # Process other files
        for file in self.other_files:
            full_path = os.path.join(self.requirements_dir, file)
            if os.path.exists(full_path):
                content = self.process_markdown_file(full_path)
                # Add to appropriate category or create 'other' category
                if 'other' not in self.metadata_categories:
                    self.metadata_categories['other'] = {
                        'keywords': [],
                        'files': [],
                        'requirements': []
                    }
                self.metadata_categories['other']['requirements'].append({
                    'file': file,
                    'content': content,
                    'category': 'other'
                })
        
        # Generate final requirements document
        await self.generate_requirements_document()

async def main():
    processor = RequirementsProcessor()
    
    # Load the index file
    index_file = os.path.join(processor.requirements_dir, "step2_index.md")
    if not os.path.exists(index_file):
        print(f"Error: Index file not found at {index_file}")
        print("Please run step2.py first to generate the requirements index.")
        return
        
    processor.load_index(index_file)
    await processor.process_all_files()
    
    print(f"Modern requirements document generated at: {processor.requirements_file}")
    print("Document is organized by metadata categories to avoid duplication.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 