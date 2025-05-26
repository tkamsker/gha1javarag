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