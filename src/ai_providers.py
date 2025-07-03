import os
import asyncio
import aiohttp
import json
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from openai import AsyncOpenAI
from dotenv import load_dotenv
import logging
import time
try:
    from config_loader import get_ollama_config
except ImportError:
    from .config_loader import get_ollama_config
import anthropic

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

class AnthropicProvider(AIProvider):
    """Anthropic Claude provider implementation"""
    
    def __init__(self):
        load_dotenv()
        
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
            
        self.model_name = os.getenv('ANTHROPIC_MODEL_NAME', 'claude-3-5-sonnet-20241022')
        self.client = anthropic.AsyncAnthropic(api_key=api_key)
        self.timeout = 360  # 6 minutes timeout for Anthropic
        
        logger.info(f"Initialized Anthropic provider with model: {self.model_name}")
    
    async def create_chat_completion(self, messages: List[Dict[str, str]], 
                                   temperature: float = 0.2, 
                                   max_tokens: int = 1500) -> str:
        """Create a chat completion using Anthropic Claude API"""
        try:
            # Convert OpenAI format to Anthropic format
            anthropic_messages = []
            system_message = None
            
            for msg in messages:
                if msg['role'] == 'system':
                    system_message = msg['content']
                else:
                    anthropic_messages.append({
                        'role': msg['role'],
                        'content': msg['content']
                    })
            
            # Log request details
            logger.info(f"Anthropic request details:")
            logger.info(f"  Model: {self.model_name}")
            logger.info(f"  Temperature: {temperature}")
            logger.info(f"  Max tokens: {max_tokens}")
            logger.info(f"  Timeout: {self.timeout} seconds")
            logger.info(f"  Message count: {len(anthropic_messages)}")
            
            # Log first message preview for debugging
            if anthropic_messages:
                first_msg_preview = anthropic_messages[0]['content'][:200] + "..." if len(anthropic_messages[0]['content']) > 200 else anthropic_messages[0]['content']
                logger.info(f"  First message preview: {first_msg_preview}")
            
            logger.info(f"Sending Anthropic request...")
            start_time = time.time()
            
            response = await self.client.messages.create(
                model=self.model_name,
                messages=anthropic_messages,
                system=system_message,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            request_time = time.time() - start_time
            logger.info(f"Anthropic response received in {request_time:.2f} seconds")
            
            if response.content and len(response.content) > 0:
                response_content = response.content[0].text
                response_preview = response_content[:200] + "..." if len(response_content) > 200 else response_content
                logger.info(f"  Response preview: {response_preview}")
                logger.info(f"  Response length: {len(response_content)} characters")
                return response_content
            else:
                logger.error(f"Empty response from Anthropic API")
                raise Exception("Empty response from Anthropic API")
                
        except Exception as e:
            logger.error(f"Anthropic API error: {str(e)}")
            logger.error(f"Request details:")
            logger.error(f"  Model: {self.model_name}")
            logger.error(f"  Temperature: {temperature}")
            logger.error(f"  Max tokens: {max_tokens}")
            raise
    
    def get_provider_name(self) -> str:
        return "Anthropic"
    
    def get_model_name(self) -> str:
        return self.model_name

class OllamaProvider(AIProvider):
    """Ollama local provider implementation"""
    
    def __init__(self):
        load_dotenv()
        
        self.base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.model_name = os.getenv('OLLAMA_MODEL_NAME', 'deepseek-r1:32b')
        
        # Get timeout from config based on environment
        ollama_config = get_ollama_config()
        self.timeout = ollama_config['timeout']
        
        logger.info(f"Initialized Ollama provider with model: {self.model_name}")
        logger.info(f"Ollama base URL: {self.base_url}")
        logger.info(f"Ollama timeout: {self.timeout} seconds (from {ollama_config['environment']} config)")
    
    async def health_check(self) -> dict:
        """Check Ollama service health and model availability"""
        try:
            async with aiohttp.ClientSession() as session:
                # Check if Ollama is running
                logger.info("Checking Ollama service health...")
                async with session.get(f"{self.base_url}/api/tags", timeout=10) as response:
                    if response.status != 200:
                        return {
                            'status': 'error',
                            'message': f'Ollama service not responding: {response.status}',
                            'details': await response.text()
                        }
                    
                    models_data = await response.json()
                    available_models = [model['name'] for model in models_data.get('models', [])]
                    
                    logger.info(f"Available Ollama models: {available_models}")
                    
                    if self.model_name in available_models:
                        return {
                            'status': 'healthy',
                            'message': f'Model {self.model_name} is available',
                            'available_models': available_models,
                            'selected_model': self.model_name
                        }
                    else:
                        return {
                            'status': 'warning',
                            'message': f'Model {self.model_name} not found',
                            'available_models': available_models,
                            'selected_model': self.model_name
                        }
                        
        except asyncio.TimeoutError:
            return {
                'status': 'error',
                'message': 'Ollama service timeout during health check',
                'timeout': 10
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Ollama health check failed: {str(e)}',
                'error': str(e)
            }
    
    async def create_chat_completion(self, messages: List[Dict[str, str]], 
                                   temperature: float = 0.2, 
                                   max_tokens: int = 1500) -> str:
        """Create a chat completion using Ollama API"""
        try:
            # Perform health check before making request
            health = await self.health_check()
            if health['status'] == 'error':
                logger.error(f"Ollama health check failed: {health['message']}")
                raise Exception(f"Ollama service unavailable: {health['message']}")
            elif health['status'] == 'warning':
                logger.warning(f"Ollama health check warning: {health['message']}")
                logger.warning(f"Available models: {health.get('available_models', [])}")
            
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
            
            # Log request details
            logger.info(f"Ollama request details:")
            logger.info(f"  URL: {self.base_url}/api/chat")
            logger.info(f"  Model: {self.model_name}")
            logger.info(f"  Temperature: {temperature}")
            logger.info(f"  Max tokens: {max_tokens}")
            logger.info(f"  Timeout: {self.timeout} seconds")
            logger.info(f"  Message count: {len(ollama_messages)}")
            
            # Log first message preview for debugging
            if ollama_messages:
                first_msg_preview = ollama_messages[0]['content'][:200] + "..." if len(ollama_messages[0]['content']) > 200 else ollama_messages[0]['content']
                logger.info(f"  First message preview: {first_msg_preview}")
            
            async with aiohttp.ClientSession() as session:
                logger.info(f"Sending Ollama request...")
                start_time = time.time()
                
                async with session.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    request_time = time.time() - start_time
                    logger.info(f"Ollama response received in {request_time:.2f} seconds")
                    logger.info(f"  Status code: {response.status}")
                    logger.info(f"  Content-Type: {response.headers.get('content-type', 'unknown')}")
                    
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Ollama API error response:")
                        logger.error(f"  Status: {response.status}")
                        logger.error(f"  Headers: {dict(response.headers)}")
                        logger.error(f"  Body: {error_text}")
                        raise Exception(f"Ollama API error: {response.status} - {error_text}")
                    
                    result = await response.json()
                    logger.info(f"Ollama response parsed successfully")
                    logger.info(f"  Response keys: {list(result.keys())}")
                    
                    if 'message' in result and 'content' in result['message']:
                        response_content = result['message']['content']
                        response_preview = response_content[:200] + "..." if len(response_content) > 200 else response_content
                        logger.info(f"  Response preview: {response_preview}")
                        logger.info(f"  Response length: {len(response_content)} characters")
                        return response_content
                    else:
                        logger.error(f"Unexpected Ollama response structure:")
                        logger.error(f"  Response: {result}")
                        raise Exception(f"Unexpected Ollama response structure: {result}")
                    
        except asyncio.TimeoutError:
            logger.error(f"Ollama request timed out after {self.timeout} seconds")
            logger.error(f"Request details:")
            logger.error(f"  URL: {self.base_url}/api/chat")
            logger.error(f"  Model: {self.model_name}")
            logger.error(f"  Timeout: {self.timeout} seconds")
            raise Exception(f"Ollama request timed out after {self.timeout} seconds")
        except aiohttp.ClientError as e:
            logger.error(f"Ollama network error: {str(e)}")
            logger.error(f"Request details:")
            logger.error(f"  URL: {self.base_url}/api/chat")
            logger.error(f"  Model: {self.model_name}")
            raise Exception(f"Ollama network error: {str(e)}")
        except Exception as e:
            logger.error(f"Ollama API error: {str(e)}")
            logger.error(f"Request details:")
            logger.error(f"  URL: {self.base_url}/api/chat")
            logger.error(f"  Model: {self.model_name}")
            logger.error(f"  Payload: {payload}")
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
    elif ai_provider == 'anthropic':
        logger.info("Creating Anthropic AI provider")
        return AnthropicProvider()
    else:
        raise ValueError(f"Unsupported AI provider: {ai_provider}. Supported providers: 'openai', 'ollama', 'anthropic'") 