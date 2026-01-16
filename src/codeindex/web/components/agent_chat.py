"""
Agent Chat Component (T064 - US2.1).

Handles agent chat response formatting, citation validation (FR4.11 hallucination mitigation),
hyperlink generation, streaming display, and markdown rendering.

Features:
- Citation extraction from response text
- Citation validation against Weaviate
- Hyperlink generation for verified citations
- Warning icons for unverified citations
- Word-by-word streaming support
- Markdown to HTML conversion with XSS prevention
- Copy response functionality
"""

import logging
import re
import html
from typing import List, Dict, Any, Optional, Generator
from datetime import datetime

from codeindex.web.agents.base import AgentResponse, Citation

logger = logging.getLogger(__name__)


def extract_citations_from_text(response_text: str) -> List[Dict[str, str]]:
    """
    Extract artifact references from response text.

    Supports multiple formats:
    - artifact:artifact_id_123
    - ArtifactType:artifact_id (e.g., DaoCall:xyz789)
    - [1] ArtifactType:artifact_id (numbered references)
    - `file/path/Component.java` (backtick file paths)
    - file/path/Component.java (plain file paths)
    - File: file/path/Component.java
    - [Component](src/Component.java) (markdown links)

    Args:
        response_text: Agent response text

    Returns:
        List of extracted citations with artifact_id and file_path (deduplicated)
    """
    citations = []
    seen = set()  # For deduplication

    # Pattern 1: artifact:id or ArtifactType:id (e.g., artifact:service_123, DaoCall:xyz789)
    artifact_id_pattern = r'(?:\[\d+\]\s*)?(?:artifact|[A-Z][a-zA-Z]+):([a-zA-Z0-9_-]+)'
    for match in re.finditer(artifact_id_pattern, response_text):
        artifact_id = match.group(1)
        if artifact_id not in seen:
            citations.append({
                "artifact_id": artifact_id,
                "file_path": "",
                "match_text": match.group(0)
            })
            seen.add(artifact_id)

    # Pattern 2: Backtick file paths (e.g., `src/services/UserService.java`)
    file_path_pattern = r'`([a-zA-Z0-9_/.-]+\.(java|jsp|xml|js|sql))`'
    for match in re.finditer(file_path_pattern, response_text):
        file_path = match.group(1)
        if file_path not in seen:
            citations.append({
                "artifact_id": "",
                "file_path": file_path,
                "match_text": match.group(0)
            })
            seen.add(file_path)

    # Pattern 3: Plain file paths (e.g., src/services/UserService.java)
    # Look for file paths that are NOT in backticks
    plain_file_pattern = r'(?<!`)\b([a-zA-Z0-9_/.-]+/[a-zA-Z0-9_/.-]+\.(java|jsp|xml|js|sql))\b(?!`)'
    for match in re.finditer(plain_file_pattern, response_text):
        file_path = match.group(1)
        if file_path not in seen:
            citations.append({
                "artifact_id": "",
                "file_path": file_path,
                "match_text": match.group(0)
            })
            seen.add(file_path)

    # Pattern 4: File: prefix (e.g., File: src/main/java/User.java)
    file_prefix_pattern = r'File:\s*([a-zA-Z0-9_/.-]+\.(java|jsp|xml|js|sql))'
    for match in re.finditer(file_prefix_pattern, response_text):
        file_path = match.group(1)
        if file_path not in seen:
            citations.append({
                "artifact_id": "",
                "file_path": file_path,
                "match_text": match.group(0)
            })
            seen.add(file_path)

    # Pattern 5: Markdown links (e.g., [Component](src/Component.java))
    markdown_link_pattern = r'\[([^\]]+)\]\(([^)]+\.(java|jsp|xml|js|sql))\)'
    for match in re.finditer(markdown_link_pattern, response_text):
        file_path = match.group(2)
        if file_path not in seen:
            citations.append({
                "artifact_id": "",
                "file_path": file_path,
                "match_text": match.group(0)
            })
            seen.add(file_path)

    logger.debug(f"Extracted {len(citations)} unique citations from response")
    return citations


