## Summary

Refactored the search to handle BM25 not respecting where clauses.

### Changes

1. Result validation (`src/store/weaviate_client.py`)
   - Filters out results that don't match the project filter
   - Logs warnings when wrong projects are found
   - Counts filtered results

2. Increased limit for BM25 with project filter
   - When using BM25 with a project filter, increases limit by 3x
   - Compensates for BM25 potentially returning wrong projects
   - After filtering, still returns the requested number of results

3. Better logging (`src/cli.py` and `src/store/weaviate_client.py`)
   - INFO-level logging to see what's happening
   - Logs how many results were found and filtered
   - Better error messages

### Test

```bash
# Test with logging to see what's happening
python main.py search --query 'dao' --project 'cuco-core'
```

The search should now:
1. Try BM25 first
2. Validate results and filter out wrong projects
3. If enough valid results, return them
4. If not, try vector search or simple query
5. Log what's happening at each step

The validation ensures correctness even if Weaviate's where clause doesn't work perfectly with BM25. This is a workaround for a potential Weaviate issue where BM25 ranking can return results that don't match the where clause filter.

Run the search again and check the logs to see what's happening.