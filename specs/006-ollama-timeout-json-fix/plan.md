# Implementation Plan: Ollama Timeout and JSON Parsing Fix

**Branch**: `006-ollama-timeout-json-fix` | **Date**: 2025-12-19 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/006-ollama-timeout-json-fix/spec.md`

## Summary

Fix two critical production issues in the PRD generation pipeline:
1. **NameError**: `READ_TIMEOUT` undefined in `ollama_client.py:280` - should reference `self.read_timeout`
2. **AttributeError**: Invalid access to `rule.field` in `prd.py:1661` - `validation_rules` contains string IDs, not objects

Both issues cause extraction failures in production, with timeout errors blocking DAO analysis and the AttributeError crashing frontend PRD generation after successful form extraction.

## Technical Context

**Language/Version**: Python 3.8+
**Primary Dependencies**: httpx (HTTP client), json (JSON parsing), logging (error tracking)
**Storage**: Weaviate vector database (for indexed artifacts), JSON files (for intermediate form/component data)
**Testing**: pytest with unit tests (ollama_client, frontend_analyzer) and integration tests (prd generation)
**Target Platform**: Linux server (production: vlcucad001-eatnl), macOS (development)
**Project Type**: CLI pipeline (codeindex command with subcommands: discover, extract, index, search, prd)
**Performance Goals**: <10ms JSON cleaning overhead, no degradation in successful request times
**Constraints**: Backward compatible with existing OllamaClient usage, existing tests must pass
**Scale/Scope**: Production codebase: 539-1000+ files, 76 DAO files in cuco-ui-admin project

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate 1: Pre-Implementation (Blocking)

- [x] **Constitution compliance reviewed**: Feature aligns with Code Quality Standards (error handling), Testing Discipline (existing tests must pass), User Experience Consistency (better error messages)
- [x] **Test strategy defined**:
  - Unit tests: `test_ollama_client.py` (timeout reference fix), `test_prd.py` (validation_rules handling)
  - Integration tests: Existing PRD generation tests will validate fixes
  - Fixtures: Production log samples with actual errors
- [x] **External dependencies documented**: No new dependencies, uses existing httpx, json, logging
- [x] **Performance impact assessed**:
  - Timeout fix: No impact (just fixes error logging)
  - validation_rules fix: No impact (fixes crash, enables PRD generation)
- [x] **User-facing changes documented**: Error messages will be more accurate (correct timeout value logged)

**Justification**: This is a bug fix, not a new feature. Changes are minimal and localized to error handling code.

### Gate 2: Implementation Complete

- [ ] All tests passing (unit, integration)
- [ ] Test coverage maintained (no decrease in coverage)
- [ ] Error messages reviewed (accurate timeout values, clear AttributeError context)
- [ ] Logging statements use appropriate levels (WARNING for timeout, ERROR for AttributeError)
- [ ] Type hints preserved (no changes to function signatures)

### Gate 3: Integration Ready

- [ ] Integration tests validate fixes with production log samples
- [ ] No performance degradation (timeout fix is logging-only, validation_rules fix prevents crash)
- [ ] Error handling tested (timeout errors logged correctly, validation_rules handled gracefully)
- [ ] Documentation updated (CLAUDE.md troubleshooting section)
- [ ] No breaking changes (backward compatible)

## Project Structure

### Documentation (this feature)

```text
specs/006-ollama-timeout-json-fix/
├── spec.md              # Feature specification (existing)
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (production error analysis)
├── data-model.md        # N/A (no data model changes)
├── quickstart.md        # Phase 1 output (fix validation quickstart)
├── contracts/           # N/A (no API changes)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created yet)
```

### Source Code (repository root)

```text
src/codeindex/
├── services/
│   ├── ollama_client.py        # Fix line 280: READ_TIMEOUT → self.read_timeout
│   └── frontend_analyzer.py    # Already correct (creates string rule IDs)
├── cli/
│   └── prd.py                  # Fix line 1661: Handle validation_rules as strings
└── utils/
    └── config.py               # Already has ollama_read_timeout property

