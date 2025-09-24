# 3-Step Code Analysis Process

This document outlines the 3-step process used to reverse-engineer a Java application, analyze its source code with AI, and generate structured documentation and an interactive query interface.

### High-Level Overview

The project is a tool for reverse-engineering Java applications. It uses AI (with support for OpenAI, Anthropic, and Ollama) to analyze source code, extract requirements, and store the results in a searchable ChromaDB database. The process is broken down into three main steps, each orchestrated by a corresponding shell script (`Step1.sh`, `Step2.sh`, `Step3.sh`).

### Step 1: Code Ingestion and Initial AI Analysis

**Script:** `Step1.sh`
**Core Python script:** `src/main.py` (or `main_test.py`/`main_debug.py`)

**Purpose:** This is the first and most critical step. It involves finding all relevant source code files, processing them, and performing an initial analysis using an AI model.

**Process:**

1.  **Environment and Configuration:** The `Step1.sh` script begins by setting up the environment. It loads variables from a `.env` file, determines which AI provider to use (OpenAI, Anthropic, or Ollama), and performs checks to ensure the necessary API keys or services are available.
2.  **File Processing:** The script then executes the main Python script (`src/main.py` or its test/debug variants). This script scans the source directory (specified by `JAVA_SOURCE_DIR` in the `.env` file) for relevant files like `.java`, `.jsp`, `.xml`, etc.
3.  **AI Analysis:** For each file (or batch of files), the script sends the code to the configured AI provider with a prompt asking for analysis. This analysis likely includes identifying the file's purpose, its key components (classes, methods, etc.), dependencies, and business logic.
4.  **Data Storage:** The results of the AI analysis, along with metadata about each file (path, type, etc.), are stored in two places:
    *   A JSON file (`output/metadata.json`) for a complete record of the analysis.
    *   A ChromaDB collection for efficient similarity searching and retrieval in later steps.
5.  **Rate Limiting:** This step is heavily rate-limited to avoid exceeding API quotas, with different modes (`test`, `production`, `emergency`) that control the number of API requests per minute.

### Step 2: Requirements Generation and Structuring

**Script:** `Step2.sh`
**Core Python script:** `src/step2.py` (or `step2_test.py`/`step2_debug.py`)

**Purpose:** This step takes the raw analysis from Step 1 and structures it into human-readable requirements documentation.

**Process:**

1.  **Load Metadata:** The `step2.py` script loads the `metadata.json` file generated in the previous step.
2.  **Analyze by Layer:** It then analyzes the metadata, likely grouping files by architectural layer (e.g., presentation, business logic, data access).
3.  **Generate Structured Documentation:** Using the AI provider again, this step generates more detailed and structured documentation from the initial analysis. It creates markdown files that summarize the requirements for different parts of the application.
4.  **Output:** The output is a set of markdown files in the `output/requirements` directory, including an index file (`step2_index.md`) that links to the layer-specific documents. This creates a browsable documentation set from the codebase.

### Step 3: Modern Requirements Generation and Web Interface

**Script:** `Step3.sh`
**Core Python script:** `src/step3.py` (or `step3_test.py`/`step3_debug.py`)

**Purpose:** This step appears to be an alternative or enhanced version of Step 2, creating what's referred to as "modern requirements." It also includes functionality for a web-based chat interface to query the system.

**Process:**

1.  **Modern Requirements:** The `step3.py` script likely performs a more advanced analysis or formatting of the requirements, possibly with different prompts or structuring logic, to create "modern" documentation.
2.  **Web Interface (FastAPI/Flask):** A key part of this step is the web interface. The `README.md` mentions running a Flask or FastAPI app (`run_flask.sh`, `run_fastapi.sh`, `start_web.sh`). This web server provides a chat interface that allows users to ask natural language questions about the codebase.
3.  **RAG (Retrieval-Augmented Generation):** When a user asks a question through the web interface, the backend queries the ChromaDB database to find the most relevant code snippets and analysis. This information is then passed to the AI model along with the user's question to generate a comprehensive answer. This is the "Retrieval-Augmented Generation" (RAG) part of the system.

