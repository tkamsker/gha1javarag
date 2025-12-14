"""
Search CLI command.

Implements the `codeindex search` command for semantic search over indexed code.
"""

import logging
import json
from typing import Optional, List

import click

from codeindex.utils.logging import get_logger
from codeindex.services.weaviate_store import WeaviateStore
from codeindex.schemas import check_weaviate_health

logger = get_logger(__name__)


@click.command(name='search')
@click.argument('query', type=str)
@click.option(
    '--project',
    type=str,
    help='Filter by project ID'
)
@click.option(
    '--type',
    'artifact_types',
    multiple=True,
    help='Filter by artifact type (can specify multiple)'
)
@click.option(
    '--limit',
    type=int,
    default=10,
    help='Maximum results (default: 10)'
)
@click.option(
    '--show-summary',
    is_flag=True,
    help='Show artifact summaries in results'
)
@click.option(
    '--show-distance',
    is_flag=True,
    help='Show semantic distance scores'
)
@click.pass_context
def search_command(
    ctx,
    query: str,
    project: Optional[str],
    artifact_types: tuple,
    limit: int,
    show_summary: bool,
    show_distance: bool
):
    """
    Search semantically over indexed code artifacts.

    Uses vector similarity search to find code artifacts matching the query.

    Examples:

        # Basic search
        codeindex search "authentication logic"

        # Filter by project
        codeindex search "user validation" --project com.example:myapp:1.0.0

        # Filter by artifact type
        codeindex search "database queries" --type JAVA_SOURCE --type SQL_SCHEMA

        # Limit results
        codeindex search "Spring controllers" --limit 5

        # Show summaries and distance scores
        codeindex search "REST API" --show-summary --show-distance
    """
    cli_context = ctx.obj
    config = cli_context.config
    output_format = cli_context.format

    # Check Weaviate availability
    try:
        check_weaviate_health(config.weaviate_url)
    except ConnectionError as e:
        click.echo(f"Error: {e}", err=True)
        ctx.exit(1)

    # Create Weaviate store
    try:
        store = WeaviateStore(config=config)
    except Exception as e:
        logger.error(f"Failed to initialize Weaviate store: {e}", exc_info=True)
        click.echo(f"Error: Failed to connect to Weaviate - {e}", err=True)
        ctx.exit(1)

    # Perform search
    if output_format == 'text':
        click.echo(f"Searching: \"{query}\"")
        if project:
            click.echo(f"  Project: {project}")
        if artifact_types:
            click.echo(f"  Types: {', '.join(artifact_types)}")
        click.echo(f"  Limit: {limit}\n")

    try:
        results = store.search_artifacts(
            query=query,
            project_id=project,
            artifact_types=list(artifact_types) if artifact_types else None,
            limit=limit
        )

        # Output results
        if output_format == 'json':
            output_data = {
                'query': query,
                'total_results': len(results),
                'results': results
            }
            click.echo(json.dumps(output_data, indent=2, default=str))
        else:
            _print_search_results(
                results,
                query,
                show_summary,
                show_distance
            )

        logger.info(f"Search complete: {len(results)} results")

    except Exception as e:
        logger.error(f"Search failed: {e}", exc_info=True)
        click.echo(f"Error: Search failed - {e}", err=True)
        ctx.exit(1)


def _print_search_results(
    results: List[dict],
    query: str,
    show_summary: bool,
    show_distance: bool
):
    """
    Print search results in human-readable format.

    Args:
        results: List of search results
        query: Original search query
        show_summary: Whether to show summaries
        show_distance: Whether to show distance scores
    """
    if not results:
        click.echo("No results found.")
        return

    click.echo("="*60)
    click.echo(f"Search Results: \"{query}\"")
    click.echo("="*60)
    click.echo(f"Found {len(results)} matches\n")

    for i, result in enumerate(results, 1):
        # Basic info
        click.echo(f"{i}. {result.get('fileName', 'Unknown')}")
        click.echo(f"   Path: {result.get('relativePath', 'N/A')}")
        click.echo(f"   Type: {result.get('artifactType', 'N/A')}")

        # Project info
        project_id = result.get('projectId')
        if project_id:
            click.echo(f"   Project: {project_id}")

        # Frameworks
        frameworks = result.get('frameworks', [])
        if frameworks:
            click.echo(f"   Frameworks: {', '.join(frameworks)}")

        # Entities
        entities = result.get('entities', [])
        if entities:
            entity_preview = ', '.join(entities[:5])
            if len(entities) > 5:
                entity_preview += f" (+{len(entities) - 5} more)"
            click.echo(f"   Entities: {entity_preview}")

        # Summary
        if show_summary:
            summary = result.get('summary', '')
            if summary:
                click.echo(f"   Summary: {summary}")

        # Distance
        if show_distance:
            additional = result.get('_additional', {})
            distance = additional.get('distance')
            if distance is not None:
                click.echo(f"   Distance: {distance:.4f}")

        click.echo()  # Blank line between results

    click.echo("="*60)
