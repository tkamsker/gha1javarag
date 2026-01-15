"""
Base agent configuration and data structures for CrewAI multi-agent system.

This module defines the core data structures used across all agents including
agent configuration, response format, and base tool definitions.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


class AgentRole(Enum):
    """Available agent roles in the system."""
    SENIOR_DEVELOPER = "Senior Developer"
    DATA_ANALYST = "Data Analyst"
    FRONTEND_SPECIALIST = "Frontend Specialist"
    BACKEND_SPECIALIST = "Backend Specialist"
    PRD_WRITER = "PRD Writer"
    SPECKIT_WRITER = "Spec-Kit Writer"
    GHERKIN_TEST_WRITER = "Gherkin Test Writer"
    PLAYWRIGHT_TEST_WRITER = "Playwright Test Writer"


@dataclass
class AgentConfig:
    """
    Configuration for a CrewAI agent.

    This dataclass defines all configuration parameters for an agent including
    identity, behavior, LLM settings, tools, and output formatting.
    """

    # Identity
    role: AgentRole
    goal: str
    backstory: str

    # Behavior
    verbose: bool = True
    max_iterations: int = 10
    allow_delegation: bool = False

    # LLM Settings
    llm_model: str = "gemma3:12b"
    temperature: float = 0.7
    max_tokens: int = 2000

    # Tools (assigned at runtime, tool names as strings)
    tools: List[str] = field(default_factory=list)

    # Output Formatting
    output_format: str = "markdown"  # 'markdown', 'json', 'text'
    citation_style: str = "inline"   # 'inline', 'footnotes', 'none'
    technical_level: str = "senior"  # 'junior', 'mid', 'senior'

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "role": self.role.value,
            "goal": self.goal,
            "backstory": self.backstory,
            "verbose": self.verbose,
            "max_iterations": self.max_iterations,
            "allow_delegation": self.allow_delegation,
            "llm_model": self.llm_model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "tools": self.tools,
            "output_format": self.output_format,
            "citation_style": self.citation_style,
            "technical_level": self.technical_level
        }


@dataclass
class Citation:
    """
    Citation reference to an artifact or code location.
    """
    artifact_id: str
    file_path: str
    line_start: Optional[int] = None
    line_end: Optional[int] = None
    artifact_type: Optional[str] = None
    confidence: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert citation to dictionary."""
        return {
            "artifact_id": self.artifact_id,
            "file_path": self.file_path,
            "line_start": self.line_start,
            "line_end": self.line_end,
            "artifact_type": self.artifact_type,
            "confidence": self.confidence
        }


@dataclass
class AgentResponse:
    """
    Response from an agent query.

    This dataclass defines the standard format for all agent responses including
    metadata, content, citations, quality indicators, and error handling.
    """

    # Metadata
    agent_role: AgentRole
    query: str
    timestamp: str
    duration_seconds: float

    # Content
    response_text: str
    citations: List[Citation] = field(default_factory=list)

    # Quality Indicators
    confidence: float = 0.8  # 0.0 to 1.0
    tokens_used: int = 0

    # Follow-Ups
    suggested_questions: List[str] = field(default_factory=list)

    # Metadata
    tools_used: List[str] = field(default_factory=list)

    # Error Handling
    error: Optional[str] = None
    retry_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        return {
            "agent_role": self.agent_role.value,
            "query": self.query,
            "timestamp": self.timestamp,
            "duration_seconds": self.duration_seconds,
            "response_text": self.response_text,
            "citations": [c.to_dict() for c in self.citations],
            "confidence": self.confidence,
            "tokens_used": self.tokens_used,
            "suggested_questions": self.suggested_questions,
            "tools_used": self.tools_used,
            "error": self.error,
            "retry_count": self.retry_count
        }

    def has_error(self) -> bool:
        """Check if response has an error."""
        return self.error is not None


