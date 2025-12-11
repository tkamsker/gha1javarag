# GEMINI.md

## Project Overview

This project is a Python-based pipeline for analyzing Java/JSP/GWT/JavaScript codebases. It extracts metadata and artifacts from the source code, indexes them in a Weaviate vector database, and uses this information to generate Product Requirements Documents (PRDs) and other documentation with the help of an Ollama-powered Large Language Model (LLM).

The primary goal is to automate the process of understanding and documenting complex, legacy codebases. By leveraging vector search and LLMs, the project provides semantic search capabilities and generates human-readable documentation from the source code itself.

**Key Technologies:**

*   **Python:** The core language for the pipeline.
*   **Click:** Used for creating the command-line interface.
*   **Weaviate:** A vector database for storing and searching code artifacts.
*   **Ollama:** A local LLM for natural language processing and generation tasks.
*   **Docker:** Used for running Weaviate.

**Architecture:**

The application is structured as a pipeline with distinct stages, each implemented as a subcommand in the CLI:

1.  **Discover:** Scans the target source code directory to find relevant files (`.java`, `.jsp`, `.js`, `.xml`, etc.).
2.  **Extract:** Parses the discovered files to extract structured artifacts, such as GWT modules, iBATIS statements, JSP forms, and database schemas.
3.  **Index:** Indexes the extracted artifacts into the Weaviate vector database, creating embeddings for semantic search.
4.  **Search:** Provides a command-line interface for searching the indexed artifacts using natural language queries.
5.  **PRD Generation:** Synthesizes the indexed information into a comprehensive Product Requirements Document (PRD) in Markdown format.
6.  **Requirements Generation:** Generates detailed requirements for each artifact.

The source code is organized into modules corresponding to these stages, located in the `src/` directory.

## Building and Running

### Prerequisites

*   Python 3.8+
*   Docker
*   Ollama

### Installation

1.  **Install Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Start Weaviate:**

    ```bash
    docker-compose up -d
    ```
    or
    ```bash
    ./docker-weaviate.sh
    ```

3.  **Start Ollama:**

    ```bash
    ollama serve
    ```

### Running the Pipeline

The main entry point for the application is `main.py`, which provides a command-line interface with several subcommands.

**Run the complete pipeline:**

```bash
python main.py all --project <project_name> --include-frontend
```

**Run individual stages:**

```bash
# Discover files
python main.py discover --project <project_name>

# Extract artifacts
python main.py extract --project <project_name> --include-frontend

# Index artifacts in Weaviate
python main.py index --project <project_name>

# Search for artifacts
python main.py search --query "<your_query>" --project <project_name>

# Generate a Product Requirements Document (PRD)
python main.py prd --project <project_name> --frontend
```

## Development Conventions

*   **Configuration:** The application uses a `config/settings.py` file for configuration, which can be overridden by environment variables or a `.env` file.
*   **Logging:** The `logging` module is used for logging, with the log level configurable via the `--verbose` flag or the `LOG_LEVEL` environment variable.
*   **CLI:** The `click` library is used for creating the command-line interface. The main CLI logic is in `src/cli.py`.
*   **Testing:** The `pytest` framework is used for testing. Tests are located in the `tests/` directory.
*   **Dependencies:** Python dependencies are managed in the `requirements.txt` file.
*   **Code Style:** The code follows standard Python conventions (PEP 8).
