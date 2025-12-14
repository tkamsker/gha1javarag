# Data Model: PRD Document Generation from Codebase Analysis

**Feature**: 002-prd-document-generation
**Date**: 2025-12-14
**Phase**: Phase 1 - Data Model Design

## Overview

This document defines the data entities, relationships, and validation rules for the PRD Document Generation feature. The model extends the existing Feature 001 artifacts (Project, CodeArtifact) and introduces new entities to support bottom-up analysis from database through services to frontend, with comprehensive document generation.

## Entity Hierarchy

```
Existing (Feature 001):
  Project → CodeArtifact[]

New (Feature 002):
  VisitLog
    └─> FileVisitEntry[]

  DatabaseEntity[]
    └─> BusinessRule[] (database-level)

  ServiceDefinition[]
    └─> APIEndpoint[]
    └─> BusinessRule[] (service-level)

  FormDefinition[]
    └─> FormField[]
    └─> BusinessRule[] (frontend-level)

  UIComponent[]
    └─> NavigationFlow[]

  PRDSection[]
    ├─> DatabasePRD (extends PRDSection)
    ├─> ServicePRD (extends PRDSection)
    ├─> FrontendPRD (extends PRDSection)
    └─> MasterPRD (aggregates all)

  IndexEntry[] (for each layer: database, services, frontend)
```

## Core Entities

### 1. DatabaseEntity

**Purpose**: Represents a database table or entity discovered from DAO classes, ORM mappings, or SQL files. This is the foundation of bottom-up analysis.

**Lifecycle**: Created during database layer analysis, enriched with LLM descriptions, persisted to JSON, referenced in PRD generation.

**Storage**: JSON file in `output/database/entities/`

**Fields**:

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| id | string | Yes | Unique identifier (table name or qualified name) | Max 200 chars, alphanumeric + underscore |
| name | string | Yes | Table or entity name | Max 200 chars |
| qualified_name | string | No | Schema-qualified name (schema.table) | Max 500 chars |
| source_type | string | Yes | Where discovered (jpa_annotation, ibatis_xml, sql_file, hibernate_mapping) | Enum: see below |
| source_files | string[] | Yes | Paths to files where entity was found | Valid file paths |
| columns | Column[] | Yes | List of columns/fields | At least 1 column |
| primary_key | string[] | No | Column names forming primary key | Must reference existing columns |
| foreign_keys | ForeignKey[] | No | Relationships to other entities | Valid references |
| indexes | Index[] | No | Database indexes | - |
| constraints | Constraint[] | No | Check constraints, unique constraints | - |
| business_rules | string[] | No | References to BusinessRule IDs | Valid BusinessRule IDs |
| description | string | No | LLM-generated description of entity purpose | Max 2000 chars |
| estimated_row_count | string | No | Estimate or category (small, medium, large, massive) | - |
| domain | string | No | Business domain (billing, auth, reporting, etc.) | Max 100 chars |
| created_at | datetime | Yes | When entity was analyzed | ISO 8601 |

**Nested Types**:

```python
Column:
  name: string (required, max 100 chars)
  data_type: string (required, max 100 chars, e.g., VARCHAR(255), INTEGER, TIMESTAMP)
  nullable: boolean (default: true)
  default_value: string (optional)
  description: string (optional, max 500 chars)

ForeignKey:
  column_name: string (required)
  referenced_table: string (required)
  referenced_column: string (required)
  on_delete: string (optional, CASCADE/SET NULL/RESTRICT/NO ACTION)
  on_update: string (optional)

Index:
  name: string (required)
  columns: string[] (required)
  unique: boolean (default: false)
  index_type: string (optional, BTREE/HASH/etc.)

Constraint:
  name: string (required)
  type: string (required, CHECK/UNIQUE/NOT NULL)
  definition: string (required)
```

**Relationships**:
- Has many BusinessRule (via business_rules array)
- Referenced by ServiceDefinition (data_dependencies)
- Referenced by FormDefinition (bound_entities)

**Validation Rules**:
- At least one column must be defined
- primary_key columns must exist in columns array
- foreign_keys must reference valid column names
- source_type must be from allowed enum
- If qualified_name is set, it should follow schema.table format

