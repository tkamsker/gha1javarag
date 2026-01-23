# Production Indexing Status Checker

Quick diagnostic script to check the health of your indexing pipeline on production server `vlcucad001-eatnl`.

## What It Checks

1. **Source Directory** - Verifies source files exist (Java, JSP, XML counts)
2. **Discovery File** - Validates discovery JSON structure and file counts
3. **Extraction File** - Counts artifacts by type from extraction results
4. **Weaviate Service** - Tests connectivity to vector database
5. **Ollama Service** - Tests connectivity to LLM service
6. **Indexed Data** - Queries Weaviate for actual artifact counts
7. **Search Function** - Tests that search is returning results

## Usage

### Copy to Production Server

```bash
# From your dev machine
scp check_production_indexing.sh user@vlcucad001-eatnl:/path/to/gha1javarag/
```

### Run on Production

```bash
# SSH to production
ssh user@vlcucad001-eatnl

# Go to project directory
cd /path/to/gha1javarag

# Activate virtual environment
source .venv/bin/activate

# Install the package if not already installed
pip install -e .

# Run checker for cuco-ui-admin
./check_production_indexing.sh cuco-ui-admin /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-admin

# Run checker for cuco-ui-app
./check_production_indexing.sh cuco-ui-app /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-app

# Run with default project name only
./check_production_indexing.sh
```

## Understanding the Output

### ✓ All Systems Operational

```
✓ ALL SYSTEMS OPERATIONAL

The indexing pipeline has run successfully:
  1. Discovery found files
  2. Extraction created artifacts
  3. Weaviate has indexed data

Next steps:
  - Test web UI: streamlit run src/codeindex/web/app.py
  - Run search: codeindex search 'your query'
```

**Meaning**: Everything is working perfectly. Your project is fully indexed and searchable.

**Next**: Use the web UI or CLI to search your codebase.

---

### ⚠ Indexing Incomplete

```
⚠ INDEXING INCOMPLETE

Pipeline ran but Weaviate has no artifacts.

Action required:
  1. Check indexing logs
  2. Re-run indexing stage
  3. Verify with codeindex status
```

**Meaning**: Discovery and extraction worked, but data didn't make it into Weaviate.

**Fix**:
```bash
# Check logs for errors
tail -100 data/indexing-cuco-ui-admin.log

# Re-run just the indexing step
codeindex index \
  --inventory data/discovery-cuco-ui-admin.jsonl \
  --extraction data/extraction-cuco-ui-admin.jsonl

# Verify it worked
codeindex status
```

---

### ⚠ Extraction Failed

```
⚠ EXTRACTION FAILED

Discovery succeeded but extraction failed.

Action required:
  1. Check Ollama is running
  2. Re-run extraction
```

**Meaning**: Files were discovered but AI extraction didn't complete.

**Fix**:
```bash
# Verify Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it
ollama serve &

# Re-run extraction
codeindex extract \
  --inventory data/discovery-cuco-ui-admin.jsonl \
  --output data/extraction-cuco-ui-admin.jsonl

# Then run indexing
codeindex index \
  --inventory data/discovery-cuco-ui-admin.jsonl \
  --extraction data/extraction-cuco-ui-admin.jsonl
```

---

### ✗ Pipeline Failed

```
✗ PIPELINE FAILED

Discovery did not find files or failed completely.

Action required:
  1. Verify source directory
  2. Re-run full pipeline
```

**Meaning**: Discovery stage failed - source directory may be wrong or inaccessible.

**Fix**:
```bash
# Verify source exists and has files
ls -la /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-admin
find /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-admin -name "*.java" | head -5

# Re-run full pipeline with correct path
./fix_indexing.sh cuco-ui-admin /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-admin
```

## Sample Output

```
==============================================
Production Indexing Status Check
==============================================
Project:    cuco-ui-admin
Source:     /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-admin
Date:       2026-01-23 10:30:00
==============================================

[INFO] Check 1: Source Directory
[✓ PASS] Source directory exists
[INFO]   Found: 145 Java, 0 JSP, 89 XML files

[INFO] Check 2: Discovery File (data/discovery-cuco-ui-admin.jsonl)
[✓ PASS] Discovery file exists: 2 lines
  Files discovered in JSON: 1,564
    - java_source: /path/to/AdminPresenter.java
    - gwt_ui_binder: /path/to/AdminView.ui.xml
    - xml: /path/to/ibatis-config.xml
[✓ PASS] Discovery file contains valid project data

[INFO] Check 3: Extraction File (data/extraction-cuco-ui-admin.jsonl)
[✓ PASS] Extraction file exists: 13,640 lines
  Total artifacts: 13,639
  Artifact types:
    - java_source: 8,234
    - gwt_presenter: 145
    - gwt_view: 142
    - dao_call: 523
    - dto_artifact: 412
[✓ PASS] Extraction file contains artifacts

[INFO] Check 4: Weaviate Service
[✓ PASS] Weaviate is accessible

[INFO] Check 5: Ollama Service
[✓ PASS] Ollama is accessible

[INFO] Check 6: Weaviate Indexed Data
  Total projects in Weaviate: 3

  ✓ Target project found: cuco-ui-admin:2f0368fb
    Artifacts: 13,635
    Last indexed: 2026-01-23 08:50:00
    Other: cuco-ui-app:abc123 (8,421 artifacts)
[✓ PASS] Project is indexed in Weaviate with artifacts

[INFO] Check 7: Search Functionality
  Search returned 5 results
    1. gwt_presenter (score: 0.89)
    2. java_source (score: 0.85)
    3. dao_call (score: 0.82)
[✓ PASS] Search is working

==============================================
Summary & Recommendations
==============================================

✓ ALL SYSTEMS OPERATIONAL

The indexing pipeline has run successfully:
  1. Discovery found files
  2. Extraction created artifacts
  3. Weaviate has indexed data

Next steps:
  - Test web UI: streamlit run src/codeindex/web/app.py
  - Run search: codeindex search 'your query'

==============================================
Done. Check output above for issues.
==============================================
```

