# Re-indexing Instructions

## Current Status

✅ Project names are correctly extracted in artifacts:
- `cuco-ui-cct-a1voip`: 23 files
- `cuco-core`: 3,124 files
- `cuco-ui-app`: 1,826 files
- And many more...

❌ Search returns no results because data needs to be re-indexed in Weaviate

## Solution

The artifacts have correct project names, but Weaviate still has the old data (with incorrect project names like "mnt"). You need to:

### Option 1: Clear and Re-index (Recommended)

1. **Clear existing Weaviate data** (optional but recommended):
   ```bash
   # Stop Weaviate
   docker-compose down
   
   # Remove Weaviate data directory (if using local storage)
   # Or use Weaviate's delete API to clear classes
   ```

2. **Re-index all artifacts**:
   ```bash
   python main.py index --all-projects
   ```
   
   This should now:
   - Load all 13,359 DAO call files
   - Load all other artifact types
   - Index them with correct project names
   - Show: "Indexed X artifacts in Weaviate" (should be 13,000+)

3. **Verify indexing**:
   ```bash
   python main.py search --query "dao" --project "cuco-ui-cct-a1voip"
   ```

### Option 2: Re-index Without Clearing (Faster)

If you don't want to clear Weaviate, just re-index. The new data will be added/updated:

```bash
python main.py index --all-projects
```

Note: This may create duplicates if the same artifacts are indexed twice. Clearing first is cleaner.

## Expected Results After Re-indexing

After re-indexing, you should see:
- **13,000+ artifacts indexed** (instead of just 495)
- **All project names correctly set** (cuco-ui-cct-a1voip, cuco-core, etc.)
- **Searches working** for all projects

## Verification

After re-indexing, test:

```bash
# Test search for a1voip
python main.py search --query "dao" --project "cuco-ui-cct-a1voip"

# Test search for other projects
python main.py search --query "dao" --project "cuco-core"
python main.py search --query "dao" --project "PastExport"
```

You should see results for all of these.

## If Search Still Fails

If search still returns no results after re-indexing:

1. **Check what's actually in Weaviate**:
   ```bash
   python check_weaviate_indexed.py
   ```
   (You may need to create this script or use the Weaviate API directly)

2. **Verify project names match exactly**:
   - Project names are case-sensitive
   - Must match exactly: "cuco-ui-cct-a1voip" not "Cuco-Ui-Cct-A1Voip"

3. **Try search without project filter**:
   ```bash
   python main.py search --query "dao"
   ```
   If this works, the issue is with project filtering.

