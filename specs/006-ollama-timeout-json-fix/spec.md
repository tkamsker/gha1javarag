# Feature 006: Ollama Timeout and JSON Parsing Fix

## Overview

Fix production issues with PRD generation pipeline where Ollama requests timeout at 60 seconds and LLM-generated JSON responses are frequently malformed, causing extraction failures.

## Problem Statement

The production `step2.sh` (PRD generation) is experiencing high failure rates analyzing DAO files:

**Observed Issues:**
- **Ollama timeouts**: Frequent timeout errors after 60 seconds on complex DAO analysis
- **Invalid JSON responses**: LLM generating malformed JSON with delimiter errors, unterminated strings
- **Missing required fields**: Entity extraction failing due to missing `entity_name`, `columns`, `description`
- **High failure rate**: 27+ failed out of 76 DAO files (35%+ failure rate)

**Root Causes:**
1. **Hardcoded timeout**: `ollama_client.py` has `READ_TIMEOUT = 60.0` seconds (line 31), ignoring config
2. **Config timeout unused**: `config.ollama_timeout` (240s default) exists but never passed to OllamaClient
3. **No JSON validation**: Direct `json.loads()` without validation or error recovery
4. **LLM output quality**: gemma3:12b model frequently generates invalid JSON

## Requirements

### Functional Requirements

**FR1: Configurable Ollama Timeout**
- OllamaClient must accept timeout as constructor parameter
- Default to config.ollama_timeout (240 seconds)
- Support override via environment variable `OLLAMA_TIMEOUT`
- Backward compatible with existing code

**FR2: Robust JSON Parsing**
- Pre-validate LLM JSON responses before parsing
- Strip markdown code fences if present (```json...```)
- Clean common JSON errors (trailing commas, unescaped quotes)
- Provide detailed error messages including malformed JSON snippet
- Graceful fallback on parse failures

**FR3: Improved Error Handling**
- Log malformed JSON responses for debugging (first 500 chars)
- Include file context in error messages
- Track and report JSON parsing failure metrics
- Continue processing other files on individual failures

### Non-Functional Requirements

**NFR1: Performance**
- Timeout increase should not impact successful fast requests
- JSON cleaning overhead <10ms per response
- No degradation in parallel processing throughput

**NFR2: Compatibility**
- Backward compatible with existing OllamaClient usage
- No breaking changes to public APIs
- Existing tests must continue passing

**NFR3: Observability**
- Log timeout values on client initialization
- Track JSON validation success/failure rates
- Include detailed context in error logs for troubleshooting

## Technical Design

### Configuration Changes

**Update `config.py`:**
```python
@property
def ollama_read_timeout(self) -> int:
    """Ollama read timeout for long-running requests (seconds)."""
    return int(os.getenv("OLLAMA_READ_TIMEOUT", "240"))

@property
def ollama_connect_timeout(self) -> int:
    """Ollama connection timeout (seconds)."""
    return int(os.getenv("OLLAMA_CONNECT_TIMEOUT", "10"))
```

### OllamaClient Changes

**Update `ollama_client.py`:**

1. **Make timeouts configurable:**
```python
class OllamaClient:
    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "gemma2:12b",
        max_retries: int = 3,
        connect_timeout: float = 10.0,
        read_timeout: float = 240.0  # Increased default
    ):
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.max_retries = max_retries
        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout

        logger.info(f"OllamaClient initialized: timeout={read_timeout}s, model={model}")

        # ... rest of initialization using self.connect_timeout and self.read_timeout
```

2. **Add JSON cleaning utility:**
```python
def _clean_json_response(self, response_text: str) -> str:
    """
    Clean common JSON formatting issues from LLM responses.

    Args:
        response_text: Raw LLM response

    Returns:
        Cleaned JSON string
    """
    # Strip markdown code fences
    if response_text.strip().startswith("```"):
        lines = response_text.strip().split('\n')
        # Remove first and last lines if they're code fences
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        response_text = '\n'.join(lines)

    # Strip leading/trailing whitespace
    response_text = response_text.strip()

    # Remove trailing commas before closing braces/brackets
    import re
    response_text = re.sub(r',(\s*[}\]])', r'\1', response_text)

    return response_text
