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


# rate limit 
# Test the rate limiter
python src/test_rate_limiter.py

# Run step2 with conservative settings
RATE_LIMIT_ENV=test python src/step2_test.py

# Run step2 with production settings  
RATE_LIMIT_ENV=production python src/step2.py

# Emergency mode for very restrictive limits
RATE_LIMIT_ENV=emergency python src/step2.py



#####
# 2025.06.23 
#
python src/test_rate_limiter.py

# Check your billing first
# Visit: https://platform.openai.com/account/billing

# Then run with emergency mode (most conservative)
./lofalassn.sh emergency

# Or test mode (very conservative)
./lofalassn.sh test

test: 10 req/min, 500 req/hour, 8s delays
production: 15 req/min, 800 req/hour, 4s delays
emergency: 5 req/min, 200 req/hour, 10s delays

# new provider ollama run deepseek-r1:32b

# AI Provider Configuration
# Set this to 'openai' or 'ollama' to switch between providers
AI_PROVIDER=openai

# OpenAI Configuration (used when AI_PROVIDER=openai)
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL_NAME=gpt-4-turbo-preview

# Ollama Configuration (used when AI_PROVIDER=ollama)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL_NAME=deepseek-r1:32b
OLLAMA_TIMEOUT=120

# Rate Limiting Environment
# Options: production, test, development, emergency
RATE_LIMIT_ENV=test

# Output Configuration
OUTPUT_DIR=./output

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/java_analysis.log

# ChromaDB Configuration
CHROMADB_DIR=./data/chromadb
CHROMADB_COLLECTION=java_analysis


## 2025.06.23 ollama 
export AI_PROVIDER=ollama
./lofalassn.sh test

# improvement of ollama 
python src/test_ollama_debug.py

export RATE_LIMIT_ENV=emergency && python src/test_ollama_debug.py

export RATE_LIMIT_ENV=production && python src/test_ollama_debug.py

python src/test_ollama_debug.py

export AI_PROVIDER=ollama
   export RATE_LIMIT_ENV=production
./lofalassn.sh test

## 2025.06.24
# Chroma DB
Disable anonymized telemetry. 
Now statistics are not sent to https://us.i.posthog.com:443
# Documentation generation
Fixes: extract necessary information from ai_analysis json object.

# 2025.06.25 antropic 
# Test Anthropic provider
AI_PROVIDER=anthropic python src/test_ai_providers.py

# Run main application with Anthropic
AI_PROVIDER=anthropic python src/main.py

# Run step2 with Anthropic
AI_PROVIDER=anthropic python src/step2.py

# Run step3 with Anthropic
AI_PROVIDER=anthropic python src/step3.py

curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What does this project do?"}'

  Step 3: Open your browser
Navigate to: http://localhost:8000
Features of the Web Interface
✅ Modern, responsive design with a clean UI
✅ Real-time server status showing connection and AI provider info
✅ Interactive chat form with loading states
✅ Error handling with clear error messages
✅ Works with both Flask and FastAPI
✅ Shows AI provider and model information in responses
What You Can Do
Ask questions about your project in natural language
Get AI-powered answers based on your ChromaDB documentation
See which AI provider is being used (OpenAI, Anthropic, Ollama)
Monitor server status and connection health
The web interface will automatically detect your AI provider configuration from the .env file and display it in the interface!


### 
# 2025.06.26 falsk 

 ./run_flask.sh
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What does this project do?"}'


  ./run_fastapi.sh

  better ./start_web.sh
  

  ./Step2.sh test

  ### 2025.06.27 

  ./Step2.sh test 
  and in strictdoc 
  Web.sh 

  

  ## 3.Juli

export   TOKENIZERS_PARALLELISM=false

python test_chromadb.py > frznbrnf.txt


curl -X GET "http://localhost:8000/debug/query/customer"

curl -X GET "http://localhost:8000/debug/query/CustomerService"

curl -X GET "http://localhost:8000/debug/query/CustomerInteractionService"

curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"question": "What is CustomerInteractionService and what does it do?", "max_results": 5}'

curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"question": "What are the main service classes in this project?", "max_results": 15, "search_mode": "keyword"}'

curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"question": "PartyService", "max_results": 5, "search_mode": "keyword"}'


# now 
python test_chromadb_functionality.py to benchmark ChromaDB and save results.
Run python demo_effective_usage.py for a guided, practical usage demo.
Use the web interface at http://localhost:8000 with the recommended strategies.