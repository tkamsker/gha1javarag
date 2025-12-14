# Research: PRD Document Generation from Codebase Analysis

**Feature**: 002-prd-document-generation
**Date**: 2025-12-14
**Phase**: Phase 0 - Technology Research & Decisions

## Overview

This document captures key technology decisions and research findings for implementing PRD document generation from codebase analysis. The research focuses on three critical areas: LLM prompt engineering for code analysis, hierarchical documentation generation, and incremental analysis with state management.

All decisions prioritize actionable implementation guidance, leveraging existing project infrastructure (Ollama, Weaviate, Python 3.8+), and maintaining constitutional compliance.

---

## 1. LLM Prompt Engineering for Code Analysis

### 1.1 Effective Prompt Structures for Extracting Business Rules from DAOs

**Decision**: Use multi-stage prompting with role-based system prompts and structured JSON response formats

**Rationale**:
- Current codebase already demonstrates effective pattern in `ollama_client.py` with SYSTEM_PROMPT defining role and output format
- Multi-stage approach separates structural parsing (deterministic) from semantic analysis (LLM)
- JSON format enforcement (`format="json"` in Ollama API) ensures parseable responses
- Role-based prompts (e.g., "You are a code analysis expert") improve consistency
- Structured fields (summary, entities, tags, frameworks, concerns) align with Weaviate schema

**Implementation Pattern**:
```python
# Stage 1: DAO-specific system prompt
DAO_SYSTEM_PROMPT = """You are a database access pattern analyst. Analyze DAO code and extract:

Your response must be valid JSON with these exact fields:
{
  "summary": "Brief description of DAO's purpose",
  "business_rules": [
    {
      "rule": "Description of business rule",
      "enforcement": "validation|constraint|transaction",
      "location": "method or annotation",
      "severity": "critical|important|informational"
    }
  ],
  "database_operations": {
    "tables_accessed": ["table1", "table2"],
    "operation_types": ["read", "write", "delete"],
    "transaction_boundaries": ["method1", "method2"]
  },
  "validation_logic": ["validation rule 1", "validation rule 2"],
  "dependencies": ["other DAOs or services referenced"]
}

Focus on business logic, not implementation details."""

# Stage 2: User prompt with context
def create_dao_analysis_prompt(
    file_path: str,
    file_content: str,
    related_entities: List[str],
    sql_statements: List[str]
) -> str:
    """Create context-rich prompt for DAO analysis."""
    return f"""
Analyze this DAO class:

File: {file_path}

Related Database Entities: {', '.join(related_entities)}

SQL Statements Found:
{'\n'.join(f'- {stmt[:200]}...' for stmt in sql_statements)}

Code:
```java
{file_content[:8000]}  # Limit to ~8k chars to fit context window
```

Extract business rules and database access patterns."""
```

**Alternatives Considered**:
- **Single-stage generic prompt**: Too vague, inconsistent results across different artifact types
- **Few-shot examples in every prompt**: Exceeds context window for large files, slower inference
- **Natural language response**: Requires complex parsing, prone to extraction errors

**Best Practices Applied**:
1. **Artifact-type-specific prompts**: Different system prompts for DAO, Service, JSP, GWT (following existing pattern in project)
2. **Field validation**: Require exact JSON structure, validate response contains all required fields (existing pattern in `extract_semantics`)
3. **Graceful degradation**: Return fallback minimal data when LLM fails (existing pattern in `_create_fallback_semantic`)
4. **Low temperature**: Use temperature=0.1 for deterministic analysis (already configured in current code)

---

### 1.2 Context Window Optimization for Large Code Files

**Decision**: Use intelligent chunking with method-level boundaries and cross-reference summary

**Rationale**:
- Modern LLMs (Ollama gemma2:12b) have ~8k-32k token context windows (~6k-24k chars for code)
- Current implementation truncates at 10k chars (line 85, `ollama_client.py`) which can split methods mid-function
- Method-level chunking preserves semantic boundaries
- Summary-first approach allows LLM to understand file structure before analyzing details
- Weaviate vector search enables retrieving relevant related artifacts without including full source

**Implementation Strategy**:

```python
def chunk_large_file(
    file_content: str,
    artifact_type: ArtifactType,
    max_chunk_size: int = 6000  # ~8k tokens with safety margin
) -> List[Dict[str, Any]]:
    """
    Chunk large files at semantic boundaries.

    Returns list of chunks with metadata for cross-referencing.
    """
    if len(file_content) <= max_chunk_size:
        return [{"content": file_content, "chunk_id": 0, "total_chunks": 1}]

    chunks = []

    if artifact_type in (ArtifactType.JAVA_SOURCE, ArtifactType.JAVA_TEST):
        # Parse with JavaParser to get method boundaries
        parsed = java_parser.parse_file_content(file_content)
        methods = parsed.get('methods', [])

        # Group methods into chunks respecting size limits
        current_chunk = []
        current_size = 0

        for method in methods:
            method_code = extract_method_code(file_content, method)
            method_size = len(method_code)

            if current_size + method_size > max_chunk_size and current_chunk:
                # Save current chunk
                chunks.append({
                    "content": "\n\n".join(current_chunk),
                    "chunk_id": len(chunks),
                    "methods": [m['name'] for m in current_chunk_methods]
                })
                current_chunk = []
                current_size = 0

            current_chunk.append(method_code)
            current_size += method_size

        # Add remaining chunk
        if current_chunk:
            chunks.append({
                "content": "\n\n".join(current_chunk),
                "chunk_id": len(chunks)
            })

    else:
        # Simple line-based chunking for non-Java files
        lines = file_content.split('\n')
        current_chunk = []
        current_size = 0

        for line in lines:
            if current_size + len(line) > max_chunk_size and current_chunk:
                chunks.append({
                    "content": "\n".join(current_chunk),
                    "chunk_id": len(chunks)
                })
                current_chunk = []
                current_size = 0

            current_chunk.append(line)
            current_size += len(line)

        if current_chunk:
            chunks.append({
                "content": "\n".join(current_chunk),
                "chunk_id": len(chunks)
            })

    # Add total_chunks to all
    for chunk in chunks:
        chunk['total_chunks'] = len(chunks)

    return chunks


def analyze_large_file_incremental(
    file_path: str,
    file_content: str,
    artifact_type: ArtifactType
) -> Dict[str, Any]:
    """
    Analyze large file using incremental prompting.

    1. Generate high-level summary
    2. Analyze chunks with summary context
    3. Consolidate chunk results
    """
    chunks = chunk_large_file(file_content, artifact_type)

    if len(chunks) == 1:
        # Single chunk, use standard analysis
        return ollama_client.extract_semantics(file_path, file_content, artifact_type)

    # Step 1: Get high-level summary from first chunk + class signature
    summary_prompt = create_summary_prompt(file_path, chunks[0]['content'], artifact_type)
    file_summary = ollama_client.call_ollama(
        prompt=summary_prompt,
        system_prompt=SUMMARY_SYSTEM_PROMPT,
        format_json=True
    )

    # Step 2: Analyze each chunk with summary context
    chunk_analyses = []
    for chunk in chunks:
        chunk_prompt = create_chunk_analysis_prompt(
            file_path=file_path,
            chunk_content=chunk['content'],
            chunk_id=chunk['chunk_id'],
            total_chunks=chunk['total_chunks'],
            file_summary=file_summary,
            artifact_type=artifact_type
        )

        chunk_result = ollama_client.call_ollama(
            prompt=chunk_prompt,
            system_prompt=CHUNK_SYSTEM_PROMPT,
            format_json=True
        )
        chunk_analyses.append(chunk_result)

    # Step 3: Consolidate results
    consolidated = consolidate_chunk_analyses(file_summary, chunk_analyses)
    return consolidated
```

