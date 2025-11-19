# Index Command Fix

## Issue

The `index` command didn't support `--all-projects` and was overwriting project names from artifacts.

## Fix Applied

### Added `--all-projects` Option

The `index` command now supports:
- `--project <name>`: Index all artifacts with the specified project name (overwrites existing)
- `--all-projects`: Index all artifacts preserving their existing project names
- No option: Default behavior now preserves existing project names (changed from previous behavior)

### Behavior Changes

**Before:**
- Always overwrote project names with `--project` value or default
- No way to index multiple projects at once

**After:**
- `--all-projects`: Preserves project names from artifacts
- `--project <name>`: Overwrites all artifacts with specified project name
- No option: Preserves existing project names (safer default)

## Usage

### Index all projects (preserve existing project names):
```bash
python main.py index --all-projects
```

### Index with specific project name (overwrites):
```bash
python main.py index --project "PastExport"
```

### Index preserving existing project names (default):
```bash
python main.py index
```

## Next Steps

1. **Re-index data with project names preserved:**
   ```bash
   python main.py index --all-projects
   ```

2. **Verify indexing worked:**
   ```bash
   python main.py search --query "PastExport" --project "PastExport"
   ```

3. **If search still returns no results, check:**
   - Artifacts have project names set in JSON files
   - Project names match exactly (case-sensitive)
   - Weaviate is running and accessible

## Files Modified

- `src/cli.py` - Added `--all-projects` option and project name preservation logic

