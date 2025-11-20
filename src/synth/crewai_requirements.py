"""
CrewAI-based multi-agent requirements generation.
Uses multiple specialized agents to generate comprehensive requirements documents.
Enhanced with source file reading capabilities and target architecture mapping.
"""
from __future__ import annotations

import json
import logging
import glob
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

from pydantic import BaseModel, Field
from crewai import Agent, Crew, Task, LLM
from crewai.tools import BaseTool

from config.settings import settings
from store.weaviate_client import WeaviateClient
from config.project_utils import extract_project_name_from_path

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
    project: Optional[str] = None  # Store project as a Pydantic field
    
    def __init__(self, project: Optional[str] = None, **kwargs):
        """Initialize the tool with optional project name for filtering."""
        super().__init__(project=project, **kwargs)
    
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
                # Try broader search strategies
                logger.info(f"No results for '{query}', trying broader search strategies")
                
                # Strategy 1: Try searching without project filter
                if self.project:
                    logger.info(f"Trying search without project filter")
                    for art_type in artifact_types:
                        class_name = class_mapping.get(art_type, "BackendDoc")
                        artifacts = client.search_artifacts(class_name, query, project=None, limit=limit * 2)
                        if artifacts:
                            # Filter manually by project name in path
                            filtered = [a for a in artifacts if self.project.lower() in a.get('path', '').lower()]
                            if filtered:
                                all_artifacts.extend(filtered[:limit])
                                type_output = [f"\n=== {art_type} ({len(filtered)} results, found via broader search) ==="]
                                for i, artifact in enumerate(filtered[:limit], 1):
                                    path = artifact.get('path', 'Unknown')
                                    text = artifact.get('text', artifact.get('summary', ''))[:500]
                                    type_output.append(f"{i}. {path}\n   {text}...")
                                all_outputs.append("\n".join(type_output))
                
                # Strategy 2: Try searching with just project name
                if not all_artifacts and self.project:
                    logger.info(f"Trying search with project name only: {self.project}")
                    for art_type in artifact_types:
                        class_name = class_mapping.get(art_type, "BackendDoc")
                        artifacts = client.search_artifacts(class_name, self.project, project=None, limit=limit * 3)
                        if artifacts:
                            filtered = [a for a in artifacts if self.project.lower() in a.get('path', '').lower()]
                            if filtered:
                                all_artifacts.extend(filtered[:limit])
                                type_output = [f"\n=== {art_type} ({len(filtered)} results, found via project name search) ==="]
                                for i, artifact in enumerate(filtered[:limit], 1):
                                    path = artifact.get('path', 'Unknown')
                                    text = artifact.get('text', artifact.get('summary', ''))[:500]
                                    type_output.append(f"{i}. {path}\n   {text}...")
                                all_outputs.append("\n".join(type_output))
            
            if not all_artifacts:
                types_str = ", ".join(artifact_types) if len(artifact_types) > 1 else artifact_types[0]
                return (
                    f"No results found for '{query}' in {types_str}.\n"
                    f"Tried multiple search strategies including broader searches.\n"
                    f"Consider using read_source_file tool to read files directly from the source directory."
                )
            
            # Combine all results
            header = f"Found {len(all_artifacts)} total artifacts across {len(artifact_types)} type(s):"
            return header + "\n" + "\n".join(all_outputs)
            
        except Exception as e:
            logger.error(f"Weaviate search failed: {e}", exc_info=True)
            return f"Error searching Weaviate: {e}. Consider using read_source_file tool as fallback."


class SourceFileReaderToolArgs(BaseModel):
    """Arguments schema for SourceFileReaderTool."""
    file_pattern: str = Field(description="File pattern to search for (e.g., '*.java', '*Dao.java', 'UserService.java')")
    project_name: Optional[str] = Field(default=None, description="Project name to filter files (optional)")
    max_files: int = Field(default=10, description="Maximum number of files to read")
    file_type: str = Field(default="java", description="File type: java, jsp, xml, js, sql")


