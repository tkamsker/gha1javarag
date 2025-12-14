"""
Database Analyzer Service for PRD Generation.

Analyzes DAO classes, JPA entities, iBATIS/MyBatis mapper XML, and SQL files
to extract database entity definitions and business rules.
"""
import logging
import hashlib
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Set
from concurrent.futures import ThreadPoolExecutor, as_completed

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
from codeindex.services.ollama_client import OllamaClient
from codeindex.utils.retry import retry

logger = logging.getLogger(__name__)


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
        prompt = DAO_EXTRACTION_PROMPT_TEMPLATE.format(
            file_path=str(file_path),
            framework=framework,
            source_code=file_content[:15000],  # Limit to 15k chars
            related_entities_summary=related_entities or "None"
        )

        try:
            # Call Ollama with JSON mode
            response = self.ollama_client.call_ollama(
                prompt=prompt,
                temperature=0.2,
                format_json=True
            )

            # Parse JSON response
            response_text = response["response"]
            extracted = json.loads(response_text)

            # Validate required fields
            if "entity_name" not in extracted:
                raise ValueError("Missing required field: entity_name")
            if "columns" not in extracted or not extracted["columns"]:
                raise ValueError("Missing or empty required field: columns")
            if "description" not in extracted:
                raise ValueError("Missing required field: description")

            self.logger.debug(f"Successfully extracted entity: {extracted.get('entity_name')}")
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
