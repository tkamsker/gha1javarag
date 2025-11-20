# Weaviate Statistics Tool

A diagnostic tool to inspect what's actually indexed in Weaviate. Helps debug search issues by showing:
- What classes are indexed
- How many objects per class
- Project distribution
- Sample paths
- Search test results

## Usage

### Quick Start

```bash
./weaviate_stats.sh
```

Or directly with Python:

```bash
source venv/bin/activate
python weaviate_stats.py
```

## What It Shows

### 1. Overall Statistics
- Total objects indexed
- Objects by class (DaoCall, IbatisStatement, etc.)
- Number of unique projects per class

### 2. Projects Overview
- All projects found in Weaviate
- Object count per project
- Sorted by most objects

### 3. Projects by Class
- For each class, shows top 10 projects
- Helps identify which projects have data in which classes

### 4. Sample Paths
- Shows example file paths for each class
- Helps verify data is correctly indexed

### 5. Search Test Results
- Tests searches for top 5 projects
- Shows if searches work for each project
- Helps identify search issues

## Example Output

```
============================================================
WEAVIATE STATISTICS
============================================================

Total Objects Indexed: 13854

Objects by Class:
┌─────────────────┬───────┬──────────┐
│ Class           │ Count │ Projects │
├─────────────────┼───────┼──────────┤
│ DaoCall         │ 13359 │ 30       │
│ IbatisStatement │ 495   │ 5        │
└─────────────────┴───────┴──────────┘

Projects Overview:
┌──────────────────────┬──────────────┐
│ Project              │ Total Objects│
├──────────────────────┼──────────────┤
│ cuco-core            │ 3124         │
│ cuco-ui-app          │ 1826         │
│ cuco-ui-common       │ 855          │
└──────────────────────┴──────────────┘
```

## Troubleshooting

### No Results in Search

1. **Check if project exists:**
   ```bash
   ./weaviate_stats.sh | grep "cuco-ui-cct-a1voip"
   ```

2. **Check if class has data:**
   - Look at "Objects by Class" table
   - If DaoCall shows 0, data isn't indexed

3. **Check project names:**
   - Look at "Projects Overview"
   - Verify exact project name (case-sensitive)

### Data Not Indexed

If statistics show 0 objects:
1. Check if Weaviate is running: `docker ps | grep weaviate`
2. Re-index: `python main.py index --all-projects`
3. Check for errors during indexing

### Wrong Project Names

If projects show incorrect names (like "mnt"):
1. Fix project names: `python fix_project_names.py`
2. Re-index: `python main.py index --all-projects`
3. Run stats again to verify

## Requirements

- Python 3.7+
- `rich` library: `pip install rich`
- Weaviate running and accessible
- Virtual environment activated (optional but recommended)

## Platform Support

- ✅ macOS
- ✅ Linux
- ✅ Works with both Docker and native Weaviate installations

