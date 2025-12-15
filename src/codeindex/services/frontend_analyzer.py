"""
Frontend Layer Analyzer.

Extracts forms, UI components, and navigation flows from JSP/HTML/GWT/JavaScript code.
"""
import json
import logging
import hashlib
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from uuid import uuid4

from codeindex.parsers.uibinder_parser import GwtUiBinderParser
from codeindex.models.prd import (
    FormDefinition,
    FormField,
    FormType,
    UIComponent,
    ComponentType,
    Event,
    DataBinding,
    NavigationFlow,
    FlowType,
    EntryPoint,
    NavigationStep,
    ExitPoint,
    BusinessRule,
    RuleLayer,
    RuleScope,
    RuleType,
    FileVisitEntry,
    VisitStatus,
    AnalysisLayer,
)
from codeindex.utils.retry import retry


# ==============================================================================
# LLM Prompt Templates
# ==============================================================================

FORM_EXTRACTION_PROMPT_TEMPLATE = """You are analyzing a frontend file to extract form definitions.

FILE: {file_path}
FILE TYPE: {file_type}

SOURCE CODE:
```
{source_code}
```

TASK:
Extract form information in JSON format:

1. **form_name**: Form identifier or name
2. **form_type**: jsp_form | html_form | gwt_form | react_form | javascript_form
3. **description**: What this form does (2-3 sentences)
4. **fields**: List of form fields with name, type, label, required, validation
5. **submission_endpoint**: URL or endpoint this form submits to
6. **submission_method**: GET or POST
7. **bound_entities**: Database entities this form creates/updates

RESPONSE FORMAT (JSON):
{{
  "form_name": "string",
  "form_type": "jsp_form | html_form | gwt_form | react_form | javascript_form",
  "description": "string",
  "fields": [
    {{
      "name": "string",
      "type": "text | email | password | number | select | checkbox | textarea | date | file",
      "label": "string or null",
      "required": boolean,
      "validation_pattern": "string or null",
      "default_value": "string or null"
    }}
  ],
  "submission_endpoint": "string or null",
  "submission_method": "GET | POST or null",
  "bound_entities": ["string (entity names)"]
}}
"""


# ==============================================================================
# FrontendAnalyzer
# ==============================================================================

