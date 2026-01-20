# Indexing Fix - Zero Artifacts Issue

## Problem Summary

You ran two nohup commands to index `cuco-ui-admin` and `cuco-ui-app`:

```bash
nohup ./run.sh /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-admin > "log_run_cuco-ui-admin_$(date +'%Y-%m-%d_%H-%M-%S').log" 2>&1 &
nohup ./run.sh /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-app > "log_run_cuco-ui-app_$(date +'%Y-%m-%d_%H-%M-%S').log" 2>&1 &
```

However, `codeindex status` shows both projects with **0 artifacts**.

## Root Causes

1. **Incorrect Script Usage**: The `run.sh` script expects TWO arguments:
   - First argument: `PROJECT_NAME` (e.g., `cuco-ui-admin`)
   - Second argument: `SOURCE_DIR` (e.g., `/mnt/cucocalcai/...`)

   Your command only passed ONE argument (the full path), causing:
   - `PROJECT_NAME` to be set to the full path string (with slashes and special chars)
   - `SOURCE_DIR` to fall back to `.env` value (wrong directory)

2. **Path Validation**: The path `/mnt/cucocalcai/...` may not exist on your system or may require special mounting.

3. **Missing Pipeline Artifacts**: No discovery or extraction files were created for these projects.

## Solution

I've created three helper scripts to diagnose and fix the issue:

### 1. Diagnose the Problem

```bash
./diagnose_indexing.sh cuco-ui-admin /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-admin
```

This script checks:
- Source directory exists and contains Java/JSP files
- Pipeline artifacts (discovery/extraction files)
- Weaviate and Ollama connectivity
- Current project status in Weaviate
- Recent log files for errors

### 2. Fix the Indexing

```bash
./fix_indexing.sh cuco-ui-admin /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-admin
```

This script:
- Validates source directory and services
- Backs up old pipeline files
- Runs full pipeline: discover → extract → index
- Verifies data in Weaviate
- Reports artifact count

**For both projects:**

```bash
# Fix cuco-ui-admin
./fix_indexing.sh cuco-ui-admin /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-admin

# Fix cuco-ui-app
./fix_indexing.sh cuco-ui-app /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-app
```

### 3. Test the Fix

```bash
./test_indexing_fix.sh cuco-ui-admin /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-admin
```

This runs 10 validation tests:
- Source directory validation
- Discovery file validation
- Extraction file validation
- Weaviate/Ollama connectivity
- Weaviate data validation
- Search functionality
- File content validation
- Project ID format
- Source file discovery

## Correct Usage of run.sh

The correct syntax is:

```bash
./run.sh <PROJECT_NAME> <SOURCE_DIR>
```

**Examples:**

```bash
# Single project mode
./run.sh cuco-ui-admin /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-admin

# Monorepo mode (project is subdirectory of source)
./run.sh backend-api /path/to/monorepo
```

## Running in Background (Correct Way)

If you want to run in background, use the fix script with nohup:

```bash
# Run in background with proper logging
nohup ./fix_indexing.sh cuco-ui-admin /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-admin > fix_cuco-ui-admin.log 2>&1 &

# Check progress
tail -f fix_cuco-ui-admin.log

# Check if still running
ps aux | grep fix_indexing.sh
```

## Expected Results

After running the fix script, you should see:

```bash
$ codeindex status

Indexed Projects: 86
Total Artifacts:  XXXX   # Should be > 92,226

Projects:
----------------------------------------------------------------------

  cuco-ui-admin:2f0368fb
  Name: cuco-ui-admin
  Artifacts: 5,234        # Should be > 0
  Last Indexed: 2026-01-20 08:50:00 (just now)

  cuco-ui-app:41637def
  Name: cuco-ui-app
  Artifacts: 3,891        # Should be > 0
  Last Indexed: 2026-01-20 08:55:00 (just now)
```

## Troubleshooting

### Path doesn't exist

If the path `/mnt/cucocalcai/...` doesn't exist:

1. **Verify the path on your Linux server:**
   ```bash
   ls -ld /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-admin
   ```

2. **Check if it needs mounting:**
   ```bash
   df -h | grep cucocalcai
   ```

3. **Use the correct path for your system:**
   ```bash
   # Find the actual location
   find /mnt -name "cuco-ui-admin" -type d 2>/dev/null
   ```

### Services not running

```bash
# Start Weaviate
./docker-weaviate.sh start

# Start Ollama
ollama serve

# Verify
curl http://localhost:8080/v1/meta
curl http://localhost:11434/api/tags
```

### Still 0 artifacts after fix

1. **Check the fix log for errors:**
   ```bash
   cat fix_cuco-ui-admin.log | grep -i error
   ```

2. **Verify discovery found files:**
   ```bash
   wc -l data/discovery-cuco-ui-admin.jsonl
   ```

3. **Check extraction succeeded:**
   ```bash
   wc -l data/extraction-cuco-ui-admin.jsonl
   ```

4. **Look for timeout issues:**
   ```bash
   grep -i timeout fix_cuco-ui-admin.log
   ```

### Extraction is too slow

If extraction takes too long, you can skip AI semantic analysis:

```bash
# Faster extraction (structural analysis only)
codeindex extract --skip-ai --inventory data/discovery-cuco-ui-admin.jsonl --output data/extraction-cuco-ui-admin.jsonl
```

## Quick Reference

| Task | Command |
|------|---------|
| Diagnose issue | `./diagnose_indexing.sh <project> <source>` |
| Fix indexing | `./fix_indexing.sh <project> <source>` |
| Test fix | `./test_indexing_fix.sh <project> <source>` |
| Check status | `codeindex status` |
| Search project | `codeindex search "query" --project <project>` |
| Full pipeline | `./run.sh <project> <source>` |

## Files Created

- `diagnose_indexing.sh` - Diagnostic script
- `fix_indexing.sh` - Re-indexing script
- `test_indexing_fix.sh` - Validation test script
- `INDEXING_FIX_README.md` - This documentation

## Next Steps

1. **Run diagnostics** to understand the current state:
   ```bash
   ./diagnose_indexing.sh cuco-ui-admin /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-admin
   ```

2. **Fix the indexing** for both projects:
   ```bash
   ./fix_indexing.sh cuco-ui-admin /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-admin
   ./fix_indexing.sh cuco-ui-app /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-app
   ```

3. **Validate** the fix worked:
   ```bash
   ./test_indexing_fix.sh cuco-ui-admin /mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-admin
   ```

4. **Verify in Weaviate**:
   ```bash
   codeindex status
   ```

5. **Test search functionality**:
   ```bash
   codeindex search "user" --project cuco-ui-admin --limit 5
   ```
