"""
SolutionAgent: synthesizes a modern target solution based on analyzed artifacts
and prior requirements. Outputs:
- Architecture (Node.js microservices + PostgreSQL + Next.js)
- Database design migration (from legacy tables)
- UI plan (Next.js app structure, routes, components)
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
import requests

from config.settings import settings

logger = logging.getLogger(__name__)


def _short(text: str, n: int = 8000) -> str:
    return text[:n]


class SolutionAgent:
    """Generates a solution blueprint and migration plan for a modern stack."""

    def __init__(self) -> None:
        self.output_dir = settings.output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        base_url = settings.ollama_base_url
        if 'host.docker.internal' in base_url:
            base_url = 'http://127.0.0.1:11434'
        self._ollama_base = base_url
        self._gen_url = f"{base_url}/api/generate"

    def _call_llm(self, prompt: str, timeouts: List[int] = [90, 120, 150]) -> str:
        payload = {
            "model": settings.ollama_model_name,
            "prompt": prompt,
            "stream": False,
        }
        for attempt, to in enumerate(timeouts, 1):
            try:
                try:
                    hc = requests.get(f"{self._ollama_base}/api/tags", timeout=5)
                    if hc.status_code != 200:
                        logger.warning("Ollama health non-200: %s", hc.status_code)
                except Exception:
                    logger.warning("Ollama health check failed (attempt %s)", attempt)
                resp = requests.post(self._gen_url, json=payload, timeout=to)
                if resp.status_code == 200:
                    return resp.json().get("response", "")
                logger.warning("Ollama generation failed %s: %s", resp.status_code, resp.text)
            except Exception as e:
                logger.warning("Ollama generation attempt %s exception: %s", attempt, e)
            import time as _t
            _t.sleep(2 * attempt)
        return ""

    def _load_artifacts(self) -> Dict[str, Any]:
        """Load key build artifacts for solution planning."""
        build_dir = settings.build_dir
        files = {
            'db_tables': ('db_schema', 'all_tables.json'),
            'dao_calls': ('java_calls', 'all_dao_calls.json'),
            'ibatis_statements': ('ibatis_statements', 'all_statements.json'),
            'gwt_client': ('gwt_client', 'all_artifacts.json'),
            'gwt_uibinder': ('gwt_uibinder', 'all_uibinder.json'),
            'backend_docs': ('backend_docs', 'all_backend_docs.json'),
        }
        data: Dict[str, Any] = {}
        for key, (subdir, fname) in files.items():
            p = build_dir / subdir / fname
            if p.exists():
                try:
                    data[key] = json.loads(p.read_text(encoding='utf-8'))
                except Exception as e:
                    logger.warning("Failed reading %s: %s", p, e)
                    data[key] = []
            else:
                data[key] = []
        return data

    def _prompt_architecture(self, project: str, artifacts: Dict[str, Any], prior_requirements: str) -> str:
        context = {
            'daoCallsCount': len(artifacts.get('dao_calls', [])),
            'ibatisCount': len(artifacts.get('ibatis_statements', [])),
            'tablesCount': len(artifacts.get('db_tables', [])),
            'uiArtifacts': len(artifacts.get('gwt_uibinder', [])) + (len(artifacts.get('gwt_client', {}).get('activities_places', [])) if isinstance(artifacts.get('gwt_client'), dict) else len(artifacts.get('gwt_client', []))),
        }
        prior = _short(prior_requirements, 12000)
        return (
            "You are a principal software architect. Design a modern target solution based on legacy Java/JSP/GWT/iBATIS artifacts.\n"
            "Target stack: Node.js microservices (TypeScript, Express/Fastify), PostgreSQL, Next.js (App Router).\n"
            "Deliver a comprehensive architecture blueprint including: service decomposition, bounded contexts, inter-service communication, API gateway, auth, observability, CI/CD, deployment (Kubernetes), and data ownership.\n"
            f"Project: {project}\n"
            f"Artifact Summary: {json.dumps(context)}\n\n"
            "Relevant legacy requirements (truncated):\n" + prior + "\n\n"
            "Output as detailed Markdown with sections: Overview, Services (with responsibilities), APIs (per service), Data (ownership, schemas), Messaging, Security, Non-Functional (SLAs/SLOs), Deployment & Ops."
        )

    def _prompt_db_migration(self, project: str, db_tables: List[Dict[str, Any]], prior_requirements: str) -> str:
        tables_snip = _short(json.dumps(db_tables, ensure_ascii=False), 16000)
        prior = _short(prior_requirements, 6000)
        return (
            "You are a database architect. Propose a PostgreSQL schema design and migration plan from legacy tables.\n"
            "Goals: normalization where appropriate, clear PK/FK, indexes, auditing, soft delete, multi-tenancy strategy if hinted, and naming conventions.\n"
            "Provide: ERD description, table definitions (SQL DDL), mapping from legacy->new, migration strategy (phase plan, scripts outline), and data quality checks.\n"
            f"Project: {project}\n\n"
            "Legacy tables (truncated JSON):\n" + tables_snip + "\n\n"
            "Relevant requirements (truncated):\n" + prior + "\n\n"
            "Output Markdown with sections: ERD, Tables (DDL blocks), Mapping, Migration Plan, Risks."
        )

    def _prompt_ui_plan(self, project: str, ui_artifacts: Dict[str, Any], prior_requirements: str) -> str:
        ui_snip = _short(json.dumps(ui_artifacts, ensure_ascii=False), 14000)
        prior = _short(prior_requirements, 6000)
        return (
            "You are a frontend architect. Produce a Next.js UI plan translating legacy JSP/GWT artifacts.\n"
            "Include: route map, layouts, pages, server actions, forms handling, client components, state management, accessibility, i18n, and testing.\n"
            f"Project: {project}\n\n"
            "Legacy UI artifacts (truncated JSON):\n" + ui_snip + "\n\n"
            "Relevant requirements (truncated):\n" + prior + "\n\n"
            "Output Markdown with sections: Information Architecture, Routes, Components, Forms, Data Fetching, State, Styling, Accessibility, Testing."
        )

    def run(self, project: str, prior_backend_md: Optional[str], prior_frontend_md: Optional[str]) -> Dict[str, Path]:
        """Generate architecture, DB design, and UI plan. Returns output file paths."""
        artifacts = self._load_artifacts()
        prior_text = "\n\n".join([t for t in [prior_backend_md, prior_frontend_md] if t])

        arch_prompt = self._prompt_architecture(project, artifacts, prior_text)
        arch_md = self._call_llm(arch_prompt)

        db_prompt = self._prompt_db_migration(project, artifacts.get('db_tables', []), prior_text)
        db_md = self._call_llm(db_prompt)

        ui_ctx = {
            'gwt_client': artifacts.get('gwt_client', {}),
            'gwt_uibinder': artifacts.get('gwt_uibinder', []),
            'jsp_forms': [],  # could be loaded if needed
        }
        ui_prompt = self._prompt_ui_plan(project, ui_ctx, prior_text)
        ui_md = self._call_llm(ui_prompt)

        out_arch = self.output_dir / f"{project}_solution_architecture.md"
        out_db = self.output_dir / f"{project}_db_design.md"
        out_ui = self.output_dir / f"{project}_ui_plan.md"

        out_arch.write_text(arch_md or "No content generated.", encoding='utf-8')
        out_db.write_text(db_md or "No content generated.", encoding='utf-8')
        out_ui.write_text(ui_md or "No content generated.", encoding='utf-8')

        combined = self.output_dir / f"{project}_solution.md"
        combined.write_text("\n\n".join([
            "# Target Solution Architecture", arch_md or "",
            "\n---\n\n# Database Design & Migration", db_md or "",
            "\n---\n\n# Next.js UI Plan", ui_md or "",
        ]), encoding='utf-8')

        return {
            'architecture': out_arch,
            'db_design': out_db,
            'ui_plan': out_ui,
            'solution': combined,
        }