# Default agent configurations
DEFAULT_AGENT_CONFIGS = {
    AgentRole.SENIOR_DEVELOPER: AgentConfig(
        role=AgentRole.SENIOR_DEVELOPER,
        goal="Explain code architecture, design patterns, and best practices",
        backstory=(
            "You are a senior software developer with 15+ years of experience "
            "in Java enterprise applications, GWT, and modern web architectures. "
            "You excel at explaining complex code structures in clear, concise terms "
            "and identifying potential improvements and refactoring opportunities."
        ),
        tools=["WeaviateSearchTool", "FileReadTool", "LLMQueryTool"]
    ),

    AgentRole.DATA_ANALYST: AgentConfig(
        role=AgentRole.DATA_ANALYST,
        goal="Analyze database schemas, data flows, and entity relationships",
        backstory=(
            "You specialize in database architecture, data modeling, and ETL patterns. "
            "You can map complex entity relationships, identify data quality issues, "
            "and generate comprehensive entity-relationship diagrams."
        ),
        tools=["WeaviateSearchTool", "SQLQueryTool"]
    ),

    AgentRole.FRONTEND_SPECIALIST: AgentConfig(
        role=AgentRole.FRONTEND_SPECIALIST,
        goal="Document UI components, user flows, and frontend architecture",
        backstory=(
            "You are an expert in GWT, JSP, and modern JavaScript frameworks. "
            "You can analyze UI components, map navigation flows, document form "
            "validations, and explain Presenter-View bindings in detail."
        ),
        tools=["WeaviateSearchTool", "FileReadTool"]
    ),

    AgentRole.BACKEND_SPECIALIST: AgentConfig(
        role=AgentRole.BACKEND_SPECIALIST,
        goal="Analyze backend services, APIs, and business logic",
        backstory=(
            "You specialize in backend architecture, RESTful APIs, service layers, "
            "and business logic. You can document service dependencies, explain "
            "transaction flows, and map API endpoints comprehensively."
        ),
        tools=["WeaviateSearchTool", "FileReadTool"]
    ),

    AgentRole.PRD_WRITER: AgentConfig(
        role=AgentRole.PRD_WRITER,
        goal="Generate comprehensive product requirements documents",
        backstory=(
            "You are a technical product manager who excels at translating code "
            "into product requirements. You write clear user stories, define "
            "success metrics, and create PRDs that bridge technical and business needs."
        ),
        tools=["WeaviateSearchTool", "DocumentGeneratorTool"]
    ),

    AgentRole.SPECKIT_WRITER: AgentConfig(
        role=AgentRole.SPECKIT_WRITER,
        goal="Create technical specifications and implementation plans",
        backstory=(
            "You are a software architect who creates detailed technical specifications. "
            "You define system architectures, break down features into tasks, and "
            "create implementation plans that development teams can execute."
        ),
        tools=["WeaviateSearchTool", "DocumentGeneratorTool"]
    ),

    AgentRole.GHERKIN_TEST_WRITER: AgentConfig(
        role=AgentRole.GHERKIN_TEST_WRITER,
        goal="Generate BDD test cases in Gherkin format",
        backstory=(
            "You are a QA engineer expert in Behavior-Driven Development (BDD). "
            "You write clear, comprehensive Gherkin scenarios with Given-When-Then "
            "steps, scenario outlines, and proper test data that cover happy paths, "
            "edge cases, and error scenarios."
        ),
        tools=["WeaviateSearchTool", "FileReadTool", "DocumentGeneratorTool"]
    ),

    AgentRole.PLAYWRIGHT_TEST_WRITER: AgentConfig(
        role=AgentRole.PLAYWRIGHT_TEST_WRITER,
        goal="Generate Playwright E2E test scripts for web UI automation",
        backstory=(
            "You are an automation engineer specializing in Playwright test development. "
            "You write maintainable test scripts using page object patterns, proper "
            "locators (CSS selectors, data-testid), async/await patterns, and "
            "comprehensive assertions for UI state and API responses."
        ),
        tools=["WeaviateSearchTool", "FileReadTool", "DocumentGeneratorTool"]
    ),
}


def get_agent_config(role: AgentRole, **overrides) -> AgentConfig:
    """
    Get agent configuration with optional overrides.

    Args:
        role: Agent role
        **overrides: Configuration overrides (from UI settings)

    Returns:
        AgentConfig instance

    Note:
        Maps UI settings to AgentConfig parameters:
        - "verbosity" (string: concise/standard/detailed) -> "verbose" (bool)
        - Filters out unknown parameters
    """
    base_config = DEFAULT_AGENT_CONFIGS.get(role)
    if base_config is None:
        raise ValueError(f"No default configuration for role: {role}")

    # Apply overrides
    config_dict = base_config.to_dict()

    # Map UI settings to AgentConfig parameters
    mapped_overrides = {}
    for key, value in overrides.items():
        if key == "verbosity":
            # Map verbosity string to verbose boolean
            # "concise" -> False, "standard"/"detailed" -> True
            mapped_overrides["verbose"] = value in ["standard", "detailed"]
        elif key in config_dict:
            # Only pass known parameters
            mapped_overrides[key] = value
        # Silently ignore unknown parameters (like UI-specific settings)

    config_dict.update(mapped_overrides)

    # Convert role back to enum if it was overridden as string
    if isinstance(config_dict["role"], str):
        config_dict["role"] = AgentRole(config_dict["role"])

    return AgentConfig(**config_dict)
