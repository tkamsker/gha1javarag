#!/usr/bin/env python3
"""
Test script for AI providers (OpenAI and Ollama)
Tests the provider switching functionality
"""

import asyncio
import os
import logging
from dotenv import load_dotenv
from ai_providers import create_ai_provider, OpenAIProvider, OllamaProvider

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_provider(provider_name: str):
    """Test a specific AI provider"""
    logger.info(f"\n=== Testing {provider_name.upper()} Provider ===")
    
    # Set environment variable for testing
    os.environ['AI_PROVIDER'] = provider_name
    
    try:
        # Create provider
        provider = create_ai_provider()
        logger.info(f"✅ Successfully created {provider.get_provider_name()} provider")
        logger.info(f"   Model: {provider.get_model_name()}")
        
        # Test simple completion
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello from {provider_name}!' in one sentence."}
        ]
        
        logger.info("Sending test request...")
        response = await provider.create_chat_completion(
            messages=messages,
            temperature=0.1,
            max_tokens=50
        )
        
        logger.info(f"✅ Received response: {response.strip()}")
        return True
        
    except Exception as e:
        logger.error(f"❌ {provider_name} test failed: {str(e)}")
        return False

async def test_provider_switching():
    """Test switching between providers"""
    logger.info("\n=== Testing Provider Switching ===")
    
    # Test OpenAI (if API key is available)
    if os.getenv('OPENAI_API_KEY'):
        openai_success = await test_provider('openai')
    else:
        logger.warning("⚠️  Skipping OpenAI test - no API key found")
        openai_success = False
    
    # Test Ollama (if available)
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:11434/api/tags', timeout=5) as response:
                if response.status == 200:
                    ollama_success = await test_provider('ollama')
                else:
                    logger.warning("⚠️  Skipping Ollama test - service not responding")
                    ollama_success = False
    except Exception:
        logger.warning("⚠️  Skipping Ollama test - service not available")
        ollama_success = False
    
    # Summary
    logger.info("\n=== Test Summary ===")
    if openai_success:
        logger.info("✅ OpenAI provider: Working")
    else:
        logger.info("❌ OpenAI provider: Failed or skipped")
    
    if ollama_success:
        logger.info("✅ Ollama provider: Working")
    else:
        logger.info("❌ Ollama provider: Failed or skipped")
    
    if not openai_success and not ollama_success:
        logger.error("❌ No providers are working!")
        logger.info("💡 Setup instructions:")
        logger.info("   OpenAI: Set OPENAI_API_KEY environment variable")
        logger.info("   Ollama: Start ollama serve and pull a model")

async def test_invalid_provider():
    """Test handling of invalid provider"""
    logger.info("\n=== Testing Invalid Provider ===")
    
    try:
        os.environ['AI_PROVIDER'] = 'invalid_provider'
        provider = create_ai_provider()
        logger.error("❌ Should have raised an error for invalid provider")
    except ValueError as e:
        logger.info(f"✅ Correctly handled invalid provider: {e}")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")

async def main():
    """Main test function"""
    load_dotenv()
    
    logger.info("Starting AI Provider Tests")
    logger.info("=" * 50)
    
    # Test invalid provider first
    await test_invalid_provider()
    
    # Test provider switching
    await test_provider_switching()
    
    logger.info("\n" + "=" * 50)
    logger.info("AI Provider Tests Completed")

if __name__ == "__main__":
    asyncio.run(main()) 