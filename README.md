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
