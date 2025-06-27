#!/bin/bash

# Check for required arguments
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <directory_with_markdown_files>"
    exit 1
fi

INPUT_DIR="$1"
OUTPUT_DIR="${INPUT_DIR%/}_strictdoc_output"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Process each markdown file
find "$INPUT_DIR" -name "*.md" | while read -r md_file; do
    # Generate output path
    rel_path="${md_file#$INPUT_DIR}"
    rel_path="${rel_path#/}"
    out_subdir="$OUTPUT_DIR/$(dirname "$rel_path")"
    mkdir -p "$out_subdir"

    # Generate output filename (replace .md with .sdoc)
    out_file="${out_subdir}/$(basename "${md_file%.md}.sdoc")"

    # Use StrictDoc to convert the file
    if strictdoc export --input-format markdown --output-dir "$out_subdir" "$md_file"; then
        echo "Converted: $md_file"
        # StrictDoc creates output in its own way; you may need to adjust or move files.
        # For most use cases, the above command is correct.
        # If the output is not as expected, check StrictDoc's --help for options.
    else
        echo "Failed to convert: $md_file"
    fi
done

echo "Conversion complete. Output directory: $OUTPUT_DIR"
