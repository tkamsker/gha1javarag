import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class RequirementDocumentGenerator:
    def __init__(self, api_key: str, model: str = "gpt-4.1"):
        """Initialize the document generator with OpenAI API key and model."""
        self.client = OpenAI(
            api_key=api_key,
            base_url=os.getenv('OPENAI_API_BASE')
        )
        self.model = model
        self.requirements: List[Dict] = []
        self.data_models: List[Dict] = []
        self.non_functional_requirements: List[Dict] = []

    def load_clusters(self, clusters_path: str) -> Dict:
        """Load clustering results from JSON file."""
        with open(clusters_path, 'r') as f:
            return json.load(f)

    def load_embeddings(self, embeddings_path: str) -> Dict:
        """Load embeddings from JSON file."""
        with open(embeddings_path, 'r') as f:
            return json.load(f)

    def extract_data_model(self, cluster_info: Dict) -> Optional[Dict]:
        """Extract data model information from code artifacts."""
        prompt = self._prepare_data_model_prompt(cluster_info)
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": """You are a data model analyst. 
                    Extract data model information in the following format:
                    {
                        "entity_name": "string",
                        "attributes": [
                            {"name": "string", "type": "string", "description": "string"}
                        ],
                        "relationships": [
                            {"entity": "string", "type": "string", "description": "string"}
                        ]
                    }
                    Return ONLY the JSON object, no additional text."""},
                    {"role": "user", "content": prompt}
                ]
            )
            try:
                return json.loads(response.choices[0].message.content.strip())
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse data model JSON: {response.choices[0].message.content}")
                return None
        except Exception as e:
            logger.error(f"Error extracting data model: {str(e)}")
            return None

    def _prepare_data_model_prompt(self, cluster_info: Dict) -> str:
        """Prepare the prompt for data model extraction."""
        return f"""
        Analyze the following cluster of code artifacts and extract data model information:
        
        Cluster ID: {cluster_info['cluster_id']}
        Artifacts: {', '.join(cluster_info['artifacts'])}
        
        Extract:
        1. Entity names and their attributes
        2. Data types and descriptions
        3. Relationships between entities
        4. Primary and foreign keys
        """

    def generate_requirement(self, cluster_info: Dict) -> Dict:
        """Generate a structured requirement for a cluster using GPT-4."""
        prompt = self._prepare_requirement_prompt(cluster_info)
        try:
            logger.info(f"Using model: {self.model} for requirement generation.")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": """You are a requirements engineer. 
                    Generate detailed requirements in the following format:
                    {
                        "feature_id": "FR-{category}-{number}",
                        "title": "string",
                        "description": "string",
                        "source_class": "string",
                        "acceptance_criteria": [
                            "string"
                        ],
                        "dependencies": [
                            "string"
                        ],
                        "priority": "string"
                    }"""},
                    {"role": "user", "content": prompt}
                ]
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Error generating requirement: {str(e)}")
            raise

    def _prepare_requirement_prompt(self, cluster_info: Dict) -> str:
        """Prepare the prompt for requirement generation."""
        return f"""
        Analyze the following cluster of code artifacts and generate a detailed functional requirement:
        
        Cluster ID: {cluster_info['cluster_id']}
        Artifacts: {', '.join(cluster_info['artifacts'])}
        
        Generate a requirement that includes:
        1. Clear, concise title and description
        2. Specific acceptance criteria
        3. Dependencies on other requirements
        4. Priority level (High/Medium/Low)
        5. Source class and method references
        6. Technical constraints and assumptions
        """

    def generate_non_functional_requirements(self) -> None:
        """Generate non-functional requirements based on the system architecture."""
        prompt = """
        Based on the system's architecture and implementation, generate non-functional requirements covering:
        1. Performance requirements
        2. Security requirements
        3. Scalability requirements
        4. Maintainability requirements
        5. Usability requirements
        
        Format each requirement as:
        {
            "requirements": [
                {
                    "requirement_id": "NFR-{category}-{number}",
                    "category": "string",
                    "description": "string",
                    "rationale": "string",
                    "verification_method": "string"
                }
            ]
        }
        Return ONLY the JSON object, no additional text.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a requirements engineer specializing in non-functional requirements."},
                    {"role": "user", "content": prompt}
                ]
            )
            try:
                result = json.loads(response.choices[0].message.content.strip())
                self.non_functional_requirements = result.get('requirements', [])
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse non-functional requirements JSON: {response.choices[0].message.content}")
                self.non_functional_requirements = []
        except Exception as e:
            logger.error(f"Error generating non-functional requirements: {str(e)}")
            self.non_functional_requirements = []

    def generate_document(self, clusters_path: str, embeddings_path: str, output_path: str) -> None:
        """Generate the complete requirements document."""
        # Load data
        clusters = self.load_clusters(clusters_path)
        embeddings = self.load_embeddings(embeddings_path)

        # Generate requirements for each cluster
        for cluster_id, artifacts in clusters['clusters'].items():
            cluster_info = {
                'cluster_id': cluster_id,
                'artifacts': artifacts
            }
            
            # Generate functional requirement
            requirement = self.generate_requirement(cluster_info)
            if requirement:
                self.requirements.append(requirement)
            
            # Extract data model
            data_model = self.extract_data_model(cluster_info)
            if data_model:
                self.data_models.append(data_model)

        # Generate non-functional requirements
        self.generate_non_functional_requirements()

        # Generate document sections
        self._generate_functional_requirements(output_path)
        self._generate_non_functional_requirements(output_path)
        self._generate_data_model(output_path)
        self._generate_traceability_matrix(output_path)

    def _generate_functional_requirements(self, output_path: str) -> None:
        """Generate the functional requirements section."""
        output_file = Path(output_path) / "functional_requirements.md"
        
        content = """# Functional Requirements

## Overview
This section describes the functional requirements of the system, organized by feature categories.

"""
        # Group requirements by category
        categories = {}
        for req in self.requirements:
            category = req['feature_id'].split('-')[1]
            if category not in categories:
                categories[category] = []
            categories[category].append(req)

        # Generate content for each category
        for category, reqs in categories.items():
            content += f"\n### {category.upper()} Requirements\n\n"
            content += "| Feature ID | Title | Description | Priority |\n"
            content += "|------------|-------|-------------|----------|\n"
            for req in reqs:
                content += f"| {req['feature_id']} | {req['title']} | {req['description']} | {req['priority']} |\n"
            
            # Add detailed information for each requirement
            for req in reqs:
                content += f"\n#### {req['feature_id']}: {req['title']}\n\n"
                content += f"**Description:** {req['description']}\n\n"
                content += "**Acceptance Criteria:**\n"
                for criterion in req['acceptance_criteria']:
                    content += f"- {criterion}\n"
                content += "\n**Dependencies:**\n"
                for dep in req['dependencies']:
                    content += f"- {dep}\n"
                content += f"\n**Source:** {req['source_class']}\n\n"

        with open(output_file, 'w') as f:
            f.write(content)
        logger.info(f"Functional requirements saved to {output_file}")

    def _generate_non_functional_requirements(self, output_path: str) -> None:
        """Generate the non-functional requirements section."""
        output_file = Path(output_path) / "non_functional_requirements.md"
        
        content = """# Non-Functional Requirements

## Overview
This section describes the non-functional requirements of the system, including performance, security, scalability, maintainability, and usability requirements.

"""
        # Group requirements by category
        categories = {}
        for req in self.non_functional_requirements:
            if req['category'] not in categories:
                categories[req['category']] = []
            categories[req['category']].append(req)

        # Generate content for each category
        for category, reqs in categories.items():
            content += f"\n### {category.upper()} Requirements\n\n"
            for req in reqs:
                content += f"#### {req['requirement_id']}\n\n"
                content += f"**Description:** {req['description']}\n\n"
                content += f"**Rationale:** {req['rationale']}\n\n"
                content += f"**Verification Method:** {req['verification_method']}\n\n"

        with open(output_file, 'w') as f:
            f.write(content)
        logger.info(f"Non-functional requirements saved to {output_file}")

    def _generate_data_model(self, output_path: str) -> None:
        """Generate the data model section."""
        output_file = Path(output_path) / "data_model.md"
        
        content = """# Data Model

## Overview
This section describes the data model of the system, including entities, attributes, and relationships.

"""
        if not self.data_models:
            content += "\nNo data models were extracted from the code artifacts.\n"
        else:
            # Generate content for each entity
            for model in self.data_models:
                if not isinstance(model, dict) or 'entity_name' not in model:
                    continue
                    
                content += f"\n### {model['entity_name']}\n\n"
                content += "**Attributes:**\n\n"
                content += "| Name | Type | Description |\n"
                content += "|------|------|-------------|\n"
                for attr in model.get('attributes', []):
                    content += f"| {attr.get('name', '')} | {attr.get('type', '')} | {attr.get('description', '')} |\n"
                
                if model.get('relationships'):
                    content += "\n**Relationships:**\n\n"
                    content += "| Entity | Type | Description |\n"
                    content += "|--------|------|-------------|\n"
                    for rel in model['relationships']:
                        content += f"| {rel.get('entity', '')} | {rel.get('type', '')} | {rel.get('description', '')} |\n"

        with open(output_file, 'w') as f:
            f.write(content)
        logger.info(f"Data model saved to {output_file}")

    def _generate_traceability_matrix(self, output_path: str) -> None:
        """Generate the traceability matrix."""
        output_file = Path(output_path) / "traceability_matrix.csv"
        
        # Create DataFrame with all requirements
        all_requirements = []
        
        # Add functional requirements
        for req in self.requirements:
            all_requirements.append({
                'requirement_id': req['feature_id'],
                'type': 'Functional',
                'title': req['title'],
                'description': req['description'],
                'source': req['source_class'],
                'priority': req['priority']
            })
        
        # Add non-functional requirements
        for req in self.non_functional_requirements:
            all_requirements.append({
                'requirement_id': req['requirement_id'],
                'type': 'Non-Functional',
                'title': req['category'],
                'description': req['description'],
                'source': 'System Architecture',
                'priority': 'N/A'
            })
        
        # Create and save DataFrame
        df = pd.DataFrame(all_requirements)
        df.to_csv(output_file, index=False)
        logger.info(f"Traceability matrix saved to {output_file}")

def main():
    """Main execution function."""
    try:
        # Initialize generator
        generator = RequirementDocumentGenerator(os.getenv('OPENAI_API_KEY'))
        
        # Set paths
        output_dir = Path("output")
        clusters_path = output_dir / "clusters.json"
        embeddings_path = output_dir / "embeddings.json"
        
        # Generate document
        generator.generate_document(
            str(clusters_path),
            str(embeddings_path),
            str(output_dir)
        )
        
        logger.info("Requirements document generation completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in document generation: {str(e)}")
        raise

if __name__ == "__main__":
    main() 