**State Transitions**:
```
DISCOVERED → ANALYZING (LLM processing) → DOCUMENTED → INDEXED_IN_PRD
                ↓
             FAILED (analysis error)
```

---

### 2. BusinessRule

**Purpose**: Represents a validation, constraint, or business logic pattern discovered in code. Can be at database, service, or frontend layer.

**Lifecycle**: Created during layer-specific analysis (database/service/frontend), enriched with LLM, persisted to JSON, referenced in PRD.

**Storage**: JSON file in `output/business_rules/`

**Fields**:

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| id | string | Yes | Unique identifier (generated UUID or hash) | UUID format |
| name | string | Yes | Short name/label for the rule | Max 200 chars |
| layer | string | Yes | Where rule is enforced | Enum: database, service, frontend, cross_layer |
| scope | string | Yes | Scope of enforcement | Enum: field, entity, transaction, application |
| rule_type | string | Yes | Type of rule | Enum: validation, constraint, calculation, workflow, authorization, business_logic |
| description | string | Yes | Natural language description of the rule | Max 2000 chars |
| source_files | string[] | Yes | Files where rule is implemented | Valid file paths |
| source_code_snippets | CodeSnippet[] | No | Relevant code excerpts | - |
| related_entities | string[] | No | DatabaseEntity or ServiceDefinition IDs | Valid entity IDs |
| conditions | string | No | Rule conditions/triggers | Max 1000 chars |
| enforcement_mechanism | string | No | How rule is enforced (annotation, SQL constraint, JS validation) | Max 500 chars |
| severity | string | No | Impact if violated | Enum: critical, high, medium, low |
| security_relevant | boolean | No | Is this a security-related rule? | Default: false |
| domain | string | No | Business domain | Max 100 chars |
| created_at | datetime | Yes | When rule was extracted | ISO 8601 |

**Nested Types**:

```python
CodeSnippet:
  file_path: string (required)
  line_start: integer (required, >= 1)
  line_end: integer (required, >= line_start)
  code_text: string (required, max 2000 chars)
  language: string (required)
```

**Relationships**:
- Referenced by DatabaseEntity (business_rules)
- Referenced by ServiceDefinition (business_rules)
- Referenced by FormDefinition (validation_rules)
- Can reference other BusinessRules (related_rules, for duplication detection)

**Validation Rules**:
- layer must be from allowed enum
- scope must be from allowed enum
- At least one source file must be provided
- If security_relevant is true, should include enforcement_mechanism
- severity if present must be from enum

**State Transitions**: Same as DatabaseEntity (DISCOVERED → ANALYZING → DOCUMENTED → INDEXED_IN_PRD)

---

### 3. ServiceDefinition

**Purpose**: Represents a backend service class with its operations, dependencies, and exposed endpoints.

**Lifecycle**: Created during service layer analysis, enriched with LLM, persisted to JSON, referenced in PRD.

**Storage**: JSON file in `output/services/definitions/`

**Fields**:

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| id | string | Yes | Unique identifier (qualified class name) | Max 500 chars |
| class_name | string | Yes | Simple class name | Max 200 chars |
| qualified_name | string | Yes | Fully qualified class name | Max 500 chars |
| package | string | Yes | Java package | Max 500 chars |
| source_file | string | Yes | Path to service class file | Valid file path |
| service_type | string | Yes | Type of service | Enum: business_service, dao_service, integration_service, controller, rest_controller, utility_service |
| description | string | No | LLM-generated description of service purpose | Max 2000 chars |
| operations | ServiceOperation[] | Yes | Public methods/operations | At least 1 operation |
| dependencies | ServiceDependency[] | No | Injected dependencies or referenced services | - |
| data_dependencies | string[] | No | DatabaseEntity IDs accessed by this service | Valid DatabaseEntity IDs |
| endpoints | string[] | No | APIEndpoint IDs exposed by this service | Valid APIEndpoint IDs |
| business_rules | string[] | No | BusinessRule IDs implemented | Valid BusinessRule IDs |
| transaction_boundaries | TransactionInfo[] | No | Transaction management details | - |
| frameworks | string[] | No | Framework annotations (Spring, EJB, etc.) | - |
| domain | string | No | Business domain | Max 100 chars |
| created_at | datetime | Yes | When service was analyzed | ISO 8601 |

**Nested Types**:

