# Quickstart Guide: PRD Document Generation

**Feature**: 002-prd-document-generation
**Date**: 2025-12-14
**Phase**: Phase 1 - Getting Started

## Overview

This guide walks you through using the PRD Document Generation feature to analyze your Java codebase and generate comprehensive Product Requirements Documents. You'll learn how to run analysis for each layer (database, services, frontend) and generate complete PRD documentation.

## Prerequisites

Before you begin, ensure you have:

1. **Feature 001 Completed**: Your codebase must be indexed in Weaviate
   ```bash
   # Run Feature 001 pipeline if not already done
   codeindex discover --source-dir /path/to/java/source
   codeindex extract
   codeindex index
   ```

2. **Services Running**:
   ```bash
   # Ollama must be running
   ollama serve

   # Verify Ollama is accessible
   curl http://localhost:11434/api/tags

   # Weaviate must be running
   ./docker-weaviate.sh start

   # Verify Weaviate is accessible
   curl http://localhost:8080/v1/meta
   ```

3. **Environment Variables Configured** (in `.env` file):
   ```env
   JAVA_SOURCE_DIR=/path/to/your/java/source
   OLLAMA_MODEL_NAME=gemma3:12b
   OLLAMA_URL=http://localhost:11434
   WEAVIATE_URL=http://localhost:8080
   OUTPUT_DIR=./output
   ```

4. **Python Environment**:
   ```bash
   # Activate virtual environment
   source .venv/bin/activate

   # Install/update dependencies
   pip install -e .
   ```

## Basic Usage

### Quick Start: Generate Full PRD

Generate a complete PRD analyzing all layers:

```bash
codeindex prd --project myapp
```

**What happens**:
- Analyzes database layer (DAOs, entities, SQL files)
- Analyzes service layer (services, controllers, REST endpoints)
- Analyzes frontend layer (JSPs, GWT components, JavaScript)
- Generates layer-specific PRDs and master PRD
- Creates cross-references showing end-to-end flows

**Output location**: `./output/prd/master_prd.md`

**Expected duration**: 5-15 minutes depending on codebase size

---

## Layer-by-Layer Analysis

### Layer 1: Database Analysis

Analyze database entities, schemas, and business rules:

```bash
codeindex prd database --project myapp
```

**What it analyzes**:
- DAO classes (Data Access Objects)
- JPA/Hibernate entity classes with annotations
- iBATIS/MyBatis mapper XML files
- SQL DDL files (CREATE TABLE statements)
- Database constraints and relationships

**Generated files**:
```
output/
├── database/
│   ├── index.md                    # Database entities index
│   └── entities/
│       ├── user.json               # User entity details
│       ├── invoice.json
│       └── ...
├── business_rules/
│   ├── index.md
│   ├── BR_001_email_validation.json
│   └── ...
└── prd/
    └── database_prd.md             # Database layer PRD
```

**Sample output** (`output/database/entities/user.json`):

```json
{
  "id": "user",
  "name": "user",
  "qualified_name": "public.user",
  "source_type": "jpa_annotation",
  "source_files": [
    "/path/to/User.java",
    "/path/to/UserDAO.java"
  ],
  "columns": [
    {
      "name": "id",
      "data_type": "BIGINT",
      "nullable": false,
      "description": "Primary key, auto-generated"
    },
    {
      "name": "email",
      "data_type": "VARCHAR(255)",
      "nullable": false,
      "description": "User email address, must be unique"
    }
  ],
  "primary_key": ["id"],
  "business_rules": ["BR_001_email_validation"],
  "description": "Stores user account information including credentials and profile data.",
  "domain": "auth",
  "created_at": "2025-12-14T10:30:15Z"
}
```

**Use case**: Understanding data model before planning migrations or modernization.

---

### Layer 2: Service Analysis

Analyze backend services, business logic, and API endpoints:

```bash
codeindex prd services --project myapp
```

**What it analyzes**:
- Service classes (business logic services)
- DAO services (data access layer)
- REST controllers and endpoints
- Service dependencies and orchestration
- Transaction boundaries
- Business rules in service layer

