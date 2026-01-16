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
from codeindex.web.services.search_service import get_search_service
from codeindex.web.services.erd_generator import get_erd_generator
from codeindex.web.services.db_quality import get_db_quality_analyzer
from codeindex.web.agents.base import AgentRole, AgentResponse
from codeindex.web.utils.session_state import (
    initialize_session_state,
    get,
    set_value,
    append_to_list,
    clear_list
)
from codeindex.web.workflows.prd_generation import PrdGenerationWorkflow
from codeindex.web.components.progress_indicator import (
    render_workflow_progress,
    render_workflow_cancellation_button
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
        },
        # T093 - Artifact selection for PRD generation
        "selected_artifacts": [],
        "artifacts_loaded": False,
        "available_artifacts": {
            "backend": [],
            "frontend": [],
            "data": []
        },
        # T094 - PRD workflow tracking
        "prd_workflow_running": False,
        "prd_workflow_progress": {
            "current_step": 0,
            "total_steps": 4,
            "current_agent": None
        },
        # T095 - Workflow cancellation
        "prd_workflow_instance": None,
        # T097 - PRD download
        "latest_prd_content": None,
        "latest_prd_timestamp": None
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


def load_available_artifacts():
    """Load available artifacts from Weaviate for PRD generation (T093)."""
    try:
        search_service = get_search_service()

        # Load backend artifacts
        backend_response = search_service.search(
            query="",
            filters={"artifact_types": ["BackendDoc", "GwtEndpoint", "DaoCall"]},
            limit=100
        )
        backend_artifacts = backend_response.get("results", [])

        # Load frontend artifacts
        frontend_response = search_service.search(
            query="",
            filters={"artifact_types": ["GwtPresenter", "GwtView", "GwtUiBinder", "JspForm"]},
            limit=100
        )
        frontend_artifacts = frontend_response.get("results", [])

        # Load data artifacts
        data_response = search_service.search(
            query="",
            filters={"artifact_types": ["DbTable", "DtoArtifact", "IbatisStatement"]},
            limit=100
        )
        data_artifacts = data_response.get("results", [])

        # Update session state
        set_value("available_artifacts", {
            "backend": backend_artifacts,
            "frontend": frontend_artifacts,
            "data": data_artifacts
        })
        set_value("artifacts_loaded", True)

        import logging
        logger = logging.getLogger(__name__)
        logger.info(
            f"Loaded artifacts for PRD: backend={len(backend_artifacts)}, "
            f"frontend={len(frontend_artifacts)}, data={len(data_artifacts)}"
        )

    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to load artifacts: {e}", exc_info=True)

        set_value("artifacts_loaded", False)