```python
ServiceOperation:
  name: string (required, max 200 chars)
  signature: string (required, max 1000 chars, full method signature)
  return_type: string (required)
  parameters: Parameter[] (optional)
  description: string (optional, max 1000 chars)
  throws: string[] (optional, exception types)
  annotations: string[] (optional)
  line_number: integer (optional)

Parameter:
  name: string (required)
  type: string (required)
  description: string (optional)

ServiceDependency:
  target_service: string (required, class name or ID)
  dependency_type: string (required, injection/reference/static)
  injection_method: string (optional, constructor/field/setter)

TransactionInfo:
  method_name: string (required)
  transaction_type: string (required, REQUIRED/REQUIRES_NEW/SUPPORTS/etc.)
  propagation: string (optional)
  isolation_level: string (optional)
  read_only: boolean (optional)
```

**Relationships**:
- Has many APIEndpoint (via endpoints)
- Has many BusinessRule (via business_rules)
- References DatabaseEntity (via data_dependencies)
- References other ServiceDefinition (via dependencies)
- Referenced by FormDefinition (submission_service)

**Validation Rules**:
- qualified_name must be valid Java class name format
- At least one operation must be defined
- service_type must be from allowed enum
- endpoints must reference valid APIEndpoint IDs
- data_dependencies must reference valid DatabaseEntity IDs

---

### 4. APIEndpoint

**Purpose**: Represents a REST or SOAP endpoint exposed by backend services.

**Lifecycle**: Created during service analysis, enriched with LLM, persisted to JSON, referenced in PRD.

**Storage**: JSON file in `output/services/endpoints/`

**Fields**:

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| id | string | Yes | Unique identifier (method:path) | Max 500 chars |
| http_method | string | Yes | HTTP method | Enum: GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS |
| path | string | Yes | URL path or pattern | Max 500 chars, valid URL path |
| service_id | string | Yes | ServiceDefinition ID implementing this endpoint | Valid ServiceDefinition ID |
| operation_name | string | Yes | Service method handling this endpoint | Max 200 chars |
| description | string | No | LLM-generated endpoint description | Max 2000 chars |
| request_format | RequestFormat | No | Request structure | - |
| response_format | ResponseFormat | No | Response structure | - |
| authentication_required | boolean | No | Requires authentication | Default: true |
| authorization_roles | string[] | No | Required roles/permissions | - |
| rate_limited | boolean | No | Has rate limiting | Default: false |
| deprecated | boolean | No | Is deprecated | Default: false |
| produces | string[] | No | Media types produced (application/json, etc.) | - |
| consumes | string[] | No | Media types consumed | - |
| source_file | string | Yes | File where endpoint is defined | Valid file path |
| created_at | datetime | Yes | When endpoint was analyzed | ISO 8601 |

**Nested Types**:

```python
RequestFormat:
  content_type: string (required)
  schema_description: string (optional, max 1000 chars)
  parameters: EndpointParameter[] (optional)
  example: string (optional, max 2000 chars, JSON/XML example)

ResponseFormat:
  content_type: string (required)
  status_codes: StatusCode[] (required)
  schema_description: string (optional, max 1000 chars)
  example: string (optional, max 2000 chars)

EndpointParameter:
  name: string (required)
  location: string (required, path/query/header/body)
  type: string (required)
  required: boolean (required)
  description: string (optional)
  default_value: string (optional)

StatusCode:
  code: integer (required, 100-599)
  description: string (required)
  response_type: string (optional)
```

**Relationships**:
- Belongs to one ServiceDefinition (via service_id)
- Referenced by FormDefinition (submission_endpoint)

**Validation Rules**:
- http_method must be valid HTTP verb
- path must start with / or be a valid URL pattern
- service_id must reference existing ServiceDefinition
- response_format should define at least one status code

---

### 5. FormDefinition

**Purpose**: Represents a UI form discovered in JSP, HTML, or GWT code with its fields and validation.

**Lifecycle**: Created during frontend analysis, enriched with LLM, persisted to JSON, referenced in PRD.

**Storage**: JSON file in `output/frontend/forms/`

