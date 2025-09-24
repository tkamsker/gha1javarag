#!/usr/bin/env python3
"""
Test script for enhanced code chunking and ChromaDB functionality
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.code_chunker import IntelligentCodeChunker
from src.chromadb_connector import EnhancedChromaDBConnector

def test_code_chunking():
    """Test the intelligent code chunking functionality"""
    print("🧪 Testing Enhanced Code Chunking")
    print("=" * 50)
    
    chunker = IntelligentCodeChunker()
    
    # Test Python code
    python_code = '''
import os
from typing import List, Dict

class TestClass:
    def __init__(self, name: str):
        self.name = name
    
    def test_method(self, param: str) -> str:
        """Test method with docstring"""
        return f"Hello {param} from {self.name}"

def main_function():
    obj = TestClass("Test")
    result = obj.test_method("World")
    print(result)

if __name__ == "__main__":
    main_function()
'''
    
    print("📝 Testing Python code chunking:")
    chunks = chunker.chunk_code(python_code, "test.py")
    
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1}:")
        print(f"  Type: {chunk.chunk_type}")
        print(f"  Language: {chunk.language}")
        if chunk.function_name:
            print(f"  Function: {chunk.function_name}")
        if chunk.class_name:
            print(f"  Class: {chunk.class_name}")
        print(f"  Lines: {chunk.start_line}-{chunk.end_line}")
        print(f"  Content preview: {chunk.content[:100]}...")
    
    # Test Java code
    java_code = '''
package com.example;

import java.util.List;
import java.util.ArrayList;

public class TestJavaClass {
    private String name;
    
    public TestJavaClass(String name) {
        this.name = name;
    }
    
    public String testMethod(String param) {
        return "Hello " + param + " from " + name;
    }
    
    public static void main(String[] args) {
        TestJavaClass obj = new TestJavaClass("Test");
        String result = obj.testMethod("World");
        System.out.println(result);
    }
}
'''
    
    print("\n📝 Testing Java code chunking:")
    chunks = chunker.chunk_code(java_code, "TestJavaClass.java")
    
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1}:")
        print(f"  Type: {chunk.chunk_type}")
        print(f"  Language: {chunk.language}")
        if chunk.function_name:
            print(f"  Function: {chunk.function_name}")
        if chunk.class_name:
            print(f"  Class: {chunk.class_name}")
        print(f"  Lines: {chunk.start_line}-{chunk.end_line}")
        print(f"  Content preview: {chunk.content[:100]}...")

def test_enhanced_chromadb():
    """Test the enhanced ChromaDB functionality"""
    print("\n🗄️ Testing Enhanced ChromaDB")
    print("=" * 50)
    
    try:
        connector = EnhancedChromaDBConnector()
        
        # Test storing enhanced metadata
        test_content = '''
def test_function():
    """This is a test function"""
    return "Hello World"

class TestClass:
    def __init__(self):
        self.value = 42
'''
        
        # Write test file to disk for file stats
        test_file_path = "test_file.py"
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write(test_content)
        
        print("💾 Storing enhanced metadata...")
        connector.store_enhanced_metadata(test_file_path, test_content, {"analysis": "Test analysis"})
        
        # Test querying
        print("🔍 Querying enhanced metadata...")
        results = connector.query_enhanced_similar("test function", 3)
        
        if results and results['documents'] and results['documents'][0]:
            print(f"Found {len(results['documents'][0])} results:")
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i]
                print(f"\nResult {i+1}:")
                print(f"  File: {metadata.get('file_path')}")
                print(f"  Type: {metadata.get('chunk_type')}")
                print(f"  Language: {metadata.get('language')}")
                print(f"  Content preview: {doc[:100]}...")
        
        # Test statistics
        print("\n📊 Getting chunk statistics...")
        stats = connector.get_chunk_statistics()
        print(f"Total chunks: {stats.get('total_chunks', 0)}")
        print(f"Languages: {stats.get('languages', {})}")
        print(f"Chunk types: {stats.get('chunk_types', {})}")
        
        # Clean up test file
        os.remove(test_file_path)
        
    except Exception as e:
        print(f"❌ Error testing ChromaDB: {e}")

def test_language_detection():
    """Test language detection functionality"""
    print("\n🔍 Testing Language Detection")
    print("=" * 50)
    
    chunker = IntelligentCodeChunker()
    
    test_files = [
        ("test.py", "def hello(): pass"),
        ("Test.java", "public class Test {}"),
        ("config.yaml", "key: value"),
        ("README.md", "# Title\n\nContent"),
        ("unknown.txt", "Some random text")
    ]
    
    for filename, content in test_files:
        detected = chunker.detect_language(filename, content)
        print(f"{filename:15} -> {detected}")

if __name__ == "__main__":
    print("🚀 Enhanced Code Analysis Test Suite")
    print("=" * 60)
    
    test_language_detection()
    test_code_chunking()
    test_enhanced_chromadb()
    
    print("\n✅ Test suite completed!") 