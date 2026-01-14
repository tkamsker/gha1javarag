"""
URL parameter utilities for persisting state in URLs (T038, T039 - US1.2).

This module provides functions for encoding/decoding state to/from URL parameters
to create shareable search links.
"""

import json
from typing import Dict, Any, Optional
from urllib.parse import urlencode, parse_qs


def encode_url_params(params: Dict[str, Any]) -> Dict[str, str]:
    """
    Encode parameters for URL query string.

    Converts complex types (dicts, lists) to JSON strings and ensures
    all values are URL-safe strings.

    Args:
        params: Dictionary of parameters to encode

    Returns:
        Dictionary with string values suitable for URL query string

    Example:
        >>> encode_url_params({"query": "test", "page": 1, "filters": {"types": ["DaoCall"]}})
        {"query": "test", "page": "1", "filters": '{"types": ["DaoCall"]}'}
    """
    encoded = {}

    for key, value in params.items():
        if value is None:
            continue

        if isinstance(value, (dict, list)):
            # Encode complex types as JSON
            encoded[key] = json.dumps(value)
        elif isinstance(value, bool):
            # Encode booleans as lowercase strings
            encoded[key] = str(value).lower()
        elif isinstance(value, (int, float)):
            # Encode numbers as strings
            encoded[key] = str(value)
        elif isinstance(value, str):
            if value:  # Skip empty strings
                encoded[key] = value

    return encoded


def decode_url_params(encoded: Dict[str, Any]) -> Dict[str, Any]:
    """
    Decode parameters from URL query string.

    Converts JSON strings back to dicts/lists and attempts to convert
    numeric strings to integers.

    Args:
        encoded: Dictionary with string values from URL

    Returns:
        Dictionary with decoded values of appropriate types

    Example:
        >>> decode_url_params({"query": "test", "page": "1", "filters": '{"types": ["DaoCall"]}'})
        {"query": "test", "page": 1, "filters": {"types": ["DaoCall"]}}
    """
    decoded = {}

    for key, value in encoded.items():
        # Handle list values from parse_qs (returns lists)
        if isinstance(value, list):
            if len(value) == 1:
                value = value[0]
            # If multiple values, keep as list

        # Try to decode as JSON first (for dicts and lists)
        if isinstance(value, str):
            # Check if it looks like JSON
            if (value.startswith("{") and value.endswith("}")) or \
               (value.startswith("[") and value.endswith("]")):
                try:
                    decoded[key] = json.loads(value)
                    continue
                except json.JSONDecodeError:
                    pass  # Not valid JSON, try other conversions

            # Try to convert to int
            if value.isdigit():
                decoded[key] = int(value)
                continue

            # Try to convert to float
            try:
                if "." in value:
                    decoded[key] = float(value)
                    continue
            except ValueError:
                pass

            # Try to convert to bool
            if value.lower() in ("true", "false"):
                decoded[key] = value.lower() == "true"
                continue

        # Keep as-is
        decoded[key] = value

    return decoded


def encode_filter_state(filters: Dict[str, Any]) -> str:
    """
    Encode filter state to compact JSON string.

    Args:
        filters: Filter dictionary with artifact_types and/or project

    Returns:
        JSON string representation of filters

    Example:
        >>> encode_filter_state({"artifact_types": ["DaoCall"], "project": "com.example:app"})
        '{"artifact_types": ["DaoCall"], "project": "com.example:app"}'
    """
    if not filters:
        return "{}"

    return json.dumps(filters, separators=(',', ':'))  # Compact JSON


def decode_filter_state(encoded: str) -> Dict[str, Any]:
    """
    Decode filter state from JSON string.

    Args:
        encoded: JSON string representation of filters

    Returns:
        Filter dictionary, or empty dict if decoding fails

    Example:
        >>> decode_filter_state('{"artifact_types": ["DaoCall"]}')
        {"artifact_types": ["DaoCall"]}
    """
    if not encoded or encoded == "{}":
        return {}

    try:
        return json.loads(encoded)
    except json.JSONDecodeError:
        return {}


def build_query_string(params: Dict[str, Any]) -> str:
    """
    Build URL query string from parameters.

    Args:
        params: Dictionary of parameters

    Returns:
        URL-encoded query string (without leading '?')

    Example:
        >>> build_query_string({"query": "test search", "page": 1})
        'query=test+search&page=1'
    """
    encoded = encode_url_params(params)
    return urlencode(encoded)


def parse_query_string(query_string: str) -> Dict[str, Any]:
    """
    Parse URL query string to parameters dictionary.

    Args:
        query_string: URL query string (with or without leading '?')

    Returns:
        Dictionary of decoded parameters

    Example:
        >>> parse_query_string("query=test+search&page=1")
        {"query": "test search", "page": 1}
    """
    # Remove leading '?' if present
    if query_string.startswith("?"):
        query_string = query_string[1:]

    # Parse query string
    parsed = parse_qs(query_string)

    # Decode values
    return decode_url_params(parsed)


def merge_url_params(
    current: Dict[str, Any],
    updates: Dict[str, Any],
    preserve_keys: Optional[list] = None
) -> Dict[str, Any]:
    """
    Merge URL parameters, updating or adding values.

    Args:
        current: Current parameter dictionary
        updates: Parameters to update or add
        preserve_keys: Keys to preserve from current even if not in updates

    Returns:
        Merged parameter dictionary

    Example:
        >>> merge_url_params({"query": "old", "page": 1}, {"query": "new"})
        {"query": "new", "page": 1}
    """
    merged = current.copy()

    # Update with new values
    for key, value in updates.items():
        if value is None:
            # Remove key if value is None
            merged.pop(key, None)
        else:
            merged[key] = value

    # Preserve specified keys
    if preserve_keys:
        for key in preserve_keys:
            if key in current and key not in updates:
                merged[key] = current[key]

    return merged


def clean_url_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean URL parameters by removing None values and empty collections.

    Args:
        params: Parameter dictionary

    Returns:
        Cleaned parameter dictionary

    Example:
        >>> clean_url_params({"query": "test", "page": None, "filters": {}})
        {"query": "test"}
    """
    cleaned = {}

    for key, value in params.items():
        if value is None:
            continue

        if isinstance(value, (list, dict)) and len(value) == 0:
            continue

        if isinstance(value, str) and not value:
            continue

        cleaned[key] = value

    return cleaned


__all__ = [
    "encode_url_params",
    "decode_url_params",
    "encode_filter_state",
    "decode_filter_state",
    "build_query_string",
    "parse_query_string",
    "merge_url_params",
    "clean_url_params"
]
