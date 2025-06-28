#!/usr/bin/env bash
# md2strictdoc.sh  —  Convert a tree of Markdown files to StrictDoc
# Usage: ./md2strictdoc.sh <SOURCE_MD_DIR> [STRICTDOC_WORKSPACE_DIR]

set -euo pipefail

# --- 0. Input ---------------------------------------------------------------
SRC_DIR="$(cd "${1:-.}" && pwd)"
WORK_DIR="$(cd "${2:-strictdoc}" && pwd)"

echo "Source MD dir : $SRC_DIR"
echo "StrictDoc dir : $WORK_DIR"
echo "------------------------------------------------------"

# --- 1. Python virtual-env --------------------------------------------------
if [[ ! -d "$WORK_DIR/.venv" ]]; then
  echo "Creating virtual-env in $WORK_DIR/.venv"
  python3 -m venv "$WORK_DIR/.venv"
fi
source "$WORK_DIR/.venv/bin/activate"
pip install --quiet --upgrade pip
pip install --quiet strictdoc==0.9.1 jinja2

# --- 2. Minimal project config ---------------------------------------------
mkdir -p "$WORK_DIR/docs"
cat > "$WORK_DIR/strictdoc.toml" <<'TOML'
[project]
title = "Markdown-to-StrictDoc"
include_doc_paths = [ "docs/**/*.sdoc" ]
TOML

# --- 3. Python converter ----------------------------------------------------
python3 - <<'PY' "$SRC_DIR" "$WORK_DIR/docs"
import sys, uuid, pathlib, re, textwrap
from jinja2 import Template

md_root   = pathlib.Path(sys.argv[1])
sdoc_root = pathlib.Path(sys.argv[2])

TEMPLATE = Template(textwrap.dedent("""
[DOCUMENT]
TITLE: {{ title }}
UID: AUTO-GEN-{{ doc_uid }}

{% for sec in sections -%}
[REQUIREMENT]
MID: {{ sec.mid }}
TITLE: {{ sec.title }}
STATEMENT: >>>
{{ sec.body }}
<<<
[/REQUIREMENT]
{% endfor -%}

[/DOCUMENT]
"""))

for md_file in md_root.rglob('*.md'):
    rel_path = md_file.relative_to(md_root).with_suffix('.sdoc')
    out_file = sdoc_root / rel_path
    out_file.parent.mkdir(parents=True, exist_ok=True)

    title = rel_path.stem.replace('_', ' ').replace('-', ' ').title()
    sections = []
    sec = {"title": title, "body": "", "mid": uuid.uuid4().hex[:16]}

    for line in md_file.read_text(encoding='utf-8').splitlines():
        h = re.match(r'^# (.+)', line)
        if h:
            sections.append(sec)
            sec = {"title": h.group(1).strip(),
                   "body": "",
                   "mid": uuid.uuid4().hex[:16]}
        else:
            sec["body"] += line.rstrip() + "\n"
    sections.append(sec)

    out_file.write_text(
        TEMPLATE.render(title=title,
                        doc_uid=uuid.uuid4().hex[:8],
                        sections=sections),
        encoding='utf-8')
    print(f"✓ {out_file}")
PY

# --- 4. Auto-generate / fix UIDs -------------------------------------------
echo "Running strictdoc manage auto-uid …"
strictdoc manage auto-uid "$WORK_DIR"

echo -e "\n✅ Done!  Generated files live in $WORK_DIR"
echo "Next:  cd $WORK_DIR && strictdoc web   # opens http://localhost:5111"
