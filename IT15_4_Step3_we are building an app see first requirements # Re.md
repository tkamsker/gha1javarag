Here are two PRDs for step 3: one for a **straightforward, classic programmatic (step3-pgm)** implementation and one for an **agent-based (step3-agent)** approach. Both address the requirement to distinguish backend (DAO, DTO, services) and frontend processes, revisit relevant source files, and enrich requirements info using Weaviate as needed.

***

# PRD: Step 3 Programmatic Implementation (step3-pgm)

## 1. Purpose

Provide a maintainable extension of Step 3 that:
- Distinguishes backend (DAO, DTO, service) and frontend code/data models.
- Revisits the source code to fetch and expand entities.
- Enriches each requirements section with relevant Weaviate semantic data.

## 2. Requirements

### Input
- `.env` configuration for LLM, Weaviate, etc.
- Codebase metadata: per-file structural and code entity information (from step2).
- Intermediate data: `intermediate_step2.json` or fallback `consolidated_metadata.json`.
- Weaviate collections populated with semantic chunks and file/entity tags.

### Processing Flow

1. **Initialization and Validation**
   - Validate `.env`, provider access, Weaviate connectivity, input file structure.

2. **Project Iteration**
   - For each project:
     - Categorize files/entities as backend (DAO, DTO, service) or frontend (JSP, TSP, HTML, JS).
     - For backend: Identify and document DTO/DAO classes, services, and their relationships.
     - For frontend: Extract forms, endpoints, UI workflows, main business logic.

3. **Source Code Revisiting**
   - For each component, revisit the original source file(s) to supplement metadata.
   - If entity-to-file mapping is ambiguous, query Weaviate for enriched semantic context or nearest-relevant vector documents/meta.

4. **Requirements Synthesis**
   - Use LLM prompts combining extracted code, augmented with Weaviate’s metadata, to generate layered documentation:
     - Separate backend (DAO, DTO, service) and frontend sections.
     - Highlight relationships and data flows.
     - Document key business processes, endpoints, and model structures.

5. **Output**
   - Requirements documentation per project:
     - Clear backend vs. frontend sections/subsections.
     - Dedicated tables/lists of DAOs, DTOs, services, and frontend processes.
   - Store traceability data (i.e., mapping from requirements to source chunks/files).

### Nonfunctional
- Batch project support; incremental output generation.
- Progress/output traceability: all steps written to logs; all LLM prompts/responses stored.
- Modular codebase: processor and renderer classes, minimal shell scripting.

***

# PRD: Step 3 Agent-Based Implementation (step3-agent)

## 1. Purpose

Leverage autonomous agent(s) to:
- Analyze project metadata and source code iteratively, making decisions about what code/entities need deeper review.
- Actively distinguish backend (DAO/DTO/service) and frontend (GUI/UI/event) requirements.
- Dynamically decide when and how to augment information by querying Weaviate for enrichment.

## 2. Requirements

### Input
- Same as programmatic: `.env`, step2 JSON, Weaviate knowledge base.

### Architecture

- **Agent Controller:** Orchestrates multiple sub-agents, each responsible for either backend, frontend, or cross-cutting concerns.
- **Backend Agent:** Extracts DTO/DAO/service definitions, relationships, and business logic from code and metadata; also consults Weaviate as needed.
- **Frontend Agent:** Catalogs forms, UI logic, event bindings, API calls, and related business logic. Revisits source code as required and queries Weaviate for clarifications or enrichment.
- **Enricher Agent:** When any primary agent detects missing or ambiguous context, it triggers enrichment: querying Weaviate for similar chunks, patterns, or entity meta.

### Processing Flow

1. **Initialization**
   - Agents receive context/config, validate sources and connectivity.

2. **Domain Loop**
   - Agent controller instructs backend/fronted agents to process all relevant files/entities.
   - Agents may request additional context by re-reading source files or asking the Enricher Agent for Weaviate lookups.

3. **Interaction**
   - Agents regularly exchange intermediate hypotheses/data.
   - E.g., Backend agent finds service class with input of unknown DTO, triggers Enricher or Frontend agent to identify relevant UI or endpoint details and supply enriched documentation.

4. **Documentation Generation**
   - Agents collectively generate structured, cross-linked requirements sections:
     - Backend: DAO, DTO, Service, business rules.
     - Frontend: Forms, workflows, endpoints, UI models.
   - Mark every enrichment with its Weaviate source (traceability).

5. **Output**
   - Per-project requirements docs with explicit agent-provided separation of backend/frontend, detailed data flow, and enrichment audit trails.
   - Optionally, agent logs/audit data to support continual improvement.

### Nonfunctional
- Modular agent pattern (can swap/extend agents for additional domains e.g., security).
- Supports distributed/parallel runs if needed in the future.
- All agent interactions, LLM prompts, and vector queries are auditable.



## 2025.10.07 

bash -lc "cd /Users/thomaskamsker/Documents/Atom/vron.one/playground/a1javarag && source venv/bin/activate && echo CURRENT_ENV_OUTPUT_DIR=$(grep '^OUTPUT_DIR=' .env | cut -d'=' -f2); ls -1d output_* | tail -n 1"

now 

./run_iteration.sh --rotate-output --force-step1 --repeat-step2 --step3=both --step3-parallel --step3-max-workers 3

