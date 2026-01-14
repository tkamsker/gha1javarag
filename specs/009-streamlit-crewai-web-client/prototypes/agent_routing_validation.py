#!/usr/bin/env python3
"""
Agent Routing Algorithm Validation Prototype

Purpose: Validate keyword-based routing can achieve >90% accuracy in <5ms
Status: Phase 0 Research - Technical Feasibility Validation
"""

import time
import re
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum


class AgentRole(Enum):
    """Available agent roles."""
    SENIOR_DEVELOPER = "Senior Developer"
    DATA_ANALYST = "Data Analyst"
    FRONTEND_SPECIALIST = "Frontend Specialist"
    BACKEND_SPECIALIST = "Backend Specialist"
    PRD_WRITER = "PRD Writer"
    SPECKIT_WRITER = "Spec-Kit Writer"
    GHERKIN_TEST_WRITER = "Gherkin Test Writer"
    PLAYWRIGHT_TEST_WRITER = "Playwright Test Writer"


@dataclass
class RoutingRule:
    """Routing rule based on keyword matching."""
    agent: AgentRole
    keywords: List[str]
    patterns: List[str]  # Regex patterns
    weight: int = 1


# Define routing rules (optimized keyword heuristics)
ROUTING_RULES = [
    # Data Analyst - Database and schema questions
    RoutingRule(
        agent=AgentRole.DATA_ANALYST,
        keywords=["database", "schema", "table", "column", "foreign key", "index",
                  "sql", "query", "entity", "relationship", "erd", "data model"],
        patterns=[r"\btable\w*\b", r"\bcolumn\w*\b", r"\bforeign\s+key", r"\bprimary\s+key"],
        weight=2
    ),

    # Frontend Specialist - UI and presentation questions
    RoutingRule(
        agent=AgentRole.FRONTEND_SPECIALIST,
        keywords=["ui", "view", "presenter", "form", "widget", "jsp", "gwt",
                  "template", "frontend", "user interface", "screen", "page"],
        patterns=[r"\bui\b", r"\bgwt\b", r"\bjsp\b", r"\bview\b", r"\bwidget\w*\b"],
        weight=2
    ),

    # Backend Specialist - Services and API questions
    RoutingRule(
        agent=AgentRole.BACKEND_SPECIALIST,
        keywords=["service", "dao", "api", "endpoint", "rest", "rpc", "servlet",
                  "backend", "business logic", "controller", "repository"],
        patterns=[r"\bservice\w*\b", r"\bdao\b", r"\bapi\b", r"\bendpoint\w*\b"],
        weight=2
    ),

    # PRD Writer - Requirements and documentation
    RoutingRule(
        agent=AgentRole.PRD_WRITER,
        keywords=["prd", "requirements", "user story", "feature", "requirement",
                  "specification", "document", "documentation"],
        patterns=[r"\bprd\b", r"\brequirement\w*\b", r"\buser\s+stor"],
        weight=2
    ),

    # Spec-Kit Writer - Technical specifications
    RoutingRule(
        agent=AgentRole.SPECKIT_WRITER,
        keywords=["spec", "specification", "technical spec", "design doc",
                  "implementation plan", "architecture doc"],
        patterns=[r"\bspec\b", r"\btechnical\s+spec"],
        weight=2
    ),

    # Gherkin Test Writer - BDD tests
    RoutingRule(
        agent=AgentRole.GHERKIN_TEST_WRITER,
        keywords=["gherkin", "bdd", "given when then", "scenario", "feature file",
                  "acceptance criteria", "behavior", "cucumber"],
        patterns=[r"\bgherkin\b", r"\bbdd\b", r"\bgiven\s+when\s+then"],
        weight=2
    ),

    # Playwright Test Writer - E2E tests
    RoutingRule(
        agent=AgentRole.PLAYWRIGHT_TEST_WRITER,
        keywords=["playwright", "e2e", "end to end", "browser test", "ui test",
                  "selenium", "test automation", "locator"],
        patterns=[r"\bplaywright\b", r"\be2e\b", r"\bend.to.end"],
        weight=2
    ),

    # Senior Developer - Architecture and general questions (fallback)
    RoutingRule(
        agent=AgentRole.SENIOR_DEVELOPER,
        keywords=["architecture", "design pattern", "explain", "how does", "what is",
                  "code", "class", "method", "function", "module"],
        patterns=[r"\bexplain\b", r"\bhow\s+does\b", r"\bwhat\s+is\b", r"\barchitecture\b"],
        weight=1  # Lower weight = fallback agent
    ),
]


def route_query(query: str) -> Tuple[AgentRole, int, float]:
    """
    Route query to appropriate agent using keyword matching.

    Returns:
        (agent_role, score, elapsed_ms)
    """
    start_time = time.perf_counter()

    query_lower = query.lower()
    scores = {}

    # Calculate scores for each agent
    for rule in ROUTING_RULES:
        score = 0

        # Keyword matching
        for keyword in rule.keywords:
            if keyword in query_lower:
                score += rule.weight

        # Pattern matching
        for pattern in rule.patterns:
            if re.search(pattern, query_lower):
                score += rule.weight

        if score > 0:
            scores[rule.agent] = scores.get(rule.agent, 0) + score

    # Select agent with highest score
    if scores:
        best_agent = max(scores, key=scores.get)
        best_score = scores[best_agent]
    else:
        # Fallback to Senior Developer for unmatched queries
        best_agent = AgentRole.SENIOR_DEVELOPER
        best_score = 0

    elapsed_ms = (time.perf_counter() - start_time) * 1000
    return best_agent, best_score, elapsed_ms


