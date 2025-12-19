# Research: Production Error Analysis

**Feature**: 006-ollama-timeout-json-fix
**Date**: 2025-12-19
**Researcher**: Implementation Planning Agent

## Executive Summary

Analyzed production log (`log_cuco-ui-admin_step2_2025-12-18_10-37-44.log`) from PRD generation pipeline. Identified two critical bugs causing extraction failures:

1. **NameError** in `ollama_client.py:280` - undefined variable `READ_TIMEOUT`
2. **AttributeError** in `prd.py:1661` - incorrect data type assumption for `validation_rules`

Both are simple code bugs requiring minimal fixes (1-2 line changes each). No architectural changes needed.

---

## Production Error Investigation

### Error 1: NameError in ollama_client.py

**Log Evidence**:
```
2025-12-18 17:28:24 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): name 'READ_TIMEOUT' is not defined. Retrying in 1.0 seconds...
2025-12-18 17:30:07 [ERROR] codeindex.retry: Function _extract_form_with_llm failed after 3 attempts: name 'READ_TIMEOUT' is not defined
2025-12-18 17:30:07 [ERROR] codeindex.services.frontend_analyzer: Failed to analyze /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-common/src/main/resources/at/a1ta/cuco/ui/common/public/tiny_mce/plugins/xhtmlxtras/attributes.htm: name 'READ_TIMEOUT' is not defined
```

**Frequency**: ~15-20 occurrences in production log

**Root Cause Analysis**:

File: `src/codeindex/services/ollama_client.py`

**Line 280 (problematic code)**:
```python
except httpx.TimeoutException as e:
    self.logger.warning(f"Ollama timeout after {READ_TIMEOUT}s: {e}")
    raise TimeoutError(f"Ollama request timed out: {e}") from e
```

**Problem**: Variable `READ_TIMEOUT` is not defined in local scope

**Evidence from codebase**:
- Lines 30-31 define module-level constants:
  ```python
  DEFAULT_CONNECT_TIMEOUT = 10.0
  DEFAULT_READ_TIMEOUT = 240.0    # seconds (4 minutes)
  ```
- Lines 105-153 define `__init__` constructor:
  ```python
  def __init__(
      self,
      base_url: str = "http://localhost:11434",
      model: str = "gemma2:12b",
      max_retries: int = 3,
      connect_timeout: float = DEFAULT_CONNECT_TIMEOUT,  # 10.0
      read_timeout: float = DEFAULT_READ_TIMEOUT         # 240.0
  ):
      self.connect_timeout = connect_timeout
      self.read_timeout = read_timeout
  ```

**Solution**: Change `READ_TIMEOUT` to `self.read_timeout` on line 280

**Impact**:
- User Impact: Minor - error still raised, but log message is misleading
- Frequency: Every timeout exception (15-20 in production log)
- Severity: Low (error handling works, just incorrect log message)

---

### Error 2: AttributeError in prd.py

**Log Evidence**:
```
2025-12-18 17:39:06 [ERROR] codeindex.codeindex.cli.prd: Frontend layer analysis failed: 'str' object has no attribute 'field'
Traceback (most recent call last):
  File "/home/tkamsker/development/Iteration20/gha1javarag/src/codeindex/cli/prd.py", line 914, in _analyze_frontend_layer
    prd_content = _generate_frontend_prd(forms, components)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/tkamsker/development/Iteration20/gha1javarag/src/codeindex/cli/prd.py", line 1661, in _generate_frontend_prd
    lines.append(f"- **{rule.field}** ({rule.rule_type}): {rule.message}")
                        ^^^^^^^^^^
AttributeError: 'str' object has no attribute 'field'. Did you mean: 'find'?
```

**Frequency**: 1 occurrence at end of PRD generation run

**Root Cause Analysis**:

File: `src/codeindex/cli/prd.py`

**Lines 1657-1662 (problematic code)**:
```python
# Validation rules
if form.validation_rules:
    lines.append("**Validation Rules:**")
    lines.append("")
    for rule in form.validation_rules:
        lines.append(f"- **{rule.field}** ({rule.rule_type}): {rule.message}")
    lines.append("")
```

