"""
Step 3 Programmatic Processor (step3-pgm)

Enhanced implementation that distinguishes backend/frontend components,
revisits source code, and enriches requirements with Weaviate semantic data.
"""

import json
import logging
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Set
from datetime import datetime

try:
    from .env_loader import Config
    from .llm_client import LLMClient
    from .weaviate_client import WeaviateClient
    from .reporting import ReportingManager
except ImportError:
    from env_loader import Config
    from llm_client import LLMClient
    from weaviate_client import WeaviateClient
    from reporting import ReportingManager


@dataclass
class ComponentAnalysis:
    """Analysis result for a code component."""
    component_type: str  # 'dao', 'dto', 'service', 'frontend', 'config', 'other'
    component_name: str
    file_path: str
    relationships: List[str]
    business_logic: List[str]
    endpoints: List[str]
    weaviate_enrichment: Dict[str, Any]


@dataclass
class ProjectLayerAnalysis:
    """Layer-wise analysis of a project."""
    project_name: str
    backend_components: Dict[str, List[ComponentAnalysis]]  # dao, dto, service
    frontend_components: List[ComponentAnalysis]
    configuration_components: List[ComponentAnalysis]
    data_flows: List[Dict[str, Any]]
    api_endpoints: List[Dict[str, Any]]
    business_processes: List[Dict[str, Any]]


