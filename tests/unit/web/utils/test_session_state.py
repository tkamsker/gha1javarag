"""
Unit tests for session state management utilities (T017).

Tests the session state helper functions including:
- Initialization with defaults
- Getting and setting values
- Nested dictionary updates
- List operations (append, extend, clear)
- Type checking and validation
- Error handling for missing keys
"""

import pytest
from unittest.mock import MagicMock, patch
import streamlit as st


# Mock streamlit.session_state before importing our module
@pytest.fixture(autouse=True)
def mock_session_state(monkeypatch):
    """Mock Streamlit session state for testing."""
    session_state = {}

    # Create a mock session_state that behaves like a dict
    mock_st = MagicMock()
    mock_st.session_state = session_state

    monkeypatch.setattr("streamlit.session_state", session_state)

    yield session_state

    # Clear session state after each test
    session_state.clear()


from codeindex.web.utils.session_state import (
    initialize_session_state,
    get,
    set_value,
    has_key,
    delete,
    clear_all,
    get_all,
    update_nested,
    append_to_list,
    extend_list,
    clear_list,
    increment,
    toggle_bool,
    ensure_initialized,
    get_or_default,
    set_if_not_exists
)


class TestSessionStateInitialization:
    """Test session state initialization functions."""

    def test_initialize_empty(self, mock_session_state):
        """Test initialization with no defaults."""
        initialize_session_state()

        assert len(mock_session_state) == 0

    def test_initialize_with_defaults(self, mock_session_state):
        """Test initialization with default values."""
        defaults = {
            "counter": 0,
            "name": "test",
            "items": [],
            "config": {"key": "value"}
        }

        initialize_session_state(defaults)

        assert mock_session_state["counter"] == 0
        assert mock_session_state["name"] == "test"
        assert mock_session_state["items"] == []
        assert mock_session_state["config"] == {"key": "value"}

    def test_initialize_preserves_existing(self, mock_session_state):
        """Test that initialization preserves existing values."""
        mock_session_state["existing"] = "value"

        defaults = {
            "existing": "new_value",
            "new_key": "new_value"
        }

        initialize_session_state(defaults)

        assert mock_session_state["existing"] == "value"  # Preserved
        assert mock_session_state["new_key"] == "new_value"  # Added

    def test_ensure_initialized(self, mock_session_state):
        """Test ensure_initialized decorator."""
        @ensure_initialized({"counter": 0})
        def increment_counter():
            return mock_session_state["counter"] + 1

        result = increment_counter()

        assert mock_session_state["counter"] == 0
        assert result == 1


class TestSessionStateGetSet:
    """Test getting and setting session state values."""

    def test_get_existing_key(self, mock_session_state):
        """Test getting an existing key."""
        mock_session_state["key"] = "value"

        result = get("key")

        assert result == "value"

    def test_get_missing_key_with_default(self, mock_session_state):
        """Test getting a missing key returns default."""
        result = get("missing", default="default_value")

        assert result == "default_value"

    def test_get_missing_key_no_default(self, mock_session_state):
        """Test getting a missing key without default returns None."""
        result = get("missing")

        assert result is None

    def test_set_value(self, mock_session_state):
        """Test setting a value."""
        set_value("key", "value")

        assert mock_session_state["key"] == "value"

    def test_set_value_overwrites(self, mock_session_state):
        """Test setting a value overwrites existing."""
        mock_session_state["key"] = "old"
        set_value("key", "new")

        assert mock_session_state["key"] == "new"

    def test_get_or_default_existing(self, mock_session_state):
        """Test get_or_default with existing key."""
        mock_session_state["key"] = "existing"

        result = get_or_default("key", "default")

        assert result == "existing"

    def test_get_or_default_missing(self, mock_session_state):
        """Test get_or_default with missing key."""
        result = get_or_default("missing", "default")

        assert result == "default"
        assert mock_session_state["missing"] == "default"  # Sets default

    def test_set_if_not_exists_new_key(self, mock_session_state):
        """Test set_if_not_exists with new key."""
        set_if_not_exists("key", "value")

        assert mock_session_state["key"] == "value"

    def test_set_if_not_exists_existing_key(self, mock_session_state):
        """Test set_if_not_exists preserves existing key."""
        mock_session_state["key"] = "existing"
        set_if_not_exists("key", "new")

        assert mock_session_state["key"] == "existing"


