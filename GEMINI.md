# Gemini CLI Project Directives

## File Discovery and Analysis
- Always use the `JAVA_SOURCE_DIR` from `.env` as the root for file discovery.
- Target files: `.java`, `.jsp`, `.tsp`, `.xml`, `.html`, `.js`, `.sql`.
- For file searching, prefer `ripgrep (rg)` over `glob` for speed and `.gitignore` support.

## AI Provider Selection
- Read `AI_PROVIDER` from `.env` to select between OpenAI, Ollama, or Anthropic.
- Use the corresponding API keys and model names as set in `.env`.

## Metadata Extraction
- For each file, generate a prompt to extract:
  - File type, purpose, classes, methods, schema, endpoints, config, comments.
- Structure metadata with:
  - File path, type, language, start/end lines, entities, relationships, comments, complexity, parent context.

## Embedding and Storage
- Store all file embeddings and metadata in Chroma DB.
- Use `CHROMADB_DIR` and `CHROMADB_COLLECTION` from `.env`.

## Documentation Generation
- Use JSON metadata as the single source of truth for requirements.
- Group documentation by logical layer: Database, Backend, Presentation.
- Follow the requirements template for each section.

## Documentation Output
- Output Markdown files to `OUTPUT_DIR`.
- If `STRICTDOC=TRUE`, generate StrictDoc files alongside Markdown.

## Iterative Process
- Refine requirements and documentation as new metadata is extracted.
- Cross-link dependencies and validate business rules across layers.

## Best Practices
- Keep requirements and rules concise and context-aware.
- Use PRD and RFC documents for each feature or logical section.

