<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# we have the issue that the quality is not sufficient we want now to have an stepped approach but using crew ai agent techniques  . please prepare an prd document for cursor ai application we have an .env file like \# =============================

# Java/JSP/GWT/JS → PRD Pipeline Configuration

# =============================

# Source Discovery

JAVA_SOURCE_DIR=/Users/thomaskamsker/Documents/Atom/vron.one/playground/java/cuco-core
JS_INCLUDE_GLOBS=**/*.js
GWT_INCLUDE_GLOBS=**/*.gwt.xml,**/*.ui.xml,**/*EntryPoint*.java,**/*Activity*.java,**/*Place*.java,**/*Service*.java,**/*RequestFactory*.java
JSP_INCLUDE_GLOBS=**/*.jsp,**/*.jspf
JAVA_INCLUDE_GLOBS=**/*.java

# Ollama Configuration

OLLAMA_MODEL_NAME=gemma3:12b

# llama3.1:8b

OLLAMA_EMBED_MODEL_NAME=nomic-embed-text
OLLAMA_BASE_URL=http://host.docker.internal:11434

# Weaviate Configuration

WEAVIATE_URL=http://localhost:8080
WEAVIATE_API_KEY=
WEAVIATE_GRPC_URL=localhost:50051

# Heuristics

GWT_RPC_DEFAULT_PATH=/gwt.rpc
GWT_RF_DEFAULT_PATH=/gwtRequest
JS_ROUTE_HINTS=\#/,\#/.*,/,/app/.*
JS_HTTP_METHOD_HINTS=GET,POST,PUT,DELETE,PATCH

# Output Configuration

OUTPUT_DIR=./data/output
BUILD_DIR=./data/build
LOG_LEVEL=INFO

# Project Configuration

DEFAULT_PROJECT_NAME=default-project
where JAVA_SOURCE_DIR gives the root to the java source which can be an project or an directory with several projects if there is an pom.xml file it is an project if not it is projects every directory name is then an project name.  in step1 we read all the sources and care about java and jsp files as well has htm html js xml xhtml and sql files  we need to use AI an local ollama llm which extracts maximum information per file and stores the information in an weavaiate datastore for later use .  we then use crewai to reiterate through all source files to create an structured json file for later use where we group the files per project to make an top down and bottom up approach. we need to work really through all files and know if we have worked on per project. then we go through all dao and dto elements to extract the data structures and rules then we should find services which might be later used then we go from jsp and html files top down to understand forms layout rules and which data they use and which bussiness rules are applied all things we dont have source coder for ar just linked we store information how it is read for later. use crewai agents for structuring that reading and understanding of the information  and in step 3 we go per project and group per frontend services data objets and api and extract an structured verry detailed requirements document in markup format and we use an prd file which explains and use the target solution like in our case  next js frontend with oauth security and and an micro service architecture where each are of data is covered and called via react apis which are done by an next js backend application like nestjs do it step by step

Below is a detailed PRD for a **stepped, CrewAI-driven requirements extraction pipeline** suitable for use in a Cursor AI application, strictly following your environment and process requirements. This document structures how source code is read, analyzed, and distilled into requirements using agentic methods and coordinated local LLM+vector DB processing.

***

# PRD: Multi-Step CrewAI Requirements Extraction Pipeline

## v1 – For Cursor AI


***

### 1. Goal

Build a multi-step requirements extraction pipeline using **CrewAI agents** orchestrated for top-down and bottom-up analysis of Java/JSP/JS/GWT projects.
The process must use a local Ollama LLM for semantic extraction, group results per project, and output requirements fit for a modern Next.js/OAuth/microservices architecture.

***

### 2. Inputs

#### Configuration

- `.env` file describing:
    - Root source directory, include patterns per tech stack, output/build/log dirs, default project name.
    - Ollama LLM and embedding model info, base URL.
    - Weaviate vector DB endpoints and API keys.
    - See user’s provided env block above for precise environment variable list.


#### Source Data

- Directory structure under `JAVA_SOURCE_DIR`:
    - Detects multi-project setups: if `pom.xml` in root, treat as one project; otherwise, every top-level directory = project.
- Files covered (by glob patterns):
    - `.java`, `.js`, `.jsp`, `.jspf`, `.htm`, `.html`, `.xml`, `.xhtml`, `.sql`, and key GWT files.
***

### 3. Pipeline Steps \& Agent Roles

#### Step 1: Source Discovery \& AI Extraction

**Objective:** Crawl all source files, extract max context per file using local Ollama LLM, and store rich file metadata in Weaviate per project.

- **Agents:**
    - `SourceReaderAgent`: Finds all relevant files, determines project boundaries via `pom.xml` or directory name.
    - `FileExtractorAgent`: Reads each file, gathers structure/comments/semantic info (classes, fields, forms, dependencies, endpoints, business logic hints). Calls Ollama LLM for per-file enrichment.
    - `DataStoreAgent`: Stores all extracted/enriched metadata into Weaviate with global/project/file/entity tags.
- **Artifacts:**
    - All enriched file-level knowledge stored in Weaviate, tagged by project/filename/entity.
    - Working set logs—trace which files/entities have been processed per project.


#### Step 2: Project Structuring \& Deep Analysis

**Objective:** Regroup and refine extracted data per project, building a deeply structured JSON index for use in requirements distillation.

- **Agents:**
    - `ProjectStructurerAgent`: Queries Weaviate for everything belonging to each project; builds an in-memory tree of files and detected entities per project (DAO, DTO, Service, JSP/UI, etc.).
    - `DAODTOAnalyzerAgent`: Traverses known DAOs/DTOs from source and Weaviate, extracts all data models, constraints, and associated business rules.
    - `ServiceLinkerAgent`: Identifies backend service classes, maps dependencies to DAOs/DTOs, prepares API-like summaries.
    - `FrontendAnalyzerAgent`: Goes from JSP/HTML files top-down, analyzes forms, input elements, layout, and data flow—links forms to data objects, business rules, and backend endpoints.
    - `LinkageAgent`: If cross-references are unresolved (e.g., data from frontend not mapped to backend), this agent flags, investigates, or re-triggers deeper file/Weaviate analysis for missing context.
- **Artifacts:**
    - Output: Structured per-project JSON containing all found files, entities, relationships, business/process rules, UI-data flow mappings.
    - All “uncertain” or externally linked information is explicitly tagged for later review or enrichment.


#### Step 3: Requirements Synthesis \& Target Solution Mapping

**Objective:** For each project, synthesize exhaustive, detailed requirements in Markdown—grouped into Frontend, Services, Data Objects, APIs—framed with a target migration solution (Next.js React apps, OAuth security, microservices via NestJS).

- **Agents:**
    - `RequirementsWriterAgent`: For each project, draws from JSON “knowledge base,” guides document creation top-down (section per Frontend, Service/API, Data Object), referencing the original file/agent source.
    - `SolutionMappingAgent`: Analyzes possible migration targets—Next.js frontend, OAuth, React APIs, NestJS backend—frames requirements so they fit the destination tech.
    - `ReviewAgent`: Iterates through generated requirements, spot-checks and cross-links business logic, API boundaries, and data models for completeness, flags inconsistencies or weakly inferred sections.
- **Artifacts:**
    - Per-project requirements documentation (Markdown), ready for modern frontend/microservices architecture.
    - Mapping table: how source legacy artifacts translate to Next.js microservices and React components.
    - Audit trail for requirements doc: for every section/entity, which agent/file/Weaviate entries it was synthesized from.

***

### 4. Additional Design Notes

- **Project Workspace Structure**

```
{OUTPUT_DIR}/
  /output/
    /{project}/
       requirements.md
       requirements_json.json
       mapping.md
  /build/
  /logs/
```

- **Traceability:** All agent actions, queries, and document edits logged by source and destination, enabling stepwise audit/reproducibility.
- **Extensibility:**
    - New agents or agent function expansions can support additional patterns (security, test analysis, etc).
    - Agents can queue or retry files/entities with low confidence or lacking context.
- **Quality Controls:**
    - Allow for manual agent override or retrigger per file/section if results are low-quality or ambiguous.
    - Document “gaps” for later human-in-the-loop review.

***

### 5. Example Target Solution Mapping Section

> \#\#\#\# Target System: Migration to Next.js + NestJS Microservices
> - All data objects will become DTOs in NestJS and interfaces in React components.
> - All legacy services will map to distinct NestJS endpoints, using JWT/OAuth for authentication (specify endpoints, scopes).
> - All JSP/GWT HTML forms will become React forms with corresponding data bindings and validation rules inferred from legacy business logic.
> - All inter-service calls/links described in requirements are mapped to REST/GraphQL APIs.

***

### 6. Success Criteria

- All source files processed and indexed in Weaviate, including enriched LLM output.
- Project boundaries discerned exactly by `pom.xml` or directory name.
- Each project outputs:

1. Structured JSON project index.
2. Complete requirements doc (with detailed mapping to Next.js/NestJS).
3. Per-entity traceability explaining data provenance and enrichment level.
- Gaps, unresolved references, or ambiguous rules identified and clearly labeled for manual follow-up.
- All steps auditable, rerunnable, and extensible by adding/kicking new agents.

***

This PRD turns agentic workflows into robust, stepwise project digestion—ensuring maximal coverage, minimal ambiguity, and easy alignment to a modern cloud, Next.js/NestJS solution.

Would you like a draft YAML or JSON for CrewAI/agent configuration, or a requirements example for one “project” as output?

