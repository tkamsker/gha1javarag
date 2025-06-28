#!/usr/bin/env bash
# Usage: ./md2sdoc.sh <md-root> <sdoc-root>
set -euo pipefail

MD_ROOT="$(cd "$1" && pwd)"
SDOC_ROOT="$(cd "$2" && pwd)"
TEMPLATE='
[DOCUMENT]
TITLE: {{ title }}
UID: GENERATED-{{ uuid }}
{% for section in sections -%}
[REQUIREMENT]
MID: {{ section.mid }}
TITLE: {{ section.heading }}
STATEMENT: >>>
{{ section.body | replace("<<<", "\\<<<") }}
<<<
[/REQUIREMENT]
{% endfor -%}
[/DOCUMENT]
'

python3 - <<PY "$MD_ROOT" "$SDOC_ROOT" "$TEMPLATE"
import sys, uuid, pathlib, re, textwrap
from jinja2 import Template

src_root = pathlib.Path(sys.argv[1])
dst_root = pathlib.Path(sys.argv[2])
tpl       = Template(sys.argv[3])

for md in src_root.rglob('*.md'):
    rel   = md.relative_to(src_root)
    title = rel.stem.replace('_', ' ').replace('-', ' ').title()

    # --- very simple Markdown splitter: H1 == requirement
    sections = []
    current  = {"heading": title, "body": "", "mid": uuid.uuid4().hex[:16]}
    for line in md.read_text(encoding='utf-8').splitlines():
        m = re.match(r'^# (.+)', line)
        if m:
            sections.append(current)
            current = {
                "heading": m.group(1).strip(),
                "body":   "",
                "mid":    uuid.uuid4().hex[:16]
            }
        else:
            current["body"] += line.rstrip() + "\n"
    sections.append(current)

    out_path = dst_root / rel.with_suffix('.sdoc')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        tpl.render(title=title,
                   uuid=uuid.uuid4().hex[:8],
                   sections=sections),
        encoding='utf-8'
    )
    print("✓", out_path)
PY

