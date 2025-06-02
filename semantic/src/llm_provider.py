import os
import logging
import requests
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from llama_cpp import Llama
from openai import AzureOpenAI, OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMProvider(ABC):
    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        pass

class OllamaProvider(LLMProvider):
    def __init__(self, model_name: str, base_url: str = "http://localhost:11434", temperature: float = 0.7):
        self.model_name = model_name
        self.base_url = base_url
        self.temperature = temperature
        logger.info(f"Initialized Ollama provider with model: {model_name}")

    def generate_text(self, prompt: str) -> str:
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "temperature": self.temperature,
                    "stream": False
                }
            )
            response.raise_for_status()
            return response.json()["response"].strip()
        except Exception as e:
            logger.error(f"Error generating text with Ollama: {str(e)}")
            raise

class LocalLlamaProvider(LLMProvider):
    def __init__(self, model_path: str, context_size: int = 4096, temperature: float = 0.7, max_tokens: int = 1024):
        self.model = Llama(
            model_path=model_path,
            n_ctx=context_size,
            n_threads=os.cpu_count() or 4
        )
        self.temperature = temperature
        self.max_tokens = max_tokens
        logger.info(f"Initialized Local Llama provider with model: {model_path}")

    def generate_text(self, prompt: str) -> str:
        try:
            response = self.model(
                prompt,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                stop=["</s>", "Human:", "Assistant:"]
            )
            return response["choices"][0]["text"].strip()
        except Exception as e:
            logger.error(f"Error generating text with Local Llama: {str(e)}")
            raise

class AzureOpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, endpoint: str, deployment_name: str, api_version: str):
        self.client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=endpoint
        )
        self.deployment_name = deployment_name
        logger.info(f"Initialized Azure OpenAI provider with deployment: {deployment_name}")

    def generate_text(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating text with Azure OpenAI: {str(e)}")
            raise

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        logger.info("Initialized OpenAI provider")

    def generate_text(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating text with OpenAI: {str(e)}")
            raise

class LLMProviderFactory:
    @staticmethod
    def create_provider() -> LLMProvider:
        load_dotenv()
        provider = os.getenv("LLM_PROVIDER", "local").lower()

        if provider == "ollama":
            model_name = os.getenv("OLLAMA_MODEL_NAME")
            if not model_name:
                raise ValueError("OLLAMA_MODEL_NAME environment variable is required for Ollama provider")
            
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
            
            return OllamaProvider(
                model_name=model_name,
                base_url=base_url,
                temperature=temperature
            )
        
        elif provider == "local":
            model_path = os.getenv("LLM_MODEL_PATH")
            if not model_path:
                raise ValueError("LLM_MODEL_PATH environment variable is required for local provider")
            
            context_size = int(os.getenv("LLM_CONTEXT_SIZE", "4096"))
            temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
            max_tokens = int(os.getenv("LLM_MAX_TOKENS", "1024"))
            
            return LocalLlamaProvider(
                model_path=model_path,
                context_size=context_size,
                temperature=temperature,
                max_tokens=max_tokens
            )
        
        elif provider == "azure":
            api_key = os.getenv("AZURE_OPENAI_API_KEY")
            endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
            api_version = os.getenv("AZURE_OPENAI_API_VERSION")
            
            if not all([api_key, endpoint, deployment_name, api_version]):
                raise ValueError("Azure OpenAI configuration is incomplete")
            
            return AzureOpenAIProvider(
                api_key=api_key,
                endpoint=endpoint,
                deployment_name=deployment_name,
                api_version=api_version
            )
        
        elif provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable is required for OpenAI provider")
            
            return OpenAIProvider(api_key=api_key)
        
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}") 