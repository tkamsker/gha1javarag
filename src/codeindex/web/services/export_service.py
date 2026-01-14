"""
Export service for generating and exporting documents (Phase 15-17).

This service provides export functionality for:
- PRDs (Product Requirements Documents)
- Technical Specifications
- Test Reports
- Multiple formats: PDF, Markdown, JSON, CSV
"""

import logging
import json
import time
from typing import Optional, Dict, List, Any
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class ExportService:
    """
    Service for exporting documents in various formats.

    Features:
    - Export to PDF, Markdown, JSON, CSV
    - PRD generation
    - Spec generation
    - Test report generation
    - Citation formatting
    """

    def __init__(self):
        """Initialize export service."""
        pass

    def export_prd(
        self,
        artifacts: List[Dict[str, Any]],
        format: str = "markdown",
        include_citations: bool = True
    ) -> str:
        """
        Export Product Requirements Document.

        Args:
            artifacts: List of artifacts to document
            format: Export format (markdown, pdf, json)
            include_citations: Whether to include code citations

        Returns:
            Exported document content
        """
        logger.info(f"Exporting PRD: {len(artifacts)} artifacts, format={format}")

        if format == "markdown":
            return self._export_prd_markdown(artifacts, include_citations)
        elif format == "json":
            return self._export_prd_json(artifacts)
        elif format == "pdf":
            # Would use ReportLab for PDF generation
            return self._export_prd_pdf(artifacts, include_citations)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _export_prd_markdown(
        self,
        artifacts: List[Dict[str, Any]],
        include_citations: bool
    ) -> str:
        """Export PRD as Markdown."""
        doc = []

        # Header
        doc.append("# Product Requirements Document")
        doc.append("")
        doc.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        doc.append("")
        doc.append("---")
        doc.append("")

        # Overview
        doc.append("## 1. Overview")
        doc.append("")
        doc.append(f"This document covers {len(artifacts)} artifacts from the codebase analysis.")
        doc.append("")

        # Objectives
        doc.append("## 2. Objectives")
        doc.append("")
        doc.append("- Document existing system functionality")
        doc.append("- Identify key components and their interactions")
        doc.append("- Provide technical reference for development team")
        doc.append("")

        # Artifacts by Type
        doc.append("## 3. System Components")
        doc.append("")

        # Group artifacts by type
        by_type = {}
        for artifact in artifacts:
            art_type = artifact.get("artifact_type", "Unknown")
            if art_type not in by_type:
                by_type[art_type] = []
            by_type[art_type].append(artifact)

        for art_type, arts in sorted(by_type.items()):
            doc.append(f"### 3.{len(doc)} {art_type}")
            doc.append("")
            doc.append(f"**Count**: {len(arts)} artifacts")
            doc.append("")

            # List artifacts
            for artifact in arts[:10]:  # Limit to 10 per type
                file_path = artifact.get("file_path", "")
                preview = artifact.get("preview", "")

                doc.append(f"#### {Path(file_path).name}")
                doc.append("")
                doc.append(f"**File**: `{file_path}`")
                doc.append("")

                if preview:
                    doc.append(f"**Description**: {preview[:200]}...")
                    doc.append("")

                if include_citations:
                    doc.append(f"*Source: {file_path}*")
                    doc.append("")

            if len(arts) > 10:
                doc.append(f"*... and {len(arts) - 10} more {art_type} artifacts*")
                doc.append("")

        # Footer
        doc.append("---")
        doc.append("")
        doc.append("## 4. Next Steps")
        doc.append("")
        doc.append("- Review artifact documentation")
        doc.append("- Identify gaps or missing components")
        doc.append("- Plan refactoring or improvements")
        doc.append("")

        return "\n".join(doc)

    def _export_prd_json(self, artifacts: List[Dict[str, Any]]) -> str:
        """Export PRD as JSON."""
        doc = {
            "title": "Product Requirements Document",
            "generated_at": datetime.now().isoformat(),
            "artifact_count": len(artifacts),
            "artifacts_by_type": {},
            "artifacts": artifacts
        }

        # Group by type
        for artifact in artifacts:
            art_type = artifact.get("artifact_type", "Unknown")
            if art_type not in doc["artifacts_by_type"]:
                doc["artifacts_by_type"][art_type] = 0
            doc["artifacts_by_type"][art_type] += 1

        return json.dumps(doc, indent=2)

    def _export_prd_pdf(
        self,
        artifacts: List[Dict[str, Any]],
        include_citations: bool
    ) -> str:
        """Export PRD as PDF (placeholder)."""
        # TODO: Implement PDF generation using ReportLab
        logger.warning("PDF export not yet implemented")

        # Return markdown as placeholder
        return self._export_prd_markdown(artifacts, include_citations)

    def export_spec(
        self,
        title: str,
        sections: Dict[str, str],
        format: str = "markdown"
    ) -> str:
        """
        Export Technical Specification.

        Args:
            title: Spec title
            sections: Dictionary of section name to content
            format: Export format

        Returns:
            Exported specification content
        """
        logger.info(f"Exporting spec: {title}, format={format}")

        if format == "markdown":
            return self._export_spec_markdown(title, sections)
        elif format == "json":
            return self._export_spec_json(title, sections)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _export_spec_markdown(
        self,
        title: str,
        sections: Dict[str, str]
    ) -> str:
        """Export spec as Markdown."""
        doc = []

        # Header
        doc.append(f"# {title}")
        doc.append("")
        doc.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        doc.append("")
        doc.append("---")
        doc.append("")

        # Sections
        for i, (section_name, content) in enumerate(sections.items(), 1):
            doc.append(f"## {i}. {section_name}")
            doc.append("")
            doc.append(content)
            doc.append("")

        return "\n".join(doc)

    def _export_spec_json(
        self,
        title: str,
        sections: Dict[str, str]
    ) -> str:
        """Export spec as JSON."""
        doc = {
            "title": title,
            "generated_at": datetime.now().isoformat(),
            "sections": sections
        }

        return json.dumps(doc, indent=2)

    def export_test_report(
        self,
        tests: List[Dict[str, Any]],
        format: str = "markdown"
    ) -> str:
        """
        Export test report.

        Args:
            tests: List of test cases
            format: Export format

        Returns:
            Exported test report content
        """
        logger.info(f"Exporting test report: {len(tests)} tests, format={format}")

        if format == "markdown":
            return self._export_test_report_markdown(tests)
        elif format == "json":
            return json.dumps({"tests": tests}, indent=2)
        elif format == "csv":
            return self._export_test_report_csv(tests)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _export_test_report_markdown(self, tests: List[Dict[str, Any]]) -> str:
        """Export test report as Markdown."""
        doc = []

        # Header
        doc.append("# Test Report")
        doc.append("")
        doc.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        doc.append("")
        doc.append(f"**Total Tests**: {len(tests)}")
        doc.append("")
        doc.append("---")
        doc.append("")

        # Tests
        for i, test in enumerate(tests, 1):
            test_type = test.get("type", "unknown")
            description = test.get("description", "")
            content = test.get("content", "")

            doc.append(f"## Test {i}: {test_type.upper()}")
            doc.append("")
            doc.append(f"**Description**: {description}")
            doc.append("")
            doc.append("```")
            doc.append(content)
            doc.append("```")
            doc.append("")

        return "\n".join(doc)

    def _export_test_report_csv(self, tests: List[Dict[str, Any]]) -> str:
        """Export test report as CSV."""
        lines = []

        # Header
        lines.append("ID,Type,Description,Generated At")

        # Tests
        for i, test in enumerate(tests, 1):
            test_type = test.get("type", "unknown")
            description = test.get("description", "").replace(",", ";")
            timestamp = test.get("timestamp", "")

            lines.append(f"{i},{test_type},{description},{timestamp}")

        return "\n".join(lines)

    def export_chat_history(
        self,
        messages: List[Dict[str, Any]],
        format: str = "markdown"
    ) -> str:
        """
        Export chat history.

        Args:
            messages: List of chat messages
            format: Export format

        Returns:
            Exported chat history
        """
        logger.info(f"Exporting chat history: {len(messages)} messages, format={format}")

        if format == "markdown":
            return self._export_chat_markdown(messages)
        elif format == "json":
            return json.dumps({"messages": messages}, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _export_chat_markdown(self, messages: List[Dict[str, Any]]) -> str:
        """Export chat history as Markdown."""
        doc = []

        # Header
        doc.append("# Chat History")
        doc.append("")
        doc.append(f"*Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        doc.append("")
        doc.append("---")
        doc.append("")

        # Messages
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")

            if role == "user":
                doc.append("## 👤 User")
                doc.append("")
                doc.append(content)
                doc.append("")

            elif role == "assistant":
                agent_role = message.get("agent_role", "Assistant")
                confidence = message.get("confidence", 0.0)
                citations = message.get("citations", [])

                doc.append(f"## 🤖 {agent_role}")
                doc.append("")
                doc.append(f"*Confidence: {confidence * 100:.0f}%*")
                doc.append("")
                doc.append(content)
                doc.append("")

                if citations:
                    doc.append("**Citations:**")
                    doc.append("")
                    for i, citation in enumerate(citations, 1):
                        file_path = citation.get("file_path", "")
                        doc.append(f"{i}. `{file_path}`")
                    doc.append("")

            doc.append("---")
            doc.append("")

        return "\n".join(doc)


# Global service instance
_export_service: Optional[ExportService] = None


def get_export_service() -> ExportService:
    """
    Get global export service instance.

    Returns:
        ExportService singleton
    """
    global _export_service

    if _export_service is None:
        _export_service = ExportService()
        logger.info("Initialized export service")

    return _export_service


__all__ = [
    "ExportService",
    "get_export_service"
]