class FrontendAnalyzer:
    """
    Analyzes frontend layer to extract:
    - Form definitions with fields and validation
    - UI components with events and data bindings
    - Navigation flows
    - Frontend-level business rules
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
        Initialize FrontendAnalyzer.

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
        self.forms_dir = self.output_dir / "frontend" / "forms"
        self.components_dir = self.output_dir / "frontend" / "components"
        self.navigation_dir = self.output_dir / "frontend" / "navigation"
        self.business_rules_dir = self.output_dir / "business_rules"
        self.visit_log_file = self.output_dir / "visit_log.jsonl"

        self.forms_dir.mkdir(parents=True, exist_ok=True)
        self.components_dir.mkdir(parents=True, exist_ok=True)
        self.navigation_dir.mkdir(parents=True, exist_ok=True)
        self.business_rules_dir.mkdir(parents=True, exist_ok=True)

        # Load visit log
        self.visit_log = self._load_visit_log()
        self.logger = logging.getLogger(__name__)

        # Initialize GWT parsers
        self.uibinder_parser = GwtUiBinderParser()

    def _load_visit_log(self) -> Dict[str, FileVisitEntry]:
        """Load visit log from JSON Lines file."""
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
                        visit_log[entry.file_path] = entry
                    except (json.JSONDecodeError, ValueError) as e:
                        self.logger.warning(f"Invalid visit log entry: {e}")
                        continue

        except Exception as e:
            self.logger.warning(f"Failed to load visit log: {e}")

        return visit_log

    def _append_visit_log(self, entry: FileVisitEntry):
        """Append entry to visit log."""
        try:
            with open(self.visit_log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry.to_dict()) + "\n")
                self.visit_log[entry.file_path] = entry
        except Exception as e:
            self.logger.error(f"Failed to append visit log: {e}")

    def _compute_file_hash(self, file_path: Path) -> str:
        """Compute SHA-256 hash of file contents."""
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    def _should_analyze_file(self, file_path: Path) -> bool:
        """Check if file should be analyzed based on visit log."""
        if self.force_refresh:
            return True

        file_path_str = str(file_path)
        if file_path_str not in self.visit_log:
            return True

        entry = self.visit_log[file_path_str]
        if entry.status != VisitStatus.SUCCESS:
            return True

        try:
            current_hash = self._compute_file_hash(file_path)
            return current_hash != entry.content_hash
        except Exception:
            return True

    def find_frontend_files(self) -> List[Path]:
        """Find all frontend-related files."""
        frontend_files = []

        patterns = [
            "**/*.jsp",
            "**/*.jspf",
            "**/*.html",
            "**/*.htm",
            "**/*View.java",  # GWT views
            "**/*Activity.java",  # GWT activities
            "**/*Widget.java",  # GWT widgets
            "**/*.ui.xml",  # GWT UiBinder
            "**/*.js",
            "**/*.jsx",
        ]

        for pattern in patterns:
            for file_path in self.source_dir.glob(pattern):
                if file_path.is_file():
                    # Skip minified files
                    if ".min." not in str(file_path):
                        frontend_files.append(file_path)

        frontend_files = list(set(frontend_files))
        self.logger.info(f"Found {len(frontend_files)} frontend files")
        return frontend_files

    def _detect_file_type(self, file_path: Path) -> str:
        """Detect frontend file type."""
        suffix = file_path.suffix.lower()
        name = file_path.name

        if suffix in [".jsp", ".jspf"]:
            return "JSP"
        elif suffix in [".html", ".htm"]:
            return "HTML"
        elif ".ui.xml" in name:
            return "GWT UiBinder"
        elif suffix == ".java" and ("View" in name or "Activity" in name or "Widget" in name):
            return "GWT"
        elif suffix in [".js", ".jsx"]:
            return "JavaScript"
        else:
            return "Unknown"

    def _convert_uibinder_to_llm_format(
        self,
        uibinder_result: Dict[str, Any],
        file_path: Path
    ) -> Dict[str, Any]:
        """
        Convert GWT UiBinder parser output to LLM-compatible format.

        Args:
            uibinder_result: Output from GwtUiBinderParser.parse()
            file_path: Path to UiBinder file

        Returns:
            Dictionary in LLM extraction format
        """
        # Map widget types to form field types
        widget_type_mapping = {
            'TextBox': 'text',
            'PasswordTextBox': 'password',
            'TextArea': 'textarea',
            'IntegerBox': 'number',
            'DoubleBox': 'number',
            'ListBox': 'select',
            'CheckBox': 'checkbox',
            'RadioButton': 'radio',
            'DateBox': 'date',
            'Button': 'button',
            'SubmitButton': 'submit',
            'ResetButton': 'button',
        }

        # Convert form fields
        fields = []
        for field_data in uibinder_result.get('form_fields', []):
            widget_type = field_data.get('widget_type', 'text')
            field_type = widget_type_mapping.get(widget_type, 'text')

            field = {
                'name': field_data.get('field_name', ''),
                'type': field_type,
                'label': field_data.get('label', ''),
                'required': '*' in field_data.get('label', '') or 'required' in field_data.get('attributes', {}),
                'validation': []
            }

            # Add options for select/listbox
            if 'options' in field_data:
                field['options'] = [opt['label'] for opt in field_data['options']]

            fields.append(field)

        return {
            'form_name': uibinder_result.get('template_name', file_path.stem),
            'form_type': 'edit',
            'fields': fields,
            'actions': [f['name'] for f in uibinder_result.get('form_fields', [])
                       if f.get('widget_type') in ['Button', 'SubmitButton']],
            'validation_rules': [],
            'data_bindings': []
        }

    @retry(max_attempts=3, base_delay=1.0, exponential_base=2.0)
    def _extract_form_with_llm(
        self,
        file_path: Path,
        file_content: str,
        file_type: str,
    ) -> Optional[Dict[str, Any]]:
        """Extract form definition using LLM."""
        prompt = FORM_EXTRACTION_PROMPT_TEMPLATE.format(
            file_path=str(file_path),
            file_type=file_type,
            source_code=file_content[:15000],
        )

        response = self.ollama_client.call_ollama(
            prompt=prompt,
        )

        if not response or "response" not in response:
            raise ValueError("Empty response from LLM")

        response_text = response["response"]

        try:
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

    def _has_form(self, file_content: str) -> bool:
        """Check if file contains a form."""
        form_patterns = [
            r'<form',  # HTML/JSP form tag
            r'@UiField.*Form',  # GWT form field
            r'new\s+\w*Form\w*\(',  # JavaScript/GWT form instantiation
            r'FormPanel',  # GWT FormPanel
        ]

        for pattern in form_patterns:
            if re.search(pattern, file_content, re.IGNORECASE):
                return True
        return False

    def analyze_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Analyze a single frontend file."""
        self.logger.info(f"Analyzing: {file_path.name}")

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                file_content = f.read()

            file_type = self._detect_file_type(file_path)

            # Check if file has a form
            if not self._has_form(file_content):
                self.logger.info(f"No form found in {file_path.name}, skipping")
                return {"status": "skipped", "reason": "no_form"}

            # Fast path: Use GWT UiBinder parser for .ui.xml files
            llm_result = None
            if file_type == "GWT UiBinder" and self.uibinder_parser.can_analyze(file_path):
                self.logger.info(f"Using GWT UiBinder parser for {file_path.name}")
                try:
                    uibinder_result = self.uibinder_parser.parse(file_path, file_content)

                    # Convert UiBinder result to LLM-compatible format
                    llm_result = self._convert_uibinder_to_llm_format(uibinder_result, file_path)
                    self.logger.info(f"GWT UiBinder parser extracted {len(llm_result.get('fields', []))} fields")
                except Exception as e:
                    self.logger.warning(f"GWT UiBinder parser failed, falling back to LLM: {e}")
                    llm_result = None

            # Fallback: Extract form using LLM if parser didn't work
            if not llm_result:
                llm_result = self._extract_form_with_llm(
                    file_path=file_path,
                    file_content=file_content,
                    file_type=file_type,
                )

            if not llm_result:
                return {"status": "failed", "error": "No LLM result"}

            # Create FormDefinition
            form = self._create_form_definition(llm_result, file_path, file_type)

            # Extract business rules
            rules = self._extract_frontend_rules(llm_result, form, file_path)

            # Save to disk
            self._save_form(form)
            for rule in rules:
                self._save_business_rule(rule)

            # Record visit
            entry = FileVisitEntry(
                file_path=str(file_path),
                timestamp=datetime.now(),
                status=VisitStatus.SUCCESS,
                content_hash=self._compute_file_hash(file_path),
                layer=AnalysisLayer.FRONTEND,
                extracted_entities=[form.id],
            )
            self._append_visit_log(entry)

            self.logger.info(f"✓ Extracted form: {form.name}")

            return {
                "status": "success",
                "form": form,
                "rules": rules,
            }

        except Exception as e:
            self.logger.error(f"Failed to analyze {file_path}: {e}")

            entry = FileVisitEntry(
                file_path=str(file_path),
                timestamp=datetime.now(),
                status=VisitStatus.FAILED,
                content_hash=self._compute_file_hash(file_path),
                layer=AnalysisLayer.FRONTEND,
                error_message=str(e),
            )
            self._append_visit_log(entry)

            return {"status": "failed", "error": str(e)}

    def _create_form_definition(
        self, llm_result: Dict[str, Any], file_path: Path, file_type: str
    ) -> FormDefinition:
        """Create FormDefinition from LLM result."""
        # Determine form type
        form_type_str = llm_result.get("form_type", "html_form")
        form_type = FormType(form_type_str)

        # Parse fields
        fields = []
        for field_data in llm_result.get("fields", []):
            field = FormField(
                name=field_data["name"],
                type=field_data["type"],
                label=field_data.get("label"),
                required=field_data.get("required", False),
                validation_pattern=field_data.get("validation_pattern"),
                default_value=field_data.get("default_value"),
            )
            fields.append(field)

        form_name = llm_result.get("form_name", file_path.stem)
        form_id = f"{file_path.stem}_{form_name}"

        return FormDefinition(
            id=form_id,
            name=form_name,
            source_file=str(file_path),
            form_type=form_type,
            description=llm_result.get("description"),
            fields=fields,
            submission_endpoint=llm_result.get("submission_endpoint"),
            submission_method=llm_result.get("submission_method"),
            bound_entities=llm_result.get("bound_entities", []),
            created_at=datetime.now(),
        )

    def _extract_frontend_rules(
        self, llm_result: Dict[str, Any], form: FormDefinition, file_path: Path
    ) -> List[BusinessRule]:
        """Extract frontend business rules."""
        rules = []

        # Extract validation rules from fields
        for field in form.fields:
            if field.validation_pattern and field.required:
                rule_id = str(uuid4())

                rule = BusinessRule(
                    id=rule_id,
                    name=f"{field.name} Validation",
                    layer=RuleLayer.FRONTEND,
                    scope=RuleScope.FIELD,
                    rule_type=RuleType.VALIDATION,
                    description=f"Field '{field.name}' must match pattern: {field.validation_pattern}",
                    source_files=[str(file_path)],
                    enforcement_mechanism="Client-side JavaScript/HTML5 validation",
                    domain=form.domain,
                    created_at=datetime.now(),
                )
                rules.append(rule)

                # Add rule ID to form
                form.validation_rules.append(rule_id)

        return rules

    def _save_form(self, form: FormDefinition):
        """Save form definition to JSON file."""
        output_file = self.forms_dir / f"{form.name}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(form.to_dict(), f, indent=2)

    def _save_business_rule(self, rule: BusinessRule):
        """Save business rule to JSON file."""
        output_file = self.business_rules_dir / f"{rule.id}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(rule.to_dict(), f, indent=2)

    def analyze_frontend_layer(self) -> Dict[str, Any]:
        """Analyze all frontend files in parallel."""
        frontend_files = self.find_frontend_files()

        # Filter files that need analysis
        files_to_analyze = [f for f in frontend_files if self._should_analyze_file(f)]

        if not files_to_analyze:
            self.logger.info("No files to analyze (all up to date)")
            return {
                "total_files": len(frontend_files),
                "analyzed": 0,
                "skipped": len(frontend_files),
                "forms_extracted": 0,
                "components_found": 0,
                "rules_identified": 0,
            }

        self.logger.info(f"Analyzing {len(files_to_analyze)} files...")

        forms_extracted = 0
        rules_identified = 0
        failed = 0
        no_forms = 0

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self.analyze_file, file_path): file_path
                for file_path in files_to_analyze
            }

            for future in as_completed(futures):
                result = future.result()
                if result:
                    if result["status"] == "success":
                        forms_extracted += 1
                        rules_identified += len(result.get("rules", []))
                    elif result["status"] == "skipped":
                        no_forms += 1
                    else:
                        failed += 1

        return {
            "total_files": len(frontend_files),
            "analyzed": len(files_to_analyze),
            "skipped": len(frontend_files) - len(files_to_analyze),
            "forms_extracted": forms_extracted,
            "components_found": 0,  # Not implemented in this version
            "navigation_flows": 0,  # Not implemented in this version
            "rules_identified": rules_identified,
            "failed": failed,
            "no_forms": no_forms,
        }

    def load_gwt_artifacts_from_extraction(
        self,
        extraction_file: Path,
        project_id: Optional[str] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Load GWT artifacts from extraction results file.

        Args:
            extraction_file: Path to extraction-results.jsonl
            project_id: Optional project filter

        Returns:
            Dictionary with lists of artifacts by role:
            {
                'presenters': [...],
                'views': [...],
                'ui_binders': [...],
                'rpc_servlets': [...],
                'shared_dtos': [...]
            }
        """
        self.logger.info(f"Loading GWT artifacts from {extraction_file}")

        gwt_artifacts = {
            'presenters': [],
            'views': [],
            'ui_binders': [],
            'rpc_servlets': [],
            'shared_dtos': []
        }

        if not extraction_file.exists():
            self.logger.warning(f"Extraction file not found: {extraction_file}")
            return gwt_artifacts

        try:
            with open(extraction_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue

                    # Skip summary line
                    if line_num == 1:
                        continue

                    try:
                        artifact = json.loads(line)

                        # Filter by project if specified
                        if project_id:
                            # Handle project ID with or without hash suffix
                            artifact_project = artifact.get('project_id', '')
                            if not (artifact_project == project_id or
                                   artifact_project.startswith(f"{project_id}:")):
                                continue

                        # Check if artifact has GWT metadata
                        semantic_data = artifact.get('semantic_data', {})
                        gwt_role = semantic_data.get('gwt_role')

                        if gwt_role == 'presenter':
                            gwt_artifacts['presenters'].append(artifact)
                        elif gwt_role == 'view':
                            gwt_artifacts['views'].append(artifact)
                        elif gwt_role == 'ui_binder':
                            gwt_artifacts['ui_binders'].append(artifact)
                        elif gwt_role == 'rpc_servlet':
                            gwt_artifacts['rpc_servlets'].append(artifact)
                        elif gwt_role == 'shared_dto':
                            gwt_artifacts['shared_dtos'].append(artifact)

                    except json.JSONDecodeError as e:
                        self.logger.warning(f"Invalid JSON at line {line_num}: {e}")
                        continue
                    except Exception as e:
                        self.logger.warning(f"Error processing line {line_num}: {e}")
                        continue

            total = sum(len(v) for v in gwt_artifacts.values())
            self.logger.info(f"Loaded {total} GWT artifacts: "
                           f"{len(gwt_artifacts['presenters'])} presenters, "
                           f"{len(gwt_artifacts['views'])} views, "
                           f"{len(gwt_artifacts['ui_binders'])} UiBinders, "
                           f"{len(gwt_artifacts['rpc_servlets'])} RPC servlets, "
                           f"{len(gwt_artifacts['shared_dtos'])} DTOs")

            return gwt_artifacts

        except Exception as e:
            self.logger.error(f"Failed to load GWT artifacts: {e}", exc_info=True)
            return gwt_artifacts

    def convert_gwt_presenter_to_component(self, artifact: Dict[str, Any]) -> UIComponent:
        """Convert GWT Presenter artifact to UIComponent."""
        semantic = artifact.get('semantic_data', {})
        file_path = artifact.get('file_path', '')

        # Extract event handlers
        events = []
        for handler_data in semantic.get('event_handlers', []):
            if isinstance(handler_data, dict):
                event = Event(
                    name=handler_data.get('name', ''),
                    type=handler_data.get('trigger', 'click'),  # Fixed: use 'type' not 'trigger'
                    handler=handler_data.get('handler', ''),
                    description=handler_data.get('description', '')
                )
                events.append(event)

        # Extract data bindings from RPC calls
        data_bindings = []
        for rpc in semantic.get('rpc_calls', []):
            if isinstance(rpc, dict):
                binding = DataBinding(
                    field_name=rpc.get('method', ''),  # Fixed: use 'field_name' not 'source'
                    data_source=rpc.get('service', ''),  # Fixed: use 'data_source' not 'target'
                    binding_type='rpc_call'
                )
                data_bindings.append(binding)

        # Extract navigation targets
        navigation_targets = []
        for nav in semantic.get('navigation_logic', []):
            if isinstance(nav, dict):
                navigation_targets.append(nav.get('target', ''))

        component_id = f"gwt_presenter_{Path(file_path).stem}"

        return UIComponent(
            id=component_id,
            name=semantic.get('presenter_name', Path(file_path).stem),
            source_file=file_path,  # Fixed: use 'source_file' not 'file_path'
            component_type=ComponentType.GWT_PRESENTER,
            created_at=datetime.now(),  # Fixed: add required created_at
            description=semantic.get('summary', ''),
            events_handled=events,  # Fixed: use 'events_handled' not 'events'
            data_bindings=data_bindings,
            navigation_targets=navigation_targets
            # Note: metadata removed as it's not a valid parameter
        )

    def convert_gwt_view_to_component(self, artifact: Dict[str, Any]) -> UIComponent:
        """Convert GWT View artifact to UIComponent."""
        semantic = artifact.get('semantic_data', {})
        file_path = artifact.get('file_path', '')

        # Extract UI fields as data bindings
        data_bindings = []
        for field in semantic.get('ui_fields', []):
            if isinstance(field, dict):
                binding = DataBinding(
                    field_name=field.get('field_name', ''),  # Fixed: use 'field_name' not 'source'
                    data_source=field.get('widget_type', ''),  # Fixed: use 'data_source' not 'target'
                    binding_type='ui_field'
                )
                data_bindings.append(binding)

        component_id = f"gwt_view_{Path(file_path).stem}"

        return UIComponent(
            id=component_id,
            name=semantic.get('view_name', Path(file_path).stem),
            source_file=file_path,  # Fixed: use 'source_file' not 'file_path'
            component_type=ComponentType.GWT_VIEW,
            created_at=datetime.now(),  # Fixed: add required created_at
            description=semantic.get('summary', ''),
            data_bindings=data_bindings
            # Note: metadata removed as it's not a valid parameter
        )

    def convert_gwt_uibinder_to_form(self, artifact: Dict[str, Any]) -> FormDefinition:
        """Convert GWT UiBinder artifact to FormDefinition."""
        semantic = artifact.get('semantic_data', {})
        file_path = artifact.get('file_path', '')

        # Widget type to form field type mapping
        widget_type_map = {
            'TextBox': 'text',
            'PasswordTextBox': 'password',
            'TextArea': 'textarea',
            'IntegerBox': 'number',
            'DoubleBox': 'number',
            'ListBox': 'select',
            'CheckBox': 'checkbox',
            'RadioButton': 'radio',
            'DateBox': 'date',
            'Button': 'button',
            'SubmitButton': 'submit'
        }

        # Convert form fields
        fields = []
        for field_data in semantic.get('form_fields', []):
            if isinstance(field_data, dict):
                widget_type = field_data.get('widget_type', 'TextBox')
                field_type = widget_type_map.get(widget_type, 'text')

                field = FormField(
                    name=field_data.get('field_name', ''),
                    type=field_type,
                    label=field_data.get('label', ''),
                    required='*' in field_data.get('label', ''),
                    validation_pattern=None,
                    default_value=field_data.get('default_value')
                )
                fields.append(field)

        # Skip UiBinders without form fields (they're templates, not forms)
        if not fields:
            return None

        form_id = f"gwt_form_{Path(file_path).stem}"

        return FormDefinition(
            id=form_id,
            name=semantic.get('template_name', Path(file_path).stem),
            source_file=file_path,
            form_type=FormType.GWT_FORM,
            fields=fields,
            created_at=datetime.now(),  # Fixed: add required created_at
            description=semantic.get('summary', ''),
            submission_endpoint=None,  # UiBinder templates don't specify endpoints
            submission_method=None,
            bound_entities=[]
        )

    def process_gwt_artifacts(
        self,
        extraction_file: Path,
        project_id: Optional[str] = None
    ) -> Dict[str, int]:
        """
        Load and process GWT artifacts from extraction file.

        Args:
            extraction_file: Path to extraction-results.jsonl
            project_id: Optional project filter

        Returns:
            Dictionary with counts of processed artifacts
        """
        self.logger.info("Processing GWT artifacts for PRD generation...")

        # Load GWT artifacts
        gwt_artifacts = self.load_gwt_artifacts_from_extraction(extraction_file, project_id)

        counts = {
            'presenters': 0,
            'views': 0,
            'ui_binders': 0,
            'total_components': 0,
            'total_forms': 0
        }

        # Process presenters
        for artifact in gwt_artifacts['presenters']:
            try:
                component = self.convert_gwt_presenter_to_component(artifact)
                self._save_ui_component(component)
                counts['presenters'] += 1
                counts['total_components'] += 1
            except Exception as e:
                self.logger.error(f"Failed to convert presenter {artifact.get('file_path')}: {e}")

        # Process views
        for artifact in gwt_artifacts['views']:
            try:
                component = self.convert_gwt_view_to_component(artifact)
                self._save_ui_component(component)
                counts['views'] += 1
                counts['total_components'] += 1
            except Exception as e:
                self.logger.error(f"Failed to convert view {artifact.get('file_path')}: {e}")

        # Process UiBinders
        for artifact in gwt_artifacts['ui_binders']:
            try:
                form = self.convert_gwt_uibinder_to_form(artifact)
                if form:  # Skip if no form fields
                    self._save_form(form)
                    counts['ui_binders'] += 1
                    counts['total_forms'] += 1
            except Exception as e:
                self.logger.error(f"Failed to convert UiBinder {artifact.get('file_path')}: {e}")

        self.logger.info(f"Processed {counts['total_components']} GWT components "
                        f"and {counts['total_forms']} forms")

        return counts

    def _save_ui_component(self, component: UIComponent):
        """Save UI component to JSON file."""
        component_file = self.components_dir / f"{component.id}.json"
        try:
            with open(component_file, 'w', encoding='utf-8') as f:
                json.dump(component.to_dict(), f, indent=2, default=str)
        except Exception as e:
            self.logger.error(f"Failed to save component {component.id}: {e}")
