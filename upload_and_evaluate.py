from codebase_processor import CodebaseProcessor
import json
from typing import List, Dict, Any
import logging
from pathlib import Path

class RAGEvaluator:
    def __init__(self, codebase_path: str, db_path: str = "chroma_db"):
        """Initialize the RAG evaluator."""
        self.processor = CodebaseProcessor(codebase_path, db_path)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def upload_codebase(self):
        """Upload the codebase to the RAG system."""
        self.logger.info("Starting codebase upload...")
        self.processor.process_codebase()
        self.logger.info("Codebase upload completed!")

    def evaluate_quality(self, test_queries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluate the quality of the RAG system using test queries."""
        results = {
            'total_queries': len(test_queries),
            'successful_matches': 0,
            'query_results': []
        }

        for query in test_queries:
            self.logger.info(f"Testing query: {query['query']}")
            search_results = self.processor.search(query['query'], n_results=3)
            
            # Check if any of the expected files/classes/methods are in the results
            found_expected = False
            for result in search_results:
                if self._is_expected_result(result, query['expected']):
                    found_expected = True
                    break

            query_result = {
                'query': query['query'],
                'found_expected': found_expected,
                'results': search_results
            }
            results['query_results'].append(query_result)
            
            if found_expected:
                results['successful_matches'] += 1

        # Calculate success rate
        results['success_rate'] = (results['successful_matches'] / results['total_queries']) * 100
        return results

    def _is_expected_result(self, result: Dict[str, Any], expected: Dict[str, Any]) -> bool:
        """Check if a search result matches the expected result."""
        metadata = result['metadata']
        
        # Check file path
        if 'path' in expected and expected['path'] not in metadata['path']:
            return False
            
        # Check type
        if 'type' in expected and expected['type'] != metadata['type']:
            return False
            
        # Check class name
        if 'class' in expected and expected['class'] != metadata.get('class', ''):
            return False
            
        # Check method name
        if 'method' in expected and expected['method'] != metadata.get('name', ''):
            return False
            
        return True

def main():
    # Define test queries with expected results
    test_queries = [
        {
            'query': "Find authentication related code",
            'expected': {
                'type': 'method',
                'class': 'UserService',
                'method': 'authenticate'
            }
        },
        {
            'query': "Show me user registration methods",
            'expected': {
                'type': 'method',
                'class': 'UserService',
                'method': 'register'
            }
        },
        {
            'query': "Find password handling code",
            'expected': {
                'type': 'class',
                'class': 'PasswordHasher'
            }
        },
        {
            'query': "Show me email update functionality",
            'expected': {
                'type': 'method',
                'class': 'UserService',
                'method': 'updateEmail'
            }
        },
        {
            'query': "Find user data model",
            'expected': {
                'type': 'class',
                'class': 'User'
            }
        }
    ]

    # Initialize evaluator
    evaluator = RAGEvaluator("java_codebase")
    
    # Upload codebase
    evaluator.upload_codebase()
    
    # Evaluate quality
    evaluation_results = evaluator.evaluate_quality(test_queries)
    
    # Print results
    print("\nEvaluation Results:")
    print("=" * 50)
    print(f"Total Queries: {evaluation_results['total_queries']}")
    print(f"Successful Matches: {evaluation_results['successful_matches']}")
    print(f"Success Rate: {evaluation_results['success_rate']:.2f}%")
    
    print("\nDetailed Results:")
    print("=" * 50)
    for query_result in evaluation_results['query_results']:
        print(f"\nQuery: {query_result['query']}")
        print(f"Found Expected Result: {'Yes' if query_result['found_expected'] else 'No'}")
        print("Top Results:")
        for result in query_result['results'][:2]:  # Show top 2 results
            print(f"- Type: {result['metadata']['type']}")
            print(f"  Path: {result['metadata']['path']}")
            if result['metadata']['type'] == 'method':
                print(f"  Class: {result['metadata']['class']}")
                print(f"  Method: {result['metadata']['name']}")
            elif result['metadata']['type'] == 'class':
                print(f"  Class: {result['metadata']['name']}")

if __name__ == "__main__":
    main() 