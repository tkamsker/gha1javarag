"""
PRD Generation CLI command.

Implements the `codeindex prd` command for generating Product Requirements
Documents from indexed codebase artifacts.
"""

import logging
import json
from pathlib import Path
from typing import Optional

import click

from codeindex.utils.logging import get_logger
from codeindex.utils.config import get_config
from codeindex.services.weaviate_store import WeaviateStore
from codeindex.services.ollama_client import OllamaClient
from codeindex.services.db_analyzer import DatabaseAnalyzer
from codeindex.services.service_analyzer import ServiceAnalyzer
from codeindex.services.frontend_analyzer import FrontendAnalyzer
from codeindex.services.markdown_builder import MarkdownBuilder
from codeindex.models.prd import AnalysisLayer, ServiceDefinition, APIEndpoint, FormDefinition, UIComponent
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

    # Note: CLI options are used directly in function calls below
    # Config properties are read-only and cannot be overridden

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

    # Initialize Ollama client
    try:
        ollama_client = OllamaClient(
            base_url=config.ollama_base_url,
            model=llm_model or config.ollama_model_name,
            max_retries=llm_retries
        )
    except Exception as e:
        if not quiet:
            click.echo(f"Error: Failed to initialize Ollama client - {e}", err=True)
        logger.error(f"Ollama client initialization failed: {e}")
        ctx.exit(EXIT_OLLAMA_CONNECTION_ERROR)

    # Track analysis results
    analysis_results = {
        "database": None,
        "services": None,
        "frontend": None,
        "success": True,
        "partial_failures": []
    }

    # Start PRD generation
    if not quiet:
        click.echo("\n" + "="*60)
        click.echo("Starting PRD Generation")
        click.echo("="*60)

    # Analyze database layer
    if layer in ['database', 'full'] and not skip_database:
        result = _analyze_database_layer(
            config=config,
            ollama_client=ollama_client,
            output_dir=output_dir,
            source_dir=source_dir or config.java_source_dir,
            parallel=parallel,
            llm_timeout=llm_timeout,
            llm_retries=llm_retries,
            force_refresh=force_refresh,
            quiet=quiet
        )
        analysis_results["database"] = result
        if not result.get("success", False):
            analysis_results["partial_failures"].append("database")

    # Analyze service layer
    if layer in ['services', 'full'] and not skip_services:
        result = _analyze_service_layer(
            config=config,
            ollama_client=ollama_client,
            output_dir=output_dir,
            source_dir=source_dir or config.java_source_dir,
            parallel=parallel,
            llm_timeout=llm_timeout,
            llm_retries=llm_retries,
            force_refresh=force_refresh,
            quiet=quiet
        )
        analysis_results["services"] = result
        if not result.get("success", False):
            analysis_results["partial_failures"].append("services")

    # Analyze frontend layer
    if layer in ['frontend', 'full'] and not skip_frontend:
        result = _analyze_frontend_layer(
            config=config,
            ollama_client=ollama_client,
            output_dir=output_dir,
            source_dir=source_dir or config.java_source_dir,
            parallel=parallel,
            llm_timeout=llm_timeout,
            llm_retries=llm_retries,
            force_refresh=force_refresh,
            quiet=quiet
        )
        analysis_results["frontend"] = result
        if not result.get("success", False):
            analysis_results["partial_failures"].append("frontend")

    # Generate final PRD documents
    if layer == 'full':
        if not quiet:
            click.echo("\n[INFO] Generating master PRD document...")
        # TODO: Implement master PRD generation (Phase 4-5)

    # Print final summary
    if not quiet:
        click.echo("\n" + "="*60)
        click.echo("PRD Generation Complete")
        click.echo("="*60)
        _print_final_summary(analysis_results, output_dir)

    logger.info(f"PRD generation complete: layer={layer}, output_dir={output_dir}")

    # Determine exit code
    if analysis_results["partial_failures"]:
        ctx.exit(EXIT_PARTIAL_SUCCESS)
    else:
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


def _analyze_database_layer(
    config,
    ollama_client: OllamaClient,
    output_dir: Path,
    source_dir: Path,
    parallel: int,
    llm_timeout: int,
    llm_retries: int,
    force_refresh: bool,
    quiet: bool
) -> dict:
    """
    Analyze database layer.

    Args:
        config: Configuration object
        ollama_client: Ollama client
        output_dir: Output directory
        source_dir: Source directory
        parallel: Parallel workers
        llm_timeout: LLM timeout
        llm_retries: LLM retries
        force_refresh: Force refresh
        quiet: Quiet mode

    Returns:
        Analysis result dict
    """
    if not quiet:
        click.echo("\n[INFO] Analyzing database layer...")

    try:
        analyzer = DatabaseAnalyzer(
            ollama_client=ollama_client,
            output_dir=output_dir,
            source_dir=source_dir,
            max_workers=parallel,
            llm_timeout=llm_timeout,
            max_retries=llm_retries,
            force_refresh=force_refresh
        )

        # Run analysis
        result = analyzer.analyze_database_layer()

        # Generate index.md
        if not quiet:
            click.echo("[INFO] Generating database index...")

        index_content = MarkdownBuilder.build_index_markdown(
            entities=analyzer.extracted_entities,
            layer=AnalysisLayer.DATABASE,
            project=None
        )

        index_file = output_dir / "database" / "index.md"
        index_file.parent.mkdir(parents=True, exist_ok=True)
        index_file.write_text(index_content, encoding="utf-8")

        # Generate database PRD
        if not quiet:
            click.echo("[INFO] Generating database PRD...")

        prd_content = _generate_database_prd(analyzer.extracted_entities, analyzer.extracted_rules)
        prd_file = output_dir / "prd" / "database_prd.md"
        prd_file.parent.mkdir(parents=True, exist_ok=True)
        prd_file.write_text(prd_content, encoding="utf-8")

        if not quiet:
            click.echo(f"[INFO] Database analysis complete: {result['entities']} entities, {result['rules']} rules")

        return {
            "success": True,
            "entities": result.get("entities", 0),
            "rules": result.get("rules", 0),
            "analyzed": result.get("analyzed", 0),
            "skipped": result.get("skipped", 0),
            "failed": result.get("failed", 0)
        }

    except Exception as e:
        logger.error(f"Database layer analysis failed: {e}", exc_info=True)
        if not quiet:
            click.echo(f"[ERROR] Database layer analysis failed: {e}", err=True)

        return {
            "success": False,
            "error": str(e)
        }


