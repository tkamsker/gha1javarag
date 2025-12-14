# LLM Prompt and Response Contracts: PRD Document Generation

**Feature**: 002-prd-document-generation
**Date**: 2025-12-14
**Phase**: Phase 1 - Contracts

## Overview

This document defines the contracts for all LLM (Ollama) interactions during PRD generation. It specifies prompt templates, expected JSON response schemas, validation rules, error handling, and retry strategies. All LLM calls use structured JSON output for reliable parsing.

## General LLM Configuration

### Connection Settings

| Parameter | Value | Description |
|-----------|-------|-------------|
| Base URL | `$OLLAMA_URL` | Ollama service endpoint (default: http://localhost:11434) |
| Model | `$OLLAMA_MODEL_NAME` | Model name (default: gemma3:12b) |
| Timeout | 120 seconds | Per-request timeout (configurable via --llm-timeout) |
| Max Retries | 3 | Maximum retry attempts (configurable via --llm-retries) |
| Retry Backoff | Exponential | 2^n seconds (1s, 2s, 4s, 8s, ...) |

### Request Format

All LLM requests use the Ollama `/api/generate` endpoint with JSON mode:

```bash
POST http://localhost:11434/api/generate
Content-Type: application/json

{
  "model": "gemma3:12b",
  "prompt": "{detailed prompt}",
  "format": "json",
  "stream": false,
  "options": {
    "temperature": 0.2,
    "top_p": 0.9,
    "num_predict": 2048
  }
}
```

### Response Format

Expected Ollama response structure:

```json
{
  "model": "gemma3:12b",
  "created_at": "2025-12-14T10:30:15Z",
  "response": "{JSON string containing structured output}",
  "done": true,
  "context": [...],
  "total_duration": 1234567890,
  "load_duration": 123456789,
  "prompt_eval_count": 45,
  "prompt_eval_duration": 234567890,
  "eval_count": 156,
  "eval_duration": 876543210
}
```

The `response` field contains a JSON string that must be parsed and validated.

---

## Database Layer Analysis

### 1. DAO Entity Extraction Prompt

**Purpose**: Extract database entity information from DAO classes or JPA entities.

**Trigger**: When analyzing a Java file with DAO naming patterns or JPA annotations.

**Context Provided**:
- File content (source code)
- File path
- Detected ORM framework (JPA, iBATIS, Hibernate)
- Related files (entity classes, mapper XMLs)

**Prompt Template**:

```
You are analyzing a Java DAO (Data Access Object) or JPA entity class to extract database structure information.

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
{
  "entity_name": "string",
  "qualified_name": "schema.table or null",
  "columns": [
    {
      "name": "string",
      "data_type": "string (e.g., VARCHAR(255), INTEGER, TIMESTAMP)",
      "nullable": boolean,
      "default_value": "string or null",
      "description": "string"
    }
  ],
  "primary_key": ["column_name"],
  "foreign_keys": [
    {
      "column_name": "string",
      "referenced_table": "string",
      "referenced_column": "string",
      "on_delete": "string or null",
      "on_update": "string or null"
    }
  ],
  "indexes": [
    {
      "name": "string",
      "columns": ["string"],
      "unique": boolean,
      "index_type": "string or null"
    }
  ],
  "constraints": [
    {
      "name": "string",
      "type": "CHECK | UNIQUE | NOT NULL",
      "definition": "string"
    }
  ],
  "business_rules": [
    {
      "name": "string",
      "description": "string",
      "enforcement": "string (how it's enforced)"
    }
  ],
  "description": "string (2-3 sentence description)",
  "estimated_row_count": "small | medium | large | massive or null",
  "domain": "string (business domain like auth, billing, reporting) or null"
}

IMPORTANT:
- Infer data types from JPA annotations (@Column(length=255) → VARCHAR(255), @Temporal → TIMESTAMP, etc.)
- For iBATIS/MyBatis, extract from result maps and SQL statements
- If information is not available, use null
- Be specific in descriptions, avoid generic statements
- Include any validation annotations as business_rules
```

**Expected Response Schema**:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["entity_name", "columns", "description"],
  "properties": {
    "entity_name": {"type": "string"},
    "qualified_name": {"type": ["string", "null"]},
    "columns": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "data_type", "nullable"],
        "properties": {
          "name": {"type": "string"},
          "data_type": {"type": "string"},
          "nullable": {"type": "boolean"},
          "default_value": {"type": ["string", "null"]},
          "description": {"type": "string"}
        }
      },
      "minItems": 1
    },
    "primary_key": {"type": "array", "items": {"type": "string"}},
    "foreign_keys": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["column_name", "referenced_table", "referenced_column"],
        "properties": {
          "column_name": {"type": "string"},
          "referenced_table": {"type": "string"},
          "referenced_column": {"type": "string"},
          "on_delete": {"type": ["string", "null"]},
          "on_update": {"type": ["string", "null"]}
        }
      }
    },
    "indexes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "columns"],
        "properties": {
          "name": {"type": "string"},
          "columns": {"type": "array", "items": {"type": "string"}},
          "unique": {"type": "boolean"},
          "index_type": {"type": ["string", "null"]}
        }
      }
    },
    "constraints": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "type", "definition"],
        "properties": {
          "name": {"type": "string"},
          "type": {"type": "string", "enum": ["CHECK", "UNIQUE", "NOT NULL"]},
          "definition": {"type": "string"}
        }
      }
    },
    "business_rules": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "description", "enforcement"],
        "properties": {
          "name": {"type": "string"},
          "description": {"type": "string"},
          "enforcement": {"type": "string"}
        }
      }
    },
    "description": {"type": "string"},
    "estimated_row_count": {"type": ["string", "null"]},
    "domain": {"type": ["string", "null"]}
  }
}
```

**Example Response**:

```json
{
  "entity_name": "user",
  "qualified_name": "public.user",
  "columns": [
    {
      "name": "id",
      "data_type": "BIGINT",
      "nullable": false,
      "default_value": null,
      "description": "Primary key, auto-generated sequence"
    },
    {
      "name": "email",
      "data_type": "VARCHAR(255)",
      "nullable": false,
      "default_value": null,
      "description": "User email address, must be unique"
    },
    {
      "name": "password_hash",
      "data_type": "VARCHAR(255)",
      "nullable": false,
      "default_value": null,
      "description": "Bcrypt hashed password"
    },
    {
      "name": "created_at",
      "data_type": "TIMESTAMP",
      "nullable": false,
      "default_value": "CURRENT_TIMESTAMP",
      "description": "Account creation timestamp"
    }
  ],
  "primary_key": ["id"],
  "foreign_keys": [],
  "indexes": [
    {
      "name": "idx_user_email",
      "columns": ["email"],
      "unique": true,
      "index_type": "BTREE"
    }
  ],
  "constraints": [
    {
      "name": "chk_email_format",
      "type": "CHECK",
      "definition": "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\\\.[A-Z|a-z]{2,}$'"
    }
  ],
  "business_rules": [
    {
      "name": "Email Uniqueness",
      "description": "Each user must have a unique email address",
      "enforcement": "Unique index on email column"
    },
    {
      "name": "Password Hashing",
      "description": "Passwords must be hashed with bcrypt before storage",
      "enforcement": "Service layer (UserService.hashPassword())"
    }
  ],
  "description": "Stores user account information including credentials, profile data, and audit timestamps. Central entity for authentication and authorization in the system.",
  "estimated_row_count": "medium",
  "domain": "auth"
}
```

**Validation Rules**:
1. entity_name must not be empty
2. At least one column must be defined
3. All column names must be non-empty strings
4. If foreign_keys present, columns and referenced tables must be valid
5. description should be 2-3 sentences (50-500 characters)

**Error Handling**:
- If response is not valid JSON, retry with clarified prompt
- If required fields missing, retry with explicit field requirements
- After 3 retries, mark file as failed in visit log with error details

---

### 2. SQL Query Business Rule Extraction Prompt

**Purpose**: Analyze complex SQL queries (in mapper XML or SQL files) to infer business rules and relationships.

**Trigger**: When analyzing iBATIS/MyBatis mapper XML or standalone SQL files.

**Prompt Template**:

```
You are analyzing a SQL query or stored procedure to extract business rules and database relationships.

