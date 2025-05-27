# iteration3.md

## Refactor and CrewAI-Based Automated Documentation for `doyen_crewai`

---

### Overview

This document describes the requirements and implementation plan for refactoring our current Java code analysis application from the `java_crew_ai` directory to a new, modular, and agent-driven architecture in the `doyen_crewai` directory. The new solution leverages Doxygen XML output, local Ollama LLM embeddings, and a CrewAI agent workflow to automate the extraction, grouping, and documentation of codebase components for large-scale Java projects.

---

## 1. Preprocessing: Structure the Codebase for Iteration

**Objective:**  
Efficiently parse and structure the codebase for downstream agent processing, using Doxygen XML and local embedding models.

**Steps:**

- **Doxygen XML Extraction:**  
  - Run Doxygen on the Java codebase to generate XML documentation (`xml/` directory). we will receive this directory via .env variable xmlinput
  - Extract entities: classes, functions, files, and call graphs.

- **Chunking and Structuring:**  
  - Parse XML files (using Python’s `ElementTree` or `lxml`) to create logical chunks per class, function, or module.
  - For each chunk, extract:
    - Name
    - Description
    - Source file
    - Call relationships
    - Documentation comments

- **Embedding with Local Ollama LLM:**  
  - For each documentation chunk, generate an embedding using the local Ollama API:
    ```
    curl http://localhost:11434/api/embeddings -d '{
      "model": "all-minilm",
      "prompt": "<documentation chunk text>"
    }'
    ```
  - Store the resulting embeddings and metadata for semantic search and agent retrieval.

- **Storage:**  
  - Save structured data and embeddings in a local vector database (e.g., ChromaDB) or as indexed files for direct access.

---

## 2. CrewAI Setup: Sequential or Hierarchical Process

**Objective:**  
Implement a CrewAI pipeline where agents process the codebase in logical order, each building on the previous agent’s output.

**Agent Roles:**

- **Parser Agent:**  
  - Parses Doxygen XML, builds call graphs, and maps relationships between code entities.
- **Modeling Agent:**  
  - Groups entities into components/modules based on call graph connectivity and extracts candidate requirements.
- **Verification Agent:**  
  - Cross-checks requirements against code metrics (e.g., cyclomatic complexity, call depth, coverage).
- **Specification Agent:**  
  - Generates Product Requirements Document (PRD) and technical requirements using structured templates.

**CrewAI Process Example:**

from crewai import Crew, Process
crew = Crew(
agents=[parser_agent, modeling_agent, verification_agent, spec_agent],
tasks=[parse_task, model_task, verify_task, spec_task],
process=Process.sequential
)
result = crew.kickoff()

- Each agent receives the output of the previous, ensuring context is preserved and the entire codebase is covered.

---

## 3. Iteration Strategies

**A. Master Iteration Agent:**  
- A dedicated agent iterates over all codebase chunks, delegating analysis tasks to sub-agents.

**B. Agent-internal Iteration:**  
- Each agent is responsible for processing all relevant units (e.g., Parser Agent processes all classes, then passes summaries to the next agent).

**C. Task-based Iteration:**  
- Define a task per codebase unit (e.g., per class/file), and CrewAI dispatches agents to handle each.

**Recommendation:**  
Use a hybrid of A and B for scalability and reliability:  
- Master agent iterates and assigns, while each agent can process batches internally for efficiency.

---

## 4. Best Practices for Large Codebases

- **Chunk Size:**  
  - Keep documentation chunks small enough to fit within the LLM’s context window.
- **Metadata Tracking:**  
  - Tag each chunk with metadata (component, type, dependencies, status) for filtering and progress tracking.
- **Batch Processing:**  
  - Batch embedding and agent tasks to optimize performance.
- **Checkpointing:**  
  - Store intermediate agent outputs to enable resumable workflows.
- **Parallelization:**  
  - Where possible, parallelize agent processing across independent codebase units.
- **Version Control and Traceability:**  
  - Maintain version history of generated documentation and code analysis results.
- **Regular Updates:**  
  - Re-run preprocessing and agent workflows as the codebase evolves to keep documentation current.

---

## 5. Example Agent Prompts

**Parser Agent Prompt:**  
> "Given this Doxygen XML chunk, extract all function names, their descriptions, and the functions they call. Output as a JSON object with `function_name`, `description`, and `calls` fields."

**Modeling Agent Prompt:**  
> "Given the following list of functions and their call relationships, group them into logical components or modules based on call graph connectivity. For each component, summarize its purpose and main responsibilities."

**Verification Agent Prompt:**  
> "For every extracted requirement, check if it is supported by at least one code entity. Report any gaps or ambiguities."

**Specification Agent Prompt:**  
> "Using the grouped components and their features, generate a Product Requirements Document section for each component, including dependencies and acceptance criteria."

---

## 6. Directory Migration

- Move all code and configuration from `java_crew_ai` to `doyen_crewai`.
- Refactor codebase structure to support modular agent workflows and clear separation between preprocessing, embedding, and CrewAI orchestration.

---

## 7. PRD and Technical Requirements Output

- Generate Markdown and JSON documentation using Jinja2 templates, following Cursor PRD best practices ([see reference][5]).
- Store outputs in version-controlled docs directory for review and iteration.

---

## References

- [Cursor PRD Guidelines][5]
- [CrewAI Sequential/Hierarchical Processes]
- [Ollama API Documentation]

---

**This requirements document ensures a robust, scalable, and maintainable approach to automated codebase documentation and requirement extraction, leveraging modern LLM and agent orchestration best practices.**
