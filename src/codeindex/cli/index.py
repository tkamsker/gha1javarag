"""
Index CLI command.

Implements the `codeindex index` command for indexing to Weaviate.
"""

import logging
import json
from pathlib import Path
from typing import Optional

import click

from codeindex.utils.logging import get_logger
from codeindex.services.indexing import IndexingService
from codeindex.schemas import check_weaviate_health

logger = get_logger(__name__)


@click.command(name='index')
@click.option(
    '--inventory',
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help='Discovery inventory file (JSONL format)'
)
@click.option(
    '--extraction',
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help='Extraction results file (JSONL format)'
)
@click.option(
    '--batch-size',
    type=int,
    default=50,
    help='Batch size for Weaviate operations (default: 50)'
)
@click.option(
    '--dry-run',
    is_flag=True,
    help='Preview indexing without writing to Weaviate'
)
@click.option(
    '--create-schema',
    is_flag=True,
    help='Create Weaviate schema if missing'
)
@click.option(
    '--quiet',
    is_flag=True,
    help='Suppress progress output'
)
@click.pass_context
def index_command(
    ctx,
    inventory: Path,
    extraction: Path,
    batch_size: int,
    dry_run: bool,
    create_schema: bool,
    quiet: bool
):
    """
    Index artifacts to Weaviate vector database.

    Loads discovery inventory and extraction results, then indexes projects
    and code artifacts to Weaviate for semantic search.

    Examples:

        # Index from discovery and extraction files
        codeindex index --inventory discovery.jsonl --extraction extraction.jsonl

        # Use custom batch size
        codeindex index --inventory discovery.jsonl --extraction extraction.jsonl --batch-size 100

        # Preview without indexing
        codeindex index --inventory discovery.jsonl --extraction extraction.jsonl --dry-run

        # Create schema if missing
        codeindex index --inventory discovery.jsonl --extraction extraction.jsonl --create-schema
    """
    cli_context = ctx.obj
    config = cli_context.config
    output_format = cli_context.format

    # Check Weaviate availability
    if not quiet and output_format == 'text':
        click.echo(f"Checking Weaviate at {config.weaviate_url}...")

    try:
        check_weaviate_health(config.weaviate_url)
        if not quiet and output_format == 'text':
            click.echo("✓ Weaviate is available")
    except ConnectionError as e:
        click.echo(f"Error: {e}", err=True)
        ctx.exit(1)

    # Validate inputs
    if not inventory.exists():
        click.echo(f"Error: Inventory file not found: {inventory}", err=True)
        ctx.exit(1)

    if not extraction.exists():
        click.echo(f"Error: Extraction file not found: {extraction}", err=True)
        ctx.exit(1)

    if dry_run:
        if output_format == 'text':
            click.echo("Running in dry-run mode (no changes will be made)")
        _dry_run_index(inventory, extraction, output_format)
        return

    # Create indexing service
    try:
        service = IndexingService(config=config)
    except Exception as e:
        logger.error(f"Failed to initialize indexing service: {e}", exc_info=True)
        click.echo(f"Error: Failed to initialize indexing service - {e}", err=True)
        ctx.exit(1)

    # Index artifacts
    if not quiet and output_format == 'text':
        click.echo(f"\nIndexing from:")
        click.echo(f"  Inventory:  {inventory}")
        click.echo(f"  Extraction: {extraction}")
        click.echo(f"  Batch size: {batch_size}\n")

    try:
        stats = service.index_from_files(
            inventory_path=inventory,
            extraction_path=extraction,
            batch_size=batch_size
        )

        # Output results
        if output_format == 'json':
            click.echo(json.dumps(stats, indent=2))
        else:
            _print_index_summary(stats)

        logger.info("Indexing complete")

    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        ctx.exit(1)
    except ConnectionError as e:
        click.echo(f"Error: Weaviate connection failed - {e}", err=True)
        ctx.exit(1)
    except Exception as e:
        logger.error(f"Indexing failed: {e}", exc_info=True)
        click.echo(f"Error: Indexing failed - {e}", err=True)
        ctx.exit(1)


def _dry_run_index(
    inventory_path: Path,
    extraction_path: Path,
    output_format: str
):
    """
    Preview indexing without writing to Weaviate.

    Args:
        inventory_path: Path to discovery inventory
        extraction_path: Path to extraction results
        output_format: Output format (text or json)
    """
    import json

    # Count projects in inventory
    project_count = 0
    with inventory_path.open('r') as f:
        for line in f:
            if line.strip():
                data = json.loads(line)
                if 'project_id' in data:
                    project_count += 1

    # Count extraction results
    artifact_count = 0
    with extraction_path.open('r') as f:
        for line in f:
            if line.strip():
                data = json.loads(line)
                if 'file_path' in data:
                    artifact_count += 1

    if output_format == 'json':
        result = {
            "dry_run": True,
            "projects_to_index": project_count,
            "artifacts_to_index": artifact_count
        }
        click.echo(json.dumps(result, indent=2))
    else:
        click.echo("\n" + "="*60)
        click.echo("Dry Run - Indexing Preview")
        click.echo("="*60)
        click.echo(f"Projects to index:  {project_count}")
        click.echo(f"Artifacts to index: {artifact_count}")
        click.echo("\nNo changes made to Weaviate.")


def _print_index_summary(stats: dict):
    """
    Print indexing summary.

    Args:
        stats: Indexing statistics
    """
    click.echo("\n" + "="*60)
    click.echo("Indexing Summary")
    click.echo("="*60)
    click.echo(f"Projects indexed:   {stats.get('projects_indexed', 0)}")
    click.echo(f"Artifacts indexed:  {stats.get('artifacts_indexed', 0)}")
    click.echo(f"Artifacts errors:   {stats.get('artifacts_errors', 0)}")
    click.echo(f"Total files:        {stats.get('total_files', 0)}")

    if stats.get('artifacts_errors', 0) > 0:
        click.echo(f"\n⚠ {stats['artifacts_errors']} artifacts failed to index")

    click.echo("\n✓ Indexing complete")