**Fields**:

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| id | string | Yes | Unique identifier (file_path + form_id/name) | Max 500 chars |
| name | string | Yes | Form name or identifier | Max 200 chars |
| source_file | string | Yes | File containing form | Valid file path |
| form_type | string | Yes | Type of form implementation | Enum: jsp_form, html_form, gwt_form, react_form, javascript_form |
| description | string | No | LLM-generated form purpose | Max 2000 chars |
| fields | FormField[] | Yes | Form fields | At least 1 field |
| submission_endpoint | string | No | APIEndpoint ID or URL this form submits to | Valid APIEndpoint ID or URL |
| submission_method | string | No | HTTP method for submission | Enum: GET, POST |
| submission_service | string | No | ServiceDefinition ID handling submission | Valid ServiceDefinition ID |
| validation_rules | string[] | No | BusinessRule IDs for client-side validation | Valid BusinessRule IDs |
| bound_entities | string[] | No | DatabaseEntity IDs this form creates/updates | Valid DatabaseEntity IDs |
| navigation_on_success | string | No | Where user goes after successful submission | Max 500 chars |
| navigation_on_cancel | string | No | Where user goes on cancel | Max 500 chars |
| security_patterns | string[] | No | Security features (CSRF protection, input sanitization) | - |
| domain | string | No | Business domain | Max 100 chars |
| created_at | datetime | Yes | When form was analyzed | ISO 8601 |

**Nested Types**:

```python
FormField:
  name: string (required, max 100 chars, field name/ID)
  label: string (optional, user-visible label)
  type: string (required, text/email/password/number/select/checkbox/textarea/date/file/etc.)
  required: boolean (default: false)
  validation_pattern: string (optional, regex or validation rule)
  validation_message: string (optional)
  default_value: string (optional)
  options: string[] (optional, for select/radio fields)
  bound_column: string (optional, DatabaseEntity column this maps to)
  description: string (optional, max 500 chars)
```

**Relationships**:
- References APIEndpoint (via submission_endpoint)
- References ServiceDefinition (via submission_service)
- References DatabaseEntity (via bound_entities)
- References BusinessRule (via validation_rules)

**Validation Rules**:
- At least one field must be defined
- form_type must be from allowed enum
- submission_endpoint if present must be valid APIEndpoint ID or URL
- fields[].type should be from standard HTML/form types
- bound_entities must reference valid DatabaseEntity IDs

---

### 6. UIComponent

**Purpose**: Represents a frontend component (GWT widget, JavaScript module, React component) with responsibilities and event handling.

**Lifecycle**: Created during frontend analysis, enriched with LLM, persisted to JSON, referenced in PRD.

**Storage**: JSON file in `output/frontend/components/`

**Fields**:

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| id | string | Yes | Unique identifier (qualified component name) | Max 500 chars |
| name | string | Yes | Component name | Max 200 chars |
| component_type | string | Yes | Type of component | Enum: gwt_widget, gwt_activity, gwt_view, gwt_presenter, js_module, js_class, react_component, vue_component |
| source_file | string | Yes | File containing component | Valid file path |
| description | string | No | LLM-generated component purpose | Max 2000 chars |
| responsibilities | string[] | No | What this component does | - |
| events_handled | Event[] | No | UI events this component responds to | - |
| events_emitted | Event[] | No | Events this component triggers | - |
| data_bindings | DataBinding[] | No | Data this component displays or modifies | - |
| navigation_targets | string[] | No | NavigationFlow IDs initiated by this component | Valid NavigationFlow IDs |
| child_components | string[] | No | UIComponent IDs of child components | Valid UIComponent IDs |
| parent_component | string | No | UIComponent ID of parent | Valid UIComponent ID |
| related_forms | string[] | No | FormDefinition IDs used by this component | Valid FormDefinition IDs |
| framework_annotations | string[] | No | Framework-specific annotations or decorators | - |
| domain | string | No | Business domain | Max 100 chars |
| created_at | datetime | Yes | When component was analyzed | ISO 8601 |

**Nested Types**:

```python
Event:
  name: string (required, max 100 chars)
  type: string (required, click/change/submit/load/etc.)
  handler: string (optional, method name)
  description: string (optional, max 500 chars)

DataBinding:
  field_name: string (required)
  data_source: string (required, model/service/API)
  bound_entity: string (optional, DatabaseEntity ID)
  binding_type: string (required, one_way/two_way)
```

**Relationships**:
- Has many FormDefinition (via related_forms)
- Has many NavigationFlow (via navigation_targets)
- Self-referential (parent_component, child_components)

