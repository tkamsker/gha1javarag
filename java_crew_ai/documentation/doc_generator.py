import os
from typing import Dict, List, Any
from pathlib import Path
import json
from jinja2 import Environment, FileSystemLoader
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentationGenerator:
    def __init__(self, analyzer_output: Dict[str, Any], output_dir: str = "documentation"):
        """Initialize the documentation generator."""
        self.analyzer_output = analyzer_output
        self.output_dir = Path(output_dir)
        self.template_dir = Path(__file__).parent / "templates"
        self.env = Environment(loader=FileSystemLoader(str(self.template_dir)))
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_documentation(self):
        """Generate all documentation files."""
        try:
            # Generate PRD
            self._generate_prd()
            
            # Generate technical requirements
            self._generate_technical_requirements()
            
            # Generate acceptance criteria
            self._generate_acceptance_criteria()
            
            # Generate component documentation
            self._generate_component_docs()
            
            logger.info("Documentation generation completed successfully")
        except Exception as e:
            logger.error(f"Failed to generate documentation: {str(e)}")
            raise
    
    def _generate_prd(self):
        """Generate Product Requirements Document."""
        template = self.env.get_template("prd.md.j2")
        
        # Group components by directory
        components_by_dir = self._group_components_by_directory()
        
        # Generate user stories
        user_stories = self._generate_user_stories(components_by_dir)
        
        # Render PRD
        prd_content = template.render(
            components=components_by_dir,
            user_stories=user_stories
        )
        
        # Write to file
        with open(self.output_dir / "product_requirements.md", "w") as f:
            f.write(prd_content)
    
    def _generate_technical_requirements(self):
        """Generate technical requirements document."""
        template = self.env.get_template("technical_requirements.md.j2")
        
        # Group components by directory
        components_by_dir = self._group_components_by_directory()
        
        # Generate technical requirements
        requirements = self._generate_technical_requirements_content(components_by_dir)
        
        # Render technical requirements
        tech_content = template.render(
            components=components_by_dir,
            requirements=requirements
        )
        
        # Write to file
        with open(self.output_dir / "technical_requirements.md", "w") as f:
            f.write(tech_content)
    
    def _generate_acceptance_criteria(self):
        """Generate acceptance criteria document."""
        template = self.env.get_template("acceptance_criteria.md.j2")
        
        # Group components by directory
        components_by_dir = self._group_components_by_directory()
        
        # Generate acceptance criteria
        criteria = self._generate_acceptance_criteria_content(components_by_dir)
        
        # Render acceptance criteria
        criteria_content = template.render(
            components=components_by_dir,
            criteria=criteria
        )
        
        # Write to file
        with open(self.output_dir / "acceptance_criteria.md", "w") as f:
            f.write(criteria_content)
    
    def _generate_component_docs(self):
        """Generate documentation for each component."""
        template = self.env.get_template("component.md.j2")
        
        # Create components directory
        components_dir = self.output_dir / "components"
        components_dir.mkdir(exist_ok=True)
        
        # Generate documentation for each component
        for key, component in self.analyzer_output['components'].items():
            # Render component documentation
            component_content = template.render(component=component)
            
            # Write to file
            component_file = components_dir / f"{component['name']}.md"
            with open(component_file, "w") as f:
                f.write(component_content)
    
    def _group_components_by_directory(self) -> Dict[str, List[Dict]]:
        """Group components by their directory."""
        components_by_dir = {}
        
        for key, component in self.analyzer_output['components'].items():
            dir_path = os.path.dirname(component['path'])
            if dir_path not in components_by_dir:
                components_by_dir[dir_path] = []
            components_by_dir[dir_path].append(component)
        
        return components_by_dir
    
    def _generate_user_stories(self, components_by_dir: Dict[str, List[Dict]]) -> List[Dict]:
        """Generate user stories based on components."""
        user_stories = []
        
        for dir_path, components in components_by_dir.items():
            for component in components:
                if component['type'] in ['class', 'interface']:
                    # Generate user story for the component
                    story = {
                        'role': 'user',
                        'action': f"use {component['name']}",
                        'benefit': self._extract_benefit_from_docs(component['documentation']),
                        'component': component['name'],
                        'directory': dir_path
                    }
                    user_stories.append(story)
        
        return user_stories
    
    def _generate_technical_requirements_content(self, components_by_dir: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        """Generate technical requirements content."""
        requirements = {}
        
        for dir_path, components in components_by_dir.items():
            requirements[dir_path] = []
            for component in components:
                req = {
                    'name': component['name'],
                    'type': component['type'],
                    'dependencies': component['dependencies'],
                    'modifiers': component['modifiers'],
                    'documentation': component['documentation']
                }
                requirements[dir_path].append(req)
        
        return requirements
    
    def _generate_acceptance_criteria_content(self, components_by_dir: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        """Generate acceptance criteria content."""
        criteria = {}
        
        for dir_path, components in components_by_dir.items():
            criteria[dir_path] = []
            for component in components:
                criterion = {
                    'component': component['name'],
                    'type': component['type'],
                    'test_scenarios': self._generate_test_scenarios(component),
                    'success_metrics': self._generate_success_metrics(component)
                }
                criteria[dir_path].append(criterion)
        
        return criteria
    
    def _extract_benefit_from_docs(self, documentation: str) -> str:
        """Extract benefit from component documentation."""
        # This is a simple implementation. You might want to enhance it
        # to better parse the documentation and extract meaningful benefits
        if not documentation:
            return "improve system functionality"
        
        # Try to extract the first sentence or meaningful phrase
        sentences = documentation.split('.')
        if sentences:
            return sentences[0].strip()
        return "improve system functionality"
    
    def _generate_test_scenarios(self, component: Dict) -> List[str]:
        """Generate test scenarios for a component."""
        scenarios = []
        
        if component['type'] == 'method':
            # Generate test scenarios for methods
            scenarios.append(f"Test {component['name']} with valid input parameters")
            scenarios.append(f"Test {component['name']} with invalid input parameters")
            scenarios.append(f"Test {component['name']} with edge cases")
        elif component['type'] in ['class', 'interface']:
            # Generate test scenarios for classes/interfaces
            scenarios.append(f"Test {component['name']} initialization")
            scenarios.append(f"Test {component['name']} with all its methods")
            scenarios.append(f"Test {component['name']} integration with other components")
        
        return scenarios
    
    def _generate_success_metrics(self, component: Dict) -> List[str]:
        """Generate success metrics for a component."""
        metrics = []
        
        if component['type'] == 'method':
            # Generate success metrics for methods
            metrics.append(f"{component['name']} executes successfully")
            metrics.append(f"{component['name']} returns expected results")
            metrics.append(f"{component['name']} handles errors appropriately")
        elif component['type'] in ['class', 'interface']:
            # Generate success metrics for classes/interfaces
            metrics.append(f"{component['name']} initializes correctly")
            metrics.append(f"{component['name']} maintains data integrity")
            metrics.append(f"{component['name']} integrates successfully with other components")
        
        return metrics 