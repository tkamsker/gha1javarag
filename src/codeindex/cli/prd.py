"""
PRD Generation CLI command.

Implements the `codeindex prd` command for generating Product Requirements
Documents from indexed codebase artifacts.
"""

import logging
from pathlib import Path
from typing import Optional

import click

from codeindex.utils.logging import get_logger
from codeindex.utils.config import get_config
from codeindex.services.weaviate_store import WeaviateStore
from codeindex.services.ollama_client import OllamaClient
from codeindex.schemas import check_weaviate_health

logger = get_logger(__name__)


# Exit codes per contracts/cli-interface.md
EXIT_SUCCESS = 0
EXIT_GENERAL_ERROR = 1
EXIT_INVALID_ARGUMENTS = 2
EXIT_SOURCE_DIR_NOT_FOUND = 3
EXIT_PROJECT_NOT_FOUND = 4
EXIT_OUTPUT_DIR_ERROR = 5
EXIT_WEAVIATE_CONNECTION_ERROR = 6
EXIT_OLLAMA_CONNECTION_ERROR = 7
EXIT_LLM_ANALYSIS_FAILED = 8
EXIT_PARTIAL_SUCCESS = 9
EXIT_NO_ARTIFACTS_FOUND = 10


@click.command(name='prd')
@click.argument(
    'layer',
    type=click.Choice(['database', 'services', 'frontend', 'full'], case_sensitive=False),
    default='full',
    required=False
)
@click.option(
    '--project',
    '-p',
    type=str,
    help='Project name/ID to analyze (filters CodeArtifacts in Weaviate)'
)
@click.option(
    '--source-dir',
    '-s',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    help='Root directory of source code (overrides JAVA_SOURCE_DIR)'
)
@click.option(
    '--output-dir',
    '-o',
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    default=Path('./output'),
    help='Output directory for generated PRD documents (default: ./output)'
)
@click.option(
    '--force-refresh',
    '-f',
    is_flag=True,
    help='Re-analyze all files even if unchanged (ignore visit log)'
)
@click.option(
    '--parallel',
    '-j',
    type=int,
    default=10,
    help='Number of parallel LLM analysis tasks (default: 10)'
)
@click.option(
    '--verbose',
    '-v',
    is_flag=True,
    help='Enable verbose logging (DEBUG level)'
)
@click.option(
    '--quiet',
    '-q',
    is_flag=True,
    help='Suppress progress output (only errors/warnings)'
)
# Layer-specific options
@click.option(
    '--skip-database',
    is_flag=True,
    help='Skip database layer analysis (only with full layer)'
)
@click.option(
    '--skip-services',
    is_flag=True,
    help='Skip service layer analysis (only with full layer)'
)
@click.option(
    '--skip-frontend',
    is_flag=True,
    help='Skip frontend layer analysis (only with full layer)'
)
# LLM configuration options
@click.option(
    '--llm-timeout',
    type=int,
    default=120,
    help='Timeout for each LLM call in seconds (default: 120)'
)
@click.option(
    '--llm-retries',
    type=int,
    default=3,
    help='Maximum retry attempts for failed LLM calls (default: 3)'
)
@click.option(
    '--llm-model',
    type=str,
    help='Ollama model to use (default: from OLLAMA_MODEL_NAME env var)'
)
# Output format options
@click.option(
    '--format',
    type=click.Choice(['markdown', 'json', 'both'], case_sensitive=False),
    default='markdown',
    help='Output format for PRD documents (default: markdown)'
)
@click.option(
    '--include-html',
    is_flag=True,
    help='Also generate HTML versions of markdown files'
)
@click.option(
    '--include-diagrams',
    is_flag=True,
    help='Generate Mermaid diagrams for ERD and architecture'
)
# Filtering options
@click.option(
    '--domain-filter',
    type=str,
    help='Only analyze entities in specified domain (e.g., auth, billing)'
)
@click.option(
    '--include-tests',
    is_flag=True,
    help='Include test files in analysis'
)
@click.option(
    '--exclude-generated',
    is_flag=True,
    default=True,
    help='Exclude auto-generated code from analysis (default: true)'
)
# Progress reporting options
@click.option(
    '--progress-interval',
    type=int,
    default=10,
    help='Progress report frequency in seconds (default: 10)'
)
@click.option(
    '--show-current-file',
    is_flag=True,
    default=True,
    help='Display currently analyzed file in progress output (default: true)'
)
@click.pass_context
def prd_command(
    ctx,
    layer: str,
    project: Optional[str],
    source_dir: Optional[Path],
    output_dir: Path,
    force_refresh: bool,
    parallel: int,
    verbose: bool,
    quiet: bool,
    skip_database: bool,
    skip_services: bool,
    skip_frontend: bool,
    llm_timeout: int,
    llm_retries: int,
    llm_model: Optional[str],
    format: str,
    include_html: bool,
    include_diagrams: bool,
    domain_filter: Optional[str],
    include_tests: bool,
    exclude_generated: bool,
    progress_interval: int,
    show_current_file: bool
):
    """
    Generate Product Requirements Documents from indexed codebase artifacts.

    Analyzes codebase layers (database, services, frontend) and generates
    comprehensive PRD documentation with business rules, API endpoints,
    data schemas, and UI components.

    LAYER: Specific layer to analyze (database|services|frontend|full)
           Default: full (analyze all layers)

    Examples:

        # Generate full PRD for a project
        codeindex prd --project myapp --output-dir ./docs/myapp-prd

        # Analyze only database layer
        codeindex prd database --project myapp

        # Analyze with custom LLM settings
        codeindex prd services --llm-timeout 180 --llm-retries 5

        # Force refresh all files
        codeindex prd --force-refresh --project myapp

        # Analyze specific domain only
        codeindex prd --domain-filter auth --project myapp

        # Generate with HTML and diagrams
        codeindex prd full --include-html --include-diagrams --project myapp

        # Quiet mode for automation
        codeindex prd --quiet --project myapp
    """
    cli_context = ctx.obj
    config = cli_context.config

    # Override config with CLI options
    if source_dir:
        config.java_source_dir = source_dir
    if llm_model:
        config.ollama_model_name = llm_model
    if parallel:
        config.max_concurrent_ai_calls = parallel

    # Enable verbose logging if requested
    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")

    # Validate arguments
    exit_code = _validate_arguments(
        ctx,
        layer,
        source_dir or config.java_source_dir,
        output_dir,
        skip_database,
        skip_services,
        skip_frontend,
        quiet
    )
    if exit_code != EXIT_SUCCESS:
        ctx.exit(exit_code)

    # Check service health
    exit_code = _check_service_health(ctx, config, quiet)
    if exit_code != EXIT_SUCCESS:
        ctx.exit(exit_code)

    # Verify project exists if specified
    if project:
        exit_code = _verify_project_exists(ctx, config, project, quiet)
        if exit_code != EXIT_SUCCESS:
            ctx.exit(exit_code)

    # Show configuration (unless quiet)
    if not quiet:
        _print_configuration(
            layer,
            project,
            source_dir or config.java_source_dir,
            output_dir,
            force_refresh,
            parallel,
            llm_timeout,
            llm_retries,
            format,
            domain_filter
        )

    # TODO: Implement PRD generation pipeline
    # This is Phase 2 skeleton - actual implementation in Phase 3-5
    if not quiet:
        click.echo("\n[INFO] PRD generation command skeleton initialized successfully")
        click.echo("[INFO] Full implementation pending (Phase 3-5: US1-US4)")
        click.echo(f"[INFO] Layer: {layer}")
        click.echo(f"[INFO] Output directory: {output_dir}")

    logger.info(f"PRD command invoked: layer={layer}, project={project}, output_dir={output_dir}")
    ctx.exit(EXIT_SUCCESS)


