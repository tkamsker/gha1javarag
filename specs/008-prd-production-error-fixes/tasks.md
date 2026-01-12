# Feature 008: PRD Production Error Fixes - Task Breakdown

**Status:** Ready for Implementation
**Created:** 2026-01-12
**Sprint Duration:** 5 days (2026-01-12 to 2026-01-17)

---

## Task Dependency Graph

```
Phase 1 (Critical Fixes) - Day 1
├── T001: Fix TransactionInfo Model ← START HERE
├── T002: Fix XML Parser Null Safety
├── T003: Add Defensive PRD Generation (depends on T001)
└── T004: Integration Test Production Errors (depends on T001, T002, T003)

Phase 2 (Timeout & Performance) - Day 2
├── T005: Implement TimeoutCalculator (depends on T004)
├── T006: Integrate Adaptive Timeouts (depends on T005)
└── T007: Add Structural Fallback (depends on T006)

Phase 3 (Frontend Quality) - Day 3
├── T008: Relax Form Detection (depends on T007)
├── T009: Add GWT Component Extraction (depends on T008)
├── T010: Add HTML Form Parser (can run in parallel with T009)
└── T011: Frontend Validation & Testing (depends on T008, T009, T010)

Phase 4 (Polish & Completeness) - Day 4
├── T012: JavaScript Parser (can run in parallel)
├── T013: Properties File Parser (can run in parallel)
└── T014: Fix Resource Leaks (can run in parallel)

Phase 5 (Production Validation) - Day 5
├── T015: Full Production Run (depends on T001-T014)
├── T016: Metrics Collection (depends on T015)
└── T017: Documentation Update (depends on T016)
```

---

## Phase 1: Critical Fixes (Day 1, 8 hours)

### T001: Fix TransactionInfo Model (P0 Critical)
**Effort:** 2 hours
**Dependencies:** None
**Assignee:** TBD

**Description:**
Add `isolation` field to TransactionInfo dataclass to fix AttributeError in services PRD generation.

**Acceptance Criteria:**
- [ ] Field `isolation: Optional[str] = None` added to TransactionInfo
- [ ] Field documented in docstring (valid values: READ_UNCOMMITTED, READ_COMMITTED, REPEATABLE_READ, SERIALIZABLE)
- [ ] Default value is None (no isolation level specified)
- [ ] Unit test validates field exists and has correct type
- [ ] Unit test validates default value
- [ ] Services PRD generation uses field without crashing

**Files to Modify:**
- `src/codeindex/models/transaction_info.py` (5 lines added)
- `tests/unit/test_models.py` (20 lines added)

**Test Cases:**
```python
def test_transaction_info_isolation_field_exists():
    tx = TransactionInfo()
    assert hasattr(tx, 'isolation')

def test_transaction_info_isolation_default_none():
    tx = TransactionInfo()
    assert tx.isolation is None

def test_transaction_info_isolation_valid_values():
    tx = TransactionInfo(isolation='READ_COMMITTED')
    assert tx.isolation == 'READ_COMMITTED'
```

**Verification:**
```bash
# Run unit tests
pytest tests/unit/test_models.py::test_transaction_info -v

# Verify model can be instantiated
python -c "from codeindex.models.transaction_info import TransactionInfo; tx = TransactionInfo(isolation='READ_COMMITTED'); print(tx)"
```

---

### T002: Fix XML Parser Null Safety (P1 High)
**Effort:** 2 hours
**Dependencies:** None
**Assignee:** TBD

**Description:**
Add null check before accessing root.tag to prevent AttributeError on malformed XML files.

**Acceptance Criteria:**
- [ ] Null check added: `if root is None: return self._empty_result()`
- [ ] Warning logged with file path when root is None
- [ ] `_empty_result()` method returns dict with empty values
- [ ] Unit test for null root scenario
- [ ] Unit test for truncated XML file
- [ ] Unit test for file with only namespace declaration
- [ ] Zero AttributeError crashes on malformed XML

**Files to Modify:**
- `src/codeindex/parsers/xml_parser.py` (10 lines added)
- `tests/unit/test_xml_parser.py` (60 lines added)

**Implementation:**
```python
def parse_tree(self, tree: ET.ElementTree) -> Dict[str, Any]:
    """Parse XML tree with null safety."""
    root = tree.getroot()

    # NULL SAFETY CHECK
    if root is None:
        logger.warning(
            f"Malformed XML file: root element is None. "
            f"File may be truncated or have only namespace declarations."
        )
        return self._empty_result()

    try:
        return {
            'root_element': self._strip_namespace(root.tag),
            'attributes': dict(root.attrib),
            'children': [self._strip_namespace(child.tag) for child in root],
            'namespaces': dict(root.nsmap) if hasattr(root, 'nsmap') else {},
        }
    except Exception as e:
        logger.error(f"Error parsing XML tree: {e}")
        return self._empty_result()

def _empty_result(self) -> Dict[str, Any]:
    """Return empty result for malformed XML."""
    return {
        'root_element': None,
        'attributes': {},
        'children': [],
        'namespaces': {},
    }
```

