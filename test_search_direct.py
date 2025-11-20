#!/usr/bin/env python3
"""Test search directly to see what's happening."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path('src')))

from store.weaviate_client import WeaviateClient
import logging

# Enable INFO logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

print("=" * 80)
print("Direct Search Test")
print("=" * 80)

wc = WeaviateClient(ensure_schema=False)

print("\n1. Testing search_artifacts with project filter...")
print("   Query: 'dao', Project: 'cuco-core', Limit: 5")
results = wc.search_artifacts('DaoCall', 'dao', project='cuco-core', limit=5)
print(f"   Results: {len(results)}")
for i, r in enumerate(results[:3], 1):
    print(f"   {i}. Project: {r.get('project')}, Path: {r.get('path', '')[:70]}")

print("\n2. Testing search_artifacts without project filter...")
print("   Query: 'dao', Project: None, Limit: 5")
results2 = wc.search_artifacts('DaoCall', 'dao', project=None, limit=5)
print(f"   Results: {len(results2)}")
for i, r in enumerate(results2[:3], 1):
    print(f"   {i}. Project: {r.get('project')}, Path: {r.get('path', '')[:70]}")

print("\n" + "=" * 80)

