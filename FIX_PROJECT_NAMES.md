# Fix Project Names in Artifacts

## Problem

Artifacts have incorrect project names (mostly "mnt" instead of actual project names like "PastExport"). This causes searches to return no results because the project filter doesn't match.

## Root Cause

The project name extraction during the `extract` phase isn't working correctly. Artifacts are being assigned incorrect or default project names.

## Solutions

### Option 1: Re-extract with Proper Project Names (Recommended)

If you have the source code available, re-extract with explicit project names:

```bash
# Extract for specific project
python main.py extract --project "PastExport" --include-frontend

# Or extract all projects (if extract supports --all-projects)
# Then index with --all-projects to preserve names
python main.py index --all-projects
```

### Option 2: Fix Project Names in Existing Artifacts

If re-extraction isn't possible, we can fix project names in existing artifacts based on file paths.

#### Step 1: Check Current Project Names

```bash
source venv/bin/activate
python check_artifacts.py
```

#### Step 2: Fix Project Names Script

Create a script to fix project names based on file paths:

```python
# fix_project_names.py
import json
from pathlib import Path
from config.project_utils import extract_project_name_from_path

build_dir = Path('data/build')

def fix_project_in_file(file_path: Path):
    """Fix project names in a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        fixed = False
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    path = item.get('path', '')
                    if path:
                        correct_project = extract_project_name_from_path(path)
                        if item.get('project') != correct_project:
                            item['project'] = correct_project
                            fixed = True
        elif isinstance(data, dict):
            path = data.get('path', '')
            if path:
                correct_project = extract_project_name_from_path(path)
                if data.get('project') != correct_project:
                    data['project'] = correct_project
                    fixed = True
        
        if fixed:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
    return False

# Fix all artifact files
artifact_files = [
    build_dir / 'jsp_forms' / 'all_forms.json',
    build_dir / 'ibatis_statements' / 'all_statements.json',
    build_dir / 'backend_docs' / 'all_backend_docs.json',
    build_dir / 'gwt_modules' / 'all_modules.json',
    build_dir / 'gwt_uibinder' / 'all_uibinder.json',
    build_dir / 'js_artifacts' / 'all_js_artifacts.json',
]

# Fix individual DAO call files
dao_dir = build_dir / 'java_calls'
if dao_dir.exists():
    for f in dao_dir.glob('*.json'):
        fix_project_in_file(f)

# Fix aggregate files
for f in artifact_files:
    if f.exists():
        if fix_project_in_file(f):
            print(f"Fixed: {f}")

print("Done fixing project names!")
```

### Option 3: Manual Project Name Mapping

If you know the correct project names, create a mapping file and update artifacts:

```python
# project_mapping.py
PROJECT_MAPPING = {
    'mnt': 'PastExport',  # Map incorrect name to correct name
    # Add more mappings as needed
}

# Then update artifacts using this mapping
```

## Verification Steps

After fixing project names:

1. **Verify project names are fixed:**
   ```bash
   python check_artifacts.py
   ```

2. **Re-index with preserved project names:**
   ```bash
   python main.py index --all-projects
   ```

3. **Test search:**
   ```bash
   python main.py search --query "PastExport" --project "PastExport"
   python main.py search --query "dao" --project "PastExport"
   ```

4. **If search works, rerun requirements:**
   ```bash
   python main.py requirements --all-projects --use-crewai
   ```

## Quick Fix Script

I'll create a comprehensive fix script that:
1. Checks all artifacts
2. Extracts correct project names from file paths
3. Updates project names in artifacts
4. Verifies the fixes

