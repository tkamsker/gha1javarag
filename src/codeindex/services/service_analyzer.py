"""
Service Layer Analyzer.

Extracts service definitions, API endpoints, and business rules from Java service classes.
"""
import json
import logging
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from uuid import uuid4

from codeindex.models.prd import (
    ServiceDefinition,
    ServiceOperation,
    Parameter,
    ServiceDependency,
    TransactionInfo,
    APIEndpoint,
    HTTPMethod,
    EndpointParameter,
    StatusCode,
    RequestFormat,
    ResponseFormat,
    BusinessRule,
    RuleLayer,
    RuleScope,
    RuleType,
    ServiceType,
    FileVisitEntry,
    VisitStatus,
    AnalysisLayer,
)
from codeindex.utils.retry import retry


# ==============================================================================
# LLM Prompt Templates
# ==============================================================================

SERVICE_EXTRACTION_PROMPT_TEMPLATE = """You are analyzing a Java service class to document its business operations and dependencies.

FILE: {file_path}
SERVICE TYPE: {detected_service_type}

SOURCE CODE:
```java
{source_code}
```

RELATED SERVICES (from Weaviate):
{related_services_summary}

DATABASE ENTITIES (from analysis):
{database_entities_accessed}

TASK:
Extract the following information in JSON format:

1. **class_name**: Simple class name
2. **qualified_name**: Fully qualified class name (package.ClassName)
3. **service_type**: business_service | dao_service | integration_service | controller | rest_controller | utility_service
4. **description**: Natural language description (2-3 sentences) of what this service does
5. **operations**: List of public methods with signatures, parameters, return types, descriptions
6. **dependencies**: Other services or DAOs injected or referenced
7. **data_dependencies**: Database entities (tables) this service accesses
8. **business_rules**: Business rules implemented in this service
9. **transaction_boundaries**: Methods with transaction management (@Transactional, etc.)

RESPONSE FORMAT (JSON):
{{
  "class_name": "string",
  "qualified_name": "string",
  "service_type": "business_service | dao_service | integration_service | controller | rest_controller | utility_service",
  "description": "string (2-3 sentences)",
  "operations": [
    {{
      "name": "string",
      "signature": "string (full method signature)",
      "return_type": "string",
      "parameters": [
        {{
          "name": "string",
          "type": "string",
          "description": "string or null"
        }}
      ],
      "description": "string (what this method does)",
      "throws": ["string (exception types)"],
      "annotations": ["string"],
      "line_number": integer or null
    }}
  ],
  "dependencies": [
    {{
      "target_service": "string (class name or qualified name)",
      "dependency_type": "injection | reference | static",
      "injection_method": "constructor | field | setter or null"
    }}
  ],
  "data_dependencies": ["string (entity names)"],
  "business_rules": [
    {{
      "name": "string",
      "description": "string",
      "enforcement": "string (how it's enforced)"
    }}
  ],
  "transaction_boundaries": [
    {{
      "method_name": "string",
      "transaction_type": "REQUIRED | REQUIRES_NEW | SUPPORTS | MANDATORY | NOT_SUPPORTED | NEVER",
      "propagation": "string or null",
      "isolation_level": "string or null",
      "read_only": boolean or null
    }}
  ],
  "frameworks": ["string (Spring, EJB, etc.)"],
  "domain": "string (business domain) or null"
}}

IMPORTANT:
- Focus on public methods (operations visible to other components)
- Infer data_dependencies from DAO method calls or entity class references
- Extract business logic from method implementations, not just method names
- Identify transaction boundaries from @Transactional or programmatic transaction management
"""


# ==============================================================================
# ServiceAnalyzer
# ==============================================================================