**Generated files**:
```
output/
├── services/
│   ├── index.md                         # Services index
│   ├── definitions/
│   │   ├── UserService.json             # Service definition
│   │   ├── BillingService.json
│   │   └── ...
│   └── endpoints/
│       ├── POST_api_user_create.json    # API endpoint details
│       ├── GET_api_user_{id}.json
│       └── ...
├── business_rules/
│   ├── BR_010_password_strength.json    # Service-level rules
│   └── ...
└── prd/
    └── service_prd.md                   # Service layer PRD
```

**Sample output** (`output/services/definitions/UserService.json`):

```json
{
  "id": "com.example.service.UserService",
  "class_name": "UserService",
  "qualified_name": "com.example.service.UserService",
  "package": "com.example.service",
  "source_file": "/path/to/UserService.java",
  "service_type": "business_service",
  "description": "Manages user account lifecycle including registration, authentication, profile updates, and account deactivation.",
  "operations": [
    {
      "name": "createUser",
      "signature": "public User createUser(UserRegistrationDTO dto) throws ValidationException",
      "return_type": "User",
      "parameters": [
        {
          "name": "dto",
          "type": "UserRegistrationDTO",
          "description": "User registration data"
        }
      ],
      "description": "Creates a new user account after validating email uniqueness and password strength.",
      "annotations": ["@Transactional"]
    }
  ],
  "dependencies": [
    {
      "target_service": "UserDAO",
      "dependency_type": "injection",
      "injection_method": "constructor"
    }
  ],
  "data_dependencies": ["user", "role"],
  "endpoints": ["POST_api_user_create"],
  "business_rules": ["BR_010_password_strength", "BR_011_email_uniqueness"],
  "domain": "auth",
  "created_at": "2025-12-14T10:35:22Z"
}
```

**Use case**: Documenting API contracts, understanding service dependencies, planning API modernization.

---

### Layer 3: Frontend Analysis

Analyze user interfaces, forms, and navigation flows:

```bash
codeindex prd frontend --project myapp
```

**What it analyzes**:
- JSP files with forms and UI elements
- HTML templates
- GWT modules, widgets, activities, views
- JavaScript files (client-side logic)
- Form validation rules
- Navigation flows and user journeys

**Generated files**:
```
output/
├── frontend/
│   ├── index.md                              # Frontend index
│   ├── forms/
│   │   ├── user_registration.json            # Form definition
│   │   ├── invoice_edit.json
│   │   └── ...
│   ├── components/
│   │   ├── UserListView.json                 # UI component
│   │   ├── InvoiceGrid.json
│   │   └── ...
│   └── navigation/
│       ├── user_registration_flow.json       # Navigation flow
│       └── ...
├── business_rules/
│   ├── BR_020_client_side_email_validation.json
│   └── ...
└── prd/
    └── frontend_prd.md                       # Frontend layer PRD
```

**Sample output** (`output/frontend/forms/user_registration.json`):

```json
{
  "id": "user_registration",
  "name": "user_registration",
  "source_file": "/path/to/register.jsp",
  "form_type": "jsp_form",
  "description": "User registration form collecting email, password, and profile information for new account creation.",
  "fields": [
    {
      "name": "email",
      "label": "Email Address",
      "type": "email",
      "required": true,
      "validation_pattern": "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}$",
      "validation_message": "Please enter a valid email address",
      "bound_column": "email"
    },
    {
      "name": "password",
      "label": "Password",
      "type": "password",
      "required": true,
      "validation_pattern": "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$",
      "validation_message": "Password must be at least 8 characters with uppercase, lowercase, number, and special character",
      "bound_column": "password_hash"
    }
  ],
  "submission_endpoint": "POST_api_user_create",
  "submission_method": "POST",
  "validation_rules": ["BR_020_client_side_email_validation"],
  "bound_entities": ["user"],
  "navigation_on_success": "/login.jsp",
  "navigation_on_cancel": "/index.jsp",
  "security_patterns": ["CSRF token included"],
  "domain": "auth",
  "created_at": "2025-12-14T10:40:15Z"
}
```

**Use case**: Planning UI modernization, understanding user workflows, replicating UX in new frameworks.

---

## Advanced Usage

### Custom Output Directory

