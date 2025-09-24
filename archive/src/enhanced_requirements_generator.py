import os
import json
from typing import Dict, List, Any
from datetime import datetime

try:
    from metadata_grouping import MetadataGrouper
except ImportError:
    from .metadata_grouping import MetadataGrouper

class EnhancedRequirementsGenerator:
    """Generate requirements documents grouped by architectural classification"""
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.grouper = MetadataGrouper()
        
        # Create output directories
        self.requirements_dir = os.path.join(output_dir, 'requirements_enhanced')
        self.layer_dir = os.path.join(self.requirements_dir, 'by_layer')
        self.component_dir = os.path.join(self.requirements_dir, 'by_component')
        self.domain_dir = os.path.join(self.requirements_dir, 'by_domain')
        self.analysis_dir = os.path.join(self.requirements_dir, 'analysis')
        
        for directory in [self.requirements_dir, self.layer_dir, self.component_dir, self.domain_dir, self.analysis_dir]:
            os.makedirs(directory, exist_ok=True)
    
    def generate_grouped_requirements(self, metadata_list: List[Dict[str, Any]]):
        """Generate requirements documents grouped by classification"""
        
        # Filter successful analyses
        successful_metadata = [m for m in metadata_list if m.get('analysis_status') == 'completed_enhanced']
        
        if not successful_metadata:
            print("No successfully analyzed files found for requirements generation")
            return
        
        print(f"Generating enhanced requirements for {len(successful_metadata)} successfully analyzed files")
        
        # Group by architectural layer
        layer_groups = self.grouper.group_by_architectural_layer(successful_metadata)
        for layer, files in layer_groups.items():
            self.generate_layer_requirements(layer, files)
        
        # Group by component type
        component_groups = self.grouper.group_by_component_type(successful_metadata)
        for component_type, files in component_groups.items():
            self.generate_component_requirements(component_type, files)
        
        # Group by business domain
        domain_groups = self.grouper.group_by_business_domain(successful_metadata)
        for domain, files in domain_groups.items():
            if domain != 'unspecified':  # Skip unspecified domain
                self.generate_domain_requirements(domain, files)
        
        # Generate cross-cutting concerns
        self.generate_integration_analysis(successful_metadata)
        self.generate_security_analysis(successful_metadata)
        self.generate_performance_analysis(successful_metadata)
        self.generate_technology_analysis(successful_metadata)
        
        # Generate master index
        self.generate_master_index(successful_metadata)
    
    def generate_layer_requirements(self, layer: str, files: List[Dict[str, Any]]):
        """Generate requirements document for architectural layer"""
        if not files:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{layer}_requirements_{timestamp}.md"
        filepath = os.path.join(self.layer_dir, filename)
        
        md_content = f"# {layer.replace('_', ' ').title()} Layer Requirements\n\n"
        md_content += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        md_content += f"**Total files in this layer**: {len(files)}\n\n"
        
        # Summary statistics
        tech_usage = {}
        pattern_usage = {}
        api_exposing_count = 0
        db_interacting_count = 0
        
        for file_meta in files:
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            classification = enhanced_analysis.get('file_classification', {})
            
            # Count technologies
            for tech in classification.get('technology_stack', []):
                tech_usage[tech] = tech_usage.get(tech, 0) + 1
            
            # Count patterns
            for pattern in classification.get('design_patterns', []):
                pattern_usage[pattern] = pattern_usage.get(pattern, 0) + 1
            
            # Count API exposing files
            if classification.get('exposes_api', False):
                api_exposing_count += 1
            
            # Count DB interacting files
            if classification.get('database_interactions', False):
                db_interacting_count += 1
        
        md_content += f"## Layer Summary\n\n"
        md_content += f"- **API Exposing Files**: {api_exposing_count}\n"
        md_content += f"- **Database Interacting Files**: {db_interacting_count}\n"
        
        if tech_usage:
            md_content += f"- **Primary Technologies**: {', '.join(tech_usage.keys())}\n"
        
        if pattern_usage:
            md_content += f"- **Design Patterns Used**: {', '.join(pattern_usage.keys())}\n"
        
        md_content += f"\n"
        
        # Group by component type within layer
        component_groups = {}
        for file_meta in files:
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            classification = enhanced_analysis.get('file_classification', {})
            component_type = classification.get('component_type', 'unknown')
            
            if component_type not in component_groups:
                component_groups[component_type] = []
            component_groups[component_type].append(file_meta)
        
        # Generate component sections
        for component_type, component_files in component_groups.items():
            md_content += f"## {component_type.replace('_', ' ').title()} Components\n\n"
            md_content += f"**Files**: {len(component_files)}\n\n"
            
            for file_meta in component_files:
                file_path = file_meta.get('file_path', '')
                enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
                classification = enhanced_analysis.get('file_classification', {})
                
                md_content += f"### {os.path.basename(file_path)}\n\n"
                md_content += f"**Path**: `{file_path}`\n\n"
                md_content += f"**Primary Purpose**: {classification.get('primary_purpose', 'Not specified')}\n\n"
                
                if classification.get('business_domain'):
                    md_content += f"**Business Domain**: {classification.get('business_domain')}\n\n"
                
                if classification.get('technology_stack'):
                    md_content += f"**Technologies**: {', '.join(classification.get('technology_stack', []))}\n\n"
                
                if classification.get('design_patterns'):
                    md_content += f"**Design Patterns**: {', '.join(classification.get('design_patterns', []))}\n\n"
                
                if enhanced_analysis.get('purpose'):
                    md_content += f"**Detailed Purpose**: {enhanced_analysis.get('purpose')}\n\n"
                
                # Components
                components = enhanced_analysis.get('components', [])
                if components:
                    md_content += f"**Components**:\n"
                    for comp in components:
                        md_content += f"- **{comp.get('name', 'Unknown')}** ({comp.get('type', 'Unknown')}): {comp.get('description', 'No description')}\n"
                    md_content += f"\n"
                
                # Data structures
                data_structures = enhanced_analysis.get('data_structures', [])
                if data_structures:
                    md_content += f"**Data Structures**:\n"
                    for ds in data_structures:
                        md_content += f"- **{ds.get('name', 'Unknown')}**: Fields: {', '.join(ds.get('fields', []))}\n"
                    md_content += f"\n"
                
                # Business rules
                business_rules = enhanced_analysis.get('business_rules', [])
                if business_rules:
                    md_content += f"**Business Rules**:\n"
                    for rule in business_rules:
                        md_content += f"- {rule.get('description', 'No description')} (Location: {rule.get('location', 'Unknown')})\n"
                    md_content += f"\n"
                
                # Quality indicators
                complexity_indicators = classification.get('complexity_indicators', [])
                if complexity_indicators:
                    md_content += f"**Complexity Indicators**: {', '.join(complexity_indicators)}\n\n"
                
                potential_issues = classification.get('potential_issues', [])
                if potential_issues:
                    md_content += f"**Potential Issues**: {', '.join(potential_issues)}\n\n"
                
                refactoring_suggestions = classification.get('refactoring_suggestions', [])
                if refactoring_suggestions:
                    md_content += f"**Refactoring Suggestions**: {', '.join(refactoring_suggestions)}\n\n"
                
                md_content += f"---\n\n"
        
        # Write file
        with open(filepath, 'w') as f:
            f.write(md_content)
        
        print(f"Generated layer requirements: {filepath}")
    
    def generate_component_requirements(self, component_type: str, files: List[Dict[str, Any]]):
        """Generate requirements document for component type"""
        if not files:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{component_type}_requirements_{timestamp}.md"
        filepath = os.path.join(self.component_dir, filename)
        
        md_content = f"# {component_type.replace('_', ' ').title()} Component Requirements\n\n"
        md_content += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        md_content += f"**Total files of this component type**: {len(files)}\n\n"
        
        # Group by architectural layer
        layer_groups = {}
        for file_meta in files:
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            classification = enhanced_analysis.get('file_classification', {})
            layer = classification.get('architectural_layer', 'unknown')
            
            if layer not in layer_groups:
                layer_groups[layer] = []
            layer_groups[layer].append(file_meta)
        
        md_content += f"## Distribution Across Layers\n\n"
        for layer, layer_files in layer_groups.items():
            md_content += f"- **{layer.replace('_', ' ').title()}**: {len(layer_files)} files\n"
        md_content += f"\n"
        
        # Generate detailed file information
        for file_meta in files:
            file_path = file_meta.get('file_path', '')
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            classification = enhanced_analysis.get('file_classification', {})
            
            md_content += f"## {os.path.basename(file_path)}\n\n"
            md_content += f"**Path**: `{file_path}`\n\n"
            md_content += f"**Layer**: {classification.get('architectural_layer', 'unknown').replace('_', ' ').title()}\n\n"
            md_content += f"**Primary Purpose**: {classification.get('primary_purpose', 'Not specified')}\n\n"
            
            if enhanced_analysis.get('purpose'):
                md_content += f"**Detailed Purpose**: {enhanced_analysis.get('purpose')}\n\n"
            
            md_content += f"---\n\n"
        
        # Write file
        with open(filepath, 'w') as f:
            f.write(md_content)
        
        print(f"Generated component requirements: {filepath}")
    
    def generate_domain_requirements(self, domain: str, files: List[Dict[str, Any]]):
        """Generate requirements document for business domain"""
        if not files:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{domain.replace(' ', '_').lower()}_domain_requirements_{timestamp}.md"
        filepath = os.path.join(self.domain_dir, filename)
        
        md_content = f"# {domain.title()} Domain Requirements\n\n"
        md_content += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        md_content += f"**Total files in this domain**: {len(files)}\n\n"
        
        # Analyze domain characteristics
        layer_distribution = {}
        component_distribution = {}
        
        for file_meta in files:
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            classification = enhanced_analysis.get('file_classification', {})
            
            layer = classification.get('architectural_layer', 'unknown')
            component = classification.get('component_type', 'unknown')
            
            layer_distribution[layer] = layer_distribution.get(layer, 0) + 1
            component_distribution[component] = component_distribution.get(component, 0) + 1
        
        md_content += f"## Domain Architecture\n\n"
        md_content += f"**Layer Distribution**:\n"
        for layer, count in layer_distribution.items():
            md_content += f"- {layer.replace('_', ' ').title()}: {count} files\n"
        md_content += f"\n"
        
        md_content += f"**Component Distribution**:\n"
        for component, count in component_distribution.items():
            md_content += f"- {component.replace('_', ' ').title()}: {count} files\n"
        md_content += f"\n"
        
        # Generate file details
        for file_meta in files:
            file_path = file_meta.get('file_path', '')
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            
            md_content += f"## {os.path.basename(file_path)}\n\n"
            md_content += f"**Path**: `{file_path}`\n\n"
            
            if enhanced_analysis.get('purpose'):
                md_content += f"**Purpose**: {enhanced_analysis.get('purpose')}\n\n"
            
            md_content += f"---\n\n"
        
        # Write file
        with open(filepath, 'w') as f:
            f.write(md_content)
        
        print(f"Generated domain requirements: {filepath}")
    
    def generate_integration_analysis(self, metadata_list: List[Dict[str, Any]]):
        """Generate integration analysis document"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"integration_analysis_{timestamp}.md"
        filepath = os.path.join(self.analysis_dir, filename)
        
        api_exposing_files = self.grouper.filter_api_exposing_files(metadata_list)
        db_interacting_files = self.grouper.filter_database_interacting_files(metadata_list)
        
        md_content = f"# Integration Points Analysis\n\n"
        md_content += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        md_content += f"## API Exposing Components\n\n"
        md_content += f"**Total**: {len(api_exposing_files)} files\n\n"
        
        for file_meta in api_exposing_files:
            file_path = file_meta.get('file_path', '')
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            classification = enhanced_analysis.get('file_classification', {})
            
            md_content += f"### {os.path.basename(file_path)}\n"
            md_content += f"- **Path**: `{file_path}`\n"
            md_content += f"- **Component Type**: {classification.get('component_type', 'unknown')}\n"
            md_content += f"- **Purpose**: {classification.get('primary_purpose', 'Not specified')}\n\n"
        
        md_content += f"## Database Interacting Components\n\n"
        md_content += f"**Total**: {len(db_interacting_files)} files\n\n"
        
        for file_meta in db_interacting_files:
            file_path = file_meta.get('file_path', '')
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            classification = enhanced_analysis.get('file_classification', {})
            
            md_content += f"### {os.path.basename(file_path)}\n"
            md_content += f"- **Path**: `{file_path}`\n"
            md_content += f"- **Component Type**: {classification.get('component_type', 'unknown')}\n"
            md_content += f"- **Purpose**: {classification.get('primary_purpose', 'Not specified')}\n\n"
        
        # Write file
        with open(filepath, 'w') as f:
            f.write(md_content)
        
        print(f"Generated integration analysis: {filepath}")
    
    def generate_security_analysis(self, metadata_list: List[Dict[str, Any]]):
        """Generate security analysis document"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"security_analysis_{timestamp}.md"
        filepath = os.path.join(self.analysis_dir, filename)
        
        security_files = self.grouper.filter_by_architectural_layer(metadata_list, 'security')
        
        md_content = f"# Security Analysis\n\n"
        md_content += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        md_content += f"## Security Components\n\n"
        md_content += f"**Total**: {len(security_files)} files\n\n"
        
        # Collect security considerations
        all_security_considerations = set()
        
        for file_meta in metadata_list:
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            security_considerations = enhanced_analysis.get('security_considerations', [])
            all_security_considerations.update(security_considerations)
        
        if all_security_considerations:
            md_content += f"## Security Considerations Identified\n\n"
            for consideration in sorted(all_security_considerations):
                md_content += f"- {consideration}\n"
            md_content += f"\n"
        
        # Write file
        with open(filepath, 'w') as f:
            f.write(md_content)
        
        print(f"Generated security analysis: {filepath}")
    
    def generate_performance_analysis(self, metadata_list: List[Dict[str, Any]]):
        """Generate performance analysis document"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"performance_analysis_{timestamp}.md"
        filepath = os.path.join(self.analysis_dir, filename)
        
        md_content = f"# Performance Analysis\n\n"
        md_content += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Collect performance considerations
        all_performance_considerations = set()
        
        for file_meta in metadata_list:
            enhanced_analysis = file_meta.get('enhanced_ai_analysis', {})
            performance_considerations = enhanced_analysis.get('performance_considerations', [])
            all_performance_considerations.update(performance_considerations)
        
        if all_performance_considerations:
            md_content += f"## Performance Considerations Identified\n\n"
            for consideration in sorted(all_performance_considerations):
                md_content += f"- {consideration}\n"
            md_content += f"\n"
        
        # Write file
        with open(filepath, 'w') as f:
            f.write(md_content)
        
        print(f"Generated performance analysis: {filepath}")
    
    def generate_technology_analysis(self, metadata_list: List[Dict[str, Any]]):
        """Generate technology stack analysis document"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"technology_analysis_{timestamp}.md"
        filepath = os.path.join(self.analysis_dir, filename)
        
        architecture_report = self.grouper.generate_architecture_report(metadata_list)
        
        md_content = f"# Technology Stack Analysis\n\n"
        md_content += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        tech_usage = architecture_report.get('technology_analysis', {}).get('technology_stack', {})
        pattern_usage = architecture_report.get('technology_analysis', {}).get('design_patterns', {})
        framework_usage = architecture_report.get('technology_analysis', {}).get('frameworks_detected', {})
        
        if tech_usage:
            md_content += f"## Technology Stack Usage\n\n"
            for tech, count in sorted(tech_usage.items(), key=lambda x: x[1], reverse=True):
                md_content += f"- **{tech}**: {count} files\n"
            md_content += f"\n"
        
        if pattern_usage:
            md_content += f"## Design Pattern Usage\n\n"
            for pattern, count in sorted(pattern_usage.items(), key=lambda x: x[1], reverse=True):
                md_content += f"- **{pattern}**: {count} files\n"
            md_content += f"\n"
        
        if framework_usage:
            md_content += f"## Framework Detection\n\n"
            for framework, count in sorted(framework_usage.items(), key=lambda x: x[1], reverse=True):
                md_content += f"- **{framework}**: {count} files\n"
            md_content += f"\n"
        
        # Write file
        with open(filepath, 'w') as f:
            f.write(md_content)
        
        print(f"Generated technology analysis: {filepath}")
    
    def generate_master_index(self, metadata_list: List[Dict[str, Any]]):
        """Generate master index of all requirements documents"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"requirements_index_{timestamp}.md"
        filepath = os.path.join(self.requirements_dir, filename)
        
        architecture_report = self.grouper.generate_architecture_report(metadata_list)
        
        md_content = f"# Enhanced Requirements Documentation Index\n\n"
        md_content += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        md_content += f"## Summary\n\n"
        summary = architecture_report.get('summary', {})
        md_content += f"- **Total Files Analyzed**: {summary.get('total_files', 0)}\n"
        md_content += f"- **Average Confidence Score**: {summary.get('average_confidence_score', 0)}\n"
        md_content += f"- **Files with API Exposure**: {summary.get('files_with_api_exposure', 0)}\n"
        md_content += f"- **Files with Database Interaction**: {summary.get('files_with_db_interaction', 0)}\n\n"
        
        md_content += f"## Generated Documents\n\n"
        md_content += f"### By Architectural Layer\n"
        
        layers = architecture_report.get('architectural_distribution', {}).get('layers', {})
        for layer, count in layers.items():
            if count > 0:
                md_content += f"- [{layer.replace('_', ' ').title()} Layer Requirements](by_layer/{layer}_requirements_*.md) ({count} files)\n"
        md_content += f"\n"
        
        md_content += f"### By Component Type\n"
        components = architecture_report.get('architectural_distribution', {}).get('components', {})
        for component, count in components.items():
            if count > 0:
                md_content += f"- [{component.replace('_', ' ').title()} Component Requirements](by_component/{component}_requirements_*.md) ({count} files)\n"
        md_content += f"\n"
        
        md_content += f"### Analysis Reports\n"
        md_content += f"- [Integration Analysis](analysis/integration_analysis_*.md)\n"
        md_content += f"- [Security Analysis](analysis/security_analysis_*.md)\n"
        md_content += f"- [Performance Analysis](analysis/performance_analysis_*.md)\n"
        md_content += f"- [Technology Analysis](analysis/technology_analysis_*.md)\n\n"
        
        # Write file
        with open(filepath, 'w') as f:
            f.write(md_content)
        
        print(f"Generated requirements index: {filepath}")