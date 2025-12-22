# Quickstart Guide: GWT Navigation Analysis and Error Fixes

**Feature**: 007-gwt-navigation-and-error-fixes
**Purpose**: Step-by-step validation and testing guide

## Quick Validation

```bash
# 1. Run full pipeline on test codebase
./run.sh cuco-ui-admin

# 2. Check for timeout errors (should be 0)
grep -c "timeout" logs/extraction.log

# 3. Check FK validation errors (should be 0)
codeindex status --project cuco-ui-admin | grep "FK validation"

# 4. Check GWT component discovery (should be >90%)
codeindex status --project cuco-ui-admin | grep "GWT components"
```

## Test Scenarios

### Scenario 1: Timeout Handling
- Test adaptive timeout calculation
- Test exponential backoff retries
- Test structural fallback
- Verify zero timeout failures on 539 files

### Scenario 2: FK Extraction
- Test Java @JoinColumn parsing
- Test iBATIS XML parsing
- Test SQL JOIN parsing
- Verify 100% FK accuracy

### Scenario 3: GWT Navigation
- Test index.html/jsp parsing
- Test GWT module traversal
- Test navigation graph building
- Verify >90% component discovery

See full implementation plan in [plan.md](./plan.md) for detailed test steps.
