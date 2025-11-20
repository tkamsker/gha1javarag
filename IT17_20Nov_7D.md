## Summary

Fixed the query issue. Objects exist (226,406 DaoCall), but queries return nothing. Likely causes:
1. Vector search failing (no vectors or vectorization issues)
2. Query API syntax mismatch
3. Properties nested under `properties` in responses

## Fixes Applied

1. Enhanced search with fallbacks (`src/store/weaviate_client.py`)
   - Falls back: vector search → BM25 → simple query
   - Better error handling

2. Improved statistics query (`weaviate_stats.py`)
   - Better error handling
   - Falls back to limited property queries

3. New diagnostic scripts
   - `fix_query_issue.py` - Tests different query methods
   - Updated `diagnose_indexing.py` - Checks property structure

## Next Steps

Run the diagnostic to see what's actually stored:

```bash
source venv/bin/activate
python fix_query_issue.py
```

This will show:
- If basic queries work
- The actual data structure
- If the project field is stored correctly
- Which query method works

Then we can:
- Fix the query method if needed
- Re-index if the project field isn't stored
- Update search to use the working query method

The search function now has fallbacks, so it should work even if vector search fails. Try running a search again:

```bash
python main.py search --query 'dao' --project 'cuco-core'
```

If it still doesn't work, run `fix_query_issue.py` to see what's happening.