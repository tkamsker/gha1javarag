# Tasks: Ollama Timeout and JSON Parsing Fix

**Input**: Design documents from `/specs/006-ollama-timeout-json-fix/`
**Prerequisites**: plan.md (complete), spec.md (complete), research.md (complete), quickstart.md (complete)

**Organization**: This is a bug fix feature with two independent fixes organized as functional requirements (FR1, FR2, FR3).

## Format: `[ID] [P?] [FR] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[FR]**: Which functional requirement this task addresses (FR1, FR2, FR3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Changes isolated to 2 files: `src/codeindex/services/ollama_client.py`, `src/codeindex/cli/prd.py`

---

## Phase 1: Setup (Validation & Environment)

**Purpose**: Verify environment and baseline before fixes

- [ ] T001 Verify Python 3.8+ environment and pytest installed
- [ ] T002 Run existing test suite to establish baseline in tests/unit/ and tests/integration/
- [ ] T003 [P] Verify production log available at project root for reference

**Checkpoint**: Environment ready, baseline test results recorded

---

## Phase 2: Bug Fix 1 - NameError in ollama_client.py (FR1: Configurable Timeout)

**Goal**: Fix NameError where `READ_TIMEOUT` is undefined, should reference `self.read_timeout`

**Root Cause**: Line 280 uses undefined variable `READ_TIMEOUT` instead of instance attribute `self.read_timeout`

**Independent Test**: Timeout exception logs correct timeout value without NameError

### Implementation for Bug Fix 1

- [ ] T004 [FR1] Search for all occurrences of `READ_TIMEOUT` in src/codeindex/services/ollama_client.py
- [ ] T005 [FR1] Fix line 280: Change `READ_TIMEOUT` to `self.read_timeout` in src/codeindex/services/ollama_client.py
- [ ] T006 [FR1] Verify no other undefined `READ_TIMEOUT` references in src/codeindex/services/ollama_client.py
- [ ] T007 [FR1] Add unit test for timeout exception logging in tests/unit/test_ollama_client.py

**Checkpoint**: ollama_client.py fix complete, timeout errors logged with correct value

---

## Phase 3: Bug Fix 2 - AttributeError in prd.py (FR2: Robust JSON Parsing)

**Goal**: Fix AttributeError where code expects `validation_rules` to contain objects, but contains string IDs

**Root Cause**: Lines 1657-1662 iterate `validation_rules` expecting objects with `.field`, `.rule_type`, `.message` attributes, but list contains string IDs

**Independent Test**: Frontend PRD generation completes without AttributeError

### Implementation for Bug Fix 2

- [ ] T008 [FR2] Locate validation_rules iteration in src/codeindex/cli/prd.py at lines 1657-1662
- [ ] T009 [FR2] Comment out lines 1657-1662 (validation_rules section) in src/codeindex/cli/prd.py
- [ ] T010 [FR2] Add TODO comment explaining validation_rules are IDs, future enhancement needed in src/codeindex/cli/prd.py
- [ ] T011 [FR2] Add unit test for validation_rules handling in tests/unit/test_prd.py

**Checkpoint**: prd.py fix complete, PRD generation no longer crashes on validation_rules

---

## Phase 4: Integration Testing (FR3: Improved Error Handling)

**Goal**: Validate both fixes work together with production data

**Independent Test**: Full PRD generation pipeline completes without NameError or AttributeError

### Integration Tests

- [ ] T012 [FR3] Run existing unit tests in tests/unit/test_ollama_client.py to verify no regressions
- [ ] T013 [FR3] Run existing unit tests in tests/unit/test_prd.py to verify no regressions
- [ ] T014 [FR3] Run integration test with production extraction file (output/cuco-ui-admin/extraction-results.jsonl) if available
- [ ] T015 [FR3] Verify no NameError in logs from integration test
- [ ] T016 [FR3] Verify no AttributeError in logs from integration test
- [ ] T017 [FR3] Verify frontend PRD generated successfully in output directory

**Checkpoint**: All tests pass, integration validated with production-like data

---

## Phase 5: Documentation & Polish

**Purpose**: Update documentation and finalize changes

- [ ] T018 [P] Update CLAUDE.md troubleshooting section with NameError fix at project root
- [ ] T019 [P] Update CLAUDE.md troubleshooting section with AttributeError fix at project root
- [ ] T020 [P] Verify quickstart.md validation steps work in specs/006-ollama-timeout-json-fix/quickstart.md
- [ ] T021 Add production error context to commit message
- [ ] T022 Run full test suite to verify no regressions in tests/

**Checkpoint**: Documentation complete, all fixes validated, ready for commit

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Bug Fix 1 (Phase 2)**: Depends on Setup (baseline established)
- **Bug Fix 2 (Phase 3)**: Independent of Bug Fix 1 - can run in parallel after Setup
- **Integration Testing (Phase 4)**: Depends on both Bug Fix 1 AND Bug Fix 2 completion
- **Documentation (Phase 5)**: Depends on Integration Testing passing

### Bug Fix Independence

- **Bug Fix 1 (ollama_client.py)**: Independent - different file than Bug Fix 2
- **Bug Fix 2 (prd.py)**: Independent - different file than Bug Fix 1

**Critical Path**: Setup → (Bug Fix 1 OR Bug Fix 2) → Integration Testing → Documentation

### Parallel Opportunities