class SourceFileReaderTool(BaseTool):
    """Tool to read source files directly from JAVA_SOURCE_DIR when Weaviate search fails."""
    name: str = "read_source_file"
    description: str = (
        "Read source files directly from the Java source directory (JAVA_SOURCE_DIR). "
        "Use this tool when Weaviate search returns no results or when you need to examine "
        "specific source files directly.\n\n"
        "Parameters:\n"
        "- file_pattern: File pattern to search (e.g., '*Dao.java', '*Service.java', '*.jsp', '*.xml')\n"
        "- project_name: Optional project name to filter files by directory path\n"
        "- max_files: Maximum number of files to read (default: 10)\n"
        "- file_type: File type filter: java, jsp, xml, js, sql (default: java)\n\n"
        "Examples:\n"
        "- file_pattern='*Dao.java', project_name='cuco-core' - Find all DAO classes in cuco-core\n"
        "- file_pattern='*.jsp', project_name='cuco-ui-admin' - Find all JSP files in cuco-ui-admin\n"
        "- file_pattern='*Service*.java' - Find all Service classes\n"
        "- file_pattern='sqlmap-*.xml' - Find all iBATIS SQL mapping files\n\n"
        "This tool searches the file system directly and reads file contents, making it useful "
        "when the Weaviate index doesn't contain the artifacts you need."
    )
    args_schema: type[BaseModel] = SourceFileReaderToolArgs
    project: Optional[str] = None  # Store project as a Pydantic field
    
    def __init__(self, project: Optional[str] = None, **kwargs):
        """Initialize the tool with optional project name."""
        super().__init__(project=project, **kwargs)
        # Store java_source_dir as instance variable (not Pydantic field)
        # since Path objects can cause issues with Pydantic serialization
        object.__setattr__(self, '_java_source_dir', 
                          Path(settings.java_source_dir) if settings.is_java_source_valid() else None)
    
    def _run(self, file_pattern: str, project_name: Optional[str] = None, max_files: int = 10, file_type: str = "java") -> str:
        """Read source files matching the pattern.
        
        Args:
            file_pattern: File pattern to search for
            project_name: Optional project name to filter
            max_files: Maximum number of files to read
            file_type: File type filter
            
        Returns:
            Formatted string with file contents
        """
        # Get java_source_dir from instance variable
        java_source_dir = getattr(self, '_java_source_dir', None)
        
        if not java_source_dir or not java_source_dir.exists():
            return f"Error: JAVA_SOURCE_DIR not configured or does not exist: {settings.java_source_dir}"
        
        # Use provided project_name or fall back to instance project
        target_project = project_name or self.project
        
        try:
            # Build search path
            if target_project:
                # Search in project-specific directory
                search_path = java_source_dir / target_project
                if not search_path.exists():
                    # Try to find project directory
                    search_path = java_source_dir
                    logger.info(f"Project directory {target_project} not found, searching in {search_path}")
            else:
                search_path = java_source_dir
            
            # Build full pattern
            if file_type == "java" and not file_pattern.endswith('.java'):
                pattern = f"**/{file_pattern}.java"
            elif file_type == "jsp" and not (file_pattern.endswith('.jsp') or file_pattern.endswith('.jspf')):
                pattern = f"**/{file_pattern}.jsp"
            elif file_type == "xml" and not file_pattern.endswith('.xml'):
                pattern = f"**/{file_pattern}.xml"
            elif file_type == "js" and not file_pattern.endswith('.js'):
                pattern = f"**/{file_pattern}.js"
            elif file_type == "sql" and not file_pattern.endswith('.sql'):
                pattern = f"**/{file_pattern}.sql"
            else:
                pattern = f"**/{file_pattern}"
            
            full_pattern = str(search_path / pattern)
            
            # Find matching files
            matches = list(glob.glob(full_pattern, recursive=True))
            
            # Filter by project if specified
            if target_project:
                matches = [m for m in matches if target_project.lower() in m.lower()]
            
            # Filter out build/test directories
            ignore_dirs = {'target', 'build', 'test', 'tests', 'node_modules', '.git', '.idea', 'generated'}
            matches = [m for m in matches if not any(f'/{d}/' in m for d in ignore_dirs)]
            
            if not matches:
                return (
                    f"No files found matching pattern '{file_pattern}' "
                    f"(type: {file_type}, project: {target_project or 'all'}) in {search_path}.\n"
                    f"Tried pattern: {full_pattern}"
                )
            
            # Limit number of files
            matches = matches[:max_files]
            
            # Read file contents
            results = []
            results.append(f"Found {len(matches)} file(s) matching '{file_pattern}':\n")
            
            for i, file_path in enumerate(matches, 1):
                try:
                    rel_path = Path(file_path).relative_to(java_source_dir)
                    file_size = os.path.getsize(file_path)
                    
                    # Read file content (limit size to avoid overwhelming)
                    max_size = 50000  # 50KB max per file
                    if file_size > max_size:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read(max_size)
                            content += f"\n... (file truncated, total size: {file_size} bytes)"
                    else:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                    
                    results.append(f"\n=== File {i}: {rel_path} ===")
                    results.append(f"Size: {file_size} bytes")
                    results.append(f"Content:\n{content}")
                    
                except Exception as e:
                    results.append(f"\n=== File {i}: {file_path} ===")
                    results.append(f"Error reading file: {e}")
            
            if len(matches) < max_files and len(glob.glob(full_pattern, recursive=True)) > len(matches):
                results.append(f"\n(Note: More files found but limited to {max_files})")
            
            return "\n".join(results)
            
        except Exception as e:
            logger.error(f"Source file reading failed: {e}", exc_info=True)
            return f"Error reading source files: {e}"


