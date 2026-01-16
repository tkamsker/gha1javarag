# Shell Script Audit Report
**Generated:** 2026-01-16
**Purpose:** Identify valid, redundant, outdated, and deprecated scripts

---

## Summary

**Total Scripts Found:** 22 (excluding .specify/ and .venv/)

### Status Breakdown
- ✅ **VALID & ESSENTIAL**: 10 scripts (keep)
- ⚠️ **VALID BUT REDUNDANT**: 5 scripts (consolidate)
- ❌ **OUTDATED**: 4 scripts (update or remove)
- 🗑️ **DEPRECATED**: 3 scripts (remove)

---

## ✅ VALID & ESSENTIAL SCRIPTS

These scripts are current, necessary, and actively used:

### 1. **docker-weaviate.sh** ✅
- **Purpose**: Comprehensive Weaviate Docker management
- **Commands**: start, stop, restart, status, clean, logs
- **OS Detection**: macOS vs Ubuntu compose files
- **Status**: VALID - Essential for Weaviate management
- **Notes**: Uses network_mode: host for Ollama access

### 2. **run-cuco.sh** ✅
- **Purpose**: Dedicated pipeline runner for cuco-ui-admin project
- **Features**:
  - Full pipeline (discover → extract → index → status)
  - Dependency resolution with --workspace-root
  - --create-schema flag (CRITICAL for DbTable schema)
  - Progress monitoring and logging
- **Status**: VALID - Production-ready for cuco project
- **Notes**: Includes sibling dependency search (Feature 005)

### 3. **run.sh** ✅
- **Purpose**: General pipeline runner for any project
- **Features**:
  - Auto-detects project name from pom.xml or uses timestamp
  - Supports monorepo mode (--project subdirectory)
  - Dependency resolution (--dependency-depth 1)
  - --create-schema flag (CRITICAL)
- **Status**: VALID - Primary pipeline script
- **Notes**: More flexible than run-cuco.sh

### 4. **start_streamlit.sh** ✅
- **Purpose**: Start Streamlit web UI (foreground mode)
- **Features**:
  - 8-step initialization with validation
  - Checks Ollama model availability
  - Sets OLLAMA_MODEL_NAME=qwen2.5-coder:32b
  - Clears Python cache
- **Status**: VALID - Feature 009 deployment
- **Created**: 2026-01-16 (recent)

### 5. **start_streamlit_background.sh** ✅
- **Purpose**: Start Streamlit in background with logging
- **Features**:
  - Uses nohup for background execution
  - Logs to streamlit.log
  - Returns PID for management
- **Status**: VALID - Production deployment
- **Created**: 2026-01-16 (recent)

### 6. **stop_streamlit.sh** ✅
- **Purpose**: Safely stop Streamlit application
- **Features**:
  - Graceful SIGTERM → forced SIGKILL
  - Verifies process stopped
- **Status**: VALID
- **Created**: 2026-01-16 (recent)

### 7. **status_streamlit.sh** ✅
- **Purpose**: Comprehensive Streamlit health monitoring
- **Features**:
  - Checks process, port, Ollama, Weaviate
  - Shows last 10 log lines
  - Displays URLs and quick actions
- **Status**: VALID
- **Created**: 2026-01-16 (recent)

### 8. **check-env.sh** ✅
- **Purpose**: Validate .env configuration
- **Features**:
  - Checks for common config issues
  - --fix option to auto-repair
- **Status**: VALID - Useful diagnostic tool

### 9. **check-services.sh** ✅
- **Purpose**: Test connectivity to all services
- **Features**:
  - Tests Ollama, Weaviate, SQLite
  - Works on macOS and Linux
- **Status**: VALID - Health check utility

### 10. **with-venv.sh** ✅
- **Purpose**: Run commands in virtual environment
- **Usage**: `./with-venv.sh codeindex --help`
- **Status**: VALID - Convenience wrapper

---

## ⚠️ VALID BUT REDUNDANT SCRIPTS

These scripts work but overlap with others or have better alternatives:

### 11. **step1.sh** ⚠️
- **Purpose**: Setup virtual environment
- **Creates**: `.venv` directory (correct)
- **Status**: REDUNDANT with manual setup
- **Recommendation**: KEEP as convenience script for new users
- **Notes**: Comprehensive with version checks and verification

