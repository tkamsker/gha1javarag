# Quick Start: GWT Application PRD Generation

**Feature**: 001-gwt-prd-support
**Audience**: Developers analyzing GWT codebases
**Time to Complete**: 10-15 minutes

## Prerequisites

Before generating PRDs for GWT applications, ensure you have:

1. **Python Environment**
   ```bash
   python --version  # 3.8 or higher required
   source .venv/bin/activate
   ```

2. **Dependencies Installed**
   ```bash
   pip install -r requirements.txt
   pip install javalang  # GWT-specific dependency
   ```

3. **Services Running**
   ```bash
   # Start Ollama (required for semantic extraction)
   ollama serve
   ollama pull gemma3:12b

   # Start Weaviate (required for indexing)
   ./docker-weaviate.sh start
   ```

4. **GWT Codebase Available**
   - Source code directory with GWT application
   - Example: `~/projects/cuco-ui-admin`

---

## Quick Start (5 Steps)

### Step 1: Set Source Directory

```bash
export JAVA_SOURCE_DIR=/path/to/your/gwt/project
# Example: export JAVA_SOURCE_DIR=~/projects/cuco-ui-admin
```

Or create a `.env` file:
```bash
echo "JAVA_SOURCE_DIR=/path/to/your/gwt/project" > .env
```

### Step 2: Run Full Pipeline

Use the convenience script to run all stages:

```bash
./run.sh
```

This executes:
1. **discover** - Scans for `.java`, `.ui.xml`, `.gwt.xml` files
2. **extract** - Parses GWT patterns (RPC servlets, presenters, views)
3. **index** - Stores artifacts in Weaviate
4. **status** - Shows indexing statistics

Expected output:
```
✓ Discovery: Found 184 files (355 static assets skipped)
✓ Extraction: Processed 184 artifacts
  - 15 RPC servlets detected
  - 23 presenters detected
  - 23 views detected
  - 18 UiBinder templates parsed
  - 12 DTOs extracted
✓ Indexing: 184 artifacts indexed successfully
✓ Status: Project 'cuco-ui-admin' ready for PRD generation
```

### Step 3: Generate PRDs

Generate complete Product Requirements Document:

```bash
codeindex prd \
  --project cuco-ui-admin \
  --output-dir ./output/prds
```

Or generate specific sections:

```bash
# Backend PRD (RPC servlets, DTOs)
codeindex prd backend \
  --project cuco-ui-admin \
  --output-dir ./output/prds

# Frontend PRD (presenters, views, UI components)
codeindex prd frontend \
  --project cuco-ui-admin \
  --output-dir ./output/prds
```

### Step 4: Review Generated PRDs

PRDs are created in `./output/prds/`:

```bash
ls -lh ./output/prds/
# cuco-ui-admin-backend-prd.md
# cuco-ui-admin-frontend-prd.md
# cuco-ui-admin-full-prd.md
```

Open in your editor:
```bash
cat ./output/prds/cuco-ui-admin-full-prd.md
```

### Step 5: Validate Results

Check that PRDs contain expected content:

```bash
# Should show RPC endpoints
grep -A 5 "## RPC Endpoints" ./output/prds/cuco-ui-admin-backend-prd.md

# Should show UI components
grep -A 5 "## UI Components" ./output/prds/cuco-ui-admin-frontend-prd.md

# Should show MVP components
grep -A 5 "## MVP Components" ./output/prds/cuco-ui-admin-frontend-prd.md
```

---

## Expected PRD Structure

### Backend PRD Sections

