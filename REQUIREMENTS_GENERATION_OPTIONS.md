# Requirements Generation Options - Implementation Overview

This document explains all the options and improvements implemented for generating requirements in the codebase.

## Two Main Approaches

The system implements **two distinct approaches** for requirements generation:

### 1. **Per-Artifact Requirements Agent** (Original Approach)
- **Class:** `RequirementsAgent` in `src/synth/requirements_agent.py`
- **Usage:** Default when `--use-crewai` flag is NOT used
- **Method:** Generates individual requirement documents for each artifact

### 2. **CrewAI Multi-Agent Requirements** (Enhanced Approach)
- **Class:** `CrewAIRequirementsGenerator` in `src/synth/crewai_requirements.py`
- **Usage:** When `--use-crewai` flag is used
- **Method:** Uses multiple specialized AI agents working together

---

## Option 1: Per-Artifact Requirements Agent

### How It Works

```python
# CLI Command
python main.py requirements --project my-project
# (without --use-crewai flag)
```

**Process:**
1. Loads artifacts from `data/build/` directory
2. For each artifact (DAO call, JSP form, backend doc, GWT UiBinder):
   - Creates a detailed prompt with artifact content
   - Calls Ollama LLM to generate requirements
   - Saves individual markdown file per artifact
3. Creates an index file (`INDEX.md`) linking all generated files

**Artifact Types Processed:**
- `dao_calls` - DAO method calls
- `jsp_forms` - JSP form definitions
- `backend_docs` - Backend documentation summaries
- `gwt_uibinder` - GWT UiBinder components

**Output Structure:**
```
output/requirements/{project}/
├── INDEX.md
├── dao_calls/
│   ├── UserDao.java.md
│   └── OrderDao.java.md
├── jsp_forms/
│   ├── order_form.jsp.md
│   └── user_form.jsp.md
├── backend_docs/
│   └── ServiceClass.java.md
└── gwt_uibinder/
    └── OrderView.ui.xml.md
```

**Characteristics:**
- ✅ Simple, straightforward approach
- ✅ One requirement file per artifact
- ✅ Good for detailed artifact-level analysis
- ❌ No cross-artifact relationships
- ❌ No comprehensive project overview
- ❌ Limited context between artifacts

---

## Option 2: CrewAI Multi-Agent Requirements (Enhanced)

### How It Works

```python
# CLI Command
python main.py requirements --project my-project --use-crewai
# OR for all projects
python main.py requirements --all-projects --use-crewai
```

**Process:**
1. Creates a "crew" of specialized AI agents
2. Each agent has specific role, tools, and tasks
3. Agents work sequentially, building on each other's work
4. Final output is a comprehensive requirements document

### The Crew: 6 Specialized Agents

#### 1. **Backend Architecture Analyst**
- **Role:** Senior software architect (15+ years experience)
- **Goal:** Detailed backend code analysis mapping Java/Spring → NestJS + PostgreSQL
- **Tools:** 
  - `WeaviateSearchTool` - Search indexed artifacts
  - `SourceFileReaderTool` - Read source files directly
- **Tasks:**
  - Service Layer Analysis (map to NestJS Services)
  - Data Access Layer (map to TypeORM Entities & Repositories)
  - API/Controller Layer (map to NestJS Controllers)
  - Business Logic and Data Flow
  - Configuration and Dependency Injection
  - Database Schema (map to PostgreSQL with TypeORM)
- **Output:** Detailed backend architecture analysis

#### 2. **Dependency and Integration Analyst**
- **Role:** Senior DevOps architect and integration specialist
- **Goal:** Detailed dependency analysis mapping Java → NestJS/Next.js
- **Tools:** Same as Backend Analyst
- **Tasks:**
  - Build Dependencies (map to package.json)
  - Frontend Dependencies (map to Next.js/React packages)
  - Internal Module Dependencies
  - Database Dependencies
  - External Service Dependencies
  - API Contracts and Integration Points
  - Configuration Dependencies
  - Runtime Dependencies
- **Output:** Complete dependency mapping

#### 3. **Frontend Trace Specialist** ⭐ NEW
- **Role:** Meticulous frontend trace specialist
- **Goal:** Follow through ALL frontend files and ensure ALL logic is discovered
- **Tools:** Same as other agents
- **Tasks:**
  - Trace HTML files → extract scripts, forms, links, GWT modules
  - For each script → find and read JavaScript files
  - For each GWT module → find .gwt.xml, EntryPoint, Activity, Place files
  - For each JSP → extract includes, imports, form structures
  - For each UiBinder → find corresponding Java owner class
  - Follow all navigation links and place tokens
  - Document complete file relationships map