Specify a custom output location:

```bash
codeindex prd --project myapp --output-dir /path/to/custom/output
```

---

### Force Refresh (Ignore Visit Log)

Re-analyze all files even if unchanged (useful after prompt/model updates):

```bash
codeindex prd --project myapp --force-refresh
```

**When to use**:
- After upgrading LLM model
- After changing prompt templates
- When you suspect cached analysis is incorrect

---

### Adjust LLM Settings

Customize LLM timeout and concurrency:

```bash
codeindex prd --project myapp --llm-timeout 180 --llm-retries 5 --parallel 5
```

**Parameters**:
- `--llm-timeout 180`: 3-minute timeout per LLM call
- `--llm-retries 5`: Retry up to 5 times on failure
- `--parallel 5`: Process 5 files concurrently

**When to adjust**:
- Large or complex files may need longer timeout
- Unstable LLM service may benefit from more retries
- Lower concurrency if LLM service gets overloaded

---

### Domain-Specific Analysis

Analyze only entities in a specific business domain:

```bash
codeindex prd --project myapp --domain-filter auth
```

**Result**: Only analyzes and documents entities tagged with domain `auth`.

**Use cases**:
- Focused subsystem documentation
- Module-specific modernization planning
- Domain-driven design analysis

---

### Include HTML Output

Generate HTML versions of markdown PRDs:

```bash
codeindex prd --project myapp --include-html
```

**Result**: Creates `.html` files alongside `.md` files for easy viewing in browsers.

---

### Skip Specific Layers

Generate PRD but skip one or more layers:

```bash
# Skip frontend (backend-only system)
codeindex prd full --skip-frontend --project myapp

# Skip services (database-first analysis)
codeindex prd full --skip-services --project myapp
```

---

## Understanding Output

### Directory Structure

After running full analysis:

```
output/
├── .visit_log.jsonl                 # File visit tracking (incremental processing)
├── database/
│   ├── index.md                     # Quick reference to all entities
│   └── entities/
│       ├── user.json
│       └── ...
├── services/
│   ├── index.md                     # Services catalog
│   ├── definitions/
│   │   └── UserService.json
│   └── endpoints/
│       └── POST_api_user_create.json
├── frontend/
│   ├── index.md                     # UI components catalog
│   ├── forms/
│   │   └── user_registration.json
│   ├── components/
│   │   └── UserListView.json
│   └── navigation/
│       └── user_registration_flow.json
├── business_rules/
│   ├── index.md                     # All business rules
│   ├── BR_001_email_validation.json
│   └── ...
└── prd/
    ├── index.md                     # Master PRD table of contents
    ├── master_prd.md                # Complete synthesized PRD
    ├── database_prd.md              # Database layer PRD
    ├── service_prd.md               # Service layer PRD
    ├── frontend_prd.md              # Frontend layer PRD
    └── cross_references.md          # Cross-layer flows (UI → Service → DB)
```

---

### Key Files to Review

1. **master_prd.md**: Start here for comprehensive overview
2. **cross_references.md**: Understand end-to-end flows (most valuable for modernization)
3. **database/index.md**: Quick reference to all data entities
4. **services/index.md**: API catalog
5. **frontend/index.md**: UI components catalog
6. **business_rules/index.md**: All extracted business rules

---

### Visit Log

The `.visit_log.jsonl` file tracks analyzed files for incremental processing:

```jsonl
{"file_path": "/path/to/UserDAO.java", "timestamp": "2025-12-14T10:30:15Z", "status": "success", "content_hash": "a1b2c3...", "layer": "database", "duration_seconds": 2.34}
{"file_path": "/path/to/UserService.java", "timestamp": "2025-12-14T10:32:48Z", "status": "success", "content_hash": "f6e5d4...", "layer": "service", "duration_seconds": 3.12}
```

**Benefits**:
- Subsequent runs skip unchanged files (faster analysis)
- Resume interrupted runs
- Track analysis history

---

## Common Troubleshooting

### Issue: "Project not found in Weaviate"

**Symptom**: Error message "No artifacts found for project 'myapp'"