**Test Cases:**
```python
def test_xml_parse_null_root():
    # Simulate malformed XML with no root
    xml_content = '<?xml version="1.0"?>\n'
    result = parser.parse_string(xml_content)
    assert result['root_element'] is None
    assert result['children'] == []

def test_xml_parse_truncated_file():
    # Simulate truncated XML (ProductPortletView.ui.xml)
    xml_content = '''<?xml version="1.0"?>
    <ui:UiBinder xmlns:ui="urn:ui">
        <g:VerticalPanel>
            <g:Label text="Test'''  # ← truncated
    result = parser.parse_file(xml_content)
    assert result is not None  # Should not crash
```

**Verification:**
```bash
# Run unit tests
pytest tests/unit/test_xml_parser.py::test_xml_parse_null_root -v
pytest tests/unit/test_xml_parser.py::test_xml_parse_truncated_file -v

# Test with actual malformed file
codeindex extract --inventory test_data/malformed_xml.jsonl
```

---

### T003: Add Defensive PRD Generation (P0 Critical)
**Effort:** 2 hours
**Dependencies:** T001
**Assignee:** TBD

**Description:**
Add hasattr() checks and null safety before accessing TransactionInfo fields in PRD generation code.

**Acceptance Criteria:**
- [ ] `hasattr(tx, 'isolation')` check before accessing isolation
- [ ] Null check: `if tx.isolation is not None`
- [ ] Default value handling for missing fields
- [ ] Try-except around transaction processing block
- [ ] Warning logged when fields are missing (don't crash)
- [ ] Services PRD section handles incomplete transaction info gracefully

**Files to Modify:**
- `src/codeindex/cli/prd.py` (15 lines modified)

**Implementation:**
```python
# BEFORE (Line 1398 - CRASHES)
if tx.isolation:
    tx_details.append(f"Isolation: {tx.isolation}")

# AFTER (Line 1398 - SAFE)
try:
    if hasattr(tx, 'isolation') and tx.isolation is not None:
        tx_details.append(f"Isolation: {tx.isolation}")

    if hasattr(tx, 'propagation') and tx.propagation is not None:
        tx_details.append(f"Propagation: {tx.propagation}")

    if hasattr(tx, 'readonly') and tx.readonly:
        tx_details.append(f"Read-only: {tx.readonly}")

    if hasattr(tx, 'timeout') and tx.timeout is not None:
        tx_details.append(f"Timeout: {tx.timeout}s")

except AttributeError as e:
    logger.warning(f"Incomplete transaction info: {e}")
    tx_details.append("Transaction details unavailable")
```

**Test Cases:**
```python
def test_prd_transaction_info_missing_isolation():
    # Create TransactionInfo without isolation field
    tx = type('TransactionInfo', (), {'propagation': 'REQUIRED'})()
    result = _generate_service_prd([...], [...])
    assert 'AttributeError' not in result  # Should not crash

def test_prd_transaction_info_null_isolation():
    tx = TransactionInfo(isolation=None)
    result = _generate_service_prd([...], [...])
    assert 'Isolation' not in result  # Should skip null values
```

**Verification:**
```bash
# Run services PRD generation with incomplete transaction info
codeindex prd services --project cuco-ui-admin --output test_output/

# Check for crashes
echo $?  # Should be 0 (success)
```

---

### T004: Integration Test Production Errors (P1 High)
**Effort:** 2 hours
**Dependencies:** T001, T002, T003
**Assignee:** TBD

**Description:**
Create integration tests that replay production error scenarios to ensure fixes work end-to-end.

**Acceptance Criteria:**
- [ ] Test case for TransactionInfo AttributeError scenario
- [ ] Test case for XML parser NoneType scenario (ProductPortletView.ui.xml)
- [ ] Test case for services timeout scenario
- [ ] Test case for frontend low extraction rate
- [ ] All tests pass with new code
- [ ] All tests fail with old code (verify test validity)

**Files to Create:**
- `tests/integration/test_production_errors.py` (200 lines)
- `tests/fixtures/production_errors/` (test data directory)

**Test Cases:**
```python
def test_production_services_prd_transaction_info():
    """Replay: Services PRD crashes on tx.isolation access."""
    # Setup: Create mock service with TransactionInfo
    service = create_mock_service_with_transaction()

    # Execute: Generate services PRD
    result = generate_services_prd([service])

    # Verify: No crashes, PRD contains transaction section
    assert 'AttributeError' not in str(result)
    assert result is not None

def test_production_xml_parse_productportletview():
    """Replay: XML parser crashes on malformed ProductPortletView.ui.xml."""
    # Setup: Use actual malformed file from production
    xml_path = 'tests/fixtures/production_errors/ProductPortletView.ui.xml'

    # Execute: Parse XML
    parser = XmlParser()
    result = parser.parse_file(xml_path)

    # Verify: No crashes, returns empty result
    assert result is not None
    assert result['root_element'] is None or result['root_element'] == ''

def test_production_services_timeout_scenarios():
    """Replay: Services timeout on SolrPartyRepository.java."""
    # Setup: Mock Ollama client with 240s timeout
    with mock.patch('ollama_client.request', side_effect=TimeoutError):
        # Execute: Extract service with retries
        result = extract_service_with_llm('SolrPartyRepository.java')

        # Verify: Falls back to structural extraction
        assert result is not None
        assert result['extraction_method'] == 'structural_fallback'

def test_production_frontend_low_extraction():
    """Verify: Frontend extraction rate >10% after fixes."""
    # Setup: Use cuco-ui-admin subset (100 files)
    frontend_files = load_frontend_files('tests/fixtures/production_errors/frontend_subset.jsonl')

    # Execute: Run frontend analyzer
    analyzer = FrontendAnalyzer()
    results = analyzer.analyze_files(frontend_files)

    # Verify: Extraction rate >10%
    forms_extracted = len([r for r in results if r['has_form']])
    extraction_rate = forms_extracted / len(frontend_files)
    assert extraction_rate > 0.10, f"Extraction rate {extraction_rate:.1%} below 10% threshold"
```

**Verification:**
```bash
# Run all production error integration tests
pytest tests/integration/test_production_errors.py -v

# Expected: 4/4 passing
```

---

## Phase 2: Timeout & Performance (Day 2, 10 hours)

### T005: Implement TimeoutCalculator (P1 High)
**Effort:** 3 hours
**Dependencies:** T004
**Assignee:** TBD

**Description:**
Create utility class to calculate adaptive timeouts based on file size and complexity.

**Acceptance Criteria:**
- [ ] TimeoutCalculator class created with configurable parameters
- [ ] Algorithm: `timeout = base + (lines / 100) * scale`
- [ ] Min/max caps enforced (120s - 600s)
- [ ] Handles edge cases (empty files, missing files, huge files)
- [ ] Unit tests for all edge cases (8 tests)
- [ ] Documentation in docstrings with examples

**Files to Create:**
- `src/codeindex/utils/timeout_calculator.py` (100 lines)
- `tests/unit/test_timeout_calculator.py` (150 lines)

**Implementation:**
```python
class TimeoutCalculator:
    """
    Calculate adaptive timeouts based on file complexity.

    Algorithm:
        timeout = base + (lines / 100) * scale
        timeout = max(min_timeout, min(timeout, max_timeout))

    Examples:
        >>> calc = TimeoutCalculator(base=120, scale=10)
        >>> calc.calculate_for_file('small.java')  # 100 lines
        130  # 120 + (100/100)*10
        >>> calc.calculate_for_file('large.java')  # 5000 lines
        600  # capped at max_timeout
    """

    def __init__(
        self,
        base: int = 120,
        scale: int = 10,
        min_timeout: int = 60,
        max_timeout: int = 600,
    ):
        self.base = base
        self.scale = scale
        self.min_timeout = min_timeout
        self.max_timeout = max_timeout

    def calculate_for_file(self, file_path: Path) -> int:
        """Calculate timeout for given file."""
        try:
            lines = self._count_lines(file_path)
            return self.calculate_for_lines(lines)
        except FileNotFoundError:
            logger.warning(f"File not found: {file_path}, using base timeout")
            return self.base
        except Exception as e:
            logger.error(f"Error calculating timeout: {e}")
            return self.base

    def calculate_for_lines(self, lines: int) -> int:
        """Calculate timeout for given line count."""
        if lines < 0:
            lines = 0

        extra = (lines / 100) * self.scale
        timeout = self.base + extra
        timeout = max(self.min_timeout, min(timeout, self.max_timeout))
        return int(timeout)

    def _count_lines(self, file_path: Path) -> int:
        """Count non-empty lines in file."""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for line in f if line.strip())
```

**Test Cases:**
```python
def test_timeout_small_file_returns_base():
    calc = TimeoutCalculator(base=120, scale=10)
    assert calc.calculate_for_lines(0) == 120
    assert calc.calculate_for_lines(50) == 125  # 120 + (50/100)*10

def test_timeout_large_file_returns_scaled():
    calc = TimeoutCalculator(base=120, scale=10)
    assert calc.calculate_for_lines(1000) == 220  # 120 + (1000/100)*10

def test_timeout_very_large_file_capped():
    calc = TimeoutCalculator(base=120, scale=10, max_timeout=600)
    assert calc.calculate_for_lines(10000) == 600  # capped

def test_timeout_zero_lines():
    calc = TimeoutCalculator()
    assert calc.calculate_for_lines(0) == calc.base

def test_timeout_negative_lines():
    calc = TimeoutCalculator()
    assert calc.calculate_for_lines(-100) == calc.base

def test_timeout_custom_scale():
    calc = TimeoutCalculator(base=100, scale=20)
    assert calc.calculate_for_lines(100) == 120  # 100 + (100/100)*20

def test_timeout_custom_cap():
    calc = TimeoutCalculator(base=100, scale=10, max_timeout=300)
    assert calc.calculate_for_lines(5000) == 300  # capped at 300

def test_timeout_file_not_found():
    calc = TimeoutCalculator()
    result = calc.calculate_for_file(Path('/nonexistent/file.java'))
    assert result == calc.base  # fallback to base
```

---

### T006: Integrate Adaptive Timeouts (P1 High)
**Effort:** 4 hours
**Dependencies:** T005
**Assignee:** TBD

**Description:**
Integrate TimeoutCalculator into extraction pipeline, service analyzer, and frontend analyzer.

**Acceptance Criteria:**
- [ ] OllamaClient accepts dynamic timeout parameter
- [ ] Extraction service calculates timeout per file
- [ ] Service analyzer uses adaptive timeout
- [ ] Frontend analyzer uses adaptive timeout
- [ ] Parallel workers reduced from 10 to 5
- [ ] Configuration allows override of timeout parameters
- [ ] Metrics logged for timeout decisions

**Files to Modify:**
- `src/codeindex/services/ollama_client.py` (20 lines modified)
- `src/codeindex/services/extraction.py` (30 lines modified)
- `src/codeindex/services/service_analyzer.py` (25 lines modified)
- `src/codeindex/services/frontend_analyzer.py` (25 lines modified)
- `src/codeindex/utils/config.py` (10 lines added)

**Implementation:**
```python
# ollama_client.py
def generate(self, prompt: str, timeout: Optional[int] = None) -> str:
    """Generate completion with dynamic timeout."""
    if timeout is None:
        timeout = self.read_timeout  # use default

    response = requests.post(
        f"{self.url}/api/generate",
        json={...},
        timeout=(self.connect_timeout, timeout),  # use dynamic timeout
    )
    return response.json()['response']

# extraction.py
def extract_file(self, file_path: Path) -> Dict[str, Any]:
    """Extract file with adaptive timeout."""
    timeout_calc = TimeoutCalculator()
    timeout = timeout_calc.calculate_for_file(file_path)

    logger.debug(f"Calculated timeout for {file_path.name}: {timeout}s")

    return self.ollama_client.generate(
        prompt=self._build_prompt(file_path),
        timeout=timeout,
    )

# config.py
ADAPTIVE_TIMEOUT_ENABLED: bool = True
TIMEOUT_BASE: int = 120
TIMEOUT_SCALE: int = 10
TIMEOUT_MIN: int = 60
TIMEOUT_MAX: int = 600
MAX_CONCURRENT_AI_CALLS: int = 5  # reduced from 10
```

**Verification:**
```bash
# Run extraction with adaptive timeouts enabled
codeindex extract --inventory discovery.jsonl --adaptive-timeout

# Check logs for timeout calculations
grep "Calculated timeout" extraction.log | head -10

# Verify timeout varies by file size
# Expected: Small files ~120s, large files ~600s
```

---

### T007: Add Structural Fallback (P1 High)
**Effort:** 3 hours
**Dependencies:** T006
**Assignee:** TBD

**Description:**
Implement fallback to structural-only extraction when LLM analysis times out after 3 retries.

**Acceptance Criteria:**
- [ ] `_extract_structural_only()` method extracts basic structure without LLM
- [ ] Extracts: class names, method signatures, field definitions, imports
- [ ] Triggered automatically after 3 timeout retries
- [ ] Logs fallback usage with file path and reason
- [ ] Result marked with `extraction_method: "structural_fallback"`
- [ ] Integration test verifies fallback behavior

**Files to Modify:**
- `src/codeindex/services/service_analyzer.py` (50 lines added)
- `src/codeindex/services/frontend_analyzer.py` (50 lines added)
- `tests/integration/test_timeout_fallback.py` (100 lines added)

**Implementation:**
```python
def _extract_service_with_llm(self, file_path: Path) -> Optional[Dict[str, Any]]:
    """Extract service with LLM, fallback to structural on timeout."""
    try:
        # Attempt LLM extraction with retries
        return self._call_llm_with_retries(file_path, retries=3)
    except TimeoutError as e:
        logger.warning(
            f"LLM extraction timed out after 3 retries: {file_path}. "
            f"Falling back to structural extraction."
        )
        return self._extract_structural_only(file_path)

def _extract_structural_only(self, file_path: Path) -> Dict[str, Any]:
    """
    Extract basic structure without LLM analysis.

    Extracts:
    - Class names and inheritance
    - Method signatures (name, params, return type)
    - Field definitions (name, type, modifiers)
    - Import statements
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Use regex/AST to extract structure
    classes = self._extract_classes(content)
    methods = self._extract_methods(content)
    fields = self._extract_fields(content)
    imports = self._extract_imports(content)

    return {
        'file_path': str(file_path),
        'extraction_method': 'structural_fallback',
        'classes': classes,
        'methods': methods,
        'fields': fields,
        'imports': imports,
        'semantic_analysis': None,  # Not available without LLM
    }
```

**Test Cases:**
```python
def test_fallback_triggered_after_3_timeouts():
    """Verify structural fallback after 3 LLM timeouts."""
    # Mock Ollama to always timeout
    with mock.patch('ollama_client.generate', side_effect=TimeoutError):
        analyzer = ServiceAnalyzer()
        result = analyzer.extract_service('TestService.java')

        # Verify fallback was used
        assert result is not None
        assert result['extraction_method'] == 'structural_fallback'
        assert 'classes' in result
        assert result['semantic_analysis'] is None
```

---

## Phase 3: Frontend Quality (Day 3, 16 hours)

### T008: Relax Form Detection (P1 High)
**Effort:** 4 hours
**Dependencies:** T007
**Assignee:** TBD

**Description:**
Update form detection heuristics to include read-only forms, display-only components, and GWT widgets.

**Acceptance Criteria:**
- [ ] Accepts any `@UiField` annotation (not just input types)
- [ ] Accepts `<g:Label>` and display-only widgets
- [ ] Accepts forms without submit buttons (read-only forms)
- [ ] Accepts HTML `<form>` tags with any input types
- [ ] "No form found" messages reduced by 90%
- [ ] False positive rate <20% (manual review of 20 samples)

**Files to Modify:**
- `src/codeindex/services/frontend_analyzer.py` (50 lines modified)
- `tests/unit/test_frontend_analyzer.py` (80 lines added)

**Implementation:**
```python
def _has_form_elements(self, content: str, file_path: Path) -> bool:
    """
    Detect form elements with relaxed heuristics.

    OLD: Only <input>, <button>, @UiField with input types
    NEW: Any @UiField, <g:*> widgets, <form>, display components
    """
    file_type = self._get_file_type(file_path)

    if file_type == 'gwt_ui_binder':
        # Any GWT widget qualifies
        has_ui_field = '@UiField' in content
        has_gwt_widget = '<g:' in content or '<ui:' in content
        return has_ui_field or has_gwt_widget

    elif file_type == 'html':
        # Any form or input element
        has_form = '<form' in content.lower()
        has_input = '<input' in content.lower()
        has_button = '<button' in content.lower()
        return has_form or has_input or has_button

    elif file_type == 'java_source':
        # Presenter or View pattern
        is_presenter = 'Presenter' in content and '@UiField' in content
        is_view = 'View' in content and 'implements' in content
        return is_presenter or is_view

    return False  # Unknown file type
```

**Test Cases:**
```python
def test_form_detection_relaxed_uibinder():
    content = '''
    <ui:UiBinder>
        <g:VerticalPanel>
            <g:Label ui:field="nameLabel" text="Name:"/>
        </g:VerticalPanel>
    </ui:UiBinder>
    '''
    assert analyzer._has_form_elements(content, Path('test.ui.xml'))

def test_form_detection_readonly_form():
    content = '''
    <form>
        <div class="field">
            <span class="label">Name:</span>
            <span class="value">John Doe</span>
        </div>
    </form>
    '''
    assert analyzer._has_form_elements(content, Path('test.html'))

def test_form_detection_gwt_label_only():
    content = '''
    @UiField Label statusLabel;
    @UiField Label messageLabel;
    '''
    assert analyzer._has_form_elements(content, Path('TestView.java'))
```

---

### T009: Add GWT Component Extraction (P1 High)
**Effort:** 6 hours
**Dependencies:** T008
**Assignee:** TBD

**Description:**
Extract GWT Presenters, Views, and UiBinder templates from extraction results and include in frontend PRD.

**Acceptance Criteria:**
- [ ] Extracts Presenters from extraction results (gwt_role: "presenter")
- [ ] Extracts Views with UI field bindings
- [ ] Links Presenter → View → UiBinder chain
- [ ] Generates GWT Components section in PRD
- [ ] Component table includes: Name, Type, UI Fields, Navigation Targets
- [ ] At least 50 GWT components extracted from cuco-ui-admin

**Files to Modify:**
- `src/codeindex/services/frontend_analyzer.py` (100 lines added)
- `src/codeindex/cli/prd.py` (80 lines added)
- `tests/integration/test_gwt_component_extraction.py` (120 lines added)

**Implementation:**
```python
def extract_gwt_components(self, extraction_file: Path) -> List[Dict[str, Any]]:
    """
    Extract GWT components from extraction results.

    Returns list of components with:
    - name: Component name (e.g., "UserPresenter")
    - type: Component type ("presenter", "view", "uibinder")
    - ui_fields: List of UI field bindings
    - event_handlers: List of event handlers (Presenters only)
    - navigation_targets: List of navigation targets (Presenters only)
    - view_class: Linked View class (Presenters only)
    - template_file: Linked UiBinder template (Views only)
    """
    components = []

    # Read extraction results
    with open(extraction_file, 'r') as f:
        for line in f:
            artifact = json.loads(line)

            if artifact.get('gwt_role') == 'presenter':
                components.append(self._extract_presenter_component(artifact))

            elif artifact.get('gwt_role') == 'view':
                components.append(self._extract_view_component(artifact))

            elif artifact.get('artifact_type') == 'gwt_ui_binder':
                components.append(self._extract_uibinder_component(artifact))

    # Link Presenter → View → UiBinder
    components = self._link_gwt_components(components)

    return components
```

**PRD Template Addition:**
```markdown
## GWT Application Components

### Component Overview

| Component | Type | UI Fields | Event Handlers | Navigation Targets |
|-----------|------|-----------|----------------|-------------------|
| UserPresenter | Presenter | 5 | 3 | UserPlace, DashboardPlace |
| UserView | View | 5 | - | - |
| UserView.ui.xml | UiBinder | 5 widgets | - | - |
...

### Presenter Details

#### UserPresenter
- **Type:** Presenter (MVP pattern)
- **View Binding:** UserView
- **Template:** UserView.ui.xml
- **Event Handlers:**
  - onSaveButtonClick → saveUser()
  - onCancelButtonClick → cancelEdit()
  - onNameFieldChange → validateName()
- **RPC Calls:**
  - UserService.getUser()
  - UserService.saveUser()
- **Navigation Targets:**
  - UserPlace (on save success)
  - DashboardPlace (on cancel)
```

---

### T010: Add HTML Form Parser (P2 Medium)
**Effort:** 4 hours
**Dependencies:** None (can run in parallel with T009)
**Assignee:** TBD

**Description:**
Create parser for static HTML forms (Kundennotizen.html, Kundensuche.html, etc.).

**Acceptance Criteria:**
- [ ] Parses `<form>` tags in HTML files
- [ ] Extracts input fields (type, name, id, value, placeholder)
- [ ] Extracts field labels (inferred from adjacent text or `<label>` tags)
- [ ] Extracts buttons (type, name, onclick)
- [ ] Handles multi-page forms (form wizard pattern)
- [ ] Unit tests for various HTML form structures

**Files to Create:**
- `src/codeindex/parsers/html_parser.py` (150 lines)
- `tests/unit/test_html_parser.py` (120 lines)

**Implementation:**
```python
class HtmlFormParser:
    """
    Parse HTML forms and extract structure.

    Supports:
    - Standard HTML forms (<form>, <input>, <button>)
    - Field label detection (adjacent text, <label> tags)
    - Multi-page forms (fieldset, form wizard)
    """

    def parse_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse HTML file and extract forms."""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')
        forms = []

        for form in soup.find_all('form'):
            forms.append(self._extract_form(form))

        return {
            'file_path': str(file_path),
            'forms': forms,
            'form_count': len(forms),
        }

    def _extract_form(self, form_element) -> Dict[str, Any]:
        """Extract structure from form element."""
        fields = []

        for input_elem in form_element.find_all(['input', 'select', 'textarea']):
            field = {
                'name': input_elem.get('name'),
                'type': input_elem.get('type', 'text'),
                'id': input_elem.get('id'),
                'placeholder': input_elem.get('placeholder'),
                'label': self._find_label(input_elem),
            }
            fields.append(field)

        buttons = []
        for button in form_element.find_all(['button', 'input']):
            if button.get('type') in ['submit', 'button', 'reset']:
                buttons.append({
                    'text': button.get_text() or button.get('value'),
                    'type': button.get('type'),
                    'onclick': button.get('onclick'),
                })

        return {
            'id': form_element.get('id'),
            'action': form_element.get('action'),
            'method': form_element.get('method', 'GET'),
            'fields': fields,
            'buttons': buttons,
        }

    def _find_label(self, input_elem) -> Optional[str]:
        """Find label for input element."""
        # Try <label> tag
        input_id = input_elem.get('id')
        if input_id:
            label = input_elem.find_previous('label', {'for': input_id})
            if label:
                return label.get_text().strip()

        # Try adjacent text
        previous_text = input_elem.find_previous(string=True)
        if previous_text:
            return previous_text.strip()

        return None
```

---

### T011: Frontend Validation & Testing (P1 High)
**Effort:** 2 hours
**Dependencies:** T008, T009, T010
**Assignee:** TBD

**Description:**
Run frontend PRD generation on cuco-ui-admin subset and validate extraction rate meets targets.

**Acceptance Criteria:**
- [ ] Frontend PRD generates on 100-file subset
- [ ] Extraction rate >10% (>10 forms)
- [ ] GWT components section present
- [ ] "No form found" messages <50% of files
- [ ] Integration test validates extraction rate threshold

**Test Implementation:**
```python
def test_frontend_extraction_rate_threshold():
    """Validate frontend extraction rate >10% on production data."""
    # Load cuco-ui-admin frontend files (100-file subset)
    frontend_files = load_test_data('cuco-ui-admin-frontend-100.jsonl')

    # Run frontend analyzer
    analyzer = FrontendAnalyzer()
    results = analyzer.analyze_files(frontend_files)

    # Count successful extractions
    forms_extracted = len([r for r in results if r.get('has_form')])
    extraction_rate = forms_extracted / len(frontend_files)

    # Assert: Rate >10%
    assert extraction_rate > 0.10, (
        f"Frontend extraction rate {extraction_rate:.1%} below 10% threshold. "
        f"Extracted {forms_extracted} forms from {len(frontend_files)} files."
    )

    # Assert: GWT components present
    gwt_components = [r for r in results if r.get('gwt_component_type')]
    assert len(gwt_components) > 0, "No GWT components extracted"
```

---

## Phase 4: Polish & Completeness (Day 4, 6 hours)

### T012: JavaScript Parser (P2 Medium)
**Effort:** 3 hours
**Dependencies:** None
**Assignee:** TBD

**Description:**
Create parser for JavaScript files to extract functions, variables, and dependencies.

**Acceptance Criteria:**
- [ ] Extracts function declarations (name, params)
- [ ] Extracts variable declarations (var, let, const)
- [ ] Extracts dependencies (import, require, script tags)
- [ ] Handles ES5 and ES6 syntax
- [ ] Unit tests for common JS patterns

**Files to Create:**
- `src/codeindex/parsers/js_parser.py` (150 lines)
- `tests/unit/test_js_parser.py` (100 lines)

---

### T013: Properties File Parser (P2 Medium)
**Effort:** 2 hours
**Dependencies:** None
**Assignee:** TBD

**Description:**
Create parser for Java .properties files to extract configuration key-value pairs.

**Acceptance Criteria:**
- [ ] Parses key=value pairs
- [ ] Handles multi-line values (backslash continuation)
- [ ] Extracts comments
- [ ] Handles Unicode escapes
- [ ] Unit tests for edge cases

**Files to Create:**
- `src/codeindex/parsers/properties_parser.py` (100 lines)
- `tests/unit/test_properties_parser.py` (80 lines)

---

### T014: Fix Resource Leaks (P2 Medium)
**Effort:** 1 hour
**Dependencies:** None
**Assignee:** TBD

**Description:**
Add context manager to OllamaClient for proper socket cleanup.

**Acceptance Criteria:**
- [ ] `__enter__` and `__exit__` methods implemented
- [ ] `close()` method closes underlying socket/session
- [ ] Usage updated to `with OllamaClient() as client:`
- [ ] Zero ResourceWarning messages after usage
- [ ] Unit test verifies cleanup on exception

**Files to Modify:**
- `src/codeindex/services/ollama_client.py` (20 lines)
- `tests/unit/test_ollama_client.py` (30 lines)

---

## Phase 5: Production Validation (Day 5, 4 hours)

### T015: Full Production Run (P0 Critical)
**Effort:** 2 hours
**Dependencies:** T001-T014
**Assignee:** TBD

**Description:**
Run full PRD generation pipeline on cuco-ui-admin (13,639 files) and verify all fixes work in production.

**Acceptance Criteria:**
- [ ] Discovery completes (13,639 files)
- [ ] Extraction completes with <2% timeouts
- [ ] Indexing completes
- [ ] Services PRD generates successfully
- [ ] Frontend PRD generates with >10% extraction rate
- [ ] Total runtime <2 hours
- [ ] Zero blocking errors

**Verification Script:**
```bash
#!/bin/bash
# production_validation.sh

PROJECT="cuco-ui-admin"
SOURCE="/mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-admin"

echo "Starting production validation run..."
START_TIME=$(date +%s)

# Run pipeline
./run.sh "$PROJECT" "$SOURCE"

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
HOURS=$((DURATION / 3600))
MINUTES=$(((DURATION % 3600) / 60))

echo "Pipeline completed in ${HOURS}h ${MINUTES}m"

# Validate results
python3 << EOF
import json

# Check services PRD
services_prd = "output/${PROJECT}/prd/services_prd.md"
assert Path(services_prd).exists(), "Services PRD not generated"

# Check frontend PRD
frontend_prd = "output/${PROJECT}/prd/frontend_prd.md"
assert Path(frontend_prd).exists(), "Frontend PRD not generated"

# Check extraction rate
with open("output/${PROJECT}/extraction-results.jsonl") as f:
    total = sum(1 for _ in f)

print(f"Extraction results: {total} files")
print(f"Duration: ${HOURS}h ${MINUTES}m")
print("✓ All validations passed")
EOF
```

---

### T016: Metrics Collection (P1 High)
**Effort:** 1 hour
**Dependencies:** T015
**Assignee:** TBD

**Description:**
Collect and document performance metrics from production run.

**Acceptance Criteria:**
- [ ] Total runtime documented (target: <2 hours)
- [ ] Timeout rate documented (target: <2%)
- [ ] Frontend extraction rate documented (target: >10%)
- [ ] Services extracted count
- [ ] Forms extracted count
- [ ] GWT components extracted count
- [ ] Comparison table (before vs after)

**Metrics Template:**
```markdown
# Production Run Metrics - Feature 008 Validation

**Date:** 2026-01-17
**Project:** cuco-ui-admin (13,639 files)

## Performance Metrics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Total Runtime | 17h | 1h 45m | 9.7x faster |
| Services PRD Success | 0% | 100% | ✓ Fixed |
| Frontend Extraction Rate | 0.35% | 12.3% | 35x better |
| Services Timeout Rate | 11.5% | 1.8% | 6.4x better |
| Frontend Timeout Rate | 1.1% | 0.5% | 2.2x better |
| Crashes | 2 | 0 | ✓ Fixed |

## Extraction Results

- **Services:** 384 extracted (100%)
- **Forms:** 170 extracted (12.3%)
- **GWT Components:** 62 extracted
- **Presenters:** 28
- **Views:** 26
- **UiBinder:** 34

## Success Criteria

- [x] Services PRD generated successfully
- [x] Frontend extraction rate >10%
- [x] Timeout rate <2%
- [x] Total runtime <2 hours
- [x] Zero blocking errors
```

---

### T017: Documentation Update (P2 Medium)
**Effort:** 1 hour
**Dependencies:** T016
**Assignee:** TBD

**Description:**
Update project documentation with new features and production results.

**Acceptance Criteria:**
- [ ] CLAUDE.md updated with adaptive timeout configuration
- [ ] Troubleshooting guide updated with new error scenarios
- [ ] Performance tuning section added
- [ ] Production validation results added
- [ ] Changelog updated

**Files to Modify:**
- `CLAUDE.md` (50 lines added)
- `docs/TROUBLESHOOTING.md` (80 lines added)
- `CHANGELOG.md` (30 lines added)

---

## Summary

**Total Tasks:** 17
**Total Effort:** 44 hours (5.5 days)
**Critical Path:** T001 → T003 → T004 → T005 → T006 → T007 → T008 → T009 → T011 → T015 → T016 → T017

**Parallel Opportunities:**
- Phase 4 tasks (T012, T013, T014) can run in parallel
- T010 (HTML Parser) can run in parallel with T009 (GWT Components)

**Checkpoints:**
- End of Day 1: T001-T004 complete (services PRD unblocked)
- End of Day 2: T005-T007 complete (timeouts reduced)
- End of Day 3: T008-T011 complete (frontend quality improved)
- End of Day 4: T012-T014 complete (polish complete)
- End of Day 5: T015-T017 complete (production validated)

**Next Steps:**
1. Review and approve task breakdown
2. Assign tasks to developers
3. Set up daily standups
4. Begin Phase 1 implementation
