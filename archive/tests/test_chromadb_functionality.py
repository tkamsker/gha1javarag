#!/usr/bin/env python3
"""
Test script to evaluate ChromaDB functionality and search capabilities
This script tests the database content and search quality without relying on AI responses
"""

import requests
import json
import time
from typing import Dict, List, Tuple

# Configuration
BASE_URL = "http://localhost:8000"
TEST_QUERIES = [
    # Customer-related queries
    "CustomerInteractionService",
    "CustomerService", 
    "customer interaction",
    "customer management",
    
    # Service-related queries
    "PartyService",
    "ServiceServiceImpl",
    "service interface",
    
    # Test-related queries
    "CustomerInteractionServiceImplTest",
    "test class",
    "unit test",
    
    # Database-related queries
    "CustomerDao",
    "database query",
    "SQL query",
    
    # Configuration queries
    "configuration",
    "XML config",
    "product offering"
]

def test_server_connectivity() -> bool:
    """Test if the Flask server is running"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Server connectivity test failed: {e}")
        return False

def test_chromadb_stats() -> Dict:
    """Test ChromaDB statistics endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/stats", timeout=10)
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ ChromaDB Stats: {stats['total_chunks']} chunks, {stats['unique_files']} files")
            return stats
        else:
            print(f"❌ Stats endpoint failed: {response.status_code}")
            return {}
    except Exception as e:
        print(f"❌ Stats test failed: {e}")
        return {}