**Validation Rules**:
- component_type must be from allowed enum
- navigation_targets must reference valid NavigationFlow IDs
- child_components must reference valid UIComponent IDs

---

### 7. NavigationFlow

**Purpose**: Represents a user journey through multiple pages or screens with transitions.

**Lifecycle**: Created during frontend analysis, enriched with LLM, persisted to JSON, referenced in PRD.

**Storage**: JSON file in `output/frontend/navigation/`

**Fields**:

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| id | string | Yes | Unique identifier (generated or meaningful name) | Max 500 chars |
| name | string | Yes | Flow name | Max 200 chars |
| description | string | No | LLM-generated flow description | Max 2000 chars |
| entry_points | EntryPoint[] | Yes | How users enter this flow | At least 1 entry point |
| steps | NavigationStep[] | Yes | Ordered steps in the flow | At least 1 step |
| exit_points | ExitPoint[] | No | How users exit this flow | - |
| flow_type | string | Yes | Type of flow | Enum: linear, branching, loop, wizard, modal |
| related_forms | string[] | No | FormDefinition IDs in this flow | Valid FormDefinition IDs |
| related_components | string[] | No | UIComponent IDs in this flow | Valid UIComponent IDs |
| business_process | string | No | High-level business process this supports | Max 500 chars |
| domain | string | No | Business domain | Max 100 chars |
| created_at | datetime | Yes | When flow was analyzed | ISO 8601 |

**Nested Types**:

```python
EntryPoint:
  entry_type: string (required, direct_url/link/button/menu_item)
  source: string (required, URL or source component/page)
  description: string (optional)

NavigationStep:
  step_number: integer (required, >= 1)
  page_url: string (optional)
  component_id: string (optional, UIComponent ID)
  form_id: string (optional, FormDefinition ID)
  action: string (required, what happens at this step)
  next_step_conditions: Condition[] (optional, for branching)

ExitPoint:
  exit_type: string (required, success/cancel/error/timeout)
  destination: string (optional, where user goes)
  description: string (optional)

Condition:
  condition_expression: string (required)
  next_step: integer (required, step number)
```

**Relationships**:
- References FormDefinition (via related_forms)
- References UIComponent (via related_components)

**Validation Rules**:
- At least one entry point must be defined
- At least one step must be defined
- steps should be sequentially numbered
- flow_type must be from allowed enum

---

### 8. VisitLog

**Purpose**: Tracks which files have been analyzed to enable incremental processing and avoid duplicate work.

**Lifecycle**: Created/updated throughout all analysis phases, persisted as JSON Lines file, loaded at start of next run.

**Storage**: JSON Lines file at `output/.visit_log.jsonl`

**Format**: One JSON object per line, each representing a FileVisitEntry

**FileVisitEntry Structure**:

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| file_path | string | Yes | Absolute path to analyzed file | Valid file path |
| timestamp | datetime | Yes | When file was last analyzed | ISO 8601 |
| status | string | Yes | Analysis result | Enum: success, failed, skipped, in_progress |
| content_hash | string | Yes | SHA-256 hash of file contents | 64 hex chars |
| layer | string | Yes | Which layer analysis was performed | Enum: database, service, frontend, cross_layer |
| analysis_type | string | No | Specific analysis performed | Max 100 chars (e.g., dao_extraction, form_parsing) |
| error_message | string | No | If status=failed, what went wrong | Max 1000 chars |
| duration_seconds | float | No | How long analysis took | >= 0 |
| extracted_entities | string[] | No | IDs of entities extracted from this file | - |

**Relationships**:
- Not directly linked to other entities but extracted_entities contains IDs referencing DatabaseEntity, ServiceDefinition, etc.

**Validation Rules**:
- file_path must be absolute path
- content_hash must be valid SHA-256 (64 hex chars)
- status must be from allowed enum
- layer must be from allowed enum
- timestamp must be valid ISO 8601

**Usage**:
- Before analyzing a file, check if it exists in VisitLog with matching content_hash
- If hash matches and status=success, skip reanalysis
- If hash differs, update entry and reanalyze
- Append new entry to .jsonl file after each file analysis

---

### 9. IndexEntry

**Purpose**: Entry in a hierarchical index file pointing to detailed documentation with metadata.