def create_code_analyst_agent(llm: LLM, project: Optional[str] = None) -> Agent:
    """Create Code Analyst agent with enhanced tools."""
    weaviate_tool = WeaviateSearchTool(project=project)
    source_reader_tool = SourceFileReaderTool(project=project)
    
    return Agent(
        role='Backend Architecture Analyst',
        goal='Provide EXTREMELY DETAILED backend code analysis organized by functional areas, mapping to NestJS + PostgreSQL target architecture',
        backstory=(
            'You are a senior software architect with 15+ years of experience analyzing enterprise Java codebases '
            'and modernizing them to NestJS + PostgreSQL. You excel at deep-dive analysis, identifying every component, '
            'mapping data flows, and documenting technical architecture in exhaustive detail. You NEVER provide generic '
            'or speculative information - you ALWAYS reference specific files, classes, methods, and SQL statements. '
            'When Weaviate search returns no results, you use the read_source_file tool to read files directly. '
            'You organize findings by functional areas and map Java/Spring patterns to NestJS equivalents. '
            'Your analysis includes file paths, class names, method signatures, SQL statement IDs, and maps them to '
            'target NestJS services, controllers, modules, and PostgreSQL entities with TypeORM.'
        ),
        llm=llm,
        tools=[weaviate_tool, source_reader_tool],
        verbose=True,
        max_iter=20,  # More iterations for detailed analysis
        max_execution_time=2400  # 40 minutes max
    )