def _analyze_service_layer(
    config,
    ollama_client: OllamaClient,
    output_dir: Path,
    source_dir: Path,
    parallel: int,
    llm_timeout: int,
    llm_retries: int,
    force_refresh: bool,
    quiet: bool
) -> dict:
    """
    Analyze service layer.

    Args:
        config: Configuration object
        ollama_client: Ollama client
        output_dir: Output directory
        source_dir: Source directory
        parallel: Parallel workers
        llm_timeout: LLM timeout
        llm_retries: LLM retries
        force_refresh: Force refresh
        quiet: Quiet mode

    Returns:
        Analysis result dict
    """
    if not quiet:
        click.echo("\n[INFO] Analyzing service layer...")

    try:
        analyzer = ServiceAnalyzer(
            ollama_client=ollama_client,
            output_dir=output_dir,
            source_dir=source_dir,
            max_workers=parallel,
            llm_timeout=llm_timeout,
            max_retries=llm_retries,
            force_refresh=force_refresh
        )

        # Run analysis
        result = analyzer.analyze_service_layer()

        # Load extracted services and endpoints from output files
        services = []
        endpoints = []

        # Load services from JSON files
        services_dir = output_dir / "services" / "definitions"
        if services_dir.exists():
            for service_file in services_dir.glob("*.json"):
                try:
                    with open(service_file, "r", encoding="utf-8") as f:
                        service_data = json.load(f)
                        services.append(ServiceDefinition.from_dict(service_data))
                except Exception as e:
                    logger.warning(f"Failed to load service from {service_file}: {e}")

        # Load endpoints from JSON files
        endpoints_dir = output_dir / "services" / "endpoints"
        if endpoints_dir.exists():
            for endpoint_file in endpoints_dir.glob("*.json"):
                try:
                    with open(endpoint_file, "r", encoding="utf-8") as f:
                        endpoint_data = json.load(f)
                        endpoints.append(APIEndpoint.from_dict(endpoint_data))
                except Exception as e:
                    logger.warning(f"Failed to load endpoint from {endpoint_file}: {e}")

        # Generate index.md
        if not quiet:
            click.echo("[INFO] Generating service index...")

        index_content = MarkdownBuilder.build_index_markdown(
            entities=services,
            layer=AnalysisLayer.SERVICE,
            project=None
        )

        index_file = output_dir / "services" / "index.md"
        index_file.parent.mkdir(parents=True, exist_ok=True)
        index_file.write_text(index_content, encoding="utf-8")

        # Generate service PRD
        if not quiet:
            click.echo("[INFO] Generating service PRD...")

        prd_content = _generate_service_prd(services, endpoints)
        prd_file = output_dir / "prd" / "service_prd.md"
        prd_file.parent.mkdir(parents=True, exist_ok=True)
        prd_file.write_text(prd_content, encoding="utf-8")

        if not quiet:
            click.echo(f"[INFO] Service analysis complete: {result.get('services_extracted', 0)} services, {result.get('endpoints_found', 0)} endpoints")

        return {
            "success": True,
            "services": result.get("services_extracted", 0),
            "endpoints": result.get("endpoints_found", 0),
            "analyzed": result.get("analyzed", 0),
            "skipped": result.get("skipped", 0),
            "failed": result.get("failed", 0)
        }

    except Exception as e:
        logger.error(f"Service layer analysis failed: {e}", exc_info=True)
        if not quiet:
            click.echo(f"[ERROR] Service layer analysis failed: {e}", err=True)

        return {
            "success": False,
            "error": str(e)
        }


