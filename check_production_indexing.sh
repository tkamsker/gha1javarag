#!/bin/bash

#############################################
# Production Indexing Status Checker
# Run this on vlcucad001-eatnl to check indexing status
#############################################

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PROJECT_NAME="${1:-cuco-ui-admin}"
SOURCE_DIR="${2:-/mnt/cucocalcai/cuco-master/cuco-master@d34bb6b6d1c/cuco-ui-admin}"

echo "=============================================="
echo "Production Indexing Status Check"
echo "=============================================="
echo "Project:    $PROJECT_NAME"
echo "Source:     $SOURCE_DIR"
echo "Date:       $(date)"
echo "=============================================="
echo ""

# Function to print status
print_status() {
    local status=$1
    local message=$2
    if [ "$status" == "PASS" ]; then
        echo -e "${GREEN}[✓ PASS]${NC} $message"
    elif [ "$status" == "FAIL" ]; then
        echo -e "${RED}[✗ FAIL]${NC} $message"
    elif [ "$status" == "WARN" ]; then
        echo -e "${YELLOW}[⚠ WARN]${NC} $message"
    else
        echo -e "${BLUE}[INFO]${NC} $message"
    fi
}

# Check 1: Source directory
print_status "INFO" "Check 1: Source Directory"
if [ -d "$SOURCE_DIR" ]; then
    java_count=$(find "$SOURCE_DIR" -name "*.java" -type f 2>/dev/null | wc -l | tr -d ' ')
    jsp_count=$(find "$SOURCE_DIR" -name "*.jsp" -type f 2>/dev/null | wc -l | tr -d ' ')
    xml_count=$(find "$SOURCE_DIR" -name "*.xml" -type f 2>/dev/null | wc -l | tr -d ' ')
    print_status "PASS" "Source directory exists"
    print_status "INFO" "  Found: $java_count Java, $jsp_count JSP, $xml_count XML files"
else
    print_status "FAIL" "Source directory not found: $SOURCE_DIR"
    exit 1
fi
echo ""

# Check 2: Discovery file
print_status "INFO" "Check 2: Discovery File (data/discovery-$PROJECT_NAME.jsonl)"
DISCOVERY_FILE="data/discovery-$PROJECT_NAME.jsonl"
if [ -f "$DISCOVERY_FILE" ]; then
    line_count=$(wc -l < "$DISCOVERY_FILE" | tr -d ' ')
    print_status "PASS" "Discovery file exists: $line_count lines"

    # Check actual file count in JSON
    python3 << EOF
import json
import sys

try:
    with open("$DISCOVERY_FILE") as f:
        lines = f.readlines()

    for line in lines:
        data = json.loads(line)
        if 'files' in data:
            file_count = len(data['files'])
            print(f"  Files discovered in JSON: {file_count:,}")
            if file_count > 0:
                # Show sample file types
                sample = data['files'][:3]
                for f in sample:
                    print(f"    - {f.get('file_type', 'unknown')}: {f.get('path', 'N/A')}")
            sys.exit(0)
        elif 'total_files' in data:
            print(f"  Total files in metadata: {data['total_files']:,}")

    print("  Warning: No 'files' array found in discovery JSON")
    sys.exit(1)
except Exception as e:
    print(f"  Error parsing discovery file: {e}")
    sys.exit(1)
EOF

    if [ $? -eq 0 ]; then
        print_status "PASS" "Discovery file contains valid project data"
    else
        print_status "FAIL" "Discovery file has invalid structure"
    fi
else
    print_status "FAIL" "Discovery file not found"
fi
echo ""

# Check 3: Extraction file
print_status "INFO" "Check 3: Extraction File (data/extraction-$PROJECT_NAME.jsonl)"
EXTRACTION_FILE="data/extraction-$PROJECT_NAME.jsonl"
if [ -f "$EXTRACTION_FILE" ]; then
    line_count=$(wc -l < "$EXTRACTION_FILE" | tr -d ' ')
    print_status "PASS" "Extraction file exists: $line_count lines"

    # Count artifacts by type
    python3 << EOF
