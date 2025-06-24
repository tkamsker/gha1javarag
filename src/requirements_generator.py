import json
import logging
from pathlib import Path
from typing import Dict, List, Any
import os
from datetime import datetime
from openai import AsyncOpenAI
from dotenv import load_dotenv

logger = logging.getLogger('java_analysis.requirements_generator')

class RequirementsGenerator:
    """Generates structured requirements documentation from metadata"""
    
    def __init__(self, metadata_path: str, output_dir: str):
        load_dotenv()
        self.metadata_path = metadata_path
        self.output_dir = output_dir
        self.metadata = None
        
        # Initialize OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.error("OPENAI_API_KEY environment variable is not set")
            raise ValueError("OPENAI_API_KEY environment variable is not set")
            
        self.model_name = os.getenv('OPENAI_MODEL_NAME', 'gpt-4-turbo-preview')
        self.client = AsyncOpenAI(api_key=api_key)
        
    async def enrich_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich metadata with AI analysis"""
        try:
            prompt = f"""Analyze this component and extract detailed requirements:
            File: {metadata.get('file_path', 'Unknown')}
            Type: {metadata.get('file_type', 'Unknown')}
            Content: {metadata.get('content', '')}
            
            Please provide a structured analysis in JSON format with:
            1. Purpose and main functionality
            2. Key components and their roles
            3. Data structures and relationships
            4. Business rules and validation logic
            5. Dependencies and external interactions
            6. Security considerations
            7. Performance requirements
            """
            
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a requirements analysis expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            
            analysis = response.choices[0].message.content
            metadata['ai_analysis'] = analysis
            return metadata
            
        except Exception as e:
            logger.error(f"Failed to enrich metadata: {str(e)}")
            return metadata
            
    def load_metadata(self) -> None:
        """Load metadata from JSON file"""
        logger.info(f"Loading metadata from {self.metadata_path}")
        try:
            with open(self.metadata_path, 'r') as f:
                self.metadata = json.load(f)
            logger.debug(f"Successfully loaded metadata with {len(self.metadata)} entries")
        except Exception as e:
            logger.error(f"Failed to load metadata: {str(e)}")
            raise
            
    def group_by_layer(self) -> Dict[str, List[Dict]]:
        """Group components by logical layers"""
        layers = {
            'database': [],
            'backend': [],
            'presentation': [],
            'configuration': [],
            'security': [],
            'integration': []
        }
        
        for item in self.metadata:
            file_path = item.get('file_path', '')
            file_type = item.get('file_type', '').lower()
            
            # Enhanced categorization
            if file_type in ['sql', 'database']:
                layers['database'].append(item)
            elif file_type in ['java', 'class', 'servlet']:
                if 'security' in file_path.lower() or 'auth' in file_path.lower():
                    layers['security'].append(item)
                elif 'api' in file_path.lower() or 'integration' in file_path.lower():
                    layers['integration'].append(item)
                else:
                    layers['backend'].append(item)
            elif file_type in ['jsp', 'html', 'javascript', 'css']:
                layers['presentation'].append(item)
            elif file_type in ['xml', 'properties', 'config']:
                layers['configuration'].append(item)
            else:
                logger.warning(f"Uncategorized file type: {file_type} for {file_path}")
                
        return layers
        
    def generate_layer_documentation(self, layer_name: str, components: List[Dict]) -> str:
        """Generate documentation for a specific layer"""
        doc = f"# Requirements Document: {layer_name.title()} Layer\n\n"
        
        # 1. Overview
        doc += "## 1. Overview\n"
        doc += f"This section describes the {layer_name} layer components and their functionality.\n\n"
        
        # 2. Components
        doc += "## 2. Components\n"
        for comp in components:
            doc += f"### {comp.get('file_path', 'Unknown')}\n"
            if 'ai_analysis' in comp:
                analysis = json.loads(comp['ai_analysis'])
                doc += f"- **Purpose:** {analysis.get('purpose', 'N/A')}\n"
                doc += f"- **Main Functionality:** {analysis.get('main_functionality', 'N/A')}\n\n"
        doc += "\n"
        
        # 3. Functionality
        doc += "## 3. Functionality\n"
        
        # Main Features
        doc += "### Main Features\n"
        features = set()
        for comp in components:
            if 'ai_analysis' in comp:
                analysis = json.loads(comp['ai_analysis'])
                if 'key_components' in analysis:
                    for component in analysis['key_components']:
                        features.add(f"{component.get('name', 'Unknown')}: {component.get('role', '')}")
        for feature in features:
            doc += f"- {feature}\n"
        doc += "\n"
        
        # Data Structures
        doc += "### Data Structures\n"
        for comp in components:
            if 'ai_analysis' in comp:
                analysis = json.loads(comp['ai_analysis'])
                if 'data_structures' in analysis:
                    for struct in analysis['data_structures']:
                        doc += f"- {struct.get('name', 'Unknown')}:\n"
                        if 'fields' in struct:
                            doc += "  - Fields: " + ", ".join(struct['fields']) + "\n"
                        if 'relationships' in struct:
                            doc += "  - Relationships: " + ", ".join(struct['relationships']) + "\n"
        doc += "\n"
        
        # Business Rules
        doc += "### Business Rules\n"
        for comp in components:
            if 'ai_analysis' in comp:
                analysis = json.loads(comp['ai_analysis'])
                if 'business_rules' in analysis:
                    for rule in analysis['business_rules']:
                        doc += f"- {rule.get('description', '')}\n"
        doc += "\n"
        
        # Security Considerations
        doc += "### Security Considerations\n"
        for comp in components:
            if 'ai_analysis' in comp:
                analysis = json.loads(comp['ai_analysis'])
                if 'security_considerations' in analysis:
                    for security in analysis['security_considerations']:
                        doc += f"- {security}\n"
        doc += "\n"
        
        # Performance Requirements
        doc += "### Performance Requirements\n"
        for comp in components:
            if 'ai_analysis' in comp:
                analysis = json.loads(comp['ai_analysis'])
                if 'performance_requirements' in analysis:
                    for perf in analysis['performance_requirements']:
                        doc += f"- {perf}\n"
        doc += "\n"
        
        # 4. Dependencies
        doc += "## 4. Dependencies\n"
        deps = set()
        for comp in components:
            if 'ai_analysis' in comp:
                analysis = json.loads(comp['ai_analysis'])
                if 'dependencies' in analysis:
                    deps.update(analysis['dependencies'])
        for dep in deps:
            doc += f"- {dep}\n"
        doc += "\n"
        
        return doc
        
    async def generate_documentation(self) -> None:
        """Generate full requirements documentation"""
        if not self.metadata:
            self.load_metadata()
            
        # Create output directory if it doesn't exist
        doc_dir = Path(self.output_dir) / "documentation"
        doc_dir.mkdir(parents=True, exist_ok=True)
        
        # Enrich metadata with AI analysis
        logger.info("Enriching metadata with AI analysis...")
        for item in self.metadata:
            item = await self.enrich_metadata(item)
        
        # Group components by layer
        layers = self.group_by_layer()
        
        # Generate documentation for each layer
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Generate individual layer documents
        for layer_name, components in layers.items():
            if components:  # Only generate for layers with components
                doc_content = self.generate_layer_documentation(layer_name, components)
                output_file = doc_dir / f"{layer_name}_requirements_{timestamp}.md"
                
                with open(output_file, 'w') as f:
                    f.write(doc_content)
                logger.info(f"Generated documentation for {layer_name} layer: {output_file}")
                
        # Generate main index document
        index_content = "# Application Requirements Documentation\n\n"
        index_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        index_content += "## Layer Documentation\n\n"
        
        for layer_name, components in layers.items():
            if components:
                index_content += f"- [{layer_name.title()} Layer](./{layer_name}_requirements_{timestamp}.md)\n"
                index_content += f"  - Components: {len(components)}\n"
                if any('ai_analysis' in comp for comp in components):
                    index_content += "  - AI Analysis: Included\n"
                
        with open(doc_dir / f"index_{timestamp}.md", 'w') as f:
            f.write(index_content)
        logger.info("Generated main index document") 