FILE: {file_path}
QUERY TYPE: {query_type (SELECT/INSERT/UPDATE/DELETE/PROCEDURE)}

SQL CODE:
```sql
{sql_code}
```

CONTEXT:
- Tables involved: {tables_from_query}
- Related entities already discovered: {related_entities}

TASK:
Extract the following information in JSON format:

1. **purpose**: What this query does (1-2 sentences)
2. **tables_accessed**: List of table names referenced in the query
3. **business_rules**: List of business rules enforced or implemented by this query (joins, WHERE conditions, CASE logic, calculations, etc.)
4. **relationships**: Any foreign key relationships or table joins discovered
5. **performance_notes**: Any performance considerations (indexes needed, potential bottlenecks, etc.)

RESPONSE FORMAT (JSON):
{
  "purpose": "string",
  "tables_accessed": ["string"],
  "business_rules": [
    {
      "name": "string",
      "description": "string",
      "sql_fragment": "string (relevant SQL snippet)"
    }
  ],
  "relationships": [
    {
      "from_table": "string",
      "from_column": "string",
      "to_table": "string",
      "to_column": "string",
      "relationship_type": "one_to_many | many_to_one | many_to_many | one_to_one"
    }
  ],
  "performance_notes": ["string"]
}
```

**Expected Response Schema**: (Similar structure to above, see schema definitions)

---

## Service Layer Analysis

### 3. Service Definition Extraction Prompt

**Purpose**: Extract service class structure, operations, dependencies, and business logic.

**Trigger**: When analyzing a Java service class (naming pattern or annotations like @Service, @Component).

**Prompt Template**:

```
You are analyzing a Java service class to document its business operations and dependencies.

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
{
  "class_name": "string",
  "qualified_name": "string",
  "service_type": "business_service | dao_service | integration_service | controller | rest_controller | utility_service",
  "description": "string (2-3 sentences)",
  "operations": [
    {
      "name": "string",
      "signature": "string (full method signature)",
      "return_type": "string",
      "parameters": [
        {
          "name": "string",
          "type": "string",
          "description": "string or null"
        }
      ],
      "description": "string (what this method does)",
      "throws": ["string (exception types)"],
      "annotations": ["string"],
      "line_number": integer or null
    }
  ],
  "dependencies": [
    {
      "target_service": "string (class name or qualified name)",
      "dependency_type": "injection | reference | static",
      "injection_method": "constructor | field | setter or null"
    }
  ],
  "data_dependencies": ["string (entity names)"],
  "business_rules": [
    {
      "name": "string",
      "description": "string",
      "enforcement": "string (how it's enforced)"
    }
  ],
  "transaction_boundaries": [
    {
      "method_name": "string",
      "transaction_type": "REQUIRED | REQUIRES_NEW | SUPPORTS | MANDATORY | NOT_SUPPORTED | NEVER",
      "propagation": "string or null",
      "isolation_level": "string or null",
      "read_only": boolean or null
    }
  ],
  "frameworks": ["string (Spring, EJB, etc.)"],
  "domain": "string (business domain) or null"
}

