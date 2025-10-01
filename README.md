# Java Codebase Analysis Tool

A Python application that analyzes Java/JSP/GWT codebases, extracts metadata and requirements, and stores/searches them in Weaviate vector database.

## Features

- **Multi-language Support**: Analyzes Java, JSP, XML, HTML, JavaScript, CSS, and GWT files
- **Vector Database Integration**: Uses Weaviate for semantic search and storage
- **Hierarchical Chunking**: Breaks down code into manageable chunks by repository, module, file, class, and method
- **Rich Metadata Extraction**: Extracts classes, methods, imports, annotations, business rules, and more
- **Requirements Generation**: Automatically generates requirements documentation
- **Multiple AI Providers**: Supports OpenAI, Ollama, and Anthropic for AI-assisted processing
- **Comprehensive Reporting**: Generates JSON catalogs and processing reports

## Quick Start

1. **Clone and Setup**:
   ```bash
   git clone <repository-url>
   cd java-codebase-analysis
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start Weaviate** (using Docker):
   ```bash
   docker run -p 8080:8080 -p 50051:50051 \
     -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
     -e PERSISTENCE_DATA_PATH='/var/lib/weaviate' \
     semitechnologies/weaviate:latest
   ```

4. **Run Analysis**:
   ```bash
   # Index your Java codebase
   python -m src.cli index
   
   # Generate requirements documentation
   python -m src.cli requirements
   
   # Query the indexed data
   python -m src.cli query
   ```

## Configuration

The tool uses a `.env` file for configuration. Copy `.env.example` to `.env` and configure:

### Required Settings

- `JAVA_SOURCE_DIR`: Path to your Java source code directory
- `OUTPUT_DIR`: Where to store generated reports and logs

### Weaviate Settings

- `WEAVIATE_URL`: Weaviate instance URL (default: http://localhost:8080)
- `WEAVIATE_API_KEY`: API key (leave empty for anonymous access)
- `EMBEDDING_PROVIDER`: Either `weaviate_ollama` or `client`
- `EMBEDDING_MODEL`: Model name for embeddings

### AI Provider Settings

- `AI_PROVIDER`: Choose from `openai`, `ollama`, or `anthropic`
- Configure the respective API keys and settings

## Project Structure

```
src/
├── env_loader.py          # Environment configuration
├── discovery.py           # Project discovery and file indexing
├── parsers/               # Language-specific parsers
│   ├── java_parser.py
│   ├── jsp_parser.py
│   ├── xml_sql_parser.py
│   ├── html_js_parser.py
│   └── gwt_parser.py
├── chunking.py            # Hierarchical chunking strategy
├── metadata.py            # Metadata extraction and management
├── weaviate_client.py     # Weaviate database operations
├── upsert.py              # Data insertion with retry logic
├── reporting.py           # Report generation
├── requirements_gen/      # Requirements documentation
└── cli.py                 # Command-line interface
```

## Usage

### Two-step workflow (per iteration10.md)

Step 1: Analyze and export consolidated JSON (Weaviate optional)

```bash
# Pure JSON export (no Weaviate upserts)
python -m src.cli analyze --no-upsert

# Optional: also upsert to Weaviate while analyzing
python -m src.cli analyze
```

This writes a consolidated metadata file to `OUTPUT_DIR/consolidated_metadata.json` and a processing report.

Step 2: Generate requirements from the consolidated JSON

```bash
python -m src.cli requirements
```

Outputs are written under `OUTPUT_DIR/requirements/` with per-project files (`database`, `backend`, `ui`) and a `_master.md` index.

#### Shell helpers

You can also use the provided shell helpers for a streamlined two-step run:

```bash
# Step 1: Analyze and export consolidated JSON (env STEP1_NO_UPSERT=1 to skip Weaviate upserts)
./step1.sh

# Step 2: Generate requirements from the JSON
./step2.sh

# Or run the full iteration wrapper, which prefers step scripts if present
./run_iteration.sh
```

`step1.sh` and `step2.sh` bootstrap the virtualenv, install dependencies, and run the corresponding CLI commands. The iteration wrapper will automatically detect and use them when available.

### Legacy single-step indexing

You can still run the combined indexing flow (schema + upserts + report):

```bash
python -m src.cli index
```

Use this if you want to push vectors to Weaviate explicitly outside the two-step analyze flow.

### Indexing (Step 1)

```bash
python -m src.cli index
```

This will:
1. Discover all projects in `JAVA_SOURCE_DIR`
2. Parse and extract metadata from all supported files
3. Create hierarchical chunks
4. Store everything in Weaviate
5. Generate JSON catalogs and reports

### Requirements Generation (Step 2)

```bash
python -m src.cli requirements
```

This will:
1. Query indexed data from Weaviate
2. Generate requirements documentation by architectural layer
3. Create cross-linked requirements documents

### Querying

```bash
python -m src.cli query
```

Interactive query interface for searching the indexed data.

### Statistics

```bash
python -m src.cli stats
```

Show statistics about the indexed data.

## Output Structure

```
output/
├── projects/              # Per-project summaries
│   ├── project1.summary.json
│   └── project2.summary.json
├── requirements/          # Generated requirements
│   ├── _master.md
│   ├── database/
│   ├── backend/
│   └── ui/
├── logs/                  # Processing logs
│   └── app.log.jsonl
├── catalog.index.json     # Global catalog
└── processing_report.json # Final processing report
```

## Weaviate Collections

The tool creates the following collections in Weaviate:

- **JavaCodeChunks**: Core code and configuration chunks
- **DocumentationChunks**: Comments, README, and documentation
- **BusinessRules**: Validation rules, workflows, and domain entities
- **IntegrationPoints**: APIs, database interactions, and external systems
- **UIComponents**: GWT and general UI components
- **NavigationFlows**: User navigation and flow patterns

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black src/
flake8 src/
mypy src/
```

### Adding New Parsers

1. Create a new parser in `src/parsers/`
2. Implement the `parse_file(file_path, content)` method
3. Add the parser to `src/parsers/__init__.py`
4. Update the CLI to use the new parser

## Troubleshooting

### Common Issues

1. **Weaviate Connection Failed**: Ensure Weaviate is running and accessible
2. **File Permission Errors**: Check file permissions for source directory
3. **Memory Issues**: Reduce `WEAVIATE_BATCH_SIZE` for large files
4. **Rate Limiting**: Adjust `RATE_LIMIT_ENV` setting

### Logs

Check the logs in `output/logs/app.log.jsonl` for detailed error information.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

[Add your license information here]



source venv/bin/activate

python -m src.cli stats


#### 

Added heuristic classification (src/metadata_classification.py) and wired it into analyze so each file in consolidated_metadata.json now has enriched fields (layer, component, tech, flags).
Ran analyze --no-upsert; verified JSON contains enhanced metadata for files.
You can now run:

Step 1: python -m src.cli analyze --no-upsert

Step 2: python -m src.cli requirements

If you want, I can enhance requirements generation to leverage these new fields next.