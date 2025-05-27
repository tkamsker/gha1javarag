from crewai import Task
from typing import List

class JavaTasks:
    @staticmethod
    def create_parsing_task(agent) -> Task:
        """Creates a task for parsing and understanding Java code structure."""
        return Task(
            description="""Analyze the Java codebase to:
            1. Identify all major classes and their relationships
            2. Map out method hierarchies and dependencies
            3. Document key design patterns used
            4. Identify potential code smells or areas for improvement""",
            agent=agent,
            expected_output="A detailed analysis of the codebase structure and relationships"
        )
    
    @staticmethod
    def create_modeling_task(agent) -> Task:
        """Creates a task for architectural modeling and analysis."""
        return Task(
            description="""Based on the code analysis:
            1. Create an architectural model of the system
            2. Identify and document design patterns
            3. Suggest architectural improvements
            4. Map out system dependencies and interactions""",
            agent=agent,
            expected_output="A comprehensive architectural model and improvement suggestions"
        )
    
    @staticmethod
    def create_specification_task(agent) -> Task:
        """Creates a task for generating technical specifications."""
        return Task(
            description="""Using the analysis and modeling results:
            1. Generate detailed technical specifications
            2. Document system architecture
            3. Create API documentation
            4. Write implementation guidelines""",
            agent=agent,
            expected_output="Complete technical specifications and documentation"
        ) 

    @staticmethod
    def create_prd_task(agent) -> Task:
        """Creates a task for generating Product Requirements Document."""
        return Task(
            description="""For each major component and feature in the codebase:
            1. Identify user roles and their needs
            2. Write user stories in the format: "As a [user role], I want [action] so that [benefit]"
            3. Group related user stories by feature/component
            4. Prioritize features based on business value
            5. Document non-functional requirements
            6. Create a structured PRD following industry best practices""",
            agent=agent,
            expected_output="A comprehensive Product Requirements Document in markdown format"
        )

    @staticmethod
    def create_technical_requirements_task(agent) -> Task:
        """Creates a task for generating technical requirements."""
        return Task(
            description="""For each directory and major component:
            1. Document technical requirements and constraints
            2. Specify system architecture details
            3. Define API contracts and interfaces
            4. Document data models and schemas
            5. Specify performance requirements
            6. Document security requirements
            7. List third-party dependencies and their versions
            8. Create a structured technical requirements document""",
            agent=agent,
            expected_output="A detailed technical requirements document in markdown format"
        )

    @staticmethod
    def create_acceptance_criteria_task(agent) -> Task:
        """Creates a task for generating acceptance criteria."""
        return Task(
            description="""For each feature and component:
            1. Define clear acceptance criteria
            2. Specify test scenarios
            3. Document expected behaviors
            4. Define success metrics
            5. List edge cases to consider
            6. Create a structured acceptance criteria document""",
            agent=agent,
            expected_output="A comprehensive acceptance criteria document in markdown format"
        ) 