**Solution**:
```bash
# Verify project exists in Weaviate
codeindex status

# If not indexed, run Feature 001 pipeline
codeindex discover --source-dir /path/to/java/source
codeindex extract
codeindex index --project myapp
```

---

### Issue: "Cannot connect to Ollama"

**Symptom**: Error message "Cannot connect to Ollama at http://localhost:11434"

**Solution**:
```bash
# Start Ollama
ollama serve

# Verify Ollama is running
curl http://localhost:11434/api/tags

# Check if model is available
ollama list | grep gemma3:12b

# Pull model if missing
ollama pull gemma3:12b
```

---

### Issue: "LLM timeout" errors

**Symptom**: Many files marked as "failed" due to timeout

**Solution 1**: Increase timeout:
```bash
codeindex prd --project myapp --llm-timeout 240
```

**Solution 2**: Reduce concurrency (less load on LLM):
```bash
codeindex prd --project myapp --parallel 3
```

**Solution 3**: Use a smaller/faster model:
```bash
export OLLAMA_MODEL_NAME=gemma2:7b
codeindex prd --project myapp
```

---

### Issue: "Invalid JSON response from LLM"

**Symptom**: Errors like "Failed to parse LLM response as JSON"

**Likely cause**: Model is generating text outside of JSON structure

**Solution**:
```bash
# Force refresh with retry logic
codeindex prd --project myapp --force-refresh --llm-retries 5
```

The retry logic includes prompt adjustments to enforce JSON-only output.

---

### Issue: Analysis is slow

**Symptom**: Analysis takes >30 minutes for medium-sized codebase

**Solutions**:

1. **Increase parallelism** (if LLM can handle it):
   ```bash
   codeindex prd --project myapp --parallel 20
   ```

2. **Skip unchanged files** (use visit log):
   ```bash
   # Don't use --force-refresh on subsequent runs
   codeindex prd --project myapp
   ```

3. **Analyze layers separately** (spread work over time):
   ```bash
   codeindex prd database --project myapp
   codeindex prd services --project myapp
   codeindex prd frontend --project myapp
   ```

---

### Issue: Missing entities in output

**Symptom**: Expected entities not appearing in output

**Diagnosis**:
```bash
# Check visit log for failures
grep "failed" output/.visit_log.jsonl

# Check verbose logs
codeindex prd --project myapp --verbose
```

**Solution**:
- Review failed files in visit log
- Check if files are being excluded (generated code filter)
- Verify source directory is correct
- Try re-analyzing specific layer with `--force-refresh`

---

## Sample Workflows

### Workflow 1: Initial Documentation for Legacy System

**Goal**: Create comprehensive documentation for an undocumented legacy Java application.

**Steps**:
```bash
# 1. Index codebase (Feature 001)
codeindex discover --source-dir /legacy/app/src
codeindex extract
codeindex index --project legacy-app

# 2. Generate complete PRD
codeindex prd --project legacy-app --output-dir /docs/legacy-app

# 3. Review master PRD
open /docs/legacy-app/prd/master_prd.md

# 4. Review cross-layer flows for critical features
open /docs/legacy-app/prd/cross_references.md

# 5. Export to HTML for stakeholders
codeindex prd --project legacy-app --include-html --output-dir /docs/legacy-app
```

**Outcome**: Comprehensive documentation ready for modernization planning.

---

### Workflow 2: API Modernization Planning

**Goal**: Document existing REST APIs to plan migration to microservices.

**Steps**:
```bash
# 1. Analyze only service layer
codeindex prd services --project myapp --output-dir /docs/api-migration

# 2. Review service definitions
ls /docs/api-migration/services/definitions/

# 3. Review API endpoints
ls /docs/api-migration/services/endpoints/

# 4. Review service dependencies (for microservices boundaries)
cat /docs/api-migration/prd/service_prd.md | grep -A 10 "Dependencies"
```

**Outcome**: Detailed API catalog with dependencies, ready for microservices decomposition.

---

### Workflow 3: Database Migration Planning

**Goal**: Understand current database schema for migration to new database system.

