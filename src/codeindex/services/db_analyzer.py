"""
Database Analyzer Service for PRD Generation.

Analyzes DAO classes, JPA entities, iBATIS/MyBatis mapper XML, and SQL files
to extract database entity definitions and business rules.
"""
import logging
import hashlib
import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Set
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

from codeindex.models.prd import (
    DatabaseEntity,
    BusinessRule,
    Column,
    ForeignKey,
    Index,
    Constraint,
    FileVisitEntry,
    SourceType,
    RuleLayer,
    RuleScope,
    RuleType,
    AnalysisLayer,
    VisitStatus,
)
from codeindex.models.foreign_key import ForeignKeyRelationship, ForeignKeySource
from codeindex.services.ollama_client import OllamaClient
from codeindex.parsers.sql_parser import SQLParser
from codeindex.utils.retry import retry
from codeindex.utils.metrics import get_metrics_collector
from codeindex.models.metrics import ForeignKeyMetric

logger = logging.getLogger(__name__)


# ==============================================================================
# FK Validation Result
# ==============================================================================

@dataclass
class FKValidationResult:
    """Result of FK column validation"""
    fk: ForeignKeyRelationship
    is_valid: bool
    error_message: Optional[str] = None


# ==============================================================================
# DAO Entity Extraction Prompt
# ==============================================================================

DAO_EXTRACTION_PROMPT_TEMPLATE = """You are analyzing a Java DAO (Data Access Object) or JPA entity class to extract database structure information.

FILE: {file_path}
FRAMEWORK: {framework}

SOURCE CODE:
```java
{source_code}
```

RELATED ENTITIES (from Weaviate):
{related_entities_summary}

TASK:
Extract the following information in JSON format:

1. **entity_name**: The database table name (inferred from @Table annotation, class name, or naming conventions)
2. **columns**: List of columns with name, data_type, nullable, description
3. **primary_key**: List of primary key column names
4. **foreign_keys**: List of foreign key relationships with referenced_table and referenced_column
5. **indexes**: List of indexes if declared
6. **constraints**: List of constraints (CHECK, UNIQUE, etc.) if any
7. **business_rules**: List of validation or business rules enforced at this level
8. **description**: A natural language description (2-3 sentences) of what this entity represents and its purpose in the system

RESPONSE FORMAT (JSON):
{{
  "entity_name": "string",
  "qualified_name": "schema.table or null",
  "columns": [
    {{
      "name": "string",
      "data_type": "string (e.g., VARCHAR(255), INTEGER, TIMESTAMP)",
      "nullable": boolean,
      "default_value": "string or null",
      "description": "string"
    }}
  ],
  "primary_key": ["column_name"],
  "foreign_keys": [
    {{
      "column_name": "string",
      "referenced_table": "string",
      "referenced_column": "string",
      "on_delete": "string or null",
      "on_update": "string or null"
    }}
  ],
  "indexes": [
    {{
      "name": "string",
      "columns": ["string"],
      "unique": boolean,
      "index_type": "string or null"
    }}
  ],
  "constraints": [
    {{
      "name": "string",
      "type": "CHECK | UNIQUE | NOT NULL",
      "definition": "string"
    }}
  ],
  "business_rules": [
    {{
      "name": "string",
      "description": "string",
      "enforcement": "string (how it's enforced)"
    }}
  ],
  "description": "string (2-3 sentence description)",
  "estimated_row_count": "small | medium | large | massive or null",
  "domain": "string (business domain like auth, billing, reporting) or null"
}}

IMPORTANT:
- Infer data types from JPA annotations (@Column(length=255) → VARCHAR(255), @Temporal → TIMESTAMP, etc.)
- For iBATIS/MyBatis, extract from result maps and SQL statements
- If information is not available, use null
- Be specific in descriptions, avoid generic statements
- Include any validation annotations as business_rules"""


# ==============================================================================
# Database Analyzer Service
# ==============================================================================

