"""
PRD markdown generation with frontend + backend fusion.
"""
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import requests
from datetime import datetime

from config.settings import settings
from synth.prompts import PromptTemplates

logger = logging.getLogger(__name__)

class PRDMarkdownGenerator:
    """Generates PRD markdown documents."""
    
    def __init__(self):
        """Initialize PRD generator."""
        self.output_dir = settings.output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Ollama API endpoint (prefer 127.0.0.1 on host to avoid IPv6 issues)
        base_url = settings.ollama_base_url
        if 'host.docker.internal' in base_url:
            base_url = 'http://127.0.0.1:11434'
        self._ollama_base = base_url
        self.ollama_generate_url = f"{base_url}/api/generate"
    
    def generate_prd(self, artifacts: Dict[str, List[Dict[str, Any]]], project_name: str) -> str:
        """Generate complete PRD markdown document."""
        logger.info(f"Generating PRD for project: {project_name}")
        
        # Generate different sections
        logger.info("Generating section: overview")
        overview = self._generate_overview_section(artifacts, project_name)
        logger.info("OK: section overview generated")

        logger.info("Generating section: features")
        features = self._generate_features_section(artifacts)
        logger.info("OK: section features generated")

        logger.info("Generating section: technical")
        technical = self._generate_technical_section(artifacts)
        logger.info("OK: section technical generated")

        logger.info("Generating section: frontend")
        frontend = self._generate_frontend_section(artifacts)
        logger.info("OK: section frontend generated")

        logger.info("Generating section: flows")
        flows = self._generate_flows_section(artifacts)
        logger.info("OK: section flows generated")

        logger.info("Generating section: requirements")
        requirements = self._generate_requirements_section(artifacts)
        logger.info("OK: section requirements generated")

        logger.info("Generating section: traceability")
        traceability = self._generate_traceability_section(artifacts)
        logger.info("OK: section traceability generated")
        
        # Combine all sections
        prd_content = self._combine_prd_sections(
            project_name, overview, features, technical, frontend, 
            flows, requirements, traceability
        )
        
        # Save PRD
        prd_file = self.output_dir / f"{project_name}_prd.md"
        with open(prd_file, 'w', encoding='utf-8') as f:
            f.write(prd_content)
        
        logger.info(f"Generated PRD: {prd_file}")
        return str(prd_file)
    
    def _generate_overview_section(self, artifacts: Dict[str, List[Dict[str, Any]]], project_name: str) -> str:
        """Generate product overview section."""
        # Collect all artifacts for context
        all_artifacts = []
        for artifact_list in artifacts.values():
            all_artifacts.extend(artifact_list)
        
        prompt = PromptTemplates.prd_section_prompt("overview", all_artifacts)
        generated_content = self._call_ollama(prompt)
        
        return f"""## 1. Product Overview

{generated_content}

### Project Information
- **Project Name**: {project_name}
- **Generated Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Artifacts Analyzed**: {len(all_artifacts)} total artifacts
- **Artifact Types**: {', '.join(artifacts.keys())}"""
    
    def _generate_features_section(self, artifacts: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate features section."""
        # Collect all artifacts for context
        all_artifacts = []
        for artifact_list in artifacts.values():
            all_artifacts.extend(artifact_list)
        
        prompt = PromptTemplates.prd_section_prompt("features", all_artifacts)
        generated_content = self._call_ollama(prompt)
        
        return f"""## 2. Features

{generated_content}

### Feature Summary
{self._generate_feature_summary(artifacts)}"""
    
    def _generate_technical_section(self, artifacts: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate technical architecture section."""
        # Collect all artifacts for context
        all_artifacts = []
        for artifact_list in artifacts.values():
            all_artifacts.extend(artifact_list)
        
        prompt = PromptTemplates.prd_section_prompt("technical", all_artifacts)
        generated_content = self._call_ollama(prompt)
        
        return f"""## 3. Technical Architecture

{generated_content}

### Technology Stack
{self._generate_technology_stack(artifacts)}

### Integration Points
{self._generate_integration_points(artifacts)}"""
    
    def _generate_frontend_section(self, artifacts: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate frontend section."""
        # Collect frontend artifacts
        frontend_artifacts = []
        frontend_types = ['gwt_modules', 'gwt_activities_places', 'gwt_uibinder', 'gwt_endpoints', 'js_artifacts', 'jsp_forms']
        
        for artifact_type in frontend_types:
            if artifact_type in artifacts:
                frontend_artifacts.extend(artifacts[artifact_type])
        
        if not frontend_artifacts:
            return "## 4. Frontend\n\nNo frontend artifacts found."
        
        prompt = PromptTemplates.prd_section_prompt("frontend", frontend_artifacts)
        generated_content = self._call_ollama(prompt)
        
        return f"""## 4. Frontend

{generated_content}

### Frontend Components
{self._generate_frontend_components(artifacts)}

### Navigation Flows
{self._generate_navigation_flows(artifacts)}"""
    
    def _generate_flows_section(self, artifacts: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate user flows section."""
        # Collect all artifacts for context
        all_artifacts = []
        for artifact_list in artifacts.values():
            all_artifacts.extend(artifact_list)
        
        prompt = PromptTemplates.flow_synthesis_prompt(all_artifacts)
        flows_json = self._call_ollama_json(prompt)
        
        if flows_json and 'flows' in flows_json:
            flows_content = self._format_flows_json(flows_json['flows'])
        else:
            flows_content = self._generate_flows_fallback(artifacts)
        
        return f"""## 5. User Flows

{flows_content}"""
    
    def _generate_requirements_section(self, artifacts: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate requirements section."""
        # Collect all artifacts for context
        all_artifacts = []
        for artifact_list in artifacts.values():
            all_artifacts.extend(artifact_list)
        
        prompt = PromptTemplates.requirement_synthesis_prompt(all_artifacts)
        requirements_json = self._call_ollama_json(prompt)
        
        if requirements_json:
            return self._format_requirements_json(requirements_json)
        else:
            return self._generate_requirements_fallback(artifacts)
    
    def _generate_traceability_section(self, artifacts: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate traceability section."""
        # Collect all artifacts for context
        all_artifacts = []
        for artifact_list in artifacts.values():
            all_artifacts.extend(artifact_list)
        
        prompt = PromptTemplates.traceability_prompt(all_artifacts)
        traceability_json = self._call_ollama_json(prompt)
        
        if traceability_json:
            return self._format_traceability_json(traceability_json)
        else:
            return self._generate_traceability_fallback(artifacts)
    
    def _generate_feature_summary(self, artifacts: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate feature summary from artifacts."""
        summary = []
        
        # Count different artifact types
        for artifact_type, artifact_list in artifacts.items():
            count = len(artifact_list)
            if count > 0:
                summary.append(f"- **{artifact_type.replace('_', ' ').title()}**: {count} artifacts")
        
        return "\n".join(summary)
    
    def _generate_technology_stack(self, artifacts: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate technology stack from artifacts."""
        technologies = []
        
        if 'gwt_modules' in artifacts and artifacts['gwt_modules']:
            technologies.append("- **GWT (Google Web Toolkit)**: Frontend framework")
        
        if 'js_artifacts' in artifacts and artifacts['js_artifacts']:
            technologies.append("- **JavaScript**: Client-side scripting")
        
        if 'jsp_forms' in artifacts and artifacts['jsp_forms']:
            technologies.append("- **JSP (JavaServer Pages)**: Server-side rendering")
        
        if 'ibatis_statements' in artifacts and artifacts['ibatis_statements']:
            technologies.append("- **iBATIS**: Data access framework")
        
        if 'db_tables' in artifacts and artifacts['db_tables']:
            technologies.append("- **Database**: SQL database")
        
        if 'dao_calls' in artifacts and artifacts['dao_calls']:
            technologies.append("- **DAO Pattern**: Data access objects")
        
        return "\n".join(technologies) if technologies else "No specific technologies identified."
    
    def _generate_integration_points(self, artifacts: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate integration points from artifacts."""
        integration_points = []
        
        # GWT RPC endpoints
        if 'gwt_endpoints' in artifacts:
            for endpoint in artifacts['gwt_endpoints']:
                if endpoint.get('style') == 'RPC':
                    integration_points.append(f"- **GWT RPC**: {endpoint.get('serviceInterface', 'Unknown')} @ {endpoint.get('endpointPath', 'Unknown')}")
        
        # JavaScript XHR calls
        if 'js_artifacts' in artifacts:
            for js_artifact in artifacts['js_artifacts']:
                try:
                    xhr_json = js_artifact.get('xhrJson', '[]')
                    xhr_calls = json.loads(xhr_json) if isinstance(xhr_json, str) else xhr_json
                    for xhr_call in xhr_calls[:3]:  # Limit to first 3
                        integration_points.append(f"- **XHR**: {xhr_call.get('method', 'GET')} {xhr_call.get('url', 'Unknown')}")
                except:
                    pass
        
        return "\n".join(integration_points) if integration_points else "No integration points identified."
    
    def _generate_frontend_components(self, artifacts: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate frontend components summary."""
        components = []
        
        # GWT UiBinder components
        if 'gwt_uibinder' in artifacts:
            for uibinder in artifacts['gwt_uibinder']:
                owner_type = uibinder.get('ownerType', 'Unknown')
                components.append(f"- **UiBinder**: {owner_type}")
        
        # JSP forms
        if 'jsp_forms' in artifacts:
            for form in artifacts['jsp_forms']:
                form_action = form.get('formAction', 'Unknown')
                components.append(f"- **JSP Form**: {form_action}")
        
        # JavaScript artifacts
        if 'js_artifacts' in artifacts:
            for js_artifact in artifacts['js_artifacts']:
                script_path = js_artifact.get('scriptPath', 'Unknown')
                components.append(f"- **JavaScript**: {Path(script_path).name}")
        
        return "\n".join(components) if components else "No frontend components identified."
    
    def _generate_navigation_flows(self, artifacts: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate navigation flows summary."""
        flows = []
        
        # GWT Activities/Places
        if 'gwt_activities_places' in artifacts:
            for activity_place in artifacts['gwt_activities_places']:
                place_class = activity_place.get('placeClass', 'Unknown')
                activity_class = activity_place.get('activityClass', 'Unknown')
                if activity_class and activity_class != 'Unknown':
                    flows.append(f"- **GWT Flow**: {place_class} ↔ {activity_class}")
                else:
                    flows.append(f"- **GWT Place**: {place_class}")
        
        # JavaScript routes
        if 'js_artifacts' in artifacts:
            for js_artifact in artifacts['js_artifacts']:
                try:
                    routes_json = js_artifact.get('routesJson', '[]')
                    routes = json.loads(routes_json) if isinstance(routes_json, str) else routes_json
                    for route in routes[:3]:  # Limit to first 3
                        flows.append(f"- **JS Route**: {route.get('pattern', 'Unknown')}")
                except:
                    pass
        
        return "\n".join(flows) if flows else "No navigation flows identified."
    
    def _format_flows_json(self, flows: List[Dict[str, Any]]) -> str:
        """Format flows JSON into markdown."""
        if not flows:
            return "No flows identified."
        
        content = []
        for i, flow in enumerate(flows, 1):
            content.append(f"### Flow {i}: {flow.get('title', 'Untitled Flow')}")
            content.append(f"**Summary**: {flow.get('summary', 'No summary available')}")
            
            if 'actors' in flow:
                content.append(f"**Actors**: {', '.join(flow['actors'])}")
            
            if 'steps' in flow:
                content.append("**Steps**:")
                for step in flow['steps']:
                    content.append(f"1. {step}")
            
            if 'entryPoints' in flow:
                content.append("**Entry Points**:")
                for entry_point in flow['entryPoints']:
                    content.append(f"- {entry_point.get('kind', 'Unknown')}: {entry_point.get('value', 'Unknown')}")
            
            content.append("")  # Empty line between flows
        
        return "\n".join(content)
    
    def _format_requirements_json(self, requirements: Dict[str, Any]) -> str:
        """Format requirements JSON into markdown."""
        content = []
        
        # Functional Requirements
        if 'functionalRequirements' in requirements:
            content.append("### Functional Requirements")
            for req in requirements['functionalRequirements']:
                content.append(f"#### {req.get('id', 'Unknown')}: {req.get('title', 'Untitled')}")
                content.append(f"**Description**: {req.get('description', 'No description')}")
                
                if 'acceptanceCriteria' in req:
                    content.append("**Acceptance Criteria**:")
                    for ac in req['acceptanceCriteria']:
                        content.append(f"- {ac}")
                
                content.append(f"**Priority**: {req.get('priority', 'Medium')}")
                content.append("")  # Empty line
        
        # Non-Functional Requirements
        if 'nonFunctionalRequirements' in requirements:
            content.append("### Non-Functional Requirements")
            for req in requirements['nonFunctionalRequirements']:
                content.append(f"#### {req.get('id', 'Unknown')}: {req.get('title', 'Untitled')}")
                content.append(f"**Description**: {req.get('description', 'No description')}")
                content.append(f"**Category**: {req.get('category', 'Unknown')}")
                content.append(f"**Priority**: {req.get('priority', 'Medium')}")
                content.append("")  # Empty line
        
        return "\n".join(content)
    
    def _format_traceability_json(self, traceability: Dict[str, Any]) -> str:
        """Format traceability JSON into markdown."""
        content = []
        
        if 'uiToApi' in traceability:
            content.append("### UI to API Mapping")
            for mapping in traceability['uiToApi']:
                content.append(f"- **{mapping.get('uiComponent', 'Unknown')}** → **{mapping.get('apiEndpoint', 'Unknown')}** ({mapping.get('method', 'Unknown')})")
            content.append("")
        
        if 'apiToDb' in traceability:
            content.append("### API to Database Mapping")
            for mapping in traceability['apiToDb']:
                content.append(f"- **{mapping.get('apiMethod', 'Unknown')}** → **{mapping.get('dbStatement', 'Unknown')}** (table: {mapping.get('table', 'Unknown')})")
            content.append("")
        
        if 'flows' in traceability:
            content.append("### End-to-End Flows")
            for flow in traceability['flows']:
                content.append(f"- **{flow.get('name', 'Unknown Flow')}**: {flow.get('path', 'Unknown path')}")
                if 'components' in flow:
                    content.append(f"  - Components: {', '.join(flow['components'])}")
            content.append("")
        
        return "\n".join(content)
    
    def _generate_flows_fallback(self, artifacts: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate flows fallback when LLM fails."""
        return "### Identified Flows\n\nFlow analysis requires LLM processing. Please check the artifacts for flow patterns."
    
    def _generate_requirements_fallback(self, artifacts: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate requirements fallback when LLM fails."""
        return "### Requirements\n\nRequirements analysis requires LLM processing. Please review the artifacts for requirement patterns."
    
    def _generate_traceability_fallback(self, artifacts: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate traceability fallback when LLM fails."""
        return "### Traceability\n\nTraceability analysis requires LLM processing. Please review the artifacts for traceability patterns."
    
    def _combine_prd_sections(self, project_name: str, overview: str, features: str, 
                             technical: str, frontend: str, flows: str, 
                             requirements: str, traceability: str) -> str:
        """Combine all PRD sections into final document."""
        return f"""# Product Requirements Document (PRD)
## {project_name}

{overview}

{features}

{technical}

{frontend}

{flows}

{requirements}

{traceability}

---

*This PRD was automatically generated from codebase analysis on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API for text generation."""
        payload = {
            "model": settings.ollama_model_name,
            "prompt": prompt,
            "stream": False
        }
        timeouts = [60, 90, 120]
        for attempt, to in enumerate(timeouts, 1):
            try:
                # quick health check
                try:
                    health = requests.get(f"{self._ollama_base}/api/tags", timeout=5)
                    if health.status_code == 200:
                        logger.info("OK: Ollama health check passed")
                    else:
                        logger.warning("Ollama health check non-200: %s", health.status_code)
                except Exception:
                    logger.warning("Ollama health check failed (attempt %s)", attempt)

                response = requests.post(
                    self.ollama_generate_url,
                    json=payload,
                    timeout=to
                )
                if response.status_code == 200:
                    result = response.json()
                    logger.info("OK: Ollama call succeeded (attempt %s, timeout %ss)", attempt, to)
                    return result.get('response', 'No response generated')
                else:
                    logger.warning("Ollama API error %s: %s", response.status_code, response.text)
            except Exception as e:
                logger.warning("Ollama call attempt %s failed: %s", attempt, e)
            # backoff
            import time as _t
            _t.sleep(2 * attempt)
        logger.error("Failed to call Ollama after retries")
        return "Error generating content"
    
    def _call_ollama_json(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Call Ollama API and parse JSON response more robustly."""
        try:
            response_text = self._call_ollama(prompt)
            if not response_text:
                return None
            # Prefer fenced JSON blocks
            try:
                import re as _re
                fence = _re.search(r"```json\s*(\{[\s\S]*?\})\s*```", response_text, _re.IGNORECASE)
                if fence:
                    return json.loads(fence.group(1))
            except Exception:
                pass
            # Fallback: first to last brace slice
            if '{' in response_text and '}' in response_text:
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                json_str = response_text[start:end]
                try:
                    return json.loads(json_str)
                except Exception:
                    pass
            return None
        except Exception as e:
            logger.error(f"Failed to parse JSON from Ollama response: {e}")
            return None
    
    def generate_backend_requirements(self, project_name: str, backend_artifacts: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate structured backend services requirements document."""
        logger.info(f"Generating backend requirements for project: {project_name}")
        
        # Generate backend-specific sections
        overview = self._generate_backend_overview(backend_artifacts, project_name)
        services = self._generate_backend_services(backend_artifacts)
        data_flow = self._generate_data_flow(backend_artifacts)
        endpoints = self._generate_api_endpoints(backend_artifacts)
        
        return f"""# Backend Services Requirements Document
## {project_name}

{overview}

{services}

{data_flow}

{endpoints}

---
*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    def generate_frontend_requirements(self, project_name: str, frontend_artifacts: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate structured frontend requirements document."""
        logger.info(f"Generating frontend requirements for project: {project_name}")
        
        # Generate frontend-specific sections
        overview = self._generate_frontend_overview(frontend_artifacts, project_name)
        components = self._generate_frontend_components_detailed(frontend_artifacts)
        navigation = self._generate_navigation_structure(frontend_artifacts)
        
        return f"""# Frontend Requirements Document
## {project_name}

{overview}

{components}

{navigation}

---
*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    def generate_consolidated_requirements(self, project_name: str, backend_content: str, frontend_content: str) -> str:
        """Generate consolidated requirements document combining backend and frontend."""
        logger.info(f"Generating consolidated requirements for project: {project_name}")
        
        return f"""# Comprehensive Requirements Document
## {project_name}

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Backend Requirements

{backend_content}

---

## Frontend Requirements

{frontend_content}

---

*This document consolidates both backend and frontend requirements for the {project_name} project.*
"""
    
    def _generate_backend_overview(self, backend_artifacts: Dict[str, List[Dict[str, Any]]], project_name: str) -> str:
        """Generate backend overview section."""
        artifact_counts = {k: len(v) for k, v in backend_artifacts.items() if v}
        total_count = sum(artifact_counts.values())
        
        return f"""## 1. Backend Overview

This document describes the backend services and data layer requirements for {project_name}.

### Artifact Summary
{chr(10).join([f"- **{k.replace('_', ' ').title()}**: {v} artifacts" for k, v in artifact_counts.items()])}

**Total Backend Artifacts**: {total_count}

### Key Components
- DAO (Data Access Object) layer for database operations
- Service layer for business logic
- RESTful API endpoints for frontend communication
- Database schema and data modeling
"""
    
    def _generate_backend_services(self, backend_artifacts: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate backend services section."""
        services = []
        
        # DAO calls
        if 'dao_calls' in backend_artifacts:
            services.append("### DAO Services")
            for dao in backend_artifacts['dao_calls'][:10]:  # Limit to first 10
                method_name = dao.get('methodName', 'Unknown')
                owner_type = dao.get('ownerType', 'Unknown')
                services.append(f"- **{method_name}** ({owner_type})")
            services.append("")
        
        # JSP forms (backend handling)
        if 'jsp_forms' in backend_artifacts:
            services.append("### Form Handlers")
            for form in backend_artifacts['jsp_forms'][:10]:
                form_action = form.get('formAction', 'Unknown')
                form_method = form.get('formMethod', 'POST')
                services.append(f"- **{form_action}** ({form_method})")
            services.append("")
        
        return "\n".join(services) if services else "### Backend Services\n\nNo specific services identified."
    
    def _generate_data_flow(self, backend_artifacts: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate data flow section."""
        flows = []
        
        if 'ibatis_statements' in backend_artifacts:
            flows.append("### SQL Data Operations")
            for stmt in backend_artifacts['ibatis_statements'][:5]:  # Limit to 5
                stmt_id = stmt.get('statementId', 'Unknown')
                operation = stmt.get('operation', 'Unknown')
                flows.append(f"- **{stmt_id}**: {operation}")
            flows.append("")
        
        if 'db_tables' in backend_artifacts:
            flows.append("### Database Tables")
            for table in backend_artifacts['db_tables'][:10]:
                table_name = table.get('tableName', 'Unknown')
                flows.append(f"- **{table_name}**")
        
        return "\n".join(flows) if flows else "### Data Flow\n\nNo data flow information available."
    
    def _generate_api_endpoints(self, backend_artifacts: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate API endpoints section."""
        endpoints = []
        
        if 'jsp_forms' in backend_artifacts:
            endpoints.append("### Form Submission Endpoints")
            for form in backend_artifacts['jsp_forms']:
                action = form.get('formAction', 'Unknown')
                method = form.get('formMethod', 'POST')
                endpoints.append(f"- **{method} {action}**")
                fields = form.get('fields', [])
                if fields:
                    endpoints.append(f"  - Fields: {len(fields)}")
        
        return "\n".join(endpoints) if endpoints else "### API Endpoints\n\nNo endpoints identified."
    
    def _generate_frontend_overview(self, frontend_artifacts: Dict[str, List[Dict[str, Any]]], project_name: str) -> str:
        """Generate frontend overview section."""
        artifact_counts = {k: len(v) for k, v in frontend_artifacts.items() if v}
        total_count = sum(artifact_counts.values())
        
        return f"""## 1. Frontend Overview

This document describes the frontend components and user interface requirements for {project_name}.

### Artifact Summary
{chr(10).join([f"- **{k.replace('_', ' ').title()}**: {v} artifacts" for k, v in artifact_counts.items()])}

**Total Frontend Artifacts**: {total_count}

### Key Technologies
- GWT (Google Web Toolkit) for rich client applications
- JavaScript for interactive features
- UiBinder for declarative UI definitions
"""
    
    def _generate_frontend_components_detailed(self, frontend_artifacts: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate detailed frontend components section."""
        components = []
        
        if 'gwt_uibinder' in frontend_artifacts:
            components.append("### GWT UiBinder Components")
            for uibinder in frontend_artifacts['gwt_uibinder'][:20]:
                owner_type = uibinder.get('ownerType', 'Unknown')
                file_path = uibinder.get('path', 'Unknown')
                components.append(f"- **{owner_type}** ({Path(file_path).name})")
            components.append("")
        
        if 'gwt_modules' in frontend_artifacts:
            components.append("### GWT Modules")
            for module in frontend_artifacts['gwt_modules'][:10]:
                module_name = module.get('moduleName', 'Unknown')
                components.append(f"- **{module_name}**")
            components.append("")
        
        return "\n".join(components) if components else "### Frontend Components\n\nNo components identified."
    
    def _generate_navigation_structure(self, frontend_artifacts: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate navigation structure section."""
        navigation = []
        
        if 'gwt_client' in frontend_artifacts:
            navigation.append("### GWT Place/Activity Navigation")
            gwt_client_data = frontend_artifacts['gwt_client']
            # Handle dict structure (from all_artifacts.json)
            if isinstance(gwt_client_data, dict):
                # If it's a dict, check for activities_places key
                if 'activities_places' in gwt_client_data and isinstance(gwt_client_data['activities_places'], list):
                    for client in gwt_client_data['activities_places'][:15]:
                        place = client.get('placeClass', 'Unknown')
                        activity = client.get('activityClass', 'Unknown')
                        navigation.append(f"- **Place**: {place} → **Activity**: {activity}")
                else:
                    navigation.append("No GWT client navigation data available")
            # Handle list structure
            elif isinstance(gwt_client_data, list):
                for client in gwt_client_data[:15]:
                    place = client.get('placeClass', 'Unknown')
                    activity = client.get('activityClass', 'Unknown')
                    navigation.append(f"- **Place**: {place} → **Activity**: {activity}")
            navigation.append("")
        
        return "\n".join(navigation) if navigation else "### Navigation Structure\n\nNo navigation patterns identified."