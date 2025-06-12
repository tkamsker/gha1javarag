# Requirements Analyzer

This application analyzes Java code clusters to extract requirements and persistence information from the source code.

## Features

- Extracts requirements from Java source code
- Identifies database persistence patterns
- Analyzes SQL operations and table structures
- Generates structured reports

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your clusters_by_class.json file in the semantic/data/results/ directory
2. Run the analyzer:
```bash
python analyzer.py
```

3. The analysis report will be generated in requirements_analyzer/analysis_report.json

## Output Format

The analysis report contains:

- Requirements list with:
  - Name
  - Description
  - Source file
  - Category
  - Persistence information (if applicable)
- Summary statistics:
  - Total number of requirements
  - Categories found
  - Database tables identified

## Example Output

```json
{
  "requirements": [
    {
      "name": "AddDoctor",
      "description": "Handles doctor registration",
      "source_file": "Controller/AddDoctor.java",
      "category": "Controller",
      "persistence_info": {
        "table_name": "doctor",
        "fields": ["id", "fname", "lname", "gender", "phone", "city", "email", "age", "address", "DateAndTime", "qualification"],
        "operations": ["insert"]
      }
    }
  ],
  "summary": {
    "total_requirements": 1,
    "categories": ["Controller"],
    "persistence_tables": ["doctor"]
  }
}
``` 