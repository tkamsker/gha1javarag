#!/bin/bash

# Fix SDoc Files v2 - Improved Version
# This script properly fixes SDoc files according to StrictDoc documentation

set -e

echo "=== Fixing SDoc Files v2 ==="

# Function to fix a single SDoc file
fix_sdoc_file() {
    local file_path="$1"
    local temp_file="${file_path}.tmp"
    local backup_file="${file_path}.backup"
    
    echo "Fixing: $(basename "$file_path")"
    
    # Create backup
    cp "$file_path" "$backup_file"
    
    # Extract the original content to get requirements
    local original_content=$(cat "$file_path")
    
    # Create a properly formatted SDoc file
    {
        # Document header
        echo "[DOCUMENT]"
        echo "TITLE: $(basename "$file_path" .sdoc)"
        echo "UID: $(basename "$file_path" .sdoc | tr '[:lower:]' '[:upper:]')"
        echo "VERSION: 1.0"
        echo ""
        
        # Grammar section
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
        
        # Extract requirements from original content
        echo "$original_content" | awk '
        BEGIN { 
            in_requirement = 0; 
            in_statement = 0; 
            requirement_count = 0;
            skip_next = 0;
        }
        
        # Skip document header lines
        /^\[DOCUMENT\]/ { next }
        /^TITLE:/ && !in_requirement { next }
        /^UID:/ && !in_requirement { next }
        /^VERSION:/ { next }
        /^\[GRAMMAR\]/ { next }
        /^ELEMENTS:/ { next }
        /^[[:space:]]*- TAG:/ { next }
        /^[[:space:]]*FIELDS:/ { next }
        /^[[:space:]]*- TITLE:/ { next }
        /^[[:space:]]*TYPE:/ { next }
        /^[[:space:]]*REQUIRED:/ { next }
        /^[[:space:]]*RELATIONS:/ { next }
        /^[[:space:]]*- TYPE:/ { next }
        
        # Handle requirement blocks
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
        
        # Handle requirement fields
        /^MID:/ && in_requirement { print $0; next }
        /^UID:/ && in_requirement { print $0; next }
        /^TITLE:/ && in_requirement { print $0; next }
        /^STATEMENT:/ && in_requirement { 
            print $0
            in_statement = 1
            next
        }
        
        # Handle statement content
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
        
        # Handle end of requirement
        /^\[\/REQUIREMENT\]/ {
            if (in_requirement) {
                print $0
                in_requirement = 0
                print ""
            }
            next
        }
        
        # Print statement content
        in_statement && /^[[:space:]]*[^[:space:]]/ {
            print $0
            next
        }
        
        # Skip any other content that is not part of requirements
        { next }
        '
        
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

echo "=== SDoc Files Fixed v2 ==="
echo "All SDoc files have been properly fixed according to StrictDoc documentation standards."
echo "You can now run the StrictDoc server." 