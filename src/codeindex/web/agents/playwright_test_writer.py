"""
Playwright Test Writer Agent for generating E2E test automation.

This agent specializes in:
- Writing Playwright test code
- Creating page object models
- Defining locator strategies
- Implementing test assertions
- E2E automation best practices
"""

import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

from codeindex.web.agents.base import (
    AgentRole,
    AgentConfig,
    AgentResponse,
    Citation,
    get_agent_config
)

logger = logging.getLogger(__name__)


class PlaywrightTestWriterAgent:
    """
    Playwright Test Writer Agent for E2E test automation.

    Specializes in:
    - Playwright test code generation
    - Page Object Model (POM) pattern
    - Locator strategies (CSS, XPath, text, role)
    - Test assertions and expectations
    - Fixture setup and teardown
    - Parallel test execution
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        """Initialize Playwright Test Writer agent."""
        if config is None:
            config = get_agent_config(AgentRole.PLAYWRIGHT_TEST_WRITER)

        self.config = config
        self.role = AgentRole.PLAYWRIGHT_TEST_WRITER

        logger.info("Initialized Playwright Test Writer agent")

    def execute_query(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """
        Execute query with Playwright Test Writer agent.

        Args:
            query: Test automation request
            context: Optional context from previous interactions

        Returns:
            AgentResponse with generated Playwright test code
        """
        start_time = datetime.now()

        try:
            logger.info(f"Playwright Test Writer processing: {query[:50]}...")

            # Step 1: Search for relevant artifacts (comprehensive)
            artifacts = self._search_relevant_artifacts(query)

            # Step 2: Generate Playwright test code using LLM
            test_code = self._generate_document(query, artifacts, context)

            # Step 3: Extract citations
            citations = self._extract_citations(artifacts)

            # Step 4: Generate follow-up questions
            suggested_questions = self._generate_follow_ups(query, artifacts)

            duration = (datetime.now() - start_time).total_seconds()

            return AgentResponse(
                agent_role=self.role,
                query=query,
                timestamp=start_time.isoformat(),
                duration_seconds=duration,
                response_text=test_code,
                citations=citations,
                confidence=0.87,
                suggested_questions=suggested_questions,
                tools_used=["WeaviateSearchTool", "LLMGenerationTool", "PlaywrightCodeGen"]
            )

        except Exception as e:
            logger.error(f"Playwright Test Writer query failed: {e}", exc_info=True)
            duration = (datetime.now() - start_time).total_seconds()

            return AgentResponse(
                agent_role=self.role,
                query=query,
                timestamp=start_time.isoformat(),
                duration_seconds=duration,
                response_text="",
                error=str(e)
            )

    def _search_relevant_artifacts(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for relevant artifacts (comprehensive).

        Args:
            query: Search query

        Returns:
            List of relevant artifacts
        """
        try:
            logger.debug(f"Searching artifacts for Playwright tests: {query}")

            from codeindex.web.services.search_service import get_search_service
            search_service = get_search_service()

            # Comprehensive search with NO type filters
            search_response = search_service.search(
                query=query,
                limit=15
            )

            artifacts = search_response.get("results", [])
            logger.info(f"Found {len(artifacts)} artifacts for test automation")

            return artifacts

        except Exception as e:
            logger.error(f"Artifact search failed: {e}")
            return []

    def _generate_document(
        self,
        query: str,
        artifacts: List[Dict[str, Any]],
        context: Optional[Dict[str, Any]]
    ) -> str:
        """
        Generate Playwright test code using LLM.

        Args:
            query: Test automation request
            artifacts: Relevant artifacts
            context: Optional context

        Returns:
            Generated Playwright test code
        """
        try:
            logger.debug("Generating Playwright test code with Ollama LLM")

            from codeindex.services.ollama_client import OllamaClient

            # Build context from artifacts
            context_parts = []

            # Group artifacts by type
            artifact_types = {}
            for artifact in artifacts:
                artifact_type = artifact.get("artifactType", "Unknown")
                if artifact_type not in artifact_types:
                    artifact_types[artifact_type] = []
                artifact_types[artifact_type].append(artifact)

            # Add artifact details (focus on UI components)
            if artifact_types:
                context_parts.append("## UI Components to Test:\n")

                # Prioritize frontend artifacts
                priority_types = ["GwtPresenter", "GwtView", "GwtUiBinder", "JspForm"]
                for artifact_type in priority_types:
                    if artifact_type in artifact_types:
                        items = artifact_types[artifact_type]
                        context_parts.append(f"\n**{artifact_type} ({len(items)}):**")
                        for item in items[:5]:
                            file_path = item.get("relativePath") or item.get("fileName", "Unknown")
                            summary = item.get("summary", "")
                            entities = item.get("entities", [])

                            context_parts.append(f"- `{file_path}`")
                            if summary:
                                context_parts.append(f"  {summary}")
                            if entities:
                                context_parts.append(f"  Elements: {', '.join(entities[:5])}")

            context_text = "\n".join(context_parts) if context_parts else "No specific UI components found."

            # Create system prompt
            system_prompt = """You are an Automation Engineer specializing in Playwright test automation.
Generate production-ready Playwright test code following these guidelines:

**Test Structure:**
```typescript
import { test, expect } from '@playwright/test';
import { PageObjectName } from './pages/PageObjectName';

test.describe('Feature Name', () => {
  test.beforeEach(async ({ page }) => {
    // Setup
  });

  test('test case name', async ({ page }) => {
    // Arrange
    const pageObject = new PageObjectName(page);

    // Act
    await pageObject.performAction();

    // Assert
    await expect(page.locator('selector')).toBeVisible();
  });
});
```

**Page Object Pattern:**
```typescript
export class PageObjectName {
  constructor(private page: Page) {}

  // Locators
  private readonly submitButton = this.page.locator('[data-testid="submit"]');
  private readonly inputField = this.page.getByLabel('Username');

  // Actions
  async fillForm(data: FormData) {
    await this.inputField.fill(data.username);
    await this.submitButton.click();
  }

  // Assertions
  async expectSuccess() {
    await expect(this.page.getByText('Success')).toBeVisible();
  }
}
```

**Best Practices:**
1. Use Page Object Model (POM) for maintainability
2. Prefer semantic locators: getByRole(), getByLabel(), getByText()
3. Use data-testid for stable locators
4. Add explicit waits: waitForLoadState(), waitForSelector()
5. Use auto-waiting assertions: expect().toBeVisible(), expect().toHaveText()
6. Handle multiple browsers: chromium, firefox, webkit
7. Implement fixtures for common setup
8. Add error screenshots on failure

Base test code on the actual UI components from the codebase."""

            # Create user prompt
            user_prompt = f"""Test Automation Request: {query}

{context_text}

Please generate Playwright test code including:
1. Test suite with describe/test blocks
2. Page Object Model classes
3. Locator strategies
4. Test assertions
5. Setup and teardown"""

            # Call Ollama with higher token limit for code generation
            ollama_client = OllamaClient()
            response = ollama_client.call_ollama(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.2,  # Precise code generation
                format_json=False
            )

            test_code = response.get("response", "")

            if not test_code:
                test_code = self._generate_fallback_test(query, artifacts)

            logger.info(f"Generated Playwright test code ({len(test_code)} chars)")
            return test_code.strip()

        except Exception as e:
            logger.error(f"Failed to generate Playwright test code: {e}")
            return self._generate_fallback_test(query, artifacts)

    def _generate_fallback_test(self, query: str, artifacts: List[Dict[str, Any]]) -> str:
        """
        Generate basic Playwright template when LLM fails.

        Args:
            query: Test request
            artifacts: Found artifacts

        Returns:
            Basic Playwright template
        """
        lines = [
            "import { test, expect } from '@playwright/test';",
            "import { Page } from '@playwright/test';\n",
            f"// Test suite for: {query}\n",
            "test.describe('Feature Test Suite', () => {",
            "  test.beforeEach(async ({ page }) => {",
            "    await page.goto('http://localhost:3000');",
            "  });\n"
        ]

        # Add test cases based on artifacts
        if artifacts:
            for i, artifact in enumerate(artifacts[:3], 1):
                artifact_type = artifact.get("artifactType", "Unknown")
                file_path = artifact.get("relativePath") or artifact.get("fileName", "Unknown")

                lines.extend([
                    f"  test('test {artifact_type} - case {i}', async ({{ page }}) => {{",
                    f"    // Testing: {file_path}",
                    "    ",
                    "    // Arrange",
                    "    const element = page.locator('[data-testid=\"test-element\"]');",
                    "    ",
                    "    // Act",
                    "    await element.click();",
                    "    ",
                    "    // Assert",
                    "    await expect(element).toBeVisible();",
                    "    await expect(page.locator('.success')).toHaveText('Success');",
                    "  });\n"
                ])
        else:
            lines.extend([
                "  test('example test case', async ({ page }) => {",
                "    // Arrange",
                "    const button = page.getByRole('button', { name: 'Submit' });",
                "    ",
                "    // Act",
                "    await button.click();",
                "    ",
                "    // Assert",
                "    await expect(page).toHaveURL(/success/);",
                "  });\n"
            ])

        lines.extend([
            "});\n",
            "// Page Object Model",
            "export class FeaturePage {",
            "  constructor(private page: Page) {}\n",
            "  // Locators",
            "  private readonly submitButton = this.page.getByRole('button', { name: 'Submit' });",
            "  private readonly inputField = this.page.getByLabel('Input');",
            "  private readonly successMessage = this.page.locator('.success');\n",
            "  // Actions",
            "  async performAction(value: string) {",
            "    await this.inputField.fill(value);",
            "    await this.submitButton.click();",
            "  }\n",
            "  // Assertions",
            "  async expectSuccess() {",
            "    await expect(this.successMessage).toBeVisible();",
            "  }",
            "}\n",
            "// Note: LLM generation failed. Please ensure Ollama is running."
        ])

        return "\n".join(lines)

    def _extract_citations(self, artifacts: List[Dict[str, Any]]) -> List[Citation]:
        """
        Extract citations from artifacts.

        Args:
            artifacts: Found artifacts

        Returns:
            List of citations
        """
        citations = []

        for artifact in artifacts[:10]:
            artifact_id = artifact.get("_additional", {}).get("id", artifact.get("id", ""))
            distance = artifact.get("_additional", {}).get("distance", 0.0)
            confidence = 1.0 - distance if distance < 1.0 else 0.5

            citations.append(Citation(
                artifact_id=artifact_id,
                file_path=artifact.get("relativePath") or artifact.get("fileName", "Unknown"),
                artifact_type=artifact.get("artifactType", "Unknown"),
                confidence=confidence
            ))

        return citations

    def _generate_follow_ups(
        self,
        query: str,
        artifacts: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Generate follow-up suggestions for test automation refinement.

        Args:
            query: Original query
            artifacts: Found artifacts

        Returns:
            List of suggested questions
        """
        suggestions = [
            "Can you add error handling test cases?",
            "What visual regression tests should we include?",
            "Can you add API mocking for this test?",
            "What accessibility tests should we add?"
        ]

        return suggestions[:4]


# Global instance
_playwright_test_writer_agent: Optional[PlaywrightTestWriterAgent] = None


def get_playwright_test_writer_agent(config: Optional[AgentConfig] = None) -> PlaywrightTestWriterAgent:
    """
    Get global Playwright Test Writer agent instance.

    Args:
        config: Optional agent configuration

    Returns:
        PlaywrightTestWriterAgent singleton
    """
    global _playwright_test_writer_agent

    if _playwright_test_writer_agent is None:
        _playwright_test_writer_agent = PlaywrightTestWriterAgent(config)
        logger.info("Created global Playwright Test Writer agent instance")

    return _playwright_test_writer_agent


__all__ = [
    "PlaywrightTestWriterAgent",
    "get_playwright_test_writer_agent"
]