# Test dataset with expected agent assignments
TEST_QUERIES = [
    # Data Analyst
    ("What tables are in the database?", AgentRole.DATA_ANALYST),
    ("Show me the entity relationship diagram", AgentRole.DATA_ANALYST),
    ("Explain the foreign key relationships", AgentRole.DATA_ANALYST),
    ("What columns are in the users table?", AgentRole.DATA_ANALYST),

    # Frontend Specialist
    ("Explain the user registration form", AgentRole.FRONTEND_SPECIALIST),
    ("What widgets are used in the login screen?", AgentRole.FRONTEND_SPECIALIST),
    ("Describe the GWT presenter for user management", AgentRole.FRONTEND_SPECIALIST),
    ("Show me the JSP templates", AgentRole.FRONTEND_SPECIALIST),

    # Backend Specialist
    ("Explain the UserService business logic", AgentRole.BACKEND_SPECIALIST),
    ("What endpoints does the API expose?", AgentRole.BACKEND_SPECIALIST),
    ("How does the DAO access the database?", AgentRole.BACKEND_SPECIALIST),
    ("Describe the REST API for user management", AgentRole.BACKEND_SPECIALIST),

    # PRD Writer
    ("Generate a PRD for the authentication module", AgentRole.PRD_WRITER),
    ("What are the user stories for checkout?", AgentRole.PRD_WRITER),
    ("Write product requirements for payment processing", AgentRole.PRD_WRITER),

    # Spec-Kit Writer
    ("Create a technical spec for the new feature", AgentRole.SPECKIT_WRITER),
    ("Write an implementation plan", AgentRole.SPECKIT_WRITER),

    # Gherkin Test Writer
    ("Generate Gherkin scenarios for login", AgentRole.GHERKIN_TEST_WRITER),
    ("Create BDD tests with given when then", AgentRole.GHERKIN_TEST_WRITER),

    # Playwright Test Writer
    ("Generate Playwright E2E tests for checkout", AgentRole.PLAYWRIGHT_TEST_WRITER),
    ("Create browser tests with Playwright", AgentRole.PLAYWRIGHT_TEST_WRITER),

    # Senior Developer (architecture/general)
    ("Explain the overall architecture", AgentRole.SENIOR_DEVELOPER),
    ("What design patterns are used?", AgentRole.SENIOR_DEVELOPER),
    ("How does the authentication flow work?", AgentRole.SENIOR_DEVELOPER),
    ("What is the purpose of this class?", AgentRole.SENIOR_DEVELOPER),
]


def run_validation():
    """Run routing validation against test queries."""
    print("=" * 80)
    print("Agent Routing Algorithm Validation")
    print("=" * 80)
    print(f"\nTest dataset: {len(TEST_QUERIES)} queries")
    print(f"Available agents: {len(set(AgentRole))} agents")
    print()

    correct = 0
    total = len(TEST_QUERIES)
    latencies = []
    errors = []

    print("Routing test results:")
    print("-" * 80)

    for query, expected_agent in TEST_QUERIES:
        routed_agent, score, elapsed_ms = route_query(query)
        latencies.append(elapsed_ms)

        is_correct = routed_agent == expected_agent
        if is_correct:
            correct += 1
            status = "✅"
        else:
            status = "❌"
            errors.append({
                "query": query,
                "expected": expected_agent.value,
                "routed": routed_agent.value,
                "score": score
            })

        print(f"{status} {query[:60]:<60} → {routed_agent.value:<20} ({elapsed_ms:.2f}ms)")

    # Calculate metrics
    accuracy = (correct / total) * 100
    avg_latency = sum(latencies) / len(latencies)
    p95_latency = sorted(latencies)[int(len(latencies) * 0.95)]

    print("-" * 80)
    print()
    print("=" * 80)
    print("Validation Summary")
    print("=" * 80)
    print()
    print("Performance Metrics:")
    print(f"  Accuracy: {correct}/{total} ({accuracy:.1f}%)")
    print(f"  Target: >90%")
    print(f"  Status: {'✅ PASS' if accuracy >= 90 else '❌ FAIL'}")
    print()
    print(f"  Average latency: {avg_latency:.2f}ms")
    print(f"  P95 latency: {p95_latency:.2f}ms")
    print(f"  Target: <5ms")
    print(f"  Status: {'✅ PASS' if p95_latency < 5 else '⚠️  ACCEPTABLE' if p95_latency < 10 else '❌ FAIL'}")
    print()

    if errors:
        print(f"Routing Errors ({len(errors)}):")
        for i, error in enumerate(errors[:5], 1):  # Show first 5 errors
            print(f"  {i}. \"{error['query'][:50]}...\"")
            print(f"     Expected: {error['expected']}, Got: {error['routed']} (score: {error['score']})")
        if len(errors) > 5:
            print(f"  ... and {len(errors) - 5} more errors")
        print()

    # Final verdict
    if accuracy >= 90 and p95_latency < 10:
        print("✅ SUCCESS - Agent routing validation passed")
        print()
        print("Recommendation: PROCEED with keyword-based routing algorithm")
        return 0
    elif accuracy >= 80:
        print("⚠️  PARTIAL SUCCESS - Routing accuracy acceptable but below target")
        print()
        print("Recommendation: REFINE keyword rules or consider hybrid approach (keywords + LLM fallback)")
        return 0
    else:
        print("❌ FAILED - Agent routing accuracy below minimum threshold")
        print()
        print("Recommendation: REDESIGN routing algorithm or use LLM-based classification")
        return 1


def main():
    """Main entry point."""
    exit(run_validation())


if __name__ == "__main__":
    main()