class ServiceAnalyzer:
    """
    Analyzes service layer classes to extract:
    - Service definitions with operations and dependencies
    - API endpoints (REST/SOAP)
    - Service-level business rules
    - Transaction boundaries
    """

    def __init__(
        self,
        ollama_client,
        output_dir: Path,
        source_dir: Path,
        max_workers: int = 10,
        llm_timeout: int = 120,
        max_retries: int = 3,
        force_refresh: bool = False,
    ):
        """
        Initialize ServiceAnalyzer.

        Args:
            ollama_client: Ollama client for LLM calls
            output_dir: Output directory for results
            source_dir: Source code directory to analyze
            max_workers: Maximum concurrent LLM requests
            llm_timeout: LLM request timeout in seconds
            max_retries: Maximum retry attempts for LLM
            force_refresh: Force re-analysis of all files
        """
        self.ollama_client = ollama_client
        self.output_dir = Path(output_dir)
        self.source_dir = Path(source_dir)
        self.max_workers = max_workers
        self.llm_timeout = llm_timeout
        self.max_retries = max_retries
        self.force_refresh = force_refresh

        # Create output directories
        self.services_dir = self.output_dir / "services" / "definitions"
        self.endpoints_dir = self.output_dir / "services" / "endpoints"
        self.business_rules_dir = self.output_dir / "business_rules"
        self.visit_log_file = self.output_dir / "visit_log.jsonl"

        self.services_dir.mkdir(parents=True, exist_ok=True)
        self.endpoints_dir.mkdir(parents=True, exist_ok=True)
        self.business_rules_dir.mkdir(parents=True, exist_ok=True)

        # Load visit log
        self.visit_log = self._load_visit_log()
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
                f.write(json.dumps(entry.to_dict()) + "\n")
                self.visit_log[entry.file_path] = entry
        except Exception as e:
            self.logger.error(f"Failed to append visit log: {e}")

    def _compute_file_hash(self, file_path: Path) -> str:
        """
        Compute SHA-256 hash of file contents.

        Args:
            file_path: Path to file

        Returns:
            Hex string (64 characters)
        """
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    def _should_analyze_file(self, file_path: Path) -> bool:
        """
        Check if file should be analyzed based on visit log.

        Args:
            file_path: Path to file

        Returns:
            True if file should be analyzed, False to skip
        """
        if self.force_refresh:
            return True

        file_path_str = str(file_path)
        if file_path_str not in self.visit_log:
            return True  # Never analyzed

        entry = self.visit_log[file_path_str]
        if entry.status != VisitStatus.SUCCESS:
            return True  # Previous analysis failed - retry

        # Check if file content changed
        try:
            current_hash = self._compute_file_hash(file_path)
            if current_hash != entry.content_hash:
                return True  # Content changed - re-analyze
            else:
                return False  # Unchanged - skip
        except Exception:
            return True  # Error computing hash - re-analyze to be safe

        return True

    def _detect_service_type(self, file_content: str, file_name: str) -> str:
        """
        Detect service type from file content and name.

        Args:
            file_content: File content
            file_name: File name

        Returns:
            Service type string
        """
        # GWT RPC Servlet (FR-002)
        if ("Servlet" in file_name and
            ("RemoteServiceServlet" in file_content or "RemoteService" in file_content)):
            return "GWT RPC Servlet"

        # REST Controller
        if "@RestController" in file_content or "@RequestMapping" in file_content:
            return "REST Controller"

        # Controller
        if "@Controller" in file_content:
            return "Controller"

        # DAO Service
        if "DAO" in file_name or "Repository" in file_name or "@Repository" in file_content:
            return "DAO Service"

        # Integration Service
        if "Integration" in file_name or "Client" in file_name or "@FeignClient" in file_content:
            return "Integration Service"

        # Business Service
        if "@Service" in file_content or "Service" in file_name:
            return "Business Service"

        # Utility Service
        if "Util" in file_name or "Helper" in file_name:
            return "Utility Service"

        return "Unknown"

    def find_service_files(self) -> List[Path]:
        """
        Find all service-related files.

        Returns:
            List of file paths to analyze
        """
        service_files = []

        # Patterns to match
        patterns = [
            "**/*Service.java",
            "**/*Controller.java",
            "**/*Rest*.java",
            "**/*Repository.java",
            "**/*DAO.java",
            "**/*Dao.java",
            "**/*Client.java",
            "**/*Facade.java",
            "**/*Servlet.java",       # GWT RPC servlets
            "**/*ServletImpl.java",   # GWT RPC servlet implementations
            "**/*Manager.java",
        ]

        for pattern in patterns:
            for file_path in self.source_dir.glob(pattern):
                if file_path.is_file():
                    service_files.append(file_path)

        # Remove duplicates
        service_files = list(set(service_files))

        self.logger.info(f"Found {len(service_files)} service-related files")
        return service_files

    @retry(max_attempts=3, base_delay=1.0, exponential_base=2.0)
    def _extract_service_with_llm(
        self,
        file_path: Path,
        file_content: str,
        detected_type: str,
        related_services: str = "",
        database_entities: str = "",
    ) -> Optional[Dict[str, Any]]:
        """
        Extract service definition using LLM.

        Args:
            file_path: Path to service file
            file_content: File content
            detected_type: Detected service type
            related_services: Summary of related services
            database_entities: Summary of database entities

        Returns:
            Parsed JSON response from LLM, or None on failure
        """
        prompt = SERVICE_EXTRACTION_PROMPT_TEMPLATE.format(
            file_path=str(file_path),
            detected_service_type=detected_type,
            source_code=file_content[:15000],  # Limit to 15k chars
            related_services_summary=related_services or "None",
            database_entities_accessed=database_entities or "None",
        )

        response = self.ollama_client.call_ollama(
            prompt=prompt,
            timeout=self.llm_timeout,
        )

        if not response or "response" not in response:
            raise ValueError("Empty response from LLM")

        # Parse JSON from response
        response_text = response["response"]

        # Try to extract JSON from response
        try:
            # If response is wrapped in markdown code blocks, extract it
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()
            elif "```" in response_text:
                start = response_text.find("```") + 3
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()

            return json.loads(response_text)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse LLM response as JSON: {e}")
            raise

    def analyze_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Analyze a single service file.

        Args:
            file_path: Path to service file

        Returns:
            Analysis result dict with status, service, endpoints, rules
        """
        self.logger.info(f"Analyzing: {file_path.name}")

        try:
            # Read file content
            with open(file_path, "r", encoding="utf-8") as f:
                file_content = f.read()

            # Detect service type
            detected_type = self._detect_service_type(file_content, file_path.name)

            # Extract service using LLM
            llm_result = self._extract_service_with_llm(
                file_path=file_path,
                file_content=file_content,
                detected_type=detected_type,
                related_services="",  # TODO: Query from Weaviate
                database_entities="",  # TODO: Load from previous analysis
            )

            if not llm_result:
                return {"status": "failed", "error": "No LLM result"}

            # Convert to ServiceDefinition
            service = self._create_service_definition(llm_result, file_path)

            # Extract API endpoints if REST controller
            endpoints = []
            if service.service_type in (ServiceType.REST_CONTROLLER, ServiceType.CONTROLLER):
                endpoints = self._extract_api_endpoints(service, file_content)

            # Extract business rules
            rules = self._extract_business_rules(llm_result, service, file_path)

            # Save to disk
            self._save_service(service)
            for endpoint in endpoints:
                self._save_endpoint(endpoint)
            for rule in rules:
                self._save_business_rule(rule)

            # Record visit
            entry = FileVisitEntry(
                file_path=str(file_path),
                timestamp=datetime.now(),
                status=VisitStatus.SUCCESS,
                content_hash=self._compute_file_hash(file_path),
                layer=AnalysisLayer.SERVICE,
                extracted_entities=[service.id],
            )
            self._append_visit_log(entry)

            self.logger.info(f"✓ Extracted service: {service.class_name}")

            return {
                "status": "success",
                "service": service,
                "endpoints": endpoints,
                "rules": rules,
            }

        except Exception as e:
            self.logger.error(f"Failed to analyze {file_path}: {e}")

            # Record failure
            entry = FileVisitEntry(
                file_path=str(file_path),
                timestamp=datetime.now(),
                status=VisitStatus.FAILED,
                content_hash=self._compute_file_hash(file_path),
                layer=AnalysisLayer.SERVICE,
                error_message=str(e),
            )
            self._append_visit_log(entry)

            return {"status": "failed", "error": str(e)}

    def _create_service_definition(
        self, llm_result: Dict[str, Any], file_path: Path
    ) -> ServiceDefinition:
        """
        Create ServiceDefinition from LLM result.

        Args:
            llm_result: Parsed JSON from LLM
            file_path: Source file path

        Returns:
            ServiceDefinition instance
        """
        # Parse service type
        service_type_str = llm_result.get("service_type", "business_service")
        service_type = ServiceType(service_type_str)

        # Parse operations
        operations = []
        for op_data in llm_result.get("operations", []):
            parameters = [
                Parameter(
                    name=p["name"],
                    type=p["type"],
                    description=p.get("description"),
                )
                for p in op_data.get("parameters", [])
            ]

            operation = ServiceOperation(
                name=op_data["name"],
                signature=op_data["signature"],
                return_type=op_data["return_type"],
                parameters=parameters,
                description=op_data.get("description"),
                throws=op_data.get("throws", []),
                annotations=op_data.get("annotations", []),
                line_number=op_data.get("line_number"),
            )
            operations.append(operation)

        # Parse dependencies
        dependencies = [
            ServiceDependency(
                target_service=dep["target_service"],
                dependency_type=dep["dependency_type"],
                injection_method=dep.get("injection_method"),
            )
            for dep in llm_result.get("dependencies", [])
        ]

        # Parse transaction boundaries
        transaction_boundaries = [
            TransactionInfo(
                method_name=tb["method_name"],
                transaction_type=tb["transaction_type"],
                propagation=tb.get("propagation"),
                isolation_level=tb.get("isolation_level"),
                read_only=tb.get("read_only"),
            )
            for tb in llm_result.get("transaction_boundaries", [])
        ]

        # Extract package from qualified name
        qualified_name = llm_result["qualified_name"]
        package = ".".join(qualified_name.split(".")[:-1]) if "." in qualified_name else ""

        return ServiceDefinition(
            id=qualified_name,
            class_name=llm_result["class_name"],
            qualified_name=qualified_name,
            package=package,
            source_file=str(file_path),
            service_type=service_type,
            description=llm_result.get("description"),
            operations=operations,
            dependencies=dependencies,
            data_dependencies=llm_result.get("data_dependencies", []),
            business_rules=[],  # Will be populated by business rule IDs
            transaction_boundaries=transaction_boundaries,
            frameworks=llm_result.get("frameworks", []),
            domain=llm_result.get("domain"),
            created_at=datetime.now(),
        )

    def _extract_api_endpoints(
        self, service: ServiceDefinition, file_content: str
    ) -> List[APIEndpoint]:
        """
        Extract API endpoints from REST controller.

        Args:
            service: ServiceDefinition
            file_content: File content

        Returns:
            List of APIEndpoint instances
        """
        endpoints = []

        # Simple extraction - look for @RequestMapping annotations
        # In production, would use more sophisticated parsing

        for operation in service.operations:
            # Check if operation has request mapping annotations
            for annotation in operation.annotations:
                if any(method in annotation for method in ["GetMapping", "PostMapping", "PutMapping", "DeleteMapping", "PatchMapping", "RequestMapping"]):
                    # Extract HTTP method
                    http_method = self._extract_http_method(annotation)

                    # Extract path
                    path = self._extract_path(annotation, operation.name)

                    # Create endpoint
                    endpoint = APIEndpoint(
                        id=f"{http_method.value}:{path}",
                        http_method=http_method,
                        path=path,
                        service_id=service.id,
                        operation_name=operation.name,
                        source_file=service.source_file,
                        description=operation.description,
                        created_at=datetime.now(),
                    )
                    endpoints.append(endpoint)

                    # Add endpoint ID to service
                    service.endpoints.append(endpoint.id)

        return endpoints

    def _extract_http_method(self, annotation: str) -> HTTPMethod:
        """Extract HTTP method from annotation."""
        if "GetMapping" in annotation or 'method = RequestMethod.GET' in annotation:
            return HTTPMethod.GET
        elif "PostMapping" in annotation or 'method = RequestMethod.POST' in annotation:
            return HTTPMethod.POST
        elif "PutMapping" in annotation or 'method = RequestMethod.PUT' in annotation:
            return HTTPMethod.PUT
        elif "DeleteMapping" in annotation or 'method = RequestMethod.DELETE' in annotation:
            return HTTPMethod.DELETE
        elif "PatchMapping" in annotation or 'method = RequestMethod.PATCH' in annotation:
            return HTTPMethod.PATCH
        else:
            return HTTPMethod.GET  # Default

    def _extract_path(self, annotation: str, operation_name: str) -> str:
        """Extract path from annotation."""
        # Simple extraction - look for value or path attribute
        if 'value = "' in annotation:
            start = annotation.find('value = "') + 9
            end = annotation.find('"', start)
            return annotation[start:end]
        elif 'path = "' in annotation:
            start = annotation.find('path = "') + 8
            end = annotation.find('"', start)
            return annotation[start:end]
        elif '("' in annotation:
            start = annotation.find('("') + 2
            end = annotation.find('"', start)
            return annotation[start:end]
        else:
            # Generate path from operation name
            return f"/{operation_name}"

    def _extract_business_rules(
        self, llm_result: Dict[str, Any], service: ServiceDefinition, file_path: Path
    ) -> List[BusinessRule]:
        """
        Extract business rules from LLM result.

        Args:
            llm_result: Parsed JSON from LLM
            service: ServiceDefinition
            file_path: Source file path

        Returns:
            List of BusinessRule instances
        """
        rules = []

        for rule_data in llm_result.get("business_rules", []):
            rule_id = str(uuid4())

            rule = BusinessRule(
                id=rule_id,
                name=rule_data["name"],
                layer=RuleLayer.SERVICE,
                scope=RuleScope.ENTITY,  # Default to entity scope
                rule_type=RuleType.BUSINESS_LOGIC,  # Default to business logic
                description=rule_data["description"],
                source_files=[str(file_path)],
                enforcement_mechanism=rule_data.get("enforcement", "Service layer validation"),
                related_entities=[service.id],
                domain=service.domain,
                created_at=datetime.now(),
            )
            rules.append(rule)

            # Add rule ID to service
            service.business_rules.append(rule_id)

        return rules

    def _save_service(self, service: ServiceDefinition):
        """Save service definition to JSON file."""
        output_file = self.services_dir / f"{service.class_name}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(service.to_dict(), f, indent=2)

    def _save_endpoint(self, endpoint: APIEndpoint):
        """Save API endpoint to JSON file."""
        # Sanitize filename
        filename = f"{endpoint.http_method.value}_{endpoint.path.replace('/', '_')}.json"
        output_file = self.endpoints_dir / filename
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(endpoint.to_dict(), f, indent=2)

    def _save_business_rule(self, rule: BusinessRule):
        """Save business rule to JSON file."""
        output_file = self.business_rules_dir / f"{rule.id}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(rule.to_dict(), f, indent=2)

    def analyze_service_layer(self) -> Dict[str, Any]:
        """
        Analyze all service files in parallel.

        Returns:
            Summary dict with statistics
        """
        service_files = self.find_service_files()

        # Filter files that need analysis
        files_to_analyze = [f for f in service_files if self._should_analyze_file(f)]

        if not files_to_analyze:
            self.logger.info("No files to analyze (all up to date)")
            return {
                "total_files": len(service_files),
                "analyzed": 0,
                "skipped": len(service_files),
                "services_extracted": 0,
                "endpoints_found": 0,
                "rules_identified": 0,
            }

        self.logger.info(f"Analyzing {len(files_to_analyze)} files...")

        # Analyze in parallel
        services_extracted = 0
        endpoints_found = 0
        rules_identified = 0
        failed = 0

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self.analyze_file, file_path): file_path
                for file_path in files_to_analyze
            }

            for future in as_completed(futures):
                result = future.result()
                if result and result["status"] == "success":
                    services_extracted += 1
                    endpoints_found += len(result.get("endpoints", []))
                    rules_identified += len(result.get("rules", []))
                else:
                    failed += 1

        return {
            "total_files": len(service_files),
            "analyzed": len(files_to_analyze),
            "skipped": len(service_files) - len(files_to_analyze),
            "services_extracted": services_extracted,
            "endpoints_found": endpoints_found,
            "rules_identified": rules_identified,
            "failed": failed,
        }
