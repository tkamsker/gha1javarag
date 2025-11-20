# Fix for Indexing Issue - Data Not Appearing in Weaviate

## Problem

The indexing reported success ("Indexed 36453 artifacts") but `weaviate_stats.sh` shows 0 objects. This indicates a schema mismatch or silent indexing failures.

## Root Causes

1. **Schema Missing `meta` Field**: Existing Weaviate classes may not have the `meta` property, causing indexing to fail silently
2. **Schema Not Updated**: The `ensure_schema()` method only created new classes but didn't update existing ones
3. **Silent Failures**: Indexing errors weren't being logged properly

## Fixes Applied

### 1. ✅ Schema Update Logic

**File**: `src/store/weaviate_client.py`

- Updated `ensure_schema()` to check for missing properties in existing classes
- Automatically adds missing properties (like `meta`) to existing schemas
- Logs when properties are added

### 2. ✅ Better Error Logging

**File**: `src/cli.py`

- Improved error logging in indexing to show which artifacts fail
- Checks return value from `index_artifact()` to detect failures
- Logs file paths of failed artifacts

### 3. ✅ Improved Statistics Query

**File**: `weaviate_stats.py`

- Checks if classes exist before querying
- Uses aggregate queries to get accurate counts
- Increased limit from 1000 to 10000 for better coverage
- Shows total counts per class

### 4. ✅ Diagnostic Script

**File**: `diagnose_indexing.py`

- New diagnostic tool to check schema and indexing
- Tests sample indexing to verify it works
- Shows detailed schema information

## Step-by-Step Fix

### Step 1: Run Diagnostic

```bash
source venv/bin/activate
python diagnose_indexing.py
```

This will show:
- Which classes exist
- Which properties they have
- Current object counts
- Test if indexing works

### Step 2: Ensure Schema is Updated

The schema will be automatically updated when you run indexing, but you can force it:

```bash
python3 << 'EOF'
from store.weaviate_client import WeaviateClient
wc = WeaviateClient(ensure_schema=True)
print("Schema ensured - missing properties should be added")
EOF
```

### Step 3: Clear and Re-index

```bash
# Clear Weaviate
python3 << 'EOF'
from store.weaviate_client import WeaviateClient
wc = WeaviateClient(ensure_schema=False)
classes = ['DaoCall', 'IbatisStatement', 'BackendDoc', 'JspForm', 
           'DbTable', 'GwtModule', 'GwtUiBinder', 'GwtActivityPlace',
           'GwtEndpoint', 'JsArtifact']
for class_name in classes:
    try:
        if wc._client.schema.exists(class_name):
            wc._client.schema.delete_class(class_name)
            print(f"Deleted: {class_name}")
    except Exception as e:
        print(f"Error deleting {class_name}: {e}")
EOF

# Re-index with schema ensure
python main.py index --all-projects
```

### Step 4: Verify

```bash
./weaviate_stats.sh
```

You should now see:
- Total Objects: 36,000+
- All classes have data
- Projects are listed

## Quick Fix Script

Or use the reload script which now includes schema updates:

```bash
./reload_all_data.sh
```

## Expected Results After Fix

- ✅ Schema includes `meta` field for all classes
- ✅ Indexing logs show success/failure for each artifact
- ✅ Statistics show 36,000+ objects
- ✅ Searches return results

## Troubleshooting

### If Still Showing 0 Objects

1. **Check Weaviate is running**:
   ```bash
   curl http://localhost:8080/v1/meta
   ```

2. **Check schema**:
   ```bash
   python diagnose_indexing.py
   ```

3. **Check indexing logs**:
   Look for error messages in the indexing output

4. **Try manual test**:
   ```bash
   python3 << 'EOF'
   from store.weaviate_client import WeaviateClient
   wc = WeaviateClient(ensure_schema=True)
   test = {'project': 'test', 'path': '/test', 'text': 'test', 'meta': {'test': True}}
   result = wc.index_artifact('DaoCall', test)
   print(f"Indexed: {result}")
   EOF
   ```

### If Schema Update Fails

You may need to delete and recreate classes:

```bash
python3 << 'EOF'
from store.weaviate_client import WeaviateClient
wc = WeaviateClient(ensure_schema=False)
classes = ['DaoCall', 'IbatisStatement', 'BackendDoc', 'JspForm', 
           'DbTable', 'GwtModule', 'GwtUiBinder', 'GwtActivityPlace',
           'GwtEndpoint', 'JsArtifact']
for class_name in classes:
    try:
        if wc._client.schema.exists(class_name):
            wc._client.schema.delete_class(class_name)
            print(f"Deleted: {class_name}")
    except:
        pass

# Now recreate with ensure_schema
wc2 = WeaviateClient(ensure_schema=True)
print("Schema recreated")
EOF
```

## Files Modified

1. `src/store/weaviate_client.py` - Schema update logic
2. `src/cli.py` - Better error logging
3. `weaviate_stats.py` - Improved querying
4. `diagnose_indexing.py` - New diagnostic tool