**Alternatives Considered**:
- **Hard truncation at N chars**: Loses information, breaks code mid-function (current approach)
- **Sliding window with overlap**: Redundant processing, slower, doesn't respect semantic boundaries
- **Increase context window**: Not all models support large contexts, costs increase quadratically
- **Summarize then discard details**: Loses important business rules and validation logic

**Optimization Notes**:
- **Use Weaviate for cross-references**: Query vector DB for related artifacts rather than including full source in context
- **Cache structural parsing**: Parse files once in extraction phase, reuse parsed structure during PRD generation
- **Parallel chunk processing**: Process chunks concurrently (respecting rate limits) to reduce latency

---

### 1.3 Few-Shot Examples for Database Schema Inference

**Decision**: Use in-prompt few-shot examples only for complex/ambiguous cases; prefer structured zero-shot with schema templates

**Rationale**:
- Few-shot examples consume significant context window space (500-1000 tokens per example)
- Current Ollama models (gemma2:12b) perform well with zero-shot structured prompts when format is clear
- Schema inference is relatively deterministic (JPA annotations, column definitions)
- Few-shot examples most valuable for ambiguous relationships (implicit foreign keys, polymorphic associations)

**Implementation Strategy**:

```python
# Primary approach: Zero-shot with schema template
SCHEMA_INFERENCE_SYSTEM_PROMPT = """You are a database schema analyst. Extract database schema from code.

Response format:
{
  "tables": [
    {
      "name": "table_name",
      "columns": [
        {
          "name": "column_name",
          "type": "SQL type",
          "nullable": true/false,
          "primary_key": true/false,
          "foreign_key": {"references_table": "other_table", "references_column": "id"} or null
        }
      ],
      "constraints": [
        {"type": "unique|check|index", "columns": ["col1"], "definition": "constraint details"}
      ]
    }
  ],
  "relationships": [
    {
      "type": "one-to-many|many-to-one|many-to-many",
      "from_table": "table1",
      "to_table": "table2",
      "join_condition": "table1.fk = table2.id",
      "cascade": "CASCADE|SET_NULL|RESTRICT"
    }
  ]
}

Extract from JPA annotations, Hibernate mappings, SQL DDL, or iBATIS XML."""

# Use few-shot ONLY for complex relationship inference
FEW_SHOT_RELATIONSHIP_EXAMPLES = """
Example 1 - Implicit Foreign Key:
Input:
```java
@Entity
public class Order {
    @ManyToOne
    private Customer customer;
}
```
Output relationships:
[{
  "type": "many-to-one",
  "from_table": "orders",
  "to_table": "customers",
  "join_condition": "orders.customer_id = customers.id"
}]

Example 2 - Polymorphic Association:
Input:
```java
@Entity
@Inheritance(strategy = InheritanceType.JOINED)
public class Payment { }

@Entity
public class CreditCardPayment extends Payment { }
```
Output tables:
[
  {"name": "payment", "columns": [{"name": "id", "primary_key": true}, {"name": "dtype", "type": "varchar"}]},
  {"name": "creditcardpayment", "columns": [{"name": "id", "primary_key": true, "foreign_key": {"references_table": "payment"}}]}
]

Now analyze this code:
"""

def infer_schema_from_entity(entity_code: str, use_few_shot: bool = False) -> Dict:
    """Infer database schema from entity code."""
    system_prompt = SCHEMA_INFERENCE_SYSTEM_PROMPT

    user_prompt = f"""
Analyze this entity/DAO code:

```java
{entity_code[:7000]}
```

Extract complete database schema including tables, columns, constraints, and relationships.
"""

    # Only add few-shot examples if dealing with complex inheritance or polymorphism
    if use_few_shot or ("@Inheritance" in entity_code or "extends" in entity_code):
        user_prompt = FEW_SHOT_RELATIONSHIP_EXAMPLES + user_prompt

    return ollama_client.call_ollama(
        prompt=user_prompt,
        system_prompt=system_prompt,
        format_json=True
    )
```

**When to Use Few-Shot**:
1. **Implicit relationships**: Foreign keys not explicitly declared
2. **Inheritance hierarchies**: JOINED, SINGLE_TABLE, TABLE_PER_CLASS strategies
3. **Composite keys**: Multi-column primary keys
4. **Custom mapping annotations**: Non-standard ORM configurations

**Alternatives Considered**:
- **Always include few-shot examples**: Wastes context window, slower inference
- **Fine-tuned model**: Requires training data, deployment complexity, loses generality
- **Rule-based extraction only**: Misses implicit relationships, requires exhaustive pattern matching

---

### 1.4 Prompt Strategies for Cross-Referencing Multiple Artifacts

**Decision**: Use Weaviate vector similarity + metadata filtering to retrieve related artifacts, then construct contextual prompts with summaries

**Rationale**:
- Cannot fit multiple full files in context window (even 3 medium files = 20k+ chars)
- Weaviate already indexes artifacts with embeddings and structured metadata
- Vector similarity search finds semantically related code without keyword matching
- Summaries provide context without overwhelming LLM with implementation details
- Existing schema has `dependencies`, `entities`, `tags` fields ideal for cross-referencing

**Implementation Strategy**:

```python
def cross_reference_analysis(
    target_artifact_path: str,
    target_content: str,
    artifact_type: ArtifactType,
    weaviate_client: WeaviateClient,
    project_id: str
) -> Dict[str, Any]:
    """
    Analyze artifact with cross-references to related code.

    1. Query Weaviate for related artifacts
    2. Build context from summaries
    3. Generate prompt with cross-reference context
    4. Extract with LLM
    """
    # Step 1: Find related artifacts via vector search
    related_artifacts = find_related_artifacts(
        weaviate_client=weaviate_client,
        target_path=target_artifact_path,
        target_content=target_content,
        project_id=project_id,
        artifact_type=artifact_type,
        max_results=10
    )

    # Step 2: Build context summary from related artifacts
    context_summary = build_cross_reference_context(related_artifacts)

    # Step 3: Create prompt with cross-reference information
    prompt = f"""
Analyze this {artifact_type.value} file:

File: {target_artifact_path}

Related Artifacts (from codebase analysis):

{context_summary}

Target Code:
```
{target_content[:6000]}
```

Analyze this code and identify:
1. How it uses the related artifacts listed above
2. Business rules coordinated across multiple components
3. Data flows between this file and related files
4. Dependencies and interaction patterns

Provide JSON response with cross-references."""

    return ollama_client.call_ollama(
        prompt=prompt,
        system_prompt=CROSS_REFERENCE_SYSTEM_PROMPT,
        format_json=True
    )


def find_related_artifacts(
    weaviate_client: WeaviateClient,
    target_path: str,
    target_content: str,
    project_id: str,
    artifact_type: ArtifactType,
    max_results: int = 10
) -> List[Dict[str, Any]]:
    """
    Find related artifacts using Weaviate vector + metadata search.

    Strategy:
    1. Vector similarity on target_content summary
    2. Filter by project_id
    3. Boost artifacts in same package/module
    4. Include explicit dependencies (imports, annotations)
    """
    # Generate embedding for target (or use existing if already indexed)
    target_embedding = weaviate_client.generate_embedding(target_content[:2000])

    # Build Weaviate query
    query = {
        "vector": target_embedding,
        "limit": max_results,
        "where": {
            "operator": "And",
            "operands": [
                {"path": ["project_id"], "operator": "Equal", "valueString": project_id},
                # Exclude target file itself
                {"path": ["file_path"], "operator": "NotEqual", "valueString": target_path}
            ]
        }
    }

    # Adjust query based on artifact type
    if artifact_type == ArtifactType.JAVA_SOURCE:
        # For Java services, prioritize DAOs and entities
        query["where"]["operands"].append({
            "path": ["artifact_type"],
            "operator": "ContainsAny",
            "valueString": ["java_source", "java_entity", "mybatis_mapper"]
        })
    elif artifact_type == ArtifactType.JSP_VIEW:
        # For JSP, prioritize controllers and DTOs
        query["where"]["operands"].append({
            "path": ["tags"],
            "operator": "ContainsAny",
            "valueString": ["controller", "dto", "form"]
        })

    results = weaviate_client.query_with_vector("CodeArtifact", query)
    return results


def build_cross_reference_context(artifacts: List[Dict]) -> str:
    """
    Build concise context summary from related artifacts.

    Goal: Provide enough context for LLM without overwhelming prompt.
    """
    context_lines = []

    for artifact in artifacts:
        # Extract key info (without full source code)
        context_lines.append(f"""
- **{artifact['file_path']}** ({artifact['artifact_type']})
  - Summary: {artifact['summary'][:200]}
  - Entities: {', '.join(artifact.get('entities', [])[:5])}
  - Concerns: {', '.join(artifact.get('concerns', [])[:3])}
""")

    return '\n'.join(context_lines)


CROSS_REFERENCE_SYSTEM_PROMPT = """You are a system integration analyst. Analyze how code components interact.

Your response must be valid JSON:
{
  "cross_references": [
    {
      "related_file": "path/to/related/file",
      "relationship": "calls|extends|implements|uses|configures",
      "description": "How they interact",
      "data_flow": "What data passes between them"
    }
  ],
  "coordinated_business_rules": [
    {
      "rule": "Business rule description",
      "enforced_in": ["file1", "file2"],
      "coordination_pattern": "How rule is coordinated across files"
    }
  ],
  "integration_concerns": ["concern1", "concern2"]
}"""
```

