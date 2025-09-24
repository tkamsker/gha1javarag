#!/usr/bin/env python3
"""
Comprehensive test script for evaluating all 10 questions against the ChromaDB and AI system.
This script tests each question and provides detailed analysis of result quality and usability.
"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from typing import Dict, List, Any, Tuple

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ai_analyzer import AIAnalyzer
from chromadb_connector import ChromaDBConnector

class QuestionTester:
    def __init__(self):
        """Initialize the question tester with AI analyzer and ChromaDB client."""
        self.ai_analyzer = AIAnalyzer()
        self.chroma_client = ChromaDBConnector()
        self.results = []
        
    def test_question(self, question: str, expected_context_types: List[str] = None) -> Dict[str, Any]:
        """
        Test a single question and return detailed results.
        
        Args:
            question: The question to test
            expected_context_types: Expected types of context (e.g., ['method', 'class', 'interface'])
            
        Returns:
            Dictionary with test results and analysis
        """
        print(f"\n{'='*80}")
        print(f"TESTING QUESTION: {question}")
        print(f"{'='*80}")
        
        start_time = time.time()
        
        # Step 1: Query ChromaDB directly
        print("1. Querying ChromaDB directly...")
        chroma_results = self.chroma_client.query(question, n_results=20)
        chroma_time = time.time() - start_time
        
        # Step 2: Get AI response
        print("2. Getting AI response...")
        ai_start_time = time.time()
        ai_response = self.ai_analyzer.analyze_question(question)
        ai_time = time.time() - ai_start_time
        
        # Step 3: Analyze results
        print("3. Analyzing results...")
        
        # Analyze ChromaDB results
        chroma_analysis = self._analyze_chroma_results(chroma_results, expected_context_types)
        
        # Analyze AI response
        ai_analysis = self._analyze_ai_response(ai_response, chroma_results)
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(chroma_analysis, ai_analysis)
        
        result = {
            'question': question,
            'timestamp': datetime.now().isoformat(),
            'chroma_results': chroma_results,
            'chroma_analysis': chroma_analysis,
            'ai_response': ai_response,
            'ai_analysis': ai_analysis,
            'overall_score': overall_score,
            'timing': {
                'chroma_query_time': chroma_time,
                'ai_response_time': ai_time,
                'total_time': time.time() - start_time
            }
        }
        
        self.results.append(result)
        
        # Print summary
        self._print_question_summary(result)
        
        return result
    
    def _analyze_chroma_results(self, results: List[Dict], expected_types: List[str] = None) -> Dict[str, Any]:
        """Analyze ChromaDB query results for quality and relevance."""
        if not results:
            return {
                'score': 0,
                'issues': ['No results returned'],
                'context_count': 0,
                'avg_similarity': 0,
                'file_diversity': 0,
                'type_distribution': {},
                'complexity_range': {'min': 0, 'max': 0, 'avg': 0}
            }
        
        # Count results
        context_count = len(results)
        
        # Calculate average similarity
        similarities = [r.get('similarity', 0) for r in results]
        avg_similarity = sum(similarities) / len(similarities) if similarities else 0
        
        # Analyze file diversity
        files = set(r.get('file', '') for r in results)
        file_diversity = len(files) / context_count if context_count > 0 else 0
        
        # Analyze type distribution
        type_distribution = {}
        for result in results:
            result_type = result.get('type', 'unknown')
            type_distribution[result_type] = type_distribution.get(result_type, 0) + 1
        
        # Analyze complexity
        complexities = [r.get('complexity', 0) for r in results if r.get('complexity') is not None]
        complexity_range = {
            'min': min(complexities) if complexities else 0,
            'max': max(complexities) if complexities else 0,
            'avg': sum(complexities) / len(complexities) if complexities else 0
        }
        
        # Identify issues
        issues = []
        if context_count < 5:
            issues.append(f'Low context count: {context_count}')
        if avg_similarity < -0.1:
            issues.append(f'Low similarity scores: {avg_similarity:.3f}')
        if file_diversity < 0.3:
            issues.append(f'Low file diversity: {file_diversity:.3f}')
        
        # Check expected types
        if expected_types:
            found_types = set(type_distribution.keys())
            missing_types = set(expected_types) - found_types
            if missing_types:
                issues.append(f'Missing expected types: {missing_types}')
        
        # Calculate score (0-100)
        score = 0
        if context_count >= 10:
            score += 25
        elif context_count >= 5:
            score += 15
        elif context_count >= 1:
            score += 5
            
        if avg_similarity > -0.05:
            score += 25
        elif avg_similarity > -0.1:
            score += 15
        elif avg_similarity > -0.2:
            score += 5
            
        if file_diversity > 0.5:
            score += 25
        elif file_diversity > 0.3:
            score += 15
        elif file_diversity > 0.1:
            score += 5
            
        if complexity_range['avg'] > 2:
            score += 25
        elif complexity_range['avg'] > 1:
            score += 15
        elif complexity_range['avg'] > 0:
            score += 5
        
        return {
            'score': min(score, 100),
            'issues': issues,
            'context_count': context_count,
            'avg_similarity': avg_similarity,
            'file_diversity': file_diversity,
            'type_distribution': type_distribution,
            'complexity_range': complexity_range
        }
    
    def _analyze_ai_response(self, response: str, chroma_results: List[Dict]) -> Dict[str, Any]:
        """Analyze AI response for quality and usefulness."""
        if not response:
            return {
                'score': 0,
                'issues': ['No AI response'],
                'response_length': 0,
                'has_code_examples': False,
                'has_specific_details': False,
                'confidence_level': 'none'
            }
        
        response_length = len(response)
        
        # Check for code examples
        has_code_examples = any(marker in response.lower() for marker in [
            'public class', 'public interface', 'public void', 'private', 'protected',
            '@override', '@autowired', 'import ', 'extends ', 'implements '
        ])
        
        # Check for specific details
        has_specific_details = any(marker in response.lower() for marker in [
            'method', 'class', 'interface', 'service', 'dao', 'dto', 'file:', 'lines:',
            'complexity:', 'function:', 'type:'
        ])
        
        # Determine confidence level
        confidence_indicators = {
            'high': ['specific', 'detailed', 'implements', 'extends', 'method', 'class'],
            'medium': ['service', 'dao', 'dto', 'file', 'lines'],
            'low': ['apologize', 'limited', 'context', 'cannot', 'unable']
        }
        
        confidence_score = 0
        for level, indicators in confidence_indicators.items():
            for indicator in indicators:
                if indicator in response.lower():
                    if level == 'high':
                        confidence_score += 3
                    elif level == 'medium':
                        confidence_score += 2
                    else:
                        confidence_score += 1
        
        if confidence_score >= 6:
            confidence_level = 'high'
        elif confidence_score >= 3:
            confidence_level = 'medium'
        else:
            confidence_level = 'low'
        
        # Identify issues
        issues = []
        if response_length < 100:
            issues.append(f'Short response: {response_length} chars')
        if not has_code_examples:
            issues.append('No code examples found')
        if not has_specific_details:
            issues.append('No specific implementation details')
        if confidence_level == 'low':
            issues.append('Low confidence indicators in response')
        
        # Calculate score (0-100)
        score = 0
        if response_length > 500:
            score += 25
        elif response_length > 200:
            score += 15
        elif response_length > 100:
            score += 5
            
        if has_code_examples:
            score += 25
        if has_specific_details:
            score += 25
        if confidence_level == 'high':
            score += 25
        elif confidence_level == 'medium':
            score += 15
        
        return {
            'score': min(score, 100),
            'issues': issues,
            'response_length': response_length,
            'has_code_examples': has_code_examples,
            'has_specific_details': has_specific_details,
            'confidence_level': confidence_level
        }
    
    def _calculate_overall_score(self, chroma_analysis: Dict, ai_analysis: Dict) -> Dict[str, Any]:
        """Calculate overall usability score for the question."""
        chroma_score = chroma_analysis.get('score', 0)
        ai_score = ai_analysis.get('score', 0)
        
        # Weighted average (ChromaDB results are more important)
        overall_score = (chroma_score * 0.6) + (ai_score * 0.4)
        
        # Determine usability level
        if overall_score >= 80:
            usability = 'excellent'
        elif overall_score >= 60:
            usability = 'good'
        elif overall_score >= 40:
            usability = 'fair'
        elif overall_score >= 20:
            usability = 'poor'
        else:
            usability = 'unusable'
        
        return {
            'score': round(overall_score, 1),
            'usability': usability,
            'chroma_weight': round(chroma_score * 0.6, 1),
            'ai_weight': round(ai_score * 0.4, 1)
        }
    
    def _print_question_summary(self, result: Dict[str, Any]):
        """Print a summary of the question test results."""
        print(f"\n📊 QUESTION SUMMARY:")
        print(f"   Question: {result['question']}")
        print(f"   Overall Score: {result['overall_score']['score']}/100 ({result['overall_score']['usability']})")
        print(f"   ChromaDB Score: {result['chroma_analysis']['score']}/100")
        print(f"   AI Score: {result['ai_analysis']['score']}/100")
        print(f"   Context Count: {result['chroma_analysis']['context_count']}")
        print(f"   Response Length: {result['ai_analysis']['response_length']} chars")
        print(f"   Total Time: {result['timing']['total_time']:.2f}s")
        
        if result['chroma_analysis']['issues']:
            print(f"   ChromaDB Issues: {', '.join(result['chroma_analysis']['issues'])}")
        if result['ai_analysis']['issues']:
            print(f"   AI Issues: {', '.join(result['ai_analysis']['issues'])}")
    
    def run_all_tests(self) -> List[Dict[str, Any]]:
        """Run tests for all 10 questions."""
        print("🚀 STARTING COMPREHENSIVE QUESTION TESTING")
        print(f"Timestamp: {datetime.now().isoformat()}")
        
        # Define the 10 test questions with expected context types
        questions = [
            {
                'question': 'What is CustomerEquipmentService and what methods does it provide?',
                'expected_types': ['class', 'interface', 'method']
            },
            {
                'question': 'How does ProductBrowserServiceImpl work and what are its main functions?',
                'expected_types': ['class', 'method']
            },
            {
                'question': 'Show me test classes for customer-related functionality',
                'expected_types': ['class', 'method']
            },
            {
                'question': 'What DTOs are used for customer data and what fields do they contain?',
                'expected_types': ['class', 'method']
            },
            {
                'question': 'How are services implemented in the cuco-core module?',
                'expected_types': ['class', 'method']
            },
            {
                'question': 'What DAO implementations exist for database operations?',
                'expected_types': ['class', 'method']
            },
            {
                'question': 'Show me XML configuration files and their structure',
                'expected_types': ['xml', 'configuration']
            },
            {
                'question': 'What interfaces are defined in the core module?',
                'expected_types': ['interface', 'class']
            },
            {
                'question': 'How is authentication and authorization handled?',
                'expected_types': ['class', 'method', 'configuration']
            },
            {
                'question': 'What are the main business entities and their relationships?',
                'expected_types': ['class', 'method', 'dto']
            }
        ]
        
        for i, q_data in enumerate(questions, 1):
            print(f"\n{'#'*80}")
            print(f"TEST {i}/10")
            print(f"{'#'*80}")
            
            try:
                result = self.test_question(
                    q_data['question'], 
                    q_data.get('expected_types')
                )
            except Exception as e:
                print(f"❌ Error testing question {i}: {e}")
                result = {
                    'question': q_data['question'],
                    'error': str(e),
                    'overall_score': {'score': 0, 'usability': 'error'}
                }
                self.results.append(result)
        
        return self.results
    
    def generate_report(self) -> str:
        """Generate a comprehensive test report."""
        if not self.results:
            return "No test results available."
        
        print(f"\n{'='*80}")
        print("📋 GENERATING COMPREHENSIVE TEST REPORT")
        print(f"{'='*80}")
        
        # Calculate statistics
        total_questions = len(self.results)
        successful_tests = len([r for r in self.results if 'error' not in r])
        error_tests = total_questions - successful_tests
        
        scores = [r['overall_score']['score'] for r in self.results if 'error' not in r]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        usability_counts = {}
        for result in self.results:
            if 'error' not in result:
                usability = result['overall_score']['usability']
                usability_counts[usability] = usability_counts.get(usability, 0) + 1
        
        # Generate report
        report = f"""
