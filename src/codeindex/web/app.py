"""
Main Streamlit application entry point for GEMINI Code Analysis Pipeline Web UI.

This module provides the main application structure with sidebar navigation,
health checks, and session state initialization.
"""

import os
import sys
from pathlib import Path
from typing import Optional

import streamlit as st

# Add src directory to Python path for imports
src_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(src_dir))

from codeindex.utils.config import get_config


def check_service_health() -> dict:
    """
    Check health of external dependencies (Weaviate, Ollama, SQLite).

    Returns:
        Dictionary with service health status
    """
    import httpx
    from pathlib import Path

    health_status = {
        "weaviate": {"status": "unknown", "url": None, "error": None},
        "ollama": {"status": "unknown", "url": None, "error": None},
        "sqlite": {"status": "unknown", "path": None, "error": None}
    }

    config = get_config()

    # Check Weaviate
    try:
        weaviate_url = config.get("WEAVIATE_URL", "http://localhost:8080")
        health_status["weaviate"]["url"] = weaviate_url

        # Attempt to reach Weaviate health endpoint
        response = httpx.get(f"{weaviate_url}/v1/.well-known/ready", timeout=5.0)
        if response.status_code == 200:
            health_status["weaviate"]["status"] = "available"
        else:
            health_status["weaviate"]["status"] = "unavailable"
            health_status["weaviate"]["error"] = f"HTTP {response.status_code}"
    except Exception as e:
        health_status["weaviate"]["status"] = "unavailable"
        health_status["weaviate"]["error"] = str(e)[:50]

    # Check Ollama
    try:
        ollama_url = config.get("OLLAMA_BASE_URL", "http://localhost:11434")
        health_status["ollama"]["url"] = ollama_url

        # Attempt to reach Ollama API endpoint
        response = httpx.get(f"{ollama_url}/api/tags", timeout=5.0)
        if response.status_code == 200:
            health_status["ollama"]["status"] = "available"
        else:
            health_status["ollama"]["status"] = "unavailable"
            health_status["ollama"]["error"] = f"HTTP {response.status_code}"
    except Exception as e:
        health_status["ollama"]["status"] = "unavailable"
        health_status["ollama"]["error"] = str(e)[:50]

    # Check SQLite
    try:
        workspace_db = config.get("WORKSPACE_DB_PATH", "data/workspaces.db")
        health_status["sqlite"]["path"] = workspace_db

        # Check if database file exists and is writable
        db_path = Path(workspace_db)

        # If database doesn't exist, check if parent directory is writable
        if not db_path.exists():
            if db_path.parent.exists() and os.access(db_path.parent, os.W_OK):
                health_status["sqlite"]["status"] = "available"
            else:
                health_status["sqlite"]["status"] = "unavailable"
                health_status["sqlite"]["error"] = "Directory not writable"
        else:
            # Database exists, check if it's accessible
            try:
                import sqlite3
                conn = sqlite3.connect(workspace_db, timeout=1.0)
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                conn.close()
                health_status["sqlite"]["status"] = "available"
            except Exception as e:
                health_status["sqlite"]["status"] = "unavailable"
                health_status["sqlite"]["error"] = str(e)[:50]

    except Exception as e:
        health_status["sqlite"]["status"] = "unavailable"
        health_status["sqlite"]["error"] = str(e)[:50]

    return health_status


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.search_query = ""
        st.session_state.search_results = []
        st.session_state.chat_history = []
        st.session_state.current_workspace = None
        st.session_state.agent_settings = {
            "verbosity": "standard",
            "technical_level": "senior",
            "citation_style": "inline"
        }


def render_sidebar():
    """Render sidebar with navigation and status."""
    with st.sidebar:
        st.title("🔍 GEMINI Analysis")
        st.markdown("---")

        # Navigation
        st.subheader("Navigation")
        st.page_link("app.py", label="🏠 Home", icon="🏠")
        st.page_link("pages/1_🔍_Search.py", label="Search", icon="🔍")
        st.page_link("pages/2_💬_Chat.py", label="Chat", icon="💬")
        st.page_link("pages/3_📊_Workspace.py", label="Workspace", icon="📊")
        st.page_link("pages/4_🗂️_Files.py", label="Files", icon="🗂️")
        st.page_link("pages/5_🧪_Tests.py", label="Tests", icon="🧪")
        st.page_link("pages/6_⚙️_Settings.py", label="Settings", icon="⚙️")

        st.markdown("---")

        # Health status
        st.subheader("Service Status")
        health = check_service_health()

        for service, info in health.items():
            status = info["status"]
            icon = "✅" if status == "available" else "❌" if status == "unavailable" else "⚠️"
            st.text(f"{icon} {service.capitalize()}")
            if info.get("url"):
                st.caption(f"   {info['url']}")
            if info.get("path"):
                st.caption(f"   {info['path']}")

        st.markdown("---")
        st.caption("Version 1.0.0 | Feature 009")


def main():
    """Main application entry point."""
    # Page configuration
    st.set_page_config(
        page_title="GEMINI Code Analysis Pipeline",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/anthropics/claude-code',
            'Report a bug': "https://github.com/anthropics/claude-code/issues",
            'About': "# GEMINI Code Analysis Pipeline\nAI-powered codebase analysis and documentation"
        }
    )

    # Initialize session state
    initialize_session_state()

    # Render sidebar
    render_sidebar()

    # Main content
    st.title("🔍 GEMINI Code Analysis Pipeline")
    st.markdown("## Interactive Web UI with Multi-Agent Intelligence")

    st.markdown("""
    Welcome to the GEMINI Code Analysis Pipeline Web UI! This interactive interface provides:

    ### 🎯 Core Features

    - **🔍 Semantic Search**: Natural language search over your entire codebase
    - **💬 AI Agent Chat**: Ask questions to specialized AI agents (Senior Developer, Data Analyst, etc.)
    - **📊 Workspaces**: Save and share analysis contexts with your team
    - **🗂️ Code Viewer**: Browse source files with syntax highlighting
    - **🧪 Test Generation**: Generate Gherkin and Playwright tests automatically
    - **📈 Visualizations**: Interactive relationship graphs and architecture diagrams

    ### 🚀 Quick Start

    1. **Search**: Use the Search page to find artifacts using natural language
    2. **Chat**: Ask questions to AI agents for detailed explanations
    3. **Explore**: View source code and navigate relationships
    4. **Generate**: Create PRDs, specs, and tests automatically

    ### 📝 Getting Help

    - Check the sidebar for service status
    - Visit the Settings page to configure agent behavior
    - Use the Files page to browse your codebase

    **Note**: Make sure Weaviate and Ollama services are running before using the web UI.
    """)

    # Service status warnings
    health = check_service_health()
    if any(info["status"] != "available" for info in health.values()):
        st.warning("""
        ⚠️ Some services are not available. Please ensure:
        - Weaviate is running at http://localhost:8080
        - Ollama is running at http://localhost:11434
        - Your codebase has been indexed using the CLI
        """)

    # Quick actions
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔍 Start Searching", use_container_width=True):
            st.switch_page("pages/1_🔍_Search.py")

    with col2:
        if st.button("💬 Chat with Agent", use_container_width=True):
            st.switch_page("pages/2_💬_Chat.py")

    with col3:
        if st.button("🗂️ Browse Files", use_container_width=True):
            st.switch_page("pages/4_🗂️_Files.py")


if __name__ == "__main__":
    main()
