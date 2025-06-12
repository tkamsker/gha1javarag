import json
import re
from dataclasses import dataclass
from typing import List, Dict, Optional
from pathlib import Path

@dataclass
class Requirement:
    name: str
    description: str
    source_file: str
    category: str
    persistence_info: Optional[Dict] = None

@dataclass
class PersistenceInfo:
    table_name: str
    fields: List[str]
    operations: List[str]

class RequirementsAnalyzer:
    def __init__(self, clusters_file: str):
        self.clusters_file = clusters_file
        self.requirements: List[Requirement] = []
        self.persistence_patterns: Dict[str, PersistenceInfo] = {}
        
    def load_clusters(self) -> Dict:
        """Load and parse the clusters JSON file."""
        with open(self.clusters_file, 'r') as f:
            return json.load(f)
            
    def extract_persistence_info(self, source_code: str) -> Optional[PersistenceInfo]:
        """Extract database persistence information from source code."""
        # Look for SQL operations
        sql_patterns = {
            'insert': r'insert\s+into\s+(\w+)\s+values',
            'update': r'update\s+(\w+)\s+set',
            'delete': r'delete\s+from\s+(\w+)',
            'select': r'select\s+.*\s+from\s+(\w+)'
        }
        
        operations = []
        table_name = None
        
        for op, pattern in sql_patterns.items():
            matches = re.finditer(pattern, source_code, re.IGNORECASE)
            for match in matches:
                operations.append(op)
                if not table_name:
                    table_name = match.group(1)
                    
        if not table_name:
            return None
            
        # Extract fields from prepared statements
        field_pattern = r'pst\.set\w+\(\d+,\s*(\w+)\)'
        fields = list(set(re.findall(field_pattern, source_code)))
        
        return PersistenceInfo(
            table_name=table_name,
            fields=fields,
            operations=operations
        )
        
    def analyze_cluster(self, cluster_name: str, cluster_data: Dict):
        """Analyze a single cluster and extract requirements."""
        for class_name, artifacts in cluster_data.items():
            for artifact in artifacts:
                if 'source_code' not in artifact:
                    continue
                    
                source_code = artifact['source_code']
                source_file = artifact.get('source_file', '')
                
                # Extract persistence information
                persistence_info = self.extract_persistence_info(source_code)
                
                # Create requirement
                requirement = Requirement(
                    name=class_name,
                    description=artifact.get('description', ''),
                    source_file=source_file,
                    category=cluster_name,
                    persistence_info=persistence_info.__dict__ if persistence_info else None
                )
                
                self.requirements.append(requirement)
                
    def analyze(self):
        """Main analysis method."""
        clusters = self.load_clusters()
        
        for cluster_name, cluster_data in clusters.items():
            self.analyze_cluster(cluster_name, cluster_data)
            
    def generate_report(self, output_file: str):
        """Generate a structured report of requirements and persistence information."""
        report = {
            'requirements': [r.__dict__ for r in self.requirements],
            'summary': {
                'total_requirements': len(self.requirements),
                'categories': list(set(r.category for r in self.requirements)),
                'persistence_tables': list(set(
                    r.persistence_info['table_name'] 
                    for r in self.requirements 
                    if r.persistence_info
                ))
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
            
def main():
    # Use the correct path to the clusters file
    clusters_file = Path(__file__).parent.parent / 'semantic' / 'data' / 'results' / 'clusters_by_class.json'
    output_file = Path(__file__).parent / 'analysis_report.json'
    
    analyzer = RequirementsAnalyzer(str(clusters_file))
    analyzer.analyze()
    analyzer.generate_report(str(output_file))

if __name__ == '__main__':
    main() 