import os
import re
import uuid

def md_to_sdoc(md_file, output_dir):
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title (first heading)
    title = re.search(r'^#\s+(.*)', content, re.MULTILINE)
    title = title.group(1).strip() if title else os.path.splitext(os.path.basename(md_file))[0]

    # Create a very simple, clean content
    # Just use the first few words to avoid any parsing issues
    words = content.split()
    simple_content = ' '.join(words[:20])  # Use only first 20 words
    if len(words) > 20:
        simple_content += "..."

    # Generate MID
    mid = str(uuid.uuid4()).replace('-', '')[:16]

    # Create a minimal, valid StrictDoc document
    sdoc_content = f"""[DOCUMENT]
TITLE: {title}
UID: {os.path.splitext(os.path.basename(md_file))[0]}

[REQUIREMENT]
MID: {mid}
UID: REQ-001
TITLE: Requirements Summary
STATEMENT: {simple_content}
[/REQUIREMENT]

[/DOCUMENT]"""

    # Create output subdirectory structure
    relative_path = os.path.relpath(md_file, input_dir)
    output_subdir = os.path.join(output_dir, os.path.dirname(relative_path))
    os.makedirs(output_subdir, exist_ok=True)

    # Write SDoc file
    output_file = os.path.join(output_subdir, os.path.splitext(os.path.basename(md_file))[0] + '.sdoc')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(sdoc_content)
    
    print(f"Converted: {md_file} -> {output_file}")

# Example usage
input_dir = '/Users/thomaskamsker/Documents/Atom/vron.one/playground/a1javarag/output/requirements'
output_dir = '/Users/thomaskamsker/Documents/Atom/vron.one/playground/a1javarag/output/requirements/nixgut'
os.makedirs(output_dir, exist_ok=True)

# Recursively find all markdown files
for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith('.md'):
            md_file = os.path.join(root, file)
            md_to_sdoc(md_file, output_dir)