- **Output:** Complete inventory of all frontend files and relationships
- **Max Iterations:** 30 (more than others for thoroughness)
- **Max Time:** 60 minutes

#### 4. **Frontend Architecture Analyst**
- **Role:** Senior UX architect and frontend specialist
- **Goal:** Detailed frontend analysis mapping GWT/JSP/HTML → Next.js + React
- **Tools:** Same as other agents
- **Tasks:**
  - Pages and Routes (map GWT Activities/Places to Next.js pages)
  - Forms and User Input (map JSP forms to React components)
  - UI Components (map UiBinder to React components)
  - State Management (map GWT state to React state)
  - API Integration (map GWT RPC to Next.js API routes)
  - User Experience and Interactions
  - User Roles and Permissions
- **Output:** Complete frontend architecture mapping
- **Uses:** Frontend trace results as starting point

#### 5. **Technical Writer**
- **Role:** Senior technical writer (20+ years experience)
- **Goal:** Create professional, comprehensive requirements documents
- **Tools:** None (synthesizes other agents' work)
- **Tasks:**
  - Consolidate all analysis into structured document
  - Organize from frontend to backend
  - Include traceability matrices
  - Write for both technical and business stakeholders
- **Output:** Initial requirements document

#### 6. **Placeholder Fulfillment Specialist** ⭐ NEW
- **Role:** Meticulous requirements analyst
- **Goal:** Identify ALL placeholders and replace with specific information
- **Tools:** Same as other agents
- **Tasks:**
  - Review requirements document for placeholders
  - Actively search for missing information (5-10 tool calls per placeholder)
  - Replace placeholders with specific details
  - Document what was found and where
- **Output:** Final requirements document with zero placeholders
- **Max Iterations:** 30
- **Max Time:** 60 minutes

### Workflow Sequence

```
1. Backend Architecture Analyst
   ↓
2. Dependency Analyst
   ↓
3. Frontend Trace Specialist ⭐ NEW
   ↓
4. Frontend Architecture Analyst
   ↓
5. Technical Writer
   ↓
6. Placeholder Fulfillment Specialist ⭐ NEW
   ↓
Final Requirements Document
```

### Tools Available to Agents

#### WeaviateSearchTool
- **Purpose:** Search Weaviate vector database for artifacts
- **Features:**
  - Multiple search strategies (BM25, vector search, fallback)
  - Project filtering
  - Supports multiple artifact types
  - Returns metadata with results
- **Artifact Types Supported:**
  - `BackendDoc`, `DaoCall`, `JspForm`, `IbatisStatement`, `DbTable`
  - `GwtModule`, `GwtUiBinder`, `GwtActivityPlace`
  - `JsArtifact`, `HtmlArtifact` ⭐ NEW

#### SourceFileReaderTool
- **Purpose:** Read source files directly from `JAVA_SOURCE_DIR`
- **Features:**
  - Pattern matching (e.g., `*Dao.java`, `*.jsp`)
  - Project filtering
  - File type filtering (java, jsp, xml, js, sql, html ⭐ NEW)
  - Reads up to 50KB per file
  - Handles multiple files (up to 10 by default)
- **Use Case:** When Weaviate search fails or when specific files are needed

### Output Structure

```
output/requirements/
├── {project}_crewai_requirements.md  (Main document)
├── {project}_code_analysis.md         (Backend analysis)
├── {project}_dependencies_analysis.md (Dependencies)
├── {project}_frontend_trace.md        (Frontend trace) ⭐ NEW
├── {project}_ui_analysis.md            (Frontend analysis)
└── {project}_initial_requirements.md  (Before placeholder fulfillment)
```

### Document Structure (Frontend → Backend)

1. **Executive Summary**
2. **Project Overview**
3. **Frontend Requirements (Next.js + React)**
   - Pages and Routes
   - UI Components
   - State Management
   - API Integration
   - User Experience
4. **Backend Requirements (NestJS + PostgreSQL)**
   - API Layer (Controllers)
   - Service Layer
   - Data Access Layer (TypeORM)
   - Database Schema
   - Business Logic
5. **Integration Requirements**
6. **Technical Architecture**
7. **Non-Functional Requirements**
8. **Traceability Matrix**

---

## Key Improvements Implemented

### 1. **HTML/HTM File Support** ⭐ NEW
- HTML files are discovered and extracted
- GWT features detected (nocache scripts, modules)
- HTML artifacts indexed in Weaviate as `HtmlArtifact` class
- Frontend Trace Agent traces HTML files

### 2. **Frontend Trace Agent** ⭐ NEW
- Ensures ALL frontend files are discovered
- Traces relationships between files
- Follows references (scripts, forms, links, GWT modules)
- Creates complete frontend file map

### 3. **Placeholder Fulfillment Agent** ⭐ NEW
- Actively searches for missing information
- Replaces all placeholders with specific details
- Ensures zero placeholders in final document
- Documents search attempts and findings

### 4. **Enhanced Search Tools**
- Multiple search strategies with fallbacks
- Direct file reading when search fails
- Project-aware filtering
- Metadata included in results

### 5. **Target Architecture Mapping**
- Java/Spring → NestJS + PostgreSQL
- GWT/JSP → Next.js + React
- Specific file path mappings
- Code transformation examples

### 6. **Comprehensive Analysis**
- Backend: Service → DAO → Database flow
- Frontend: HTML → JS → GWT → Backend flow
- Dependencies: Build → Runtime → External
- Integration: API contracts, endpoints, data formats

### 7. **Traceability**
- Every requirement linked to source artifacts
- File paths, class names, method names included
- Migration path documented for each component

---

## Comparison: Per-Artifact vs CrewAI

| Feature | Per-Artifact | CrewAI Multi-Agent |
|---------|-------------|-------------------|
| **Approach** | One file per artifact | Comprehensive project document |
| **Context** | Limited to single artifact | Cross-artifact relationships |
| **Frontend Coverage** | Basic | Complete with trace |
| **HTML Support** | ❌ | ✅ |
| **Placeholder Handling** | ❌ | ✅ Active fulfillment |
| **Target Architecture** | Generic | Specific (NestJS/Next.js) |
| **Traceability** | Basic | Complete with matrices |
| **Execution Time** | Faster (per artifact) | Slower (comprehensive) |
| **Output Quality** | Good for details | Excellent for overview |
| **Use Case** | Quick artifact analysis | Full project migration planning |

---

## Usage Examples

### Per-Artifact Approach
```bash
# Generate requirements for one project
python main.py requirements --project cuco-core

# Generate for all projects
python main.py requirements --all-projects
```

### CrewAI Approach
```bash
# Generate comprehensive requirements for one project
python main.py requirements --project cuco-core --use-crewai

# Generate for all projects (recommended)
python main.py requirements --all-projects --use-crewai

# Or use the convenience script
./start_requirements_generation.sh 1  # All projects
./start_requirements_generation.sh 2 cuco-ui-admin  # Specific project
```

---

## Recommendations

### Use Per-Artifact When:
- You need detailed analysis of specific artifacts
- Quick turnaround is needed
- You're focusing on individual components
- HTML/frontend trace is not critical

### Use CrewAI When:
- You need comprehensive project overview
- Planning full migration (Java → NestJS/Next.js)
- Frontend trace is important
- You want zero placeholders
- You need complete traceability

### Best Practice:
**Use CrewAI for production requirements generation** - it provides the most comprehensive, actionable requirements with complete frontend coverage and target architecture mapping.

---

## Future Enhancements

Potential improvements that could be added:

1. **Parallel Agent Execution** - Run some agents in parallel for speed
2. **Incremental Updates** - Update requirements when code changes
3. **Validation Agent** - Verify requirements completeness
4. **Comparison Agent** - Compare with previous requirements versions
5. **Visualization** - Generate diagrams from requirements
6. **Export Formats** - Export to Jira, Confluence, etc.

---

## Technical Details

### Configuration
- **LLM:** Ollama (configurable via `OLLAMA_MODEL_NAME`)
- **Embeddings:** Ollama nomic-embed-text
- **Vector DB:** Weaviate
- **Timeout:** 20 minutes per agent task (configurable)
- **Max Iterations:** 20-30 per agent (configurable)

### Error Handling
- Agents continue on errors (non-blocking)
- Partial results saved if agent fails
- Logging for debugging
- Graceful degradation

### Performance
- **Per-Artifact:** ~1-5 minutes per artifact
- **CrewAI:** ~10-60 minutes per project (depending on size)
- **All Projects:** ~8-15 hours total

---

## Summary

The codebase implements **two complementary approaches** for requirements generation:

1. **Per-Artifact Agent** - Simple, fast, artifact-focused
2. **CrewAI Multi-Agent** - Comprehensive, thorough, project-focused with:
   - 6 specialized agents
   - Frontend trace capability
   - Placeholder fulfillment
   - HTML/HTM support
   - Target architecture mapping
   - Complete traceability

**The CrewAI approach is recommended for production use** as it provides the most comprehensive requirements with complete frontend coverage and ensures all logic is discovered and documented.

