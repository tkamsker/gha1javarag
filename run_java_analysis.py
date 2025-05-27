import os
from dotenv import load_dotenv
from crewai import Crew, Agent, Task
from java_crew_ai.agents.java_agents import JavaAgents
from java_crew_ai.tasks.java_tasks import JavaTasks
from java_crew_ai.analyzers.java_analyzer import JavaCodeAnalyzer
from java_crew_ai.documentation.doc_generator import DocumentationGenerator

def main():
    # Load environment variables
    load_dotenv()
    
    # Get the codebase path from environment variable
    codebase_path = os.getenv('CUCOCALC_PATH')
    if not codebase_path:
        raise ValueError("CUCOCALC_PATH environment variable not set")
    
    # Analyze the codebase
    analyzer = JavaCodeAnalyzer(codebase_path)
    analysis_result = analyzer.analyze_codebase()
    
    # Generate documentation
    doc_generator = DocumentationGenerator(analysis_result)
    doc_generator.generate_documentation()
    
    # Create agents
    agents = JavaAgents()
    parser_agent = agents.create_parser_agent()
    modeling_agent = agents.create_modeling_agent()
    specification_agent = agents.create_specification_agent()
    prd_agent = agents.create_prd_agent()
    technical_writer_agent = agents.create_technical_writer_agent()
    qa_agent = agents.create_qa_agent()
    
    # Create tasks
    tasks = JavaTasks()
    parsing_task = tasks.create_parsing_task(parser_agent)
    modeling_task = tasks.create_modeling_task(modeling_agent)
    specification_task = tasks.create_specification_task(specification_agent)
    prd_task = tasks.create_prd_task(prd_agent)
    technical_requirements_task = tasks.create_technical_requirements_task(technical_writer_agent)
    acceptance_criteria_task = tasks.create_acceptance_criteria_task(qa_agent)
    
    # Create and run the crew
    crew = Crew(
        agents=[
            parser_agent,
            modeling_agent,
            specification_agent,
            prd_agent,
            technical_writer_agent,
            qa_agent
        ],
        tasks=[
            parsing_task,
            modeling_task,
            specification_task,
            prd_task,
            technical_requirements_task,
            acceptance_criteria_task
        ],
        verbose=True
    )
    
    # Execute tasks and get results
    result = crew.kickoff()
    
    # Create output directory if it doesn't exist
    os.makedirs("documentation", exist_ok=True)
    
    # Write the full analysis results
    with open("documentation/java_analysis_results.txt", "w") as f:
        f.write(str(result))
    
    # Extract and write PRD
    with open("documentation/product_requirements.md", "w") as f:
        f.write("# Product Requirements Document\n\n")
        # Extract PRD content from the result
        prd_content = str(result).split("Product Requirements Document")[-1].split("Technical Requirements")[0]
        f.write(prd_content.strip())
    
    # Extract and write technical requirements
    with open("documentation/technical_requirements.md", "w") as f:
        f.write("# Technical Requirements\n\n")
        # Extract technical requirements content from the result
        tech_content = str(result).split("Technical Requirements")[-1].split("Acceptance Criteria")[0]
        f.write(tech_content.strip())
    
    # Extract and write acceptance criteria
    with open("documentation/acceptance_criteria.md", "w") as f:
        f.write("# Acceptance Criteria\n\n")
        # Extract acceptance criteria content from the result
        criteria_content = str(result).split("Acceptance Criteria")[-1]
        f.write(criteria_content.strip())

if __name__ == "__main__":
    main() 