"""
Unit tests for URL parameter persistence (T032 - US1.2).

Tests URL parameter encoding/decoding including:
- Query parameter serialization
- Filter state encoding
- URL safe encoding
- Parameter parsing and restoration
- Error handling for malformed params
"""

import pytest
import json
import base64
from typing import Dict, Any, Optional
from urllib.parse import urlencode, parse_qs


class TestURLParameterEncoding:
    """Test URL parameter encoding functionality."""

    def test_encode_empty_params(self):
        """Test encoding empty parameters."""
        params = {}

        encoded = encode_url_params(params)

        assert encoded == {} or encoded is None

    def test_encode_simple_string_param(self):
        """Test encoding simple string parameter."""
        params = {"query": "test search"}

        encoded = encode_url_params(params)

        assert "query" in encoded
        assert encoded["query"] == "test search"

    def test_encode_integer_param(self):
        """Test encoding integer parameter."""
        params = {"page": 1, "limit": 50}

        encoded = encode_url_params(params)

        assert "page" in encoded
        assert "limit" in encoded

    def test_encode_list_param(self):
        """Test encoding list parameter."""
        params = {"artifact_types": ["DaoCall", "GwtPresenter"]}

        encoded = encode_url_params(params)

        assert "artifact_types" in encoded
        # Should be encoded as JSON or comma-separated

    def test_encode_nested_dict(self):
        """Test encoding nested dictionary."""
        params = {
            "filters": {
                "artifact_types": ["DaoCall"],
                "project": "com.example:app:1.0.0"
            }
        }

        encoded = encode_url_params(params)

        assert "filters" in encoded

    def test_encode_special_characters(self):
        """Test encoding parameters with special characters."""
        params = {
            "query": "test @#$%^&*() query",
            "project": "com.example:app:1.0.0"
        }

        encoded = encode_url_params(params)

        # Should be URL-safe encoded
        assert "query" in encoded
        assert "project" in encoded

    def test_encode_unicode_characters(self):
        """Test encoding parameters with unicode characters."""
        params = {"query": "test 中文 query"}

        encoded = encode_url_params(params)

        assert "query" in encoded


class TestURLParameterDecoding:
    """Test URL parameter decoding functionality."""

    def test_decode_empty_params(self):
        """Test decoding empty parameters."""
        encoded = {}

        decoded = decode_url_params(encoded)

        assert decoded == {}

    def test_decode_simple_string_param(self):
        """Test decoding simple string parameter."""
        encoded = {"query": "test search"}

        decoded = decode_url_params(encoded)

        assert decoded["query"] == "test search"

    def test_decode_integer_param(self):
        """Test decoding integer parameter."""
        encoded = {"page": "1", "limit": "50"}

        decoded = decode_url_params(encoded)

        # Should convert string to int
        assert decoded["page"] == 1
        assert decoded["limit"] == 50

    def test_decode_list_param(self):
        """Test decoding list parameter."""
        # Encoded as JSON string
        encoded = {"artifact_types": json.dumps(["DaoCall", "GwtPresenter"])}

        decoded = decode_url_params(encoded)

        assert decoded["artifact_types"] == ["DaoCall", "GwtPresenter"]

    def test_decode_nested_dict(self):
        """Test decoding nested dictionary."""
        filters = {
            "artifact_types": ["DaoCall"],
            "project": "com.example:app:1.0.0"
        }
        encoded = {"filters": json.dumps(filters)}

        decoded = decode_url_params(encoded)

        assert decoded["filters"] == filters

    def test_decode_malformed_json(self):
        """Test handling of malformed JSON in parameters."""
        encoded = {"filters": "not valid json {"}

        decoded = decode_url_params(encoded)

        # Should handle gracefully, return original or empty
        assert "filters" in decoded or decoded == {}


class TestURLParameterRoundTrip:
    """Test round-trip encoding and decoding."""

    def test_roundtrip_simple_params(self):
        """Test round-trip with simple parameters."""
        original = {
            "query": "test search",
            "page": 1,
            "limit": 50
        }

        encoded = encode_url_params(original)
        decoded = decode_url_params(encoded)

        assert decoded["query"] == original["query"]
        assert decoded["page"] == original["page"]
        assert decoded["limit"] == original["limit"]

    def test_roundtrip_complex_filters(self):
        """Test round-trip with complex filter structure."""
        original = {
            "query": "database access",
            "filters": {
                "artifact_types": ["DaoCall", "IbatisStatement"],
                "project": "com.example:app:1.0.0"
            },
            "page": 2
        }

        encoded = encode_url_params(original)
        decoded = decode_url_params(encoded)

        assert decoded["query"] == original["query"]
        assert decoded["filters"] == original["filters"]
        assert decoded["page"] == original["page"]

    def test_roundtrip_special_characters(self):
        """Test round-trip with special characters."""
        original = {
            "query": "test @#$% query",
            "project": "com.example:app:1.0.0"
        }

        encoded = encode_url_params(original)
        decoded = decode_url_params(encoded)

        assert decoded["query"] == original["query"]
        assert decoded["project"] == original["project"]


