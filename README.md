# Java/JSP/GWT/JS → PRD Pipeline (iteration17b)

# nohup 
nohup ./new_run.sh > "lognew_run_$(date +'%Y-%m-%d_%H-%M-%S').log" 2>&1 &
#
nohup ./run_iteration.sh > "log_run_iteration$(date +'%Y-%m-%d_%H-%M-%S').log" 2>&1 &

A comprehensive Python application that analyzes Java/JSP/GWT/JavaScript codebases, extracts metadata and requirements, and generates Product Requirements Documents (PRDs) using Ollama (LLM + embeddings) and Weaviate (vector database).

## 🚀 Features


maybe weaviate cant access ollama osx -> http://host.docker.internal:11434 

- **Multi-technology Support**: Java, JSP, GWT, JavaScript, iBATIS, SQL
- **Frontend Analysis**: GWT Activities/Places, UiBinder templates, JavaScript routes and XHR calls
- **Backend Analysis**: iBATIS statements, DAO calls, JSP forms, database schema
- **Vector Search**: Semantic search using Weaviate with Ollama embeddings
- **PRD Generation**: Automated PRD creation with frontend + backend fusion
- **Traceability**: Complete traceability from UI components to database tables

## 📋 Prerequisites

- Python 3.8+
- Docker (for Weaviate)
- Ollama (optional, for LLM features)
- Java source code to analyze

## 🛠️ Installation

1. **Clone and setup**:
   ```bash
   git clone <repository>
   cd a1javarag
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your Java source directory
   ```

3. **Start Weaviate**:
   ```bash
   ./docker-weaviate.sh
   ```

4. **Start Ollama** (optional):
   ```bash
   ollama serve
   ollama pull llama3.1:8b
   ollama pull nomic-embed-text
   ```

## 🚀 Quick Start

1. **Update configuration**:
   Edit `.env` file and set your Java source directory:
   ```ini
   JAVA_SOURCE_DIR=/path/to/your/java/source
   ```

2. **Run the complete pipeline**:
   ```bash
   ./run_iteration17b.sh my-project true
   ```

3. **Check outputs**:
   - PRD document: `./data/output/my-project_prd.md`
   - Build artifacts: `./data/build/`
   - Weaviate data: `./weaviate-data/`

## 📖 Usage

### Command Line Interface

```bash
# Discover files
python main.py discover --project my-project --include-frontend

# Extract artifacts
python main.py extract --project my-project --include-frontend

# Index in Weaviate
python main.py index --project my-project

# Search artifacts
python main.py search --query "order creation" --project my-project --frontend

# Generate PRD
python main.py prd --project my-project --frontend

# Run complete pipeline
python main.py all --project my-project --include-frontend
```

### Shell Script

```bash
# Run with frontend analysis
./run_iteration17b.sh my-project true

# Run without frontend analysis
./run_iteration17b.sh my-project false

# Check system status
./run_iteration17b.sh check

# Clean build artifacts
./run_iteration17b.sh clean
```

## 🏗️ Architecture

```
src/
├── config/          # Configuration management
├── discover/        # File discovery
├── extract/         # Artifact extraction
│   ├── gwt_modules.py      # GWT module extraction
│   ├── gwt_client.py       # GWT Activities/Places/RPC
│   ├── gwt_uibinder.py     # UiBinder templates
│   ├── js_static.py        # JavaScript analysis
│   ├── ibatis_xml.py       # iBATIS statements
│   ├── java_calls.py       # DAO method calls
│   ├── jsp_forms.py        # JSP form extraction
│   └── db_schema.py        # Database schema
├── chunk/           # Chunking and embedding
├── store/           # Weaviate integration
├── synth/           # PRD synthesis
└── cli.py           # Command-line interface
```

## 🔍 Supported Artifacts

### Frontend (GWT/JS)
- **GWT Modules**: `*.gwt.xml` files with entry points and inheritance
- **Activities/Places**: Navigation patterns and token mapping
- **UiBinder**: Widget definitions, event handlers, i18n keys
- **RPC/RequestFactory**: Service endpoints and method signatures
- **JavaScript**: Routes, XHR calls, validations, global exports

