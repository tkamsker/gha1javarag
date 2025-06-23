import os
import asyncio
import aiohttp
import json
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from openai import AsyncOpenAI
from dotenv import load_dotenv
import logging

logger = logging.getLogger('java_analysis.ai_providers')

class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    async def create_chat_completion(self, messages: List[Dict[str, str]], 
                                   temperature: float = 0.2, 
                                   max_tokens: int = 1500) -> str:
        """Create a chat completion and return the response content"""
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Return the name of the provider"""
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """Return the model name being used"""
        pass

class OpenAIProvider(AIProvider):
    """OpenAI API provider implementation"""
    
    def __init__(self):
        load_dotenv()
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        self.model_name = os.getenv('OPENAI_MODEL_NAME', 'gpt-4-turbo-preview')
        self.client = AsyncOpenAI(api_key=api_key)
        logger.info(f"Initialized OpenAI provider with model: {self.model_name}")
    
    async def create_chat_completion(self, messages: List[Dict[str, str]], 
                                   temperature: float = 0.2, 
                                   max_tokens: int = 1500) -> str:
        """Create a chat completion using OpenAI API"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
    
    def get_provider_name(self) -> str:
        return "OpenAI"
    
    def get_model_name(self) -> str:
        return self.model_name

class OllamaProvider(AIProvider):
    """Ollama local provider implementation"""
    
    def __init__(self):
        load_dotenv()
        
        self.base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.model_name = os.getenv('OLLAMA_MODEL_NAME', 'deepseek-r1:32b')
        self.timeout = int(os.getenv('OLLAMA_TIMEOUT', '120'))  # 2 minutes default
        
        logger.info(f"Initialized Ollama provider with model: {self.model_name}")
        logger.info(f"Ollama base URL: {self.base_url}")
    
    async def create_chat_completion(self, messages: List[Dict[str, str]], 
                                   temperature: float = 0.2, 
                                   max_tokens: int = 1500) -> str:
        """Create a chat completion using Ollama API"""
        try:
            # Convert OpenAI format to Ollama format
            ollama_messages = []
            for msg in messages:
                if msg['role'] == 'system':
                    # Ollama doesn't have system messages, prepend to user message
                    continue
                ollama_messages.append({
                    'role': msg['role'],
                    'content': msg['content']
                })
            
            # If there was a system message, prepend it to the first user message
            if messages and messages[0]['role'] == 'system':
                if ollama_messages and ollama_messages[0]['role'] == 'user':
                    ollama_messages[0]['content'] = f"{messages[0]['content']}\n\n{ollama_messages[0]['content']}"
            
            payload = {
                'model': self.model_name,
                'messages': ollama_messages,
                'options': {
                    'temperature': temperature,
                    'num_predict': max_tokens
                },
                'stream': False
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"Ollama API error: {response.status} - {error_text}")
                    
                    result = await response.json()
                    return result['message']['content']
                    
        except asyncio.TimeoutError:
            logger.error(f"Ollama request timed out after {self.timeout} seconds")
            raise Exception(f"Ollama request timed out after {self.timeout} seconds")
        except Exception as e:
            logger.error(f"Ollama API error: {str(e)}")
            raise
    
    def get_provider_name(self) -> str:
        return "Ollama"
    
    def get_model_name(self) -> str:
        return self.model_name

def create_ai_provider() -> AIProvider:
    """Factory function to create the appropriate AI provider based on environment variables"""
    load_dotenv()
    
    ai_provider = os.getenv('AI_PROVIDER', 'openai').lower()
    
    if ai_provider == 'ollama':
        logger.info("Creating Ollama AI provider")
        return OllamaProvider()
    elif ai_provider == 'openai':
        logger.info("Creating OpenAI AI provider")
        return OpenAIProvider()
    else:
        raise ValueError(f"Unsupported AI provider: {ai_provider}. Supported providers: 'openai', 'ollama'") 