class TestSessionStateChecks:
    """Test session state checking functions."""

    def test_has_key_exists(self, mock_session_state):
        """Test has_key returns True for existing key."""
        mock_session_state["key"] = "value"

        assert has_key("key") is True

    def test_has_key_missing(self, mock_session_state):
        """Test has_key returns False for missing key."""
        assert has_key("missing") is False

    def test_get_all(self, mock_session_state):
        """Test get_all returns all session state."""
        mock_session_state["key1"] = "value1"
        mock_session_state["key2"] = "value2"

        result = get_all()

        assert result == {"key1": "value1", "key2": "value2"}


class TestSessionStateDelete:
    """Test session state deletion functions."""

    def test_delete_existing_key(self, mock_session_state):
        """Test deleting an existing key."""
        mock_session_state["key"] = "value"

        delete("key")

        assert "key" not in mock_session_state

    def test_delete_missing_key(self, mock_session_state):
        """Test deleting a missing key doesn't raise error."""
        delete("missing")  # Should not raise

    def test_clear_all(self, mock_session_state):
        """Test clearing all session state."""
        mock_session_state["key1"] = "value1"
        mock_session_state["key2"] = "value2"

        clear_all()

        assert len(mock_session_state) == 0


class TestSessionStateNested:
    """Test nested dictionary operations."""

    def test_update_nested_existing_dict(self, mock_session_state):
        """Test updating nested dictionary value."""
        mock_session_state["config"] = {"key1": "value1"}

        update_nested("config", "key2", "value2")

        assert mock_session_state["config"] == {
            "key1": "value1",
            "key2": "value2"
        }

    def test_update_nested_creates_dict(self, mock_session_state):
        """Test update_nested creates dict if missing."""
        update_nested("config", "key", "value")

        assert mock_session_state["config"] == {"key": "value"}

    def test_update_nested_overwrites_value(self, mock_session_state):
        """Test update_nested overwrites existing nested value."""
        mock_session_state["config"] = {"key": "old"}

        update_nested("config", "key", "new")

        assert mock_session_state["config"]["key"] == "new"

    def test_update_nested_non_dict_raises(self, mock_session_state):
        """Test update_nested raises error if base is not dict."""
        mock_session_state["config"] = "not_a_dict"

        with pytest.raises(TypeError):
            update_nested("config", "key", "value")


class TestSessionStateList:
    """Test list operations."""

    def test_append_to_list_existing(self, mock_session_state):
        """Test appending to existing list."""
        mock_session_state["items"] = [1, 2]

        append_to_list("items", 3)

        assert mock_session_state["items"] == [1, 2, 3]

    def test_append_to_list_creates_list(self, mock_session_state):
        """Test append creates list if missing."""
        append_to_list("items", 1)

        assert mock_session_state["items"] == [1]

    def test_append_to_list_non_list_raises(self, mock_session_state):
        """Test append raises error if base is not list."""
        mock_session_state["items"] = "not_a_list"

        with pytest.raises(TypeError):
            append_to_list("items", "value")

    def test_extend_list_existing(self, mock_session_state):
        """Test extending existing list."""
        mock_session_state["items"] = [1, 2]

        extend_list("items", [3, 4])

        assert mock_session_state["items"] == [1, 2, 3, 4]

    def test_extend_list_creates_list(self, mock_session_state):
        """Test extend creates list if missing."""
        extend_list("items", [1, 2])

        assert mock_session_state["items"] == [1, 2]

    def test_extend_list_non_list_raises(self, mock_session_state):
        """Test extend raises error if base is not list."""
        mock_session_state["items"] = "not_a_list"

        with pytest.raises(TypeError):
            extend_list("items", [1, 2])

    def test_clear_list_existing(self, mock_session_state):
        """Test clearing existing list."""
        mock_session_state["items"] = [1, 2, 3]

        clear_list("items")

        assert mock_session_state["items"] == []

    def test_clear_list_missing(self, mock_session_state):
        """Test clearing missing list creates empty list."""
        clear_list("items")

        assert mock_session_state["items"] == []

    def test_clear_list_non_list_raises(self, mock_session_state):
        """Test clear raises error if base is not list."""
        mock_session_state["items"] = "not_a_list"

        with pytest.raises(TypeError):
            clear_list("items")