### Backend (Java/JSP/SQL)
- **iBATIS Statements**: SQL mappings and parameter definitions
- **DAO Calls**: Method calls and statement references
- **JSP Forms**: Form fields, validations, and actions
- **Database Schema**: Tables, columns, constraints, indexes

## 📊 Weaviate Schema

The system creates the following classes in Weaviate:

- `IbatisStatement` - iBATIS SQL statements
- `DaoCall` - DAO method calls
- `JspForm` - JSP form definitions
- `DbTable` - Database table schemas
- `GwtModule` - GWT module descriptors
- `GwtUiBinder` - UiBinder templates
- `GwtActivityPlace` - GWT navigation patterns
- `GwtEndpoint` - GWT RPC/RequestFactory endpoints
- `JsArtifact` - JavaScript artifacts
- `FrontendRoute` - Frontend routing information

## 🎯 PRD Generation

The system generates comprehensive PRDs including:

1. **Product Overview** - Vision, features, target users
2. **Features** - User stories and acceptance criteria
3. **Technical Architecture** - Technology stack and integration points
4. **Frontend** - UI components and navigation flows
5. **User Flows** - End-to-end user journeys
6. **Requirements** - Functional and non-functional requirements
7. **Traceability** - UI → API → DB mapping

## 🔧 Configuration

Key configuration options in `.env`:

```ini
# Source Discovery
JAVA_SOURCE_DIR=/path/to/java/source
JS_INCLUDE_GLOBS=**/*.js
GWT_INCLUDE_GLOBS=**/*.gwt.xml,**/*.ui.xml

# Ollama Configuration
OLLAMA_MODEL_NAME=llama3.1:8b
OLLAMA_EMBED_MODEL_NAME=nomic-embed-text

# Weaviate Configuration
WEAVIATE_URL=http://localhost:8080
```

## 🧪 Testing

```bash
# Run system checks
./run_iteration17b.sh check

# Test with sample data
python main.py discover --project test-project
python main.py extract --project test-project --include-frontend
```

## 📝 Output Examples

