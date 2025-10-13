"""
RequirementsAgent: generates extreme-detailed requirement docs per artifact (form/function/etc).
Produces per-artifact markdown files and an index summary.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, List, Any
import requests

from config.settings import settings

logger = logging.getLogger(__name__)


def _ollama_generate(prompt: str) -> str:
    base_url = settings.ollama_base_url
    if 'host.docker.internal' in base_url:
        base_url = 'http://127.0.0.1:11434'
    url = f"{base_url}/api/generate"
    payload = {
        "model": settings.ollama_model_name,
        "prompt": prompt,
        "stream": False
    }
    timeouts = [60, 90, 120]
    for attempt, to in enumerate(timeouts, 1):
        try:
            # health check
            try:
                hc = requests.get(f"{base_url}/api/tags", timeout=5)
                if hc.status_code != 200:
                    logger.warning("Ollama health non-200: %s", hc.status_code)
            except Exception:
                logger.warning("Ollama health check failed (attempt %s)", attempt)

            resp = requests.post(url, json=payload, timeout=to)
            if resp.status_code == 200:
                return resp.json().get("response", "")
            logger.warning("Ollama generation failed %s: %s", resp.status_code, resp.text)
        except Exception as e:
            logger.warning("Ollama generation attempt %s exception: %s", attempt, e)
        import time as _t
        _t.sleep(2 * attempt)
    return ""


def _short(text: str, n: int = 2000) -> str:
    return text[:n]


class RequirementsAgent:
    """Generates per-artifact requirement documents using LLM."""

    def __init__(self) -> None:
        self.output_root = settings.output_dir / "requirements"
        self.output_root.mkdir(parents=True, exist_ok=True)

    def _artifact_prompt(self, artifact_type: str, artifact: Dict[str, Any]) -> str:
        """Build a prompt tailored for artifact type."""
        path = artifact.get("path", "Unknown")
        text = artifact.get("text") or artifact.get("summary") or artifact.get("rawXml") or ""
        meta = artifact.copy()
        # keep prompt bounded
        text_snip = _short(str(text), 6000)
        meta_snip = _short(json.dumps(meta, ensure_ascii=False), 3000)
        return (
            "You are a senior business analyst. Generate EXTREMELY detailed software requirements for one artifact.\n"
            "Include: purpose, inputs, outputs, validations, field definitions, states, error cases,\n"
            "business rules, dependencies, integration points, traceability hints (file, class, method).\n"
            "Write in structured Markdown with headings, bullet points, and acceptance criteria.\n\n"
            f"Artifact Type: {artifact_type}\n"
            f"File Path: {path}\n\n"
            f"Artifact Snapshot (truncated):\n{text_snip}\n\n"
            f"Artifact Metadata (truncated JSON):\n{meta_snip}\n\n"
            "Now produce the requirements as a standalone section suitable for a PRD."
        )

    def _write_file(self, project: str, artifact_type: str, stem: str, content: str) -> Path:
        out_dir = self.output_root / project / artifact_type
        out_dir.mkdir(parents=True, exist_ok=True)
        safe_stem = stem.replace('/', '_')[:120]
        out_path = out_dir / f"{safe_stem}.md"
        out_path.write_text(content or "No content generated.", encoding='utf-8')
        logger.info("OK: wrote requirements file %s", out_path)
        return out_path

    def run(self, project: str, artifacts: Dict[str, List[Dict[str, Any]]]) -> Path:
        """Generate requirement docs for selected artifact types, return index path."""
        # Choose artifact groups to cover forms/functions/backend docs
        groups = [
            ("dao_calls", artifacts.get("dao_calls", [])),
            ("jsp_forms", artifacts.get("jsp_forms", [])),
            ("backend_docs", artifacts.get("backend_docs", [])),
            ("gwt_uibinder", artifacts.get("gwt_uibinder", [])),
        ]

        index_lines: List[str] = [f"# Detailed Requirements Index - {project}", ""]

        for artifact_type, items in groups:
            if not items:
                continue
            index_lines.append(f"## {artifact_type.replace('_', ' ').title()} ({len(items)})")
            for i, artifact in enumerate(items, 1):
                try:
                    prompt = self._artifact_prompt(artifact_type, artifact)
                    content = _ollama_generate(prompt)
                    name = artifact.get("path") or artifact.get("ownerType") or artifact.get("methodName") or f"{artifact_type}_{i}"
                    out_path = self._write_file(project, artifact_type, Path(str(name)).name, content)
                    index_lines.append(f"- [{Path(str(name)).name}]({out_path})")
                except Exception as e:
                    logger.warning("Failed to generate requirements for %s #%s: %s", artifact_type, i, e)
            index_lines.append("")

        index_path = self.output_root / project / "INDEX.md"
        index_path.write_text("\n".join(index_lines), encoding='utf-8')
        return index_path