def create_dependency_analyst_agent(llm: LLM, project: Optional[str] = None) -> Agent:
    """Create Build/Dependency Analyst agent with enhanced tools."""
    weaviate_tool = WeaviateSearchTool(project=project)
    source_reader_tool = SourceFileReaderTool(project=project)
    
    return Agent(
        role='Dependency and Integration Analyst',
        goal='Provide EXTREMELY DETAILED dependency analysis mapping Java dependencies to NestJS/Next.js equivalents',
        backstory=(
            'You are a senior DevOps architect and integration specialist with expertise in enterprise Java applications '
            'and modernizing them to NestJS + Next.js. You excel at mapping complex dependency graphs, documenting build '
            'configurations, and identifying all integration points. You NEVER provide generic dependency lists - you '
            'ALWAYS include specific module names, endpoint paths, service interface names, API contracts, and version '
            'information. When Weaviate search fails, you use read_source_file to examine pom.xml, package.json, and '
            'configuration files directly. You map Java/Spring dependencies to NestJS modules and Next.js packages, '
            'document internal dependencies, external services, build requirements, and integration patterns with complete '
            'technical detail including file paths and configuration locations.'
        ),
        llm=llm,
        tools=[weaviate_tool, source_reader_tool],
        verbose=True,
        max_iter=20,
        max_execution_time=2400
    )


