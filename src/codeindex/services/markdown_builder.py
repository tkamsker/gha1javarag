"""
Markdown Document Builder Service for PRD Generation.

This module provides markdown generation functionality for creating
Product Requirements Documents from extracted codebase artifacts.
"""
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from codeindex.models.prd import (
    DatabaseEntity,
    ServiceDefinition,
    FormDefinition,
    UIComponent,
    NavigationFlow,
    BusinessRule,
    APIEndpoint,
    PRDSection,
    AnalysisLayer,
)


class MarkdownBuilder:
    """
    Builder for generating markdown documentation from PRD entities.

    This class provides methods to generate markdown documents for
    different layers of the application (database, services, frontend)
    and to assemble complete PRD documents.
    """

    @staticmethod
    def build_entity_markdown(entity: DatabaseEntity) -> str:
        """
        Build markdown documentation for a database entity.

        Args:
            entity: DatabaseEntity to document

        Returns:
            Markdown string
        """
        lines = []

        # Header
        lines.append(f"# {entity.name}\n")

        # Metadata
        lines.append("## Overview\n")
        lines.append(f"- **Type**: {entity.source_type.value if entity.source_type else 'Unknown'}")
        lines.append(f"- **Qualified Name**: `{entity.qualified_name}`")
        lines.append(f"- **Domain**: {entity.domain or 'N/A'}")
        if entity.estimated_row_count:
            lines.append(f"- **Estimated Row Count**: {entity.estimated_row_count:,}")
        lines.append("")

        # Description
        if entity.description:
            lines.append("## Description\n")
            lines.append(entity.description)
            lines.append("")

        # Columns
        if entity.columns:
            lines.append("## Columns\n")
            headers = ["Name", "Type", "Constraints"]
            rows = []
            for col in entity.columns:
                constraints = []
                if col.is_primary_key:
                    constraints.append("PRIMARY KEY")
                if col.is_foreign_key:
                    constraints.append("FOREIGN KEY")
                if col.nullable:
                    constraints.append("NULLABLE")
                if col.unique:
                    constraints.append("UNIQUE")
                if col.default_value:
                    constraints.append(f"DEFAULT: {col.default_value}")

                rows.append([
                    col.name,
                    col.data_type,
                    ", ".join(constraints) if constraints else "-"
                ])

            lines.append(MarkdownBuilder.format_table(headers, rows))
            lines.append("")

        # Primary Key
        if entity.primary_key:
            lines.append("## Primary Key\n")
            pk_cols = ", ".join([f"`{col}`" for col in entity.primary_key])
            lines.append(f"- {pk_cols}")
            lines.append("")

        # Foreign Keys
        if entity.foreign_keys:
            lines.append("## Foreign Keys\n")
            for fk in entity.foreign_keys:
                fk_cols = ", ".join([f"`{col}`" for col in fk.columns])
                ref_cols = ", ".join([f"`{col}`" for col in fk.referenced_columns])
                lines.append(f"- **{fk.name}**: {fk_cols} → {fk.referenced_table}({ref_cols})")
            lines.append("")

        # Indexes
        if entity.indexes:
            lines.append("## Indexes\n")
            for idx in entity.indexes:
                idx_cols = ", ".join([f"`{col}`" for col in idx.columns])
                idx_type = f" ({idx.index_type})" if idx.index_type else ""
                unique_label = " (UNIQUE)" if idx.unique else ""
                lines.append(f"- **{idx.name}**{idx_type}{unique_label}: {idx_cols}")
            lines.append("")

        # Constraints
        if entity.constraints:
            lines.append("## Constraints\n")
            for constraint in entity.constraints:
                lines.append(f"- **{constraint.name}** ({constraint.constraint_type}): {constraint.definition}")
            lines.append("")

        # Business Rules
        if entity.business_rules:
            lines.append("## Business Rules\n")
            for rule_id in entity.business_rules:
                lines.append(f"- [{rule_id}](../../business_rules/{rule_id}.json)")
            lines.append("")

        # Source Files
        lines.append("## Source Files\n")
        for source_file in entity.source_files:
            lines.append(f"- `{source_file}`")
        lines.append("")

        # Metadata
        lines.append("---\n")
        lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

        return "\n".join(lines)

    @staticmethod
    def build_service_markdown(service: ServiceDefinition) -> str:
        """
        Build markdown documentation for a service.

        Args:
            service: ServiceDefinition to document

        Returns:
            Markdown string
        """
        lines = []

        # Header
        lines.append(f"# {service.class_name}\n")

        # Metadata
        lines.append("## Overview\n")
        lines.append(f"- **Package**: `{service.package}`")
        lines.append(f"- **Qualified Name**: `{service.qualified_name}`")
        lines.append(f"- **Type**: {service.service_type.value if service.service_type else 'Unknown'}")
        lines.append(f"- **Domain**: {service.domain or 'N/A'}")
        lines.append("")

        # Description
        if service.description:
            lines.append("## Description\n")
            lines.append(service.description)
            lines.append("")

        # Frameworks
        if service.frameworks:
            lines.append("## Frameworks\n")
            for fw in service.frameworks:
                lines.append(f"- {fw}")
            lines.append("")

        # Operations
        if service.operations:
            lines.append("## Operations\n")
            for op in service.operations:
                # Operation signature
                params = ", ".join([f"{p.name}: {p.data_type}" for p in op.parameters])
                lines.append(f"### {op.name}({params})\n")

                # Description
                if op.description:
                    lines.append(op.description)
                    lines.append("")

                # Visibility and modifiers
                lines.append(f"- **Visibility**: {op.visibility}")
                if op.return_type:
                    lines.append(f"- **Returns**: {op.return_type}")
                if op.annotations:
                    lines.append(f"- **Annotations**: {', '.join([f'@{a}' for a in op.annotations])}")
                if op.exceptions_thrown:
                    lines.append(f"- **Throws**: {', '.join(op.exceptions_thrown)}")
                if op.line_number:
                    lines.append(f"- **Location**: Line {op.line_number}")
                lines.append("")

        # Dependencies
        if service.dependencies:
            lines.append("## Dependencies\n")
            for dep in service.dependencies:
                dep_type = f" ({dep.dependency_type})" if dep.dependency_type else ""
                lines.append(f"- **{dep.name}**{dep_type}: `{dep.qualified_name}`")
            lines.append("")

        # Data Dependencies
        if service.data_dependencies:
            lines.append("## Data Dependencies\n")
            for entity_id in service.data_dependencies:
                lines.append(f"- [{entity_id}](../../database/entities/{entity_id}.json)")
            lines.append("")

        # API Endpoints
        if service.endpoints:
            lines.append("## API Endpoints\n")
            for endpoint_id in service.endpoints:
                lines.append(f"- [{endpoint_id}](../endpoints/{endpoint_id}.json)")
            lines.append("")

        # Transaction Boundaries
        if service.transaction_boundaries:
            lines.append("## Transaction Boundaries\n")
            for tx in service.transaction_boundaries:
                lines.append(f"- **{tx.method_name}**")
                if tx.propagation:
                    lines.append(f"  - Propagation: {tx.propagation}")
                if tx.isolation:
                    lines.append(f"  - Isolation: {tx.isolation}")
                if tx.read_only is not None:
                    lines.append(f"  - Read-Only: {tx.read_only}")
            lines.append("")

        # Business Rules
        if service.business_rules:
            lines.append("## Business Rules\n")
            for rule_id in service.business_rules:
                lines.append(f"- [{rule_id}](../../business_rules/{rule_id}.json)")
            lines.append("")

        # Source File
        lines.append("## Source File\n")
        lines.append(f"- `{service.source_file}`")
        lines.append("")

        # Metadata
        lines.append("---\n")
        lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

        return "\n".join(lines)

    @staticmethod
    def build_form_markdown(form: FormDefinition) -> str:
        """
        Build markdown documentation for a form.

        Args:
            form: FormDefinition to document

        Returns:
            Markdown string
        """
        lines = []

        # Header
        lines.append(f"# {form.name}\n")

        # Metadata
        lines.append("## Overview\n")
        lines.append(f"- **Type**: {form.form_type.value if form.form_type else 'Unknown'}")
        lines.append(f"- **Domain**: {form.domain or 'N/A'}")
        lines.append("")

        # Description
        if form.description:
            lines.append("## Description\n")
            lines.append(form.description)
            lines.append("")

        # Form Fields
        if form.fields:
            lines.append("## Fields\n")
            headers = ["Name", "Type", "Label", "Required", "Validation"]
            rows = []
            for field in form.fields:
                validation = field.validation_pattern or "-"
                rows.append([
                    field.name,
                    field.type,
                    field.label or "-",
                    "Yes" if field.required else "No",
                    validation
                ])

            lines.append(MarkdownBuilder.format_table(headers, rows))
            lines.append("")

        # Submission
        lines.append("## Submission\n")
        if form.submission_endpoint:
            lines.append(f"- **Endpoint**: `{form.submission_method} {form.submission_endpoint}`")
        if form.submission_service:
            lines.append(f"- **Service**: `{form.submission_service}`")
        lines.append("")

        # Navigation
        if form.navigation_on_success or form.navigation_on_cancel:
            lines.append("## Navigation\n")
            if form.navigation_on_success:
                lines.append(f"- **On Success**: {form.navigation_on_success}")
            if form.navigation_on_cancel:
                lines.append(f"- **On Cancel**: {form.navigation_on_cancel}")
            lines.append("")

        # Validation Rules
        if form.validation_rules:
            lines.append("## Validation Rules\n")
            for rule in form.validation_rules:
                lines.append(f"- **{rule.field}**: {rule.rule_type} - {rule.message}")
            lines.append("")

        # Bound Entities
        if form.bound_entities:
            lines.append("## Bound Entities\n")
            for entity in form.bound_entities:
                lines.append(f"- {entity}")
            lines.append("")

        # Security Patterns
        if form.security_patterns:
            lines.append("## Security\n")
            for pattern in form.security_patterns:
                lines.append(MarkdownBuilder.format_security_admonition(
                    pattern.pattern_type,
                    pattern.description,
                    pattern.source_location,
                    pattern.recommendation
                ))
            lines.append("")

        # Source File
        lines.append("## Source File\n")
        lines.append(f"- `{form.source_file}`")
        lines.append("")

        # Metadata
        lines.append("---\n")
        lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

        return "\n".join(lines)

    @staticmethod
    def build_index_markdown(
        entities: List[Any],
        layer: AnalysisLayer,
        project: Optional[str] = None
    ) -> str:
        """
        Build index markdown for a layer.

        Args:
            entities: List of entities (DatabaseEntity, ServiceDefinition, FormDefinition, etc.)
            layer: Analysis layer
            project: Optional project name

        Returns:
            Markdown string
        """
        lines = []

        # Header
        layer_name = layer.value.title()
        title = f"{layer_name} Layer Documentation"
        if project:
            title += f" - {project}"

        lines.append(f"# {title}\n")
        lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")

        # Summary
        lines.append("## Summary\n")
        lines.append(f"- **Total Entities**: {len(entities)}")

        # Group by domain
        by_domain: Dict[str, List[Any]] = {}
        for entity in entities:
            domain = getattr(entity, 'domain', None) or 'Uncategorized'
            if domain not in by_domain:
                by_domain[domain] = []
            by_domain[domain].append(entity)

        lines.append(f"- **Domains**: {len(by_domain)}")
        lines.append("")

        # List by domain
        for domain in sorted(by_domain.keys()):
            domain_entities = by_domain[domain]
            lines.append(f"## {domain}\n")
            lines.append(f"*{len(domain_entities)} entities*\n")

            for entity in sorted(domain_entities, key=lambda e: getattr(e, 'name', str(e))):
                entity_name = getattr(entity, 'name', str(entity))
                entity_desc = getattr(entity, 'description', None)

                # Determine link path based on layer
                if layer == AnalysisLayer.DATABASE:
                    link = f"entities/{entity.id}.json"
                elif layer == AnalysisLayer.SERVICE:
                    link = f"definitions/{entity.class_name}.json"
                elif layer == AnalysisLayer.FRONTEND:
                    link = f"forms/{entity.name}.json"
                else:
                    link = f"{entity_name}.json"

                lines.append(f"- [{entity_name}]({link})")
                if entity_desc:
                    desc_preview = entity_desc.split('\n')[0][:100]
                    if len(entity_desc) > 100:
                        desc_preview += "..."
                    lines.append(f"  - {desc_preview}")

            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def build_prd_section(section: PRDSection) -> str:
        """
        Build markdown for a PRD section.

        Args:
            section: PRDSection to render

        Returns:
            Markdown string
        """
        lines = []

        # Header (level based on section.level)
        header_prefix = "#" * section.level
        lines.append(f"{header_prefix} {section.title}\n")

        # Content
        lines.append(section.content)
        lines.append("")

        # Cross-references
        if section.cross_references:
            lines.append("### Related Items\n")
            for ref in section.cross_references:
                lines.append(f"- [{ref.target_name}]({ref.target_path})")
                if ref.relationship:
                    lines.append(f"  - *{ref.relationship}*")
            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def format_table(headers: List[str], rows: List[List[str]]) -> str:
        """
        Format a markdown table.

        Args:
            headers: Table header row
            rows: Table data rows

        Returns:
            Markdown table string
        """
        if not headers or not rows:
            return ""

        lines = []

        # Calculate column widths
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))

        # Header row
        header_cells = [headers[i].ljust(col_widths[i]) for i in range(len(headers))]
        lines.append("| " + " | ".join(header_cells) + " |")

        # Separator row
        sep_cells = ["-" * col_widths[i] for i in range(len(headers))]
        lines.append("| " + " | ".join(sep_cells) + " |")

        # Data rows
        for row in rows:
            data_cells = [str(row[i]).ljust(col_widths[i]) for i in range(len(row))]
            lines.append("| " + " | ".join(data_cells) + " |")

        return "\n".join(lines)

    @staticmethod
    def format_list(items: List[str]) -> str:
        """
        Format a markdown list.

        Args:
            items: List items

        Returns:
            Markdown list string
        """
        return "\n".join([f"- {item}" for item in items])

    @staticmethod
    def format_code_block(code: str, language: str = "") -> str:
        """
        Format a markdown code block.

        Args:
            code: Code content
            language: Code language for syntax highlighting

        Returns:
            Markdown code block string
        """
        return f"```{language}\n{code}\n```"

    @staticmethod
    def format_security_admonition(
        pattern: str,
        description: str,
        source: str,
        recommendation: str
    ) -> str:
        """
        Format a security pattern admonition.

        Args:
            pattern: Security pattern type
            description: Pattern description
            source: Source location
            recommendation: Recommended action

        Returns:
            Markdown admonition string
        """
        lines = []
        lines.append(f"> **Security**: {pattern}")
        lines.append(f"> ")
        lines.append(f"> {description}")
        lines.append(f"> ")
        lines.append(f"> **Source**: `{source}`")
        lines.append(f"> ")
        lines.append(f"> **Recommendation**: {recommendation}")
        return "\n".join(lines)


# Convenience functions

def build_entity_markdown(entity: DatabaseEntity) -> str:
    """Build markdown for database entity."""
    return MarkdownBuilder.build_entity_markdown(entity)


def build_service_markdown(service: ServiceDefinition) -> str:
    """Build markdown for service definition."""
    return MarkdownBuilder.build_service_markdown(service)


def build_form_markdown(form: FormDefinition) -> str:
    """Build markdown for form definition."""
    return MarkdownBuilder.build_form_markdown(form)


def build_index_markdown(
    entities: List[Any],
    layer: AnalysisLayer,
    project: Optional[str] = None
) -> str:
    """Build index markdown for a layer."""
    return MarkdownBuilder.build_index_markdown(entities, layer, project)


def build_prd_section(section: PRDSection) -> str:
    """Build markdown for PRD section."""
    return MarkdownBuilder.build_prd_section(section)
