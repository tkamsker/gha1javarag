"""
Step 3 Requirements Synthesis Processor

Refactored implementation of step3 functionality as per PRD specifications.
Provides modular, testable, and maintainable requirements synthesis using LLM and Weaviate.
"""

import json
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime

try:
    from .env_loader import Config
    from .llm_client import LLMClient
    from .weaviate_client import WeaviateClient
    from .reporting import ReportingManager
except ImportError:
    # Fallback for direct execution
    from env_loader import Config
    from llm_client import LLMClient
    from weaviate_client import WeaviateClient
    from reporting import ReportingManager


@dataclass
class Step3Config:
    """Configuration validation for Step3 processing."""
    
    def __init__(self, config: Config):
        self.config = config
        self._validate_environment()
        self._validate_prerequisites()
    
    def _validate_environment(self) -> None:
        """Validate required environment variables."""
        required_vars = [
            'WEAVIATE_URL',
            'OUTPUT_DIR'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(self.config, var.lower(), None):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    def _validate_prerequisites(self) -> None:
        """Validate file system prerequisites."""
        output_dir = Path(self.config.output_dir)
        if not output_dir.exists():
            raise FileNotFoundError(f"Output directory does not exist: {output_dir}")


class Step3ProcessingError(Exception):
    """Custom exception for Step3 processing errors."""
    pass


class Step3Processor:
    """
    Main processor for Step 3 requirements synthesis.
    
    Handles the complete workflow from data loading to output generation
    with proper error handling and parallel processing capabilities.
    """
    
    def __init__(self, config: Config):
        self.config = Step3Config(config)
        self.base_config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.llm_client: Optional[LLMClient] = None
        self.weaviate_client: Optional[WeaviateClient] = None
        self.reporting: Optional[ReportingManager] = None
        
        # Thread safety for concurrent processing
        self._lock = threading.Lock()
        self._stats_cache: Optional[Dict] = None
        
        # Output tracking
        self.requirements_dir = Path(self.base_config.output_dir) / 'requirements'
        self.projects_dir = self.requirements_dir / 'projects'
        
    def initialize_components(self) -> None:
        """Initialize LLM, Weaviate, and reporting components with validation."""
        try:
            self.logger.info("Initializing Step3 components...")
            
            # Initialize LLM client
            self.llm_client = LLMClient(self.base_config)
            
            # Initialize Weaviate client with connectivity test
            self.weaviate_client = WeaviateClient(self.base_config)
            
            # Test connectivity
            try:
                self.weaviate_client.get_all_collection_stats()
                self.logger.info("Weaviate connectivity verified")
            except Exception as e:
                raise Step3ProcessingError(f"Weaviate connectivity failed: {e}")
            
            # Initialize reporting
            self.reporting = ReportingManager(self.base_config)
            
            self.logger.info("All components initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Component initialization failed: {e}")
            raise Step3ProcessingError(f"Failed to initialize components: {e}")
    
    def load_intermediate_data(self) -> Dict[str, Any]:
        """Load intermediate JSON data with fallback strategy."""
        output_dir = Path(self.base_config.output_dir)
        
        # Primary data source
        primary_path = output_dir / 'intermediate_step2.json'
        fallback_path = output_dir / 'consolidated_metadata.json'
        
        data_path = None
        if primary_path.exists():
            data_path = primary_path
            self.logger.info(f"Loading primary data source: {primary_path}")
        elif fallback_path.exists():
            data_path = fallback_path
            self.logger.warning(f"Primary data not found, using fallback: {fallback_path}")
        else:
            raise Step3ProcessingError(
                f"No intermediate data found. Expected: {primary_path} or {fallback_path}"
            )
        
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate data structure
            self._validate_data_structure(data)
            
            projects = data.get('projects', {})
            self.logger.info(f"Loaded data for {len(projects)} projects from {data_path}")
            
            return data
            
        except json.JSONDecodeError as e:
            raise Step3ProcessingError(f"Invalid JSON in {data_path}: {e}")
        except Exception as e:
            raise Step3ProcessingError(f"Error loading data from {data_path}: {e}")
    
    def _validate_data_structure(self, data: Dict[str, Any]) -> None:
        """Validate the structure of loaded intermediate data."""
        if not isinstance(data, dict):
            raise Step3ProcessingError("Data must be a dictionary")
        
        projects = data.get('projects', {})
        if not isinstance(projects, dict):
            raise Step3ProcessingError("'projects' must be a dictionary")
        
        for project_name, project_data in projects.items():
            if not isinstance(project_data, dict):
                raise Step3ProcessingError(f"Project {project_name} data must be a dictionary")
            
            required_fields = ['name', 'path', 'total_files']
            for field in required_fields:
                if field not in project_data:
                    self.logger.warning(f"Project {project_name} missing field: {field}")
    
    def collect_weaviate_statistics(self) -> Dict[str, Any]:
        """Collect and cache Weaviate statistics for reuse across projects."""
        with self._lock:
            if self._stats_cache is not None:
                return self._stats_cache
            
            try:
                self.logger.info("Collecting Weaviate statistics...")
                stats = self.weaviate_client.get_all_collection_stats()
                self._stats_cache = stats
                
                total_objects = stats.get('total_count', 0)
                self.logger.info(f"Collected statistics for {total_objects} total objects")
                
                return stats
                
            except Exception as e:
                self.logger.error(f"Failed to collect Weaviate statistics: {e}")
                # Return empty stats rather than failing
                self._stats_cache = {'error': str(e), 'total_count': 0}
                return self._stats_cache
    
    def synthesize_requirements(self, project_name: str, project_data: Dict[str, Any], 
                              stats: Dict[str, Any]) -> str:
        """Generate requirements markdown for a single project using LLM."""
        try:
            # Build context for LLM
            project_summary = {
                'name': project_data.get('name', project_name),
                'path': project_data.get('path', ''),
                'total_files': project_data.get('total_files', 0),
                'file_count_by_type': self._analyze_file_types(project_data),
                'architectural_layers': self._analyze_architectural_layers(project_data)
            }
            
            # Create LLM prompt
            prompt = self._build_llm_prompt(project_summary, stats)
            
            # Generate requirements using LLM
            self.logger.debug(f"Generating requirements for project: {project_name}")
            
            markdown = self.llm_client._complete_text(
                prompt,
                system="You create clean, structured requirement outlines in Markdown format. "
                       "Focus on functional requirements, technical architecture, and integration points.",
                max_tokens=1500
            )
            
            if not markdown or markdown.strip() == '':
                raise Step3ProcessingError(f"Empty response from LLM for project {project_name}")
            
            return markdown
            
        except Exception as e:
            self.logger.error(f"Error synthesizing requirements for {project_name}: {e}")
            # Return fallback content rather than failing
            return self._generate_fallback_requirements(project_name, project_data)
    
    def _analyze_file_types(self, project_data: Dict[str, Any]) -> Dict[str, int]:
        """Analyze file types in project for context."""
        file_types = {}
        file_list = project_data.get('file_list', [])
        
        for file_info in file_list:
            language = file_info.get('language', 'unknown')
            file_types[language] = file_types.get(language, 0) + 1
        
        return file_types
    
    def _analyze_architectural_layers(self, project_data: Dict[str, Any]) -> Dict[str, int]:
        """Analyze architectural layers from AI analysis."""
        layers = {}
        file_list = project_data.get('file_list', [])
        
        for file_info in file_list:
            enhanced = file_info.get('enhanced_ai_analysis', {})
            classification = enhanced.get('file_classification', {})
            layer = classification.get('architectural_layer', 'unknown')
            
            layers[layer] = layers.get(layer, 0) + 1
        
        return layers
    
    def _build_llm_prompt(self, project_summary: Dict[str, Any], stats: Dict[str, Any]) -> str:
        """Build comprehensive LLM prompt for requirements generation."""
        prompt = f"""Synthesize concise functional requirements overview for project: {project_summary['name']}

Project Context:
- Total Files: {project_summary['total_files']}
- File Types: {json.dumps(project_summary['file_count_by_type'], indent=2)}
- Architectural Layers: {json.dumps(project_summary['architectural_layers'], indent=2)}

Weaviate Vector Database Statistics:
{json.dumps({k: v for k, v in stats.items() if k not in ['timestamp', 'error']}, indent=2)}

Please generate a structured Markdown requirements document with the following sections:
1. ## Project Overview
2. ## Functional Requirements
3. ## Technical Architecture
4. ## Integration Points
5. ## Data Requirements

Focus on actionable requirements based on the code analysis and architectural patterns identified.
Keep each section concise but comprehensive."""

        return prompt
    
    def _generate_fallback_requirements(self, project_name: str, project_data: Dict[str, Any]) -> str:
        """Generate fallback requirements when LLM fails."""
        return f"""# Requirements for {project_name}

## Project Overview
- **Location**: {project_data.get('path', 'Unknown')}
- **Total Files**: {project_data.get('total_files', 0)}

## Status
⚠️ **Note**: Requirements were generated using fallback method due to LLM processing error.
Manual review and enhancement recommended.

## File Analysis
Based on static analysis of project files:

{self._format_file_analysis(project_data)}

## Next Steps
1. Review and enhance these requirements manually
2. Validate technical architecture assumptions
3. Add specific functional requirements based on business context
"""
    
    def _format_file_analysis(self, project_data: Dict[str, Any]) -> str:
        """Format basic file analysis for fallback requirements."""
        file_types = self._analyze_file_types(project_data)
        
        analysis = "### File Type Distribution\n"
        for file_type, count in file_types.items():
            analysis += f"- **{file_type}**: {count} files\n"
        
        return analysis
    
    def generate_output_files(self, project_name: str, requirements_markdown: str) -> None:
        """Generate structured output files for a project."""
        try:
            # Create project directory
            project_dir = self.projects_dir / project_name
            project_dir.mkdir(parents=True, exist_ok=True)
            
            # Write main requirements file
            requirements_file = project_dir / 'requirements.md'
            with open(requirements_file, 'w', encoding='utf-8') as f:
                f.write(requirements_markdown)
            
            # Generate additional structured files
            self._generate_architecture_file(project_dir, project_name, requirements_markdown)
            self._generate_dependencies_file(project_dir, project_name)
            
            self.logger.info(f"Generated output files for project: {project_name}")
            
        except Exception as e:
            self.logger.error(f"Error generating output files for {project_name}: {e}")
            raise Step3ProcessingError(f"Failed to generate output files for {project_name}: {e}")
    
    def _generate_architecture_file(self, project_dir: Path, project_name: str, 
                                  requirements_markdown: str) -> None:
        """Generate architecture-focused documentation."""
        architecture_file = project_dir / 'architecture.md'
        
        # Extract architecture section from requirements if available
        architecture_content = f"""# Technical Architecture - {project_name}

## Overview
This document outlines the technical architecture and design patterns identified in {project_name}.

## Architecture Analysis
*Extracted from requirements synthesis and code analysis*

{self._extract_architecture_section(requirements_markdown)}

## Generated on
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        with open(architecture_file, 'w', encoding='utf-8') as f:
            f.write(architecture_content)
    
    def _generate_dependencies_file(self, project_dir: Path, project_name: str) -> None:
        """Generate dependencies and integration points documentation."""
        dependencies_file = project_dir / 'dependencies.md'
        
        dependencies_content = f"""# Dependencies & Integration Points - {project_name}

## External Dependencies
*To be populated based on detailed code analysis*

## Integration Points
*Based on Weaviate analysis of integration patterns*

## API Endpoints
*Identified from code analysis*

## Database Interactions
*Data access patterns and database usage*

## Generated on
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
*Note: This file contains placeholder structure. Enhance with specific dependency analysis.*
"""
        
        with open(dependencies_file, 'w', encoding='utf-8') as f:
            f.write(dependencies_content)
    
    def _extract_architecture_section(self, markdown: str) -> str:
        """Extract architecture-related content from requirements markdown."""
        lines = markdown.split('\n')
        architecture_lines = []
        in_architecture_section = False
        
        for line in lines:
            if '## Technical Architecture' in line:
                in_architecture_section = True
                continue
            elif line.startswith('## ') and in_architecture_section:
                break
            elif in_architecture_section:
                architecture_lines.append(line)
        
        return '\n'.join(architecture_lines) if architecture_lines else "*No specific architecture section found*"
    
    def generate_executive_summary(self, projects: Dict[str, str]) -> None:
        """Generate executive summary from all project requirements."""
        try:
            summary_file = self.requirements_dir / '_step3_overview.md'
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(f"""# Step 3: Requirements Synthesis Overview

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

This document provides an overview of requirements synthesized for {len(projects)} projects using LLM analysis and Weaviate vector database insights.

## Projects Processed

""")
                
                for project_name in sorted(projects.keys()):
                    f.write(f"### [{project_name}](projects/{project_name}/requirements.md)\n\n")
                    
                    # Add brief summary if available
                    summary_line = self._extract_project_summary(projects[project_name])
                    if summary_line:
                        f.write(f"{summary_line}\n\n")
                    
                    f.write(f"- **Requirements**: [View Details](projects/{project_name}/requirements.md)\n")
                    f.write(f"- **Architecture**: [View Details](projects/{project_name}/architecture.md)\n")
                    f.write(f"- **Dependencies**: [View Details](projects/{project_name}/dependencies.md)\n\n")
                
                f.write(f"""
## Processing Statistics

- **Total Projects**: {len(projects)}
- **Processing Method**: LLM + Weaviate Analysis
- **Output Format**: Structured Markdown

## Next Steps

1. Review individual project requirements
2. Validate technical assumptions
3. Enhance with business context
4. Update integration specifications
""")
            
            self.logger.info(f"Generated executive summary for {len(projects)} projects")
            
        except Exception as e:
            self.logger.error(f"Error generating executive summary: {e}")
            raise Step3ProcessingError(f"Failed to generate executive summary: {e}")
    
    def _extract_project_summary(self, requirements_markdown: str) -> str:
        """Extract first meaningful line from project requirements for summary."""
        lines = requirements_markdown.split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and len(line) > 20:
                return line[:200] + ('...' if len(line) > 200 else '')
        return ""
    
    def process_projects_parallel(self, projects: Dict[str, Any], max_workers: int = 3) -> Dict[str, str]:
        """Process projects in parallel with thread safety."""
        self.logger.info(f"Processing {len(projects)} projects with {max_workers} workers")
        
        # Collect stats once for all projects
        stats = self.collect_weaviate_statistics()
        
        project_requirements = {}
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_project = {
                executor.submit(self._process_single_project, name, data, stats): name
                for name, data in projects.items()
            }
            
            # Collect results
            for future in as_completed(future_to_project):
                project_name = future_to_project[future]
                try:
                    requirements = future.result()
                    project_requirements[project_name] = requirements
                    self.logger.info(f"Completed processing: {project_name}")
                except Exception as e:
                    self.logger.error(f"Error processing {project_name}: {e}")
                    # Continue with other projects
                    project_requirements[project_name] = self._generate_fallback_requirements(
                        project_name, projects[project_name]
                    )
        
        return project_requirements
    
    def _process_single_project(self, project_name: str, project_data: Dict[str, Any], 
                              stats: Dict[str, Any]) -> str:
        """Process a single project (thread-safe)."""
        # Generate requirements
        requirements = self.synthesize_requirements(project_name, project_data, stats)
        
        # Generate output files
        self.generate_output_files(project_name, requirements)
        
        return requirements
    
    def run(self, parallel: bool = True, max_workers: int = 3) -> None:
        """Main execution method for Step 3 processing."""
        try:
            self.logger.info("Starting Step 3 requirements synthesis...")
            
            # Initialize components
            self.initialize_components()
            
            # Load data
            data = self.load_intermediate_data()
            projects = data.get('projects', {})
            
            if not projects:
                self.logger.warning("No projects found in intermediate data")
                return
            
            # Create output directories
            self.requirements_dir.mkdir(parents=True, exist_ok=True)
            self.projects_dir.mkdir(parents=True, exist_ok=True)
            
            # Process projects
            if parallel and len(projects) > 1:
                project_requirements = self.process_projects_parallel(projects, max_workers)
            else:
                self.logger.info("Processing projects sequentially")
                stats = self.collect_weaviate_statistics()
                project_requirements = {}
                
                for project_name, project_data in projects.items():
                    try:
                        requirements = self._process_single_project(project_name, project_data, stats)
                        project_requirements[project_name] = requirements
                    except Exception as e:
                        self.logger.error(f"Error processing {project_name}: {e}")
                        project_requirements[project_name] = self._generate_fallback_requirements(
                            project_name, project_data
                        )
            
            # Generate executive summary
            self.generate_executive_summary(project_requirements)
            
            self.logger.info("Step 3 requirements synthesis completed successfully")
            
        except Exception as e:
            self.logger.error(f"Step 3 processing failed: {e}")
            raise Step3ProcessingError(f"Step 3 processing failed: {e}")
        finally:
            # Cleanup
            if self.weaviate_client:
                self.weaviate_client.close()
    
    def run_incremental(self, force_regenerate: bool = False) -> None:
        """Run with incremental processing - skip existing outputs unless forced."""
        try:
            self.logger.info("Starting incremental Step 3 processing...")
            
            # Load data first to check what needs processing
            data = self.load_intermediate_data()
            projects = data.get('projects', {})
            
            if force_regenerate:
                self.logger.info("Force regenerate enabled - processing all projects")
                self.run()
                return
            
            # Filter projects that need processing
            projects_to_process = {}
            for project_name, project_data in projects.items():
                project_dir = self.projects_dir / project_name
                requirements_file = project_dir / 'requirements.md'
                
                if not requirements_file.exists():
                    projects_to_process[project_name] = project_data
                    self.logger.info(f"Project {project_name} needs processing")
                else:
                    self.logger.debug(f"Project {project_name} already processed, skipping")
            
            if not projects_to_process:
                self.logger.info("All projects already processed, updating executive summary only")
                # Still regenerate executive summary in case it's missing
                existing_requirements = {}
                for project_name in projects:
                    req_file = self.projects_dir / project_name / 'requirements.md'
                    if req_file.exists():
                        with open(req_file, 'r', encoding='utf-8') as f:
                            existing_requirements[project_name] = f.read()
                
                if existing_requirements:
                    self.generate_executive_summary(existing_requirements)
                return
            
            # Process only the projects that need it
            self.logger.info(f"Processing {len(projects_to_process)} new/modified projects")
            
            # Initialize components
            self.initialize_components()
            
            # Create output directories
            self.requirements_dir.mkdir(parents=True, exist_ok=True)
            self.projects_dir.mkdir(parents=True, exist_ok=True)
            
            # Process filtered projects
            stats = self.collect_weaviate_statistics()
            new_requirements = {}
            
            for project_name, project_data in projects_to_process.items():
                try:
                    requirements = self._process_single_project(project_name, project_data, stats)
                    new_requirements[project_name] = requirements
                except Exception as e:
                    self.logger.error(f"Error processing {project_name}: {e}")
                    new_requirements[project_name] = self._generate_fallback_requirements(
                        project_name, project_data
                    )
            
            # Collect all requirements for executive summary
            all_requirements = new_requirements.copy()
            for project_name in projects:
                if project_name not in all_requirements:
                    req_file = self.projects_dir / project_name / 'requirements.md'
                    if req_file.exists():
                        with open(req_file, 'r', encoding='utf-8') as f:
                            all_requirements[project_name] = f.read()
            
            # Generate updated executive summary
            self.generate_executive_summary(all_requirements)
            
            self.logger.info(f"Incremental Step 3 processing completed - processed {len(new_requirements)} projects")
            
        except Exception as e:
            self.logger.error(f"Incremental Step 3 processing failed: {e}")
            raise Step3ProcessingError(f"Incremental Step 3 processing failed: {e}")
        finally:
            # Cleanup
            if self.weaviate_client:
                self.weaviate_client.close()