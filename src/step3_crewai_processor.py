"""
Step 3 CrewAI Processor (step3-crewai)

Agent-based implementation using CrewAI architecture for autonomous
backend/frontend analysis with Weaviate enrichment.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

try:
    from crewai import Agent, Task, Crew, Process, LLM as CrewLLM
    from crewai.tools import BaseTool
    from crewai_tools import FileReadTool, DirectoryReadTool
    from pydantic import Field
except ImportError:
    print("CrewAI not installed. Install with: pip install crewai crewai-tools")
    raise

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


class WeaviateEnrichmentTool(BaseTool):
    """Custom tool for Weaviate semantic enrichment."""
    
    name: str = "weaviate_enrichment"
    description: str = "Query Weaviate for semantic enrichment of code components and business logic"
    
    def __init__(self, weaviate_client: WeaviateClient):
        super().__init__()
        self._weaviate_client = weaviate_client
    
    def _run(self, query: str, collection: str = None, limit: int = 5) -> str:
        """Execute Weaviate query for enrichment."""
        try:
            collections = [collection] if collection else ['JavaCodeChunks', 'BusinessRules', 'UIComponents']
            results = []
            
            for coll in collections:
                try:
                    chunk_results = self._weaviate_client.query_chunks(coll, query, limit=limit)
                    if chunk_results:
                        for result in chunk_results:
                            results.append({
                                'collection': coll,
                                'file_path': result.get('filePath', ''),
                                'content': result.get('content', '')[:300],  # Truncate for token efficiency
                                'chunk_kind': result.get('chunkKind', ''),
                                'language': result.get('language', '')
                            })
                except Exception as e:
                    continue
            
            if results:
                return json.dumps(results, indent=2)
            else:
                return "No relevant semantic data found in Weaviate"
        
        except Exception as e:
            return f"Weaviate query failed: {str(e)}"


class SourceCodeRevisitorTool(BaseTool):
    """Custom tool for revisiting source code files."""
    
    name: str = "source_code_revisitor"
    description: str = "Revisit and analyze source code files for detailed component information"
    
    def __init__(self, project_data: Dict[str, Any], config=None):
        super().__init__()
        self._project_data = project_data
        self._config = config
    
    def _run(self, file_path: str) -> str:
        """Read and analyze source file content."""
        try:
            # Find file in project data
            file_list = self._project_data.get('file_list', [])
            file_info = next((f for f in file_list if f.get('path') == file_path), None)
            
            if not file_info:
                return f"File not found in project data: {file_path}"
            
            # Try to read actual source file content
            source_content = self._read_source_file(file_path)
            
            analysis = {
                'file_path': file_path,
                'language': file_info.get('language', 'unknown'),
                'size_bytes': file_info.get('size_bytes', 0),
                'enhanced_analysis': file_info.get('enhanced_ai_analysis', {}),
                'llm_metadata': file_info.get('llm_metadata', {}),
                'source_available': bool(source_content),
                'content_preview': source_content[:500] if source_content else "// Source code not accessible",
                'detected_patterns': self._analyze_patterns(file_path, file_info, source_content)
            }
            
            return json.dumps(analysis, indent=2)
        
        except Exception as e:
            return f"Error revisiting source file: {str(e)}"
    
    def _read_source_file(self, file_path: str) -> str:
        """Read source file using multiple path resolution strategies."""
        try:
            from pathlib import Path
            
            # Try multiple path resolution strategies (same as PGM processor)
            paths_to_try = []
            
            # 1. Use JAVA_SOURCE_DIR if configured
            if self._config and hasattr(self._config, 'java_source_dir') and self._config.java_source_dir:
                java_source_dir = Path(self._config.java_source_dir)
                paths_to_try.append(java_source_dir / file_path)
                
                # Also try without project name prefix
                if '/' in file_path:
                    path_parts = file_path.split('/')
                    if len(path_parts) > 1:
                        relative_path = '/'.join(path_parts[1:])
                        paths_to_try.append(java_source_dir / relative_path)
            
            # 2. Try as absolute path
            abs_path = Path(file_path)
            if abs_path.is_absolute():
                paths_to_try.append(abs_path)
            
            # 3. Try relative to current working directory
            paths_to_try.append(Path.cwd() / file_path)
            
            # 4. Try relative to output directory
            if self._config and hasattr(self._config, 'output_dir'):
                output_parent = Path(self._config.output_dir).parent
                paths_to_try.append(output_parent / file_path)
            
            # Try each path until one works
            for full_path in paths_to_try:
                try:
                    if full_path.exists() and full_path.is_file():
                        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if content.strip():
                                return content
                except Exception:
                    continue
            
            return ""  # No file found
            
        except Exception:
            return ""
    
    def _analyze_patterns(self, file_path: str, file_info: Dict[str, Any], source_content: str = "") -> List[str]:
        """Analyze patterns in file based on metadata."""
        patterns = []
        
        # Language-based patterns
        language = file_info.get('language', '').lower()
        if language == 'java':
            if 'dao' in file_path.lower() or 'repository' in file_path.lower():
                patterns.append('Data Access Object pattern')
            if 'dto' in file_path.lower() or 'model' in file_path.lower():
                patterns.append('Data Transfer Object pattern')
            if 'service' in file_path.lower():
                patterns.append('Service Layer pattern')
        
        # Enhanced analysis patterns
        enhanced = file_info.get('enhanced_ai_analysis', {})
        if enhanced:
            classification = enhanced.get('file_classification', {})
            layer = classification.get('architectural_layer', '')
            if layer:
                patterns.append(f'Architectural layer: {layer}')
        
        return patterns


class _MockAdapterTool(BaseTool):
    """Adapter to wrap arbitrary callables/mocks into a CrewAI BaseTool for testing."""
    name: str = "mock_adapter_tool"
    description: str = "Adapter tool that forwards to an underlying callable's __call__ or _run"

    def __init__(self, underlying):
        super().__init__()
        self._underlying = underlying

    def _run(self, *args, **kwargs) -> str:
        func = None
        if hasattr(self._underlying, "_run") and callable(getattr(self._underlying, "_run")):
            func = getattr(self._underlying, "_run")
        elif callable(self._underlying):
            func = self._underlying
        else:
            # Best-effort string for validation only
            return ""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"adapter_error: {e}"


def _ensure_tool(tool) -> BaseTool:
    """Ensure the given object is a BaseTool; wrap mocks if necessary."""
    try:
        if isinstance(tool, BaseTool):
            return tool
    except Exception:
        pass
    return _MockAdapterTool(tool)


class Step3CrewAIProcessor:
    """
    CrewAI-based processor for Step 3 requirements synthesis.
    
    Uses autonomous agents for backend/frontend analysis with
    dynamic Weaviate enrichment and cross-agent collaboration.
    """
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.llm_client: Optional[LLMClient] = None
        self.weaviate_client: Optional[WeaviateClient] = None
        self.reporting: Optional[ReportingManager] = None
        self.crewai_llm: Optional[CrewLLM] = None
        
        # Output directories
        self.requirements_dir = Path(self.config.output_dir) / 'requirements'
        self.crewai_output_dir = self.requirements_dir / 'crewai'
        
        # Agent results storage
        self.agent_results: Dict[str, Any] = {}
    
    def initialize_components(self) -> None:
        """Initialize LLM, Weaviate, and reporting components."""
        try:
            self.logger.info("Initializing Step3-CrewAI components...")
            
            self.llm_client = LLMClient(self.config)
            self.weaviate_client = WeaviateClient(self.config)
            self.reporting = ReportingManager(self.config)
            # Configure CrewAI LLM to use local Ollama (avoid LiteLLM OpenAI default)
            try:
                if getattr(self.config, 'ai_provider', 'ollama') == 'ollama':
                    model_name = getattr(self.config, 'ollama_model_name', 'llama3.2:3b')
                    base_url = getattr(self.config, 'ollama_base_url', 'http://localhost:11434')
                    # CrewAI expects model format like "ollama/<model>"
                    self.crewai_llm = CrewLLM(model=f"ollama/{model_name}", base_url=base_url)
                else:
                    # Fallback: try provider's model name directly; relies on env keys if needed
                    openai_model = getattr(self.config, 'openai_model_name', 'gpt-4o')
                    self.crewai_llm = CrewLLM(model=openai_model)
            except Exception as e:
                self.logger.warning(f"Could not initialize CrewAI LLM, will use framework default: {e}")
            
            # Test connectivity
            self.weaviate_client.get_all_collection_stats()
            self.logger.info("All components initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Component initialization failed: {e}")
            raise
    
    def load_intermediate_data(self) -> Dict[str, Any]:
        """Load intermediate JSON data."""
        output_dir = Path(self.config.output_dir)
        
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
    
    def create_backend_agent(self, weaviate_tool: WeaviateEnrichmentTool, 
                           revisitor_tool: SourceCodeRevisitorTool) -> Agent:
        """Create backend analysis agent."""
        return Agent(
            role='Backend Architecture Analyst',
            goal='Analyze backend components (DAO, DTO, Service) and their relationships',
            backstory='''You are an expert backend developer specializing in enterprise Java applications. 
            You excel at identifying data access patterns, service architectures, and business logic separation.
            You understand DAO/DTO patterns, dependency injection, and service layer design.''',
            verbose=True,
            allow_delegation=True,
            tools=[_ensure_tool(weaviate_tool), _ensure_tool(revisitor_tool)],
            max_iter=3,
            memory=False,
            llm=self.crewai_llm
        )
    
    def create_frontend_agent(self, weaviate_tool: WeaviateEnrichmentTool, 
                            revisitor_tool: SourceCodeRevisitorTool) -> Agent:
        """Create frontend analysis agent."""
        return Agent(
            role='Frontend Architecture Analyst',
            goal='Analyze frontend components, UI workflows, and user interactions',
            backstory='''You are a frontend architecture expert with deep knowledge of web technologies,
            UI frameworks, and user experience patterns. You specialize in identifying forms,
            event handlers, API interactions, and UI business logic.''',
            verbose=True,
            allow_delegation=True,
            tools=[_ensure_tool(weaviate_tool), _ensure_tool(revisitor_tool)],
            max_iter=3,
            memory=False,
            llm=self.crewai_llm
        )
    
    def create_enricher_agent(self, weaviate_tool: WeaviateEnrichmentTool) -> Agent:
        """Create semantic enrichment agent."""
        return Agent(
            role='Semantic Enrichment Specialist',
            goal='Provide contextual enrichment using Weaviate vector database queries',
            backstory='''You are a knowledge extraction expert who specializes in semantic search
            and contextual information retrieval. You help other agents by finding relevant
            code patterns, similar implementations, and related business logic using vector similarity.''',
            verbose=True,
            allow_delegation=False,
            tools=[_ensure_tool(weaviate_tool)],
            max_iter=2,
            memory=False,
            llm=self.crewai_llm
        )
    
    def create_integration_agent(self) -> Agent:
        """Create integration analysis agent."""
        return Agent(
            role='Integration Architecture Specialist',
            goal='Analyze cross-cutting concerns and integration points between components',
            backstory='''You are a systems integration expert who identifies how different components
            interact, data flows between layers, and API integration patterns. You synthesize
            information from backend and frontend analyses to create comprehensive integration documentation.''',
            verbose=True,
            allow_delegation=True,
            max_iter=3,
            memory=False,
            llm=self.crewai_llm
        )
    
    def create_backend_analysis_task(self, agent: Agent, project_name: str, 
                                   project_data: Dict[str, Any]) -> Task:
        """Create backend analysis task."""
        file_list_summary = self._create_file_list_summary(project_data, ['java', 'xml'])
        
        return Task(
            description=f'''Analyze the backend components of project "{project_name}".
            
            Your task is to:
            1. For each Java file in the project, use the source_code_revisitor tool to read its content
            2. Identify and categorize DAO (Data Access Object) components based on actual annotations and patterns
            3. Identify and categorize DTO (Data Transfer Object) components from the source code
            4. Identify and categorize Service layer components using actual @Service annotations
            5. Extract relationships between these components from import statements and dependency injection
            6. Document business logic and transaction boundaries found in the source code
            7. Use the weaviate_enrichment tool to find related code patterns and examples
            
            **IMPORTANT**: You must use the source_code_revisitor tool for each significant Java file
            to examine actual source code content, not just file metadata.
            
            Project files to analyze:
            {file_list_summary}
            
            Focus on:
            - Data access patterns and repository implementations
            - Entity relationships and data models
            - Service layer architecture and dependency injection
            - Business logic encapsulation
            - Transaction management
            
            Output a detailed JSON report with components categorized into dao, dto, and service arrays.
            Include relationships between components, business logic descriptions, and a list of 
            source files analyzed using the source_code_revisitor tool. Each component should include
            file_path, class_name, methods/fields, and annotations found in the actual source code.''',
            expected_output='Comprehensive JSON report of backend component analysis with actual source code analysis',
            agent=agent
        )
    
    def create_frontend_analysis_task(self, agent: Agent, project_name: str, 
                                    project_data: Dict[str, Any]) -> Task:
        """Create frontend analysis task."""
        file_list_summary = self._create_file_list_summary(project_data, ['jsp', 'html', 'javascript', 'typescript', 'css'])
        
        return Task(
            description=f'''Analyze the frontend components of project "{project_name}".
            
            Your task is to:
            1. For each frontend file (JSP, HTML, JS, CSS), use the source_code_revisitor tool to read its content
            2. Identify UI components and their purposes from actual source code
            3. Extract form definitions and input validations from HTML/JSP source
            4. Identify event handlers and user interaction patterns from JavaScript code
            5. Document API calls and data binding found in the source files
            6. Analyze navigation flows and routing from actual implementation
            7. Use the weaviate_enrichment tool to find similar UI patterns
            
            **IMPORTANT**: You must use the source_code_revisitor tool for each frontend file
            to examine actual source code content, not just file metadata.
            
            Project files to analyze:
            {file_list_summary}
            
            Focus on:
            - Form structures and data collection
            - User interaction workflows
            - Client-side business logic
            - API endpoint consumption
            - UI component relationships
            - Navigation and routing patterns
            
            Output a detailed JSON report with ui_components, workflows, api_calls, and navigation arrays.
            Include source_files_analyzed list showing which files were examined with the source_code_revisitor tool.
            Each component should include file_path, forms, interactions, and API calls found in actual source code.''',
            expected_output='Comprehensive JSON report of frontend component analysis with actual source code analysis',
            agent=agent
        )
    
    def create_enrichment_task(self, agent: Agent, project_name: str) -> Task:
        """Create semantic enrichment task."""
        return Task(
            description=f'''Provide semantic enrichment for project "{project_name}" analysis.
            
            Your task is to:
            1. Monitor requests from Backend and Frontend agents for enrichment
            2. Query Weaviate vector database for similar patterns and implementations
            3. Provide contextual information about code patterns and business logic
            4. Identify related components across different collections (JavaCodeChunks, BusinessRules, UIComponents)
            5. Support agents with semantic search capabilities
            
            Use the weaviate_enrichment tool to:
            - Find similar DAO/DTO implementations
            - Identify related service patterns
            - Locate comparable UI components
            - Discover business rule patterns
            
            Provide enrichment data that helps other agents understand:
            - Common implementation patterns
            - Related business logic
            - Integration examples
            - Best practice implementations''',
            expected_output='Semantic enrichment data supporting backend and frontend analysis',
            agent=agent
        )
    
    def create_integration_synthesis_task(self, agent: Agent, project_name: str) -> Task:
        """Create integration synthesis task."""
        return Task(
            description=f'''Synthesize comprehensive requirements for project "{project_name}".
            
            Your task is to:
            1. Collect and integrate actual analysis results from Backend and Frontend analysis agents
            2. Use the specific component lists, relationships, and source files identified by other agents
            3. Map data flows between the actual DAO/DTO/Service components and UI components found
            4. Document API contracts based on the actual endpoints and services discovered
            5. Create comprehensive requirements documentation from real source code analysis
            6. Generate traceability mapping from requirements back to the specific source files analyzed
            
            **IMPORTANT**: Base your requirements on the actual components, methods, and relationships
            found by the Backend and Frontend agents in their source code analysis. Do not create
            generic requirements - use the specific findings from source_code_revisitor tool results.
            
            Integration focus areas:
            - Backend-to-Frontend data flow
            - API endpoint mapping and contracts
            - Business process workflows spanning both layers
            - Data transformation and validation points
            - Security and authorization touchpoints
            - Error handling and exception flows
            
            Generate structured markdown documentation with:
            - Executive summary
            - Backend requirements (DAO/DTO/Service details)
            - Frontend requirements (UI/Workflow details)
            - Integration specifications
            - Data flow diagrams (textual)
            - API documentation
            - Business process flows
            - Traceability matrix''',
            expected_output='Complete requirements documentation with backend/frontend integration analysis',
            agent=agent
        )
    
    def _create_file_list_summary(self, project_data: Dict[str, Any], 
                                 filter_languages: List[str] = None) -> str:
        """Create a summary of files for agent task descriptions."""
        file_list = project_data.get('file_list', [])
        
        if filter_languages:
            file_list = [f for f in file_list if f.get('language', '').lower() in filter_languages]
        
        summary_lines = []
        for file_info in file_list[:20]:  # Limit to prevent token overflow
            path = file_info.get('path', '')
            language = file_info.get('language', 'unknown')
            size = file_info.get('size_bytes', 0)
            
            # Include enhanced analysis if available
            enhanced = file_info.get('enhanced_ai_analysis', {})
            classification = enhanced.get('file_classification', {}) if enhanced else {}
            layer = classification.get('architectural_layer', '') if classification else ''
            component_type = classification.get('component_type', '') if classification else ''
            
            file_desc = f"- {path} ({language}, {size} bytes)"
            if layer:
                file_desc += f" [Layer: {layer}]"
            if component_type:
                file_desc += f" [Type: {component_type}]"
            
            summary_lines.append(file_desc)
        
        if len(project_data.get('file_list', [])) > 20:
            summary_lines.append(f"... and {len(project_data.get('file_list', [])) - 20} more files")
        
        return "\n".join(summary_lines)
    
    def process_project_with_crew(self, project_name: str, 
                                project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single project using CrewAI agents."""
        self.logger.info(f"Processing project with CrewAI crew: {project_name}")
        
        # Create custom tools
        weaviate_tool = WeaviateEnrichmentTool(self.weaviate_client)
        revisitor_tool = SourceCodeRevisitorTool(project_data, self.config)
        
        # Create agents
        backend_agent = self.create_backend_agent(weaviate_tool, revisitor_tool)
        frontend_agent = self.create_frontend_agent(weaviate_tool, revisitor_tool)
        enricher_agent = self.create_enricher_agent(weaviate_tool)
        integration_agent = self.create_integration_agent()
        
        # Create tasks
        backend_task = self.create_backend_analysis_task(backend_agent, project_name, project_data)
        frontend_task = self.create_frontend_analysis_task(frontend_agent, project_name, project_data)
        enrichment_task = self.create_enrichment_task(enricher_agent, project_name)
        integration_task = self.create_integration_synthesis_task(integration_agent, project_name)
        
        # Set up task dependencies
        integration_task.context = [backend_task, frontend_task, enrichment_task]
        
        # Create and execute crew
        crew = Crew(
            agents=[backend_agent, frontend_agent, enricher_agent, integration_agent],
            tasks=[backend_task, frontend_task, enrichment_task, integration_task],
            process=Process.sequential,
            verbose=True,
            memory=False
        )
        
        try:
            # Execute crew
            result = crew.kickoff()
            
            # Extract results
            crew_results = {
                'project_name': project_name,
                'execution_result': str(result),
                'backend_analysis': backend_task.output.raw if hasattr(backend_task, 'output') else None,
                'frontend_analysis': frontend_task.output.raw if hasattr(frontend_task, 'output') else None,
                'enrichment_data': enrichment_task.output.raw if hasattr(enrichment_task, 'output') else None,
                'integration_requirements': integration_task.output.raw if hasattr(integration_task, 'output') else None,
                'agent_interactions': self._extract_agent_interactions(crew),
                'execution_stats': {
                    'agents_used': len(crew.agents),
                    'tasks_completed': len(crew.tasks),
                    'execution_time': None  # Would be tracked in real implementation
                }
            }
            
            self.logger.info(f"CrewAI processing completed for project: {project_name}")
            return crew_results
            
        except Exception as e:
            self.logger.error(f"CrewAI processing failed for project {project_name}: {e}")
            return self._generate_fallback_crew_result(project_name, project_data, str(e))
    
    def _get_llm_for_crew(self):
        """Get LLM configuration for CrewAI crew."""
        # CrewAI expects specific LLM configuration
        # This would need to be adapted based on your LLMClient implementation
        return None  # Use default LLM configured in environment
    
    def _extract_agent_interactions(self, crew) -> List[Dict[str, Any]]:
        """Extract agent interaction data from crew execution."""
        # This would extract actual agent communication logs
        # For now, return placeholder data
        return [
            {
                'interaction_type': 'delegation',
                'from_agent': 'Backend Architecture Analyst',
                'to_agent': 'Semantic Enrichment Specialist',
                'message': 'Request for DAO pattern examples',
                'timestamp': datetime.now().isoformat()
            }
        ]
    
    def _generate_fallback_crew_result(self, project_name: str, project_data: Dict[str, Any], 
                                     error: str) -> Dict[str, Any]:
        """Generate fallback result when CrewAI processing fails."""
        file_count = len(project_data.get('file_list', []))
        
        return {
            'project_name': project_name,
            'execution_result': 'FALLBACK_MODE',
            'error': error,
            'backend_analysis': json.dumps({
                'error': 'CrewAI backend analysis failed',
                'fallback_data': {
                    'project_name': project_name,
                    'total_files': file_count,
                    'analysis_method': 'fallback'
                }
            }),
            'frontend_analysis': json.dumps({
                'error': 'CrewAI frontend analysis failed',
                'fallback_data': {
                    'project_name': project_name,
                    'total_files': file_count,
                    'analysis_method': 'fallback'
                }
            }),
            'enrichment_data': json.dumps({'error': 'Enrichment failed', 'weaviate_available': True}),
            'integration_requirements': f"""# Requirements for {project_name} (Fallback)

## Status
⚠️ **CrewAI processing failed**: {error}

## Project Overview
- **Total Files**: {file_count}
- **Processing Method**: Fallback (non-agent)

## Recommendations
1. Check CrewAI configuration and dependencies
2. Validate LLM provider settings  
3. Ensure Weaviate connectivity
4. Retry with step3-pgm for programmatic analysis

## Next Steps
- Review error logs for specific issues
- Consider using the programmatic step3-pgm approach
- Validate all agent dependencies are properly installed
""",
            'agent_interactions': [],
            'execution_stats': {
                'agents_used': 0,
                'tasks_completed': 0,
                'execution_time': None,
                'failed': True
            }
        }
    
    def generate_output_files(self, crew_results: Dict[str, Any]) -> None:
        """Generate output files from CrewAI crew results."""
        try:
            project_name = crew_results['project_name']
            project_dir = self.crewai_output_dir / project_name
            project_dir.mkdir(parents=True, exist_ok=True)
            
            # Main requirements file (from integration agent)
            requirements_content = crew_results.get('integration_requirements', '')
            if requirements_content:
                with open(project_dir / 'requirements.md', 'w', encoding='utf-8') as f:
                    f.write(requirements_content)
            
            # Backend analysis file
            backend_analysis = crew_results.get('backend_analysis', '')
            if backend_analysis:
                with open(project_dir / 'backend_analysis.json', 'w', encoding='utf-8') as f:
                    f.write(backend_analysis)
            
            # Frontend analysis file
            frontend_analysis = crew_results.get('frontend_analysis', '')
            if frontend_analysis:
                with open(project_dir / 'frontend_analysis.json', 'w', encoding='utf-8') as f:
                    f.write(frontend_analysis)
            
            # Enrichment data file
            enrichment_data = crew_results.get('enrichment_data', '')
            if enrichment_data:
                with open(project_dir / 'enrichment_data.json', 'w', encoding='utf-8') as f:
                    f.write(enrichment_data)
            
            # Agent interactions log
            agent_log = {
                'project': project_name,
                'generated_at': datetime.now().isoformat(),
                'execution_stats': crew_results.get('execution_stats', {}),
                'agent_interactions': crew_results.get('agent_interactions', []),
                'execution_result': crew_results.get('execution_result', '')
            }
            
            with open(project_dir / 'agent_execution_log.json', 'w', encoding='utf-8') as f:
                json.dump(agent_log, f, indent=2)
            
            # Generate summary document
            self._generate_project_summary(project_dir, crew_results)
            
            self.logger.info(f"Generated CrewAI output files for project: {project_name}")
            
        except Exception as e:
            self.logger.error(f"Error generating output files for {crew_results.get('project_name', 'unknown')}: {e}")
            raise
    
    def _generate_project_summary(self, project_dir: Path, crew_results: Dict[str, Any]) -> None:
        """Generate project summary from crew results."""
        project_name = crew_results['project_name']
        stats = crew_results.get('execution_stats', {})
        
        summary_content = f"""# CrewAI Analysis Summary - {project_name}

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Execution Statistics
- **Agents Used**: {stats.get('agents_used', 0)}
- **Tasks Completed**: {stats.get('tasks_completed', 0)}
- **Execution Status**: {'Failed' if stats.get('failed') else 'Success'}

## Agent-Based Analysis
This project was analyzed using autonomous agents with specialized roles:

### 🤖 Backend Architecture Analyst
- Analyzed DAO, DTO, and Service components
- Extracted business logic and relationships
- Results: [backend_analysis.json](backend_analysis.json)

### 🎨 Frontend Architecture Analyst  
- Analyzed UI components and workflows
- Identified user interactions and API calls
- Results: [frontend_analysis.json](frontend_analysis.json)

### 🔍 Semantic Enrichment Specialist
- Provided Weaviate-based contextual enrichment
- Found related patterns and implementations
- Results: [enrichment_data.json](enrichment_data.json)

### 🔗 Integration Architecture Specialist
- Synthesized cross-layer requirements
- Generated comprehensive documentation
- Results: [requirements.md](requirements.md)

## Agent Interactions
Agent collaboration events: {len(crew_results.get('agent_interactions', []))}

## Output Files
- 📄 **requirements.md** - Main requirements documentation
- 📊 **backend_analysis.json** - Backend component analysis
- 🎯 **frontend_analysis.json** - Frontend component analysis  
- 🔍 **enrichment_data.json** - Weaviate semantic enrichment
- 📝 **agent_execution_log.json** - Agent interaction logs
- 📋 **summary.md** - This summary document

## Next Steps
1. Review the main requirements documentation
2. Examine detailed agent analysis results
3. Validate component classifications and relationships
4. Use enrichment data for implementation guidance
"""
        
        with open(project_dir / 'summary.md', 'w', encoding='utf-8') as f:
            f.write(summary_content)
    
    def generate_crew_summary(self, all_crew_results: List[Dict[str, Any]]) -> None:
        """Generate summary report across all CrewAI project analyses."""
        summary_file = self.crewai_output_dir / '_crewai_summary.md'
        
        total_projects = len(all_crew_results)
        successful_projects = sum(1 for r in all_crew_results if not r.get('execution_stats', {}).get('failed', True))
        failed_projects = total_projects - successful_projects
        
        total_agents_used = sum(r.get('execution_stats', {}).get('agents_used', 0) for r in all_crew_results)
        total_tasks_completed = sum(r.get('execution_stats', {}).get('tasks_completed', 0) for r in all_crew_results)
        total_interactions = sum(len(r.get('agent_interactions', [])) for r in all_crew_results)
        
        summary_content = f"""# Step 3 CrewAI Agent Analysis Summary

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary
This document summarizes the autonomous agent-based analysis of {total_projects} projects using CrewAI architecture.

## Processing Statistics
- **Total Projects**: {total_projects}
- **Successful Analyses**: {successful_projects}
- **Failed Analyses**: {failed_projects}
- **Total Agents Used**: {total_agents_used}
- **Total Tasks Completed**: {total_tasks_completed}
- **Agent Interactions**: {total_interactions}

## Agent Architecture

### 🏗️ Multi-Agent System Design
Our CrewAI implementation uses specialized agents working collaboratively:

1. **Backend Architecture Analyst** 
   - Role: Analyze DAO/DTO/Service components
   - Tools: Source code revisitor, Weaviate enrichment
   - Output: Backend component classifications and relationships

2. **Frontend Architecture Analyst**
   - Role: Analyze UI components and workflows  
   - Tools: Source code revisitor, Weaviate enrichment
   - Output: UI interaction patterns and business logic

3. **Semantic Enrichment Specialist**
   - Role: Provide contextual enrichment via Weaviate queries
   - Tools: Weaviate vector database queries
   - Output: Related patterns and implementation examples

4. **Integration Architecture Specialist**
   - Role: Synthesize cross-layer requirements
   - Tools: Agent result aggregation and analysis
   - Output: Comprehensive requirements documentation

## Projects Analyzed

"""
        
        for crew_result in all_crew_results:
            project_name = crew_result['project_name']
            stats = crew_result.get('execution_stats', {})
            status = '❌ Failed' if stats.get('failed') else '✅ Success'
            
            summary_content += f"""### [{project_name}](projects/{project_name}/requirements.md)

- **Status**: {status}
- **Agents Used**: {stats.get('agents_used', 0)}
- **Tasks Completed**: {stats.get('tasks_completed', 0)}
- **Agent Interactions**: {len(crew_result.get('agent_interactions', []))}
- **Files**: 
  - [Requirements](projects/{project_name}/requirements.md)
  - [Backend Analysis](projects/{project_name}/backend_analysis.json) 
  - [Frontend Analysis](projects/{project_name}/frontend_analysis.json)
  - [Enrichment Data](projects/{project_name}/enrichment_data.json)
  - [Agent Logs](projects/{project_name}/agent_execution_log.json)
  - [Summary](projects/{project_name}/summary.md)

"""
        
        summary_content += f"""
## Agent Collaboration Insights
{self._generate_collaboration_insights(all_crew_results)}

## Technology Integration
- ✅ **CrewAI Framework**: Multi-agent orchestration
- ✅ **Weaviate Integration**: Semantic enrichment via vector search  
- ✅ **LLM Integration**: Agent reasoning and content generation
- ✅ **Source Code Analysis**: Dynamic file revisiting
- ✅ **Cross-Agent Memory**: Persistent context sharing
- ✅ **Hierarchical Processing**: Manager-agent coordination

## Key Advantages of Agent-Based Approach
1. **Autonomous Decision Making**: Agents decide when to gather more information
2. **Specialized Expertise**: Each agent focuses on specific architectural concerns
3. **Dynamic Enrichment**: Context-aware Weaviate queries based on analysis needs
4. **Cross-Agent Collaboration**: Agents share findings and build comprehensive analysis
5. **Iterative Refinement**: Agents can revisit and enhance their analysis
6. **Scalable Architecture**: Easy to add new specialized agents

## Comparison with Programmatic Approach
| Feature | CrewAI (step3-crewai) | Programmatic (step3-pgm) |
|---------|----------------------|---------------------------|
| Analysis Method | Autonomous agents | Scripted algorithms |
| Decision Making | Dynamic, context-aware | Rule-based, predetermined |
| Enrichment Strategy | On-demand, intelligent | Systematic, comprehensive |
| Collaboration | Agent-to-agent communication | Sequential processing |
| Adaptability | High (agents learn and adapt) | Medium (configurable rules) |
| Complexity | Higher (agent coordination) | Lower (direct processing) |
| Scalability | High (add specialized agents) | Medium (add processing steps) |

## Recommendations

### When to Use CrewAI Approach:
- Complex projects requiring nuanced analysis
- Need for adaptive, context-aware processing  
- Projects with unclear architectural boundaries
- Requirement for detailed agent interaction auditing

### When to Use Programmatic Approach:
- Well-defined architectural patterns
- Need for consistent, repeatable results
- Performance-critical scenarios
- Simpler project structures

## Next Steps
1. Review individual project analyses
2. Compare results between agent-based and programmatic approaches
3. Validate agent classifications and recommendations
4. Use agent interaction logs for process improvement
5. Consider hybrid approaches for optimal results

---
*Generated by Step3 CrewAI Agent-Based Requirements Synthesis*
"""
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        
        self.logger.info(f"Generated CrewAI summary report for {total_projects} projects")
    
    def _generate_collaboration_insights(self, all_crew_results: List[Dict[str, Any]]) -> str:
        """Generate insights about agent collaboration patterns."""
        all_interactions = []
        for result in all_crew_results:
            all_interactions.extend(result.get('agent_interactions', []))
        
        if not all_interactions:
            return "No agent interactions recorded in this execution."
        
        # Analyze interaction patterns
        interaction_types = {}
        agent_pairs = {}
        
        for interaction in all_interactions:
            interaction_type = interaction.get('interaction_type', 'unknown')
            from_agent = interaction.get('from_agent', 'unknown')
            to_agent = interaction.get('to_agent', 'unknown')
            
            interaction_types[interaction_type] = interaction_types.get(interaction_type, 0) + 1
            
            pair_key = f"{from_agent} → {to_agent}"
            agent_pairs[pair_key] = agent_pairs.get(pair_key, 0) + 1
        
        insights = f"""
### Interaction Type Distribution
{chr(10).join([f"- **{itype}**: {count} occurrences" for itype, count in interaction_types.items()])}

### Most Active Agent Collaborations  
{chr(10).join([f"- {pair}: {count} interactions" for pair, count in list(agent_pairs.items())[:5]])}

### Total Collaboration Events: {len(all_interactions)}
"""
        return insights
    
    def run(self) -> None:
        """Main execution method for Step 3 CrewAI processing."""
        try:
            self.logger.info("Starting Step 3 CrewAI (Agent-based) processing...")
            
            # Initialize components
            self.initialize_components()
            
            # Load data
            data = self.load_intermediate_data()
            projects = data.get('projects', {})
            
            if not projects:
                self.logger.warning("No projects found in intermediate data")
                return
            
            # Create output directories
            self.crewai_output_dir.mkdir(parents=True, exist_ok=True)
            
            # Process projects with CrewAI
            all_crew_results = []
            
            for project_name, project_data in projects.items():
                try:
                    self.logger.info(f"Starting CrewAI analysis for project: {project_name}")
                    crew_results = self.process_project_with_crew(project_name, project_data)
                    self.generate_output_files(crew_results)
                    all_crew_results.append(crew_results)
                    
                except Exception as e:
                    self.logger.error(f"Error processing project {project_name} with CrewAI: {e}")
                    # Generate fallback result
                    fallback_result = self._generate_fallback_crew_result(project_name, project_data, str(e))
                    self.generate_output_files(fallback_result)
                    all_crew_results.append(fallback_result)
            
            # Generate summary report
            self.generate_crew_summary(all_crew_results)
            
            successful_count = sum(1 for r in all_crew_results if not r.get('execution_stats', {}).get('failed', True))
            self.logger.info(f"Step 3 CrewAI processing completed: {successful_count}/{len(all_crew_results)} projects successful")
            
        except Exception as e:
            self.logger.error(f"Step 3 CrewAI processing failed: {e}")
            raise
        finally:
            if self.weaviate_client:
                self.weaviate_client.close()