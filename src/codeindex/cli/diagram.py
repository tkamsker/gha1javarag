"""
Diagram Generation CLI Command

Generate architecture diagrams from analyzed codebase artifacts.
"""

import click
import sys
from pathlib import Path

from codeindex.utils.logging import get_logger
from codeindex.utils.config import get_config
from codeindex.services.diagram_generator import DiagramGenerator
from codeindex.services.weaviate_store import WeaviateStore
from codeindex.schemas import check_weaviate_health

logger = get_logger(__name__)


# Exit codes
EXIT_SUCCESS = 0
EXIT_GENERAL_ERROR = 1
EXIT_INVALID_ARGUMENTS = 2
EXIT_OUTPUT_DIR_ERROR = 5
EXIT_WEAVIATE_CONNECTION_ERROR = 6


@click.group()
def diagram():
    """Generate architecture diagrams from codebase artifacts."""
    pass


@diagram.command()
@click.option(
    '--project',
    type=str,
    help='Project name filter (optional)'
)
@click.option(
    '--output',
    '--output-dir',
    type=click.Path(),
    help='Output directory for diagrams (default: ./output)'
)
@click.option(
    '--format',
    type=click.Choice(['mermaid', 'plantuml', 'd2', 'dot'], case_sensitive=False),
    default='mermaid',
    help='Output format (default: mermaid)'
)
@click.option(
    '--style',
    type=click.Choice(['default', 'detailed', 'minimal'], case_sensitive=False),
    default='default',
    help='Diagram style (default: default)'
)
@click.option(
    '--depth',
    type=int,
    default=3,
    help='Dependency depth to include (default: 3)'
)
@click.option(
    '--open',
    is_flag=True,
    help='Open generated diagram in browser/viewer'
)
def component(project, output, format, style, depth, open):
    """Generate component architecture diagram."""
    logger.info("Starting component diagram generation")

    # Get configuration
    config = get_config()
    output_dir = Path(output) if output else Path(config.output_dir)

    # Validate output directory
    if not output_dir.exists():
        logger.error(f"Output directory does not exist: {output_dir}")
        logger.info("Run 'codeindex prd' first to generate PRD artifacts")
        sys.exit(EXIT_OUTPUT_DIR_ERROR)

    # Create diagram generator
    generator = DiagramGenerator(output_dir=output_dir)

    try:
        # Generate component diagram
        diagram_file = generator.generate_component_diagram(
            project_id=project,
            output_format=format,
            style=style,
            depth=depth
        )

        if diagram_file:
            logger.info(f"✓ Component diagram generated: {diagram_file}")

            # Open in viewer if requested
            if open:
                _open_diagram(diagram_file)

            sys.exit(EXIT_SUCCESS)
        else:
            logger.warning("No components found for diagram generation")
            logger.info("Ensure PRD artifacts exist in output directory")
            sys.exit(EXIT_GENERAL_ERROR)

    except Exception as e:
        logger.error(f"Failed to generate component diagram: {e}", exc_info=True)
        sys.exit(EXIT_GENERAL_ERROR)


@diagram.command()
@click.option(
    '--extraction-file',
    type=click.Path(exists=True),
    help='Path to extraction-results.jsonl file'
)
@click.option(
    '--output',
    '--output-dir',
    type=click.Path(),
    help='Output directory for diagrams (default: ./output)'
)
@click.option(
    '--format',
    type=click.Choice(['mermaid', 'plantuml'], case_sensitive=False),
    default='mermaid',
    help='Output format (default: mermaid)'
)
@click.option(
    '--style',
    type=click.Choice(['default', 'detailed', 'minimal'], case_sensitive=False),
    default='default',
    help='Diagram style (default: default)'
)
@click.option(
    '--open',
    is_flag=True,
    help='Open generated diagram in browser/viewer'
)
def gwt(extraction_file, output, format, style, open):
    """Generate GWT MVP architecture diagram."""
    logger.info("Starting GWT MVP diagram generation")

    # Get configuration
    config = get_config()
    output_dir = Path(output) if output else Path(config.output_dir)

    # Find extraction file if not specified
    if not extraction_file:
        # Try common locations
        candidates = [
            output_dir / "extraction-results.jsonl",
            output_dir / "gwt-validation" / "extraction-results.jsonl",
            Path("output/extraction-results.jsonl")
        ]

        for candidate in candidates:
            if candidate.exists():
                extraction_file = candidate
                logger.info(f"Using extraction file: {extraction_file}")
                break

    if not extraction_file or not Path(extraction_file).exists():
        logger.error("Extraction file not found")
        logger.info("Specify --extraction-file or ensure extraction-results.jsonl exists")
        sys.exit(EXIT_INVALID_ARGUMENTS)

    # Create diagram generator
    generator = DiagramGenerator(output_dir=output_dir)

    try:
        # Generate GWT MVP diagram
        diagram_file = generator.generate_gwt_mvp_diagram(
            extraction_file=Path(extraction_file),
            output_format=format,
            style=style
        )

        if diagram_file:
            logger.info(f"✓ GWT MVP diagram generated: {diagram_file}")

            # Open in viewer if requested
            if open:
                _open_diagram(diagram_file)

            sys.exit(EXIT_SUCCESS)
        else:
            logger.warning("No GWT artifacts found for diagram generation")
            logger.info("Ensure extraction-results.jsonl contains GWT artifacts")
            sys.exit(EXIT_GENERAL_ERROR)

    except Exception as e:
        logger.error(f"Failed to generate GWT diagram: {e}", exc_info=True)
        sys.exit(EXIT_GENERAL_ERROR)


