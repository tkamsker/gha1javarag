#!/usr/bin/env python3
"""
Test script for Ollama debugging
Demonstrates enhanced logging and error handling
"""

import asyncio
import os
import logging
from dotenv import load_dotenv
from ai_providers import OllamaProvider

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_ollama_debug():
    """Test Ollama with enhanced debugging"""
    load_dotenv()
    
    logger.info("=== Ollama Debug Test ===")
    
    try:
        # Create Ollama provider
        provider = OllamaProvider()
        logger.info(f"Provider created: {provider.get_provider_name()}")
        logger.info(f"Model: {provider.get_model_name()}")
        
        # Test health check
        logger.info("\n--- Health Check ---")
        health = await provider.health_check()
        logger.info(f"Health status: {health['status']}")
        logger.info(f"Health message: {health['message']}")
        
        if health['status'] == 'error':
            logger.error("Health check failed, cannot proceed")
            return
        
        # Test simple completion
        logger.info("\n--- Test Completion ---")
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello from Ollama debug test!' in one sentence."}
        ]
        
        response = await provider.create_chat_completion(
            messages=messages,
            temperature=0.1,
            max_tokens=50
        )
        
        logger.info(f"✅ Success! Response: {response.strip()}")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {str(e)}")
        logger.error("Check the logs above for detailed debugging information")

async def test_ollama_timeout():
    """Test Ollama timeout handling"""
    logger.info("\n=== Ollama Timeout Test ===")
    
    try:
        # Create provider with very short timeout
        os.environ['OLLAMA_TIMEOUT'] = '5'  # 5 seconds timeout
        provider = OllamaProvider()
        
        # Send a complex request that might timeout
        messages = [
            {"role": "system", "content": "You are a code analysis expert. Provide detailed analysis."},
            {"role": "user", "content": "Analyze this complex Java code in detail: " + "public class Test { " * 1000}
        ]
        
        response = await provider.create_chat_completion(
            messages=messages,
            temperature=0.2,
            max_tokens=2000
        )
        
        logger.info(f"✅ Timeout test completed: {len(response)} characters")
        
    except Exception as e:
        logger.error(f"❌ Timeout test failed (expected): {str(e)}")
        logger.info("This demonstrates the enhanced timeout logging")

async def main():
    """Main test function"""
    logger.info("Starting Ollama Debug Tests")
    logger.info("=" * 60)
    
    # Test normal operation
    await test_ollama_debug()
    
    # Test timeout handling
    await test_ollama_timeout()
    
    logger.info("\n" + "=" * 60)
    logger.info("Ollama Debug Tests Completed")
    logger.info("Check the logs above for detailed debugging information")

if __name__ == "__main__":
    asyncio.run(main()) 