tests/
├── unit/
│   ├── test_ollama_client.py   # Verify timeout logging fix
│   └── test_prd.py             # Verify validation_rules handling fix
└── integration/
    └── test_prd_generation.py  # E2E validation with production samples
```

**Structure Decision**: Single project structure. Changes are isolated to 2 files in existing codebase. No new modules or refactoring required.

## Complexity Tracking

No constitution violations. This is a straightforward bug fix with no architectural changes.

---

## Phase 0: Outline & Research

### Research Tasks

1. **Production Error Analysis**
   - Analyzed production log: `log_cuco-ui-admin_step2_2025-12-18_10-37-44.log`
   - Identified two distinct error patterns:
     - `NameError: name 'READ_TIMEOUT' is not defined` at line 280 in ollama_client.py
     - `AttributeError: 'str' object has no attribute 'field'` at line 1661 in prd.py

2. **Root Cause Investigation**
   - **Issue 1 (ollama_client.py:280)**:
     - Error occurs in httpx.TimeoutException handler
     - Code uses undefined variable `READ_TIMEOUT` instead of `self.read_timeout`
     - Constants defined at module level (lines 30-31): `DEFAULT_READ_TIMEOUT = 240.0`
     - Instance variable set in `__init__`: `self.read_timeout = read_timeout`
     - Fix: Change `READ_TIMEOUT` to `self.read_timeout`

   - **Issue 2 (prd.py:1661)**:
     - Code iterates `form.validation_rules` expecting objects with `.field`, `.rule_type`, `.message`
     - Actual data structure: `validation_rules` is `List[str]` containing rule IDs
     - Evidence from frontend_analyzer.py:520: `form.validation_rules.append(rule_id)` (appends strings)
     - Evidence from frontend_analyzer.py:316: `'validation_rules': []` (initialized as empty list)
     - Fix: Skip validation_rules section or look up rules by ID (requires accessing rules collection)

3. **Impact Assessment**
   - **Issue 1**: Prevents accurate timeout error reporting, confuses users debugging slow LLM requests
   - **Issue 2**: Crashes frontend PRD generation after successful form extraction (waste of processing time)
   - **Production frequency**:
     - Timeout errors: ~15-20 occurrences in production log
     - AttributeError: 1 occurrence at end of run, but blocks PRD output
   - **User impact**:
     - Issue 1: Minor (error still raised, just wrong log message)
     - Issue 2: Critical (no frontend PRD generated)

4. **Solution Design**
   - **Issue 1**: One-line fix, change variable reference
   - **Issue 2**: Two options:
     - Option A: Skip validation_rules section entirely (simple, loses info)
     - Option B: Load rules from JSON files by ID and display them (complex, keeps info)
   - **Recommendation**: Option A for immediate fix (reduces crash), Option B for future enhancement

### Decision Log

| Decision | Rationale | Alternatives Considered |
|----------|-----------|-------------------------|
| Fix ollama_client.py:280 with self.read_timeout | Correct variable reference, aligns with instance attribute | None (clear bug) |
| Skip validation_rules in prd.py (Option A) | Simplest fix, prevents crash, minimal code change | Option B: Load rules by ID (requires file I/O, more complex) |
| No JSON cleaning changes | Spec included JSON cleaning, but production errors are variable reference bugs, not JSON parsing issues | Add JSON cleaning (deferred - no evidence of JSON parse failures in this log) |

**Output**: research.md (this section documents research findings)

---

## Phase 1: Design & Contracts

### Design Document

**File**: `data-model.md` (N/A - no data model changes)

**File**: `quickstart.md`

#### Quick Fix Validation Steps

1. **Verify ollama_client.py fix**:
   ```bash
   # Check current code (should fail)
   grep -n "READ_TIMEOUT" src/codeindex/services/ollama_client.py
   # Expected: Line 280: self.logger.warning(f"Ollama timeout after {READ_TIMEOUT}s: {e}")

   # After fix (should pass)
   grep -n "self.read_timeout" src/codeindex/services/ollama_client.py
   # Expected: Line 280: self.logger.warning(f"Ollama timeout after {self.read_timeout}s: {e}")
   ```

2. **Verify prd.py fix**:
   ```bash
   # Check current code (should fail)
   grep -A5 "for rule in form.validation_rules:" src/codeindex/cli/prd.py
   # Expected: Line 1661: lines.append(f"- **{rule.field}** ({rule.rule_type}): {rule.message}")

   # After fix (should pass)
   grep -A5 "if form.validation_rules:" src/codeindex/cli/prd.py
   # Expected: Skipped section or safe iteration
   ```

3. **Run unit tests**:
   ```bash
   pytest tests/unit/test_ollama_client.py -v
   pytest tests/unit/test_prd.py -v
   ```

4. **Run integration test with production sample**:
   ```bash
   # Test with cuco-ui-admin project
   codeindex prd frontend --extraction-file output/cuco-ui-admin/extraction-results.jsonl --output output/cuco-ui-admin-prd
   ```

#### Testing Strategy

**Unit Tests**:
- `test_ollama_client.py`:
  - Test timeout exception logging includes correct timeout value
  - Mock httpx.TimeoutException and verify log message

- `test_prd.py`:
  - Test `_generate_frontend_prd` with forms containing validation_rules as strings
  - Verify no AttributeError raised
  - Verify PRD generated successfully (validation_rules section skipped or handled safely)

**Integration Tests**:
- Use production extraction-results.jsonl from cuco-ui-admin
- Run frontend PRD generation
- Verify completion without AttributeError
- Check generated PRD for completeness (forms, fields, components)

### API Contracts

**File**: `contracts/` (N/A - no API changes)

No public API changes. Fixes are internal to error handling logic.

### Agent Context Update

```bash
# No new technologies added, skip agent context update
# .specify/memory/claude-context.md unchanged
```

**Output**: quickstart.md (validation steps documented above)

---

## Phase 2: Implementation Plan

**Note**: Phase 2 is handled by `/speckit.tasks` command. This plan provides the foundation for task generation.

### Implementation Overview

**Estimated Effort**: 30 minutes
- Issue 1 fix: 5 minutes (one-line change)
- Issue 2 fix: 10 minutes (skip validation_rules section)
- Testing: 15 minutes (unit tests + integration test)

### Key Implementation Areas

1. **ollama_client.py:280**
   - Change `READ_TIMEOUT` to `self.read_timeout`
   - Verify no other references to undefined `READ_TIMEOUT`
   - Test timeout exception logging

2. **prd.py:1661**
   - Comment out or conditionally skip validation_rules section
   - Add comment explaining validation_rules are IDs, not objects
   - Consider future enhancement to load rules by ID
   - Test with forms containing validation_rules

3. **Testing**
   - Add/update unit tests for both fixes
   - Run integration test with production data
   - Verify no regressions

### Files to Modify

| File | Lines | Change Type | Complexity |
|------|-------|-------------|------------|
| `src/codeindex/services/ollama_client.py` | 280 | Variable reference fix | Trivial |
| `src/codeindex/cli/prd.py` | 1657-1662 | Skip validation_rules section | Low |
| `tests/unit/test_ollama_client.py` | New test | Add timeout logging test | Low |
| `tests/unit/test_prd.py` | New test | Add validation_rules test | Low |

### Dependencies Between Changes

No dependencies. Both fixes are independent and can be implemented in parallel.

### Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Timeout logging fix breaks other code | Search for all `READ_TIMEOUT` references before fix |
| Skipping validation_rules loses important info | Add TODO comment for future enhancement (load rules by ID) |
| Test suite doesn't catch regressions | Add explicit tests for both error scenarios |
| Production deployment fails | Test with actual production data (cuco-ui-admin) before merging |

---

## Phase 3: Validation & Testing

### Test Coverage Requirements

**Target Coverage**: Maintain existing coverage (no decrease)

**New Tests**:
1. `test_ollama_timeout_logging` in `test_ollama_client.py`
   - Mock httpx.TimeoutException
   - Verify log message contains correct timeout value
   - Verify exception raised

2. `test_prd_validation_rules_as_strings` in `test_prd.py`
   - Create form with validation_rules as strings
   - Call `_generate_frontend_prd`
   - Verify no AttributeError
   - Verify PRD generated

**Existing Tests to Verify**:
- All ollama_client tests pass
- All prd generation tests pass
- Integration tests with Weaviate pass

### Integration Test Plan

1. **Setup**:
   - Use production extraction file: `output/cuco-ui-admin/extraction-results.jsonl`
   - Ensure Ollama running: `ollama serve`
   - Ensure Weaviate running: `./docker-weaviate.sh status`

2. **Execute**:
   ```bash
   codeindex prd frontend \
     --extraction-file output/cuco-ui-admin/extraction-results.jsonl \
     --output output/cuco-ui-admin-prd-test \
     --quiet
   ```

3. **Verify**:
   - Command completes successfully (exit code 0)
   - No NameError in logs
   - No AttributeError in logs
   - Frontend PRD generated: `output/cuco-ui-admin-prd-test/prd/frontend_prd.md`
   - PRD contains forms and components
   - PRD does not crash on validation_rules section

4. **Cleanup**:
   ```bash
   rm -rf output/cuco-ui-admin-prd-test
   ```

### Performance Validation

**Baseline**: Existing PRD generation time for cuco-ui-admin (before fixes)
**Target**: No performance degradation (within 5% of baseline)

**Measurement**:
```bash
time codeindex prd frontend \
  --extraction-file output/cuco-ui-admin/extraction-results.jsonl \
  --output output/cuco-ui-admin-prd-test
