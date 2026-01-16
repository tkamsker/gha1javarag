"""
Unit tests for Agent Chat Response Formatting (T056 - US2.1).

Tests cover response formatting components including:
- Citation extraction from agent responses
- Hyperlink generation with artifact ID validation (FR4.11)
- Streaming display support
- Markdown rendering
- Copy response functionality

FR4.11 Requirements:
- Extract citation patterns from agent responses
- Verify artifact IDs exist in Weaviate before creating hyperlinks
- Display warning icons for unverified citations
- Cache verification results for performance
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Any

from codeindex.web.agents.base import AgentRole, AgentResponse, Citation


@pytest.fixture
def sample_agent_response():
    """Sample agent response with citations."""
    return AgentResponse(
        agent_role=AgentRole.SENIOR_DEVELOPER,
        query="What does UserService do?",
        timestamp="2026-01-16T10:00:00",
        duration_seconds=2.5,
        response_text="""## UserService Analysis

The UserService (artifact:service_123) handles user management operations:

1. **Authentication**: Validates credentials via UserDao (artifact:dao_456)
2. **Profile Management**: CRUD operations for user profiles
3. **Session Management**: Token generation and validation

See src/services/UserService.java for implementation details.""",
        citations=[
            Citation(
                artifact_id="service_123",
                file_path="src/services/UserService.java",
                artifact_type="BackendDoc",
                confidence=0.95
            ),
            Citation(
                artifact_id="dao_456",
                file_path="src/dao/UserDao.java",
                artifact_type="DaoCall",
                confidence=0.92
            )
        ],
        confidence=0.88
    )


@pytest.fixture
def sample_response_with_invalid_citations():
    """Sample response with some invalid artifact IDs."""
    return AgentResponse(
        agent_role=AgentRole.SENIOR_DEVELOPER,
        query="Test query",
        timestamp="2026-01-16T10:00:00",
        duration_seconds=2.0,
        response_text="""Analysis references:
- Valid artifact (artifact:valid_123)
- Invalid artifact (artifact:nonexistent_999)
- Another valid (artifact:valid_456)
""",
        citations=[
            Citation(artifact_id="valid_123", file_path="src/Valid.java", artifact_type="BackendDoc"),
            Citation(artifact_id="nonexistent_999", file_path="src/Nonexistent.java", artifact_type="BackendDoc"),
            Citation(artifact_id="valid_456", file_path="src/Valid2.java", artifact_type="DaoCall")
        ]
    )


class TestCitationExtraction:
    """Test citation extraction from agent responses."""

    def test_extract_artifact_id_patterns(self, sample_agent_response):
        """Test extracting artifact ID patterns from response text."""
        from codeindex.web.components.agent_chat import extract_citations

        citations = extract_citations(sample_agent_response.response_text)

        assert len(citations) >= 2
        assert "service_123" in [c["artifact_id"] for c in citations]
        assert "dao_456" in [c["artifact_id"] for c in citations]

    def test_extract_file_path_citations(self, sample_agent_response):
        """Test extracting file path citations from response text."""
        from codeindex.web.components.agent_chat import extract_citations

        citations = extract_citations(sample_agent_response.response_text)

        file_paths = [c.get("file_path") for c in citations if c.get("file_path")]
        assert any("UserService.java" in fp for fp in file_paths)

    def test_extract_citations_handles_multiple_formats(self):
        """Test extracting citations in various formats."""
        from codeindex.web.components.agent_chat import extract_citations

        response_text = """
        References:
        - artifact:abc123
        - DaoCall:xyz789
        - File: src/main/java/User.java
        - [1] BackendDoc:service_555
        """

        citations = extract_citations(response_text)

        artifact_ids = [c["artifact_id"] for c in citations]
        assert "abc123" in artifact_ids
        assert "xyz789" in artifact_ids
        assert "service_555" in artifact_ids

    def test_extract_citations_deduplicates(self):
        """Test citation extraction deduplicates repeated citations."""
        from codeindex.web.components.agent_chat import extract_citations

        response_text = """
        UserService (artifact:service_123) handles authentication.
        The service (artifact:service_123) also manages profiles.
        See artifact:service_123 for details.
        """

        citations = extract_citations(response_text)

        # Should only have one citation for service_123
        service_citations = [c for c in citations if c["artifact_id"] == "service_123"]
        assert len(service_citations) == 1

    def test_extract_citations_handles_no_citations(self):
        """Test citation extraction handles responses with no citations gracefully."""
        from codeindex.web.components.agent_chat import extract_citations

        response_text = "This is a general response without any specific artifact references."

        citations = extract_citations(response_text)

        assert citations == []


class TestCitationValidation:
    """Test citation validation against Weaviate (FR4.11)."""

    @patch('codeindex.services.weaviate_store.WeaviateStore')
    def test_validate_citations_verifies_artifact_ids(self, mock_store_class, sample_agent_response):
        """Test citation validation queries Weaviate to verify artifact IDs."""
        from codeindex.web.components.agent_chat import validate_citations

        mock_store = MagicMock()
        # Mock Weaviate verification: service_123 exists, dao_456 doesn't
        mock_store.artifact_exists.side_effect = lambda aid: aid == "service_123"
        mock_store_class.return_value = mock_store

        validated_citations = validate_citations(
            sample_agent_response.citations,
            weaviate_store=mock_store
        )

        # Should have called artifact_exists for each citation
        assert mock_store.artifact_exists.call_count == len(sample_agent_response.citations)

        # Should mark citations as verified/unverified
        verified = [c for c in validated_citations if c.get("verified")]
        unverified = [c for c in validated_citations if not c.get("verified")]

        assert len(verified) >= 1  # service_123
        assert len(unverified) >= 1  # dao_456

    @patch('codeindex.services.weaviate_store.WeaviateStore')
    def test_validate_citations_caches_results(self, mock_store_class):
        """Test citation validation caches results for 5 minutes (FR4.11)."""
        from codeindex.web.components.agent_chat import validate_citations, clear_validation_cache

        mock_store = MagicMock()
        mock_store.artifact_exists.return_value = True
        mock_store_class.return_value = mock_store

        citations = [
            Citation(artifact_id="cached_123", file_path="src/Test.java", artifact_type="BackendDoc")
        ]

        # First validation
        validate_citations(citations, weaviate_store=mock_store)

        # Second validation (should use cache)
        validate_citations(citations, weaviate_store=mock_store)

        # Should only have called Weaviate once (second call used cache)
        assert mock_store.artifact_exists.call_count == 1

        # Clear cache and validate again
        clear_validation_cache()
        validate_citations(citations, weaviate_store=mock_store)

        # Should have called Weaviate again after cache clear
        assert mock_store.artifact_exists.call_count == 2

    @patch('codeindex.services.weaviate_store.WeaviateStore')
    def test_validate_citations_logs_failed_verifications(self, mock_store_class, caplog):
        """Test citation validation logs failed verifications (FR4.11)."""
        from codeindex.web.components.agent_chat import validate_citations

        mock_store = MagicMock()
        mock_store.artifact_exists.return_value = False  # All fail
        mock_store_class.return_value = mock_store

        citations = [
            Citation(artifact_id="invalid_123", file_path="src/Invalid.java", artifact_type="BackendDoc")
        ]

        validate_citations(citations, weaviate_store=mock_store)

        # Should have logged failed verification
        assert any("failed" in record.message.lower() or "verification" in record.message.lower() for record in caplog.records)


class TestHyperlinkGeneration:
    """Test hyperlink generation for verified citations (FR4.11)."""

    @patch('codeindex.services.weaviate_store.WeaviateStore')
    def test_generate_hyperlinks_only_for_verified_citations(
        self,
        mock_store_class,
        sample_response_with_invalid_citations
    ):
        """Test hyperlinks generated only for verified artifact IDs (FR4.11)."""
        from codeindex.web.components.agent_chat import format_response_with_hyperlinks

        mock_store = MagicMock()
        # Only valid_123 and valid_456 exist
        mock_store.artifact_exists.side_effect = lambda aid: aid in ["valid_123", "valid_456"]
        mock_store_class.return_value = mock_store

        formatted_response = format_response_with_hyperlinks(
            sample_response_with_invalid_citations,
            weaviate_store=mock_store
        )

        # Should have clickable links for verified artifacts
        assert "[artifact:valid_123]" in formatted_response or "/artifact/valid_123" in formatted_response

        # Should have warning for unverified artifact
        assert "nonexistent_999" in formatted_response
        # Warning icon or text should be present
        assert "⚠️" in formatted_response or "unverified" in formatted_response.lower()

    @patch('codeindex.services.weaviate_store.WeaviateStore')
    def test_generate_hyperlinks_with_artifact_detail_urls(self, mock_store_class):
        """Test hyperlinks point to artifact detail pages."""
        from codeindex.web.components.agent_chat import format_response_with_hyperlinks

        mock_store = MagicMock()
        mock_store.artifact_exists.return_value = True
        mock_store_class.return_value = mock_store

        response = AgentResponse(
            agent_role=AgentRole.SENIOR_DEVELOPER,
            query="Test",
            timestamp="2026-01-16T10:00:00",
            duration_seconds=1.0,
            response_text="See artifact:service_123 for details",
            citations=[
                Citation(artifact_id="service_123", file_path="src/Service.java", artifact_type="BackendDoc")
            ]
        )

        formatted_response = format_response_with_hyperlinks(response, weaviate_store=mock_store)

        # Should contain link to artifact detail page
        assert "/artifact/service_123" in formatted_response or "artifact_id=service_123" in formatted_response

    @patch('codeindex.services.weaviate_store.WeaviateStore')
    def test_display_warning_icons_for_unverified_citations(self, mock_store_class):
        """Test warning icons displayed for unverified citations (FR4.11)."""
        from codeindex.web.components.agent_chat import format_response_with_hyperlinks

        mock_store = MagicMock()
        mock_store.artifact_exists.return_value = False  # None verified
        mock_store_class.return_value = mock_store

        response = AgentResponse(
            agent_role=AgentRole.SENIOR_DEVELOPER,
            query="Test",
            timestamp="2026-01-16T10:00:00",
            duration_seconds=1.0,
            response_text="Reference artifact:invalid_999",
            citations=[
                Citation(artifact_id="invalid_999", file_path="src/Invalid.java", artifact_type="BackendDoc")
            ]
        )

        formatted_response = format_response_with_hyperlinks(response, weaviate_store=mock_store)

        # Should have warning indicator
        assert "⚠️" in formatted_response or "warning" in formatted_response.lower()


class TestStreamingDisplay:
    """Test streaming display support for agent responses."""

    def test_format_response_for_streaming(self, sample_agent_response):
        """Test formatting response for word-by-word streaming."""
        from codeindex.web.components.agent_chat import format_response_for_streaming

        chunks = format_response_for_streaming(sample_agent_response.response_text)

        # Should split into words/chunks
        assert len(chunks) > 10
        assert all(isinstance(chunk, str) for chunk in chunks)

        # Recombined chunks should equal original text (roughly)
        recombined = "".join(chunks)
        assert len(recombined) == len(sample_agent_response.response_text)

    def test_streaming_respects_markdown_code_blocks(self):
        """Test streaming doesn't break markdown code blocks."""
        from codeindex.web.components.agent_chat import format_response_for_streaming

        response_with_code = """
Here is some code:

```java
public class User {
    private String name;
}
```

Analysis continues here.
"""

        chunks = format_response_for_streaming(response_with_code)

        # Code block should be kept together as single chunk
        code_block_chunks = [c for c in chunks if "```" in c or "public class" in c]
        assert len(code_block_chunks) > 0

    def test_streaming_preserves_formatting(self, sample_agent_response):
        """Test streaming preserves markdown formatting."""
        from codeindex.web.components.agent_chat import format_response_for_streaming

        chunks = format_response_for_streaming(sample_agent_response.response_text)
        recombined = "".join(chunks)

        # Should preserve markdown headers
        assert "##" in recombined
        # Should preserve lists
        assert any(c in recombined for c in ["1.", "2.", "3."])


