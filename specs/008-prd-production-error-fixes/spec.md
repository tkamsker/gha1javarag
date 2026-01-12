# Feature 008: PRD Production Error Fixes

**Status:** Planning
**Priority:** P0 Critical
**Created:** 2026-01-12
**Target Completion:** 2026-01-15 (3 days)

---

## Problem Statement

A production run of the PRD generation pipeline on the cuco-ui-admin project (13,639 files) **FAILED** due to critical errors in the services PRD generation and delivered minimal output in the frontend PRD (0.35% extraction rate).

**Blockers Identified:**
1. **Services PRD Fatal Error** (P0): `AttributeError: 'TransactionInfo' object has no attribute 'isolation'`
2. **Frontend PRD Low Quality** (P1): Only 5 forms extracted from 1,380 files (99.6% miss rate)
3. **Ollama Timeout Epidemic** (P1): 11.5% timeout rate in services, 1.1% in frontend
4. **XML Parser Crashes** (P1): 2 crashes on malformed XML files

**Impact:**
- Zero backend requirements documentation generated
- Incomplete frontend requirements (missing 195+ expected forms)
- ~17 hour total runtime (unacceptable for production)
- Cannot deliver PRDs to stakeholders

**Reference:** See `docs/PRODUCTION_ERROR_ANALYSIS_2026-01-12.md` for detailed analysis.

---

## Objectives

### Primary Goals
1. **Fix blocking AttributeError** - Enable services PRD generation to complete
2. **Improve frontend extraction rate** - Achieve >10% form extraction (138+ forms)
3. **Reduce timeout failures** - Lower timeout rate from 11.5% to <2%
4. **Eliminate parser crashes** - Zero NoneType errors in XML parsing

### Secondary Goals
5. Add missing parsers (JavaScript, Properties files)
6. Fix resource leaks (socket cleanup)
7. Improve overall PRD generation performance by 30%

### Success Metrics
- **Services PRD:** Generates successfully, processes all 384 services, <2% timeouts
- **Frontend PRD:** Extracts >138 forms (10%+ rate), includes GWT components
- **Performance:** Total runtime <2 hours (down from 17 hours)
- **Reliability:** Zero crashes, zero blocking errors
- **Test Coverage:** 100% coverage of production error scenarios

---

## User Stories

### US1: Fix Services PRD Fatal Error (P0 Critical)

**As a** developer running PRD generation
**I want** the services PRD to generate without crashes
**So that** I can document backend requirements

**Acceptance Criteria:**
- [ ] TransactionInfo model has `isolation` field
- [ ] PRD generation code handles missing/null isolation gracefully
- [ ] Services PRD markdown file is generated
- [ ] Zero AttributeError failures in production run
- [ ] Unit test validates isolation field access

**Effort:** 2 story points (4 hours)
**Priority:** P0 - Blocking

**Technical Details:**
```python
# Current failing code (prd.py:1398)
if tx.isolation:  # ← AttributeError

# Required fix options:
# Option 1: Add field to model
class TransactionInfo:
    isolation: Optional[str] = None  # ← ADD THIS

# Option 2: Defensive check in PRD code
if hasattr(tx, 'isolation') and tx.isolation:
```

---

### US2: Implement Adaptive Timeout Strategy (P1 High)

**As a** pipeline operator
**I want** timeout thresholds to adapt based on file complexity
**So that** large files complete successfully without unnecessary delays

**Acceptance Criteria:**
- [ ] Timeout calculated as: `base_timeout + (lines / 100) * 10`
- [ ] Timeout range: 120s (min) to 600s (max)
- [ ] Parallel workers reduced from 10 to 5
- [ ] Fallback to structural extraction after 3 retries
- [ ] Services timeout rate <2% (down from 11.5%)
- [ ] Frontend timeout rate <1% (down from 1.1%)

**Effort:** 5 story points (10 hours)
**Priority:** P1 - High