def _analyze_frontend_layer(
    config,
    ollama_client: OllamaClient,
    output_dir: Path,
    source_dir: Path,
    parallel: int,
    llm_timeout: int,
    llm_retries: int,
    force_refresh: bool,
    quiet: bool
) -> dict:
    """
    Analyze frontend layer.

    Args:
        config: Configuration object
        ollama_client: Ollama client
        output_dir: Output directory
        source_dir: Source directory
        parallel: Parallel workers
        llm_timeout: LLM timeout
        llm_retries: LLM retries
        force_refresh: Force refresh
        quiet: Quiet mode

    Returns:
        Analysis result dict
    """
    if not quiet:
        click.echo("\n[INFO] Analyzing frontend layer...")

    try:
        analyzer = FrontendAnalyzer(
            ollama_client=ollama_client,
            output_dir=output_dir,
            source_dir=source_dir,
            max_workers=parallel,
            llm_timeout=llm_timeout,
            max_retries=llm_retries,
            force_refresh=force_refresh
        )

        # Run analysis
        result = analyzer.analyze_frontend_layer()

        # Generate index.md
        if not quiet:
            click.echo("[INFO] Generating frontend index...")

        index_content = MarkdownBuilder.build_index_markdown(
            entities=analyzer.extracted_forms,
            layer=AnalysisLayer.FRONTEND,
            project=None
        )

        index_file = output_dir / "frontend" / "index.md"
        index_file.parent.mkdir(parents=True, exist_ok=True)
        index_file.write_text(index_content, encoding="utf-8")

        # Generate frontend PRD
        if not quiet:
            click.echo("[INFO] Generating frontend PRD...")

        prd_content = _generate_frontend_prd(analyzer.extracted_forms, analyzer.extracted_components)
        prd_file = output_dir / "prd" / "frontend_prd.md"
        prd_file.parent.mkdir(parents=True, exist_ok=True)
        prd_file.write_text(prd_content, encoding="utf-8")

        if not quiet:
            click.echo(f"[INFO] Frontend analysis complete: {result['forms']} forms, {result['components']} components")

        return {
            "success": True,
            "forms": result.get("forms", 0),
            "components": result.get("components", 0),
            "analyzed": result.get("analyzed", 0),
            "skipped": result.get("skipped", 0),
            "failed": result.get("failed", 0)
        }

    except Exception as e:
        logger.error(f"Frontend layer analysis failed: {e}", exc_info=True)
        if not quiet:
            click.echo(f"[ERROR] Frontend layer analysis failed: {e}", err=True)

        return {
            "success": False,
            "error": str(e)
        }


