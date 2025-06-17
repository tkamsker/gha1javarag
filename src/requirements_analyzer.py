import json
import logging
from pathlib import Path
from typing import Dict, List, Any
import os
from datetime import datetime
from chromadb_connector import ChromaDBConnector
from dotenv import load_dotenv

logger = logging.getLogger('java_analysis.requirements_analyzer')

class RequirementsAnalyzer:
    """Analyzes metadata and generates detailed requirements documentation"""
    
    def __init__(self, output_dir: str):
        load_dotenv()
        logger.debug("Environment variables loaded")
        
        self.output_dir = output_dir
        self.chroma_connector = ChromaDBConnector()
        
    def analyze_layer(self, layer_name: str, components: List[Dict]) -> Dict[str, Any]:
        """Analyze a specific layer and generate structured information"""
        logger.info(f"Analyzing {layer_name} layer")
        
        analysis = {
            'name': layer_name,
            'overview': f"Analysis of {layer_name} layer components and functionality",
            'components': [],
            'features': set(),
            'data_structures': [],
            'methods': [],
            'dependencies': set(),
            'business_rules': []
        }
        
        try:
            for comp in components:
                # Add component information
                analysis['components'].append({
                    'path': comp.get('file_path', 'Unknown'),
                    'type': comp.get('file_type', 'Unknown'),
                    'purpose': comp.get('purpose', '')
                })
                
                # Extract features
                if 'purpose' in comp:
                    analysis['features'].add(comp['purpose'])
                
                # Extract data structures
                if 'data_structures' in comp:
                    for struct in comp['data_structures']:
                        analysis['data_structures'].append({
                            'name': struct.get('name', 'Unknown'),
                            'fields': struct.get('fields', []),
                            'relationships': struct.get('relationships', [])
                        })
                
                # Extract methods/functions
                if 'components' in comp:
                    for method in comp['components']:
                        analysis['methods'].append({
                            'name': method.get('name', 'Unknown'),
                            'description': method.get('description', ''),
                            'parameters': method.get('parameters', []),
                            'returns': method.get('returns', '')
                        })
                
                # Extract dependencies
                if 'dependencies' in comp:
                    analysis['dependencies'].update(comp['dependencies'])
                
                # Extract business rules
                if 'business_rules' in comp:
                    analysis['business_rules'].extend(comp['business_rules'])
            
            logger.debug(f"Completed analysis of {layer_name} layer")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing {layer_name} layer: {str(e)}")
            raise
    
    def generate_layer_documentation(self, analysis: Dict[str, Any]) -> str:
        """Generate markdown documentation for a layer based on analysis"""
        doc = f"# Requirements Document: {analysis['name'].title()} Layer\n\n"
        
        # 1. Overview
        doc += "## 1. Overview\n"
        doc += f"{analysis['overview']}\n\n"
        
        # 2. Components
        doc += "## 2. Components\n"
        for comp in analysis['components']:
            doc += f"- {comp['path']} ({comp['type']})\n"
            if comp['purpose']:
                doc += f"  - Purpose: {comp['purpose']}\n"
        doc += "\n"
        
        # 3. Functionality
        doc += "## 3. Functionality\n"
        
        # Main Features
        doc += "### Main Features\n"
        for feature in analysis['features']:
            doc += f"- {feature}\n"
        doc += "\n"
        
        # Data Structures
        doc += "### Data Structures\n"
        for struct in analysis['data_structures']:
            doc += f"#### {struct['name']}\n"
            if struct['fields']:
                doc += "Fields:\n"
                for field in struct['fields']:
                    doc += f"- {field}\n"
            if struct['relationships']:
                doc += "Relationships:\n"
                for rel in struct['relationships']:
                    doc += f"- {rel}\n"
        doc += "\n"
        
        # Methods/Functions
        doc += "### Key Methods/Functions\n"
        for method in analysis['methods']:
            doc += f"#### {method['name']}\n"
            doc += f"Description: {method['description']}\n"
            if method['parameters']:
                doc += "Parameters:\n"
                for param in method['parameters']:
                    doc += f"- {param}\n"
            if method['returns']:
                doc += f"Returns: {method['returns']}\n"
        doc += "\n"
        
        # 4. Dependencies
        doc += "## 4. Dependencies\n"
        for dep in analysis['dependencies']:
            doc += f"- {dep}\n"
        doc += "\n"
        
        # 5. Business Rules
        doc += "## 5. Business Rules\n"
        for rule in analysis['business_rules']:
            doc += f"- {rule.get('description', '')}\n"
            if 'validation' in rule:
                doc += f"  - Validation: {rule['validation']}\n"
        doc += "\n"
        
        return doc
    
    def generate_index_document(self, analyses: List[Dict[str, Any]], timestamp: str) -> str:
        """Generate the main index document"""
        doc = "# Application Requirements Documentation\n\n"
        doc += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Summary
        doc += "## Summary\n\n"
        total_components = sum(len(analysis['components']) for analysis in analyses)
        total_features = sum(len(analysis['features']) for analysis in analyses)
        doc += f"- Total Components: {total_components}\n"
        doc += f"- Total Features: {total_features}\n"
        doc += f"- Analyzed Layers: {len(analyses)}\n\n"
        
        # Layer Documentation
        doc += "## Layer Documentation\n\n"
        for analysis in analyses:
            doc += f"### {analysis['name'].title()} Layer\n"
            doc += f"- Components: {len(analysis['components'])}\n"
            doc += f"- Features: {len(analysis['features'])}\n"
            doc += f"- Business Rules: {len(analysis['business_rules'])}\n"
            doc += f"- [Detailed Documentation](./{analysis['name']}_requirements_{timestamp}.md)\n\n"
        
        return doc
    
    def analyze_and_generate(self, metadata_list: List[Dict[str, Any]]) -> None:
        """Analyze metadata and generate comprehensive requirements documentation"""
        logger.info("Starting requirements analysis and documentation generation")
        
        try:
            # Create output directory
            doc_dir = Path(self.output_dir) / "documentation"
            doc_dir.mkdir(parents=True, exist_ok=True)
            
            # Group by layer
            layers = {
                'database': [],
                'backend': [],
                'presentation': [],
                'configuration': []
            }
            
            for item in metadata_list:
                file_type = item.get('file_type', '').lower()
                if 'sql' in file_type or 'database' in file_type:
                    layers['database'].append(item)
                elif 'java' in file_type or 'class' in file_type:
                    layers['backend'].append(item)
                elif any(x in file_type for x in ['jsp', 'html', 'js', 'css']):
                    layers['presentation'].append(item)
                elif any(x in file_type for x in ['xml', 'properties', 'config']):
                    layers['configuration'].append(item)
            
            # Generate timestamp for this documentation set
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Analyze each layer and generate documentation
            analyses = []
            for layer_name, components in layers.items():
                if components:
                    # Analyze layer
                    analysis = self.analyze_layer(layer_name, components)
                    analyses.append(analysis)
                    
                    # Generate and save layer documentation
                    doc_content = self.generate_layer_documentation(analysis)
                    output_file = doc_dir / f"{layer_name}_requirements_{timestamp}.md"
                    with open(output_file, 'w') as f:
                        f.write(doc_content)
                    logger.info(f"Generated documentation for {layer_name} layer: {output_file}")
            
            # Generate and save index document
            index_content = self.generate_index_document(analyses, timestamp)
            with open(doc_dir / f"index_{timestamp}.md", 'w') as f:
                f.write(index_content)
            logger.info("Generated main index document")
            
        except Exception as e:
            logger.error(f"Error during requirements analysis: {str(e)}")
            raise 