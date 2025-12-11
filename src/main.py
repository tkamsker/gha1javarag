import click
import os
import pickle
from dotenv import load_dotenv
from src.discovery.discover_files import discover_files
from src.extraction.extract_artifacts import extract_artifacts
from src.indexing.index_artifacts import index_artifacts, get_weaviate_client
from src.search.search_artifacts import search_artifacts
from src.prd.generate_prd import generate_prd
from src.common.logging import setup_logging, get_logger

load_dotenv()
logger = get_logger(__name__)

@click.group()
def cli():
    """
    GEMINI is a CLI tool for analyzing Java/JSP/GWT/JavaScript codebases
    and generating Product Requirements Documents (PRDs).
    """
    setup_logging()
    pass

@cli.command()
@click.option('--project', required=True, help='The name of the project to analyze.')
def discover(project):
    """Discover files in the source directory."""
    source_dir = os.environ.get("JAVA_SOURCE_DIR")
    if not source_dir:
        logger.error("JAVA_SOURCE_DIR environment variable not set.")
        click.echo("Error: JAVA_SOURCE_DIR environment variable not set.", err=True)
        return

    logger.info(f"Starting file discovery for project: {project} in {source_dir}")
    discovered_files = discover_files(project, source_dir)
    with open(f"{project}_discovered_files.pkl", "wb") as f:
        pickle.dump(discovered_files, f)
    logger.info(f"Discovered {len(discovered_files)} files and saved to {project}_discovered_files.pkl")
    click.echo(f"Discovered {len(discovered_files)} files and saved to {project}_discovered_files.pkl")

@cli.command()
@click.option('--project', required=True, help='The name of the project to analyze.')
@click.option('--include-frontend', is_flag=True, help='Include frontend artifacts in the analysis.')
def extract(project, include_frontend):
    """Extract artifacts from discovered files."""
    logger.info(f"Starting artifact extraction for project: {project}")
    try:
        with open(f"{project}_discovered_files.pkl", "rb") as f:
            discovered_files = pickle.load(f)
    except FileNotFoundError:
        logger.error("Discovered files not found. Please run the discover command first.")
        click.echo("Error: Discovered files not found. Please run the discover command first.", err=True)
        return

    artifacts = extract_artifacts(project, discovered_files)
    with open(f"{project}_artifacts.pkl", "wb") as f:
        pickle.dump(artifacts, f)
    logger.info(f"Extracted {len(artifacts)} artifacts and saved to {project}_artifacts.pkl")
    click.echo(f"Extracted {len(artifacts)} artifacts and saved to {project}_artifacts.pkl")

@cli.command()
@click.option('--project', required=True, help='The name of the project to analyze.')
def index(project):
    """Index artifacts into Weaviate."""
    logger.info(f"Starting artifact indexing for project: {project}")
    try:
        with open(f"{project}_artifacts.pkl", "rb") as f:
            artifacts = pickle.load(f)
    except FileNotFoundError:
        logger.error("Artifacts not found. Please run the extract command first.")
        click.echo("Error: Artifacts not found. Please run the extract command first.", err=True)
        return
    
    client = get_weaviate_client()
    index_artifacts(project, artifacts, client)
    logger.info(f"Indexed {len(artifacts)} artifacts into Weaviate for project {project}.")
    click.echo(f"Indexed {len(artifacts)} artifacts into Weaviate for project {project}.")
    client.close()

@cli.command()
@click.option('--project', required=True, help='The name of the project to analyze.')
@click.option('--query', required=True, help='The natural language query.')
def search(project, query):
    """Search for artifacts using natural language."""
    logger.info(f"Starting artifact search for project: {project} with query: '{query}'")
    client = get_weaviate_client()
    results = search_artifacts(project, query, client)
    logger.info(f"Found {len(results)} relevant artifacts for query: '{query}'")
    click.echo(f"Found {len(results)} relevant artifacts for query: '{query}'")
    for artifact in results:
        click.echo(f"- ID: {artifact.id}, Type: {artifact.artifact_type}, Path: {artifact.file_path}")
    client.close()

@cli.command()
@click.option('--project', required=True, help='The name of the project to analyze.')
@click.option('--frontend', is_flag=True, help='Generate PRD for frontend artifacts only.')
@click.option('--include-frontend', is_flag=True, help='Include frontend artifacts in the generated PRD.')
def prd(project, frontend, include_frontend):
    """Generate a Product Requirements Document (PRD)."""
    logger.info(f"Starting PRD generation for project: {project}")
    try:
        with open(f"{project}_artifacts.pkl", "rb") as f:
            artifacts = pickle.load(f)
    except FileNotFoundError:
        logger.error("Artifacts not found. Please run the extract command first.")
        click.echo("Error: Artifacts not found. Please run the extract command first.", err=True)
        return

    output_dir = "output/prd"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{project}_prd.md")

    generate_prd(project, artifacts, output_file, frontend, include_frontend)
    logger.info(f"Generated PRD for project {project} at {output_file}")
    click.echo(f"Generated PRD for project {project} at {output_file}")

@cli.command()
@click.option('--project', required=True, help='The name of the project to analyze.')
@click.option('--include-frontend', is_flag=True, help='Include frontend artifacts in the analysis.')
@click.option('--frontend', is_flag=True, help='Generate PRD for frontend artifacts only.')
@click.pass_context
def all(ctx, project, include_frontend, frontend):
    """Run the complete pipeline (discover, extract, index, prd)."""
    logger.info(f"Running complete pipeline for project: {project}")
    click.echo(f"Running complete pipeline for project: {project}")
    click.echo(f"DEBUG: 'all' command received project={project}, include_frontend={include_frontend}, frontend={frontend}")
    
    # Discover
    ctx.invoke(discover, project=project)

    # Extract
    ctx.invoke(extract, project=project, include_frontend=include_frontend)

    # Index
    ctx.invoke(index, project=project)

    # PRD Generation
    ctx.invoke(prd, project=project, frontend=frontend, include_frontend=include_frontend)

    logger.info(f"Complete pipeline finished for project: {project}")
    click.echo(f"Complete pipeline finished for project: {project}")

if __name__ == '__main__':
    cli()