class TestSessionStateNumeric:
    """Test numeric operations."""

    def test_increment_existing(self, mock_session_state):
        """Test incrementing existing counter."""
        mock_session_state["counter"] = 5

        increment("counter", amount=2)

        assert mock_session_state["counter"] == 7

    def test_increment_creates_counter(self, mock_session_state):
        """Test increment creates counter if missing."""
        increment("counter", amount=5)

        assert mock_session_state["counter"] == 5

    def test_increment_default_amount(self, mock_session_state):
        """Test increment with default amount (1)."""
        mock_session_state["counter"] = 10

        increment("counter")

        assert mock_session_state["counter"] == 11

    def test_increment_negative(self, mock_session_state):
        """Test increment with negative amount (decrement)."""
        mock_session_state["counter"] = 10

        increment("counter", amount=-3)

        assert mock_session_state["counter"] == 7

    def test_increment_non_numeric_raises(self, mock_session_state):
        """Test increment raises error if base is not numeric."""
        mock_session_state["counter"] = "not_a_number"

        with pytest.raises(TypeError):
            increment("counter")


class TestSessionStateBoolean:
    """Test boolean operations."""

    def test_toggle_bool_true_to_false(self, mock_session_state):
        """Test toggling True to False."""
        mock_session_state["flag"] = True

        toggle_bool("flag")

        assert mock_session_state["flag"] is False

    def test_toggle_bool_false_to_true(self, mock_session_state):
        """Test toggling False to True."""
        mock_session_state["flag"] = False

        toggle_bool("flag")

        assert mock_session_state["flag"] is True

    def test_toggle_bool_creates_false(self, mock_session_state):
        """Test toggle creates False if missing."""
        toggle_bool("flag")

        assert mock_session_state["flag"] is False

    def test_toggle_bool_non_bool_raises(self, mock_session_state):
        """Test toggle raises error if base is not bool."""
        mock_session_state["flag"] = "not_a_bool"

        with pytest.raises(TypeError):
            toggle_bool("flag")


class TestSessionStateIntegration:
    """Integration tests for session state utilities."""

    def test_complex_workflow(self, mock_session_state):
        """Test complex workflow with multiple operations."""
        # Initialize
        initialize_session_state({
            "search_query": "",
            "search_results": [],
            "filters": {"type": "all"},
            "page": 1
        })

        # Update values
        set_value("search_query", "test query")
        update_nested("filters", "project", "myproject")
        append_to_list("search_results", {"id": 1, "name": "result1"})
        append_to_list("search_results", {"id": 2, "name": "result2"})
        increment("page")

        # Verify state
        assert get("search_query") == "test query"
        assert get("filters") == {"type": "all", "project": "myproject"}
        assert len(get("search_results")) == 2
        assert get("page") == 2

    def test_chat_history_workflow(self, mock_session_state):
        """Test chat history management workflow."""
        initialize_session_state({"chat_history": []})

        # Add messages
        append_to_list("chat_history", {"role": "user", "content": "Hello"})
        append_to_list("chat_history", {"role": "assistant", "content": "Hi there"})
        append_to_list("chat_history", {"role": "user", "content": "How are you?"})

        # Verify
        history = get("chat_history")
        assert len(history) == 3
        assert history[0]["role"] == "user"
        assert history[1]["role"] == "assistant"

        # Clear history
        clear_list("chat_history")
        assert get("chat_history") == []

    def test_workspace_state_workflow(self, mock_session_state):
        """Test workspace state management workflow."""
        initialize_session_state({
            "current_workspace": None,
            "workspace_artifacts": [],
            "workspace_modified": False
        })

        # Load workspace
        set_value("current_workspace", "ws-123")
        extend_list("workspace_artifacts", ["art-1", "art-2", "art-3"])
        toggle_bool("workspace_modified")  # False -> True

        # Verify
        assert get("current_workspace") == "ws-123"
        assert len(get("workspace_artifacts")) == 3
        assert get("workspace_modified") is True

        # Save workspace
        toggle_bool("workspace_modified")  # True -> False
        assert get("workspace_modified") is False