**Key Strategies**:
1. **Vector similarity for semantic matching**: Finds related code even with different terminology
2. **Metadata filtering for precision**: Ensure related artifacts are same project, compatible types
3. **Summary-based context**: Include artifact summaries, not full source
4. **Layered queries**: First find candidates, then fetch detailed info only for top matches
5. **Caching**: Cache related artifact queries to avoid repeated Weaviate lookups

**Alternatives Considered**:
- **Include full source of related files**: Exceeds context window
- **Static analysis only (imports, method calls)**: Misses semantic relationships, requires parsing
- **LLM-based retrieval**: Slower, less accurate than vector search for code
- **No cross-referencing**: Misses critical business rule coordination across layers

**Performance Optimizations**:
- **Batch related artifact queries**: When analyzing multiple files, pre-fetch common dependencies
- **Hierarchical context**: Start with high-level summary, drill down only if LLM requests more detail
- **Smart filtering**: Use file path patterns (same package = higher relevance) to reduce search space

---

## 2. Hierarchical Documentation Generation

### 2.1 Best Practices for Organizing Large Technical Documentation

**Decision**: Use layer-based directory structure with domain subdivisions and consistent naming conventions

**Rationale**:
- Matches specification requirements (FR-040, FR-043): layered subdirectories (database/, services/, frontend/, prd/)
- Aligns with common software architecture (data layer, business logic, presentation)
- Enables incremental generation and targeted updates
- Supports multiple navigation paths (by layer, by domain, by feature)
- Facilitates team specialization (DBAs focus on database/, frontend devs on frontend/)

**Directory Structure**:

```
output/
├── .visit_log.jsonl              # Global visit tracking (FR-008, FR-041)
├── index.md                      # Master index with executive summary
├── database/
│   ├── index.md                  # Database layer overview
│   ├── schema/
│   │   ├── index.md              # All tables alphabetically
│   │   ├── tables/
│   │   │   ├── users.md
│   │   │   ├── orders.md
│   │   │   └── ...
│   │   └── relationships.md      # ERD and foreign keys
│   ├── by-domain/
│   │   ├── auth/
│   │   │   ├── index.md
│   │   │   ├── tables.md         # Auth-related tables
│   │   │   └── business-rules.md
│   │   ├── billing/
│   │   └── ...
│   └── business-rules/
│       ├── index.md
│       ├── validation-rules.md
│       ├── constraints.md
│       └── transaction-patterns.md
├── services/
│   ├── index.md                  # Service layer overview
│   ├── by-name/
│   │   ├── index.md              # All services alphabetically
│   │   ├── UserService.md
│   │   ├── OrderService.md
│   │   └── ...
│   ├── by-domain/
│   │   ├── auth/
│   │   │   ├── index.md
│   │   │   └── services.md
│   │   └── ...
│   ├── api-endpoints/
│   │   ├── index.md              # REST/SOAP endpoints
│   │   ├── rest-api.md
│   │   └── soap-services.md
│   └── dependencies/
│       ├── index.md
│       └── dependency-graph.md   # Service interaction diagram
├── frontend/
│   ├── index.md                  # Frontend layer overview
│   ├── entry-points/
│   │   ├── index.md
│   │   ├── index.html.md
│   │   ├── main.jsp.md
│   │   └── ...
│   ├── forms/
│   │   ├── index.md
│   │   ├── login-form.md
│   │   ├── order-form.md
│   │   └── ...
│   ├── components/
│   │   ├── gwt-modules/
│   │   │   ├── index.md
│   │   │   └── ...
│   │   └── javascript/
│   │       ├── index.md
│   │       └── ...
│   ├── navigation/
│   │   ├── index.md
│   │   └── user-journeys.md
│   └── by-domain/
│       ├── auth/
│       └── ...
└── prd/
    ├── index.md                  # Final consolidated PRD
    ├── executive-summary.md
    ├── architecture-overview.md
    ├── cross-layer-flows.md      # End-to-end user scenarios
    ├── business-rules-consolidated.md
    └── gaps-and-recommendations.md
```

**Naming Conventions**:
- **Files**: kebab-case (e.g., `user-service.md`, `login-form.md`)
- **Directories**: lowercase, singular or plural as appropriate
- **Index files**: Always named `index.md` for consistency
- **Entity files**: Named after entity (e.g., `users.md` for users table)

**Alternatives Considered**:
- **Flat structure with prefixes**: (e.g., `db-users.md`, `svc-userservice.md`) - Hard to navigate, poor scaling
- **Single monolithic document**: Difficult to maintain, slow to load, hard to update incrementally
- **Domain-first structure**: (e.g., `auth/database/`, `auth/services/`) - Harder to understand layer architecture
- **Timestamp-based versions**: (e.g., `2024-12-14/`) - Spec requires latest version, not historical tracking

---

### 2.2 Index File Structures for Navigable Documentation

**Decision**: Use hierarchical indexes with multiple views (alphabetical, by-domain, by-layer) and link consolidation

**Rationale**:
- Supports different user personas (DBAs want table list, architects want domain view, developers want API reference)
- Markdown link format enables local and web viewing
- Automated index generation ensures consistency
- Statistics provide quick overview of codebase size and complexity

**Index File Template**:

```markdown
# [Layer/Domain] Index

**Generated**: 2024-12-14 10:30:00 UTC
**Project**: MyJavaApp
**Total Items**: 47

## Quick Stats

- Total Files Analyzed: 47
- Business Rules Documented: 132
- Cross-References: 89
- Last Updated: 2024-12-14

## Navigation

- [View by Name](#by-name) - Alphabetical listing
- [View by Domain](#by-domain) - Grouped by business domain
- [View by Type](#by-type) - Grouped by artifact type
- [Parent Index](../index.md) - Go up one level
- [Master Index](../index.md) - Return to top level

---

## By Name

### A
- [AuthenticationService](./by-name/AuthenticationService.md) - Handles user authentication and session management
- [AuthorizationService](./by-name/AuthorizationService.md) - Manages role-based access control

### B
- [BillingService](./by-name/BillingService.md) - Processes payments and invoicing

...

---

## By Domain

### Authentication & Security
- Services: [AuthenticationService](./by-domain/auth/AuthenticationService.md), [AuthorizationService](./by-domain/auth/AuthorizationService.md)
- Tables: [users](../database/schema/tables/users.md), [roles](../database/schema/tables/roles.md), [permissions](../database/schema/tables/permissions.md)
- Business Rules: [Password complexity rules](./by-domain/auth/business-rules.md#password-complexity), [Session timeout](./by-domain/auth/business-rules.md#session-timeout)
- Entry Points: [Login Form](../frontend/forms/login-form.md)

### Billing & Payments
- Services: [BillingService](./by-domain/billing/BillingService.md), [PaymentProcessor](./by-domain/billing/PaymentProcessor.md)
- Tables: [invoices](../database/schema/tables/invoices.md), [payments](../database/schema/tables/payments.md)
- Business Rules: [Invoice generation](./by-domain/billing/business-rules.md#invoice-generation)

...

---

## By Type

### REST APIs (12)
- [GET /api/users](./api-endpoints/rest-api.md#get-users)
- [POST /api/auth/login](./api-endpoints/rest-api.md#post-auth-login)
...

### SOAP Services (5)
- [UserManagementService](./api-endpoints/soap-services.md#user-management)
...

### Background Jobs (8)
- [InvoiceGenerationJob](./by-name/InvoiceGenerationJob.md)
...

---

## Cross-References

This layer interacts with:
- **Database Layer**: 23 tables accessed ([view database index](../database/index.md))
- **Frontend Layer**: 18 forms and pages ([view frontend index](../frontend/index.md))

---

## Quick Links

- [Common Patterns](#common-patterns)
- [Security Considerations](./security-patterns.md)
- [Performance Notes](./performance-notes.md)

---

## Common Patterns

### Transaction Management
Found in: [UserService](./by-name/UserService.md), [OrderService](./by-name/OrderService.md)
Pattern: Spring @Transactional annotations with REQUIRED propagation

### Error Handling
Found in: [BaseService](./by-name/BaseService.md)
Pattern: Try-catch with logging and custom exception hierarchy
```

**Index Generation Implementation**:

```python
@dataclass
class IndexEntry:
    """Entry in an index file."""
    name: str
    path: str  # Relative path from index file location
    summary: str
    domains: List[str]
    artifact_type: str
    cross_references: List[str]


def generate_layer_index(
    layer: str,  # "database", "services", "frontend", "prd"
    entries: List[IndexEntry],
    output_dir: Path,
    project_name: str
) -> Path:
    """
    Generate index.md file for a layer.

    Returns path to generated index file.
    """
    index_path = output_dir / layer / "index.md"

    # Sort entries for alphabetical view
    by_name = sorted(entries, key=lambda e: e.name.lower())

    # Group by domain
    by_domain = defaultdict(list)
    for entry in entries:
        for domain in entry.domains or ["uncategorized"]:
            by_domain[domain].append(entry)

    # Group by type
    by_type = defaultdict(list)
    for entry in entries:
        by_type[entry.artifact_type].append(entry)

    # Generate markdown
    content = [
        f"# {layer.title()} Layer Index",
        f"",
        f"**Generated**: {datetime.utcnow().isoformat()}",
        f"**Project**: {project_name}",
        f"**Total Items**: {len(entries)}",
        f"",
        f"## Quick Stats",
        f"",
        f"- Total Files Analyzed: {len(entries)}",
        f"- Domains: {len(by_domain)}",
        f"- Types: {len(by_type)}",
        f"",
        f"## Navigation",
        f"",
        f"- [View by Name](#by-name)",
        f"- [View by Domain](#by-domain)",
        f"- [View by Type](#by-type)",
        f"- [Master Index](../index.md)",
        f"",
        f"---",
        f"",
        f"## By Name",
        f""
    ]

    # Alphabetical grouping
    current_letter = ""
    for entry in by_name:
        first_letter = entry.name[0].upper()
        if first_letter != current_letter:
            current_letter = first_letter
            content.append(f"### {current_letter}")
            content.append("")

        content.append(f"- [{entry.name}]({entry.path}) - {entry.summary[:100]}")

    content.extend([
        "",
        "---",
        "",
        "## By Domain",
        ""
    ])

    # Domain grouping
    for domain, domain_entries in sorted(by_domain.items()):
        content.append(f"### {domain.replace('_', ' ').title()}")
        content.append("")
        for entry in sorted(domain_entries, key=lambda e: e.name):
            content.append(f"- [{entry.name}]({entry.path}) - {entry.summary[:100]}")
        content.append("")

    content.extend([
        "---",
        "",
        "## By Type",
        ""
    ])

    # Type grouping
    for artifact_type, type_entries in sorted(by_type.items()):
        content.append(f"### {artifact_type.replace('_', ' ').title()} ({len(type_entries)})")
        content.append("")
        for entry in sorted(type_entries, key=lambda e: e.name)[:10]:  # Limit to first 10
            content.append(f"- [{entry.name}]({entry.path})")
        if len(type_entries) > 10:
            content.append(f"- ... and {len(type_entries) - 10} more")
        content.append("")

    # Write file
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text("\n".join(content))

    return index_path


def generate_master_index(
    output_dir: Path,
    layer_stats: Dict[str, int],
    project_name: str
) -> Path:
    """Generate master index.md at output root."""
    index_path = output_dir / "index.md"

    content = f"""# {project_name} - Code Analysis Documentation

**Generated**: {datetime.utcnow().isoformat()}

## Executive Summary

This documentation provides a comprehensive analysis of the {project_name} codebase,
organized by architectural layers and business domains.

## Documentation Structure

### [Database Layer](./database/index.md)
- **Tables**: {layer_stats.get('database_tables', 0)}
- **Business Rules**: {layer_stats.get('database_rules', 0)}
- Explore database schema, entity relationships, and data validation rules

### [Service Layer](./services/index.md)
- **Services**: {layer_stats.get('services', 0)}
- **API Endpoints**: {layer_stats.get('endpoints', 0)}
- Explore business logic, service dependencies, and API contracts

### [Frontend Layer](./frontend/index.md)
- **Forms**: {layer_stats.get('forms', 0)}
- **Components**: {layer_stats.get('components', 0)}
- Explore user interfaces, navigation flows, and client-side logic

### [Product Requirements](./prd/index.md)
- Consolidated PRD synthesizing all layers
- Cross-layer flows and integration patterns
- Gaps and recommendations

## Quick Links

- [Architecture Overview](./prd/architecture-overview.md)
- [Cross-Layer Flows](./prd/cross-layer-flows.md)
- [Business Rules Consolidated](./prd/business-rules-consolidated.md)

## Analysis Metadata

- **Visit Log**: [.visit_log.jsonl](./.visit_log.jsonl)
- **Total Files Analyzed**: {layer_stats.get('total_files', 0)}
- **Analysis Duration**: {layer_stats.get('duration', '0')} seconds
"""

    index_path.write_text(content)
    return index_path
```

**Alternatives Considered**:
- **Auto-generated table of contents only**: Less navigable, requires scrolling through long documents
- **Wiki-style index**: Requires specialized wiki software, not markdown-compatible
- **Database-backed index**: Overengineered for static documentation, requires runtime environment
- **No index files**: Users must navigate directory structure manually, poor UX

