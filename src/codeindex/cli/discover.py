"""
Discover CLI command.

Implements the `codeindex discover` command for Maven project discovery.
"""

import logging
import json
from pathlib import Path
from typing import Optional

import click

from codeindex.utils.logging import get_logger
from codeindex.services.discovery import DiscoveryService
# Progress tracking will be added in future iterations

logger = get_logger(__name__)


@click.command(name='discover')
@click.option(
    '--source-dir',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    help='Root directory containing Java source code to analyze'
)
@click.option(
    '--output',
    type=click.Path(path_type=Path),
    help='Output file path for discovery inventory (JSONL format)'
)
@click.option(
    '--project',
    type=str,
    help='Filter to specific project by artifact ID'
)
@click.option(
    '--dry-run',
    is_flag=True,
    help='Preview discovery without writing output file'
)
@click.option(
    '--quiet',
    is_flag=True,
    help='Suppress progress output'
)
@click.pass_context
def discover_command(
    ctx,
    source_dir: Optional[Path],
    output: Optional[Path],
    project: Optional[str],
    dry_run: bool,
    quiet: bool
):
    """
    Discover Maven projects and create file inventory.

    Scans the source directory for Maven projects (pom.xml files),
    analyzes their structure, and generates a discovery inventory.

    Examples:

        # Discover projects in current directory
        codeindex discover

        # Discover projects in specific directory
        codeindex discover --source-dir /path/to/java/project

        # Save inventory to file
        codeindex discover --output inventory.jsonl

        # Filter to specific project
        codeindex discover --project my-app

        # Preview without writing
        codeindex discover --dry-run
    """
    cli_context = ctx.obj
    config = cli_context.config
    output_format = cli_context.format

    # Determine source directory
    if not source_dir:
        source_dir = config.java_source_dir
        if not source_dir:
            click.echo(
                "Error: No source directory specified. "
                "Use --source-dir or set JAVA_SOURCE_DIR in .env",
                err=True
            )
            ctx.exit(1)

    if not source_dir.exists():
        click.echo(f"Error: Source directory not found: {source_dir}", err=True)
        ctx.exit(1)

    # Determine output path
    if not output:
        output = config.output_dir / "discovery-inventory.jsonl"

    logger.info(f"Discovering Maven projects in {source_dir}")

    # Create discovery service
    service = DiscoveryService(config=config)


    try:
        # Show progress message
        if not quiet and output_format == 'text':
            click.echo(f"Discovering Maven projects in {source_dir}...")

        # Generate discovery inventory
        if project:
            logger.info(f"Filtering to project: {project}")

        inventory = service.generate_inventory(source_dir)

        # Filter projects if requested
        if project:
            original_count = len(inventory.projects)
            inventory.projects = [
                p for p in inventory.projects
                if project in p.get('artifact_id', '')
            ]
            filtered_count = len(inventory.projects)
            logger.info(f"Filtered {original_count} -> {filtered_count} projects")

        # Output results
        if output_format == 'json':
            # JSON output to stdout
            result = {
                "scan_timestamp": inventory.scan_timestamp.isoformat(),
                "source_dir": inventory.root_directory,
                "total_projects": len(inventory.projects),
                "total_files": inventory.total_files,
                "scan_duration_seconds": inventory.scan_duration_seconds,
                "projects": inventory.projects,
                "files_by_type": inventory.files_by_type
            }
            click.echo(json.dumps(result, indent=2))
        else:
            # Text output
            click.echo("\n" + "="*60)
            click.echo("Discovery Results")
            click.echo("="*60)
            click.echo(f"Root directory: {inventory.root_directory}")
            click.echo(f"Scan timestamp: {inventory.scan_timestamp}")
            click.echo(f"Duration: {inventory.scan_duration_seconds:.2f}s")
            click.echo(f"\nProjects found: {len(inventory.projects)}")
            click.echo(f"Total files: {inventory.total_files}")

            if inventory.files_by_type:
                click.echo("\nFiles by type:")
                for file_type, count in sorted(
                    inventory.files_by_type.items(),
                    key=lambda x: x[1],
                    reverse=True
                ):
                    click.echo(f"  {file_type:20s}: {count:>6d}")

            if inventory.projects:
                click.echo("\nProjects:")
                for proj in inventory.projects:
                    artifact_id = proj.get('artifact_id') or 'unknown'
                    version = proj.get('version') or 'unknown'
                    file_count = proj.get('file_count', 0)
                    click.echo(f"  • {artifact_id:30s} v{version:15s} ({file_count} files)")

        # Save to file if not dry-run
        if not dry_run:
            if output:
                output.parent.mkdir(parents=True, exist_ok=True)
                inventory.save_jsonl(output)
                logger.info(f"Saved discovery inventory to {output}")

                if output_format == 'text':
                    click.echo(f"\n✓ Inventory saved to: {output}")
        else:
            if output_format == 'text':
                click.echo("\n[Dry run - no files written]")

        # Handle empty state
        if len(inventory.projects) == 0:
            if output_format == 'text':
                click.echo("\n⚠ No projects found in the specified directory")
                click.echo("Make sure the directory contains Maven projects with pom.xml files")
            logger.warning("No projects discovered")
            ctx.exit(0)

        logger.info("Discovery complete")

    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        ctx.exit(1)
    except PermissionError as e:
        click.echo(f"Error: Permission denied - {e}", err=True)
        ctx.exit(1)
    except Exception as e:
        logger.error(f"Discovery failed: {e}", exc_info=True)
        click.echo(f"Error: Discovery failed - {e}", err=True)
        ctx.exit(1)