def _validate_arguments(
    ctx,
    layer: str,
    source_dir: Path,
    output_dir: Path,
    skip_database: bool,
    skip_services: bool,
    skip_frontend: bool,
    quiet: bool
) -> int:
    """
    Validate CLI arguments.

    Args:
        ctx: Click context
        layer: Analysis layer
        source_dir: Source directory
        output_dir: Output directory
        skip_database: Skip database layer
        skip_services: Skip services layer
        skip_frontend: Skip frontend layer
        quiet: Quiet mode

    Returns:
        Exit code (0 for success, error code otherwise)
    """
    # Check source directory exists
    if not source_dir:
        if not quiet:
            click.echo("Error: Source directory not specified. Set JAVA_SOURCE_DIR or use --source-dir", err=True)
        logger.error("Source directory not specified")
        return EXIT_INVALID_ARGUMENTS

    if not source_dir.exists():
        if not quiet:
            click.echo(f"Error: Source directory does not exist: {source_dir}", err=True)
        logger.error(f"Source directory not found: {source_dir}")
        return EXIT_SOURCE_DIR_NOT_FOUND

    # Check output directory is writable
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        # Try writing a test file
        test_file = output_dir / ".write_test"
        test_file.touch()
        test_file.unlink()
    except Exception as e:
        if not quiet:
            click.echo(f"Error: Cannot write to output directory: {output_dir} - {e}", err=True)
        logger.error(f"Output directory not writable: {output_dir} - {e}")
        return EXIT_OUTPUT_DIR_ERROR

    # Validate skip flags only apply to 'full' layer
    if layer != 'full' and (skip_database or skip_services or skip_frontend):
        if not quiet:
            click.echo("Error: --skip-* options only valid with 'full' layer", err=True)
        logger.error("Skip flags used with non-full layer")
        return EXIT_INVALID_ARGUMENTS

    return EXIT_SUCCESS