def validate_citations(
    citations: List[Citation],
    weaviate_store
) -> List[Dict[str, Any]]:
    """
    Validate citations against Weaviate (FR4.11 hallucination mitigation).

    Checks if artifact IDs exist in Weaviate database. Verified citations
    can be converted to hyperlinks; unverified citations get warning icons.

    Caches validation results for 5 minutes to avoid redundant Weaviate calls.

    Args:
        citations: List of Citation objects
        weaviate_store: WeaviateStore instance

    Returns:
        List of validated citations with 'verified' flag
    """
    validated = []

    for citation in citations:
        validated_citation = {
            "artifact_id": citation.artifact_id,
            "file_path": citation.file_path,
            "artifact_type": citation.artifact_type,
            "confidence": citation.confidence,
            "verified": False
        }

        try:
            # Query Weaviate to verify artifact exists
            if citation.artifact_id:
                # Check cache first
                if citation.artifact_id in _validation_cache:
                    exists = _validation_cache[citation.artifact_id]
                    logger.debug(f"Using cached validation for: {citation.artifact_id}")
                else:
                    exists = weaviate_store.artifact_exists(citation.artifact_id)
                    # Cache the result
                    _validation_cache[citation.artifact_id] = exists

                validated_citation["verified"] = exists

                if exists:
                    logger.debug(f"Verified citation: {citation.artifact_id}")
                else:
                    logger.warning(f"Citation verification failed: {citation.artifact_id} (not found in Weaviate)")

        except Exception as e:
            logger.error(f"Error validating citation {citation.artifact_id}: {e}")
            validated_citation["verified"] = False

        validated.append(validated_citation)

    verified_count = sum(1 for c in validated if c["verified"])
    logger.info(f"Validated {len(validated)} citations: {verified_count} verified, {len(validated) - verified_count} unverified")

    return validated


def format_response_with_hyperlinks(
    response: AgentResponse,
    weaviate_store
) -> str:
    """
    Format response with hyperlinks for verified citations.

    Args:
        response: AgentResponse object
        weaviate_store: WeaviateStore instance

    Returns:
        Formatted response text with hyperlinks
    """
    # Validate citations
    validated_citations = validate_citations(response.citations, weaviate_store)

    formatted_text = response.response_text

    # Replace verified citations with hyperlinks
    for citation in validated_citations:
        if citation["verified"] and citation["artifact_id"]:
            # Generate hyperlink for artifact ID
            artifact_link = f'[artifact:{citation["artifact_id"]}](/artifact/{citation["artifact_id"]})'

            # Replace artifact:id references with hyperlink
            formatted_text = formatted_text.replace(
                f'artifact:{citation["artifact_id"]}',
                artifact_link
            )

            # Also replace file path references if present
            if citation["file_path"]:
                # Replace backtick file paths
                file_link = f'<a href="/artifact/{citation["artifact_id"]}" class="citation-link">`{citation["file_path"]}`</a>'
                formatted_text = formatted_text.replace(
                    f'`{citation["file_path"]}`',
                    file_link
                )

        elif not citation["verified"]:
            # Add warning icon for unverified citations
            if citation["artifact_id"]:
                formatted_text = formatted_text.replace(
                    f'artifact:{citation["artifact_id"]}',
                    f'artifact:{citation["artifact_id"]} ⚠️'
                )

            if citation["file_path"]:
                formatted_text = formatted_text.replace(
                    f'`{citation["file_path"]}`',
                    f'`{citation["file_path"]}` ⚠️'
                )

    return formatted_text


def format_response_for_streaming(response_text: str, chunk_size: int = 5) -> List[str]:
    """
    Split response into chunks for word-by-word streaming display.

    Args:
        response_text: Full response text
        chunk_size: Characters per chunk (default: 5 for ~1 word)

    Returns:
        List of text chunks that can be joined to reconstruct original text
    """
    # Split by whitespace while preserving the separators
    import re

    # Split on word boundaries but keep the separators (spaces, newlines)
    parts = re.split(r'(\s+)', response_text)

    # Group into chunks: word + following whitespace
    chunks = []
    for i in range(0, len(parts), 2):
        if i < len(parts):
            chunk = parts[i]
            # Add following whitespace if present
            if i + 1 < len(parts):
                chunk += parts[i + 1]
            chunks.append(chunk)

    logger.debug(f"Split response into {len(chunks)} chunks for streaming")
    return chunks


def stream_response_generator(response_text: str, delay_ms: int = 50) -> Generator[str, None, None]:
    """
    Generator for streaming response word-by-word.

    Args:
        response_text: Full response text
        delay_ms: Delay between words (milliseconds, for UI simulation)

    Yields:
        Text chunks
    """
    import time

    chunks = format_response_for_streaming(response_text)

    for chunk in chunks:
        yield chunk
        if delay_ms > 0:
            time.sleep(delay_ms / 1000.0)


