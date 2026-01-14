#!/usr/bin/env python3
"""
CrewAI + Ollama Multi-Agent Validation Prototype

Purpose: Validate that CrewAI can orchestrate multiple agents with Ollama backend
Status: Phase 0 Research - Technical Feasibility Validation
"""

import sys
import time
from pathlib import Path

try:
    from langchain_community.llms import Ollama
    from crewai import Agent, Task, Crew, Process
except ImportError:
    print("ERROR: Required packages not installed")
    print("Install with: pip install crewai langchain-community")
    sys.exit(1)


def create_ollama_llm(timeout: int = 300) -> Ollama:
    """Create Ollama LLM instance with configuration."""
    return Ollama(
        model="gemma3:12b",
        base_url="http://localhost:11434",
        temperature=0.7,
        timeout=timeout,
        # Reuse existing timeout/retry patterns
        num_ctx=4096,  # Context window
    )


def create_agents(llm: Ollama) -> tuple[Agent, Agent, Agent]:
    """Create 3 test agents for validation."""

    senior_dev = Agent(
        role="Senior Developer",
        goal="Analyze code architecture and identify design patterns",
        backstory=(
            "You are a senior developer with 15+ years of experience in "
            "Java enterprise applications. You excel at explaining complex "
            "architectures in clear terms."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    backend_specialist = Agent(
        role="Backend Specialist",
        goal="Analyze backend services and data access patterns",
        backstory=(
            "You specialize in backend architecture, focusing on services, "
            "DAOs, database schemas, and API design."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    prd_writer = Agent(
        role="PRD Writer",
        goal="Synthesize technical findings into clear product requirements",
        backstory=(
            "You write comprehensive PRDs that bridge technical details "
            "and business requirements."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    return senior_dev, backend_specialist, prd_writer


def create_tasks(agents: tuple[Agent, Agent, Agent]) -> list[Task]:
    """Create sequential tasks for multi-agent workflow."""
    senior_dev, backend_specialist, prd_writer = agents

    # Sample artifacts (simulating Weaviate results)
    artifacts_context = """
    Sample Artifacts:
    1. UserDAO.java - Data access for user management
       - Methods: findByUsername, create, update, delete
       - Database: users table

    2. UserService.java - Business logic for user operations
       - Dependencies: UserDAO, ValidationService
       - Methods: registerUser, authenticateUser, updateProfile

    3. UserController.java - REST API endpoints
       - Endpoints: POST /users, GET /users/{id}, PUT /users/{id}
       - Authentication: JWT-based
    """

    task1 = Task(
        description=(
            f"Analyze the following code artifacts and identify the overall "
            f"architecture pattern (e.g., MVC, layered architecture):\n\n"
            f"{artifacts_context}\n\n"
            f"Provide a brief summary (2-3 sentences) of the design pattern."
        ),
        agent=senior_dev,
        expected_output="Brief architectural pattern summary"
    )

    task2 = Task(
        description=(
            f"Based on the senior developer's analysis, examine the backend "
            f"components in detail. Focus on:\n"
            f"1. Data access patterns\n"
            f"2. Service layer responsibilities\n"
            f"3. API design\n\n"
            f"Artifacts:\n{artifacts_context}\n\n"
            f"Provide a technical summary (3-4 sentences)."
        ),
        agent=backend_specialist,
        expected_output="Backend technical summary",
        context=[task1]  # Depends on task1 output
    )

    task3 = Task(
        description=(
            f"Synthesize the architectural analysis and backend findings into "
            f"a PRD section. Include:\n"
            f"1. System Overview (based on architecture)\n"
            f"2. Key Components (based on backend analysis)\n"
            f"3. User Stories (inferred from functionality)\n\n"
            f"Keep it concise (4-5 sentences)."
        ),
        agent=prd_writer,
        expected_output="PRD section with overview and components",
        context=[task1, task2]  # Depends on both previous tasks
    )

    return [task1, task2, task3]


def run_validation() -> dict:
    """Run multi-agent workflow validation."""
    print("=" * 80)
    print("CrewAI + Ollama Multi-Agent Validation")
    print("=" * 80)
    print()

    # Check Ollama availability
    print("[1/5] Checking Ollama availability...")
    try:
        llm = create_ollama_llm()
        # Test connection with simple prompt
        response = llm("Say 'OK' if you are available.")
        print(f"✅ Ollama available: {response.strip()[:50]}")
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        return {"success": False, "error": str(e)}

    print()
    print("[2/5] Creating agents...")
    agents = create_agents(llm)
    print(f"✅ Created {len(agents)} agents")

    print()
    print("[3/5] Creating tasks...")
    tasks = create_tasks(agents)
    print(f"✅ Created {len(tasks)} tasks with dependencies")

    print()
    print("[4/5] Executing multi-agent workflow...")
    print("This may take 3-5 minutes...\n")

    start_time = time.time()

    try:
        # Create crew with sequential process (agents execute in order)
        crew = Crew(
            agents=list(agents),
            tasks=tasks,
            process=Process.sequential,  # Sequential execution with context passing
            verbose=True
        )

        # Execute workflow
        result = crew.kickoff()

        elapsed_time = time.time() - start_time

        print()
        print("=" * 80)
        print("[5/5] Workflow completed successfully!")
        print("=" * 80)
        print(f"⏱️  Total time: {elapsed_time:.1f} seconds ({elapsed_time/60:.2f} minutes)")
        print()
        print("Final Output:")
        print("-" * 80)
        print(result)
        print("-" * 80)

        return {
            "success": True,
            "elapsed_time": elapsed_time,
            "result": str(result),
            "agents_count": len(agents),
            "tasks_count": len(tasks)
        }

    except Exception as e:
        elapsed_time = time.time() - start_time
        print()
        print("=" * 80)
        print("❌ Workflow failed")
        print("=" * 80)
        print(f"Error: {e}")
        print(f"Time before failure: {elapsed_time:.1f} seconds")

        return {
            "success": False,
            "elapsed_time": elapsed_time,
            "error": str(e)
        }


def main():
    """Main entry point."""
    result = run_validation()

    print()
    print("=" * 80)
    print("Validation Summary")
    print("=" * 80)

    if result["success"]:
        print("✅ SUCCESS - Multi-agent workflow validation passed")
        print()
        print("Key Findings:")
        print(f"  - CrewAI + Ollama integration: WORKING")
        print(f"  - Agent count: {result['agents_count']}")
        print(f"  - Task count: {result['tasks_count']}")
        print(f"  - Execution time: {result['elapsed_time']:.1f}s")
        print(f"  - Target: <300s (5 minutes)")
        print(f"  - Status: {'PASS' if result['elapsed_time'] < 300 else 'FAIL'}")
        print()
        print("Recommendation: PROCEED with Feature 009 implementation")
        sys.exit(0)
    else:
        print("❌ FAILED - Multi-agent workflow validation failed")
        print()
        print(f"Error: {result['error']}")
        print()
        print("Recommendation: INVESTIGATE and resolve before proceeding")
        sys.exit(1)


if __name__ == "__main__":
    main()