def _check_service_health(ctx, config, quiet: bool) -> int:
    """
    Check health of Weaviate and Ollama services.

    Args:
        ctx: Click context
        config: Configuration object
        quiet: Quiet mode

    Returns:
        Exit code (0 for success, error code otherwise)
    """
    # Check Weaviate
    try:
        check_weaviate_health(config.weaviate_url)
    except ConnectionError as e:
        if not quiet:
            click.echo(f"Error: Cannot connect to Weaviate at {config.weaviate_url}", err=True)
            click.echo(f"  {e}", err=True)
            click.echo("  Run './docker-weaviate.sh status' to check service.", err=True)
        logger.error(f"Weaviate connection failed: {e}")
        return EXIT_WEAVIATE_CONNECTION_ERROR

    # Check Ollama
    try:
        import httpx
        response = httpx.get(f"{config.ollama_base_url}/api/tags", timeout=5.0)
        if response.status_code != 200:
            raise ConnectionError(f"HTTP {response.status_code}")
    except Exception as e:
        if not quiet:
            click.echo(f"Error: Cannot connect to Ollama at {config.ollama_base_url}", err=True)
            click.echo(f"  {e}", err=True)
            click.echo("  Run 'ollama serve' to start Ollama service.", err=True)
        logger.error(f"Ollama connection failed: {e}")
        return EXIT_OLLAMA_CONNECTION_ERROR

    return EXIT_SUCCESS


def _verify_project_exists(ctx, config, project: str, quiet: bool) -> int:
    """
    Verify project exists in Weaviate.

    Args:
        ctx: Click context
        config: Configuration object
        project: Project ID
        quiet: Quiet mode

    Returns:
        Exit code (0 for success, error code otherwise)
    """
    try:
        store = WeaviateStore(config=config)

        # Query for any artifact with this project ID
        # TODO: Implement proper project existence check
        # For now, just succeed (will be implemented in Phase 3)

        return EXIT_SUCCESS

    except Exception as e:
        if not quiet:
            click.echo(f"Error: Failed to verify project '{project}' in Weaviate", err=True)
            click.echo(f"  {e}", err=True)
        logger.error(f"Project verification failed: {e}")
        return EXIT_WEAVIATE_CONNECTION_ERROR


def _print_configuration(
    layer: str,
    project: Optional[str],
    source_dir: Path,
    output_dir: Path,
    force_refresh: bool,
    parallel: int,
    llm_timeout: int,
    llm_retries: int,
    format: str,
    domain_filter: Optional[str]
):
    """
    Print configuration summary.

    Args:
        layer: Analysis layer
        project: Project ID
        source_dir: Source directory
        output_dir: Output directory
        force_refresh: Force refresh flag
        parallel: Parallel workers
        llm_timeout: LLM timeout
        llm_retries: LLM retries
        format: Output format
        domain_filter: Domain filter
    """
    click.echo("="*60)
    click.echo("PRD Generation Configuration")
    click.echo("="*60)
    click.echo(f"Layer:         {layer}")
    if project:
        click.echo(f"Project:       {project}")
    click.echo(f"Source Dir:    {source_dir}")
    click.echo(f"Output Dir:    {output_dir}")
    click.echo(f"Format:        {format}")
    if domain_filter:
        click.echo(f"Domain Filter: {domain_filter}")
    click.echo(f"Force Refresh: {force_refresh}")
    click.echo(f"Parallel:      {parallel} workers")
    click.echo(f"LLM Timeout:   {llm_timeout}s")
    click.echo(f"LLM Retries:   {llm_retries}")
    click.echo("="*60)
    click.echo()
