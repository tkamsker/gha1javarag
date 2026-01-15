# Streamlit Web UI Testing Guide

**Last Updated**: 2026-01-15
**Feature**: 009-streamlit-crewai-web-client
**Status**: Production Ready - All 8 agents connected to Ollama

---

## Overview

This guide provides comprehensive testing instructions for the Streamlit Web UI integrated with the production pipeline data.

## Prerequisites

### 1. Services Running

```bash
# Check all services are healthy
./check-services.sh

# Expected output:
# ✅ Ollama: Connected
# ✅ Weaviate: Connected
# ✅ SQLite: Database exists
# ✅ All services healthy!
```

### 2. Production Data Indexed

```bash
# Run the production pipeline to index your codebase
./production-requirements-generation.sh <project-name> <source-dir>

# Example:
./production-requirements-generation.sh cuco-ui-admin /path/to/source

# Verify data is indexed
./weaviate_stats.py

# Should show:
# - Total artifacts: >0
# - Project count: ≥1
# - Artifact types: GwtPresenter, DaoCall, DbTable, etc.
```

### 3. Environment Configuration

Verify `.env` file has correct settings:
```bash
grep -E "JAVA_SOURCE_DIR|WEAVIATE_URL|OLLAMA" .env

# Should show:
# JAVA_SOURCE_DIR=/path/to/your/source
# WEAVIATE_URL=http://localhost:8080
# OLLAMA_BASE_URL=http://localhost:11434
# OLLAMA_MODEL_NAME=gemma3:12b
```

---

## Launch Streamlit

```bash
# Activate virtual environment
source .venv/bin/activate

# Launch Streamlit web UI
streamlit run src/codeindex/web/app.py

# Access at: http://localhost:8501
```

---

## Test Scenarios

### Test 1: Home Page Navigation

**Steps:**
1. Open http://localhost:8501
2. Verify home page loads without errors
3. Check navigation sidebar shows all pages:
   - 🏠 Home
   - 🔍 Search
   - 💬 Chat
   - 🗂️ Files
   - 🧪 Tests
   - ⚙️ Settings
   - 📊 Workspace

**Expected Result:**
- ✅ Home page displays welcome message
- ✅ All navigation links are visible
- ✅ No errors in console

---

### Test 2: Search Functionality (Real Weaviate Data)

**Purpose**: Verify search returns real artifacts from production pipeline

**Steps:**
1. Navigate to 🔍 Search page
2. Enter query: `"user authentication"`
3. Click Search button

**Expected Results:**
- ✅ Search executes without errors
- ✅ Results display artifacts from Weaviate:
  - Artifact type (GwtPresenter, DaoCall, etc.)
  - File path
  - Summary
  - Confidence score (if available)
- ✅ Execution time displayed (e.g., "42ms")
- ✅ Total results count shown

**Additional Tests:**
- **Test 2a - Project Filter**:
  1. Select project from dropdown
  2. Search again
  3. Verify results are filtered by project

- **Test 2b - Artifact Type Filter**:
  1. Select artifact types (e.g., GwtPresenter, DaoCall)
  2. Search again
  3. Verify only selected types are returned

- **Test 2c - Pagination**:
  1. Search with query that returns many results
  2. Verify pagination controls work
  3. Navigate to page 2, 3, etc.

**Troubleshooting:**
- If no results: Check `./weaviate_stats.py` to verify data is indexed
- If error "Cannot connect to Weaviate": Ensure Weaviate is running (`./docker-weaviate.sh status`)

---

### Test 3: Senior Developer Agent

**Purpose**: Verify AI-powered code explanations with real Ollama LLM

**Steps:**
1. Navigate to 💬 Chat page
2. Select agent: "Senior Developer"
3. Ask question: `"Explain how user authentication works in this codebase"`
4. Submit

**Expected Results:**
- ✅ Agent searches Weaviate for relevant artifacts
- ✅ Response includes:
  - AI-generated explanation (from Ollama)
  - Specific code references
  - Architecture insights
  - Best practices mentioned
- ✅ Citations section shows:
  - File paths
  - Artifact types
  - Confidence scores
- ✅ Follow-up questions suggested (3-4 questions)
- ✅ Execution time displayed

**Additional Questions to Test:**
- "What design patterns are used in this codebase?"
- "Explain the presenter-view architecture"
- "How does dependency injection work here?"

**Troubleshooting:**
- If placeholder response: Agent not connected to Ollama (check commit 5b99f65)
- If error "Cannot connect to Ollama": Ensure `ollama serve` is running
- If timeout: Large files may take longer, check Ollama logs

---

### Test 4: Data Analyst Agent

