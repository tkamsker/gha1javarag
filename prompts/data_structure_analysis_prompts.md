# Data Structure Analysis Prompts

## Field Analysis Prompt

```
Analyze the following Java code and extract detailed field information for all data structures, forms, and UI components.

### Code to Analyze:
{code_content}

### Required Output Format:
```json
{
  "classes": [
    {
      "name": "ClassName",
      "type": "class", 
      "fields": [
        {
          "name": "fieldName",
          "type": "FieldType",
          "annotations": ["@Annotation"],
          "is_collection": false,
          "is_relationship": false,
          "validation_rules": ["required", "unique", "email_format"],
          "database_type": "VARCHAR(255)",
          "constraints": ["NOT NULL", "UNIQUE"]
        }
      ],
      "form_fields": [
        {
          "name": "fieldName",
          "input_type": "textbox",
          "validation": ["required", "email"],
          "ui_component": "TextBox"
        }
      ]
    }
  ]
}
```

### Focus Areas:
1. Extract ALL fields with their exact types and annotations
2. Identify form input fields and their validation rules
3. Determine database mapping requirements
4. Identify UI component types (GWT widgets)
5. Extract validation annotations and business rules
6. Map relationships between entities

### Important:
- Be comprehensive - don't miss any fields
- Include both class fields and form fields
- Identify GWT UI component types accurately
- Extract validation rules from annotations and code
- Do NOT include conversation markers
- Provide clean, structured JSON output
```

## UI Component Analysis Prompt

```
Analyze the following Java/GWT code and extract comprehensive UI component information.

### Code to Analyze:
{code_content}

### Required Output Format:
```json
{
  "ui_components": [
    {
      "name": "ComponentName",
      "type": "gwt_composite",
      "widgets": [
        {
          "name": "widgetName",
          "type": "Button|TextBox|Grid|DialogBox|etc",
          "purpose": "Description of widget purpose",
          "interactions": ["click", "selection", "input"],
          "validation": ["client_side_rules"]
        }
      ],
      "form_fields": [
        {
          "name": "fieldName",
          "type": "String|Integer|etc", 
          "required": true,
          "validation_rules": ["required", "email_format", "phone_format"],
          "ui_widget": "TextBox|DatePicker|etc"
        }
      ],
      "user_interactions": ["click_handler", "selection_handler", "form_submission"],
      "backend_services": ["service_name_inferred_from_usage"],
      "business_domain": "customer|billing|product|admin"
    }
  ]
}
```

### Analysis Focus:
1. Identify all GWT widgets and their types
2. Extract form fields with validation rules
3. Map user interactions and event handlers  
4. Infer required backend services from UI operations
5. Determine business domain from context
6. Extract UI behavior patterns

### Important:
- Analyze @UiField annotations to identify widgets
- Extract @UiHandler methods for interactions
- Infer backend service needs from UI operations
- Be specific about widget types (Button, Grid, TextBox, etc.)
- Include validation rules from both annotations and code logic
- Do NOT include conversation artifacts
```

## Database Schema Generation Prompt

```
Based on the following field analysis, generate comprehensive database schema requirements.

### Field Analysis:
{field_analysis}

### UI Components:
{ui_components}

### Required Output:
Generate detailed database schema with:

1. **Table Definitions**
   - Table name (derived from class name)
   - All fields with appropriate SQL types
   - Primary keys and foreign keys
   - Constraints (NOT NULL, UNIQUE, CHECK, etc.)

2. **Data Types Mapping**
   - Java String → VARCHAR(255) or TEXT
   - Java Integer → INTEGER
   - Java Date → TIMESTAMP
   - Custom types → Appropriate SQL types

3. **Validation Rules**
   - Field-level constraints
   - Business rule constraints
   - Reference integrity constraints

4. **Indexing Strategy**
   - Primary key indexes
   - Foreign key indexes
   - Search field indexes (for common queries)
   - Composite indexes where needed

5. **Sample DDL**
   - CREATE TABLE statements
   - ALTER TABLE for constraints
   - CREATE INDEX statements

### Focus:
- Be comprehensive and specific
- Include all fields identified in the analysis
- Map validation rules to database constraints
- Consider performance implications
- Provide production-ready DDL
- Do NOT include AI conversation artifacts
```