In summary, the 3-step process is a comprehensive pipeline that:
1.  **Ingests and analyzes** a Java codebase using AI.
2.  **Generates structured requirements** documentation from the analysis.
3.  **Creates a searchable knowledge base** and provides a chat interface for interactive querying.

### Test and Script Files Analysis

This section provides an overview of the various test and script files in the project, categorized by their function.

#### Orchestration Scripts

These scripts control the main workflow of the application.

*   **`Lofalassn.sh`**: This appears to be the main orchestration script that runs the entire 3-step process in sequence. It takes a mode (`test`, `production`, or `emergency`) as an argument to control rate limiting and other settings.
*   **`Step1.sh`**: Executes the first step of the process: code ingestion and initial AI analysis. It calls the corresponding Python scripts (`main.py`, `main_test.py`, or `main_debug.py`).
*   **`Step2.sh`**: Executes the second step: generating structured requirements documentation. It calls `step2.py` and its variants.
*   **`Step3.sh`**: Executes the third step: generating "modern" requirements and enabling the web interface. It calls `step3.py` and its variants.
*   **`setup.sh`**: A script to set up the Python virtual environment and install dependencies from `requirements.txt`.

#### Test Scripts

These scripts are used to test various components of the application.

*   **`test_all_questions.py`**: A comprehensive test script that evaluates a predefined set of 10 questions against the entire system (ChromaDB and AI). It analyzes the quality and usability of the results and generates a detailed report.
*   **`test_questions_simple.py`**: A simplified version of `test_all_questions.py` that uses the Flask app's HTTP endpoints to test the questions, avoiding direct module imports.
*   **`test_chromadb.py`**: A script to inspect the contents of the ChromaDB database, providing insights into the stored data and verifying the chunking process.
*   **`test_chromadb_functionality.py`**: Evaluates the search capabilities of ChromaDB by running a series of test queries and analyzing the quality of the results without involving the AI model.
*   **`test_debug_feature.py`**: Tests the debug functionality, including the processing of debug files and analysis of `pom.xml` files.
*   **`test_enhanced_chunking.py`**: Tests the intelligent code chunking logic and the enhanced ChromaDB metadata storage.
*   **`src/test_ai_providers.py`**: Tests the functionality of switching between different AI providers (OpenAI, Ollama, Anthropic).
*   **`src/test_ollama_debug.py`**: A specific test script for debugging the Ollama provider, including enhanced logging and error handling.
*   **`src/test_rate_limiter.py`**: Tests the rate limiting functionality, including handling of quota exceeded errors.
*   **`test_strictdoc_parsing.sh`**: A shell script to test if the generated `.sdoc` files can be parsed correctly by StrictDoc.

#### Web Server Scripts

These scripts are used to run the web interface.

*   **`run_fastapi.sh`**: Starts the FastAPI web server.
*   **`run_flask.sh`**: Starts the Flask web server.
*   **`start_web.sh`**: A user-friendly script that prompts the user to choose between starting the Flask or FastAPI server.

#### Utility Scripts

These scripts perform various utility and maintenance tasks.

*   **`fix_sdoc_files.sh`**, **`fix_sdoc_files_v2.sh`**, **`fix_sdoc_files_v3.sh`**: A series of scripts for fixing malformed `.sdoc` files to make them compliant with the StrictDoc standard.
*   **`infra/create_debugfile.sh`**: A script to generate a list of source files to be used for debugging purposes.
*   **`strictdoc/convert_md_to_sdoc.sh`**: Converts Markdown files to StrictDoc's `.sdoc` format.
*   **`strictdoc/copy_sdoc_files.sh`**: Copies `.sdoc` files to the requirements directory.
*   **`strictdoc/md2doc.sh`** and **`strictdoc/md2strictdoc.sh`**: Scripts for converting Markdown files to `.sdoc` format with more advanced options.
*   **`strictdoc/run_server.sh`**: Runs the StrictDoc server to serve the generated documentation.
*   **`strictdoc/setup_strictdoc_server.sh`**: A comprehensive script for validating `.sdoc` files, setting up the requirements directory, and running the StrictDoc server.
*   **`strictdoc/Web.sh`**: A simple script to run the StrictDoc web server.