**Purpose**: Verify database schema and data flow analysis

**Steps:**
1. Navigate to 💬 Chat page
2. Select agent: "Data Analyst"
3. Ask: `"Show me the database schema and table relationships"`
4. Submit

**Expected Results:**
- ✅ Agent searches for DbTable, DaoCall, IbatisStatement artifacts
- ✅ Response includes:
  - List of database tables
  - DAO methods and patterns
  - iBATIS statement count
  - Data flow descriptions
- ✅ Citations to database artifacts
- ✅ Follow-up questions about FKs, queries, indexes

**Additional Questions:**
- "What DAO patterns are used for database access?"
- "Explain the data flow for user registration"
- "What are the foreign key relationships?"

---

### Test 5: Frontend Specialist Agent

**Purpose**: Verify GWT/JSP/JavaScript UI analysis

**Steps:**
1. Navigate to 💬 Chat page
2. Select agent: "Frontend Specialist"
3. Ask: `"Describe the main UI components and navigation flow"`
4. Submit

**Expected Results:**
- ✅ Agent searches for GwtPresenter, GwtView, GwtUiBinder, JspForm
- ✅ Response includes:
  - UI component descriptions
  - Presenter-View bindings
  - Navigation targets
  - Form fields and validations
- ✅ Citations to frontend artifacts
- ✅ Follow-up questions about events, widgets, JSP forms

**Additional Questions:**
- "How does the user login form work?"
- "Explain the GWT MVP pattern in this app"
- "What widgets are used in the main dashboard?"

---

### Test 6: Backend Specialist Agent

**Purpose**: Verify service layer and API analysis

**Steps:**
1. Navigate to 💬 Chat page
2. Select agent: "Backend Specialist"
3. Ask: `"Document the API endpoints and service layer"`
4. Submit

**Expected Results:**
- ✅ Agent searches for BackendDoc, GwtEndpoint, DaoCall
- ✅ Response includes:
  - Service layer descriptions
  - RPC endpoint mappings
  - Business logic flows
  - DAO integration patterns
- ✅ Citations to backend artifacts
- ✅ Follow-up questions about transactions, errors, DTOs

**Additional Questions:**
- "How are RPC services implemented?"
- "What business logic exists in the service layer?"
- "Explain error handling in the backend"

---

### Test 7: PRD Writer Agent

**Purpose**: Verify automated PRD generation

**Steps:**
1. Navigate to 💬 Chat page
2. Select agent: "PRD Writer"
3. Ask: `"Generate a product requirements document for the payment processing feature"`
4. Submit

**Expected Results:**
- ✅ Agent searches all artifact types for comprehensive context
- ✅ Response includes PRD format:
  - **Objectives**: Feature goals
  - **User Stories**: With acceptance criteria
  - **Requirements**: Functional and non-functional
  - **Success Metrics**: Measurable outcomes
- ✅ Citations to relevant artifacts
- ✅ Follow-up questions about scope, priorities, edge cases

**Notes:**
- PRD generation may take 30-60 seconds due to document length
- Temperature set to 0.4 for slightly creative business language

---

### Test 8: Spec-Kit Writer Agent

**Purpose**: Verify technical specification generation

**Steps:**
1. Navigate to 💬 Chat page
2. Select agent: "Spec-Kit Writer"
3. Ask: `"Create a technical specification for the authentication module"`
4. Submit

**Expected Results:**
- ✅ Response includes technical spec format:
  - **Architecture**: System design
  - **Components**: Class/module breakdown
  - **Data Models**: Entity definitions
  - **API Contracts**: Endpoint specifications
  - **Implementation Plan**: Step-by-step tasks
- ✅ Citations to technical artifacts
- ✅ Follow-up questions about design, dependencies, testing

---

### Test 9: Gherkin Test Writer Agent

**Purpose**: Verify BDD test scenario generation

**Steps:**
1. Navigate to 💬 Chat page
2. Select agent: "Gherkin Test Writer"
3. Ask: `"Write Gherkin test scenarios for user login"`
4. Submit

**Expected Results:**
- ✅ Response includes Gherkin format:
  ```gherkin
  Feature: User Login

    Scenario: Successful login with valid credentials
      Given the user is on the login page
      When the user enters valid username "john@example.com"
      And the user enters valid password "SecurePass123"
      And the user clicks the "Login" button
      Then the user should be redirected to the dashboard
      And the user should see a welcome message

    Scenario Outline: Failed login attempts
      Given the user is on the login page
      When the user enters username "<username>"
      And the user enters password "<password>"
      And the user clicks the "Login" button
      Then the user should see error message "<error>"

      Examples:
        | username          | password      | error                     |
        | invalid@email.com | any           | Invalid credentials       |
        | john@example.com  | wrongpass     | Invalid credentials       |
        |                   | SecurePass123 | Username is required      |
  ```
