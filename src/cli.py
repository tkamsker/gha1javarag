"""
Command-line interface for the Java/JSP/GWT/JS → PRD pipeline.
"""
import logging
import sys
from pathlib import Path
from typing import Optional, List
import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from config.settings import settings
from discover.file_discovery import FileDiscovery
from extract.gwt_modules import GwtModuleExtractor
from extract.gwt_client import GwtClientExtractor
from extract.gwt_uibinder import GwtUiBinderExtractor
from extract.js_static import JavaScriptExtractor
from extract.ibatis_xml import IbatisXmlExtractor
from extract.java_calls import JavaCallsExtractor
from extract.jsp_forms import JspFormsExtractor
from extract.db_schema import DatabaseSchemaExtractor
from extract.backend_llm import BackendLLMExtractor
from chunk.build_chunks import ChunkBuilder
from store.weaviate_client import WeaviateClient
from synth.prd_markdown import PRDMarkdownGenerator

# Setup logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

console = Console()

@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def cli(verbose):
    """Java/JSP/GWT/JS → PRD Pipeline CLI"""
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

@cli.command()
@click.option('--project', '-p', default=None, help='Project name (defaults to auto-detection)')
@click.option('--include-frontend', is_flag=True, help='Include frontend extraction (GWT/JS)')
def discover(project: Optional[str], include_frontend: bool):
    """Discover files in the Java source directory"""
    console.print("[bold blue]Discovering files...[/bold blue]")
    
    discovery = FileDiscovery()
    discovered_files = discovery.discover_all_files(project)
    
    # Create summary table
    table = Table(title="File Discovery Results")
    table.add_column("File Type", style="cyan")
    table.add_column("Count", style="magenta")
    table.add_column("Files", style="green")
    
    total_files = 0
    for file_type, files in discovered_files.items():
        if files:
            table.add_row(
                file_type.upper(),
                str(len(files)),
                ", ".join([Path(f).name for f in list(files)[:3]]) + 
                (f" (+{len(files)-3} more)" if len(files) > 3 else "")
            )
            total_files += len(files)
    
    console.print(table)
    console.print(f"[bold green]Total files discovered: {total_files}[/bold green]")

