"""
Test Generation page for GEMINI Code Analysis Pipeline Web UI (Phase 12).

This page provides automated test generation with:
- Gherkin BDD test generation
- Playwright E2E test generation
- Test preview with syntax highlighting
- Export tests to files
- Test from artifacts or natural language descriptions
"""

import streamlit as st
import sys
import time
from pathlib import Path
from typing import Optional, Dict, List, Any

# Add src directory to Python path
src_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(src_dir))

from codeindex.web.services.agent_service import get_agent_service
from codeindex.web.agents.base import AgentRole
from codeindex.web.utils.session_state import (
    initialize_session_state,
    get,
    set_value,
    append_to_list,
    clear_list
)


def initialize_tests_state():
    """Initialize session state for tests page."""
    defaults = {
        "test_type": "gherkin",
        "test_input": "",
        "generated_tests": [],
        "test_loading": False,
        "test_error": None,
        "validation_results": None,  # T122: Validation status
        "test_coverage_summary": None  # T125: Coverage summary
    }

    initialize_session_state(defaults)


def render_test_type_selector():
    """Render test type selection."""
    st.subheader("🧪 Test Generation")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📝 Gherkin (BDD)", use_container_width=True, type="primary" if get("test_type") == "gherkin" else "secondary"):
            set_value("test_type", "gherkin")
            st.rerun()

    with col2:
        if st.button("🎭 Playwright (E2E)", use_container_width=True, type="primary" if get("test_type") == "playwright" else "secondary"):
            set_value("test_type", "playwright")
            st.rerun()

    test_type = get("test_type", "gherkin")

    if test_type == "gherkin":
        st.info("""
        **Gherkin BDD Tests**: Generate behavior-driven development scenarios in Given-When-Then format.
        Perfect for documenting user stories and acceptance criteria.
        """)
    else:
        st.info("""
        **Playwright E2E Tests**: Generate end-to-end test scripts for web UI automation.
        Includes page object patterns, proper locators, and comprehensive assertions.
        """)


def render_test_input():
    """Render test generation input."""
    st.subheader("📋 Describe What to Test")

    test_type = get("test_type", "gherkin")

    if test_type == "gherkin":
        placeholder = """Example:
Feature: User Login
  As a user
  I want to log in to the application
  So that I can access my account

Describe the login feature, authentication flow, and edge cases..."""
    else:
        placeholder = """Example:
Test the user login flow:
1. Navigate to login page
2. Enter valid credentials
3. Click login button
4. Verify dashboard is displayed

Describe the UI elements and expected behavior..."""

    test_input = st.text_area(
        "Test Description",
        value=get("test_input", ""),
        height=200,
        placeholder=placeholder,
        help="Describe the feature or user flow you want to test"
    )

    set_value("test_input", test_input)

    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        if st.button("🎯 Generate Tests", type="primary", use_container_width=True):
            if test_input.strip():
                generate_tests(test_input)
                st.rerun()
            else:
                st.error("❌ Please provide a test description")

    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            set_value("test_input", "")
            clear_list("generated_tests")
            st.rerun()


