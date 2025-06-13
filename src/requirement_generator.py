from typing import Dict, List
import logging
from pathlib import Path
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_API_BASE')
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RequirementGenerator:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        """Initialize the requirement generator with OpenAI API key and model."""
        self.model = model
        self.client = client

    def generate_requirements(self, clusters: Dict[int, List[str]], code_artifacts: Dict) -> List[str]:
        """Generate requirements for each cluster."""
        requirements = []
        for cluster_id, cluster_members in clusters.items():
            cluster_info = self._prepare_cluster_info(cluster_members, code_artifacts)
            # Ensure cluster_info is a dictionary
            if isinstance(cluster_info, str):
                cluster_info = {"cluster": cluster_info}
            requirement = self._generate_requirement(cluster_info)
            requirements.append(requirement)
        return requirements

    def _prepare_cluster_info(self, artifact_ids: List[str], code_artifacts: Dict) -> str:
        """Prepare information about the cluster for the LLM."""
        cluster_info = []
        
        for artifact_id in artifact_ids:
            if artifact_id.startswith("class:"):
                class_name = artifact_id[6:]
                if class_name in code_artifacts["classes"]:
                    class_info = code_artifacts["classes"][class_name]
                    cluster_info.append(f"""
                    Class: {class_name}
                    Documentation: {class_info['documentation']}
                    Methods: {', '.join(m['name'] for m in class_info['methods'])}
                    """)
            
            elif artifact_id.startswith("method:"):
                method_key = artifact_id[7:]
                if method_key in code_artifacts["methods"]:
                    method_info = code_artifacts["methods"][method_key]
                    cluster_info.append(f"""
                    Method: {method_info['name']}
                    Return Type: {method_info['return_type']}
                    Parameters: {method_info['parameters']}
                    Documentation: {method_info['documentation']}
                    """)

        return "\n".join(cluster_info)

    def _prepare_cluster_prompt(self, cluster_info: Dict) -> str:
        """Format cluster information into a prompt for the OpenAI API."""
        prompt = "Based on the following code artifacts, generate a requirement:\n\n"
        for key, value in cluster_info.items():
            prompt += f"{key}: {value}\n"
        return prompt

    def _generate_requirement(self, cluster_info: Dict) -> str:
        """Generate a requirement for a cluster using GPT-4."""
        prompt = self._prepare_cluster_prompt(cluster_info)
        try:
            logger.info(f"Using model: {self.model} for requirement generation.")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a requirements engineer."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating requirement with GPT-4: {str(e)}")
            raise

    def save_requirements(self, requirements: List[Dict], output_path: str) -> None:
        """Save generated requirements to a JSON file."""
        try:
            output_file = Path(output_path)
            with open(output_file, 'w') as f:
                json.dump(requirements, f, indent=2)
            logger.info(f"Requirements saved to {output_path}")
        except Exception as e:
            logger.error(f"Error saving requirements: {str(e)}")
            raise

    def load_requirements(self, input_path: str) -> List[Dict]:
        """Load requirements from a JSON file."""
        try:
            input_file = Path(input_path)
            if input_file.exists():
                with open(input_file, 'r') as f:
                    requirements = json.load(f)
                logger.info(f"Requirements loaded from {input_path}")
                return requirements
            return []
        except Exception as e:
            logger.error(f"Error loading requirements: {str(e)}")
            raise 