IMPORTANT:
- Focus on public methods (operations visible to other components)
- Infer data_dependencies from DAO method calls or entity class references
- Extract business logic from method implementations, not just method names
- Identify transaction boundaries from @Transactional or programmatic transaction management
```

**Expected Response Schema**: (See data-model.md for ServiceDefinition structure)

**Example Response**:

```json
{
  "class_name": "UserService",
  "qualified_name": "com.example.service.UserService",
  "service_type": "business_service",
  "description": "Manages user account lifecycle including registration, authentication, profile updates, and account deactivation. Coordinates with UserDAO for persistence and EmailService for notifications.",
  "operations": [
    {
      "name": "createUser",
      "signature": "public User createUser(UserRegistrationDTO dto) throws ValidationException, DuplicateEmailException",
      "return_type": "User",
      "parameters": [
        {
          "name": "dto",
          "type": "UserRegistrationDTO",
          "description": "User registration data with email, password, and profile info"
        }
      ],
      "description": "Creates a new user account after validating email uniqueness and password strength. Sends welcome email upon success.",
      "throws": ["ValidationException", "DuplicateEmailException"],
      "annotations": ["@Transactional", "@PreAuthorize(\"hasRole('ADMIN')\")"],
      "line_number": 45
    },
    {
      "name": "authenticateUser",
      "signature": "public AuthToken authenticateUser(String email, String password) throws AuthenticationException",
      "return_type": "AuthToken",
      "parameters": [
        {
          "name": "email",
          "type": "String",
          "description": "User email address"
        },
        {
          "name": "password",
          "type": "String",
          "description": "Plaintext password (hashed during authentication)"
        }
      ],
      "description": "Authenticates user credentials and returns JWT token on success.",
      "throws": ["AuthenticationException"],
      "annotations": [],
      "line_number": 78
    }
  ],
  "dependencies": [
    {
      "target_service": "UserDAO",
      "dependency_type": "injection",
      "injection_method": "constructor"
    },
    {
      "target_service": "EmailService",
      "dependency_type": "injection",
      "injection_method": "field"
    },
    {
      "target_service": "PasswordHasher",
      "dependency_type": "injection",
      "injection_method": "constructor"
    }
  ],
  "data_dependencies": ["user", "role", "permission"],
  "business_rules": [
    {
      "name": "Email Uniqueness Validation",
      "description": "Before creating a user, validate that email address is not already registered",
      "enforcement": "Query UserDAO.findByEmail(), throw DuplicateEmailException if exists"
    },
    {
      "name": "Password Strength Requirement",
      "description": "Passwords must be at least 8 characters with uppercase, lowercase, number, and special character",
      "enforcement": "PasswordValidator.validate() before hashing"
    }
  ],
  "transaction_boundaries": [
    {
      "method_name": "createUser",
      "transaction_type": "REQUIRED",
      "propagation": "REQUIRED",
      "isolation_level": "READ_COMMITTED",
      "read_only": false
    }
  ],
  "frameworks": ["Spring", "Spring Security"],
  "domain": "auth"
}
```

---

### 4. REST Endpoint Extraction Prompt

**Purpose**: Extract REST API endpoint details from controller classes.

**Trigger**: When analyzing a controller class with @RestController or @RequestMapping.

**Prompt Template**:

```
You are analyzing a REST controller to extract API endpoint definitions.