```markdown
# Backend PRD: cuco-ui-admin

## 1. Objectives and Stakeholders
[Generated from project metadata]

## 2. RPC Endpoints

### FlashInfoServlet
**Service Interface**: `FlashInfoService`
**URL Mapping**: `/flashinfo`

#### Methods:
- **createFlashInfo(FlashInfoDTO dto)**
  - Input: FlashInfoDTO
  - Output: FlashInfoDTO
  - Description: Creates new flash info message
  - Exceptions: RemoteException

- **updateFlashInfo(FlashInfoDTO dto)**
  - Input: FlashInfoDTO
  - Output: FlashInfoDTO
  - Description: Updates existing flash info message
  - Exceptions: RemoteException

## 3. Data Transfer Objects

### FlashInfoDTO
**Package**: `com.example.shared.dto`
**Serializable**: Yes

#### Fields:
- `id: Long` - Unique identifier
- `title: String` - Flash message title (required, max 100 chars)
- `message: String` - Flash message content (required)
- `active: Boolean` - Whether message is active

#### Validation Rules:
- title: @NotNull, @Size(max=100)
- message: @NotNull
```

### Frontend PRD Sections

```markdown
# Frontend PRD: cuco-ui-admin

## 1. Objectives and Stakeholders
[Generated from project metadata]

## 2. MVP Components

### FlashAdministrationPresenter
**View**: FlashAdministrationView (90% confidence)
**Purpose**: Manage flash info messages

#### Event Handlers:
- `onEditButtonClick()` - Opens edit dialog for flash info
- `onDeleteButtonClick()` - Deletes selected flash info
- `onSaveButtonClick()` - Saves flash info changes

#### Navigation:
- `goToAdminMain()` → AdminMainPresenter
- `goToFlashList()` → FlashListPresenter

#### RPC Calls:
- FlashInfoService.createFlashInfo()
- FlashInfoService.updateFlashInfo()
- FlashInfoService.deleteFlashInfo()

## 3. UI Components

### FlashInfoEditView
**Type**: Popup Dialog
**UiBinder Template**: FlashInfoEditView.ui.xml

#### Form Fields:
- **titleField** (TextBox)
  - Label: "Title"
  - Required: Yes
  - Max Length: 100

- **messageField** (TextArea)
  - Label: "Message"
  - Required: Yes
  - Rows: 5

- **activeCheckbox** (CheckBox)
  - Label: "Active"
  - Default: true

#### Actions:
- **Save Button** - Submits form to presenter
- **Cancel Button** - Closes dialog without saving
```

---

## Troubleshooting

### Issue: Empty PRDs (0 endpoints, 0 components)

**Symptom**: Generated PRDs show no content

**Solution**:
```bash
# 1. Check if GWT was detected
codeindex status --project cuco-ui-admin | grep GWT

# 2. Verify extraction found GWT patterns
cat ./output/extraction-results.jsonl | grep gwt_role

# 3. Re-run with debug logging
export LOG_LEVEL=DEBUG
./run.sh
```

### Issue: XML Parsing Errors

**Symptom**: `XMLSyntaxError: Entity 'nbsp' not defined`

**Solution**: Ensure xml_parser.py has recover mode enabled (already fixed in this implementation)

```python
# Check xml_parser.py line 30-38
self.parser = etree.XMLParser(
    recover=True,  # Should be True
    resolve_entities=False
)
```

### Issue: UnicodeDecodeError on Binary Files

**Symptom**: `UnicodeDecodeError: 'utf-8' codec can't decode byte`

**Solution**: Verify binary files are classified as STATIC_ASSET

```bash
# Check classifier is detecting binary files
python -c "
from pathlib import Path
from codeindex.services.classifier import classify_file
result = classify_file(Path('./path/to/image.gif'))
print(result)  # Should be ArtifactType.STATIC_ASSET
"
```

### Issue: Low Presenter-View Binding Confidence

**Symptom**: PRDs show "Unknown view" for presenters

**Solution**: Check presenter detection strategies

```bash
# Search for Display interface pattern (90% confidence)
grep -r "interface Display" $JAVA_SOURCE_DIR

# Search for view field declarations (85% confidence)
grep -r "private.*View " $JAVA_SOURCE_DIR

# Naming convention fallback (70% confidence) - always works
# UserPresenter → UserView (automatic)
```