import json
from collections import Counter

artifact_types = []
try:
    with open("$EXTRACTION_FILE") as f:
        for line in f:
            data = json.loads(line)
            if 'artifact_type' in data:
                artifact_types.append(data['artifact_type'])

    if artifact_types:
        counts = Counter(artifact_types)
        print(f"  Total artifacts: {len(artifact_types):,}")
        print(f"  Artifact types:")
        for atype, count in counts.most_common():
            print(f"    - {atype}: {count:,}")
    else:
        print("  Warning: No artifacts found in extraction file")
except Exception as e:
    print(f"  Error: {e}")
EOF

    if [ $? -eq 0 ]; then
        print_status "PASS" "Extraction file contains artifacts"
    else
        print_status "WARN" "Extraction file may be incomplete"
    fi
else
    print_status "FAIL" "Extraction file not found"
fi
echo ""

# Check 4: Weaviate connectivity
print_status "INFO" "Check 4: Weaviate Service"
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/v1/meta | grep -q "200"; then
    print_status "PASS" "Weaviate is accessible"
else
    print_status "FAIL" "Weaviate is not accessible at http://localhost:8080"
    print_status "INFO" "Try: docker ps | grep weaviate"
    exit 1
fi
echo ""

# Check 5: Ollama connectivity
print_status "INFO" "Check 5: Ollama Service"
if curl -s -o /dev/null -w "%{http_code}" http://localhost:11434/api/tags | grep -q "200"; then
    print_status "PASS" "Ollama is accessible"
else
    print_status "FAIL" "Ollama is not accessible at http://localhost:11434"
    print_status "INFO" "Try: ollama serve &"
fi
echo ""

# Check 6: Weaviate indexed data
print_status "INFO" "Check 6: Weaviate Indexed Data"
python3 << EOF
import sys
sys.path.insert(0, 'src')

from codeindex.services.weaviate_client import WeaviateManager

try:
    manager = WeaviateManager()
    status = manager.get_project_status()

    if not status:
        print("  Warning: No projects found in Weaviate")
        sys.exit(1)

    print(f"  Total projects in Weaviate: {len(status)}")

    target_found = False
    for project in status:
        project_id = project['project_id']
        artifact_count = project['artifact_count']
        last_indexed = project.get('last_indexed', 'Unknown')

        if "$PROJECT_NAME" in project_id:
            print(f"\n  ✓ Target project found: {project_id}")
            print(f"    Artifacts: {artifact_count:,}")
            print(f"    Last indexed: {last_indexed}")
            target_found = True

            if artifact_count == 0:
                print(f"    ⚠ WARNING: Zero artifacts indexed!")
                sys.exit(1)
        else:
            print(f"    Other: {project_id} ({artifact_count:,} artifacts)")

    if not target_found:
        print(f"\n  ⚠ WARNING: Project '$PROJECT_NAME' not found in Weaviate")
        sys.exit(1)

    sys.exit(0)
