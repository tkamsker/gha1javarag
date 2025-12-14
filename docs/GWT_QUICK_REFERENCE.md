# GWT Support - Quick Reference Guide

**Quick reference for analyzing Google Web Toolkit (GWT) applications**

## At a Glance

| Feature | Status | Details |
|---------|--------|---------|
| **Presenter Analysis** | ✅ Full Support | MVP pattern, view binding, event handlers, navigation |
| **View Analysis** | ✅ Full Support | Component types, UI fields, UiBinder integration |
| **DTO Analysis** | ✅ Full Support | Fields, validation, serialization, nested DTOs |
| **RPC Servlet Analysis** | ✅ Full Support | Service methods, async interfaces, inheritance |
| **UiBinder Templates** | ✅ Full Support | Form fields, widgets, labels, structure |
| **GWT Module Detection** | ✅ Full Support | Entry points, source paths, dependencies |

## Quick Commands

### 1. Discover GWT App
```bash
codeindex discover --source-dir /path/to/gwt-app --project myapp
# Output: discovery-inventory.jsonl with GWT artifacts classified
```

### 2. Extract Metadata
```bash
# With AI (slower, more semantic info)
codeindex extract --inventory discovery-inventory.jsonl --output extraction-results.jsonl

# Without AI (faster, structural only)
codeindex extract --skip-ai --inventory discovery-inventory.jsonl
```

### 3. Index & Search
```bash
# Index
codeindex index --inventory discovery-inventory.jsonl --extraction extraction-results.jsonl

# Search
codeindex search "user authentication presenter" --project myapp
```

## File Pattern Recognition

| File Pattern | Classified As | Analyzer Used |
|--------------|---------------|---------------|
| `*Presenter.java` | `java_source` | GwtPresenterAnalyzer |
| `*View.java` | `java_source` | GwtViewAnalyzer |
| `*DTO.java` | `java_source` | GwtModelAnalyzer |
| `*ServletImpl.java` | `java_source` | GwtRpcAnalyzer |
| `*.ui.xml` | `gwt_ui_binder` | GwtUiBinderParser |
| `*.gwt.xml` | `gwt_module` | XML Parser |

**Note**: Java files are classified as `java_source`, then GWT analyzers detect specific roles based on content.

## GWT Metadata Fields

### Presenter Metadata
```json
{
  "gwt_role": "presenter",
  "view_binding": {
    "view_interface": "MyView.Display",
    "binding_type": "display_interface",
    "confidence": 90
  },
  "event_handlers": [
    {
      "widget_getter": "getSaveButton",
      "event_type": "ClickEvent",
      "handler_method": "onSave"
    }
  ],
  "navigation_logic": ["EditPlace", "ListPlace"],
  "rpc_calls": ["userService.save", "userService.load"]
}
```

### View Metadata
```json
{
  "gwt_role": "view",
  "component_type": "Composite",
  "ui_fields": [
    {
      "name": "nameTextBox",
      "widget_type": "TextBox"
    }
  ],
  "uibinder_template": {
    "template_file": "MyView.ui.xml"
  }
}
```

### DTO Metadata
```json
{
  "gwt_role": "shared_dto",
  "fields": [
    {
      "name": "username",
      "type": "String",
      "validation_rules": [
        {"type": "NotNull"},
        {"type": "Size", "min": 3, "max": 50}
      ]
    }
  ],
  "gwt_serializable": true,
  "java_serializable": true,
  "nested_dtos": ["AddressDTO", "ProfileDTO"]
}
```

### UiBinder Metadata
```json
{
  "gwt_role": "ui_binder",
  "template_name": "LoginView",
  "form_fields": [
    {
      "field_name": "usernameTextBox",
      "widget_type": "TextBox",
      "label": "Username"
    }
  ],
  "field_count": 5
}
```

### RPC Servlet Metadata
```json
{
  "gwt_role": "rpc_servlet",
  "service_interface": "UserService",
  "async_interface": "UserServiceAsync",
  "rpc_methods": [
    {
      "name": "getUser",
      "return_type": "UserDTO",
      "parameters": [{"name": "userId", "type": "Long"}]
    }
  ]
}
```

