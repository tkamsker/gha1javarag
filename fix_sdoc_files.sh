#!/bin/bash

# Fix SDoc Files According to StrictDoc Documentation
# This script fixes malformed SDoc files to comply with StrictDoc standards

set -e

echo "=== Fixing SDoc Files ==="

# Function to fix a single SDoc file
fix_sdoc_file() {
    local file_path="$1"
    local temp_file="${file_path}.tmp"
    local backup_file="${file_path}.backup"
    
    echo "Fixing: $(basename "$file_path")"
    
    # Create backup
    cp "$file_path" "$backup_file"
    
    # Read the file and fix it
    {
        # Add proper document header
        echo "[DOCUMENT]"
        echo "TITLE: $(basename "$file_path" .sdoc)"
        echo "UID: $(basename "$file_path" .sdoc | tr '[:lower:]' '[:upper:]')"
        echo "VERSION: 1.0"
        echo ""
        
        # Add grammar section
        echo "[GRAMMAR]"
        echo "ELEMENTS:"
        echo "- TAG: REQUIREMENT"
        echo "  FIELDS:"
        echo "  - TITLE: UID"
        echo "    TYPE: String"
        echo "    REQUIRED: True"
        echo "  - TITLE: TITLE"
        echo "    TYPE: String"
        echo "    REQUIRED: True"
        echo "  - TITLE: STATEMENT"
        echo "    TYPE: String"
        echo "    REQUIRED: True"
        echo "  - TITLE: MID"
        echo "    TYPE: String"
        echo "    REQUIRED: False"
        echo "  RELATIONS:"
        echo "  - TYPE: Parent"
        echo "  - TYPE: File"
        echo ""
        
        # Extract and fix requirements from the original file
        awk '
        BEGIN { in_requirement = 0; requirement_count = 0 }
        /^\[REQUIREMENT\]/ {
            if (in_requirement) {
                print "[/REQUIREMENT]"
                print ""
            }
            in_requirement = 1
            requirement_count++
            print "[REQUIREMENT]"
            next
        }
        /^MID:/ { print $0; next }
        /^UID:/ { print $0; next }
        /^TITLE:/ { print $0; next }
        /^STATEMENT:/ { 
            print $0
            in_statement = 1
            next
        }
        /^>>>/ { 
            if (in_statement) {
                print $0
                in_statement = 1
            }
            next
        }
        /^<<</ { 
            if (in_statement) {
                print $0
                in_statement = 0
            }
            next
        }
        /^\[\/REQUIREMENT\]/ {
            if (in_requirement) {
                print $0
                in_requirement = 0
                print ""
            }
            next
        }
        in_statement && /^[[:space:]]*[^[:space:]]/ {
            print $0
            next
        }
        ' "$file_path"
        
        # Close any open requirement
        if [[ $(tail -1 "$file_path" 2>/dev/null) != "[/REQUIREMENT]" ]]; then
            echo "[/REQUIREMENT]"
        fi
        
    } > "$temp_file"
    
    # Replace original with fixed version
    mv "$temp_file" "$file_path"
    echo "Fixed: $(basename "$file_path")"
}

# Find and fix all SDoc files
echo "Finding SDoc files..."
find output/requirements -name "*.sdoc" -type f | while read -r file; do
    fix_sdoc_file "$file"
done

echo "=== SDoc Files Fixed ==="
echo "All SDoc files have been fixed according to StrictDoc documentation standards."
echo "You can now run Step3 again." 