def _generate_database_prd(entities: list, rules: list) -> str:
    """Generate comprehensive database PRD markdown."""
    from datetime import datetime

    lines = []

    # Header
    lines.append("# Database Schema Documentation")
    lines.append("")
    lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    lines.append("")

    # Table of Contents
    lines.append("## Table of Contents")
    lines.append("")
    lines.append("1. [Overview](#overview)")
    lines.append("2. [Entity Catalog](#entity-catalog)")
    lines.append("3. [Relationships](#relationships)")
    lines.append("4. [Business Rules](#business-rules)")
    lines.append("5. [Data Dictionary](#data-dictionary)")
    lines.append("")

    # Overview
    lines.append("## Overview")
    lines.append("")
    lines.append(f"This document describes the database schema with **{len(entities)} entities** and **{len(rules)} business rules**.")
    lines.append("")

    # Group entities by domain
    entities_by_domain = {}
    for entity in entities:
        domain = entity.domain or 'Uncategorized'
        if domain not in entities_by_domain:
            entities_by_domain[domain] = []
        entities_by_domain[domain].append(entity)

    lines.append("### Schema Statistics")
    lines.append("")
    lines.append(f"- **Total Entities**: {len(entities)}")
    lines.append(f"- **Total Columns**: {sum(len(e.columns) for e in entities)}")
    lines.append(f"- **Total Foreign Keys**: {sum(len(e.foreign_keys) for e in entities)}")
    lines.append(f"- **Domains**: {len(entities_by_domain)}")
    lines.append("")

    # Entity Catalog
    lines.append("## Entity Catalog")
    lines.append("")

    for domain in sorted(entities_by_domain.keys()):
        lines.append(f"### Domain: {domain}")
        lines.append("")

        for entity in sorted(entities_by_domain[domain], key=lambda e: e.name):
            lines.append(f"#### {entity.name}")
            lines.append("")

            if entity.description:
                lines.append(entity.description)
                lines.append("")

            # Entity metadata
            lines.append("**Entity Information:**")
            lines.append("")
            lines.append(f"- **Table Name**: `{entity.name}`")
            if entity.qualified_name and entity.qualified_name != entity.name:
                lines.append(f"- **Qualified Name**: `{entity.qualified_name}`")
            lines.append(f"- **Source Type**: {entity.source_type.value if entity.source_type else 'Unknown'}")
            lines.append(f"- **Primary Key**: {', '.join([f'`{pk}`' for pk in entity.primary_key]) if entity.primary_key else 'None'}")
            lines.append(f"- **Column Count**: {len(entity.columns)}")
            if entity.estimated_row_count:
                lines.append(f"- **Estimated Rows**: {entity.estimated_row_count}")
            lines.append("")

            # Columns table
            if entity.columns:
                lines.append("**Columns:**")
                lines.append("")

                headers = ["Column", "Type", "Nullable", "Default", "Constraints"]
                rows = []
                for col in entity.columns:
                    constraints = []
                    # Check if column is primary key
                    if col.name in entity.primary_key:
                        constraints.append("PK")
                    # Check if column is foreign key
                    if any(fk.column_name == col.name for fk in entity.foreign_keys):
                        constraints.append("FK")
                    # Check if column has unique index
                    if any(idx.unique and col.name in idx.columns for idx in entity.indexes):
                        constraints.append("UNIQUE")

                    rows.append([
                        f"`{col.name}`",
                        col.data_type,
                        "Yes" if col.nullable else "No",
                        col.default_value or "-",
                        ", ".join(constraints) if constraints else "-"
                    ])

                lines.append(MarkdownBuilder.format_table(headers, rows))
                lines.append("")

            # Foreign Keys
            if entity.foreign_keys:
                lines.append("**Foreign Keys:**")
                lines.append("")
                for fk in entity.foreign_keys:
                    on_actions = []
                    if fk.on_delete:
                        on_actions.append(f"ON DELETE {fk.on_delete}")
                    if fk.on_update:
                        on_actions.append(f"ON UPDATE {fk.on_update}")
                    actions_str = f" ({', '.join(on_actions)})" if on_actions else ""
                    lines.append(f"- `{fk.column_name}` → `{fk.referenced_table}`.`{fk.referenced_column}`{actions_str}")
                lines.append("")

            # Indexes
            if entity.indexes:
                lines.append("**Indexes:**")
                lines.append("")
                for idx in entity.indexes:
                    idx_cols = ", ".join([f"`{col}`" for col in idx.columns])
                    unique_str = " (UNIQUE)" if idx.unique else ""
                    type_str = f" [{idx.index_type}]" if idx.index_type else ""
                    lines.append(f"- `{idx.name}`{unique_str}{type_str}: {idx_cols}")
                lines.append("")

            # Source files
            lines.append("**Source Files:**")
            lines.append("")
            for source in entity.source_files:
                lines.append(f"- `{source}`")
            lines.append("")
            lines.append("---")
            lines.append("")

    # Relationships
    lines.append("## Relationships")
    lines.append("")
    lines.append("### Foreign Key Relationships")
    lines.append("")

    # Collect all relationships
    relationships = []
    for entity in entities:
        for fk in entity.foreign_keys:
            # Generate a descriptive name for the foreign key
            fk_name = f"fk_{entity.name}_{fk.column_name}"
            relationships.append({
                'from': entity.name,
                'to': fk.referenced_table,
                'column': fk.column_name,
                'ref_column': fk.referenced_column,
                'name': fk_name,
                'on_delete': fk.on_delete,
                'on_update': fk.on_update
            })

    if relationships:
        headers = ["From Table", "Foreign Key Column", "To Table", "Referenced Column", "Actions"]
        rows = []
        for rel in sorted(relationships, key=lambda r: (r['from'], r['to'])):
            actions = []
            if rel.get('on_delete'):
                actions.append(f"DELETE: {rel['on_delete']}")
            if rel.get('on_update'):
                actions.append(f"UPDATE: {rel['on_update']}")
            actions_str = ", ".join(actions) if actions else "-"

            rows.append([
                f"`{rel['from']}`",
                f"`{rel['column']}`",
                f"`{rel['to']}`",
                f"`{rel['ref_column']}`",
                actions_str
            ])
        lines.append(MarkdownBuilder.format_table(headers, rows))
    else:
        lines.append("*No foreign key relationships defined.*")
    lines.append("")

    # Business Rules
    lines.append("## Business Rules")
    lines.append("")

    if rules:
        for rule in sorted(rules, key=lambda r: r.name):
            lines.append(f"### {rule.name}")
            lines.append("")

            lines.append("**Rule Details:**")
            lines.append("")
            lines.append(f"- **ID**: `{rule.id}`")
            lines.append(f"- **Type**: {rule.rule_type.value if rule.rule_type else 'N/A'}")
            lines.append(f"- **Layer**: {rule.layer.value if rule.layer else 'N/A'}")
            lines.append(f"- **Scope**: {rule.scope.value if rule.scope else 'N/A'}")
            if rule.severity:
                lines.append(f"- **Severity**: {rule.severity.value}")
            lines.append("")

            if rule.description:
                lines.append("**Description:**")
                lines.append("")
                lines.append(rule.description)
                lines.append("")

            if rule.conditions:
                lines.append("**Conditions:**")
                lines.append("")
                lines.append(f"```\n{rule.conditions}\n```")
                lines.append("")

            if rule.enforcement_mechanism:
                lines.append(f"**Enforcement**: {rule.enforcement_mechanism}")
                lines.append("")

            if rule.related_entities:
                lines.append("**Related Entities:**")
                lines.append("")
                for entity in rule.related_entities:
                    lines.append(f"- `{entity}`")
                lines.append("")

            lines.append("---")
            lines.append("")
    else:
        lines.append("*No business rules documented.*")
        lines.append("")

    # Data Dictionary
    lines.append("## Data Dictionary")
    lines.append("")
    lines.append("### All Columns by Entity")
    lines.append("")

    for entity in sorted(entities, key=lambda e: e.name):
        if entity.columns:
            lines.append(f"#### {entity.name}")
            lines.append("")
            for col in entity.columns:
                lines.append(f"**`{col.name}`**")
                if col.description:
                    lines.append(f": {col.description}")
                else:
                    lines.append(f": {col.data_type}" + (" (nullable)" if col.nullable else " (required)"))
                lines.append("")

    return "\n".join(lines)


