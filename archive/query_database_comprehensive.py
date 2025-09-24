#!/usr/bin/env python3
"""
Comprehensive Database Query Script
Master script that combines DAO analysis and data structures analysis
Provides a unified view of the entire application's data architecture
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

class ComprehensiveDatabaseAnalyzer:
    """Master analyzer that combines all database-related analysis"""
    
    def __init__(self):
        load_dotenv()
        self.connector = EnhancedChromaDBConnector()
        
    def query_all_architectural_layers(self) -> Dict[str, List[Dict[str, Any]]]:
        """Query all architectural layers in the application"""
        layers = ['presentation', 'business', 'data', 'integration', 'service', 'controller', 'model', 'dao', 'entity']
        
        layer_analysis = {}
        
        for layer in layers:
            try:
                results = self.connector.query_by_architectural_layer(layer, 15)
                
                layer_components = []
                if results and results.get('documents'):
                    # Handle different result formats
                    documents = results['documents'] if isinstance(results['documents'][0], str) else results['documents'][0]
                    metadatas = results['metadatas'] if isinstance(results['metadatas'][0], dict) else results['metadatas'][0]
                    
                    for i, doc in enumerate(documents):
                        metadata = metadatas[i]
                        
                        component = {
                            'file_path': metadata.get('file_path', ''),
                            'class_name': metadata.get('class_name', ''),
                            'function_name': metadata.get('function_name', ''),
                            'component_type': metadata.get('component_type', ''),
                            'business_domain': metadata.get('business_domain', ''),
                            'primary_purpose': metadata.get('primary_purpose', ''),
                            'exposes_api': metadata.get('exposes_api', 'False'),
                            'consumes_api': metadata.get('consumes_api', 'False'),
                            'database_interactions': metadata.get('database_interactions', 'False'),
                            'content_preview': doc[:200] + "..." if len(doc) > 200 else doc
                        }
                        
                        layer_components.append(component)
                
                layer_analysis[layer] = layer_components
                logger.info(f"Found {len(layer_components)} components in {layer} layer")
                
            except Exception as e:
                logger.error(f"Error querying {layer} layer: {e}")
                layer_analysis[layer] = []
        
        return layer_analysis
    
    def query_all_component_types(self) -> Dict[str, List[Dict[str, Any]]]:
        """Query all component types in the application"""
        component_types = [
            'controller', 'service', 'repository', 'dao', 'entity', 'model', 
            'dto', 'vo', 'util', 'config', 'exception', 'validator',
            'servlet', 'filter', 'listener', 'interceptor'
        ]
        
        component_analysis = {}
        
        for component_type in component_types:
            try:
                results = self.connector.query_by_component_type(component_type, 12)
                
                components = []
                if results and results.get('documents'):
                    # Handle different result formats
                    documents = results['documents'] if isinstance(results['documents'][0], str) else results['documents'][0]
                    metadatas = results['metadatas'] if isinstance(results['metadatas'][0], dict) else results['metadatas'][0]
                    
                    for i, doc in enumerate(documents):
                        metadata = metadatas[i]
                        
                        component = {
                            'file_path': metadata.get('file_path', ''),
                            'class_name': metadata.get('class_name', ''),
                            'function_name': metadata.get('function_name', ''),
                            'architectural_layer': metadata.get('architectural_layer', ''),
                            'business_domain': metadata.get('business_domain', ''),
                            'database_interactions': metadata.get('database_interactions', 'False'),
                            'technology_stack': metadata.get('technology_stack', '[]'),
                            'design_patterns': metadata.get('design_patterns', '[]'),
                            'complexity_score': metadata.get('complexity_score', '1.0'),
                            'content_preview': doc[:250] + "..." if len(doc) > 250 else doc
                        }
                        
                        components.append(component)
                
                component_analysis[component_type] = components
                if components:
                    logger.info(f"Found {len(components)} {component_type} components")
                
            except Exception as e:
                logger.error(f"Error querying {component_type} components: {e}")
                component_analysis[component_type] = []
        
        return component_analysis
    
    def analyze_technology_stack(self) -> Dict[str, List[Dict[str, Any]]]:
        """Analyze technology stack usage across the application"""
        technologies = [
            'spring', 'hibernate', 'jpa', 'jsp', 'servlet', 'jdbc',
            'struts', 'mybatis', 'ejb', 'jsf', 'maven', 'gradle',
            'junit', 'log4j', 'slf4j', 'jackson', 'gson'
        ]
        
        tech_analysis = {}
        
        for tech in technologies:
            try:
                results = self.connector.query_by_technology_stack(tech, 10)
                
                tech_components = []
                if results and results.get('documents'):
                    # Handle different result formats based on query_by_technology_stack implementation
                    if isinstance(results.get('documents'), list) and results['documents']:
                        documents = results['documents']
                        metadatas = results.get('metadatas', [])
                        
                        for i, doc in enumerate(documents):
                            metadata = metadatas[i] if i < len(metadatas) else {}
                            
                            component = {
                                'file_path': metadata.get('file_path', ''),
                                'class_name': metadata.get('class_name', ''),
                                'component_type': metadata.get('component_type', ''),
                                'architectural_layer': metadata.get('architectural_layer', ''),
                                'content_preview': doc[:200] + "..." if len(doc) > 200 else doc
                            }
                            
                            tech_components.append(component)
                
                tech_analysis[tech] = tech_components
                if tech_components:
                    logger.info(f"Found {len(tech_components)} components using {tech}")
                
            except Exception as e:
                logger.error(f"Error analyzing technology {tech}: {e}")
                tech_analysis[tech] = []
        
        return tech_analysis
    
    def query_business_domains(self) -> Dict[str, List[Dict[str, Any]]]:
        """Query components by business domain"""
        # First, let's get all unique business domains
        try:
            all_results = self.connector.collection.get(include=['metadatas'])
            domains = set()
            
            for metadata in all_results.get('metadatas', []):
                domain = metadata.get('business_domain', '').strip()
                if domain and domain.lower() != 'unknown':
                    domains.add(domain)
            
            domain_analysis = {}
            
            for domain in list(domains)[:10]:  # Limit to first 10 domains
                try:
                    results = self.connector.query_by_business_domain(domain, 10)
                    
                    domain_components = []
                    if results and results.get('documents'):
                        # Handle different result formats
                        documents = results['documents'] if isinstance(results['documents'][0], str) else results['documents'][0]
                        metadatas = results['metadatas'] if isinstance(results['metadatas'][0], dict) else results['metadatas'][0]
                        
                        for i, doc in enumerate(documents):
                            metadata = metadatas[i]
                            
                            component = {
                                'file_path': metadata.get('file_path', ''),
                                'class_name': metadata.get('class_name', ''),
                                'component_type': metadata.get('component_type', ''),
                                'architectural_layer': metadata.get('architectural_layer', ''),
                                'primary_purpose': metadata.get('primary_purpose', ''),
                                'database_interactions': metadata.get('database_interactions', 'False'),
                                'content_preview': doc[:200] + "..." if len(doc) > 200 else doc
                            }
                            
                            domain_components.append(component)
                    
                    domain_analysis[domain] = domain_components
                    logger.info(f"Found {len(domain_components)} components in {domain} domain")
                    
                except Exception as e:
                    logger.error(f"Error querying domain {domain}: {e}")
                    domain_analysis[domain] = []
            
            return domain_analysis
            
        except Exception as e:
            logger.error(f"Error querying business domains: {e}")
            return {}
    
    def analyze_api_patterns(self) -> Dict[str, List[Dict[str, Any]]]:
        """Analyze API exposure and consumption patterns"""
        api_analysis = {
            'api_exposers': [],
            'api_consumers': [],
            'rest_endpoints': [],
            'soap_services': []
        }
        
        try:
            # Find API exposers
            exposers_result = self.connector.query_files_with_api_exposure(15)
            if exposers_result and exposers_result.get('documents'):
                documents = exposers_result['documents'] if isinstance(exposers_result['documents'][0], str) else exposers_result['documents'][0]
                metadatas = exposers_result['metadatas'] if isinstance(exposers_result['metadatas'][0], dict) else exposers_result['metadatas'][0]
                
                for i, doc in enumerate(documents):
                    metadata = metadatas[i]
                    
                    exposer = {
                        'file_path': metadata.get('file_path', ''),
                        'class_name': metadata.get('class_name', ''),
                        'component_type': metadata.get('component_type', ''),
                        'business_domain': metadata.get('business_domain', ''),
                        'content_preview': doc[:200] + "..." if len(doc) > 200 else doc
                    }
                    
                    api_analysis['api_exposers'].append(exposer)
            
            # Find REST endpoints
            rest_queries = ['@RestController @RequestMapping @GetMapping @PostMapping']
            for query in rest_queries:
                results = self.connector.query_enhanced_similar(query, 10)
                if results and results.get('documents') and results['documents'][0]:
                    for i, doc in enumerate(results['documents'][0]):
                        metadata = results['metadatas'][0][i]
                        
                        endpoint = {
                            'file_path': metadata.get('file_path', ''),
                            'class_name': metadata.get('class_name', ''),
                            'function_name': metadata.get('function_name', ''),
                            'query_matched': query,
                            'content_preview': doc[:200] + "..." if len(doc) > 200 else doc
                        }
                        
                        api_analysis['rest_endpoints'].append(endpoint)
            
            # Find SOAP services
            soap_queries = ['@WebService @WebMethod SOAP wsdl']
            for query in soap_queries:
                results = self.connector.query_enhanced_similar(query, 8)
                if results and results.get('documents') and results['documents'][0]:
                    for i, doc in enumerate(results['documents'][0]):
                        metadata = results['metadatas'][0][i]
                        
                        service = {
                            'file_path': metadata.get('file_path', ''),
                            'class_name': metadata.get('class_name', ''),
                            'function_name': metadata.get('function_name', ''),
                            'query_matched': query,
                            'content_preview': doc[:200] + "..." if len(doc) > 200 else doc
                        }
                        
                        api_analysis['soap_services'].append(service)
            
        except Exception as e:
            logger.error(f"Error analyzing API patterns: {e}")
        
        return api_analysis
    
    def generate_architecture_overview(self) -> Dict[str, Any]:
        """Generate a comprehensive architecture overview"""
        logger.info("Generating comprehensive architecture overview...")
        
        # Get database statistics first
        db_stats = self.connector.get_chunk_statistics()
        
        if db_stats.get('total_chunks', 0) == 0:
            return {
                'error': 'No data found in ChromaDB. Please run Step1.sh to process source files first.',
                'database_statistics': db_stats
            }
        
        overview = {
            'timestamp': str(os.popen('date').read().strip()),
            'database_statistics': db_stats,
            'architectural_layers': self.query_all_architectural_layers(),
            'component_types': self.query_all_component_types(),
            'technology_stack': self.analyze_technology_stack(),
            'business_domains': self.query_business_domains(),
            'api_patterns': self.analyze_api_patterns()
        }
        
        # Generate summary statistics
        overview['summary'] = self._generate_summary_statistics(overview)
        
        # Generate architectural insights
        overview['insights'] = self._generate_architectural_insights(overview)
        
        return overview
    
    def _generate_summary_statistics(self, overview: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary statistics from the analysis"""
        summary = {
            'total_architectural_layers': len([layer for layer, components in overview['architectural_layers'].items() if components]),
            'total_component_types': len([comp_type for comp_type, components in overview['component_types'].items() if components]),
            'total_technologies_used': len([tech for tech, components in overview['technology_stack'].items() if components]),
            'total_business_domains': len([domain for domain, components in overview['business_domains'].items() if components]),
            'total_api_exposers': len(overview['api_patterns']['api_exposers']),
            'total_rest_endpoints': len(overview['api_patterns']['rest_endpoints']),
            'total_soap_services': len(overview['api_patterns']['soap_services']),
            'database_enabled_components': 0
        }
        
        # Count database-enabled components
        for layer, components in overview['architectural_layers'].items():
            for component in components:
                if component.get('database_interactions') == 'True':
                    summary['database_enabled_components'] += 1
        
        return summary
    
    def _generate_architectural_insights(self, overview: Dict[str, Any]) -> Dict[str, Any]:
        """Generate architectural insights"""
        insights = {
            'dominant_architectural_pattern': 'unknown',
            'data_access_strategy': 'unknown',
            'api_strategy': 'unknown',
            'technology_modernization_score': 'unknown',
            'complexity_assessment': 'unknown'
        }
        
        # Analyze dominant architectural pattern
        layer_counts = {layer: len(components) for layer, components in overview['architectural_layers'].items() if components}
        if layer_counts:
            dominant_layer = max(layer_counts, key=layer_counts.get)
            if dominant_layer in ['presentation', 'controller']:
                insights['dominant_architectural_pattern'] = 'MVC/Layered'
            elif dominant_layer in ['service', 'business']:
                insights['dominant_architectural_pattern'] = 'Service-Oriented'
            elif dominant_layer in ['data', 'dao']:
                insights['dominant_architectural_pattern'] = 'Data-Centric'
        
        # Analyze data access strategy
        dao_components = len(overview['component_types'].get('dao', []))
        repository_components = len(overview['component_types'].get('repository', []))
        entity_components = len(overview['component_types'].get('entity', []))
        
        if dao_components > repository_components:
            insights['data_access_strategy'] = 'DAO Pattern'
        elif repository_components > 0:
            insights['data_access_strategy'] = 'Repository Pattern'
        elif entity_components > 0:
            insights['data_access_strategy'] = 'Entity-Based'
        
        # Analyze API strategy
        rest_count = len(overview['api_patterns']['rest_endpoints'])
        soap_count = len(overview['api_patterns']['soap_services'])
        
        if rest_count > soap_count and rest_count > 0:
            insights['api_strategy'] = 'REST-focused'
        elif soap_count > 0:
            insights['api_strategy'] = 'SOAP-focused'
        elif rest_count > 0 or soap_count > 0:
            insights['api_strategy'] = 'Hybrid'
        
        # Technology modernization score
        modern_techs = ['spring', 'jpa', 'hibernate']
        legacy_techs = ['ejb', 'struts', 'jsp']
        
        modern_count = sum(1 for tech in modern_techs if overview['technology_stack'].get(tech))
        legacy_count = sum(1 for tech in legacy_techs if overview['technology_stack'].get(tech))
        
        if modern_count > legacy_count:
            insights['technology_modernization_score'] = 'modern'
        elif legacy_count > modern_count:
            insights['technology_modernization_score'] = 'legacy'
        else:
            insights['technology_modernization_score'] = 'mixed'
        
        return insights