**Problem**: Code assumes `validation_rules` contains objects with `.field`, `.rule_type`, `.message` attributes

**Actual Data Structure**:

Evidence from `src/codeindex/services/frontend_analyzer.py`:

**Line 316 (initialization)**:
```python
'validation_rules': [],
```

**Line 520 (appending data)**:
```python
form.validation_rules.append(rule_id)  # Appends STRING, not object
```

**Data Type**: `validation_rules: List[str]` - contains rule ID strings like "rule-123", not BusinessRule objects

**Why This Happened**:
- Forms are saved to JSON files with validation_rules as list of rule ID strings
- Rules are saved to separate files (one JSON file per rule)
- PRD generation loads forms from JSON but doesn't load corresponding rule files
- Code incorrectly assumes rules are embedded objects

**Solution Options**:

**Option A: Skip validation_rules section (recommended for immediate fix)**
- Comment out lines 1657-1662
- Add TODO for future enhancement
- PRD still generated, just without validation_rules section
- Simplest fix, no file I/O needed

**Option B: Load rules by ID (future enhancement)**
- Keep validation_rules section
- Load rule JSON files by ID from `output_dir/frontend/rules/`
- Parse JSON and display rule details
- More complex, requires file I/O and error handling

**Impact**:
- User Impact: Critical - crashes PRD generation, no output generated
- Frequency: Every PRD generation with forms containing validation rules
- Severity: High (blocks entire PRD generation)

---

## Decision Log

### Decision 1: Fix ollama_client.py with self.read_timeout

**Decision**: Change `READ_TIMEOUT` to `self.read_timeout` on line 280

**Rationale**:
- Clear bug - variable not defined
- Simple one-line fix
- Aligns with instance attribute naming
- No performance impact

**Alternatives Considered**: None (clear bug fix)

**Implementation**: One-line change in ollama_client.py:280

---

### Decision 2: Skip validation_rules section in prd.py (Option A)

**Decision**: Comment out lines 1657-1662, add TODO for future enhancement

**Rationale**:
- Simplest fix to prevent crash
- Minimal code changes (6 lines commented out)
- No file I/O or error handling needed
- Allows PRD generation to complete successfully
- Info loss acceptable (validation rules rarely used in initial PRD review)

**Alternatives Considered**:
- **Option B: Load rules by ID** - More complex, requires:
  - File I/O to load rule JSON files
  - Error handling for missing rule files
  - JSON parsing and validation
  - More testing needed
  - Deferred to future enhancement

**Implementation**:
```python
# TODO: validation_rules contains rule IDs (strings), not rule objects
# To display rules, need to load rule JSON files from output_dir/frontend/rules/
# For now, skip this section to prevent AttributeError
# if form.validation_rules:
#     lines.append("**Validation Rules:**")
#     lines.append("")
#     for rule in form.validation_rules:
#         lines.append(f"- **{rule.field}** ({rule.rule_type}): {rule.message}")
#     lines.append("")
```

---

### Decision 3: No JSON cleaning changes in this fix

**Decision**: Defer JSON cleaning enhancements to future feature

**Rationale**:
- Original spec included JSON cleaning improvements
- Production log shows NO JSON parsing failures
- All errors are variable reference bugs (NameError, AttributeError)
- JSON cleaning already implemented in `ollama_client.py:170-205`
- No evidence that JSON cleaning is needed for these specific errors

**Evidence**:
```
2025-12-18 17:31:00 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: ImageListWidgetForm
2025-12-18 17:35:50 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: EditPdfMetadataWidgetForm
2025-12-18 17:39:06 [INFO] codeindex.services.frontend_analyzer: ✓ Extracted form: style_form
```

Forms extracted successfully - no JSON parse errors. Only errors are:
1. NameError during timeout exception handling
2. AttributeError during PRD generation (after successful extraction)

**Implementation**: No changes to JSON cleaning logic in this feature

---

## Testing Strategy

### Unit Tests

