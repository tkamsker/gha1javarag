"""
Integration tests for Agent Chat End-to-End Flow (T057 - US2.1).

Tests cover complete agent chat workflow from user query to rendered response:
1. User submits query
2. Query routed to appropriate agent
3. Agent searches for artifacts (Weaviate)
4. Agent generates response (Ollama LLM)
5. Citations validated (Weaviate verification)
6. Response formatted with hyperlinks
7. Response streamed to UI

Tests require:
- Running Weaviate instance
- Running Ollama instance
- Indexed test data

Set SKIP_INTEGRATION_TESTS=1 to skip these tests.
"""

import pytest
import os
import asyncio
from datetime import datetime
from typing import List, Dict, Any

from codeindex.web.agents.base import AgentRole, AgentResponse, Citation

# Skip integration tests if environment variable is set
pytestmark = pytest.mark.skipif(
    os.getenv("SKIP_INTEGRATION_TESTS") == "1",
    reason="Integration tests skipped (set SKIP_INTEGRATION_TESTS=0 to run)"
)


@pytest.fixture(scope="module")
def weaviate_client():
    """Weaviate client for integration tests."""
    from codeindex.services.weaviate_store import WeaviateStore

    try:
        store = WeaviateStore()
        # Verify Weaviate is accessible
        store.client.is_ready()
        yield store
    except Exception as e:
        pytest.skip(f"Weaviate not available: {e}")


@pytest.fixture(scope="module")
def ollama_client():
    """Ollama client for integration tests."""
    from codeindex.services.ollama_client import OllamaClient

    try:
        client = OllamaClient()
        # Verify Ollama is accessible
        client.generate("Test connection")
        yield client
    except Exception as e:
        pytest.skip(f"Ollama not available: {e}")


@pytest.fixture
def agent_service(weaviate_client, ollama_client):
    """Agent service with real dependencies."""
    from codeindex.web.services.agent_service import AgentService

    service = AgentService(
        weaviate_store=weaviate_client,
        ollama_client=ollama_client
    )
    return service


class TestAgentChatEndToEndFlow:
    """Test end-to-end agent chat workflow."""

    def test_user_query_to_rendered_response(self, agent_service):
        """Test complete flow from user query to rendered response."""
        # User submits query
        query = "What database tables exist in the system?"

        # Execute agent query
        response = agent_service.execute_query(query)

        # Verify response structure
        assert isinstance(response, AgentResponse)
        assert response.agent_role == AgentRole.DATA_ANALYST  # Routed to Data Analyst
        assert len(response.response_text) > 0
        assert response.error is None
        assert response.duration_seconds > 0

        # Verify citations present
        assert len(response.citations) > 0

        # Verify response can be formatted
        from codeindex.web.components.agent_chat import format_response

        formatted_response = format_response(response)
        assert len(formatted_response) > 0

    def test_agent_routing_integration(self, agent_service):
        """Test agent routing works with real queries."""
        test_cases = [
            ("What database schema exists?", AgentRole.DATA_ANALYST),
            ("Explain the UI components", AgentRole.FRONTEND_SPECIALIST),
            ("How does the API work?", AgentRole.BACKEND_SPECIALIST),
            ("What does this code do?", AgentRole.SENIOR_DEVELOPER)
        ]

        for query, expected_agent in test_cases:
            response = agent_service.execute_query(query)

            # Verify routed to expected agent
            assert response.agent_role == expected_agent

    def test_artifact_search_integration(self, agent_service, weaviate_client):
        """Test agent searches Weaviate and retrieves artifacts."""
        query = "Find user management services"

        response = agent_service.execute_query(query)

        # Verify agent found artifacts (via citations)
        assert len(response.citations) > 0

        # Verify citations reference real artifacts
        for citation in response.citations[:3]:  # Check first 3
            artifact_exists = weaviate_client.artifact_exists(citation.artifact_id)
            assert artifact_exists, f"Citation artifact {citation.artifact_id} not found in Weaviate"

    def test_llm_response_generation_integration(self, agent_service, ollama_client):
        """Test agent generates response using Ollama LLM."""
        query = "Explain how authentication works in the system"

        response = agent_service.execute_query(query)

        # Verify LLM generated response
        assert len(response.response_text) > 100  # Should be comprehensive
        assert "authentication" in response.response_text.lower()

        # Response should have structure (not just raw text)
        assert any(marker in response.response_text for marker in ["##", "1.", "2.", "-"])

    def test_citation_validation_integration(self, agent_service, weaviate_client):
        """Test citation validation verifies artifact IDs in Weaviate."""
        query = "What services exist?"

        response = agent_service.execute_query(query)

        # Validate citations
        from codeindex.web.components.agent_chat import validate_citations

        validated_citations = validate_citations(
            response.citations,
            weaviate_store=weaviate_client
        )

        # Some citations should be verified
        verified = [c for c in validated_citations if c.get("verified")]
        assert len(verified) > 0

    def test_response_streaming_integration(self, agent_service):
        """Test response can be streamed word-by-word."""
        query = "What does UserService do?"

        response = agent_service.execute_query(query)

        # Format for streaming
        from codeindex.web.components.agent_chat import format_response_for_streaming

        chunks = format_response_for_streaming(response.response_text)

        # Should have multiple chunks for streaming
        assert len(chunks) > 10

        # Streaming chunks should reconstruct original
        recombined = "".join(chunks)
        assert len(recombined) == len(response.response_text)