def _generate_service_prd(services: list, endpoints: list) -> str:
    """Generate comprehensive service PRD markdown."""
    from datetime import datetime

    lines = []

    # Header
    lines.append("# Backend Services Documentation")
    lines.append("")
    lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    lines.append("")

    # Table of Contents
    lines.append("## Table of Contents")
    lines.append("")
    lines.append("1. [Overview](#overview)")
    lines.append("2. [Service Catalog](#service-catalog)")
    lines.append("3. [API Endpoints](#api-endpoints)")
    lines.append("4. [Service Dependencies](#service-dependencies)")
    lines.append("5. [Business Operations](#business-operations)")
    lines.append("")

    # Overview
    lines.append("## Overview")
    lines.append("")
    lines.append(f"This document describes **{len(services)} services** with **{len(endpoints)} API endpoints**.")
    lines.append("")

    # Group services by type and domain
    services_by_type = {}
    services_by_domain = {}
    for service in services:
        svc_type = service.service_type.value if service.service_type else 'unknown'
        if svc_type not in services_by_type:
            services_by_type[svc_type] = []
        services_by_type[svc_type].append(service)

        domain = service.domain or 'Uncategorized'
        if domain not in services_by_domain:
            services_by_domain[domain] = []
        services_by_domain[domain].append(service)

    lines.append("### Service Statistics")
    lines.append("")
    lines.append(f"- **Total Services**: {len(services)}")
    lines.append(f"- **Total Operations**: {sum(len(s.operations) for s in services)}")
    lines.append(f"- **Total API Endpoints**: {len(endpoints)}")
    lines.append(f"- **Service Types**: {len(services_by_type)}")
    lines.append(f"- **Domains**: {len(services_by_domain)}")
    lines.append("")

    lines.append("### Services by Type")
    lines.append("")
    for svc_type in sorted(services_by_type.keys()):
        lines.append(f"- **{svc_type}**: {len(services_by_type[svc_type])} services")
    lines.append("")

    # Service Catalog
    lines.append("## Service Catalog")
    lines.append("")

    for domain in sorted(services_by_domain.keys()):
        lines.append(f"### Domain: {domain}")
        lines.append("")

        for service in sorted(services_by_domain[domain], key=lambda s: s.class_name):
            lines.append(f"#### {service.class_name}")
            lines.append("")

            if service.description:
                lines.append(service.description)
                lines.append("")

            # Service metadata
            lines.append("**Service Information:**")
            lines.append("")
            lines.append(f"- **Package**: `{service.package}`")
            lines.append(f"- **Qualified Name**: `{service.qualified_name}`")
            lines.append(f"- **Type**: {service.service_type.value if service.service_type else 'Unknown'}")
            lines.append(f"- **Operations**: {len(service.operations)}")
            if service.frameworks:
                lines.append(f"- **Frameworks**: {', '.join(service.frameworks)}")
            lines.append("")

            # Operations
            if service.operations:
                lines.append("**Operations:**")
                lines.append("")

                for op in service.operations:
                    params_str = ", ".join([f"{p.name}: {p.type}" for p in op.parameters])
                    lines.append(f"- **`{op.name}({params_str})`**")
                    if op.description:
                        lines.append(f"  - {op.description}")
                    if op.return_type:
                        lines.append(f"  - Returns: `{op.return_type}`")
                    if op.throws:
                        lines.append(f"  - Throws: {', '.join([f'`{e}`' for e in op.throws])}")
                    if op.annotations:
                        lines.append(f"  - Annotations: {', '.join([f'@{a}' for a in op.annotations])}")
                lines.append("")

            # Dependencies
            if service.dependencies:
                lines.append("**Dependencies:**")
                lines.append("")
                for dep in service.dependencies:
                    injection = f" [{dep.injection_method}]" if dep.injection_method else ""
                    dep_type = f" ({dep.dependency_type})" if dep.dependency_type else ""
                    lines.append(f"- `{dep.target_service}`{injection}{dep_type}")
                lines.append("")

            # Data Dependencies
            if service.data_dependencies:
                lines.append("**Data Dependencies (Database Entities):**")
                lines.append("")
                for entity_id in service.data_dependencies:
                    lines.append(f"- `{entity_id}`")
                lines.append("")

            # Transaction Boundaries
            if service.transaction_boundaries:
                lines.append("**Transaction Boundaries:**")
                lines.append("")
                for tx in service.transaction_boundaries:
                    props = []
                    if tx.propagation:
                        props.append(f"propagation={tx.propagation}")
                    if tx.isolation:
                        props.append(f"isolation={tx.isolation}")
                    if tx.read_only is not None:
                        props.append(f"readOnly={tx.read_only}")
                    props_str = f" ({', '.join(props)})" if props else ""
                    lines.append(f"- `{tx.method_name}`{props_str}")
                lines.append("")

            # Source file
            lines.append("**Source File:**")
            lines.append("")
            lines.append(f"- `{service.source_file}`")
            lines.append("")
            lines.append("---")
            lines.append("")

    # API Endpoints
    lines.append("## API Endpoints")
    lines.append("")

    if endpoints:
        # Group endpoints by HTTP method
        endpoints_by_method = {}
        for endpoint in endpoints:
            method = endpoint.http_method.value if endpoint.http_method else 'UNKNOWN'
            if method not in endpoints_by_method:
                endpoints_by_method[method] = []
            endpoints_by_method[method].append(endpoint)

        lines.append("### Endpoints by HTTP Method")
        lines.append("")

        for method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD']:
            if method in endpoints_by_method:
                method_endpoints = endpoints_by_method[method]
                lines.append(f"#### {method} Endpoints ({len(method_endpoints)})")
                lines.append("")

                headers = ["Path", "Service", "Operation", "Auth", "Description"]
                rows = []
                for endpoint in sorted(method_endpoints, key=lambda e: e.path):
                    auth_str = "Yes" if endpoint.authentication_required else "No"
                    desc_preview = (endpoint.description[:50] + "...") if endpoint.description and len(endpoint.description) > 50 else (endpoint.description or "-")

                    rows.append([
                        f"`{endpoint.path}`",
                        endpoint.service_id.split('.')[-1] if endpoint.service_id else "-",
                        endpoint.operation_name or "-",
                        auth_str,
                        desc_preview
                    ])

                lines.append(MarkdownBuilder.format_table(headers, rows))
                lines.append("")

        # Detailed endpoint documentation
        lines.append("### Detailed Endpoint Documentation")
        lines.append("")

        for endpoint in sorted(endpoints, key=lambda e: e.path):
            method_str = endpoint.http_method.value if endpoint.http_method else 'UNKNOWN'
            lines.append(f"#### `{method_str} {endpoint.path}`")
            lines.append("")

            if endpoint.description:
                lines.append(endpoint.description)
                lines.append("")

            lines.append("**Endpoint Details:**")
            lines.append("")
            lines.append(f"- **Service**: `{endpoint.service_id}`")
            lines.append(f"- **Operation**: `{endpoint.operation_name}`")
            lines.append(f"- **Authentication Required**: {'Yes' if endpoint.authentication_required else 'No'}")

            if endpoint.authorization_roles:
                lines.append(f"- **Required Roles**: {', '.join([f'`{r}`' for r in endpoint.authorization_roles])}")

            if endpoint.rate_limited:
                lines.append("- **Rate Limited**: Yes")

            if endpoint.deprecated:
                lines.append("- **⚠️ DEPRECATED**: This endpoint is deprecated")

            lines.append("")

            # Request format
            if endpoint.request_format:
                lines.append("**Request:**")
                lines.append("")
                if endpoint.request_format.content_type:
                    lines.append(f"- Content-Type: `{endpoint.request_format.content_type}`")
                if endpoint.request_format.parameters:
                    lines.append("- Parameters:")
                    for param in endpoint.request_format.parameters:
                        required_str = " (required)" if param.required else " (optional)"
                        lines.append(f"  - `{param.name}`: {param.param_type}{required_str}")
                lines.append("")

            # Response format
            if endpoint.response_format:
                lines.append("**Response:**")
                lines.append("")
                if endpoint.response_format.content_type:
                    lines.append(f"- Content-Type: `{endpoint.response_format.content_type}`")
                if endpoint.response_format.status_codes:
                    lines.append("- Status Codes:")
                    for status in endpoint.response_format.status_codes:
                        lines.append(f"  - `{status.code}`: {status.description}")
                lines.append("")

            lines.append("---")
            lines.append("")
    else:
        lines.append("*No API endpoints documented.*")
        lines.append("")

    # Service Dependencies
    lines.append("## Service Dependencies")
    lines.append("")

    # Build dependency graph
    all_dependencies = []
    for service in services:
        for dep in service.dependencies:
            all_dependencies.append({
                'from': service.class_name,
                'to': dep.target_service,
                'type': dep.dependency_type or 'reference'
            })

    if all_dependencies:
        headers = ["Service", "Depends On", "Dependency Type"]
        rows = []
        for dep in sorted(all_dependencies, key=lambda d: (d['from'], d['to'])):
            rows.append([
                f"`{dep['from']}`",
                f"`{dep['to']}`",
                dep['type']
            ])
        lines.append(MarkdownBuilder.format_table(headers, rows))
    else:
        lines.append("*No service dependencies documented.*")
    lines.append("")

    # Business Operations
    lines.append("## Business Operations")
    lines.append("")
    lines.append("### Key Business Operations by Service")
    lines.append("")

    for service in sorted(services, key=lambda s: s.class_name):
        if service.operations:
            lines.append(f"#### {service.class_name}")
            lines.append("")
            for op in service.operations:
                params_str = ", ".join([f"{p.name}: {p.type}" for p in op.parameters])
                lines.append(f"- **`{op.name}({params_str})`**")
                if op.description:
                    lines.append(f"  - {op.description}")
            lines.append("")

    return "\n".join(lines)


