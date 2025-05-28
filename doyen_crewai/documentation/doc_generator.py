"""Documentation generator for Doyen CrewAI."""

import os
import json
from pathlib import Path
from typing import Dict, List, Any
import jinja2
import logging

logger = logging.getLogger(__name__)

class DocumentationGenerator:
    """Generates documentation from codebase using templates."""
    
    def __init__(self, template_dir: str):
        """Initialize the documentation generator.
        
        Args:
            template_dir: Path to the directory containing templates
        """
        self.template_dir = Path(template_dir)
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(self.template_dir)),
            autoescape=True
        )
    
    def _load_template(self, template_name: str) -> jinja2.Template:
        """Load a template by name.
        
        Args:
            template_name: Name of the template file
            
        Returns:
            Loaded Jinja2 template
        """
        return self.env.get_template(template_name)
    
    def _get_components(self, codebase_path: str) -> Dict[str, List[Dict[str, Any]]]:
        """Extract components from the codebase.
        
        Args:
            codebase_path: Path to the codebase
            
        Returns:
            Dictionary mapping directory paths to lists of components
        """
        components = {}
        for root, _, files in os.walk(codebase_path):
            dir_path = os.path.relpath(root, codebase_path)
            if dir_path == ".":
                dir_path = "root"
            
            dir_components = []
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    component = self._parse_component(file_path)
                    if component:
                        dir_components.append(component)
            
            if dir_components:
                components[dir_path] = dir_components
        
        return components
    
    def _parse_component(self, file_path: str) -> Dict[str, Any]:
        """Parse a Python file into a component.
        
        Args:
            file_path: Path to the Python file
            
        Returns:
            Component dictionary
        """
        try:
            with open(file_path, "r") as f:
                content = f.read()
            
            # Basic component info
            component = {
                "name": os.path.basename(file_path)[:-3],
                "type": "module",
                "path": file_path,
                "documentation": "",
                "dependencies": [],
                "parameters": [],
                "return_type": None,
                "children": [],
                "agent_interactions": [],
                "embedding_requirements": []
            }
            
            # Extract docstring
            docstring_start = content.find('"""')
            if docstring_start != -1:
                docstring_end = content.find('"""', docstring_start + 3)
                if docstring_end != -1:
                    component["documentation"] = content[docstring_start + 3:docstring_end].strip()
            
            # Extract imports
            for line in content.split("\n"):
                if line.startswith("import ") or line.startswith("from "):
                    component["dependencies"].append(line.strip())
            
            return component
            
        except Exception as e:
            logger.error(f"Error parsing component {file_path}: {str(e)}")
            return None
    
    def generate_prd(self, codebase_path: str, output_path: str):
        """Generate PRD documentation.
        
        Args:
            codebase_path: Path to the codebase
            output_path: Path to write the output file
        """
        template = self._load_template("prd.md.j2")
        components = self._get_components(codebase_path)
        
        # Create sample user stories
        user_stories = [
            {
                "component": "Embedding Generator",
                "role": "developer",
                "action": "generate embeddings for code entities",
                "benefit": "enable semantic search and analysis",
                "directory": "src/preprocessing"
            },
            {
                "component": "Parser Agent",
                "role": "developer",
                "action": "analyze codebase structure",
                "benefit": "understand code relationships and dependencies",
                "directory": "src/agents"
            }
        ]
        
        content = template.render(
            components=components,
            user_stories=user_stories
        )
        
        with open(output_path, "w") as f:
            f.write(content)
    
    def generate_technical_requirements(self, codebase_path: str, output_path: str):
        """Generate technical requirements documentation.
        
        Args:
            codebase_path: Path to the codebase
            output_path: Path to write the output file
        """
        template = self._load_template("technical_requirements.md.j2")
        components = self._get_components(codebase_path)
        
        content = template.render(components=components)
        
        with open(output_path, "w") as f:
            f.write(content)
    
    def generate_acceptance_criteria(self, codebase_path: str, output_path: str):
        """Generate acceptance criteria documentation.
        
        Args:
            codebase_path: Path to the codebase
            output_path: Path to write the output file
        """
        template = self._load_template("acceptance_criteria.md.j2")
        components = self._get_components(codebase_path)
        
        # Add test scenarios and success metrics
        for dir_components in components.values():
            for component in dir_components:
                component["test_scenarios"] = [
                    f"Test {component['name']} initialization",
                    f"Test {component['name']} functionality",
                    f"Test {component['name']} error handling"
                ]
                component["success_metrics"] = [
                    f"{component['name']} should pass all unit tests",
                    f"{component['name']} should meet performance requirements",
                    f"{component['name']} should handle errors gracefully"
                ]
        
        content = template.render(components=components)
        
        with open(output_path, "w") as f:
            f.write(content)
    
    def generate_component_docs(self, codebase_path: str, output_dir: str):
        """Generate documentation for each component.
        
        Args:
            codebase_path: Path to the codebase
            output_dir: Directory to write the output files
        """
        template = self._load_template("component.md.j2")
        components = self._get_components(codebase_path)
        
        os.makedirs(output_dir, exist_ok=True)
        
        for dir_path, dir_components in components.items():
            for component in dir_components:
                # Add agent interactions and embedding requirements
                component["agent_interactions"] = [
                    f"Interacts with {dep}" for dep in component["dependencies"]
                    if "agent" in dep.lower()
                ]
                component["embedding_requirements"] = [
                    "Must generate embeddings efficiently",
                    "Should support batch processing",
                    "Must handle errors gracefully"
                ]
                
                content = template.render(component=component)
                output_path = os.path.join(
                    output_dir,
                    f"{component['name']}.md"
                )
                
                with open(output_path, "w") as f:
                    f.write(content)
    
    def generate_all_docs(self, codebase_path: str, output_dir: str):
        """Generate all documentation.
        
        Args:
            codebase_path: Path to the codebase
            output_dir: Directory to write the output files
        """
        os.makedirs(output_dir, exist_ok=True)
        
        self.generate_prd(
            codebase_path,
            os.path.join(output_dir, "prd.md")
        )
        
        self.generate_technical_requirements(
            codebase_path,
            os.path.join(output_dir, "technical_requirements.md")
        )
        
        self.generate_acceptance_criteria(
            codebase_path,
            os.path.join(output_dir, "acceptance_criteria.md")
        )
        
        self.generate_component_docs(
            codebase_path,
            os.path.join(output_dir, "components")
        ) 