def render_artifact_selection():
    """Render artifact selection UI for PRD generation (T093)."""
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 PRD Artifact Selection")

    st.sidebar.caption("Select artifacts to include in PRD generation")

    # Load artifacts if not loaded
    if not get("artifacts_loaded", False):
        if st.sidebar.button("🔄 Load Artifacts", use_container_width=True):
            with st.spinner("Loading artifacts..."):
                load_available_artifacts()
            st.rerun()
        return

    available_artifacts = get("available_artifacts", {})
    selected_artifacts = get("selected_artifacts", [])

    # Backend artifacts
    backend_artifacts = available_artifacts.get("backend", [])
    if backend_artifacts:
        st.sidebar.markdown("**⚙️ Backend** ({} artifacts)".format(len(backend_artifacts)))

        # Select all/none buttons
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("All", key="backend_all", use_container_width=True):
                backend_ids = [a["id"] for a in backend_artifacts]
                selected_artifacts = list(set(selected_artifacts + backend_ids))
                set_value("selected_artifacts", selected_artifacts)
                st.rerun()
        with col2:
            if st.button("None", key="backend_none", use_container_width=True):
                backend_ids = [a["id"] for a in backend_artifacts]
                selected_artifacts = [aid for aid in selected_artifacts if aid not in backend_ids]
                set_value("selected_artifacts", selected_artifacts)
                st.rerun()

        # Show top 10 backend artifacts with checkboxes
        for artifact in backend_artifacts[:10]:
            artifact_id = artifact["id"]
            artifact_name = artifact.get("fileName", artifact_id)
            artifact_type = artifact.get("artifactType", "")

            is_selected = artifact_id in selected_artifacts

            if st.sidebar.checkbox(
                f"{artifact_name} ({artifact_type})",
                value=is_selected,
                key=f"artifact_{artifact_id}"
            ):
                if artifact_id not in selected_artifacts:
                    selected_artifacts.append(artifact_id)
            else:
                if artifact_id in selected_artifacts:
                    selected_artifacts.remove(artifact_id)

        if len(backend_artifacts) > 10:
            st.sidebar.caption(f"+ {len(backend_artifacts) - 10} more backend artifacts")

    # Frontend artifacts
    frontend_artifacts = available_artifacts.get("frontend", [])
    if frontend_artifacts:
        st.sidebar.markdown("**🎨 Frontend** ({} artifacts)".format(len(frontend_artifacts)))

        # Select all/none buttons
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("All", key="frontend_all", use_container_width=True):
                frontend_ids = [a["id"] for a in frontend_artifacts]
                selected_artifacts = list(set(selected_artifacts + frontend_ids))
                set_value("selected_artifacts", selected_artifacts)
                st.rerun()
        with col2:
            if st.button("None", key="frontend_none", use_container_width=True):
                frontend_ids = [a["id"] for a in frontend_artifacts]
                selected_artifacts = [aid for aid in selected_artifacts if aid not in frontend_ids]
                set_value("selected_artifacts", selected_artifacts)
                st.rerun()

        # Show top 10 frontend artifacts
        for artifact in frontend_artifacts[:10]:
            artifact_id = artifact["id"]
            artifact_name = artifact.get("fileName", artifact_id)
            artifact_type = artifact.get("artifactType", "")

            is_selected = artifact_id in selected_artifacts

            if st.sidebar.checkbox(
                f"{artifact_name} ({artifact_type})",
                value=is_selected,
                key=f"artifact_{artifact_id}"
            ):
                if artifact_id not in selected_artifacts:
                    selected_artifacts.append(artifact_id)
            else:
                if artifact_id in selected_artifacts:
                    selected_artifacts.remove(artifact_id)

        if len(frontend_artifacts) > 10:
            st.sidebar.caption(f"+ {len(frontend_artifacts) - 10} more frontend artifacts")

    # Data artifacts
    data_artifacts = available_artifacts.get("data", [])
    if data_artifacts:
        st.sidebar.markdown("**📊 Data** ({} artifacts)".format(len(data_artifacts)))

        # Select all/none buttons
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("All", key="data_all", use_container_width=True):
                data_ids = [a["id"] for a in data_artifacts]
                selected_artifacts = list(set(selected_artifacts + data_ids))
                set_value("selected_artifacts", selected_artifacts)
                st.rerun()
        with col2:
            if st.button("None", key="data_none", use_container_width=True):
                data_ids = [a["id"] for a in data_artifacts]
                selected_artifacts = [aid for aid in selected_artifacts if aid not in data_ids]
                set_value("selected_artifacts", selected_artifacts)
                st.rerun()

        # Show top 10 data artifacts
        for artifact in data_artifacts[:10]:
            artifact_id = artifact["id"]
            artifact_name = artifact.get("fileName", artifact_id)
            artifact_type = artifact.get("artifactType", "")

            is_selected = artifact_id in selected_artifacts

            if st.sidebar.checkbox(
                f"{artifact_name} ({artifact_type})",
                value=is_selected,
                key=f"artifact_{artifact_id}"
            ):
                if artifact_id not in selected_artifacts:
                    selected_artifacts.append(artifact_id)
            else:
                if artifact_id in selected_artifacts:
                    selected_artifacts.remove(artifact_id)

        if len(data_artifacts) > 10:
            st.sidebar.caption(f"+ {len(data_artifacts) - 10} more data artifacts")

    # Update session state
    set_value("selected_artifacts", selected_artifacts)

    # Show selection summary
    st.sidebar.markdown("---")
    st.sidebar.caption(f"**Selected:** {len(selected_artifacts)} artifact(s)")

    # Clear selection button
    if selected_artifacts:
        if st.sidebar.button("🗑️ Clear Selection", use_container_width=True):
            set_value("selected_artifacts", [])
            st.rerun()

    # T097 - PRD download button
    latest_prd = get("latest_prd_content")
    prd_timestamp = get("latest_prd_timestamp")

    if latest_prd:
        st.sidebar.markdown("---")
        st.sidebar.subheader("📥 Download PRD")

        # Format timestamp
        if prd_timestamp:
            timestamp_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(prd_timestamp))
            st.sidebar.caption(f"Last generated: {timestamp_str}")

        # Download button
        prd_filename = f"prd_{int(prd_timestamp or time.time())}.md"

        st.sidebar.download_button(
            label="📥 Download PRD (Markdown)",
            data=latest_prd,
            file_name=prd_filename,
            mime="text/markdown",
            use_container_width=True,
            key="download_prd_button"
        )


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


