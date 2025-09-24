#!/usr/bin/env python3
"""
DAO Elements Query Script
Queries ChromaDB for Data Access Objects and related database interaction patterns
"""

import sys
import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chromadb_connector import EnhancedChromaDBConnector

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DAOElementsAnalyzer:
    """Analyzes and extracts DAO elements from ChromaDB"""
    
    def __init__(self):
        load_dotenv()
        self.connector = EnhancedChromaDBConnector()
        
    def get_database_statistics(self) -> Dict[str, Any]:
        """Get comprehensive database statistics"""
        try:
            stats = self.connector.get_chunk_statistics()
            
            # Add collection info
            collection_info = {
                'collection_name': self.connector.collection.name,
                'collection_id': str(self.connector.collection.id),
                'total_documents': self.connector.collection.count() if hasattr(self.connector.collection, 'count') else 0
            }
            
            stats.update(collection_info)
            return stats
            
        except Exception as e:
            logger.error(f"Error getting database statistics: {e}")
            return {'error': str(e)}
    
    def find_dao_elements(self) -> List[Dict[str, Any]]:
        """Find all DAO-related elements in the database"""
        dao_queries = [
            "DAO data access object",
            "Repository pattern database",
            "CRUD operations create read update delete",
            "Database connection PreparedStatement ResultSet",
            "Entity bean JPA hibernate",
            "SQL query INSERT UPDATE DELETE SELECT",
            "@Repository @Entity @Table annotation",
            "DataSource ConnectionPool database"
        ]
        
        dao_elements = []
        
        for query in dao_queries:
            try:
                results = self.connector.query_enhanced_similar(query, 10)
                
                if results and results.get('documents') and results['documents'][0]:
                    for i, doc in enumerate(results['documents'][0]):
                        metadata = results['metadatas'][0][i]
                        
                        dao_element = {
                            'query_matched': query,
                            'file_path': metadata.get('file_path', 'Unknown'),
                            'class_name': metadata.get('class_name', ''),
                            'function_name': metadata.get('function_name', ''),
                            'chunk_type': metadata.get('chunk_type', 'Unknown'),
                            'language': metadata.get('language', 'Unknown'),
                            'architectural_layer': metadata.get('architectural_layer', ''),
                            'component_type': metadata.get('component_type', ''),
                            'database_interactions': metadata.get('database_interactions', 'False'),
                            'start_line': metadata.get('start_line', '1'),
                            'end_line': metadata.get('end_line', '1'),
                            'complexity_score': metadata.get('complexity_score', '1.0'),
                            'content_preview': doc[:300] + "..." if len(doc) > 300 else doc,
                            'similarity_distance': results['distances'][0][i] if results.get('distances') else 0
                        }
                        
                        # Parse enhanced analysis if available
                        if metadata.get('enhanced_ai_analysis'):
                            try:
                                enhanced = json.loads(metadata['enhanced_ai_analysis'])
                                dao_element['enhanced_analysis'] = enhanced
                            except (json.JSONDecodeError, TypeError):
                                pass
                        
                        dao_elements.append(dao_element)
                        
            except Exception as e:
                logger.error(f"Error querying for '{query}': {e}")
                continue
        
        return dao_elements
    
    def find_database_interaction_files(self) -> List[Dict[str, Any]]:
        """Find files that have database interactions flag set"""
        try:
            results = self.connector.query_files_with_database_interactions(20)
            
            db_files = []
            if results and results.get('documents'):
                # Handle different result formats
                documents = results['documents'] if isinstance(results['documents'][0], str) else results['documents'][0]
                metadatas = results['metadatas'] if isinstance(results['metadatas'][0], dict) else results['metadatas'][0]
                
                for i, doc in enumerate(documents):
                    metadata = metadatas[i]
                    
                    db_file = {
                        'file_path': metadata.get('file_path', 'Unknown'),
                        'class_name': metadata.get('class_name', ''),
                        'function_name': metadata.get('function_name', ''),
                        'chunk_type': metadata.get('chunk_type', 'Unknown'),
                        'architectural_layer': metadata.get('architectural_layer', ''),
                        'component_type': metadata.get('component_type', ''),
                        'exposes_api': metadata.get('exposes_api', 'False'),
                        'consumes_api': metadata.get('consumes_api', 'False'),
                        'business_domain': metadata.get('business_domain', ''),
                        'content_preview': doc[:300] + "..." if len(doc) > 300 else doc
                    }
                    
                    db_files.append(db_file)
            
            return db_files
            
        except Exception as e:
            logger.error(f"Error finding database interaction files: {e}")
            return []
    
    def analyze_data_structures(self) -> List[Dict[str, Any]]:
        """Analyze data structures and entity definitions"""
        structure_queries = [
            "class entity bean model",
            "private String int long double field variable",
            "getter setter accessor mutator",
            "constructor initialization",
            "toString equals hashCode",
            "@Column @Id @GeneratedValue @ManyToOne @OneToMany",
            "validation constraints NotNull NotEmpty",
            "serializable persistent transient"
        ]
        
        data_structures = []
        
        for query in structure_queries:
            try:
                results = self.connector.query_enhanced_similar(query, 8)
                
                if results and results.get('documents') and results['documents'][0]:
                    for i, doc in enumerate(results['documents'][0]):
                        metadata = results['metadatas'][0][i]
                        
                        structure = {
                            'pattern_matched': query,
                            'file_path': metadata.get('file_path', 'Unknown'),
                            'class_name': metadata.get('class_name', ''),
                            'function_name': metadata.get('function_name', ''),
                            'chunk_type': metadata.get('chunk_type', 'Unknown'),
                            'architectural_layer': metadata.get('architectural_layer', ''),
                            'component_type': metadata.get('component_type', ''),
                            'primary_purpose': metadata.get('primary_purpose', ''),
                            'business_domain': metadata.get('business_domain', ''),
                            'design_patterns': metadata.get('design_patterns', '[]'),
                            'content_preview': doc[:400] + "..." if len(doc) > 400 else doc
                        }
                        
                        data_structures.append(structure)
                        
            except Exception as e:
                logger.error(f"Error analyzing structures for '{query}': {e}")
                continue
        
        return data_structures
    
    def find_business_rules(self) -> List[Dict[str, Any]]:
        """Find business logic and rules implementations"""
        business_queries = [
            "business logic validation rule",
            "if else condition check validate",
            "switch case business decision",
            "calculation compute calculate",
            "workflow process step",
            "exception error handling business",
            "constraint rule policy",
            "state transition status"
        ]
        
        business_rules = []
        
        for query in business_queries:
            try:
                results = self.connector.query_enhanced_similar(query, 8)
                
                if results and results.get('documents') and results['documents'][0]:
                    for i, doc in enumerate(results['documents'][0]):
                        metadata = results['metadatas'][0][i]
                        
                        rule = {
                            'business_pattern': query,
                            'file_path': metadata.get('file_path', 'Unknown'),
                            'class_name': metadata.get('class_name', ''),
                            'function_name': metadata.get('function_name', ''),
                            'chunk_type': metadata.get('chunk_type', 'Unknown'),
                            'complexity_score': metadata.get('complexity_score', '1.0'),
                            'business_domain': metadata.get('business_domain', ''),
                            'primary_purpose': metadata.get('primary_purpose', ''),
                            'content_preview': doc[:350] + "..." if len(doc) > 350 else doc
                        }
                        
                        business_rules.append(rule)
                        
            except Exception as e:
                logger.error(f"Error finding business rules for '{query}': {e}")
                continue
        
        return business_rules
    
    def generate_comprehensive_report(self, output_file: str = None) -> Dict[str, Any]:
        """Generate comprehensive DAO and data structure analysis report"""
        logger.info("Starting comprehensive DAO elements analysis...")
        
        report = {
            'timestamp': str(os.popen('date').read().strip()),
            'database_statistics': self.get_database_statistics(),
            'dao_elements': self.find_dao_elements(),
            'database_interaction_files': self.find_database_interaction_files(),
            'data_structures': self.analyze_data_structures(),
            'business_rules': self.find_business_rules()
        }
        
        # Add summary statistics
        report['summary'] = {
            'total_dao_elements': len(report['dao_elements']),
            'database_interaction_files': len(report['database_interaction_files']),
            'data_structures_found': len(report['data_structures']),
            'business_rules_found': len(report['business_rules']),
            'unique_files_analyzed': len(set([
                item.get('file_path', '') for item in 
                report['dao_elements'] + report['data_structures'] + report['business_rules']
                if item.get('file_path')
            ]))
        }
        
        if output_file:
            try:
                with open(output_file, 'w') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
                logger.info(f"Report saved to: {output_file}")
            except Exception as e:
                logger.error(f"Error saving report: {e}")
        
        return report

