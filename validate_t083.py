#!/usr/bin/env python3
"""
T083 Validation: PRD GWT Coverage

Validates that the frontend PRD documents at least 80% of GWT components
(presenters, views, UiBinder forms, and RPC servlets).
"""

import json
from pathlib import Path

# Expected totals from extraction
EXPECTED_PRESENTERS = 40
EXPECTED_VIEWS = 30
EXPECTED_UIBINDERS = 33  # 32 with form fields, 1 without
EXPECTED_RPC_SERVLETS = 16
TOTAL_GWT_ARTIFACTS = 119

# Read frontend PRD
prd_file = Path("output/gwt-validation/prd/frontend_prd.md")
if not prd_file.exists():
    print(f"❌ FAILED: PRD file not found: {prd_file}")
    exit(1)

prd_content = prd_file.read_text()

# Count GWT sections
has_gwt_presenters_section = "## GWT Application Components" in prd_content or "### GWT Presenters" in prd_content
has_gwt_views_section = "### GWT Views" in prd_content

# Count documented forms (UiBinder)
form_count = prd_content.count("**Form Type**: gwt_form")

# Count documented presenters (in presenter details)
presenter_count = prd_content.count("##### ") - prd_content.count("##### View Details") - form_count

# Count documented views (in view table rows)
view_table_start = prd_content.find("### GWT Views")
if view_table_start > 0:
    view_section = prd_content[view_table_start:view_table_start+5000]
    # Count rows in the views table (each view has | at start)
    view_lines = [line for line in view_section.split('\n') if line.startswith('| `')]
    view_count = len(view_lines) - 1  # Subtract header row
else:
    view_count = 0

# Calculate documented artifacts
documented_presenters = min(presenter_count, EXPECTED_PRESENTERS)
documented_views = min(view_count, EXPECTED_VIEWS)
documented_forms = form_count  # 32 forms with fields
total_documented = documented_presenters + documented_views + documented_forms

# Calculate coverage
coverage_pct = (total_documented / TOTAL_GWT_ARTIFACTS) * 100

print("=" * 60)
print("T083 Validation: PRD GWT Coverage")
print("=" * 60)
print()
print(f"Expected GWT Artifacts: {TOTAL_GWT_ARTIFACTS}")
print(f"  - Presenters: {EXPECTED_PRESENTERS}")
print(f"  - Views: {EXPECTED_VIEWS}")
print(f"  - UiBinder Forms: {EXPECTED_UIBINDERS} (32 with fields, 1 template)")
print(f"  - RPC Servlets: {EXPECTED_RPC_SERVLETS}")
print()
print(f"Documented in PRD: {total_documented}")
print(f"  - Presenters: {documented_presenters}/{EXPECTED_PRESENTERS}")
print(f"  - Views: {documented_views}/{EXPECTED_VIEWS}")
print(f"  - UiBinder Forms: {documented_forms}/32 (forms with fields)")
print()
print(f"Coverage: {coverage_pct:.1f}%")
print()

# Verify sections exist
if has_gwt_presenters_section:
    print("✓ GWT Presenters section found")
else:
    print("✗ GWT Presenters section NOT found")

if has_gwt_views_section:
    print("✓ GWT Views section found")
else:
    print("✗ GWT Views section NOT found")

print()

# Pass/Fail
if coverage_pct >= 80.0:
    print(f"✅ PASSED: Coverage {coverage_pct:.1f}% >= 80%")
    exit(0)
else:
    print(f"❌ FAILED: Coverage {coverage_pct:.1f}% < 80%")
    exit(1)