**Lifecycle**: Created when generating layer-specific index.md files, persisted as markdown, used for navigation.

**Storage**: Markdown files at `output/database/index.md`, `output/services/index.md`, `output/frontend/index.md`

**Fields** (logical structure, rendered as markdown):

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Entry title/name |
| link | string | Yes | Relative path to detailed doc file |
| entity_type | string | Yes | Type of entity (table, service, form, etc.) |
| domain | string | No | Business domain |
| category | string | No | Grouping category |
| description | string | No | Brief description |
| metadata | dict | No | Additional key-value metadata |

**Markdown Rendering Example**:

```markdown
## Database Entities

### Authentication Domain

- **[User](entities/user.md)** (Table) - User account information with credentials
- **[Role](entities/role.md)** (Table) - User roles for authorization
- **[Permission](entities/permission.md)** (Table) - Granular permissions

### Billing Domain

- **[Invoice](entities/invoice.md)** (Table) - Customer invoices with line items
- **[Payment](entities/payment.md)** (Table) - Payment transactions and status
```

**Relationships**:
- References DatabaseEntity, ServiceDefinition, FormDefinition, UIComponent, etc. via links

**Validation Rules**:
- link must be valid relative path to existing markdown file
- entity_type should correspond to actual entity being linked

---

### 10. PRDSection

**Purpose**: A section of the final PRD document with title, content, and cross-references. Base type for layer-specific PRD documents.

**Lifecycle**: Created during PRD generation, enriched with LLM synthesis, persisted as markdown.

**Storage**: Markdown files in `output/prd/`

**Fields**:

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| id | string | Yes | Unique section identifier | Max 200 chars |
| title | string | Yes | Section title | Max 200 chars |
| level | integer | Yes | Heading level (1-6) | 1 to 6 |
| content | string | Yes | Markdown content of section | Max 50000 chars |
| section_type | string | Yes | Type of section | Enum: summary, data_model, business_logic, ui_design, architecture, cross_references, gaps, appendix |
| cross_references | CrossReference[] | No | Links to other sections or entities | - |
| metadata | dict | No | Additional section metadata | - |
| order | integer | Yes | Display order within parent | >= 0 |
| parent_section | string | No | Parent section ID for hierarchy | Valid PRDSection ID |
| created_at | datetime | Yes | When section was generated | ISO 8601 |

**Nested Types**:

```python
CrossReference:
  target_type: string (required, section/entity/service/form/etc.)
  target_id: string (required)
  link_text: string (required)
  description: string (optional)
```

**Specialized Subtypes**:

**DatabasePRD** (extends PRDSection):
- Contains sections for: Overview, Entity Catalog, Relationships Diagram, Business Rules, Data Dictionary
- Links to DatabaseEntity[] and BusinessRule[]
- File: `output/prd/database_prd.md`

**ServicePRD** (extends PRDSection):
- Contains sections for: Overview, Service Catalog, API Endpoints, Dependencies Graph, Business Operations
- Links to ServiceDefinition[], APIEndpoint[], BusinessRule[]
- File: `output/prd/service_prd.md`

**FrontendPRD** (extends PRDSection):
- Contains sections for: Overview, Component Hierarchy, Forms Catalog, Navigation Flows, User Journeys
- Links to FormDefinition[], UIComponent[], NavigationFlow[]
- File: `output/prd/frontend_prd.md`

**MasterPRD** (extends PRDSection):
- Contains sections for: Executive Summary, Architecture Overview, Cross-Layer Flows, Consolidated Business Rules, Gaps and Recommendations
- Aggregates all layer PRDs with cross-references
- File: `output/prd/master_prd.md`

**Relationships**:
- Self-referential (parent_section for hierarchical sections)
- References all entity types via cross_references

**Validation Rules**:
- level must be 1-6
- section_type must be from allowed enum
- order must be non-negative
- parent_section if present must reference valid PRDSection ID

---

## Enumerations and Controlled Vocabularies

### Source Types (DatabaseEntity)

```python
SOURCE_TYPES = [
    "jpa_annotation",       # JPA @Entity, @Table, @Column
    "ibatis_xml",          # iBATIS/MyBatis mapper XML
    "sql_file",            # SQL DDL files
    "hibernate_mapping",   # Hibernate HBM XML
    "dao_code",            # Inferred from DAO method calls
]
```