def main():
    """Main function to run DAO elements analysis"""
    analyzer = DAOElementsAnalyzer()
    
    # Generate timestamp for output file
    timestamp = os.popen('date +"%Y%m%d_%H%M%S"').read().strip()
    output_file = f"./output/dao_elements_analysis_{timestamp}.json"
    
    # Ensure output directory exists
    os.makedirs('./output', exist_ok=True)
    
    try:
        # Generate comprehensive report
        report = analyzer.generate_comprehensive_report(output_file)
        
        # Print summary to console
        print("\n=== DAO Elements Analysis Summary ===")
        print(f"Database Statistics: {json.dumps(report['database_statistics'], indent=2)}")
        print(f"\nSummary: {json.dumps(report['summary'], indent=2)}")
        
        if report['summary']['total_dao_elements'] > 0:
            print(f"\n=== Found {report['summary']['total_dao_elements']} DAO Elements ===")
            for i, dao in enumerate(report['dao_elements'][:5], 1):  # Show first 5
                print(f"\n{i}. File: {dao['file_path']}")
                print(f"   Class: {dao['class_name']} | Function: {dao['function_name']}")
                print(f"   Type: {dao['chunk_type']} | Layer: {dao['architectural_layer']}")
                print(f"   Preview: {dao['content_preview'][:150]}...")
        
        if report['summary']['database_interaction_files'] > 0:
            print(f"\n=== Database Interaction Files ({report['summary']['database_interaction_files']}) ===")
            for i, db_file in enumerate(report['database_interaction_files'][:3], 1):  # Show first 3
                print(f"\n{i}. {db_file['file_path']}")
                print(f"   Component: {db_file['component_type']} | Domain: {db_file['business_domain']}")
        
        print(f"\nFull report saved to: {output_file}")
        
    except Exception as e:
        logger.error(f"Error running analysis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()