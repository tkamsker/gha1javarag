#!/usr/bin/env python3
"""Find what project names exist in DAO call files."""
import json
from pathlib import Path
from collections import Counter

dao_dir = Path('data/build/java_calls')
projects = Counter()
a1voip_files = []

if dao_dir.exists():
    json_files = list(dao_dir.glob('*.json'))
    print(f"Checking {len(json_files)} DAO call files...")
    
    for i, f in enumerate(json_files):
        if i % 1000 == 0:
            print(f"  Processed {i}/{len(json_files)} files...")
        try:
            data = json.load(open(f))
            if isinstance(data, dict):
                proj = data.get('project', 'NO_PROJECT')
                path = data.get('path', '')
                projects[proj] += 1
                
                # Check for a1voip in path
                if 'a1voip' in path.lower() or 'cuco-ui-cct-a1voip' in path.lower():
                    a1voip_files.append({
                        'project': proj,
                        'path': path
                    })
        except Exception as e:
            pass

print("\n" + "=" * 60)
print("Project names found in DAO call files:")
print("=" * 60)
for proj, count in projects.most_common(30):
    print(f"  {proj}: {count} files")

print("\n" + "=" * 60)
print(f"Files with 'a1voip' in path: {len(a1voip_files)}")
print("=" * 60)
if a1voip_files:
    for f in a1voip_files[:10]:
        print(f"  Project: {f['project']}")
        print(f"  Path: {f['path'][:120]}")
        print()
else:
    print("  No files found with 'a1voip' in path")
    print("\n  Searching for 'cuco-ui-cct' instead...")
    cuco_cct_files = []
    for f in list(dao_dir.glob('*.json'))[:5000]:
        try:
            data = json.load(open(f))
            if isinstance(data, dict):
                path = data.get('path', '')
                if 'cuco-ui-cct' in path.lower():
                    cuco_cct_files.append({
                        'project': data.get('project', 'NO_PROJECT'),
                        'path': path
                    })
        except:
            pass
    
    print(f"  Found {len(cuco_cct_files)} files with 'cuco-ui-cct' in path")
    if cuco_cct_files:
        projects_in_cct = Counter([f['project'] for f in cuco_cct_files])
        print(f"  Projects: {dict(projects_in_cct)}")
        print("\n  Sample paths:")
        for f in cuco_cct_files[:5]:
            print(f"    {f['project']}: {f['path'][:100]}")