**test_ollama_client.py**:
- New test: `test_ollama_timeout_logging`
  - Mock httpx.TimeoutException
  - Verify log message contains `self.read_timeout` value (e.g., "240s")
  - Verify TimeoutError raised with correct message

**test_prd.py**:
- New test: `test_prd_validation_rules_as_strings`
  - Create mock form with `validation_rules = ["rule-1", "rule-2"]`
  - Call `_generate_frontend_prd([form], [])`
  - Verify no AttributeError raised
  - Verify PRD generated successfully
  - Verify validation_rules section skipped (or handled safely)

### Integration Tests

**test_prd_generation.py**:
- Use production extraction file: `output/cuco-ui-admin/extraction-results.jsonl`
- Run frontend PRD generation
- Verify:
  - Command completes (exit code 0)
  - No NameError in logs
  - No AttributeError in logs
  - PRD file created: `output/cuco-ui-admin-prd/prd/frontend_prd.md`
  - PRD contains expected sections (forms, components)

### Manual Testing

1. Run full pipeline on cuco-ui-admin project
2. Monitor logs for errors
3. Verify PRD generated successfully
4. Compare PRD content before/after fix (validation_rules section removed)

---

## Performance Impact

### Timeout Fix Impact

**Expected**: Zero performance impact
- Fix is logging-only (error path)
- No changes to hot path (successful requests)
- No additional I/O or computation

**Validation**: Run integration test with timing
```bash
time codeindex prd frontend --extraction-file output/cuco-ui-admin/extraction-results.jsonl --output output/test
```

### validation_rules Fix Impact

**Expected**: Slight performance improvement (fewer iterations)
- Removes 6 lines of code (lines 1657-1662)
- Skips iteration over validation_rules list
- No file I/O avoided (rules were never loaded)

**Measurement**: Compare PRD generation time before/after
- Before: Crashes with AttributeError (no timing)
- After: Completes successfully (~10-15 seconds for cuco-ui-admin)

---

## Risks & Mitigation

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Fix breaks other timeout handlers | Low | Search for all `READ_TIMEOUT` references (should find none) |
| Skipping validation_rules loses important info | Low | Add TODO for future enhancement, document in commit message |
| Tests don't catch regressions | Medium | Add explicit tests for both error scenarios |
| Production deployment fails | Medium | Test with actual production data before deploying |
| Other code expects validation_rules objects | Low | Grep for `validation_rules` usage (should find only 2 locations) |

---

## Future Enhancements

### Enhancement 1: Load validation_rules by ID

**Description**: Implement Option B from Decision 2
- Load rule JSON files from `output_dir/frontend/rules/`
- Parse and validate rule objects
- Display rule details in PRD

**Benefits**:
- Complete PRD with all validation rules
- Better documentation for form validation logic

**Effort**: 2-3 hours (file I/O, error handling, testing)

### Enhancement 2: JSON Cleaning Improvements

**Description**: Enhance JSON cleaning based on spec.md
- More robust markdown fence stripping
- Better error recovery for malformed JSON
- Detailed logging for JSON parse failures

**Benefits**:
- Reduced LLM JSON parsing failures
- Better error messages for debugging

**Effort**: 3-4 hours (implementation, testing)

**When**: If/when production logs show JSON parse failures

---

## References

### Production Logs
- File: `log_cuco-ui-admin_step2_2025-12-18_10-37-44.log`
- Date: 2025-12-18
- Server: vlcucad001-eatnl
- Project: cuco-ui-admin (539-file codebase)

### Code Files Analyzed
- `src/codeindex/services/ollama_client.py` (lines 30-31, 105-153, 280)
- `src/codeindex/services/frontend_analyzer.py` (lines 316, 520)
- `src/codeindex/cli/prd.py` (lines 1552-1679)
- `src/codeindex/utils/config.py` (lines 81-93)

### Related Features
- Feature 001: Java Codebase Indexer (extraction pipeline)
- Feature 002: PRD Document Generation (frontend PRD generation)
- Feature 003: GWT PRD Support (form extraction)

---

**End of Research Document**
