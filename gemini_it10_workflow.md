# Step-by-Step Reverse Engineering Workflow

## 1. Preparation
- Ensure Python, Cursor.ai, and Chroma DB are installed.
- Clone the Java JSP application codebase locally.
- Configure the `.env` file with:
  - `JAVA_SOURCE_DIR`
  - `OUTPUT_DIR`
  - `CHROMADB_DIR`
  - AI provider and model settings (OpenAI, Ollama, Anthropic, etc.).

## 2. Automated Metadata Extraction
- Run `step1.sh` to:
  - Recursively scan `JAVA_SOURCE_DIR` for `.java`, `.jsp`, `.tsp`, `.xml`, `.html`, `.js`, `.sql` files.
  - For each file, generate an AI prompt to extract:
    - File type, purpose, classes/methods, schema, endpoints, config, comments.
  - Use the configured AI provider to enrich and structure metadata.
  - Store embeddings and metadata in Chroma DB with unique IDs and tags.
  - Export a consolidated JSON file in `OUTPUT_DIR`.

## 3. Requirements Documentation Generation
- Run `step2.sh` to:
  - Load the exported JSON metadata.
  - Group components by logical layers: Database, Backend, Presentation.
  - For each group, generate a requirements document using the provided template.
  - Use AI to refine, cross-link, and validate requirements and business rules.

## 4. Documentation and Review
- Assemble requirements into a master specification.
- Review for completeness, accuracy, and clarity.
- Iterate as needed based on feedback or new findings.

## 5. Project Rules and Best Practices
- Maintain `.cursor/index.mdc` and `.cursor/rules/*.mdc` for coding standards and architectural rules.
- Use PRD and RFC documents for each feature or logical section.
- If `STRICTDOC=TRUE` in `.env`, generate StrictDoc documents alongside Markdown files.
