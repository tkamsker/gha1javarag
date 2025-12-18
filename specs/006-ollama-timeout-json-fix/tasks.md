# Tasks: Feature 006 - Ollama Timeout and JSON Parsing Fix

## Setup Phase

- [X] T001: Create feature branch `006-ollama-timeout-json-fix`
- [X] T002: Create feature specification document
- [ ] T003: Review specification with stakeholders

## Phase 1: Configuration Updates

- [ ] T010: Add `ollama_read_timeout` property to `src/codeindex/utils/config.py` (default 240s)
- [ ] T011: Add `ollama_connect_timeout` property to `src/codeindex/utils/config.py` (default 10s)
- [ ] T012: Update `.env.example` with new timeout configuration examples
- [ ] T013: Add timeout configuration to README.md documentation

## Phase 2: OllamaClient Enhancements

- [ ] T020: Add `connect_timeout` and `read_timeout` parameters to `OllamaClient.__init__`
- [ ] T021: Update httpx.Timeout initialization to use instance timeout values
- [ ] T022: Add initialization logging for timeout values and model name
- [ ] T023: Implement `_clean_json_response()` method in OllamaClient
  - Strip markdown code fences (```json...```)
  - Remove trailing commas before closing braces/brackets
  - Strip leading/trailing whitespace
- [ ] T024: Update `extract_semantics()` to use `_clean_json_response()`
- [ ] T025: Improve error logging in `extract_semantics()` with response preview (500 chars)
- [ ] T026: Update `create_ollama_client()` convenience function to pass config timeouts

## Phase 3: DatabaseAnalyzer Improvements

- [ ] T030: Update `_extract_entity_with_llm()` to use `_clean_json_response()`
- [ ] T031: Improve JSON parse error logging with file context and response preview
- [ ] T032: Enhance required field validation error messages with file context
- [ ] T033: Change validation success log from DEBUG to INFO level (✓ Extracted entity: ...)

## Phase 4: CLI Integration

- [ ] T040: Update `src/codeindex/cli/prd.py` database command to pass config timeouts
- [ ] T041: Update `src/codeindex/cli/prd.py` backend command to pass config timeouts
- [ ] T042: Update `src/codeindex/cli/prd.py` frontend command to pass config timeouts
- [ ] T043: Update any other CLI commands using OllamaClient (search codebase)

## Phase 5: Testing

- [ ] T050: Add unit test for `OllamaClient` configurable timeouts
- [ ] T051: Add unit test for `_clean_json_response()` with markdown code fences
- [ ] T052: Add unit test for `_clean_json_response()` with trailing commas
- [ ] T053: Add unit test for `_clean_json_response()` with whitespace issues
- [ ] T054: Add unit test for JSON parse fallback behavior
- [ ] T055: Update existing OllamaClient tests to use new parameters
- [ ] T056: Add integration test with malformed JSON samples
- [ ] T057: Run full test suite and ensure all tests pass

## Phase 6: Production Validation

- [ ] T060: Test with actual problematic DAO files from production logs
- [ ] T061: Run `./step2.sh cuco-ui-admin` and verify reduced errors
- [ ] T062: Measure success rate improvement (target >90%)
- [ ] T063: Verify timeout behavior with slow/complex files
- [ ] T064: Check PRD output quality for completeness

## Phase 7: Documentation

- [ ] T070: Update README.md with new timeout configuration section
- [ ] T071: Update CLAUDE.md troubleshooting section with JSON parsing guidance
- [ ] T072: Document JSON cleaning behavior in code comments
- [ ] T073: Add production troubleshooting guide for timeout issues

## Phase 8: Code Review and Merge

- [ ] T080: Self-review all changes
- [ ] T081: Run linting and code quality checks
- [ ] T082: Create pull request with detailed description
- [ ] T083: Address review feedback
- [ ] T084: Merge to main branch
- [ ] T085: Tag release version

## Dependencies

- T020-T026 must complete before T030-T033 (OllamaClient changes needed first)
- T030-T033 must complete before T040-T043 (DatabaseAnalyzer changes needed first)
- T010-T043 must complete before T050-T057 (implementation before testing)
- T050-T057 must pass before T060-T064 (tests must pass before production validation)

## Parallel Execution

Tasks within the same phase can be executed in parallel:
- Phase 1: T010, T011, T012, T013 [P]
- Phase 2: T023, T024, T025 can be done in parallel after T020-T022 [P]
- Phase 4: T040, T041, T042, T043 [P]
- Phase 5: T050-T056 [P]
- Phase 7: T070, T071, T072, T073 [P]

## Estimated Effort

- Setup: 0.5 hours (complete)
- Phase 1: 0.5 hours
- Phase 2: 2 hours
- Phase 3: 1 hour
- Phase 4: 0.5 hours
- Phase 5: 2 hours
- Phase 6: 1 hour
- Phase 7: 0.5 hours
- Phase 8: 1 hour

**Total: ~9 hours**

## Success Criteria

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Production DAO files process with >90% success rate
- [ ] Timeout errors reduced to <7%
- [ ] JSON parse errors reduced to <4%
- [ ] No regression in processing time for successful requests
- [ ] Documentation updated
- [ ] Code reviewed and merged
