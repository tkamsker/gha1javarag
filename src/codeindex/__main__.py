"""
Main CLI entry point for Java Codebase Indexer Pipeline.

Usage: python -m codeindex [COMMAND] [OPTIONS]
       codeindex [COMMAND] [OPTIONS]  (after pip install)
"""
import sys
import click
from pathlib import Path
from typing import Optional

from .utils.config import Config, get_config
from .utils.logging import setup_logging, get_logger


# ==============================================================================
# CLI Context
# ==============================================================================

class CLIContext:
    """
    Context object passed to all CLI commands.

    Contains shared configuration and logger instances.
    """

    def __init__(self, config: Config, logger, verbose: bool = False, format: str = "text"):
        """
        Initialize CLI context.

        Args:
            config: Configuration instance
            logger: Logger instance
            verbose: Verbose mode flag
            format: Output format (text or json)
        """
        self.config = config
        self.logger = logger
        self.verbose = verbose
        self.format = format


# ==============================================================================
# Main CLI Group
# ==============================================================================

@click.group()
@click.option(
    '--config',
    type=click.Path(exists=True, path_type=Path),
    help='Path to .env configuration file'
)
@click.option(
    '--log-level',
    type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR'], case_sensitive=False),
    help='Logging level (default: INFO or from LOG_LEVEL env var)'
)
@click.option(
    '--format',
    type=click.Choice(['text', 'json'], case_sensitive=False),
    default='text',
    help='Output format (default: text)'
)
@click.option(
    '--verbose',
    '-v',
    is_flag=True,
    help='Enable verbose output (sets log level to DEBUG)'
)
@click.pass_context
def main(ctx, config: Optional[Path], log_level: Optional[str], format: str, verbose: bool):
    """
    Java Codebase Indexer Pipeline - Discover, analyze, and index Java codebases with AI.

    This CLI provides commands to:
    - discover: Scan directory tree to find Maven projects
    - extract: Use AI to understand file semantics
    - index: Store artifacts in Weaviate for search
    - search: Semantic search over indexed code
    - status: View indexing statistics
    """
    # Setup logging
    logger = setup_logging(level=log_level, verbose=verbose)

    # Load configuration
    cfg = get_config(config_file=config)

    # Create CLI context
    ctx.obj = CLIContext(
        config=cfg,
        logger=logger,
        verbose=verbose,
        format=format
    )

    # Log configuration (debug level)
    if verbose:
        logger.debug("Configuration loaded:")
        for key, value in cfg.to_dict().items():
            logger.debug(f"  {key}: {value}")


# ==============================================================================
# Command Imports
# ==============================================================================

# Import and register discover command (Phase 3)
from .cli.discover import discover_command
main.add_command(discover_command, name='discover')

# Import and register extract command (Phase 4)
from .cli.extract import extract_command
main.add_command(extract_command, name='extract')

# Import and register index command (Phase 5)
from .cli.index import index_command
main.add_command(index_command, name='index')

# Import and register search command (Phase 5)
from .cli.search import search_command
main.add_command(search_command, name='search')

# Import and register status command (Phase 6)
from .cli.status import status_command
main.add_command(status_command, name='status')


# ==============================================================================
# Entry Point
# ==============================================================================

if __name__ == '__main__':
    main()