FILE: {file_path}
CONTROLLER CLASS: {class_name}

SOURCE CODE:
```java
{source_code}
```

RELATED SERVICES:
{related_services_summary}

TASK:
For each REST endpoint method, extract:

1. **http_method**: GET | POST | PUT | DELETE | PATCH
2. **path**: URL path (combine class-level and method-level @RequestMapping)
3. **operation_name**: Method name implementing this endpoint
4. **description**: What this endpoint does (1-2 sentences)
5. **request_format**: Request body structure, parameters (path/query/header/body)
6. **response_format**: Response structure, status codes
7. **authentication_required**: Whether authentication is required
8. **authorization_roles**: Required roles if any

RESPONSE FORMAT (JSON):
{
  "endpoints": [
    {
      "http_method": "GET | POST | PUT | DELETE | PATCH",
      "path": "string (e.g., /api/user/{id})",
      "operation_name": "string",
      "description": "string",
      "request_format": {
        "content_type": "string or null",
        "parameters": [
          {
            "name": "string",
            "location": "path | query | header | body",
            "type": "string",
            "required": boolean,
            "description": "string or null",
            "default_value": "string or null"
          }
        ],
        "schema_description": "string or null",
        "example": "string (JSON example) or null"
      },
      "response_format": {
        "content_type": "string",
        "status_codes": [
          {
            "code": integer,
            "description": "string",
            "response_type": "string or null"
          }
        ],
        "schema_description": "string or null",
        "example": "string or null"
      },
      "authentication_required": boolean,
      "authorization_roles": ["string"],
      "rate_limited": boolean,
      "deprecated": boolean,
      "produces": ["string"],
      "consumes": ["string"]
    }
  ]
}

