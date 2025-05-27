from crewai import Agent
from java_crew_ai.tools.rag_tools import chroma_search_tool, code_analysis_tool

class JavaAgents:
    def __init__(self):
        self.chroma_tool = chroma_search_tool
        self.code_analysis_tool = code_analysis_tool
    
    def create_parser_agent(self) -> Agent:
        """Creates an agent specialized in parsing and understanding Java code structure."""
        return Agent(
            role='Java Code Parser',
            goal='Parse and understand Java code structure, identifying classes, methods, and their relationships',
            backstory="""You are an expert Java code parser with deep knowledge of Java syntax, 
            design patterns, and best practices. Your specialty is breaking down complex Java code 
            into understandable components and identifying key structural elements.""",
            tools=[self.chroma_tool, self.code_analysis_tool],
            verbose=True
        )
    
    def create_modeling_agent(self) -> Agent:
        """Creates an agent specialized in modeling and architecture analysis."""
        return Agent(
            role='Java Architecture Modeler',
            goal='Analyze and model Java application architecture, identifying patterns and suggesting improvements',
            backstory="""You are a senior Java architect with extensive experience in enterprise 
            applications. Your expertise lies in understanding system architecture, identifying 
            design patterns, and suggesting architectural improvements.""",
            tools=[self.chroma_tool, self.code_analysis_tool],
            verbose=True
        )
    
    def create_specification_agent(self) -> Agent:
        """Creates an agent specialized in generating technical specifications."""
        return Agent(
            role='Technical Specification Writer',
            goal='Generate detailed technical specifications based on code analysis',
            backstory="""You are a technical writer specialized in Java applications. 
            Your strength is in creating clear, detailed technical specifications that 
            bridge the gap between code and documentation.""",
            tools=[self.chroma_tool, self.code_analysis_tool],
            verbose=True
        )

    def create_prd_agent(self) -> Agent:
        """Creates an agent specialized in generating Product Requirements Documents."""
        return Agent(
            role='Product Requirements Document Writer',
            goal='Create comprehensive PRDs with user stories and requirements',
            backstory="""You are an expert product manager with extensive experience in 
            creating detailed PRDs. Your specialty is translating technical capabilities 
            into clear user stories and requirements that follow industry best practices.""",
            tools=[self.chroma_tool, self.code_analysis_tool],
            verbose=True
        )

    def create_technical_writer_agent(self) -> Agent:
        """Creates an agent specialized in technical documentation."""
        return Agent(
            role='Technical Documentation Writer',
            goal='Create detailed technical requirements and specifications',
            backstory="""You are a senior technical writer with deep knowledge of software 
            development and documentation best practices. Your expertise lies in creating 
            clear, comprehensive technical documentation that serves both developers and 
            stakeholders.""",
            tools=[self.chroma_tool, self.code_analysis_tool],
            verbose=True
        )

    def create_qa_agent(self) -> Agent:
        """Creates an agent specialized in defining acceptance criteria."""
        return Agent(
            role='Quality Assurance Specialist',
            goal='Define clear acceptance criteria and test scenarios',
            backstory="""You are a senior QA engineer with extensive experience in defining 
            acceptance criteria and test scenarios. Your specialty is ensuring that all 
            requirements are testable and that edge cases are properly considered.""",
            tools=[self.chroma_tool, self.code_analysis_tool],
            verbose=True
        ) 