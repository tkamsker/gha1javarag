# Documentation Generation with CrewAI

This project uses CrewAI to generate comprehensive documentation from Doxygen XML output.

## Prerequisites

- Python 3.8 or higher
- Doxygen XML output from your codebase
- Required Python packages (see requirements.txt)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with the following content:
```env
# Path to Doxygen XML output directory
XML_INPUT_DIR=/path/to/doxygen/xml

# Optional: Configure logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# Optional: Configure chunk size for processing
CHUNK_SIZE=1000
```

## Usage

1. Generate Doxygen XML documentation for your codebase:
```bash
doxygen Doxyfile
```

2. Update the `XML_INPUT_DIR` in your `.env` file to point to the Doxygen XML output directory.

3. Run the documentation generation script:
```bash
python src/run_documentation_crew.py
```

The script will:
- Parse the Doxygen XML files
- Extract code entities and their relationships
- Group entities into logical components
- Verify requirements and code metrics
- Generate comprehensive documentation

## Output

The generated documentation will be available in the `generated_documentation` directory:
- `prd.md`: Product Requirements Document
- `technical_requirements.md`: Technical Requirements Specification
- `acceptance_criteria.md`: Acceptance Criteria and Test Scenarios

## Project Structure

```
doyen_crewai/
├── src/
│   ├── agents/
│   │   └── documentation_crew.py
│   └── run_documentation_crew.py
├── documentation/
│   └── templates/
│       ├── prd.md.j2
│       ├── technical_requirements.md.j2
│       └── acceptance_criteria.md.j2
├── .env
├── requirements.txt
└── README.md
```

## Customization

You can customize the documentation generation by:
1. Modifying the Jinja2 templates in `documentation/templates/`
2. Adjusting the chunk size in `.env`
3. Configuring logging levels
4. Extending the DocumentationCrew class with additional functionality

## Troubleshooting

If you encounter issues:
1. Check that the XML_INPUT_DIR is correctly set in `.env`
2. Verify that Doxygen XML files are present in the specified directory
3. Check the logs for detailed error messages
4. Ensure all dependencies are installed correctly

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
pytest tests -v


# run the script 

python src/run_documentation_crew.py



# -------- now we have first version 

Step-by-step: How to ensure ChromaDB is loaded for documentation generation

**1. Prepare your Doxygen XML files in the directory specified by XML_INPUT_DIR in your .env.**

**2. Run the embedding loader:**
Apply to README.md
Run
   cd doyen_crewai
   python -m src.load_embeddings

This parses XML, generates embeddings, and loads them into ChromaDB.

**3. Check the logs for:**

Number of entities parsed and loaded.
No errors about empty embeddings.

**4. Run your documentation generation:**

Run
   python src/run_documentation_crew.py
   
This script will now be able to access the embeddings and metadata in ChromaDB.

# run 
cd doyen_crewai && python src/run_documentation_crew.py
