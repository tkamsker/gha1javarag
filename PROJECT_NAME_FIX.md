# Project Name Extraction Fix

## Problem

The project name extraction was picking up "mnt" from the path instead of the actual project directories. This happened because:

1. `JAVA_SOURCE_DIR` is `/mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c`
2. The actual projects are subdirectories like `administration.ui`, `cuco`, `cuco-cct-core`, etc.
3. The extraction logic wasn't using `JAVA_SOURCE_DIR` as the base directory

## Solution

Updated `extract_project_name_from_path()` in `src/config/project_utils.py` to:

1. **Prioritize JAVA_SOURCE_DIR**: Always use `JAVA_SOURCE_DIR` as the base directory
2. **Extract first subdirectory**: The first directory after `JAVA_SOURCE_DIR` is the project name
3. **Handle both structures**:
   - Multi-project: `JAVA_SOURCE_DIR/project-name/src/...` → `project-name`
   - Single project: `JAVA_SOURCE_DIR/src/...` → basename of `JAVA_SOURCE_DIR`

## Example

**Before (incorrect):**
- Path: `/mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-cct-a1voip/src/...`
- Extracted: `mnt` ❌

**After (correct):**
- Path: `/mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-cct-a1voip/src/...`
- JAVA_SOURCE_DIR: `/mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c`
- Relative path: `cuco-ui-cct-a1voip/src/...`
- Extracted: `cuco-ui-cct-a1voip` ✅

## Files Modified

1. **`src/config/project_utils.py`**:
   - Updated `extract_project_name_from_path()` to prioritize `JAVA_SOURCE_DIR`
   - Added system paths to ignore list (`mnt`, `cucocalcai`, `cuco-master`)
   - Uses `settings.java_source_dir` as default if not provided

2. **`fix_project_names.py`**:
   - Already uses `extract_project_name_from_path()` which now uses settings
   - Will correctly fix project names when run

## How to Fix Existing Artifacts

### Step 1: Verify JAVA_SOURCE_DIR is set correctly

Check your `.env` file:
```bash
grep JAVA_SOURCE_DIR .env
```

Should be:
```
JAVA_SOURCE_DIR=/mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c
```

### Step 2: Fix project names in existing artifacts

```bash
source venv/bin/activate
python fix_project_names.py
```

This will:
- Read all artifact files
- Extract correct project names using the updated logic
- Update project names in artifacts
- Show summary of changes

### Step 3: Verify fixes

```bash
python check_artifacts.py
```

You should see correct project names like:
- `cuco-ui-cct-a1voip`
- `administration.ui`
- `cuco-core`
- etc.

Instead of:
- `mnt` ❌

### Step 4: Re-index with correct project names

```bash
python main.py index --all-projects
```

### Step 5: Test search

```bash
python main.py search --query "PastExport" --project "PastExport"
# Or for other projects:
python main.py search --query "dao" --project "cuco-ui-cct-a1voip"
```

### Step 6: Rerun requirements generation

```bash
python main.py requirements --all-projects --use-crewai
```

## Expected Project Names

Based on your directory listing, the following project names should be extracted:

- `administration.ui`
- `cuco`
- `cuco-cct-core`
- `cuco-core`
- `cuco.dbmaintain`
- `cuco-ui-admin`
- `cuco-ui-app`
- `cuco-ui-cct`
- `cuco-ui-cct-a1bn`
- `cuco-ui-cct-a1cml`
- `cuco-ui-cct-a1ps`
- `cuco-ui-cct-a1tvres`
- `cuco-ui-cct-a1voip`
- `cuco-ui-cct-bfw`
- `cuco-ui-cct-bi`
- `cuco-ui-cct-ccs`
- `cuco-ui-cct-common`
- `cuco-ui-cct-etgt`
- `cuco-ui-cct-marketingproduct`
- `cuco-ui-cct-pshc`
- `cuco-ui-common`
- `cuco-ui-mycuco`
- `cuco-ui-pkb`
- `cuco-ui-visitreports`
- `framework.ui`
- `pkb-core`
- `pkb.ui`
- `pkb-ui-common`

Note: `_deprecated` and `_scripts` are ignored as they start with underscore.

## Future Extractions

When you run `python main.py extract` in the future, the project names will be correctly extracted automatically because the extraction code uses `extract_project_name_from_path()` which now properly handles `JAVA_SOURCE_DIR`.

