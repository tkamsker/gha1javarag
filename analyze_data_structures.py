#!/usr/bin/env python3
"""
Data Structures and Business Rules Analysis Script
Deep analysis of data models, entities, and business logic patterns
"""

import sys
import os
import json
import re
import logging
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
from collections import defaultdict
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from weaviate_connector import EnhancedWeaviateConnector

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataStructuresAnalyzer:
    """Advanced analyzer for data structures, entities, and business rules"""
    
    def __init__(self):
        load_dotenv()
        self.connector = EnhancedWeaviateConnector()
        
    async def extract_entity_relationships(self) -> Dict[str, List[Dict[str, Any]]]:
        """Extract entity relationships and associations"""
        relationship_patterns = {
            'one_to_many': ['@OneToMany', 'List<', 'Set<', 'Collection<', 'hasMany'],
            'many_to_one': ['@ManyToOne', 'foreign key', 'belongsTo', 'references'],
            'many_to_many': ['@ManyToMany', 'join table', 'cross reference'],
            'one_to_one': ['@OneToOne', 'unique foreign key', 'hasOne'],
            'inheritance': ['extends', 'implements', '@Inheritance', 'super class'],
            'composition': ['private.*new', 'has-a relationship', 'composed of'],
            'aggregation': ['List<.*>', 'Set<.*>', 'Map<.*>', 'contains']
        }
        
        relationships = defaultdict(list)
        
        for relationship_type, patterns in relationship_patterns.items():
            for pattern in patterns:
                try:
                    # Use Weaviate semantic search
                    query_result = await self.connector.semantic_search(
                        query=pattern,
                        limit=10,
                        where_filter=None
                    )
                    
                    if query_result and query_result.objects:
                        for obj in query_result.objects:
                            properties = obj.get('properties', {})
                            content = properties.get('content', '')
                            
                            relationship = {
                                'relationship_type': relationship_type,
                                'pattern_matched': pattern,
                                'source_entity': properties.get('class_name', ''),
                                'file_path': properties.get('file_path', ''),
                                'function_name': properties.get('method_name', ''),
                                'content_preview': content[:200] + "..." if len(content) > 200 else content,
                                'extracted_entities': self._extract_entity_names_from_content(content),
                                'annotations': self._extract_annotations_from_content(content)
                            }
                            
                            relationships[relationship_type].append(relationship)
                            
                except Exception as e:
                    logger.error(f"Error analyzing relationship pattern '{pattern}': {e}")
                    continue
        
        return dict(relationships)
    
    def _extract_entity_names_from_content(self, content: str) -> List[str]:
        """Extract entity/class names from code content"""
        entity_patterns = [
            r'class\s+(\w+)',  # class definitions
            r'@Entity.*?class\s+(\w+)',  # JPA entities
            r'@Table\(name\s*=\s*["\'](\w+)["\']',  # table names
            r'List<(\w+)>',  # generic types
            r'Set<(\w+)>',
            r'Map<\w+,\s*(\w+)>',
            r'private\s+(\w+)\s+\w+',  # field types
        ]
        
        entities = set()
        for pattern in entity_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            entities.update(matches)
        
        # Filter out common Java keywords and primitives
        java_keywords = {'String', 'Integer', 'Long', 'Double', 'Boolean', 'Date', 'Object', 'void', 'int', 'long', 'double', 'boolean'}
        return [entity for entity in entities if entity not in java_keywords and len(entity) > 2]
    
    def _extract_annotations_from_content(self, content: str) -> List[str]:
        """Extract annotations from code content"""
        annotation_pattern = r'@(\w+)(?:\([^)]*\))?'
        annotations = re.findall(annotation_pattern, content)
        return list(set(annotations))
    
    async def analyze_data_validation_rules(self) -> List[Dict[str, Any]]:
        """Analyze data validation and business rules"""
        validation_queries = [
            'validation constraint NotNull NotEmpty Size',
            'validation rule check validate',
            'if.*null.*throw Exception',
            'business rule constraint policy',
            'Assert.*validate.*condition',
            'Pattern RegExp regular expression',
            'Min Max Range validation',
            'Custom validation annotation'
        ]
        
        validation_rules = []
        
        for query in validation_queries:
            try:
                query_result = await self.connector.semantic_search(
                    query=query,
                    limit=8,
                    where_filter=None
                )
                
                if query_result and query_result.objects:
                    for obj in query_result.objects:
                        properties = obj.get('properties', {})
                        content = properties.get('content', '')
                        
                        rule = {
                            'validation_type': query,
                            'file_path': properties.get('file_path', ''),
                            'class_name': properties.get('class_name', ''),
                            'function_name': properties.get('method_name', ''),
                            'complexity_score': float(properties.get('complexity_score', 1.0)),
                            'business_domain': properties.get('business_domain', ''),
                            'validation_annotations': self._extract_validation_annotations(content),
                            'validation_logic': self._extract_validation_logic(content),
                            'content_snippet': content[:300] + "..." if len(content) > 300 else content
                        }
                        
                        validation_rules.append(rule)
                        
            except Exception as e:
                logger.error(f"Error analyzing validation for '{query}': {e}")
                continue
        
        return validation_rules
    
    def _extract_validation_annotations(self, content: str) -> List[str]:
        """Extract validation-specific annotations"""
        validation_annotations = [
            'NotNull', 'NotEmpty', 'NotBlank', 'Size', 'Min', 'Max',
            'Pattern', 'Email', 'Valid', 'AssertTrue', 'AssertFalse',
            'DecimalMin', 'DecimalMax', 'Digits', 'Future', 'Past'
        ]
        
        found_annotations = []
        for annotation in validation_annotations:
            if f'@{annotation}' in content:
                found_annotations.append(annotation)
        
        return found_annotations
    
    def _extract_validation_logic(self, content: str) -> List[str]:
        """Extract validation logic patterns"""
        validation_patterns = [
            r'if\s*\(\s*.*\s*==\s*null.*\)',
            r'if\s*\(\s*.*\.isEmpty\(\).*\)',
            r'if\s*\(\s*.*\.length\(\)\s*[<>]=?.*\)',
            r'throw new.*Exception\(',
            r'Assert\..*\(',
            r'validate.*\(',
            r'check.*\('
        ]
        
        logic_found = []
        for pattern in validation_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
            logic_found.extend(matches)
        
        return logic_found[:5]  # Limit to avoid too much detail
    
    async def analyze_database_schema_patterns(self) -> Dict[str, List[Dict[str, Any]]]:
        """Analyze database schema and mapping patterns"""
        schema_patterns = {
            'table_definitions': ['@Table @Entity CREATE TABLE'],
            'primary_keys': ['@Id @GeneratedValue PRIMARY KEY'],
            'foreign_keys': ['@ManyToOne @OneToMany FOREIGN KEY REFERENCES'],
            'indexes': ['@Index CREATE INDEX'],
            'constraints': ['@Column unique nullable length CHECK CONSTRAINT'],
            'sequences': ['@SequenceGenerator @GeneratedValue SEQUENCE'],
            'stored_procedures': ['@NamedStoredProcedureQuery CALL EXEC'],
            'triggers': ['TRIGGER BEFORE AFTER INSERT UPDATE DELETE']
        }
        
        schema_analysis = {}
        
        for pattern_type, queries in schema_patterns.items():
            pattern_results = []
            
            for query in queries:
                try:
                    query_result = await self.connector.semantic_search(
                        query=query,
                        limit=8,
                        where_filter=None
                    )
                    
                    if query_result and query_result.objects:
                        for obj in query_result.objects:
                            properties = obj.get('properties', {})
                            content = properties.get('content', '')
                            
                            schema_element = {
                                'query_matched': query,
                                'file_path': properties.get('file_path', ''),
                                'class_name': properties.get('class_name', ''),
                                'table_name': self._extract_table_name(content),
                                'column_definitions': self._extract_column_definitions(content),
                                'constraints': self._extract_constraints(content),
                                'content_preview': content[:250] + "..." if len(content) > 250 else content
                            }
                            
                            pattern_results.append(schema_element)
                            
                except Exception as e:
                    logger.error(f"Error analyzing schema pattern '{query}': {e}")
                    continue
            
            schema_analysis[pattern_type] = pattern_results
        
        return schema_analysis
    
    def _extract_table_name(self, content: str) -> str:
        """Extract table name from content"""
        table_patterns = [
            r'@Table\s*\(\s*name\s*=\s*["\'](\w+)["\']',
            r'CREATE\s+TABLE\s+(\w+)',
            r'FROM\s+(\w+)',
            r'INSERT\s+INTO\s+(\w+)'
        ]
        
        for pattern in table_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return ''
    
    def _extract_column_definitions(self, content: str) -> List[Dict[str, str]]:
        """Extract column definitions from content"""
        column_patterns = [
            r'@Column\s*\([^)]*name\s*=\s*["\'](\w+)["\'][^)]*\)',
            r'private\s+(\w+)\s+(\w+);',
            r'(\w+)\s+(\w+)\s+(?:NOT\s+NULL|NULL)'
        ]
        
        columns = []
        for pattern in column_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if len(match) >= 2:
                    columns.append({
                        'name': match[1] if len(match) > 1 else match[0],
                        'type': match[0] if len(match) > 1 else 'unknown'
                    })
        
        return columns[:10]  # Limit to avoid too much detail
    
    def _extract_constraints(self, content: str) -> List[str]:
        """Extract database constraints"""
        constraint_patterns = [
            r'@Column\s*\([^)]*nullable\s*=\s*(false|true)[^)]*\)',
            r'@Column\s*\([^)]*unique\s*=\s*(false|true)[^)]*\)',
            r'@Column\s*\([^)]*length\s*=\s*(\d+)[^)]*\)',
            r'CHECK\s*\([^)]+\)',
            r'UNIQUE\s*\([^)]+\)',
            r'NOT\s+NULL',
            r'PRIMARY\s+KEY',
            r'FOREIGN\s+KEY'
        ]
        
        constraints = []
        for pattern in constraint_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            constraints.extend([str(match) for match in matches])
        
        return constraints[:8]  # Limit to most relevant
    
    async def generate_entity_relationship_diagram_data(self) -> Dict[str, Any]:
        """Generate data for creating entity relationship diagrams"""
        relationships = await self.extract_entity_relationships()
        
        # Extract unique entities
        entities = set()
        connections = []
        
        for rel_type, rel_list in relationships.items():
            for rel in rel_list:
                source = rel.get('source_entity', '')
                if source:
                    entities.add(source)
                
                for target in rel.get('extracted_entities', []):
                    entities.add(target)
                    if source and target:
                        connections.append({
                            'source': source,
                            'target': target,
                            'relationship_type': rel_type,
                            'file_path': rel.get('file_path', '')
                        })
        
        return {
            'entities': list(entities),
            'relationships': connections,
            'entity_count': len(entities),
            'relationship_count': len(connections)
        }
    
    async def generate_comprehensive_analysis(self, output_file: str = None) -> Dict[str, Any]:
        """Generate comprehensive data structures and business rules analysis"""
        logger.info("Starting comprehensive data structures analysis...")
        
        analysis = {
            'timestamp': str(os.popen('date').read().strip()),
            'entity_relationships': await self.extract_entity_relationships(),
            'data_validation_rules': await self.analyze_data_validation_rules(),
            'database_schema_patterns': await self.analyze_database_schema_patterns(),
            'entity_relationship_diagram': await self.generate_entity_relationship_diagram_data()
        }
        
        # Add summary statistics
        total_relationships = sum(len(rels) for rels in analysis['entity_relationships'].values())
        
        analysis['summary_statistics'] = {
            'total_entity_relationships': total_relationships,
            'validation_rules_found': len(analysis['data_validation_rules']),
            'unique_entities_identified': analysis['entity_relationship_diagram']['entity_count'],
            'entity_connections': analysis['entity_relationship_diagram']['relationship_count'],
            'relationship_types': list(analysis['entity_relationships'].keys()),
            'schema_pattern_types': list(analysis['database_schema_patterns'].keys())
        }
        
        # Generate insights
        analysis['insights'] = self._generate_insights(analysis)
        
        if output_file:
            try:
                with open(output_file, 'w') as f:
                    json.dump(analysis, f, indent=2, ensure_ascii=False)
                logger.info(f"Analysis saved to: {output_file}")
            except Exception as e:
                logger.error(f"Error saving analysis: {e}")
        
        return analysis
    
    def _generate_insights(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate insights from the analysis data"""
        insights = {
            'most_common_relationship_type': '',
            'most_complex_validation_rules': [],
            'entities_with_most_relationships': [],
            'validation_coverage': 'unknown',
            'data_model_complexity': 'unknown'
        }
        
        # Find most common relationship type
        rel_counts = {rel_type: len(rels) for rel_type, rels in analysis['entity_relationships'].items()}
        if rel_counts:
            insights['most_common_relationship_type'] = max(rel_counts, key=rel_counts.get)
        
        # Find most complex validation rules
        validation_rules = analysis['data_validation_rules']
        if validation_rules:
            complex_rules = sorted(validation_rules, key=lambda x: x.get('complexity_score', 0), reverse=True)[:5]
            insights['most_complex_validation_rules'] = [
                {
                    'class': rule.get('class_name', ''),
                    'function': rule.get('function_name', ''),
                    'complexity': rule.get('complexity_score', 0),
                    'file': rule.get('file_path', '')
                }
                for rule in complex_rules
            ]
        
        # Analyze validation coverage
        total_entities = analysis['entity_relationship_diagram']['entity_count']
        validated_entities = len(set(rule.get('class_name', '') for rule in validation_rules if rule.get('class_name')))
        
        if total_entities > 0:
            coverage_ratio = validated_entities / total_entities
            if coverage_ratio > 0.8:
                insights['validation_coverage'] = 'high'
            elif coverage_ratio > 0.5:
                insights['validation_coverage'] = 'medium'
            else:
                insights['validation_coverage'] = 'low'
        
        # Assess data model complexity
        relationship_count = analysis['entity_relationship_diagram']['relationship_count']
        entity_count = analysis['entity_relationship_diagram']['entity_count']
        
        if entity_count > 0:
            complexity_ratio = relationship_count / entity_count
            if complexity_ratio > 2:
                insights['data_model_complexity'] = 'high'
            elif complexity_ratio > 1:
                insights['data_model_complexity'] = 'medium'
            else:
                insights['data_model_complexity'] = 'low'
        
        return insights

async def main():
    """Main function to run data structures analysis"""
    analyzer = DataStructuresAnalyzer()
    
    # Generate timestamp for output file
    timestamp = os.popen('date +"%Y%m%d_%H%M%S"').read().strip()
    output_file = f"./output/data_structures_analysis_{timestamp}.json"
    
    # Ensure output directory exists
    os.makedirs('./output', exist_ok=True)
    
    try:
        # Generate comprehensive analysis
        analysis = await analyzer.generate_comprehensive_analysis(output_file)
        
        # Print summary to console
        print("\n=== Data Structures and Business Rules Analysis ===")
        print(f"Summary Statistics: {json.dumps(analysis['summary_statistics'], indent=2)}")
        print(f"\nInsights: {json.dumps(analysis['insights'], indent=2)}")
        
        # Show entity relationships
        if analysis['entity_relationships']:
            print(f"\n=== Entity Relationships Found ===")
            for rel_type, relationships in analysis['entity_relationships'].items():
                if relationships:
                    print(f"\n{rel_type.upper()} ({len(relationships)} instances):")
                    for rel in relationships[:3]:  # Show first 3
                        print(f"  - {rel['source_entity']} -> {rel.get('extracted_entities', [])} in {rel['file_path']}")
        
        # Show validation rules
        if analysis['data_validation_rules']:
            print(f"\n=== Data Validation Rules ({len(analysis['data_validation_rules'])}) ===")
            for rule in analysis['data_validation_rules'][:3]:  # Show first 3
                print(f"  - {rule['class_name']}.{rule['function_name']}: {rule['validation_annotations']}")
        
        # Show ERD data
        erd_data = analysis['entity_relationship_diagram']
        print(f"\n=== Entity Relationship Diagram Data ===")
        print(f"Entities ({erd_data['entity_count']}): {erd_data['entities'][:10]}...")  # Show first 10
        print(f"Connections: {erd_data['relationship_count']}")
        
        print(f"\nFull analysis saved to: {output_file}")
        
    except Exception as e:
        logger.error(f"Error running analysis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())