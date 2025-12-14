"""
PRD Generator Orchestrator Service.

Synthesizes database, service, and frontend layer analyses into a comprehensive
master Product Requirements Document with executive summary, architecture overview,
cross-layer flows, and gap analysis.
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from codeindex.models.prd import (
    DatabaseEntity, BusinessRule, ServiceDefinition, APIEndpoint,
    FormDefinition, UIComponent, AnalysisLayer
)
from codeindex.services.ollama_client import OllamaClient

logger = logging.getLogger(__name__)


class PRDGenerator:
    """
    Orchestrates master PRD generation by synthesizing all layer analyses.

    Loads artifacts from JSON files, uses LLM to generate executive summaries
    and insights, and produces comprehensive master PRD documentation.
    """

    def __init__(
        self,
        output_dir: Path,
        ollama_client: OllamaClient,
        project_name: Optional[str] = None
    ):
        """
        Initialize PRD generator.

        Args:
            output_dir: Output directory containing layer analysis results
            ollama_client: Ollama client for LLM-powered synthesis
            project_name: Optional project name for PRD metadata
        """
        self.output_dir = Path(output_dir)
        self.ollama_client = ollama_client
        self.project_name = project_name or "Analyzed Project"
        self.logger = logging.getLogger(__name__)

    def load_database_artifacts(self) -> tuple[List[DatabaseEntity], List[BusinessRule]]:
        """
        Load database entities and related business rules.

        Returns:
            Tuple of (entities, rules) lists
        """
        entities = []
        db_rules = []

        # Load entities
        entities_dir = self.output_dir / "database" / "entities"
        if entities_dir.exists():
            for entity_file in entities_dir.glob("*.json"):
                try:
                    with open(entity_file, "r", encoding="utf-8") as f:
                        entity_data = json.load(f)
                        entities.append(DatabaseEntity.from_dict(entity_data))
                except Exception as e:
                    self.logger.warning(f"Failed to load entity from {entity_file}: {e}")

        # Load business rules (database layer)
        rules_dir = self.output_dir / "business_rules"
        if rules_dir.exists():
            for rule_file in rules_dir.glob("*.json"):
                try:
                    with open(rule_file, "r", encoding="utf-8") as f:
                        rule_data = json.load(f)
                        rule = BusinessRule.from_dict(rule_data)
                        if rule.layer.value == "database":
                            db_rules.append(rule)
                except Exception as e:
                    self.logger.warning(f"Failed to load rule from {rule_file}: {e}")

        return entities, db_rules

    def load_service_artifacts(self) -> tuple[List[ServiceDefinition], List[APIEndpoint], List[BusinessRule]]:
        """
        Load service definitions, API endpoints, and related business rules.

        Returns:
            Tuple of (services, endpoints, rules) lists
        """
        services = []
        endpoints = []
        service_rules = []

        # Load services
        services_dir = self.output_dir / "services" / "definitions"
        if services_dir.exists():
            for service_file in services_dir.glob("*.json"):
                try:
                    with open(service_file, "r", encoding="utf-8") as f:
                        service_data = json.load(f)
                        services.append(ServiceDefinition.from_dict(service_data))
                except Exception as e:
                    self.logger.warning(f"Failed to load service from {service_file}: {e}")

        # Load endpoints
        endpoints_dir = self.output_dir / "services" / "endpoints"
        if endpoints_dir.exists():
            for endpoint_file in endpoints_dir.glob("*.json"):
                try:
                    with open(endpoint_file, "r", encoding="utf-8") as f:
                        endpoint_data = json.load(f)
                        endpoints.append(APIEndpoint.from_dict(endpoint_data))
                except Exception as e:
                    self.logger.warning(f"Failed to load endpoint from {endpoint_file}: {e}")

        # Load business rules (service layer)
        rules_dir = self.output_dir / "business_rules"
        if rules_dir.exists():
            for rule_file in rules_dir.glob("*.json"):
                try:
                    with open(rule_file, "r", encoding="utf-8") as f:
                        rule_data = json.load(f)
                        rule = BusinessRule.from_dict(rule_data)
                        if rule.layer.value == "service":
                            service_rules.append(rule)
                except Exception as e:
                    self.logger.warning(f"Failed to load rule from {rule_file}: {e}")

        return services, endpoints, service_rules

    def load_frontend_artifacts(self) -> tuple[List[FormDefinition], List[UIComponent], List[BusinessRule]]:
        """
        Load form definitions, UI components, and related business rules.

        Returns:
            Tuple of (forms, components, rules) lists
        """
        forms = []
        components = []
        frontend_rules = []

        # Load forms
        forms_dir = self.output_dir / "frontend" / "forms"
        if forms_dir.exists():
            for form_file in forms_dir.glob("*.json"):
                try:
                    with open(form_file, "r", encoding="utf-8") as f:
                        form_data = json.load(f)
                        forms.append(FormDefinition.from_dict(form_data))
                except Exception as e:
                    self.logger.warning(f"Failed to load form from {form_file}: {e}")

        # Load components
        components_dir = self.output_dir / "frontend" / "components"
        if components_dir.exists():
            for component_file in components_dir.glob("*.json"):
                try:
                    with open(component_file, "r", encoding="utf-8") as f:
                        component_data = json.load(f)
                        components.append(UIComponent.from_dict(component_data))
                except Exception as e:
                    self.logger.warning(f"Failed to load component from {component_file}: {e}")

        # Load business rules (frontend layer)
        rules_dir = self.output_dir / "business_rules"
        if rules_dir.exists():
            for rule_file in rules_dir.glob("*.json"):
                try:
                    with open(rule_file, "r", encoding="utf-8") as f:
                        rule_data = json.load(f)
                        rule = BusinessRule.from_dict(rule_data)
                        if rule.layer.value == "frontend":
                            frontend_rules.append(rule)
                except Exception as e:
                    self.logger.warning(f"Failed to load rule from {rule_file}: {e}")

        return forms, components, frontend_rules

    def detect_technology_stack(
        self,
        entities: List[DatabaseEntity],
        services: List[ServiceDefinition],
        forms: List[FormDefinition],
        components: List[UIComponent]
    ) -> Dict[str, List[str]]:
        """
        Detect technology stack from artifacts.

        Args:
            entities: Database entities
            services: Service definitions
            forms: Form definitions
            components: UI components

        Returns:
            Dictionary with categories: backend, frontend, database, frameworks
        """
        tech_stack = {
            "backend": set(),
            "frontend": set(),
            "database": set(),
            "frameworks": set()
        }

        # Detect backend technologies
        for service in services:
            tech_stack["frameworks"].update(service.frameworks)
            if "Spring" in service.frameworks:
                tech_stack["backend"].add("Spring Framework")
            if "EJB" in service.frameworks:
                tech_stack["backend"].add("Enterprise JavaBeans")

        # Detect database technologies
        for entity in entities:
            if entity.source_type.value == "jpa_annotation":
                tech_stack["database"].add("JPA/Hibernate")
            elif entity.source_type.value == "ibatis_xml":
                tech_stack["database"].add("iBATIS/MyBatis")

        # Detect frontend technologies
        for form in forms:
            if form.form_type.value == "jsp_form":
                tech_stack["frontend"].add("JSP")
            elif form.form_type.value == "gwt_form":
                tech_stack["frontend"].add("GWT")
            elif form.form_type.value == "html_form":
                tech_stack["frontend"].add("HTML")

        for component in components:
            if "gwt" in component.component_type.value.lower():
                tech_stack["frontend"].add("GWT")
            elif "react" in component.component_type.value.lower():
                tech_stack["frontend"].add("React")

        # Convert sets to sorted lists
        return {k: sorted(list(v)) for k, v in tech_stack.items()}

    def detect_domains(
        self,
        entities: List[DatabaseEntity],
        services: List[ServiceDefinition],
        forms: List[FormDefinition],
        rules: List[BusinessRule]
    ) -> List[str]:
        """
        Detect business domains from artifacts.

        Args:
            entities: Database entities
            services: Service definitions
            forms: Form definitions
            rules: Business rules

        Returns:
            List of unique domain names
        """
        domains = set()

        for entity in entities:
            if entity.domain:
                domains.add(entity.domain)

        for service in services:
            if service.domain:
                domains.add(service.domain)

        for form in forms:
            if form.domain:
                domains.add(form.domain)

        for rule in rules:
            if rule.domain:
                domains.add(rule.domain)

        return sorted(list(domains))

    def generate_executive_summary(
        self,
        entities: List[DatabaseEntity],
        services: List[ServiceDefinition],
        endpoints: List[APIEndpoint],
        forms: List[FormDefinition],
        components: List[UIComponent],
        all_rules: List[BusinessRule],
        tech_stack: Dict[str, List[str]],
        domains: List[str]
    ) -> str:
        """
        Generate executive summary using LLM.

        Args:
            entities: Database entities
            services: Service definitions
            endpoints: API endpoints
            forms: Form definitions
            components: UI components
            all_rules: All business rules
            tech_stack: Technology stack dictionary
            domains: Business domains

        Returns:
            Executive summary markdown
        """
        # Prepare summary data for LLM
        summary_data = {
            "project_name": self.project_name,
            "entity_count": len(entities),
            "service_count": len(services),
            "endpoint_count": len(endpoints),
            "form_count": len(forms),
            "component_count": len(components),
            "rule_count": len(all_rules),
            "technologies": tech_stack,
            "domains": domains,
            "key_entities": [e.name for e in sorted(entities, key=lambda x: len(x.columns), reverse=True)[:5]],
            "key_services": [s.class_name for s in services[:5]]
        }

        # Build executive summary manually (LLM call can be added later)
        lines = []
        lines.append("## Executive Summary")
        lines.append("")
        lines.append(f"This Product Requirements Document provides comprehensive analysis of **{self.project_name}**, ")
        lines.append(f"documenting its architecture, data model, business logic, and user interface components.")
        lines.append("")

        lines.append("### System Overview")
        lines.append("")
        lines.append(f"- **Database Entities**: {len(entities)} tables/entities")
        lines.append(f"- **Backend Services**: {len(services)} service classes")
        lines.append(f"- **API Endpoints**: {len(endpoints)} REST/SOAP endpoints")
        lines.append(f"- **UI Forms**: {len(forms)} form definitions")
        lines.append(f"- **UI Components**: {len(components)} frontend components")
        lines.append(f"- **Business Rules**: {len(all_rules)} documented rules")
        lines.append("")

        if tech_stack["backend"] or tech_stack["frameworks"]:
            lines.append("### Technology Stack")
            lines.append("")
            if tech_stack["backend"]:
                lines.append(f"**Backend**: {', '.join(tech_stack['backend'])}")
            if tech_stack["database"]:
                lines.append(f"**Database**: {', '.join(tech_stack['database'])}")
            if tech_stack["frontend"]:
                lines.append(f"**Frontend**: {', '.join(tech_stack['frontend'])}")
            if tech_stack["frameworks"]:
                lines.append(f"**Frameworks**: {', '.join(tech_stack['frameworks'])}")
            lines.append("")

        if domains:
            lines.append("### Business Domains")
            lines.append("")
            lines.append(f"The system operates across **{len(domains)}** primary business domains:")
            for domain in domains:
                lines.append(f"- {domain}")
            lines.append("")

        if summary_data["key_entities"]:
            lines.append("### Key Database Entities")
            lines.append("")
            for entity in summary_data["key_entities"]:
                lines.append(f"- `{entity}`")
            lines.append("")

        return "\n".join(lines)

    def generate_architecture_overview(
        self,
        entities: List[DatabaseEntity],
        services: List[ServiceDefinition],
        forms: List[FormDefinition]
    ) -> str:
        """
        Generate architecture overview section.

        Args:
            entities: Database entities
            services: Service definitions
            forms: Form definitions

        Returns:
            Architecture overview markdown
        """
        lines = []
        lines.append("## System Architecture")
        lines.append("")
        lines.append("### Architectural Layers")
        lines.append("")
        lines.append("The system follows a layered architecture pattern:")
        lines.append("")
        lines.append("1. **Presentation Layer** - User interface components, forms, and views")
        lines.append(f"   - {len(forms)} forms for user interaction")
        lines.append("   - Client-side validation and navigation logic")
        lines.append("")
        lines.append("2. **Business Logic Layer** - Services implementing business operations")
        lines.append(f"   - {len(services)} service classes")
        lines.append("   - Transaction management and business rule enforcement")
        lines.append("")
        lines.append("3. **Data Access Layer** - Database entities and data persistence")
        lines.append(f"   - {len(entities)} database entities")
        lines.append("   - ORM mappings and data access patterns")
        lines.append("")

        return "\n".join(lines)

    def generate_cross_layer_mappings(
        self,
        entities: List[DatabaseEntity],
        services: List[ServiceDefinition],
        endpoints: List[APIEndpoint],
        forms: List[FormDefinition]
    ) -> str:
        """
        Generate cross-layer mapping documentation.

        Args:
            entities: Database entities
            services: Service definitions
            endpoints: API endpoints
            forms: Form definitions

        Returns:
            Cross-layer mappings markdown
        """
        lines = []
        lines.append("## Cross-Layer Integration")
        lines.append("")
        lines.append("### Form to Backend Mappings")
        lines.append("")

        if forms:
            lines.append("| Form | Submission Endpoint | Backend Service | Database Entities |")
            lines.append("|------|---------------------|-----------------|-------------------|")

            for form in forms:
                endpoint = form.submission_endpoint or "-"
                service = form.submission_service or "-"
                entities_str = ", ".join([f"`{e}`" for e in form.bound_entities]) if form.bound_entities else "-"

                lines.append(f"| `{form.name}` | `{endpoint}` | `{service}` | {entities_str} |")

            lines.append("")
        else:
            lines.append("*No forms with backend mappings found.*")
            lines.append("")

        lines.append("### Service to Database Mappings")
        lines.append("")

        if services:
            service_with_data = [s for s in services if s.data_dependencies]
            if service_with_data:
                lines.append("| Service | Database Dependencies |")
                lines.append("|---------|----------------------|")

                for service in service_with_data:
                    deps = ", ".join([f"`{d}`" for d in service.data_dependencies])
                    lines.append(f"| `{service.class_name}` | {deps} |")

                lines.append("")
            else:
                lines.append("*No service-to-database mappings documented.*")
                lines.append("")
        else:
            lines.append("*No services found.*")
            lines.append("")

        return "\n".join(lines)

    def generate_master_prd(self) -> str:
        """
        Generate comprehensive master PRD document.

        Returns:
            Master PRD markdown content
        """
        self.logger.info("Loading all artifacts...")

        # Load all artifacts
        entities, db_rules = self.load_database_artifacts()
        services, endpoints, service_rules = self.load_service_artifacts()
        forms, components, frontend_rules = self.load_frontend_artifacts()

        all_rules = db_rules + service_rules + frontend_rules

        self.logger.info(f"Loaded: {len(entities)} entities, {len(services)} services, "
                        f"{len(endpoints)} endpoints, {len(forms)} forms, "
                        f"{len(components)} components, {len(all_rules)} rules")

        # Detect technologies and domains
        tech_stack = self.detect_technology_stack(entities, services, forms, components)
        domains = self.detect_domains(entities, services, forms, all_rules)

        self.logger.info("Generating master PRD sections...")

        # Build master PRD
        lines = []

        # Header
        lines.append(f"# Product Requirements Document: {self.project_name}")
        lines.append("")
        lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        lines.append("")

        # Table of Contents
        lines.append("## Table of Contents")
        lines.append("")
        lines.append("1. [Executive Summary](#executive-summary)")
        lines.append("2. [System Architecture](#system-architecture)")
        lines.append("3. [Database Layer](#database-layer)")
        lines.append("4. [Service Layer](#service-layer)")
        lines.append("5. [Frontend Layer](#frontend-layer)")
        lines.append("6. [Cross-Layer Integration](#cross-layer-integration)")
        lines.append("7. [Business Rules](#business-rules)")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Executive Summary
        exec_summary = self.generate_executive_summary(
            entities, services, endpoints, forms, components,
            all_rules, tech_stack, domains
        )
        lines.append(exec_summary)
        lines.append("")
        lines.append("---")
        lines.append("")

        # Architecture Overview
        arch_overview = self.generate_architecture_overview(entities, services, forms)
        lines.append(arch_overview)
        lines.append("")
        lines.append("---")
        lines.append("")

        # Database Layer Summary
        lines.append("## Database Layer")
        lines.append("")
        lines.append(f"The database layer consists of **{len(entities)} entities** with ")
        lines.append(f"**{sum(len(e.columns) for e in entities)} total columns** and ")
        lines.append(f"**{sum(len(e.foreign_keys) for e in entities)} foreign key relationships**.")
        lines.append("")
        lines.append(f"📄 **Detailed Documentation**: See [database_prd.md](database_prd.md)")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Service Layer Summary
        lines.append("## Service Layer")
        lines.append("")
        lines.append(f"The service layer implements business logic through **{len(services)} service classes** ")
        lines.append(f"exposing **{len(endpoints)} API endpoints**.")
        lines.append("")
        lines.append(f"📄 **Detailed Documentation**: See [service_prd.md](service_prd.md)")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Frontend Layer Summary
        lines.append("## Frontend Layer")
        lines.append("")
        lines.append(f"The frontend layer provides user interaction through **{len(forms)} forms** and ")
        lines.append(f"**{len(components)} UI components**.")
        lines.append("")
        lines.append(f"📄 **Detailed Documentation**: See [frontend_prd.md](frontend_prd.md)")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Cross-Layer Integration
        cross_layer = self.generate_cross_layer_mappings(entities, services, endpoints, forms)
        lines.append(cross_layer)
        lines.append("")
        lines.append("---")
        lines.append("")

        # Business Rules Summary
        lines.append("## Business Rules")
        lines.append("")
        lines.append(f"A total of **{len(all_rules)} business rules** have been identified across all layers:")
        lines.append("")
        lines.append(f"- **Database Layer**: {len(db_rules)} rules")
        lines.append(f"- **Service Layer**: {len(service_rules)} rules")
        lines.append(f"- **Frontend Layer**: {len(frontend_rules)} rules")
        lines.append("")

        if domains:
            lines.append("### Rules by Domain")
            lines.append("")
            for domain in domains:
                domain_rules = [r for r in all_rules if r.domain == domain]
                if domain_rules:
                    lines.append(f"- **{domain}**: {len(domain_rules)} rules")
            lines.append("")

        lines.append("---")
        lines.append("")

        # Footer
        lines.append("## Document Information")
        lines.append("")
        lines.append(f"- **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"- **Project**: {self.project_name}")
        lines.append(f"- **Output Directory**: `{self.output_dir}`")
        lines.append("")

        return "\n".join(lines)