# COMPREHENSIVE QUESTION TESTING REPORT
Generated: {datetime.now().isoformat()}

## EXECUTIVE SUMMARY
- Total Questions Tested: {total_questions}
- Successful Tests: {successful_tests}
- Failed Tests: {error_tests}
- Average Score: {avg_score:.1f}/100

## USABILITY BREAKDOWN
"""
        
        for usability, count in sorted(usability_counts.items(), key=lambda x: ['excellent', 'good', 'fair', 'poor', 'unusable'].index(x[0])):
            percentage = (count / successful_tests * 100) if successful_tests > 0 else 0
            report += f"- {usability.title()}: {count} questions ({percentage:.1f}%)\n"
        
        report += "\n## DETAILED RESULTS\n"
        
        for i, result in enumerate(self.results, 1):
            report += f"\n### Question {i}: {result['question']}\n"
            
            if 'error' in result:
                report += f"- **Status**: ❌ ERROR - {result['error']}\n"
                report += f"- **Score**: 0/100 (error)\n"
            else:
                score = result['overall_score']['score']
                usability = result['overall_score']['usability']
                report += f"- **Status**: ✅ SUCCESS\n"
                report += f"- **Score**: {score}/100 ({usability})\n"
                report += f"- **ChromaDB Score**: {result['chroma_analysis']['score']}/100\n"
                report += f"- **AI Score**: {result['ai_analysis']['score']}/100\n"
                report += f"- **Context Count**: {result['chroma_analysis']['context_count']}\n"
                report += f"- **Response Length**: {result['ai_analysis']['response_length']} chars\n"
                report += f"- **Timing**: {result['timing']['total_time']:.2f}s\n"
                
                if result['chroma_analysis']['issues']:
                    report += f"- **ChromaDB Issues**: {', '.join(result['chroma_analysis']['issues'])}\n"
                if result['ai_analysis']['issues']:
                    report += f"- **AI Issues**: {', '.join(result['ai_analysis']['issues'])}\n"
        
        # Recommendations
        report += "\n## RECOMMENDATIONS\n"
        
        if avg_score >= 80:
            report += "- 🎉 **Excellent Results**: The system is working very well for most questions.\n"
        elif avg_score >= 60:
            report += "- ✅ **Good Results**: The system provides useful answers for most questions.\n"
        elif avg_score >= 40:
            report += "- ⚠️ **Fair Results**: Some improvements needed for better usability.\n"
        else:
            report += "- ❌ **Poor Results**: Significant improvements needed.\n"
        
        # Identify common issues
        all_chroma_issues = []
        all_ai_issues = []
        
        for result in self.results:
            if 'error' not in result:
                all_chroma_issues.extend(result['chroma_analysis']['issues'])
                all_ai_issues.extend(result['ai_analysis']['issues'])
        
        if all_chroma_issues:
            common_chroma_issues = {}
            for issue in all_chroma_issues:
                common_chroma_issues[issue] = common_chroma_issues.get(issue, 0) + 1
            
            report += "\n### Common ChromaDB Issues:\n"
            for issue, count in sorted(common_chroma_issues.items(), key=lambda x: x[1], reverse=True):
                report += f"- {issue}: {count} occurrences\n"
        
        if all_ai_issues:
            common_ai_issues = {}
            for issue in all_ai_issues:
                common_ai_issues[issue] = common_ai_issues.get(issue, 0) + 1
            
            report += "\n### Common AI Issues:\n"
            for issue, count in sorted(common_ai_issues.items(), key=lambda x: x[1], reverse=True):
                report += f"- {issue}: {count} occurrences\n"
        
        return report
    
    def save_results(self, filename: str = None):
        """Save test results to a JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"question_test_results_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'results': self.results
            }, f, indent=2)
        
        print(f"\n💾 Results saved to: {filename}")

