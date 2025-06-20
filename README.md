# Java JSP Application Reverse Engineering Tool

This tool helps reverse engineer Java JSP applications by extracting detailed requirements, data structures, and business rules using AI-powered analysis and ChromaDB for storage.

## Setup

1. Clone this repository
2. Create a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.template` to `.env` and configure:
   ```bash
   cp .env.template .env
   ```
   Edit `.env` and set:
   - `JAVA_SOURCE_DIR`: Path to your Java/JSP source code
   - `OUTPUT_DIR`: Where to save generated documentation
   - `CHROMADB_DIR`: Where to store ChromaDB data
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `OPENAI_MODEL_NAME`: Preferred OpenAI model (default: gpt-4-turbo-preview)

## Usage

1. Place your Java/JSP source code in the directory specified by `JAVA_SOURCE_DIR`

2. Run the analysis:
   ```bash
   python src/main.py
   ```

3. The tool will:
   - Scan the source directory for relevant files
   - Analyze each file using AI
   - Store metadata in ChromaDB
   - Generate requirements documentation
   - Save all outputs to the specified output directory

## Output

The tool generates:
1. `metadata.json`: Raw metadata and analysis for all processed files
2. ChromaDB collection: Searchable database of code and analysis
3. Requirements documentation (coming soon)

## Supported File Types

- Java source files (.java)
- Java Server Pages (.jsp)
- XML configuration files (.xml)
- HTML files (.html)
- JavaScript files (.js)
- SQL scripts (.sql)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

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



#  20205 06 17 

1. Now we have successfully separated the requirements generation into two distinct steps:
- First Step (in main.py):
- Process and analyze files
- Extract metadata
- AI analysis
- Store in JSON and ChromaDB

2. Second Step (in requirements_analyzer.py):
- Analyze metadata by layer
- Generate structured analysis
- Create detailed documentation
- Generate index and layer-specific documents

The separation provides better organization and makes it easier to maintain and extend each step independently. The RequirementsAnalyzer class now handles all the complex analysis and documentation generation, while the main script orchestrates the overall process.


# new implement 
 output/
   └── requirements/
       ├── step2_index.md
       ├── index.md
       ├── home.md
       └── [other files].md

# 2025.06.18  prompt 

we have an requirement please explain in detail "ai_analysis"

# 2025.06.20 Tets of code onlinebookstore 
