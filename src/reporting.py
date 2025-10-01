"""
Reporting module for generating JSON catalogs and requirements documentation.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging


class ReportingManager:
    """Manages reporting and documentation generation."""
    
    def __init__(self, config):
        """Initialize reporting manager with configuration."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Create output directories
        self.output_dir = Path(config.output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.projects_dir = self.output_dir / 'projects'
        self.projects_dir.mkdir(exist_ok=True)
        
        self.requirements_dir = self.output_dir / 'requirements'
        self.requirements_dir.mkdir(exist_ok=True)
        
        self.logs_dir = self.output_dir / 'logs'
        self.logs_dir.mkdir(exist_ok=True)
        
        # Initialize counters
        self.processed_files = 0
        self.failed_files = 0
        self.total_chunks = 0
        self.start_time = datetime.now()
    
    def log_file_processed(self, file_path: str, chunk_count: int):
        """Log a successfully processed file."""
        self.processed_files += 1
        self.total_chunks += chunk_count
        
        if self.config.verbose_logging:
            self.logger.debug(f"Processed {file_path} -> {chunk_count} chunks")
    
    def log_file_error(self, file_path: str, error: str):
        """Log a file processing error."""
        self.failed_files += 1
        self.logger.error(f"Failed to process {file_path}: {error}")
    
    def generate_project_summary(self, project_name: str, project_data: Dict[str, Any]):
        """Generate a summary JSON file for a project."""
        try:
            summary_file = self.projects_dir / f"{project_name}.summary.json"
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, indent=2, default=str)
            
            self.logger.info(f"Generated project summary: {summary_file}")
        
        except Exception as e:
            self.logger.error(f"Error generating project summary for {project_name}: {e}")
    
    def generate_catalog_index(self, projects: List[Dict[str, Any]]):
        """Generate the global catalog index."""
        try:
            catalog = {
                'generation_timestamp': datetime.now().isoformat(),
                'source_directory': self.config.java_source_dir,
                'total_projects': len(projects),
                'total_files': sum(p.get('total_files', 0) for p in projects),
                'total_size_bytes': sum(p.get('total_size_bytes', 0) for p in projects),
                'projects': projects
            }
            
            catalog_file = self.output_dir / 'catalog.index.json'
            
            with open(catalog_file, 'w', encoding='utf-8') as f:
                json.dump(catalog, f, indent=2, default=str)
            
            self.logger.info(f"Generated catalog index: {catalog_file}")
        
        except Exception as e:
            self.logger.error(f"Error generating catalog index: {e}")
    
    def generate_final_report(self, total_files: int, total_chunks: int):
        """Generate the final processing report."""
        try:
            end_time = datetime.now()
            duration = end_time - self.start_time
            
            report = {
                'processing_summary': {
                    'start_time': self.start_time.isoformat(),
                    'end_time': end_time.isoformat(),
                    'duration_seconds': duration.total_seconds(),
                    'total_files_processed': total_files,
                    'total_chunks_created': total_chunks,
                    'successful_files': self.processed_files,
                    'failed_files': self.failed_files,
                    'success_rate': (self.processed_files / total_files * 100) if total_files > 0 else 0
                },
                'configuration': {
                    'java_source_dir': self.config.java_source_dir,
                    'output_dir': self.config.output_dir,
                    'weaviate_url': self.config.weaviate_url,
                    'embedding_provider': self.config.embedding_provider,
                    'ai_provider': self.config.ai_provider,
                    'max_file_bytes': self.config.max_file_bytes,
                    'include_file_types': self.config.include_file_types,
                    'exclude_dirs': self.config.exclude_dirs
                },
                'performance_metrics': {
                    'files_per_second': total_files / duration.total_seconds() if duration.total_seconds() > 0 else 0,
                    'chunks_per_second': total_chunks / duration.total_seconds() if duration.total_seconds() > 0 else 0,
                    'average_chunks_per_file': total_chunks / total_files if total_files > 0 else 0
                }
            }
            
            report_file = self.output_dir / 'processing_report.json'
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, default=str)
            
            self.logger.info(f"Generated processing report: {report_file}")
            
            # Print summary to console
            self.logger.info("=" * 50)
            self.logger.info("PROCESSING SUMMARY")
            self.logger.info("=" * 50)
            self.logger.info(f"Duration: {duration}")
            self.logger.info(f"Files processed: {total_files}")
            self.logger.info(f"Chunks created: {total_chunks}")
            self.logger.info(f"Success rate: {report['processing_summary']['success_rate']:.1f}%")
            self.logger.info(f"Performance: {report['performance_metrics']['files_per_second']:.1f} files/sec")
            self.logger.info("=" * 50)
        
        except Exception as e:
            self.logger.error(f"Error generating final report: {e}")
    
    def generate_requirements(self):
        """Generate requirements documentation from indexed data."""
        try:
            # This would typically query Weaviate for data and generate requirements
            # For now, create a placeholder structure
            
            requirements_data = {
                'generation_timestamp': datetime.now().isoformat(),
                'projects': []
            }
            
            # Create master requirements file
            master_requirements = self.requirements_dir / '_master.md'
            
            with open(master_requirements, 'w', encoding='utf-8') as f:
                f.write("# Master Requirements Document\n\n")
                f.write(f"Generated: {datetime.now().isoformat()}\n\n")
                f.write("This document contains consolidated requirements from all analyzed projects.\n\n")
                f.write("## Project Structure\n\n")
                f.write("Requirements are organized by project and architectural layer:\n\n")
                f.write("- Database Layer: Data models, schemas, and persistence logic\n")
                f.write("- Backend Layer: Business logic, services, and APIs\n")
                f.write("- UI Layer: User interfaces, components, and interactions\n\n")
                f.write("## Individual Project Requirements\n\n")
                f.write("See individual project directories for detailed requirements.\n")
            
            self.logger.info(f"Generated master requirements: {master_requirements}")
            
            # Create placeholder for each architectural layer
            for layer in ['database', 'backend', 'ui']:
                layer_dir = self.requirements_dir / layer
                layer_dir.mkdir(exist_ok=True)
                
                layer_file = layer_dir / f'{layer}_requirements.md'
                
                with open(layer_file, 'w', encoding='utf-8') as f:
                    f.write(f"# {layer.title()} Layer Requirements\n\n")
                    f.write(f"Generated: {datetime.now().isoformat()}\n\n")
                    f.write("## Overview\n")
                    f.write(f"Requirements for the {layer} layer of the application.\n\n")
                    f.write("## Components\n")
                    f.write("- [To be populated from Weaviate data]\n\n")
                    f.write("## Functionality\n")
                    f.write("- [To be populated from Weaviate data]\n\n")
                    f.write("## Dependencies\n")
                    f.write("- [To be populated from Weaviate data]\n\n")
                    f.write("## Notes\n")
                    f.write("- [To be populated from Weaviate data]\n")
                
                self.logger.info(f"Generated {layer} requirements: {layer_file}")
        
        except Exception as e:
            self.logger.error(f"Error generating requirements: {e}")
    
    def generate_project_requirements(self, project_name: str, project_data: Dict[str, Any]):
        """Generate requirements for a specific project."""
        try:
            project_dir = self.requirements_dir / project_name
            project_dir.mkdir(exist_ok=True)
            
            # Generate requirements for each architectural layer
            for layer in ['database', 'backend', 'ui']:
                layer_file = project_dir / f'{layer}_requirements.md'
                
                with open(layer_file, 'w', encoding='utf-8') as f:
                    f.write(f"# {project_name} - {layer.title()} Layer Requirements\n\n")
                    f.write(f"Generated: {datetime.now().isoformat()}\n\n")
                    f.write("## Overview\n")
                    f.write(f"Requirements for the {layer} layer of project {project_name}.\n\n")
                    f.write("## Components\n")
                    f.write("- [To be populated from project data]\n\n")
                    f.write("## Functionality\n")
                    f.write("- [To be populated from project data]\n\n")
                    f.write("## Dependencies\n")
                    f.write("- [To be populated from project data]\n\n")
                    f.write("## Notes\n")
                    f.write("- [To be populated from project data]\n")
            
            self.logger.info(f"Generated requirements for project {project_name}")
        
        except Exception as e:
            self.logger.error(f"Error generating requirements for project {project_name}: {e}")
    
    def log_processing_event(self, level: str, event: str, file_path: str = "", detail: str = "", exception: str = ""):
        """Log a processing event to JSONL log file."""
        try:
            log_entry = {
                'ts': datetime.now().isoformat(),
                'level': level.upper(),
                'event': event,
                'file': file_path,
                'detail': detail
            }
            
            if exception:
                log_entry['exception'] = exception
            
            log_file = self.logs_dir / 'app.log.jsonl'
            
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + '\n')
        
        except Exception as e:
            self.logger.error(f"Error writing to log file: {e}")
    
    def cleanup_old_logs(self, days_to_keep: int = 7):
        """Clean up old log files."""
        try:
            cutoff_time = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
            
            for log_file in self.logs_dir.glob('*.log.jsonl'):
                if log_file.stat().st_mtime < cutoff_time:
                    log_file.unlink()
                    self.logger.info(f"Cleaned up old log file: {log_file}")
        
        except Exception as e:
            self.logger.error(f"Error cleaning up old logs: {e}")
