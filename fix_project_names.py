#!/usr/bin/env python3
"""Fix project names in artifacts based on file paths."""
import json
import sys
from pathlib import Path
from collections import Counter

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from config.project_utils import extract_project_name_from_path

build_dir = Path('data/build')
stats = Counter()
fixed_count = 0
total_count = 0

def fix_project_in_item(item: dict, file_path: Path) -> bool:
    """Fix project name in a single artifact item."""
    global fixed_count, total_count
    
    if not isinstance(item, dict):
        return False
    
    total_count += 1
    original_project = item.get('project', 'NO_PROJECT')
    path = item.get('path', '')
    
    if not path:
        return False
    
    # Extract correct project name from path
    correct_project = extract_project_name_from_path(path)
    
    if original_project != correct_project:
        item['project'] = correct_project
        stats[f"{original_project} -> {correct_project}"] += 1
        fixed_count += 1
        return True
    
    return False

def fix_project_in_file(file_path: Path) -> int:
    """Fix project names in a JSON file. Returns number of items fixed."""
    if not file_path.exists():
        return 0
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        fixed = 0
        if isinstance(data, list):
            for item in data:
                if fix_project_in_item(item, file_path):
                    fixed += 1
        elif isinstance(data, dict):
            if fix_project_in_item(data, file_path):
                fixed = 1
        
        if fixed > 0:
            # Write back the fixed data
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"  ✓ Fixed {fixed} items in {file_path.name}")
        
        return fixed
        
    except Exception as e:
        print(f"  ✗ Error fixing {file_path}: {e}")
        return 0

def main():
    print("=" * 60)
    print("Fixing Project Names in Artifacts")
    print("=" * 60)
    
    # Fix aggregate artifact files
    artifact_files = [
        build_dir / 'jsp_forms' / 'all_forms.json',
        build_dir / 'ibatis_statements' / 'all_statements.json',
        build_dir / 'backend_docs' / 'all_backend_docs.json',
        build_dir / 'gwt_modules' / 'all_modules.json',
        build_dir / 'gwt_uibinder' / 'all_uibinder.json',
        build_dir / 'js_artifacts' / 'all_js_artifacts.json',
    ]
    
    print("\nFixing aggregate artifact files...")
    for f in artifact_files:
        if f.exists():
            fix_project_in_file(f)
    
    # Fix individual DAO call files
    dao_dir = build_dir / 'java_calls'
    if dao_dir.exists():
        json_files = list(dao_dir.glob('*.json'))
        print(f"\nFixing {len(json_files)} individual DAO call files...")
        fixed_files = 0
        for f in json_files:
            if fix_project_in_file(f) > 0:
                fixed_files += 1
        print(f"  Fixed {fixed_files} files")
    
    # Fix GWT client artifacts
    gwt_client_dir = build_dir / 'gwt_client'
    if gwt_client_dir.exists():
        print("\nFixing GWT client artifacts...")
        for f in gwt_client_dir.glob('*.json'):
            fix_project_in_file(f)
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total artifacts checked: {total_count}")
    print(f"Artifacts fixed: {fixed_count}")
    print(f"Artifacts unchanged: {total_count - fixed_count}")
    
    if stats:
        print("\nProject name changes:")
        for change, count in stats.most_common(10):
            print(f"  {change}: {count} artifacts")
    
    print("\n" + "=" * 60)
    print("Next steps:")
    print("1. Verify fixes: python check_artifacts.py")
    print("2. Re-index: python main.py index --all-projects")
    print("3. Test search: python main.py search --query 'PastExport' --project 'PastExport'")
    print("=" * 60)

if __name__ == '__main__':
    main()

