import os
from dotenv import load_dotenv
from crewai import Crew
from java_crew_ai.agents.java_agents import JavaAgents
from java_crew_ai.tasks.java_tasks import JavaTasks

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize agents
    java_agents = JavaAgents()
    parser_agent = java_agents.create_parser_agent()
    modeling_agent = java_agents.create_modeling_agent()
    specification_agent = java_agents.create_specification_agent()
    
    # Create tasks
    java_tasks = JavaTasks()
    parsing_task = java_tasks.create_parsing_task(parser_agent)
    modeling_task = java_tasks.create_modeling_task(modeling_agent)
    specification_task = java_tasks.create_specification_task(specification_agent)
    
    # Create and run the crew
    crew = Crew(
        agents=[parser_agent, modeling_agent, specification_agent],
        tasks=[parsing_task, modeling_task, specification_task],
        verbose=True
    )
    
    # Execute the crew's tasks
    result = crew.kickoff()
    
    # Save the results
    with open("analysis_results.md", "w") as f:
        f.write("# Java Codebase Analysis Results\n\n")
        f.write(result)

if __name__ == "__main__":
    main() 