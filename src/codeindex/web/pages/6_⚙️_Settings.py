"""
Settings page for GEMINI Code Analysis Pipeline Web UI (Phase 14).

This page provides configuration management with:
- Agent settings (verbosity, technical level, citation style)
- Service connection settings
- UI preferences
- Export settings
- System diagnostics
"""

import streamlit as st
import sys
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(src_dir))

from codeindex.utils.config import get_config
from codeindex.web.utils.session_state import (
    initialize_session_state,
    get,
    set_value,
    update_nested
)


def initialize_settings_state():
    """Initialize session state for settings page."""
    defaults = {
        "settings": {
            "agent": {
                "verbosity": "standard",
                "technical_level": "senior",
                "citation_style": "inline",
                "max_iterations": 10,
                "temperature": 0.7
            },
            "ui": {
                "theme": "light",
                "page_size": 50,
                "enable_animations": True
            },
            "export": {
                "default_format": "pdf",
                "include_citations": True,
                "include_timestamps": True
            }
        },
        "settings_saved": False
    }

    initialize_session_state(defaults)


def render_agent_settings():
    """Render agent configuration settings."""
    st.subheader("🤖 Agent Settings")

    agent_settings = get("settings", {}).get("agent", {})

    # Verbosity
    verbosity = st.select_slider(
        "Response Detail Level",
        options=["concise", "standard", "detailed"],
        value=agent_settings.get("verbosity", "standard"),
        help="Control how detailed agent responses should be"
    )

    # Technical level
    technical_level = st.select_slider(
        "Technical Explanation Level",
        options=["junior", "mid", "senior"],
        value=agent_settings.get("technical_level", "senior"),
        help="Adjust explanations for your technical expertise"
    )

    # Citation style
    citation_style = st.selectbox(
        "Citation Style",
        options=["inline", "footnotes", "none"],
        index=["inline", "footnotes", "none"].index(
            agent_settings.get("citation_style", "inline")
        ),
        help="How to display code references"
    )

    # Max iterations
    max_iterations = st.slider(
        "Max Agent Iterations",
        min_value=5,
        max_value=20,
        value=agent_settings.get("max_iterations", 10),
        help="Maximum reasoning steps for agent"
    )

    # Temperature
    temperature = st.slider(
        "LLM Temperature",
        min_value=0.0,
        max_value=1.0,
        value=agent_settings.get("temperature", 0.7),
        step=0.1,
        help="Higher = more creative, Lower = more focused"
    )

    # Update settings
    update_nested("settings", "agent", {
        "verbosity": verbosity,
        "technical_level": technical_level,
        "citation_style": citation_style,
        "max_iterations": max_iterations,
        "temperature": temperature
    })


def render_ui_settings():
    """Render UI preferences."""
    st.subheader("🎨 UI Preferences")

    ui_settings = get("settings", {}).get("ui", {})

    # Theme (placeholder - Streamlit handles this)
    st.info("💡 Use the Streamlit theme selector (☰ menu → Settings → Theme) to change appearance")

    # Page size
    page_size = st.slider(
        "Search Results Per Page",
        min_value=10,
        max_value=100,
        value=ui_settings.get("page_size", 50),
        step=10,
        help="Number of results to show per page"
    )

    # Animations
    enable_animations = st.checkbox(
        "Enable Animations",
        value=ui_settings.get("enable_animations", True),
        help="Show loading animations and transitions"
    )

    # Update settings
    update_nested("settings", "ui", {
        "page_size": page_size,
        "enable_animations": enable_animations
    })


