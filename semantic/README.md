# Semantic Code Search & Clustering Application

This application processes Java code artifacts from Doxygen XML files, generates embeddings, clusters similar code, and generates requirements using GenAI.

## Prerequisites

- Python 3.8 or higher
- Doxygen XML output from your Java project
- OpenAI API key

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with the following variables:
```
XML_INPUT_DIR=/path/to/doxygen/xml
JAVA_SOURCE_DIR=/path/to/java/source
OPENAI_API_KEY=your_openai_api_key
```

## Directory Structure

```
semantic/
├── config/
│   └── app.yaml           # Configuration file
├── data/
│   ├── doxygen_xml/       # Input Doxygen XML files
│   ├── chroma_db/         # ChromaDB persistent storage
│   └── output/            # Generated requirements
├── src/
│   ├── doxygen_parser.py  # XML → code artifact extraction
│   ├── embedder.py        # Embedding generation
│   ├── chroma_connector.py # ChromaDB interface
│   ├── cluster_engine.py  # Clustering logic
│   ├── requirement_gen.py # GenAI requirement generation
│   └── main.py           # Main workflow
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Usage

1. Ensure your Doxygen XML files are in the directory specified by `XML_INPUT_DIR` in your `.env` file.

2. Run the main workflow:
```bash
python src/main.py
```

3. The application will:
   - Parse Doxygen XML files
   - Generate embeddings for code artifacts
   - Store artifacts in ChromaDB
   - Cluster similar code artifacts
   - Generate requirements for individual artifacts and clusters

4. Results will be saved in `data/output/`:
   - `cluster_requirements.txt`: Requirements for each cluster
   - `artifact_requirements.txt`: Requirements for individual artifacts

## Configuration

The application can be configured through `config/app.yaml`:

- `embedding_model`: The model used for generating embeddings
- `clustering`: Clustering algorithm settings
- `chroma`: ChromaDB settings
- `openai`: OpenAI API settings
- `processing`: General processing settings

## Output

The application generates two types of requirements:

1. **Cluster Requirements**: High-level requirements that describe the purpose of groups of related code artifacts.
2. **Artifact Requirements**: Specific requirements for individual code artifacts.

Requirements are saved in text files in the `data/output/` directory.

## Error Handling

The application includes comprehensive error handling and logging. Check the console output for any issues during processing.

## Contributing

Feel free to submit issues and enhancement requests! 


## .env 
# Doxygen XML input directory
XML_INPUT_DIR=/Users/thomaskamsker/Desktop/AKT_Docs/2025/AI/Cucocalc/code/doxygen/hotel_docs_doxygen/xml

# Java source code directory
JAVA_SOURCE_DIR=/Users/thomaskamsker/Desktop/AKT_Docs/2025/AI/Cucocalc/code/HospitalManagementSysyem

# OpenAI API key
OPENAI_API_KEY=sk-svcacct-ulHz4SoGxJ6Rb-
#
KMP_DUPLICATE_LIB_OK=TRUE
OMP_NUM_THREADS=1

PROJECT_ROOT=/Users/thomaskamsker/Documents/Atom/vron.one/playground/a1javarag
CHROMA_DB_DIR=/Users/thomaskamsker/Documents/Atom/vron.one/playground/a1javarag/semantic/data/chroma_db

# LLM Configuration local or azure openai
#LLM_PROVIDER=local
#LLM_MODEL_PATH=/path/to/your/llama/model.gguf
#LLM_CONTEXT_SIZE=4096
#LLM_TEMPERATURE=0.7
#LLM_MAX_TOKENS=1024

# LLM Configuration
LLM_PROVIDER=ollama
OLLAMA_MODEL_NAME=deepseek-r1
OLLAMA_BASE_URL=http://localhost:11434
LLM_TEMPERATURE=0.7

## 
# from semantic 
#
python -m src.main


### 3 June 

python -m src.main --force-reanalysis

PYTHONPATH=. python -m unittest test_doxygen_parser.py -v

cd semantic/src && python -m unittest test_doxygen_parser.py -v

# tests 
python -m unittest test_embedding_manager.py -v

# 12 Jun 
./generate_test_data.sh

PYTHONPATH=. python -m unittest src.test_doxygen_parser -v

