# Plan to Fix PRD Generation for GWT Applications

## Problem Analysis

### Root Cause
The PRD generation system is designed for **traditional Java EE** applications with:
- DAO/Entity patterns (`*DAO.java`, `*Entity.java`)
- REST/SOAP services (`*Service.java`, `*Controller.java`)
- JSP/HTML forms

But **cuco-ui-admin** is a **GWT (Google Web Toolkit)** application with:
- GWT RPC servlets (`*ServletImpl.java`)
- GWT presenters/views (MVP pattern)
- UiBinder XML files (`*.ui.xml`)
- No traditional DAO layer

### Current Issues

1. **Database Analyzer (`db_analyzer.py`)**
   - Searches for: `*DAO.java`, `*Entity.java`, `*Mapper.xml`
   - ❌ **Found**: 0 files (GWT doesn't use these patterns)

2. **Service Analyzer (`service_analyzer.py`)**
   - Searches for: `*Service.java`, `*Controller.java`, REST endpoints
   - ❌ **Found**: 0 files (GWT uses RPC servlets instead)

3. **Frontend Analyzer (`frontend_analyzer.py`)**
   - Searches for: Form fields in JSP/HTML
   - ❌ **Found**: 0 forms (GWT uses UiBinder XML + Java code)
   - Analyzed 63 files but found "No form" in each

### What We Actually Have (184 indexed files)

From the extraction logs, the codebase contains:
- **136 Java source files**: GWT servlets, presenters, views, models
- **34 XML config files**: UiBinder templates, Spring config
- **9 Java test files**: JUnit tests
- **4 other text files**: Config files
- **1 GWT module**: GWT module descriptor

## Solution Architecture

### Phase 1: Understand GWT Architecture (Current Task)

**Objective**: Analyze how cuco-ui-admin works to design appropriate extractors

1. **Map GWT Patterns**
   - ✅ Identify GWT RPC servlets (server-side)
   - ✅ Identify presenters (MVP pattern)
   - ✅ Identify views (UI components)
   - ✅ Identify UiBinder templates

2. **Analyze Existing Extractions**
   - ✅ Review what semantic data was extracted
   - ✅ Check if framework detection caught "GWT"
   - ✅ Verify Weaviate has the data

3. **Study GWT Application Structure**
   ```
   cuco-ui-admin/
   ├── client/                    # Frontend (compiled to JS)
   │   ├── servlet/              # RPC interfaces
   │   ├── ui/
   │   │   ├── popup/           # Dialogs/popups
   │   │   └── portlet/         # Main UI components
   │   ├── presenter/           # MVP presenters
   │   └── view/                # MVP views
   ├── server/                   # Backend
   │   └── servlet/             # RPC implementations
   └── shared/                   # Shared models (client + server)
   ```

### Phase 2: Enhance Semantic Extraction

**Objective**: Extract GWT-specific patterns during semantic extraction

1. **Update Ollama Prompts**
   - Detect GWT RPC methods
   - Extract presenter-view relationships
   - Identify UiBinder form fields
   - Extract data transfer objects (DTOs)

2. **Improve Framework Detection**
   - Better detection of GWT patterns
   - Identify MVP components
   - Tag files by GWT role (servlet/presenter/view)

3. **Add GWT Metadata to Artifacts**
   ```json
   {
     "gwt_role": "rpc_servlet" | "presenter" | "view" | "shared_model",
     "rpc_methods": [...],
     "ui_components": [...],
     "form_fields": [...],
     "presenter_view_binding": "..."
   }
   ```

### Phase 3: Create GWT Analyzers

**Objective**: Build new analyzers specifically for GWT applications

1. **GWT RPC Analyzer** (`gwt_rpc_analyzer.py`)
   - Find: `*Servlet.java`, `*ServletImpl.java`, `*ServletAsync.java`
   - Extract: RPC methods, DTOs, exception handling
   - Output: Service-like PRD for RPC endpoints

2. **GWT Presenter Analyzer** (`gwt_presenter_analyzer.py`)
   - Find: `*Presenter.java`
   - Extract: Business logic, view interactions, navigation
   - Output: Business logic PRD

3. **GWT View Analyzer** (`gwt_view_analyzer.py`)
   - Find: `*View.java`, `*.ui.xml`
   - Extract: UI components, form fields, layouts
   - Output: Frontend PRD with actual components

4. **GWT Model Analyzer** (`gwt_model_analyzer.py`)
   - Find: DTOs in `shared/` directory
   - Extract: Data structures, validation rules
   - Output: Data model PRD

### Phase 4: Update Existing Analyzers

**Objective**: Make existing analyzers GWT-aware

1. **Database Analyzer**
   - Add GWT DTO detection
   - Look for shared models instead of entities
   - Extract data structures from RPC methods

2. **Service Analyzer**
   - Recognize GWT RPC servlets as services
   - Parse `*ServletImpl.java` files
   - Extract RPC method signatures

3. **Frontend Analyzer**
   - Parse UiBinder XML (`*.ui.xml`)
   - Extract form fields from `<g:...>` widgets
   - Link views to presenters

### Phase 5: Enhance PRD Templates

**Objective**: Generate GWT-appropriate PRDs

1. **RPC Endpoints Section**
   ```markdown
   ## RPC Endpoints

   ### FlashInfoServlet
   - Method: `createFlashInfo(FlashInfoDTO dto)`
   - Input: FlashInfoDTO
   - Output: FlashInfoDTO
   - Description: Creates new flash info message
   ```

2. **MVP Components Section**
   ```markdown
   ## MVP Components

   ### FlashAdministrationPresenter
   - View: FlashAdministrationView
   - Purpose: Manage flash info messages
   - Events: onEdit, onDelete, onSave
   - Navigation: AdminMainPresenter
   ```

3. **UI Components Section**
   ```markdown
   ## UI Components

   ### FlashInfoEditView
   - Type: Popup Dialog
   - Fields:
     - title: TextBox (required)
     - message: TextArea (required)
     - active: CheckBox
   - Actions: Save, Cancel
   ```

### Phase 6: Leverage Indexed Data

**Objective**: Use the data already in Weaviate

1. **Query Weaviate for GWT Patterns**
   - Search for framework tag "GWT"
   - Filter by file paths (client/, server/, shared/)
   - Use semantic search for "RPC", "presenter", "view"

2. **Extract from Semantic Data**
   - The 184 files are already indexed with semantic analysis
   - Check what's in the `semantic_data` field
   - Use LLM-extracted information

3. **Fall Back to Structural Data**
   - If semantic data is insufficient
   - Parse Java AST for method signatures
   - Parse XML for UI components

## Implementation Priority

### Quick Wins (Immediate)

1. ✅ **Fix Errors**
   - ✅ Add .pspimage to static assets filter
   - ✅ Handle HTML entities in XML parser

2. **Query Existing Indexed Data**
   - Write test queries to Weaviate
   - See what semantic data was extracted
   - Determine if we can use it as-is

3. **Basic GWT RPC Analyzer**
   - Find *ServletImpl.java files
   - Extract RPC methods using regex
   - Generate basic service PRD

### Medium Priority (Next)

4. **GWT View Analyzer**
   - Parse *.ui.xml files
   - Extract form widgets
   - Generate frontend PRD

5. **Update PRD Templates**
   - Add GWT-specific sections
   - Format for RPC instead of REST

### Long Term (Future)

6. **Full GWT Support**
   - Complete all 4 GWT analyzers
   - Update semantic extraction prompts
   - Add GWT patterns to documentation

## Testing Strategy

### Test Cases

1. **Test Weaviate Queries**
   ```python
   # Query for GWT servlets
   results = search_artifacts(
       project="cuco-ui-admin",
       query="GWT RPC servlet",
       limit=10
   )
   ```

2. **Test File Pattern Detection**
   ```python
   # Find GWT files
   servlets = find_gwt_servlets(source_dir)
   presenters = find_gwt_presenters(source_dir)
   views = find_gwt_views(source_dir)
   ```

3. **Test PRD Generation**
   ```bash
   # Generate RPC endpoint PRD
   codeindex prd gwt-rpc \
       --project cuco-ui-admin \
       --output-dir ./output/test
   ```

### Success Criteria

- ✅ PRD shows > 0 RPC endpoints
- ✅ PRD shows > 0 presenters
- ✅ PRD shows > 0 UI components
- ✅ PRD content is accurate and useful

## Next Steps

1. **Immediate**:
   - Query Weaviate to see what data we have
   - Check semantic extraction results
   - Design GWT RPC analyzer

2. **This Week**:
   - Implement basic GWT RPC analyzer
   - Generate first useful PRD
   - Test on cuco-ui-admin

3. **Next Sprint**:
   - Complete all GWT analyzers
   - Update semantic extraction
   - Document GWT support

## Resources Needed

- [ ] GWT documentation review
- [ ] Sample GWT application analysis
- [ ] Ollama prompt engineering for GWT
- [ ] Weaviate query testing

## Open Questions

1. **Should we support both Java EE and GWT?**
   - Yes - detect application type and use appropriate analyzers

2. **Can we auto-detect GWT vs Java EE?**
   - Yes - look for GWT module descriptor, GWT imports, file structure

3. **Should we update semantic extraction or work with existing data?**
   - Start with existing data, enhance extraction in Phase 2

4. **Priority: Complete GWT support or improve Java EE support?**
   - Start with GWT basics, maintain Java EE compatibility
