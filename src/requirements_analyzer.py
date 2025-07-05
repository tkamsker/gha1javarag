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
        self.java_source_dir = Path(os.getenv('JAVA_SOURCE_DIR', './infra/cuco')) # Default to a sensible path
        
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
                    'purpose': None if 'ai_analysis' not in comp else comp['ai_analysis'].get('purpose', '')
                })

                if 'ai_analysis' in comp:
                    # Extract features
                    if 'purpose' in comp['ai_analysis']:
                        analysis['features'].add(comp['ai_analysis']['purpose'])

                    # Extract data structures
                    if 'data_structures' in comp['ai_analysis']:
                        for struct in comp['ai_analysis']['data_structures']:
                            analysis['data_structures'].append({
                                'name': struct.get('name', 'Unknown'),
                                'fields': struct.get('fields', []),
                                'relationships': struct.get('relationships', [])
                            })

                    # Extract methods/functions
                    if 'components' in comp['ai_analysis']:
                        for method in comp['ai_analysis']['components']:
                            analysis['methods'].append({
                                'name': method.get('name', 'Unknown'),
                                'description': method.get('description', ''),
                                'parameters': method.get('parameters', []),
                                'returns': method.get('returns', '')
                            })

                    # Extract dependencies
                    if 'dependencies' in comp['ai_analysis']:
                        analysis['dependencies'].update(comp['ai_analysis']['dependencies'])

                    # Extract business rules
                    if 'business_rules' in comp['ai_analysis']:
                        analysis['business_rules'].extend(comp['ai_analysis']['business_rules'])

            logger.debug(f"Completed analysis of {layer_name} layer")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing {layer_name} layer: {str(e)}")
            raise
    
    def _get_unique_filepath(self, base_path: Path) -> Path:
        """Generates a unique filepath by appending a number if the file already exists."""
        if not base_path.exists():
            return base_path
        
        stem = base_path.stem
        suffix = base_path.suffix
        parent = base_path.parent
        
        counter = 1
        while True:
            new_name = f"{stem}-{counter}{suffix}"
            new_path = parent / new_name
            if not new_path.exists():
                return new_path
            counter += 1

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
            # Create base output directory for documentation
            base_doc_dir = Path(self.output_dir) / "documentation"
            base_doc_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate timestamp for this documentation set
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            all_analyses = [] # To collect all individual file analyses for the index
            
            for item in metadata_list:
                file_path_str = item.get('file_path')
                if not file_path_str:
                    logger.warning(f"Skipping item with no file_path: {item}")
                    continue
                
                try:
                    original_file_path = Path(file_path_str)
                    
                    # Determine relative path from JAVA_SOURCE_DIR
                    relative_path = original_file_path.relative_to(self.java_source_dir)
                    
                    # Construct output directory path mirroring source structure
                    output_sub_dir = base_doc_dir / relative_path.parent
                    output_sub_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Base filename for the requirement document
                    # Use the original file stem and add .md extension
                    base_filename = f"{original_file_path.stem}.md"
                    
                    # Construct the full base path for the new document
                    base_output_file_path = output_sub_dir / base_filename
                    
                    # Get a unique file path to prevent overwriting
                    unique_output_file_path = self._get_unique_filepath(base_output_file_path)
                    
                    # Generate documentation for this single file
                    # For now, we'll use a simplified analysis for individual files
                    # This part needs to be refined based on how detailed individual file docs should be
                    
                    # Create a dummy analysis for the single file for now
                    # In a real scenario, you'd call a method to analyze this single file's metadata
                    # and format it into a document.
                    
                    # For demonstration, let's just put the AI analysis directly if available
                    file_analysis_content = ""
                    if 'ai_analysis' in item and isinstance(item['ai_analysis'], dict):
                        file_analysis_content = json.dumps(item['ai_analysis'], indent=2)
                    elif 'ai_analysis' in item:
                        file_analysis_content = str(item['ai_analysis'])
                    else:
                        file_analysis_content = "No AI analysis available for this file."
                    
                    doc_content = f"# Requirements for {original_file_path.name}\n\n"
                    doc_content += f"## Original Path: {file_path_str}\n\n"
                    doc_content += f"## File Type: {item.get('file_type', 'Unknown')}\n\n"
                    doc_content += f"## AI Analysis\n\n```json\n{file_analysis_content}\n```\n"
                    
                    with open(unique_output_file_path, 'w') as f:
                        f.write(doc_content)
                    logger.info(f"Generated documentation for {file_path_str}: {unique_output_file_path}")
                    
                    # Add this file's info to all_analyses for the index document
                    all_analyses.append({
                        'name': original_file_path.name,
                        'path': str(unique_output_file_path.relative_to(base_doc_dir)),
                        'original_path': file_path_str,
                        'file_type': item.get('file_type', 'Unknown'),
                        'purpose': item.get('ai_analysis', {}).get('purpose', 'N/A')
                    })
                    
                except Exception as e:
                    logger.error(f"Error processing file {file_path_str}: {str(e)}")
                    # Continue to next file even if one fails
            
            # Generate and save index document
            # The index document generation needs to be adapted to the new structure
            # For now, a simplified index will be generated
            index_content = self.generate_new_index_document(all_analyses, timestamp)
            with open(base_doc_dir / f"index_{timestamp}.md", 'w') as f:
                f.write(index_content)
            logger.info("Generated main index document")
            
        except Exception as e:
            logger.error(f"Error during requirements analysis: {str(e)}")
            raise
            
    def generate_new_index_document(self, analyses: List[Dict[str, Any]], timestamp: str) -> str:
        """Generate a new index document for file-based requirements"""
        doc = "# Application Requirements Documentation Index\n\n"
        doc += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        doc += "## Documented Files\n\n"
        for analysis_item in analyses:
            doc += f"- [{analysis_item['name']}]({analysis_item['path']})\n"
            doc += f"  - Original Path: {analysis_item['original_path']}\n"
            doc += f"  - File Type: {analysis_item['file_type']}\n"
            doc += f"  - Purpose: {analysis_item['purpose']}\n"
        
        return doc 