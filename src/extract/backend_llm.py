"""
LLM-backed extraction for backend files (java, xml, jsp, sql) to produce searchable summaries.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, List
import requests

from config.settings import settings

logger = logging.getLogger(__name__)


class BackendLLMExtractor:
    """Walk backend files and produce LLM summaries suitable for Weaviate indexing."""

    def __init__(self) -> None:
        self.build_dir = settings.build_dir / "backend_docs"
        self.build_dir.mkdir(parents=True, exist_ok=True)
        # Use localhost for host-side LLM calls even if settings points to host.docker.internal for Docker reachability
        base_url = settings.ollama_base_url
        if 'host.docker.internal' in base_url:
            base_url = 'http://127.0.0.1:11434'
        self.ollama_generate_url = f"{base_url}/api/generate"

    def _is_backend_file(self, path: str) -> bool:
        p = path.lower()
        if p.endswith(('.ui.xml', '.gwt.xml')):
            return False
        if p.endswith(('.js', '.ts', '.tsx')):
            return False
        return p.endswith(('.java', '.xml', '.jsp', '.jspf', '.sql'))

    def _detect_language(self, path: str) -> str:
        p = path.lower()
        if p.endswith('.java'):
            return 'java'
        if p.endswith(('.xml', '.ui.xml', '.gwt.xml')):
            return 'xml'
        if p.endswith(('.jsp', '.jspf')):
            return 'jsp'
        if p.endswith('.sql'):
            return 'sql'
        return 'text'

    def _summarize(self, path: Path, content: str) -> str:
        prompt = (
            "You are analyzing a backend source file. Summarize the business purpose, key data entities, "
            "important functions/methods/statements, inputs/outputs, and any domain terms. "
            "Keep it concise but information-dense.\n\n"
            f"File: {path}\nLanguage: {self._detect_language(str(path))}\n\n"
            "=== BEGIN FILE CONTENT (truncated if large) ===\n"
        )
        # Limit content to ~8k chars to avoid huge payloads
        snippet = content[:8000]
        payload = {
            "model": settings.ollama_model_name,
            "prompt": f"{prompt}{snippet}\n=== END FILE CONTENT ===",
            "stream": False
        }
        try:
            resp = requests.post(self.ollama_generate_url, json=payload, timeout=60)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("response", "")
            logger.warning("LLM summarize failed %s: %s", path, resp.text)
            return ""
        except Exception as e:
            logger.warning("LLM summarize exception %s: %s", path, e)
            return ""

    def extract_backend_docs(self, discovered_files: Dict[str, List[str]], project: str) -> List[Dict]:
        docs: List[Dict] = []
        # Combine all discovered paths and filter to backend-only
        all_paths: List[str] = []
        for files in discovered_files.values():
            all_paths.extend(list(files))

        backend_paths = [p for p in all_paths if self._is_backend_file(p)]
        logger.info("Backend LLM extractor will process %d files", len(backend_paths))

        for path_str in backend_paths:
            try:
                path = Path(path_str)
                if not path.exists() or not path.is_file():
                    continue
                content = path.read_text(encoding='utf-8', errors='ignore')
                summary = self._summarize(path, content)
                doc = {
                    "project": project,
                    "path": str(path),
                    "language": self._detect_language(str(path)),
                    "text": content[:2000],  # store a snippet for search context
                    "summary": summary,
                }
                docs.append(doc)
            except Exception as e:
                logger.warning("Skipping %s due to error: %s", path_str, e)

        # Save
        out_file = self.build_dir / "all_backend_docs.json"
        with out_file.open('w', encoding='utf-8') as f:
            json.dump(docs, f, ensure_ascii=False, indent=2)
        logger.info("Saved %d backend docs to %s", len(docs), out_file)
        return docs


