"""
Database quality analyzer for schema validation and recommendations.

Analyzes database schemas for quality issues including missing foreign keys,
missing indexes, naming convention violations, and generates improvement recommendations.
"""

import logging
import re
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class DbQualityAnalyzer:
    """
    Analyzer for database schema quality and best practices.

    Features:
    - Detect missing foreign key relationships
    - Identify missing indexes on FK columns
    - Validate naming conventions (snake_case)
    - Check for missing primary keys
    - Generate quality score and recommendations
    """

    def analyze_schema(self, tables: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze database schema for quality issues.

        Args:
            tables: List of database table artifacts

        Returns:
            Quality report dictionary with issues and recommendations
        """
        logger.info(f"Analyzing schema quality for {len(tables)} tables")

        report = {
            "total_tables": len(tables),
            "missing_foreign_keys": [],
            "missing_indexes": [],
            "naming_issues": [],
            "missing_primary_keys": [],
            "redundant_indexes": [],
            "recommendations": [],
            "issues": [],
            "quality_score": 100.0
        }

        if not tables:
            return report

        # Analyze each table
        for table in tables:
            table_name = self._get_table_name(table)

            # Check naming convention
            if not self._check_naming_convention(table_name):
                issue = f"Table '{table_name}' does not follow snake_case convention"
                report["naming_issues"].append(issue)
                report["quality_score"] -= 5

            # Check for primary key
            if not self._has_primary_key(table):
                issue = f"Table '{table_name}' is missing a primary key"
                report["missing_primary_keys"].append(issue)
                report["quality_score"] -= 10
                report["issues"].append({
                    "severity": "HIGH",
                    "table": table_name,
                    "issue": "Missing primary key"
                })

            # Find potential foreign keys
            potential_fks = self._find_potential_foreign_keys(table)
            for fk in potential_fks:
                issue = f"Column '{fk['column']}' in table '{table_name}' appears to be a foreign key but is not declared"
                report["missing_foreign_keys"].append(issue)
                report["quality_score"] -= 3
                report["issues"].append({
                    "severity": "MEDIUM",
                    "table": table_name,
                    "column": fk["column"],
                    "issue": "Potential undeclared foreign key"
                })

            # Find missing indexes
            index_candidates = self._find_index_candidates(table)
            for candidate in index_candidates:
                issue = f"Column '{candidate}' in table '{table_name}' should be indexed (foreign key or frequently queried)"
                report["missing_indexes"].append(issue)
                report["quality_score"] -= 2

            # Check for redundant indexes (optional advanced feature)
            redundant = self._find_redundant_indexes(table)
            if redundant:
                report["redundant_indexes"].extend(redundant)

        # Ensure quality score doesn't go below 0
        report["quality_score"] = max(0, report["quality_score"])

        # Generate recommendations
        report["recommendations"] = self._generate_recommendations(report)

        logger.info(f"Schema quality score: {report['quality_score']:.1f}/100")
        logger.info(f"Issues found: {len(report['issues'])}")

        return report

    def _get_table_name(self, table: Dict[str, Any]) -> str:
        """Extract table name from artifact."""
        if "metadata" in table and "table_name" in table["metadata"]:
            return table["metadata"]["table_name"]

        if "entities" in table and len(table["entities"]) > 0:
            return table["entities"][0]

        filename = table.get("fileName", "unknown")
        return filename.replace(".sql", "").replace(".SQL", "")

    def _check_naming_convention(self, name: str) -> bool:
        """
        Check if name follows snake_case convention.

        Args:
            name: Table or column name

        Returns:
            True if valid snake_case, False otherwise
        """
        # Valid snake_case: lowercase letters, numbers, underscores
        # Must start with letter
        pattern = r'^[a-z][a-z0-9_]*$'
        return bool(re.match(pattern, name))

    def _has_primary_key(self, table: Dict[str, Any]) -> bool:
        """Check if table has a primary key defined."""
        # Check metadata
        if "metadata" in table:
            metadata = table["metadata"]

            # Check primary_key field
            if metadata.get("primary_key"):
                return True

            # Check columns for primary_key flag
            if "columns" in metadata:
                for col in metadata["columns"]:
                    if col.get("primary_key"):
                        return True

        return False

    def _find_potential_foreign_keys(self, table: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Find columns that appear to be foreign keys but aren't declared.

        Args:
            table: Table artifact

        Returns:
            List of potential FK columns
        """
        potential_fks = []

        if "metadata" not in table or "columns" not in table["metadata"]:
            return potential_fks

        columns = table["metadata"]["columns"]
        declared_fks = set()

        # Get list of declared foreign keys
        if "foreign_keys" in table.get("metadata", {}):
            for fk in table["metadata"]["foreign_keys"]:
                declared_fks.add(fk.get("column", ""))

        # Check for columns ending in _id that aren't declared as FKs
        for col in columns:
            col_name = col.get("name", "")

            # Skip if it's a primary key
            if col.get("primary_key"):
                continue

            # Skip if already marked as FK
            if col.get("foreign_key") or col_name in declared_fks:
                continue

            # Check naming pattern: ends with _id (but not just "id")
            if col_name.endswith("_id") and col_name != "id":
                # Infer referenced table
                ref_table = col_name[:-3]  # Remove _id suffix
                potential_fks.append({
                    "column": col_name,
                    "potential_reference": ref_table
                })

        return potential_fks

    def _find_index_candidates(self, table: Dict[str, Any]) -> List[str]:
        """
        Find columns that should be indexed.

        Args:
            table: Table artifact

        Returns:
            List of column names that should be indexed
        """
        candidates = []

        if "metadata" not in table:
            return candidates

        metadata = table["metadata"]
        columns = metadata.get("columns", [])
        existing_indexes = set()

        # Get list of already indexed columns
        if "indexes" in metadata:
            for idx in metadata["indexes"]:
                existing_indexes.add(idx.get("column", ""))

        # Foreign key columns should be indexed
        if "foreign_keys" in metadata:
            for fk in metadata["foreign_keys"]:
                fk_col = fk.get("column", "")
                if fk_col and fk_col not in existing_indexes:
                    candidates.append(fk_col)

        # Columns marked as foreign_key but not indexed
        for col in columns:
            col_name = col.get("name", "")

            # Skip if already in candidates or indexed
            if col_name in candidates or col_name in existing_indexes:
                continue

            # Check if it's a declared FK
            if col.get("foreign_key"):
                candidates.append(col_name)
                continue

            # Check if it looks like a FK (ends with _id but is not primary key)
            if col_name.endswith("_id") and col_name != "id" and not col.get("primary_key"):
                candidates.append(col_name)

        return candidates

    def _find_redundant_indexes(self, table: Dict[str, Any]) -> List[str]:
        """
        Find redundant or duplicate indexes (advanced feature).

        Args:
            table: Table artifact

        Returns:
            List of redundant index descriptions
        """
        redundant = []

        if "metadata" not in table or "indexes" not in table["metadata"]:
            return redundant

        indexes = table["metadata"]["indexes"]
        seen_columns = {}

        for idx in indexes:
            col = idx.get("column", "")
            idx_type = idx.get("type", "INDEX")

            if col in seen_columns:
                # Potential redundancy
                prev_type = seen_columns[col]
                if idx_type == prev_type:
                    redundant.append(f"Duplicate index on column '{col}'")
                elif idx_type == "INDEX" and prev_type == "UNIQUE":
                    redundant.append(f"Redundant INDEX on '{col}' (already has UNIQUE)")

            seen_columns[col] = idx_type

        return redundant

    def _generate_recommendations(self, report: Dict[str, Any]) -> List[str]:
        """
        Generate actionable recommendations based on issues found.

        Args:
            report: Quality report with identified issues

        Returns:
            List of recommendation strings
        """
        recommendations = []

        # Primary key recommendations
        if report["missing_primary_keys"]:
            recommendations.append(
                f"Add primary keys to {len(report['missing_primary_keys'])} table(s) to ensure unique row identification"
            )

        # Foreign key recommendations
        if report["missing_foreign_keys"]:
            count = len(report["missing_foreign_keys"])
            recommendations.append(
                f"Declare {count} foreign key relationship(s) to enforce referential integrity"
            )

        # Index recommendations
        if report["missing_indexes"]:
            count = len(report["missing_indexes"])
            recommendations.append(
                f"Add indexes to {count} foreign key column(s) to improve join performance"
            )

        # Naming recommendations
        if report["naming_issues"]:
            recommendations.append(
                "Rename tables to follow snake_case convention for consistency"
            )

        # Redundant index recommendations
        if report["redundant_indexes"]:
            recommendations.append(
                f"Remove {len(report['redundant_indexes'])} redundant index(es) to reduce storage overhead"
            )

        # Quality score recommendations
        if report["quality_score"] < 50:
            recommendations.append(
                "Schema quality is low. Prioritize fixing HIGH severity issues first."
            )
        elif report["quality_score"] < 80:
            recommendations.append(
                "Schema quality is moderate. Address MEDIUM severity issues to improve reliability."
            )
        else:
            recommendations.append(
                "Schema quality is good. Consider addressing remaining minor issues."
            )

        return recommendations

    def format_report_markdown(self, report: Dict[str, Any]) -> str:
        """
        Format quality report as Markdown for Streamlit display.

        Args:
            report: Quality report dictionary

        Returns:
            Markdown-formatted report string
        """
        lines = []

        # Header
        lines.append("## Database Quality Report")
        lines.append("")

        # Summary
        quality_score = report.get("quality_score", 0)
        total_tables = report.get("total_tables", 0)

        score_emoji = "🟢" if quality_score >= 80 else "🟡" if quality_score >= 50 else "🔴"
        lines.append(f"**Overall Quality Score:** {score_emoji} {quality_score:.1f}/100")
        lines.append(f"**Total Tables:** {total_tables}")
        lines.append("")

        # Issues summary
        total_issues = len(report.get("issues", []))
        if total_issues > 0:
            lines.append(f"**Issues Found:** {total_issues}")
            lines.append("")

        # Missing primary keys
        missing_pks = report.get("missing_primary_keys", [])
        if missing_pks:
            lines.append("### ❌ Missing Primary Keys")
            for issue in missing_pks[:5]:  # Limit to 5
                lines.append(f"- {issue}")
            if len(missing_pks) > 5:
                lines.append(f"- *... and {len(missing_pks) - 5} more*")
            lines.append("")

        # Missing foreign keys
        missing_fks = report.get("missing_foreign_keys", [])
        if missing_fks:
            lines.append("### ⚠️ Potential Missing Foreign Keys")
            for issue in missing_fks[:10]:  # Limit to 10
                lines.append(f"- {issue}")
            if len(missing_fks) > 10:
                lines.append(f"- *... and {len(missing_fks) - 10} more*")
            lines.append("")

        # Missing indexes
        missing_indexes = report.get("missing_indexes", [])
        if missing_indexes:
            lines.append("### 📊 Recommended Indexes")
            for issue in missing_indexes[:10]:
                lines.append(f"- {issue}")
            if len(missing_indexes) > 10:
                lines.append(f"- *... and {len(missing_indexes) - 10} more*")
            lines.append("")

        # Naming issues
        naming_issues = report.get("naming_issues", [])
        if naming_issues:
            lines.append("### 📝 Naming Convention Issues")
            for issue in naming_issues[:5]:
                lines.append(f"- {issue}")
            if len(naming_issues) > 5:
                lines.append(f"- *... and {len(naming_issues) - 5} more*")
            lines.append("")

        # Recommendations
        recommendations = report.get("recommendations", [])
        if recommendations:
            lines.append("### 💡 Recommendations")
            for rec in recommendations:
                lines.append(f"- {rec}")
            lines.append("")

        return "\n".join(lines)


# Global singleton instance
_db_quality_analyzer: Optional[DbQualityAnalyzer] = None


def get_db_quality_analyzer() -> DbQualityAnalyzer:
    """
    Get global database quality analyzer instance.

    Returns:
        DbQualityAnalyzer singleton
    """
    global _db_quality_analyzer

    if _db_quality_analyzer is None:
        _db_quality_analyzer = DbQualityAnalyzer()
        logger.info("Initialized database quality analyzer")

    return _db_quality_analyzer


__all__ = [
    "DbQualityAnalyzer",
    "get_db_quality_analyzer"
]
