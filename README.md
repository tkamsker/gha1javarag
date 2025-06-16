# Java Code Search with ChromaDB

This application provides a semantic search functionality for Java code using ChromaDB and FastAPI. It allows you to ingest Java code files and perform semantic searches across the codebase.

## Features

- Java code parsing using tree-sitter
- Semantic code search using ChromaDB
- RESTful API for search and ingestion
- Support for processing entire directories of Java code
- Background processing for large codebases
- Comprehensive error handling and logging

## Prerequisites

- Python 3.8+
- Git
- ChromaDB server running at `https://chromadb.dev.motorenflug.at`

## Quick Setup

1. Run the setup script:
```bash
./setup.sh
```

This will:
- Create a virtual environment
- Install all dependencies
- Set up tree-sitter Java grammar
- Create necessary directories

2. Activate the virtual environment:
```bash
source venv/bin/activate
```

3. Start the API server:
```bash
python src/api/main.py
```

## Manual Setup

If you prefer to set up manually:

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up tree-sitter:
```bash
# Create directories
mkdir -p vendor build

# Clone Java grammar
git clone https://github.com/tree-sitter/tree-sitter-java.git vendor/tree-sitter-java

# Build grammar
python -c "from tree_sitter import Language; Language.build_library('build/my-languages.so', ['vendor/tree-sitter-java'])"
```

## Usage

The API will be available at `http://localhost:8000`

### API Endpoints

#### Health Check
- `GET /`
  ```json
  {
    "status": "healthy",
    "message": "Java Code Search API is running",
    "version": "1.0.0"
  }
  ```

#### Search Code
- `POST /search`
  ```json
  {
    "query": "your search query",
    "n_results": 5  // Optional, defaults to 5, max 20
  }
  ```
  Response:
  ```json
  [
    {
      "code": "found code snippet",
      "metadata": {
        "name": "method/class name",
        "type": "method_declaration/class_declaration",
        "start_line": 1,
        "end_line": 10,
        "file_path": "/path/to/file.java"
      }
    }
  ]
  ```

#### Ingest Code
- `POST /ingest`
  ```json
  {
    "directory_path": "/path/to/java/files"
  }
  ```
  Response:
  ```json
  {
    "message": "Started processing directory: /path/to/java/files",
    "status": "processing"
  }
  ```

## Integration with Dify

The API is designed to be compatible with Dify. You can use the search endpoint to retrieve relevant code snippets based on semantic queries. The results include both the code and metadata about its location and context.

### Example Dify Integration

1. Configure Dify to use the `/search` endpoint
2. Set the request format to match the API specification
3. Use the response format to display code snippets with context

## Development

- `src/ingestion/`: Contains the Java code processing logic
- `src/api/`: Contains the FastAPI application
- `tests/`: Contains test files
- `vendor/`: Contains the tree-sitter Java grammar

## Error Handling

The application includes comprehensive error handling:
- File not found errors
- Invalid directory paths
- Tree-sitter parsing errors
- ChromaDB connection issues
- Invalid search queries

All errors are logged and returned with appropriate HTTP status codes.

## Troubleshooting

If you encounter any issues:

1. Make sure all dependencies are installed correctly:
```bash
pip install -r requirements.txt
```

2. Verify tree-sitter setup:
```bash
python -c "from tree_sitter import Language; print(Language('build/my-languages.so', 'java'))"
```

3. Check ChromaDB connection:
```bash
python -c "import chromadb; client = chromadb.HttpClient(host='chromadb.dev.motorenflug.at', port=443, ssl=True)"
```

## License

MIT

# Example .env for remote ChromaDB
CUCOCALC_PATH=java_codebase
LOCAL_DB_PATH=chroma_db
CHROMA_API_URL=https://chromadb.dev.motorenflug.at
CHROMA_API_KEY=your_api_key_here
CHROMA_TENANT=your_tenant_name_here
CHROMA_DATABASE=your_database_name_here
COLLECTION_NAME=cucocalc
USE_REMOTE_DB=false
DEBUG=true

curl -X POST "https://chromadb.dev.motorenflug.at/api/v2/ingest" -H "Content-Type: application/json"   -d '{"directory_path": "/Users/thomaskamsker/Desktop/AKT_Docs/2025/AI/Cucocalc/code/cuco-master@d34bb6b6d1c"}'



# iteration 6 


# generate it 
python src/main.py

# extract 
python src/requirement_document_generator.py

## ---- 16 Jun

pip install langchain==0.1.12 langchain-core==0.1.31 langchain-openai==0.0.5 pydantic==2.11.6 python-dotenv==1.0.1


The refactored solution now consists of two main components:
1. Main Application (src/main.py):
 - Processes Doxygen HTML output
 - Extracts class information using BeautifulSoup
 - Stores data in ChromaDB for later use
 - Handles metadata and class hierarchy

2. Requirement Generator (src/requirement_generator.py):
 - Accesses stored data from ChromaDB
 - Generates requirements using LLM
 - Creates traceability matrix
 - Generates comprehensive reports