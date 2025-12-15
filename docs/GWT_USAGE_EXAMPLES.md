# GWT Analysis - Usage Examples

**Real-world examples for analyzing GWT applications with the codeindex tool**

## Table of Contents

- [Basic Workflow](#basic-workflow)
- [Analyzing a Complete GWT Application](#analyzing-a-complete-gwt-application)
- [Extracting Specific GWT Components](#extracting-specific-gwt-components)
- [Searching GWT Artifacts](#searching-gwt-artifacts)
- [PRD Generation for GWT Apps](#prd-generation-for-gwt-apps)
- [Troubleshooting Examples](#troubleshooting-examples)
- [Advanced Use Cases](#advanced-use-cases)

## Basic Workflow

### Example 1: Analyze a Small GWT Module

**Scenario**: You have a small GWT module with 50 files to analyze.

```bash
# Step 1: Set environment variable
export JAVA_SOURCE_DIR=/path/to/my-gwt-module

# Step 2: Start services
ollama serve &  # Start Ollama
./docker-weaviate.sh start  # Start Weaviate

# Step 3: Discover files
codeindex discover \
  --source-dir $JAVA_SOURCE_DIR \
  --project my-gwt-module \
  --output output/discovery.jsonl

# Expected output:
# Projects found: 1
# Total files: 50
# gwt_ui_binder: 10
# java_source: 35
# gwt_module: 1

# Step 4: Extract with AI
codeindex extract \
  --inventory output/discovery.jsonl \
  --output output/extraction.jsonl

# Step 5: Index
codeindex index \
  --inventory output/discovery.jsonl \
  --extraction output/extraction.jsonl

# Step 6: Verify
codeindex status --project my-gwt-module
```

### Example 2: Quick Analysis Without AI

**Scenario**: Fast structural analysis without semantic AI analysis.

```bash
# Discovery
codeindex discover --source-dir /path/to/gwt-app --project fastapp

# Extract without AI (much faster)
codeindex extract --skip-ai \
  --inventory output/discovery.jsonl \
  --output output/extraction-fast.jsonl

# Index
codeindex index \
  --inventory output/discovery.jsonl \
  --extraction output/extraction-fast.jsonl

# This approach:
# - Extracts structural metadata only
# - No AI semantic analysis
# - 10x faster than with AI
# - Good for large codebases or rapid exploration
```

## Analyzing a Complete GWT Application

### Example 3: Multi-Module GWT Application

**Scenario**: A GWT app with separate client, server, and shared modules.

```bash
# Directory structure:
# myapp/
# ├── myapp-client/    (GWT client code)
# ├── myapp-server/    (RPC servlets)
# └── myapp-shared/    (DTOs)

# Step 1: Discover all modules
codeindex discover \
  --source-dir /path/to/myapp \
  --project myapp \
  --output output/myapp-discovery.jsonl

# Step 2: Check what was found
echo "=== Discovery Summary ==="
jq -r '.files_by_type | to_entries[] | "\(.key): \(.value)"' \
  output/myapp-discovery.jsonl

# Expected output:
# java_source: 150
# gwt_ui_binder: 25
# gwt_module: 3
# xml_config: 5

# Step 3: Extract with controlled parallelism
codeindex extract \
  --inventory output/myapp-discovery.jsonl \
  --output output/myapp-extraction.jsonl \
  --parallel 5  # Reduce if hitting Ollama rate limits

# Step 4: Monitor progress
tail -f output/extraction.log | grep -E "Progress:|ERROR"

# Step 5: Index with project context
codeindex index \
  --inventory output/myapp-discovery.jsonl \
  --extraction output/myapp-extraction.jsonl \
  --project myapp

# Step 6: Validate indexing
codeindex status --project myapp

# Expected output:
# Project: myapp
# Artifacts: ~180
# Presenters: ~30
# Views: ~28
# DTOs: ~40
# RPC Servlets: ~15
# UiBinder: ~25
```

## Extracting Specific GWT Components

### Example 4: Analyze Only Presenters

**Scenario**: Focus analysis on presenter layer for architecture review.

```bash
# Step 1: Filter discovery for presenters
grep "Presenter.java" output/discovery.jsonl > output/presenters-only.jsonl

# Step 2: Extract presenter metadata
codeindex extract \
  --inventory output/presenters-only.jsonl \
  --output output/presenter-analysis.jsonl

# Step 3: Analyze results
echo "=== Presenter Analysis ==="

# Count presenters
PRESENTER_COUNT=$(grep -c '"gwt_role":"presenter"' output/presenter-analysis.jsonl)
echo "Total Presenters: $PRESENTER_COUNT"

# Check MVP patterns
echo "\n=== MVP Binding Patterns ==="
jq -r '.view_binding.binding_type' output/presenter-analysis.jsonl | sort | uniq -c

# Expected output:
#   15 display_interface
#    8 separate_interface
#    5 naming_convention

# List navigation targets
echo "\n=== Navigation Targets ==="
jq -r '.navigation_logic[]?' output/presenter-analysis.jsonl | sort | uniq

# List RPC services used
echo "\n=== RPC Services ==="
jq -r '.rpc_calls[]?' output/presenter-analysis.jsonl | sort | uniq
```

### Example 5: Analyze DTOs and Validation Rules

**Scenario**: Document all DTOs and their validation requirements.

```bash
# Step 1: Extract DTOs
grep "DTO.java" output/discovery.jsonl | \
  grep "shared" > output/dtos-only.jsonl

# Step 2: Extract DTO metadata
codeindex extract \
  --inventory output/dtos-only.jsonl \
  --output output/dto-analysis.jsonl

# Step 3: Generate validation report
cat > analyze-dtos.sh << 'SCRIPT'
#!/bin/bash
echo "=== DTO Validation Report ==="
echo ""

# For each DTO
jq -c '. | select(.gwt_role=="shared_dto")' output/dto-analysis.jsonl | while read dto; do
    NAME=$(echo "$dto" | jq -r '.file_name')
    FIELD_COUNT=$(echo "$dto" | jq '.fields | length')

    echo "## $NAME"
    echo "Fields: $FIELD_COUNT"

    # List fields with validation
    echo "$dto" | jq -r '.fields[] |
        select(.validation_rules | length > 0) |
        "\(.name) (\(.type)): \(.validation_rules | map(.type) | join(", "))"'

    echo ""
done
SCRIPT

chmod +x analyze-dtos.sh
./analyze-dtos.sh > output/dto-validation-report.txt
```

### Example 6: Analyze UiBinder Templates

**Scenario**: Document all form fields in UiBinder templates.

```bash
# Step 1: Extract UiBinder files
grep "gwt_ui_binder" output/discovery.jsonl > output/uibinder-only.jsonl

# Step 2: Extract template metadata
codeindex extract \
  --inventory output/uibinder-only.jsonl \
  --output output/uibinder-analysis.jsonl

# Step 3: Generate form field catalog
cat > catalog-forms.sh << 'SCRIPT'
#!/bin/bash
echo "# UiBinder Form Field Catalog"
echo ""

jq -c '. | select(.gwt_role=="ui_binder")' output/uibinder-analysis.jsonl | while read template; do
    NAME=$(echo "$template" | jq -r '.template_name')
    FIELD_COUNT=$(echo "$template" | jq -r '.field_count')

    echo "## $NAME"
    echo "Fields: $FIELD_COUNT"
    echo ""
    echo "| Field | Widget Type | Label |"
    echo "|-------|-------------|-------|"

    echo "$template" | jq -r '.form_fields[] |
        "| \(.field_name) | \(.widget_type) | \(.label) |"'

    echo ""
done
SCRIPT

chmod +x catalog-forms.sh
./catalog-forms.sh > output/form-field-catalog.md
```

## Searching GWT Artifacts

### Example 7: Find Authentication Components

**Scenario**: Locate all authentication-related GWT components.

```bash
# Search for authentication presenters
codeindex search "authentication login" \
  --project myapp \
  --limit 20

# Search for user-related DTOs
codeindex search "user credentials DTO" \
  --project myapp

# Search for login forms
codeindex search "login form uibinder" \
  --project myapp

# Search for authentication RPC services
codeindex search "authenticate user service" \
  --project myapp

# Export results to file
codeindex search "authentication" \
  --project myapp \
  --limit 50 \
  --format json > output/auth-components.json
```

### Example 8: Find Navigation Patterns

**Scenario**: Map application navigation flow.

```bash
# Search for navigation-related code
codeindex search "navigation place activity" \
  --project myapp

# Extract navigation from all presenters
jq -r '.navigation_logic[]?' output/presenter-analysis.jsonl | \
  sort | uniq > output/navigation-targets.txt

# Create navigation graph
cat > generate-nav-graph.sh << 'SCRIPT'
#!/bin/bash
echo "digraph Navigation {"

jq -c '. | select(.gwt_role=="presenter")' output/presenter-analysis.jsonl | while read presenter; do
    SOURCE=$(echo "$presenter" | jq -r '.file_name' | sed 's/Presenter.java//')

    echo "$presenter" | jq -r '.navigation_logic[]?' | while read target; do
        TARGET=$(echo "$target" | sed 's/Place$//' | sed 's/Activity$//')
        echo "  \"$SOURCE\" -> \"$TARGET\";"
    done
done

echo "}"
SCRIPT

chmod +x generate-nav-graph.sh
./generate-nav-graph.sh > output/navigation-graph.dot

# Render with Graphviz (if installed)
dot -Tpng output/navigation-graph.dot -o output/navigation-graph.png
```

## PRD Generation for GWT Apps

### Example 9: Generate GWT-Focused PRD

**Scenario**: Create PRD documentation emphasizing GWT architecture.

```bash
# Generate frontend-focused PRD
codeindex prd frontend \
  --project myapp \
  --output output/myapp-frontend-prd.md

# Expected PRD sections:
# - UI Components (Presenters, Views, UiBinder templates)
# - Form definitions and validation
# - Navigation patterns
# - RPC client-server communication
# - Data transfer objects (DTOs)

# Review the generated PRD
less output/myapp-frontend-prd.md
```

### Example 10: Generate Full PRD with GWT Context

**Scenario**: Complete system documentation including GWT frontend.

```bash
# Generate full PRD
codeindex prd full \
  --project myapp \
  --source-dir /path/to/myapp \
  --output-dir output/prd

# This generates:
# - database_prd.md (backend entities)
# - service_prd.md (RPC servlets, business logic)
# - frontend_prd.md (GWT MVP components)
# - master_prd.md (integrated view)

# Check GWT sections in master PRD
grep -A20 "GWT" output/prd/master_prd.md
```

## Troubleshooting Examples

### Example 11: Debug Missing GWT Roles

**Scenario**: Some GWT files aren't getting gwt_role metadata.

```bash
# Step 1: Check discovery
echo "=== Files Discovered ==="
jq -r '.files_by_type | to_entries[] | "\(.key): \(.value)"' \
  output/discovery.jsonl

# Step 2: Check which files got GWT roles
echo "\n=== GWT Roles Assigned ==="
grep '"gwt_role"' output/extraction.jsonl | \
  grep -o '"gwt_role":"[^"]*"' | sort | uniq -c

# Step 3: Find files without GWT role
echo "\n=== Files Without GWT Role ==="
jq -r 'select(.gwt_role == null) | .file_path' \
  output/extraction.jsonl | grep -E "Presenter|View|DTO|Servlet"

# Step 4: Check specific file
FILE_PATH="path/to/MyPresenter.java"
jq ". | select(.file_path == \"$FILE_PATH\")" output/extraction.jsonl

# Step 5: Manual test
echo "\n=== Manual Analysis ==="
echo "Checking: $FILE_PATH"

# Check naming pattern
basename "$FILE_PATH" | grep -E "Presenter|View|DTO|Servlet"

# Check content for GWT patterns
grep -E "Display|RemoteServiceServlet|IsSerializable" "$FILE_PATH"
```

### Example 12: Fix UiBinder Extraction Issues

**Scenario**: UiBinder templates failing to extract.

```bash
# Step 1: Identify failing templates
grep "ERROR.*ui.xml" extraction.log

# Step 2: Validate XML structure
for uixml in $(find /path/to/source -name "*.ui.xml"); do
    echo "Checking: $uixml"
    xmllint --noout "$uixml" 2>&1
done

# Step 3: Check namespace
for uixml in $(find /path/to/source -name "*.ui.xml"); do
    if ! grep -q "urn:ui:com.google.gwt.uibinder" "$uixml"; then
        echo "Missing GWT namespace: $uixml"
    fi
done

# Step 4: Test extraction on single file
codeindex extract \
  --file path/to/MyView.ui.xml \
  --type GWT_UI_BINDER \
  --output test-extraction.json

# Step 5: Check result
jq '.' test-extraction.json
```

## Advanced Use Cases

### Example 13: Incremental Re-Analysis

**Scenario**: Re-analyze only changed files.

```bash
# Step 1: Get list of changed files (from git)
git diff --name-only HEAD~1 HEAD | \
  grep -E "\.java$|\.ui\.xml$" > changed-files.txt

# Step 2: Filter discovery for changed files
jq -c '.' output/discovery.jsonl | while read item; do
    FILE_PATH=$(echo "$item" | jq -r '.file_path')
    if grep -q "$FILE_PATH" changed-files.txt; then
        echo "$item"
    fi
done > output/changed-discovery.jsonl

# Step 3: Extract only changed files
codeindex extract \
  --inventory output/changed-discovery.jsonl \
  --output output/changed-extraction.jsonl

# Step 4: Re-index (upsert mode)
codeindex index \
  --inventory output/changed-discovery.jsonl \
  --extraction output/changed-extraction.jsonl
```

### Example 14: Compare GWT Patterns Across Versions

**Scenario**: Analyze how MVP patterns evolved between versions.

```bash
# Analyze version 1
git checkout v1.0
codeindex discover --source-dir . --project myapp-v1
codeindex extract --skip-ai --inventory output/discovery.jsonl \
  --output output/v1-extraction.jsonl

# Analyze version 2
git checkout v2.0
codeindex discover --source-dir . --project myapp-v2
codeindex extract --skip-ai --inventory output/discovery.jsonl \
  --output output/v2-extraction.jsonl

# Compare presenter count
V1_COUNT=$(grep -c '"gwt_role":"presenter"' output/v1-extraction.jsonl)
V2_COUNT=$(grep -c '"gwt_role":"presenter"' output/v2-extraction.jsonl)

echo "Presenters: v1=$V1_COUNT, v2=$V2_COUNT, change=$((V2_COUNT - V1_COUNT))"

# Compare MVP patterns
echo "\n=== v1.0 MVP Patterns ==="
jq -r '.view_binding.binding_type' output/v1-extraction.jsonl | sort | uniq -c

echo "\n=== v2.0 MVP Patterns ==="
jq -r '.view_binding.binding_type' output/v2-extraction.jsonl | sort | uniq -c
```

### Example 15: Export GWT Metadata to Database

**Scenario**: Load GWT metadata into PostgreSQL for custom analysis.

```bash
# Create database schema
createdb gwt_analysis

psql gwt_analysis << 'SQL'
CREATE TABLE presenters (
    id SERIAL PRIMARY KEY,
    file_name TEXT,
    view_interface TEXT,
    binding_type TEXT,
    confidence INT,
    event_handler_count INT,
    rpc_call_count INT
);

CREATE TABLE dtos (
    id SERIAL PRIMARY KEY,
    file_name TEXT,
    field_count INT,
    gwt_serializable BOOLEAN,
    java_serializable BOOLEAN,
    validation_rule_count INT
);
SQL

# Extract and insert presenter data
jq -c '. | select(.gwt_role=="presenter")' output/extraction.jsonl | while read presenter; do
    FILE=$(echo "$presenter" | jq -r '.file_name')
    VIEW=$(echo "$presenter" | jq -r '.view_binding.view_interface')
    BINDING=$(echo "$presenter" | jq -r '.view_binding.binding_type')
    CONF=$(echo "$presenter" | jq -r '.view_binding.confidence')
    HANDLERS=$(echo "$presenter" | jq '.event_handlers | length')
    RPCS=$(echo "$presenter" | jq '.rpc_calls | length')

    psql gwt_analysis -c "INSERT INTO presenters VALUES (
        DEFAULT, '$FILE', '$VIEW', '$BINDING', $CONF, $HANDLERS, $RPCS
    );"
done

# Run custom queries
psql gwt_analysis -c "
    SELECT binding_type, AVG(confidence), COUNT(*)
    FROM presenters
    GROUP BY binding_type;
"
```

## Best Practices Summary

### Quick Checklist

Before starting GWT analysis:
- [ ] Ollama running with gemma3:12b model
- [ ] Weaviate container started
- [ ] JAVA_SOURCE_DIR set correctly
- [ ] GWT application uses standard naming conventions
- [ ] Test on small module first

During analysis:
- [ ] Monitor extraction log for errors
- [ ] Check progress periodically
- [ ] Validate GWT role assignment
- [ ] Review confidence scores for MVP patterns

After analysis:
- [ ] Verify all expected GWT files processed
- [ ] Check Weaviate indexing status
- [ ] Test semantic search quality
- [ ] Generate and review PRD

## Support

For more examples and support:
- **Full Documentation**: README.md, CLAUDE.md
- **Quick Reference**: GWT_QUICK_REFERENCE.md
- **Test Fixtures**: tests/fixtures/gwt/
- **Validation Report**: output/gwt-validation/VALIDATION_REPORT.md

---

**Last Updated**: 2025-12-14
**Examples Tested With**: codeindex v1.0, GWT support branch 001-gwt-prd-support