IMPORTANT:
- Combine class-level @RequestMapping with method-level paths
- Infer authentication/authorization from @PreAuthorize, @Secured, etc.
- List all expected status codes (200, 400, 401, 404, 500, etc.)
- Provide example request/response JSON if possible
```

**Expected Response Schema**: (See data-model.md for APIEndpoint structure)

---

## Frontend Layer Analysis

### 5. JSP Form Extraction Prompt

**Purpose**: Extract form structure, fields, validation, and submission targets from JSP files.

**Trigger**: When analyzing JSP files containing `<form>` tags.

**Prompt Template**:

```
You are analyzing a JSP file to extract form definitions and user interface structure.

FILE: {file_path}

JSP CODE:
```jsp
{jsp_code}
```

RELATED ENDPOINTS (from service analysis):
{related_endpoints}

TASK:
For each form in the JSP, extract:

1. **name**: Form name or ID
2. **description**: What this form is used for
3. **fields**: List of form fields with name, label, type, validation
4. **submission_endpoint**: URL this form submits to (action attribute)
5. **submission_method**: GET | POST
6. **validation_rules**: Client-side validation rules (JavaScript, HTML5 constraints)
7. **bound_entities**: Database entities this form creates or updates (infer from field names and endpoint)

RESPONSE FORMAT (JSON):
{
  "forms": [
    {
      "name": "string",
      "description": "string",
      "fields": [
        {
          "name": "string",
          "label": "string or null",
          "type": "text | email | password | number | select | checkbox | textarea | date | file | hidden | etc.",
          "required": boolean,
          "validation_pattern": "string (regex or rule) or null",
          "validation_message": "string or null",
          "default_value": "string or null",
          "options": ["string (for select/radio)"] or null,
          "bound_column": "string (database column name) or null",
          "description": "string or null"
        }
      ],
      "submission_endpoint": "string (URL or endpoint ID)",
      "submission_method": "GET | POST",
      "validation_rules": [
        {
          "name": "string",
          "description": "string",
          "enforcement": "string (JavaScript function, HTML5 attribute, etc.)"
        }
      ],
      "bound_entities": ["string (entity names)"],
      "navigation_on_success": "string (URL or page name) or null",
      "navigation_on_cancel": "string or null",
      "security_patterns": ["string (CSRF token, input sanitization, etc.)"]
    }
  ]
}

IMPORTANT:
- Extract all input fields including hidden fields
- Identify validation from JavaScript, HTML5 attributes (required, pattern, min, max), or JSP tags
- Match submission_endpoint to known API endpoints if possible
- Infer bound_entities from field names matching database column names
```

**Expected Response Schema**: (See data-model.md for FormDefinition structure)

---

### 6. GWT Component Extraction Prompt

**Purpose**: Extract GWT widget, activity, and view structures.

**Trigger**: When analyzing GWT Java files (widgets, activities, views, presenters).

**Prompt Template**:

```
You are analyzing a GWT component to extract UI structure and responsibilities.

FILE: {file_path}
COMPONENT TYPE: {gwt_widget | gwt_activity | gwt_view | gwt_presenter}

SOURCE CODE:
```java
{source_code}
```

RELATED COMPONENTS:
{related_components}

TASK:
Extract the following information:

1. **name**: Component name
2. **component_type**: gwt_widget | gwt_activity | gwt_view | gwt_presenter
3. **description**: What this component does (2-3 sentences)
4. **responsibilities**: List of responsibilities (display data, handle events, navigate, etc.)
5. **events_handled**: UI events this component responds to
6. **events_emitted**: Events this component triggers
7. **data_bindings**: Data this component displays or modifies
8. **navigation_targets**: Places or views this component navigates to
9. **child_components**: Child widgets or components
10. **related_forms**: Forms used by this component

