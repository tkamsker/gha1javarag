
## Summary

Refactored the search method based on the diagnostic results.

### Changes

1. Simplified search method (`src/store/weaviate_client.py`)
   - Tries BM25 first (known to work)
   - Falls back to vector search if BM25 fails
   - Falls back to a simple query if both fail
   - Clearer error handling and logging

2. Fixed statistics query (`weaviate_stats.py`)
   - Simplified query logic
   - Better fallback handling

### Test the fix

```bash
# Test project filter
python test_project_filter.py

# Test actual search
python main.py search --query 'dao' --project 'cuco-core'
```

### Expected results

- Search should work with project filter
- BM25 search used by default
- Better error messages if something fails
- Statistics should show correct counts

The refactored search method is simpler and more reliable. It tries BM25 first (which the diagnostic confirmed works), then falls back to other methods if needed.

Note: The `meta` field isn't being stored because the artifacts being indexed don't have a `meta` field. This doesn't affect search functionality, but if you need metadata, ensure artifacts include a `meta` field during indexing.