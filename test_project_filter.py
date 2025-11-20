#!/usr/bin/env python3
"""Test project filter in Weaviate queries."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path('src')))

from store.weaviate_client import WeaviateClient

wc = WeaviateClient(ensure_schema=False)
client = wc._client

print("Testing project filter...")

# Test 1: Simple query with project filter
print("\n1. Testing query with project filter (cuco-core)...")
try:
    res = client.query.get("DaoCall", ["project", "path"]).with_where({
        "path": ["project"],
        "operator": "Equal",
        "valueText": "cuco-core"
    }).with_limit(5).do()
    hits = res.get('data', {}).get('Get', {}).get('DaoCall', [])
    print(f"  ✓ Found {len(hits)} objects")
    if hits:
        for h in hits[:3]:
            print(f"    - {h.get('project')}: {h.get('path', '')[:60]}")
except Exception as e:
    print(f"  ✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 2: BM25 with project filter
print("\n2. Testing BM25 search with project filter...")
try:
    res = client.query.get("DaoCall", ["project", "path", "text"]).with_where({
        "path": ["project"],
        "operator": "Equal",
        "valueText": "cuco-core"
    }).with_bm25(query="dao").with_limit(5).do()
    hits = res.get('data', {}).get('Get', {}).get('DaoCall', [])
    print(f"  ✓ Found {len(hits)} objects")
    if hits:
        for h in hits[:5]:
            proj = h.get('project', 'NO_PROJECT')
            path = h.get('path', '')[:60]
            match = "✓" if proj == "cuco-core" else "✗"
            print(f"    {match} {proj}: {path}")
        
        # Check if all match
        all_match = all(h.get('project') == 'cuco-core' for h in hits)
        if not all_match:
            print(f"  ⚠ WARNING: Some results don't match project filter!")
            wrong_projects = set(h.get('project') for h in hits if h.get('project') != 'cuco-core')
            print(f"    Wrong projects found: {wrong_projects}")
except Exception as e:
    print(f"  ✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Check what projects actually exist
print("\n3. Checking what projects exist...")
try:
    res = client.query.get("DaoCall", ["project"]).with_limit(100).do()
    hits = res.get('data', {}).get('Get', {}).get('DaoCall', [])
    projects = set(h.get('project') for h in hits if h.get('project'))
    print(f"  ✓ Found {len(projects)} unique projects in sample:")
    for p in sorted(list(projects))[:20]:
        print(f"    - {p}")
    if 'cuco-core' in projects:
        print(f"  ✓ 'cuco-core' exists in sample")
    else:
        print(f"  ⚠ 'cuco-core' NOT in sample (might exist in other objects)")
except Exception as e:
    print(f"  ✗ Error: {e}")