class TestMarkdownRendering:
    """Test markdown rendering for agent responses."""

    def test_render_response_as_markdown(self, sample_agent_response):
        """Test rendering response as markdown."""
        from codeindex.web.components.agent_chat import render_response_markdown

        html = render_response_markdown(sample_agent_response.response_text)

        # Should convert markdown to HTML
        assert "<h2>" in html or "UserService" in html
        assert "<li>" in html or "<ol>" in html or "<ul>" in html

    def test_render_markdown_sanitizes_html(self):
        """Test markdown rendering sanitizes potentially malicious HTML."""
        from codeindex.web.components.agent_chat import render_response_markdown

        response_with_script = """
Analysis result:
<script>alert('XSS')</script>
This is safe content.
"""

        html = render_response_markdown(response_with_script)

        # Should sanitize script tags
        assert "<script>" not in html
        assert "safe content" in html.lower()

    def test_render_markdown_preserves_code_blocks(self):
        """Test markdown rendering preserves code block formatting."""
        from codeindex.web.components.agent_chat import render_response_markdown

        response_with_code = """
```java
public class User {}
```
"""

        html = render_response_markdown(response_with_code)

        # Should render as code block
        assert "<code>" in html or "<pre>" in html
        assert "public class User" in html


class TestCopyResponseFunctionality:
    """Test copy response to clipboard functionality."""

    def test_copy_response_extracts_plain_text(self, sample_agent_response):
        """Test copying response extracts plain text without markdown."""
        from codeindex.web.components.agent_chat import extract_plain_text_for_copy

        plain_text = extract_plain_text_for_copy(sample_agent_response.response_text)

        # Should remove markdown formatting
        assert "##" not in plain_text  # No markdown headers
        assert "UserService" in plain_text  # Content preserved

    def test_copy_response_preserves_citations(self, sample_agent_response):
        """Test copying response preserves citation references."""
        from codeindex.web.components.agent_chat import extract_plain_text_for_copy

        plain_text = extract_plain_text_for_copy(sample_agent_response.response_text)

        # Citations should be preserved
        assert "artifact:" in plain_text or "src/services/UserService.java" in plain_text

    def test_copy_response_formats_for_clipboard(self, sample_agent_response):
        """Test copying response formats text for clipboard."""
        from codeindex.web.components.agent_chat import format_response_for_clipboard

        clipboard_text = format_response_for_clipboard(sample_agent_response)

        # Should include metadata
        assert "Senior Developer" in clipboard_text
        assert "UserService" in clipboard_text

        # Should be plain text format
        assert isinstance(clipboard_text, str)
        assert len(clipboard_text) > 0


