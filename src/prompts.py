"""
Prompt templates for per-file intelligent metadata extraction (iteration10.md).
These prompts ask the LLM to return STRICT JSON with typed fields.
"""

from typing import Dict


SYSTEM_BASE = (
    "You are a senior software archeologist. Extract structured metadata from source files. "
    "Return STRICT JSON only with double-quoted keys and strings. No markdown, no prose, no code fences."
)


def prompt_for_file(language: str, project: str, path: str, content_sample: str) -> Dict[str, str]:
    """Return system+user prompt for a given file type."""
    base_user = f"Project: {project}\nPath: {path}\nLanguage: {language}\n\nContent:\n" + content_sample
    if language == 'java':
        schema = (
            '{"file":"' + path + '","language":"' + language + '","package":"","imports":[],'
            '"classes":[{"name":"","annotations":[],"extends":"","implements":[],'
            '"methods":[{"name":"","annotations":[],"params":[],"returnType":"","httpMapping":""}]}],'
            '"endpoints":[],"databaseObjects":[],"businessRules":[]}'
        )
        user = (
            "Extract package, imports, classes, methods, annotations, REST mappings, potential domain entities, "
            "and DB interactions. Return a SINGLE JSON object matching this schema strictly (double-quoted):\n" + schema
        )
        return {"system": SYSTEM_BASE, "user": base_user + "\n\n" + user}

    if language in ['jsp', 'html']:
        schema = (
            '{"file":"' + path + '","language":"' + language + '","forms":[{"action":"","method":"","fields":[{"name":"","type":""}]}],'
            '"scripts":[],"uiComponents":[],"navigation":[]}'
        )
        user = (
            "Extract forms, fields, actions, scripts, UI components, and navigation cues. Return a SINGLE JSON object (double-quoted) strictly matching:\n" + schema
        )
        return {"system": SYSTEM_BASE, "user": base_user + "\n\n" + user}

    if language in ['xml', 'sql']:
        schema = (
            '{"file":"' + path + '","language":"' + language + '","configuration":{"servlets":[],"filters":[],"datasources":[]},'
            '"tables":[],"queries":[]}'
        )
        user = (
            "Extract configuration (servlets, filters), tables, and queries. Return a SINGLE JSON object (double-quoted) strictly matching:\n" + schema
        )
        return {"system": SYSTEM_BASE, "user": base_user + "\n\n" + user}

    if language in ['javascript', 'css']:
        schema = (
            '{"file":"' + path + '","language":"' + language + '","functions":[],"classes":[],"rules":[]}'
        )
        user = ("Extract functions/classes (JS) or rules (CSS). Return a SINGLE JSON object (double-quoted) strictly matching:\n" + schema)
        return {"system": SYSTEM_BASE, "user": base_user + "\n\n" + user}

    if language in ['ini', 'properties', 'config']:
        schema = (
            '{"file":"' + path + '","language":"' + language + '","sections":[],"keys":{},"envDependencies":[]}'
        )
        user = (
            "Extract sections and key-value pairs, and identify environment-dependent keys (URLs, credentials, feature flags). Return STRICT JSON matching:\n" + schema
        )
        return {"system": SYSTEM_BASE, "user": base_user + "\n\n" + user}

    # default
    schema = '{"file":"' + path + '","language":"' + language + '","notes":""}'
    user = ("Extract any useful metadata. Return a SINGLE JSON object (double-quoted) strictly matching:\n" + schema)
    return {"system": SYSTEM_BASE, "user": base_user + "\n\n" + user}


