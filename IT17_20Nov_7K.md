Reviewing the current setup to identify where to add HTML/HTM and GWT support in the Weaviate loader and to add a CrewAI agent for frontend analysis.


## Summary

Improved the Weaviate loading process to include HTML/HTM files with GWT feature detection, and added a frontend-focused CrewAI agent.

### 1. HTML/HTM file discovery
- Updated `FileDiscovery` to discover HTML/HTM files
- Added `_discover_html_files()` method

### 2. HTML extractor with GWT detection
- Created `HtmlExtractor` (`src/extract/html_static.py`)
- Features:
  - Parses HTML/HTM files
  - Detects GWT features (nocache scripts, module references, patterns)
  - Extracts forms, scripts, links, and meta tags
  - Identifies GWT module references and traces them

### 3. Weaviate schema updates
- Added `HtmlArtifact` class to Weaviate schema
- Properties: `project`, `path`, `text`, `title`, `isGwt`, `meta`
- Updated indexing and search to handle HTML artifacts

### 4. CLI integration
- Updated `extract` command to include HTML extraction
- Updated `index` command to load and index HTML artifacts
- Updated `search` command to include HTML artifacts in frontend searches
- HTML artifacts saved to `html_artifacts/all_html_artifacts.json`

### 5. Frontend-focused CrewAI agent
- Created `create_frontend_trace_agent()` that:
  - Traces all frontend files (HTML, JSP, GWT, JS)
  - Follows references (scripts, forms, links, GWT modules)
  - Maps relationships between frontend files
  - Ensures no frontend logic is missed
- Added as `task3_trace` in the CrewAI workflow, running before UI analysis

### 6. CrewAI requirements updates
- Updated `WeaviateSearchTool` to include `HtmlArtifact` in searchable types
- Updated `SourceFileReaderTool` to handle HTML file reading
- Enhanced `create_ui_flow_analyst_agent()` to work with HTML files
- Frontend trace agent integrated into the sequential workflow

### 7. Script updates
- Updated `reload_all_data.sh` to include `HtmlArtifact` in the classes list

### Workflow
1. HTML files are discovered during file discovery
2. HTML files are extracted with GWT feature detection
3. HTML artifacts are indexed in Weaviate
4. Frontend Trace Agent traces all frontend files and their relationships
5. UI Analyst Agent uses trace results for comprehensive frontend analysis
6. Requirements document includes all discovered frontend logic

The system now captures frontend files, especially GWT features, and the Frontend Trace Agent ensures all frontend logic is discovered and documented.