def generate_prd_workflow():
    """
    Execute multi-agent PRD generation workflow (T094).

    This function:
    1. Retrieves selected artifacts from session state
    2. Executes 4-agent workflow (Backend → Frontend → Data → PRD Writer)
    3. Displays real-time progress with progress indicator
    4. Adds generated PRD to chat history with agent responses
    """
    set_value("prd_workflow_running", True)
    set_value("chat_error", None)

    try:
        import logging
        logger = logging.getLogger(__name__)
        logger.info("Starting PRD generation workflow")

        # Step 1: Get selected artifacts
        selected_artifact_ids = get("selected_artifacts", [])

        if not selected_artifact_ids:
            # No artifacts selected
            append_to_list("chat_history", {
                "role": "assistant",
                "agent_role": "PRD Writer",
                "content": "⚠️ No artifacts selected. Please select at least one artifact from the sidebar before generating a PRD.",
                "confidence": 1.0,
                "citations": [],
                "suggested_questions": [
                    "How do I select artifacts for PRD generation?",
                    "What artifact types are available?"
                ]
            })
            return

        # Step 2: Load full artifact data from Weaviate
        available_artifacts = get("available_artifacts", {})
        all_artifacts = (
            available_artifacts.get("backend", []) +
            available_artifacts.get("frontend", []) +
            available_artifacts.get("data", [])
        )

        selected_artifacts = [
            artifact for artifact in all_artifacts
            if artifact["id"] in selected_artifact_ids
        ]

        logger.info(f"Selected {len(selected_artifacts)} artifacts for PRD generation")

        if not selected_artifacts:
            append_to_list("chat_history", {
                "role": "assistant",
                "agent_role": "PRD Writer",
                "content": "⚠️ Selected artifacts could not be loaded. Please try reloading artifacts.",
                "confidence": 0.0,
                "citations": [],
                "suggested_questions": []
            })
            return

        # Step 3: Define progress callback
        def progress_callback(current_step, total_steps, current_agent):
            """Update progress in session state."""
            set_value("prd_workflow_progress", {
                "current_step": current_step,
                "total_steps": total_steps,
                "current_agent": current_agent
            })

        # Step 4: Execute workflow
        workflow = PrdGenerationWorkflow()

        # T095 - Store workflow instance for cancellation
        set_value("prd_workflow_instance", workflow)

        result = workflow.execute(
            artifacts=selected_artifacts,
            project_name="Generated PRD",
            progress_callback=progress_callback
        )

        logger.info(f"PRD workflow completed: success={result['success']}")

        # Step 5: Add result to chat history
        if result["success"]:
            # Successful PRD generation
            prd_content = result["prd_content"]
            steps = result["steps"]

            # T097 - Store PRD for download
            set_value("latest_prd_content", prd_content)
            set_value("latest_prd_timestamp", time.time())

            # Create response with PRD content
            response_content = f"""## 📝 Product Requirements Document Generated

**Summary:** Analyzed {len(selected_artifacts)} artifact(s) using 4 specialized agents

### Generated PRD

{prd_content}

---

*Generated at {time.strftime('%Y-%m-%d %H:%M:%S')}*
"""

            # Collect citations from all steps
            all_citations = []
            for step in steps:
                if step["status"] == "completed":
                    step_citations = step.get("citations", [])
                    all_citations.extend(step_citations)

            # Deduplicate citations by artifact_id
            seen_ids = set()
            unique_citations = []
            for citation in all_citations:
                artifact_id = citation.get("artifact_id", "")
                if artifact_id and artifact_id not in seen_ids:
                    seen_ids.add(artifact_id)
                    unique_citations.append(citation)

            append_to_list("chat_history", {
                "role": "assistant",
                "agent_role": "PRD Writer",
                "content": response_content,
                "confidence": 1.0,
                "citations": unique_citations[:10],  # Limit to top 10 citations
                "suggested_questions": [
                    "Can you explain the user stories in detail?",
                    "What are the main functional requirements?",
                    "Are there any technical risks identified?",
                    "What should be done next with this PRD?"
                ]
            })

        else:
            # Workflow failed
            error_message = result.get("error", "Unknown error")
            steps = result.get("steps", [])

            append_to_list("chat_history", {
                "role": "assistant",
                "agent_role": "PRD Writer",
                "content": f"""❌ PRD generation failed: {error_message}

**Workflow Steps:**
{_format_workflow_steps(steps)}

Please check the logs for more details or try again with different artifacts.
""",
                "confidence": 0.0,
                "citations": [],
                "suggested_questions": [
                    "What went wrong with PRD generation?",
                    "How can I troubleshoot this error?"
                ]
            })

            set_value("chat_error", error_message)

        logger.info("PRD workflow results added to chat history")

    except Exception as e:
        # Error handling
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"PRD generation workflow failed: {e}", exc_info=True)

        set_value("chat_error", str(e))

        append_to_list("chat_history", {
            "role": "assistant",
            "agent_role": "PRD Writer",
            "content": f"❌ Failed to generate PRD: {str(e)}",
            "confidence": 0.0,
            "citations": [],
            "suggested_questions": []
        })

    finally:
        set_value("prd_workflow_running", False)
        set_value("prd_workflow_instance", None)  # T095 - Clear workflow instance
        st.rerun()


