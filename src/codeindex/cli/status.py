"""
Status CLI command.

Implements the `codeindex status` command for monitoring and validating indexing status.
"""

import logging
import json
from typing import Optional
from datetime import datetime

import click

from codeindex.utils.logging import get_logger
from codeindex.services.weaviate_store import WeaviateStore
from codeindex.services.ollama_client import OllamaClient

logger = get_logger(__name__)


@click.command(name='status')
@click.option(
    '--project',
    type=str,
    help='Show status for specific project'
)
@click.option(
    '--verbose',
    is_flag=True,
    help='Show detailed information including type breakdowns'
)
@click.pass_context
def status_command(
    ctx,
    project: Optional[str],
    verbose: bool
):
    """
    Monitor and validate indexing status.

    Shows:
    - Service health (Weaviate, Ollama)
    - Project counts and details
    - Artifact counts and type breakdowns
    - Last indexed timestamps

    Examples:

        # Show overall status
        codeindex status

        # Show status for specific project
        codeindex status --project com.example:myapp:1.0.0

        # Show detailed breakdown
        codeindex status --verbose

        # Get JSON output for programmatic use
        codeindex --format json status
    """
    cli_context = ctx.obj
    config = cli_context.config
    output_format = cli_context.format

    # Check service health
    weaviate_healthy = False
    ollama_healthy = False

    try:
        store = WeaviateStore(config=config, auto_create_schema=False)
        weaviate_healthy = store.health_check()
    except Exception as e:
        logger.debug(f"Weaviate connection failed: {e}")
        weaviate_healthy = False

    try:
        ollama = OllamaClient(
            base_url=config.ollama_base_url,
            model=config.ollama_model_name,
            connect_timeout=float(config.ollama_connect_timeout),
            read_timeout=float(config.ollama_read_timeout)
        )
        ollama_healthy = ollama.health_check()
        ollama.close()
    except Exception as e:
        logger.debug(f"Ollama connection failed: {e}")
        ollama_healthy = False

    # Get statistics if Weaviate is available
    statistics = None
    if weaviate_healthy:
        try:
            if project:
                # Get project-specific statistics
                statistics = store.get_project_statistics(project)
            else:
                # Get overall statistics
                statistics = store.get_statistics()
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}", exc_info=True)
            statistics = None

    # Format output
    if output_format == 'json':
        _output_json(weaviate_healthy, ollama_healthy, statistics, project)
    else:
        _output_text(
            weaviate_healthy,
            ollama_healthy,
            statistics,
            project,
            verbose
        )


def _output_json(
    weaviate_healthy: bool,
    ollama_healthy: bool,
    statistics: Optional[dict],
    project_filter: Optional[str]
):
    """Output status as JSON."""
    output = {
        "services": {
            "weaviate": {
                "status": "connected" if weaviate_healthy else "unavailable"
            },
            "ollama": {
                "status": "connected" if ollama_healthy else "unavailable"
            }
        },
        "statistics": statistics if statistics else {},
        "filter": {
            "project": project_filter
        }
    }

    click.echo(json.dumps(output, indent=2, default=str))


def _output_text(
    weaviate_healthy: bool,
    ollama_healthy: bool,
    statistics: Optional[dict],
    project_filter: Optional[str],
    verbose: bool
):
    """Output status as human-readable text."""
    click.echo("=" * 70)
    click.echo("Code Indexer Status")
    click.echo("=" * 70)
    click.echo()

    # Service health
    click.echo("Service Health:")
    click.echo(f"  Weaviate: {_status_indicator(weaviate_healthy)}")
    click.echo(f"  Ollama:   {_status_indicator(ollama_healthy)}")
    click.echo()

    # If Weaviate is down, show error and suggest fix
    if not weaviate_healthy:
        click.echo(click.style("ERROR: ", fg="red", bold=True) +
                  "Weaviate is not accessible.")
        click.echo()
        click.echo("To start Weaviate:")
        click.echo("  ./docker-weaviate.sh start")
        click.echo("  # or")
        click.echo("  docker-compose up -d")
        click.echo()
        return

    # If no statistics, show empty state
    if not statistics:
        _show_empty_state()
        return

    # Show project-specific status
    if project_filter:
        _show_project_status(statistics, verbose)
    else:
        _show_overall_status(statistics, verbose)


