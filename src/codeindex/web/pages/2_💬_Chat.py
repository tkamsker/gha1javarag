"""
Chat page for GEMINI Code Analysis Pipeline Web UI (T058 - US2.1).

This page provides AI agent chat interface with:
- Multi-agent support (Senior Developer, Data Analyst, Frontend/Backend Specialists, etc.)
- Chat history with messages
- Agent response streaming
- Citation display with hyperlinks
- Agent selection dropdown
- Follow-up question suggestions
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
from codeindex.web.agents.base import AgentRole, AgentResponse
from codeindex.web.utils.session_state import (
    initialize_session_state,
    get,
    set_value,
    append_to_list,
    clear_list
)


def initialize_chat_state():
    """Initialize session state for chat page."""
    defaults = {
        "chat_history": [],
        "chat_input": "",
        "chat_loading": False,
        "chat_error": None,
        "selected_agent": None,  # None = auto-route
        "agent_settings": {
            "verbosity": "standard",
            "technical_level": "senior",
            "citation_style": "inline"
        }
    }

    initialize_session_state(defaults)


def render_agent_selector():
    """Render agent selection dropdown in sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.subheader("🤖 Agent Selection")

    agent_options = {
        "Auto (Recommended)": None,
        "Senior Developer": AgentRole.SENIOR_DEVELOPER,
        "Data Analyst": AgentRole.DATA_ANALYST,
        "Frontend Specialist": AgentRole.FRONTEND_SPECIALIST,
        "Backend Specialist": AgentRole.BACKEND_SPECIALIST,
        "PRD Writer": AgentRole.PRD_WRITER,
        "Spec-Kit Writer": AgentRole.SPECKIT_WRITER,
        "Gherkin Test Writer": AgentRole.GHERKIN_TEST_WRITER,
        "Playwright Test Writer": AgentRole.PLAYWRIGHT_TEST_WRITER
    }

    selected = st.sidebar.selectbox(
        "Select Agent",
        options=list(agent_options.keys()),
        index=0,
        help="Choose 'Auto' to let the system route your query to the best agent"
    )

    set_value("selected_agent", agent_options[selected])

    # Show agent description
    if agent_options[selected]:
        role = agent_options[selected]
        descriptions = {
            AgentRole.SENIOR_DEVELOPER: "Explains code architecture, design patterns, and best practices",
            AgentRole.DATA_ANALYST: "Analyzes database schemas, data flows, and entity relationships",
            AgentRole.FRONTEND_SPECIALIST: "Documents UI components, user flows, and frontend architecture",
            AgentRole.BACKEND_SPECIALIST: "Analyzes backend services, APIs, and business logic",
            AgentRole.PRD_WRITER: "Generates product requirements documents",
            AgentRole.SPECKIT_WRITER: "Creates technical specifications and implementation plans",
            AgentRole.GHERKIN_TEST_WRITER: "Generates BDD test cases in Gherkin format",
            AgentRole.PLAYWRIGHT_TEST_WRITER: "Generates Playwright E2E test scripts"
        }

        st.sidebar.caption(f"**{role.value}**: {descriptions[role]}")