**Technical Details:**
- Affects: `ollama_client.py`, `extraction.py`, `service_analyzer.py`, `frontend_analyzer.py`
- Algorithm:
  ```python
  def calculate_timeout(file_path: Path) -> int:
      lines = count_lines(file_path)
      base = 120  # 2 minutes
      extra = (lines / 100) * 10  # +10s per 100 lines
      return min(max(base, base + extra), 600)  # cap at 10 minutes
  ```

---

### US3: Fix XML Parser Null Safety (P1 High)

**As a** pipeline operator
**I want** XML parsing to handle malformed files gracefully
**So that** one corrupt file doesn't crash the entire pipeline

**Acceptance Criteria:**
- [ ] Null check before accessing `root.tag`
- [ ] Returns empty result on malformed XML (not crash)
- [ ] Logs warning with file path and error details
- [ ] Zero NoneType AttributeErrors
- [ ] Handles truncated files (partial XML)
- [ ] Unit tests for malformed XML edge cases

**Effort:** 2 story points (4 hours)
**Priority:** P1 - High

**Technical Details:**
```python
# Current failing code (xml_parser.py:84)
root = tree.getroot()
return {
    'root_element': self._strip_namespace(root.tag),  # ← root is None
    ...
}

# Required fix:
root = tree.getroot()
if root is None:
    logger.warning(f"Malformed XML (no root): {file_path}")
    return self._empty_result()

return {
    'root_element': self._strip_namespace(root.tag),
    ...
}
```

---

### US4: Improve Frontend Form Detection (P1 High)

**As a** requirements analyst
**I want** frontend PRD to extract most forms in the codebase
**So that** UI requirements are comprehensively documented

**Acceptance Criteria:**
- [ ] Form extraction rate >10% (138+ forms from 1,380 files)
- [ ] Includes GWT Presenters and Views (not just forms)
- [ ] Includes read-only forms (display-only UI)
- [ ] Includes HTML static forms
- [ ] "No form found" messages reduced by 90%
- [ ] Frontend PRD includes GWT Components section

**Effort:** 8 story points (16 hours)
**Priority:** P1 - High

**Technical Details:**
- Relax form detection heuristics:
  - Currently requires: `<input>`, `<button>`, or `@UiField` with specific types
  - Should include: Any `@UiField`, `<g:Label>`, display-only components
- Add GWT component extraction:
  - Extract Presenters from extraction results
  - Extract Views and UiBinder templates
  - Link Presenter → View → UiBinder chain
- Add HTML form parser:
  - Parse `<form>` tags in .html files
  - Extract input fields, labels, buttons

---

### US5: Add Missing Parsers (P2 Medium)

**As a** pipeline operator
**I want** all artifact types to have parsers
**So that** no files are skipped due to "No parser available"

**Acceptance Criteria:**
- [ ] JS_SCRIPT parser implemented (basic structure)
- [ ] PROPERTIES_FILE parser implemented (key-value extraction)
- [ ] Zero "No parser for artifact type" warnings
- [ ] JavaScript functions and variables extracted
- [ ] Properties key-value pairs indexed

**Effort:** 3 story points (6 hours)
**Priority:** P2 - Medium

**Technical Details:**
- JS_SCRIPT parser:
  - Extract function names
  - Extract variable declarations
  - Extract dependencies (imports/requires)
  - No semantic analysis (structural only)
- PROPERTIES_FILE parser:
  - Parse key=value pairs
  - Handle multi-line values
  - Extract comments

---

### US6: Fix Resource Leaks (P2 Medium)

**As a** system administrator
**I want** the pipeline to clean up resources properly
**So that** long-running jobs don't exhaust system resources

**Acceptance Criteria:**
- [ ] OllamaClient implements context manager (`__enter__`, `__exit__`)
- [ ] Sockets properly closed on normal exit
- [ ] Sockets properly closed on exception
- [ ] Zero ResourceWarning messages
- [ ] No file descriptor leaks after 1000 requests