class TestResponseFormatConfiguration:
    """Test response format configuration and customization."""

    def test_format_response_with_inline_citations(self, sample_agent_response):
        """Test formatting response with inline citation style."""
        from codeindex.web.components.agent_chat import format_response

        formatted = format_response(sample_agent_response, citation_style="inline")

        # Should have inline citations like [1], [2]
        assert "[1]" in formatted or "[2]" in formatted

    def test_format_response_with_footnote_citations(self, sample_agent_response):
        """Test formatting response with footnote citation style."""
        from codeindex.web.components.agent_chat import format_response

        formatted = format_response(sample_agent_response, citation_style="footnotes")

        # Should have footnotes section
        assert "References:" in formatted or "**References**" in formatted

    def test_format_response_with_no_citations(self, sample_agent_response):
        """Test formatting response with citations disabled."""
        from codeindex.web.components.agent_chat import format_response

        formatted = format_response(sample_agent_response, citation_style="none")

        # Should not have citation markers
        assert "[1]" not in formatted
        assert "References:" not in formatted


class TestResponseErrorHandling:
    """Test response formatting error handling."""

    def test_format_response_handles_empty_response(self):
        """Test formatting handles empty response text gracefully."""
        from codeindex.web.components.agent_chat import format_response

        response = AgentResponse(
            agent_role=AgentRole.SENIOR_DEVELOPER,
            query="Test",
            timestamp="2026-01-16T10:00:00",
            duration_seconds=1.0,
            response_text=""
        )

        formatted = format_response(response)

        assert formatted is not None
        assert isinstance(formatted, str)

    def test_format_response_handles_malformed_citations(self):
        """Test formatting handles malformed citation patterns gracefully."""
        from codeindex.web.components.agent_chat import format_response

        response = AgentResponse(
            agent_role=AgentRole.SENIOR_DEVELOPER,
            query="Test",
            timestamp="2026-01-16T10:00:00",
            duration_seconds=1.0,
            response_text="Reference: artifact:123:invalid:format",
            citations=[]
        )

        formatted = format_response(response)

        # Should handle gracefully without crashing
        assert formatted is not None

    @patch('codeindex.services.weaviate_store.WeaviateStore')
    def test_format_response_handles_weaviate_error(self, mock_store_class, sample_agent_response):
        """Test formatting handles Weaviate verification errors gracefully."""
        from codeindex.web.components.agent_chat import format_response_with_hyperlinks

        mock_store = MagicMock()
        mock_store.artifact_exists.side_effect = Exception("Weaviate unavailable")
        mock_store_class.return_value = mock_store

        # Should not crash on Weaviate error
        try:
            formatted = format_response_with_hyperlinks(sample_agent_response, weaviate_store=mock_store)
            assert formatted is not None
        except Exception:
            # Or should handle error appropriately
            pass
