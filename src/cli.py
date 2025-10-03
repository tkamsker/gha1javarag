"""
Command-line interface for the Java codebase analysis tool.
"""

import click
import logging
import sys
from pathlib import Path
from typing import Optional

from .env_loader import load_config
from .discovery import ProjectDiscovery
from .parsers import JavaParser, JSPParser, XMLSQLParser, HTMLJSParser, GWTParser
from .chunking import ChunkingStrategy
from .metadata import MetadataExtractor
from .weaviate_client import WeaviateClient
from .reporting import ReportingManager
from .metadata_classification import classify_file
from .llm_client import LLMClient
from .prompts import prompt_for_file


def setup_logging(level: str, verbose: bool):
    """Setup logging configuration."""
    log_level = getattr(logging, level.upper(), logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Setup console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    
    if verbose:
        # Enable debug logging for specific modules
        logging.getLogger('src').setLevel(logging.DEBUG)


@click.group()
@click.option('--config', '-c', help='Path to .env configuration file')
@click.option('--log-level', default='INFO', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']))
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.pass_context
def cli(ctx, config: Optional[str], log_level: str, verbose: bool):
    """Java Codebase Analysis Tool - Analyze Java/JSP/GWT codebases and store in Weaviate."""
    # Setup logging
    setup_logging(log_level, verbose)
    
    # Load configuration
    try:
        config_obj = load_config(config)
        ctx.ensure_object(dict)
        ctx.obj['config'] = config_obj
    except Exception as e:
        click.echo(f"Error loading configuration: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def index(ctx):
    """Index Java projects and store in Weaviate (Step 1)."""
    config = ctx.obj['config']
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting project indexing...")
        
        # Initialize components
        discovery = ProjectDiscovery(config)
        weaviate_client = WeaviateClient(config)
        
        # Create Weaviate schemas
        logger.info("Creating Weaviate schemas...")
        weaviate_client.create_schemas()
        
        # Discover projects
        logger.info("Discovering projects...")
        projects = discovery.discover_projects()
        logger.info(f"Found {len(projects)} projects")
        
        # Create reporting manager
        reporting = ReportingManager(config)
        
        # Process each project
        total_files = 0
        total_chunks = 0
        
        for project in projects:
            logger.info(f"Processing project: {project.name}")
            
            # Process files in project
            project_chunks = process_project(project, config, weaviate_client, reporting)
            total_chunks += project_chunks
            total_files += project.total_files
            
            logger.info(f"Processed {project.total_files} files, created {project_chunks} chunks")
        
        # Generate final reports
        logger.info("Generating reports...")
        reporting.generate_final_report(total_files, total_chunks)
        
        # Get Weaviate statistics
        stats = weaviate_client.get_all_collection_stats()
        logger.info(f"Weaviate statistics: {stats}")
        
        logger.info("Indexing completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during indexing: {e}")
        sys.exit(1)
    finally:
        if 'weaviate_client' in locals():
            weaviate_client.close()


@cli.command(name='analyze')
@click.option('--no-upsert', is_flag=True, default=False, help='Skip Weaviate upserts; export consolidated JSON only')
@click.option('--llm-enrich', is_flag=True, default=True, help='Use LLM prompts to enrich per-file metadata')
@click.pass_context
def analyze(ctx, no_upsert: bool, llm_enrich: bool):
    """Step 1 per iteration10.md: analyze codebase, export consolidated JSON; Weaviate optional."""
    config = ctx.obj['config']
    logger = logging.getLogger(__name__)

    try:
        logger.info("Starting analysis (Step 1) ...")
        discovery = ProjectDiscovery(config)
        projects = discovery.discover_projects()
        logger.info(f"Found {len(projects)} projects")

        reporting = ReportingManager(config)
        llm: LLMClient | None = None
        if llm_enrich:
            llm = LLMClient(config)

        # Build catalogs
        catalog = discovery.create_project_catalog(projects)

        # Optionally upsert chunks to Weaviate but not required for JSON export
        weaviate_client = None
        if not no_upsert:
            weaviate_client = WeaviateClient(config)
            logger.info("Creating Weaviate schemas...")
            weaviate_client.create_schemas()

        # Collect per-project file lists and enrich with heuristic classification
        projects_map = {}
        total_files = 0
        total_chunks = 0
        for project in projects:
            projects_map[project.name] = {
                'name': project.name,
                'path': project.path,
                'total_files': project.total_files,
                'total_size_bytes': project.total_size,
                'file_list': [],
                'hierarchy': {
                    'repository': project.name,
                    'modules': []
                }
            }

            # If upserting, process and upsert similar to index path
            if weaviate_client is not None:
                created = process_project(project, config, weaviate_client, reporting)
                total_chunks += created
            total_files += project.total_files

            # Enrich JSON for each file
            # Build a naive module grouping by top-level package/dir
            module_map = {}
            for f in project.files:
                try:
                    content = ""
                    # Only sample content lightly to keep memory reasonable
                    with open(f.file_path, 'r', encoding='utf-8', errors='ignore') as fh:
                        content = fh.read(40000)  # 40KB sample
                except Exception:
                    content = ""

                # Heuristic classifier first
                enhanced = classify_file(f.relative_path, f.language, content)

                # LLM enrichment per iteration10 prompts
                llm_meta = {}
                if llm is not None:
                    p = prompt_for_file(f.language, project.name, f.relative_path, content)
                    llm_meta = llm.complete_json(p['user'], system=p['system'], max_tokens=1800) or {}

                file_record = {
                    'path': f.relative_path,
                    'language': f.language,
                    'size_bytes': f.size_bytes,
                    'sha256': f.sha256,
                    'last_modified': f.last_modified.isoformat(),
                    'enhanced_ai_analysis': {
                        'file_classification': enhanced,
                        'purpose': enhanced.get('primary_purpose', 'Source file')
                    },
                    'llm_metadata': llm_meta
                }
                projects_map[project.name]['file_list'].append(file_record)

                # Module key by first directory segment
                module_key = (f.relative_path.split('/')[:1] or ['root'])[0]
                module_map.setdefault(module_key, []).append(file_record)

            # Emit hierarchy modules with file lists
            for module_name, files_list in module_map.items():
                projects_map[project.name]['hierarchy']['modules'].append({
                    'name': module_name,
                    'files': [fl['path'] for fl in files_list]
                })

        # Write consolidated JSON for Step 2
        reporting.write_consolidated_metadata(catalog, projects_map)

        # Also write intermediate hierarchical JSON for Step 3
        intermediate = {
            'generation': 'step2_intermediate',
            'projects': projects_map,
        }
        from pathlib import Path
        inter_path = Path(config.output_dir) / 'intermediate_step2.json'
        import json
        with open(inter_path, 'w', encoding='utf-8') as fh:
            json.dump(intermediate, fh, indent=2)

        # Final processing report
        reporting.generate_final_report(total_files, total_chunks)

        logger.info("Analysis completed successfully!")

    except Exception as e:
        logger.error(f"Error during analyze: {e}")
        sys.exit(1)
    finally:
        if 'weaviate_client' in locals() and weaviate_client is not None:
            weaviate_client.close()


@cli.command()
@click.option('--parallel/--sequential', default=True, help='Enable parallel processing of projects')
@click.option('--max-workers', default=3, help='Maximum number of parallel workers')
@click.option('--incremental', is_flag=True, help='Run incremental processing (skip existing outputs)')
@click.option('--force', is_flag=True, help='Force regenerate all outputs (used with --incremental)')
@click.pass_context
def step3(ctx, parallel: bool, max_workers: int, incremental: bool, force: bool):
    """Generate LLM+Weaviate-driven requirements (Step 3) - Refactored Implementation."""
    config = ctx.obj['config']
    logger = logging.getLogger(__name__)

    try:
        from .step3_processor import Step3Processor
        
        logger.info("Starting Step 3 requirements synthesis (refactored)...")
        processor = Step3Processor(config)
        
        if incremental:
            processor.run_incremental(force_regenerate=force)
        else:
            processor.run(parallel=parallel, max_workers=max_workers)
        
        logger.info("Step 3 synthesis completed successfully")

    except Exception as e:
        logger.error(f"Error in step3: {e}")
        sys.exit(1)

@cli.command()
@click.pass_context
def requirements(ctx):
    """Generate requirements documentation (Step 2)."""
    config = ctx.obj['config']
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting requirements generation...")
        
        # Initialize components
        reporting = ReportingManager(config)
        
        # Generate requirements
        reporting.generate_requirements()
        
        logger.info("Requirements generation completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during requirements generation: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def query(ctx):
    """Query the indexed data in Weaviate."""
    config = ctx.obj['config']
    logger = logging.getLogger(__name__)
    
    try:
        weaviate_client = WeaviateClient(config)
        
        # Interactive query mode
        while True:
            query_text = click.prompt("Enter your query (or 'quit' to exit)", default="quit")
            if query_text.lower() in ['quit', 'exit', 'q']:
                break
            
            # Query all collections
            collections = ['JavaCodeChunks', 'DocumentationChunks', 'BusinessRules', 
                          'IntegrationPoints', 'UIComponents', 'NavigationFlows']
            
            for collection in collections:
                results = weaviate_client.query_chunks(collection, query_text, limit=5)
                if results:
                    click.echo(f"\n--- {collection} ---")
                    for i, result in enumerate(results, 1):
                        click.echo(f"{i}. {result.get('filePath', 'Unknown')} - {result.get('className', '')}")
                        click.echo(f"   {result.get('content', '')[:200]}...")
                        click.echo()
        
        weaviate_client.close()
        
    except Exception as e:
        logger.error(f"Error during query: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def stats(ctx):
    """Show statistics about the indexed data."""
    config = ctx.obj['config']
    logger = logging.getLogger(__name__)
    
    try:
        weaviate_client = WeaviateClient(config)
        
        # Get statistics
        stats = weaviate_client.get_all_collection_stats()
        
        click.echo("Weaviate Collection Statistics:")
        click.echo("=" * 40)
        
        for collection, data in stats.items():
            if collection in ['total_count', 'timestamp']:
                continue
            
            count = data.get('count', 0)
            click.echo(f"{collection}: {count} objects")
        
        click.echo(f"\nTotal objects: {stats.get('total_count', 0)}")
        click.echo(f"Generated at: {stats.get('timestamp', 'Unknown')}")
        
        weaviate_client.close()
        
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        sys.exit(1)


def process_project(project, config, weaviate_client, reporting):
    """Process a single project and return number of chunks created."""
    logger = logging.getLogger(__name__)
    
    # Initialize parsers
    parsers = {
        'java': JavaParser(),
        'jsp': JSPParser(),
        'xml': XMLSQLParser(),
        'html': HTMLJSParser(),
        'javascript': HTMLJSParser(),
        'css': HTMLJSParser(),
        'gwt_java': GWTParser(),
        'gwt_uibinder': GWTParser(),
        'gwt_config': GWTParser()
    }
    
    chunking_strategy = ChunkingStrategy(config)
    metadata_extractor = MetadataExtractor(config)
    
    total_chunks = 0
    
    for file_info in project.files:
        try:
            # Read file content
            with open(file_info.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Parse file
            parser = parsers.get(file_info.language, parsers['java'])
            parsed_data = parser.parse_file(file_info.file_path, content)
            
            # Extract metadata
            file_metadata = metadata_extractor.extract_metadata(
                file_info.file_path, content, parsed_data
            )
            
            # Create chunks
            chunks = chunking_strategy.chunk_file(
                file_info.file_path, content, parsed_data
            )
            
            # Determine collection for chunks
            collection_name = determine_collection(file_metadata.language, chunks[0].chunk_kind if chunks else 'file')
            
            # Convert chunks to Weaviate objects
            weaviate_objects = []
            for chunk in chunks:
                weaviate_object = metadata_extractor.create_weaviate_object(
                    chunk, file_metadata, collection_name
                )
                weaviate_objects.append(weaviate_object)
            
            # Upsert to Weaviate
            if weaviate_objects:
                result = weaviate_client.upsert_chunks(weaviate_objects, collection_name)
                if result['success']:
                    total_chunks += result['count']
                else:
                    logger.error(f"Failed to upsert chunks for {file_info.file_path}: {result['errors']}")
            
            # Log progress
            reporting.log_file_processed(file_info.file_path, len(chunks))
        
        except Exception as e:
            logger.error(f"Error processing file {file_info.file_path}: {e}")
            reporting.log_file_error(file_info.file_path, str(e))
            continue
    
    return total_chunks


def determine_collection(language: str, chunk_kind: str) -> str:
    """Determine the appropriate Weaviate collection for a chunk."""
    # Map chunk types to collections
    if chunk_kind in ['ui', 'navigation']:
        return 'UIComponents'
    elif chunk_kind == 'integration':
        return 'IntegrationPoints'
    elif chunk_kind in ['business', 'validation']:
        return 'BusinessRules'
    elif chunk_kind in ['documentation', 'comment']:
        return 'DocumentationChunks'
    else:
        return 'JavaCodeChunks'


if __name__ == '__main__':
    cli()