class Step3PgmProcessor:
    """
    Programmatic processor for enhanced Step 3 requirements synthesis.
    
    Focuses on backend/frontend separation, source code revisiting,
    and Weaviate semantic enrichment.
    """
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.llm_client: Optional[LLMClient] = None
        self.weaviate_client: Optional[WeaviateClient] = None
        self.reporting: Optional[ReportingManager] = None
        
        # Output directories
        self.requirements_dir = Path(self.config.output_dir) / 'requirements'
        self.pgm_output_dir = self.requirements_dir / 'pgm'
        self.pgm_projects_dir = self.pgm_output_dir / 'projects'
        
        # Component classification patterns
        self.backend_patterns = {
            'dao': [r'.*[Dd]ao\.java$', r'.*Repository\.java$', r'.*[Dd]ata[Aa]ccess.*\.java$'],
            'dto': [r'.*[Dd]to\.java$', r'.*[Mm]odel\.java$', r'.*[Ee]ntity\.java$', r'.*[Bb]ean\.java$'],
            'service': [r'.*[Ss]ervice\.java$', r'.*[Mm]anager\.java$', r'.*[Pp]rocessor\.java$', r'.*[Hh]andler\.java$']
        }
        
        self.frontend_patterns = [
            r'.*\.jsp$', r'.*\.tsx?$', r'.*\.jsx?$', r'.*\.html$', r'.*\.vue$', r'.*\.gwt\.xml$'
        ]
        
        # Traceability tracking
        self.traceability_data: Dict[str, List[Dict[str, Any]]] = {}
    
    def initialize_components(self) -> None:
        """Initialize LLM, Weaviate, and reporting components."""
        try:
            self.logger.info("Initializing Step3-PGM components...")
            
            self.llm_client = LLMClient(self.config)
            self.weaviate_client = WeaviateClient(self.config)
            self.reporting = ReportingManager(self.config)
            
            # Test connectivity
            self.weaviate_client.get_all_collection_stats()
            self.logger.info("All components initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Component initialization failed: {e}")
            raise
    
    def load_intermediate_data(self) -> Dict[str, Any]:
        """Load intermediate JSON data with validation."""
        output_dir = Path(self.config.output_dir)
        
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
            raise FileNotFoundError(f"No intermediate data found. Expected: {primary_path} or {fallback_path}")
        
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        projects = data.get('projects', {})
        self.logger.info(f"Loaded data for {len(projects)} projects from {data_path}")
        
        return data
    
    def classify_component(self, file_path: str, file_content: str, 
                          enhanced_analysis: Dict[str, Any]) -> str:
        """Classify a component as backend (dao/dto/service) or frontend."""
        relative_path = file_path.lower()
        
        # Check backend patterns
        for component_type, patterns in self.backend_patterns.items():
            if any(re.match(pattern, relative_path) for pattern in patterns):
                return component_type
        
        # Check frontend patterns
        if any(re.match(pattern, relative_path) for pattern in self.frontend_patterns):
            return 'frontend'
        
        # Use enhanced AI analysis if available
        if enhanced_analysis:
            classification = enhanced_analysis.get('file_classification', {})
            layer = classification.get('architectural_layer', '').lower()
            component_type = classification.get('component_type', '').lower()
            
            if 'data_access' in layer or 'dao' in component_type:
                return 'dao'
            elif 'model' in component_type or 'entity' in component_type:
                return 'dto'
            elif 'service' in layer or 'service' in component_type:
                return 'service'
            elif 'frontend' in layer or 'ui' in component_type:
                return 'frontend'
        
        # Fallback to content analysis
        if self._contains_dao_patterns(file_content):
            return 'dao'
        elif self._contains_dto_patterns(file_content):
            return 'dto'
        elif self._contains_service_patterns(file_content):
            return 'service'
        elif self._contains_frontend_patterns(file_content):
            return 'frontend'
        
        return 'other'
    
    def _contains_dao_patterns(self, content: str) -> bool:
        """Check if content contains DAO-like patterns."""
        dao_indicators = [
            'extends.*Repository', 'implements.*Dao', '@Repository', 
            'EntityManager', 'Query', 'createQuery', 'persist', 'merge'
        ]
        return any(re.search(pattern, content, re.IGNORECASE) for pattern in dao_indicators)
    
    def _contains_dto_patterns(self, content: str) -> bool:
        """Check if content contains DTO-like patterns."""
        dto_indicators = [
            '@Entity', '@Table', '@Column', 'private.*get', 'private.*set',
            'public.*get.*{', 'public.*set.*{', 'serialVersionUID'
        ]
        return any(re.search(pattern, content, re.IGNORECASE) for pattern in dto_indicators)
    
    def _contains_service_patterns(self, content: str) -> bool:
        """Check if content contains Service-like patterns."""
        service_indicators = [
            '@Service', '@Component', '@Autowired', 'business logic',
            'implements.*Service', 'transaction', '@Transactional'
        ]
        return any(re.search(pattern, content, re.IGNORECASE) for pattern in service_indicators)
    
    def _contains_frontend_patterns(self, content: str) -> bool:
        """Check if content contains frontend-like patterns."""
        frontend_indicators = [
            '<form', '<input', 'onClick', 'onChange', 'useState', 'useEffect',
            'jQuery', '$', 'document.', 'window.', '<script', '</script>'
        ]
        return any(re.search(pattern, content, re.IGNORECASE) for pattern in frontend_indicators)
    
    def revisit_source_file(self, file_path: str) -> str:
        """Revisit and read source file content for detailed analysis."""
        try:
            # Try multiple path resolution strategies
            paths_to_try = []
            
            # 1. Use JAVA_SOURCE_DIR if configured
            if hasattr(self.config, 'java_source_dir') and self.config.java_source_dir:
                java_source_dir = Path(self.config.java_source_dir)
                paths_to_try.append(java_source_dir / file_path)
                
                # Also try without project name prefix (common case)
                # e.g., "cuco-core/src/main/..." -> "src/main/..."
                if '/' in file_path:
                    path_parts = file_path.split('/')
                    if len(path_parts) > 1:
                        # Try removing first part (project name)
                        relative_path = '/'.join(path_parts[1:])
                        paths_to_try.append(java_source_dir / relative_path)
            
            # 2. Try as absolute path
            abs_path = Path(file_path)
            if abs_path.is_absolute():
                paths_to_try.append(abs_path)
            
            # 3. Try relative to current working directory
            paths_to_try.append(Path.cwd() / file_path)
            
            # 4. Try relative to output directory (common case)
            if hasattr(self.config, 'output_dir'):
                output_parent = Path(self.config.output_dir).parent
                paths_to_try.append(output_parent / file_path)
            
            # Try each path until one works
            for full_path in paths_to_try:
                try:
                    if full_path.exists() and full_path.is_file():
                        self.logger.debug(f"Reading source file from: {full_path}")
                        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if content.strip():  # Only return non-empty content
                                return content
                except Exception as read_error:
                    self.logger.debug(f"Failed to read {full_path}: {read_error}")
                    continue
            
            # If no file found, log warning and return empty
            self.logger.warning(f"Source file not found in any of the attempted paths: {file_path}")
            self.logger.debug(f"Attempted paths: {[str(p) for p in paths_to_try]}")
            return ""
            
        except Exception as e:
            self.logger.error(f"Error reading source file {file_path}: {e}")
            return ""
    
    def enrich_with_weaviate(self, component: ComponentAnalysis, 
                           query_context: str) -> Dict[str, Any]:
        """Enrich component analysis with Weaviate semantic data."""
        try:
            # Query relevant collections based on component type
            collections = []
            if component.component_type in ['dao', 'dto', 'service']:
                collections = ['JavaCodeChunks', 'BusinessRules']
            elif component.component_type == 'frontend':
                collections = ['UIComponents', 'NavigationFlows']
            else:
                collections = ['JavaCodeChunks']
            
            enrichment_data = {
                'related_chunks': [],
                'similar_patterns': [],
                'integration_points': []
            }
            
            for collection in collections:
                try:
                    # Query for similar components
                    query = f"{component.component_name} {component.component_type} {query_context}"
                    results = self.weaviate_client.query_chunks(collection, query, limit=3)
                    
                    if results:
                        enrichment_data['related_chunks'].extend([
                            {
                                'collection': collection,
                                'file_path': result.get('filePath', ''),
                                'content_snippet': result.get('content', '')[:200],
                                'relevance_score': result.get('_additional', {}).get('distance', 0.0)
                            }
                            for result in results
                        ])
                
                except Exception as e:
                    self.logger.warning(f"Weaviate query failed for {collection}: {e}")
            
            return enrichment_data
            
        except Exception as e:
            self.logger.error(f"Weaviate enrichment failed for {component.component_name}: {e}")
            return {'error': str(e)}
    
    def extract_relationships(self, component: ComponentAnalysis, 
                            source_content: str) -> List[str]:
        """Extract relationships from source code."""
        relationships = []
        
        if component.component_type == 'dao':
            # Look for entity relationships, other DAOs
            entity_refs = re.findall(r'@.*Entity.*\((.*?)\)', source_content, re.IGNORECASE)
            relationships.extend(entity_refs)
            
        elif component.component_type == 'dto':
            # Look for field types, relationships
            field_types = re.findall(r'private\s+(\w+)\s+\w+;', source_content)
            relationships.extend(field_types)
            
        elif component.component_type == 'service':
            # Look for injected dependencies
            autowired_refs = re.findall(r'@Autowired.*?(\w+)\s+\w+;', source_content, re.DOTALL)
            relationships.extend(autowired_refs)
        
        return list(set(relationships))  # Remove duplicates
    
    def extract_business_logic(self, component: ComponentAnalysis, 
                             source_content: str) -> List[str]:
        """Extract business logic patterns from source code."""
        business_logic = []
        
        # Look for method signatures that suggest business operations
        methods = re.findall(r'public\s+\w+\s+(\w+)\s*\([^)]*\)', source_content)
        business_methods = [m for m in methods if any(
            keyword in m.lower() for keyword in 
            ['create', 'update', 'delete', 'process', 'calculate', 'validate', 'transform']
        )]
        business_logic.extend(business_methods)
        
        # Look for transaction boundaries
        if '@Transactional' in source_content:
            business_logic.append('Transactional operations')
        
        # Look for validation annotations
        validation_patterns = re.findall(r'@(Valid|NotNull|Size|Email|Pattern)', source_content)
        if validation_patterns:
            business_logic.append(f'Validation: {", ".join(set(validation_patterns))}')
        
        return business_logic
    
    def extract_api_endpoints(self, component: ComponentAnalysis, 
                            source_content: str) -> List[str]:
        """Extract API endpoints from source code."""
        endpoints = []
        
        # Look for REST annotations
        rest_mappings = re.findall(r'@(GetMapping|PostMapping|PutMapping|DeleteMapping|RequestMapping)\s*\(\s*"([^"]*)"', 
                                 source_content)
        for method, path in rest_mappings:
            endpoints.append(f"{method}: {path}")
        
        # Look for servlet mappings
        servlet_patterns = re.findall(r'@WebServlet\s*\(\s*"([^"]*)"', source_content)
        endpoints.extend([f"Servlet: {pattern}" for pattern in servlet_patterns])
        
        return endpoints
    
    def analyze_project_components(self, project_name: str, 
                                 project_data: Dict[str, Any]) -> ProjectLayerAnalysis:
        """Analyze project components and create layered analysis."""
        self.logger.info(f"Analyzing components for project: {project_name}")
        
        backend_components = {'dao': [], 'dto': [], 'service': []}
        frontend_components = []
        configuration_components = []
        
        file_list = project_data.get('file_list', [])
        
        for file_info in file_list:
            file_path = file_info.get('path', '')
            enhanced_analysis = file_info.get('enhanced_ai_analysis', {})
            
            # Revisit source file for detailed analysis
            source_content = self.revisit_source_file(file_path)
            
            # Classify component
            component_type = self.classify_component(file_path, source_content, enhanced_analysis)
            
            if component_type in ['other', '']:
                continue
            
            # Create component analysis
            component_name = Path(file_path).stem
            component = ComponentAnalysis(
                component_type=component_type,
                component_name=component_name,
                file_path=file_path,
                relationships=[],
                business_logic=[],
                endpoints=[],
                weaviate_enrichment={}
            )
            
            # Extract detailed information
            component.relationships = self.extract_relationships(component, source_content)
            component.business_logic = self.extract_business_logic(component, source_content)
            component.endpoints = self.extract_api_endpoints(component, source_content)
            
            # Enrich with Weaviate data
            query_context = f"project:{project_name} type:{component_type}"
            component.weaviate_enrichment = self.enrich_with_weaviate(component, query_context)
            
            # Categorize component
            if component_type in backend_components:
                backend_components[component_type].append(component)
            elif component_type == 'frontend':
                frontend_components.append(component)
            elif component_type == 'config':
                configuration_components.append(component)
        
        # Analyze data flows and business processes
        data_flows = self.analyze_data_flows(backend_components, frontend_components)
        api_endpoints = self.analyze_api_endpoints(backend_components, frontend_components)
        business_processes = self.analyze_business_processes(backend_components, frontend_components)
        
        return ProjectLayerAnalysis(
            project_name=project_name,
            backend_components=backend_components,
            frontend_components=frontend_components,
            configuration_components=configuration_components,
            data_flows=data_flows,
            api_endpoints=api_endpoints,
            business_processes=business_processes
        )
    
    def analyze_data_flows(self, backend_components: Dict[str, List[ComponentAnalysis]], 
                          frontend_components: List[ComponentAnalysis]) -> List[Dict[str, Any]]:
        """Analyze data flows between components."""
        data_flows = []
        
        # Analyze DTO -> DAO relationships
        dtos = backend_components.get('dto', [])
        daos = backend_components.get('dao', [])
        
        for dto in dtos:
            for dao in daos:
                # Check if DAO references this DTO
                if any(dto.component_name in rel for rel in dao.relationships):
                    data_flows.append({
                        'from': dto.component_name,
                        'to': dao.component_name,
                        'type': 'data_access',
                        'description': f'DTO {dto.component_name} used by DAO {dao.component_name}'
                    })
        
        # Analyze Service -> DAO relationships
        services = backend_components.get('service', [])
        for service in services:
            for dao in daos:
                if any(dao.component_name in rel for rel in service.relationships):
                    data_flows.append({
                        'from': service.component_name,
                        'to': dao.component_name,
                        'type': 'service_data',
                        'description': f'Service {service.component_name} uses DAO {dao.component_name}'
                    })
        
        return data_flows
    
    def analyze_api_endpoints(self, backend_components: Dict[str, List[ComponentAnalysis]], 
                            frontend_components: List[ComponentAnalysis]) -> List[Dict[str, Any]]:
        """Analyze API endpoints across components."""
        api_endpoints = []
        
        # Collect all endpoints from services
        services = backend_components.get('service', [])
        for service in services:
            for endpoint in service.endpoints:
                api_endpoints.append({
                    'component': service.component_name,
                    'endpoint': endpoint,
                    'layer': 'backend',
                    'business_logic': service.business_logic
                })
        
        # Collect endpoints from frontend components
        for frontend in frontend_components:
            for endpoint in frontend.endpoints:
                api_endpoints.append({
                    'component': frontend.component_name,
                    'endpoint': endpoint,
                    'layer': 'frontend',
                    'business_logic': frontend.business_logic
                })
        
        return api_endpoints
    
    def analyze_business_processes(self, backend_components: Dict[str, List[ComponentAnalysis]], 
                                 frontend_components: List[ComponentAnalysis]) -> List[Dict[str, Any]]:
        """Analyze business processes across layers."""
        business_processes = []
        
        # Group related business logic
        all_components = []
        for component_list in backend_components.values():
            all_components.extend(component_list)
        all_components.extend(frontend_components)
        
        # Extract common business themes
        business_themes = {}
        for component in all_components:
            for logic in component.business_logic:
                theme = logic.lower().split()[0] if logic else 'general'
                if theme not in business_themes:
                    business_themes[theme] = []
                business_themes[theme].append({
                    'component': component.component_name,
                    'type': component.component_type,
                    'logic': logic
                })
        
        for theme, components in business_themes.items():
            if len(components) > 1:  # Cross-component processes
                business_processes.append({
                    'process_name': theme.title(),
                    'components_involved': components,
                    'description': f'Business process involving {len(components)} components'
                })
        
        return business_processes
    
    def generate_layered_requirements(self, analysis: ProjectLayerAnalysis) -> str:
        """Generate layered requirements documentation using LLM."""
        try:
            # Build comprehensive prompt
            prompt = self._build_requirements_prompt(analysis)
            
            # Generate requirements using LLM
            requirements = self.llm_client._complete_text(
                prompt,
                system="You are a technical requirements analyst. Generate structured, detailed "
                       "requirements documentation that clearly separates backend and frontend concerns. "
                       "Include data flows, API specifications, and business processes. "
                       "Use markdown format with clear sections and subsections.",
                max_tokens=2500
            )
            
            return requirements
            
        except Exception as e:
            self.logger.error(f"Error generating layered requirements for {analysis.project_name}: {e}")
            return self._generate_fallback_requirements(analysis)
    
    def _build_requirements_prompt(self, analysis: ProjectLayerAnalysis) -> str:
        """Build comprehensive LLM prompt from analysis."""
        prompt = f"""Generate detailed requirements documentation for project: {analysis.project_name}

## Backend Components Analysis:

### Data Access Objects (DAOs):
{self._format_components_for_prompt(analysis.backend_components.get('dao', []))}

### Data Transfer Objects (DTOs):
{self._format_components_for_prompt(analysis.backend_components.get('dto', []))}

### Services:
{self._format_components_for_prompt(analysis.backend_components.get('service', []))}

## Frontend Components:
{self._format_components_for_prompt(analysis.frontend_components)}

## Data Flows:
{json.dumps(analysis.data_flows, indent=2)}

## API Endpoints:
{json.dumps(analysis.api_endpoints, indent=2)}

## Business Processes:
{json.dumps(analysis.business_processes, indent=2)}

Please generate structured requirements with the following sections:
1. Project Overview
2. Backend Requirements (DAOs, DTOs, Services)
3. Frontend Requirements (UI, Workflows)
4. API Specifications
5. Data Models and Relationships
6. Business Process Flows
7. Integration Points

Include specific details about relationships, data flows, and business logic for each component.
"""
        return prompt
    
    def _format_components_for_prompt(self, components: List[ComponentAnalysis]) -> str:
        """Format components for LLM prompt."""
        if not components:
            return "None identified"
        
        formatted = []
        for comp in components:
            enrichment_summary = ""
            if comp.weaviate_enrichment and 'related_chunks' in comp.weaviate_enrichment:
                chunk_count = len(comp.weaviate_enrichment['related_chunks'])
                enrichment_summary = f" (Weaviate: {chunk_count} related chunks)"
            
            formatted.append(
                f"- {comp.component_name} ({comp.file_path}){enrichment_summary}\n"
                f"  Relationships: {', '.join(comp.relationships) if comp.relationships else 'None'}\n"
                f"  Business Logic: {', '.join(comp.business_logic) if comp.business_logic else 'None'}\n"
                f"  Endpoints: {', '.join(comp.endpoints) if comp.endpoints else 'None'}"
            )
        
        return "\n".join(formatted)
    
    def _generate_fallback_requirements(self, analysis: ProjectLayerAnalysis) -> str:
        """Generate fallback requirements when LLM fails."""
        backend_count = sum(len(comps) for comps in analysis.backend_components.values())
        frontend_count = len(analysis.frontend_components)
        
        return f"""# Requirements for {analysis.project_name}

## Project Overview
- **Backend Components**: {backend_count}
- **Frontend Components**: {frontend_count}
- **Data Flows**: {len(analysis.data_flows)}
- **API Endpoints**: {len(analysis.api_endpoints)}

⚠️ **Note**: Requirements generated using fallback method due to LLM processing error.

## Backend Requirements

### Data Access Objects (DAOs)
{self._format_component_list(analysis.backend_components.get('dao', []))}

### Data Transfer Objects (DTOs)
{self._format_component_list(analysis.backend_components.get('dto', []))}

### Services
{self._format_component_list(analysis.backend_components.get('service', []))}

## Frontend Requirements
{self._format_component_list(analysis.frontend_components)}

## Data Flows
{self._format_data_flows(analysis.data_flows)}

## API Endpoints
{self._format_api_endpoints(analysis.api_endpoints)}

## Traceability
All components analyzed with Weaviate enrichment and source code revisiting.
"""
    
    def _format_component_list(self, components: List[ComponentAnalysis]) -> str:
        """Format component list for fallback requirements."""
        if not components:
            return "None identified"
        
        formatted = []
        for comp in components:
            formatted.append(f"- **{comp.component_name}** ({comp.file_path})")
            if comp.relationships:
                formatted.append(f"  - Relationships: {', '.join(comp.relationships)}")
            if comp.business_logic:
                formatted.append(f"  - Business Logic: {', '.join(comp.business_logic)}")
        
        return "\n".join(formatted)
    
    def _format_data_flows(self, data_flows: List[Dict[str, Any]]) -> str:
        """Format data flows for fallback requirements."""
        if not data_flows:
            return "No data flows identified"
        
        formatted = []
        for flow in data_flows:
            formatted.append(f"- {flow['from']} → {flow['to']} ({flow['type']})")
        
        return "\n".join(formatted)
    
    def _format_api_endpoints(self, api_endpoints: List[Dict[str, Any]]) -> str:
        """Format API endpoints for fallback requirements."""
        if not api_endpoints:
            return "No API endpoints identified"
        
        formatted = []
        for endpoint in api_endpoints:
            formatted.append(f"- **{endpoint['component']}** ({endpoint['layer']}): {endpoint['endpoint']}")
        
        return "\n".join(formatted)
    
    def generate_traceability_report(self, analysis: ProjectLayerAnalysis) -> str:
        """Generate traceability report linking requirements to source code and Weaviate data."""
        traceability = {
            'project': analysis.project_name,
            'generated_at': datetime.now().isoformat(),
            'component_traceability': [],
            'weaviate_enrichment_summary': {
                'total_queries': 0,
                'successful_enrichments': 0,
                'collections_used': set()
            }
        }
        
        all_components = []
        for component_list in analysis.backend_components.values():
            all_components.extend(component_list)
        all_components.extend(analysis.frontend_components)
        
        for comp in all_components:
            comp_trace = {
                'component_name': comp.component_name,
                'component_type': comp.component_type,
                'source_file': comp.file_path,
                'relationships_traced': len(comp.relationships),
                'business_logic_items': len(comp.business_logic),
                'api_endpoints': len(comp.endpoints),
                'weaviate_enrichment': {
                    'enriched': bool(comp.weaviate_enrichment and 'related_chunks' in comp.weaviate_enrichment),
                    'related_chunks_count': len(comp.weaviate_enrichment.get('related_chunks', [])),
                    'collections_queried': list(set(
                        chunk['collection'] for chunk in comp.weaviate_enrichment.get('related_chunks', [])
                    ))
                }
            }
            
            traceability['component_traceability'].append(comp_trace)
            
            # Update summary stats
            if comp_trace['weaviate_enrichment']['enriched']:
                traceability['weaviate_enrichment_summary']['successful_enrichments'] += 1
                traceability['weaviate_enrichment_summary']['collections_used'].update(
                    comp_trace['weaviate_enrichment']['collections_queried']
                )
            traceability['weaviate_enrichment_summary']['total_queries'] += 1
        
        # Convert set to list for JSON serialization
        traceability['weaviate_enrichment_summary']['collections_used'] = list(
            traceability['weaviate_enrichment_summary']['collections_used']
        )
        
        return json.dumps(traceability, indent=2)
    
    def generate_output_files(self, analysis: ProjectLayerAnalysis) -> None:
        """Generate structured output files for a project."""
        try:
            project_dir = self.pgm_projects_dir / analysis.project_name
            project_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate main requirements
            requirements = self.generate_layered_requirements(analysis)
            requirements_file = project_dir / 'requirements.md'
            with open(requirements_file, 'w', encoding='utf-8') as f:
                f.write(requirements)
            
            # Generate backend-specific documentation
            self._generate_backend_documentation(project_dir, analysis)
            
            # Generate frontend-specific documentation
            self._generate_frontend_documentation(project_dir, analysis)
            
            # Generate traceability report
            traceability = self.generate_traceability_report(analysis)
            trace_file = project_dir / 'traceability.json'
            with open(trace_file, 'w', encoding='utf-8') as f:
                f.write(traceability)
            
            self.logger.info(f"Generated PGM output files for project: {analysis.project_name}")
            
        except Exception as e:
            self.logger.error(f"Error generating output files for {analysis.project_name}: {e}")
            raise
    
    def _generate_backend_documentation(self, project_dir: Path, analysis: ProjectLayerAnalysis) -> None:
        """Generate backend-specific documentation."""
        backend_content = f"""# Backend Documentation - {analysis.project_name}

## Data Access Layer (DAOs)
{self._format_component_list(analysis.backend_components.get('dao', []))}

## Data Model Layer (DTOs)
{self._format_component_list(analysis.backend_components.get('dto', []))}

## Service Layer
{self._format_component_list(analysis.backend_components.get('service', []))}

## Data Flow Analysis
{self._format_data_flows(analysis.data_flows)}

## Business Processes
{json.dumps(analysis.business_processes, indent=2)}

## Generated on
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        with open(project_dir / 'backend_details.md', 'w', encoding='utf-8') as f:
            f.write(backend_content)
    
    def _generate_frontend_documentation(self, project_dir: Path, analysis: ProjectLayerAnalysis) -> None:
        """Generate frontend-specific documentation."""
        frontend_content = f"""# Frontend Documentation - {analysis.project_name}

