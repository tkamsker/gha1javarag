import asyncio
import json
import os
from typing import Dict, Any, List
from dotenv import load_dotenv
import logging

try:
    from file_processor import FileProcessor
    from enhanced_ai_analyzer import EnhancedAIAnalyzer
    from chromadb_connector import EnhancedChromaDBConnector
    from requirements_analyzer import RequirementsAnalyzer
    from metadata_grouping import MetadataGrouper
    from logger_config import setup_logging
    from rate_limiter import RateLimiter, RateLimitConfig
    from ai_providers import create_ai_provider
except ImportError:
    from .file_processor import FileProcessor
    from .enhanced_ai_analyzer import EnhancedAIAnalyzer
    from .chromadb_connector import EnhancedChromaDBConnector
    from .requirements_analyzer import RequirementsAnalyzer
    from .metadata_grouping import MetadataGrouper
    from .logger_config import setup_logging
    from .rate_limiter import RateLimiter, RateLimitConfig
    from .ai_providers import create_ai_provider

logger = setup_logging()

class EnhancedBatchAIAnalyzer:
    """Enhanced batch AI analyzer with architectural classification"""
    
    def __init__(self):
        load_dotenv()
        self.output_dir = os.getenv('OUTPUT_DIR', './output')
        
        # Initialize components
        self.enhanced_analyzer = EnhancedAIAnalyzer()
        self.chromadb_connector = EnhancedChromaDBConnector()
        self.grouper = MetadataGrouper()
        
        logger.info("Enhanced batch analyzer initialized with classification capabilities")
        
        # Batch processing configuration
        self.max_files_per_batch = 1  # Process files individually for better classification accuracy
        self.max_files_to_process = 500000

    def prioritize_files(self, files_metadata: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritize files based on importance and type"""
        priority_order = [
            # High priority - core application files
            lambda f: f.get('file_path', '').endswith('.java'),
            lambda f: f.get('file_path', '').endswith('.jsp'),
            lambda f: 'index' in f.get('file_path', '').lower(),
            lambda f: 'home' in f.get('file_path', '').lower(),
            lambda f: 'main' in f.get('file_path', '').lower(),
            # Medium priority - configuration files
            lambda f: f.get('file_path', '').endswith('.xml'),
            lambda f: f.get('file_path', '').endswith('.xsd'),
            lambda f: f.get('file_path', '').endswith('.wsdl'),
            lambda f: f.get('file_path', '').endswith('.xslt'),
            lambda f: f.get('file_path', '').endswith('.properties'),
            lambda f: f.get('file_path', '').endswith('.sql'),
            # Lower priority - other files
            lambda f: True  # Catch all remaining files
        ]
        
        prioritized = []
        for priority_func in priority_order:
            for item in files_metadata:
                if priority_func(item) and item not in prioritized:
                    prioritized.append(item)
                    # Limit total files to process
                    if len(prioritized) >= self.max_files_to_process:
                        break
            if len(prioritized) >= self.max_files_to_process:
                break
        
        return prioritized

    def should_skip_file(self, file_path: str) -> bool:
        """Determine if a file should be skipped to reduce API calls"""
        import re
        skip_patterns = [
            r'\.git/',
            r'node_modules/',
            r'\.DS_Store',
            r'\.log$',
            r'\.tmp$',
            r'\.bak$',
            r'\.swp$',
            r'\.swo$',
            r'\.class$',  # Compiled Java files
            r'\.jar$',    # JAR files
            r'\.war$',    # WAR files
            r'\.ear$',    # EAR files
            r'package-info\.java$',  # Package info files
        ]
        
        for pattern in skip_patterns:
            if re.search(pattern, file_path, re.IGNORECASE):
                return True
        return False

    async def analyze_files_with_classification(self, files_metadata: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze files with enhanced classification"""
        logger.info(f"Starting enhanced analysis of {len(files_metadata)} files")
        
        # Filter out files that should be skipped
        filtered_files = [f for f in files_metadata if not self.should_skip_file(f.get('file_path', ''))]
        logger.info(f"Filtered to {len(filtered_files)} files after skipping unnecessary files")
        
        # Prioritize files for analysis
        prioritized_files = self.prioritize_files(filtered_files)
        logger.info(f"Prioritized {len(prioritized_files)} files for analysis")
        
        # Analyze files with enhanced classification
        analyzed_files = []
        for idx, file_meta in enumerate(prioritized_files, 1):
            logger.info(f"Processing file {idx}/{len(prioritized_files)}: {file_meta.get('file_path', 'unknown')}")
            
            try:
                # Enhanced analysis
                analyzed_file = await self.enhanced_analyzer.analyze_file_with_classification(file_meta)
                analyzed_files.append(analyzed_file)
                
                # Store in ChromaDB with enhanced metadata
                enhanced_analysis = analyzed_file.get('enhanced_ai_analysis')
                if enhanced_analysis:
                    self.chromadb_connector.store_enhanced_metadata(
                        file_path=analyzed_file.get('file_path', ''),
                        content=analyzed_file.get('content', ''),
                        ai_analysis=analyzed_file.get('ai_analysis'),
                        enhanced_analysis=enhanced_analysis
                    )
                    logger.debug(f"Stored enhanced metadata in ChromaDB for: {analyzed_file.get('file_path', 'unknown')}")
                
            except Exception as e:
                logger.error(f"Error analyzing file {file_meta.get('file_path', 'unknown')}: {e}")
                file_meta.update({
                    'analysis_status': 'failed',
                    'error': str(e)
                })
                analyzed_files.append(file_meta)
        
        # Generate architecture report
        logger.info("Generating architecture report...")
        architecture_report = self.grouper.generate_architecture_report(analyzed_files)
        
        # Save architecture report
        report_file = os.path.join(self.output_dir, 'enhanced_architecture_report.json')
        os.makedirs(os.path.dirname(report_file), exist_ok=True)
        with open(report_file, 'w') as f:
            json.dump(architecture_report, f, indent=2)
        
        logger.info(f"Generated enhanced architecture report: {report_file}")
        
        # Generate layer-specific reports
        layers = architecture_report.get('architectural_distribution', {}).get('layers', {})
        for layer in layers.keys():
            if layer != 'unknown':
                layer_summary = self.grouper.generate_layer_summary(analyzed_files, layer)
                layer_file = os.path.join(self.output_dir, f'layer_summary_{layer}.json')
                with open(layer_file, 'w') as f:
                    json.dump(layer_summary, f, indent=2)
                logger.info(f"Generated layer summary for {layer}: {layer_file}")
        
        return analyzed_files

    def save_enhanced_metadata(self, analyzed_metadata: List[Dict[str, Any]]) -> None:
        """Save enhanced metadata to output directory"""
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Save enhanced metadata
        metadata_file = os.path.join(self.output_dir, 'enhanced_metadata.json')
        with open(metadata_file, 'w') as f:
            json.dump(analyzed_metadata, f, indent=2)
        
        logger.info(f"Enhanced metadata saved to: {metadata_file}")
        
        # Save classification summary
        successful_analyses = [m for m in analyzed_metadata if m.get('analysis_status') == 'completed_enhanced']
        failed_analyses = [m for m in analyzed_metadata if m.get('analysis_status') == 'failed']
        
        summary = {
            'total_files': len(analyzed_metadata),
            'successful_analyses': len(successful_analyses),
            'failed_analyses': len(failed_analyses),
            'success_rate': len(successful_analyses) / len(analyzed_metadata) if analyzed_metadata else 0
        }
        
        summary_file = os.path.join(self.output_dir, 'analysis_summary.json')
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Analysis summary saved to: {summary_file}")


async def main():
    """Main function for enhanced analysis"""
    logger.info("Starting enhanced Java application analysis with architectural classification")
    
    try:
        # Initialize enhanced batch analyzer
        analyzer = EnhancedBatchAIAnalyzer()
        
        # Initialize file processor
        file_processor = FileProcessor()
        
        # Process files to get metadata
        logger.info("Processing files to extract metadata...")
        files_metadata = file_processor.process_files()
        logger.info(f"Found {len(files_metadata)} files to analyze")
        
        # Analyze files with enhanced classification
        analyzed_metadata = await analyzer.analyze_files_with_classification(files_metadata)
        
        # Save enhanced metadata
        analyzer.save_enhanced_metadata(analyzed_metadata)
        
        logger.info("Enhanced analysis completed successfully")
        
        # Print summary
        successful = len([m for m in analyzed_metadata if m.get('analysis_status') == 'completed_enhanced'])
        failed = len([m for m in analyzed_metadata if m.get('analysis_status') == 'failed'])
        
        print(f"\n=== Enhanced Analysis Summary ===")
        print(f"Total files processed: {len(analyzed_metadata)}")
        print(f"Successfully analyzed: {successful}")
        print(f"Failed analyses: {failed}")
        print(f"Success rate: {successful/len(analyzed_metadata)*100:.1f}%" if analyzed_metadata else "0%")
        print(f"Enhanced architecture report saved to: {analyzer.output_dir}/enhanced_architecture_report.json")
        
    except Exception as e:
        logger.error(f"Enhanced analysis failed: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())