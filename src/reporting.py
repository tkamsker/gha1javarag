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
            # Consume consolidated JSON if available (Step 2 per iteration10.md)
            consolidated_path = self.output_dir / 'consolidated_metadata.json'

            projects = []
            if consolidated_path.exists():
                with open(consolidated_path, 'r', encoding='utf-8') as f:
                    consolidated = json.load(f)
                    projects = [p.get('name', 'unknown') for p in consolidated.get('projects', [])]

                # Generate per-project requirements structured by layers
                for project in consolidated.get('projects', []):
                    project_name = project.get('name', 'unknown')
                    self._generate_requirements_from_project_json(project_name, project)
            else:
                self.logger.warning("consolidated_metadata.json not found. Generating placeholder requirements.")

            # Master requirements
            master_requirements = self.requirements_dir / '_master.md'
            with open(master_requirements, 'w', encoding='utf-8') as f:
                f.write("# Master Requirements Document\n\n")
                f.write(f"Generated: {datetime.now().isoformat()}\n\n")
                f.write("This document contains consolidated requirements from all analyzed projects.\n\n")
                f.write("## Projects\n\n")
                for name in projects:
                    f.write(f"- {name}\n")
                f.write("\n## Architectural Layers\n\n")
                f.write("- Database (SQL/XML)\n")
                f.write("- Backend (Java classes/servlets)\n")
                f.write("- Presentation (JSP/TSP/HTML/JS)\n")
            self.logger.info(f"Generated master requirements: {master_requirements}")
        
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

    # --- JSON export/ingestion helpers for 2-step flow ---

    def write_consolidated_metadata(self, catalog: Dict[str, Any], projects_data: Dict[str, Any]):
        """Write consolidated metadata JSON for Step 2 consumption."""
        try:
            consolidated = {
                'generation_timestamp': datetime.now().isoformat(),
                'catalog': catalog,
                'projects': list(projects_data.values())
            }
            out_file = self.output_dir / 'consolidated_metadata.json'
            with open(out_file, 'w', encoding='utf-8') as f:
                json.dump(consolidated, f, indent=2, default=str)
            self.logger.info(f"Wrote consolidated metadata: {out_file}")
        except Exception as e:
            self.logger.error(f"Error writing consolidated metadata: {e}")

    def _generate_requirements_from_project_json(self, project_name: str, project: Dict[str, Any]):
        """Generate requirements files from a single project's JSON structure."""
        try:
            project_dir = self.requirements_dir / project_name
            project_dir.mkdir(exist_ok=True)

            # Prefer enhanced classifier fields to group layers; fallback to language
            files = project.get('file_list', [])

            def infer_layer_from_classifier(fi: Dict[str, Any]) -> str:
                cls = (fi.get('enhanced_ai_analysis') or {}).get('file_classification') or {}
                layer = (cls.get('architectural_layer') or '').lower()
                if layer in ['frontend']:
                    return 'ui'
                if layer in ['data_access', 'persistence', 'configuration']:
                    return 'database'
                if layer in ['backend_service', 'integration', 'security', 'batch_process', 'configuration']:
                    return 'backend'
                return ''

            database_files: List[Dict[str, Any]] = []
            backend_files: List[Dict[str, Any]] = []
            ui_files: List[Dict[str, Any]] = []

            for fi in files:
                inferred = infer_layer_from_classifier(fi)
                if inferred == 'database':
                    database_files.append(fi)
                elif inferred == 'backend':
                    backend_files.append(fi)
                elif inferred == 'ui':
                    ui_files.append(fi)
                else:
                    # Fallback to language-based grouping if classifier not decisive
                    lang = (fi.get('language') or '').lower()
                    if lang in ['sql', 'xml']:
                        database_files.append(fi)
                    elif lang in ['jsp', 'html', 'javascript', 'css']:
                        ui_files.append(fi)
                    else:
                        backend_files.append(fi)

            def write_layer(layer_name: str, file_group: List[Dict[str, Any]]):
                layer_path = project_dir / f"{layer_name}_requirements.md"
                with open(layer_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {project_name} - {layer_name.title()} Layer Requirements\n\n")
                    f.write("## 1. Overview\n\n")
                    f.write(f"Brief purpose within the application for the {layer_name} layer.\n\n")

                    # Components grouped by component_type with flags
                    f.write("## 2. Components\n\n")
                    from collections import defaultdict
                    comps: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
                    for fi in file_group[:1000]:
                        cls = (fi.get('enhanced_ai_analysis') or {}).get('file_classification') or {}
                        comps[(cls.get('component_type') or 'unknown')].append(fi)
                    for comp_type, items in sorted(comps.items(), key=lambda x: x[0]):
                        f.write(f"### Component Type: {comp_type}\n\n")
                        for item in items[:300]:
                            cls = (item.get('enhanced_ai_analysis') or {}).get('file_classification') or {}
                            api_flags = []
                            if cls.get('exposes_api'): api_flags.append('exposes_api')
                            if cls.get('consumes_api'): api_flags.append('consumes_api')
                            if cls.get('database_interactions'): api_flags.append('db')
                            flags_str = (" [" + ", ".join(api_flags) + "]") if api_flags else ""
                            domain = cls.get('business_domain') or ''
                            domain_str = f" domain:{domain}" if domain else ""
                            f.write(f"- {item.get('path')} ({item.get('language')}){flags_str}{domain_str}\n")
                        f.write("\n")

                    # Functional summary from heuristics
                    f.write("\n## 3. Functionality\n\n")
                    tech_counts: Dict[str, int] = {}
                    pattern_counts: Dict[str, int] = {}
                    exposes = consumes = dbi = 0
                    for fi in file_group:
                        cls = (fi.get('enhanced_ai_analysis') or {}).get('file_classification') or {}
                        for t in cls.get('technology_stack', []) or []:
                            tech_counts[t] = tech_counts.get(t, 0) + 1
                        for p in cls.get('design_patterns', []) or []:
                            pattern_counts[p] = pattern_counts.get(p, 0) + 1
                        if cls.get('exposes_api'): exposes += 1
                        if cls.get('consumes_api'): consumes += 1
                        if cls.get('database_interactions'): dbi += 1

                    top_tech = ', '.join([k for k,_ in sorted(tech_counts.items(), key=lambda x: -x[1])[:8]]) or 'n/a'
                    top_patterns = ', '.join([k for k,_ in sorted(pattern_counts.items(), key=lambda x: -x[1])[:8]]) or 'n/a'

                    f.write("- **Main Features:** Heuristic summary based on component classification.\n")
                    f.write(f"- **Technology Stack (top):** {top_tech}\n")
                    f.write(f"- **Design Patterns (top):** {top_patterns}\n")
                    f.write(f"- **Inputs/Outputs:** API exposure {exposes}, API consumers {consumes}, DB interactions {dbi}.\n")
                    f.write("- **Key Methods/Functions:** [To be derived in advanced analysis]\n\n")

                    # Endpoint summary if applicable
                    if layer_name == 'backend' and (exposes > 0 or consumes > 0):
                        f.write("### API Endpoints Summary\n\n")
                        for fi in file_group[:500]:
                            cls = (fi.get('enhanced_ai_analysis') or {}).get('file_classification') or {}
                            if cls.get('exposes_api') or cls.get('consumes_api'):
                                flags = []
                                if cls.get('exposes_api'): flags.append('exposes')
                                if cls.get('consumes_api'): flags.append('consumes')
                                f.write(f"- {fi.get('path')} ({', '.join(flags)})\n")
                        f.write("\n")

                    f.write("## 4. Dependencies\n\n- [To be cross-linked]\n\n")
                    f.write("## 5. Notes\n\n- [Business rule nuances]\n")

            write_layer('database', database_files)
            write_layer('backend', backend_files)
            write_layer('ui', ui_files)
            self.logger.info(f"Generated requirements from JSON for project {project_name}")
        except Exception as e:
            self.logger.error(f"Error generating project requirements from JSON for {project_name}: {e}")