## UI Components
{self._format_component_list(analysis.frontend_components)}

## Frontend API Endpoints
{self._format_frontend_endpoints(analysis)}

## UI Business Logic
{self._format_frontend_business_logic(analysis)}

## Generated on
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        with open(project_dir / 'frontend_details.md', 'w', encoding='utf-8') as f:
            f.write(frontend_content)
    
    def _format_frontend_endpoints(self, analysis: ProjectLayerAnalysis) -> str:
        """Format frontend-specific endpoints."""
        frontend_endpoints = [ep for ep in analysis.api_endpoints if ep['layer'] == 'frontend']
        
        if not frontend_endpoints:
            return "No frontend-specific endpoints identified"
        
        formatted = []
        for endpoint in frontend_endpoints:
            formatted.append(f"- **{endpoint['component']}**: {endpoint['endpoint']}")
        
        return "\n".join(formatted)
    
    def _format_frontend_business_logic(self, analysis: ProjectLayerAnalysis) -> str:
        """Format frontend business logic."""
        if not analysis.frontend_components:
            return "No frontend business logic identified"
        
        formatted = []
        for comp in analysis.frontend_components:
            if comp.business_logic:
                formatted.append(f"## {comp.component_name}")
                for logic in comp.business_logic:
                    formatted.append(f"- {logic}")
                formatted.append("")
        
        return "\n".join(formatted)
    
    def run(self, parallel: bool = True, max_workers: int = 3) -> None:
        """Main execution method for Step 3 PGM processing."""
        try:
            self.logger.info("Starting Step 3 Programmatic (PGM) processing...")
            
            # Initialize components
            self.initialize_components()
            
            # Load data
            data = self.load_intermediate_data()
            projects = data.get('projects', {})
            
            if not projects:
                self.logger.warning("No projects found in intermediate data")
                return
            
            # Create output directories
            self.pgm_output_dir.mkdir(parents=True, exist_ok=True)
            self.pgm_projects_dir.mkdir(parents=True, exist_ok=True)
            
            # Process projects
            project_analyses = {}
            
            if parallel and len(projects) > 1:
                self.logger.info(f"Processing {len(projects)} projects in parallel with {max_workers} workers")
                project_analyses = self._process_projects_parallel(projects, max_workers)
            else:
                self.logger.info("Processing projects sequentially")
                for project_name, project_data in projects.items():
                    try:
                        analysis = self.analyze_project_components(project_name, project_data)
                        self.generate_output_files(analysis)
                        project_analyses[project_name] = analysis
                    except Exception as e:
                        self.logger.error(f"Error processing project {project_name}: {e}")
            
            # Generate summary report
            self._generate_summary_report(project_analyses)
            
            self.logger.info("Step 3 PGM processing completed successfully")
            
        except Exception as e:
            self.logger.error(f"Step 3 PGM processing failed: {e}")
            raise
        finally:
            if self.weaviate_client:
                self.weaviate_client.close()
    
    def _process_projects_parallel(self, projects: Dict[str, Any], max_workers: int) -> Dict[str, ProjectLayerAnalysis]:
        """Process projects in parallel."""
        project_analyses = {}
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_project = {
                executor.submit(self._process_single_project, name, data): name
                for name, data in projects.items()
            }
            
            # Collect results
            for future in as_completed(future_to_project):
                project_name = future_to_project[future]
                try:
                    analysis = future.result()
                    self.generate_output_files(analysis)
                    project_analyses[project_name] = analysis
                    self.logger.info(f"Completed PGM processing: {project_name}")
                except Exception as e:
                    self.logger.error(f"Error processing {project_name}: {e}")
        
        return project_analyses
    
    def _process_single_project(self, project_name: str, project_data: Dict[str, Any]) -> ProjectLayerAnalysis:
        """Process a single project (thread-safe)."""
        return self.analyze_project_components(project_name, project_data)
    
    def _generate_summary_report(self, project_analyses: Dict[str, ProjectLayerAnalysis]) -> None:
        """Generate summary report across all projects."""
        summary_file = self.pgm_output_dir / '_pgm_summary.md'
        
        total_backend = sum(
            sum(len(comps) for comps in analysis.backend_components.values())
            for analysis in project_analyses.values()
        )
        total_frontend = sum(len(analysis.frontend_components) for analysis in project_analyses.values())
        total_data_flows = sum(len(analysis.data_flows) for analysis in project_analyses.values())
        
        summary_content = f"""# Step 3 Programmatic (PGM) Summary

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Processing Statistics
- **Total Projects**: {len(project_analyses)}
- **Total Backend Components**: {total_backend}
- **Total Frontend Components**: {total_frontend}
- **Total Data Flows**: {total_data_flows}

## Projects Processed

"""
        
        for project_name, analysis in project_analyses.items():
            backend_count = sum(len(comps) for comps in analysis.backend_components.values())
            summary_content += f"""### [{project_name}](projects/{project_name}/requirements.md)

- **Backend Components**: {backend_count} (DAO: {len(analysis.backend_components.get('dao', []))}, DTO: {len(analysis.backend_components.get('dto', []))}, Service: {len(analysis.backend_components.get('service', []))})
- **Frontend Components**: {len(analysis.frontend_components)}
- **Data Flows**: {len(analysis.data_flows)}
- **API Endpoints**: {len(analysis.api_endpoints)}
- **Business Processes**: {len(analysis.business_processes)}
- **[Requirements](projects/{project_name}/requirements.md)** | **[Backend Details](projects/{project_name}/backend_details.md)** | **[Frontend Details](projects/{project_name}/frontend_details.md)** | **[Traceability](projects/{project_name}/traceability.json)**

"""
        
        summary_content += f"""
## Enhanced Features
- ✅ Backend/Frontend separation
- ✅ Source code revisiting
- ✅ Weaviate semantic enrichment
- ✅ Component relationship analysis
- ✅ Data flow tracing
- ✅ API endpoint documentation
- ✅ Business process identification
- ✅ Traceability reporting

## Next Steps
1. Review detailed project requirements
2. Validate component classifications
3. Enhance business process definitions
4. Update API specifications
"""
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        
        self.logger.info(f"Generated PGM summary report for {len(project_analyses)} projects")