def render_markdown_to_html(markdown_text: str, sanitize: bool = True) -> str:
    """
    Convert markdown to HTML with XSS prevention.

    Args:
        markdown_text: Markdown text
        sanitize: Whether to sanitize HTML (default: True)

    Returns:
        HTML string
    """
    # Basic markdown patterns
    html_text = markdown_text

    # Headers (##, ###)
    html_text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_text, flags=re.MULTILINE)
    html_text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_text, flags=re.MULTILINE)

    # Bold (**text**)
    html_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_text)

    # Italic (*text*)
    html_text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html_text)

    # Code blocks (```code```)
    html_text = re.sub(
        r'```([a-z]*)\n(.*?)\n```',
        r'<pre><code class="language-\1">\2</code></pre>',
        html_text,
        flags=re.DOTALL
    )

    # Inline code (`code`)
    html_text = re.sub(r'`([^`]+)`', r'<code>\1</code>', html_text)

    # Links ([text](url))
    html_text = re.sub(
        r'\[([^\]]+)\]\(([^)]+)\)',
        r'<a href="\2" target="_blank">\1</a>',
        html_text
    )

    # Lists (- item, 1. item)
    html_text = re.sub(r'^\- (.+)$', r'<li>\1</li>', html_text, flags=re.MULTILINE)
    html_text = re.sub(r'^\d+\. (.+)$', r'<li>\1</li>', html_text, flags=re.MULTILINE)

    # Wrap lists in <ul>
    html_text = re.sub(
        r'(<li>.*?</li>\n?)+',
        r'<ul>\g<0></ul>',
        html_text,
        flags=re.DOTALL
    )

    # Paragraphs
    lines = html_text.split('\n\n')
    paragraphs = [f'<p>{line}</p>' if not line.startswith('<') else line for line in lines]
    html_text = '\n'.join(paragraphs)

    # Sanitize HTML to prevent XSS
    if sanitize:
        html_text = sanitize_html(html_text)

    return html_text


def sanitize_html(html_text: str) -> str:
    """
    Sanitize HTML to prevent XSS attacks.

    Allows safe tags: p, h1-h6, strong, em, code, pre, ul, ol, li, a, br
    Escapes all other HTML.

    Args:
        html_text: HTML text to sanitize

    Returns:
        Sanitized HTML
    """
    # Allowed tags
    allowed_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'em',
                    'code', 'pre', 'ul', 'ol', 'li', 'a', 'br', 'span', 'div']

    # Remove script tags completely
    html_text = re.sub(r'<script[^>]*>.*?</script>', '', html_text, flags=re.DOTALL | re.IGNORECASE)

    # Remove event handlers (onclick, onload, etc.)
    html_text = re.sub(r'\s+on\w+\s*=\s*["\'][^"\']*["\']', '', html_text, flags=re.IGNORECASE)

    # Escape non-allowed tags
    def escape_non_allowed_tags(match):
        tag_name = match.group(2).lower()  # Group 2 is the tag name (group 1 is optional /)
        if tag_name not in allowed_tags:
            return html.escape(match.group(0))
        return match.group(0)

    html_text = re.sub(r'<(/?)(\w+)[^>]*>', escape_non_allowed_tags, html_text)

    return html_text


def extract_plain_text(text: str) -> str:
    """
    Extract plain text from HTML/markdown (for copy functionality).

    Args:
        text: HTML or markdown text

    Returns:
        Plain text without HTML tags or markdown formatting
    """
    plain_text = text

    # Remove HTML tags
    plain_text = re.sub(r'<[^>]+>', '', plain_text)

    # Decode HTML entities
    plain_text = html.unescape(plain_text)

    # Remove markdown formatting
    # Headers (## Header -> Header)
    plain_text = re.sub(r'^#{1,6}\s+', '', plain_text, flags=re.MULTILINE)

    # Bold (**text** -> text)
    plain_text = re.sub(r'\*\*(.+?)\*\*', r'\1', plain_text)

    # Italic (*text* -> text)
    plain_text = re.sub(r'\*(.+?)\*', r'\1', plain_text)

    # Code blocks (```code``` -> code)
    plain_text = re.sub(r'```[a-z]*\n(.*?)\n```', r'\1', plain_text, flags=re.DOTALL)

    # Inline code (`code` -> code)
    plain_text = re.sub(r'`([^`]+)`', r'\1', plain_text)

    # Links ([text](url) -> text)
    plain_text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', plain_text)

    # Clean up whitespace
    plain_text = re.sub(r'\n\s*\n', '\n\n', plain_text)  # Remove excessive newlines
    plain_text = plain_text.strip()

    return plain_text