def test_debug_chromadb() -> Dict:
    """Test ChromaDB debug endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/debug/chromadb", timeout=10)
        if response.status_code == 200:
            debug_info = response.json()
            print(f"✅ Debug endpoint working")
            return debug_info
        else:
            print(f"❌ Debug endpoint failed: {response.status_code}")
            return {}
    except Exception as e:
        print(f"❌ Debug test failed: {e}")
        return {}

def test_query_endpoint(query: str, search_mode: str = "keyword") -> Dict:
    """Test the debug query endpoint"""
    try:
        encoded_query = requests.utils.quote(query)
        response = requests.get(f"{BASE_URL}/debug/query/{encoded_query}", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Query endpoint failed for '{query}': {response.status_code}")
            return {}
    except Exception as e:
        print(f"❌ Query test failed for '{query}': {e}")
        return {}

def test_chat_endpoint(query: str, search_mode: str = "keyword", max_results: int = 5) -> Dict:
    """Test the chat endpoint (without relying on AI response)"""
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
            print(f"❌ Chat endpoint failed for '{query}': {response.status_code}")
            return {}
    except Exception as e:
        print(f"❌ Chat test failed for '{query}': {e}")
        return {}

def analyze_query_results(query: str, results: Dict) -> Dict:
    """Analyze the quality of query results"""
    analysis = {
        "query": query,
        "has_results": False,
        "result_count": 0,
        "relevant_results": 0,
        "file_types": set(),
        "languages": set(),
        "avg_content_length": 0,
        "quality_score": 0
    }
    
    if not results or "results" not in results:
        return analysis
    
    results_list = results.get("results", [])
    analysis["has_results"] = len(results_list) > 0
    analysis["result_count"] = len(results_list)
    
    if not results_list:
        return analysis
    
    total_length = 0
    relevant_count = 0
    
    for result in results_list:
        # Extract metadata
        file_path = result.get("file_path", "")
        chunk_type = result.get("chunk_type", "")
        language = result.get("language", "")
        content = result.get("content", "")
        content_length = result.get("content_length", 0)
        
        analysis["file_types"].add(chunk_type)
        analysis["languages"].add(language)
        total_length += content_length
        
        # Check relevance (simple heuristic)
        query_lower = query.lower()
        content_lower = content.lower()
        
        # Check if query terms appear in content
        query_terms = query_lower.split()
        matching_terms = sum(1 for term in query_terms if term in content_lower)
        
        if matching_terms > 0:
            relevant_count += 1
    
    analysis["relevant_results"] = relevant_count
    analysis["avg_content_length"] = total_length / len(results_list) if results_list else 0
    
    # Calculate quality score (0-100)
    if analysis["result_count"] > 0:
        relevance_ratio = analysis["relevant_results"] / analysis["result_count"]
        diversity_score = len(analysis["file_types"]) / 5  # Normalize by expected max
        content_score = min(analysis["avg_content_length"] / 1000, 1.0)  # Normalize by expected length
        
        analysis["quality_score"] = int((relevance_ratio * 0.5 + diversity_score * 0.3 + content_score * 0.2) * 100)
    
    # Convert sets to lists for JSON serialization
    analysis["file_types"] = list(analysis["file_types"])
    analysis["languages"] = list(analysis["languages"])
    
    return analysis

def run_comprehensive_test():
    """Run comprehensive ChromaDB functionality tests"""
    print("🚀 Starting ChromaDB Functionality Test Suite")
    print("=" * 60)
    
    # Test 1: Server connectivity
    print("\n1. Testing server connectivity...")
    if not test_server_connectivity():
        print("❌ Cannot proceed - server not available")
        return
    print("✅ Server is running")
    
    # Test 2: ChromaDB statistics
    print("\n2. Testing ChromaDB statistics...")
    stats = test_chromadb_stats()
    if not stats:
        print("❌ Cannot proceed - ChromaDB not available")
        return
    
    # Test 3: Debug endpoint
    print("\n3. Testing debug endpoint...")
    debug_info = test_debug_chromadb()
    if not debug_info:
        print("❌ Debug endpoint not working")
        return
    
    # Test 4: Query testing
    print("\n4. Testing query functionality...")
    print("-" * 40)
    
    query_results = []
    total_quality_score = 0
    
    for i, query in enumerate(TEST_QUERIES, 1):
        print(f"\nQuery {i}/{len(TEST_QUERIES)}: '{query}'")
        
        # Test both debug query and chat endpoints
        debug_results = test_query_endpoint(query, "keyword")
        chat_results = test_chat_endpoint(query, "keyword", 5)
        
        # Analyze debug results
        debug_analysis = analyze_query_results(query, debug_results)
        query_results.append({
            "query": query,
            "debug_analysis": debug_analysis,
            "chat_available": bool(chat_results),
            "ai_available": chat_results.get("answer", "").startswith("Error") == False if chat_results else False
        })
        
        total_quality_score += debug_analysis["quality_score"]
        
        # Print summary
        print(f"  Results: {debug_analysis['result_count']} chunks")
        print(f"  Relevant: {debug_analysis['relevant_results']}/{debug_analysis['result_count']}")
        print(f"  Quality Score: {debug_analysis['quality_score']}/100")
        print(f"  Languages: {', '.join(debug_analysis['languages'])}")
        print(f"  Types: {', '.join(debug_analysis['file_types'])}")
        
        # Small delay to avoid overwhelming the server
        time.sleep(0.5)
    
    # Test 5: Summary and analysis
    print("\n5. Test Summary")
    print("=" * 60)
    
    avg_quality_score = total_quality_score / len(TEST_QUERIES) if TEST_QUERIES else 0
    successful_queries = sum(1 for r in query_results if r["debug_analysis"]["has_results"])
    chat_available_count = sum(1 for r in query_results if r["chat_available"])
    ai_available_count = sum(1 for r in query_results if r["ai_available"])
    
    print(f"Database Statistics:")
    print(f"  Total Chunks: {stats.get('total_chunks', 0):,}")
    print(f"  Unique Files: {stats.get('unique_files', 0):,}")
    print(f"  Languages: {list(stats.get('languages', {}).keys())}")
    
    print(f"\nQuery Performance:")
    print(f"  Total Queries Tested: {len(TEST_QUERIES)}")
    print(f"  Successful Queries: {successful_queries}/{len(TEST_QUERIES)} ({successful_queries/len(TEST_QUERIES)*100:.1f}%)")
    print(f"  Average Quality Score: {avg_quality_score:.1f}/100")
    print(f"  Chat Endpoint Available: {chat_available_count}/{len(TEST_QUERIES)} ({chat_available_count/len(TEST_QUERIES)*100:.1f}%)")
    print(f"  AI Provider Available: {ai_available_count}/{len(TEST_QUERIES)} ({ai_available_count/len(TEST_QUERIES)*100:.1f}%)")
    
    print(f"\nTop Performing Queries:")
    top_queries = sorted(query_results, key=lambda x: x["debug_analysis"]["quality_score"], reverse=True)[:5]
    for i, result in enumerate(top_queries, 1):
        print(f"  {i}. '{result['query']}' - Score: {result['debug_analysis']['quality_score']}/100")
    
    print(f"\nBottom Performing Queries:")
    bottom_queries = sorted(query_results, key=lambda x: x["debug_analysis"]["quality_score"])[:5]
    for i, result in enumerate(bottom_queries, 1):
        print(f"  {i}. '{result['query']}' - Score: {result['debug_analysis']['quality_score']}/100")
    
    # Overall assessment
    print(f"\nOverall Assessment:")
    if avg_quality_score >= 70:
        print("  🟢 EXCELLENT - ChromaDB is working very well")
    elif avg_quality_score >= 50:
        print("  🟡 GOOD - ChromaDB is working reasonably well")
    elif avg_quality_score >= 30:
        print("  🟠 FAIR - ChromaDB needs improvement")
    else:
        print("  🔴 POOR - ChromaDB needs significant improvement")
    
    if successful_queries / len(TEST_QUERIES) >= 0.8:
        print("  🟢 Query Success Rate: Excellent")
    elif successful_queries / len(TEST_QUERIES) >= 0.6:
        print("  🟡 Query Success Rate: Good")
    else:
        print("  🔴 Query Success Rate: Needs improvement")
    
    # Save detailed results
    with open("chromadb_test_results.json", "w") as f:
        json.dump({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "stats": stats,
            "query_results": query_results,
            "summary": {
                "avg_quality_score": avg_quality_score,
                "successful_queries": successful_queries,
                "total_queries": len(TEST_QUERIES),
                "chat_available": chat_available_count,
                "ai_available": ai_available_count
            }
        }, f, indent=2)
    
    print(f"\n📊 Detailed results saved to: chromadb_test_results.json")

if __name__ == "__main__":
    run_comprehensive_test() 