### Generated PRD Structure
```markdown
# Product Requirements Document (PRD)
## my-project

## 1. Product Overview
- Product Vision
- Key Features
- Target Users

## 2. Features
- Feature descriptions
- User stories
- Acceptance criteria

## 3. Technical Architecture
- System architecture
- Technology stack
- Integration points

## 4. Frontend
- UI components
- Navigation flows
- Client-side validations

## 5. User Flows
- End-to-end flows
- Entry points
- Navigation patterns

## 6. Requirements
- Functional requirements
- Non-functional requirements
- Acceptance criteria

## 7. Traceability
- UI to API mapping
- API to Database mapping
- End-to-end flows
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

1. **Weaviate not running**:
   ```bash
   ./docker-weaviate.sh
   ```

2. **Ollama not running**:
   ```bash
   ollama serve
   ollama pull llama3.1:8b
   ```

3. **Java source directory not found**:
   Update `JAVA_SOURCE_DIR` in `.env` file

4. **Python dependencies missing**:
   ```bash
   pip install -r requirements.txt
   ```

### Debug Mode

Run with verbose logging:
```bash
python main.py --verbose discover --project my-project
```

## 📚 References

- [Weaviate Documentation](https://weaviate.io/developers/weaviate)
- [Ollama Documentation](https://ollama.ai/docs)
- [GWT Documentation](https://www.gwtproject.org/)
- [iBATIS Documentation](https://ibatis.apache.org/) 



# ---
# 2025.10.24

# For Ubuntu deployment
./docker-weaviate.sh start ubuntu

# For macOS (auto-detect)
./docker-weaviate.sh start

# Other commands with OS override
./docker-weaviate.sh stop ubuntu
./docker-weaviate.sh restart ubuntu
./docker-weaviate.sh status

./start_weaviate_simple !!! 

# 26.Okt. 
source venv/bin/activate

 ./docker-weaviate.sh clean

nohup ./new_run.sh > "lognew_run_$(date +'%Y-%m-%d_%H-%M-%S').log" 2>&1 &

###


./start_web_client.sh 

#
pkill -f weaviate_client.py

# ---
# 2025.10.10 
# IT 17 new try 

nohup ./run_production_linux.sh production-project true  > "logprod_run_$(date +'%Y-%m-%d_%H-%M-%S').log" 2>&1 &

# 2025.Nov.18 

# Step 1: Install all other dependencies (this should work now)
pip install -r requirements.txt

# Step 2: Install CrewAI separately (avoids resolution conflicts)
pip install crewai==0.203.1

# Optional: Remove chromadb if you don't want it
# pip uninstall chromadb -y

python main.py requirements --project production-project --use-crewai

# fix 16:19 18Nov 

Usage
For all projects (recommended for multi-project setups):
python main.py requirements --all-projects
For a specific project:
python main.py requirements --project cuco-cct-core
With CrewAI:
python main.py requirements --all-projects --use-crewai

**How It Works**
1. Loads all artifacts from data/build/
2. Extracts unique project names from the project field in artifacts
3. For each project:
- Filters artifacts by project name
- Generates requirements in data/output/requirements/{project_name}/
- Creates per-project index files

This ensures each project gets its own requirements directory, preventing overwrites and keeping requirements organized.
The solution handles your example path /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-cct-core/src/test/java/... and correctly identifies cuco-cct-core as the project name instead of mnt


**Almost ok **
Next Steps
Since your artifacts were already extracted with incorrect project names, you need to re-extract them:
# Re-extract artifacts with the updated project name detectionpython main.py extract --project production-project --include-frontend# Then re-index in Weaviatepython main.py index --project production-project# Now generate requirements with correct project namespython main.py requirements --all-projects --use-crewai
The WeaviateClient error should now be resolved, and after re-extraction, project names should be correctly detected (e.g., "cuco-cct-core" instead of "mnt").



** ------------------------------- **

How --all-projects is handled in run_production_linux.sh
New parameter
The script now has 4 parameters:
./run_production_linux.sh [PROJECT_NAME] [INCLUDE_FRONTEND] [USE_CREWAI] [REQUIREMENTS_ALL_PROJECTS]
PROJECT_NAME (default: "production-project")
INCLUDE_FRONTEND (default: "true")
USE_CREWAI (default: "true")
REQUIREMENTS_ALL_PROJECTS (default: "true") — new
How it works
The REQUIREMENTS_ALL_PROJECTS parameter controls whether to use --all-projects or --project:

if [ "$REQUIREMENTS_ALL_PROJECTS" = "true" ]; then    
# Uses --all-projects flag    
   python main.py requirements --all-projects [--use-crewai]
else    
# Uses --project with PROJECT_NAME    
   python main.py requirements --project "$PROJECT_NAME" [--use-crewai]
fi

**Examples**

1. Generate for all projects (default):
./run_production_linux.sh
# Equivalent to: ./run_production_linux.sh production-project true true true
# Uses: --all-projects

2. Generate for specific project only:
./run_production_linux.sh my-project true true false
# Uses: --project my-project

3. All projects with CrewAI:
./run_production_linux.sh my-project true true true
# Uses: --all-projects --use-crewai

4. Specific project with CrewAI:
./run_production_linux.sh my-project true true false
# Uses: --project my-project --use-crewai

5. All projects without CrewAI:
./run_production_linux.sh my-project true false true# Uses: --all-projects

6. Specific project without CrewAI:
./run_production_linux.sh my-project true false false# Uses: --project my-project

Parameter combinations

Command	Frontend	CrewAI	All Projects	Result
./run_production_linux.sh	✅	✅	✅	--all-projects --use-crewai
./run_production_linux.sh proj true true true	✅	✅	✅	--all-projects --use-crewai
./run_production_linux.sh proj true true false	✅	✅	❌	--project proj --use-crewai
./run_production_linux.sh proj true false true	✅	❌	✅	--all-projects
./run_production_linux.sh proj true false false	✅	❌	❌	--project proj

**Summary**
REQUIREMENTS_ALL_PROJECTS=true → Uses --all-projects (discovers all projects from artifacts)
REQUIREMENTS_ALL_PROJECTS=false → Uses --project "$PROJECT_NAME" (only the specified project)
The script now supports both modes, with --all-projects as the default.