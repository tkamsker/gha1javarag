#!/usr/bin/env python3
"""Test Ollama embedding API"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import httpx
import json

# Test the embedding API
url = "http://localhost:11434/api/embeddings"
payload = {
    "model": "nomic-embed-text:latest",
    "input": "This is a test sentence"
}

print("Testing Ollama Embeddings API...")
print(f"URL: {url}")
print(f"Payload: {json.dumps(payload, indent=2)}")

try:
    response = httpx.post(url, json=payload, timeout=60.0)
    print(f"\nStatus: {response.status_code}")
    result = response.json()
    
    embedding = result.get("embedding", [])
    print(f"Embedding length: {len(embedding)}")
    
    if embedding and len(embedding) > 0:
        print(f"First 5 values: {embedding[:5]}")
        print("✅ Embedding API working correctly!")
    else:
        print("⚠️  Empty embedding returned")
        print(f"Full response: {json.dumps(result, indent=2)}")
        print("\nPossible issues:")
        print("1. Model may need to be loaded: ollama run nomic-embed-text")
        print("2. Model might not support embeddings properly")
        print("3. Check model: ollama show nomic-embed-text")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

