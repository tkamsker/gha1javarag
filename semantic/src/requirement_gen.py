import logging
from typing import List, Dict, Any
from src.llm_provider import LLMProviderFactory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RequirementGenerator:
    def __init__(self):
        self.llm = LLMProviderFactory.create_provider()
        logger.info("Initialized RequirementGenerator")

    def _create_prompt(self, artifacts: List[Dict[str, Any]]) -> str:
        """Create a prompt for requirement generation based on artifacts."""
        prompt = "Given the following Java code artifacts, generate a comprehensive requirement that these artifacts fulfill:\n\n"
        
        for artifact in artifacts:
            prompt += f"Class: {artifact.get('class', 'N/A')}\n"
            prompt += f"Name: {artifact.get('name', 'N/A')}\n"
            prompt += f"Definition: {artifact.get('definition', 'N/A')}\n"
            prompt += f"Documentation: {artifact.get('document', 'N/A')}\n\n"
        
        prompt += "Requirement:"
        return prompt

    def generate_cluster_requirements(self, artifacts: List[Dict[str, Any]]) -> str:
        """Generate requirements for a cluster of artifacts."""
        try:
            prompt = self._create_prompt(artifacts)
            requirement = self.llm.generate_text(prompt)
            logger.info(f"Generated requirement for cluster with {len(artifacts)} artifacts")
            return requirement
        except Exception as e:
            logger.error(f"Error generating cluster requirement: {str(e)}")
            raise

    def generate_artifact_requirement(self, artifact: Dict[str, Any]) -> str:
        """Generate a requirement for a single artifact."""
        try:
            prompt = self._create_prompt([artifact])
            requirement = self.llm.generate_text(prompt)
            logger.info(f"Generated requirement for artifact: {artifact.get('name', 'N/A')}")
            return requirement
        except Exception as e:
            logger.error(f"Error generating artifact requirement: {str(e)}")
            raise 