**Steps**:
```bash
# 1. Analyze only database layer
codeindex prd database --project myapp --output-dir /docs/db-migration

# 2. Review entity relationship diagram (if generated)
cat /docs/db-migration/database/schema_diagram.mmd

# 3. Review business rules at database level
cat /docs/db-migration/business_rules/index.md

# 4. Export to JSON for schema migration tooling
# (entity JSON files already in JSON format)
```

**Outcome**: Complete database schema documentation with business rules for migration planning.

---

### Workflow 4: UI Modernization (Rewriting Frontend)

**Goal**: Document existing UI to replicate in React/Vue/Angular.

**Steps**:
```bash
# 1. Analyze frontend layer
codeindex prd frontend --project myapp --output-dir /docs/ui-rewrite

# 2. Review form definitions
ls /docs/ui-rewrite/frontend/forms/

# 3. Review navigation flows
ls /docs/ui-rewrite/frontend/navigation/

# 4. Review cross-references to understand backend APIs used by frontend
cat /docs/ui-rewrite/prd/cross_references.md

# 5. Use form definitions as spec for new UI components
cat /docs/ui-rewrite/frontend/forms/user_registration.json
```

**Outcome**: Detailed UI specifications for frontend rewrite in modern framework.

---

### Workflow 5: Incremental Analysis During Active Development

**Goal**: Keep PRD documentation up-to-date as code changes.

**Steps**:
```bash
# 1. Initial full analysis
codeindex prd --project myapp

# 2. After code changes, re-run (only changed files analyzed)
codeindex prd --project myapp
# Visit log ensures only changed files are re-analyzed

# 3. Review what changed
git diff output/prd/master_prd.md
```

**Outcome**: Always-up-to-date documentation with minimal re-analysis time.

---

## Next Steps

After generating your PRD:

1. **Review Documentation**: Start with `master_prd.md` for overview
2. **Validate Findings**: Spot-check LLM-generated descriptions for accuracy
3. **Plan Modernization**: Use cross-references to identify migration priorities
4. **Share with Stakeholders**: Export to HTML or PDF for non-technical stakeholders
5. **Iterate**: Re-run analysis as codebase evolves

For more details:
- **Data Model**: See `data-model.md` for entity structures
- **CLI Reference**: See `contracts/cli-interface.md` for all command options
- **Output Formats**: See `contracts/output-formats.md` for file format details
- **LLM Contracts**: See `contracts/llm-contracts.md` for prompt templates

---

## Getting Help

If you encounter issues:

1. **Check Logs**: Use `--verbose` flag for detailed logging
2. **Review Visit Log**: Check `output/.visit_log.jsonl` for failed files
3. **Test Services**: Verify Weaviate and Ollama are running and accessible
4. **Consult Documentation**: Review contracts and data model specifications
5. **File Issue**: Report bugs or feature requests on GitHub

---

## Performance Benchmarks

Expected performance on typical codebases:

| Codebase Size | Database Layer | Service Layer | Frontend Layer | Total (Full PRD) |
|---------------|----------------|---------------|----------------|------------------|
| Small (10-50 files) | 1-2 min | 1-3 min | 2-5 min | 5-10 min |
| Medium (50-200 files) | 3-8 min | 5-15 min | 10-25 min | 15-45 min |
| Large (200-1000 files) | 10-30 min | 20-60 min | 30-90 min | 60-180 min |
| Very Large (1000+ files) | 30+ min | 60+ min | 90+ min | 180+ min |

**Note**: Times assume 10 parallel LLM calls, 120s timeout, gemma3:12b model on typical hardware.

---

## Tips for Best Results

1. **Run Feature 001 First**: Always ensure codebase is indexed in Weaviate
2. **Use Visit Log**: Don't use `--force-refresh` unless necessary (much faster)
3. **Start with One Layer**: Analyze database → services → frontend for incremental understanding
4. **Adjust Concurrency**: Start with default (10), increase if LLM is underutilized, decrease if timeouts occur
5. **Review Output Incrementally**: Don't wait for full analysis; review layer outputs as they complete
6. **Validate LLM Output**: Spot-check generated descriptions for accuracy
7. **Use Domain Filters**: For large codebases, analyze by domain for manageable documentation
8. **Export to HTML**: Easier for stakeholders to navigate than raw markdown

---

Happy documenting!