## Troubleshooting Common Issues

### Issue: "Project not found in Weaviate"

**Symptoms**: Check 6 fails, no project in Weaviate

**Cause**: Indexing step never ran or failed silently

**Solution**:
```bash
# Run indexing with verbose output
codeindex index \
  --inventory data/discovery-cuco-ui-admin.jsonl \
  --extraction data/extraction-cuco-ui-admin.jsonl \
  --verbose

# Check logs
tail -50 data/indexing-cuco-ui-admin.log | grep -i error
```

---

### Issue: "0 artifacts indexed"

**Symptoms**: Project found but artifact_count = 0

**Cause**: Extraction file is empty or invalid

**Solution**:
```bash
# Check extraction file content
head -5 data/extraction-cuco-ui-admin.jsonl

# If empty, re-run extraction
codeindex extract \
  --inventory data/discovery-cuco-ui-admin.jsonl \
  --output data/extraction-cuco-ui-admin.jsonl

# Then index
codeindex index \
  --inventory data/discovery-cuco-ui-admin.jsonl \
  --extraction data/extraction-cuco-ui-admin.jsonl
```

---

### Issue: "Search returned no results"

**Symptoms**: Check 7 fails, search returns empty

**Cause**: Data indexed but embeddings not generated

**Solution**:
```bash
# Check Ollama embeddings model
ollama list | grep nomic

# If missing, pull it
ollama pull nomic-embed-text

# Re-index with fresh embeddings
codeindex index \
  --inventory data/discovery-cuco-ui-admin.jsonl \
  --extraction data/extraction-cuco-ui-admin.jsonl \
  --force-reindex
```

---

### Issue: "Weaviate is not accessible"

**Symptoms**: Check 4 fails, can't connect to port 8080

**Cause**: Docker container not running

**Solution**:
```bash
# Check docker status
docker ps | grep weaviate

# If not running, start it
./docker-weaviate.sh start

# Check logs
./docker-weaviate.sh logs
```

---

### Issue: "Ollama is not accessible"

**Symptoms**: Check 5 fails, can't connect to port 11434

**Cause**: Ollama service not started

**Solution**:
```bash
# Start Ollama in background
ollama serve &

# Verify it's running
curl http://localhost:11434/api/tags

# Check available models
ollama list
```

## Quick Commands Reference

```bash
# Full status check
./check_production_indexing.sh cuco-ui-admin /path/to/source

# Re-run discovery only
codeindex discover --source-dir /path/to/source --output data/discovery-PROJECT.jsonl

# Re-run extraction only
codeindex extract --inventory data/discovery-PROJECT.jsonl --output data/extraction-PROJECT.jsonl

# Re-run indexing only
codeindex index --inventory data/discovery-PROJECT.jsonl --extraction data/extraction-PROJECT.jsonl

# Full pipeline (all stages)
./fix_indexing.sh PROJECT_NAME /path/to/source

# Check Weaviate status
codeindex status

# Test search
codeindex search "presenter" --project PROJECT_NAME

# Start web UI
streamlit run src/codeindex/web/app.py
```

## Files Created

- `check_production_indexing.sh` - Main diagnostic script
- `PRODUCTION_CHECK_README.md` - This documentation

## Support

If the script shows errors you can't resolve:

1. **Capture full output**:
   ```bash
   ./check_production_indexing.sh cuco-ui-admin /path/to/source 2>&1 | tee check-output.txt
   ```

2. **Check logs**:
   ```bash
   ls -lh data/*.log
   tail -100 data/indexing-cuco-ui-admin.log
   ```

3. **Verify environment**:
   ```bash
   echo $JAVA_SOURCE_DIR
   cat .env | grep -v "^#"
   which python3
   python3 --version
   ```

4. **Review CLAUDE.md** for detailed troubleshooting in the main documentation
