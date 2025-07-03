#!/usr/bin/env python3
"""
Test script to examine ChromaDB contents and provide insights into stored data.
This helps debug what's actually in the database and verify the chunking process.
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from chromadb_connector import EnhancedChromaDBConnector
    from ai_providers import create_ai_provider
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running from the project root directory")
    sys.exit(1)

def test_chromadb_contents():
    """Test and display ChromaDB contents"""
    print("🔍 ChromaDB Content Analysis")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    try:
        # Initialize ChromaDB connector
        print("📡 Connecting to ChromaDB...")
        connector = EnhancedChromaDBConnector()
        print("✅ ChromaDB connection established")
        
        # Get statistics
        print("\n📊 ChromaDB Statistics:")
        print("-" * 30)
        stats = connector.get_chunk_statistics()
        
        if stats:
            print(f"Total chunks: {stats.get('total_chunks', 'N/A')}")
            print(f"Unique files: {stats.get('unique_files', 'N/A')}")
            print(f"Average complexity: {stats.get('avg_complexity', 'N/A')}")
            print(f"Languages found: {stats.get('languages', 'N/A')}")
            print(f"Chunk types: {stats.get('chunk_types', 'N/A')}")
        else:
            print("❌ No statistics available")
        
        # Test different queries to see what's available
        print("\n🔍 Testing Sample Queries:")
        print("-" * 30)
        
        test_queries = [
            "java class",
            "customer service",
            "database sql",
            "controller",
            "test",
            "xml configuration",
            "main function"
        ]
        
        for query in test_queries:
            print(f"\nQuery: '{query}'")
            try:
                results = connector.query_enhanced_similar(query, n_results=3)
                if results and results.get('documents') and results['documents'][0]:
                    print(f"  Found {len(results['documents'][0])} results")
                    for i, doc in enumerate(results['documents'][0][:2]):  # Show first 2
                        metadata = results['metadatas'][0][i] if i < len(results['metadatas'][0]) else {}
                        print(f"  - {metadata.get('file_path', 'unknown')} ({metadata.get('chunk_type', 'unknown')})")
                else:
                    print("  No results found")
            except Exception as e:
                print(f"  Error: {e}")
        
        # Get a sample of all documents
        print("\n📋 Sample of All Documents:")
        print("-" * 30)
        try:
            # Use a very generic query to get more results
            all_results = connector.query_enhanced_similar("", n_results=20)
            if all_results and all_results.get('documents') and all_results['documents'][0]:
                documents = all_results['documents'][0]
                metadatas = all_results['metadatas'][0]
                
                print(f"Retrieved {len(documents)} sample documents:")
                
                # Group by file path
                file_groups = {}
                for i, metadata in enumerate(metadatas):
                    file_path = metadata.get('file_path', 'unknown')
                    chunk_type = metadata.get('chunk_type', 'unknown')
                    language = metadata.get('language', 'unknown')
                    
                    if file_path not in file_groups:
                        file_groups[file_path] = {
                            'chunks': 0,
                            'types': set(),
                            'languages': set()
                        }
                    
                    file_groups[file_path]['chunks'] += 1
                    file_groups[file_path]['types'].add(chunk_type)
                    file_groups[file_path]['languages'].add(language)
                
                # Display grouped results
                for file_path, info in sorted(file_groups.items())[:10]:  # Show first 10 files
                    print(f"  📄 {file_path}")
                    print(f"     Chunks: {info['chunks']}")
                    print(f"     Types: {', '.join(info['types'])}")
                    print(f"     Languages: {', '.join(info['languages'])}")
                    print()
            else:
                print("❌ No documents found in ChromaDB")
                
        except Exception as e:
            print(f"❌ Error retrieving documents: {e}")
        
        # Test specific file path queries
        print("\n🔍 Testing File Path Queries:")
        print("-" * 30)
        
        test_paths = ["cuco-core", "cuco", "admin", "test"]
        for path in test_paths:
            print(f"\nFiles containing '{path}':")
            try:
                # Use a broader query to get more results, then filter by path
                results = connector.query_enhanced_similar(
                    query="",
                    n_results=50,  # Get more results to filter from
                    filters=None
                )
                if results and results.get('documents') and results['documents'][0]:
                    metadatas = results['metadatas'][0]
                    unique_files = set()
                    for metadata in metadatas:
                        file_path = metadata.get('file_path', '')
                        if path.lower() in file_path.lower():
                            unique_files.add(file_path)
                    
                    if unique_files:
                        for file_path in sorted(unique_files)[:5]:  # Show first 5
                            print(f"  - {file_path}")
                    else:
                        print("  No files found with this path pattern")
                else:
                    print("  No files found")
            except Exception as e:
                print(f"  Error: {e}")
        
        print("\n✅ ChromaDB test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during ChromaDB test: {e}")
        import traceback
        traceback.print_exc()

def test_ai_provider():
    """Test AI provider connection"""
    print("\n🤖 AI Provider Test")
    print("=" * 30)
    
    try:
        provider = create_ai_provider()
        print(f"✅ AI Provider: {provider.get_provider_name()}")
        print(f"✅ Model: {provider.get_model_name()}")
        
        # Test a simple query
        print("\n🧪 Testing AI Provider with simple query...")
        test_messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello from AI provider test'"}
        ]
        
        import asyncio
        response = asyncio.run(provider.create_chat_completion(test_messages, temperature=0.1, max_tokens=50))
        print(f"✅ AI Response: {response}")
        
    except Exception as e:
        print(f"❌ AI Provider Error: {e}")

if __name__ == "__main__":
    print("🚀 Starting ChromaDB and AI Provider Tests")
    print("=" * 60)
    
    test_chromadb_contents()
    test_ai_provider()
    
    print("\n🎉 All tests completed!") 