def render_export_settings():
    """Render export configuration."""
    st.subheader("📤 Export Settings")

    export_settings = get("settings", {}).get("export", {})

    # Default format
    default_format = st.selectbox(
        "Default Export Format",
        options=["pdf", "markdown", "json", "csv"],
        index=["pdf", "markdown", "json", "csv"].index(
            export_settings.get("default_format", "pdf")
        ),
        help="Preferred format for exporting reports"
    )

    # Include citations
    include_citations = st.checkbox(
        "Include Citations in Exports",
        value=export_settings.get("include_citations", True),
        help="Add source file references to exported documents"
    )

    # Include timestamps
    include_timestamps = st.checkbox(
        "Include Timestamps in Exports",
        value=export_settings.get("include_timestamps", True),
        help="Add generation timestamps to exported documents"
    )

    # Update settings
    update_nested("settings", "export", {
        "default_format": default_format,
        "include_citations": include_citations,
        "include_timestamps": include_timestamps
    })


def render_service_diagnostics():
    """Render service connection diagnostics."""
    st.subheader("🔧 Service Diagnostics")

    config = get_config()

    # Check services
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Weaviate**")
        weaviate_url = config.get("WEAVIATE_URL", "http://localhost:8080")
        st.code(weaviate_url)

        if st.button("Test Connection", key="test_weaviate"):
            import httpx
            try:
                response = httpx.get(f"{weaviate_url}/v1/.well-known/ready", timeout=5.0)
                if response.status_code == 200:
                    st.success("✅ Connected")
                else:
                    st.error(f"❌ HTTP {response.status_code}")
            except Exception as e:
                st.error(f"❌ {str(e)[:50]}")

    with col2:
        st.markdown("**Ollama**")
        ollama_url = config.get("OLLAMA_BASE_URL", "http://localhost:11434")
        st.code(ollama_url)

        if st.button("Test Connection", key="test_ollama"):
            import httpx
            try:
                response = httpx.get(f"{ollama_url}/api/tags", timeout=5.0)
                if response.status_code == 200:
                    st.success("✅ Connected")
                else:
                    st.error(f"❌ HTTP {response.status_code}")
            except Exception as e:
                st.error(f"❌ {str(e)[:50]}")

    st.markdown("---")

    # Database info
    st.markdown("**SQLite Database**")
    workspace_db = config.get("WORKSPACE_DB_PATH", "data/workspaces.db")
    st.code(workspace_db)

    if Path(workspace_db).exists():
        size = Path(workspace_db).stat().st_size
        st.caption(f"Size: {size:,} bytes")
    else:
        st.warning("Database file not created yet")


def render_system_info():
    """Render system information."""
    st.subheader("ℹ️ System Information")

    config = get_config()

    info = {
        "Source Directory": config.get("JAVA_SOURCE_DIR", "Not configured"),
        "Workspace DB": config.get("WORKSPACE_DB_PATH", "data/workspaces.db"),
        "Export Directory": config.get("EXPORT_DIR", "data/exports"),
        "Max Concurrent Agents": config.get("MAX_CONCURRENT_AGENTS", 3),
        "LLM Model": config.get("OLLAMA_MODEL_NAME", "gemma3:12b")
    }

    for key, value in info.items():
        st.text(f"{key}: {value}")


def save_settings():
    """Save settings (placeholder - would persist to config)."""
    set_value("settings_saved", True)
    st.success("✅ Settings saved successfully!")


def reset_settings():
    """Reset settings to defaults."""
    initialize_settings_state()
    st.success("✅ Settings reset to defaults")


def main():
    """Main settings page function."""
    # Page configuration
    st.title("⚙️ Settings")

    st.markdown("""
    Configure agent behavior, UI preferences, and system settings.
    """)

    # Initialize session state
    initialize_settings_state()

    # Render settings sections
    render_agent_settings()

    st.markdown("---")

    render_ui_settings()

    st.markdown("---")

    render_export_settings()

    st.markdown("---")

    render_service_diagnostics()

    st.markdown("---")

    render_system_info()

    st.markdown("---")

    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        if st.button("💾 Save Settings", use_container_width=True):
            save_settings()

    with col2:
        if st.button("🔄 Reset to Defaults", use_container_width=True):
            reset_settings()
            st.rerun()

    # Show save confirmation
    if get("settings_saved", False):
        st.info("💡 Settings are saved for this session")


if __name__ == "__main__":
    main()