def _generate_frontend_prd(forms: list, components: list) -> str:
    """Generate comprehensive frontend PRD markdown."""
    from datetime import datetime

    lines = []

    # Header
    lines.append("# Frontend Documentation")
    lines.append("")
    lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    lines.append("")

    # Table of Contents
    lines.append("## Table of Contents")
    lines.append("")
    lines.append("1. [Overview](#overview)")
    lines.append("2. [Form Catalog](#form-catalog)")
    lines.append("3. [UI Components](#ui-components)")
    lines.append("4. [Form-to-Backend Mapping](#form-to-backend-mapping)")
    lines.append("5. [Navigation Flows](#navigation-flows)")
    lines.append("")

    # Overview
    lines.append("## Overview")
    lines.append("")
    lines.append(f"This document describes **{len(forms)} forms** and **{len(components)} UI components**.")
    lines.append("")

    # Group forms by type and domain
    forms_by_type = {}
    forms_by_domain = {}
    for form in forms:
        form_type = form.form_type.value if form.form_type else 'unknown'
        if form_type not in forms_by_type:
            forms_by_type[form_type] = []
        forms_by_type[form_type].append(form)

        domain = form.domain or 'Uncategorized'
        if domain not in forms_by_domain:
            forms_by_domain[domain] = []
        forms_by_domain[domain].append(form)

    lines.append("### Frontend Statistics")
    lines.append("")
    lines.append(f"- **Total Forms**: {len(forms)}")
    lines.append(f"- **Total Form Fields**: {sum(len(f.fields) for f in forms)}")
    lines.append(f"- **Total UI Components**: {len(components)}")
    lines.append(f"- **Form Types**: {len(forms_by_type)}")
    lines.append(f"- **Domains**: {len(forms_by_domain)}")
    lines.append("")

    lines.append("### Forms by Type")
    lines.append("")
    for form_type in sorted(forms_by_type.keys()):
        lines.append(f"- **{form_type}**: {len(forms_by_type[form_type])} forms")
    lines.append("")

    # Form Catalog
    lines.append("## Form Catalog")
    lines.append("")

    for domain in sorted(forms_by_domain.keys()):
        lines.append(f"### Domain: {domain}")
        lines.append("")

        for form in sorted(forms_by_domain[domain], key=lambda f: f.name):
            lines.append(f"#### {form.name}")
            lines.append("")

            if form.description:
                lines.append(form.description)
                lines.append("")

            # Form metadata
            lines.append("**Form Information:**")
            lines.append("")
            lines.append(f"- **Form Type**: {form.form_type.value if form.form_type else 'Unknown'}")
            lines.append(f"- **Field Count**: {len(form.fields)}")
            if form.submission_endpoint and form.submission_method:
                lines.append(f"- **Submission**: `{form.submission_method} {form.submission_endpoint}`")
            if form.submission_service:
                lines.append(f"- **Backend Service**: `{form.submission_service}`")
            lines.append("")

            # Form fields table
            if form.fields:
                lines.append("**Form Fields:**")
                lines.append("")

                headers = ["Field", "Type", "Label", "Required", "Validation"]
                rows = []
                for field in form.fields:
                    validation = field.validation_pattern or "-"
                    rows.append([
                        f"`{field.name}`",
                        field.type,
                        field.label or "-",
                        "Yes" if field.required else "No",
                        validation if len(validation) < 30 else validation[:27] + "..."
                    ])

                lines.append(MarkdownBuilder.format_table(headers, rows))
                lines.append("")

            # Validation rules
            if form.validation_rules:
                lines.append("**Validation Rules:**")
                lines.append("")
                for rule in form.validation_rules:
                    lines.append(f"- **{rule.field}** ({rule.rule_type}): {rule.message}")
                lines.append("")

            # Navigation
            if form.navigation_on_success or form.navigation_on_cancel:
                lines.append("**Navigation:**")
                lines.append("")
                if form.navigation_on_success:
                    lines.append(f"- **On Success**: {form.navigation_on_success}")
                if form.navigation_on_cancel:
                    lines.append(f"- **On Cancel**: {form.navigation_on_cancel}")
                lines.append("")

            # Bound entities
            if form.bound_entities:
                lines.append("**Bound Database Entities:**")
                lines.append("")
                for entity in form.bound_entities:
                    lines.append(f"- `{entity}`")
                lines.append("")

            # Security patterns
            if form.security_patterns:
                lines.append("**Security Considerations:**")
                lines.append("")
                for pattern in form.security_patterns:
                    lines.append(f"- {pattern}")
                lines.append("")

            # Source file
            lines.append("**Source File:**")
            lines.append("")
            lines.append(f"- `{form.source_file}`")
            lines.append("")
            lines.append("---")
            lines.append("")

    # UI Components
    lines.append("## UI Components")
    lines.append("")

    if components:
        # Group components by type
        components_by_type = {}
        for component in components:
            comp_type = component.component_type.value if component.component_type else 'unknown'
            if comp_type not in components_by_type:
                components_by_type[comp_type] = []
            components_by_type[comp_type].append(component)

        lines.append("### Components by Type")
        lines.append("")

        for comp_type in sorted(components_by_type.keys()):
            lines.append(f"#### {comp_type} ({len(components_by_type[comp_type])})")
            lines.append("")

            for component in sorted(components_by_type[comp_type], key=lambda c: c.name):
                lines.append(f"##### {component.name}")
                lines.append("")

                if component.description:
                    lines.append(component.description)
                    lines.append("")

                lines.append("**Component Information:**")
                lines.append("")
                lines.append(f"- **ID**: `{component.id}`")
                lines.append(f"- **Type**: {component.component_type.value if component.component_type else 'Unknown'}")

                if component.responsibilities:
                    lines.append("- **Responsibilities**:")
                    for resp in component.responsibilities:
                        lines.append(f"  - {resp}")

                if component.framework_annotations:
                    lines.append(f"- **Framework Annotations**: {', '.join([f'@{a}' for a in component.framework_annotations])}")

                lines.append("")

                # Events
                if component.events_handled:
                    lines.append("**Events Handled:**")
                    lines.append("")
                    for event in component.events_handled:
                        lines.append(f"- `{event}`")
                    lines.append("")

                if component.events_emitted:
                    lines.append("**Events Emitted:**")
                    lines.append("")
                    for event in component.events_emitted:
                        lines.append(f"- `{event}`")
                    lines.append("")

                # Data bindings
                if component.data_bindings:
                    lines.append("**Data Bindings:**")
                    lines.append("")
                    for binding in component.data_bindings:
                        lines.append(f"- `{binding.target_property}` ← `{binding.source_expression}` ({binding.binding_type})")
                    lines.append("")

                # Navigation targets
                if component.navigation_targets:
                    lines.append("**Navigation Targets:**")
                    lines.append("")
                    for target in component.navigation_targets:
                        lines.append(f"- `{target}`")
                    lines.append("")

                # Child components
                if component.child_components:
                    lines.append("**Child Components:**")
                    lines.append("")
                    for child in component.child_components:
                        lines.append(f"- `{child}`")
                    lines.append("")

                # Related forms
                if component.related_forms:
                    lines.append("**Related Forms:**")
                    lines.append("")
                    for form_id in component.related_forms:
                        lines.append(f"- `{form_id}`")
                    lines.append("")

                lines.append("**Source File:**")
                lines.append("")
                lines.append(f"- `{component.source_file}`")
                lines.append("")
                lines.append("---")
                lines.append("")
    else:
        lines.append("*No UI components documented.*")
        lines.append("")

    # Form-to-Backend Mapping
    lines.append("## Form-to-Backend Mapping")
    lines.append("")

    # Collect form submissions
    form_submissions = []
    for form in forms:
        if form.submission_endpoint or form.submission_service:
            form_submissions.append({
                'form': form.name,
                'endpoint': form.submission_endpoint or '-',
                'method': form.submission_method or '-',
                'service': form.submission_service or '-',
                'entities': ', '.join([f"`{e}`" for e in form.bound_entities]) if form.bound_entities else '-'
            })

    if form_submissions:
        headers = ["Form", "Endpoint", "Method", "Backend Service", "Database Entities"]
        rows = []
        for sub in sorted(form_submissions, key=lambda s: s['form']):
            rows.append([
                f"`{sub['form']}`",
                f"`{sub['endpoint']}`" if sub['endpoint'] != '-' else '-',
                sub['method'],
                f"`{sub['service']}`" if sub['service'] != '-' else '-',
                sub['entities']
            ])
        lines.append(MarkdownBuilder.format_table(headers, rows))
    else:
        lines.append("*No form-to-backend mappings documented.*")
    lines.append("")

    # Navigation Flows
    lines.append("## Navigation Flows")
    lines.append("")
    lines.append("### Form Navigation Patterns")
    lines.append("")

    # Collect navigation patterns
    nav_patterns = {}
    for form in forms:
        if form.navigation_on_success or form.navigation_on_cancel:
            nav_patterns[form.name] = {
                'success': form.navigation_on_success,
                'cancel': form.navigation_on_cancel
            }

    if nav_patterns:
        for form_name in sorted(nav_patterns.keys()):
            pattern = nav_patterns[form_name]
            lines.append(f"**{form_name}:**")
            lines.append("")
            if pattern['success']:
                lines.append(f"- On Success → `{pattern['success']}`")
            if pattern['cancel']:
                lines.append(f"- On Cancel → `{pattern['cancel']}`")
            lines.append("")
    else:
        lines.append("*No navigation flows documented.*")
        lines.append("")

    return "\n".join(lines)