- ✅ Citations to UI and validation artifacts
- ✅ Temperature 0.2 for precise Gherkin syntax

---

### Test 10: Playwright Test Writer Agent

**Purpose**: Verify E2E test automation code generation

**Steps:**
1. Navigate to 💬 Chat page
2. Select agent: "Playwright Test Writer"
3. Ask: `"Generate Playwright tests for the user registration flow"`
4. Submit

**Expected Results:**
- ✅ Response includes Playwright test code:
  ```typescript
  import { test, expect } from '@playwright/test';

  test.describe('User Registration', () => {
    test('should register new user successfully', async ({ page }) => {
      // Navigate to registration page
      await page.goto('/register');

      // Fill registration form
      await page.fill('[data-testid="username-input"]', 'newuser');
      await page.fill('[data-testid="email-input"]', 'newuser@example.com');
      await page.fill('[data-testid="password-input"]', 'SecurePassword123');

      // Submit form
      await page.click('[data-testid="register-button"]');

      // Assert success
      await expect(page).toHaveURL('/dashboard');
      await expect(page.locator('.success-message')).toBeVisible();
    });
  });
  ```
- ✅ Page Object Model pattern used
- ✅ Proper locators (data-testid, CSS selectors)
- ✅ Async/await patterns
- ✅ Temperature 0.2 for precise code

---

### Test 11: Agent Routing

**Purpose**: Verify automatic agent selection based on query keywords

**Steps:**
1. Navigate to 💬 Chat page
2. Keep agent selection as "Auto" (default)
3. Try different questions:
   - "database schema" → Should route to Data Analyst
   - "UI components" → Should route to Frontend Specialist
   - "service layer" → Should route to Backend Specialist
   - "explain code" → Should route to Senior Developer (fallback)

**Expected Results:**
- ✅ Agent is automatically selected based on keywords
- ✅ Response indicates which agent was used
- ✅ Correct agent specialization in response

---

### Test 12: Settings Page

**Purpose**: Verify agent configuration

**Steps:**
1. Navigate to ⚙️ Settings page
2. Modify agent settings:
   - Verbosity: Standard / Detailed / Concise
   - Technical Level: Junior / Mid / Senior
   - Citation Style: Inline / Footnotes / None
3. Save settings
4. Return to Chat and ask a question
5. Verify settings are applied

**Expected Results:**
- ✅ Settings are persisted in session state
- ✅ Agent responses reflect verbosity choice
- ✅ Technical level affects response complexity

---

### Test 13: Files Page

**Purpose**: Verify file browser shows indexed files

**Steps:**
1. Navigate to 🗂️ Files page
2. Browse file tree

**Expected Results:**
- ✅ File tree displays files from JAVA_SOURCE_DIR
- ✅ Can navigate directory structure
- ✅ File details shown (size, type)
- ✅ Can preview file contents (if implemented)

---

### Test 14: Workspace Persistence

**Purpose**: Verify session workspace is saved to SQLite

**Steps:**
1. Navigate to 📊 Workspace page
2. Create new workspace or use default
3. Add some data (if applicable)
4. Close browser tab
5. Reopen Streamlit
6. Check workspace is persisted

**Expected Results:**
- ✅ Workspaces are stored in SQLite (data/workspaces.db)
- ✅ Can list all workspaces
- ✅ Can switch between workspaces
- ✅ Data persists across sessions

---

## Performance Testing

### Search Performance

**Test:**
1. Execute search with common query
2. Note execution time
3. Repeat 5 times

**Expected:**
- ✅ Average search time: <1000ms
- ✅ Weaviate vector search overhead: ~100-500ms
- ✅ Consistent timing across runs

### Agent Response Time

**Test:**
1. Ask agent a complex question
2. Note response time
3. Test different agent types

**Expected:**
- ✅ Simple queries: 2-5 seconds
- ✅ Complex queries with context: 10-30 seconds
- ✅ Document generation: 30-60 seconds
- ✅ Timeouts handled gracefully

### Concurrent Users

**Test:**
1. Open multiple browser tabs
2. Execute searches and agent queries simultaneously
3. Verify no conflicts or errors

**Expected:**
- ✅ Multiple sessions work independently
- ✅ No session state conflicts
- ✅ Rate limiting prevents Ollama overload

---

## Error Handling Testing

### Test: Ollama Unavailable

**Steps:**
1. Stop Ollama: `killall ollama` (or `Ctrl+C` in Ollama terminal)
2. Ask agent a question
3. Observe error handling