## MVP Pattern Detection

| Pattern | Confidence | Detection Method |
|---------|------------|------------------|
| **Inner Display Interface** | 90% | `interface Display extends ...` inside presenter |
| **Separate View Interface** | 85% | Presenter references external view interface |
| **Naming Convention** | 70% | `FooPresenter` + `FooView` file pairing |

**Example: Display Interface (90% confidence)**
```java
public class UserPresenter {
    public interface Display {
        HasClickHandlers getSaveButton();
        HasValue<String> getUsername();
    }
}
```

**Example: Separate Interface (85% confidence)**
```java
public class UserPresenter {
    private UserView view;  // Reference to view interface
}

// Separate file
public interface UserView {
    HasClickHandlers getSaveButton();
}
```

**Example: Naming Convention (70% confidence)**
```
UserPresenter.java  ← Presenter file
UserView.java       ← View file (matched by naming)
```

## DTO Recognition Rules

DTOs are recognized if they match **either** condition:

### Option 1: Package Structure
```
src/main/java/com/example/shared/UserDTO.java
                            ^^^^^^
                            Must contain ".shared."
```

### Option 2: Serialization Markers
```java
// GWT serialization
public class UserDTO implements IsSerializable { }

// Java serialization
public class UserDTO implements Serializable { }

// Serial version UID
private static final long serialVersionUID = 1L;
```

**Note**: If DTO is not in `.shared.` package, it MUST have serialization markers in the file content.

## UiBinder Template Analysis

### Field Label Detection

UiBinder parser uses multiple heuristics to find labels:

1. **Inline Text** (CheckBox, Button): `<g:CheckBox ui:field="rememberMe">Remember Me</g:CheckBox>`
2. **Label Widget**: `<g:Label ui:field="usernameLabel">Username:</g:Label>`
3. **Naming Convention**: `usernameTextBox` → looks for `usernameLabel`
4. **Same Table Row**: Finds Label in same `<tr>` as widget
5. **Plain Text**: Extracts text from `<td>` cells near widget

### Widget Types Detected

- **Input**: TextBox, TextArea, PasswordTextBox, IntegerBox, DoubleBox
- **Selection**: ListBox, CheckBox, RadioButton
- **Date**: DateBox, DatePicker
- **Action**: Button, SubmitButton, ResetButton
- **Display**: Label, HTML, HTMLPanel

## Common Workflows

### Analyze Single GWT File

```bash
# Extract just one file
codeindex extract --file path/to/MyPresenter.java --type JAVA_SOURCE

# Check what was extracted
jq '.gwt_role' path/to/result.json
```

### Monitor Extraction Progress

```bash
# Watch log in real-time
tail -f extraction.log | grep -E "Extracting|ERROR|Progress"

# Count GWT artifacts processed
grep '"gwt_role"' extraction-results.jsonl | wc -l

# See GWT role breakdown
grep '"gwt_role"' extraction-results.jsonl | \
  grep -o '"gwt_role":"[^"]*"' | sort | uniq -c
```

### Validate GWT Detection

```bash
# Count expected GWT files
find /path/to/source -name "*Presenter.java" | wc -l
find /path/to/source -name "*View.java" | wc -l
find /path/to/source -name "*DTO.java" | wc -l
find /path/to/source -name "*.ui.xml" | wc -l

# Compare with discovery results
grep -c '"artifact_type":"gwt_ui_binder"' discovery-inventory.jsonl
grep -c '"gwt_role":"presenter"' extraction-results.jsonl
```

## Troubleshooting Decision Tree

### Problem: Files Not Discovered

```
└─ Check file extensions
   ├─ *.java files → Should be discovered
   ├─ *.ui.xml files → Should be discovered
   └─ *.gwt.xml files → Should be discovered

└─ Check discovery log
   └─ grep "Discovered project" discovery.log

└─ Verify source directory
   └─ ls -la /path/to/source/src/main/java
```

### Problem: GWT Role Not Detected

