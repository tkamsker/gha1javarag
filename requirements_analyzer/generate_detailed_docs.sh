#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the documentation generator
python detailed_docs_generator.py

# Check if the generation was successful
if [ $? -eq 0 ]; then
    echo "Detailed documentation generated successfully!"
    echo "Check the 'detailed_docs' directory for the following files:"
    echo "- servlet_analysis.md: Analysis of JSP/Servlet components"
    echo "- data_model.md: Data model specification"
    echo "- business_rules.md: Business rules catalog"
else
    echo "Error generating documentation"
    exit 1
fi 