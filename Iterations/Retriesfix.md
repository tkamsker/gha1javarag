Perfect! The timeout handling improvements have been successfully implemented, tested, and pushed. Here's what was accomplished:

  Summary of Changes

  Problem Addressed: Extraction was taking 5+ minutes per file with Ollama timeouts at 300s, resulting in very slow overall processing (only 10 files in 7 minutes).

  Solution Implemented (Option 2: Timeout Handling):

  1. Reduced Ollama timeout from 300s to 60s in ollama_client.py:
    - Files that take longer than 60s are now immediately skipped
    - Prevents long waits for complex/problematic files
  2. Updated retry logic in ollama_client.py:
    - Modified @retry decorator to exclude TimeoutError from retries
    - Only retries on ConnectionError and HTTPStatusError
    - Prevents 3 retry attempts on timeouts (was up to 900s per file)
  3. Enhanced timeout handling in extraction.py:
    - Added specific TimeoutError handler that logs warning and skips file
    - Modified _create_fallback_semantic() to accept timeout flag
    - Timed-out files are marked with "(TIMEOUT)" prefix for easy identification
    - Falls back to structural-only analysis (no AI semantics)

  Performance Impact:
  - Before: 300s timeout + 3 retries = up to 900 seconds per slow file
  - After: 60s timeout, no retries = max 60 seconds per slow file
  - Expected improvement: 15x faster extraction for slow/complex files

  Testing: All 644 tests passed with no regressions introduced.

  Git: Changes committed (f51e1a0) and pushed to remote repository.

  The extraction pipeline should now process files much more efficiently, skipping problematic files that would have previously caused long delays.