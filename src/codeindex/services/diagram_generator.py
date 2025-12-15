"""
Diagram Generator Service

Generates architecture diagrams from codebase artifacts.
Supports multiple diagram types and output formats.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from codeindex.utils.logging import get_logger


class DiagramGenerator:
    """Generate architecture diagrams from codebase analysis."""

    def __init__(
        self,
        output_dir: Path,
        weaviate_store=None,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize diagram generator.

        Args:
            output_dir: Directory for generated diagrams
            weaviate_store: Optional Weaviate store for querying artifacts
            logger: Optional logger instance
        """
        self.output_dir = Path(output_dir)
        self.weaviate_store = weaviate_store
        self.logger = logger or get_logger(__name__)

        # Create output directory structure
        self.diagrams_dir = self.output_dir / "diagrams"
        self.component_dir = self.diagrams_dir / "component"
        self.gwt_dir = self.diagrams_dir / "gwt"
        self.database_dir = self.diagrams_dir / "database"
        self.sequence_dir = self.diagrams_dir / "sequence"

        # Create directories
        for directory in [
            self.diagrams_dir,
            self.component_dir,
            self.gwt_dir,
            self.database_dir,
            self.sequence_dir
        ]:
            directory.mkdir(parents=True, exist_ok=True)

    def generate_component_diagram(
        self,
        project_id: Optional[str] = None,
        output_format: str = "mermaid",
        style: str = "default",
        depth: int = 3
    ) -> Path:
        """
        Generate component architecture diagram.

        Args:
            project_id: Optional project filter
            output_format: Output format (mermaid, plantuml, d2, dot)
            style: Diagram style (default, detailed, minimal)
            depth: Dependency depth to include

        Returns:
            Path to generated diagram file
        """
        self.logger.info(f"Generating component diagram (format={output_format}, style={style})")

        # Load components from PRD artifacts
        components = self._load_components_from_prd(project_id)

        if not components:
            self.logger.warning("No components found for diagram generation")
            return None

        # Generate diagram based on format
        if output_format == "mermaid":
            from codeindex.services.diagram_renderers.mermaid_renderer import MermaidRenderer
            renderer = MermaidRenderer()
            diagram_content = renderer.render_component_diagram(
                components=components,
                style=style,
                depth=depth
            )
            output_file = self.component_dir / "architecture.mmd"
        else:
            raise ValueError(f"Unsupported output format: {output_format}")

        # Write diagram to file
        output_file.write_text(diagram_content, encoding="utf-8")
        self.logger.info(f"Component diagram saved to: {output_file}")

        return output_file

    def generate_gwt_mvp_diagram(
        self,
        extraction_file: Path,
        output_format: str = "mermaid",
        style: str = "default"
    ) -> Path:
        """
        Generate GWT MVP architecture diagram.

        Args:
            extraction_file: Path to extraction-results.jsonl
            output_format: Output format (mermaid, plantuml)
            style: Diagram style

        Returns:
            Path to generated diagram file
        """
        self.logger.info("Generating GWT MVP diagram")

        # Load GWT artifacts
        gwt_artifacts = self._load_gwt_artifacts(extraction_file)

        if not gwt_artifacts:
            self.logger.warning("No GWT artifacts found for diagram generation")
            return None

        # Generate diagram
        if output_format == "mermaid":
            from codeindex.services.diagram_renderers.mermaid_renderer import MermaidRenderer
            renderer = MermaidRenderer()
            diagram_content = renderer.render_gwt_mvp_diagram(
                presenters=gwt_artifacts.get('presenters', []),
                views=gwt_artifacts.get('views', []),
                style=style
            )
            output_file = self.gwt_dir / "mvp-overview.mmd"
        else:
            raise ValueError(f"Unsupported output format: {output_format}")

        # Write diagram
        output_file.write_text(diagram_content, encoding="utf-8")
        self.logger.info(f"GWT MVP diagram saved to: {output_file}")

        return output_file

    def generate_all_diagrams(
        self,
        project_id: Optional[str] = None,
        extraction_file: Optional[Path] = None,
        output_format: str = "mermaid"
    ) -> Dict[str, Path]:
        """
        Generate all available diagrams.

        Args:
            project_id: Optional project filter
            extraction_file: Optional extraction results file
            output_format: Output format for all diagrams

        Returns:
            Dictionary mapping diagram type to output file path
        """
        self.logger.info("Generating all diagrams")
        results = {}

        # Component diagram
        try:
            component_file = self.generate_component_diagram(
                project_id=project_id,
                output_format=output_format
            )
            if component_file:
                results['component'] = component_file
        except Exception as e:
            self.logger.error(f"Failed to generate component diagram: {e}")

        # GWT MVP diagram
        if extraction_file and extraction_file.exists():
            try:
                gwt_file = self.generate_gwt_mvp_diagram(
                    extraction_file=extraction_file,
                    output_format=output_format
                )
                if gwt_file:
                    results['gwt'] = gwt_file
            except Exception as e:
                self.logger.error(f"Failed to generate GWT diagram: {e}")

        # Generate README
        self._generate_readme(results)

        return results

    def _load_components_from_prd(
        self,
        project_id: Optional[str] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Load components from PRD artifacts.

        Args:
            project_id: Optional project filter

        Returns:
            Dictionary with component lists by type
        """
        components = {
            'services': [],
            'daos': [],
            'controllers': [],
            'presenters': [],
            'views': [],
            'forms': []
        }

        # Check for PRD output directories
        services_dir = self.output_dir / "services" / "services"
        frontend_dir = self.output_dir / "frontend"

        # Load services
        if services_dir.exists():
            for service_file in services_dir.glob("*.json"):
                try:
                    import json
                    with open(service_file) as f:
                        service = json.load(f)
                        components['services'].append(service)
                except Exception as e:
                    self.logger.warning(f"Failed to load service {service_file}: {e}")

        # Load frontend components
        components_dir = frontend_dir / "components"
        if components_dir.exists():
            for component_file in components_dir.glob("*.json"):
                try:
                    import json
                    with open(component_file) as f:
                        component = json.load(f)
                        component_type = component.get('component_type', 'unknown')
                        if component_type == 'gwt_presenter':
                            components['presenters'].append(component)
                        elif component_type == 'gwt_view':
                            components['views'].append(component)
                except Exception as e:
                    self.logger.warning(f"Failed to load component {component_file}: {e}")

        # Load forms
        forms_dir = frontend_dir / "forms"
        if forms_dir.exists():
            for form_file in forms_dir.glob("*.json"):
                try:
                    import json
                    with open(form_file) as f:
                        form = json.load(f)
                        components['forms'].append(form)
                except Exception as e:
                    self.logger.warning(f"Failed to load form {form_file}: {e}")

        return components

    def _load_gwt_artifacts(
        self,
        extraction_file: Path
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Load GWT artifacts from extraction file.

        Args:
            extraction_file: Path to extraction-results.jsonl

        Returns:
            Dictionary with GWT artifacts by role
        """
        import json

        artifacts = {
            'presenters': [],
            'views': [],
            'ui_binders': [],
            'rpc_servlets': []
        }

        if not extraction_file.exists():
            return artifacts

        with open(extraction_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                # Skip summary line
                if line_num == 1:
                    continue

                try:
                    artifact = json.loads(line)
                    semantic_data = artifact.get('semantic_data', {})
                    gwt_role = semantic_data.get('gwt_role')

                    if gwt_role == 'presenter':
                        artifacts['presenters'].append(artifact)
                    elif gwt_role == 'view':
                        artifacts['views'].append(artifact)
                    elif gwt_role == 'ui_binder':
                        artifacts['ui_binders'].append(artifact)
                    elif gwt_role == 'rpc_servlet':
                        artifacts['rpc_servlets'].append(artifact)
                except Exception as e:
                    self.logger.warning(f"Failed to parse line {line_num}: {e}")

        return artifacts

    def _generate_readme(self, generated_diagrams: Dict[str, Path]) -> None:
        """
        Generate README.md for diagrams directory.

        Args:
            generated_diagrams: Dictionary of diagram type to file path
        """
        readme_path = self.diagrams_dir / "README.md"

        content = f"""# Architecture Diagrams

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Tool**: CodeIndex PRD Generator

---

## Available Diagrams

"""

        for diagram_type, file_path in generated_diagrams.items():
            relative_path = file_path.relative_to(self.diagrams_dir)
            content += f"- **{diagram_type.title()}**: `{relative_path}`\n"

        content += """
---

## Viewing Diagrams

### Mermaid (.mmd)

Mermaid diagrams can be viewed in:
- **GitHub/GitLab**: Automatically rendered in markdown files
- **VS Code**: Install "Markdown Preview Mermaid Support" extension
- **Online**: Paste content at [Mermaid Live Editor](https://mermaid.live)
- **CLI**: Use `mmdc` (mermaid-cli) to convert to PNG/SVG

Example:
```bash
# Install mermaid-cli
npm install -g @mermaid-js/mermaid-cli

# Convert to SVG
mmdc -i diagram.mmd -o diagram.svg
```

### PlantUML (.puml)

PlantUML diagrams can be viewed in:
- **Online**: Upload to [PlantUML Server](http://www.plantuml.com/plantuml/)
- **VS Code**: Install "PlantUML" extension
- **IntelliJ**: Built-in PlantUML integration
- **CLI**: Use `plantuml.jar` to convert to PNG/SVG

---

## Diagram Types

### Component Diagram
Shows high-level system components and their dependencies:
- Services and business logic
- Data access objects (DAOs)
- Frontend presenters and views
- Dependencies and data flow

### GWT MVP Diagram
Documents GWT presenter-view relationships:
- MVP pattern structure
- Event handlers and RPC calls
- Navigation flows
- UI field bindings

---

## Regenerating Diagrams

```bash
# Component architecture
codeindex diagram component --output {self.output_dir}

# GWT MVP architecture
codeindex diagram gwt --output {self.output_dir}

# All diagrams
codeindex diagram all --output {self.output_dir}
```

---

Generated by CodeIndex - Java Codebase Analysis and PRD Generator
"""

        readme_path.write_text(content, encoding="utf-8")
        self.logger.info(f"Generated README at: {readme_path}")
