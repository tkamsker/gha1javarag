import json
from typing import Dict, List, Any
from collections import defaultdict

try:
    from metadata_schemas import ArchitecturalLayer, ComponentType
except ImportError:
    from .metadata_schemas import ArchitecturalLayer, ComponentType

class MetadataGrouper:
    """Groups and filters files based on enhanced classification"""
    
    @staticmethod
    def group_by_architectural_layer(metadata_list: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group files by architectural layer"""
        groups = defaultdict(list)
        
        for file_meta in metadata_list:
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            classification = enhanced_analysis.get('file_classification', {})
            layer = classification.get('architectural_layer', 'unknown')
            groups[layer].append(file_meta)
        
        return dict(groups)
    
    @staticmethod
    def group_by_component_type(metadata_list: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group files by component type"""
        groups = defaultdict(list)
        
        for file_meta in metadata_list:
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            classification = enhanced_analysis.get('file_classification', {})
            component_type = classification.get('component_type', 'unknown')
            groups[component_type].append(file_meta)
        
        return dict(groups)
    
    @staticmethod
    def group_by_business_domain(metadata_list: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group files by business domain"""
        groups = defaultdict(list)
        
        for file_meta in metadata_list:
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            classification = enhanced_analysis.get('file_classification', {})
            domain = classification.get('business_domain') or 'unspecified'
            groups[domain].append(file_meta)
        
        return dict(groups)
    
    @staticmethod
    def filter_by_technology_stack(metadata_list: List[Dict[str, Any]], 
                                  technology: str) -> List[Dict[str, Any]]:
        """Filter files by technology stack"""
        filtered = []
        
        for file_meta in metadata_list:
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            classification = enhanced_analysis.get('file_classification', {})
            tech_stack = classification.get('technology_stack', [])
            
            if technology.lower() in [tech.lower() for tech in tech_stack]:
                filtered.append(file_meta)
        
        return filtered
    
    @staticmethod
    def filter_high_complexity(metadata_list: List[Dict[str, Any]], 
                              min_confidence: float = 0.7) -> List[Dict[str, Any]]:
        """Filter files with complexity indicators"""
        filtered = []
        
        for file_meta in metadata_list:
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            classification = enhanced_analysis.get('file_classification', {})
            
            confidence = classification.get('confidence_score', 0.0)
            complexity_indicators = classification.get('complexity_indicators', [])
            
            if confidence >= min_confidence and complexity_indicators:
                filtered.append(file_meta)
        
        return filtered
    
    @staticmethod
    def filter_by_architectural_layer(metadata_list: List[Dict[str, Any]], 
                                    layer: str) -> List[Dict[str, Any]]:
        """Filter files by architectural layer"""
        filtered = []
        
        for file_meta in metadata_list:
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            classification = enhanced_analysis.get('file_classification', {})
            
            if classification.get('architectural_layer') == layer:
                filtered.append(file_meta)
        
        return filtered
    
    @staticmethod
    def filter_by_component_type(metadata_list: List[Dict[str, Any]], 
                               component_type: str) -> List[Dict[str, Any]]:
        """Filter files by component type"""
        filtered = []
        
        for file_meta in metadata_list:
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            classification = enhanced_analysis.get('file_classification', {})
            
            if classification.get('component_type') == component_type:
                filtered.append(file_meta)
        
        return filtered
    
    @staticmethod
    def filter_api_exposing_files(metadata_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter files that expose APIs"""
        filtered = []
        
        for file_meta in metadata_list:
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            classification = enhanced_analysis.get('file_classification', {})
            
            if classification.get('exposes_api', False):
                filtered.append(file_meta)
        
        return filtered
    
    @staticmethod
    def filter_database_interacting_files(metadata_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter files that interact with database"""
        filtered = []
        
        for file_meta in metadata_list:
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            classification = enhanced_analysis.get('file_classification', {})
            
            if classification.get('database_interactions', False):
                filtered.append(file_meta)
        
        return filtered
    
    @staticmethod
    def generate_architecture_report(metadata_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive architecture report"""
        layer_groups = MetadataGrouper.group_by_architectural_layer(metadata_list)
        component_groups = MetadataGrouper.group_by_component_type(metadata_list)
        domain_groups = MetadataGrouper.group_by_business_domain(metadata_list)
        
        # Technology analysis
        tech_usage = defaultdict(int)
        pattern_usage = defaultdict(int)
        framework_usage = defaultdict(int)
        
        # Quality metrics
        total_confidence = 0
        confidence_count = 0
        complexity_indicators_count = defaultdict(int)
        potential_issues_count = defaultdict(int)
        
        for file_meta in metadata_list:
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            classification = enhanced_analysis.get('file_classification', {})
            
            # Technology stack analysis
            for tech in classification.get('technology_stack', []):
                tech_usage[tech] += 1
            
            # Design pattern analysis
            for pattern in classification.get('design_patterns', []):
                pattern_usage[pattern] += 1
            
            # Framework analysis
            for framework in classification.get('frameworks_detected', []):
                framework_usage[framework] += 1
            
            # Quality metrics
            confidence = classification.get('confidence_score', 0)
            if confidence > 0:
                total_confidence += confidence
                confidence_count += 1
            
            # Complexity indicators
            for indicator in classification.get('complexity_indicators', []):
                complexity_indicators_count[indicator] += 1
            
            # Potential issues
            for issue in classification.get('potential_issues', []):
                potential_issues_count[issue] += 1
        
        # Calculate average confidence
        avg_confidence = total_confidence / confidence_count if confidence_count > 0 else 0
        
        return {
            'summary': {
                'total_files': len(metadata_list),
                'average_confidence_score': round(avg_confidence, 3),
                'files_analyzed': confidence_count,
                'files_with_api_exposure': len(MetadataGrouper.filter_api_exposing_files(metadata_list)),
                'files_with_db_interaction': len(MetadataGrouper.filter_database_interacting_files(metadata_list))
            },
            'architectural_distribution': {
                'layers': {layer: len(files) for layer, files in layer_groups.items()},
                'components': {comp: len(files) for comp, files in component_groups.items()},
                'business_domains': {domain: len(files) for domain, files in domain_groups.items()}
            },
            'technology_analysis': {
                'technology_stack': dict(tech_usage),
                'design_patterns': dict(pattern_usage),
                'frameworks_detected': dict(framework_usage)
            },
            'quality_metrics': {
                'complexity_indicators': dict(complexity_indicators_count),
                'potential_issues': dict(potential_issues_count),
                'high_complexity_files': len(MetadataGrouper.filter_high_complexity(metadata_list))
            },
            'detailed_breakdown': {
                'by_layer': {layer: [f.get('file_path', 'unknown') for f in files] 
                           for layer, files in layer_groups.items()},
                'by_component': {comp: [f.get('file_path', 'unknown') for f in files] 
                               for comp, files in component_groups.items()}
            }
        }
    
    @staticmethod
    def generate_layer_summary(metadata_list: List[Dict[str, Any]], layer: str) -> Dict[str, Any]:
        """Generate detailed summary for a specific architectural layer"""
        layer_files = MetadataGrouper.filter_by_architectural_layer(metadata_list, layer)
        
        if not layer_files:
            return {'error': f'No files found in layer: {layer}'}
        
        component_breakdown = defaultdict(list)
        tech_stack = defaultdict(int)
        design_patterns = defaultdict(int)
        
        for file_meta in layer_files:
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            classification = enhanced_analysis.get('file_classification', {})
            
            component_type = classification.get('component_type', 'unknown')
            component_breakdown[component_type].append(file_meta.get('file_path', 'unknown'))
            
            for tech in classification.get('technology_stack', []):
                tech_stack[tech] += 1
            
            for pattern in classification.get('design_patterns', []):
                design_patterns[pattern] += 1
        
        return {
            'layer': layer,
            'total_files': len(layer_files),
            'component_breakdown': dict(component_breakdown),
            'component_counts': {comp: len(files) for comp, files in component_breakdown.items()},
            'technology_usage': dict(tech_stack),
            'design_patterns': dict(design_patterns),
            'files': [f.get('file_path', 'unknown') for f in layer_files]
        }
    
    @staticmethod
    def find_related_files(metadata_list: List[Dict[str, Any]], 
                          target_file: str, 
                          relationship_types: List[str] = None) -> List[Dict[str, Any]]:
        """Find files related to a target file based on various relationship types"""
        if relationship_types is None:
            relationship_types = ['same_domain', 'same_layer', 'same_component_type', 'shared_dependencies']
        
        target_meta = None
        for file_meta in metadata_list:
            if file_meta.get('file_path') == target_file:
                target_meta = file_meta
                break
        
        if not target_meta:
            return []
        
        target_analysis = target_meta.get('enhanced_ai_analysis', {})
        target_classification = target_analysis.get('file_classification', {})
        
        related_files = []
        
        for file_meta in metadata_list:
            if file_meta.get('file_path') == target_file:
                continue  # Skip the target file itself
            
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            classification = enhanced_analysis.get('file_classification', {})
            
            relationship_score = 0
            relationships = []
            
            if 'same_domain' in relationship_types:
                if (target_classification.get('business_domain') and 
                    target_classification.get('business_domain') == classification.get('business_domain')):
                    relationship_score += 3
                    relationships.append('same_business_domain')
            
            if 'same_layer' in relationship_types:
                if target_classification.get('architectural_layer') == classification.get('architectural_layer'):
                    relationship_score += 2
                    relationships.append('same_architectural_layer')
            
            if 'same_component_type' in relationship_types:
                if target_classification.get('component_type') == classification.get('component_type'):
                    relationship_score += 2
                    relationships.append('same_component_type')
            
            if 'shared_dependencies' in relationship_types:
                target_deps = set(target_classification.get('dependencies', []))
                file_deps = set(classification.get('dependencies', []))
                shared_deps = target_deps.intersection(file_deps)
                if shared_deps:
                    relationship_score += len(shared_deps)
                    relationships.append(f'shared_dependencies: {list(shared_deps)}')
            
            if relationship_score > 0:
                related_files.append({
                    'file_path': file_meta.get('file_path'),
                    'relationship_score': relationship_score,
                    'relationships': relationships,
                    'metadata': file_meta
                })
        
        # Sort by relationship score (descending)
        related_files.sort(key=lambda x: x['relationship_score'], reverse=True)
        
        return related_files