def _print_final_summary(results: dict, output_dir: Path):
    """Print final summary of PRD generation."""
    click.echo("\nSummary:")
    click.echo("-" * 60)

    # Database
    if results["database"]:
        db = results["database"]
        if db.get("success"):
            click.echo(f"Database:  {db['entities']} entities, {db['rules']} rules")
            click.echo(f"           ({db['analyzed']} analyzed, {db['skipped']} skipped, {db['failed']} failed)")
        else:
            click.echo(f"Database:  FAILED - {db.get('error', 'Unknown error')}")

    # Services
    if results["services"]:
        svc = results["services"]
        if svc.get("success"):
            click.echo(f"Services:  {svc['services']} services, {svc['endpoints']} endpoints")
            click.echo(f"           ({svc['analyzed']} analyzed, {svc['skipped']} skipped, {svc['failed']} failed)")
        else:
            click.echo(f"Services:  FAILED - {svc.get('error', 'Unknown error')}")

    # Frontend
    if results["frontend"]:
        fe = results["frontend"]
        if fe.get("success"):
            click.echo(f"Frontend:  {fe['forms']} forms, {fe['components']} components")
            click.echo(f"           ({fe['analyzed']} analyzed, {fe['skipped']} skipped, {fe['failed']} failed)")
        else:
            click.echo(f"Frontend:  FAILED - {fe.get('error', 'Unknown error')}")

    click.echo("-" * 60)
    click.echo(f"\nOutput directory: {output_dir}")
    click.echo(f"  - database/: Entity definitions and index")
    click.echo(f"  - services/: Service definitions and endpoints")
    click.echo(f"  - frontend/: Forms and UI components")
    click.echo(f"  - business_rules/: Business rule definitions")
    click.echo(f"  - prd/: Generated PRD markdown documents")