RESPONSE FORMAT (JSON):
{
  "name": "string",
  "component_type": "gwt_widget | gwt_activity | gwt_view | gwt_presenter",
  "description": "string",
  "responsibilities": ["string"],
  "events_handled": [
    {
      "name": "string",
      "type": "click | change | submit | load | etc.",
      "handler": "string (method name) or null",
      "description": "string or null"
    }
  ],
  "events_emitted": [
    {
      "name": "string",
      "type": "string",
      "description": "string or null"
    }
  ],
  "data_bindings": [
    {
      "field_name": "string",
      "data_source": "string (model/service/API)",
      "bound_entity": "string (DatabaseEntity ID) or null",
      "binding_type": "one_way | two_way"
    }
  ],
  "navigation_targets": ["string (place names or URLs)"],
  "child_components": ["string (component names or IDs)"],
  "related_forms": ["string (form IDs)"]
}
```

**Expected Response Schema**: (See data-model.md for UIComponent structure)

---

## PRD Generation

### 7. Executive Summary Generation Prompt

**Purpose**: Generate high-level PRD executive summary from all analyzed artifacts.

**Trigger**: After all layers analyzed, when generating master PRD.

**Context Provided**:
- Count of entities, services, endpoints, forms, components
- Detected frameworks and technologies
- Business domains identified
- Key business rules
- Architectural patterns

**Prompt Template**:

```
You are generating an executive summary for a Product Requirements Document based on comprehensive codebase analysis.

SYSTEM OVERVIEW:
- **Database Entities**: {entity_count}
- **Services**: {service_count}
- **API Endpoints**: {endpoint_count}
- **UI Forms**: {form_count}
- **UI Components**: {component_count}
- **Business Rules**: {rule_count}

TECHNOLOGIES:
{technologies_list}

DOMAINS:
{domains_list}

KEY ENTITIES:
{top_entities_summary}

KEY SERVICES:
{top_services_summary}

TASK:
Write a comprehensive executive summary (3-5 paragraphs) covering:

1. **System Purpose**: What does this system do? Who uses it?
2. **Architecture Overview**: High-level architectural patterns (layered, MVC, microservices, etc.)
3. **Technology Stack**: Key technologies and frameworks used
4. **Business Domains**: Main business areas covered (authentication, billing, reporting, etc.)
5. **Key Capabilities**: Most important features and operations
6. **Integration Points**: External systems or APIs integrated

RESPONSE FORMAT (JSON):
{
  "executive_summary": "string (3-5 paragraphs, markdown formatted)",
  "key_findings": [
    "string (bullet points of notable findings)"
  ],
  "architectural_patterns": ["string"],
  "technology_stack": {
    "backend": ["string"],
    "frontend": ["string"],
    "database": ["string"],
    "frameworks": ["string"]
  },
  "primary_domains": ["string"]
}

IMPORTANT:
- Write in business-friendly language (avoid excessive technical jargon)
- Focus on capabilities and value, not implementation details
- Highlight any notable architectural decisions or patterns
- Be specific (e.g., "Implements role-based access control with 5 predefined roles" not "Has security")
```

**Expected Response Schema**:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["executive_summary", "key_findings", "architectural_patterns", "technology_stack", "primary_domains"],
  "properties": {
    "executive_summary": {"type": "string", "minLength": 100},
    "key_findings": {"type": "array", "items": {"type": "string"}},
    "architectural_patterns": {"type": "array", "items": {"type": "string"}},
    "technology_stack": {
      "type": "object",
      "properties": {
        "backend": {"type": "array", "items": {"type": "string"}},
        "frontend": {"type": "array", "items": {"type": "string"}},
        "database": {"type": "array", "items": {"type": "string"}},
        "frameworks": {"type": "array", "items": {"type": "string"}}
      }
    },
    "primary_domains": {"type": "array", "items": {"type": "string"}}
  }
}
```

---

### 8. Cross-Layer Flow Generation Prompt

