"""
Requirements generator for creating documentation from indexed data.
"""

from typing import Dict, List, Any, Optional
from pathlib import Path
import logging


class RequirementsGenerator:
    """Generates requirements documentation from indexed data."""
    
    def __init__(self, config, weaviate_client):
        """Initialize requirements generator."""
        self.config = config
        self.weaviate_client = weaviate_client
        self.logger = logging.getLogger(__name__)
    
    def generate_requirements(self, project_name: str = None):
        """Generate requirements documentation."""
        try:
            if project_name:
                self._generate_project_requirements(project_name)
            else:
                self._generate_all_requirements()
        
        except Exception as e:
            self.logger.error(f"Error generating requirements: {e}")
            raise
    
    def _generate_all_requirements(self):
        """Generate requirements for all projects."""
        # Query all projects from Weaviate
        projects = self._get_projects()
        
        for project in projects:
            self._generate_project_requirements(project)
        
        # Generate master requirements
        self._generate_master_requirements(projects)
    
    def _generate_project_requirements(self, project_name: str):
        """Generate requirements for a specific project."""
        self.logger.info(f"Generating requirements for project: {project_name}")
        
        # Query data for each architectural layer
        database_data = self._query_layer_data(project_name, 'database')
        backend_data = self._query_layer_data(project_name, 'backend')
        ui_data = self._query_layer_data(project_name, 'ui')
        
        # Generate requirements for each layer
        self._generate_layer_requirements(project_name, 'database', database_data)
        self._generate_layer_requirements(project_name, 'backend', backend_data)
        self._generate_layer_requirements(project_name, 'ui', ui_data)
    
    def _query_layer_data(self, project_name: str, layer: str) -> List[Dict[str, Any]]:
        """Query data for a specific architectural layer."""
        # This would typically query Weaviate for data
        # For now, return empty list as placeholder
        return []
    
    def _generate_layer_requirements(self, project_name: str, layer: str, data: List[Dict[str, Any]]):
        """Generate requirements for a specific layer."""
        requirements_dir = Path(self.config.output_dir) / 'requirements' / project_name
        requirements_dir.mkdir(parents=True, exist_ok=True)
        
        layer_file = requirements_dir / f'{layer}_requirements.md'
        
        with open(layer_file, 'w', encoding='utf-8') as f:
            f.write(f"# {project_name} - {layer.title()} Layer Requirements\n\n")
            f.write("## 1. Overview\n")
            f.write(f"Brief purpose within the application for the {layer} layer.\n\n")
            f.write("## 2. Components\n")
            f.write("- [To be populated from Weaviate data]\n\n")
            f.write("## 3. Functionality\n")
            f.write("- **Main Features:** [To be populated]\n")
            f.write("- **Inputs/Outputs:** [To be populated]\n")
            f.write("- **Key Methods/Functions:** [To be populated]\n\n")
            f.write("## 4. Dependencies\n")
            f.write("- [To be populated]\n\n")
            f.write("## 5. Notes\n")
            f.write("- [To be populated]\n")
    
    def _generate_master_requirements(self, projects: List[str]):
        """Generate master requirements document."""
        master_file = Path(self.config.output_dir) / 'requirements' / '_master.md'
        
        with open(master_file, 'w', encoding='utf-8') as f:
            f.write("# Master Requirements Document\n\n")
            f.write("## Overview\n")
            f.write("Consolidated requirements from all analyzed projects.\n\n")
            f.write("## Projects\n")
            for project in projects:
                f.write(f"- [{project}](./{project}/)\n")
            f.write("\n## Architectural Layers\n")
            f.write("- [Database Layer](./database/)\n")
            f.write("- [Backend Layer](./backend/)\n")
            f.write("- [UI Layer](./ui/)\n")
    
    def _get_projects(self) -> List[str]:
        """Get list of all projects from Weaviate."""
        # This would typically query Weaviate for unique project names
        # For now, return empty list as placeholder
        return []
