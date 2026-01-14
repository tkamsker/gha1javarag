# Feature 009: Streamlit Web Client - Quickstart Guide

## Overview

Feature 009 adds an interactive web interface to the GEMINI Code Analysis Pipeline with intelligent multi-agent capabilities powered by CrewAI framework.

**Key Capabilities**:
- 🔍 **Interactive Search**: Real-time semantic search over Weaviate with natural language queries
- 💬 **AI Agent Assistance**: 6 specialized agents (Senior Developer, Data Analyst, Frontend/Backend Specialists, PRD Writer, Spec-Kit Writer)
- 📊 **Visual Exploration**: Interactive relationship graphs, code viewer, file system browser
- 🤝 **Collaboration**: Shared workspaces, annotations, export reports (PDF, Markdown, JSON)
- 🚀 **Production-Ready**: Supports 50+ concurrent users with <2s search latency

## Quick Start

### Prerequisites

- Python 3.8+
- Weaviate running at `http://localhost:8080` (populated with artifacts)
- Ollama running at `http://localhost:11434` with gemma3:12b model
- `JAVA_SOURCE_DIR` environment variable set

### Installation

```bash
# Install dependencies (after Feature 009 implementation)
pip install streamlit crewai streamlit-code-editor streamlit-cytoscape reportlab

# Set environment variables
export JAVA_SOURCE_DIR=/path/to/java/source
export WEAVIATE_URL=http://localhost:8080
export OLLAMA_URL=http://localhost:11434

# Launch web application
streamlit run src/codeindex/web/app.py
```

### Access

Open browser to `http://localhost:8501`

## Core User Flows

### Flow 1: Search and Explore (2 minutes)

1. Open web UI at `http://localhost:8501`
2. Enter natural language query in search bar (e.g., "user authentication")
3. View results with artifact types, confidence scores, previews
4. Click result to see full metadata
5. Click "Show Relationships" to visualize dependencies
6. Click artifact node in graph to navigate

### Flow 2: Ask AI Agent (3 minutes)

1. Navigate to Chat page (💬 tab)
2. Type question (e.g., "What does the UserService do?")
3. Agent responds with explanation + citations
4. Ask follow-up question (context retained)
5. Click "Export Chat" to save conversation

### Flow 3: Generate PRD (5 minutes)

1. Navigate to Search page
2. Search for module (e.g., "payment processing")
3. Select relevant artifacts (checkboxes)
4. Click "Generate PRD" button
5. Watch multi-agent workflow progress
6. Download generated PRD (Markdown + PDF)

### Flow 4: Code Review (10 minutes)

1. Navigate to Files page (🗂️ tab)
2. Browse file tree, select files for review
3. Click "Start Code Review" button
4. Senior Developer + Backend Specialist analyze code
5. View findings report (design patterns, security, performance)
6. Export report as PDF

## Key Pages

| Page | URL | Purpose |
|------|-----|---------|
| Search | `/1_🔍_Search.py` | Semantic search over Weaviate |
| Chat | `/2_💬_Chat.py` | Ask questions to AI agents |
| Workspace | `/3_📊_Workspace.py` | Manage saved workspaces |
| Files | `/4_🗂️_Files.py` | Browse source code files |
| Settings | `/5_⚙️_Settings.py` | Configure agents and UI |

## Agent Roles

| Agent | Expertise | Example Query |
|-------|-----------|---------------|
| Senior Developer | Architecture, design patterns | "Explain the MVP pattern in this codebase" |
| Data Analyst | Database schemas, entity relationships | "Map all foreign keys in the database" |
| Frontend Specialist | GWT/JSP UI, navigation flows | "Document the user registration form" |
| Backend Specialist | Services, APIs, business logic | "How does the order processing service work?" |
| PRD Writer | Product requirements, user stories | "Generate PRD for checkout module" |
| Spec-Kit Writer | Technical specs, implementation plans | "Create spec for new payment gateway feature" |

## Configuration

Key environment variables (see `.env` file):

```bash
# Web Server
STREAMLIT_PORT=8501
STREAMLIT_HOST=localhost

# Data Sources
JAVA_SOURCE_DIR=/path/to/java/source   # Required
WEAVIATE_URL=http://localhost:8080     # Vector database
OLLAMA_URL=http://localhost:11434      # LLM service

# Agent Settings
OLLAMA_MODEL_NAME=gemma3:12b           # LLM model
MAX_CONCURRENT_AGENTS=3                # Parallel agent limit

# Storage
WORKSPACE_DB_PATH=data/workspaces.db   # SQLite database
ANNOTATIONS_DB_PATH=data/annotations.db
EXPORT_DIR=data/exports/               # Temporary export storage

# Logging
LOG_LEVEL=INFO                         # DEBUG, INFO, WARNING, ERROR
```

## Implementation Phases

| Phase | Duration | Deliverables | Status |
|-------|----------|--------------|--------|
| 1: Foundation | 2 weeks | Streamlit app, basic search, code viewer | Not Started |
| 2: Agent Framework | 2 weeks | CrewAI integration, chat interface, 6 agents | Not Started |
| 3: Multi-Agent Workflows | 2 weeks | PRD generation, code review workflows | Not Started |
| 4: Visualization | 2 weeks | Relationship graphs, workspaces, annotations | Not Started |
| 5: Advanced Features | 2 weeks | PDF export, file tree, follow-ups, shortcuts | Not Started |
| 6: Production | 2 weeks | Auth, rate limiting, metrics, deployment | Not Started |

**Total Estimated Duration**: 12 weeks

## Success Metrics

- **Adoption**: 80% of team uses web UI within 1 month
- **Performance**: Search <2s (p95), agent responses <30s (p95)
- **Quality**: Agent PRDs require <20% manual revision
- **Satisfaction**: NPS ≥8/10 for UI usability
- **Scalability**: Support 50 concurrent users

## Next Steps

1. **Review Spec**: Team reviews `spec.md` for completeness and accuracy
2. **Generate Plan**: Run `/speckit.plan` to create implementation plan
3. **Break Down Tasks**: Run `/speckit.tasks` to generate actionable task list
4. **Implement**: Run `/speckit.implement` to execute tasks
5. **Test**: Validate against constitution quality gates
6. **Deploy**: Launch web UI for team use

## Related Documentation

- **Full Specification**: `specs/009-streamlit-crewai-web-client/spec.md`
- **Constitution**: `.specify/memory/constitution.md`
- **Main README**: `CLAUDE.md`
- **Feature 001**: `specs/001-java-codebase-indexer/` (CLI foundation)
- **Feature 007**: `specs/007-gwt-navigation-and-error-fixes/` (GWT support)

## Support

For questions or issues:
- Review full spec: `specs/009-streamlit-crewai-web-client/spec.md`
- Check CLAUDE.md troubleshooting section
- Review Streamlit docs: https://docs.streamlit.io
- Review CrewAI docs: https://docs.crewai.com

---

**Version**: 1.0.0 | **Created**: 2026-01-14 | **Status**: Draft
