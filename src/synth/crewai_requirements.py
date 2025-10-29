"""
CrewAI-based multi-agent requirements generation.
Uses multiple specialized agents to generate comprehensive requirements documents.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

from crewai import Agent, Crew, Task, LLM
from crewai.tools import BaseTool

from config.settings import settings
from store.weaviate_client import WeaviateClient

logger = logging.getLogger(__name__)


class WeaviateSearchTool(BaseTool):
    name: str = "search_weaviate"
    description: str = (
        "Search Weaviate vector database for relevant artifacts. "
        "Use this tool to retrieve context about DAO calls, JSP forms, backend documentation, "
        "GWT modules, and other code artifacts."
    )
    
    def _run(self, query: str, artifact_type: str = "BackendDoc", limit: int = 5) -> str:
        """Search Weaviate for relevant artifacts."""
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
            
            class_name = class_mapping.get(artifact_type, "BackendDoc")
            
            results = client.client.query.get(
                class_name,
                ["path", "text", "summary", "project"]
            ).with_near_text({
                "concepts": [query]
            }).with_limit(limit).do()
            
            if not results or 'data' not in results:
                return f"No results found for '{query}' in {artifact_type}"
            
            artifacts = results['data']['Get'][class_name]
            
            output = [f"Found {len(artifacts)} {artifact_type} artifacts:\n"]
            for i, artifact in enumerate(artifacts[:limit], 1):
                path = artifact.get('path', 'Unknown')
                text = artifact.get('text', artifact.get('summary', ''))[:500]
                output.append(f"{i}. {path}")
                output.append(f"   {text}...")
            
            return "\n".join(output)
            
        except Exception as e:
            logger.error(f"Weaviate search failed: {e}")
            return f"Error searching Weaviate: {e}"


def create_code_analyst_agent(llm: LLM) -> Agent:
    """Create Code Analyst agent."""
    weaviate_tool = WeaviateSearchTool()
    
    return Agent(
        role='Code Analyst',
        goal='Analyze codebase structure, identify key components, and understand system architecture',
        backstory=(
            'You are a senior software engineer with expertise in analyzing legacy codebases. '
            'You excel at understanding complex systems, identifying patterns, and breaking down '
            'code into meaningful components. You work with DAO patterns, service layers, '
            'database interactions, and business logic.'
        ),
        llm=llm,
        tools=[weaviate_tool],
        verbose=True
    )


def create_dependency_analyst_agent(llm: LLM) -> Agent:
    """Create Build/Dependency Analyst agent."""
    weaviate_tool = WeaviateSearchTool()
    
    return Agent(
        role='Build and Dependency Analyst',
        goal='Understand system dependencies, build configurations, and integration points',
        backstory=(
            'You are a DevOps and build engineer specialist. You understand build systems, '
            'dependencies, module structures, and how components integrate. You identify '
            'internal and external dependencies, API contracts, and integration requirements.'
        ),
        llm=llm,
        tools=[weaviate_tool],
        verbose=True
    )


def create_ui_flow_analyst_agent(llm: LLM) -> Agent:
    """Create UI Flow Mapper agent."""
    weaviate_tool = WeaviateSearchTool()
    
    return Agent(
        role='UI Flow Mapper',
        goal='Map user interfaces, navigation flows, and frontend interactions',
        backstory=(
            'You are a UX/UI analyst specialized in understanding user interfaces and workflows. '
            'You analyze forms, screens, navigation patterns, user flows, and frontend interactions. '
            'You excel at documenting how users interact with the system.'
        ),
        llm=llm,
        tools=[weaviate_tool],
        verbose=True
    )


def create_technical_writer_agent(llm: LLM) -> Agent:
    """Create Technical Writer agent."""
    return Agent(
        role='Technical Writer',
        goal='Write clear, comprehensive, and well-structured requirements documents',
        backstory=(
            'You are an experienced technical writer who transforms technical analysis into '
            'clear requirements documents. You write for both technical teams and business stakeholders. '
            'You excel at organizing information, using proper structure, and ensuring completeness.'
        ),
        llm=llm,
        verbose=True
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
            
        self.llm = LLM(
            model=model_name,
            base_url=base_url,
            temperature=0.7
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
        
        # Create agents
        code_analyst = create_code_analyst_agent(self.llm)
        dependency_analyst = create_dependency_analyst_agent(self.llm)
        ui_analyst = create_ui_flow_analyst_agent(self.llm)
        technical_writer = create_technical_writer_agent(self.llm)
        
        # Create tasks
        artifact_summary = self._create_artifact_summary(artifact_context)
        
        task1_code = Task(
            description=(
                f"Analyze the codebase for project '{project}'. "
                f"Context: {artifact_summary}\n\n"
                "Your task:\n"
                "1. Identify key backend components (DAOs, services, controllers)\n"
                "2. Understand the data flow and business logic\n"
                "3. Map database interactions and data models\n"
                "4. Document technical architecture patterns\n\n"
                "Use the Weaviate search tool to find relevant code artifacts. "
                "Focus on BackendDoc, DaoCall, and IbatisStatement artifacts. "
                "Produce a comprehensive code analysis in markdown format."
            ),
            agent=code_analyst,
            expected_output="Markdown document analyzing code structure, components, and data flow"
        )
        
        task2_deps = Task(
            description=(
                f"Analyze dependencies and integration points for project '{project}'. "
                "Your task:\n"
                "1. Identify internal module dependencies\n"
                "2. Document build and configuration requirements\n"
                "3. Identify external service dependencies\n"
                "4. Map integration points and API contracts\n\n"
                "Use the Weaviate search tool to find relevant artifacts. "
                "Focus on GwtModule, GwtEndpoint, and JsArtifact artifacts. "
                "Produce a dependencies analysis in markdown format."
            ),
            agent=dependency_analyst,
            expected_output="Markdown document outlining dependencies, build requirements, and integration points"
        )
        
        task3_ui = Task(
            description=(
                f"Map UI flows and user interactions for project '{project}'. "
                "Your task:\n"
                "1. Identify all forms and user input screens\n"
                "2. Map navigation flows and user journeys\n"
                "3. Document UI components and interactions\n"
                "4. Identify user roles and permissions\n\n"
                "Use the Weaviate search tool to find relevant artifacts. "
                "Focus on JspForm, GwtUiBinder, and GwtActivityPlace artifacts. "
                "Produce a UI flow mapping document in markdown format."
            ),
            agent=ui_analyst,
            expected_output="Markdown document mapping UI flows, forms, and user interactions"
        )
        
        task4_write = Task(
            description=(
                f"Consolidate all analysis into a comprehensive requirements document for project '{project}'. "
                "You will receive:\n"
                "- Code analysis from Code Analyst\n"
                "- Dependencies analysis from Dependency Analyst\n"
                "- UI flow mapping from UI Analyst\n\n"
                "Your task:\n"
                "1. Synthesize all inputs into a coherent requirements document\n"
                "2. Organize into clear sections: Overview, Functional Requirements, Technical Requirements, "
                "User Interface Requirements, and Dependencies\n"
                "3. Ensure completeness and traceability\n"
                "4. Write for both technical and business audiences\n\n"
                "Produce a complete, well-structured markdown requirements document."
            ),
            agent=technical_writer,
            expected_output="Complete requirements document in markdown format with all sections"
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
        """Create a summary of available artifacts."""
        summary_parts = []
        
        for artifact_type, artifacts in artifact_context.items():
            if artifacts:
                summary_parts.append(
                    f"- {artifact_type}: {len(artifacts)} artifacts"
                )
        
        return "\n".join(summary_parts) if summary_parts else "No artifacts found"
    
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

