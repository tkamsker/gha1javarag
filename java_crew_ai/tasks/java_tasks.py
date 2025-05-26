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