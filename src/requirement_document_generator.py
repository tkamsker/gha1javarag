import json
import logging
from pathlib import Path
from typing import Dict, List
import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv

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

    def load_clusters(self, clusters_path: str) -> Dict:
        """Load clustering results from JSON file."""
        with open(clusters_path, 'r') as f:
            return json.load(f)

    def load_embeddings(self, embeddings_path: str) -> Dict:
        """Load embeddings from JSON file."""
        with open(embeddings_path, 'r') as f:
            return json.load(f)

    def generate_requirement(self, cluster_info: Dict) -> Dict:
        """Generate a structured requirement for a cluster using GPT-4."""
        prompt = self._prepare_requirement_prompt(cluster_info)
        try:
            logger.info(f"Using model: {self.model} for requirement generation.")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": """You are a requirements engineer. 
                    Generate requirements in the following format:
                    | Feature ID | Description | Source Class |
                    |------------|-------------|--------------|
                    Use FR-{category}-{number} format for Feature IDs."""},
                    {"role": "user", "content": prompt}
                ]
            )
            return self._parse_requirement_response(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Error generating requirement: {str(e)}")
            raise

    def _prepare_requirement_prompt(self, cluster_info: Dict) -> str:
        """Prepare the prompt for requirement generation."""
        return f"""
        Analyze the following cluster of code artifacts and generate a functional requirement:
        
        Cluster ID: {cluster_info['cluster_id']}
        Artifacts: {', '.join(cluster_info['artifacts'])}
        
        Generate a requirement that:
        1. Describes the functionality
        2. Identifies the source class
        3. Uses a clear, concise description
        4. Follows the specified table format
        """

    def _parse_requirement_response(self, response: str) -> Dict:
        """Parse the LLM response into a structured requirement."""
        # Extract the table row from the response
        lines = response.strip().split('\n')
        for line in lines:
            if '|' in line and 'FR-' in line:
                parts = [p.strip() for p in line.split('|') if p.strip()]
                if len(parts) >= 3:
                    return {
                        'feature_id': parts[0],
                        'description': parts[1],
                        'source_class': parts[2]
                    }
        return None

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
            requirement = self.generate_requirement(cluster_info)
            if requirement:
                self.requirements.append(requirement)

        # Generate document sections
        self._generate_functional_requirements(output_path)
        self._generate_traceability_matrix(output_path)

    def _generate_functional_requirements(self, output_path: str) -> None:
        """Generate the functional requirements section."""
        output_file = Path(output_path) / "functional_requirements.md"
        
        content = """# Functional Requirements

| Feature ID | Description | Source Class |
|------------|-------------|--------------|
"""
        for req in self.requirements:
            content += f"| {req['feature_id']} | {req['description']} | {req['source_class']} |\n"

        with open(output_file, 'w') as f:
            f.write(content)
        logger.info(f"Functional requirements saved to {output_file}")

    def _generate_traceability_matrix(self, output_path: str) -> None:
        """Generate the traceability matrix."""
        output_file = Path(output_path) / "traceability_matrix.csv"
        
        # Create DataFrame
        df = pd.DataFrame(self.requirements)
        df['Type'] = 'Functional'  # Add requirement type
        
        # Save as CSV
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