"""
CrewAI-based multi-agent requirements generation.
Uses multiple specialized agents to generate comprehensive requirements documents.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

from pydantic import BaseModel, Field
from crewai import Agent, Crew, Task, LLM
from crewai.tools import BaseTool

from config.settings import settings
from store.weaviate_client import WeaviateClient

logger = logging.getLogger(__name__)


class WeaviateSearchToolArgs(BaseModel):
    """Arguments schema for WeaviateSearchTool."""
    query: str = Field(description="Search query string")
    artifact_type: Union[str, List[str]] = Field(
        default="BackendDoc",
        description=(
            "Artifact type(s) to search. Can be a single string or a list of strings. "
            "Available types: BackendDoc, DaoCall, JspForm, IbatisStatement, DbTable, "
            "GwtModule, GwtUiBinder, GwtActivityPlace, JsArtifact"
        )
    )
    limit: int = Field(default=5, description="Maximum number of results per artifact type")


class WeaviateSearchTool(BaseTool):
    name: str = "search_weaviate"
    description: str = (
        "Search Weaviate vector database for relevant artifacts. "
        "Use this tool to retrieve context about DAO calls, JSP forms, backend documentation, "
        "GWT modules, and other code artifacts.\n\n"
        "Parameters:\n"
        "- query: Search query string\n"
        "- artifact_type: Single artifact type (string) OR list of artifact types (list). "
        "Available types: BackendDoc, DaoCall, JspForm, IbatisStatement, DbTable, "
        "GwtModule, GwtUiBinder, GwtActivityPlace, JsArtifact\n"
        "- limit: Maximum number of results per artifact type (default: 5)\n\n"
        "If artifact_type is a list, the tool will search each type and combine results. "
        "Example: artifact_type='BackendDoc' or artifact_type=['BackendDoc', 'DaoCall']\n\n"
        "Note: The tool automatically filters results by the current project context."
    )
    args_schema: type[BaseModel] = WeaviateSearchToolArgs
    
    def __init__(self, project: Optional[str] = None, **kwargs):
        """Initialize the tool with optional project name for filtering."""
        super().__init__(**kwargs)
        self.project = project
    
    def _run(self, query: str, artifact_type: Union[str, List[str]] = "BackendDoc", limit: int = 5) -> str:
        """Search Weaviate for relevant artifacts.
        
        Args:
            query: Search query string
            artifact_type: Single artifact type (string) or list of artifact types
            limit: Maximum number of results per artifact type
            
        Returns:
            Formatted string with search results
        """
        try:
            client = WeaviateClient(ensure_schema=False)
            
            # Map friendly names to Weaviate class names
            class_mapping = {
                "BackendDoc": "BackendDoc",
                "DaoCall": "DaoCall", 
                "JspForm": "JspForm",
                "IbatisStatement": "IbatisStatement",
                "DbTable": "DbTable",
                "GwtModule": "GwtModule",
                "GwtUiBinder": "GwtUiBinder",
                "GwtActivityPlace": "GwtActivityPlace",
                "JsArtifact": "JsArtifact"
            }
            
            # Handle both string and list inputs
            if isinstance(artifact_type, str):
                artifact_types = [artifact_type]
            elif isinstance(artifact_type, list):
                artifact_types = artifact_type
            else:
                # Fallback: try to convert to string
                artifact_types = [str(artifact_type)]
            
            all_artifacts = []
            all_outputs = []
            
            # Search each artifact type
            for art_type in artifact_types:
                class_name = class_mapping.get(art_type, "BackendDoc")
                
                # Use the search_artifacts method from WeaviateClient
                # Pass project name if available to filter results
                artifacts = client.search_artifacts(class_name, query, project=self.project, limit=limit)
                
                if artifacts:
                    all_artifacts.extend(artifacts)
                    type_output = [f"\n=== {art_type} ({len(artifacts)} results) ==="]
                    for i, artifact in enumerate(artifacts[:limit], 1):
                        path = artifact.get('path', 'Unknown')
                        text = artifact.get('text', artifact.get('summary', ''))[:500]
                        meta = artifact.get('meta', {})
                        
                        # Build artifact info with metadata
                        artifact_info = [f"{i}. {path}"]
                        artifact_info.append(f"   {text}...")
                        
                        # Add relevant metadata if available
                        if isinstance(meta, dict) and meta:
                            meta_parts = []
                            for key, value in meta.items():
                                if value and key not in ['rawXml', 'fullContent']:  # Skip large fields
                                    meta_parts.append(f"{key}={value}")
                            if meta_parts:
                                artifact_info.append(f"   Metadata: {', '.join(meta_parts[:5])}")  # Limit to 5 fields
                        
                        type_output.append("\n".join(artifact_info))
                    all_outputs.append("\n".join(type_output))
            
            if not all_artifacts:
                types_str = ", ".join(artifact_types) if len(artifact_types) > 1 else artifact_types[0]
                return f"No results found for '{query}' in {types_str}"
            
            # Combine all results
            header = f"Found {len(all_artifacts)} total artifacts across {len(artifact_types)} type(s):"
            return header + "\n" + "\n".join(all_outputs)
            
        except Exception as e:
            logger.error(f"Weaviate search failed: {e}", exc_info=True)
            return f"Error searching Weaviate: {e}"


def create_code_analyst_agent(llm: LLM, project: Optional[str] = None) -> Agent:
    """Create Code Analyst agent."""
    weaviate_tool = WeaviateSearchTool(project=project)
    
    return Agent(
        role='Code Analyst',
        goal='Provide EXTREMELY DETAILED code analysis organized by functional areas with specific file paths, class names, and code references',
        backstory=(
            'You are a senior software architect with 15+ years of experience analyzing enterprise Java codebases. '
            'You excel at deep-dive analysis, identifying every component, mapping data flows, and documenting '
            'technical architecture in exhaustive detail. You NEVER provide generic or speculative information - '
            'you ALWAYS reference specific files, classes, methods, and SQL statements. You organize your findings '
            'by functional areas and provide comprehensive coverage of backend architecture, database interactions, '
            'business logic, and integration points. Your analysis includes file paths, line numbers, class names, '
            'method signatures, SQL statement IDs, and all relevant technical details.'
        ),
        llm=llm,
        tools=[weaviate_tool],
        verbose=True,
        max_iter=15,  # Allow more iterations for detailed analysis
        max_execution_time=1800  # 30 minutes max
    )


def create_dependency_analyst_agent(llm: LLM, project: Optional[str] = None) -> Agent:
    """Create Build/Dependency Analyst agent."""
    weaviate_tool = WeaviateSearchTool(project=project)
    
    return Agent(
        role='Build and Dependency Analyst',
        goal='Provide EXTREMELY DETAILED dependency analysis with specific module names, endpoint paths, service interfaces, and integration contracts',
        backstory=(
            'You are a senior DevOps architect and integration specialist with expertise in enterprise Java applications. '
            'You excel at mapping complex dependency graphs, documenting build configurations, and identifying all '
            'integration points. You NEVER provide generic dependency lists - you ALWAYS include specific module names, '
            'GWT module inheritance, endpoint paths, service interface names, API contracts, and version information. '
            'You document internal dependencies, external services, build requirements, runtime dependencies, and '
            'integration patterns with complete technical detail including file paths and configuration locations.'
        ),
        llm=llm,
        tools=[weaviate_tool],
        verbose=True,
        max_iter=15,
        max_execution_time=1800
    )


def create_ui_flow_analyst_agent(llm: LLM, project: Optional[str] = None) -> Agent:
    """Create UI Flow Mapper agent."""
    weaviate_tool = WeaviateSearchTool(project=project)
    
    return Agent(
        role='UI Flow Mapper',
        goal='Provide EXTREMELY DETAILED UI analysis with specific form IDs, place tokens, component names, navigation flows, and user interaction patterns',
        backstory=(
            'You are a senior UX architect and frontend specialist with deep expertise in GWT, JSP, and enterprise web applications. '
            'You excel at mapping complex user interfaces, documenting every form field, navigation pattern, and user interaction. '
            'You NEVER provide generic UI descriptions - you ALWAYS include specific form IDs, form actions, place tokens, '
            'activity classes, component names, event handlers, and file paths. You document complete navigation flows, '
            'form validations, user roles, permissions, UI state management, and all user interaction patterns with '
            'exhaustive detail including JSP paths, UiBinder file names, and JavaScript artifacts.'
        ),
        llm=llm,
        tools=[weaviate_tool],
        verbose=True,
        max_iter=15,
        max_execution_time=1800
    )


def create_technical_writer_agent(llm: LLM) -> Agent:
    """Create Technical Writer agent."""
    return Agent(
        role='Technical Writer',
        goal='Create PROFESSIONAL, COMPREHENSIVE requirements documents with detailed sections, traceability, and specific examples organized by functional areas',
        backstory=(
            'You are a senior technical writer and requirements engineer with 20+ years of experience creating '
            'enterprise software requirements documents. You excel at synthesizing complex technical analysis into '
            'clear, comprehensive, and actionable requirements. You NEVER create generic or vague requirements - '
            'you ALWAYS include specific examples, file references, class names, and traceability links. You organize '
            'requirements by functional areas, include acceptance criteria, maintain traceability matrices, and write '
            'for both technical development teams and business stakeholders. Your documents are professional, complete, '
            'and suitable for software development planning and implementation.'
        ),
        llm=llm,
        verbose=True,
        max_iter=20,
        max_execution_time=2400  # 40 minutes for comprehensive document
    )


class CrewAIRequirementsGenerator:
    """Generate requirements using CrewAI multi-agent approach."""
    
    def __init__(self):
        """Initialize the generator."""
        self.output_root = settings.output_dir / "requirements"
        self.output_root.mkdir(parents=True, exist_ok=True)
        
        # Configure LLM for Ollama
        # Adjust base URL if needed
        base_url = settings.ollama_base_url
        if 'host.docker.internal' in base_url:
            base_url = 'http://127.0.0.1:11434'
            
        # Use Ollama model name from settings
        # For Ollama, we need to prepend the base URL with the model name
        model_name = f"ollama/{settings.ollama_model_name}"
            
        # Configure LLM with increased timeout for complex tasks
        # Default timeout is 600s, increase to 1200s (20 minutes) for CrewAI tasks
        self.llm = LLM(
            model=model_name,
            base_url=base_url,
            temperature=0.7,
            timeout=1200.0  # 20 minutes timeout for complex multi-agent tasks
        )
        
    def generate_requirements(self, project: str, artifact_context: Dict[str, Any]) -> List[Path]:
        """
        Generate requirements using CrewAI multi-agent approach.
        
        Args:
            project: Project name
            artifact_context: Context about artifacts from the codebase
            
        Returns:
            List of generated requirement file paths
        """
        logger.info(f"Starting CrewAI requirements generation for project: {project}")
        
        # Create agents with project context for proper Weaviate filtering
        code_analyst = create_code_analyst_agent(self.llm, project=project)
        dependency_analyst = create_dependency_analyst_agent(self.llm, project=project)
        ui_analyst = create_ui_flow_analyst_agent(self.llm, project=project)
        technical_writer = create_technical_writer_agent(self.llm)
        
        # Create tasks
        artifact_summary = self._create_artifact_summary(artifact_context)
        
        task1_code = Task(
            description=(
                f"Analyze the codebase for project '{project}'. "
                f"Context: {artifact_summary}\n\n"
                "Your task is to provide a DETAILED, COMPREHENSIVE code analysis organized by functional areas:\n\n"
                "## 1. Backend Architecture Analysis\n"
                "- Identify all DAO (Data Access Object) classes and their methods\n"
                "- Map service layer components and their responsibilities\n"
                "- Document controller/servlet classes and their endpoints\n"
                "- Identify business logic patterns and service boundaries\n\n"
                "## 2. Database Layer Analysis\n"
                "- Document all iBATIS/MyBatis SQL statements (SELECT, INSERT, UPDATE, DELETE)\n"
                "- Map database tables used by this project\n"
                "- Document parameter types, result types, and result maps\n"
                "- Identify database relationships and foreign keys\n"
                "- Document dynamic SQL patterns and conditional queries\n\n"
                "## 3. Data Flow and Business Logic\n"
                "- Trace data flow from UI → Service → DAO → Database\n"
                "- Document business rules and validation logic\n"
                "- Identify data transformation and mapping logic\n"
                "- Document error handling and exception patterns\n\n"
                "## 4. Technical Architecture Patterns\n"
                "- Document design patterns used (DAO, Service Layer, MVC, etc.)\n"
                "- Identify dependency injection and configuration patterns\n"
                "- Document transaction management approaches\n"
                "- Identify caching strategies if any\n\n"
                "## 5. Integration Points\n"
                "- Document internal module dependencies\n"
                "- Identify external service integrations\n"
                "- Document API contracts and interfaces\n\n"
                "Use the Weaviate search tool extensively to find relevant artifacts. "
                "Search for specific components, database operations, and business logic. "
                "Focus on BackendDoc, DaoCall, and IbatisStatement artifacts. "
                "Include file paths, class names, method names, and SQL statement IDs in your analysis. "
                "Produce a comprehensive, well-structured markdown document with clear sections and subsections."
            ),
            agent=code_analyst,
            expected_output="Detailed markdown document analyzing code structure, components, data flow, organized by functional areas with specific examples and file references"
        )
        
        task2_deps = Task(
            description=(
                f"Analyze dependencies and integration points for project '{project}'. "
                "Your task is to provide a DETAILED, COMPREHENSIVE dependencies analysis:\n\n"
                "## 1. Internal Module Dependencies\n"
                "- List all internal Java modules/packages this project depends on\n"
                "- Document shared libraries and common utilities used\n"
                "- Identify cross-project dependencies (other projects in the monorepo)\n"
                "- Map dependency relationships and their purposes\n\n"
                "## 2. Build and Configuration Requirements\n"
                "- Document build system requirements (Maven, Gradle, Ant)\n"
                "- List all external libraries and their versions (if available)\n"
                "- Document configuration files and their purposes\n"
                "- Identify environment-specific configurations\n"
                "- Document deployment and packaging requirements\n\n"
                "## 3. Frontend Dependencies\n"
                "- Document GWT module dependencies and inheritance\n"
                "- List JavaScript libraries and frameworks used\n"
                "- Document CSS/styling dependencies\n"
                "- Identify frontend build tools and processes\n\n"
                "## 4. External Service Dependencies\n"
                "- Document REST/SOAP API dependencies\n"
                "- Identify external databases or data sources\n"
                "- Document third-party service integrations\n"
                "- Map authentication/authorization service dependencies\n\n"
                "## 5. Integration Points and API Contracts\n"
                "- Document GWT RPC endpoints and their contracts\n"
                "- List RequestFactory services and their methods\n"
                "- Document JavaScript API endpoints\n"
                "- Map data exchange formats (JSON, XML, etc.)\n"
                "- Document API versioning and compatibility requirements\n\n"
                "## 6. Runtime Dependencies\n"
                "- Document application server requirements\n"
                "- List required runtime libraries\n"
                "- Document JVM version requirements\n"
                "- Identify required environment variables and configuration\n\n"
                "Use the Weaviate search tool extensively. Search for GwtModule, GwtEndpoint, JsArtifact, "
                "and BackendDoc artifacts. Include specific module names, endpoint paths, service interfaces, "
                "and file references in your analysis. Produce a comprehensive markdown document with clear sections."
            ),
            agent=dependency_analyst,
            expected_output="Detailed markdown document outlining all dependencies, build requirements, and integration points with specific examples and references"
        )
        
        task3_ui = Task(
            description=(
                f"Map UI flows and user interactions for project '{project}'. "
                "Your task is to provide a DETAILED, COMPREHENSIVE UI analysis:\n\n"
                "## 1. Forms and User Input Screens\n"
                "- List ALL JSP forms with their actions, methods, and purposes\n"
                "- Document all form fields, their types, and validation rules\n"
                "- Map form submissions to backend endpoints\n"
                "- Document form dependencies and conditional fields\n"
                "- Identify multi-step forms and wizard patterns\n\n"
                "## 2. Navigation Flows and User Journeys\n"
                "- Map GWT Activity-Place navigation patterns\n"
                "- Document all Place classes and their tokens\n"
                "- Trace navigation flows between screens\n"
                "- Document deep linking and bookmarkable URLs\n"
                "- Identify navigation guards and access controls\n\n"
                "## 3. UI Components and Interactions\n"
                "- Document GWT UiBinder components and their structure\n"
                "- List reusable UI widgets and their properties\n"
                "- Document event handlers and user interactions\n"
                "- Map UI components to their Java backing classes\n"
                "- Document i18n keys and internationalization\n\n"
                "## 4. User Roles and Permissions\n"
                "- Identify role-based access control patterns\n"
                "- Document permission checks in UI components\n"
                "- Map user roles to accessible features\n"
                "- Document authentication flows in the UI\n\n"
                "## 5. UI State Management\n"
                "- Document client-side state management patterns\n"
                "- Identify data binding and model-view relationships\n"
                "- Document UI refresh and update mechanisms\n\n"
                "## 6. User Experience Patterns\n"
                "- Document error handling and user feedback mechanisms\n"
                "- Identify loading states and progress indicators\n"
                "- Document confirmation dialogs and user prompts\n"
                "- Map success/error message patterns\n\n"
                "Use the Weaviate search tool extensively. Search for JspForm, GwtUiBinder, GwtActivityPlace, "
                "and JsArtifact artifacts. Include specific form IDs, place tokens, component names, and file paths. "
                "Produce a comprehensive markdown document with clear sections and navigation flow diagrams."
            ),
            agent=ui_analyst,
            expected_output="Detailed markdown document mapping all UI flows, forms, components, and user interactions with specific examples and file references"
        )
        
        task4_write = Task(
            description=(
                f"Consolidate all analysis into a comprehensive, DETAILED requirements document for project '{project}'. "
                "You will receive:\n"
                "- Detailed code analysis from Code Analyst\n"
                "- Comprehensive dependencies analysis from Dependency Analyst\n"
                "- Complete UI flow mapping from UI Analyst\n\n"
                "Your task is to create a PROFESSIONAL, DETAILED requirements document:\n\n"
                "## Document Structure\n"
                "1. **Executive Summary** - High-level overview of the project\n"
                "2. **Project Overview** - Purpose, scope, and context\n"
                "3. **Functional Requirements** (organized by area):\n"
                "   - Data Management Requirements\n"
                "   - Business Logic Requirements\n"
                "   - User Interface Requirements\n"
                "   - Integration Requirements\n"
                "   - Security and Access Control Requirements\n"
                "   - Error Handling and Validation Requirements\n"
                "4. **Technical Requirements**:\n"
                "   - Architecture and Design Patterns\n"
                "   - Technology Stack\n"
                "   - Performance Requirements\n"
                "   - Scalability Requirements\n"
                "5. **Dependencies and Integration Points**\n"
                "6. **User Interface Specifications**\n"
                "7. **Database Schema and Data Model**\n"
                "8. **API and Service Contracts**\n"
                "9. **Non-Functional Requirements**\n"
                "10. **Traceability Matrix** - Link requirements to code artifacts\n\n"
                "## Requirements for Each Section\n"
                "- Use clear, specific language\n"
                "- Include file paths, class names, method names, SQL statement IDs where relevant\n"
                "- Organize by functional areas (e.g., User Management, Order Processing, Reporting)\n"
                "- Include acceptance criteria for major requirements\n"
                "- Add traceability references to source artifacts\n"
                "- Use proper markdown formatting with headings, lists, tables, and code blocks\n"
                "- Write for both technical teams and business stakeholders\n\n"
                "## Quality Standards\n"
                "- Be comprehensive - include ALL findings from the analysis\n"
                "- Be specific - use concrete examples and references\n"
                "- Be organized - clear structure and logical flow\n"
                "- Be traceable - link requirements to source code artifacts\n"
                "- Be actionable - requirements should be implementable\n\n"
                "Produce a complete, professional requirements document suitable for software development teams."
            ),
            agent=technical_writer,
            expected_output="Complete, detailed requirements document in markdown format with all sections, organized by functional areas, with traceability and specific examples"
        )
        
        # Create crew
        crew = Crew(
            agents=[code_analyst, dependency_analyst, ui_analyst, technical_writer],
            tasks=[task1_code, task2_deps, task3_ui, task4_write],
            verbose=True,
            process="sequential"
        )
        
        # Execute crew
        logger.info("Executing CrewAI crew...")
        result = crew.kickoff()
        
        # Extract outputs
        analysis_results = {
            'code_analysis': task1_code.output,
            'dependencies_analysis': task2_deps.output,
            'ui_analysis': task3_ui.output,
            'final_requirements': task4_write.output
        }
        
        # Save outputs
        output_files = self._save_results(project, analysis_results)
        
        logger.info(f"CrewAI requirements generation complete for project: {project}")
        return output_files
    
    def _create_artifact_summary(self, artifact_context: Dict[str, Any]) -> str:
        """Create a detailed summary of available artifacts."""
        summary_parts = []
        
        # Map artifact types to friendly names
        type_names = {
            'dao_calls': 'DAO Calls',
            'ibatis_statements': 'iBATIS SQL Statements',
            'jsp_forms': 'JSP Forms',
            'backend_docs': 'Backend Documentation',
            'gwt_modules': 'GWT Modules',
            'gwt_uibinder': 'GWT UiBinder Components',
            'gwt_client': 'GWT Client Activities/Places',
            'js_artifacts': 'JavaScript Artifacts',
            'db_tables': 'Database Tables'
        }
        
        total_artifacts = 0
        for artifact_type, artifacts in artifact_context.items():
            if artifacts:
                friendly_name = type_names.get(artifact_type, artifact_type)
                count = len(artifacts)
                total_artifacts += count
                summary_parts.append(
                    f"- {friendly_name}: {count} artifacts"
                )
        
        if summary_parts:
            header = f"Available artifacts ({total_artifacts} total):"
            return header + "\n" + "\n".join(summary_parts)
        else:
            return "No artifacts found in artifact context. Use Weaviate search tool to find artifacts."
    
    def _save_results(self, project: str, results: Dict[str, Any]) -> List[Path]:
        """Save crew outputs to files."""
        project_dir = self.output_root / project / "crewai"
        project_dir.mkdir(parents=True, exist_ok=True)
        
        saved_files = []
        
        def _normalize_content(value: Any) -> str:
            # CrewAI Task.output may be a TaskOutput; try to extract text
            if isinstance(value, str):
                return value
            # common attributes seen on LLM outputs
            for attr in ("raw", "output", "final_output", "content"):
                try:
                    v = getattr(value, attr)
                    if isinstance(v, str) and v.strip():
                        return v
                except Exception:
                    pass
            try:
                return str(value)
            except Exception:
                return ""

        for section_name, content in results.items():
            file_path = project_dir / f"{section_name}.md"
            text = _normalize_content(content)
            file_path.write_text(text or "No content generated", encoding='utf-8')
            saved_files.append(file_path)
            logger.info(f"Saved: {file_path}")
        
        # Save the final consolidated requirements as the main output
        main_output = settings.output_dir / f"{project}_crewai_requirements.md"
        main_output.write_text(_normalize_content(results.get('final_requirements')), encoding='utf-8')
        saved_files.append(main_output)
        logger.info(f"Saved main requirements: {main_output}")
        
        return saved_files


def generate_requirements_with_crewai(project: str, artifact_context: Dict[str, Any]) -> List[Path]:
    """
    Convenience function to generate requirements with CrewAI.
    
    Args:
        project: Project name
        artifact_context: Context about artifacts
        
    Returns:
        List of generated file paths
    """
    generator = CrewAIRequirementsGenerator()
    return generator.generate_requirements(project, artifact_context)