def render_agent_settings():
    """Render agent settings in sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Agent Settings")

    verbosity = st.sidebar.select_slider(
        "Response Detail",
        options=["concise", "standard", "detailed"],
        value=get("agent_settings", {}).get("verbosity", "standard"),
        help="Control how detailed the agent responses should be"
    )

    technical_level = st.sidebar.select_slider(
        "Technical Level",
        options=["junior", "mid", "senior"],
        value=get("agent_settings", {}).get("technical_level", "senior"),
        help="Adjust explanations for your technical expertise level"
    )

    citation_style = st.sidebar.selectbox(
        "Citation Style",
        options=["inline", "footnotes", "none"],
        index=["inline", "footnotes", "none"].index(
            get("agent_settings", {}).get("citation_style", "inline")
        ),
        help="How to display code references in responses"
    )

    # Update settings
    set_value("agent_settings", {
        "verbosity": verbosity,
        "technical_level": technical_level,
        "citation_style": citation_style
    })


def render_chat_history():
    """Render chat message history."""
    history = get("chat_history", [])

    if not history:
        st.info("👋 Welcome! Ask me anything about your codebase.")

        st.markdown("""
        **Example questions:**
        - "What does the user registration module do?"
        - "Explain the database schema for orders"
        - "How is authentication implemented?"
        - "What are the main GWT presenters?"
        - "Generate a PRD for the payment workflow"
        """)
        return

    # Render messages
    for message in history:
        role = message.get("role", "user")
        content = message.get("content", "")

        if role == "user":
            with st.chat_message("user"):
                st.markdown(content)

        elif role == "assistant":
            agent_role = message.get("agent_role", "Assistant")
            confidence = message.get("confidence", 0.0)
            citations = message.get("citations", [])
            suggested_questions = message.get("suggested_questions", [])

            with st.chat_message("assistant"):
                # Agent badge
                st.caption(f"🤖 **{agent_role}** • Confidence: {confidence * 100:.0f}%")

                # Response content
                st.markdown(content)

                # Citations
                if citations:
                    with st.expander(f"📚 Citations ({len(citations)})"):
                        for i, citation in enumerate(citations, 1):
                            file_path = citation.get("file_path", "")
                            artifact_type = citation.get("artifact_type", "")
                            line_start = citation.get("line_start")
                            line_end = citation.get("line_end")

                            citation_text = f"{i}. `{file_path}`"
                            if artifact_type:
                                citation_text += f" ({artifact_type})"
                            if line_start and line_end:
                                citation_text += f" - Lines {line_start}-{line_end}"

                            st.markdown(citation_text)

                # Suggested follow-ups
                if suggested_questions:
                    st.caption("**💡 Follow-up questions:**")
                    for question in suggested_questions:
                        if st.button(question, key=f"followup_{hash(question)}_{time.time()}"):
                            set_value("chat_input", question)
                            st.rerun()


def render_chat_input():
    """Render chat input field (T059)."""
    # Chat input
    user_input = st.chat_input(
        "Ask a question about your codebase...",
        key="chat_message_input"
    )

    if user_input:
        # Add user message to history
        append_to_list("chat_history", {
            "role": "user",
            "content": user_input
        })

        # Execute agent query
        execute_agent_query(user_input)

        st.rerun()


def execute_agent_query(query: str):
    """Execute agent query and add response to history."""
    set_value("chat_loading", True)
    set_value("chat_error", None)

    try:
        # Get agent service
        agent_service = get_agent_service()

        # Get selected agent and settings
        selected_agent = get("selected_agent")
        agent_settings = get("agent_settings", {})

        # Execute query
        start_time = time.time()

        response: AgentResponse = agent_service.execute_query(
            query=query,
            agent_role=selected_agent,
            agent_settings=agent_settings
        )

        end_time = time.time()

        # Log performance
        import logging
        logger = logging.getLogger(__name__)
        logger.info(
            f"Agent query executed: agent={response.agent_role.value}, "
            f"query='{query[:50]}...', "
            f"time={response.duration_seconds:.2f}s"
        )

        # Add response to history
        if response.has_error():
            # Error response
            append_to_list("chat_history", {
                "role": "assistant",
                "agent_role": response.agent_role.value,
                "content": f"❌ Error: {response.error}",
                "confidence": 0.0,
                "citations": [],
                "suggested_questions": []
            })

            set_value("chat_error", response.error)

        else:
            # Successful response
            append_to_list("chat_history", {
                "role": "assistant",
                "agent_role": response.agent_role.value,
                "content": response.response_text,
                "confidence": response.confidence,
                "citations": [c.to_dict() for c in response.citations],
                "suggested_questions": response.suggested_questions
            })

    except Exception as e:
        # Error handling
        set_value("chat_error", str(e))

        append_to_list("chat_history", {
            "role": "assistant",
            "agent_role": "System",
            "content": f"❌ Failed to process query: {str(e)}",
            "confidence": 0.0,
            "citations": [],
            "suggested_questions": []
        })

        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Agent query failed: {e}", exc_info=True)

    finally:
        set_value("chat_loading", False)


def render_chat_actions():
    """Render chat action buttons."""
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            clear_list("chat_history")
            set_value("chat_error", None)
            st.rerun()

    with col2:
        if st.button("💾 Export Chat", use_container_width=True):
            export_chat_history()


def export_chat_history():
    """Export chat history to markdown."""
    history = get("chat_history", [])

    if not history:
        st.warning("No chat history to export")
        return

    # Build markdown
    markdown = "# Chat History\n\n"
    markdown += f"*Exported: {time.strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    markdown += "---\n\n"

    for message in history:
        role = message.get("role", "user")
        content = message.get("content", "")

        if role == "user":
            markdown += f"## 👤 User\n\n{content}\n\n"

        elif role == "assistant":
            agent_role = message.get("agent_role", "Assistant")
            confidence = message.get("confidence", 0.0)
            citations = message.get("citations", [])

            markdown += f"## 🤖 {agent_role}\n\n"
            markdown += f"*Confidence: {confidence * 100:.0f}%*\n\n"
            markdown += f"{content}\n\n"

            if citations:
                markdown += "**Citations:**\n\n"
                for i, citation in enumerate(citations, 1):
                    file_path = citation.get("file_path", "")
                    markdown += f"{i}. `{file_path}`\n"
                markdown += "\n"

        markdown += "---\n\n"

    # Show download button
    st.download_button(
        label="📥 Download Markdown",
        data=markdown,
        file_name=f"chat_history_{int(time.time())}.md",
        mime="text/markdown"
    )


def main():
    """Main chat page function."""
    # Page configuration
    st.title("💬 AI Agent Chat")

    st.markdown("""
    Ask questions to specialized AI agents who can analyze your codebase and provide
    detailed explanations, generate documentation, and more.
    """)

    # Initialize session state
    initialize_chat_state()

    # Render sidebar controls
    render_agent_selector()
    render_agent_settings()

    # Show loading indicator
    if get("chat_loading", False):
        with st.spinner("🤖 Agent is thinking..."):
            time.sleep(0.1)

    # Show error if present
    error = get("chat_error")
    if error:
        st.error(f"❌ {error}")

    # Render chat history
    render_chat_history()

    # Render action buttons
    st.markdown("---")
    render_chat_actions()

    # Render input (at bottom)
    render_chat_input()


if __name__ == "__main__":
    main()