@cli.command()
@click.option('--project', '-p', default=None, help='Project name')
@click.option('--include-frontend', is_flag=True, help='Include frontend extraction')
def extract(project: Optional[str], include_frontend: bool):
    """Extract artifacts from discovered files"""
    console.print("[bold blue]Extracting artifacts...[/bold blue]")
    
    # Discover files
    discovery = FileDiscovery()
    discovered_files = discovery.discover_all_files(project)
    
    # Initialize extractors
    extractors = {
        'ibatis_statements': IbatisXmlExtractor(),
        'dao_calls': JavaCallsExtractor(),
        'jsp_forms': JspFormsExtractor(),
        'db_tables': DatabaseSchemaExtractor(),
        'backend_docs': BackendLLMExtractor()
    }
    
    if include_frontend:
        extractors.update({
            'gwt_modules': GwtModuleExtractor(),
            'gwt_activities_places': GwtClientExtractor(),
            'gwt_uibinder': GwtUiBinderExtractor(),
            'js_artifacts': JavaScriptExtractor()
        })
    
    # Extract artifacts
    all_artifacts = {}
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        # Backend extraction
        task1 = progress.add_task("Extracting iBATIS statements...", total=None)
        if 'xml' in discovered_files:
            all_artifacts['ibatis_statements'] = extractors['ibatis_statements'].extract_ibatis_statements(
                list(discovered_files['xml'])
            )
        progress.update(task1, description="iBATIS statements extracted")
        
        task2 = progress.add_task("Extracting DAO calls...", total=None)
        if 'java' in discovered_files:
            all_artifacts['dao_calls'] = extractors['dao_calls'].extract_java_calls(
                list(discovered_files['java'])
            )
        progress.update(task2, description="DAO calls extracted")
        
        task3 = progress.add_task("Extracting JSP forms...", total=None)
        if 'jsp' in discovered_files:
            all_artifacts['jsp_forms'] = extractors['jsp_forms'].extract_jsp_forms(
                list(discovered_files['jsp'])
            )
        progress.update(task3, description="JSP forms extracted")
        
        task4 = progress.add_task("Extracting database schema...", total=None)
        if 'sql' in discovered_files:
            all_artifacts['db_tables'] = extractors['db_tables'].extract_database_schema(
                list(discovered_files['sql'])
            )
        progress.update(task4, description="Database schema extracted")

        # Backend docs via LLM summarization
        task4b = progress.add_task("Summarizing backend files (LLM)...", total=None)
        project_name = project or settings.default_project_name
        all_artifacts['backend_docs'] = extractors['backend_docs'].extract_backend_docs(
            discovered_files, project_name
        )
        progress.update(task4b, description="Backend summaries extracted")
        
        # Frontend extraction
        if include_frontend:
            task5 = progress.add_task("Extracting GWT modules...", total=None)
            if 'gwt' in discovered_files:
                all_artifacts['gwt_modules'] = extractors['gwt_modules'].extract_modules(
                    list(discovered_files['gwt'])
                )
            progress.update(task5, description="GWT modules extracted")
            
            task6 = progress.add_task("Extracting GWT client code...", total=None)
            if 'java' in discovered_files:
                gwt_client_artifacts = extractors['gwt_activities_places'].extract_client_artifacts(
                    list(discovered_files['java'])
                )
                all_artifacts['gwt_activities_places'] = gwt_client_artifacts.get('activities_places', [])
                all_artifacts['gwt_endpoints'] = gwt_client_artifacts.get('endpoints', [])
            progress.update(task6, description="GWT client code extracted")
            
            task7 = progress.add_task("Extracting UiBinder files...", total=None)
            if 'gwt' in discovered_files:
                ui_xml_files = [f for f in discovered_files['gwt'] if f.endswith('.ui.xml')]
                all_artifacts['gwt_uibinder'] = extractors['gwt_uibinder'].extract_uibinder_files(ui_xml_files)
            progress.update(task7, description="UiBinder files extracted")
            
            task8 = progress.add_task("Extracting JavaScript artifacts...", total=None)
            if 'js' in discovered_files:
                all_artifacts['js_artifacts'] = extractors['js_artifacts'].extract_js_artifacts(
                    list(discovered_files['js'])
                )
            progress.update(task8, description="JavaScript artifacts extracted")
    
    # Display results
    table = Table(title="Extraction Results")
    table.add_column("Artifact Type", style="cyan")
    table.add_column("Count", style="magenta")
    
    total_artifacts = 0
    for artifact_type, artifacts in all_artifacts.items():
        if artifacts:
            table.add_row(artifact_type.replace('_', ' ').title(), str(len(artifacts)))
            total_artifacts += len(artifacts)
    
    console.print(table)
    console.print(f"[bold green]Total artifacts extracted: {total_artifacts}[/bold green]")

