from typing import Dict, List, Any
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
import logging
from pathlib import Path
import json
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_API_BASE')
)

class Embedder:
    def __init__(self, api_key: str, model: str = "text-embedding-3-small"):
        """Initialize the embedder with OpenAI API key and model."""
        self.client = client
        self.model = model

    def generate_embeddings(self, artifacts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate embeddings for code artifacts."""
        try:
            embeddings = []
            for artifact in artifacts:
                # Create a text representation of the artifact
                text = self._create_artifact_text(artifact)
                
                # Generate embedding
                response = self.client.embeddings.create(
                    model=self.model,
                    input=text
                )
                
                # Store the embedding with metadata
                embeddings.append({
                    'id': artifact['name'],
                    'text': text,
                    'embedding': response.data[0].embedding,
                    'metadata': {
                        'type': artifact['type'],
                        'name': artifact['name'],
                        'brief': artifact.get('brief', ''),
                        'detailed': artifact.get('detailed', '')
                    }
                })
            
            logger.info(f"Generated {len(embeddings)} embeddings")
            return embeddings
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise

    def _create_artifact_text(self, artifact: Dict[str, Any]) -> str:
        """Create a text representation of an artifact for embedding."""
        text_parts = []
        
        # Add type and name
        text_parts.append(f"{artifact['type']}: {artifact['name']}")
        
        # Add brief description
        if artifact.get('brief'):
            text_parts.append(f"Brief: {artifact['brief']}")
        
        # Add detailed description
        if artifact.get('detailed'):
            text_parts.append(f"Detailed: {artifact['detailed']}")
        
        # Add fields for classes
        if artifact['type'] == 'class' and artifact.get('fields'):
            text_parts.append("Fields:")
            for field in artifact['fields']:
                text_parts.append(f"- {field['name']} ({field['type']}): {field['description']}")
        
        # Add parameters for methods
        if artifact['type'] == 'function' and artifact.get('parameters'):
            text_parts.append("Parameters:")
            for param in artifact['parameters']:
                text_parts.append(f"- {param['name']} ({param['type']})")
        
        return "\n".join(text_parts)

    def save_embeddings(self, embeddings: List[Dict[str, Any]], output_path: str) -> None:
        """Save embeddings to a JSON file."""
        try:
            output_file = Path(output_path)
            with open(output_file, 'w') as f:
                json.dump(embeddings, f, indent=2)
            logger.info(f"Embeddings saved to {output_path}")
        except Exception as e:
            logger.error(f"Error saving embeddings: {str(e)}")
            raise

    def load_embeddings(self, input_path: str) -> None:
        """Load embeddings from a JSON file."""
        try:
            input_file = Path(input_path)
            if input_file.exists():
                with open(input_file, 'r') as f:
                    self.embeddings_cache = json.load(f)
                logger.info(f"Embeddings loaded from {input_path}")
        except Exception as e:
            logger.error(f"Error loading embeddings: {str(e)}")
            raise

    def _generate_requirement(self, cluster_info: Dict) -> str:
        """Generate a requirement for a cluster using GPT-4."""
        prompt = self._prepare_cluster_prompt(cluster_info)
        try:
            logger.info(f"Using model: {self.model} for requirement generation.")
            response = openai.chat.completions.create(
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