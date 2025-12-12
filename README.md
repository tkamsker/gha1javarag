# GEMINI Code Analysis and PRD Generator

This project is a Python-based pipeline that analyzes Java/JSP/GWT/JavaScript codebases, extracts structured information, and generates high-quality Product Requirements Documents (PRDs) and requirements from the code itself.

# Prompt : perplexit 
you are an IT expert and we are tasked to generate requirements from source codes  organized in directories of subprojects where .env variable JAVA_SOURCE_DIR points to start of directories take all details from GEMINI.md file and write an initial document to be used by [https://github.com/github/spec-kit](https://github.com/github/spec-kit)  where we have one part which is reading into the aviate database for later use and then generating requirements for backend services and frontends do it step by step and then we need to create prd files to have best results using spec kit for deploying