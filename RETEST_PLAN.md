# Retest Plan - Production Fix Validation

**Date**: 2026-01-08  
**Fix Applied**: Phase 1 - Output Directory Issue (CRITICAL)  
**Status**: Ready for Testing

---

## Summary of Fixes Applied

### ✅ Fix 1.1: Updated `production-requirements-generation.sh`
- Changed to use absolute paths based on script directory
- Added explicit creation of `prd` subdirectory before PRD generation
- Ensures script works regardless of current working directory

### ✅ Fix 1.2: Enhanced `prd.py` Directory Validation
- Added better error handling with OSError-specific handling
- Improved error messages showing absolute paths and current working directory
- Added explicit parent directory creation before output directory

---

## Pre-Test Checklist

Before running the retest, verify:

- [ ] **Weaviate is running**: `docker ps | grep weaviate`
- [ ] **Ollama is running**: `curl http://localhost:11434/api/tags` (or check your Ollama endpoint)
- [ ] **Virtual environment is activated**: `source .venv/bin/activate`
- [ ] **Codeindex is installed**: `codeindex --version`
- [ ] **Source directory exists**: Verify `/mnt/cucocalcai/cuco-master/cuco-ui-admin` exists (or your test path)
- [ ] **Disk space available**: `df -h` (ensure sufficient space for output)

---

## Test Steps

### Step 1: Quick Validation Test (5 minutes)

**Purpose**: Verify the output directory fix works without running full pipeline

**Commands**:
```bash
cd /Users/thomaskamsker/Documents/Atom/vron.one/playground/Iteration20/gha1javarag

# Test directory creation
./production-requirements-generation.sh cuco-ui-admin /mnt/cucocalcai/cuco-master/cuco-ui-admin
```

**Expected Results**:
- ✅ Script starts without errors
- ✅ Output directory is created: `output/cuco-ui-admin/prd/`
- ✅ No "Cannot write to output directory" errors
- ✅ Both services and frontend PRD processes start

**Validation**:
```bash
# Check if directory was created
ls -la output/cuco-ui-admin/prd/

# Check logs for directory creation messages
tail -20 logs/log_cuco-ui-admin_services_prd_*.log | grep -i "output\|directory"
tail -20 logs/log_cuco-ui-admin_frontend_prd_*.log | grep -i "output\|directory"
```

**If this fails**: Check error messages - they should now show absolute paths and current working directory for debugging.

---

### Step 2: Full Pipeline Test (30-60 minutes)

**Purpose**: Run complete pipeline to verify end-to-end functionality

**Prerequisites**:
- Step 1 passed successfully
- Weaviate and Ollama are running
- Sufficient disk space

**Commands**:
```bash
cd /Users/thomaskamsker/Documents/Atom/vron.one/playground/Iteration20/gha1javarag

# Run full production pipeline
./production-requirements-generation.sh cuco-ui-admin /mnt/cucocalcai/cuco-master/cuco-ui-admin
```

**Expected Results**:
- ✅ Step 1 (Pipeline): Completes successfully (discover → extract → index)
- ✅ Step 2 (Services PRD): Completes with exit code 0
- ✅ Step 2 (Frontend PRD): Completes with exit code 0
- ✅ Final success message displayed
- ✅ PRD files generated: `output/cuco-ui-admin/prd/services_prd.md` and `frontend_prd.md`

**Validation Commands**:
```bash
# Check exit code (should be 0)
echo $?

# Verify PRD files exist
ls -lh output/cuco-ui-admin/prd/*.md

# Check file sizes (should be > 0)
wc -l output/cuco-ui-admin/prd/services_prd.md
wc -l output/cuco-ui-admin/prd/frontend_prd.md

# Verify no output directory errors in logs
grep -i "output.*directory\|cannot write" logs/log_cuco-ui-admin_*_prd_*.log
```

---

### Step 3: Error Scenario Test (Optional - 5 minutes)

**Purpose**: Verify error messages are helpful when directory creation fails

**Test**: Run with insufficient permissions (if possible)

**Commands**:
```bash
# Create a read-only directory and try to write to it
mkdir -p /tmp/test_readonly
chmod 555 /tmp/test_readonly

# Try to run PRD generation pointing to read-only location
# (This should fail gracefully with helpful error message)
codeindex prd services --project cuco-ui-admin --output-dir /tmp/test_readonly/prd
```

**Expected Results**:
- ✅ Clear error message showing absolute path
- ✅ Current working directory shown in error
- ✅ Exit code 5 (OUTPUT_DIR_ERROR)
- ✅ Helpful error details

**Cleanup**:
```bash
chmod 755 /tmp/test_readonly
rm -rf /tmp/test_readonly
```

---

## Success Criteria

The fix is successful if:

