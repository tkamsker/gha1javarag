"""
LLM client abstraction supporting OpenAI, Ollama, and Anthropic providers.
Used for per-file intelligent prompting and requirements synthesis.
"""

from typing import Dict, Any, Optional
import json
import logging
import httpx
from pathlib import Path
from datetime import datetime


class LLMClient:
    """Thin client to call different LLM providers behind a simple interface."""

    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.provider = config.ai_provider

    def complete_json(self, prompt: str, system: Optional[str] = None, max_tokens: int = 2000) -> Dict[str, Any]:
        """Call provider and return parsed JSON; if parsing fails, return empty dict."""
        text = self._complete_text(prompt, system=system, max_tokens=max_tokens)
        # Try to extract JSON from text robustly
        try:
            candidate = self._extract_first_json(text)
            return json.loads(candidate)
        except Exception as e:
            self._log_raw_llm_output(text, reason=str(e))
            self.logger.debug("LLM JSON parse failed; returning empty dict")
            return {}

    def _complete_text(self, prompt: str, system: Optional[str] = None, max_tokens: int = 2000) -> str:
        if self.provider == 'openai':
            return self._openai_chat(prompt, system, max_tokens)
        if self.provider == 'ollama':
            return self._ollama_chat(prompt, system, max_tokens)
        if self.provider == 'anthropic':
            return self._anthropic_chat(prompt, system, max_tokens)
        raise ValueError(f"Unsupported AI provider: {self.provider}")

    def _openai_chat(self, prompt: str, system: Optional[str], max_tokens: int) -> str:
        url = f"{self.config.openai_api_base}/chat/completions"
        headers = {"Authorization": f"Bearer {self.config.openai_api_key}", "Content-Type": "application/json"}
        body = {
            "model": self.config.openai_model_name,
            "messages": ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": max_tokens,
        }
        with httpx.Client(timeout=self.config.ollama_timeout) as client:
            resp = client.post(url, headers=headers, json=body)
            resp.raise_for_status()
            data = resp.json()
            return (data.get('choices') or [{}])[0].get('message', {}).get('content', '')

    def _ollama_chat(self, prompt: str, system: Optional[str], max_tokens: int) -> str:
        url = f"{self.config.ollama_base_url}/api/chat"
        body = {
            "model": self.config.ollama_model_name,
            "messages": ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}],
            "options": {"temperature": 0.1, "num_predict": max_tokens},
            "stream": False
        }
        with httpx.Client(timeout=self.config.ollama_timeout) as client:
            resp = client.post(url, json=body)
            resp.raise_for_status()
            data = resp.json()
            # Expect a single message object when stream=False
            if isinstance(data, dict) and 'message' in data:
                return data['message'].get('content', '')
            # Fallbacks for unexpected formats
            if isinstance(data, list):
                parts = [d.get('message', {}).get('content', '') for d in data]
                return ''.join(parts)
            return ''

    def _anthropic_chat(self, prompt: str, system: Optional[str], max_tokens: int) -> str:
        url = f"{self.config.anthropic_api_base}/v1/messages"
        headers = {
            "x-api-key": self.config.anthropic_api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        body = {
            "model": self.config.anthropic_model_name,
            "max_tokens": max_tokens,
            "messages": ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}],
        }
        with httpx.Client(timeout=self.config.ollama_timeout) as client:
            resp = client.post(url, headers=headers, json=body)
            resp.raise_for_status()
            data = resp.json()
            blocks = data.get('content') or []
            texts = [b.get('text', '') for b in blocks if b.get('type') == 'text']
            return ''.join(texts)

    # --- helpers ---

    def _extract_first_json(self, text: str) -> str:
        """Extract the first balanced JSON object or array from text; also strips code fences.

        Raises ValueError if nothing that looks like JSON is found.
        """
        if not text:
            raise ValueError("empty LLM response")

        # Strip common markdown fences
        stripped = text.strip()
        if stripped.startswith("```"):
            # remove opening fence line
            stripped = '\n'.join(stripped.splitlines()[1:])
        if stripped.endswith("```"):
            stripped = '\n'.join(stripped.splitlines()[:-1])
        stripped = stripped.strip()

        # Quick path: direct JSON
        try:
            obj = json.loads(stripped)
            # If this works, return canonical slice
            return json.dumps(obj)
        except Exception:
            pass

        # Scan for first balanced {...} or [...] region
        openers = {'{': '}', '[': ']'}
        closers = set(openers.values())
        stack = []
        start_index = -1
        for i, ch in enumerate(stripped):
            if ch in openers:
                if not stack:
                    start_index = i
                stack.append(openers[ch])
            elif ch in closers and stack:
                expected = stack.pop()
                # If mismatch, continue scanning but do not error
                if ch != expected:
                    continue
                if not stack and start_index != -1:
                    candidate = stripped[start_index:i + 1]
                    # Validate candidate
                    json.loads(candidate)  # may raise
                    return candidate
        # As a last attempt, try to locate the first '{' ... last '}' span
        s = stripped.find('{')
        e = stripped.rfind('}')
        if s != -1 and e != -1 and e > s:
            candidate = stripped[s:e + 1]
            json.loads(candidate)  # may raise
            return candidate
        raise ValueError("no JSON found in LLM output")

    def _log_raw_llm_output(self, text: str, reason: str) -> None:
        """Persist raw LLM response to logs directory for debugging."""
        try:
            out_dir = Path(getattr(self.config, 'output_dir', '.')) / 'logs'
            out_dir.mkdir(parents=True, exist_ok=True)
            ts = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            file_path = out_dir / f"llm_raw_{ts}.txt"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"reason: {reason}\n")
                f.write("--- raw ---\n")
                f.write(text or '')
            self.logger.debug(f"Wrote raw LLM output to {file_path}")
        except Exception:
            # do not raise from logging path
            pass


