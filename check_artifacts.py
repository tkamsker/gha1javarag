#!/usr/bin/env python3
"""Diagnostic script to check project names in artifacts."""
import json
from pathlib import Path
from collections import Counter

build_dir = Path('data/build')
projects = Counter()
artifact_counts = Counter()

print("=" * 60)
print("Checking artifacts for project names...")
print("=" * 60)

# Check dao_calls (individual files in java_calls)
dao_dir = build_dir / 'java_calls'
if dao_dir.exists():
    json_files = list(dao_dir.glob('*.json'))
    print(f"\nChecking {len(json_files)} DAO call files...")
    for f in json_files[:20]:  # Check first 20
        try:
            data = json.load(open(f))
            if isinstance(data, dict):
                proj = data.get('project', 'NO_PROJECT')
                projects[proj] += 1
                artifact_counts['DaoCall'] += 1
        except Exception as e:
            print(f"  Error reading {f.name}: {e}")

# Check all_forms.json
forms_file = build_dir / 'jsp_forms' / 'all_forms.json'
if forms_file.exists():
    try:
        data = json.load(open(forms_file))
        print(f"\nChecking JSP forms ({len(data) if isinstance(data, list) else 0} items)...")
        items = data if isinstance(data, list) else []
        for item in items:
            if isinstance(item, dict):
                proj = item.get('project', 'NO_PROJECT')
                projects[proj] += 1
                artifact_counts['JspForm'] += 1
    except Exception as e:
        print(f"  Error reading forms: {e}")

# Check all_statements.json
stmt_file = build_dir / 'ibatis_statements' / 'all_statements.json'
if stmt_file.exists():
    try:
        data = json.load(open(stmt_file))
        print(f"\nChecking iBATIS statements ({len(data) if isinstance(data, list) else 0} items)...")
        items = data if isinstance(data, list) else []
        for item in items:
            if isinstance(item, dict):
                proj = item.get('project', 'NO_PROJECT')
                projects[proj] += 1
                artifact_counts['IbatisStatement'] += 1
    except Exception as e:
        print(f"  Error reading statements: {e}")

# Check all_backend_docs.json
backend_file = build_dir / 'backend_docs' / 'all_backend_docs.json'
if backend_file.exists():
    try:
        data = json.load(open(backend_file))
        print(f"\nChecking backend docs ({len(data) if isinstance(data, list) else 0} items)...")
        items = data if isinstance(data, list) else []
        for item in items:
            if isinstance(item, dict):
                proj = item.get('project', 'NO_PROJECT')
                projects[proj] += 1
                artifact_counts['BackendDoc'] += 1
    except Exception as e:
        print(f"  Error reading backend docs: {e}")

# Check all_modules.json
modules_file = build_dir / 'gwt_modules' / 'all_modules.json'
if modules_file.exists():
    try:
        data = json.load(open(modules_file))
        print(f"\nChecking GWT modules ({len(data) if isinstance(data, list) else 0} items)...")
        items = data if isinstance(data, list) else []
        for item in items:
            if isinstance(item, dict):
                proj = item.get('project', 'NO_PROJECT')
                projects[proj] += 1
                artifact_counts['GwtModule'] += 1
    except Exception as e:
        print(f"  Error reading modules: {e}")

# Check all_uibinder.json
uibinder_file = build_dir / 'gwt_uibinder' / 'all_uibinder.json'
if uibinder_file.exists():
    try:
        data = json.load(open(uibinder_file))
        print(f"\nChecking GWT UiBinder ({len(data) if isinstance(data, list) else 0} items)...")
        items = data if isinstance(data, list) else []
        for item in items:
            if isinstance(item, dict):
                proj = item.get('project', 'NO_PROJECT')
                projects[proj] += 1
                artifact_counts['GwtUiBinder'] += 1
    except Exception as e:
        print(f"  Error reading uibinder: {e}")

# Check all_js_artifacts.json
js_file = build_dir / 'js_artifacts' / 'all_js_artifacts.json'
if js_file.exists():
    try:
        data = json.load(open(js_file))
        print(f"\nChecking JS artifacts ({len(data) if isinstance(data, list) else 0} items)...")
        items = data if isinstance(data, list) else []
        for item in items:
            if isinstance(item, dict):
                proj = item.get('project', 'NO_PROJECT')
                projects[proj] += 1
                artifact_counts['JsArtifact'] += 1
    except Exception as e:
        print(f"  Error reading JS artifacts: {e}")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"\nTotal artifacts checked by type:")
for artifact_type, count in sorted(artifact_counts.items()):
    print(f"  {artifact_type}: {count}")

print(f"\nProject names found in artifacts:")
if projects:
    for proj, count in projects.most_common(20):
        print(f"  {proj}: {count} artifacts")
else:
    print("  No project names found!")

# Check for PastExport specifically
past_export_count = projects.get('PastExport', 0)
print(f"\n'PastExport' project: {past_export_count} artifacts")

if past_export_count == 0:
    print("\n⚠️  WARNING: No 'PastExport' artifacts found!")
    print("   This means either:")
    print("   1. The artifacts don't have 'PastExport' as project name")
    print("   2. The project name extraction didn't work correctly")
    print("   3. The data needs to be re-extracted with proper project names")