```
└─ Check file naming
   ├─ Does it end with Presenter.java? → Should get presenter role
   ├─ Does it end with View.java? → Should get view role
   └─ Does it end with DTO.java? → Check next step

└─ For DTOs, check package OR content
   ├─ Package contains ".shared."? → Should work
   └─ Contains IsSerializable/Serializable? → Should work

└─ Check extraction log
   └─ grep "gwt_role" extraction-results.jsonl | grep filename
```

### Problem: UiBinder Extraction Failed

```
└─ Verify XML structure
   ├─ Run: xmllint --noout file.ui.xml
   └─ Check: grep "ui:UiBinder" file.ui.xml

└─ Check GWT namespace
   └─ Should have: xmlns:ui="urn:ui:com.google.gwt.uibinder"

└─ Check extraction log
   └─ grep "ERROR.*ui.xml" extraction.log
```

### Problem: MVP Binding Not Detected

```
└─ Check presenter code
   ├─ Has inner Display interface? → 90% confidence
   ├─ References external view interface? → 85% confidence
   └─ Matches naming with *View.java? → 70% confidence

└─ View binding metadata
   └─ grep "view_binding" extraction-results.jsonl | jq .
```

## Testing GWT Support

```bash
# Run all GWT tests
pytest tests/ -k gwt -v

# Specific test suites
pytest tests/integration/test_gwt_prd_generation.py -v
pytest tests/integration/test_gwt_weaviate_simple.py -v
pytest tests/unit/test_classifier.py::TestGwtClassification -v

# Test individual analyzers
pytest tests/unit/test_gwt_presenter_analyzer.py -v
pytest tests/unit/test_gwt_model_analyzer.py -v
pytest tests/unit/test_uibinder_parser.py -v
```

## Performance Tips

### Speed Up Extraction

```bash
# Skip AI for faster extraction (structural analysis only)
codeindex extract --skip-ai --inventory discovery-inventory.jsonl

# Reduce parallelism if hitting rate limits
codeindex extract --parallel 5 --inventory discovery-inventory.jsonl

# Process specific files only
grep "Presenter.java" discovery-inventory.jsonl > presenters-only.jsonl
codeindex extract --inventory presenters-only.jsonl
```

### Batch Processing

```bash
# Extract in batches
split -l 50 discovery-inventory.jsonl batch-
for batch in batch-*; do
    codeindex extract --inventory $batch --output ${batch}-results.jsonl
done
cat batch-*-results.jsonl > extraction-results.jsonl
```

## Integration Points

### With Weaviate

```bash
# Check indexed GWT artifacts
curl -s http://localhost:8080/v1/objects | \
  jq '.objects[] | select(.properties.gwt_role != null)'

# Count by role
curl -s http://localhost:8080/v1/objects | \
  jq '.objects[].properties.gwt_role' | sort | uniq -c
```

### With PRD Generation

```bash
# Generate PRD focusing on GWT components
codeindex prd frontend --project myapp --output prd.md

# Filter by domain
codeindex prd full --domain-filter authentication --project myapp
```

## Best Practices

✅ **DO**:
- Use standard GWT package structure (`client`, `server`, `shared`)
- Follow naming conventions (`*Presenter`, `*View`, `*DTO`)
- Co-locate UiBinder templates with view classes
- Use consistent MVP patterns (Display interface recommended)
- Add serialization markers to DTOs

❌ **DON'T**:
- Mix different MVP patterns in same codebase
- Put DTOs outside `shared` package without serialization markers
- Use non-standard file naming
- Omit GWT namespaces in UiBinder templates
- Skip testing on representative codebase first

## Support & Resources

- **Full Documentation**: See `README.md` and `CLAUDE.md`
- **Test Examples**: `tests/fixtures/gwt/` directory
- **Validation Report**: `output/gwt-validation/VALIDATION_REPORT.md`
- **Troubleshooting**: See "GWT Troubleshooting" sections in docs
- **Issues**: https://github.com/tkamsker/gha1javarag/issues

---

**Last Updated**: 2025-12-14
**GWT Support Version**: v1.0 (Branch: 001-gwt-prd-support)
**Test Coverage**: 38 integration tests passing
