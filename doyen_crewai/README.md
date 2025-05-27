# Doyen CrewAI

A modular, agent-driven architecture for automated Java codebase documentation and analysis using Doxygen XML output, local Ollama LLM embeddings, and CrewAI agent workflows.

## Project Structure

```
doyen_crewai/
├── src/
│   ├── agents/           # CrewAI agent implementations
│   ├── preprocessing/    # Doxygen XML parsing and embedding
│   └── utils/           # Utility functions and helpers
├── tests/               # Test suite
├── docs/               # Generated documentation
└── requirements.txt    # Project dependencies
```

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and configure your environment variables:
   ```bash
   cp .env.example .env
   ```

4. Ensure you have Ollama running locally with the required model:
   ```bash
   ollama pull all-minilm
   ```

## Usage

1. Run Doxygen on your Java codebase to generate XML documentation
2. Configure the XML input directory in your `.env` file
3. Run the main processing script:
   ```bash
   python -m src.main
   ```

## Development

- Use `black` for code formatting
- Use `isort` for import sorting
- Use `mypy` for type checking
- Run tests with `pytest`

## License

MIT License 


## -----------

refactor !!!

I've separated the embedding generation and storage from the CrewAI analysis process. Here's what changed:

1. Created a new ChromaDBLoader class that handles:
-- Loading embeddings into ChromaDB
-- Retrieving entity data and embeddings
-- Finding similar entities using semantic search
-- Managing the ChromaDB collection

2. Created a separate load_embeddings.py script that:
-- Parses Doxygen XML files
-- Generates embeddings using Ollama
-- Loads everything into ChromaDB
-- This only needs to be run once or when the codebase changes

3. Updated the main script to:
-- Use ChromaDB for data access instead of generating embeddings
-- Check if embeddings exist before running analysis
-- Pass the ChromaDB loader to the ParserAgent

4. Enhanced the ParserAgent to:
-- Work with ChromaDB instead of direct entity access
-- Add semantic similarity search using embeddings
-- Improve error handling and data retrieval

**To use the refactored system:**

1. First, load the embeddings (only needed once or when codebase changes):

python -m src.load_embeddings

2. Then run the analysis (can be run multiple times):

python -m src.main


**Benefits of this separation:**
1. Faster analysis runs since embeddings are pre-computed
2. Persistent storage of embeddings and metadata
3. Ability to perform semantic similarity searches
4. Better scalability for large codebases
5. Reduced API calls to Ollama

Would you like me to:
Add more features to the ChromaDB loader?
Implement additional analysis capabilities?
Add tests for the new components?
Or focus on something else?

**Tests**

# Run all tests
pytest

# Run tests with coverage report
pytest --cov=src

# Run specific test file
pytest tests/test_chroma_loader.py

# Run tests with verbose output
pytest -v
