#!/usr/bin/env python3
"""
Enhanced Weaviate UI Processor for Iteration 14
Integrates UI analysis with the existing Enhanced Weaviate system
"""

import asyncio
import logging
import json
import os
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from enhanced_ui_file_processor import EnhancedUIFileProcessor
from weaviate_ui_schema import WeaviateUISchemaManager
from enhanced_weaviate_processor import EnhancedWeaviateProcessor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    import weaviate
    WEAVIATE_AVAILABLE = True
except ImportError as e:
    logger.warning(f"⚠️  Weaviate client not available: {e}. Using mock implementation.")
    WEAVIATE_AVAILABLE = False
    weaviate = None

class EnhancedWeaviateUIProcessor(EnhancedWeaviateProcessor):
    """Enhanced Weaviate processor with comprehensive UI analysis capabilities"""
    
    def __init__(self, java_root_path: str = ".", output_dir: str = "./output"):
        super().__init__(java_root_path, output_dir)
        self.ui_file_processor = EnhancedUIFileProcessor()
        self.ui_schema_manager = None
        self.ui_analysis_results = {}
        
    def initialize_ui_collections(self):
        """Initialize UI collections in Weaviate"""
        if not WEAVIATE_AVAILABLE:
            logger.warning("Weaviate not available - using mock UI collections")
            return True
            
        try:
            # Initialize UI schema manager
            self.ui_schema_manager = WeaviateUISchemaManager(self.weaviate_client)
            
            # Check if UI collections exist, delete if necessary for clean slate
            try:
                existing_collections = self.weaviate_client.schema.get()
                ui_collections = ['UIComponents', 'NavigationFlows']
                
                for collection in ui_collections:
                    if any(cls['class'] == collection for cls in existing_collections.get('classes', [])):
                        logger.info(f"Deleting existing {collection} collection for clean initialization")
                        self.weaviate_client.schema.delete_class(collection)
            except Exception as e:
                logger.warning(f"Could not check/delete existing UI collections: {e}")
            
            # Create new UI collections
            success = self.ui_schema_manager.create_ui_collections()
            
            if success:
                logger.info("✅ UI collections initialized successfully")
                return True
            else:
                logger.error("❌ Failed to initialize UI collections")
                return False
                
        except Exception as e:
            logger.error(f"Error initializing UI collections: {e}")
            return False
    
    async def process_with_ui_analysis(self, mode: str = "production") -> Dict[str, Any]:
        """Enhanced processing with comprehensive UI analysis"""
        
        logger.info(f"🚀 Starting Enhanced Weaviate UI Processing - Mode: {mode}")
        start_time = time.time()
        
        try:
            # Initialize UI collections
            if not self.initialize_ui_collections():
                raise Exception("Failed to initialize UI collections")
            
            # Process files with UI analysis
            logger.info("📁 Processing files with UI analysis...")
            ui_results = self.ui_file_processor.process_files_with_ui_analysis()
            self.ui_analysis_results = ui_results
            
            # Store UI analysis in Weaviate
            if WEAVIATE_AVAILABLE and self.ui_schema_manager:
                logger.info("💾 Storing UI analysis in Weaviate...")
                storage_stats = self.ui_schema_manager.store_ui_analysis_results(ui_results)
                logger.info(f"Storage Stats: {storage_stats}")
            
            # Run traditional data structure analysis
            logger.info("🔍 Running traditional data structure analysis...")
            traditional_results = await super().process_files(mode)
            
            # Combine results
            combined_results = {
                'ui_analysis': ui_results,
                'data_structure_analysis': traditional_results,
                'processing_metadata': {
                    'mode': mode,
                    'processing_time': time.time() - start_time,
                    'timestamp': datetime.now().isoformat(),
                    'ui_components_found': len(ui_results.get('ui_components', {})),
                    'navigation_flows_mapped': len(ui_results.get('navigation_flows', [])),
                    'data_structures_found': len(traditional_results.get('data_structures', {})) if traditional_results else 0
                }
            }
            
            # Generate comprehensive summary
            summary = self._generate_comprehensive_summary(combined_results)
            combined_results['summary'] = summary
            
            # Save results
            await self._save_combined_results(combined_results, mode)
            
            processing_time = time.time() - start_time
            logger.info(f"✅ Enhanced UI Processing complete in {processing_time:.2f} seconds")
            
            return combined_results
            
        except Exception as e:
            logger.error(f"❌ Error in enhanced UI processing: {e}")
            raise
    
    def _generate_comprehensive_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive summary combining UI and data analysis"""
        ui_analysis = results.get('ui_analysis', {})
        data_analysis = results.get('data_structure_analysis', {})
        metadata = results.get('processing_metadata', {})
        
        # UI Statistics
        ui_stats = ui_analysis.get('ui_statistics', {})
        ui_arch = ui_analysis.get('ui_architecture', {})
        ui_modern = ui_analysis.get('modernization_analysis', {})
        
        # Data Structure Statistics
        data_stats = data_analysis.get('summary', {}) if data_analysis else {}
        
        summary = {
            'overview': {
                'total_processing_time': f"{metadata.get('processing_time', 0):.2f} seconds",
                'processing_mode': metadata.get('mode', 'unknown'),
                'timestamp': metadata.get('timestamp', datetime.now().isoformat())
            },
            'file_processing': {
                'total_files_analyzed': ui_stats.get('total_files', 0),
                'ui_relevant_files': ui_stats.get('ui_files', 0),
                'java_components': ui_stats.get('java_components', 0),
                'uibinder_templates': ui_stats.get('uibinder_templates', 0),
                'gwt_modules': ui_stats.get('gwt_modules', 0),
                'css_files': ui_stats.get('css_files', 0),
                'javascript_files': ui_stats.get('js_files', 0)
            },
            'ui_architecture': {
                'total_ui_components': ui_arch.get('total_components', 0),
                'navigation_flows': ui_arch.get('total_navigation_flows', 0),
                'component_types': ui_arch.get('component_types', {}),
                'business_domains': ui_arch.get('business_domains', []),
                'gwt_widgets_catalog': len(ui_arch.get('gwt_widgets_used', []))
            },
            'data_structures': {
                'total_entities': data_stats.get('total_entities', 0),
                'data_structures_found': data_stats.get('data_structures', 0),
                'entity_relationships': data_stats.get('relationships', 0),
                'business_domains_data': data_stats.get('business_domains', [])
            },
            'modernization_assessment': {
                'high_priority_ui_components': ui_modern.get('high_priority_count', 0),
                'medium_priority_ui_components': ui_modern.get('medium_priority_count', 0),
                'low_priority_ui_components': ui_modern.get('low_priority_count', 0),
                'average_ui_complexity': ui_modern.get('average_complexity_score', 0),
                'critical_components': ui_modern.get('high_priority_components', [])
            },
            'integration_metrics': {
                'ui_to_data_coverage': self._calculate_ui_data_coverage(ui_analysis, data_analysis),
                'business_domain_alignment': self._analyze_domain_alignment(ui_analysis, data_analysis),
                'modernization_readiness': self._assess_modernization_readiness(ui_analysis, data_analysis)
            }
        }
        
        return summary
    
    def _calculate_ui_data_coverage(self, ui_analysis: Dict, data_analysis: Dict) -> Dict[str, Any]:
        """Calculate coverage between UI components and data structures"""
        ui_domains = set(ui_analysis.get('ui_architecture', {}).get('business_domains', []))
        data_domains = set(data_analysis.get('summary', {}).get('business_domains', []) if data_analysis else [])
        
        coverage = {
            'ui_domains': list(ui_domains),
            'data_domains': list(data_domains),
            'common_domains': list(ui_domains.intersection(data_domains)),
            'ui_only_domains': list(ui_domains - data_domains),
            'data_only_domains': list(data_domains - ui_domains),
            'coverage_percentage': len(ui_domains.intersection(data_domains)) / max(len(ui_domains.union(data_domains)), 1) * 100
        }
        
        return coverage
    
    def _analyze_domain_alignment(self, ui_analysis: Dict, data_analysis: Dict) -> Dict[str, Any]:
        """Analyze alignment between UI and data layer business domains"""
        ui_components = ui_analysis.get('ui_components', {})
        
        # Map UI components to their business domains
        domain_component_mapping = {}
        for component in ui_components.values():
            for domain in component.business_domains:
                if domain not in domain_component_mapping:
                    domain_component_mapping[domain] = []
                domain_component_mapping[domain].append(component.component_name)
        
        alignment = {
            'domain_component_mapping': domain_component_mapping,
            'domains_with_ui': list(domain_component_mapping.keys()),
            'ui_component_distribution': {domain: len(components) for domain, components in domain_component_mapping.items()}
        }
        
        return alignment
    
    def _assess_modernization_readiness(self, ui_analysis: Dict, data_analysis: Dict) -> Dict[str, Any]:
        """Assess overall modernization readiness"""
        ui_modern = ui_analysis.get('modernization_analysis', {})
        ui_arch = ui_analysis.get('ui_architecture', {})
        
        total_components = ui_arch.get('total_components', 0)
        high_priority = ui_modern.get('high_priority_count', 0)
        
        readiness_score = 0
        factors = []
        
        # UI Complexity Factor
        avg_complexity = ui_modern.get('average_complexity_score', 0)
        if avg_complexity < 30:
            readiness_score += 30
            factors.append("Low UI complexity favorable for migration")
        elif avg_complexity < 60:
            readiness_score += 20
            factors.append("Moderate UI complexity manageable for migration")
        else:
            readiness_score += 10
            factors.append("High UI complexity requires careful migration planning")
        
        # High Priority Components Factor
        if total_components > 0:
            high_priority_ratio = high_priority / total_components
            if high_priority_ratio < 0.3:
                readiness_score += 25
                factors.append("Low ratio of high-priority components")
            elif high_priority_ratio < 0.6:
                readiness_score += 15
                factors.append("Moderate ratio of high-priority components")
            else:
                readiness_score += 5
                factors.append("High ratio of high-priority components needs attention")
        
        # Component Diversity Factor
        component_types = len(ui_arch.get('component_types', {}))
        if component_types >= 4:
            readiness_score += 15
            factors.append("Good component diversity supports modern architecture")
        else:
            readiness_score += 10
            factors.append("Limited component diversity may simplify migration")
        
        # Navigation Complexity Factor
        nav_flows = ui_arch.get('total_navigation_flows', 0)
        if nav_flows < total_components:
            readiness_score += 15
            factors.append("Simple navigation patterns")
        else:
            readiness_score += 10
            factors.append("Complex navigation requires careful redesign")
        
        # Business Domain Coverage Factor
        domain_count = len(ui_arch.get('business_domains', []))
        if domain_count >= 4:
            readiness_score += 15
            factors.append("Comprehensive business domain coverage")
        else:
            readiness_score += 10
            factors.append("Focused business domain scope")
        
        # Determine readiness level
        if readiness_score >= 80:
            readiness_level = "High - Ready for comprehensive modernization"
        elif readiness_score >= 60:
            readiness_level = "Medium - Requires planning and phased approach"
        else:
            readiness_level = "Low - Significant challenges require careful strategy"
        
        return {
            'readiness_score': readiness_score,
            'readiness_level': readiness_level,
            'contributing_factors': factors,
            'recommendations': self._generate_readiness_recommendations(readiness_score, ui_analysis)
        }
    
    def _generate_readiness_recommendations(self, score: int, ui_analysis: Dict) -> List[str]:
        """Generate modernization readiness recommendations"""
        recommendations = []
        
        ui_modern = ui_analysis.get('modernization_analysis', {})
        
        if score >= 80:
            recommendations.extend([
                "Proceed with comprehensive modernization strategy",
                "Consider modern framework migration (React, Vue, Angular)",
                "Implement design system for consistency",
                "Plan parallel development approach"
            ])
        elif score >= 60:
            recommendations.extend([
                "Implement phased modernization approach",
                "Start with high-priority components",
                "Establish UI component library",
                "Plan gradual migration strategy"
            ])
        else:
            recommendations.extend([
                "Focus on technical debt reduction first",
                "Simplify complex components before migration",
                "Establish clear modernization roadmap",
                "Consider incremental improvements"
            ])
        
        # Add specific recommendations based on analysis
        high_priority = ui_modern.get('high_priority_count', 0)
        if high_priority > 10:
            recommendations.append(f"Address {high_priority} high-priority components first")
        
        return recommendations
    
    async def _save_combined_results(self, results: Dict[str, Any], mode: str):
        """Save combined UI and data analysis results"""
        output_dir = Path(self.ui_file_processor.output_dir)
        output_dir.mkdir(exist_ok=True)
        
        # Save comprehensive results
        results_file = output_dir / f"enhanced_ui_analysis_{mode}.json"
        
        try:
            # Make results serializable
            serializable_results = self.ui_file_processor._make_serializable(results)
            
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(serializable_results, f, indent=2, ensure_ascii=False)
            
            logger.info(f"💾 Saved combined results to: {results_file}")
            
        except Exception as e:
            logger.error(f"Error saving combined results: {e}")
    
    def get_enhanced_summary(self) -> str:
        """Get enhanced summary with UI analysis"""
        if not self.ui_analysis_results:
            return "No UI analysis results available"
        
        return self.ui_file_processor.get_ui_file_summary(self.ui_analysis_results)

# Main execution function for script usage
async def main():
    """Main function for standalone execution"""
    import sys
    
    mode = sys.argv[1] if len(sys.argv) > 1 else "production"
    
    processor = EnhancedWeaviateUIProcessor()
    
    try:
        results = await processor.process_with_ui_analysis(mode)
        
        # Print summary
        print("\n" + "="*80)
        print("ENHANCED WEAVIATE UI ANALYSIS COMPLETE")
        print("="*80)
        print(processor.get_enhanced_summary())
        print("\n" + "="*80)
        
        return 0
        
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)