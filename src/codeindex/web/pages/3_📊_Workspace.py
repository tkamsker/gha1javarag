"""
Workspace page for GEMINI Code Analysis Pipeline Web UI (Phase 7-8).

This page provides workspace management with:
- Create/save/load workspaces
- Workspace list with metadata
- Save current search/chat state
- Share workspace with team
- Workspace annotations
"""

import streamlit as st
import sys
from pathlib import Path
from typing import Optional, Dict, List, Any
import json

# Add src directory to Python path
src_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(src_dir))

from codeindex.web.database.connection import get_workspace_manager
from codeindex.web.utils.session_state import (
    initialize_session_state,
    get,
    set_value
)


def initialize_workspace_state():
    """Initialize session state for workspace page."""
    defaults = {
        "current_workspace": None,
        "workspace_list": [],
        "workspace_loading": False,
        "workspace_error": None
    }

    initialize_session_state(defaults)


def load_workspaces():
    """Load all workspaces from database."""
    try:
        manager = get_workspace_manager()

        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, description, tags, created_at, updated_at,
                       artifact_count, view_count
                FROM workspaces
                ORDER BY updated_at DESC
            """)

            workspaces = []
            for row in cursor.fetchall():
                workspaces.append({
                    "id": row["id"],
                    "name": row["name"],
                    "description": row["description"],
                    "tags": row["tags"],
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                    "artifact_count": row["artifact_count"],
                    "view_count": row["view_count"]
                })

            set_value("workspace_list", workspaces)

    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to load workspaces: {e}")
        set_value("workspace_error", str(e))


def create_workspace(name: str, description: str, tags: str):
    """Create new workspace."""
    try:
        manager = get_workspace_manager()
        workspace_id = manager.generate_uuid()

        # Get current state to save
        state = {
            "search_query": get("search_query", ""),
            "search_filters": get("search_filters", {}),
            "chat_history": get("chat_history", [])
        }

        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO workspaces (id, name, description, tags, state_json)
                VALUES (?, ?, ?, ?, ?)
            """, (workspace_id, name, description, tags, json.dumps(state)))

        st.success(f"✅ Workspace '{name}' created successfully!")
        load_workspaces()

    except Exception as e:
        st.error(f"❌ Failed to create workspace: {e}")


def load_workspace(workspace_id: str):
    """Load workspace and restore state."""
    try:
        manager = get_workspace_manager()

        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, state_json FROM workspaces WHERE id = ?
            """, (workspace_id,))

            row = cursor.fetchone()

            if row:
                # Parse state
                state = json.loads(row["state_json"])

                # Restore state
                set_value("search_query", state.get("search_query", ""))
                set_value("search_filters", state.get("search_filters", {}))
                set_value("chat_history", state.get("chat_history", []))
                set_value("current_workspace", workspace_id)

                # Increment view count
                cursor.execute("""
                    UPDATE workspaces
                    SET view_count = view_count + 1
                    WHERE id = ?
                """, (workspace_id,))

                st.success(f"✅ Loaded workspace: {row['name']}")

    except Exception as e:
        st.error(f"❌ Failed to load workspace: {e}")


def delete_workspace(workspace_id: str):
    """Delete workspace."""
    try:
        manager = get_workspace_manager()

        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM workspaces WHERE id = ?", (workspace_id,))

        st.success("✅ Workspace deleted")
        load_workspaces()

    except Exception as e:
        st.error(f"❌ Failed to delete workspace: {e}")


def render_workspace_list():
    """Render list of workspaces."""
    workspaces = get("workspace_list", [])

    if not workspaces:
        st.info("📂 No workspaces yet. Create your first workspace below!")
        return

    st.subheader(f"📊 Your Workspaces ({len(workspaces)})")

    for workspace in workspaces:
        with st.container():
            col1, col2, col3 = st.columns([4, 1, 1])

            with col1:
                st.markdown(f"### {workspace['name']}")
                if workspace['description']:
                    st.caption(workspace['description'])

                if workspace['tags']:
                    tags = workspace['tags'].split(',')
                    tag_str = " ".join([f"`{tag.strip()}`" for tag in tags])
                    st.markdown(f"🏷️ {tag_str}")

                st.caption(f"📅 Updated: {workspace['updated_at']} • 👁️ Views: {workspace['view_count']}")

            with col2:
                if st.button("📂 Load", key=f"load_{workspace['id']}", use_container_width=True):
                    load_workspace(workspace['id'])
                    st.rerun()

            with col3:
                if st.button("🗑️ Delete", key=f"delete_{workspace['id']}", use_container_width=True):
                    delete_workspace(workspace['id'])
                    st.rerun()

            st.markdown("---")


def render_create_workspace():
    """Render create workspace form."""
    st.subheader("➕ Create New Workspace")

    with st.form("create_workspace_form"):
        name = st.text_input("Workspace Name", placeholder="e.g., User Authentication Analysis")
        description = st.text_area("Description", placeholder="Brief description of this workspace...")
        tags = st.text_input("Tags", placeholder="Comma-separated tags (e.g., backend, authentication, security)")

        submitted = st.form_submit_button("Create Workspace", use_container_width=True)

        if submitted:
            if not name:
                st.error("❌ Workspace name is required")
            else:
                create_workspace(name, description, tags)
                st.rerun()


def render_current_workspace():
    """Render current workspace info."""
    current_id = get("current_workspace")

    if current_id:
        try:
            manager = get_workspace_manager()

            with manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM workspaces WHERE id = ?", (current_id,))
                row = cursor.fetchone()

                if row:
                    st.sidebar.success(f"📊 **Workspace**: {row['name']}")

                    if st.sidebar.button("💾 Save Changes", use_container_width=True):
                        save_current_workspace(current_id)

                    if st.sidebar.button("✖️ Close Workspace", use_container_width=True):
                        set_value("current_workspace", None)
                        st.rerun()

        except Exception as e:
            st.sidebar.error(f"❌ Error: {e}")


def save_current_workspace(workspace_id: str):
    """Save current state to workspace."""
    try:
        manager = get_workspace_manager()

        # Get current state
        state = {
            "search_query": get("search_query", ""),
            "search_filters": get("search_filters", {}),
            "chat_history": get("chat_history", [])
        }

        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE workspaces
                SET state_json = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (json.dumps(state), workspace_id))

        st.sidebar.success("✅ Workspace saved")

    except Exception as e:
        st.sidebar.error(f"❌ Save failed: {e}")


def main():
    """Main workspace page function."""
    # Page configuration
    st.title("📊 Workspaces")

    st.markdown("""
    Workspaces let you save and organize your analysis sessions. Create workspaces for
    different features, modules, or investigations and easily switch between them.
    """)

    # Initialize session state
    initialize_workspace_state()

    # Load workspaces
    if not get("workspace_list"):
        load_workspaces()

    # Render current workspace in sidebar
    render_current_workspace()

    # Show error if present
    error = get("workspace_error")
    if error:
        st.error(f"❌ {error}")

    # Render workspace list
    render_workspace_list()

    st.markdown("---")

    # Render create form
    render_create_workspace()


if __name__ == "__main__":
    main()