### Issue: Missing RPC Methods

**Symptom**: RPC servlets detected but methods not extracted

**Solution**:
```bash
# 1. Check if javalang is installed
pip show javalang

# 2. If javalang fails, regex fallback should work
# Check extraction logs for fallback messages
cat ./output/extraction.log | grep "Fallback to regex"

# 3. Verify Java syntax is valid
javac -Xlint $JAVA_SOURCE_DIR/path/to/Servlet.java
```

---

## Advanced Usage

### Custom Project Name

By default, project name is derived from directory. Override with:

```bash
codeindex discover \
  --source-dir /path/to/gwt/project \
  --project my-custom-name \
  --output ./output/discovery-inventory.jsonl
```

### Filter by GWT Role

Query specific GWT artifact types:

```bash
# Search for RPC servlets only
codeindex search "authentication" \
  --project cuco-ui-admin \
  --filter gwt_role:rpc_servlet

# Search for presenters only
codeindex search "user management" \
  --project cuco-ui-admin \
  --filter gwt_role:presenter
```

### Export to Spec Kit

Use generated PRDs with GitHub Spec Kit:

```bash
# 1. Copy PRD to specs directory
mkdir -p specs/002-gwt-analysis
cp ./output/prds/cuco-ui-admin-full-prd.md \
   specs/002-gwt-analysis/prd.md

# 2. Run Spec Kit workflow
/speckit.specify
/speckit.plan
/speckit.tasks
```

### Performance Tuning

For large GWT codebases (1000+ files):

```bash
# Increase concurrent AI calls
export MAX_CONCURRENT_AI_CALLS=20

# Increase batch size
export BATCH_SIZE=100

# Run with progress output
codeindex extract \
  --inventory ./output/discovery-inventory.jsonl \
  --output ./output/extraction-results.jsonl \
  --show-progress
```

---

## Configuration Reference

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `JAVA_SOURCE_DIR` | (required) | Root directory of GWT source |
| `OLLAMA_URL` | http://localhost:11434 | Ollama service endpoint |
| `OLLAMA_MODEL_NAME` | gemma3:12b | LLM model for extraction |
| `WEAVIATE_URL` | http://localhost:8080 | Weaviate database endpoint |
| `MAX_CONCURRENT_AI_CALLS` | 10 | Parallel semantic extractions |
| `BATCH_SIZE` | 50 | Weaviate batch size |
| `LOG_LEVEL` | INFO | DEBUG/INFO/WARNING/ERROR |
| `OUTPUT_DIR` | ./output | Directory for intermediate files |

### File Patterns Detected

| Pattern | GWT Role | Description |
|---------|----------|-------------|
| `*Servlet.java` | rpc_servlet | RPC endpoint implementation |
| `*ServletImpl.java` | rpc_servlet | RPC endpoint implementation |
| `*Presenter.java` | presenter | MVP presenter component |
| `*View.java` | view | MVP view component |
| `*.ui.xml` | ui_binder | UiBinder template |
| `*DTO.java` | shared_dto | Data Transfer Object |
| `*.gwt.xml` | gwt_module | GWT module descriptor |

---

## Next Steps

After generating PRDs, consider:

1. **Review for Accuracy**: Manually verify RPC methods, form fields, and MVP bindings
2. **Add Domain Labels**: Tag artifacts with business domains (authentication, user-management, etc.)
3. **Generate Requirements**: Use `/speckit.specify` to transform PRDs into feature specifications
4. **Plan Implementation**: Use `/speckit.plan` and `/speckit.tasks` for implementation planning
5. **Re-index Incrementally**: After code changes, re-run extraction and indexing

---

## Support

- **Documentation**: See `CLAUDE.md` for full CLI reference
- **Issues**: Report bugs at https://github.com/anthropics/claude-code/issues
- **Examples**: Sample GWT files in `tests/fixtures/gwt/`

---

**Estimated Total Time**: 8-10 minutes for 200-file GWT codebase
