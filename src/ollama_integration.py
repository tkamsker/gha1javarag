"""
Ollama Integration Module for Qwen3-Coder-30B-A3B-Instruct-1M-Unsloth
Optimized for 1M token context window processing and MoE architecture utilization.
"""

import asyncio
import aiohttp
import json
import logging
import time
import psutil
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

logger = logging.getLogger('java_analysis.ollama_integration')

@dataclass
class OllamaModel:
    """Represents an Ollama model configuration"""
    name: str
    size: int
    modified: str
    digest: str
    details: Dict[str, Any]

@dataclass
class ContextWindowConfig:
    """Configuration for 1M token context window optimization"""
    max_tokens: int = 1_048_576  # 1M tokens
    target_utilization: float = 0.98  # 98% utilization target
    chunk_overlap: int = 1024  # Token overlap between chunks
    batch_size: int = 8  # Batch size for processing
    moe_optimization: bool = True  # MoE architecture optimization

@dataclass
class QwenAnalysisResult:
    """Result from Qwen3-Coder analysis"""
    content: str
    tokens_used: int
    processing_time: float
    model_info: Dict[str, Any]
    context_utilization: float
    confidence_score: float

class OllamaIntegration:
    """
    Enhanced Ollama integration optimized for Qwen3-Coder-30B-A3B-Instruct-1M-Unsloth
    Handles 1M token context windows and MoE architecture optimization.
    """
    
    def __init__(self, base_url: str = None, model_name: str = None, timeout: int = 300):
        load_dotenv()
        
        self.base_url = base_url or os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.model_name = model_name or os.getenv('OLLAMA_MODEL_NAME', 
                                                  'danielsheep/qwen3-coder-30b-a3b-instruct-1m-unsloth')
        self.timeout = timeout or int(os.getenv('OLLAMA_TIMEOUT', '300'))
        
        # Qwen3-Coder specific configuration
        self.context_config = ContextWindowConfig()
        self._embedding_model = 'nomic-embed-text'
        self._session = None
        self._model_loaded = False
        self._performance_stats = {
            'total_requests': 0,
            'total_tokens': 0,
            'average_response_time': 0.0,
            'context_utilization_avg': 0.0
        }
        
        logger.info(f"Initialized Ollama integration with model: {self.model_name}")
        logger.info(f"Base URL: {self.base_url}, Timeout: {self.timeout}s")

    @asynccontextmanager
    async def _get_session(self):
        """Get or create aiohttp session with optimized settings for large contexts"""
        if self._session is None:
            timeout = aiohttp.ClientTimeout(
                total=self.timeout,
                connect=30,
                sock_read=self.timeout
            )
            connector = aiohttp.TCPConnector(
                limit=100,
                limit_per_host=20,
                keepalive_timeout=60
            )
            self._session = aiohttp.ClientSession(
                timeout=timeout,
                connector=connector,
                headers={'Content-Type': 'application/json'}
            )
        
        try:
            yield self._session
        except Exception as e:
            logger.error(f"Session error: {e}")
            if self._session:
                await self._session.close()
                self._session = None
            raise

    async def health_check(self) -> bool:
        """Check if Ollama service is healthy and responsive"""
        try:
            async with self._get_session() as session:
                async with session.get(f"{self.base_url}/api/tags") as response:
                    if response.status == 200:
                        data = await response.json()
                        models = [model['name'] for model in data.get('models', [])]
                        
                        # Check if our target model is available
                        model_available = any(self.model_name in model for model in models)
                        
                        if model_available:
                            logger.info(f"Health check passed. Model {self.model_name} is available.")
                            return True
                        else:
                            logger.warning(f"Model {self.model_name} not found in available models: {models}")
                            return False
                    else:
                        logger.error(f"Health check failed with status: {response.status}")
                        return False
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

    async def list_models(self) -> List[OllamaModel]:
        """List all available models with their details"""
        try:
            async with self._get_session() as session:
                async with session.get(f"{self.base_url}/api/tags") as response:
                    if response.status == 200:
                        data = await response.json()
                        models = []
                        for model_data in data.get('models', []):
                            models.append(OllamaModel(
                                name=model_data.get('name', ''),
                                size=model_data.get('size', 0),
                                modified=model_data.get('modified', ''),
                                digest=model_data.get('digest', ''),
                                details=model_data.get('details', {})
                            ))
                        
                        logger.info(f"Retrieved {len(models)} models from Ollama")
                        return models
                    else:
                        logger.error(f"Failed to list models: HTTP {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []

    async def ensure_model_loaded(self) -> bool:
        """Ensure the Qwen3-Coder model is loaded and ready"""
        if self._model_loaded:
            return True
            
        try:
            # Pre-load the model by sending a small request
            test_prompt = "// Test Java class\npublic class Test {}"
            
            async with self._get_session() as session:
                payload = {
                    "model": self.model_name,
                    "prompt": f"Analyze this code:\n{test_prompt}",
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "num_predict": 50
                    }
                }
                
                logger.info(f"Pre-loading model: {self.model_name}")
                start_time = time.time()
                
                async with session.post(f"{self.base_url}/api/generate", 
                                      json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        load_time = time.time() - start_time
                        
                        self._model_loaded = True
                        logger.info(f"Model loaded successfully in {load_time:.2f}s")
                        logger.info(f"Model info: {data.get('model', 'N/A')}")
                        
                        return True
                    else:
                        error_text = await response.text()
                        logger.error(f"Failed to load model: HTTP {response.status} - {error_text}")
                        return False
                        
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False

    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count for text (approximation)"""
        # Rough estimation: 1 token ≈ 4 characters for code
        # This is conservative for Qwen3-Coder which may be more efficient
        return len(text) // 3

    def _optimize_for_moe_architecture(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize request payload for MoE architecture (3.3B active from 30B total)"""
        if self.context_config.moe_optimization:
            # MoE optimization settings for Qwen3-Coder
            payload["options"] = payload.get("options", {})
            payload["options"].update({
                "num_ctx": min(self.context_config.max_tokens, 1_048_576),  # Full context window
                "num_batch": 512,  # Optimized batch size for MoE
                "num_gqa": 8,      # Grouped query attention optimization
                "rope_frequency_base": 1000000.0,  # Extended context optimization
                "repeat_penalty": 1.1,
                "temperature": 0.2,
                "top_k": 40,
                "top_p": 0.95,
            })
        
        return payload

    async def analyze_code_repository(self, 
                                    repository_context: str, 
                                    specific_query: str = None,
                                    analysis_type: str = "comprehensive") -> QwenAnalysisResult:
        """
        Analyze entire repository context using 1M token window
        Optimized for Qwen3-Coder's code understanding capabilities
        """
        if not await self.ensure_model_loaded():
            raise RuntimeError("Failed to ensure model is loaded")
        
        # Estimate tokens and validate context size
        estimated_tokens = self._estimate_tokens(repository_context)
        
        if estimated_tokens > self.context_config.max_tokens * 0.8:
            logger.warning(f"Repository context ({estimated_tokens} tokens) approaching limit")
        
        # Build optimized prompt for repository analysis
        if analysis_type == "comprehensive":
            system_prompt = """You are an expert software architect analyzing a Java/JSP codebase. 
            Analyze the provided repository context and extract:
            1. Architectural patterns and design decisions
            2. Business logic and domain rules
            3. Data flow and integration points
            4. Code quality issues and technical debt
            5. Modernization opportunities (JSP to modern frameworks)
            6. Performance bottlenecks and optimization opportunities
            
            Focus on repository-wide insights that leverage the full codebase context."""
        else:
            system_prompt = f"Analyze this Java/JSP repository focusing on: {analysis_type}"
        
        if specific_query:
            system_prompt += f"\n\nSpecific query: {specific_query}"
        
        # Construct the full prompt
        full_prompt = f"{system_prompt}\n\nRepository Context:\n{repository_context}"
        
        try:
            async with self._get_session() as session:
                payload = {
                    "model": self.model_name,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.2,
                        "num_predict": 2048,  # Allow substantial response
                    }
                }
                
                # Apply MoE optimizations
                payload = self._optimize_for_moe_architecture(payload)
                
                start_time = time.time()
                logger.info(f"Starting repository analysis with {estimated_tokens} estimated tokens")
                
                async with session.post(f"{self.base_url}/api/generate", 
                                      json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        processing_time = time.time() - start_time
                        
                        # Extract response details
                        content = data.get('response', '')
                        tokens_used = estimated_tokens + self._estimate_tokens(content)
                        context_utilization = tokens_used / self.context_config.max_tokens
                        
                        # Update performance stats
                        self._update_performance_stats(tokens_used, processing_time, context_utilization)
                        
                        # Calculate confidence score based on response completeness
                        confidence_score = min(1.0, len(content) / 1000)  # Simple heuristic
                        
                        result = QwenAnalysisResult(
                            content=content,
                            tokens_used=tokens_used,
                            processing_time=processing_time,
                            model_info=data.get('model_info', {}),
                            context_utilization=context_utilization,
                            confidence_score=confidence_score
                        )
                        
                        logger.info(f"Analysis completed: {processing_time:.2f}s, "
                                  f"{tokens_used} tokens, "
                                  f"{context_utilization:.1%} context utilization")
                        
                        return result
                    else:
                        error_text = await response.text()
                        raise RuntimeError(f"Analysis failed: HTTP {response.status} - {error_text}")
                        
        except Exception as e:
            logger.error(f"Repository analysis error: {e}")
            raise

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using nomic-embed-text model"""
        try:
            async with self._get_session() as session:
                embeddings = []
                
                for text in texts:
                    payload = {
                        "model": self._embedding_model,
                        "prompt": text,
                        "stream": False
                    }
                    
                    async with session.post(f"{self.base_url}/api/embeddings", 
                                          json=payload) as response:
                        if response.status == 200:
                            data = await response.json()
                            embedding = data.get('embedding', [])
                            embeddings.append(embedding)
                        else:
                            logger.error(f"Embedding generation failed for text: {text[:50]}...")
                            embeddings.append([])
                
                logger.info(f"Generated {len(embeddings)} embeddings")
                return embeddings
                
        except Exception as e:
            logger.error(f"Embedding generation error: {e}")
            return []

    def _update_performance_stats(self, tokens_used: int, processing_time: float, context_utilization: float):
        """Update internal performance statistics"""
        self._performance_stats['total_requests'] += 1
        self._performance_stats['total_tokens'] += tokens_used
        
        # Update running average for response time
        current_avg = self._performance_stats['average_response_time']
        total_requests = self._performance_stats['total_requests']
        self._performance_stats['average_response_time'] = (
            (current_avg * (total_requests - 1) + processing_time) / total_requests
        )
        
        # Update context utilization average
        current_util_avg = self._performance_stats['context_utilization_avg']
        self._performance_stats['context_utilization_avg'] = (
            (current_util_avg * (total_requests - 1) + context_utilization) / total_requests
        )

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get current performance statistics"""
        stats = self._performance_stats.copy()
        
        # Add system resource usage
        stats['system_memory_usage'] = psutil.virtual_memory().percent
        stats['system_cpu_usage'] = psutil.cpu_percent()
        
        return stats

    async def cleanup(self):
        """Clean up resources"""
        if self._session:
            await self._session.close()
            self._session = None
        logger.info("Ollama integration cleaned up")

    async def __aenter__(self):
        """Async context manager entry"""
        await self.health_check()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.cleanup()

# Convenience factory function
def create_ollama_integration(**kwargs) -> OllamaIntegration:
    """Factory function to create configured OllamaIntegration instance"""
    return OllamaIntegration(**kwargs)