def generate_tests(description: str):
    """Generate tests using appropriate agent or workflow."""
    set_value("test_loading", True)
    set_value("test_error", None)

    try:
        test_type = get("test_type", "gherkin")

        if test_type == "gherkin":
            # Use workflow for comprehensive Gherkin generation (T118)
            from codeindex.web.workflows.gherkin_generation import get_gherkin_generation_workflow
            workflow = get_gherkin_generation_workflow()

            result = workflow.execute(description)

            # Check for errors
            if "error" in result:
                set_value("test_error", result["error"])
                return

            # Store validation results (T122)
            set_value("validation_results", result["validation"])

            # Calculate coverage summary (T125)
            from codeindex.web.services.gherkin_validation import count_gherkin_elements
            element_counts = count_gherkin_elements(result["gherkin_content"])

            summary = {
                "scenario_count": element_counts.get("scenarios", 0),
                "step_count": element_counts.get("steps", 0),
                "example_count": element_counts.get("examples", 0),
                "background_steps": element_counts.get("background_steps", 0),
                "duration_seconds": result["total_duration_seconds"]
            }
            set_value("test_coverage_summary", summary)

            # Add to generated tests
            append_to_list("generated_tests", {
                "type": test_type,
                "description": description,
                "content": result["gherkin_content"],
                "timestamp": result["timestamp"],
                "citations": [c.to_dict() for c in result["citations"]],
                "validation": result["validation"],
                "summary": summary
            })

        else:
            # T132: Use workflow for comprehensive Playwright generation
            from codeindex.web.workflows.playwright_generation import get_playwright_generation_workflow
            from codeindex.web.services.search_service import get_search_service

            # Get UI artifacts for context
            search_service = get_search_service()
            search_results = search_service.search(description, limit=10)
            artifacts = search_results.get("results", [])

            # Use workflow with progress tracking (T136)
            workflow = get_playwright_generation_workflow()

            progress_container = st.empty()

            def progress_callback(stage: str, progress: float):
                """Update progress indicator."""
                progress_container.progress(progress / 100.0, text=f"🔄 {stage} ({progress:.0f}%)")

            try:
                result = workflow.execute(
                    test_request=description,
                    artifacts=artifacts,
                    progress_callback=progress_callback
                )

                progress_container.empty()

                # T133: Validate Playwright syntax
                from codeindex.web.services.playwright_validation import validate_playwright_syntax, count_playwright_elements
                test_code = result["test_code"]
                is_valid, errors = validate_playwright_syntax(test_code, language='typescript')

                validation_results = {
                    "is_valid": is_valid,
                    "errors": errors
                }

                # T134: Calculate coverage summary
                element_counts = count_playwright_elements(test_code)
                summary = {
                    "test_count": element_counts.get("test_cases", 0),
                    "describe_count": element_counts.get("describe_blocks", 0),
                    "expectation_count": element_counts.get("expectations", 0),
                    "hook_count": element_counts.get("beforeEach_hooks", 0) + element_counts.get("afterEach_hooks", 0),
                    "duration_seconds": result["duration_seconds"]
                }

                # Add to generated tests
                append_to_list("generated_tests", {
                    "type": test_type,
                    "description": description,
                    "content": test_code,
                    "timestamp": result["timestamp"],
                    "citations": [],  # Playwright workflow doesn't return citations
                    "validation": validation_results,  # T133
                    "summary": summary,  # T134
                    "frontend_analysis": result.get("frontend_analysis", ""),
                    "backend_analysis": result.get("backend_analysis", "")
                })

            except Exception as workflow_error:
                progress_container.empty()
                raise workflow_error

        # Log performance
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Test generation: type={test_type}")

    except Exception as e:
        set_value("test_error", str(e))

        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Test generation failed: {e}", exc_info=True)

    finally:
        set_value("test_loading", False)


def render_generated_tests():
    """Render generated test results with validation and coverage (T122, T123, T124, T125)."""
    tests = get("generated_tests", [])

    if not tests:
        return

    st.markdown("---")
    st.subheader("📄 Generated Tests")

    for i, test in enumerate(reversed(tests)):  # Show newest first
        with st.expander(f"{test['type'].upper()} Test - {test['timestamp'][:19]}", expanded=i==0):
            # Description
            st.caption(f"**Description**: {test['description'][:100]}...")

            # T122 & T133: Validation status (for Gherkin and Playwright tests)
            if 'validation' in test:
                validation = test['validation']
                is_valid = validation.get("is_valid", False)
                errors = validation.get("errors", [])

                if is_valid:
                    st.success(f"✅ {test['type'].capitalize()} syntax valid - ready for download")
                else:
                    st.error(f"❌ {test['type'].capitalize()} syntax validation failed")
                    with st.expander("Validation Errors", expanded=True):
                        for error in errors:
                            st.markdown(f"- {error}")

            # T125 & T134: Test coverage summary (for Gherkin and Playwright tests)
            if 'summary' in test:
                summary = test['summary']

                st.markdown("**📊 Test Coverage:**")

                if test['type'] == "gherkin":
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Scenarios", summary.get("scenario_count", 0))
                    with col2:
                        st.metric("Steps", summary.get("step_count", 0))
                    with col3:
                        st.metric("Examples", summary.get("example_count", 0))
                    with col4:
                        duration = summary.get("duration_seconds", 0)
                        st.metric("Time", f"{duration:.1f}s")
                else:  # playwright
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Tests", summary.get("test_count", 0))
                    with col2:
                        st.metric("Describes", summary.get("describe_count", 0))
                    with col3:
                        st.metric("Expectations", summary.get("expectation_count", 0))
                    with col4:
                        duration = summary.get("duration_seconds", 0)
                        st.metric("Time", f"{duration:.1f}s")

            # Show workflow analysis (for Playwright tests)
            if test['type'] == "playwright" and ('frontend_analysis' in test or 'backend_analysis' in test):
                with st.expander("🔍 Workflow Analysis", expanded=False):
                    if test.get('frontend_analysis'):
                        st.markdown("**Frontend Specialist Analysis:**")
                        st.text(test['frontend_analysis'][:500] + "..." if len(test['frontend_analysis']) > 500 else test['frontend_analysis'])

                    if test.get('backend_analysis'):
                        st.markdown("**Backend Specialist Analysis:**")
                        st.text(test['backend_analysis'][:500] + "..." if len(test['backend_analysis']) > 500 else test['backend_analysis'])

            st.markdown("---")

            # T123: Test content with syntax highlighting
            if test['type'] == "gherkin":
                st.code(test['content'], language="gherkin", line_numbers=True)
            else:
                st.code(test['content'], language="javascript", line_numbers=True)

            # T124 & T135: Download button (with validation check for both Gherkin and Playwright)
            col1, col2, col3 = st.columns([1, 1, 4])

            with col1:
                # Check if download should be enabled (T124 & T135: FR8.8)
                is_downloadable = True
                if 'validation' in test:
                    is_downloadable = test['validation'].get("is_valid", False)

                # Download button
                extension = ".feature" if test['type'] == "gherkin" else ".spec.ts"
                filename = f"{test['type']}_test_{int(time.time())}{extension}"

                st.download_button(
                    label="⬇️ Download",
                    data=test['content'],
                    file_name=filename,
                    mime="text/plain",
                    key=f"download_{i}",
                    disabled=not is_downloadable,
                    help="Download test file" + ("" if is_downloadable else " (blocked due to validation errors)")
                )

            with col2:
                # Copy button hint
                st.caption("📋 Use browser copy")

            # Citations
            if test.get('citations'):
                with st.expander(f"📚 References ({len(test['citations'])})"):
                    for j, citation in enumerate(test['citations'], 1):
                        file_path = citation.get("file_path", "")
                        st.markdown(f"{j}. `{file_path}`")


