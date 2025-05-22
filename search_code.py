from codebase_processor import CodebaseProcessor

def main():
    processor = CodebaseProcessor("java_codebase")
    
    # Test different search queries
    queries = [
        "Find authentication related code",
        "Show me user registration methods",
        "Find password handling code",
        "Show me email update functionality"
    ]
    
    for query in queries:
        print(f"\nSearching for: {query}")
        print("-" * 50)
        results = processor.search(query, n_results=3)
        
        for result in results:
            print(f"\nType: {result['metadata']['type']}")
            print(f"Path: {result['metadata']['path']}")
            if result['metadata']['type'] == 'method':
                print(f"Class: {result['metadata']['class']}")
                print(f"Method: {result['metadata']['name']}")
            elif result['metadata']['type'] == 'class':
                print(f"Class: {result['metadata']['name']}")
            print(f"Content: {result['content']}")

if __name__ == "__main__":
    main() 