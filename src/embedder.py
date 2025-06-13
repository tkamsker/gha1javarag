from typing import Dict, List
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

class CodeEmbedder:
    def __init__(self, api_key: str):
        """Initialize the embedder with OpenAI API key."""
        self.client = client
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=api_key,
            openai_api_base=os.getenv('OPENAI_API_BASE')
        )
        self.embeddings_cache: Dict[str, List[float]] = {}

    def generate_embeddings(self, code_artifacts: Dict) -> Dict[str, List[float]]:
        """Generate embeddings for all code artifacts."""
        try:
            # Process classes
            for class_name, class_info in code_artifacts["classes"].items():
                class_text = self._prepare_class_text(class_info)
                self.embeddings_cache[f"class:{class_name}"] = self._get_embedding(class_text)

            # Process methods
            for method_key, method_info in code_artifacts["methods"].items():
                method_text = self._prepare_method_text(method_info)
                self.embeddings_cache[f"method:{method_key}"] = self._get_embedding(method_text)

            return self.embeddings_cache

        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise

    def _prepare_class_text(self, class_info: Dict) -> str:
        """Prepare class information for embedding."""
        return f"""
        Class: {class_info['name']}
        Documentation: {class_info['documentation']}
        Methods: {', '.join(m['name'] for m in class_info['methods'])}
        """

    def _prepare_method_text(self, method_info: Dict) -> str:
        """Prepare method information for embedding."""
        return f"""
        Method: {method_info['name']}
        Return Type: {method_info['return_type']}
        Parameters: {method_info['parameters']}
        Documentation: {method_info['documentation']}
        """

    def _get_embedding(self, text: str) -> List[float]:
        """Get embedding for a text using OpenAI's API."""
        try:
            return self.embeddings.embed_query(text)
        except Exception as e:
            logger.error(f"Error getting embedding: {str(e)}")
            raise

    def save_embeddings(self, output_path: str) -> None:
        """Save embeddings to a JSON file."""
        try:
            output_file = Path(output_path)
            with open(output_file, 'w') as f:
                json.dump(self.embeddings_cache, f)
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