### Service Types (ServiceDefinition)

```python
SERVICE_TYPES = [
    "business_service",     # Business logic service
    "dao_service",          # Data access service
    "integration_service",  # External system integration
    "controller",           # MVC controller (non-REST)
    "rest_controller",      # REST API controller
    "utility_service",      # Utility/helper service
]
```

### Form Types (FormDefinition)

```python
FORM_TYPES = [
    "jsp_form",            # JSP-based form
    "html_form",           # Static HTML form
    "gwt_form",            # GWT form panel
    "react_form",          # React form component
    "javascript_form",     # JavaScript-generated form
]
```

### Component Types (UIComponent)

```python
COMPONENT_TYPES = [
    "gwt_widget",          # GWT Widget subclass
    "gwt_activity",        # GWT Activity
    "gwt_view",            # GWT View interface/impl
    "gwt_presenter",       # GWT Presenter
    "js_module",           # JavaScript module
    "js_class",            # JavaScript class/prototype
    "react_component",     # React component
    "vue_component",       # Vue component
]
```

### Flow Types (NavigationFlow)

```python
FLOW_TYPES = [
    "linear",              # Sequential steps (wizard)
    "branching",           # Conditional branches
    "loop",                # Repeating steps
    "wizard",              # Multi-step form wizard
    "modal",               # Modal dialog flow
]
```

### Analysis Layers

```python
ANALYSIS_LAYERS = [
    "database",            # Database layer analysis
    "service",             # Service layer analysis
    "frontend",            # Frontend layer analysis
    "cross_layer",         # Cross-layer analysis (PRD generation)
]
```

### Visit Status (VisitLog)

```python
VISIT_STATUS = [
    "success",             # Successfully analyzed
    "failed",              # Analysis failed
    "skipped",             # Intentionally skipped (binary, generated, etc.)
    "in_progress",         # Currently being analyzed
]
```

### Rule Types (BusinessRule)

```python
RULE_TYPES = [
    "validation",          # Input validation rule
    "constraint",          # Database or field constraint
    "calculation",         # Calculation or formula
    "workflow",            # Workflow or state transition
    "authorization",       # Authorization/permission rule
    "business_logic",      # General business logic
]
```

### Rule Layers (BusinessRule)

```python
RULE_LAYERS = [
    "database",            # Enforced at DB level
    "service",             # Enforced in service layer
    "frontend",            # Enforced in UI
    "cross_layer",         # Enforced across multiple layers
]
```

## State Transitions

### Analysis Pipeline States

```
NOT_STARTED → DATABASE_ANALYSIS → SERVICE_ANALYSIS → FRONTEND_ANALYSIS → PRD_GENERATION → COMPLETED
                    ↓                    ↓                    ↓                 ↓
                 FAILED               FAILED               FAILED            FAILED
```

### File Visit States (VisitLog)

```
NOT_VISITED → IN_PROGRESS → SUCCESS
                    ↓
                 FAILED → (can retry) → IN_PROGRESS
                    ↓
                SKIPPED (binary, generated, etc.)
```

### Entity Documentation States

```
DISCOVERED → ANALYZING (LLM enrichment) → DOCUMENTED → INDEXED_IN_PRD → PUBLISHED
                    ↓
                FAILED (retry or manual review)
```

## Data Integrity Rules

### Referential Integrity

1. ServiceDefinition.data_dependencies MUST reference existing DatabaseEntity IDs
2. FormDefinition.submission_endpoint MUST reference existing APIEndpoint ID (if set)
3. FormDefinition.bound_entities MUST reference existing DatabaseEntity IDs
4. BusinessRule.related_entities MUST reference valid entity IDs
5. Cross-references in PRDSection MUST point to existing entities or sections
6. VisitLog entries SHOULD be unique by file_path (latest entry wins)

### Idempotency Rules

1. Re-analyzing same file with unchanged content_hash → skip analysis, reuse results
2. Re-analyzing same file with changed content_hash → update entities, update VisitLog
3. Re-generating PRD with unchanged entities → regenerate markdown, update timestamps
4. Entity IDs MUST be deterministic based on qualified names or paths

### Validation on Write

