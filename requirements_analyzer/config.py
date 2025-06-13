import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR.parent / "semantic" / "data"
RESULTS_DIR = DATA_DIR / "results"

# Input files
CLUSTERS_FILE = os.getenv("CLUSTERS_FILE", str(RESULTS_DIR / "clusters_by_class.json"))
ANALYSIS_REPORT_FILE = os.getenv("ANALYSIS_REPORT_FILE", str(BASE_DIR / "analysis_report.json"))

# Output directories
OUTPUT_DIR = BASE_DIR / "detailed_docs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Output files
SERVLET_ANALYSIS_FILE = OUTPUT_DIR / "servlet_analysis.md"
DATA_MODEL_FILE = OUTPUT_DIR / "data_model.md"
BUSINESS_RULES_FILE = OUTPUT_DIR / "business_rules.md"

# Documentation templates
DOC_TEMPLATES = {
    "servlet": {
        "header": "# Servlet Analysis\n\n",
        "section": "## {name}\n\n",
        "input_params": "### Input Parameters\n\n",
        "output_dest": "### Output Destinations\n\n",
        "error_handling": "### Error Handling\n\n"
    },
    "data_model": {
        "header": "# Data Model Specification\n\n",
        "section": "## {name}\n\n",
        "attributes": "### Attributes\n\n",
        "relationships": "### Relationships\n\n",
        "constraints": "### Constraints\n\n"
    },
    "business_rules": {
        "header": "# Business Rules Catalog\n\n",
        "section": "## {id}\n\n",
        "description": "### Description\n{description}\n\n",
        "source_files": "### Source Files\n",
        "affected_entities": "### Affected Entities\n",
        "validation_logic": "### Validation Logic\n"
    }
}

# Regex patterns for code analysis
CODE_PATTERNS = {
    "param": r'@param\s+(\w+)\s+(.*?)(?=@|\Z)',
    "db_operation": r'(?:executeQuery|executeUpdate|prepareStatement).*?["\'](.*?)["\']',
    "error_handling": r'try\s*{([^}]*)}.*?catch\s*\(([^)]*)\)\s*{([^}]*)}',
    "class": r'class\s+(\w+)\s*{([^}]*)}',
    "attribute": r'private\s+(\w+)\s+(\w+)\s*;',
    "validation": r'(?:validate|check|isValid).*?{([^}]*)}'
}

# Logging configuration
LOG_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": BASE_DIR / "docs_generator.log"
} 