@diagram.command()
@click.option(
    '--project',
    type=str,
    help='Project name filter (optional)'
)
@click.option(
    '--extraction-file',
    type=click.Path(exists=True),
    help='Path to extraction-results.jsonl file'
)
@click.option(
    '--output',
    '--output-dir',
    type=click.Path(),
    help='Output directory for diagrams (default: ./output)'
)
@click.option(
    '--format',
    type=click.Choice(['mermaid', 'plantuml', 'd2', 'dot'], case_sensitive=False),
    default='mermaid',
    help='Output format (default: mermaid)'
)
@click.option(
    '--open',
    is_flag=True,
    help='Open generated diagrams in browser/viewer'
)
def all(project, extraction_file, output, format, open):
    """Generate all available diagrams."""
    logger.info("Starting generation of all diagrams")

    # Get configuration
    config = get_config()
    output_dir = Path(output) if output else Path(config.output_dir)

    # Find extraction file if not specified
    if not extraction_file:
        candidates = [
            output_dir / "extraction-results.jsonl",
            output_dir / "gwt-validation" / "extraction-results.jsonl",
            Path("output/extraction-results.jsonl")
        ]

        for candidate in candidates:
            if candidate.exists():
                extraction_file = candidate
                break

    # Create diagram generator
    generator = DiagramGenerator(output_dir=output_dir)

    try:
        # Generate all diagrams
        results = generator.generate_all_diagrams(
            project_id=project,
            extraction_file=Path(extraction_file) if extraction_file else None,
            output_format=format
        )

        if results:
            logger.info(f"✓ Generated {len(results)} diagram(s):")
            for diagram_type, file_path in results.items():
                logger.info(f"  - {diagram_type}: {file_path}")

            # Open first diagram if requested
            if open and results:
                first_diagram = list(results.values())[0]
                _open_diagram(first_diagram)

            sys.exit(EXIT_SUCCESS)
        else:
            logger.warning("No diagrams could be generated")
            logger.info("Ensure PRD artifacts and extraction results exist")
            sys.exit(EXIT_GENERAL_ERROR)

    except Exception as e:
        logger.error(f"Failed to generate diagrams: {e}", exc_info=True)
        sys.exit(EXIT_GENERAL_ERROR)


def _open_diagram(file_path: Path) -> None:
    """
    Open diagram in appropriate viewer.

    Args:
        file_path: Path to diagram file
    """
    import subprocess
    import platform

    try:
        system = platform.system()

        if file_path.suffix == '.mmd':
            # Open Mermaid Live Editor in browser
            logger.info("Opening Mermaid Live Editor...")
            content = file_path.read_text(encoding='utf-8')

            # Remove code fence markers
            content = content.replace('```mermaid\n', '').replace('\n```', '')

            # URL encode and open
            import urllib.parse
            encoded = urllib.parse.quote(content)
            url = f"https://mermaid.live/edit#pako:{encoded}"

            if system == "Darwin":  # macOS
                subprocess.run(["open", url], check=False)
            elif system == "Windows":
                subprocess.run(["start", url], shell=True, check=False)
            else:  # Linux
                subprocess.run(["xdg-open", url], check=False)

        else:
            # Open file in default application
            if system == "Darwin":
                subprocess.run(["open", str(file_path)], check=False)
            elif system == "Windows":
                subprocess.run(["start", str(file_path)], shell=True, check=False)
            else:
                subprocess.run(["xdg-open", str(file_path)], check=False)

    except Exception as e:
        logger.warning(f"Could not open diagram: {e}")


if __name__ == '__main__':
    diagram()