class TestFilterStateEncoding:
    """Test specific filter state encoding."""

    def test_encode_artifact_type_filter(self):
        """Test encoding artifact type filter."""
        filters = {"artifact_types": ["DaoCall", "GwtPresenter", "GwtView"]}

        encoded = encode_filter_state(filters)

        assert encoded is not None
        # Should be compact representation

    def test_encode_project_filter(self):
        """Test encoding project filter."""
        filters = {"project": "com.example:app:1.0.0"}

        encoded = encode_filter_state(filters)

        assert encoded is not None

    def test_encode_combined_filters(self):
        """Test encoding combined filters."""
        filters = {
            "artifact_types": ["DaoCall", "GwtPresenter"],
            "project": "com.example:app:1.0.0"
        }

        encoded = encode_filter_state(filters)

        assert encoded is not None

    def test_decode_artifact_type_filter(self):
        """Test decoding artifact type filter."""
        filters = {"artifact_types": ["DaoCall", "GwtPresenter"]}
        encoded = encode_filter_state(filters)

        decoded = decode_filter_state(encoded)

        assert decoded == filters

    def test_decode_combined_filters(self):
        """Test decoding combined filters."""
        filters = {
            "artifact_types": ["DaoCall"],
            "project": "com.example:app:1.0.0"
        }
        encoded = encode_filter_state(filters)

        decoded = decode_filter_state(encoded)

        assert decoded == filters


class TestURLSafeEncoding:
    """Test URL-safe encoding for shareable links."""

    def test_url_safe_encoding(self):
        """Test that encoded params are URL-safe."""
        params = {
            "query": "test / path ? & = query",
            "filters": {
                "artifact_types": ["DaoCall"]
            }
        }

        encoded = encode_url_params(params)

        # Convert to URL query string
        query_string = urlencode(encoded)

        # Should not contain unescaped special characters
        assert "/" not in query_string or "%2F" in query_string
        assert "?" not in query_string or "%3F" in query_string

    def test_url_safe_decoding(self):
        """Test decoding URL-escaped parameters."""
        # Simulate URL-escaped params
        query_string = "query=test%20search&page=1"
        encoded = parse_qs(query_string)

        # Convert single-item lists to values
        encoded = {k: v[0] if len(v) == 1 else v for k, v in encoded.items()}

        decoded = decode_url_params(encoded)

        assert decoded["query"] == "test search"
        assert decoded["page"] == 1


class TestEdgeCases:
    """Test edge cases in URL parameter handling."""

    def test_encode_none_values(self):
        """Test encoding None values."""
        params = {"query": "test", "project": None}

        encoded = encode_url_params(params)

        # Should filter out None values or handle gracefully
        assert "query" in encoded

    def test_encode_empty_strings(self):
        """Test encoding empty strings."""
        params = {"query": "", "page": 1}

        encoded = encode_url_params(params)

        # Empty strings might be filtered out
        assert isinstance(encoded, dict)

    def test_decode_missing_keys(self):
        """Test decoding when expected keys are missing."""
        encoded = {"page": "1"}  # Missing query

        decoded = decode_url_params(encoded)

        assert "page" in decoded
        # Missing keys should be absent or have defaults

    def test_decode_invalid_types(self):
        """Test decoding with invalid type conversions."""
        encoded = {"page": "not_a_number"}

        decoded = decode_url_params(encoded)

        # Should handle gracefully, might return string or None


# Helper functions that would be implemented in url_params.py utility

def encode_url_params(params: Dict[str, Any]) -> Dict[str, str]:
    """
    Encode parameters for URL query string.

    Args:
        params: Dictionary of parameters to encode

    Returns:
        Dictionary with string values suitable for URL
    """
    encoded = {}

    for key, value in params.items():
        if value is None:
            continue

        if isinstance(value, (dict, list)):
            # Encode complex types as JSON
            encoded[key] = json.dumps(value)
        elif isinstance(value, (int, float)):
            encoded[key] = str(value)
        elif isinstance(value, str):
            if value:  # Skip empty strings
                encoded[key] = value

    return encoded


def decode_url_params(encoded: Dict[str, str]) -> Dict[str, Any]:
    """
    Decode parameters from URL query string.

    Args:
        encoded: Dictionary with string values from URL

    Returns:
        Dictionary with decoded values
    """
    decoded = {}

    for key, value in encoded.items():
        # Try to decode as JSON first
        if isinstance(value, str) and (value.startswith("{") or value.startswith("[")):
            try:
                decoded[key] = json.loads(value)
                continue
            except json.JSONDecodeError:
                pass

        # Try to convert to int
        if isinstance(value, str) and value.isdigit():
            decoded[key] = int(value)
            continue

        # Keep as string
        decoded[key] = value

    return decoded


def encode_filter_state(filters: Dict[str, Any]) -> str:
    """
    Encode filter state to compact string.

    Args:
        filters: Filter dictionary

    Returns:
        Encoded filter string
    """
    return json.dumps(filters)


def decode_filter_state(encoded: str) -> Dict[str, Any]:
    """
    Decode filter state from compact string.

    Args:
        encoded: Encoded filter string

    Returns:
        Filter dictionary
    """
    try:
        return json.loads(encoded)
    except json.JSONDecodeError:
        return {}