@cli.command()
@click.option('--project', '-p', default=None, help='Project name')
def index(project: Optional[str]):
    """Index artifacts in Weaviate"""
    console.print("[bold blue]Indexing artifacts in Weaviate...[/bold blue]")
    
    try:
        # Initialize Weaviate client
        weaviate_client = WeaviateClient()
        
        # Load artifacts from build directory
        build_dir = settings.build_dir
        all_artifacts = {}
        
        # Load all artifact JSON files
        artifact_files = {
            'ibatis_statements': 'all_statements.json',
            'dao_calls': 'all_dao_calls.json', 
            'jsp_forms': 'all_forms.json',
            'db_tables': 'all_tables.json',
            'gwt_modules': 'all_modules.json',
            'gwt_uibinder': 'all_uibinder.json',
            'gwt_client': 'all_artifacts.json',
            'js_artifacts': 'all_js_artifacts.json',
            'backend_docs': 'all_backend_docs.json'
        }
        
        for artifact_type, filename in artifact_files.items():
            artifact_file = build_dir / artifact_type / filename
            if artifact_file.exists():
                import json
                with open(artifact_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Handle different data structures
                    if isinstance(data, dict) and artifact_type == 'gwt_client':
                        # For gwt_client, extract the arrays from the dict
                        all_artifacts[artifact_type] = []
                        for key, value in data.items():
                            if isinstance(value, list):
                                all_artifacts[artifact_type].extend(value)
                    else:
                        all_artifacts[artifact_type] = data
        
        # Index artifacts
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            total_indexed = 0
            for artifact_type, artifacts in all_artifacts.items():
                if artifacts:
                    task = progress.add_task(f"Indexing {artifact_type}...", total=len(artifacts))
                    
                    for artifact in artifacts:
                        try:
                            # Ensure project is set consistently
                            artifact_project = project or settings.default_project_name
                            artifact['project'] = artifact_project
                            # Map artifact types to Weaviate class names
                            class_mapping = {
                                'ibatis_statements': 'IbatisStatement',
                                'dao_calls': 'DaoCall',
                                'jsp_forms': 'JspForm', 
                                'db_tables': 'DbTable',
                                'gwt_modules': 'GwtModule',
                                'gwt_uibinder': 'GwtUiBinder',
                                'gwt_client': 'GwtActivityPlace',  # Map client artifacts to ActivityPlace
                                'js_artifacts': 'JsArtifact',
                                'backend_docs': 'BackendDoc'
                            }
                            
                            class_name = class_mapping.get(artifact_type, artifact_type)
                            weaviate_client.index_artifact(class_name, artifact)
                            total_indexed += 1
                            progress.advance(task)
                        except Exception as e:
                            logger.error(f"Failed to index {artifact_type} artifact: {e}")
                    
                    progress.update(task, description=f"{artifact_type} indexed")
        
        console.print(f"[bold green]Indexed {total_indexed} artifacts in Weaviate[/bold green]")
        
    except Exception as e:
        console.print(f"[bold red]Failed to index artifacts: {e}[/bold red]")
        sys.exit(1)

@cli.command()
@click.option('--query', '-q', required=True, help='Search query')
@click.option('--project', '-p', default=None, help='Project name')
@click.option('--frontend', is_flag=True, help='Include frontend artifacts in search')
@click.option('--limit', '-l', default=10, help='Maximum number of results')
def search(query: str, project: Optional[str], frontend: bool, limit: int):
    """Search artifacts in Weaviate"""
    console.print(f"[bold blue]Searching for: {query}[/bold blue]")
    
    try:
        weaviate_client = WeaviateClient(ensure_schema=False)
        
        # Define search classes
        search_classes = ['IbatisStatement', 'DaoCall', 'JspForm', 'DbTable', 'BackendDoc']
        if frontend:
            search_classes.extend(['GwtModule', 'GwtUiBinder', 'GwtActivityPlace', 'GwtEndpoint', 'JsArtifact'])
        
        # Search each class
        all_results = []
        for class_name in search_classes:
            results = weaviate_client.search_artifacts(class_name, query, project, limit)
            for result in results:
                result['class'] = class_name
                all_results.append(result)
        
        # Display results
        if all_results:
            table = Table(title=f"Search Results for: {query}")
            table.add_column("Class", style="cyan")
            table.add_column("Text", style="green")
            table.add_column("Path", style="yellow")
            
            for result in all_results[:limit]:
                text = result.get('text', 'No text')[:100] + "..." if len(result.get('text', '')) > 100 else result.get('text', 'No text')
                path = result.get('path', 'Unknown')
                table.add_row(result.get('class', 'Unknown'), text, path)
            
            console.print(table)
        else:
            console.print("[yellow]No results found[/yellow]")
    
    except Exception as e:
        console.print(f"[bold red]Search failed: {e}[/bold red]")
        sys.exit(1)

@cli.command(name="backend-search")
@click.option('--query', '-q', required=True, help='Search query (look in BackendDoc summary/text)')
@click.option('--project', '-p', default=None, help='Project name')
@click.option('--limit', '-l', default=10, help='Maximum number of results')
def backend_search(query: str, project: Optional[str], limit: int):
    """Search only BackendDoc with fallback matching on summary and text, printing path + snippet."""
    console.print(f"[bold blue]BackendDoc search for: {query}[/bold blue]")
    try:
        weaviate_client = WeaviateClient(ensure_schema=False)
        results = weaviate_client.search_artifacts('BackendDoc', query, project, limit)

        if results:
            table = Table(title=f"BackendDoc Results for: {query}")
            table.add_column("Path", style="yellow")
            table.add_column("Snippet", style="green")

            for r in results[:limit]:
                path = r.get('path', 'Unknown')
                # prefer summary, fallback to text
                snippet = r.get('summary') or r.get('text') or ''
                snippet = (snippet[:140] + '...') if len(snippet) > 140 else snippet
                table.add_row(path, snippet)

            console.print(table)
        else:
            console.print("[yellow]No BackendDoc results found[/yellow]")

    except Exception as e:
        console.print(f"[bold red]BackendDoc search failed: {e}[/bold red]")
        sys.exit(1)

@cli.command()
@click.option('--project', '-p', default=None, help='Project name')
@click.option('--frontend', is_flag=True, help='Include frontend analysis in PRD')
def prd(project: Optional[str], frontend: bool):
    """Generate PRD from indexed artifacts"""
    console.print("[bold blue]Generating PRD...[/bold blue]")
    
    try:
        # Load artifacts from build directory
        build_dir = settings.build_dir
        all_artifacts = {}
        
        # Load all artifact JSON files
        for artifact_type in ['ibatis_statements', 'dao_calls', 'jsp_forms', 'db_tables']:
            artifact_file = build_dir / artifact_type / "all_artifacts.json"
            if artifact_file.exists():
                import json
                with open(artifact_file, 'r', encoding='utf-8') as f:
                    all_artifacts[artifact_type] = json.load(f)
        
        if frontend:
            for artifact_type in ['gwt_modules', 'gwt_activities_places', 'gwt_uibinder', 
                                 'gwt_endpoints', 'js_artifacts']:
                artifact_file = build_dir / artifact_type / "all_artifacts.json"
                if artifact_file.exists():
                    import json
                    with open(artifact_file, 'r', encoding='utf-8') as f:
                        all_artifacts[artifact_type] = json.load(f)
        
        # Generate PRD
        prd_generator = PRDMarkdownGenerator()
        project_name = project or settings.default_project_name
        prd_file = prd_generator.generate_prd(all_artifacts, project_name)
        
        console.print(f"[bold green]PRD generated: {prd_file}[/bold green]")
    
    except Exception as e:
        console.print(f"[bold red]PRD generation failed: {e}[/bold red]")
        sys.exit(1)

@cli.command()
def schema():
    """Ensure Weaviate schema is created"""
    console.print("[bold blue]Ensuring Weaviate schema...[/bold blue]")
    
    try:
        weaviate_client = WeaviateClient()
        console.print("[bold green]Weaviate schema ensured[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Schema creation failed: {e}[/bold red]")
        sys.exit(1)

@cli.command()
@click.option('--project', '-p', default=None, help='Project name')
@click.option('--include-frontend', is_flag=True, help='Include frontend extraction')
def all(project: Optional[str], include_frontend: bool):
    """Run the complete pipeline: discover → extract → index → prd"""
    console.print("[bold blue]Running complete pipeline...[/bold blue]")
    
    # Run all steps
    ctx = click.Context(cli)
    
    # Discover
    ctx.invoke(discover, project=project, include_frontend=include_frontend)
    
    # Extract
    ctx.invoke(extract, project=project, include_frontend=include_frontend)
    
    # Index
    ctx.invoke(index, project=project)
    
    # Generate PRD
    ctx.invoke(prd, project=project, frontend=include_frontend)
    
    console.print("[bold green]Complete pipeline finished![/bold green]")

if __name__ == '__main__':
    cli()
