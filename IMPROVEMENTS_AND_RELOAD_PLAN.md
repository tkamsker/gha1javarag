# Improvements and Reload Plan

## Overview

This document outlines the improvements made and step-by-step plan to reload all data with enhanced metadata support and improved CrewAI requirements generation.

## Improvements Made

### 1. ✅ Metadata Storage in Weaviate

**Problem:** The `meta` field from artifacts was not being stored in Weaviate, losing valuable metadata.

**Fix Applied:**
- Added `meta` field to all Weaviate class schemas
- Updated `index_artifact()` to serialize and store `meta` as JSON string
- Updated `search_artifacts()` to parse `meta` JSON back to dict
- Enhanced search results to include all metadata fields

**Files Modified:**
- `src/store/weaviate_client.py`

### 2. ✅ Enhanced CrewAI Prompts

**Problem:** CrewAI prompts were too generic and didn't produce detailed, area-specific requirements.

**Fix Applied:**
- **Code Analyst Task**: Now includes 5 detailed sections:
  - Backend Architecture Analysis
  - Database Layer Analysis
  - Data Flow and Business Logic
  - Technical Architecture Patterns
  - Integration Points

- **Dependency Analyst Task**: Now includes 6 detailed sections:
  - Internal Module Dependencies
  - Build and Configuration Requirements
  - Frontend Dependencies
  - External Service Dependencies
  - Integration Points and API Contracts
  - Runtime Dependencies

- **UI Analyst Task**: Now includes 6 detailed sections:
  - Forms and User Input Screens
  - Navigation Flows and User Journeys
  - UI Components and Interactions
  - User Roles and Permissions
  - UI State Management
  - User Experience Patterns

- **Technical Writer Task**: Now includes 10-section document structure:
  - Executive Summary
  - Project Overview
  - Functional Requirements (by area)
  - Technical Requirements
  - Dependencies
  - UI Specifications
  - Database Schema
  - API Contracts
  - Non-Functional Requirements
  - Traceability Matrix

**Files Modified:**
- `src/synth/crewai_requirements.py`

### 3. ✅ Enhanced Search Tool Results

**Problem:** Search tool didn't include metadata in results.

**Fix Applied:**
- Updated `WeaviateSearchTool` to include metadata in output
- Shows relevant metadata fields (excluding large fields like rawXml)
- Better formatted output with metadata context

**Files Modified:**
- `src/synth/crewai_requirements.py`

### 4. ✅ Search Command Enhancement

**Problem:** No way to explicitly search across all projects.

**Fix Applied:**
- Added `--all` / `-a` flag to search commands
- Shows project column when searching all projects
- Better output formatting

**Files Modified:**
- `src/cli.py`

## Step-by-Step Reload Plan

### Step 1: Clear Weaviate Data

**Option A: Use the reload script (Recommended)**
```bash
./reload_all_data.sh
```

**Option B: Manual clear**
```bash
python3 << 'EOF'
from store.weaviate_client import WeaviateClient
wc = WeaviateClient(ensure_schema=False)
classes = ['DaoCall', 'IbatisStatement', 'BackendDoc', 'JspForm', 
           'DbTable', 'GwtModule', 'GwtUiBinder', 'GwtActivityPlace',
           'GwtEndpoint', 'JsArtifact']
for class_name in classes:
    try:
        wc._client.batch.delete_objects(
            class_name=class_name,
            where={"operator": "Like", "path": ["project"], "valueText": "*"}
        )
    except:
        pass
EOF
```

### Step 2: Fix Project Names

```bash
source venv/bin/activate
python fix_project_names.py
```

**Expected:** Shows summary of project name fixes

### Step 3: Re-index All Artifacts

```bash
python main.py index --all-projects
```

**Expected output:**
```
Loading 13359 DAO call files from java_calls directory...
Loaded 13359 DAO call artifacts
Found X projects in artifacts: ...
Indexing dao_calls...
Indexing ibatis_statements...
...
Indexed X artifacts in Weaviate
```

**Time:** 5-15 minutes

**What's new:**
- Metadata (`meta` field) is now stored for all artifacts
- All metadata fields are preserved as JSON

### Step 4: Verify Indexing

```bash
./weaviate_stats.sh
```

**Expected:**
- Total Objects: 13,000+
- All classes have data
- Projects are correctly named

### Step 5: Test Search with Metadata

```bash
# Test search
python main.py search --query "dao" --project "cuco-core"

# Test search across all projects
python main.py search --query "dao" --all
```

**Expected:** Results should include metadata information

### Step 6: Generate Requirements with Enhanced CrewAI

```bash
# Generate for all projects
nohup python main.py requirements --all-projects --use-crewai > "logprod_crewai_$(date +'%Y-%m-%d_%H-%M-%S').log" 2>&1 &
```

**What's improved:**
- More detailed analysis per area
- Better organized requirements
- Includes metadata in analysis
- More comprehensive documentation

**Time:** 1-3 hours for all projects

### Step 7: Monitor and Verify

```bash
# Monitor requirements generation
tail -f logprod_crewai_*.log

# Check generated requirements
ls -la output/*_crewai_requirements.md

# Review a sample requirement document
cat output/cuco-core_crewai_requirements.md | head -100
```

## Expected Improvements in Requirements

### Before:
- Generic requirements
- Limited detail
- No area-specific organization
- Missing metadata context

### After:
- **Detailed requirements** organized by functional areas
- **Specific examples** with file paths, class names, SQL IDs
- **Comprehensive coverage** of all aspects (backend, frontend, database, etc.)
- **Metadata context** included in analysis
- **Traceability** links to source artifacts
- **Professional structure** suitable for development teams

## Verification Checklist

After completing all steps:

- [ ] Weaviate statistics show 13,000+ objects
- [ ] Metadata is stored (check with `weaviate_stats.sh`)
- [ ] Searches return results with metadata
- [ ] Project names are correct (not "mnt")
- [ ] Requirements documents are more detailed
- [ ] Requirements are organized by functional areas
- [ ] Requirements include specific file/class references
- [ ] Requirements include traceability information

## Troubleshooting

### If Metadata Not Stored

1. **Check schema:**
   ```bash
   python3 << 'EOF'
   from store.weaviate_client import WeaviateClient
   wc = WeaviateClient(ensure_schema=False)
   # Check if meta field exists in schema
   EOF
   ```

2. **Re-run indexing** after ensuring schema has `meta` field

### If Requirements Still Generic

1. **Check CrewAI version:**
   ```bash
   pip show crewai
   ```

2. **Check logs** for errors during generation

3. **Verify search tool is finding results** - if no results, requirements will be generic

## Files Modified

1. `src/store/weaviate_client.py` - Added metadata storage
2. `src/synth/crewai_requirements.py` - Enhanced prompts and metadata handling
3. `src/cli.py` - Added --all flag to search
4. `reload_all_data.sh` - New script for complete reload

## Next Steps After Reload

1. Review generated requirements documents
2. Verify they contain detailed, area-specific information
3. Check traceability links work
4. Use requirements for development planning