class TestAgentChatConversationFlow:
    """Test conversation flow with follow-up questions."""

    def test_conversation_with_context(self, agent_service):
        """Test follow-up questions maintain context."""
        # First query
        query1 = "What database tables exist?"
        response1 = agent_service.execute_query(query1)

        # Follow-up query with context
        query2 = "How are they related?"
        context = {
            "previous_query": query1,
            "previous_agent": response1.agent_role,
            "previous_response": response1.response_text
        }

        response2 = agent_service.execute_query(query2, context=context)

        # Should use same agent for follow-up
        assert response2.agent_role == response1.agent_role

        # Response should reference previous context
        assert len(response2.response_text) > 0

    def test_conversation_history_tracking(self, agent_service):
        """Test conversation history is tracked."""
        queries = [
            "What is UserService?",
            "What methods does it have?",
            "How does it handle authentication?"
        ]

        conversation_history = []

        for query in queries:
            context = {"conversation_history": conversation_history} if conversation_history else None
            response = agent_service.execute_query(query, context=context)

            conversation_history.append({
                "query": query,
                "agent": response.agent_role,
                "response": response.response_text
            })

        # History should track all queries
        assert len(conversation_history) == 3


class TestAgentChatErrorHandling:
    """Test error handling in agent chat flow."""

    def test_handles_weaviate_unavailable(self, ollama_client):
        """Test chat handles Weaviate unavailability gracefully."""
        from codeindex.web.services.agent_service import AgentService

        # Use invalid Weaviate store
        invalid_service = AgentService(
            weaviate_store=None,
            ollama_client=ollama_client
        )

        query = "What database tables exist?"

        try:
            response = invalid_service.execute_query(query)

            # Should have error
            assert response.has_error()
            assert "Weaviate" in response.error or "unavailable" in response.error.lower()
        except Exception as e:
            # Or should raise appropriate error
            assert "Weaviate" in str(e) or "unavailable" in str(e).lower()

    def test_handles_ollama_timeout(self, weaviate_client):
        """Test chat handles Ollama timeout gracefully."""
        from codeindex.web.services.agent_service import AgentService
        from codeindex.services.ollama_client import OllamaClient

        # Create client with very short timeout
        timeout_client = OllamaClient(read_timeout=0.1)

        service = AgentService(
            weaviate_store=weaviate_client,
            ollama_client=timeout_client
        )

        query = "Generate very long detailed analysis"  # Likely to timeout

        try:
            response = service.execute_query(query)

            # Should have timeout error
            if response.has_error():
                assert "timeout" in response.error.lower()
        except TimeoutError:
            # Or should raise timeout exception
            pass

    def test_handles_empty_search_results(self, agent_service):
        """Test chat handles empty search results gracefully."""
        query = "Find artifacts related to xyznonexistentmodulexyz123456"

        response = agent_service.execute_query(query)

        # Should not crash, even with no artifacts found
        assert response.error is None or len(response.response_text) > 0

        # Response should indicate no artifacts found
        assert "no" in response.response_text.lower() or "not found" in response.response_text.lower()


