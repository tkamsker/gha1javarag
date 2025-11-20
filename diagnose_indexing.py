#!/usr/bin/env python3
"""
Diagnostic script to check Weaviate indexing issues.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path('src')))

from store.weaviate_client import WeaviateClient
import json

print("=" * 80)
print("Weaviate Indexing Diagnostic")
print("=" * 80)

# Initialize client with schema ensure
print("\n1. Initializing Weaviate client...")
wc = WeaviateClient(ensure_schema=True)
client = wc._client

# Check schema
print("\n2. Checking schema...")
classes = ['DaoCall', 'IbatisStatement', 'BackendDoc', 'JspForm', 
           'DbTable', 'GwtModule', 'GwtUiBinder', 'GwtActivityPlace',
           'GwtEndpoint', 'JsArtifact']

for class_name in classes:
    if client.schema.exists(class_name):
        schema = client.schema.get(class_name)
        props = [p.get('name') for p in schema.get('properties', [])]
        print(f"  {class_name}: {len(props)} properties")
        print(f"    Properties: {', '.join(props)}")
        if 'meta' not in props:
            print(f"    ⚠ WARNING: 'meta' property missing!")
    else:
        print(f"  {class_name}: DOES NOT EXIST")

# Check object counts
print("\n3. Checking object counts...")
for class_name in classes:
    try:
        if client.schema.exists(class_name):
            # Try aggregate query
            try:
                result = client.query.aggregate(class_name).with_meta_count().do()
                count = result.get('data', {}).get('Aggregate', {}).get(class_name, [{}])[0].get('meta', {}).get('count', 0)
                print(f"  {class_name}: {count} objects")
            except Exception as e:
                print(f"  {class_name}: Error getting count: {e}")
                # Try direct query
                try:
                    result = client.query.get(class_name, ['project']).with_limit(1).do()
                    hits = result.get('data', {}).get('Get', {}).get(class_name, [])
                    print(f"  {class_name}: At least {len(hits)} objects (sampled)")
                except Exception as e2:
                    print(f"  {class_name}: Error querying: {e2}")
    except Exception as e:
        print(f"  {class_name}: Error: {e}")

# Test indexing a sample artifact
print("\n4. Testing sample indexing...")
test_artifact = {
    'project': 'test-project',
    'path': '/test/path.java',
    'text': 'Test artifact for diagnostic',
    'meta': {'test': True, 'diagnostic': 'sample'}
}

try:
    result = wc.index_artifact('DaoCall', test_artifact)
    if result:
        print(f"  ✓ Successfully indexed test artifact: {result}")
        
        # Try to retrieve it
        try:
            retrieved = client.data_object.get_by_id(result, class_name='DaoCall')
            if retrieved:
                print(f"  ✓ Successfully retrieved test artifact")
                props = retrieved.get('properties', {})
                print(f"    Project: {props.get('project', 'NOT FOUND')}")
                print(f"    Path: {props.get('path', 'NOT FOUND')}")
                print(f"    Meta: {props.get('meta', 'NOT FOUND')}")
                print(f"    All properties: {list(props.keys())}")
            else:
                print(f"  ⚠ Could not retrieve test artifact")
        except Exception as e:
            print(f"  ⚠ Error retrieving test artifact: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"  ✗ Failed to index test artifact (returned None)")
except Exception as e:
    print(f"  ✗ Error indexing test artifact: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("Diagnostic complete")
print("=" * 80)