def _format_workflow_steps(steps: List[Dict[str, Any]]) -> str:
    """Format workflow steps for display."""
    if not steps:
        return "No steps recorded"

    lines = []
    for step in steps:
        agent_role = step.get("agent_role", "Unknown")
        status = step.get("status", "pending")

        status_icon = {
            "completed": "✅",
            "failed": "❌",
            "in_progress": "⏳",
            "pending": "⏸️"
        }.get(status, "❓")

        lines.append(f"- {status_icon} **{agent_role}**: {status}")

        if status == "failed":
            error = step.get("error", "No error details")
            lines.append(f"  - Error: {error}")

    return "\n".join(lines)


def analyze_database_schema():
    """
    Analyze database schema workflow (T075, T076).

    This function:
    1. Queries Weaviate for all DbTable artifacts
    2. Generates ERD diagram using ErdGenerator
    3. Generates quality report using DbQualityAnalyzer
    4. Adds results to chat history with formatted Mermaid diagram and report
    """
    set_value("chat_loading", True)
    set_value("chat_error", None)

    try:
        import logging
        logger = logging.getLogger(__name__)
        logger.info("Starting database schema analysis workflow")

        # Step 1: Query Weaviate for DbTable artifacts
        search_service = get_search_service()
        search_response = search_service.search(
            query="",  # Empty query to get all tables
            filters={"artifact_types": ["DbTable"]},
            limit=100
        )

        tables = search_response.get("results", [])
        total_tables = search_response.get("total", 0)

        logger.info(f"Found {total_tables} database tables")

        if not tables:
            # No tables found
            append_to_list("chat_history", {
                "role": "assistant",
                "agent_role": "Data Analyst",
                "content": "⚠️ No database tables found in the indexed codebase. Please ensure database schema files have been discovered and indexed.",
                "confidence": 1.0,
                "citations": [],
                "suggested_questions": [
                    "What artifact types are indexed?",
                    "How do I index database schema files?"
                ]
            })
            return

        # Step 2: Generate ERD diagram
        erd_generator = get_erd_generator()
        erd_diagram = erd_generator.generate_mermaid_erd(tables)

        logger.info(f"Generated ERD diagram with {len(tables)} tables")

        # Step 3: Generate quality report
        quality_analyzer = get_db_quality_analyzer()
        quality_report = quality_analyzer.analyze_schema(tables)
        quality_markdown = quality_analyzer.format_report_markdown(quality_report)

        logger.info(f"Generated quality report with score: {quality_report['quality_score']:.1f}/100")

        # Step 4: Build response content
        response_content = f"""## 🗄️ Database Schema Analysis

**Summary:** Analyzed {total_tables} database table(s)

### Entity-Relationship Diagram

```mermaid
{erd_diagram}
```

### Quality Analysis

{quality_markdown}

---

*Analysis completed at {time.strftime('%Y-%m-%d %H:%M:%S')}*
"""

        # Step 5: Add to chat history
        append_to_list("chat_history", {
            "role": "assistant",
            "agent_role": "Data Analyst",
            "content": response_content,
            "confidence": 1.0,
            "citations": [
                {
                    "file_path": table.get("relativePath", table.get("fileName", "unknown")),
                    "artifact_type": "DbTable"
                }
                for table in tables[:10]  # Limit citations to first 10 tables
            ],
            "suggested_questions": [
                "What are the main entities in this schema?",
                "Explain the relationships between tables",
                "What quality issues should be fixed first?",
                "Show me the data flow through this schema"
            ]
        })

        logger.info("Database schema analysis workflow completed successfully")

    except Exception as e:
        # Error handling
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Database schema analysis failed: {e}", exc_info=True)

        set_value("chat_error", str(e))

        append_to_list("chat_history", {
            "role": "assistant",
            "agent_role": "Data Analyst",
            "content": f"❌ Failed to analyze database schema: {str(e)}",
            "confidence": 0.0,
            "citations": [],
            "suggested_questions": []
        })

    finally:
        set_value("chat_loading", False)
        st.rerun()