**Purpose**: Generate end-to-end flow documentation showing UI → Service → Database.

**Trigger**: When generating cross-references section of master PRD.

**Context Provided**:
- Form definitions with submission_endpoint
- API endpoints with service_id
- Service definitions with data_dependencies
- Database entities

**Prompt Template**:

```
You are documenting an end-to-end user flow from frontend form submission through backend service to database.

FORM:
{form_json}

SUBMISSION ENDPOINT:
{endpoint_json}

IMPLEMENTING SERVICE:
{service_json}

DATABASE ENTITIES ACCESSED:
{entities_json}

TASK:
Generate a step-by-step flow description showing how this user action flows through the system layers.

RESPONSE FORMAT (JSON):
{
  "flow_name": "string (e.g., User Registration Flow)",
  "description": "string (1-2 sentences)",
  "steps": [
    {
      "step_number": integer,
      "layer": "frontend | service | database",
      "component": "string (form name, service name, table name)",
      "action": "string (what happens at this step)",
      "details": "string (additional details)"
    }
  ],
  "business_rules_applied": ["string (rule IDs or names)"],
  "mermaid_diagram": "string (Mermaid sequence diagram code or null)"
}

IMPORTANT:
- Start from user action (form submission)
- Follow through each layer (frontend → endpoint → service → database)
- Include business rules applied at each step
- Generate a Mermaid sequence diagram if possible
```

**Expected Response Schema**: (See above)

**Example Response**:

```json
{
  "flow_name": "User Registration Flow",
  "description": "End-to-end flow for new user account creation from registration form submission to database persistence.",
  "steps": [
    {
      "step_number": 1,
      "layer": "frontend",
      "component": "user_registration.jsp",
      "action": "User fills registration form and submits",
      "details": "Form includes email, password, first name, last name fields. Client-side validation checks email format and password strength."
    },
    {
      "step_number": 2,
      "layer": "frontend",
      "component": "user_registration.jsp",
      "action": "Form submits POST request to /api/user/create",
      "details": "CSRF token included in request header for security."
    },
    {
      "step_number": 3,
      "layer": "service",
      "component": "UserController.createUser()",
      "action": "Controller receives request and validates input",
      "details": "Checks required fields, email format, password strength (BR_001, BR_003)."
    },
    {
      "step_number": 4,
      "layer": "service",
      "component": "UserService.createUser()",
      "action": "Business service validates email uniqueness",
      "details": "Queries UserDAO.findByEmail() to ensure email not already registered (BR_002)."
    },
    {
      "step_number": 5,
      "layer": "service",
      "component": "UserService.createUser()",
      "action": "Service hashes password using bcrypt",
      "details": "PasswordHasher.hash() generates bcrypt hash with salt."
    },
    {
      "step_number": 6,
      "layer": "database",
      "component": "user table",
      "action": "Insert new user record",
      "details": "Transaction begins. User entity inserted with auto-generated ID. Database enforces email uniqueness constraint."
    },
    {
      "step_number": 7,
      "layer": "service",
      "component": "EmailService.sendWelcomeEmail()",
      "action": "Send welcome email to new user",
      "details": "Asynchronous email sent via email service."
    },
    {
      "step_number": 8,
      "layer": "service",
      "component": "UserController.createUser()",
      "action": "Return HTTP 201 Created with user ID",
      "details": "Transaction commits successfully."
    },
    {
      "step_number": 9,
      "layer": "frontend",
      "component": "user_registration.jsp",
      "action": "Redirect user to login page",
      "details": "Success message displayed: 'Registration successful. Please log in.'"
    }
  ],
  "business_rules_applied": ["BR_001_email_validation", "BR_002_email_uniqueness", "BR_003_password_strength"],
  "mermaid_diagram": "sequenceDiagram\n    participant User\n    participant Form as user_registration.jsp\n    participant Controller as UserController\n    participant Service as UserService\n    participant DAO as UserDAO\n    participant DB as Database\n    participant Email as EmailService\n    User->>Form: Fill form and submit\n    Form->>Controller: POST /api/user/create\n    Controller->>Controller: Validate input (BR_001, BR_003)\n    Controller->>Service: createUser(dto)\n    Service->>DAO: findByEmail(email)\n    DAO->>DB: SELECT * FROM user WHERE email=?\n    DB-->>DAO: No results\n    DAO-->>Service: null (email available)\n    Service->>Service: Hash password (bcrypt)\n    Service->>DAO: insert(user)\n    DAO->>DB: INSERT INTO user VALUES (...)\n    DB-->>DAO: ID=123\n    DAO-->>Service: User object\n    Service->>Email: sendWelcomeEmail(user)\n    Service-->>Controller: User object\n    Controller-->>Form: 201 Created {id: 123}\n    Form-->>User: Redirect to login page"
}
```