**Expected:**
- ✅ Graceful error message displayed
- ✅ Fallback response with artifact list
- ✅ Clear instructions to start Ollama
- ✅ No application crash

### Test: Weaviate Unavailable

**Steps:**
1. Stop Weaviate: `./docker-weaviate.sh stop`
2. Execute search or agent query
3. Observe error handling

**Expected:**
- ✅ Connection error displayed
- ✅ Clear instructions to start Weaviate
- ✅ No application crash

### Test: No Indexed Data

**Steps:**
1. Use empty Weaviate (or clean database)
2. Execute search
3. Ask agent questions

**Expected:**
- ✅ "No results found" message
- ✅ Instructions to run pipeline
- ✅ Agent provides limited response without context

---

## Browser Compatibility

Test on:
- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)

Verify:
- Layout renders correctly
- Navigation works
- Interactive elements functional
- No console errors

---

## Mobile Responsiveness

Test on:
- ✅ iPhone (Safari)
- ✅ Android (Chrome)
- ✅ Tablet

Verify:
- Sidebar collapses on mobile
- Search input accessible
- Chat messages readable
- Navigation functional

---

## Acceptance Criteria

### Core Functionality
- ✅ Search returns real Weaviate data
- ✅ All 8 agents use Ollama LLM
- ✅ Citations displayed with confidence scores
- ✅ Follow-up questions generated
- ✅ Agent routing works correctly

### Performance
- ✅ Search: <1s average
- ✅ Agent response: <30s for complex queries
- ✅ No memory leaks
- ✅ Handles concurrent users

### Error Handling
- ✅ Graceful degradation when services unavailable
- ✅ Clear error messages
- ✅ No application crashes
- ✅ Fallback responses provided

### User Experience
- ✅ Intuitive navigation
- ✅ Responsive design
- ✅ Clear status indicators
- ✅ Loading states shown

---

## Troubleshooting Common Issues

### Issue: "No results found" in Search

**Cause**: Weaviate is empty or project name mismatch

**Solution**:
```bash
# Check Weaviate has data
./weaviate_stats.py

# If empty, run pipeline
./production-requirements-generation.sh <project> <source>

# Check project names match
curl -s http://localhost:8080/v1/objects | jq '.objects[].properties.projectId' | sort -u
```

### Issue: Agent returns placeholder response

**Cause**: Agent not connected to Ollama (old code)

**Solution**:
```bash
# Check commit history
git log --oneline src/codeindex/web/agents/

# Ensure commits present:
# 5b99f65 - Senior Developer
# d9c0acb - Data Analyst
# f851a83 - Frontend & Backend
# 33a21a1 - Writer agents
```

### Issue: "Cannot connect to Ollama"

**Cause**: Ollama not running

**Solution**:
```bash
# Start Ollama
ollama serve

# Verify model is available
ollama list | grep gemma3:12b

# If not available, pull it
ollama pull gemma3:12b
```

### Issue: Slow agent responses

**Cause**: Large context, slow LLM, or timeout issues

**Solution**:
- Reduce search result limit in agent code
- Check Ollama logs for performance issues
- Verify adaptive timeout settings
- Consider using smaller model (e.g., gemma2:9b)

---

## Test Report Template

After completing tests, document results:

```markdown
# Test Report - Streamlit Web UI

**Date**: YYYY-MM-DD
**Tester**: Your Name
**Environment**: macOS/Linux, Python 3.x

## Test Results Summary

| Test | Status | Notes |
|------|--------|-------|
| Search Functionality | ✅ Pass | 23 artifacts found |
| Senior Developer | ✅ Pass | Response time: 8s |
| Data Analyst | ✅ Pass | Found 5 DB tables |
| Frontend Specialist | ✅ Pass | 12 UI components |
| Backend Specialist | ✅ Pass | 8 service endpoints |
| PRD Writer | ✅ Pass | 45s generation time |
| Spec-Kit Writer | ✅ Pass | Complete spec |
| Gherkin Test Writer | ✅ Pass | 5 scenarios |
| Playwright Test Writer | ✅ Pass | Page Object pattern |

## Issues Found

1. [Issue description]
2. [Issue description]

## Recommendations

1. [Recommendation]
2. [Recommendation]
```

---

## Next Steps After Testing

If all tests pass:
1. ✅ Mark feature as production-ready
2. 📝 Conduct user acceptance testing
3. 📝 Create deployment documentation
4. 📝 Phase 18: Production polish

If issues found:
1. Document issues in test report
2. Prioritize by severity
3. Create fix tasks
4. Re-test after fixes