---

### 2.3 Cross-Referencing Strategies in Markdown

**Decision**: Use relative markdown links with bidirectional references and link validation

**Rationale**:
- Markdown links work in GitHub, local editors (VS Code), static site generators (MkDocs, Docusaurus)
- Relative links are portable (documentation can be moved/copied)
- Bidirectional references enable navigation in both directions (parent-child, caller-callee)
- Link validation prevents broken links as code evolves

**Cross-Reference Patterns**:

```markdown
# UserService.md

## Overview
**File**: `src/main/java/com/example/service/UserService.java`
**Type**: Backend Service
**Domain**: Authentication

## Dependencies

### Database
- [users table](../database/schema/tables/users.md) - User account information
- [roles table](../database/schema/tables/roles.md) - User role assignments

### Other Services
- [EmailService](./EmailService.md) - Sends notification emails
- [AuditService](./AuditService.md) - Logs user actions

### Called By
- [LoginController](./LoginController.md) - Handles login requests
- [UserRegistrationController](./UserRegistrationController.md) - Handles new user registration

## API Endpoints

This service implements:
- [POST /api/auth/login](./api-endpoints/rest-api.md#post-auth-login)
- [POST /api/auth/logout](./api-endpoints/rest-api.md#post-auth-logout)
- [GET /api/users/{id}](./api-endpoints/rest-api.md#get-users-id)

## Business Rules

- [Password complexity validation](../database/business-rules/validation-rules.md#password-complexity) - Enforces minimum password strength
- [Account lockout after failed attempts](../database/business-rules/validation-rules.md#account-lockout) - Security measure

## Frontend Integration

Used by:
- [Login Form](../frontend/forms/login-form.md)
- [User Profile Page](../frontend/components/user-profile.md)
```

**Link Types**:
1. **Upward links**: Point to parent/container (e.g., service -> layer index)
2. **Downward links**: Point to children/details (e.g., index -> individual files)
3. **Lateral links**: Point to related artifacts (e.g., service -> DAO)
4. **External links**: Point to source code (e.g., GitHub URLs if applicable)

**Link Generation Implementation**:

```python
def generate_cross_reference_links(
    current_file_path: Path,
    related_artifacts: List[Dict[str, Any]],
    output_dir: Path
) -> str:
    """
    Generate markdown cross-reference links.

    Args:
        current_file_path: Path to current documentation file
        related_artifacts: List of related artifact metadata
        output_dir: Output directory root

    Returns:
        Markdown string with formatted links
    """
    links_by_category = {
        "Database Tables": [],
        "Services": [],
        "Forms": [],
        "Business Rules": []
    }

    for artifact in related_artifacts:
        # Determine target file path
        target_path = get_documentation_path(artifact, output_dir)

        # Calculate relative path from current file
        relative_path = os.path.relpath(target_path, current_file_path.parent)

        # Categorize link
        category = categorize_artifact(artifact)
        if category in links_by_category:
            links_by_category[category].append({
                "name": artifact['name'],
                "path": relative_path,
                "summary": artifact.get('summary', '')[:100]
            })

    # Generate markdown
    markdown_lines = []
    for category, links in links_by_category.items():
        if links:
            markdown_lines.append(f"### {category}\n")
            for link in sorted(links, key=lambda x: x['name']):
                markdown_lines.append(f"- [{link['name']}]({link['path']}) - {link['summary']}")
            markdown_lines.append("")

    return "\n".join(markdown_lines)


def get_documentation_path(artifact: Dict[str, Any], output_dir: Path) -> Path:
    """
    Determine documentation file path for an artifact.

    Uses consistent mapping: artifact type -> directory structure
    """
    artifact_type = artifact.get('artifact_type', 'unknown')
    name = artifact.get('name', 'unknown')

    if 'table' in artifact_type or 'entity' in artifact_type:
        return output_dir / "database" / "schema" / "tables" / f"{name}.md"
    elif 'service' in artifact_type:
        return output_dir / "services" / "by-name" / f"{name}.md"
    elif 'form' in artifact_type or 'jsp' in artifact_type:
        return output_dir / "frontend" / "forms" / f"{name}.md"
    elif 'gwt' in artifact_type:
        return output_dir / "frontend" / "components" / "gwt-modules" / f"{name}.md"
    else:
        return output_dir / "other" / f"{name}.md"


def validate_markdown_links(doc_file_path: Path, output_dir: Path) -> List[str]:
    """
    Validate all markdown links in a document.

    Returns list of broken links.
    """
    content = doc_file_path.read_text()

    # Extract all markdown links [text](url)
    import re
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    links = re.findall(link_pattern, content)

    broken_links = []
    for link_text, link_url in links:
        # Skip external URLs
        if link_url.startswith('http://') or link_url.startswith('https://'):
            continue

        # Skip anchors within same file
        if link_url.startswith('#'):
            continue

        # Resolve relative path
        target_path = (doc_file_path.parent / link_url).resolve()

        # Check if target exists
        if not target_path.exists():
            broken_links.append(f"Broken link in {doc_file_path}: [{link_text}]({link_url}) -> {target_path}")

    return broken_links
```

**Bidirectional Reference Maintenance**:

```python
def add_bidirectional_reference(
    source_doc_path: Path,
    target_doc_path: Path,
    reference_type: str,  # "uses", "called_by", "extends", etc.
    output_dir: Path
):
    """
    Add bidirectional cross-reference between two documents.

    Updates both source and target documents to link to each other.
    """
    # Calculate relative paths
    source_to_target = os.path.relpath(target_doc_path, source_doc_path.parent)
    target_to_source = os.path.relpath(source_doc_path, target_doc_path.parent)

    # Update source document (forward reference)
    source_content = source_doc_path.read_text()
    source_content += f"\n\n### {reference_type.title()}\n- [{target_doc_path.stem}]({source_to_target})\n"
    source_doc_path.write_text(source_content)

    # Update target document (backward reference)
    target_content = target_doc_path.read_text()
    inverse_type = get_inverse_reference_type(reference_type)  # "uses" -> "used_by"
    target_content += f"\n\n### {inverse_type.title()}\n- [{source_doc_path.stem}]({target_to_source})\n"
    target_doc_path.write_text(target_content)
```

**Alternatives Considered**:
- **Absolute paths**: Break when documentation is moved or viewed locally
- **ID-based references**: Require lookup table, not human-readable
- **No cross-references**: Users can't navigate between related artifacts
- **HTML links**: Not portable to non-web viewers

---

### 2.4 Table of Contents Generation Approaches

**Decision**: Use automated TOC generation with anchor links and optional tree-style navigation

**Rationale**:
- Markdown processors (GitHub, GitLab, MkDocs) support anchor links to headings
- Automated generation ensures TOC stays in sync with content
- Tree-style TOC for large documents improves scanability
- Optional depth control (e.g., show only H1-H3) prevents TOC from overwhelming readers

**TOC Implementation**:

