# Production Run Failure Analysis & Fix Plan

**Date**: 2026-01-08  
**Analysis Source**: `/Users/thomaskamsker/Desktop/AKT_Docs/2026/AI/CucoCalc/20260107_cuco`  
**Status**: Failed - Exit Code 5 (OUTPUT_DIR_ERROR)

---

## Executive Summary

The production run failed with three main categories of issues:

1. **CRITICAL**: Output directory path resolution failure (Exit Code 5)
2. **HIGH**: Weaviate schema validation errors (dependencies/entities stored as objects instead of text arrays)
3. **MEDIUM**: Ollama timeout errors (20 files failed after 240s timeout)

**Pipeline Status**:
- ✅ Discovery: Completed successfully
- ✅ Extraction: Completed successfully  
- ✅ Indexing: Completed (13,639 artifacts indexed) but with schema errors
- ❌ Services PRD: Failed (Exit Code 5)
- ✅ Frontend PRD: Completed (44 forms, 20 files failed due to timeouts)

---

## Issue Analysis

### Issue #1: Output Directory Error (CRITICAL - Exit Code 5)

**Error Message**:
```
Error: Cannot write to output directory: output/cuco-ui-admin/prd - [Errno 2] No such file or directory: 'output/cuco-ui-admin/prd/.write_test'
```

**Root Cause**:
- The `production-requirements-generation.sh` script uses relative path `output/cuco-ui-admin/prd`
- The script runs `nohup` commands which may execute from a different working directory
- The output directory validation in `prd.py` tries to create the directory but fails because parent directories don't exist or working directory is wrong

**Location**: 
- `production-requirements-generation.sh` line 103, 114
- `src/codeindex/cli/prd.py` line 454-465

**Impact**: Services PRD generation completely failed, preventing completion of the pipeline.

---

### Issue #2: Weaviate Schema Validation Errors (HIGH)

**Error Messages**:
```
{'error': [{'message': "invalid text array property 'entities' on class 'CodeArtifact': not a text array, but map[string]interface {}"}]}
{'error': [{'message': "invalid text array property 'dependencies' on class 'CodeArtifact': invalid text array value: [map[description:The script relies on TinyMCE for its popup functionality... name:TinyMCE]]"}]}
```

**Root Cause**:
- The LLM extraction returns `dependencies` and `entities` as objects/maps with fields like `{name: "...", description: "..."}`
- Weaviate schema expects `text[]` (array of strings)
- The `_artifact_to_weaviate()` method in `weaviate_store.py` directly passes these objects without normalization

**Location**:
- `src/codeindex/services/weaviate_store.py` line 365, 369

**Impact**: 
- Some artifacts fail to index properly (though the error count shows 0, these are validation errors)
- Data integrity issues - dependencies/entities stored incorrectly
- May cause search/query issues later

---

### Issue #3: Ollama Timeout Errors (MEDIUM)

**Error Pattern**:
```
[WARNING] Function _extract_form_with_llm failed (attempt 1/3): Ollama request timed out: timed out
[ERROR] Function _extract_form_with_llm failed after 3 attempts: Ollama request timed out: timed out
[ERROR] Failed to analyze .../tiny_mce/plugins/.../media.htm: Ollama request timed out: timed out
```

**Root Cause**:
- Large/complex HTML files (TinyMCE plugins, etc.) take longer than 240 seconds to analyze
- The timeout is already set to 240s (4 minutes) which is quite high
- Some files may be too large or complex for the LLM to process efficiently

**Affected Files**: 20 files (mostly TinyMCE plugin HTML files)

**Location**:
- `src/codeindex/services/frontend_analyzer.py`
- `src/codeindex/services/ollama_client.py`

**Impact**:
- 20 files skipped in frontend analysis
- Frontend PRD completed but incomplete (missing some forms)

---

## Step-by-Step Fix Plan

### Phase 1: Fix Output Directory Issue (CRITICAL - Do First)

#### Step 1.1: Update `production-requirements-generation.sh` to use absolute paths

**File**: `production-requirements-generation.sh`

**Changes**:
1. Convert `OUTPUT_DIR` to absolute path using `$(pwd)` or `$PWD`
2. Ensure output directory is created before running PRD commands
3. Pass absolute path to `--output-dir` flag