def render_test_examples():
    """Render test generation examples."""
    st.sidebar.markdown("---")
    st.sidebar.subheader("💡 Examples")

    test_type = get("test_type", "gherkin")

    if test_type == "gherkin":
        examples = {
            "User Login": """Feature: User Authentication
Test the login flow with valid and invalid credentials, password reset, and account lockout scenarios.""",

            "Search Feature": """Feature: Artifact Search
Test natural language search, filtering by artifact type, pagination, and empty results handling.""",

            "Workspace Management": """Feature: Workspace Collaboration
Test creating, saving, loading, and sharing workspaces with team members."""
        }
    else:
        examples = {
            "Login Flow": """Test the complete user login flow:
- Navigate to login page
- Enter credentials
- Handle success/error cases
- Verify redirect to dashboard""",

            "Search Interaction": """Test search functionality:
- Enter search query
- Apply filters
- Verify results display
- Test pagination controls""",

            "Form Submission": """Test form submission:
- Fill form fields
- Validate input
- Submit form
- Verify success message"""
        }

    for title, example in examples.items():
        if st.sidebar.button(f"📝 {title}", key=f"example_{title}"):
            set_value("test_input", example)
            st.rerun()


def render_test_templates():
    """Render test templates."""
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 Templates")

    test_type = get("test_type", "gherkin")

    if test_type == "gherkin":
        template = """Feature: [Feature Name]
  As a [user role]
  I want to [action]
  So that [benefit]

  Scenario: [Scenario Name]
    Given [initial context]
    When [action occurs]
    Then [expected outcome]

  Scenario Outline: [Parameterized Scenario]
    Given [context with <parameter>]
    When [action with <parameter>]
    Then [outcome with <parameter>]

    Examples:
      | parameter |
      | value1    |
      | value2    |
"""
    else:
        template = """import { test, expect } from '@playwright/test';

test.describe('[Feature Name]', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('[Test Name]', async ({ page }) => {
    // Arrange
    await page.locator('[data-testid="element"]').click();

    // Act
    await page.fill('[data-testid="input"]', 'value');
    await page.click('[data-testid="submit"]');

    // Assert
    await expect(page.locator('[data-testid="result"]'))
      .toContainText('expected text');
  });
});
"""

    with st.sidebar.expander("View Template"):
        st.code(template, language="gherkin" if test_type == "gherkin" else "javascript")

        if st.button("📋 Use Template"):
            set_value("test_input", template)
            st.rerun()


def main():
    """Main tests page function."""
    # Page configuration
    st.title("🧪 Test Generation")

    st.markdown("""
    Generate automated tests using AI agents. Describe your feature or user flow,
    and get production-ready test cases in Gherkin or Playwright format.
    """)

    # Initialize session state
    initialize_tests_state()

    # Render examples and templates in sidebar
    render_test_examples()
    render_test_templates()

    # Show loading indicator
    if get("test_loading", False):
        with st.spinner("🤖 Generating tests..."):
            time.sleep(0.1)

    # Show error if present
    error = get("test_error")
    if error:
        st.error(f"❌ {error}")

    # Render test type selector
    render_test_type_selector()

    st.markdown("---")

    # Render input
    render_test_input()

    # Render generated tests
    render_generated_tests()


if __name__ == "__main__":
    main()
