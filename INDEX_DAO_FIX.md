# Index Command Fix for DAO Calls

## Problem

The index command was only indexing iBATIS statements (495 artifacts) and not DAO calls. This happened because:

1. DAO calls are stored as **individual JSON files** in `data/build/java_calls/` directory (13,359 files)
2. The index command was looking for an aggregate file `all_dao_calls.json` which doesn't exist
3. Only iBATIS statements were being indexed, so searches for DAO-related queries returned no results

## Solution

Updated the `index` command in `src/cli.py` to:

1. **Check for individual DAO call files** in `java_calls` directory first
2. **Load all individual JSON files** and aggregate them into a list
3. **Index all DAO calls** along with other artifact types

## Changes Made

### Before:
- Only looked for `all_dao_calls.json` aggregate file
- Skipped DAO calls if aggregate file didn't exist
- Only indexed 495 iBATIS statements

### After:
- Checks `java_calls` directory for individual JSON files
- Loads all individual files and aggregates them
- Indexes all artifact types including DAO calls

## Next Steps

1. **Fix project names in DAO call files** (if not already done):
   ```bash
   python fix_project_names.py
   ```
   This will fix project names in all 13,359 individual DAO call files.

2. **Re-index all artifacts**:
   ```bash
   python main.py index --all-projects
   ```
   This should now index:
   - All DAO calls from `java_calls/` directory
   - iBATIS statements
   - Other artifact types

3. **Verify indexing**:
   ```bash
   python main.py search --query "dao" --project "cuco-ui-cct-a1voip"
   ```

4. **Check what was indexed**:
   You should see output like:
   ```
   Loading 13359 DAO call files from java_calls directory...
   Loaded 13359 DAO call artifacts
   Found X projects in artifacts: ...
   Indexing dao_calls...
   Indexed X artifacts in Weaviate
   ```

## Expected Results

After re-indexing, you should have:
- **13,359+ DAO calls** indexed (instead of 0)
- **All project names** correctly extracted (cuco-ui-cct-a1voip, etc.)
- **Searches working** for DAO-related queries

## Files Modified

- `src/cli.py` - Added logic to load individual DAO call files from `java_calls` directory