**Implementation**:
```bash
# After line 33, add:
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

# After line 34, change to:
OUTPUT_DIR="${SCRIPT_DIR}/output/${PROJECT_NAME}"

# After line 53, add explicit directory creation:
mkdir -p "${OUTPUT_DIR}/prd"
```

**Expected Result**: Output directory will be created relative to script location, not current working directory.

---

#### Step 1.2: Add defensive directory creation in PRD command

**File**: `src/codeindex/cli/prd.py`

**Changes**:
1. Improve error message to show absolute path
2. Add better error handling for parent directory creation
3. Log the actual working directory for debugging

**Implementation** (around line 454-465):
```python
# Check output directory is writable
try:
    # Ensure parent directories exist
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    # Try writing a test file
    test_file = output_dir / ".write_test"
    test_file.touch()
    test_file.unlink()
except OSError as e:
    import os
    cwd = os.getcwd()
    abs_output_dir = output_dir.resolve()
    if not quiet:
        click.echo(f"Error: Cannot write to output directory: {abs_output_dir}", err=True)
        click.echo(f"  Current working directory: {cwd}", err=True)
        click.echo(f"  Error details: {e}", err=True)
    logger.error(f"Output directory not writable: {abs_output_dir} (cwd: {cwd}) - {e}")
    return EXIT_OUTPUT_DIR_ERROR
except Exception as e:
    # ... existing code ...
```

**Expected Result**: Better error messages and more robust directory creation.

---

### Phase 2: Fix Weaviate Schema Validation Errors (HIGH)

#### Step 2.1: Normalize dependencies to text array

**File**: `src/codeindex/services/weaviate_store.py`

**Changes**:
1. Add helper function to normalize dependencies/entities to strings
2. Handle both string arrays and object arrays
3. Extract meaningful string representation from objects

**Implementation** (add before `_artifact_to_weaviate` method, around line 320):

```python
def _normalize_to_string_array(self, value: Any) -> List[str]:
    """
    Normalize a value to a list of strings.
    
    Handles:
    - List of strings: returns as-is
    - List of dicts: extracts 'name' field or converts to string
    - Single string: wraps in list
    - None/empty: returns empty list
    
    Args:
        value: Value to normalize
        
    Returns:
        List of strings
    """
    if not value:
        return []
    
    if isinstance(value, str):
        return [value]
    
    if not isinstance(value, list):
        return [str(value)]
    
    result = []
    for item in value:
        if isinstance(item, str):
            result.append(item)
        elif isinstance(item, dict):
            # Extract name field if available, otherwise convert to string
            if "name" in item:
                result.append(str(item["name"]))
            elif "library_name" in item:
                result.append(str(item["library_name"]))
            else:
                # Fallback: create a meaningful string representation
                result.append(str(item))
        else:
            result.append(str(item))
    
    return result
```

**Update `_artifact_to_weaviate` method** (around line 365, 369):

```python
# Replace:
"entities": semantic.get("entities", []),
# With:
"entities": self._normalize_to_string_array(semantic.get("entities", [])),

# Replace:
"dependencies": semantic.get("dependencies", []),
# With:
"dependencies": self._normalize_to_string_array(semantic.get("dependencies", [])),
```

**Expected Result**: Dependencies and entities will be stored as text arrays, matching Weaviate schema.

---

#### Step 2.2: Add validation logging

**File**: `src/codeindex/services/weaviate_store.py`

**Changes**:
1. Log when normalization occurs (for debugging)
2. Add warning if objects are detected

**Implementation** (in `_normalize_to_string_array`):
```python
# After checking if item is dict:
if isinstance(item, dict):
    logger.debug(f"Normalizing dependency/entity object to string: {item}")
    # ... rest of normalization code ...
```

**Expected Result**: Better visibility into data normalization issues.

---

### Phase 3: Address Ollama Timeout Issues (MEDIUM)

#### Step 3.1: Add file size filtering

**File**: `src/codeindex/services/frontend_analyzer.py`

**Changes**:
1. Skip files larger than a threshold (e.g., 500KB) for LLM analysis
2. Log skipped files
3. Optionally use simpler extraction for large files