```

**Expected**: No significant difference (fixes are in error paths and removed code)

---

## Acceptance Criteria

**AC1: NameError Fix (ollama_client.py:280)**
- [x] Variable reference changed from `READ_TIMEOUT` to `self.read_timeout`
- [ ] Timeout exception logged with correct timeout value
- [ ] All existing ollama_client tests pass
- [ ] New test added for timeout logging

**AC2: AttributeError Fix (prd.py:1661)**
- [ ] validation_rules section skipped or safely handled
- [ ] No AttributeError when validation_rules contains strings
- [ ] Frontend PRD generation completes successfully
- [ ] New test added for validation_rules handling

**AC3: Integration Validation**
- [ ] Production data test passes (cuco-ui-admin)
- [ ] No NameError in production logs after deployment
- [ ] No AttributeError in production logs after deployment
- [ ] Frontend PRDs generated successfully

**AC4: Testing & Documentation**
- [ ] All tests passing (unit + integration)
- [ ] Test coverage maintained or improved
- [ ] CLAUDE.md updated with troubleshooting notes
- [ ] Commit message includes bug details and fixes

---

## Success Metrics

**Before (Production Issues)**:
- NameError: ~15-20 timeout errors with wrong error messages
- AttributeError: 1 crash blocking frontend PRD generation
- PRD generation success rate: 0% (blocked by AttributeError)

**After (Target)**:
- NameError: 0 (correct timeout value logged)
- AttributeError: 0 (section skipped safely)
- PRD generation success rate: 100% (completes without crashes)

---

## Appendix: Production Error Context

### Error 1: NameError in ollama_client.py

```
2025-12-18 17:28:24 [WARNING] codeindex.retry: Function _extract_form_with_llm failed (attempt 1/3): name 'READ_TIMEOUT' is not defined. Retrying in 1.0 seconds...
2025-12-18 17:30:07 [ERROR] codeindex.retry: Function _extract_form_with_llm failed after 3 attempts: name 'READ_TIMEOUT' is not defined
2025-12-18 17:30:07 [ERROR] codeindex.services.frontend_analyzer: Failed to analyze /mnt/cucocalcai/.../attributes.htm: name 'READ_TIMEOUT' is not defined
```

**Context**: Occurs during `_extract_form_with_llm` → `ollama_client.call_ollama` → httpx.TimeoutException handler

### Error 2: AttributeError in prd.py

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

**Context**: Occurs at end of frontend PRD generation, after successful form extraction

---

**End of Implementation Plan**