**Effort:** 2 story points (4 hours)
**Priority:** P2 - Medium

**Technical Details:**
```python
class OllamaClient:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if hasattr(self, '_session'):
            self._session.close()
```

---

## Technical Approach

### Architecture Changes

#### 1. TransactionInfo Model Extension
```python
# src/codeindex/models/transaction_info.py
@dataclass
class TransactionInfo:
    propagation: Optional[str] = None
    isolation: Optional[str] = None  # ← NEW FIELD
    readonly: bool = False
    timeout: Optional[int] = None
```

#### 2. Adaptive Timeout System
```python
# src/codeindex/utils/timeout_calculator.py
class TimeoutCalculator:
    def __init__(self, base: int = 120, scale: int = 10, cap: int = 600):
        self.base = base
        self.scale = scale
        self.cap = cap

    def calculate(self, file_path: Path) -> int:
        lines = self._count_lines(file_path)
        extra = (lines / 100) * self.scale
        return min(max(self.base, self.base + extra), self.cap)
```

#### 3. XML Parser Defensive Coding
```python
# src/codeindex/parsers/xml_parser.py
def parse_tree(self, tree: ET.ElementTree) -> Dict[str, Any]:
    root = tree.getroot()

    # NULL SAFETY CHECK
    if root is None:
        logger.warning(f"Malformed XML: root is None")
        return self._empty_result()

    try:
        return {
            'root_element': self._strip_namespace(root.tag),
            ...
        }
    except Exception as e:
        logger.error(f"XML parse error: {e}")
        return self._empty_result()
```

#### 4. Frontend Analyzer Relaxation
```python
# src/codeindex/services/frontend_analyzer.py
def _has_form_elements(self, content: str, file_type: str) -> bool:
    # OLD: Strict check
    # return '<input' in content or '<button' in content

    # NEW: Relaxed check
    if file_type == 'gwt_ui_binder':
        # Any UiField qualifies
        return '@UiField' in content or '<g:' in content
    elif file_type == 'html':
        # Any form element
        return '<form' in content or '<input' in content
    elif file_type == 'java_source':
        # Presenter/View pattern
        return 'Presenter' in content or 'View' in content
```

---

## Implementation Plan

### Phase 1: Critical Fixes (Day 1, 8 hours)
**Goal:** Unblock services PRD generation

#### Task 1.1: Fix TransactionInfo Model (2h)
- [ ] Add `isolation` field to TransactionInfo dataclass
- [ ] Set default value: `None`
- [ ] Update model documentation
- [ ] Add unit test: `test_transaction_info_isolation_field`
- [ ] Verify services PRD generation completes

**Files:**
- `src/codeindex/models/transaction_info.py`
- `tests/unit/test_models.py`

#### Task 1.2: Fix XML Parser Null Safety (2h)
- [ ] Add null check in `parse_tree` method
- [ ] Return `_empty_result()` on null root
- [ ] Add warning log with file path
- [ ] Add unit test: `test_xml_parse_null_root`
- [ ] Add unit test: `test_xml_parse_truncated_file`

**Files:**
- `src/codeindex/parsers/xml_parser.py`
- `tests/unit/test_xml_parser.py`