**After Setup (Phase 1) completes:**
- T004-T007 (Bug Fix 1) can run in parallel with T008-T011 (Bug Fix 2)
- Both fix different files with no dependencies

**In Documentation (Phase 5):**
- T018, T019, T020 can all run in parallel (different files)

---

## Parallel Example: Both Bug Fixes Together

Since the fixes are independent and affect different files, they can be implemented in parallel:

```bash
# After completing Phase 1 (Setup), launch both fix phases together:

# Developer A or Agent A:
Task: "Search for all occurrences of READ_TIMEOUT in src/codeindex/services/ollama_client.py"
Task: "Fix line 280: Change READ_TIMEOUT to self.read_timeout in src/codeindex/services/ollama_client.py"
Task: "Verify no other undefined READ_TIMEOUT references in src/codeindex/services/ollama_client.py"
Task: "Add unit test for timeout exception logging in tests/unit/test_ollama_client.py"

# Developer B or Agent B (in parallel):
Task: "Locate validation_rules iteration in src/codeindex/cli/prd.py at lines 1657-1662"
Task: "Comment out lines 1657-1662 (validation_rules section) in src/codeindex/cli/prd.py"
Task: "Add TODO comment explaining validation_rules are IDs, future enhancement needed in src/codeindex/cli/prd.py"
Task: "Add unit test for validation_rules handling in tests/unit/test_prd.py"
```

---

## Implementation Strategy

### Sequential Execution (Single Developer)

1. **Phase 1: Setup** (5 minutes)
   - Verify environment
   - Run baseline tests
   - Record results

2. **Phase 2: Bug Fix 1** (10 minutes)
   - Search for READ_TIMEOUT references
   - Fix line 280
   - Add unit test
   - Verify fix

3. **Phase 3: Bug Fix 2** (10 minutes)
   - Locate validation_rules section
   - Comment out problematic lines
   - Add TODO
   - Add unit test

4. **Phase 4: Integration Testing** (15 minutes)
   - Run all unit tests
   - Run integration test with production data
   - Verify both fixes work together
   - Check logs for errors

5. **Phase 5: Documentation** (10 minutes)
   - Update CLAUDE.md
   - Verify quickstart
   - Prepare commit message

**Total Time**: ~50 minutes (30 minutes fixes + 20 minutes validation/docs)

### Parallel Execution (Two Developers/Agents)

1. **Phase 1: Setup** (5 minutes) - Together
2. **Phases 2 & 3: Both Bug Fixes** (10 minutes) - In parallel
3. **Phase 4: Integration Testing** (15 minutes) - Together
4. **Phase 5: Documentation** (10 minutes) - Parallel on different docs

**Total Time**: ~35 minutes (time saved by parallel fix implementation)

### MVP Approach (Bug Fix 1 Only)

If prioritizing timeout errors first:

1. Complete Phase 1 (Setup)
2. Complete Phase 2 (Bug Fix 1 - NameError)
3. Test Bug Fix 1 independently
4. **STOP and VALIDATE**: Verify timeout errors now log correctly
5. Deploy/merge if urgent
6. Later: Complete Bug Fix 2 (AttributeError) separately

---

## Success Criteria

### Before (Production Issues)

- NameError: ~15-20 timeout errors with undefined variable `READ_TIMEOUT`
- AttributeError: 1 crash blocking frontend PRD generation
- PRD generation success rate: 0% (blocked by AttributeError)

### After (Target)

- NameError: 0 (timeout value logged correctly as `self.read_timeout`)
- AttributeError: 0 (validation_rules section skipped safely)
- PRD generation success rate: 100% (completes without crashes)
- All existing tests pass (630+ unit, 42+ integration)
- Test coverage maintained or improved

---

## Testing Validation

### Unit Tests Added

1. **test_ollama_client.py**:
   - `test_ollama_timeout_logging`: Mock httpx.TimeoutException, verify log message contains correct timeout value

2. **test_prd.py**:
   - `test_prd_validation_rules_as_strings`: Create form with validation_rules as strings, verify no AttributeError

### Integration Test Validation

- Run frontend PRD generation with production extraction file
- Verify command completes (exit code 0)
- Verify no NameError in logs
- Verify no AttributeError in logs
- Verify PRD file generated with expected content

### Regression Testing

- All existing ollama_client tests pass
- All existing prd tests pass
- All integration tests pass
- No decrease in test coverage percentages

---

## Notes

- Both fixes are independent (different files)
- No architectural changes required
- Backward compatible with existing code
- No new dependencies needed
- No breaking changes to public APIs
- Fixes validated against production log samples
- Each fix can be tested independently before integration
- validation_rules fix includes TODO for future enhancement (load rules by ID)
- Commit after each phase or logical group
- Reference production log in commit message: `log_cuco-ui-admin_step2_2025-12-18_10-37-44.log`

---

## Future Enhancements (Not in This Feature)

Based on research.md, these are deferred to future features:

1. **Enhancement 1**: Load validation_rules by ID from JSON files
   - Effort: 2-3 hours
   - Benefit: Complete PRD with validation rule details
   - When: If validation rules documentation becomes important

2. **Enhancement 2**: JSON cleaning improvements
   - Effort: 3-4 hours
   - Benefit: Reduced LLM JSON parsing failures
   - When: If/when production logs show JSON parse failures (not seen in current logs)

---

**End of Tasks**
