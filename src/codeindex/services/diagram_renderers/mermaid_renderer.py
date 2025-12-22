"""
Mermaid Diagram Renderer

Generates diagrams in Mermaid format for GitHub/GitLab rendering.
"""

from typing import List, Dict, Any, Set
from pathlib import Path


class MermaidRenderer:
    """Render diagrams in Mermaid format."""

    def _extract_component_name(self, component: Dict[str, Any], fallback: str = 'Unknown') -> str:
        """
        Extract correct component name from various sources.

        Args:
            component: Component artifact dictionary
            fallback: Fallback name if extraction fails

        Returns:
            Component name
        """
        name = component.get('name', '')

        # If name is invalid, try alternative sources
        if not name or name == 'View':
            # Try id field (e.g., "gwt_presenter_AdminMainPresenter")
            comp_id = component.get('id', '')
            if comp_id:
                # Extract name from id: "gwt_presenter_AdminMainPresenter" -> "AdminMainPresenter"
                parts = comp_id.split('_', 2)
                if len(parts) >= 3:
                    name = parts[2]

            # Try source_file or file_path
            if not name or name == 'View':
                source_file = component.get('source_file') or component.get('file_path', '')
                if source_file:
                    from pathlib import Path
                    name = Path(source_file).stem

            # Try entities list
            if not name or name == 'View':
                semantic = component.get('semantic_data', {})
                entities = semantic.get('entities', [])
                # Look for entity ending with Presenter or View
                for entity in entities:
                    if 'Presenter' in entity or 'View' in entity:
                        name = entity
                        break

        return name if name and name != 'View' else fallback

    def render_component_diagram(
        self,
        components: Dict[str, List[Dict[str, Any]]],
        style: str = "default",
        depth: int = 3
    ) -> str:
        """
        Render component architecture diagram in Mermaid format.

        Args:
            components: Dictionary with component lists by type
            style: Diagram style (default, detailed, minimal)
            depth: Dependency depth to include

        Returns:
            Mermaid diagram content as string
        """
        lines = []

        # Header
        lines.append("graph TB")
        lines.append("")

        # Frontend Layer
        presenters = components.get('presenters', [])
        views = components.get('views', [])
        forms = components.get('forms', [])

        if presenters or views or forms:
            lines.append("    subgraph Frontend[\"Frontend Layer\"]")

            # Add presenters
            for presenter in presenters[:10]:  # Limit to 10
                name = self._extract_component_name(presenter, 'UnknownPresenter')
                node_id = self._sanitize_id(name)
                lines.append(f"        {node_id}[{name}]")

            # Add views
            for view in views[:10]:  # Limit to 10
                name = self._extract_component_name(view, 'UnknownView')
                node_id = self._sanitize_id(name)
                lines.append(f"        {node_id}[{name}]")

            # Add forms
            if style == "detailed":
                for form in forms[:5]:  # Limit to 5
                    name = form.get('name', 'UnknownForm')
                    node_id = self._sanitize_id(name)
                    lines.append(f"        {node_id}[{name}]")

            lines.append("    end")
            lines.append("")

        # Backend Layer
        services = components.get('services', [])
        daos = components.get('daos', [])

        if services or daos:
            lines.append("    subgraph Backend[\"Backend Layer\"]")

            # Add services
            for service in services[:15]:  # Limit to 15
                class_name = service.get('class_name', service.get('name', 'UnknownService'))
                node_id = self._sanitize_id(class_name)
                lines.append(f"        {node_id}[{class_name}]")

            # Add DAOs
            if daos:
                for dao in daos[:10]:  # Limit to 10
                    name = dao.get('name', 'UnknownDAO')
                    node_id = self._sanitize_id(name)
                    lines.append(f"        {node_id}[{name}]")

            lines.append("    end")
            lines.append("")

        # Data Layer
        lines.append("    subgraph Data[\"Data Layer\"]")
        lines.append("        DB[(Database)]")
        lines.append("    end")
        lines.append("")

        # Add connections
        lines.extend(self._generate_connections(components, style))

        # Styling
        lines.append("")
        lines.append("    classDef frontend fill:#e1f5ff,stroke:#01579b,stroke-width:2px")
        lines.append("    classDef backend fill:#fff9e1,stroke:#f57f17,stroke-width:2px")
        lines.append("    classDef data fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px")
        lines.append("")
        lines.append("    class Frontend frontend")
        lines.append("    class Backend backend")
        lines.append("    class Data data")

        return "\n".join(lines)

    def render_gwt_mvp_diagram(
        self,
        presenters: List[Dict[str, Any]],
        views: List[Dict[str, Any]],
        style: str = "default",
        navigation_graph: Any = None,
        presenter_view_bindings: Dict[str, Any] = None
    ) -> str:
        """
        Render GWT MVP architecture diagram in Mermaid format.

        Implements T079 (navigation flows) and T080 (binding relationships).

        Args:
            presenters: List of presenter artifacts
            views: List of view artifacts
            style: Diagram style
            navigation_graph: Optional navigation graph with navigation edges
            presenter_view_bindings: Optional presenter-view-UiBinder bindings

        Returns:
            Mermaid diagram content as string
        """
        lines = []

        # Header
        lines.append("graph TB")
        lines.append("")

        # Presenters
        if presenters:
            lines.append("    subgraph Presenters[\"GWT Presenters\"]")
            for presenter in presenters[:10]:  # Limit to 10
                semantic = presenter.get('semantic_data', {})

                # Try to get presenter name from multiple sources
                name = semantic.get('presenter_name', '')
                if not name or name == 'View':
                    # Try to extract from file path
                    file_path = presenter.get('file_path', '')
                    if file_path:
                        from pathlib import Path
                        name = Path(file_path).stem
                    # Or use first entity that ends with Presenter
                    if not name or name == 'View':
                        entities = semantic.get('entities', [])
                        for entity in entities:
                            if 'Presenter' in entity:
                                name = entity
                                break
                if not name:
                    name = 'UnknownPresenter'

                node_id = self._sanitize_id(name)

                # Get event handler count
                event_count = len(semantic.get('event_handlers', []))
                rpc_count = len(semantic.get('rpc_calls', []))

                if style == "detailed":
                    label = f"{name}\\n({event_count} events, {rpc_count} RPC)"
                else:
                    label = name

                lines.append(f"        {node_id}[\"{label}\"]")

            lines.append("    end")
            lines.append("")

        # Views
        if views:
            lines.append("    subgraph Views[\"GWT Views\"]")
            for view in views[:10]:  # Limit to 10
                semantic = view.get('semantic_data', {})
                name = semantic.get('view_name', 'UnknownView')
                node_id = self._sanitize_id(name)

                # Get UI field count
                ui_field_count = len(semantic.get('ui_fields', []))

                if style == "detailed":
                    label = f"{name}\\n({ui_field_count} fields)"
                else:
                    label = name

                lines.append(f"        {node_id}[\"{label}\"]")

            lines.append("    end")
            lines.append("")

        # RPC Services
        rpc_services = self._extract_rpc_services(presenters)
        if rpc_services:
            lines.append("    subgraph RPCServices[\"RPC Services\"]")
            for service in list(rpc_services)[:8]:  # Limit to 8
                node_id = self._sanitize_id(f"RPC_{service}")
                lines.append(f"        {node_id}[\"{service}\"]")
            lines.append("    end")
            lines.append("")

        # T080: Add UiBinder templates section if bindings provided
        if presenter_view_bindings and style == "detailed":
            lines.append("    subgraph UiBinder[\"UiBinder Templates\"]")
            # Show up to 5 templates
            template_count = 0
            for presenter_class, binding in list(presenter_view_bindings.items())[:5]:
                if binding.get('template_file'):
                    template_name = Path(binding['template_file']).stem
                    template_id = self._sanitize_id(f"Template_{template_name}")
                    confidence = binding.get('confidence', 0) * 100
                    lines.append(f"        {template_id}[\"{template_name}.ui.xml\\n({confidence:.0f}% confidence)\"]")
                    template_count += 1

            if template_count == 0:
                lines.append("        NoTemplates[\"No templates found\"]")

            lines.append("    end")
            lines.append("")

        # Add connections (T079: includes navigation flows)
        lines.extend(self._generate_gwt_connections(
            presenters, views, rpc_services, style,
            navigation_graph=navigation_graph,
            presenter_view_bindings=presenter_view_bindings
        ))

        # Styling
        lines.append("")
        lines.append("    classDef presenter fill:#e1f5ff,stroke:#01579b,stroke-width:2px")
        lines.append("    classDef view fill:#fff9e1,stroke:#f57f17,stroke-width:2px")
        lines.append("    classDef rpc fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px")

        return "\n".join(lines)

    def _sanitize_id(self, name: str) -> str:
        """
        Sanitize name for use as Mermaid node ID.

        Args:
            name: Original name

        Returns:
            Sanitized ID safe for Mermaid
        """
        # Remove special characters, replace with underscore
        import re
        sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        # Ensure doesn't start with number
        if sanitized and sanitized[0].isdigit():
            sanitized = f"N{sanitized}"
        return sanitized or "Unknown"

    def _generate_connections(
        self,
        components: Dict[str, List[Dict[str, Any]]],
        style: str
    ) -> List[str]:
        """
        Generate connection lines between components.

        Args:
            components: Dictionary with component lists
            style: Diagram style

        Returns:
            List of connection lines
        """
        lines = []

        presenters = components.get('presenters', [])
        views = components.get('views', [])
        services = components.get('services', [])
        daos = components.get('daos', [])

        # Presenter -> View connections
        for presenter in presenters[:10]:
            presenter_name = self._extract_component_name(presenter, '')
            if not presenter_name:
                continue
            presenter_id = self._sanitize_id(presenter_name)

            # Try to find matching view
            view_name = presenter_name.replace('Presenter', 'View')
            for view in views:
                extracted_view_name = self._extract_component_name(view, '')
                if extracted_view_name == view_name:
                    view_id = self._sanitize_id(extracted_view_name)
                    lines.append(f"    {presenter_id} -->|Display| {view_id}")
                    break

        # Presenter -> Service connections (via RPC)
        for presenter in presenters[:10]:
            semantic = presenter.get('semantic_data', {})
            rpc_calls = semantic.get('rpc_calls', [])

            if rpc_calls:
                presenter_id = self._sanitize_id(presenter.get('name', ''))
                # Connect to first RPC service mentioned
                if rpc_calls:
                    service_name = rpc_calls[0].get('service', 'Service')
                    service_id = self._sanitize_id(service_name)
                    lines.append(f"    {presenter_id} -->|RPC| {service_id}")

        # Service -> DAO connections
        for service in services[:10]:
            service_name = service.get('class_name', service.get('name', ''))
            service_id = self._sanitize_id(service_name)

            # Try to find matching DAO
            dao_name = service_name.replace('Service', 'DAO')
            for dao in daos:
                if dao.get('name', '') == dao_name:
                    dao_id = self._sanitize_id(dao_name)
                    lines.append(f"    {service_id} --> {dao_id}")
                    break

        # DAO -> Database connections
        for dao in daos[:5]:
            dao_name = dao.get('name', '')
            dao_id = self._sanitize_id(dao_name)
            lines.append(f"    {dao_id} --> DB")

        return lines

    def _generate_gwt_connections(
        self,
        presenters: List[Dict[str, Any]],
        views: List[Dict[str, Any]],
        rpc_services: Set[str],
        style: str,
        navigation_graph: Any = None,
        presenter_view_bindings: Dict[str, Any] = None
    ) -> List[str]:
        """
        Generate connections for GWT MVP diagram.

        Implements T079 (navigation flows) and T080 (binding relationships).

        Args:
            presenters: List of presenters
            views: List of views
            rpc_services: Set of RPC service names
            style: Diagram style
            navigation_graph: Optional navigation graph with navigation edges
            presenter_view_bindings: Optional presenter-view-UiBinder bindings

        Returns:
            List of connection lines
        """
        lines = []

        # T080: Presenter -> View -> UiBinder connections (if bindings provided)
        if presenter_view_bindings:
            for presenter_class, binding in list(presenter_view_bindings.items())[:10]:
                presenter_name = presenter_class.split('.')[-1]
                presenter_id = self._sanitize_id(presenter_name)

                view_class = binding.get('view_class')
                if view_class:
                    view_name = view_class.split('.')[-1]
                    view_id = self._sanitize_id(view_name)

                    confidence = binding.get('confidence', 0)
                    pattern = binding.get('binding_pattern', '')

                    if confidence >= 0.7:
                        label = f"binds ({confidence*100:.0f}%)"
                    else:
                        label = "weak binding"

                    lines.append(f"    {presenter_id} -->|{label}| {view_id}")

                    # View -> UiBinder template connection
                    if binding.get('template_file') and style == "detailed":
                        template_name = Path(binding['template_file']).stem
                        template_id = self._sanitize_id(f"Template_{template_name}")
                        lines.append(f"    {view_id} -->|uses| {template_id}")

        # Original presenter -> View connections (fallback if no bindings)
        if not presenter_view_bindings:
            for presenter in presenters[:10]:
                semantic = presenter.get('semantic_data', {})

                # Get presenter name (same logic as render method)
                presenter_name = semantic.get('presenter_name', '')
                if not presenter_name or presenter_name == 'View':
                    file_path = presenter.get('file_path', '')
                    if file_path:
                        from pathlib import Path
                        presenter_name = Path(file_path).stem
                    if not presenter_name or presenter_name == 'View':
                        entities = semantic.get('entities', [])
                        for entity in entities:
                            if 'Presenter' in entity:
                                presenter_name = entity
                                break
                if not presenter_name:
                    presenter_name = 'UnknownPresenter'

                presenter_id = self._sanitize_id(presenter_name)

                # Try to find matching view by name
                view_binding = semantic.get('view_binding')
                if not view_binding or not isinstance(view_binding, str):
                    view_binding = presenter_name.replace('Presenter', 'View')

                for view in views:
                    view_semantic = view.get('semantic_data', {})
                    view_name = view_semantic.get('view_name', '')
                    if view_name and (view_binding in view_name or view_name in presenter_name):
                        view_id = self._sanitize_id(view_name)
                        lines.append(f"    {presenter_id} -->|binds| {view_id}")
                        break

        # Presenter -> RPC Service connections
        for presenter in presenters[:10]:
            semantic = presenter.get('semantic_data', {})

            # Get presenter name (same logic as above)
            presenter_name = semantic.get('presenter_name', '')
            if not presenter_name or presenter_name == 'View':
                file_path = presenter.get('file_path', '')
                if file_path:
                    from pathlib import Path
                    presenter_name = Path(file_path).stem
                if not presenter_name or presenter_name == 'View':
                    entities = semantic.get('entities', [])
                    for entity in entities:
                        if 'Presenter' in entity:
                            presenter_name = entity
                            break
            if not presenter_name:
                presenter_name = 'UnknownPresenter'

            presenter_id = self._sanitize_id(presenter_name)
            rpc_calls = semantic.get('rpc_calls', [])

            for rpc in rpc_calls[:3]:  # Limit to 3 RPC calls per presenter
                service_name = rpc.get('service', '')
                if service_name in rpc_services:
                    service_id = self._sanitize_id(f"RPC_{service_name}")
                    method = rpc.get('method', '')
                    if style == "detailed" and method:
                        lines.append(f"    {presenter_id} -->|{method}| {service_id}")
                    else:
                        lines.append(f"    {presenter_id} --> {service_id}")

        # T079: Add navigation flows if navigation_graph provided
        if navigation_graph:
            # Extract navigation edges from graph
            nav_edges = getattr(navigation_graph, 'edges', [])

            # Add navigation connections (limit to avoid clutter)
            for source_id, target_id in nav_edges[:10]:
                # Extract simple names from module IDs
                source_name = source_id.split('.')[-1] if '.' in source_id else source_id
                target_name = target_id.split('.')[-1] if '.' in target_id else target_id

                source_node = self._sanitize_id(source_name)
                target_node = self._sanitize_id(target_name)

                # Add navigation edge with distinct style
                lines.append(f"    {source_node} -.->|navigates to| {target_node}")

        return lines

    def _extract_rpc_services(
        self,
        presenters: List[Dict[str, Any]]
    ) -> Set[str]:
        """
        Extract unique RPC service names from presenters.

        Args:
            presenters: List of presenter artifacts

        Returns:
            Set of unique RPC service names
        """
        services = set()

        for presenter in presenters:
            semantic = presenter.get('semantic_data', {})
            rpc_calls = semantic.get('rpc_calls', [])
            for rpc in rpc_calls:
                service_name = rpc.get('service', '')
                if service_name:
                    services.add(service_name)

        return services
