Adding an `--all` switch to the search command to search across all projects:


[3 tools called]


Updating the `backend-search` command to include the same option:


[3 tools called]


Added the `--all` option to both search commands. Summary:

## Changes Made

### 1. Updated `search` command
- Added `--all` / `-a` flag to search across all projects
- When `--all` is used, the `--project` option is ignored
- Shows project column in results when searching all projects
- Displays total results count

### 2. Updated `backend-search` command
- Added the same `--all` / `-a` flag
- Consistent behavior with the main search command

## Usage Examples

### Search in a specific project:
```bash
python main.py search --query "dao" --project "cuco-core"
```

### Search across all projects:
```bash
python main.py search --query "dao" --all
# or
python main.py search --query "dao" -a
```

### Search without project filter (default behavior):
```bash
python main.py search --query "dao"
# This already searches all projects if no --project is specified
```

### Backend search across all projects:
```bash
python main.py backend-search --query "authentication" --all
```

## Features

1. When `--all` is used:
   - Project filter is disabled
   - Results show a "Project" column
   - Total results count is displayed

2. When `--project` is specified:
   - Only searches that project
   - No project column (since it's the same for all results)

3. When neither is specified:
   - Searches all projects (no filter)
   - Shows project column in results

The `--all` flag makes it explicit that you want to search across all projects, which is useful for debugging and discovery.