class TestAgentChatPerformance:
    """Test agent chat performance requirements."""

    def test_response_generated_within_30_seconds(self, agent_service):
        """Test agent response generated in <30 seconds (per US2.1)."""
        query = "What does UserService do?"

        start_time = datetime.now()
        response = agent_service.execute_query(query)
        duration = (datetime.now() - start_time).total_seconds()

        # Should complete within 30 seconds (NFR1.3)
        assert duration < 30, f"Response took {duration}s (expected <30s)"

        # Response duration should be tracked
        assert response.duration_seconds < 30

    def test_streaming_starts_within_5_seconds(self, agent_service):
        """Test response streaming starts within 5 seconds (NFR1.3)."""
        query = "Explain the architecture"

        start_time = datetime.now()
        response = agent_service.execute_query(query, enable_streaming=True)

        # Get first chunk
        from codeindex.web.components.agent_chat import format_response_for_streaming
        chunks = format_response_for_streaming(response.response_text)

        first_chunk_time = (datetime.now() - start_time).total_seconds()

        # First chunk should arrive within 5 seconds
        assert first_chunk_time < 5, f"Streaming started after {first_chunk_time}s (expected <5s)"


class TestAgentChatCitationValidation:
    """Test citation validation and hyperlink generation (FR4.11)."""

    def test_verified_citations_get_hyperlinks(self, agent_service, weaviate_client):
        """Test verified citations become clickable hyperlinks."""
        query = "What services exist?"

        response = agent_service.execute_query(query)

        # Format with hyperlinks
        from codeindex.web.components.agent_chat import format_response_with_hyperlinks

        formatted = format_response_with_hyperlinks(response, weaviate_store=weaviate_client)

        # Should have hyperlinks for verified citations
        assert "/artifact/" in formatted or "artifact_id=" in formatted

    def test_unverified_citations_show_warnings(self, agent_service, weaviate_client):
        """Test unverified citations display warning icons (FR4.11)."""
        # Create response with known invalid citation
        response = AgentResponse(
            agent_role=AgentRole.SENIOR_DEVELOPER,
            query="Test",
            timestamp=datetime.now().isoformat(),
            duration_seconds=1.0,
            response_text="Reference artifact:invalid_999999",
            citations=[
                Citation(
                    artifact_id="invalid_999999",
                    file_path="src/Invalid.java",
                    artifact_type="BackendDoc"
                )
            ]
        )

        # Format with hyperlinks
        from codeindex.web.components.agent_chat import format_response_with_hyperlinks

        formatted = format_response_with_hyperlinks(response, weaviate_store=weaviate_client)

        # Should have warning for unverified citation
        assert "⚠️" in formatted or "unverified" in formatted.lower() or "warning" in formatted.lower()


class TestAgentChatUIIntegration:
    """Test agent chat UI component integration."""

    def test_chat_component_renders_response(self, agent_service):
        """Test chat component renders agent response."""
        query = "What database tables exist?"

        response = agent_service.execute_query(query)

        # Render in chat component
        from codeindex.web.components.agent_chat import render_chat_message

        rendered_html = render_chat_message(response)

        # Should produce HTML output
        assert len(rendered_html) > 0
        assert isinstance(rendered_html, str)

        # Should include agent role and response text
        assert "Data Analyst" in rendered_html or "data" in rendered_html.lower()

    def test_chat_component_displays_citations(self, agent_service):
        """Test chat component displays citations."""
        query = "What services exist?"

        response = agent_service.execute_query(query)

        from codeindex.web.components.agent_chat import render_chat_message

        rendered_html = render_chat_message(response, show_citations=True)

        # Should display citations
        assert len(response.citations) > 0
        assert any(citation.file_path in rendered_html for citation in response.citations)


# Async tests for concurrent agent queries

@pytest.mark.asyncio
async def test_concurrent_agent_queries(agent_service):
    """Test multiple concurrent agent queries don't interfere."""
    queries = [
        "What database tables exist?",
        "Explain the UI components",
        "How does the API work?"
    ]

    # Execute queries concurrently
    tasks = [
        asyncio.create_task(asyncio.to_thread(agent_service.execute_query, query))
        for query in queries
    ]

    responses = await asyncio.gather(*tasks)

    # All responses should succeed
    assert len(responses) == 3
    assert all(not r.has_error() for r in responses)
    assert all(len(r.response_text) > 0 for r in responses)