class DatabaseAnalyzer:
    """
    Analyzes database layer of a codebase.

    Scans DAO classes, JPA entities, iBATIS/MyBatis XML, and SQL files to
    extract database entities and business rules using LLM analysis.
    """

    def __init__(
        self,
        ollama_client: OllamaClient,
        output_dir: Path,
        source_dir: Path,
        max_workers: int = 10,
        llm_timeout: int = 120,
        max_retries: int = 3,
        force_refresh: bool = False
    ):
        """
        Initialize database analyzer.

        Args:
            ollama_client: Ollama client for LLM analysis
            output_dir: Output directory for generated files
            source_dir: Source code root directory
            max_workers: Maximum parallel LLM calls
            llm_timeout: LLM call timeout in seconds
            max_retries: Maximum retry attempts for LLM calls
            force_refresh: Re-analyze all files ignoring visit log
        """
        self.ollama_client = ollama_client
        self.output_dir = Path(output_dir)
        self.source_dir = Path(source_dir)
        self.max_workers = max_workers
        self.llm_timeout = llm_timeout
        self.max_retries = max_retries
        self.force_refresh = force_refresh

        # Create output directories
        self.db_entities_dir = self.output_dir / "database" / "entities"
        self.business_rules_dir = self.output_dir / "business_rules"
        self.visit_log_file = self.output_dir / ".visit_log.jsonl"

        self.db_entities_dir.mkdir(parents=True, exist_ok=True)
        self.business_rules_dir.mkdir(parents=True, exist_ok=True)

        # Load visit log
        self.visit_log: Dict[str, FileVisitEntry] = self._load_visit_log()

        # Tracking
        self.extracted_entities: List[DatabaseEntity] = []
        self.extracted_rules: List[BusinessRule] = []

        self.logger = logging.getLogger(__name__)

    def _load_visit_log(self) -> Dict[str, FileVisitEntry]:
        """
        Load visit log from JSON Lines file.

        Returns:
            Dict mapping file_path to FileVisitEntry (latest entry wins)
        """
        visit_log = {}

        if not self.visit_log_file.exists():
            return visit_log

        try:
            with open(self.visit_log_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        entry_data = json.loads(line)
                        entry = FileVisitEntry.from_dict(entry_data)
                        visit_log[entry.file_path] = entry  # Latest wins
                    except (json.JSONDecodeError, ValueError) as e:
                        self.logger.warning(f"Invalid visit log entry: {e}")
                        continue

        except Exception as e:
            self.logger.warning(f"Failed to load visit log: {e}")

        return visit_log

    def _append_visit_log(self, entry: FileVisitEntry):
        """
        Append entry to visit log (JSON Lines format).

        Args:
            entry: FileVisitEntry to append
        """
        try:
            with open(self.visit_log_file, "a", encoding="utf-8") as f:
                json.dump(entry.to_dict(), f)
                f.write("\n")

            # Update in-memory log
            self.visit_log[entry.file_path] = entry

        except Exception as e:
            self.logger.error(f"Failed to append visit log entry: {e}")

    def _compute_file_hash(self, file_path: Path) -> str:
        """
        Compute SHA-256 hash of file contents.

        Args:
            file_path: Path to file

        Returns:
            Hex string of SHA-256 hash (64 chars)
        """
        sha256 = hashlib.sha256()

        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)

        return sha256.hexdigest()

    def _should_analyze_file(self, file_path: Path) -> bool:
        """
        Check if file should be analyzed based on visit log.

        Args:
            file_path: Path to file

        Returns:
            True if file should be analyzed, False if can skip
        """
        if self.force_refresh:
            return True

        file_path_str = str(file_path)

        # Not in visit log yet - analyze
        if file_path_str not in self.visit_log:
            return True

        entry = self.visit_log[file_path_str]

        # Failed before - retry
        if entry.status == VisitStatus.FAILED:
            return True

        # In progress (interrupted) - retry
        if entry.status == VisitStatus.IN_PROGRESS:
            return True

        # Skipped - don't analyze
        if entry.status == VisitStatus.SKIPPED:
            return False

        # Success - check if content changed
        if entry.status == VisitStatus.SUCCESS:
            try:
                current_hash = self._compute_file_hash(file_path)
                if current_hash != entry.content_hash:
                    self.logger.info(f"File changed: {file_path.name}")
                    return True  # Content changed - re-analyze
                else:
                    self.logger.debug(f"Skipping unchanged file: {file_path.name}")
                    return False  # Unchanged - skip
            except Exception as e:
                self.logger.warning(f"Cannot compute hash for {file_path}: {e}")
                return True  # Error computing hash - re-analyze to be safe

        return True

    def _detect_framework(self, file_content: str) -> str:
        """
        Detect ORM framework from file content.

        Args:
            file_content: File content

        Returns:
            Framework name (JPA, iBATIS, Hibernate, SQL, etc.)
        """
        if "@Entity" in file_content or "@Table" in file_content:
            return "JPA"
        elif "mybatis" in file_content.lower() or "ibatis" in file_content.lower() or "<mapper" in file_content:
            return "iBATIS/MyBatis"
        elif "hibernate.hbm" in file_content.lower():
            return "Hibernate"
        elif file_content.strip().upper().startswith("CREATE TABLE"):
            return "SQL DDL"
        else:
            return "Unknown"

    def find_dao_files(self) -> List[Path]:
        """
        Find all DAO, entity, and database-related files.

        Returns:
            List of file paths to analyze
        """
        dao_files = []

        # Patterns to match
        patterns = [
            "**/*DAO.java",
            "**/*Dao.java",
            "**/*Entity.java",
            "**/*Mapper.xml",
            "**/*mapper.xml",
            "**/*.hbm.xml",
            "**/schema.sql",
            "**/ddl/*.sql",
        ]

        for pattern in patterns:
            for file_path in self.source_dir.glob(pattern):
                if file_path.is_file():
                    dao_files.append(file_path)

        self.logger.info(f"Found {len(dao_files)} database-related files")
        return dao_files

    @retry(max_attempts=3, base_delay=1.0, exponential_base=2.0)
    def _extract_entity_with_llm(
        self,
        file_path: Path,
        file_content: str,
        framework: str,
        related_entities: str = ""
    ) -> Optional[Dict[str, Any]]:
        """
        Extract database entity using LLM.

        Args:
            file_path: Path to file
            file_content: File content
            framework: Detected framework
            related_entities: Related entities summary from Weaviate

        Returns:
            Extracted entity data as dict, or None on failure

        Raises:
            TimeoutError: On LLM timeout
            ValueError: On invalid response
        """
        # Reduce source code size for better LLM comprehension
        max_source_chars = 10000  # Reduced from 15000
        truncated_source = file_content[:max_source_chars]
        if len(file_content) > max_source_chars:
            truncated_source += f"\n\n... [truncated {len(file_content) - max_source_chars} chars]"

        prompt = DAO_EXTRACTION_PROMPT_TEMPLATE.format(
            file_path=str(file_path),
            framework=framework,
            source_code=truncated_source,
            related_entities_summary=related_entities or "None"
        )

        try:
            # Call Ollama with JSON mode
            response = self.ollama_client.call_ollama(
                prompt=prompt,
                temperature=0.2,
                format_json=True
            )

            # Parse JSON response with cleaning
            response_text = response["response"]
            cleaned_text = self.ollama_client._clean_json_response(response_text)

            try:
                extracted = json.loads(cleaned_text)
            except json.JSONDecodeError as e:
                # Log error with file context and response preview
                response_preview = cleaned_text[:1000] if len(cleaned_text) > 1000 else cleaned_text
                self.logger.error(
                    f"Failed to parse LLM JSON for {file_path.name}: {e}\n"
                    f"Response preview (first 1000 chars): {response_preview}"
                )

                # Dump full details to separate error log file for debugging
                error_log_path = self.output_dir / ".error_logs" / f"{file_path.stem}_parse_error.txt"
                error_log_path.parent.mkdir(exist_ok=True)
                with open(error_log_path, "w", encoding="utf-8") as f:
                    f.write(f"=== PARSE ERROR for {file_path.name} ===\n")
                    f.write(f"Error: {e}\n\n")
                    f.write(f"=== PROMPT (first 2000 chars) ===\n")
                    f.write(prompt[:2000] + "...\n\n")
                    f.write(f"=== FULL RESPONSE ===\n")
                    f.write(cleaned_text)
                self.logger.info(f"Full error details saved to: {error_log_path}")

                raise ValueError(f"Invalid JSON from LLM: {e}")

            # Validate and fix missing required fields with resilient defaults
            is_incomplete = False

            if "entity_name" not in extracted or not extracted.get("entity_name"):
                self.logger.warning(f"Missing entity_name in response for {file_path.name}, using filename")
                # Use filename as fallback entity name
                extracted["entity_name"] = file_path.stem.replace("DAO", "").replace("Dao", "")
                is_incomplete = True

            if "columns" not in extracted or not extracted.get("columns"):
                self.logger.warning(f"Missing or empty columns in response for {file_path.name}")

                # Dump full details to error log for missing columns
                error_log_path = self.output_dir / ".error_logs" / f"{file_path.stem}_missing_columns.txt"
                error_log_path.parent.mkdir(exist_ok=True)
                with open(error_log_path, "w", encoding="utf-8") as f:
                    f.write(f"=== MISSING COLUMNS for {file_path.name} ===\n")
                    f.write(f"Entity name: {extracted.get('entity_name', 'UNKNOWN')}\n\n")
                    f.write(f"=== PROMPT (first 2000 chars) ===\n")
                    f.write(prompt[:2000] + "...\n\n")
                    f.write(f"=== FULL RESPONSE ===\n")
                    f.write(json.dumps(extracted, indent=2))
                self.logger.info(f"Full error details saved to: {error_log_path}")

                # Create minimal column entry as fallback
                extracted["columns"] = [
                    {
                        "name": "id",
                        "data_type": "BIGINT",
                        "nullable": False,
                        "default_value": None,
                        "description": f"Primary key for {extracted.get('entity_name', 'entity')} (auto-detected fallback)"
                    }
                ]
                is_incomplete = True

            if "description" not in extracted or not extracted.get("description"):
                self.logger.warning(f"Missing description in response for {file_path.name}, using generic")
                extracted["description"] = f"Database entity extracted from {file_path.name}"
                is_incomplete = True

            # Fill in optional fields with defaults if missing
            if "primary_key" not in extracted:
                extracted["primary_key"] = []
            if "foreign_keys" not in extracted:
                extracted["foreign_keys"] = []
            if "indexes" not in extracted:
                extracted["indexes"] = []
            if "constraints" not in extracted:
                extracted["constraints"] = []
            if "business_rules" not in extracted:
                extracted["business_rules"] = []

            # Log success with INFO level (was DEBUG)
            status = "⚠ Partially extracted" if is_incomplete else "✓ Extracted entity"
            self.logger.info(f"{status}: {extracted.get('entity_name')}")
            return extracted

        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse LLM JSON response: {e}")
            raise ValueError(f"Invalid JSON from LLM: {e}")

        except Exception as e:
            self.logger.error(f"LLM extraction failed: {e}")
            raise

    def _create_database_entity(
        self,
        extracted: Dict[str, Any],
        source_file: Path,
        source_type: SourceType
    ) -> DatabaseEntity:
        """
        Create DatabaseEntity from LLM extraction.

        Args:
            extracted: LLM-extracted data
            source_file: Source file path
            source_type: Source type

        Returns:
            DatabaseEntity instance
        """
        # Create columns
        columns = [
            Column(
                name=col["name"],
                data_type=col["data_type"],
                nullable=col.get("nullable", True),
                default_value=col.get("default_value"),
                description=col.get("description")
            )
            for col in extracted.get("columns", [])
        ]

        # Create foreign keys
        foreign_keys = [
            ForeignKey(
                column_name=fk["column_name"],
                referenced_table=fk["referenced_table"],
                referenced_column=fk["referenced_column"],
                on_delete=fk.get("on_delete"),
                on_update=fk.get("on_update")
            )
            for fk in extracted.get("foreign_keys", [])
        ]

        # Create indexes
        indexes = [
            Index(
                name=idx["name"],
                columns=idx["columns"],
                unique=idx.get("unique", False),
                index_type=idx.get("index_type")
            )
            for idx in extracted.get("indexes", [])
        ]

        # Create constraints
        constraints = [
            Constraint(
                name=cons["name"],
                type=cons["type"],
                definition=cons["definition"]
            )
            for cons in extracted.get("constraints", [])
        ]

        # Create entity
        entity = DatabaseEntity(
            id=extracted["entity_name"],
            name=extracted["entity_name"],
            qualified_name=extracted.get("qualified_name"),
            source_type=source_type,
            source_files=[str(source_file)],
            columns=columns,
            primary_key=extracted.get("primary_key", []),
            foreign_keys=foreign_keys,
            indexes=indexes,
            constraints=constraints,
            business_rules=[],  # Will be populated from business rules
            description=extracted.get("description"),
            estimated_row_count=extracted.get("estimated_row_count"),
            domain=extracted.get("domain"),
            created_at=datetime.now()
        )

        return entity

    def _create_business_rules(
        self,
        extracted: Dict[str, Any],
        source_file: Path,
        entity_id: str
    ) -> List[BusinessRule]:
        """
        Create BusinessRule instances from LLM extraction.

        Args:
            extracted: LLM-extracted data
            source_file: Source file path
            entity_id: Database entity ID

        Returns:
            List of BusinessRule instances
        """
        rules = []

        for rule_data in extracted.get("business_rules", []):
            rule_id = f"BR_DB_{entity_id}_{len(rules) + 1}"

            rule = BusinessRule(
                id=rule_id,
                name=rule_data["name"],
                layer=RuleLayer.DATABASE,
                scope=RuleScope.ENTITY,  # Default for database rules
                rule_type=RuleType.VALIDATION,  # Default
                description=rule_data["description"],
                source_files=[str(source_file)],
                related_entities=[entity_id],
                enforcement_mechanism=rule_data.get("enforcement"),
                domain=extracted.get("domain"),
                created_at=datetime.now()
            )

            rules.append(rule)

        return rules

    def analyze_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Analyze a single DAO/entity file.

        Args:
            file_path: Path to file

        Returns:
            Analysis result dict with entity and rules, or None on skip/failure
        """
        start_time = datetime.now()

        # Check if should analyze
        if not self._should_analyze_file(file_path):
            return None

        self.logger.info(f"Analyzing: {file_path.name}")

        # Compute content hash
        try:
            content_hash = self._compute_file_hash(file_path)
        except Exception as e:
            self.logger.error(f"Cannot read file {file_path}: {e}")
            return None

        # Mark as in progress
        in_progress_entry = FileVisitEntry(
            file_path=str(file_path),
            timestamp=datetime.now(),
            status=VisitStatus.IN_PROGRESS,
            content_hash=content_hash,
            layer=AnalysisLayer.DATABASE,
            analysis_type="dao_extraction"
        )
        self._append_visit_log(in_progress_entry)

        # Read file content
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                file_content = f.read()
        except Exception as e:
            self.logger.error(f"Cannot read file {file_path}: {e}")

            # Mark as failed
            failed_entry = FileVisitEntry(
                file_path=str(file_path),
                timestamp=datetime.now(),
                status=VisitStatus.FAILED,
                content_hash=content_hash,
                layer=AnalysisLayer.DATABASE,
                analysis_type="dao_extraction",
                error_message=f"Cannot read file: {e}",
                duration_seconds=(datetime.now() - start_time).total_seconds()
            )
            self._append_visit_log(failed_entry)
            return None

        # Detect framework
        framework = self._detect_framework(file_content)

        # Determine source type
        if file_path.suffix == ".xml":
            source_type = SourceType.IBATIS_XML
        elif file_path.suffix == ".sql":
            source_type = SourceType.SQL_FILE
        elif "@Entity" in file_content:
            source_type = SourceType.JPA_ANNOTATION
        else:
            source_type = SourceType.DAO_CODE

        # Extract with LLM
        try:
            extracted = self._extract_entity_with_llm(
                file_path,
                file_content,
                framework
            )

            if not extracted:
                raise ValueError("LLM returned empty extraction")

            # Create entity
            entity = self._create_database_entity(extracted, file_path, source_type)
            self.extracted_entities.append(entity)

            # Create business rules
            rules = self._create_business_rules(extracted, file_path, entity.id)
            self.extracted_rules.extend(rules)

            # Update entity with rule IDs
            entity.business_rules = [rule.id for rule in rules]

            # Save entity to JSON
            entity_file = self.db_entities_dir / f"{entity.id}.json"
            with open(entity_file, "w", encoding="utf-8") as f:
                json.dump(entity.to_dict(), f, indent=2)

            # Save business rules to JSON
            for rule in rules:
                rule_file = self.business_rules_dir / f"{rule.id}.json"
                with open(rule_file, "w", encoding="utf-8") as f:
                    json.dump(rule.to_dict(), f, indent=2)

            # Mark as success
            success_entry = FileVisitEntry(
                file_path=str(file_path),
                timestamp=datetime.now(),
                status=VisitStatus.SUCCESS,
                content_hash=content_hash,
                layer=AnalysisLayer.DATABASE,
                analysis_type="dao_extraction",
                duration_seconds=(datetime.now() - start_time).total_seconds(),
                extracted_entities=[entity.id]
            )
            self._append_visit_log(success_entry)

            self.logger.info(f"✓ Extracted entity: {entity.name}")

            return {
                "entity": entity,
                "rules": rules,
                "status": "success"
            }

        except Exception as e:
            self.logger.error(f"Failed to analyze {file_path.name}: {e}")

            # Mark as failed
            failed_entry = FileVisitEntry(
                file_path=str(file_path),
                timestamp=datetime.now(),
                status=VisitStatus.FAILED,
                content_hash=content_hash,
                layer=AnalysisLayer.DATABASE,
                analysis_type="dao_extraction",
                error_message=str(e),
                duration_seconds=(datetime.now() - start_time).total_seconds()
            )
            self._append_visit_log(failed_entry)

            return {"status": "failed", "error": str(e)}

    def analyze_database_layer(self) -> Dict[str, Any]:
        """
        Analyze entire database layer.

        Returns:
            Summary dict with counts and statistics
        """
        self.logger.info("=" * 60)
        self.logger.info("Starting Database Layer Analysis")
        self.logger.info("=" * 60)

        # Find files to analyze
        dao_files = self.find_dao_files()

        if not dao_files:
            self.logger.warning("No DAO/entity files found")
            return {
                "total_files": 0,
                "analyzed": 0,
                "skipped": 0,
                "failed": 0,
                "entities": 0,
                "rules": 0
            }

        # Analyze files in parallel
        analyzed_count = 0
        skipped_count = 0
        failed_count = 0

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self.analyze_file, file_path): file_path
                for file_path in dao_files
            }

            for future in as_completed(futures):
                result = future.result()

                if result is None:
                    skipped_count += 1
                elif result.get("status") == "success":
                    analyzed_count += 1
                else:
                    failed_count += 1

                # Progress reporting
                total_processed = analyzed_count + skipped_count + failed_count
                if total_processed % 10 == 0:
                    self.logger.info(
                        f"Progress: {total_processed}/{len(dao_files)} files "
                        f"({analyzed_count} analyzed, {skipped_count} skipped, {failed_count} failed)"
                    )

        # Summary
        self.logger.info("=" * 60)
        self.logger.info("Database Layer Analysis Complete")
        self.logger.info("=" * 60)
        self.logger.info(f"Total files: {len(dao_files)}")
        self.logger.info(f"Analyzed: {analyzed_count}")
        self.logger.info(f"Skipped: {skipped_count}")
        self.logger.info(f"Failed: {failed_count}")
        self.logger.info(f"Entities extracted: {len(self.extracted_entities)}")
        self.logger.info(f"Business rules extracted: {len(self.extracted_rules)}")

        return {
            "total_files": len(dao_files),
            "analyzed": analyzed_count,
            "skipped": skipped_count,
            "failed": failed_count,
            "entities": len(self.extracted_entities),
            "rules": len(self.extracted_rules)
        }

    # ==========================================================================
    # Foreign Key Extraction Methods (Feature 007 US2)
    # ==========================================================================

    def _collect_columns(self, file_path: Path, file_content: str) -> Set[str]:
        """
        Collect all column names from a Java DAO/Entity file.

        Extracts columns from:
        - JPA @Column annotations
        - Field declarations
        - iBATIS resultMap entries

        Args:
            file_path: Path to file
            file_content: File content

        Returns:
            Set of column names found in the file
        """
        columns: Set[str] = set()

        # Pattern 1: @Column(name = "column_name")
        column_pattern = re.compile(r'@Column\s*\([^)]*name\s*=\s*"([^"]+)"', re.IGNORECASE)
        for match in column_pattern.finditer(file_content):
            columns.add(match.group(1))

        # Pattern 2: @JoinColumn(name = "fk_column")
        join_column_pattern = re.compile(r'@JoinColumn\s*\([^)]*name\s*=\s*"([^"]+)"', re.IGNORECASE)
        for match in join_column_pattern.finditer(file_content):
            columns.add(match.group(1))

        # Pattern 3: Field declarations (private Type fieldName) -> convert to snake_case
        field_pattern = re.compile(r'private\s+\w+(?:<[^>]+>)?\s+(\w+)\s*;')
        for match in field_pattern.finditer(file_content):
            field_name = match.group(1)
            # Convert camelCase to snake_case
            snake_case = re.sub('([a-z0-9])([A-Z])', r'\1_\2', field_name).lower()
            columns.add(snake_case)

        # Pattern 4: iBATIS resultMap <result property="field" column="column_name"/>
        if file_path.suffix == ".xml":
            result_pattern = re.compile(r'<result\s+property="[^"]*"\s+column="([^"]+)"', re.IGNORECASE)
            for match in result_pattern.finditer(file_content):
                columns.add(match.group(1))

            # iBATIS <id> tag
            id_pattern = re.compile(r'<id\s+property="[^"]*"\s+column="([^"]+)"', re.IGNORECASE)
            for match in id_pattern.finditer(file_content):
                columns.add(match.group(1))

        logger.debug(f"Collected {len(columns)} columns from {file_path.name}: {columns}")
        return columns

    def _extract_fk_from_java(self, file_path: Path, file_content: str, entity_name: str) -> List[ForeignKeyRelationship]:
        """
        Extract foreign keys from Java @JoinColumn annotations.

        Args:
            file_path: Path to Java file
            file_content: File content
            entity_name: Source entity name

        Returns:
            List of ForeignKeyRelationship from Java annotations
        """
        fk_relationships: List[ForeignKeyRelationship] = []

        # Pattern: @JoinColumn(name = "user_id", referencedColumnName = "id", nullable = false)
        # private UserDao user;
        join_column_pattern = re.compile(
            r'@JoinColumn\s*\('
            r'[^)]*name\s*=\s*"([^"]+)"'  # FK column name
            r'[^)]*referencedColumnName\s*=\s*"([^"]+)"'  # Target column
            r'[^)]*\)'
            r'\s*private\s+(\w+)\s+(\w+);',  # Target entity type and field name
            re.MULTILINE | re.DOTALL
        )

        for match in join_column_pattern.finditer(file_content):
            fk_column = match.group(1)
            target_column = match.group(2)
            target_type = match.group(3)  # e.g., UserDao, User
            field_name = match.group(4)

            # Clean target entity name (remove Dao suffix)
            target_entity = target_type.replace("Dao", "").replace("DAO", "")

            # Check for nullable attribute
            nullable = True
            nullable_match = re.search(r'nullable\s*=\s*(true|false)', match.group(0), re.IGNORECASE)
            if nullable_match:
                nullable = nullable_match.group(1).lower() == "true"

            # Check for fetch type
            fetch_type = None
            fetch_match = re.search(r'fetch\s*=\s*FetchType\.(\w+)', file_content[max(0, match.start()-200):match.start()])
            if fetch_match:
                fetch_type = fetch_match.group(1)

            # Check relationship type (@ManyToOne, @OneToOne, @OneToMany)
            relationship_type = None
            if "@ManyToOne" in file_content[max(0, match.start()-100):match.start()]:
                relationship_type = "ManyToOne"
            elif "@OneToOne" in file_content[max(0, match.start()-100):match.start()]:
                relationship_type = "OneToOne"
            elif "@OneToMany" in file_content[max(0, match.start()-100):match.start()]:
                relationship_type = "OneToMany"

            fk = ForeignKeyRelationship(
                source_entity=entity_name,
                source_column=fk_column,
                target_entity=target_entity,
                target_column=target_column,
                fk_source=ForeignKeySource.JAVA,
                nullable=nullable,
                fetch_type=fetch_type,
                relationship_type=relationship_type
            )

            fk_relationships.append(fk)
            logger.debug(f"Extracted Java FK: {fk_column} -> {target_entity}.{target_column}")

        return fk_relationships

    def _extract_fk_from_ibatis(self, file_path: Path, file_content: str, entity_name: str) -> List[ForeignKeyRelationship]:
        """
        Extract foreign keys from iBATIS XML associations and collections.

        Args:
            file_path: Path to iBATIS XML file
            file_content: File content
            entity_name: Source entity name

        Returns:
            List of ForeignKeyRelationship from iBATIS XML
        """
        fk_relationships: List[ForeignKeyRelationship] = []

        # Pattern 1: <association property="user" javaType="UserDao">
        #              <id property="id" column="user_id" />
        #            </association>
        association_pattern = re.compile(
            r'<association\s+property="(\w+)"\s+javaType="([^"]+)"[^>]*>'
            r'(.*?)'
            r'</association>',
            re.MULTILINE | re.DOTALL
        )

        for match in association_pattern.finditer(file_content):
            property_name = match.group(1)
            java_type = match.group(2)
            association_content = match.group(3)

            # Extract target entity from javaType (e.g., com.example.dao.UserDao -> UserDao)
            target_entity = java_type.split(".")[-1].replace("Dao", "").replace("DAO", "")

            # Extract FK column from <id> or <result> tags
            id_pattern = re.compile(r'<id\s+property="(\w+)"\s+column="([^"]+)"', re.IGNORECASE)
            id_match = id_pattern.search(association_content)

            if id_match:
                target_column_property = id_match.group(1)
                fk_column = id_match.group(2)

                fk = ForeignKeyRelationship(
                    source_entity=entity_name,
                    source_column=fk_column,
                    target_entity=target_entity,
                    target_column=target_column_property,  # Usually "id"
                    fk_source=ForeignKeySource.IBATIS
                )

                fk_relationships.append(fk)
                logger.debug(f"Extracted iBATIS FK: {fk_column} -> {target_entity}.{target_column_property}")

        # Pattern 2: <collection property="notes" ofType="MyNotesDao">
        #              <result property="userId" column="user_id" />
        #            </collection>
        collection_pattern = re.compile(
            r'<collection\s+property="(\w+)"\s+ofType="([^"]+)"[^>]*>'
            r'(.*?)'
            r'</collection>',
            re.MULTILINE | re.DOTALL
        )

        for match in collection_pattern.finditer(file_content):
            property_name = match.group(1)
            of_type = match.group(2)
            collection_content = match.group(3)

            # Extract FK from result tags (e.g., <result property="userId" column="user_id"/>)
            result_pattern = re.compile(r'<result\s+property="(\w+)"\s+column="([^"]+)"', re.IGNORECASE)
            for result_match in result_pattern.finditer(collection_content):
                property_field = result_match.group(1)
                fk_column = result_match.group(2)

                # If property looks like a FK (ends with Id or contains foreign entity name)
                if "id" in property_field.lower() or property_field.endswith("Id"):
                    # Infer target entity from property name (e.g., userId -> User)
                    target_entity = property_field.replace("Id", "").replace("id", "")
                    target_entity = target_entity[0].upper() + target_entity[1:]  # Capitalize

                    fk = ForeignKeyRelationship(
                        source_entity=of_type.split(".")[-1].replace("Dao", "").replace("DAO", ""),
                        source_column=fk_column,
                        target_entity=target_entity,
                        target_column="id",
                        fk_source=ForeignKeySource.IBATIS
                    )

                    fk_relationships.append(fk)
                    logger.debug(f"Extracted iBATIS collection FK: {fk_column} -> {target_entity}.id")

        return fk_relationships

    def _validate_fk_columns(
        self,
        fk_relationships: List[ForeignKeyRelationship],
        collected_columns: Set[str]
    ) -> List[FKValidationResult]:
        """
        Validate that FK columns exist in collected columns.

        Args:
            fk_relationships: List of FK to validate
            collected_columns: Set of column names collected from entity

        Returns:
            List of FKValidationResult with validation status
        """
        results: List[FKValidationResult] = []

        for fk in fk_relationships:
            if fk.source_column in collected_columns:
                # Valid FK
                results.append(FKValidationResult(
                    fk=fk,
                    is_valid=True,
                    error_message=None
                ))
                logger.debug(f"✓ FK column validated: {fk.source_column}")
            else:
                # Invalid FK - column not found
                error_msg = f"Column {fk.source_column} not found in collected columns"
                results.append(FKValidationResult(
                    fk=fk,
                    is_valid=False,
                    error_message=error_msg
                ))
                logger.warning(f"✗ FK validation failed: {error_msg}")

        return results

    def extract_foreign_keys(
        self,
        file_path: Path,
        file_content: str,
        entity_name: str
    ) -> List[ForeignKeyRelationship]:
        """
        Extract and merge foreign keys from all sources (Java, iBATIS, SQL).

        Implements Feature 007 US2 FK extraction with merge logic.

        Args:
            file_path: Path to file
            file_content: File content
            entity_name: Entity name

        Returns:
            Merged list of ForeignKeyRelationship with duplicates removed
        """
        all_fk: List[ForeignKeyRelationship] = []

        # Extract from Java @JoinColumn
        if file_path.suffix == ".java":
            java_fk = self._extract_fk_from_java(file_path, file_content, entity_name)
            all_fk.extend(java_fk)
            logger.info(f"Extracted {len(java_fk)} FK from Java annotations")

        # Extract from iBATIS XML
        if file_path.suffix == ".xml":
            ibatis_fk = self._extract_fk_from_ibatis(file_path, file_content, entity_name)
            all_fk.extend(ibatis_fk)
            logger.info(f"Extracted {len(ibatis_fk)} FK from iBATIS XML")

        # Extract from SQL JOIN statements (T041)
        sql_fk = self._extract_fk_from_sql(file_content, entity_name)
        if sql_fk:
            all_fk.extend(sql_fk)
            logger.info(f"Extracted {len(sql_fk)} FK from SQL JOIN statements")

        # Merge duplicates using priority: Java (3) > iBATIS (2) > SQL (1)
        merged_fk = self._merge_fk_by_priority(all_fk)

        logger.info(f"Merged {len(all_fk)} FK into {len(merged_fk)} unique relationships")
        return merged_fk

    def _extract_fk_from_sql(self, file_content: str, entity_name: str) -> List[ForeignKeyRelationship]:
        """
        Extract foreign keys from SQL JOIN statements embedded in Java code.

        Args:
            file_content: File content (Java or SQL)
            entity_name: Entity name

        Returns:
            List of ForeignKeyRelationship from SQL
        """
        sql_parser = SQLParser()
        return sql_parser.extract_foreign_keys_from_joins(file_content)

    def _merge_fk_by_priority(self, fk_list: List[ForeignKeyRelationship]) -> List[ForeignKeyRelationship]:
        """
        Merge FK relationships by priority, keeping highest priority source.

        Priority: Java (3) > iBATIS (2) > SQL (1)

        Args:
            fk_list: List of FK relationships to merge

        Returns:
            Merged list with duplicates removed (keeping highest priority)
        """
        fk_map: Dict[tuple, ForeignKeyRelationship] = {}

        for fk in fk_list:
            # Create key from entities and columns (ignoring source)
            key = (fk.source_entity, fk.source_column, fk.target_entity, fk.target_column)

            if key in fk_map:
                # Duplicate found - keep higher priority
                existing_fk = fk_map[key]
                if fk.get_source_priority() > existing_fk.get_source_priority():
                    fk_map[key] = fk
                    logger.debug(
                        f"Merged FK {fk.source_column}: {fk.fk_source.value} "
                        f"(priority {fk.get_source_priority()}) replaces "
                        f"{existing_fk.fk_source.value} (priority {existing_fk.get_source_priority()})"
                    )
            else:
                fk_map[key] = fk

        return list(fk_map.values())

    def extract_foreign_keys_from_file(self, file_path: Path) -> List[ForeignKeyRelationship]:
        """
        Extract foreign keys from a single DAO/Entity file.

        Wrapper method for integration tests.

        Args:
            file_path: Path to file

        Returns:
            List of ForeignKeyRelationship extracted from file
        """
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                file_content = f.read()

            # Infer entity name from filename
            entity_name = file_path.stem.replace("Dao", "").replace("DAO", "")

            # Extract FK
            fk_relationships = self.extract_foreign_keys(file_path, file_content, entity_name)

            # Log FK metric
            # Count FK by source
            fk_from_java = sum(1 for fk in fk_relationships if fk.fk_source == ForeignKeySource.JAVA)
            fk_from_ibatis = sum(1 for fk in fk_relationships if fk.fk_source == ForeignKeySource.IBATIS)
            fk_from_sql = sum(1 for fk in fk_relationships if fk.fk_source == ForeignKeySource.SQL)

            metric = ForeignKeyMetric(
                dao_file=str(file_path),
                fk_extracted=len(fk_relationships),
                fk_from_java=fk_from_java,
                fk_from_ibatis=fk_from_ibatis,
                fk_from_sql=fk_from_sql,
                validation_errors=0,  # Will be updated during validation
                columns_collected=0   # Will be updated if column collection runs
            )

            metrics_collector = get_metrics_collector()
            metrics_collector.add_fk_metric(metric)

            return fk_relationships

        except Exception as e:
            logger.error(f"Failed to extract FK from {file_path}: {e}")
            return []

    def merge_foreign_keys(self, fk_lists: List[List[ForeignKeyRelationship]]) -> List[ForeignKeyRelationship]:
        """
        Merge FK from multiple sources (e.g., Java files and iBATIS XML).

        Args:
            fk_lists: List of FK lists from different files

        Returns:
            Merged list of unique FK relationships
        """
        all_fk: List[ForeignKeyRelationship] = []
        for fk_list in fk_lists:
            all_fk.extend(fk_list)

        return self._merge_fk_by_priority(all_fk)

    def validate_foreign_keys(
        self,
        fk_relationships: List[ForeignKeyRelationship],
        collected_columns: Set[str]
    ) -> List[FKValidationResult]:
        """
        Validate FK relationships against collected columns.

        Args:
            fk_relationships: List of FK to validate
            collected_columns: Set of column names from entity

        Returns:
            List of FKValidationResult
        """
        return self._validate_fk_columns(fk_relationships, collected_columns)


# ==============================================================================
# Type Alias for Backwards Compatibility
# ==============================================================================

# Alias for integration tests that expect DbAnalyzer
DbAnalyzer = DatabaseAnalyzer
