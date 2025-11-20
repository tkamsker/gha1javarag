#!/usr/bin/env python3
"""Debug search to see what's happening."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path('src')))

from store.weaviate_client import WeaviateClient
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('store.weaviate_client')
logger.setLevel(logging.DEBUG)

print("=" * 80)
print("Debug Search")
print("=" * 80)

wc = WeaviateClient(ensure_schema=False)

print("\n1. Testing search_artifacts with project filter...")
results = wc.search_artifacts('DaoCall', 'dao', project='cuco-core', limit=5)
print(f"  Results: {len(results)}")
for r in results[:3]:
    print(f"    - Project: {r.get('project')}, Path: {r.get('path', '')[:60]}")

print("\n2. Testing without project filter...")
results2 = wc.search_artifacts('DaoCall', 'dao', project=None, limit=5)
print(f"  Results: {len(results2)}")
for r in results2[:3]:
    print(f"    - Project: {r.get('project')}, Path: {r.get('path', '')[:60]}")