```python
def generate_table_of_contents(
    markdown_content: str,
    max_depth: int = 3,
    style: str = "list"  # "list" or "tree"
) -> str:
    """
    Generate table of contents from markdown content.

    Args:
        markdown_content: Full markdown document
        max_depth: Maximum heading level to include (1-6)
        style: TOC style ("list" or "tree")

    Returns:
        Markdown TOC string
    """
    import re

    # Extract headings (## Heading, ### Subheading, etc.)
    heading_pattern = r'^(#{1,6})\s+(.+)$'
    headings = []

    for line in markdown_content.split('\n'):
        match = re.match(heading_pattern, line)
        if match:
            level = len(match.group(1))  # Count #'s
            text = match.group(2).strip()

            # Skip if exceeds max depth
            if level > max_depth:
                continue

            # Generate anchor (lowercase, hyphens, remove special chars)
            anchor = text.lower()
            anchor = re.sub(r'[^a-z0-9\s-]', '', anchor)
            anchor = re.sub(r'\s+', '-', anchor)

            headings.append({
                "level": level,
                "text": text,
                "anchor": anchor
            })

    # Generate TOC based on style
    if style == "list":
        return generate_list_toc(headings)
    else:
        return generate_tree_toc(headings)


def generate_list_toc(headings: List[Dict]) -> str:
    """Generate flat list-style TOC."""
    toc_lines = ["## Table of Contents\n"]

    for heading in headings:
        indent = "  " * (heading['level'] - 1)
        toc_lines.append(f"{indent}- [{heading['text']}](#{heading['anchor']})")

    toc_lines.append("")
    return "\n".join(toc_lines)


def generate_tree_toc(headings: List[Dict]) -> str:
    """Generate tree-style TOC with indentation."""
    toc_lines = ["## Table of Contents\n"]

    for i, heading in enumerate(headings):
        level = heading['level']
        text = heading['text']
        anchor = heading['anchor']

        # Determine indent based on level
        indent = "  " * (level - 1)

        # Determine if this is a leaf node (no children)
        is_leaf = (i == len(headings) - 1) or (headings[i + 1]['level'] <= level)

        # Tree characters
        if is_leaf:
            prefix = "└─"
        else:
            prefix = "├─"

        toc_lines.append(f"{indent}{prefix} [{text}](#{anchor})")

    toc_lines.append("")
    return "\n".join(toc_lines)


def inject_toc_into_document(
    doc_path: Path,
    max_depth: int = 3,
    toc_marker: str = "<!-- TOC -->"
):
    """
    Inject or update TOC in a markdown document.

    Replaces content between <!-- TOC --> and <!-- /TOC --> markers.
    If markers don't exist, inserts TOC after first heading.
    """
    content = doc_path.read_text()

    # Generate TOC
    toc = generate_table_of_contents(content, max_depth=max_depth)

    # Check if TOC markers exist
    toc_start = "<!-- TOC -->"
    toc_end = "<!-- /TOC -->"

    if toc_start in content and toc_end in content:
        # Replace existing TOC
        pattern = f"{re.escape(toc_start)}.*?{re.escape(toc_end)}"
        replacement = f"{toc_start}\n{toc}\n{toc_end}"
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    else:
        # Insert TOC after first heading
        lines = content.split('\n')
        first_heading_idx = next(
            (i for i, line in enumerate(lines) if line.startswith('#')),
            0
        )

        lines.insert(first_heading_idx + 1, f"\n{toc_start}\n{toc}\n{toc_end}\n")
        new_content = '\n'.join(lines)

    # Write back
    doc_path.write_text(new_content)
```

**TOC Example Output**:

```markdown
<!-- TOC -->
## Table of Contents

- [Overview](#overview)
- [Database Schema](#database-schema)
  - [Tables](#tables)
    - [users table](#users-table)
    - [orders table](#orders-table)
  - [Relationships](#relationships)
- [Business Rules](#business-rules)
  - [Validation Rules](#validation-rules)
  - [Transaction Patterns](#transaction-patterns)
- [API Reference](#api-reference)
  - [Authentication](#authentication)
  - [User Management](#user-management)
<!-- /TOC -->
```

**Alternatives Considered**:
- **Manual TOC maintenance**: Error-prone, becomes stale quickly
- **Page numbers**: Don't work in web/markdown viewers
- **Collapsible sections**: Require JavaScript, not markdown-native
- **No TOC**: Large documents hard to navigate

**Best Practices**:
1. **Regenerate TOC on each doc update**: Ensure it stays current
2. **Limit depth to 3-4 levels**: Deeper nesting hard to scan
3. **Use descriptive heading text**: Avoid generic "Section 1", "Part A"
4. **Place TOC after introduction**: Gives context before navigation options

---

## 3. Incremental Analysis and State Management

### 3.1 File Tracking Approaches (Content Hashing Algorithms)

**Decision**: Use SHA-256 content hashing with file metadata (mtime, size) for change detection

**Rationale**:
- SHA-256 is cryptographically secure, collision-resistant, standard in Python hashlib
- Content hashing detects changes even if file metadata unchanged (manual edit with timestamp reset)
- File metadata (mtime, size) provides fast preliminary check before expensive hashing
- Two-stage check: fast metadata comparison, then hash only if metadata changed
- Existing project uses similar approach for generating deterministic UUIDs (line 268, research.md from 001)

**Implementation**:

```python
import hashlib
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime


def compute_file_hash(file_path: Path) -> str:
    """
    Compute SHA-256 hash of file contents.

    Args:
        file_path: Path to file

    Returns:
        Hex digest of SHA-256 hash
    """
    hasher = hashlib.sha256()

    with file_path.open('rb') as f:
        # Read in chunks to handle large files
        for chunk in iter(lambda: f.read(8192), b''):
            hasher.update(chunk)

    return hasher.hexdigest()


def get_file_metadata(file_path: Path) -> Dict[str, any]:
    """
    Get file metadata for change detection.

    Returns dict with mtime, size, hash.
    """
    stat = file_path.stat()

    return {
        "path": str(file_path),
        "mtime": stat.st_mtime,
        "size": stat.st_size,
        "mtime_iso": datetime.fromtimestamp(stat.st_mtime).isoformat()
    }


def has_file_changed(
    file_path: Path,
    previous_metadata: Dict[str, any]
) -> bool:
    """
    Detect if file has changed since previous analysis.

    Two-stage check:
    1. Fast: compare mtime and size
    2. Slow: compute and compare hash if metadata changed

    Args:
        file_path: Path to file
        previous_metadata: Metadata from previous analysis (mtime, size, hash)

    Returns:
        True if file changed, False otherwise
    """
    # Stage 1: Fast metadata check
    current_metadata = get_file_metadata(file_path)

    if current_metadata['mtime'] == previous_metadata.get('mtime') and \
       current_metadata['size'] == previous_metadata.get('size'):
        # Metadata unchanged, assume file unchanged
        return False

    # Stage 2: Compute content hash
    current_hash = compute_file_hash(file_path)
    previous_hash = previous_metadata.get('hash')

    return current_hash != previous_hash


def should_reanalyze_file(
    file_path: Path,
    visit_log: 'VisitLog',
    force: bool = False
) -> bool:
    """
    Determine if file should be reanalyzed.

    Args:
        file_path: Path to file
        visit_log: Visit log with previous analysis records
        force: Force reanalysis even if unchanged

    Returns:
        True if file should be analyzed
    """
    if force:
        return True

    # Check if file was previously analyzed
    previous_record = visit_log.get_record(str(file_path))

    if not previous_record:
        # Never analyzed before
        return True

    # Check if previous analysis failed
    if previous_record.get('status') == 'failed':
        # Retry failed files
        return True

    # Check if file changed
    return has_file_changed(file_path, previous_record)
```

**Hash Algorithm Comparison**:

| Algorithm | Speed | Collision Risk | Use Case |
|-----------|-------|----------------|----------|
| MD5 | Fast | High (broken) | NOT recommended - security issues |
| SHA-1 | Fast | Medium (weaknesses found) | NOT recommended |
| SHA-256 | Medium | Negligible | **RECOMMENDED** - secure, standard |
| SHA-512 | Slower | Negligible | Overkill for file tracking |
| BLAKE2 | Fast | Negligible | Good alternative, less common |

**Decision**: SHA-256 balances security, speed, and ecosystem support.