except Exception as e:
    print(f"  Error querying Weaviate: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
EOF

if [ $? -eq 0 ]; then
    print_status "PASS" "Project is indexed in Weaviate with artifacts"
else
    print_status "FAIL" "Project missing or has zero artifacts in Weaviate"
fi
echo ""

# Check 7: Search functionality
print_status "INFO" "Check 7: Search Functionality"
python3 << EOF
import sys
sys.path.insert(0, 'src')

from codeindex.services.weaviate_client import WeaviateManager

try:
    manager = WeaviateManager()
    results = manager.search("service", project_filter="$PROJECT_NAME", limit=5)

    if results:
        print(f"  Search returned {len(results)} results")
        for i, result in enumerate(results[:3], 1):
            artifact_type = result.get('artifact_type', 'unknown')
            score = result.get('_additional', {}).get('certainty', 0)
            print(f"    {i}. {artifact_type} (score: {score:.2f})")
        sys.exit(0)
    else:
        print("  Warning: Search returned no results")
        sys.exit(1)
except Exception as e:
    print(f"  Error searching: {e}")
    sys.exit(1)
EOF

if [ $? -eq 0 ]; then
    print_status "PASS" "Search is working"
else
    print_status "WARN" "Search returned no results"
fi
echo ""

# Summary
echo "=============================================="
echo "Summary & Recommendations"
echo "=============================================="

python3 << EOF
import json

discovery_ok = False
extraction_ok = False
weaviate_ok = False

# Check discovery
try:
    with open("data/discovery-$PROJECT_NAME.jsonl") as f:
        for line in f:
            data = json.loads(line)
            if 'files' in data and len(data['files']) > 0:
                discovery_ok = True
                break
except:
    pass

# Check extraction
try:
    with open("data/extraction-$PROJECT_NAME.jsonl") as f:
        lines = sum(1 for _ in f)
        if lines > 100:
            extraction_ok = True
except:
    pass

# Simple heuristic for Weaviate
import subprocess
try:
    result = subprocess.run(
        ['python3', '-c',
         'import sys; sys.path.insert(0, "src"); '
         'from codeindex.services.weaviate_client import WeaviateManager; '
         'm = WeaviateManager(); '
         's = m.get_project_status(); '
         'print(sum(1 for p in s if "$PROJECT_NAME" in p["project_id"] and p["artifact_count"] > 0))'],
        capture_output=True, text=True, timeout=10
    )
    if result.returncode == 0 and int(result.stdout.strip()) > 0:
        weaviate_ok = True
except:
    pass

print()
if discovery_ok and extraction_ok and weaviate_ok:
    print("✓ ALL SYSTEMS OPERATIONAL")
    print()
    print("The indexing pipeline has run successfully:")
    print("  1. Discovery found files")
    print("  2. Extraction created artifacts")
    print("  3. Weaviate has indexed data")
    print()
    print("Next steps:")
    print("  - Test web UI: streamlit run src/codeindex/web/app.py")
    print("  - Run search: codeindex search 'your query'")
elif discovery_ok and extraction_ok and not weaviate_ok:
    print("⚠ INDEXING INCOMPLETE")
    print()
    print("Pipeline ran but Weaviate has no artifacts.")
    print()
    print("Action required:")
    print("  1. Check indexing logs:")
    print("     tail -100 data/indexing-$PROJECT_NAME.log")
    print()
    print("  2. Re-run indexing stage:")
    print("     codeindex index --inventory data/discovery-$PROJECT_NAME.jsonl \\")
    print("                     --extraction data/extraction-$PROJECT_NAME.jsonl")
    print()
    print("  3. Verify with:")
    print("     codeindex status")
elif discovery_ok and not extraction_ok:
    print("⚠ EXTRACTION FAILED")
    print()
    print("Discovery succeeded but extraction failed.")
    print()
    print("Action required:")
    print("  1. Check Ollama is running:")
    print("     curl http://localhost:11434/api/tags")
    print()
    print("  2. Re-run extraction:")
    print("     codeindex extract --inventory data/discovery-$PROJECT_NAME.jsonl \\")
    print("                       --output data/extraction-$PROJECT_NAME.jsonl")
else:
    print("✗ PIPELINE FAILED")
    print()
    print("Discovery did not find files or failed completely.")
    print()
    print("Action required:")
    print("  1. Verify source directory:")
    print("     ls -la $SOURCE_DIR")
    print()
    print("  2. Re-run full pipeline:")
    print("     ./fix_indexing.sh $PROJECT_NAME $SOURCE_DIR")
    print()
    print("  3. Check for errors in:")
    print("     - data/discovery-$PROJECT_NAME.jsonl")
    print("     - Pipeline logs")
EOF

echo ""
echo "=============================================="
echo "Done. Check output above for issues."
echo "=============================================="
