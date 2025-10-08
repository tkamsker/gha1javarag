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
        
        # Ollama API endpoint (use localhost if host.docker.internal is set)
        base_url = settings.ollama_base_url
        if 'host.docker.internal' in base_url:
            base_url = 'http://127.0.0.1:11434'
        self.ollama_generate_url = f"{base_url}/api/generate"
    
    def generate_prd(self, artifacts: Dict[str, List[Dict[str, Any]]], project_name: str) -> str:
        """Generate complete PRD markdown document."""
        logger.info(f"Generating PRD for project: {project_name}")
        
        # Generate different sections
        overview = self._generate_overview_section(artifacts, project_name)
        features = self._generate_features_section(artifacts)
        technical = self._generate_technical_section(artifacts)
        frontend = self._generate_frontend_section(artifacts)
        flows = self._generate_flows_section(artifacts)
        requirements = self._generate_requirements_section(artifacts)
        traceability = self._generate_traceability_section(artifacts)
        
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
        try:
            payload = {
                "model": settings.ollama_model_name,
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(
                self.ollama_generate_url,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'No response generated')
            else:
                logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                return "Error generating content"
                
        except Exception as e:
            logger.error(f"Failed to call Ollama: {e}")
            return "Error generating content"
    
    def _call_ollama_json(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Call Ollama API and parse JSON response."""
        try:
            response_text = self._call_ollama(prompt)
            # Try to extract JSON from response
            if '{' in response_text and '}' in response_text:
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                json_str = response_text[start:end]
                return json.loads(json_str)
            return None
        except Exception as e:
            logger.error(f"Failed to parse JSON from Ollama response: {e}")
            return None
