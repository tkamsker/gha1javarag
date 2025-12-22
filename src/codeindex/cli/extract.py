"""
Extract CLI command.

Implements the `codeindex extract` command for semantic extraction.
"""

import logging
import json
from pathlib import Path
from typing import Optional

import click

from codeindex.utils.logging import get_logger
from codeindex.services.extraction import ExtractionService
from codeindex.models.inventory import DiscoveryInventory
from codeindex.models import ArtifactType

logger = get_logger(__name__)


@click.command(name='extract')
@click.option(
    '--inventory',
    type=click.Path(exists=True, path_type=Path),
    help='Discovery inventory file (JSONL format)'
)
@click.option(
    '--output',
    type=click.Path(path_type=Path),
    help='Output file path for extraction results (JSONL format)'
)
@click.option(
    '--file',
    type=click.Path(exists=True, path_type=Path),
    help='Extract single file (requires --type)'
)
@click.option(
    '--type',
    type=str,
    help='Artifact type for single file extraction'
)
@click.option(
    '--batch-size',
    type=int,
    default=10,
    help='Number of files to process in parallel (default: 10)'
)
@click.option(
    '--limit',
    type=int,
    help='Limit number of files to extract'
)
@click.option(
    '--dry-run',
    is_flag=True,
    help='Preview extraction without writing output file'
)
@click.option(
    '--quiet',
    is_flag=True,
    help='Suppress progress output'
)
@click.option(
    '--skip-ai',
    is_flag=True,
    help='Skip AI semantic extraction (structural only)'
)
@click.pass_context
def extract_command(
    ctx,
    inventory: Optional[Path],
    output: Optional[Path],
    file: Optional[Path],
    type: Optional[str],
    batch_size: int,
    limit: Optional[int],
    dry_run: bool,
    quiet: bool,
    skip_ai: bool
):
    """
    Extract semantic information from code files.

    Uses AI (Ollama) to understand code semantics combined with structural parsing.

    Examples:

        # Extract from discovery inventory
        codeindex extract --inventory discovery-inventory.jsonl

        # Extract single file
        codeindex extract --file src/Main.java --type JAVA_SOURCE

        # Save extraction results
        codeindex extract --inventory discovery.jsonl --output extraction.jsonl

        # Preview without writing
        codeindex extract --inventory discovery.jsonl --dry-run

        # Limit extraction to 100 files
        codeindex extract --inventory discovery.jsonl --limit 100
    """
    cli_context = ctx.obj
    config = cli_context.config
    output_format = cli_context.format

    # Validate inputs
    if file and not type:
        click.echo("Error: --type is required when using --file", err=True)
        ctx.exit(1)

    if not file and not inventory:
        click.echo("Error: Either --file or --inventory must be specified", err=True)
        ctx.exit(1)

    # Determine output path
    if not output and not dry_run:
        output = config.output_dir / "extraction-results.jsonl"

    # Create extraction service
    service = ExtractionService(config=config)

    # Check Ollama availability
    if not skip_ai:
        if not service.ollama_client.health_check():
            if output_format == 'text':
                click.echo("⚠ Warning: Ollama is not available. Will use structural extraction only.", err=True)
                click.echo("  Start Ollama with: ollama serve", err=True)
            logger.warning("Ollama unavailable, falling back to structural extraction")

    try:
        if file:
            # Single file extraction
            _extract_single_file(
                service, file, type, output, output_format, dry_run, quiet
            )
        else:
            # Batch extraction from inventory
            _extract_from_inventory(
                service, inventory, output, output_format,
                dry_run, quiet, limit, batch_size
            )

        logger.info("Extraction complete")

    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        ctx.exit(1)
    except Exception as e:
        logger.error(f"Extraction failed: {e}", exc_info=True)
        click.echo(f"Error: Extraction failed - {e}", err=True)
        ctx.exit(1)


def _extract_single_file(
    service: ExtractionService,
    file_path: Path,
    artifact_type_str: str,
    output: Optional[Path],
    output_format: str,
    dry_run: bool,
    quiet: bool
):
    """Extract single file."""
    # Parse artifact type
    try:
        artifact_type = ArtifactType[artifact_type_str]
    except KeyError:
        click.echo(f"Error: Invalid artifact type: {artifact_type_str}", err=True)
        click.echo(f"Valid types: {', '.join(t.name for t in ArtifactType)}", err=True)
        return

    if not quiet and output_format == 'text':
        click.echo(f"Extracting {artifact_type.value}: {file_path}")

    # Extract
    result = service.extract_file(file_path, artifact_type)

    # Output
    if output_format == 'json':
        click.echo(json.dumps(result.to_dict(), indent=2, default=str))
    else:
        _print_extraction_result(result)

    # Save to file
    if not dry_run and output:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open('w') as f:
            json.dump(result.to_dict(), f, default=str)
            f.write('\n')

        if output_format == 'text':
            click.echo(f"\n✓ Results saved to: {output}")