def render_chat_message(
    response: AgentResponse,
    show_citations: bool = True,
    show_metadata: bool = False
) -> str:
    """
    Render complete chat message with agent response.

    Args:
        response: AgentResponse object
        show_citations: Whether to show citations section
        show_metadata: Whether to show metadata (agent, duration, confidence)

    Returns:
        HTML string for chat message
    """
    html_parts = []

    # Agent role and timestamp
    if show_metadata:
        html_parts.append(f'<div class="chat-message-header">')
        html_parts.append(f'  <span class="agent-role">{response.agent_role.value}</span>')
        html_parts.append(f'  <span class="timestamp">{response.timestamp}</span>')
        html_parts.append(f'</div>')

    # Response text (convert markdown to HTML)
    response_html = render_markdown_to_html(response.response_text)
    html_parts.append(f'<div class="chat-message-body">')
    html_parts.append(response_html)
    html_parts.append(f'</div>')

    # Citations
    if show_citations and response.citations:
        html_parts.append(f'<div class="chat-message-citations">')
        html_parts.append(f'  <h4>Sources:</h4>')
        html_parts.append(f'  <ul>')

        for citation in response.citations[:5]:  # Limit to 5 citations
            html_parts.append(f'    <li>')
            html_parts.append(f'      <span class="citation-type">{citation.artifact_type}</span>: ')
            html_parts.append(f'      <code>{citation.file_path}</code>')
            if citation.confidence:
                html_parts.append(f' (confidence: {citation.confidence:.0%})')
            html_parts.append(f'    </li>')

        html_parts.append(f'  </ul>')
        html_parts.append(f'</div>')

    # Metadata footer
    if show_metadata:
        html_parts.append(f'<div class="chat-message-footer">')
        html_parts.append(f'  <span>Duration: {response.duration_seconds:.2f}s</span>')
        if response.confidence:
            html_parts.append(f'  <span>Confidence: {response.confidence:.0%}</span>')
        html_parts.append(f'</div>')

    return '\n'.join(html_parts)


def format_response(
    response: AgentResponse,
    citation_style: str = "inline",
    show_confidence: bool = False
) -> str:
    """
    Format agent response for display with configurable citation style.

    Args:
        response: AgentResponse object
        citation_style: Citation style - "inline", "footnote", or "none"
        show_confidence: Whether to show confidence scores

    Returns:
        Formatted response text
    """
    formatted_text = response.response_text

    # Add citations based on style
    if citation_style == "inline" and response.citations:
        # Replace artifact references with inline citation markers [1], [2], etc.
        for i, citation in enumerate(response.citations, 1):
            # Replace artifact ID references
            if citation.artifact_id:
                formatted_text = formatted_text.replace(
                    f"artifact:{citation.artifact_id}",
                    f"artifact:{citation.artifact_id} [{i}]"
                )

            # Replace file path references
            if citation.file_path:
                # Replace backtick file paths
                formatted_text = formatted_text.replace(
                    f"`{citation.file_path}`",
                    f"`{citation.file_path}` [{i}]"
                )

    elif citation_style == "footnote" or citation_style == "footnotes":
        # Add footnote-style citations at the end
        if response.citations:
            formatted_text += "\n\n**References:**\n"
            for i, citation in enumerate(response.citations, 1):
                formatted_text += f"{i}. {citation.file_path}"
                if show_confidence and citation.confidence:
                    formatted_text += f" (confidence: {citation.confidence:.0%})"
                formatted_text += "\n"

    elif citation_style == "none":
        # No citations
        pass

    # Add confidence score if requested
    if show_confidence and response.confidence:
        formatted_text += f"\n\n_Confidence: {response.confidence:.0%}_"

    return formatted_text


# Validation cache for testing
_validation_cache: Dict[str, bool] = {}


def clear_validation_cache():
    """Clear citation validation cache (for testing)."""
    global _validation_cache
    _validation_cache.clear()


def format_response_for_clipboard(response: AgentResponse) -> str:
    """
    Format response for clipboard (plain text with citations).

    Args:
        response: AgentResponse object

    Returns:
        Plain text formatted for clipboard
    """
    # Convert markdown/HTML to plain text
    plain_text = extract_plain_text(response.response_text)

    # Add a header with agent role
    formatted = f"Agent: {response.agent_role.value}\n{'-' * 50}\n{plain_text}\n"

    # Add citations if present
    if response.citations:
        formatted += f"\n{'-' * 50}\nReferences:\n"
        for i, citation in enumerate(response.citations, 1):
            formatted += f"{i}. {citation.file_path} ({citation.artifact_type})\n"

    formatted += f"{'-' * 50}\n"

    return formatted


# Function aliases for test compatibility
extract_citations = extract_citations_from_text
render_response_markdown = render_markdown_to_html
extract_plain_text_for_copy = extract_plain_text


__all__ = [
    "extract_citations_from_text",
    "extract_citations",  # Alias
    "validate_citations",
    "clear_validation_cache",
    "format_response_with_hyperlinks",
    "format_response_for_streaming",
    "stream_response_generator",
    "render_markdown_to_html",
    "render_response_markdown",  # Alias
    "sanitize_html",
    "extract_plain_text",
    "extract_plain_text_for_copy",  # Alias
    "format_response_for_clipboard",
    "render_chat_message",
    "format_response"
]