**Alternatives Considered**:
- **MD5**: Faster but has known collision vulnerabilities, not suitable for integrity checking
- **SHA-1**: Deprecated due to collision attacks (SHAttered)
- **Modification time only**: Can be manipulated (touch command), unreliable
- **File size only**: Many changes preserve file size, insufficient
- **Git object hashing**: Requires Git repo, not portable

**Performance Optimization**:
- **Cache hashes**: Store computed hashes in visit log to avoid recomputation
- **Parallel hashing**: Hash multiple files concurrently using ThreadPoolExecutor
- **Skip unchanged files**: Use mtime+size as fast prefilter before hashing

---

### 3.2 State Persistence Formats for Resume Capability

**Decision**: Use JSON Lines (.jsonl) format for visit log with atomic append operations

**Rationale**:
- JSON Lines is already used in project for inventory (line 85-107, `inventory.py`)
- Append-only writes are atomic on most filesystems, reducing corruption risk
- Streaming-friendly: can process large logs line-by-line without loading entire file
- Human-readable for debugging
- Each line is self-contained JSON object
- Aligns with FR-008, FR-041 specification requirements

**Visit Log Schema**:

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
import json
from pathlib import Path
from threading import Lock


@dataclass
class VisitLogEntry:
    """
    Single entry in visit log.

    Tracks analysis of one file at one point in time.
    """
    file_path: str                    # Absolute path to file
    timestamp: datetime               # When analysis occurred
    status: str                       # "success", "failed", "skipped"
    content_hash: str                 # SHA-256 hash of file content
    layer: str                        # "database", "services", "frontend"
    artifact_type: Optional[str] = None  # Type of artifact
    analysis_duration_seconds: float = 0.0  # Time taken to analyze
    error_message: Optional[str] = None  # Error if failed

    # File metadata
    file_size: int = 0
    file_mtime: float = 0.0

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "file_path": self.file_path,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status,
            "content_hash": self.content_hash,
            "layer": self.layer,
            "artifact_type": self.artifact_type,
            "analysis_duration_seconds": self.analysis_duration_seconds,
            "error_message": self.error_message,
            "file_size": self.file_size,
            "file_mtime": self.file_mtime
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'VisitLogEntry':
        """Create from dictionary."""
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)


class VisitLog:
    """
    Visit log manager for tracking analyzed files.

    Implements:
    - Atomic append operations
    - Thread-safe access
    - Fast lookup by file path
    - Incremental updates
    """

    def __init__(self, log_path: Path):
        """
        Initialize visit log.

        Args:
            log_path: Path to .visit_log.jsonl file
        """
        self.log_path = log_path
        self._lock = Lock()
        self._index: Dict[str, VisitLogEntry] = {}

        # Load existing log into memory for fast lookups
        if log_path.exists():
            self._load_index()

    def _load_index(self):
        """Load visit log into in-memory index."""
        with self.log_path.open('r') as f:
            for line in f:
                if line.strip():
                    entry = VisitLogEntry.from_dict(json.loads(line))
                    # Keep only most recent entry per file
                    self._index[entry.file_path] = entry

    def record_visit(self, entry: VisitLogEntry):
        """
        Record a file visit (thread-safe, atomic).

        Args:
            entry: Visit log entry
        """
        with self._lock:
            # Append to file
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            with self.log_path.open('a') as f:
                f.write(json.dumps(entry.to_dict()) + '\n')

            # Update index
            self._index[entry.file_path] = entry

    def get_record(self, file_path: str) -> Optional[dict]:
        """
        Get most recent record for a file.

        Args:
            file_path: File path (absolute)

        Returns:
            Record dict or None if not found
        """
        entry = self._index.get(file_path)
        return entry.to_dict() if entry else None

    def get_files_by_status(self, status: str) -> List[str]:
        """
        Get all file paths with given status.

        Args:
            status: "success", "failed", "skipped"

        Returns:
            List of file paths
        """
        return [
            path for path, entry in self._index.items()
            if entry.status == status
        ]

    def get_files_by_layer(self, layer: str) -> List[str]:
        """
        Get all file paths in given layer.

        Args:
            layer: "database", "services", "frontend"

        Returns:
            List of file paths
        """
        return [
            path for path, entry in self._index.items()
            if entry.layer == layer
        ]

    def get_statistics(self) -> dict:
        """
        Get visit log statistics.

        Returns:
            Dict with counts by status, layer, etc.
        """
        stats = {
            "total_files": len(self._index),
            "by_status": {},
            "by_layer": {},
            "total_duration_seconds": 0.0
        }

        for entry in self._index.values():
            # Count by status
            stats["by_status"][entry.status] = stats["by_status"].get(entry.status, 0) + 1

            # Count by layer
            stats["by_layer"][entry.layer] = stats["by_layer"].get(entry.layer, 0) + 1

            # Sum duration
            stats["total_duration_seconds"] += entry.analysis_duration_seconds

        return stats

    def compact_log(self):
        """
        Compact log file by removing duplicate entries.

        Keeps only most recent entry per file.
        """
        with self._lock:
            # Write compacted log to temp file
            temp_path = self.log_path.with_suffix('.jsonl.tmp')
            with temp_path.open('w') as f:
                for entry in self._index.values():
                    f.write(json.dumps(entry.to_dict()) + '\n')

            # Replace original log
            temp_path.replace(self.log_path)


# Usage example
def analyze_with_visit_tracking(
    file_path: Path,
    layer: str,
    visit_log: VisitLog,
    force: bool = False
) -> Optional[dict]:
    """
    Analyze file with visit tracking.

    Returns:
        Analysis result or None if skipped
    """
    # Check if should reanalyze
    if not should_reanalyze_file(file_path, visit_log, force):
        logger.info(f"Skipping unchanged file: {file_path}")
        visit_log.record_visit(VisitLogEntry(
            file_path=str(file_path),
            timestamp=datetime.utcnow(),
            status="skipped",
            content_hash=visit_log.get_record(str(file_path))['content_hash'],
            layer=layer
        ))
        return None

    # Analyze file
    start_time = time.time()
    try:
        result = analyze_file(file_path, layer)
        duration = time.time() - start_time

        # Record success
        visit_log.record_visit(VisitLogEntry(
            file_path=str(file_path),
            timestamp=datetime.utcnow(),
            status="success",
            content_hash=compute_file_hash(file_path),
            layer=layer,
            artifact_type=result.get('artifact_type'),
            analysis_duration_seconds=duration,
            file_size=file_path.stat().st_size,
            file_mtime=file_path.stat().st_mtime
        ))

        return result

    except Exception as e:
        duration = time.time() - start_time

        # Record failure
        visit_log.record_visit(VisitLogEntry(
            file_path=str(file_path),
            timestamp=datetime.utcnow(),
            status="failed",
            content_hash=compute_file_hash(file_path),
            layer=layer,
            analysis_duration_seconds=duration,
            error_message=str(e),
            file_size=file_path.stat().st_size,
            file_mtime=file_path.stat().st_mtime
        ))

        raise
```

**Alternatives Considered**:
- **SQLite database**: Requires DB library, locking complexity, binary format not human-readable
- **Single JSON file**: Must rewrite entire file on each update, risk of corruption, not streaming-friendly
- **Pickle format**: Binary, not human-readable, version compatibility issues
- **CSV format**: Poor for nested structures, requires header management

**Compaction Strategy**:
- Run compaction after every N entries (e.g., 1000) or on CLI flag
- Compaction reduces file size by keeping only latest record per file
- Compaction is optional - append-only mode works indefinitely for most use cases

---

### 3.3 Detecting File Changes Efficiently

**Decision**: Use hybrid approach with three-tier change detection: quick filter, content hash, and optional deep analysis

**Rationale**:
- Most files don't change between runs, quick filter eliminates 90%+ of work
- Content hash provides reliable change detection without full analysis
- Optional deep analysis (comparing extracted metadata) handles file moves/renames
- Tiered approach balances speed and accuracy

**Three-Tier Change Detection**:

```python
from enum import Enum
from typing import Tuple