#### Task 1.3: Add Defensive PRD Generation (2h)
- [ ] Add `hasattr()` check before accessing `tx.isolation`
- [ ] Add null check for other TransactionInfo fields
- [ ] Add try-except around transaction processing
- [ ] Log warning on missing fields (don't crash)

**Files:**
- `src/codeindex/cli/prd.py`

#### Task 1.4: Integration Test (2h)
- [ ] Create test with production error data
- [ ] Test services PRD with mock TransactionInfo
- [ ] Test XML parsing with ProductPortletView.ui.xml
- [ ] Verify all tests pass

**Files:**
- `tests/integration/test_production_errors.py`

**Milestone:** Services PRD generates successfully, zero crashes

---

### Phase 2: Timeout & Performance (Day 2, 10 hours)
**Goal:** Reduce timeout failures to <2%

#### Task 2.1: Implement TimeoutCalculator (3h)
- [ ] Create `timeout_calculator.py` utility
- [ ] Implement adaptive algorithm (base + lines/100 * scale)
- [ ] Add min/max caps (120s - 600s)
- [ ] Add unit tests for edge cases
- [ ] Document algorithm in docstrings

**Files:**
- `src/codeindex/utils/timeout_calculator.py`
- `tests/unit/test_timeout_calculator.py`

#### Task 2.2: Integrate Adaptive Timeouts (4h)
- [ ] Update OllamaClient to accept dynamic timeout
- [ ] Update extraction service to calculate timeout per file
- [ ] Update service_analyzer to use adaptive timeout
- [ ] Update frontend_analyzer to use adaptive timeout
- [ ] Reduce parallel workers from 10 to 5

**Files:**
- `src/codeindex/services/ollama_client.py`
- `src/codeindex/services/extraction.py`
- `src/codeindex/services/service_analyzer.py`
- `src/codeindex/services/frontend_analyzer.py`
- `src/codeindex/utils/config.py`

#### Task 2.3: Add Structural Fallback (3h)
- [ ] Implement `_extract_structural_only()` method
- [ ] Extract class names, method signatures without LLM
- [ ] Use fallback after 3 timeout retries
- [ ] Log fallback usage for monitoring

**Files:**
- `src/codeindex/services/service_analyzer.py`
- `src/codeindex/services/frontend_analyzer.py`

**Milestone:** Timeout rate <2%, average runtime reduced by 30%

---

### Phase 3: Frontend Quality (Day 3, 16 hours)
**Goal:** Achieve >10% form extraction rate

#### Task 3.1: Relax Form Detection (4h)
- [ ] Update `_has_form_elements()` to include read-only forms
- [ ] Accept any `@UiField` in GWT files (not just inputs)
- [ ] Accept `<g:Label>` and display-only widgets
- [ ] Update heuristic documentation
- [ ] Add unit tests for new detection rules

**Files:**
- `src/codeindex/services/frontend_analyzer.py`
- `tests/unit/test_frontend_analyzer.py`

#### Task 3.2: Add GWT Component Extraction (6h)
- [ ] Extract Presenters from extraction results
- [ ] Extract Views with UI field bindings
- [ ] Link Presenter → View → UiBinder
- [ ] Add GWT Components section to PRD
- [ ] Generate component table (Name, Type, UI Fields)

**Files:**
- `src/codeindex/services/frontend_analyzer.py`
- `src/codeindex/cli/prd.py`
- `tests/integration/test_gwt_component_extraction.py`

#### Task 3.3: Add HTML Form Parser (4h)
- [ ] Create `html_parser.py`
- [ ] Parse `<form>` tags
- [ ] Extract input fields (type, name, label)
- [ ] Extract buttons and their actions
- [ ] Integrate with frontend analyzer

**Files:**
- `src/codeindex/parsers/html_parser.py`
- `src/codeindex/services/frontend_analyzer.py`
- `tests/unit/test_html_parser.py`

#### Task 3.4: Validation & Testing (2h)
- [ ] Run frontend PRD on cuco-ui-admin subset
- [ ] Verify >10% extraction rate
- [ ] Verify GWT components present
- [ ] Update integration tests

**Milestone:** Frontend PRD extracts 138+ forms, includes GWT components

---

### Phase 4: Polish & Completeness (Day 4, 6 hours)
**Goal:** Add missing parsers, fix resource leaks

#### Task 4.1: JavaScript Parser (3h)
- [ ] Create `js_parser.py`
- [ ] Extract function declarations
- [ ] Extract variable declarations
- [ ] Extract dependencies (imports)
- [ ] Add unit tests

**Files:**
- `src/codeindex/parsers/js_parser.py`
- `tests/unit/test_js_parser.py`

#### Task 4.2: Properties File Parser (2h)
- [ ] Create `properties_parser.py`
- [ ] Parse key=value pairs
- [ ] Handle multi-line values
- [ ] Add unit tests

**Files:**
- `src/codeindex/parsers/properties_parser.py`
- `tests/unit/test_properties_parser.py`

#### Task 4.3: Fix Resource Leaks (1h)
- [ ] Add `__enter__` and `__exit__` to OllamaClient
- [ ] Implement `close()` method for socket cleanup
- [ ] Update usage to context manager pattern
- [ ] Verify zero ResourceWarning messages

**Files:**
- `src/codeindex/services/ollama_client.py`
- `tests/unit/test_ollama_client.py`

**Milestone:** All artifact types have parsers, zero resource warnings

---

### Phase 5: Production Validation (Day 5, 4 hours)
**Goal:** Verify fixes on full production dataset

#### Task 5.1: Full Production Run (2h)
- [ ] Run on cuco-ui-admin (13,639 files)
- [ ] Monitor timeout rates
- [ ] Monitor extraction rates
- [ ] Verify services PRD generated
- [ ] Verify frontend PRD quality

#### Task 5.2: Metrics Collection (1h)
- [ ] Document runtime (target: <2 hours)
- [ ] Document timeout rate (target: <2%)
- [ ] Document extraction rates (target: >10%)
- [ ] Document success rate (target: 100%)

#### Task 5.3: Documentation Update (1h)
- [ ] Update CLAUDE.md with new features
- [ ] Update troubleshooting guide
- [ ] Document adaptive timeout configuration
- [ ] Add production run results

**Milestone:** Production run completes successfully in <2 hours

---

## Testing Strategy

### Unit Tests (40 tests, 80% coverage target)

#### TransactionInfo Model Tests (3 tests)
- `test_transaction_info_isolation_field_exists`
- `test_transaction_info_isolation_default_none`
- `test_transaction_info_all_fields_optional`

#### XML Parser Tests (6 tests)
- `test_xml_parse_null_root`
- `test_xml_parse_truncated_file`
- `test_xml_parse_empty_file`
- `test_xml_parse_namespace_only`
- `test_xml_parse_malformed_attributes`
- `test_xml_parse_encoding_error`

#### Timeout Calculator Tests (8 tests)
- `test_timeout_small_file_returns_base`
- `test_timeout_large_file_returns_scaled`
- `test_timeout_very_large_file_capped`
- `test_timeout_zero_lines`
- `test_timeout_negative_lines`
- `test_timeout_custom_scale`
- `test_timeout_custom_cap`
- `test_timeout_file_not_found`

#### Frontend Analyzer Tests (10 tests)
- `test_form_detection_relaxed_uibinder`
- `test_form_detection_readonly_form`
- `test_form_detection_gwt_label_only`
- `test_form_detection_html_form`
- `test_gwt_component_extraction_presenter`
- `test_gwt_component_extraction_view`
- `test_gwt_component_linking`
- `test_frontend_prd_gwt_components_section`
- `test_frontend_extraction_rate_threshold`
- `test_frontend_no_form_found_reduced`

#### Parser Tests (10 tests)
- `test_js_parser_function_extraction`
- `test_js_parser_variable_extraction`
- `test_js_parser_dependency_extraction`
- `test_properties_parser_key_value`
- `test_properties_parser_multiline_value`
- `test_properties_parser_comments`

#### Resource Management Tests (3 tests)
- `test_ollama_client_context_manager`
- `test_ollama_client_socket_cleanup`
- `test_ollama_client_cleanup_on_exception`

### Integration Tests (8 tests)

#### Production Error Replay Tests (4 tests)
- `test_production_services_prd_transaction_info`
- `test_production_xml_parse_productportletview`
- `test_production_services_timeout_scenarios`
- `test_production_frontend_low_extraction`

#### End-to-End Tests (4 tests)
- `test_e2e_services_prd_generation`
- `test_e2e_frontend_prd_generation`
- `test_e2e_adaptive_timeout_behavior`
- `test_e2e_full_pipeline_cuco_ui_admin_subset`

### Performance Tests (4 tests)

#### Timeout Performance (2 tests)
- `test_perf_timeout_rate_below_2_percent`
- `test_perf_adaptive_timeout_vs_fixed`

#### Extraction Performance (2 tests)
- `test_perf_frontend_extraction_rate_above_10_percent`
- `test_perf_total_runtime_below_2_hours`

---

## Acceptance Criteria (Feature-Level)

### Functional Requirements
- [ ] Services PRD generates successfully on cuco-ui-admin
- [ ] Frontend PRD extracts >138 forms (10%+ rate)
- [ ] Zero AttributeError crashes
- [ ] Zero NoneType crashes in XML parser
- [ ] Timeout rate <2% across all phases
- [ ] All artifact types have parsers
- [ ] Resource leaks eliminated

### Performance Requirements
- [ ] Total pipeline runtime <2 hours (down from 17)
- [ ] Average file processing time <2 seconds
- [ ] Adaptive timeout overhead <5%
- [ ] Parallel worker efficiency >80%

### Quality Requirements
- [ ] Test coverage >80% for new code
- [ ] Zero regressions in existing tests
- [ ] All production error scenarios covered by tests
- [ ] Documentation updated (CLAUDE.md, troubleshooting)

### Production Readiness
- [ ] Full production run on cuco-ui-admin succeeds
- [ ] Generated PRDs meet quality standards
- [ ] Error handling is graceful (no crashes)
- [ ] Logging provides actionable diagnostics

---

## Risks and Mitigations

### Risk 1: Adaptive Timeout Complexity
**Likelihood:** Medium
**Impact:** Medium

**Risk:** Adaptive timeout algorithm may not work for all file types (XML, properties, JS) which have different complexity characteristics.

**Mitigation:**
- Use file-type-specific timeout multipliers
- Monitor timeout rates per file type in production
- Provide override configuration per file type

### Risk 2: Frontend Detection Over-Relaxation
**Likelihood:** Medium
**Impact:** Low

**Risk:** Relaxing form detection may extract non-forms (false positives), reducing PRD quality.

**Mitigation:**
- Add confidence scoring to form detection
- Filter out low-confidence forms (<0.7)
- Manual review of 10 randomly sampled forms

### Risk 3: GWT Component Extraction Incomplete
**Likelihood:** Medium
**Impact:** Medium

**Risk:** GWT component extraction from earlier extraction results may miss components if extraction was incomplete.

**Mitigation:**
- Re-run extraction phase with `--skip-ai` for structural data
- Verify extraction results have GWT metadata before PRD generation
- Fall back to file-based heuristics if extraction incomplete

### Risk 4: Performance Regression
**Likelihood:** Low
**Impact:** High

**Risk:** Adaptive timeout calculation and reduced parallelism may increase total runtime instead of decreasing it.

**Mitigation:**
- Benchmark current vs new implementation on 1000-file subset
- Use profiling to identify bottlenecks
- Maintain fast path for simple files (cached timeout calculation)

---

## Dependencies

### Internal Dependencies
- Feature 007 (GWT Navigation) - Uses GWT extraction results
- Feature 004 (Maven Dependencies) - Uses DTO extraction
- Feature 003 (Diagram Generation) - May need PRD data

### External Dependencies
- Ollama service (local LLM)
- Weaviate (vector database)
- Python 3.8+ with asyncio support

### Tool Dependencies
- pytest (testing framework)
- pytest-asyncio (async test support)
- lxml (XML parsing)
- pydantic (data validation)

---

## Rollout Plan

### Development Environment (Days 1-4)
- Implement all tasks
- Run unit and integration tests
- Fix failing tests

### Testing Environment (Day 5 morning)
- Run full production dataset (cuco-ui-admin)
- Collect metrics
- Verify success criteria

### Production Deployment (Day 5 afternoon)
- Merge to main branch
- Update documentation
- Notify stakeholders
- Monitor first production run

### Rollback Plan
If production run fails:
1. Revert to previous main branch commit
2. Re-run with old code to generate PRDs
3. Debug issues in separate branch
4. Repeat testing phase

---

## Success Metrics (Measurable)

### Before (Baseline)
- Services PRD: **FAILED** (exit code 9)
- Frontend PRD: 5 forms / 1,380 files = **0.35%**
- Timeout rate: Services **11.5%**, Frontend **1.1%**
- Total runtime: **~17 hours**
- Crashes: **2** (services PRD + XML parser)

### After (Target)
- Services PRD: **SUCCESS** (markdown generated)
- Frontend PRD: 138+ forms / 1,380 files = **>10%** (28x improvement)
- Timeout rate: **<2%** across all phases (5.75x improvement)
- Total runtime: **<2 hours** (8.5x improvement)
- Crashes: **0** (100% reliability)

### Key Performance Indicators
| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| Services PRD Success Rate | 0% | 100% | Binary (pass/fail) |
| Frontend Form Extraction Rate | 0.35% | >10% | Forms / Files analyzed |
| Services Timeout Rate | 11.5% | <2% | Timeouts / Services |
| Frontend Timeout Rate | 1.1% | <1% | Timeouts / Forms |
| Total Runtime | 17h | <2h | Wall clock time |
| Crash Count | 2 | 0 | Error log analysis |

---

## Documentation Requirements

### User Documentation
- [ ] Update CLAUDE.md with adaptive timeout configuration
- [ ] Update troubleshooting guide with new error messages
- [ ] Add performance tuning section
- [ ] Document frontend form detection heuristics

### Developer Documentation
- [ ] Add docstrings to TimeoutCalculator
- [ ] Document adaptive timeout algorithm
- [ ] Add architecture diagrams for timeout flow
- [ ] Document GWT component extraction process

### Operations Documentation
- [ ] Add monitoring guide for timeout rates
- [ ] Add runbook for common production errors
- [ ] Document resource usage expectations
- [ ] Add performance baseline metrics

---

## Open Questions

1. **Timeout Configuration:**
   - Should timeout scale factor be configurable per deployment?
   - Should we expose timeout caps as CLI parameters?

2. **Form Detection:**
   - What is the acceptable false positive rate for form detection?
   - Should we add manual review step for low-confidence forms?

3. **GWT Components:**
   - Should we re-run extraction phase or use existing results?
   - How to handle incomplete extraction data?

4. **Performance:**
   - Is 2-hour runtime target achievable with qwen2.5-coder:32b?
   - Should we recommend smaller model for production?

5. **Testing:**
   - Do we need performance regression tests in CI/CD?
   - Should we maintain production test dataset in repo?

---

## References

- **Analysis Document:** `docs/PRODUCTION_ERROR_ANALYSIS_2026-01-12.md`
- **Production Log:** `log_3production_req_gen_2026-01-08_10-08-41.log`
- **Services PRD Log:** `logs/log_cuco-ui-admin_services_prd_2026-01-08_10-08-41.log`
- **Frontend PRD Log:** `logs/log_cuco-ui-admin_frontend_prd_2026-01-08_10-08-41.log`
- **Feature 007 (GWT):** `specs/007-gwt-navigation-and-error-fixes/`
- **Feature 004 (DTOs):** `specs/004-maven-dependency-resolution/`

---

## Changelog

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| 2026-01-12 | 1.0 | Claude Code | Initial specification created from production error analysis |

---

**Next Steps:**
1. Review and approve specification
2. Create implementation plan
3. Execute Phase 1 (critical fixes)
4. Daily standup to track progress
5. Production validation on Day 5
