"""
Enhanced Component Classification System
Integrates with step3_pgm_processor to replace pattern-matching with content analysis
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

from .content_analyzer import ContentAnalyzer, FileAnalysis, ComponentType

class EnhancedComponentClassifier:
    """
    Enhanced component classifier that uses LLM-based content analysis
    instead of simple pattern matching
    """
    
    def __init__(self, config, llm_client, logger: logging.Logger):
        self.config = config
        self.llm_client = llm_client
        self.logger = logger
        self.content_analyzer = ContentAnalyzer(llm_client, logger)
        
        # Statistics tracking
        self.stats = {
            'files_analyzed': 0,
            'files_excluded': 0,
            'files_failed': 0,
            'analysis_time': 0,
            'component_counts': {}
        }
    
    def classify_project_components(self, project_data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Enhanced component classification using content analysis
        
        Returns:
            {
                'dao': [list of DAO components],
                'dto': [list of DTO components], 
                'service': [list of Service components],
                'controller': [list of Controller components],
                'frontend': [list of Frontend components],
                'configuration': [list of Config components],
                'excluded': [list of excluded files],
                'statistics': {...}
            }
        """
        start_time = time.time()
        self.logger.info("Starting enhanced component classification with content analysis")
        
        file_list = project_data.get('file_list', [])
        if not file_list:
            self.logger.warning("No files found in project data")
            return self._empty_classification_result()
        
        # Filter files for analysis (exclude obvious non-components)
        files_to_analyze = self._filter_files_for_analysis(file_list)
        self.logger.info(f"Analyzing {len(files_to_analyze)} files out of {len(file_list)} total files")
        
        # Analyze files (with optional parallel processing)
        if self.config.parallel_processing and len(files_to_analyze) > 10:
            analyses = self._analyze_files_parallel(files_to_analyze, project_data)
        else:
            analyses = self._analyze_files_sequential(files_to_analyze, project_data)
        
        # Group results by component type
        classification_result = self._group_analyses_by_type(analyses)
        
        # Add statistics
        self.stats['analysis_time'] = time.time() - start_time
        classification_result['statistics'] = self.stats.copy()
        
        self.logger.info(f"Classification completed in {self.stats['analysis_time']:.2f}s")
        self._log_classification_summary(classification_result)
        
        return classification_result
    
    def _filter_files_for_analysis(self, file_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Pre-filter files to exclude obvious non-components and improve performance
        """
        analysis_worthy_extensions = {
            '.java', '.jsp', '.html', '.js', '.jsx', '.ts', '.tsx', '.vue',
            '.xml', '.json', '.properties', '.yml', '.yaml',  # Config files we want to classify properly
            '.css', '.scss', '.sass'  # Frontend assets
        }
        
        exclude_patterns = [
            # Build and generated files
            '/target/', '/build/', '/.git/', '/node_modules/', '/.gradle/',
            '.class', '.jar', '.war', '.ear',
            
            # Logs and temporary files  
            '.log', '.tmp', '.bak', '.swp',
            
            # IDE files
            '.iml', '.idea/', '.vscode/', '.settings/',
            
            # Documentation that doesn't need analysis
            'README', 'CHANGELOG', 'LICENSE'
        ]
        
        filtered_files = []
        
        for file_info in file_list:
            file_path = file_info.get('path', '')
            if not file_path:
                continue
                
            # Check extension
            extension = Path(file_path).suffix.lower()
            if extension and extension not in analysis_worthy_extensions:
                continue
            
            # Check exclude patterns
            should_exclude = False
            for pattern in exclude_patterns:
                if pattern in file_path.lower():
                    should_exclude = True
                    break
            
            if not should_exclude:
                filtered_files.append(file_info)
        
        return filtered_files
    
    def _analyze_files_sequential(self, files_to_analyze: List[Dict[str, Any]], 
                                project_data: Dict[str, Any]) -> List[FileAnalysis]:
        """Sequential analysis of files"""
        analyses = []
        
        for i, file_info in enumerate(files_to_analyze):
            if i % 50 == 0:  # Progress logging
                self.logger.info(f"Analyzing file {i+1}/{len(files_to_analyze)}")
            
            analysis = self._analyze_single_file(file_info, project_data)
            analyses.append(analysis)
            self.stats['files_analyzed'] += 1
        
        return analyses
    
    def _analyze_files_parallel(self, files_to_analyze: List[Dict[str, Any]], 
                              project_data: Dict[str, Any]) -> List[FileAnalysis]:
        """Parallel analysis of files with rate limiting"""
        analyses = []
        max_workers = min(3, len(files_to_analyze))  # Limit workers to avoid API rate limits
        
        self.logger.info(f"Using parallel analysis with {max_workers} workers")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit batches to avoid overwhelming the LLM API
            batch_size = 20
            for batch_start in range(0, len(files_to_analyze), batch_size):
                batch_end = min(batch_start + batch_size, len(files_to_analyze))
                batch_files = files_to_analyze[batch_start:batch_end]
                
                # Submit batch
                future_to_file = {
                    executor.submit(self._analyze_single_file, file_info, project_data): file_info
                    for file_info in batch_files
                }
                
                # Collect results
                for future in as_completed(future_to_file):
                    file_info = future_to_file[future]
                    try:
                        analysis = future.result(timeout=30)  # 30s timeout per file
                        analyses.append(analysis)
                        self.stats['files_analyzed'] += 1
                    except Exception as e:
                        self.logger.error(f"Analysis failed for {file_info.get('path', 'unknown')}: {e}")
                        # Create error analysis
                        error_analysis = FileAnalysis(
                            file_path=file_info.get('path', 'unknown'),
                            component_type=ComponentType.UNKNOWN,
                            confidence=0.0,
                            purpose="Analysis failed",
                            business_logic="",
                            api_endpoints=[],
                            dependencies=[],
                            annotations=[],
                            key_methods=[],
                            error_message=str(e)
                        )
                        analyses.append(error_analysis)
                        self.stats['files_failed'] += 1
                
                # Rate limiting between batches
                if batch_end < len(files_to_analyze):
                    time.sleep(1)  # 1 second between batches
                    self.logger.info(f"Completed batch {batch_start//batch_size + 1}, processed {batch_end}/{len(files_to_analyze)} files")
        
        return analyses
    
    def _analyze_single_file(self, file_info: Dict[str, Any], 
                           project_data: Dict[str, Any]) -> FileAnalysis:
        """Analyze a single file using content analysis"""
        file_path = file_info.get('path', '')
        
        try:
            # Try to read file content
            file_content = self._read_file_content(file_path)
            
            # Get enhanced metadata if available
            enhanced_metadata = file_info.get('enhanced_ai_analysis', {})
            
            # Perform content analysis
            analysis = self.content_analyzer.analyze_file_content(
                file_path=file_path,
                content=file_content,
                metadata=enhanced_metadata
            )
            
            return analysis
            
        except Exception as e:
            self.logger.warning(f"Failed to analyze {file_path}: {e}")
            return FileAnalysis(
                file_path=file_path,
                component_type=ComponentType.UNKNOWN,
                confidence=0.0,
                purpose="Analysis error",
                business_logic="",
                api_endpoints=[],
                dependencies=[],
                annotations=[],
                key_methods=[],
                error_message=str(e)
            )
    
    def _read_file_content(self, file_path: str) -> str:
        """
        Read file content using improved path resolution from step3_pgm_processor
        """
        if not self.config.java_source_dir:
            self.logger.debug(f"JAVA_SOURCE_DIR not configured, skipping content read for {file_path}")
            return ""
        
        java_source_dir = Path(self.config.java_source_dir)
        
        # Try primary path
        full_path = java_source_dir / file_path
        if full_path.exists() and full_path.is_file():
            return self._safe_read_file(full_path)
        
        # Try with project name stripped
        if '/' in file_path:
            relative_path = '/'.join(file_path.split('/')[1:])
            fallback_path = java_source_dir / relative_path  
            if fallback_path.exists() and fallback_path.is_file():
                return self._safe_read_file(fallback_path)
        
        # File not found - return empty content
        self.logger.debug(f"Could not read file content for {file_path}")
        return ""
    
    def _safe_read_file(self, file_path: Path) -> str:
        """Safely read file with proper encoding handling"""
        try:
            # Try UTF-8 first
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return content
        except UnicodeDecodeError:
            # Fallback to latin-1 for files with special characters
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
                    return content
            except Exception as e:
                self.logger.warning(f"Failed to read {file_path} with latin-1: {e}")
                return ""
        except Exception as e:
            self.logger.warning(f"Failed to read {file_path}: {e}")
            return ""
    
    def _group_analyses_by_type(self, analyses: List[FileAnalysis]) -> Dict[str, List[Dict[str, Any]]]:
        """Group file analyses by component type"""
        
        result = {
            'dao': [],
            'dto': [],
            'service': [],
            'controller': [],
            'frontend': [],
            'configuration': [],
            'test': [],
            'excluded': [],
            'unknown': []
        }
        
        for analysis in analyses:
            component_dict = {
                'file_path': analysis.file_path,
                'component_type': analysis.component_type.value,
                'confidence': analysis.confidence,
                'purpose': analysis.purpose,
                'business_logic': analysis.business_logic,
                'api_endpoints': analysis.api_endpoints,
                'dependencies': analysis.dependencies,
                'annotations': analysis.annotations,
                'key_methods': analysis.key_methods
            }
            
            if analysis.error_message:
                component_dict['error_message'] = analysis.error_message
            
            # Group by component type
            if analysis.component_type == ComponentType.DAO:
                result['dao'].append(component_dict)
            elif analysis.component_type == ComponentType.DTO:
                result['dto'].append(component_dict)
            elif analysis.component_type == ComponentType.SERVICE:
                result['service'].append(component_dict)
            elif analysis.component_type == ComponentType.CONTROLLER:
                result['controller'].append(component_dict)
            elif analysis.component_type in [ComponentType.FRONTEND_VIEW, ComponentType.FRONTEND_SCRIPT, ComponentType.FRONTEND_STYLE]:
                result['frontend'].append(component_dict)
            elif analysis.component_type == ComponentType.CONFIGURATION:
                result['configuration'].append(component_dict)
            elif analysis.component_type == ComponentType.TEST:
                result['test'].append(component_dict)
            elif analysis.component_type == ComponentType.EXCLUDE:
                result['excluded'].append(component_dict)
                self.stats['files_excluded'] += 1
            else:
                result['unknown'].append(component_dict)
            
            # Update component count statistics
            component_type_str = analysis.component_type.value
            self.stats['component_counts'][component_type_str] = self.stats['component_counts'].get(component_type_str, 0) + 1
        
        return result
    
    def _empty_classification_result(self) -> Dict[str, List]:
        """Return empty classification result"""
        return {
            'dao': [],
            'dto': [],
            'service': [],
            'controller': [], 
            'frontend': [],
            'configuration': [],
            'test': [],
            'excluded': [],
            'unknown': [],
            'statistics': self.stats.copy()
        }
    
    def _log_classification_summary(self, classification_result: Dict[str, List]) -> None:
        """Log summary of classification results"""
        self.logger.info("=== Component Classification Summary ===")
        self.logger.info(f"Total files analyzed: {self.stats['files_analyzed']}")
        self.logger.info(f"Analysis time: {self.stats['analysis_time']:.2f}s")
        
        for component_type, components in classification_result.items():
            if component_type != 'statistics' and components:
                self.logger.info(f"{component_type.upper()}: {len(components)} components")
        
        if self.stats['files_excluded'] > 0:
            self.logger.info(f"Files excluded: {self.stats['files_excluded']}")
        
        if self.stats['files_failed'] > 0:
            self.logger.warning(f"Analysis failures: {self.stats['files_failed']}")
    
    def validate_classification_quality(self, classification_result: Dict[str, List]) -> Dict[str, Any]:
        """
        Validate the quality of classification results
        Returns quality metrics and recommendations
        """
        total_components = sum(len(components) for key, components in classification_result.items() if key != 'statistics')
        
        quality_metrics = {
            'total_components': total_components,
            'exclusion_ratio': self.stats['files_excluded'] / max(1, self.stats['files_analyzed']),
            'failure_ratio': self.stats['files_failed'] / max(1, self.stats['files_analyzed']),
            'avg_confidence': 0.0,
            'low_confidence_count': 0,
            'recommendations': []
        }
        
        # Calculate confidence metrics
        all_confidences = []
        low_confidence_threshold = 0.7
        
        for component_type, components in classification_result.items():
            if component_type == 'statistics':
                continue
                
            for component in components:
                confidence = component.get('confidence', 0.0)
                all_confidences.append(confidence)
                
                if confidence < low_confidence_threshold:
                    quality_metrics['low_confidence_count'] += 1
        
        if all_confidences:
            quality_metrics['avg_confidence'] = sum(all_confidences) / len(all_confidences)
        
        # Generate recommendations
        if quality_metrics['exclusion_ratio'] > 0.8:
            quality_metrics['recommendations'].append("High exclusion ratio - consider reviewing file filtering")
        
        if quality_metrics['failure_ratio'] > 0.1:
            quality_metrics['recommendations'].append("High failure ratio - check LLM connectivity and file access")
        
        if quality_metrics['avg_confidence'] < 0.8:
            quality_metrics['recommendations'].append("Low average confidence - consider improving LLM prompts")
        
        if quality_metrics['low_confidence_count'] > total_components * 0.2:
            quality_metrics['recommendations'].append(f"{quality_metrics['low_confidence_count']} components with low confidence - review classifications manually")
        
        return quality_metrics