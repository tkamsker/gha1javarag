# Fixes Applied to CrewAI Requirements Generation

## Summary

Fixed two critical errors identified in the log file `log_run_2026Nov19_A.log`:

1. **Tool Validation Error**: Fixed `WeaviateSearchTool` to accept both string and list inputs for `artifact_type`
2. **Ollama Timeout Error**: Increased timeout from 600s (10 min) to 1200s (20 min)

## Changes Made

### File: `src/synth/crewai_requirements.py`

#### 1. Added Custom Pydantic Schema for Tool Arguments

**Added** `WeaviateSearchToolArgs` class to properly handle Union types:
```python
class WeaviateSearchToolArgs(BaseModel):
    """Arguments schema for WeaviateSearchTool."""
    query: str = Field(description="Search query string")
    artifact_type: Union[str, List[str]] = Field(
        default="BackendDoc",
        description="Artifact type(s) to search. Can be a single string or a list of strings..."
    )
    limit: int = Field(default=5, description="Maximum number of results per artifact type")
```

**Updated** `WeaviateSearchTool` to use the custom schema:
```python
class WeaviateSearchTool(BaseTool):
    args_schema: type[BaseModel] = WeaviateSearchToolArgs
    # ... rest of the class
```

#### 2. Enhanced Tool Implementation

**Updated** `_run` method to handle both string and list inputs:
- Converts string input to list for uniform processing
- Searches each artifact type when a list is provided
- Combines results from multiple artifact types
- Improved error handling with better logging

#### 3. Increased Ollama Timeout

**Updated** LLM configuration in `CrewAIRequirementsGenerator.__init__()`:
```python
self.llm = LLM(
    model=model_name,
    base_url=base_url,
    temperature=0.7,
    timeout=1200.0  # 20 minutes timeout (was 600s default)
)
```

## Testing Recommendations

### Step 1: Verify Ollama is Running
```bash
curl http://localhost:11434/api/tags
```

### Step 2: Test with a Single Project
```bash
python main.py requirements --project <test-project-name> --use-crewai
```

### Step 3: Monitor for Errors
- Watch for tool validation errors (should be fixed)
- Monitor timeout issues (should be reduced with 20-min timeout)
- Check if tool accepts list inputs correctly

### Step 4: Full Run (If Step 2 Succeeds)
```bash
nohup python main.py requirements --all-projects --use-crewai > "logprod_crewai_$(date +'%Y-%m-%d_%H-%M-%S').log" 2>&1 &
```

## Expected Behavior After Fixes

1. **Tool Validation**: No more "Input should be a valid string" errors when LLM passes lists
2. **Timeout**: Should handle longer-running tasks with 20-minute timeout
3. **Tool Functionality**: Tool now properly searches multiple artifact types when provided as a list

## Potential Issues to Monitor

1. **Timeout Still Occurring**: If 20 minutes isn't enough, consider:
   - Optimizing prompts to reduce response time
   - Breaking tasks into smaller chunks
   - Using a faster model

2. **Tool Performance**: Searching multiple artifact types may be slower - monitor performance

3. **LLM Behavior**: The LLM may still prefer single artifact types - the tool now handles both

## Rollback Instructions

If issues occur, revert changes:
```bash
git checkout src/synth/crewai_requirements.py
```

Or manually revert:
1. Remove `WeaviateSearchToolArgs` class
2. Remove `args_schema` line from `WeaviateSearchTool`
3. Revert `_run` method to original implementation
4. Revert timeout to default (remove timeout parameter)

## Next Steps

1. ✅ Fixes applied
2. ⏳ Test with single project
3. ⏳ Monitor first run
4. ⏳ Adjust if needed based on results
5. ⏳ Rerun full collection if test succeeds

