#!/usr/bin/env python3
"""
Demo script showing how to use the ChromaDB system effectively
This demonstrates the best practices for querying the system
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"

# Effective query examples based on our testing
EFFECTIVE_QUERIES = {
    "service_analysis": [
        "service interface",
        "service implementation", 
        "service class",
        "business logic"
    ],
    "customer_management": [
        "customer interaction",
        "customer data",
        "customer service",
        "customer management"
    ],
    "configuration": [
        "configuration",
        "XML config",
        "product offering",
        "default configuration"
    ],
    "testing": [
        "test class",
        "unit test",
        "test implementation",
        "test method"
    ],
    "database": [
        "database query",
        "SQL query", 
        "data access",
        "DAO implementation"
    ]
}

def test_query(query: str, search_mode: str = "keyword", max_results: int = 5):
    """Test a query and return results"""
    try:
        payload = {
            "question": query,
            "max_results": max_results,
            "search_mode": search_mode
        }
        response = requests.post(f"{BASE_URL}/chat", json=payload, timeout=15)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def demo_effective_search_strategies():
    """Demonstrate effective search strategies"""
    print("🎯 ChromaDB System - Effective Usage Demo")
    print("=" * 60)
    
    print("\n📋 Search Strategy Guidelines:")
    print("1. Use KEYWORD search mode for specific terms")
    print("2. Use broader, descriptive terms instead of exact class names")
    print("3. Try multiple related terms for better coverage")
    print("4. Focus on functionality rather than exact naming")
    print("5. Use the web interface for interactive exploration")
    
    print("\n🔍 Testing Effective Query Strategies...")
    print("-" * 40)
    
    for category, queries in EFFECTIVE_QUERIES.items():
        print(f"\n📂 Category: {category.replace('_', ' ').title()}")
        print("-" * 30)
        
        for query in queries:
            print(f"\nQuery: '{query}'")
            result = test_query(query, "keyword", 3)
            
            if "error" in result:
                print(f"  ❌ Error: {result['error']}")
            elif "answer" in result:
                answer = result["answer"]
                if answer.startswith("Error"):
                    print(f"  ⚠️  AI Provider: {answer}")
                else:
                    # Truncate long answers for demo
                    preview = answer[:200] + "..." if len(answer) > 200 else answer
                    print(f"  ✅ AI Response: {preview}")
                
                # Show metadata
                filters = result.get("filters_applied", {})
                print(f"  📊 Search Mode: {filters.get('search_mode', 'unknown')}")
                print(f"  📊 Max Results: {filters.get('max_results', 'unknown')}")
            
            time.sleep(1)  # Be nice to the server
    
    print("\n" + "=" * 60)
    print("🎯 Key Takeaways:")
    print("✅ Use 'keyword' search mode for best results")
    print("✅ Try broader terms: 'service interface' vs 'CustomerService'")
    print("✅ The system works well for configuration and business logic queries")
    print("✅ AI provider gives detailed answers when available")
    print("✅ Web interface at http://localhost:8000 for interactive use")

def demo_web_interface_usage():
    """Show how to use the web interface effectively"""
    print("\n🌐 Web Interface Usage Guide")
    print("=" * 40)
    print("1. Open http://localhost:8000 in your browser")
    print("2. Use these effective search strategies:")
    print("   • Search Mode: 'Keyword Search'")
    print("   • Max Results: 10-15 for good coverage")
    print("   • File Path Filter: 'cuco-core' for core functionality")
    print("   • Language Filter: 'java' for Java code")
    print("   • Chunk Type Filter: 'class' or 'method' for specific types")
    
    print("\n💡 Effective Query Examples for Web Interface:")
    print("• 'service interface' - Find service classes")
    print("• 'customer interaction' - Find customer-related code")
    print("• 'configuration' - Find configuration files")
    print("• 'test class' - Find test implementations")
    print("• 'database query' - Find SQL and data access code")
    print("• 'product offering' - Find product configuration")
    
    print("\n🔧 Advanced Filtering:")
    print("• File Path: 'cuco-core' for core business logic")
    print("• File Path: 'cuco-cct-core' for CCT functionality")
    print("• Language: 'java' for Java code, 'xml' for config")
    print("• Chunk Type: 'class' for classes, 'method' for methods")

def demo_troubleshooting():
    """Show common issues and solutions"""
    print("\n🔧 Troubleshooting Guide")
    print("=" * 30)
    
    print("\n❌ Common Issues:")
    print("1. 'No relevant context found'")
    print("   → Try broader terms or keyword search")
    print("   → Check if the term exists in the codebase")
    
    print("\n2. 'AI provider overloaded'")
    print("   → Wait a few minutes and try again")
    print("   → Use debug endpoints to check ChromaDB directly")
    
    print("\n3. 'No results from ChromaDB'")
    print("   → Try different search terms")
    print("   → Use the debug endpoint to test queries")
    
    print("\n4. 'Irrelevant results'")
    print("   → Use more specific terms")
    print("   → Apply file path or language filters")
    print("   → Try different search modes")
    
    print("\n✅ Best Practices:")
    print("• Start with keyword search")
    print("• Use descriptive terms, not exact class names")
    print("• Try multiple related queries")
    print("• Use filters to narrow results")
    print("• Check debug endpoints for direct ChromaDB access")

def run_demo():
    """Run the complete demo"""
    print("🚀 Starting ChromaDB Effective Usage Demo")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code != 200:
            print("❌ Server not available. Please start the Flask app first.")
            return
    except:
        print("❌ Cannot connect to server. Please start the Flask app first.")
        return
    
    print("✅ Server is running")
    
    # Run demos
    demo_effective_search_strategies()
    demo_web_interface_usage()
    demo_troubleshooting()
    
    print("\n" + "=" * 60)
    print("🎉 Demo Complete!")
    print("💡 Remember: The system works best with keyword search and descriptive terms")
    print("🌐 Visit http://localhost:8000 for interactive exploration")

if __name__ == "__main__":
    run_demo() 