### 12. **step2.sh** ⚠️
- **Purpose**: Generate PRD documents after indexing
- **Features**:
  - Runs all PRD layers (database, services, frontend, full)
  - Service health checks
  - Verification and statistics
- **Status**: REDUNDANT with direct `codeindex prd` commands
- **Recommendation**: KEEP for guided PRD generation workflow
- **Notes**: User-friendly wrapper with progress reporting

### 13. **production-requirements-generation.sh** ⚠️
- **Purpose**: Combined pipeline + PRD generation
- **Features**:
  - Runs run.sh + PRD generation in one script
  - Parallel PRD generation (services + frontend)
  - Uses --llm-timeout 240 --llm-retries 3
- **Status**: REDUNDANT with run.sh + step2.sh
- **Recommendation**: CONSOLIDATE into run.sh or remove
- **Notes**: Could be replaced by: `./run.sh && ./step2.sh`

### 14. **weaviate_stats.sh** ⚠️
- **Purpose**: Show Weaviate indexing statistics
- **Features**: Uses Python script to display stats
- **Status**: REDUNDANT with `codeindex status`
- **Recommendation**: KEEP as alternative diagnostic tool
- **Notes**: Requires `rich` Python package

### 15. **init-database.sh** ⚠️
- **Purpose**: Initialize SQLite databases for Streamlit
- **Status**: VALID but may not be needed if Streamlit auto-creates
- **Recommendation**: Test if still required, remove if redundant

---

## ❌ OUTDATED SCRIPTS

These scripts have issues or reference old patterns:

### 16. **setup_venv.sh** ❌
- **Purpose**: Create virtual environment
- **Issue**: Creates `venv/` directory instead of `.venv/`
- **Status**: OUTDATED - Inconsistent with step1.sh
- **Recommendation**: REMOVE - Use step1.sh instead
- **Notes**: All other scripts expect `.venv/` not `venv/`

### 17. **start_weaviate_simple.sh** ❌
- **Purpose**: Simple Weaviate startup
- **Issue**: Less comprehensive than docker-weaviate.sh
- **Status**: OUTDATED - Superseded by docker-weaviate.sh
- **Recommendation**: REMOVE - Use docker-weaviate.sh instead

### 18. **monitor-extraction.sh** ❌
- **Purpose**: Monitor overnight extraction progress
- **Issue**: Incomplete implementation (only has comments)
- **Status**: OUTDATED - Stub/placeholder
- **Recommendation**: REMOVE or implement properly
- **Notes**: Only 4 lines of comments, no actual code

### 19. **fix-weaviate-ollama.sh** ❌
- **Purpose**: Fix "text2vec-ollama module not found" error
- **Issue**: Should be fixed by --create-schema in run.sh
- **Status**: OUTDATED - Problem solved in pipeline
- **Recommendation**: REMOVE - Issue fixed by proper schema creation
- **Notes**: Was a workaround for schema issues

---

## 🗑️ DEPRECATED SCRIPTS

These scripts are for specific test scenarios or one-time migrations:

### 20. **validate_t015_production.sh** 🗑️
- **Purpose**: Validate Feature 008 improvements
- **Status**: DEPRECATED - Feature 008 complete
- **Recommendation**: ARCHIVE to tests/validation/
- **Notes**: Historical validation script

### 21. **deploy-ubuntu-prod.sh** 🗑️
- **Purpose**: Feature 007 production deployment guide
- **Status**: DEPRECATED - Feature 007 complete (76%)
- **Recommendation**: ARCHIVE to docs/deployment/
- **Notes**: Deployment documentation, not actively maintained

### 22. **scripts/validate_feature_007.sh** 🗑️
- **Purpose**: Validate Feature 007 completion
- **Status**: DEPRECATED - Feature 007 complete
- **Recommendation**: ARCHIVE to tests/validation/
- **Notes**: One-time validation script

---

## CRITICAL FINDINGS

### 🚨 Schema Creation Issue (RESOLVED)

**Problem**: User reported "No database tables found" in Streamlit Chat

**Root Cause**: Old Weaviate schema has `CodeArtifact` instead of typed classes like `DbTable`

**Solution**: Both `run.sh` and `run-cuco.sh` now use `--create-schema` flag:

```bash
# Line 163 in run.sh, Line 212 in run-cuco.sh
codeindex index --inventory "$DISCOVERY_FILE" --extraction "$EXTRACTION_FILE" --create-schema
```