def _show_overall_status(statistics: dict, verbose: bool):
    """Show overall indexing status."""
    project_count = statistics.get("project_count", 0)
    artifact_count = statistics.get("artifact_count", 0)
    projects = statistics.get("projects", [])

    if project_count == 0:
        _show_empty_state()
        return

    # Summary
    click.echo(f"Indexed Projects: {project_count}")
    click.echo(f"Total Artifacts:  {artifact_count:,}")
    click.echo()

    # Project list
    if projects:
        click.echo("Projects:")
        click.echo("-" * 70)

        for proj in projects:
            project_id = proj.get("project_id", "Unknown")
            name = proj.get("name", "Unknown")
            count = proj.get("artifact_count", 0)
            last_indexed = proj.get("last_indexed")

            # Project header
            click.echo()
            click.echo(click.style(f"  {project_id}", fg="cyan", bold=True))
            if name and name != project_id:
                click.echo(f"  Name: {name}")

            click.echo(f"  Artifacts: {count:,}")

            # Last indexed
            if last_indexed:
                last_indexed_str = _format_timestamp(last_indexed)
                click.echo(f"  Last Indexed: {last_indexed_str}")

            # Type breakdown if verbose
            if verbose:
                type_breakdown = proj.get("type_breakdown", {})
                if type_breakdown:
                    click.echo("  Types:")
                    for artifact_type, type_count in sorted(
                        type_breakdown.items(),
                        key=lambda x: x[1],
                        reverse=True
                    ):
                        percentage = (type_count / count * 100) if count > 0 else 0
                        click.echo(f"    {artifact_type:20s} {type_count:5,} ({percentage:5.1f}%)")

        click.echo()
        click.echo("-" * 70)


def _show_project_status(statistics: dict, verbose: bool):
    """Show status for specific project."""
    if not statistics.get("found", False):
        project_id = statistics.get("project_id", "unknown")
        click.echo(click.style(f"Project not found: {project_id}", fg="yellow"))
        click.echo()
        click.echo("Available projects:")
        click.echo("  Run 'codeindex status' to see all indexed projects")
        return

    # Project details
    project_id = statistics.get("project_id")
    name = statistics.get("name", "Unknown")
    artifact_count = statistics.get("artifact_count", 0)
    last_indexed = statistics.get("last_indexed")

    click.echo(f"Project: {click.style(project_id, fg='cyan', bold=True)}")
    if name and name != project_id:
        click.echo(f"Name: {name}")
    click.echo(f"Artifacts: {artifact_count:,}")

    if last_indexed:
        last_indexed_str = _format_timestamp(last_indexed)
        click.echo(f"Last Indexed: {last_indexed_str}")

    click.echo()

    # Type breakdown
    type_breakdown = statistics.get("type_breakdown", {})
    if type_breakdown:
        click.echo("Artifact Type Breakdown:")
        click.echo("-" * 60)

        total = sum(type_breakdown.values())
        for artifact_type, count in sorted(
            type_breakdown.items(),
            key=lambda x: x[1],
            reverse=True
        ):
            percentage = (count / total * 100) if total > 0 else 0
            bar = _create_bar(percentage)
            click.echo(f"  {artifact_type:20s} {count:6,} {bar} {percentage:5.1f}%")

        click.echo("-" * 60)
        click.echo(f"  {'Total':20s} {total:6,}")
    else:
        click.echo("No type breakdown available")


def _show_empty_state():
    """Show empty state when no data is indexed."""
    click.echo(click.style("No indexed data found.", fg="yellow"))
    click.echo()
    click.echo("To index your codebase:")
    click.echo()
    click.echo("  1. Discover projects:")
    click.echo("     codeindex discover --source-dir /path/to/java/source")
    click.echo()
    click.echo("  2. Extract semantic information:")
    click.echo("     codeindex extract")
    click.echo()
    click.echo("  3. Index to Weaviate:")
    click.echo("     codeindex index")
    click.echo()
    click.echo("Then run 'codeindex status' again to see your indexed projects.")
    click.echo()


def _status_indicator(healthy: bool) -> str:
    """Create a status indicator string."""
    if healthy:
        return click.style("✓ Connected", fg="green")
    else:
        return click.style("✗ Unavailable", fg="red")


def _format_timestamp(timestamp_str: str) -> str:
    """Format ISO timestamp for display."""
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        now = datetime.now(dt.tzinfo)

        # Calculate time difference
        diff = now - dt

        # Format relative time
        if diff.days > 0:
            if diff.days == 1:
                relative = "1 day ago"
            else:
                relative = f"{diff.days} days ago"
        elif diff.seconds >= 3600:
            hours = diff.seconds // 3600
            if hours == 1:
                relative = "1 hour ago"
            else:
                relative = f"{hours} hours ago"
        elif diff.seconds >= 60:
            minutes = diff.seconds // 60
            if minutes == 1:
                relative = "1 minute ago"
            else:
                relative = f"{minutes} minutes ago"
        else:
            relative = "just now"

        # Format absolute time
        absolute = dt.strftime("%Y-%m-%d %H:%M:%S")

        return f"{absolute} ({relative})"
    except Exception:
        return timestamp_str


def _create_bar(percentage: float, width: int = 20) -> str:
    """Create a text-based progress bar."""
    filled = int(width * percentage / 100)
    empty = width - filled
    return f"[{'█' * filled}{'░' * empty}]"