def main():
    """Main function to run comprehensive database analysis"""
    analyzer = ComprehensiveDatabaseAnalyzer()
    
    # Generate timestamp for output file
    timestamp = os.popen('date +"%Y%m%d_%H%M%S"').read().strip()
    output_file = f"./output/comprehensive_database_analysis_{timestamp}.json"
    
    # Ensure output directory exists
    os.makedirs('./output', exist_ok=True)
    
    try:
        # Generate comprehensive overview
        overview = analyzer.generate_architecture_overview()
        
        # Save to file
        with open(output_file, 'w') as f:
            json.dump(overview, f, indent=2, ensure_ascii=False)
        
        # Print summary to console
        if 'error' in overview:
            print(f"\n❌ {overview['error']}")
            print(f"Database Statistics: {json.dumps(overview['database_statistics'], indent=2)}")
            return
        
        print("\n=== Comprehensive Database Analysis Results ===")
        print(f"Database Statistics: {json.dumps(overview['database_statistics'], indent=2)}")
        print(f"\nSummary Statistics: {json.dumps(overview['summary'], indent=2)}")
        print(f"\nArchitectural Insights: {json.dumps(overview['insights'], indent=2)}")
        
        # Show architectural layers
        print(f"\n=== Architectural Layers ===")
        for layer, components in overview['architectural_layers'].items():
            if components:
                print(f"{layer}: {len(components)} components")
                for comp in components[:2]:  # Show first 2
                    print(f"  - {comp['class_name']} ({comp['file_path']})")
        
        # Show component types
        print(f"\n=== Component Types ===")
        for comp_type, components in overview['component_types'].items():
            if components:
                print(f"{comp_type}: {len(components)} components")
        
        # Show API patterns
        api_patterns = overview['api_patterns']
        print(f"\n=== API Patterns ===")
        print(f"API Exposers: {len(api_patterns['api_exposers'])}")
        print(f"REST Endpoints: {len(api_patterns['rest_endpoints'])}")
        print(f"SOAP Services: {len(api_patterns['soap_services'])}")
        
        print(f"\nFull analysis saved to: {output_file}")
        
    except Exception as e:
        logger.error(f"Error running comprehensive analysis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()