def render_chat_actions():
    """Render chat action buttons."""
    col1, col2, col3, col4 = st.columns([1, 1, 2, 2])

    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            clear_list("chat_history")
            set_value("chat_error", None)
            st.rerun()

    with col2:
        if st.button("💾 Export Chat", use_container_width=True):
            export_chat_history()

    with col3:
        if st.button("🗄️ Analyze Database Schema", use_container_width=True):
            analyze_database_schema()

    with col4:
        # T094 - Generate PRD workflow button
        selected_count = len(get("selected_artifacts", []))
        button_label = f"📝 Generate PRD ({selected_count} artifacts)"
        button_enabled = selected_count > 0 and not get("prd_workflow_running", False)

        if st.button(button_label, use_container_width=True, disabled=not button_enabled):
            generate_prd_workflow()


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
    render_artifact_selection()  # T093 - Artifact selection UI

    # Show PRD workflow progress (T094)
    if get("prd_workflow_running", False):
        st.markdown("---")
        st.markdown("### 📝 Generating PRD...")

        progress = get("prd_workflow_progress", {})
        current_step = progress.get("current_step", 0)
        total_steps = progress.get("total_steps", 4)
        current_agent = progress.get("current_agent")

        render_workflow_progress(
            current_step=current_step,
            total_steps=total_steps,
            current_agent=current_agent
        )

        # T095 - Workflow cancellation button
        def cancel_workflow():
            """Cancel the running PRD workflow."""
            workflow = get("prd_workflow_instance")
            if workflow:
                workflow.cancel()
                st.warning("⚠️ Workflow cancellation requested...")

        render_workflow_cancellation_button(
            on_cancel=cancel_workflow,
            key="cancel_prd_workflow"
        )

        st.markdown("---")

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
