"""
Settings page for agent configuration (T102 - US2.4).

This page allows users to configure agent behavior including:
- Agent verbosity (concise, standard, verbose)
- Technical level (junior, mid, senior)
- Citation style (inline, footnotes, none)
- UI theme (light, dark)
- Output format (markdown, text)

Settings persist per user session and apply to all agent queries.
"""

import streamlit as st
import sys
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(src_dir))

from codeindex.web.services.settings_service import (
    load_settings,
    save_settings,
    reset_settings,
    validate_settings,
    get_default_settings
)
from codeindex.web.components.settings_preview import render_settings_preview
from codeindex.web.utils.session_state import initialize_session_state, get, set_value


def initialize_settings_page():
    """Initialize session state for settings page."""
    defaults = {
        "settings_changed": False,
        "settings_error": None
    }

    initialize_session_state(defaults)


def render_agent_verbosity_settings(current_settings: dict):
    """Render agent verbosity settings (T103)."""
    st.subheader("📝 Agent Verbosity")

    st.caption("Control how detailed agent responses should be")

    verbosity = st.radio(
        "Response Detail Level",
        options=["concise", "standard", "verbose"],
        index=["concise", "standard", "verbose"].index(current_settings.get("verbosity", "standard")),
        horizontal=True,
        help=(
            "**Concise**: Brief responses focusing on key points only\n\n"
            "**Standard**: Balanced detail with clear explanations\n\n"
            "**Verbose**: Comprehensive responses with examples and thorough explanations"
        )
    )

    current_settings["verbosity"] = verbosity


def render_technical_level_settings(current_settings: dict):
    """Render technical level settings (T104)."""
    st.subheader("🎓 Technical Level")

    st.caption("Adjust explanations for your technical expertise")

    technical_level = st.radio(
        "Target Audience",
        options=["junior", "mid", "senior"],
        index=["junior", "mid", "senior"].index(current_settings.get("technical_level", "senior")),
        horizontal=True,
        help=(
            "**Junior**: Simple explanations, avoid jargon, define technical terms\n\n"
            "**Mid**: Balanced technical content with clear explanations\n\n"
            "**Senior**: Use technical terminology freely, assume advanced knowledge"
        )
    )

    current_settings["technical_level"] = technical_level


def render_citation_style_settings(current_settings: dict):
    """Render citation style settings (T105)."""
    st.subheader("📚 Citation Style")

    st.caption("How to display code references in responses")

    citation_style = st.radio(
        "Citation Format",
        options=["inline", "footnotes", "none"],
        index=["inline", "footnotes", "none"].index(current_settings.get("citation_style", "inline")),
        horizontal=True,
        help=(
            "**Inline**: References within text like [1] [2]\n\n"
            "**Footnotes**: Numbered references at end of response\n\n"
            "**None**: No citation references (content only)"
        )
    )

    current_settings["citation_style"] = citation_style


def render_ui_theme_settings(current_settings: dict):
    """Render UI theme settings (T106)."""
    st.subheader("🎨 UI Theme")

    st.caption("Visual theme for the application interface")

    ui_theme = st.radio(
        "Theme",
        options=["light", "dark"],
        index=["light", "dark"].index(current_settings.get("ui_theme", "light")),
        horizontal=True,
        help=(
            "**Light**: Light background with dark text (default)\n\n"
            "**Dark**: Dark background with light text\n\n"
            "*Note: Theme changes apply on page refresh*"
        )
    )

    current_settings["ui_theme"] = ui_theme


def render_output_format_settings(current_settings: dict):
    """Render output format settings (T107)."""
    st.subheader("📄 Output Format")

    st.caption("Format for agent responses")

    output_format = st.radio(
        "Format",
        options=["markdown", "text"],
        index=["markdown", "text"].index(current_settings.get("output_format", "markdown")),
        horizontal=True,
        help=(
            "**Markdown**: Formatted text with headings, bold, code blocks\n\n"
            "**Text**: Plain text without formatting"
        )
    )

    current_settings["output_format"] = output_format


def main():
    """Main settings page function."""
    # Page configuration
    st.title("⚙️ Agent Settings")

    st.markdown("""
    Configure how AI agents respond to your queries. Settings apply to all agent interactions
    in your current session and persist until you reset them.
    """)

    # Initialize session state
    initialize_settings_page()

    # Load current settings (T108)
    current_settings = load_settings()

    # Create a form for settings
    st.markdown("---")

    # T103-T107: Render all setting sections
    with st.container():
        col1, col2 = st.columns([2, 1])

        with col1:
            render_agent_verbosity_settings(current_settings)
            st.markdown("---")

            render_technical_level_settings(current_settings)
            st.markdown("---")

            render_citation_style_settings(current_settings)
            st.markdown("---")

            render_ui_theme_settings(current_settings)
            st.markdown("---")

            render_output_format_settings(current_settings)

        with col2:
            # T109: Settings preview (T110)
            st.markdown("### Preview")
            render_settings_preview(current_settings)

    # Action buttons
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        # T108: Apply settings button
        if st.button("✅ Apply Settings", use_container_width=True, type="primary"):
            # Validate settings
            is_valid, errors = validate_settings(current_settings)

            if is_valid:
                # Save settings (T108)
                save_settings(current_settings)
                st.success("✅ Settings applied successfully!")
                set_value("settings_changed", True)

                # Show what changed
                defaults = get_default_settings()
                changes = []
                for key, value in current_settings.items():
                    if defaults.get(key) != value:
                        changes.append(f"- **{key.replace('_', ' ').title()}**: {value}")

                if changes:
                    with st.expander("Changed Settings"):
                        st.markdown("\n".join(changes))
            else:
                st.error(f"❌ Invalid settings: {', '.join(errors.values())}")
                set_value("settings_error", errors)

    with col2:
        # T111: Reset to defaults button
        if st.button("🔄 Reset to Defaults", use_container_width=True):
            reset_settings()
            st.success("✅ Settings reset to defaults")
            set_value("settings_changed", True)
            st.rerun()

    # Settings info
    st.markdown("---")

    with st.expander("ℹ️ About Settings"):
        st.markdown("""
        ### How Settings Work

        **Session Persistence**: Settings are stored in your browser session and persist
        across page navigation. They reset when you close the browser tab or clear session data.

        **Agent Application**: Settings apply to all agent queries including:
        - Chat conversations
        - PRD generation
        - Test generation
        - Code analysis

        **Default Values**:
        - **Verbosity**: Standard (balanced detail)
        - **Technical Level**: Senior (assume advanced knowledge)
        - **Citation Style**: Inline (references within text)
        - **UI Theme**: Light (light background)
        - **Output Format**: Markdown (formatted text)

        ### Tips for Best Results

        - **New to codebase?** Use `verbose` verbosity and `junior` level for detailed explanations
        - **Quick answers?** Use `concise` verbosity and `senior` level
        - **Formal docs?** Use `footnotes` citations and `markdown` format
        - **Copy-paste friendly?** Use `text` format to avoid markdown syntax

        ### Performance Impact

        - **Verbose** responses may take slightly longer to generate
        - **Concise** responses are typically faster
        - Citation style and format have minimal performance impact
        """)

    # Current settings display
    with st.expander("🔍 Current Settings (Raw JSON)"):
        st.json(current_settings)


if __name__ == "__main__":
    main()