def main():
    """Main function to run the comprehensive question testing."""
    print("🔍 COMPREHENSIVE QUESTION TESTING SCRIPT")
    print("This script will test all 10 questions against ChromaDB and AI system")
    print("to evaluate result quality and usability.\n")
    
    # Initialize tester
    tester = QuestionTester()
    
    try:
        # Run all tests
        results = tester.run_all_tests()
        
        # Generate and display report
        report = tester.generate_report()
        print(report)
        
        # Save results
        tester.save_results()
        
        # Save report to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"question_test_report_{timestamp}.md"
        with open(report_filename, 'w') as f:
            f.write(report)
        
        print(f"\n📄 Report saved to: {report_filename}")
        
        # Final summary
        successful_tests = len([r for r in results if 'error' not in r])
        if successful_tests > 0:
            avg_score = sum(r['overall_score']['score'] for r in results if 'error' not in r) / successful_tests
            print(f"\n🎯 FINAL SUMMARY:")
            print(f"   Successful Tests: {successful_tests}/{len(results)}")
            print(f"   Average Score: {avg_score:.1f}/100")
            
            if avg_score >= 80:
                print("   🎉 EXCELLENT: System is working very well!")
            elif avg_score >= 60:
                print("   ✅ GOOD: System provides useful answers")
            elif avg_score >= 40:
                print("   ⚠️ FAIR: Some improvements needed")
            else:
                print("   ❌ POOR: Significant improvements needed")
        else:
            print("\n❌ No successful tests completed.")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Testing interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 