1. ✅ **No Exit Code 5 Errors**: Services PRD generation completes successfully
2. ✅ **Directory Creation**: `output/cuco-ui-admin/prd/` is created automatically
3. ✅ **Absolute Paths**: Error messages (if any) show absolute paths
4. ✅ **Both PRDs Generated**: Both services and frontend PRD files are created
5. ✅ **Logs Clean**: No "Cannot write to output directory" errors in logs

---

## Failure Analysis

If the test fails, check:

### Issue: Still getting Exit Code 5

**Check**:
1. Verify script is using absolute paths:
   ```bash
   grep "SCRIPT_DIR\|OUTPUT_DIR" production-requirements-generation.sh
   ```

2. Check current working directory in error message:
   ```bash
   grep -A 5 "Current working directory" logs/log_cuco-ui-admin_services_prd_*.log
   ```

3. Verify directory permissions:
   ```bash
   ls -ld output/cuco-ui-admin/prd/
   ```

**Possible Causes**:
- Script not updated correctly
- Insufficient disk space
- Permission issues
- Path contains special characters

### Issue: Directory created but PRD generation fails

**Check**:
1. Look for other errors in logs:
   ```bash
   grep -i "error\|exception\|failed" logs/log_cuco-ui-admin_services_prd_*.log | tail -20
   ```

2. Verify Weaviate connection:
   ```bash
   codeindex status
   ```

3. Check Ollama connection:
   ```bash
   curl http://localhost:11434/api/tags
   ```

---

## Monitoring During Test

While the test is running, monitor:

1. **Process Status**:
   ```bash
   ps aux | grep codeindex
   ```

2. **Directory Creation**:
   ```bash
   watch -n 5 'ls -la output/cuco-ui-admin/prd/ 2>/dev/null || echo "Directory not created yet"'
   ```

3. **Log Growth**:
   ```bash
   tail -f logs/log_cuco-ui-admin_services_prd_*.log
   tail -f logs/log_cuco-ui-admin_frontend_prd_*.log
   ```

4. **Disk Usage**:
   ```bash
   watch -n 10 'du -sh output/cuco-ui-admin/prd/'
   ```

---

## Post-Test Validation

After successful test:

1. **Verify Output Files**:
   ```bash
   find output/cuco-ui-admin/prd -type f -name "*.md" -exec ls -lh {} \;
   find output/cuco-ui-admin/prd -type f -name "*.json" | wc -l
   ```

2. **Check Log Summary**:
   ```bash
   echo "=== Services PRD Log Summary ==="
   tail -50 logs/log_cuco-ui-admin_services_prd_*.log | grep -E "SUCCESS|ERROR|Complete|Failed"
   
   echo "=== Frontend PRD Log Summary ==="
   tail -50 logs/log_cuco-ui-admin_frontend_prd_*.log | grep -E "SUCCESS|ERROR|Complete|Failed"
   ```

3. **Verify No Directory Errors**:
   ```bash
   echo "=== Directory Errors Check ==="
   grep -i "output.*directory\|cannot write" logs/log_cuco-ui-admin_*_prd_*.log || echo "No directory errors found - SUCCESS!"
   ```

---

## Next Steps After Successful Test

Once Phase 1 fix is validated:

1. **Document Results**: Update PRODUCTION_FIX_PLAN.md with test results
2. **Proceed to Phase 2**: Fix Weaviate schema normalization (HIGH priority)
3. **Monitor Production**: Deploy fix and monitor next production run
4. **Plan Phase 3**: Address timeout issues (MEDIUM priority)

---

## Rollback Plan

If the fix causes issues:

1. **Revert Changes**:
   ```bash
   git checkout HEAD -- production-requirements-generation.sh
   git checkout HEAD -- src/codeindex/cli/prd.py
   ```

2. **Manual Workaround** (temporary):
   ```bash
   # Create output directory manually before running
   mkdir -p output/cuco-ui-admin/prd
   ./production-requirements-generation.sh cuco-ui-admin /mnt/cucocalcai/cuco-master/cuco-ui-admin
   ```

---

## Test Report Template

After running tests, document results:

```
Test Date: ___________
Tester: ___________

Step 1 (Quick Validation):
[ ] PASSED - Directory created successfully
[ ] FAILED - Error: ___________

Step 2 (Full Pipeline):
[ ] PASSED - Both PRDs generated successfully
[ ] FAILED - Error: ___________

Exit Codes:
- Services PRD: _____
- Frontend PRD: _____

Output Files:
- services_prd.md: [ ] EXISTS [ ] MISSING (size: _____)
- frontend_prd.md: [ ] EXISTS [ ] MISSING (size: _____)

Issues Found:
1. ___________
2. ___________

Recommendation:
[ ] PROCEED to Phase 2
[ ] NEEDS MORE FIXES
[ ] ROLLBACK REQUIRED
```

---

## Notes

- The fix ensures output directory is created relative to script location, not current working directory
- Error messages now include absolute paths and current working directory for easier debugging
- The script will work correctly even when called from different directories or via cron/scheduler