def _extract_from_inventory(
    service: ExtractionService,
    inventory_path: Path,
    output: Optional[Path],
    output_format: str,
    dry_run: bool,
    quiet: bool,
    limit: Optional[int],
    batch_size: int
):
    """Extract from discovery inventory."""
    if not quiet and output_format == 'text':
        click.echo(f"Loading inventory from {inventory_path}...")

    # Load inventory
    inventory = DiscoveryInventory.load_jsonl(inventory_path)

    if not quiet and output_format == 'text':
        click.echo(f"Found {inventory.total_files} files to extract")
        if limit:
            click.echo(f"Limiting to {limit} files")

    # Build file list from inventory
    files_to_extract = []

    for project in inventory.projects:
        project_path = Path(project.get('path', ''))

        for file_entry in project.get('files', []):
            file_path = Path(file_entry['path'])
            artifact_type = ArtifactType[file_entry['type']]

            files_to_extract.append((file_path, artifact_type))

            if limit and len(files_to_extract) >= limit:
                break

        if limit and len(files_to_extract) >= limit:
            break

    total_files = len(files_to_extract)

    if total_files == 0:
        if output_format == 'text':
            click.echo("No files to extract")
        return

    # Extract files
    results = []
    processed = 0

    for i in range(0, total_files, batch_size):
        batch = files_to_extract[i:i + batch_size]

        if not quiet and output_format == 'text':
            click.echo(f"Processing batch {i // batch_size + 1} ({len(batch)} files)...")

        batch_results = service.extract_batch(batch)
        results.extend(batch_results)

        processed += len(batch)

        if not quiet and output_format == 'text':
            click.echo(f"  Progress: {processed}/{total_files} files")

    # Output results
    if output_format == 'json':
        output_data = {
            'total_files': total_files,
            'results': [r.to_dict() for r in results]
        }
        click.echo(json.dumps(output_data, indent=2, default=str))
    else:
        _print_extraction_summary(results, inventory)

    # Save to file
    if not dry_run and output:
        output.parent.mkdir(parents=True, exist_ok=True)

        with output.open('w') as f:
            # Write metadata header
            metadata = {
                'extraction_timestamp': results[0].extracted_at.isoformat() if results else None,
                'total_files': total_files,
                'inventory_source': str(inventory_path)
            }
            f.write(json.dumps(metadata, default=str) + '\n')

            # Write results
            for result in results:
                f.write(json.dumps(result.to_dict(), default=str) + '\n')

        if output_format == 'text':
            click.echo(f"\n✓ Results saved to: {output}")


def _print_extraction_result(result):
    """Print single extraction result."""
    click.echo("\n" + "="*60)
    click.echo("Extraction Result")
    click.echo("="*60)
    click.echo(f"File: {result.file_path}")
    click.echo(f"Type: {result.artifact_type.value if hasattr(result.artifact_type, 'value') else result.artifact_type}")

    if result.semantic_data:
        click.echo(f"\nSummary: {result.semantic_data.get('summary', 'N/A')}")

        if result.semantic_data.get('entities'):
            click.echo(f"Entities: {', '.join(result.semantic_data['entities'][:5])}")

        if result.semantic_data.get('frameworks'):
            click.echo(f"Frameworks: {', '.join(result.semantic_data['frameworks'])}")

    if result.error:
        click.echo(f"\n⚠ Error: {result.error}")


def _print_extraction_summary(results, inventory):
    """Print extraction summary."""
    click.echo("\n" + "="*60)
    click.echo("Extraction Summary")
    click.echo("="*60)
    click.echo(f"Total files: {len(results)}")

    # Count by type
    type_counts = {}
    for result in results:
        artifact_type = result.artifact_type.value if hasattr(result.artifact_type, 'value') else str(result.artifact_type)
        type_counts[artifact_type] = type_counts.get(artifact_type, 0) + 1

    click.echo("\nFiles by type:")
    for artifact_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        click.echo(f"  {artifact_type:20s}: {count:>6d}")

    # Count errors
    errors = sum(1 for r in results if r.error)
    if errors > 0:
        click.echo(f"\n⚠ Errors: {errors}")

    # Frameworks detected
    frameworks = set()
    for result in results:
        if result.semantic_data and result.semantic_data.get('frameworks'):
            frameworks.update(result.semantic_data['frameworks'])

    if frameworks:
        click.echo(f"\nFrameworks detected: {', '.join(sorted(frameworks))}")

    # T093: Count DTOs classified
    dto_count = 0
    for result in results:
        if result.semantic_data and result.semantic_data.get('is_dto'):
            dto_count += 1

    if dto_count > 0:
        click.echo(f"\nDTOs classified: {dto_count}")

    # T030: Display timeout metrics summary
    from codeindex.utils.metrics import get_metrics_collector
    metrics_collector = get_metrics_collector()
    timeout_summary = metrics_collector.get_timeout_summary()

    if timeout_summary['total_files'] > 0:
        click.echo("\n" + "-"*60)
        click.echo("Timeout Handling Summary")
        click.echo("-"*60)
        click.echo(f"Total files processed: {timeout_summary['total_files']}")
        click.echo(f"Timeouts encountered: {timeout_summary['timeout_count']}")
        click.echo(f"Successful retries: {timeout_summary['retry_success']}")
        click.echo(f"Fallback used: {timeout_summary['fallback_count']}")
        click.echo(f"Failed extractions: {timeout_summary['failed_count']}")

        if timeout_summary['avg_retry_count'] > 0:
            click.echo(f"Avg retry count: {timeout_summary['avg_retry_count']:.2f}")
        if timeout_summary['avg_timeout_duration'] > 0:
            click.echo(f"Avg timeout duration: {timeout_summary['avg_timeout_duration']:.1f}s")
        logger.info(f"Classified {dto_count} Data Transfer Objects")

    # T044: Display FK extraction metrics
    fk_summary = metrics_collector.get_fk_summary()

    if fk_summary.get('total_extracted', 0) > 0:
        click.echo("\n" + "-"*60)
        click.echo("Foreign Key Extraction Summary")
        click.echo("-"*60)
        click.echo(f"Total FK extracted: {fk_summary['total_extracted']}")
        click.echo(f"Validated FK: {fk_summary['validated_count']}")
        click.echo(f"Failed validation: {fk_summary['failed_validation']}")

        # Sources breakdown
        sources = fk_summary.get('sources_breakdown', {})
        if sources:
            click.echo("\nFK by source:")
            for source, count in sorted(sources.items()):
                click.echo(f"  {source}: {count}")