**Implementation** (find where files are analyzed):
```python
# Before calling LLM, check file size:
MAX_FILE_SIZE_FOR_LLM = 500 * 1024  # 500KB

file_size = file_path.stat().st_size
if file_size > MAX_FILE_SIZE_FOR_LLM:
    logger.warning(f"Skipping LLM analysis for large file ({file_size} bytes): {file_path}")
    # Optionally: try simpler extraction or skip entirely
    continue
```

**Expected Result**: Large files won't cause timeouts.

---

#### Step 3.2: Add timeout configuration option

**File**: `src/codeindex/cli/prd.py`

**Changes**:
1. Allow per-layer timeout configuration
2. Increase default timeout for frontend (HTML files are larger)

**Implementation** (around line 113-116):
```python
@click.option(
    '--llm-timeout',
    type=int,
    default=120,
    help='Timeout for each LLM call in seconds (default: 120, recommended: 240 for frontend)'
)
```

**Update production script** (already done - uses 240s).

**Expected Result**: More flexible timeout configuration.

---

#### Step 3.3: Add retry with exponential backoff for timeouts

**File**: `src/codeindex/services/ollama_client.py`

**Changes**:
1. Implement exponential backoff for timeout errors
2. Increase delay between retries for timeouts

**Implementation**: Check if already implemented, if not add exponential backoff.

**Expected Result**: Better handling of transient timeout issues.

---

### Phase 4: Testing & Validation

#### Step 4.1: Test output directory fix

**Commands**:
```bash
cd /path/to/project
./production-requirements-generation.sh cuco-ui-admin /mnt/cucocalcai/cuco-master/cuco-ui-admin
```

**Validation**:
- Check that `output/cuco-ui-admin/prd` directory is created
- Verify both services and frontend PRD generation complete
- Check exit code is 0

---

#### Step 4.2: Test Weaviate schema fix

**Commands**:
```bash
# Re-index a small subset to test
codeindex index --inventory "data/discovery-cuco-ui-admin.jsonl" --extraction "data/extraction-cuco-ui-admin.jsonl"
```

**Validation**:
- Check logs for schema errors (should be zero)
- Verify dependencies/entities are stored as text arrays in Weaviate
- Query Weaviate to confirm data format

---

#### Step 4.3: Test timeout handling

**Commands**:
```bash
# Run frontend PRD generation with verbose logging
codeindex prd frontend --project cuco-ui-admin --llm-timeout 240 --verbose
```

**Validation**:
- Check that large files are skipped or handled gracefully
- Verify timeout errors are reduced
- Check that frontend PRD completes successfully

---

## Implementation Priority

1. **IMMEDIATE** (Fix before next production run):
   - Phase 1: Output directory fix
   - Phase 2: Weaviate schema normalization

2. **SHORT TERM** (Next sprint):
   - Phase 3: Timeout handling improvements

3. **ONGOING**:
   - Phase 4: Testing and monitoring

---

## Expected Outcomes

After implementing fixes:

1. ✅ **Output Directory**: Services PRD generation will succeed
2. ✅ **Weaviate Schema**: All artifacts will index without validation errors
3. ✅ **Timeouts**: Reduced timeout failures, better handling of large files
4. ✅ **Pipeline Completion**: Full pipeline will complete successfully

---

## Monitoring & Validation

After fixes are deployed:

1. **Monitor logs** for:
   - Output directory creation messages
   - Weaviate schema errors (should be zero)
   - Timeout warnings (should be reduced)

2. **Validate output**:
   - Check `output/cuco-ui-admin/prd/services_prd.md` exists
   - Check `output/cuco-ui-admin/prd/frontend_prd.md` exists
   - Verify PRD content quality

3. **Check Weaviate**:
   - Query sample artifacts to verify dependencies/entities format
   - Run `codeindex status` to verify indexing

---

## Notes

- The frontend PRD completed successfully despite timeouts (44 forms extracted)
- The pipeline indexing completed (13,639 artifacts) but with schema warnings
- The main blocker was the output directory issue preventing services PRD generation
- Schema errors don't prevent indexing but may cause data quality issues

---

## Related Files

- `production-requirements-generation.sh` - Main production script
- `src/codeindex/cli/prd.py` - PRD generation CLI
- `src/codeindex/services/weaviate_store.py` - Weaviate storage service
- `src/codeindex/services/frontend_analyzer.py` - Frontend analysis service
- `src/codeindex/services/ollama_client.py` - Ollama client service

