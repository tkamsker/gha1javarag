import os
from dotenv import load_dotenv
from crewai import Crew, Agent, Task
from java_crew_ai.agents.java_agents import JavaAgents
from java_crew_ai.tasks.java_tasks import JavaTasks

def main():
    # Load environment variables
    load_dotenv()
    
    # Create agents
    agents = JavaAgents()
    parser_agent = agents.create_parser_agent()
    modeling_agent = agents.create_modeling_agent()
    specification_agent = agents.create_specification_agent()
    
    # Create tasks
    tasks = JavaTasks()
    parsing_task = tasks.create_parsing_task(parser_agent)
    modeling_task = tasks.create_modeling_task(modeling_agent)
    specification_task = tasks.create_specification_task(specification_agent)
    
    # Create and run the crew
    crew = Crew(
        agents=[parser_agent, modeling_agent, specification_agent],
        tasks=[parsing_task, modeling_task, specification_task],
        verbose=True
    )
    
    result = crew.kickoff()
    
    # Convert result to string and write to file
    with open("java_analysis_results.txt", "w") as f:
        f.write(str(result))

if __name__ == "__main__":
    main() 