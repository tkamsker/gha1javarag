# Fix Plan for CrewAI Requirements Generation Errors

## Issues Identified

### 1. Tool Validation Error (Critical)
**Problem**: The LLM is passing a list `['BackendDoc', 'IbatisStatement']` to `artifact_type` parameter, but the tool schema expects a string.

**Error Message**:
```
Arguments validation failed: 1 validation error for WeaviateSearchToolSchema
artifact_type
  Input should be a valid string [type=string_type, input_value=['BackendDoc', 'IbatisStatement'], input_type=list]
```

**Location**: `src/synth/crewai_requirements.py` - `WeaviateSearchTool` class

**Root Cause**: The tool description doesn't clearly state that only ONE artifact type can be searched at a time. The LLM is trying to search multiple types simultaneously.

### 2. Ollama Timeout Error (Critical)
**Problem**: Ollama connection times out after 600 seconds (10 minutes).

**Error Message**:
```
litellm.Timeout: Connection timed out after 600.0 seconds.
OllamaException - litellm.Timeout: Connection timed out after 600.0 seconds.
```

**Location**: `src/synth/crewai_requirements.py` - `CrewAIRequirementsGenerator.__init__()` - LLM configuration

**Root Cause**: 
- No explicit timeout configuration in LLM setup
- Using `gemma3:12b` model which may be slow for large prompts
- Default timeout of 600 seconds may not be sufficient for complex tasks

### 3. Telemetry Connection Errors (Non-Critical)
**Problem**: CrewAI telemetry service connection timeouts (doesn't affect functionality).

**Error Message**:
```
HTTPSConnectionPool(host='telemetry.crewai.com', port=4319): Max retries exceeded
```

**Impact**: Low - only affects telemetry, not core functionality.

---

## Step-by-Step Fix Plan

### Step 1: Fix WeaviateSearchTool Schema Issue

**Option A (Recommended)**: Update tool to handle multiple artifact types
- Modify `_run` method to accept a list or string
- If list provided, search each type and combine results
- Update tool description to clarify it can accept either

**Option B**: Improve tool description to prevent LLM from passing lists
- Make description more explicit: "artifact_type must be a single string, one of: BackendDoc, DaoCall, JspForm, etc."
- Add examples in description

**Implementation**: We'll use Option A as it's more robust and allows the LLM flexibility.

### Step 2: Fix Ollama Timeout Configuration

**Actions**:
1. Add explicit timeout configuration to LLM initialization
2. Increase timeout to 1200 seconds (20 minutes) for complex tasks
3. Add retry logic with exponential backoff
4. Consider adding request size limits or chunking for very large prompts

**Implementation**: Update `CrewAIRequirementsGenerator.__init__()` to configure timeout.

### Step 3: Improve Tool Description

**Actions**:
1. Update `WeaviateSearchTool.description` to be more explicit about:
   - Single artifact type per call
   - Available artifact types
   - How to search multiple types (make multiple calls)
2. Add better error messages in tool execution

### Step 4: Add Error Handling and Recovery

**Actions**:
1. Add try-catch around tool execution with better error messages
2. Add validation in `_run` method to handle edge cases
3. Log warnings when LLM passes invalid types

### Step 5: Test Fixes

**Actions**:
1. Test tool with single artifact type (should work)
2. Test tool with list of artifact types (should now work with Option A)
3. Test with timeout scenarios
4. Run a small test project to verify end-to-end

### Step 6: Rerun Collection (If Needed)

**Actions**:
1. Check if any projects completed successfully before the error
2. Identify which projects failed
3. Rerun only failed projects
4. Monitor for timeout issues

---

## Implementation Details

### File: `src/synth/crewai_requirements.py`

#### Changes Needed:

1. **Update WeaviateSearchTool._run()**:
   - Accept `artifact_type` as Union[str, List[str]]
   - Handle both string and list inputs
   - If list, search each type and combine results

2. **Update WeaviateSearchTool.description**:
   - Clarify that artifact_type can be a single string or list of strings
   - List all available artifact types
   - Provide examples

3. **Update CrewAIRequirementsGenerator.__init__()**:
   - Add `timeout` parameter to LLM configuration
   - Set timeout to 1200 seconds (20 minutes)
   - Add retry configuration if supported

---

## Verification Steps

1. **Check Ollama is running**:
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. **Test tool with single type**:
   - Should work as before

3. **Test tool with list of types**:
   - Should now work without validation errors

4. **Monitor timeout**:
   - Check if 20-minute timeout is sufficient
   - Monitor Ollama logs for performance issues

5. **Run test project**:
   ```bash
   python main.py requirements --project <test-project> --use-crewai
   ```

---

## Rollback Plan

If fixes cause issues:
1. Revert changes to `src/synth/crewai_requirements.py`
2. Use git to restore previous version
3. Consider using Option B (description-only fix) instead

---

## Next Steps After Fixes

1. Monitor first run after fixes
2. Collect metrics on:
   - Tool call success rate
   - Average response time
   - Timeout frequency
3. Adjust timeout if needed based on real-world usage
4. Consider optimizing prompts to reduce response time