def create_ui_flow_analyst_agent(llm: LLM, project: Optional[str] = None) -> Agent:
    """Create UI Flow Mapper agent with enhanced tools."""
    weaviate_tool = WeaviateSearchTool(project=project)
    source_reader_tool = SourceFileReaderTool(project=project)
    
    return Agent(
        role='Frontend Architecture Analyst',
        goal='Provide EXTREMELY DETAILED frontend analysis mapping GWT/JSP to Next.js + React target architecture',
        backstory=(
            'You are a senior UX architect and frontend specialist with deep expertise in GWT, JSP, and modernizing them '
            'to Next.js + React. You excel at mapping complex user interfaces, documenting every form field, navigation '
            'pattern, and user interaction. You NEVER provide generic UI descriptions - you ALWAYS include specific form IDs, '
            'form actions, place tokens, activity classes, component names, event handlers, and file paths. When Weaviate '
            'search fails, you use read_source_file to read JSP, UiBinder, and JavaScript files directly. You map GWT '
            'Activities/Places to Next.js pages/routes, JSP forms to React components, and document complete navigation flows, '
            'form validations, user roles, permissions, UI state management, and all user interaction patterns with '
            'exhaustive detail. You map GWT patterns to React hooks, Next.js App Router, and modern frontend patterns.'
        ),
        llm=llm,
        tools=[weaviate_tool, source_reader_tool],
        verbose=True,
        max_iter=20,
        max_execution_time=2400
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
                f"Analyze the BACKEND architecture for project '{project}' and map to NestJS + PostgreSQL target. "
                f"Context: {artifact_summary}\n\n"
                "CRITICAL: If Weaviate search returns no results, use read_source_file tool to read files directly. "
                "Try multiple search queries and file patterns. NEVER give up - always find the source code.\n\n"
                "Your task is to provide DETAILED backend analysis organized by functional areas, mapping to NestJS:\n\n"
                "## 1. Service Layer Analysis (Map to NestJS Services)\n"
                "- Identify ALL service classes and their methods (search: '*Service.java', '*ServiceImpl.java')\n"
                "- Map each service method to NestJS service methods\n"
                "- Document business logic, validation rules, and data transformations\n"
                "- Identify service dependencies and injection patterns → map to NestJS dependency injection\n"
                "- Document transaction boundaries → map to NestJS transaction decorators\n\n"
                "## 2. Data Access Layer (Map to TypeORM Entities & Repositories)\n"
                "- Identify ALL DAO classes and methods (search: '*Dao.java', '*DAO.java')\n"
                "- Document all iBATIS SQL statements (search: 'sqlmap-*.xml')\n"
                "- Map each SQL statement to TypeORM entity and repository methods\n"
                "- Document database tables, columns, relationships, foreign keys\n"
                "- Map Java entity classes to TypeORM entity classes with decorators\n"
                "- Document parameter types, result types, result maps → map to TypeScript types\n"
                "- Identify dynamic SQL patterns → map to TypeORM query builder\n\n"
                "## 3. API/Controller Layer (Map to NestJS Controllers)\n"
                "- Identify servlet/controller classes and endpoints (search: '*Controller.java', '*Servlet.java')\n"
                "- Map HTTP methods and paths to NestJS controller routes\n"
                "- Document request/response DTOs → map to NestJS DTOs with class-validator\n"
                "- Identify authentication/authorization → map to NestJS guards\n"
                "- Document error handling → map to NestJS exception filters\n\n"
                "## 4. Business Logic and Data Flow\n"
                "- Trace complete data flow: Request → Controller → Service → DAO → Database\n"
                "- Document business rules, validations, and transformations\n"
                "- Identify data mapping logic → map to NestJS mappers/DTOs\n"
                "- Document error handling and exception patterns\n"
                "- Identify caching strategies → map to NestJS cache manager\n\n"
                "## 5. Configuration and Dependency Injection\n"
                "- Document Spring configuration files (search: 'applicationContext.xml', '*Config.java')\n"
                "- Map Spring beans to NestJS providers/modules\n"
                "- Document property files and environment configuration\n"
                "- Identify dependency injection patterns → map to NestJS DI\n\n"
                "## 6. Database Schema (Map to PostgreSQL with TypeORM)\n"
                "- Document all database tables, columns, types, constraints\n"
                "- Map Java types to PostgreSQL types and TypeScript types\n"
                "- Document relationships (OneToMany, ManyToOne, etc.) → map to TypeORM relations\n"
                "- Identify indexes, foreign keys, and constraints\n"
                "- Document migration requirements\n\n"
                "For each component, provide:\n"
                "- Original Java file path and class name\n"
                "- Target NestJS file path and class name\n"
                "- Mapping explanation and migration notes\n"
                "- Code examples showing Java → NestJS transformation\n\n"
                "Use BOTH search_weaviate AND read_source_file tools. If search fails, read files directly!"
            ),
            agent=code_analyst,
            expected_output="Detailed markdown document analyzing backend architecture, mapping Java/Spring to NestJS + PostgreSQL with specific file paths, class names, and migration mappings"
        )
        
        task2_deps = Task(
            description=(
                f"Analyze dependencies and integration points for project '{project}' and map to NestJS/Next.js equivalents. "
                "CRITICAL: If Weaviate search returns no results, use read_source_file to read pom.xml, package.json, "
                "*.gwt.xml, and configuration files directly.\n\n"
                "Your task is to provide DETAILED dependencies analysis mapping to target stack:\n\n"
                "## 1. Build Dependencies (Map to package.json)\n"
                "- Read pom.xml or build files (use read_source_file: 'pom.xml')\n"
                "- List all Maven/Gradle dependencies → map to npm packages\n"
                "  - Spring Framework → NestJS core packages\n"
                "  - Hibernate/iBATIS → TypeORM\n"
                "  - Jackson → class-transformer, class-validator\n"
                "  - Logging (Log4j, SLF4J) → NestJS Logger, Winston\n"
                "  - Testing (JUnit) → Jest, NestJS Testing\n"
                "- Document build scripts → map to npm scripts\n"
                "- Map Java version requirements → Node.js version requirements\n\n"
                "## 2. Frontend Dependencies (Map to Next.js/React packages)\n"
                "- Read GWT module files (use read_source_file: '*.gwt.xml')\n"
                "- Document GWT module dependencies → map to Next.js packages\n"
                "  - GWT Widgets → React component libraries (Material-UI, Ant Design, etc.)\n"
                "  - GWT RPC → Next.js API routes + fetch\n"
                "  - GWT i18n → next-intl or react-i18next\n"
                "- List JavaScript libraries → map to npm packages\n"
                "- Document CSS frameworks → map to Tailwind CSS or similar\n"
                "- Map frontend build tools → Next.js build system\n\n"
                "## 3. Internal Module Dependencies\n"
                "- List all internal Java packages this project imports\n"
                "- Map to NestJS module structure\n"
                "- Document shared libraries → map to shared NestJS modules\n"
                "- Identify cross-project dependencies → map to npm workspace packages\n"
                "- Document dependency relationships and purposes\n\n"
                "## 4. Database Dependencies\n"
                "- Document database driver (JDBC) → map to PostgreSQL driver for TypeORM\n"
                "- Map connection pooling → TypeORM connection pool\n"
                "- Document database version requirements\n"
                "- Map migration tools → TypeORM migrations\n\n"
                "## 5. External Service Dependencies\n"
                "- Document REST/SOAP clients → map to NestJS HttpModule/axios\n"
                "- Identify external APIs → document as NestJS HTTP clients\n"
                "- Map authentication services → map to NestJS auth strategies\n"
                "- Document third-party integrations → map to NestJS modules\n\n"
                "## 6. API Contracts and Integration Points\n"
                "- Document GWT RPC interfaces → map to Next.js API route types\n"
                "- List RequestFactory services → map to Next.js API handlers\n"
                "- Document JavaScript API endpoints → standardize to REST\n"
                "- Map data formats (JSON, XML) → standardize to JSON\n"
                "- Document API versioning → map to Next.js API versioning\n\n"
                "## 7. Configuration Dependencies\n"
                "- Read configuration files (use read_source_file: 'application.properties', 'web.xml')\n"
                "- Map Spring configuration → NestJS ConfigModule\n"
                "- Document environment variables → map to Next.js env variables\n"
                "- Map property files → map to .env files\n\n"
                "## 8. Runtime Dependencies\n"
                "- Map application server (Tomcat, Jetty) → NestJS server\n"
                "- Document JVM requirements → map to Node.js requirements\n"
                "- Map runtime libraries → map to Node.js runtime\n"
                "- Document deployment requirements → map to Docker/containerization\n\n"
                "For each dependency, provide:\n"
                "- Original Java/GWT dependency name and version\n"
                "- Target NestJS/Next.js package name and version\n"
                "- Migration notes and compatibility considerations\n\n"
                "Use BOTH search_weaviate AND read_source_file tools. Read build and config files directly!"
            ),
            agent=dependency_analyst,
            expected_output="Detailed markdown document mapping all dependencies from Java/GWT to NestJS/Next.js with specific package names, versions, and migration notes"
        )
        
        task3_ui = Task(
            description=(
                f"Analyze the FRONTEND architecture for project '{project}' and map to Next.js + React target. "
                "CRITICAL: If Weaviate search returns no results, use read_source_file tool to read files directly. "
                "Try multiple search queries: '*.jsp', '*Activity.java', '*Place.java', '*.ui.xml', '*.js'.\n\n"
                "Your task is to provide DETAILED frontend analysis organized from UI down to details, mapping to Next.js + React:\n\n"
                "## 1. Pages and Routes (Map to Next.js App Router)\n"
                "- Map GWT Activities to Next.js pages (search: '*Activity.java')\n"
                "- Map GWT Places to Next.js routes (search: '*Place.java')\n"
                "- Document all Place tokens → map to Next.js route parameters\n"
                "- Trace navigation flows → map to Next.js Link/navigation\n"
                "- Document deep linking → map to Next.js dynamic routes\n"
                "- Identify route guards → map to Next.js middleware/auth\n\n"
                "## 2. Forms and User Input (Map to React Components)\n"
                "- List ALL JSP forms (search: '*.jsp', read files directly)\n"
                "- Map each JSP form to React form components\n"
                "- Document all form fields, types, validation rules\n"
                "- Map form actions to Next.js API routes\n"
                "- Document form state management → map to React useState/useForm\n"
                "- Identify multi-step forms → map to React multi-step components\n"
                "- Document conditional fields and dependencies\n\n"
                "## 3. UI Components (Map to React Components)\n"
                "- Document GWT UiBinder components (search: '*.ui.xml', read files)\n"
                "- Map each UiBinder to React functional components\n"
                "- List reusable widgets → map to React component library\n"
                "- Document component props → map to TypeScript interfaces\n"
                "- Map event handlers → map to React event handlers\n"
                "- Document component composition patterns\n\n"
                "## 4. State Management (Map to React State)\n"
                "- Document GWT client-side state → map to React useState/useReducer\n"
                "- Identify global state → map to React Context or Zustand\n"
                "- Document data binding → map to React controlled components\n"
                "- Map model-view relationships → map to React props/state\n"
                "- Document UI refresh mechanisms → map to React re-rendering\n\n"
                "## 5. API Integration (Map to Next.js API Routes)\n"
                "- Document GWT RPC calls → map to Next.js API routes\n"
                "- Map RequestFactory services → map to Next.js API handlers\n"
                "- Document JavaScript XHR/fetch calls → map to Next.js fetch\n"
                "- Map data exchange formats (JSON, XML) → standardize to JSON\n"
                "- Document error handling → map to React error boundaries\n\n"
                "## 6. User Experience and Interactions\n"
                "- Document loading states → map to React Suspense/loading states\n"
                "- Identify error handling UI → map to React error boundaries\n"
                "- Document user feedback (toasts, dialogs) → map to React UI libraries\n"
                "- Map i18n/internationalization → map to next-intl or similar\n"
                "- Document accessibility patterns → ensure React a11y compliance\n\n"
                "## 7. User Roles and Permissions\n"
                "- Identify role-based UI access → map to Next.js middleware\n"
                "- Document permission checks → map to React conditional rendering\n"
                "- Map user roles to accessible features\n"
                "- Document authentication flows → map to NextAuth.js or similar\n\n"
                "For each component, provide:\n"
                "- Original GWT/JSP file path\n"
                "- Target Next.js/React file path\n"
                "- Component mapping and migration notes\n"
                "- Code examples showing GWT/JSP → React transformation\n\n"
                "Use BOTH search_weaviate AND read_source_file tools. Read JSP and UiBinder files directly if needed!"
            ),
            agent=ui_analyst,
            expected_output="Detailed markdown document mapping frontend architecture from GWT/JSP to Next.js + React, organized from pages/routes down to components and interactions"
        )
        
        task4_write = Task(
            description=(
                f"Consolidate all analysis into a comprehensive, DETAILED requirements document for project '{project}' "
                f"mapping to target architecture: NestJS backend + PostgreSQL + Next.js frontend + React.\n\n"
                "You will receive:\n"
                "- Detailed backend analysis (Java/Spring → NestJS + PostgreSQL) from Backend Architecture Analyst\n"
                "- Comprehensive dependencies analysis from Dependency Analyst\n"
                "- Complete frontend analysis (GWT/JSP → Next.js + React) from Frontend Architecture Analyst\n\n"
                "Your task is to create a PROFESSIONAL, DETAILED requirements document structured FROM FRONTEND TO BACKEND:\n\n"
                "## Document Structure (Frontend → Backend)\n"
                "1. **Executive Summary** - High-level overview, target architecture (NestJS + PostgreSQL + Next.js + React)\n"
                "2. **Project Overview** - Purpose, scope, current architecture, target architecture\n\n"
                "3. **Frontend Requirements (Next.js + React)** - START HERE, work down to details:\n"
                "   - **3.1 Pages and Routes** - Next.js pages mapped from GWT Activities/Places\n"
                "     - List all pages with routes, parameters, navigation flows\n"
                "     - Map GWT Place tokens to Next.js route params\n"
                "     - Document route guards and authentication\n"
                "   - **3.2 UI Components** - React components mapped from JSP/UiBinder\n"
                "     - List all components with props, state, events\n"
                "     - Map JSP forms to React form components\n"
                "     - Document reusable component library\n"
                "   - **3.3 State Management** - React state patterns\n"
                "     - Component state, global state, data fetching\n"
                "     - Map GWT client state to React patterns\n"
                "   - **3.4 API Integration** - Next.js API routes and data fetching\n"
                "     - Map GWT RPC to Next.js API routes\n"
                "     - Document data fetching patterns (SSR, SSG, CSR)\n"
                "   - **3.5 User Experience** - Loading, errors, feedback, i18n\n\n"
                "4. **Backend Requirements (NestJS + PostgreSQL)** - Continue from frontend:\n"
                "   - **4.1 API Layer** - NestJS Controllers mapped from Servlets/Controllers\n"
                "     - List all endpoints with HTTP methods, paths, DTOs\n"
                "     - Map request/response handling\n"
                "     - Document authentication/authorization guards\n"
                "   - **4.2 Service Layer** - NestJS Services mapped from Java Services\n"
                "     - List all services with methods and business logic\n"
                "     - Document business rules, validations, transformations\n"
                "     - Map service dependencies and injection\n"
                "   - **4.3 Data Access Layer** - TypeORM Entities & Repositories\n"
                "     - Map DAO classes to TypeORM repositories\n"
                "     - Document all database operations (CRUD)\n"
                "     - Map iBATIS SQL to TypeORM queries\n"
                "   - **4.4 Database Schema** - PostgreSQL schema mapped from current DB\n"
                "     - List all tables, columns, types, constraints\n"
                "     - Document relationships (TypeORM relations)\n"
                "     - Map Java types to PostgreSQL/TypeScript types\n"
                "     - Document migrations required\n"
                "   - **4.5 Business Logic** - Detailed business rules and workflows\n"
                "     - Document data flow: Frontend → API → Service → Repository → DB\n"
                "     - Map business rules and validations\n"
                "     - Document error handling and exceptions\n\n"
                "5. **Integration Requirements**\n"
                "   - Internal module dependencies\n"
                "   - External service integrations\n"
                "   - API contracts and interfaces\n\n"
                "6. **Technical Architecture**\n"
                "   - Target stack: NestJS, PostgreSQL, TypeORM, Next.js, React, TypeScript\n"
                "   - Architecture patterns and design decisions\n"
                "   - Migration strategy from Java/Spring/GWT to NestJS/Next.js\n\n"
                "7. **Non-Functional Requirements**\n"
                "   - Performance, scalability, security\n"
                "   - Deployment and DevOps requirements\n\n"
                "8. **Traceability Matrix**\n"
                "   - Link each requirement to source code artifacts\n"
                "   - Map original files to target files\n"
                "   - Document migration path for each component\n\n"
                "## Requirements for Each Section\n"
                "- Use clear, specific language with concrete examples\n"
                "- Include original file paths AND target file paths\n"
                "- Show code examples: Java → TypeScript, GWT → React\n"
                "- Organize by functional areas within each layer\n"
                "- Include acceptance criteria for major requirements\n"
                "- Add traceability references to source artifacts\n"
                "- Use proper markdown with headings, lists, tables, code blocks\n"
                "- Write for development teams implementing the migration\n\n"
                "## Quality Standards\n"
                "- Be comprehensive - include ALL findings, NO placeholders\n"
                "- Be specific - use concrete examples, file paths, class names\n"
                "- Be organized - clear structure from frontend to backend\n"
                "- Be traceable - link every requirement to source code\n"
                "- Be actionable - requirements must be implementable\n"
                "- Map to target architecture - always show NestJS/Next.js equivalents\n\n"
                "Produce a complete, professional requirements document suitable for development teams migrating to NestJS + PostgreSQL + Next.js + React."
            ),
            agent=technical_writer,
            expected_output="Complete, detailed requirements document structured from frontend to backend, mapping Java/GWT to NestJS/Next.js with specific examples, file paths, and migration mappings"
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

