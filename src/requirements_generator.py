import json
import logging
from pathlib import Path
from typing import Dict, List, Any
import os
from datetime import datetime

logger = logging.getLogger('java_analysis.requirements_generator')

class RequirementsGenerator:
    """Generates structured requirements documentation from metadata"""
    
    def __init__(self, metadata_path: str, output_dir: str):
        self.metadata_path = metadata_path
        self.output_dir = output_dir
        self.metadata = None
        
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
            'configuration': []
        }
        
        for item in self.metadata:
            file_path = item.get('file_path', '')
            file_type = item.get('file_type', '').lower()
            
            # Categorize by file type
            if file_type in ['sql', 'database']:
                layers['database'].append(item)
            elif file_type in ['java', 'class', 'servlet']:
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
            doc += f"- {comp.get('file_path', 'Unknown')}\n"
        doc += "\n"
        
        # 3. Functionality
        doc += "## 3. Functionality\n"
        
        # Main Features
        doc += "### Main Features\n"
        features = set()
        for comp in components:
            if 'purpose' in comp:
                features.add(comp['purpose'])
        for feature in features:
            doc += f"- {feature}\n"
        doc += "\n"
        
        # Inputs/Outputs
        doc += "### Inputs/Outputs\n"
        for comp in components:
            if 'data_structures' in comp:
                for struct in comp['data_structures']:
                    doc += f"- {struct.get('name', 'Unknown')}:\n"
                    if 'fields' in struct:
                        doc += "  - Fields: " + ", ".join(struct['fields']) + "\n"
                    if 'relationships' in struct:
                        doc += "  - Relationships: " + ", ".join(struct['relationships']) + "\n"
        doc += "\n"
        
        # Key Methods/Functions
        doc += "### Key Methods/Functions\n"
        for comp in components:
            if 'components' in comp:
                for method in comp['components']:
                    doc += f"- {method.get('name', 'Unknown')}: {method.get('description', '')}\n"
        doc += "\n"
        
        # 4. Dependencies
        doc += "## 4. Dependencies\n"
        deps = set()
        for comp in components:
            if 'dependencies' in comp:
                deps.update(comp['dependencies'])
        for dep in deps:
            doc += f"- {dep}\n"
        doc += "\n"
        
        # 5. Notes
        doc += "## 5. Notes\n"
        for comp in components:
            if 'business_rules' in comp:
                for rule in comp['business_rules']:
                    doc += f"- {rule.get('description', '')}\n"
        doc += "\n"
        
        return doc
        
    def generate_documentation(self) -> None:
        """Generate full requirements documentation"""
        if not self.metadata:
            self.load_metadata()
            
        # Create output directory if it doesn't exist
        doc_dir = Path(self.output_dir) / "documentation"
        doc_dir.mkdir(parents=True, exist_ok=True)
        
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
                
        with open(doc_dir / f"index_{timestamp}.md", 'w') as f:
            f.write(index_content)
        logger.info("Generated main index document") 