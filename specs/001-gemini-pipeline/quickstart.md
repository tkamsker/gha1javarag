# Quickstart Guide: GEMINI Code Analysis and PRD Generator

This guide provides the steps to set up and run the GEMINI pipeline.

## 1. Prerequisites

- Python 3.8+
- Docker
- Ollama

## 2. Installation

1.  **Install Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Start Weaviate:**

    The project includes `docker-compose.yml` files for starting Weaviate. Use the appropriate one for your system.

    ```bash
    # For Linux
    docker-compose -f docker-compose.ubuntu.yml up -d

    # For macOS
    docker-compose -f docker-compose.macos.yml up -d
    ```

3.  **Start Ollama:**

    Ensure the Ollama service is running.

    ```bash
    ollama serve
    ```

    You also need to have a model pulled for text generation. For example:

    ```bash
    ollama pull llama2
    ```

## 3. Configuration

- Create a `.env` file in the root of the project.
- Add the following environment variable to point to your Java source code:
- example /Users/thomaskamsker/Documents/Atom/vron.one/playground/java/cuco-ui-admin

  ```
  JAVA_SOURCE_DIR=/path/to/your/java/project
  ```

- You can also configure the Weaviate host and other settings in `config/settings.py`.

## 4. Running the Pipeline

The main entry point for the application is `main.py`.

### Run the complete pipeline:

```bash
python main.py all --project <project_name> --include-frontend
```

### Run individual stages:

- **Discover files:**
  ```bash
  python main.py discover --project <project_name>
  ```

- **Extract artifacts:**
  ```bash
  python main.py extract --project <project_name> --include-frontend
  ```

- **Index artifacts in Weaviate:**
  ```bash
  python main.py index --project <project_name>
  ```

- **Search for artifacts:**
  ```bash
  python main.py search --project <project_name> --query "<your_query>"
  ```

- **Generate a Product Requirements Document (PRD):**
  ```bash
  python main.py prd --project <project_name> --frontend
  ```

## 5. Output

- Generated PRDs will be located in the `output/prd/` directory.
- These PRDs can be used as input for `speckit` commands like `/speckit.specify` and `/speckit.tasks`.