```

3. **Update call_ollama to use cleaned JSON:**
```python
def call_ollama(...) -> Dict[str, Any]:
    # ... existing request code ...

    try:
        response = self.client.post("/api/generate", json=payload)
        response.raise_for_status()
        result = response.json()

        if "response" not in result:
            raise ValueError("Invalid Ollama response: missing 'response' field")

        return result

    except httpx.TimeoutException as e:
        self.logger.warning(f"Ollama timeout after {self.read_timeout}s: {e}")
        raise TimeoutError(f"Ollama request timed out: {e}") from e
    # ... rest of exception handling ...
```

4. **Update extract_semantics with robust JSON parsing:**
```python
def extract_semantics(...) -> Dict[str, Any]:
    # ... existing prompt creation ...

    try:
        response = self.call_ollama(...)
        response_text = response["response"]

        # Clean JSON response
        cleaned_text = self._clean_json_response(response_text)

        try:
            extracted = json.loads(cleaned_text)
        except json.JSONDecodeError as e:
            self.logger.error(
                f"Failed to parse JSON after cleaning: {e}\n"
                f"First 500 chars: {cleaned_text[:500]}"
            )
            # Return minimal fallback
            extracted = {...}

        # ... rest of validation ...
```

### DatabaseAnalyzer Changes

**Update `db_analyzer.py`:**

1. **Update _extract_entity_with_llm:**
```python
def _extract_entity_with_llm(...) -> Optional[Dict[str, Any]]:
    prompt = DAO_EXTRACTION_PROMPT_TEMPLATE.format(...)

    try:
        response = self.ollama_client.call_ollama(
            prompt=prompt,
            temperature=0.2,
            format_json=True
        )

        response_text = response["response"]

        # Clean and validate JSON
        cleaned_text = self.ollama_client._clean_json_response(response_text)

        try:
            extracted = json.loads(cleaned_text)
        except json.JSONDecodeError as e:
            error_context = cleaned_text[:500] if len(cleaned_text) > 500 else cleaned_text
            self.logger.error(
                f"Failed to parse LLM JSON for {file_path.name}: {e}\n"
                f"Response preview: {error_context}"
            )
            raise ValueError(f"Invalid JSON from LLM: {e}")

        # Validate required fields with better error messages
        if "entity_name" not in extracted or not extracted["entity_name"]:
            self.logger.error(f"Missing entity_name in response for {file_path.name}")
            raise ValueError("Missing required field: entity_name")

        if "columns" not in extracted or not extracted["columns"]:
            self.logger.error(f"Missing or empty columns in response for {file_path.name}")
            raise ValueError("Missing or empty required field: columns")

        if "description" not in extracted:
            self.logger.error(f"Missing description in response for {file_path.name}")
            raise ValueError("Missing required field: description")

        self.logger.info(f"✓ Extracted entity: {extracted.get('entity_name')}")
        return extracted

    except json.JSONDecodeError as e:
        self.logger.error(f"Failed to parse LLM JSON response: {e}")
        raise ValueError(f"Invalid JSON from LLM: {e}")
    except Exception as e:
        self.logger.error(f"LLM extraction failed: {e}")
        raise
```

2. **Update create_ollama_client calls:**

Ensure all code that creates OllamaClient passes timeout from config:
```python
from codeindex.utils.config import get_config

