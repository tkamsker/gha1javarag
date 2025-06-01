from openai import OpenAI
from typing import List, Dict, Any
import logging
import yaml
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RequirementGenerator:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        logger.info("Initialized requirement generator")

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            raise

    def generate_requirement(self, artifact: Dict[str, Any]) -> str:
        """Generate a requirement for a single artifact."""
        try:
            prompt = self._create_prompt(artifact)
            
            response = self.client.chat.completions.create(
                model=self.config['openai']['model'],
                messages=[{"role": "user", "content": prompt}],
                temperature=self.config['openai']['temperature'],
                max_tokens=self.config['openai']['max_tokens']
            )
            
            requirement = response.choices[0].message.content.strip()
            logger.info(f"Generated requirement for {artifact['id']}")
            return requirement
        except Exception as e:
            logger.error(f"Error generating requirement: {str(e)}")
            raise

    def generate_cluster_requirements(self, artifacts: List[Dict[str, Any]]) -> Dict[int, str]:
        """Generate requirements for a cluster of artifacts."""
        try:
            cluster_requirements = {}
            
            # Group artifacts by cluster
            clusters = {}
            for artifact in artifacts:
                cluster_id = artifact['cluster']
                if cluster_id not in clusters:
                    clusters[cluster_id] = []
                clusters[cluster_id].append(artifact)
            
            # Generate requirements for each cluster
            for cluster_id, cluster_artifacts in clusters.items():
                prompt = self._create_cluster_prompt(cluster_artifacts)
                
                response = self.client.chat.completions.create(
                    model=self.config['openai']['model'],
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.config['openai']['temperature'],
                    max_tokens=self.config['openai']['max_tokens']
                )
                
                cluster_requirements[cluster_id] = response.choices[0].message.content.strip()
                logger.info(f"Generated requirement for cluster {cluster_id}")
            
            return cluster_requirements
        except Exception as e:
            logger.error(f"Error generating cluster requirements: {str(e)}")
            raise

    def _create_prompt(self, artifact: Dict[str, Any]) -> str:
        """Create a prompt for generating a requirement for a single artifact."""
        return f"""Given the following Java code artifact, write a clear and concise requirement that this code fulfills:

Class: {artifact['class']}
Method: {artifact['name']}
Definition: {artifact['definition']}
Arguments: {artifact['args']}
Documentation: {artifact['doc']}

Write a requirement that describes what this code is responsible for and what it should accomplish.
The requirement should be specific, measurable, and testable.

Requirement:"""

    def _create_cluster_prompt(self, artifacts: List[Dict[str, Any]]) -> str:
        """Create a prompt for generating a requirement for a cluster of artifacts."""
        artifacts_text = "\n\n".join([
            f"Artifact {i+1}:\n"
            f"Class: {a['class']}\n"
            f"Method: {a['name']}\n"
            f"Definition: {a['definition']}\n"
            f"Documentation: {a['doc']}"
            for i, a in enumerate(artifacts)
        ])
        
        return f"""Given the following cluster of related Java code artifacts, write a high-level requirement that this group of code fulfills:

{artifacts_text}

Write a requirement that describes the overall purpose and responsibility of this group of related code artifacts.
The requirement should be specific, measurable, and testable.

Requirement:""" 