**Impact**: Running either script will create the correct schema with:
- BackendDoc
- DaoCall
- **DbTable** ← Required for database analysis in Chat
- GwtModule
- JspForm
- IbatisStatement
- GwtEndpoint
- GwtUiBinder
- DtoArtifact
- Project

**Action Required**: User must run pipeline to create schema:
```bash
# Option 1: Clean rebuild
./docker-weaviate.sh clean
./docker-weaviate.sh start
./run-cuco.sh --yes /path/to/cuco-ui-admin

# Option 2: Quick check
curl -s http://localhost:8080/v1/schema | jq -r '.classes[].class'
# Should show DbTable, not just CodeArtifact
```

---

## RECOMMENDATIONS

### Immediate Actions

1. **REMOVE Outdated Scripts** ❌
   ```bash
   rm setup_venv.sh              # Use step1.sh instead
   rm start_weaviate_simple.sh   # Use docker-weaviate.sh instead
   rm monitor-extraction.sh      # Incomplete stub
   rm fix-weaviate-ollama.sh     # Issue resolved by --create-schema
   ```

2. **ARCHIVE Test/Validation Scripts** 🗑️
   ```bash
   mkdir -p tests/validation docs/deployment
   mv validate_t015_production.sh tests/validation/
   mv scripts/validate_feature_007.sh tests/validation/
   mv deploy-ubuntu-prod.sh docs/deployment/
   ```

3. **UPDATE Documentation**
   - Add STREAMLIT_DEPLOYMENT.md reference to main README
   - Document that run.sh and run-cuco.sh create schema automatically
   - Clarify that production-requirements-generation.sh = run.sh + step2.sh

4. **CONSOLIDATE Redundant Scripts** (Optional)
   - Consider merging production-requirements-generation.sh into run.sh with --prd flag
   - Example: `./run.sh myproject --prd` could run full pipeline + PRD generation

### Script Usage Guide

**For New Users:**
```bash
./step1.sh                                    # Setup environment
./docker-weaviate.sh start                    # Start Weaviate
./run.sh myproject /path/to/source            # Index codebase
./step2.sh myproject /path/to/source          # Generate PRDs
```

**For Production (cuco-ui-admin):**
```bash
./docker-weaviate.sh start
./run-cuco.sh --yes /path/to/cuco-ui-admin
# Or use production-requirements-generation.sh for all-in-one
```

**For Streamlit Web UI:**
```bash
./start_streamlit_background.sh               # Start in background
./status_streamlit.sh                         # Check status
./stop_streamlit.sh                           # Stop when done
```

**For Diagnostics:**
```bash
./check-services.sh                           # Test all services
./check-env.sh --fix                          # Validate .env
./with-venv.sh codeindex status               # Check indexing
```

---

## SCRIPT DEPENDENCY MATRIX

```
Essential Infrastructure:
  docker-weaviate.sh (Weaviate management)
  ├── check-services.sh (health checks)
  └── check-env.sh (config validation)

Pipeline Scripts:
  step1.sh (environment setup)
  ├── run.sh (general pipeline)
  │   └── step2.sh (PRD generation)
  └── run-cuco.sh (cuco-specific pipeline)
      └── production-requirements-generation.sh (all-in-one)

Streamlit Deployment:
  start_streamlit.sh (foreground)
  start_streamlit_background.sh (background)
  ├── status_streamlit.sh (monitoring)
  └── stop_streamlit.sh (shutdown)

Utilities:
  with-venv.sh (venv wrapper)
  weaviate_stats.sh (diagnostics)
  init-database.sh (SQLite setup)

Outdated (Remove):
  setup_venv.sh → use step1.sh
  start_weaviate_simple.sh → use docker-weaviate.sh
  monitor-extraction.sh → incomplete
  fix-weaviate-ollama.sh → issue resolved

Deprecated (Archive):
  validate_t015_production.sh → tests/validation/
  scripts/validate_feature_007.sh → tests/validation/
  deploy-ubuntu-prod.sh → docs/deployment/
```

---

## CONCLUSION

**Final Count:**
- **Keep**: 15 scripts (10 essential + 5 redundant but useful)
- **Remove**: 4 scripts (outdated)
- **Archive**: 3 scripts (deprecated test/validation)

**Most Important**: Ensure users run `run.sh` or `run-cuco.sh` with `--create-schema` flag to fix the "No database tables found" issue in Streamlit.
