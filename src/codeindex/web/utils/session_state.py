"""
Streamlit session state management utilities.

This module provides helper functions for managing Streamlit session state
with type safety and default value handling.
"""

from typing import Any, Optional, Dict, List
import streamlit as st


def initialize_session_state(defaults: Optional[Dict[str, Any]] = None):
    """
    Initialize session state with default values.

    Args:
        defaults: Dictionary of default key-value pairs
    """
    if defaults is None:
        defaults = get_default_session_state()

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_default_session_state() -> Dict[str, Any]:
    """
    Get default session state values for the application.

    Returns:
        Dictionary of default session state values
    """
    return {
        # General
        "initialized": True,

        # Search page
        "search_query": "",
        "search_results": [],
        "search_filters": {
            "artifact_types": [],
            "project": None,
            "date_range": None
        },
        "selected_artifacts": [],

        # Chat page
        "chat_history": [],
        "current_agent": "Senior Developer",

        # Workspace page
        "current_workspace": None,
        "workspace_list": [],

        # Agent settings
        "agent_settings": {
            "verbosity": "standard",
            "technical_level": "senior",
            "citation_style": "inline",
            "output_format": "markdown"
        },

        # UI state
        "sidebar_expanded": True,
        "theme": "light",
        "active_page": "Home"
    }


def get(key: str, default: Any = None) -> Any:
    """
    Get value from session state with default fallback.

    Args:
        key: Session state key
        default: Default value if key doesn't exist

    Returns:
        Value from session state or default
    """
    return st.session_state.get(key, default)


def set_value(key: str, value: Any):
    """
    Set value in session state.

    Args:
        key: Session state key
        value: Value to set
    """
    st.session_state[key] = value


def has_key(key: str) -> bool:
    """
    Check if key exists in session state.

    Args:
        key: Session state key

    Returns:
        True if key exists, False otherwise
    """
    return key in st.session_state


def delete(key: str):
    """
    Delete key from session state.

    Args:
        key: Session state key
    """
    if key in st.session_state:
        del st.session_state[key]


def clear(preserve_keys: Optional[List[str]] = None):
    """
    Clear session state, optionally preserving certain keys.

    Args:
        preserve_keys: List of keys to preserve (default: preserve agent settings)
    """
    if preserve_keys is None:
        preserve_keys = ["agent_settings", "theme"]

    # Save preserved values
    preserved = {key: st.session_state.get(key) for key in preserve_keys if key in st.session_state}

    # Clear session state
    for key in list(st.session_state.keys()):
        if key not in preserve_keys:
            del st.session_state[key]

    # Restore preserved values
    for key, value in preserved.items():
        st.session_state[key] = value

    # Re-initialize with defaults
    initialize_session_state()


def update_nested(key: str, nested_key: str, value: Any):
    """
    Update a nested value in session state (for dictionaries).

    Args:
        key: Session state key (must be a dictionary)
        nested_key: Key within the nested dictionary
        value: Value to set

    Example:
        update_nested("search_filters", "project", "com.example:app")
    """
    if key not in st.session_state:
        st.session_state[key] = {}

    if not isinstance(st.session_state[key], dict):
        raise ValueError(f"Session state key '{key}' is not a dictionary")

    st.session_state[key][nested_key] = value


def get_nested(key: str, nested_key: str, default: Any = None) -> Any:
    """
    Get a nested value from session state (for dictionaries).

    Args:
        key: Session state key (must be a dictionary)
        nested_key: Key within the nested dictionary
        default: Default value if key doesn't exist

    Returns:
        Nested value or default
    """
    if key not in st.session_state:
        return default

    if not isinstance(st.session_state[key], dict):
        return default

    return st.session_state[key].get(nested_key, default)


def append_to_list(key: str, value: Any):
    """
    Append value to a list in session state.

    Args:
        key: Session state key (must be a list)
        value: Value to append
    """
    if key not in st.session_state:
        st.session_state[key] = []

    if not isinstance(st.session_state[key], list):
        raise ValueError(f"Session state key '{key}' is not a list")

    st.session_state[key].append(value)


def remove_from_list(key: str, value: Any):
    """
    Remove value from a list in session state.

    Args:
        key: Session state key (must be a list)
        value: Value to remove
    """
    if key not in st.session_state:
        return

    if not isinstance(st.session_state[key], list):
        raise ValueError(f"Session state key '{key}' is not a list")

    if value in st.session_state[key]:
        st.session_state[key].remove(value)


def clear_list(key: str):
    """
    Clear a list in session state (empty the list).

    Args:
        key: Session state key (must be a list)
    """
    if key not in st.session_state:
        st.session_state[key] = []
        return

    if not isinstance(st.session_state[key], list):
        raise ValueError(f"Session state key '{key}' is not a list")

    st.session_state[key] = []


def toggle(key: str):
    """
    Toggle boolean value in session state.

    Args:
        key: Session state key (must be boolean)
    """
    if key not in st.session_state:
        st.session_state[key] = True
    else:
        st.session_state[key] = not st.session_state[key]


def increment(key: str, amount: int = 1):
    """
    Increment numeric value in session state.

    Args:
        key: Session state key (must be numeric)
        amount: Amount to increment (default: 1)
    """
    if key not in st.session_state:
        st.session_state[key] = 0

    st.session_state[key] += amount


def get_all() -> Dict[str, Any]:
    """
    Get all session state as a dictionary.

    Returns:
        Dictionary of all session state values
    """
    return dict(st.session_state)


def debug_print():
    """Print session state for debugging purposes."""
    st.write("### Session State Debug")
    st.json(get_all())
