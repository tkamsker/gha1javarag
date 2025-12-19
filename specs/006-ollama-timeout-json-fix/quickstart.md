# Quick Fix Validation Guide

**Feature**: 006-ollama-timeout-json-fix
**Purpose**: Validate the two bug fixes in ollama_client.py and prd.py

## Prerequisites

- Python 3.8+ environment activated
- Repository cloned and at project root
- pytest installed (`pip install pytest`)
- Production test data available (optional for integration tests)

---

## Fix 1: ollama_client.py - READ_TIMEOUT NameError

### Verify Current Bug

```bash
# Check for problematic line
grep -n "READ_TIMEOUT" src/codeindex/services/ollama_client.py

# Expected output (BEFORE fix):
# 280:                self.logger.warning(f"Ollama timeout after {READ_TIMEOUT}s: {e}")
```

### Apply Fix

**File**: `src/codeindex/services/ollama_client.py`
**Line**: 280

**Change FROM**:
```python
self.logger.warning(f"Ollama timeout after {READ_TIMEOUT}s: {e}")
```

**Change TO**:
```python
self.logger.warning(f"Ollama timeout after {self.read_timeout}s: {e}")
```

### Verify Fix Applied

```bash
# Check for correct reference
grep -n "self.read_timeout" src/codeindex/services/ollama_client.py | grep 280

# Expected output (AFTER fix):
# 280:                self.logger.warning(f"Ollama timeout after {self.read_timeout}s: {e}")
```

### Test Fix

```bash
# Run unit tests
pytest tests/unit/test_ollama_client.py -v

# Expected: All tests pass, no NameError
```

---

## Fix 2: prd.py - validation_rules AttributeError

### Verify Current Bug

```bash
# Check for problematic lines
grep -A5 "for rule in form.validation_rules:" src/codeindex/cli/prd.py

# Expected output (BEFORE fix):
# 1660:                for rule in form.validation_rules:
# 1661:                    lines.append(f"- **{rule.field}** ({rule.rule_type}): {rule.message}")
```

### Apply Fix

**File**: `src/codeindex/cli/prd.py`
**Lines**: 1657-1662

**Change FROM**:
```python
            # Validation rules
            if form.validation_rules:
                lines.append("**Validation Rules:**")
                lines.append("")
                for rule in form.validation_rules:
                    lines.append(f"- **{rule.field}** ({rule.rule_type}): {rule.message}")
                lines.append("")
```

**Change TO**:
```python
            # Validation rules
            # TODO: validation_rules contains rule IDs (strings), not rule objects
            # To display rules, need to load rule JSON files from output_dir/frontend/rules/
            # For now, skip this section to prevent AttributeError
            # if form.validation_rules:
            #     lines.append("**Validation Rules:**")
            #     lines.append("")
            #     for rule in form.validation_rules:
            #         lines.append(f"- **{rule.field}** ({rule.rule_type}): {rule.message}")
            #     lines.append("")
```

### Verify Fix Applied

```bash
# Check that lines are commented out
grep -A5 "# TODO: validation_rules contains" src/codeindex/cli/prd.py

# Expected output (AFTER fix):
# Shows commented-out lines with TODO
```

### Test Fix

```bash
# Run unit tests
pytest tests/unit/test_prd.py -v

# Expected: All tests pass, no AttributeError
```

---

## Integration Test (Optional)

### Prerequisites

1. Ollama running: `ollama serve` (in separate terminal)
2. Weaviate running: `./docker-weaviate.sh status` (should show running)
3. Production extraction file available (or generate one)

### Run Frontend PRD Generation

```bash
# Generate PRD with production data
codeindex prd frontend \
  --extraction-file output/cuco-ui-admin/extraction-results.jsonl \
  --output output/test-prd-fix \
  --quiet

# Check exit code
echo $?
# Expected: 0 (success)
```

### Verify Output

```bash
# Check that PRD was generated
ls -lh output/test-prd-fix/prd/frontend_prd.md

# Expected: File exists, >10KB in size

# Check for errors in log (if not --quiet)
# Expected: No NameError, no AttributeError

# View PRD content
head -50 output/test-prd-fix/prd/frontend_prd.md

# Expected: Markdown header, forms listed, no errors
```

### Cleanup

```bash
rm -rf output/test-prd-fix
```

---

## Full Test Suite

### Run All Tests

```bash
# Run all unit tests
pytest tests/unit/ -v

# Expected: All tests pass (630+ tests)

# Run integration tests
pytest tests/integration/ -v

# Expected: All tests pass (42+ tests)
```

### Check Test Coverage

```bash
# Generate coverage report
pytest --cov=src/codeindex --cov-report=term-missing tests/

# Expected: No decrease in coverage percentages
```

---

## Troubleshooting

### Issue: Tests fail with import errors

**Solution**:
```bash
# Install package in development mode
pip install -e .

# Run tests again
pytest tests/unit/test_ollama_client.py -v
```

### Issue: Integration test fails with "Ollama not available"

**Solution**:
```bash
# Start Ollama service
ollama serve

# In another terminal, verify
curl http://localhost:11434/api/tags

# Expected: JSON response with model list
```

### Issue: Integration test fails with "Weaviate not available"

**Solution**:
```bash
# Start Weaviate container
./docker-weaviate.sh start

# Verify status
./docker-weaviate.sh status

# Expected: Container running, health check OK
```

### Issue: PRD generation crashes with different error

**Solution**:
```bash
# Check detailed error log
codeindex prd frontend \
  --extraction-file output/cuco-ui-admin/extraction-results.jsonl \
  --output output/test-prd-fix

# Review error details, compare with production log
```

---

## Validation Checklist

- [ ] Fix 1: `READ_TIMEOUT` changed to `self.read_timeout` in ollama_client.py:280
- [ ] Fix 2: validation_rules section commented out in prd.py:1657-1662
- [ ] Unit tests pass for ollama_client
- [ ] Unit tests pass for prd
- [ ] Integration test completes (if production data available)
- [ ] Frontend PRD generated successfully
- [ ] No NameError in logs
- [ ] No AttributeError in logs
- [ ] Test coverage maintained
- [ ] No regressions in existing tests

---

## Next Steps

After validation:

1. **Commit changes**:
   ```bash
   git add src/codeindex/services/ollama_client.py src/codeindex/cli/prd.py
   git commit -m "fix: resolve NameError and AttributeError in PRD generation

   - Fix NameError in ollama_client.py:280 (READ_TIMEOUT → self.read_timeout)
   - Fix AttributeError in prd.py:1661 (skip validation_rules section)
   - validation_rules contains rule IDs (strings), not objects
   - Add TODO for future enhancement to load rules by ID

   Resolves production errors in cuco-ui-admin PRD generation"
   ```

2. **Push to branch**:
   ```bash
   git push origin 006-ollama-timeout-json-fix
   ```

3. **Run full pipeline test** (optional):
   ```bash
   ./run.sh cuco-ui-admin
   # Verify complete pipeline works end-to-end
   ```

4. **Update CLAUDE.md** with troubleshooting notes

5. **Create pull request** for review

---

## Production Deployment

After merging:

1. Pull latest code on production server
2. Restart services (if needed)
3. Run step2.sh with cuco-ui-admin project
4. Monitor logs for errors
5. Verify PRD generated successfully

**Expected Results**:
- No NameError in logs
- No AttributeError in logs
- Frontend PRD generated: `output/cuco-ui-admin-prd/prd/frontend_prd.md`
- Forms and components documented
- validation_rules section skipped (no crash)

---

**End of Quick Fix Validation Guide**
