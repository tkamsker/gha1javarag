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
from codeindex.services.gwt_navigation_analyzer import GWTNavigationAnalyzer
from codeindex.models.project_configuration import ProjectConfiguration
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
    help='Project subdirectory within source directory for focused analysis (e.g., "my-service" or "parent/child")'
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
@click.option(
    '--dependency-depth',
    type=int,
    default=1,
    help='Maximum depth for Maven dependency resolution (default: 1)'
)
@click.option(
    '--workspace-root',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    help='Workspace root directory for sibling dependency search (Feature 005). Auto-detected if not specified.'
)
@click.option(
    '--search-siblings/--no-search-siblings',
    default=True,
    help='Enable/disable sibling directory search for dependencies (default: enabled)'
)
@click.pass_context
def discover_command(
    ctx,
    source_dir: Optional[Path],
    output: Optional[Path],
    project: Optional[str],
    dry_run: bool,
    quiet: bool,
    dependency_depth: int,
    workspace_root: Optional[Path],
    search_siblings: bool
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

        # Scope to specific project subdirectory (monorepo)
        codeindex discover --project my-service

        # Scope to nested project
        codeindex discover --project services/backend/api

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

    # Create project configuration for scoped analysis (T071, T076-T077, T080)
    try:
        proj_config = ProjectConfiguration(
            java_source_dir=source_dir,
            project_subdirectory=project,
            dependency_depth=dependency_depth
        )
    except ValueError as e:
        # T077: Clear error message for invalid project directory (FR-024)
        click.echo(f"Error: {e}", err=True)
        ctx.exit(1)

    # T080: Log resolved base directory (FR-027)
    effective_dir = proj_config.effective_base_dir
    if project:
        logger.info(f"Project-scoped analysis: {project}")
        logger.info(f"  Base directory: {source_dir}")
        logger.info(f"  Effective directory: {effective_dir}")
        if not quiet and output_format == 'text':
            click.echo(f"Project scope: {project}")
            click.echo(f"Analyzing: {effective_dir}")
    else:
        logger.info(f"Discovering Maven projects in {effective_dir}")

    # Create discovery service
    service = DiscoveryService(config=config, dependency_depth=dependency_depth)

    try:
        # Show progress message
        if not quiet and output_format == 'text':
            if not project:
                click.echo(f"Discovering Maven projects in {effective_dir}...")
            if dependency_depth > 0:
                click.echo(f"Dependency resolution depth: {dependency_depth}")
                if search_siblings:
                    if workspace_root:
                        click.echo(f"Workspace root (sibling search): {workspace_root}")
                    else:
                        click.echo(f"Sibling search enabled (auto-detect workspace root)")

        # Generate discovery inventory from effective directory
        # T078: Pass source_dir as dependency_base_dir for monorepo support
        # Feature 005: Pass workspace_root and search_siblings for sibling dependency search
        inventory = service.generate_inventory(
            root_directory=effective_dir,
            dependency_base_dir=source_dir if project else None,
            workspace_root=workspace_root,
            search_siblings=search_siblings
        )

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
                total_deps_resolved = 0
                total_deps_not_found = 0
                for proj in inventory.projects:
                    artifact_id = proj.get('artifact_id') or 'unknown'
                    version = proj.get('version') or 'unknown'
                    file_count = proj.get('file_count', 0)
                    click.echo(f"  • {artifact_id:30s} v{version:15s} ({file_count} files)")

                    # T093: Track dependency resolution metrics
                    if 'dependency_resolution' in proj and proj['dependency_resolution']:
                        dep_res = proj['dependency_resolution']
                        total_deps_resolved += dep_res.get('resolved', 0)
                        total_deps_not_found += dep_res.get('not_found', 0)

                # T093: Log dependency resolution metrics
                if dependency_depth > 0 and total_deps_resolved > 0:
                    click.echo(f"\nDependency Resolution:")
                    click.echo(f"  Resolved: {total_deps_resolved}")
                    if total_deps_not_found > 0:
                        click.echo(f"  Not found: {total_deps_not_found}")
                    logger.info(f"Resolved {total_deps_resolved} dependencies, {total_deps_not_found} not found")

        # T065: GWT Navigation Analysis Phase
        # Check for GWT entry points (index.html, index.jsp) in discovered files
        navigation_graph = None
        entry_point_files = []
        for file_artifact in inventory.file_artifacts:
            file_path = Path(file_artifact.get('file_path', ''))
            file_name = file_path.name.lower()
            if file_name in ['index.html', 'index.jsp']:
                entry_point_files.append(file_path)

        if entry_point_files:
            if not quiet and output_format == 'text':
                click.echo(f"\n{'='*60}")
                click.echo("GWT Navigation Analysis")
                click.echo("="*60)
                click.echo(f"Found {len(entry_point_files)} GWT entry point(s)")

            # Analyze navigation starting from first entry point
            try:
                analyzer = GWTNavigationAnalyzer(source_dir=effective_dir)
                navigation_graph = analyzer.build_navigation_graph(
                    index_file=entry_point_files[0],
                    source_dir=effective_dir
                )

                if output_format == 'text':
                    click.echo(f"Entry point: {entry_point_files[0].name}")
                    click.echo(f"Modules discovered: {len(navigation_graph.nodes)}")
                    click.echo(f"Max depth: {navigation_graph.max_depth}")
                    click.echo(f"Entry modules: {len(navigation_graph.metadata.get('entry_modules', []))}")

                    # Save navigation graph to file
                    if not dry_run:
                        nav_graph_file = output.parent / "navigation-graph.json"
                        nav_graph_file.write_text(
                            json.dumps(navigation_graph.to_dict(), indent=2),
                            encoding='utf-8'
                        )
                        click.echo(f"✓ Navigation graph saved to: {nav_graph_file}")
                        logger.info(f"Saved navigation graph to {nav_graph_file}")

                logger.info(
                    f"Navigation analysis complete: {len(navigation_graph.nodes)} modules, "
                    f"max depth {navigation_graph.max_depth}"
                )

            except Exception as e:
                logger.warning(f"Navigation analysis failed: {e}", exc_info=True)
                if output_format == 'text':
                    click.echo(f"⚠ Navigation analysis failed: {e}")

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