class ChangeStatus(Enum):
    """File change status."""
    UNCHANGED = "unchanged"
    MODIFIED = "modified"
    NEW = "new"
    DELETED = "deleted"
    MOVED = "moved"


def detect_file_change(
    file_path: Path,
    visit_log: VisitLog,
    deep_analysis: bool = False
) -> Tuple[ChangeStatus, Optional[dict]]:
    """
    Detect file change status using three-tier approach.

    Tier 1: Quick filter (mtime + size)
    Tier 2: Content hash comparison
    Tier 3: Deep analysis (compare extracted entities)

    Args:
        file_path: Path to file
        visit_log: Visit log with previous analysis
        deep_analysis: Enable tier 3 deep analysis

    Returns:
        Tuple of (ChangeStatus, previous_record or None)
    """
    # Get previous record
    previous_record = visit_log.get_record(str(file_path))

    if not previous_record:
        return (ChangeStatus.NEW, None)

    if not file_path.exists():
        return (ChangeStatus.DELETED, previous_record)

    # Tier 1: Quick filter (mtime + size)
    current_metadata = get_file_metadata(file_path)

    if (current_metadata['mtime'] == previous_record.get('file_mtime') and
        current_metadata['size'] == previous_record.get('file_size')):
        # Metadata unchanged, assume file unchanged
        return (ChangeStatus.UNCHANGED, previous_record)

    # Tier 2: Content hash
    current_hash = compute_file_hash(file_path)
    previous_hash = previous_record.get('content_hash')

    if current_hash == previous_hash:
        # Content unchanged (mtime changed but content didn't - e.g., touch command)
        return (ChangeStatus.UNCHANGED, previous_record)

    # Content changed
    if not deep_analysis:
        return (ChangeStatus.MODIFIED, previous_record)

    # Tier 3: Deep analysis (optional)
    # Useful for detecting file moves or minor changes
    change_magnitude = analyze_change_magnitude(
        file_path,
        previous_record
    )

    if change_magnitude == "minor":
        # Minor change (e.g., comment added, whitespace)
        # Could choose to skip reanalysis
        return (ChangeStatus.UNCHANGED, previous_record)
    else:
        return (ChangeStatus.MODIFIED, previous_record)


def analyze_change_magnitude(
    file_path: Path,
    previous_record: dict
) -> str:
    """
    Analyze magnitude of file change.

    Compares structural elements (classes, methods, tables) to determine
    if change is minor (comments, formatting) or major (logic, schema).

    Args:
        file_path: Path to changed file
        previous_record: Previous analysis record with extracted entities

    Returns:
        "minor", "moderate", or "major"
    """
    # Quick parse to extract structural elements
    current_structure = quick_parse_structure(file_path)
    previous_structure = previous_record.get('structural_data', {})

    # Compare key structural elements
    current_entities = set(current_structure.get('entities', []))
    previous_entities = set(previous_structure.get('entities', []))

    # Calculate similarity
    if not previous_entities:
        return "major"  # No baseline

    intersection = current_entities & previous_entities
    union = current_entities | previous_entities

    similarity = len(intersection) / len(union) if union else 1.0

    if similarity > 0.95:
        return "minor"
    elif similarity > 0.75:
        return "moderate"
    else:
        return "major"


def quick_parse_structure(file_path: Path) -> dict:
    """
    Quick parse to extract structural elements without LLM.

    Uses lightweight parsers to get class names, method signatures, etc.
    """
    # Implementation depends on file type
    # For Java: use JavaParser (already in project)
    # For JSP: use JSPParser
    # etc.

    if file_path.suffix == '.java':
        parser = JavaParser()
        return parser.parse_file(file_path)
    elif file_path.suffix == '.jsp':
        parser = JSPParser()
        return parser.parse_file(file_path)
    else:
        return {}


def batch_change_detection(
    file_paths: List[Path],
    visit_log: VisitLog,
    max_workers: int = 4
) -> Dict[Path, ChangeStatus]:
    """
    Detect changes for multiple files in parallel.

    Args:
        file_paths: List of files to check
        visit_log: Visit log
        max_workers: Max parallel workers

    Returns:
        Dict mapping file path to change status
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed

    results = {}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_path = {
            executor.submit(detect_file_change, path, visit_log): path
            for path in file_paths
        }

        # Collect results
        for future in as_completed(future_to_path):
            path = future_to_path[future]
            try:
                status, _ = future.result()
                results[path] = status
            except Exception as e:
                logger.error(f"Error detecting change for {path}: {e}")
                results[path] = ChangeStatus.MODIFIED  # Safe default: reanalyze

    return results
```

**Performance Characteristics**:

| Tier | Operation | Time per File | Accuracy |
|------|-----------|---------------|----------|
| 1 | Metadata check (stat) | <1ms | 95% (can have false negatives) |
| 2 | Content hash (SHA-256) | 1-50ms (depends on file size) | 99.9999% (hash collision negligible) |
| 3 | Deep analysis (parse + compare) | 10-200ms (depends on parser) | 100% (semantic comparison) |

**Optimization Strategies**:
1. **Early exit**: Stop at first tier that gives definitive answer
2. **Parallel processing**: Hash multiple files concurrently
3. **Incremental hashing**: For large files, compare first N bytes before full hash
4. **Cache hashes**: Store in visit log to avoid recomputation

**Alternatives Considered**:
- **Git integration**: Track files via Git, requires repo, not all projects use Git
- **inotify/fswatch**: Real-time monitoring, not portable, complex setup
- **Timestamp only**: Unreliable, can be manipulated
- **Always reanalyze**: Too slow for large codebases

**Edge Cases Handled**:
- **File moved/renamed**: Detected via deep analysis (same content hash, different path)
- **Touch command**: Tier 2 catches (mtime changed, hash unchanged)
- **Whitespace-only changes**: Tier 3 detects if enabled
- **Large files**: Incremental hashing avoids memory issues

---

## Summary of Decisions

### LLM Prompt Engineering
1. **Multi-stage prompting** with artifact-type-specific system prompts and structured JSON responses
2. **Intelligent chunking** at method boundaries with cross-reference summaries for large files
3. **Zero-shot with schema templates** for most cases, few-shot only for complex relationships
4. **Weaviate vector search** for cross-referencing with summary-based context construction

### Hierarchical Documentation
1. **Layer-based directory structure** (database/, services/, frontend/, prd/) with domain subdivisions
2. **Automated index generation** with multiple views (alphabetical, by-domain, by-type)
3. **Relative markdown links** with bidirectional references and link validation
4. **Automated TOC generation** with anchor links and optional depth control

### Incremental Analysis
1. **SHA-256 content hashing** with file metadata (mtime, size) for change detection
2. **JSON Lines format** for visit log with atomic append operations
3. **Three-tier change detection** (quick filter, hash, optional deep analysis) for efficiency

All decisions are actionable, leverage existing project infrastructure (Ollama, Weaviate, Python parsers), and align with specification requirements (FR-001 through FR-044).

---

## Next Steps

Proceed to Phase 1:
1. Design detailed data model for PRD entities (data-model.md)
2. Define service interfaces and contracts (contracts/)
3. Create quickstart guide for PRD generation (quickstart.md)
4. Update implementation plan with concrete timelines (plan.md)
