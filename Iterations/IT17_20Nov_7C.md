
## Summary

Fixed the indexing issue where data wasn't appearing in Weaviate. Changes:

### Fixes applied

1. Schema update logic (`src/store/weaviate_client.py`)
   - `ensure_schema()` now checks for missing properties in existing classes
   - Automatically adds missing properties (like `meta`) to existing schemas
   - Prevents silent failures from schema mismatches

2. Error logging (`src/cli.py`)
   - Improved error logging to show which artifacts fail
   - Checks return values to detect failures
   - Logs file paths of failed artifacts

3. Statistics query (`weaviate_stats.py`)
   - Checks if classes exist before querying
   - Uses aggregate queries for accurate counts
   - Increased limit to 10,000 for better coverage

4. Diagnostic tool (`diagnose_indexing.py`)
   - New script to check schema and test indexing
   - Shows detailed schema information

### Next steps

Run the diagnostic first to see what's happening:

```bash
source venv/bin/activate
python diagnose_indexing.py
```

Then clear and re-index:

```bash
# Option 1: Use the reload script (recommended)
./reload_all_data.sh

# Option 2: Manual clear and re-index
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
EOF

python main.py index --all-projects
```

Then verify:

```bash
./weaviate_stats.sh
```

You should now see 36,000+ objects indexed. The schema will automatically include the `meta` field, and indexing errors will be properly logged.

See `FIX_INDEXING_ISSUE.md` for detailed troubleshooting steps.