---

## Error Handling and Retry Strategies

### Retry Conditions

Retry LLM calls if:
1. **Connection Error**: Cannot connect to Ollama service
2. **Timeout**: Request exceeds timeout duration (default: 120s)
3. **Invalid JSON**: Response is not parseable JSON
4. **Missing Required Fields**: Response JSON missing required fields
5. **Schema Validation Failure**: Response JSON doesn't match expected schema

### Retry Strategy

- **Max Retries**: 3 (configurable via --llm-retries)
- **Backoff**: Exponential (2^n seconds: 1s, 2s, 4s, 8s, ...)
- **Retry Prompt Adjustment**:
  - On invalid JSON: Add "IMPORTANT: Respond ONLY with valid JSON, no additional text"
  - On missing fields: Add "IMPORTANT: Include all required fields: {field_list}"
  - On schema failure: Add example of expected structure

### Failure Handling

After max retries exhausted:
1. Log error with file path and error details
2. Mark file as `failed` in visit log with error_message
3. Continue with next file (do not abort entire analysis)
4. Report failures in final summary

---

## LLM Response Validation

### Validation Steps

1. **Parse JSON**: Attempt to parse response as JSON
2. **Schema Validation**: Validate against expected JSON schema
3. **Required Fields**: Check all required fields present
4. **Data Type Validation**: Validate field types (string, integer, boolean, array, etc.)
5. **Enum Validation**: Validate enum fields match allowed values
6. **Content Validation**: Check content makes sense (e.g., description not empty, column count > 0)

### Confidence Scoring

Assign confidence score (0.0 to 1.0) based on:
- LLM response includes specific details (high confidence)
- LLM response includes "I'm not sure", "possibly", "maybe" (medium confidence)
- LLM response very generic or vague (low confidence)
- Missing optional but important fields (lower confidence)

**Threshold**: Flag responses with confidence < 0.6 for manual review.

---

## Performance Optimization

### Batching

- **Small Files**: Batch multiple small files (<200 lines) into single LLM call
- **Large Files**: Process large files (>2000 lines) individually, possibly in chunks

### Caching

- **Content Hash Cache**: Cache LLM responses by SHA-256 hash of input (file content)
- **Cache Location**: `output/.llm_cache/` directory with hash-named JSON files
- **Cache Invalidation**: Clear cache on model change or prompt template change

### Parallel Execution

- **Concurrency**: Process up to MAX_CONCURRENT_AI_CALLS files in parallel (default: 10)
- **Rate Limiting**: Respect Ollama service capacity (adjust concurrency if timeouts occur)
- **Progress Tracking**: Report progress across all parallel tasks

---

## Testing LLM Contracts

### Unit Tests

```bash
pytest tests/unit/test_llm_prompts.py
pytest tests/unit/test_llm_response_validation.py
```

### Integration Tests

```bash
pytest tests/integration/test_llm_extraction.py --slow
```

### Manual Testing

```bash
# Test individual prompt on sample file
python scripts/test_llm_prompt.py --prompt dao_extraction --file tests/fixtures/UserDAO.java
```

---

## See Also

- `cli-interface.md` - CLI command specification
- `output-formats.md` - Output file format specifications
- `data-model.md` - Entity definitions
- `quickstart.md` - Usage examples