config = get_config()
ollama_client = OllamaClient(
    base_url=config.ollama_base_url,
    model=config.ollama_model_name,
    connect_timeout=config.ollama_connect_timeout,
    read_timeout=config.ollama_read_timeout
)
```

### CLI Updates

**Update all CLI commands that use OllamaClient:**

- `src/codeindex/cli/prd.py` - database, backend, frontend commands
- `src/codeindex/cli/extract.py` - if using Ollama
- Any other services creating OllamaClient instances

## Implementation Plan

### Phase 1: Configuration and OllamaClient (2 hours)
1. Add `ollama_read_timeout` and `ollama_connect_timeout` to config.py
2. Update OllamaClient constructor to accept timeout parameters
3. Add JSON cleaning utility `_clean_json_response`
4. Update `call_ollama` to use configurable timeouts
5. Update `extract_semantics` with robust JSON parsing
6. Add logging for timeout values and JSON issues
7. Update unit tests for OllamaClient

### Phase 2: DatabaseAnalyzer Updates (1 hour)
1. Update `_extract_entity_with_llm` with robust JSON parsing
2. Improve error messages with context
3. Update all OllamaClient instantiations to pass config timeouts
4. Add unit tests for JSON cleaning

### Phase 3: CLI and Integration (1 hour)
1. Update all CLI commands to pass config to OllamaClient
2. Update integration tests
3. Test with production data sample
4. Update documentation

### Phase 4: Testing and Validation (1 hour)
1. Run full test suite
2. Test with problematic DAO files from production
3. Verify timeout behavior (use sleep test)
4. Validate JSON cleaning with malformed samples
5. Check backward compatibility

## Acceptance Criteria

**AC1: Timeout Configuration**
- [ ] OllamaClient accepts timeout parameters
- [ ] Config timeout is used by default
- [ ] Environment variables override config
- [ ] Timeout values logged on initialization

**AC2: JSON Parsing Robustness**
- [ ] Markdown code fences stripped from responses
- [ ] Trailing commas removed
- [ ] Parse errors logged with response preview (500 chars)
- [ ] Graceful fallback on JSON errors

**AC3: Error Handling**
- [ ] File context included in error messages
- [ ] Malformed JSON logged for debugging
- [ ] Other files continue processing on failures
- [ ] Clear error messages for missing fields

**AC4: Production Validation**
- [ ] DAO files that previously timed out complete successfully
- [ ] JSON parsing failures reduced by >50%
- [ ] Overall extraction success rate >90%
- [ ] No regression in processing time for successful requests

**AC5: Testing**
- [ ] All existing tests pass
- [ ] New tests for JSON cleaning
- [ ] New tests for configurable timeouts
- [ ] Integration tests with malformed JSON samples

## Testing Strategy

### Unit Tests

**test_ollama_client.py:**
- Test configurable timeouts
- Test JSON cleaning with various malformed inputs
- Test graceful fallback on JSON errors
- Test timeout behavior (mock httpx timeout)

**test_db_analyzer.py:**
- Test robust JSON parsing in _extract_entity_with_llm
- Test error context in log messages
- Test required field validation

### Integration Tests

**test_prd_generation.py:**
- Test with actual problematic DAO files
- Test with timeout scenarios (mock slow responses)
- Test with malformed JSON responses
- Validate success rate improvement

### Manual Testing

1. Run step2.sh with cuco-ui-admin project
2. Monitor log output for timeout and JSON errors
3. Verify >90% success rate
4. Check PRD output quality

## Risks and Mitigation

**Risk: Increased timeout may hide performance issues**
- Mitigation: Log request duration, monitor for slow files

**Risk: JSON cleaning may alter valid responses**
- Mitigation: Only apply safe transformations, extensive testing

**Risk: Backward compatibility breakage**
- Mitigation: Make parameters optional with sensible defaults

**Risk: LLM still generates invalid JSON**
- Mitigation: Consider model switch to gemma2:12b or add prompt improvements

## Dependencies

- No new external dependencies
- Requires Python 3.8+ (existing requirement)
- Uses existing httpx, json, re modules

## Documentation Updates

- Update README.md with new timeout configuration
- Update CLAUDE.md with troubleshooting section
- Document JSON cleaning behavior
- Add example .env entries

## Success Metrics

**Before (Production Issues):**
- Timeout errors: ~15-20 per 76 files
- JSON parse errors: ~10-15 per 76 files
- Overall failure rate: ~35%

**After (Target):**
- Timeout errors: <5 per 76 files (<7%)
- JSON parse errors: <3 per 76 files (<4%)
- Overall failure rate: <10%
- Processing time for successful requests: No significant change

## Future Enhancements

1. **Adaptive timeout**: Adjust timeout based on file size/complexity
2. **Model auto-selection**: Try gemma2:12b first, fallback to gemma3:12b
3. **JSON schema validation**: Validate against expected schema before processing
4. **Retry with cleaned prompt**: On JSON error, retry with simpler prompt
5. **Caching**: Cache successful extractions to avoid reprocessing on failures