1. All required fields must be present
2. Enums must match controlled vocabularies
3. Foreign key references must exist (entity IDs)
4. Dates must be valid ISO 8601
5. Hashes must be valid SHA-256 hex strings (64 chars)
6. File paths must be valid absolute paths
7. Markdown content must be well-formed (basic validation)

## Cross-Layer Analysis

### Bottom-Up Flow

1. **Database Layer** → Extract DatabaseEntity[] and database-level BusinessRule[]
2. **Service Layer** → Extract ServiceDefinition[] and APIEndpoint[], link to DatabaseEntity via data_dependencies
3. **Frontend Layer** → Extract FormDefinition[] and UIComponent[], link to APIEndpoint and DatabaseEntity
4. **PRD Generation** → Synthesize all layers, identify cross-layer flows, consolidate duplicate rules

### Cross-Reference Graph

```
FormDefinition
    ├─> submission_endpoint (APIEndpoint)
    ├─> submission_service (ServiceDefinition)
    ├─> bound_entities (DatabaseEntity[])
    └─> validation_rules (BusinessRule[])

APIEndpoint
    └─> service_id (ServiceDefinition)

ServiceDefinition
    ├─> data_dependencies (DatabaseEntity[])
    └─> business_rules (BusinessRule[])

DatabaseEntity
    └─> business_rules (BusinessRule[])
```

## Performance Optimizations

### Incremental Analysis

1. **VisitLog Check**: Before analyzing file, check if file_path exists with matching content_hash
2. **Skip Unchanged**: If hash matches and status=success, skip analysis entirely
3. **Update Changed**: If hash differs, update VisitLog entry and reanalyze
4. **Batch Writes**: Write VisitLog entries in batches (every 10 files or 10 seconds)

### LLM Call Optimization

1. **Batch Prompts**: Group multiple small files into single LLM call when possible
2. **Caching**: Cache LLM responses by content_hash to avoid re-calling for identical files
3. **Timeout & Retry**: 120 second timeout per call, max 3 retries with exponential backoff
4. **Parallel Calls**: Process up to MAX_CONCURRENT_AI_CALLS files in parallel (default: 10)

### Memory Management

1. **Streaming**: Never load all entities into memory; process and write incrementally
2. **Chunking**: For large files, process in chunks and aggregate results
3. **Lazy Loading**: Load entities from disk only when needed for cross-referencing

## File Organization

```
output/
├── .visit_log.jsonl                    # Visit log (append-only)
├── database/
│   ├── index.md                        # Database layer index
│   ├── entities/
│   │   ├── user.json                   # DatabaseEntity
│   │   ├── invoice.json
│   │   └── ...
│   └── schema_diagram.md               # Optional: auto-generated ER diagram
├── services/
│   ├── index.md                        # Service layer index
│   ├── definitions/
│   │   ├── UserService.json            # ServiceDefinition
│   │   ├── BillingService.json
│   │   └── ...
│   └── endpoints/
│       ├── POST_api_user_create.json   # APIEndpoint
│       └── ...
├── frontend/
│   ├── index.md                        # Frontend layer index
│   ├── forms/
│   │   ├── user_registration.json      # FormDefinition
│   │   └── ...
│   ├── components/
│   │   ├── UserListView.json           # UIComponent
│   │   └── ...
│   └── navigation/
│       ├── user_registration_flow.json # NavigationFlow
│       └── ...
├── business_rules/
│   ├── index.md                        # Business rules index
│   ├── BR_001_email_validation.json    # BusinessRule
│   ├── BR_002_user_age_constraint.json
│   └── ...
└── prd/
    ├── index.md                        # Master PRD index/TOC
    ├── master_prd.md                   # MasterPRD (synthesized)
    ├── database_prd.md                 # DatabasePRD
    ├── service_prd.md                  # ServicePRD
    ├── frontend_prd.md                 # FrontendPRD
    └── cross_references.md             # Cross-layer flow documentation
```

## Next Steps

1. Define CLI interface contract (contracts/cli-prd-interface.md)
2. Define output file format contracts (contracts/output-formats.md)
3. Define LLM prompt/response contracts (contracts/llm-contracts.md)
4. Create quickstart guide (quickstart.md)
5. Implement Python dataclasses for each entity
6. Create validation functions for each entity
7. Implement serialization/deserialization for JSON and markdown
