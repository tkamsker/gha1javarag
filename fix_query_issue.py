#!/usr/bin/env python3
"""
Fix query issue - check why queries return empty results even though objects exist.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path('src')))

from store.weaviate_client import WeaviateClient
import json

print("=" * 80)
print("Fixing Query Issue")
print("=" * 80)

wc = WeaviateClient(ensure_schema=False)
client = wc._client

# Test 1: Check if we can query without properties
print("\n1. Testing basic query...")
try:
    res = client.query.get("DaoCall", ["project"]).with_limit(5).do()
    hits = res.get('data', {}).get('Get', {}).get('DaoCall', [])
    print(f"  ✓ Retrieved {len(hits)} objects")
    if hits:
        print(f"  Sample: {hits[0]}")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 2: Check actual stored data
print("\n2. Checking stored data directly...")
try:
    # Get a few objects directly
    res = client.data_object.get(class_name="DaoCall", limit=5)
    if res and 'objects' in res:
        print(f"  ✓ Retrieved {len(res['objects'])} objects directly")
        for obj in res['objects'][:2]:
            props = obj.get('properties', {})
            print(f"    Project: {props.get('project', 'NONE')}")
            print(f"    Path: {props.get('path', 'NONE')[:80]}")
            print(f"    Has text: {'text' in props}")
            print(f"    Has meta: {'meta' in props}")
    else:
        print(f"  ✗ No objects returned")
except Exception as e:
    print(f"  ✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Try search with bm25
print("\n3. Testing BM25 search...")
try:
    res = client.query.get("DaoCall", ["project", "path", "text"]).with_bm25(query="dao").with_limit(5).do()
    hits = res.get('data', {}).get('Get', {}).get('DaoCall', [])
    print(f"  ✓ BM25 search returned {len(hits)} objects")
    if hits:
        print(f"  Sample project: {hits[0].get('project', 'NONE')}")
except Exception as e:
    print(f"  ✗ BM25 search error: {e}")

# Test 4: Check project distribution
print("\n4. Checking project distribution...")
try:
    # Use aggregate to get project counts
    res = client.query.aggregate("DaoCall").with_group_by(["project"]).with_fields("groupedBy {value}").do()
    groups = res.get('data', {}).get('Aggregate', {}).get('DaoCall', [])
    print(f"  ✓ Found {len(groups)} unique projects")
    for group in groups[:10]:
        proj = group.get('groupedBy', {}).get('value', 'NONE')
        print(f"    - {proj}")
except Exception as e:
    print(f"  ✗ Aggregate error: {e}")

print("\n" + "=" * 80)
print("Diagnostic complete")
print("=" * 80)

